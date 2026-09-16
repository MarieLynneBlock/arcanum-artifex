# Model Packaging, Registry, and Release

Use this guide when packaging preprocessing/custom code, introducing a registry, preparing inference,
or reviewing a promotion. Keep model quality, package correctness, and deployment approval separate.

## Identity and Ownership

| Object | Identifies | Does not establish |
| --- | --- | --- |
| Experiment/run | Execution context and recorded evidence | A deployable package or approval |
| Logged model | Packaged model and its recorded metadata | A registered version or running service |
| Registered model version | Version under a governed model name | A tested deployment in every environment |
| Alias | Mutable pointer to a version | Immutable release identity or automatic hot reload |
| Deployment revision | Actual image/model/configuration serving requests | Long-term statistical validity |

Record `ModelInfo.model_uri` returned by logging. Do not reconstruct model locations by assuming
an older `runs:/...` layout. For releases, resolve aliases to immutable version identities and
record both. Registry stages have been deprecated since MLflow 2.9; retain them only for deliberate
legacy compatibility or migration, not as the default design for new projects.

## Choose a Packaging Interface

| Need | Starting point | Contract to test |
| --- | --- | --- |
| Supported sklearn/framework model | Native flavour plus pyfunc where supported | Output meaning and flavour-specific dependencies |
| Custom preprocessing or inference | `mlflow.pyfunc.PythonModel` with explicit artefacts | Signature, resource loading, batching, error handling |
| External service wrapper | Approved runtime client/configuration | Authentication, timeouts, retries, data egress, provider version |
| R consumer | Supported R flavour or approved service boundary | Actual R/Python compatibility and prediction shape |
| GenAI/agent serving | Current documented agent/application interface | Streaming, tool calls, session state, safety and deployment support |

The [custom pyfunc example](../examples/custom_pyfunc.py) logs the bundled
[model source](../examples/model_code.py) and configuration artefact. `load_context` reads the copied
artefact, not a developer's working-directory path. The source-based interface is version-sensitive;
verify its status and behaviour in the target client. Both source execution and pickle-based
deserialisation require trusted provenance.

## Package Checklist

- Include preprocessing, feature ordering, class/label ordering, output units and decision threshold.
- Infer or construct the signature from representative, sanitised inputs. Include nullability,
  integer-with-missing-value cases, categories, nested schemas and tensor dimensions as appropriate.
- A signature is not a full semantic validator. Test finite values, allowed ranges, null handling,
  row-count limits, unknown categories and application-specific constraints explicitly.
- Bundle required files using the flavour's artefact mechanism. Review `code_paths` before including
  source; do not assume inferred code paths package non-Python files or exclude confidential code.
- Supply one dependency mechanism at a time: `pip_requirements`, `extra_pip_requirements`, or
  `conda_env` according to the documented API. Include custom wheels/native libraries and record
  the OS/architecture/CUDA constraints that a Python dependency file cannot express.
- Never log credentials as model configuration or resource artefacts. Runtime credentials must be
  injected by the approved identity mechanism.
- Audit the saved package contents and licensing. Unreviewed arbitrary models must not be loaded
  simply to inspect metadata; use a trusted, isolated inspection process where required.

The classical example explicitly uses `skops` with a narrowly reviewed `numpy.dtype` trust entry
for its locally trained pipeline. It records the `skops` version. Do not generate a trust allow-list
from arbitrary artefacts and accept it automatically, or switch to pickle merely to bypass review.

## Verification Ladder

1. Save/log completes and the returned model URI resolves.
2. Same-environment reload agrees on a fixed reference batch within documented tolerance.
3. A new process outside the source working directory can load and predict without original files.
4. A rebuilt environment from the release lock/image works without developer-only dependencies.
5. Target runtime handles schema errors, batch sizes, device/dtype, concurrency and resource limits.
6. Batch/HTTP/streaming adapter output matches the offline contract, including errors and ordering.
7. Canary or shadow checks, rollback and operational monitoring are approved and exercised.

The examples illustrate saving and reloading; perform the verification ladder in the consuming
project, including fresh-process and rebuilt-environment checks. For a local serving check,
inspect `mlflow models serve --help` in the chosen version and use an approved,
loopback-bound process. `--env-manager local` reuses the environment; it is not reconstruction.
Test the documented request format, status codes, output schema and invalid requests in the target
adapter. Do not expose the local scoring server as an unauthenticated production service.

## Registry Transaction

Before any registry write, identify the registry backend, model owner, naming convention, permitted
identity, approval requirements and source artefact access. Self-hosted registry use requires an
appropriate SQL backend; a tracking directory alone is not a shared governance design.

The core Python operations, after approval, are:

```python
version = mlflow.register_model(model_uri, registered_name)
client.set_registered_model_alias(registered_name, "candidate", version.version)
resolved = client.get_model_version_by_alias(registered_name, "candidate")
```

These are API illustrations using project-provided objects, not permission to execute. Registering
again can create another version; account for retries and deduplication using immutable source
identifiers. Alias writes can race. Serialise promotions through the project's deployment mechanism
and verify the observed version afterwards; a read-before-write is not an atomic compare-and-swap.

Do not assume different tracking and registry backends automatically copy artefacts or preserve
access. Verify supported cross-environment migration and consumer access. Separate dev/test/prod
boundaries according to the actual access model, not merely a tag or experiment name.

## Release and Rollback

Complete the [release record](../assets/release-record.md) with immutable model URI/version, code and
image digest, protocol/evidence IDs, approver, serving configuration, previous known-good version,
monitoring owner and rollback action. Resolve the release version once when building/deploying;
repeated alias resolution during a batch can mix models within one output dataset.

An alias update affects subsequent resolution, not models already loaded in memory. A service needs
an explicit restart/reload/deployment strategy. Rollback includes compatible preprocessing,
configuration and infrastructure, not just moving an alias. Preserve old artefacts until retention,
audit and rollback obligations expire.

After release, monitor input quality, serving errors, latency, cost, prediction distribution and,
when labels mature, task performance. Distinguish covariate drift from measured performance loss.
Define investigation and retraining triggers; MLflow tracking alone does not provide a complete
production monitoring or incident-response system.

Sources: [model registry workflow](https://mlflow.org/docs/latest/ml/model-registry/workflow/),
[pyfunc API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html),
[sklearn API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html).
