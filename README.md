---
license: apache-2.0
library_name: transformers
pipeline_tag: text-classification
base_model: answerdotai/ModernBERT-base
base_model_relation: finetune
datasets:
  - MaziyarPanahi/AgentToolDecisions-180K
tags:
  - modernbert
  - encoder
  - decision-model
  - tool-routing
  - agentic
  - preview
language:
  - en
---

<div align="center">

# ModernJEV-Decide-Preview

### Give your agent a next move.

**A small encoder for choosing an action or a tool from the options you provide.** We trained this 60,000-decision prototype for **about $6.60 in A100 compute, including setup and evaluation**. The training phase itself accounted for **about $5.40**. Both figures are estimates from the measured runtime.

149.6M parameters · 4,096-token inputs · Typed choices · Built on ModernBERT

</div>

> **Experimental preview.** The final checkpoint processed **60,000/60,000 selected training decisions**. Held-out results cover **1,158 next-action**, **542 tool-selection**, and **3,652 unseen When2Call** decisions, reported separately. This is a small choice-ranking prototype, not a Jev reproduction.

An agent doesn't need to write a paragraph every time it makes a decision. Sometimes the useful output is simply **answer**, **call a tool**, or **choose this tool**.

ModernJEV-Decide-Preview reads a conversation, its policy and available tools, then scores the choices supplied with your question. Your application receives one of those labels, along with the scores for the alternatives. The model ranks choices; your application executes the selected action.

The architecture is a **ModernBERT cross-encoder with one scalar scoring head**. Choice labels and descriptions are input text, so the output is not limited to a fixed vocabulary of tool names. This is a Jev-style choice model built from public agent decisions, with its own training and evaluation; it is not a reproduction of Jev.

![How decisions are scored](architecture.svg)

## Where it fits

| Use case | Supply | Receive |
|---|---|---|
| **Next-action routing** | Current conversation, policy, tool list | A declared action such as `text_response` or `tool_call` |
| **Tool selection** | The task and each available tool's purpose | The label of the selected tool |
| **Workflow branching** | A text state and clearly described alternatives | One branch label; evaluate on your own workflow before adoption |
| **Decision-model experiments** | Your choices and held-out tasks | Candidate rankings you can inspect and compare |

Useful places to start: support agents choosing between lookup and escalation, assistants selecting an API, and workflows choosing between a direct answer and a tool-backed step. The model does not generate tool arguments or execute tools.

## Train a decision model with HuggingChat ML Intern

We tested this workflow with **one execution message, an attached tested recipe, and a budget setup click**. In a fresh HuggingChat conversation, ML Intern prepared the code, ran its own checks, launched an OpenMed A100 job, trained **6,000 decisions in 1,500 optimizer steps**, and uploaded a new private checkpoint. No follow-up implementation prompt, Codex code repair or Codex job launch was needed in that conversation. Training took **996.9 seconds (16 minutes 37 seconds)**; that excludes chat preparation, setup and subsequent evaluation.

**These are two separate runs:**

| | Weights in this repository | ML Intern recipe replay |
|---|---|---|
| Selected training decisions | 60,000 | 6,000 |
| Optimizer steps | 3,720 | 1,500 |
| Execution | Started with ML Intern; Codex debugged, launched and completed the run | ML Intern executed from one message with supplied source files |
| Evidence | Per-task model results below | Exact row coverage and checkpoint upload independently verified |
| Status at this documentation revision | Training and evaluation complete | Training and fresh checkpoint verified; operator stopped after workflow proof |

The first replay attempt stopped **before GPU spend** because HuggingChat's tools could not read the existing private source repository, although the local HF login could. We preserved that failed attempt and opened a fresh conversation with the source files attached. The successful training therefore demonstrates **one-prompt execution of a supplied recipe after setup**, not first-attempt success, code invention from scratch, or a guarantee for arbitrary training tasks. ML Intern made its own pre-launch code corrections. After the first GPU run had trained and verified checkpoint reload, its finalizer failed because stdin execution did not define `__file__`. It detected that failure and a reversed When2Call baseline unpack itself, then used the authorized corrective retry. The retry also trained all 6,000 rows and saved a checkpoint. The operator then stopped the remaining evaluations and CPU sandbox because the requested workflow proof was already established. Full replay packaging was not completed. These autonomous repairs, failed compute and the operator termination are part of the recorded run.

### Try the same workflow

1. Open [HuggingChat](https://huggingface.co/chat/) and enable **ML Intern**. Our replay used **GLM-5.3-Flash**.
2. Select your intended billing account or organization in HuggingChat settings. Ensure you can create/write a private model repository and submit Jobs in that namespace.
3. Download [the execution prompt](workflow/PROMPT-R2.txt) and [the tested source bundle](workflow/recipe-bundle.txt). Change the billing namespace and destination to your own **new private model repository** throughout the prompt. Keep the pinned source revisions. Do not reuse our destination name.
4. Attach both files to one message and send the instruction below. Set the conversation's compute-budget control to **$10**; the written budget alone does not replace that UI setting.
5. Let ML Intern do its checks, execution and monitoring. A submitted job is not proof of a trained model: check row coverage, saved weights, reload, costs and per-task evaluations.

This was the actual execution message accompanying our attachments:

```text
Execute PROMPT-R2.txt now in ML Intern using the supplied recipe-bundle.txt.
OpenMed is the billing namespace. This single message authorizes the bounded
experiment described in the prompt. The earlier attempt stopped before compute
because the private source lookup failed; use these supplied source files,
and preserve that fact in the final report.
```

For your run, replace `OpenMed` in that message with your billing namespace as well. The full attached prompt is part of the instruction, not optional background. It specifies the 6,000-row selection, 4,096-token inputs, rehearsal, privacy, one A100, timeout, total compute cap, at most one bounded retry, and per-task evaluation requirements. Do not claim our measured runtime or results for a new run before measuring them.

[Exact prompt](workflow/PROMPT-R2.txt) · [Source bundle and hashes](workflow/recipe-manifest.json) · [Run provenance](workflow/ONE-PROMPT-REPLAY.md) · [Replay job](https://huggingface.co/jobs/OpenMed/6abe2b6ffbc85ba6823612cc)

## Quick start

Install PyTorch and Transformers, then use the included inference helper so the input formatting matches training:

```bash
pip install "torch==2.12.0" "transformers==5.17.0" "huggingface-hub==1.33.0"
```

Download the supplied helper, then run it alongside your application. During the private preview, your Hugging Face account must have access to the repository.

```bash
hf download MaziyarPanahi/ModernJEV-Decide-Preview predict.py --local-dir modernjev
cd modernjev
```

The included helper was executed against this checkpoint. See [the observed example output](example-output.json); the snippet below prints the actual prediction rather than promising a fixed answer.

```python
from predict import DecisionModel

model = DecisionModel("MaziyarPanahi/ModernJEV-Decide-Preview")
decision = model.decide(
    state={
        "policy": "Use the order lookup tool when a customer asks about an order.",
        "conversation": [
            {"role": "user", "content": "Where is order A123?"}
        ],
        "available_tools": [
            {"name": "lookup_order", "description": "Retrieve an order's delivery status."},
            {"name": "search_catalog", "description": "Find products in the catalog."},
        ],
    },
    question="Which tool should the assistant call next?",
    criteria={
        "lookup_order": "Retrieve the delivery status of the customer's order.",
        "search_catalog": "Search for products that match a shopping request.",
    },
)
print(decision["predicted_label"])
print(decision["candidates"])
```

You can also supply `criteria=["Escalate to a human", "Search the product catalog"]` when each answer is its own description. The result contains the selected label, all candidate scores, and whether input truncation occurred. Scores are normalized **within the supplied choice set**; they are not calibrated confidence estimates and cannot be compared directly across unrelated requests.

## Training recipe

| Setting | Recorded configuration |
|---|---|
| Base | `answerdotai/ModernBERT-base` |
| Base revision | `8949b909ec900327062f0ebf497f51aef5e6f0c8` |
| Parameters with scalar head | 149,605,633 |
| Input limit | 4,096 tokens including both sequences and special tokens |
| Dataset | `MaziyarPanahi/AgentToolDecisions-180K` |
| Dataset revision | `f2fb14e4ec977c420f376c08785664cd38763d7e` |
| Selected training target | Exactly 60,000 train-split decisions, stratified by family, seed 42 |
| Actual training coverage | 60,000 decisions; 3,720 optimizer steps |
| Attention backend | kernels-community/flash-attn2@f50dc99ed079b35990bc895d43fd353ea0cb376d |
| Training elapsed | 129.8 minutes |
| GPU | NVIDIA A100-SXM4-80GB |
| Task families | `agent_next_action_type`, `tool_selection` |
| Objective | Per-decision softmax cross-entropy over candidate scores |
| Candidate grouping | `row_id`, preserving `group_id` only for episode/split boundaries |
| Candidate pool | Gold plus up to three declared negatives per training decision; evaluation ranks every declared choice |
| Evaluation | Monitor official validation; evaluate the final fixed-epoch checkpoint on 1,700 in-scope official test decisions |

The dataset has 180,000 total rows. This prototype targets 60,000 of its 112,973 in-scope training decisions; **180,000 is not the number used for training**. Exact selected row IDs, coverage, steps and dependency versions accompany this checkpoint. This repository contains model artifacts; it does not expose an inference endpoint.

## Evaluation

Every task is reported separately. The checkpoint was fixed after one pass over the selected training rows; no When2Call labels were used for training, checkpoint selection or hyperparameter tuning. The three single-label task families are excluded from quality claims.

| Task | Correct / cases | Model accuracy | Constant-majority reference | Lift |
|---|---:|---:|---:|---:|
| Next action | 850 / 1,158 | 73.40% | 53.20% | +20.21 pp |
| Tool selection | 337 / 542 | 62.18% | 14.58% | +47.60 pp |
| When2Call — unseen task family | 1,256 / 3,652 | 34.39% | 35.46% | -1.07 pp |

**Transfer limitation:** When2Call is below its majority reference. Accepting a new question and new answer labels does not establish that the model understands that task reliably. This preview demonstrates gains on its trained task families; general decision-making and clinical use remain unvalidated.

The next-action majority label is `text_response`; the tool-selection majority label is `transfer_to_human_agent`. Both are also the most frequent labels in the selected training subset. The fixed tool label is absent from 235 of the 542 choice lists, so it is a descriptive constant-label reference, not a valid per-row router. When2Call has no training rows: its reference is the test-set majority (a tie between `cannot_answer` and `tool_call`), not a fitted training baseline.

The stronger **allowed-choice training-frequency baseline** always chooses among the supplied answers. It is distinct from the constant-majority reference above.

| Comparison | Next action (1,158 cases) | Tool selection (542 cases) |
|---|---:|---:|
| ModernJEV-Decide-Preview | 73.40% | 62.18% |
| ModernBERT + untrained scalar head, seed 42 | 42.83% | 0.74% |
| Allowed-choice training-frequency baseline | 53.20% | 22.88% |
| Uniform over supplied choices, expected accuracy | 33.33% | 5.19% |

Next-action rows have three choices. Tool-selection rows have a median of 20 choices (range 11–32). When2Call rows have four choices; uniform expected accuracy is 25%. Evaluation ranks all declared candidates, including choices not sampled during training.

Untrained ModernBERT is a pretrained encoder with a randomly initialized scalar head, not a trained decision classifier. No frozen-backbone trained-head comparison or Jev API comparison was completed in this bounded run.

### Open answer labels

The helper accepts arbitrary string labels with descriptions, or a list of unique answer strings. It has no fixed output-class vocabulary. Final-checkpoint interface checks passed with 2, 3, 7 and 20 supplied answers, including reversed order and fresh opaque labels. These are interface checks, not a broad capability benchmark.

For one illustrative routing scenario at four answer-list sizes, the intended description was selected at 2, 3 and 7 choices, but not at 20. Renaming labels while retaining descriptions changed the selected description in the 3- and 7-choice variants. **Label wording matters:** use descriptive labels and validate your own question/answer sets. The small illustrative checks are published in full, including the misses.

Candidate-order label agreement on the official test subset was **100% across five permutations of 299 decisions**. Reordering a fixed set of label strings is a different test from renaming those strings. Ties use lexical label order.

GPU latency for **one candidate forward pass**, excluding tokenization: median **23.6 ms**, p95 **24.2 ms**. A full decision scores multiple candidates; these are not end-to-end decision timings. The two trained tasks were evaluated with GPU BF16 inference. Supplemental When2Call and open-label checks used local CPU FP32 inference on the same saved weights.

See [per-task results](per-task-results.json), [all When2Call predictions](evaluation/when2call-predictions.jsonl), [open-label checks](evaluation/open-label-checks.json), [baseline definitions](evaluation/per-task-baselines.json), [training coverage](training_coverage.json), [runtime versions](runtime-versions.json) and [the pinned training recipe](recipe/train.py). The split audit found no cross-split episode or full upstream source conflicts. The 4,096-token limit truncated 414 candidate pairs in the two trained task tests; no When2Call rows were truncated.

### Compute accounting

**For a successful run of the 60k recipe, allow about $6.60 in GPU compute at our measured runtime.** We used one A100 80GB at the published [Hugging Face Jobs rate of $2.50/hour](https://huggingface.co/docs/hub/jobs-pricing).

| Scope | Measured time | Estimated GPU compute |
|---|---:|---:|
| Training phase: 60,000 decisions, 3,720 optimizer steps | 129.8 minutes | **$5.41** |
| Full successful job: setup, training, evaluation and packaging | 157 minutes | **$6.58**, conservatively rounded; about **$6.60** |
| Earlier development attempts and pilots | Across multiple jobs | **$2.21** |
| Original development total, including the successful job | Across all original jobs | **$8.79** |

The **$8.79** figure includes our earlier failed attempts and pilots; it is not the cost of the final successful run. The $10 authorization was a spending cap, not a quoted training price. These figures refer to the original **60k checkpoint in this repository**, separately from the later 6k ML Intern workflow test.

Costs are runtime/rate estimates, not reconciled invoice amounts. They exclude HuggingChat inference, local CPU work and operator time; another run's runtime may differ. See [cost accounting](COST-AUDIT.json) for the job-level receipts and training-phase calculation.

## Input design matters

- Give every choice a concrete, distinct description. Include the same available tool information the application actually has.
- Use the supplied serialization helper. Long state may need truncation at the 4,096-token limit; the helper reports it.
- The training data is English agent conversations and tool decisions. New domains and arbitrary workflow labels need their own evaluation.
- `tool_and_response` is a declared next-action choice but never a gold label in this dataset. That action is outside demonstrated positive training coverage.
- This preview implements **choice ranking**. It does not implement Jev's other primitives, vision inputs, generated explanations, or autonomous tool execution.

## Reproduce the 60k model or the 6k workflow

Use [the original 60k training recipe](recipe/train.py) and [its detailed training prompt](PUBLIC-PROMPT.md) to inspect how these weights were built. Use the **6k ML Intern replay instructions above** to test the one-message execution workflow. Their scope, checkpoints, runtimes and metrics are different. All model-quality results on this page belong to the original 60k checkpoint.

## Attribution

Base model: [Answer.AI ModernBERT](https://huggingface.co/answerdotai/ModernBERT-base), Apache 2.0.

Decision dataset: [MaziyarPanahi/AgentToolDecisions-180K](https://huggingface.co/datasets/MaziyarPanahi/AgentToolDecisions-180K), transformed from the upstream agentic sources documented in its card. Keep the pinned revisions and source attribution with derivative work, and follow the upstream dataset licenses when redistributing data.

**Original 60k workflow:** HuggingChat ML Intern prepared the proposal, training code, helper and model-card draft. Codex audited the data and corrected candidate targets, padding budgets, coverage accounting and checkpoint verification. Hugging Face Jobs was launched with the operator's approved local HF credential after the connector's write permissions returned 403. This is an assisted training workflow; HuggingChat did not autonomously execute the training job.
