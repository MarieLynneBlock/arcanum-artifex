# R and Interoperability

Use MLflow in R workflows to track experiments, record evaluation results and package supported R
models. Work with the documented API for the installed R package version, and use an explicit Python
or service boundary where needed.

## Establish the R Environment

- Record R and R `mlflow` package versions, the Python MLflow installation used by R, and server
  version independently. Use the project's `renv` or other existing dependency lock.
- The R package requires an MLflow Python installation. Check `MLFLOW_PYTHON_BIN` and `MLFLOW_BIN`
  to select the intended Python and MLflow executables; do not assume the editor or shell chose them.
- Keep Windows and WSL/R/Linux environments separate. Verify process execution, path quoting,
  artefact upload and CA/proxy configuration in the OS running R.
- Inspect `help()` and `args()` for the installed R functions before translating a Python example.
  R model logging uses `artifact_path` in the documented API; Python's modern model `name` argument
  is not a universal cross-language substitution.

## Local Tracking Smoke Test

The bundled [tracking.R](../examples/tracking.R) needs a compatible R/Python pair and an explicitly
configured loopback HTTP tracking server. Follow the local server setup in
[platforms and operations](platforms-and-operations.md), using a disposable store and a free port.
After reviewing/installing the project's compatible R dependencies, a PowerShell launch pattern is:

```powershell
$env:MLFLOW_TRACKING_URI = "http://127.0.0.1:5001"
Rscript examples/tracking.R
```

Run from the skill folder. The URI is a local development example, not a real project endpoint.
Use a dedicated process and retain the original environment configuration outside that process.
The script refuses non-loopback targets, creates/selects its own experiment, fits a simple synthetic
linear model, logs held-out RMSE and R metadata, and marks the run failed if execution raises an error.
It does not log or register a model, read real data, or modify cloud/cluster configuration.

Acceptance in the target environment: run status is finished, parameters/metric are visible, the
session metadata artefact downloads successfully, and a controlled error yields a failed run.
Then test the intended R model flavour separately. A Python test passing is not R compatibility evidence.

## Capability Boundaries

| Need | R route | Verify separately |
| --- | --- | --- |
| Experiments and runs | `mlflow_set_experiment`, `mlflow_start_run`, `mlflow_end_run` | Return structure, failure behaviour, active-run semantics |
| Parameters, metrics, artefacts | `mlflow_log_param`, `mlflow_log_metric`, `mlflow_log_artifact` | Serialization, path/encoding, approved data handling |
| Native R model packaging | Supported R flavour, including documented crate-based functions where appropriate | Actual saved flavour, dependencies, load/predict in fresh R process |
| Python model consumed by R | Supported load/predict path or approved inference service | Available flavours, conversion of factors/dates/nulls and output shape |
| Registry aliases or GenAI | Use a verified supported API or explicit Python/service boundary | Do not invent same-named R functions or assume Python parity |

For a crate/function-based model, capture required dependencies and resources explicitly. A captured
R closure can retain unintended data or environment state. Inspect the package and validate a fresh
session with no training objects present. Do not assume all Python flavours can be loaded through R.

## Shared Experiment and Prediction Contracts

Agree on names and semantics across languages: metric units and direction, dataset/split IDs,
positive class, factor levels, column order, missing-value representation, time zone, decimal/integer
conversion and row order. Equal metric names do not establish equivalent calculations.

For HTTP/batch interoperability, use a documented service schema with a contract fixture, versioned
model identity and numerical tolerances. Test both clients against the same expected results and
include invalid inputs. Avoid shelling out to an unpinned Python environment or passing credentials
on a command line as an improvised integration layer.

The [evaluation protocol](../assets/evaluation-protocol.md) and
[release record](../assets/release-record.md) are language-independent. Populate them with actual R
evidence where R participates in training or inference; label delegated Python steps explicitly.

Source: [official R API reference](https://mlflow.org/docs/latest/api_reference/R-api.html).
