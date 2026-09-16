# Tracking and Reproducibility

Use this guide when instrumenting a project, designing an experiment hierarchy, or investigating
why a result cannot be reproduced. Start with the [project contract](../assets/project-contract.md).

## Choose the Smallest Useful Integration

| Situation | Default | Verify before extending |
| --- | --- | --- |
| One local experiment | Explicit local SQLite backend and local artefacts | Repeatable run and model reload |
| Existing training service | Existing tracking endpoint, explicit experiment and run ownership | Identity, storage mode, retries, failure policy |
| Parameter search | Parent for the search; child for each trial | Trial failures retained, shared protocol, validation-only selection |
| Cross-validation | Trial summary plus fold evidence | Preprocessing refitted per fold, correct aggregation |
| Distributed training | Coordinator owns aggregate metrics and final model | Worker/rank identity and checkpoint ownership |
| Notebook investigation | Explicit context-managed runs | Rerunning a cell cannot attach to an unintended active run |

MLflow is a record of execution, not the scheduler or data versioning system. Reuse the project's
orchestrator and data catalogue. Experiment names should group comparable work, not create a new
experiment for every parameter combination.

## Evidence Contract

Keep searchable facts small; put structured details in approved artefacts. These are suggested
project conventions, not reserved MLflow fields.

| Surface | Suggested contents | Avoid |
| --- | --- | --- |
| Tags | Project, task, owner/team, protocol ID, phase, parent decision | Raw identifiers, secrets, unbounded JSON |
| Parameters | Hyperparameters, seed, feature-set version, window sizes | Changing one parameter's value inside the same run |
| Metrics | Numeric value, meaningful unit, monotonic step for a series | Mixing percentages and fractions or different populations |
| Dataset inputs | Approved source/version, digest, target, context | Treating a digest as a dataset snapshot |
| Artefacts | Lock, sanitised configuration, evaluation tables, plots, manifests | Environment dumps, raw production extracts, credentials |
| Model package | Signature, safe input example, dependencies, preprocessing | A notebook's hidden state or absolute developer paths |

For code provenance, record the commit and dirty-state status. A commit hash does not identify
uncommitted code. Preserve an approved patch or source snapshot where policy permits; otherwise
state that exact reconstruction is unavailable. Record the executable command, working directory
assumptions, Python/R versions, OS/architecture, framework, and container digest when relevant.

For data provenance, record snapshot or object version, extraction/query revision, filters,
event/ingestion time cut-offs, schema, target construction, feature availability, and split identity.
Hashing personal identifiers does not necessarily anonymise them. Prefer approved catalogue IDs;
do not log raw membership lists from real data merely because the synthetic example does so.

## Manual Logging Pattern

After the project's approved tracking URI and experiment have been configured:

```python
import mlflow

with mlflow.start_run(run_name="candidate-validation"):
    mlflow.set_tags({"phase": "validation", "protocol_id": protocol_id})
    mlflow.log_params(training_parameters)
    mlflow.log_input(training_dataset, context="training")
    mlflow.log_input(validation_dataset, context="validation")
    mlflow.log_metrics(validation_metrics)
    mlflow.log_dict(sanitised_manifest, "provenance/manifest.json")
```

The variables above are project inputs, not a runnable example. The complete
[classical example](../examples/classical_ml.py) constructs its own synthetic data and local store.
Dataset metadata logging does not guarantee that the underlying data remains recoverable.

## Autologging Decision

1. Inspect the installed framework integration and its supported versions.
2. Decide which parameters, metrics, models, datasets, input examples, and traces may be captured.
3. Configure the framework-specific autologger before training; do not assume every integration
   accepts the same switches or records the same information.
4. Run a small synthetic or approved sample. Inspect the actual run and artefacts for duplicated
   logs, unwanted training rows, source code, environment details, or large checkpoints.
5. Add manual logging only for missing evidence; document who owns the final model package.

Generic `mlflow.autolog()` may enable multiple integrations. Do not enable it blindly in a long-lived
process that also handles sensitive GenAI traffic. Autologging success is not evidence of complete
lineage, leakage-safe splits, or correct metric definitions.

## Concurrency, Failure, and Resume

- The fluent API is not thread-safe and the active run is thread-local. Use explicit run IDs with
  `MlflowClient` for worker interactions; give each logical trial clear ownership.
- For multiprocessing or distributed jobs, pass immutable metadata explicitly. Do not rely on
  inherited active-run state. Aggregate metrics by sample count where required, not by averaging
  worker averages with unequal denominators.
- Choose whether a tracking outage fails training or buffers evidence for later. A silent logging
  failure must not be presented as a fully auditable success. Bound retries and report partial runs.
- Keep failed and pruned trials visible. Distinguish a handled pruning event from a completed model.
- Resume only an intended run, recording resume/checkpoint identity. Do not rewrite earlier
  parameters to make a resumed run look like a fresh, differently configured experiment.
- A run's metric summary is not necessarily its best checkpoint value. Retrieve metric history
  and use the predeclared checkpoint-selection rule when comparing training curves.
- Flush and verify asynchronous logging before process termination. Check installed APIs before
  depending on a particular asynchronous logging option.

## Completion Checks

- Run exists in the intended experiment; status and parent/child relationships are correct.
- Metric names, units, steps, and population counts match the protocol.
- Training, selection, and final-test evidence remain distinguishable.
- Artefacts can be read using the intended consumer identity, not just the training identity.
- A fresh process can load the model; a separately rebuilt environment is tested before release.
- Data retention, deletion, and backups cover metadata and artefacts separately.

Source: [MLflow Python tracking API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html).
