"""Typed-choice inference for ModernJEV-Decide-Preview.
The encoder scores each declared (state, candidate) pair; it does not generate text.
"""
import json
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MAX_LEN = 4096
MODEL_ID = "OpenMed/ModernJEV-Decide-Preview"

def serialize_state(state):
    if not isinstance(state, dict):
        raise TypeError("state must be a dict containing conversation and available_tools")
    conv = state.get("conversation") or []
    policy = state.get("policy")
    first = conv[0] if conv else None
    duplicate = (policy is not None and isinstance(first, dict)
                 and first.get("role") == "system" and first.get("content") == policy)
    compact = {"available_tools": state.get("available_tools") or [], "conversation": conv}
    if policy is not None and not duplicate:
        compact["policy"] = policy
    return json.dumps(compact, ensure_ascii=False)

def normalize_criteria(criteria):
    if isinstance(criteria, list):
        if not criteria or any(not isinstance(v, str) or not v.strip() for v in criteria):
            raise ValueError("Answer list must contain nonempty strings")
        if len(set(criteria)) != len(criteria):
            raise ValueError("Answer list must contain unique strings")
        criteria = {v: v for v in criteria}
    if not isinstance(criteria, dict) or not criteria:
        raise ValueError("criteria must be a nonempty mapping or list of unique answer strings")
    if any(not isinstance(k, str) or not k.strip() or not isinstance(v, str)
           for k, v in criteria.items()):
        raise TypeError("Choice labels must be nonempty strings and descriptions must be strings")
    return criteria

class DecisionModel:
    def __init__(self, model_path=MODEL_ID, device=None, revision=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, revision=revision)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path, revision=revision, attn_implementation="sdpa").to(self.device).eval()
        if self.model.config.num_labels != 1:
            raise ValueError("Expected a trained scalar candidate-scoring head")

    @torch.inference_mode()
    def decide(self, *, state, question, criteria, candidate_batch_size=8):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question must be nonempty text")
        criteria = normalize_criteria(criteria)
        if not isinstance(candidate_batch_size, int) or isinstance(candidate_batch_size, bool) or candidate_batch_size < 1:
            raise ValueError("candidate_batch_size must be a positive integer")
        keys = list(criteria)
        text_a = question + "\n\nSTATE:\n" + serialize_state(state)
        text_bs = [f"{k}: {criteria[k]}" for k in keys]
        raw_a_length = len(self.tokenizer(text_a, add_special_tokens=False, verbose=False)["input_ids"])
        special = self.tokenizer.num_special_tokens_to_add(pair=True)
        raw_lengths = [raw_a_length + len(self.tokenizer(t, add_special_tokens=False)["input_ids"]) + special for t in text_bs]
        scores = []
        for begin in range(0, len(keys), candidate_batch_size):
            ts = text_bs[begin:begin + candidate_batch_size]
            encoded = self.tokenizer([text_a] * len(ts), ts, truncation="only_first",
                max_length=MAX_LEN, padding=True, return_tensors="pt", verbose=False).to(self.device)
            with torch.autocast(device_type=self.device.split(":")[0],
                                dtype=torch.bfloat16, enabled=self.device.startswith("cuda")):
                logits = self.model(input_ids=encoded["input_ids"],
                                    attention_mask=encoded["attention_mask"]).logits.squeeze(-1)
            scores.extend(logits.float().cpu().tolist())
        probabilities = torch.softmax(torch.tensor(scores), dim=0).tolist()
        order = sorted(range(len(keys)), key=lambda i: (-scores[i], keys[i]))
        return {"predicted_label": keys[order[0]], "allowed_choices": keys,
            "candidates": [{"label": keys[i], "score": probabilities[i], "raw_score": scores[i],
                            "rank": rank + 1} for rank,i in enumerate(order)],
            "truncated": any(n > MAX_LEN for n in raw_lengths),
            "max_sequence_length": MAX_LEN,
            "note": "Scores rank this supplied choice set; they are not calibrated confidence."}

_default = None
def predict_typed(question_text, state_json, criteria_json):
    global _default
    if _default is None:
        _default = DecisionModel(os.environ.get("MODEL_PATH", MODEL_ID))
    state = json.loads(state_json) if isinstance(state_json, str) else state_json
    criteria = json.loads(criteria_json) if isinstance(criteria_json, str) else criteria_json
    return _default.decide(state=state, question=question_text, criteria=criteria)

def predict_batch(rows):
    return [predict_typed(r["question_text"], r["state_json"], r["criteria_json"]) for r in rows]

