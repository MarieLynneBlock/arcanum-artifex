# Troubleshooting and Source Notes

Use the smallest synthetic reproduction that distinguishes the suspected layer. Preserve evidence
and avoid destructive cleanup as a first response. Never print complete environment/configuration
dumps, connection strings or credentials while debugging.

## Diagnostic Routing

| Symptom | First discriminating check | Likely next action |
| --- | --- | --- |
| Pylance cannot resolve MLflow/SQLAlchemy | Selected interpreter and dependencies in the consuming project | Follow the [dependency guidance](../examples/README.md); do not suppress valid import diagnostics |
| Runs appear in the wrong place | Intended interpreter/process, active experiment, explicit tracking configuration | Correct the owning process; do not move/delete stores blindly |
| Tracking HTTP error | Bounded authenticated metadata request; server/version compatibility | Separate DNS, TLS, proxy, authentication, authorisation and payload errors |
| TLS failure on corporate network | Approved CA chain and process trust configuration | Configure trust; never disable verification |
| Metadata works, artefacts fail | Small synthetic upload and download under consumer identity | Check proxy/direct mode, recorded artefact URI, S3/KMS/network permissions |
| Experiment mode changed but old runs fail | Existing experiment and model artefact locations | Plan migration or retain old access; flags do not relocate data |
| Duplicate/unexpected runs | Active-run ownership and autologger/callback configuration | Choose one owner and remove duplicate instrumentation locally |
| Parameters cannot be updated | Same run being reused with a changed configuration | New run or explicit resume contract, not hidden mutation |
| Run metric differs from selected checkpoint | Metric history and checkpoint-selection rule | Compare the agreed step/checkpoint, not just latest metric |
| Model loads only in notebook | New-process reload from another working directory | Bundle code/resources and test dependency reconstruction |
| sklearn untrusted-type failure | Locally generated package and exact serializer versions/types | Review a narrow trust decision; never auto-trust arbitrary types |
| Schema rejects missing integers | Actual input types/nullability and signature | Fix the declared input contract and representative example |
| Serving differs from offline | Same immutable model, adapter payload, device/dtype and preprocessing | Add target-runtime parity test |
| Alias changes but predictions do not | Version loaded by the running process | Explicit reload/deployment; alias does not hot-swap memory |
| GenAI aggregate looks too good | Expected rows versus valid assessments, scorer errors and exclusions | Fail incomplete evidence and repair evaluation coverage |
| OpenShift permission error | Runtime UID and writable directories under restricted policy | Fix image/runtime paths, not a privileged SCC workaround |
| Managed AWS API unsupported | Actual server/client/plugin pairing and region support | Use supported APIs/versions; do not assume OSS latest parity |
| R cannot find MLflow | R package, `MLFLOW_PYTHON_BIN`, `MLFLOW_BIN`, executable permissions | Correct and lock the intended R/Python pair |

## Minimal Investigation Record

1. Expected behaviour and a bounded failing command/input.
2. Versions, OS/runtime and relevant configuration *names*, with values redacted where needed.
3. One local hypothesis and a check that could disprove it.
4. Actual result: layer, error class, affected run/model ID where safe to disclose.
5. Smallest repair and rerun of the same check.
6. Remaining uncertainty and any required operator approval.

Avoid unrestricted `mlflow.doctor` output in shared conversations; diagnostics can reveal sensitive
configuration. Inspect a specific safe fact such as `mlflow.__version__` or a function signature instead.
Do not query a production server or load unknown model code just to answer a local API question.

## Version-Sensitive Facts

| Surface | Guidance used in this package |
| --- | --- |
| Python examples | Exercised end to end with Python 3.12.10 and MLflow 3.16.0 (exit code 0 for all entry points); adapt and validate in the [consuming project's environment](../examples/README.md) |
| Model logging | Use supported `name` and returned model URI; older `artifact_path` examples need review |
| sklearn serialisation | Example explicitly selects skops and a reviewed dtype trust entry |
| Registry | Stages deprecated since 2.9; aliases do not implement approval or hot reload |
| Validation | `mlflow.validate_evaluation_results`; `MetricThreshold(greater_is_better=...)` |
| GenAI | `mlflow.genai.evaluate`, custom `scorer`, actual row assessments and trace coverage |
| R | Separate API and Python dependency; model `artifact_path` remains documented in R |
| Hosting | Authentication/RBAC, trace storage, artefact transfer and job coordination vary by release |
| Managed services | Provider compatibility tables take precedence over versions used to exercise reference examples |

The metric comparator imports `ModelValidationFailedException` from
`mlflow.models.evaluation.validation`, as verified with MLflow 3.16.0. Retest that import when
upgrading. Do not assume the exception lives in the general `mlflow.exceptions` module.

## Official Sources

Documentation was consulted on 16 September 2026. The links below are discovery references, not
runtime dependencies of the skill or proof of compatibility with any installed target. `latest` can
change; use documentation matching the project's chosen version before adopting an API.

| Source | What it supports |
| --- | --- |
| [Tutorials and examples](https://mlflow.org/docs/latest/ml/tutorials-and-examples/) | Workload discovery and official learning routes |
| [Releases](https://mlflow.org/releases) | Release/version context; 3.16.0 was the current release inspected |
| [Python tracking/evaluation API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html) | Run, dataset, evaluation and validation APIs |
| [Pyfunc API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html) | Source/custom models, resources, signatures and dependencies |
| [GenAI API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.genai.html) | Evaluation and prompt APIs |
| [Custom scorers](https://mlflow.org/docs/latest/genai/eval-monitor/scorers/custom/) | Scorer inputs, outputs and evaluation behaviour |
| [Registry workflow](https://mlflow.org/docs/latest/ml/model-registry/workflow/) | Version/alias operations and legacy stages |
| [Tracking server architecture](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/) | Backend/artefact configuration and server boundaries |
| [R API](https://mlflow.org/docs/latest/api_reference/R-api.html) | R functions, Python dependency and model flavours |
| [AWS MLflow integration](https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-track-experiments.html) | Managed-server plugin, ARN and version pairing |
| [AWS tracking servers](https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-create-tracking-server.html) | Managed tracking lifecycle and IAM prerequisites |
| [OpenShift 4.18 image guidance](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/images/creating-images) | Arbitrary UID, writable paths and image/runtime practices |

Additional framework/model API links in the guides are reference routes; their integrations were
not executed here. The local audit checks Markdown targets and packaged resources, not continued
reachability or unchanged content of every external documentation page.

## Updating This Package

When changing example sources or the comparator, check release notes and exact API signatures in
the intended project environment. Add project-level checks for model serialisation, input contracts,
trace assessment shape and exception locations using the [validation guidance](../examples/README.md).
Record tested versions and outcomes only after execution. Do not infer GPU/R/managed-service support
from passing local CPU checks.
