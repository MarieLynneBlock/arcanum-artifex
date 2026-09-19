# Evaluation and Model Selection

Use this guide when selecting a candidate, auditing leakage, building regression checks, or deciding
whether evidence supports release. Complete the [evaluation protocol](../assets/evaluation-protocol.md)
before running a search. MLflow records and evaluates results; it does not choose a valid study design.

## Match the Split to Deployment

| Data-generating situation | Evaluation design | Frequent invalid shortcut |
| --- | --- | --- |
| Independent observations | Stratified split for classification when appropriate | Fitting scalers, imputers, or selectors before splitting |
| Repeated customers/patients/devices | Entity-disjoint groups; respect time within entities | Same entity appearing in training and test |
| Forecasting | Rolling/expanding backtests; explicit horizon and gap | Random split or features unavailable at forecast time |
| Delayed outcomes | Time cut-off that respects label maturity | Using recently collected, incomplete labels as negatives |
| Spatial dependence | Geographic blocking appropriate to intended transfer | Nearby observations leaking across nominally separate sets |
| Small datasets and tuning | Nested cross-validation where feasible | Reporting the tuning CV maximum as unbiased generalisation |
| Ranking/recommendation | Query/user grouping and chronological availability | Random interactions from the same query in both sets |
| GenAI/RAG/agents | Versioned tasks, independent challenge set, human calibration | Prompt tuning on the final benchmark |

No split design repairs a target defined using future information. Specify the prediction instant,
observation unit, label window, exclusions, and feature availability first. For causal claims,
uplift, or policy effects, obtain a defensible identification strategy; predictive accuracy alone
does not establish treatment benefit.

## Metric Families and Baselines

| Task | Candidate measures | Required interpretation |
| --- | --- | --- |
| Binary classification | PR-AUC, ROC-AUC, log loss, calibration, recall at fixed precision | Positive class, prevalence, threshold and operating cost |
| Multiclass classification | Log loss, macro/weighted F1, per-class recall | Class ordering, averaging method, rare-class counts |
| Regression | MAE, RMSE, quantile loss, interval coverage | Units, outliers, asymmetric cost, segment distribution |
| Forecasting | Horizon-wise error, scaled error, coverage, bias | Seasonal-naive baseline, cut-offs, zero denominators |
| Ranking | NDCG/recall at k, coverage, relevance judgements | Query weighting, candidate set, logged-policy bias |
| Clustering/anomaly detection | Stability, reviewed precision, alert burden, external labels | Proxy limitations; silhouette alone is not business value |
| GenAI | Task success, groundedness, retrieval quality, tool success, safety, cost | Judge error, failure coverage, repeated-run variance |

Use a trivial baseline and, when available, the current approved system. Evaluate baselines on the
same rows and protocol as candidates. State when the production baseline cannot be reproduced;
do not quietly substitute a weaker reference. Predeclare tie-breaking, meaningful improvement,
and latency/memory/cost limits.

## Selection Protocol

1. Freeze dataset version, split identity, metric definitions, budget, and search space.
2. Fit all learned preprocessing inside the training pipeline or each CV fold. This includes
   resampling, encoders, feature selection, calibration, and target-dependent transforms.
3. Tune hyperparameters, thresholds, and checkpoint choice on validation evidence only.
4. Record every attempted trial, including failures and resource limits. Inspect uncertainty,
   slices, calibration and operational constraints, not just the top scalar.
5. Freeze the selected configuration. Refit on allowed development data if the protocol calls for
   it. Preserve the selected trial ID and document the change in training population.
6. Evaluate once on the agreed final holdout. A failed final test is not permission to tune on it;
   revise the study and obtain new independent evidence where needed.

The [classical example](../examples/classical_ml.py) follows this sequence with a tiny IID dataset.
Its single split, three logistic-regression candidates and fixed 0.5 threshold are demonstrations,
not recommendations for every domain. It returns probabilities with class ordering recorded.

## Uncertainty and Error Analysis

- Use paired comparisons on common observations. Bootstrap at the independent unit: entity,
  query, time block, or other justified cluster, not automatically individual rows.
- Separate sampling uncertainty from seed/training variability. Repeated seeds on the same test
  data do not create independent test sets. Account for search and repeated testing when interpreting
  confidence intervals and significance.
- Report denominators, exclusions, missing predictions, timeouts and failed scorers. A mean over
  successful requests can hide a production-breaking failure rate.
- Predeclare subgroup definitions and minimum sample sizes. Small slices should be marked as
  insufficient evidence, not declared equivalent because a test is non-significant.
- Inspect calibration, threshold stability, residuals/confusion matrices, and representative errors.
  Apply disclosure controls to tables and plots; evaluation artefacts can contain row-level data.
- For sensitive or regulated decisions, include domain, fairness, privacy and governance review.
  No universal fairness metric or scalar quality threshold replaces this review.

## MLflow Evaluation APIs

For compatible classical models, `mlflow.evaluate` can produce metrics and artefacts from labelled
data. Choose `model_type`, target, positive class, evaluator configuration, and prediction contract
explicitly. A pyfunc probability matrix is not automatically equivalent to a native sklearn
classifier for every evaluator; verify which metrics were actually produced.

Disable optional explainability with `evaluator_config={"log_model_explainability": False}` when
it is outside scope. Where explainability is required, record the method, background population,
cost and limitations. An explanation does not prove causality or eliminate data leakage.

Use `mlflow.validate_evaluation_results` for scalar thresholds; the bundled
[metric comparator](../scripts/compare_metrics.py) wraps that API with evidence checks.

## Local Metric Gate

1. Adapt [metric-policy.example.json](../assets/metric-policy.example.json). Its numbers are
   illustrative, not default acceptance criteria. Set metric names, direction, absolute threshold,
   and optional minimum absolute/relative improvement before seeing candidate results.
2. Populate [evaluation-evidence.template.json](../assets/evaluation-evidence.template.json) from
   the actual candidate and baseline evaluations. Use identical protocol, dataset, split and phase
   identifiers only when that is genuinely true. Include immutable run and model identifiers.
3. From the skill folder, use the consuming project's interpreter with a compatible MLflow
  installation, as described in the [reference examples](../examples/README.md):

```text
python scripts/compare_metrics.py --evidence evidence.json --policy policy.json
```

Here `python` must resolve to that interpreter; the skill does not create an environment or install
dependencies.

`evidence.json` and `policy.json` above are project-owned copies, not bundled inputs to invent or
overwrite. The command reads local JSON only and never registers, promotes, or deploys a model.
Exit codes: `0` scalar checks passed; `1` quality threshold failed and nothing else; `2` invalid
evidence or policy, an unavailable dependency, or another failure to run the check. Treat `2` as
no verdict, never as a pass or a regression.

Both records must declare the same `protocol_id`, `evaluation_dataset_id`, `split_id`, and `phase`.
`phase` must be exactly `validation` or `final-test`; any remaining `[TODO]` value is rejected.

The comparator requires finite numeric candidate and baseline values for every policy metric,
rejects mismatched identities, and requires a positive baseline for relative improvement. The policy
key `higher_is_better` maps to MLflow's `greater_is_better` argument. Unknown rule keys fail validation.
Missing data does not become zero. Empty policies cannot pass.

The gate trusts the supplied identity labels; it does not verify their provenance, calculate
confidence intervals, validate slice coverage, or check approval. Use it as one CI check, not a
release authorisation service. Preserve the raw evaluation evidence and policy revision alongside
its outcome in the [release record](../assets/release-record.md).

Sources: [MLflow evaluation and validation API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html),
[model evaluation types](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.models.html).
