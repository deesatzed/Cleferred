# Train your own small agent decision model with HuggingChat

Open https://huggingface.co/chat/, enable **ML Intern**, replace the three settings below, and paste the prompt. Start without granting compute. After reviewing the proposal, grant the stated budget to authorize the pilot and bounded prototype. Builders need their own Hugging Face compute credits and permission to write the destination model repository.

**Check both billing accounts:** select the intended user or organization inside HuggingChat before using the coding model, and pass that namespace on every Hugging Face Job. A Job's organization does not automatically change the account charged for chat-model tokens.

```text
NAMESPACE = <your HF username or organization>
MODEL_REPO = <NAMESPACE>/ModernJEV-Decide-Preview
TRAINING_DECISIONS_TARGET = 60000
MAX_SEQUENCE_LENGTH = 4096
TOTAL_COMPUTE_BUDGET_USD = 10

Help me train a small open decision model from
MaziyarPanahi/AgentToolDecisions-180K using HuggingChat ML Intern.
Do a read-only preflight first, show your executable plan and budget,
then STOP for my explicit authorization before any compute job,
sandbox, repository creation, training or Hub write.
Use read-only Hub metadata and dataset previews for that preflight.
Any executable dataset audit, model-load or GPU check belongs in the
approved pilot; do not provision compute to satisfy a zero-spend step.

The model should read an agent's state, a question, and the allowed
choices, then return one of those choices. It is a Jev-style choice
scorer, not a reproduction of Jev and not a chatbot.

DATA
Pin dataset revision f2fb14e4ec977c420f376c08785664cd38763d7e.
Keep the published train/validation/test splits; never resplit.
Train ONLY agent_next_action_type and tool_selection.
Their combined train/validation/test counts are 112973/1798/1700.
Inspect actual rows, label balance and input lengths before training.
Exclude the single-label tool_or_text_action,
tool_argument_completeness and tool_response_preference families,
and exclude the test-only when_to_call_tool family from training.
After freezing the final checkpoint, evaluate all 3,652 When2Call
test rows separately as unseen-task transfer, without tuning on them.
Report only per-task scores, never overall or macro accuracy.
Reverify constant-majority references: 616/1158 next-action,
79/542 tool-selection, and 1295/3652 When2Call. Distinguish these
from the stronger allowed-choice training-frequency baseline.
When2Call majority is a descriptive test-set reference, not fitted.
Next-action has three declared choices but only two gold labels;
tool_and_response is never gold. Do not imply three-class coverage.
Assert no group_id crosses splits. For source-row leakage, use the
full tuple (source_dataset, source_revision, source_config,
source_split, source_row_id), never bare source_row_id.

MODEL AND LOSS
Start with answerdotai/ModernBERT-base at revision
8949b909ec900327062f0ebf497f51aef5e6f0c8.
Use AutoModelForSequenceClassification(num_labels=1,
attn_implementation='sdpa'). Score each (question + state,
candidate label + criterion) pair. Apply softmax cross-entropy
within each decision's row_id; group_id is an episode, NOT the
loss grouping key. Score only the row's declared choices.
Support arbitrary caller-supplied labels and unique answer-string lists;
test 2/3/7/20 choices, reordered candidates and renamed labels.
Report API acceptance separately from semantic correctness.
Do not feed gold labels, gold JSON, gold scores or provenance into
model inputs. Do not include candidate indices in candidate text.
Verify trainer and dependency APIs against installed versions.
In Transformers 5.17, use warmup_steps=0.03 for 3% warmup;
warmup_ratio was removed. Instantiate the complete production
TrainingArguments branch before any expensive data preparation.
Test the full trainer/validation/checkpoint path locally on a tiny
subset, not only the separate pilot branch.
Prefer lazy batch tokenization with prefetching so optimizer steps
begin without an upfront full-dataset mapping pass.
Do not substitute a different ranking objective without approval.
For long 4096-token inputs, benchmark ModernBERT's documented
FlashAttention backend as well as SDPA. Match the installed Torch/CUDA
ABI to an available prebuilt kernel; do not assume the newest Torch
release has a matching kernel. Pin and record the kernel revision. For the verified environment in this
run: torch 2.12.0 + cu126, transformers 5.17.0, kernels 0.16.0;
Transformers 5.17 rejects kernels 0.17.x. The pinned FlashAttention
revision is f50dc99ed079b35990bc895d43fd353ea0cb376d.
Inspect the kernel repository type used by the installed loader. The
model repository and kernel repository may have different revisions.
Before data loading, run a small CUDA forward/backward kernel smoke.
Datasets 5 columns are lazy: bulk-materialize metadata and NumPy arrays
before numerical comparisons or sorting. Tokenize only sampled training
candidates if using a sampled pool; evaluation must rank all candidates.
Verify checkpoint parameter equality and compare predictions at the
same precision. Do not compare a Trainer BF16-wrapped forward to FP32
inference with an unrealistically strict tolerance.

INPUTS
The audited 192-row sample had 2221 candidate pairs: full-input
p50 2460 tokens, p95 3935, max 5179. At 2048, 1643 pairs truncate.
Start the pilot at 4096 tokens. Preserve question and candidate;
document any state truncation and measure its frequency. Remove
duplicated policy only when exactly equal to the first system
message. Batch by candidate count/token cost and measure GPU
memory. Never claim all input was read when it was truncated.

RUN
Pass NAMESPACE on EVERY job so billing uses the intended account.
Check current hardware price and private Hub write permissions.
If write access is missing, ask me to reconnect with the appropriate
repository permissions; never request a token pasted into the chat.
Use one A100 80GB (a100-large) if available at $2.50/hour:
first a 25-step pilot with a 20-minute timeout, then at most one
prototype job with a 165-minute timeout. Set a total $10 compute budget.
Select exactly TRAINING_DECISIONS_TARGET rows from the training split,
stratified by task family with seed 42; freeze and hash their row IDs.
Use measured pilot throughput to check whether one complete epoch fits,
leaving time for validation, final evaluation and upload.
Record the actual rows, steps, elapsed time and cost. No guarantee
of a full epoch, no parallel jobs, no automatic retries or extensions.
If the pilot makes the deadline infeasible, stop and report it.

Create a NEW PRIVATE model repository only after authorization.
Save checkpoints, tokenizer, input template, prediction code,
dependency pins, metrics and a model card there. Do not overwrite
an existing repository. Persist the pilot before its job exits.
Never create a Hugging Face Space or change any Space visibility.
Use local JSONL metrics; optionally use Trackio only after verifying
space_id=None performs local logging without creating a Space.
Never call create_trackio or provision a dashboard Space.
Never paste tokens into chat, code, logs or artifacts; use secrets.

EVALUATION AND DELIVERY
Use a fixed one-epoch recipe and its final checkpoint for the first
prototype; monitor validation without selecting on the test set.
If the time limit stops training early, disclose the actual row coverage.
Evaluate the final checkpoint
once on the 1700 in-scope official test decisions, per family.
Compare with uniform-choice and training-derived majority/frequency
baselines restricted to the declared candidates. Check shuffled
candidate order and report label agreement, with a stated tie rule.
Return typed-choice prediction code and a reproducible recipe.
Preserve source attribution and inspect licenses before release.
Report failures and unmeasured results honestly. Do not claim Jev
parity, general agent competence or support for other primitives.
Keep weights private until I separately authorize publication.
```
