# Evaluation Protocol

Freeze this record before candidate comparison. A changed protocol needs a new identity and an
explicit account of which prior results remain comparable. Do not place raw personal data here.

## Study Identity

- Protocol ID and revision: [TODO]
- Decision, intended use and prohibited use: [TODO]
- Owners and review/approval requirements: [TODO]
- Prediction instant, observation unit and deployment population: [TODO]
- Evaluation dataset ID, snapshot/cut-off and target construction: [TODO]
- Data exclusions, missing labels and label-maturity rules: [TODO]
- Split ID, train/validation/test boundaries, grouping and temporal gaps: [TODO]
- Data access, consent/licensing, retention and egress constraints: [TODO]

## Comparison Contract

| Item | Predeclared decision |
| --- | --- |
| Trivial and current-system baselines | [TODO] |
| Candidate family and search space | [TODO] |
| Search budget, seeds, folds and stopping rule | [TODO] |
| Primary metric, unit, direction and aggregation | [TODO] |
| Absolute threshold and meaningful improvement | [TODO] |
| Secondary metrics and hard guardrails | [TODO] |
| Threshold/calibration/checkpoint selection | [TODO] |
| Tie-breaking and multi-objective trade-off | [TODO] |
| Refit policy before final testing | [TODO] |
| Final test access and reuse restrictions | [TODO] |

## Uncertainty and Coverage

- Confidence interval/comparison method and independent sampling unit: [TODO]
- Repeated-seed variability and multiple-comparison handling: [TODO]
- Required slices, minimum counts and insufficient-evidence rule: [TODO]
- Prediction/scorer error denominator, exclusions and timeout treatment: [TODO]
- Calibration, error analysis and domain/fairness review: [TODO]
- Latency, throughput, memory, cost and reliability measurement conditions: [TODO]

## GenAI Extension

Use `Not applicable` for non-GenAI work.

- Application/prompt, provider/model, retrieval corpus/index and tool versions: [TODO]
- Task/reference dataset, expected outputs and acceptable alternatives: [TODO]
- Deterministic scorers, judge versions/rubric and human calibration set: [TODO]
- Trace collection/redaction, permitted providers and cost ceiling: [TODO]
- Retrieval/tool correctness, groundedness, task success and safety cases: [TODO]
- Repeated-run policy, judge errors/disagreement and assessment coverage rule: [TODO]

## Evidence and Decision

- Immutable candidate/baseline model IDs and run IDs: [TODO]
- Observed metrics, uncertainty, slice counts and failure rates: [TODO]
- Policy revision and scalar-gate outcome: [TODO]
- Deviations from the frozen protocol and impact: [TODO]
- Decision: pass / fail / insufficient evidence: [TODO]
- Authorised next action and approving owner: [TODO]

Store machine-readable comparisons using [evaluation-evidence.template.json](evaluation-evidence.template.json).
The [example policy](metric-policy.example.json) is illustrative; derive thresholds from this protocol.
