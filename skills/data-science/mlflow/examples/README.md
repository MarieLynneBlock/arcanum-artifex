# MLflow Reference Examples

These sources illustrate MLflow patterns to adapt in a consuming project. The skill needs no
installation and does not bundle a Python project, dependency lock, virtual environment or test suite.
Use the project's existing environment and dependency manager; validate any adopted code there.

## Dependencies and Compatibility

The Python examples use MLflow, SQLAlchemy, NumPy, pandas, scikit-learn and skops, including the
version reporting in [common.py](common.py). The [metric comparator](../scripts/compare_metrics.py)
needs MLflow only, in addition to the Python standard library. Review compatible versions before
adding dependencies through the project's approved process; do not install into a global environment.
In VS Code, select that project's interpreter when investigating unresolved imports.

The Python sources were exercised end to end (all three example entry points plus the metric
comparator) on Windows with Python 3.12.10, MLflow 3.16.0, NumPy 2.5.3, pandas 3.0.5,
scikit-learn 1.9.1 and skops 0.14.0 on 16 September 2026, each completing with exit code 0 and the
documented row/metric outcomes. This is historical compatibility evidence, not a dependency pin or
a guarantee for another environment. Check installed API signatures, especially model logging,
serialisation, GenAI assessments and the comparator's validation exception import.

## Reference Patterns

| Source | Illustrates | Deliberate limits |
| --- | --- | --- |
| [classical_ml.py](classical_ml.py) | Stratified splits, baseline, nested selection runs, final refit/test, dataset metadata, probability model and reload | One synthetic split, no uncertainty analysis or production approval |
| [custom_pyfunc.py](custom_pyfunc.py) | Source-based model, bundled JSON artefact, signature, semantic checks and reload without original configuration | Affine arithmetic only; no external service or native library |
| [model_code.py](model_code.py) | Artefact-based configuration, finite-value checks and a stable output frame | Loaded by MLflow through `set_model`, not runnable alone |
| [genai_eval.py](genai_eval.py) | Traced deterministic application, custom scorer, row coverage and aggregate agreement | Local lookup, not an LLM benchmark; one intentionally wrong answer |
| [tracking.R](tracking.R) | Local-server tracking and failed-run handling | Requires a compatible R/Python pair; not executed during authoring |
| [compare_metrics.py](../scripts/compare_metrics.py) | Comparable candidate/baseline evidence and scalar validation | No provenance verification, registry write or approval |

The classical model returns two probability columns, not class labels; class order is logged.
Its `skops` serialisation trusts `numpy.dtype` for this known pipeline only. Do not extend that trust
to unknown models. Treat all logged code/models as executable content requiring trusted provenance.

The GenAI example expects two successful rows out of three. Correctly measuring the deliberate
failure is not evidence that the application meets a production quality threshold.

## Local Inspection

The Python examples use synthetic data, SQLite metadata and local artefacts. They neither register
nor deploy models and do not call an LLM provider. To run an unmodified example after verifying the
dependencies, use the project interpreter from the folder containing [SKILL.md](../SKILL.md):

```text
python examples/classical_ml.py
```

The shared setup refuses inherited `MLFLOW_` and `OTEL_` settings before importing MLflow and reports
names only. Use a dedicated process with those settings unset; do not clear a real project's
configuration. Do not transplant this local-only setup into a shared service.

Each Python entry point prints its retained output directory: a database, artefacts and JSON summary.
An optional `--output-dir` must name a new directory; otherwise a temporary one is created.
Do not commit generated runs. Remove only the specific output directory when it is no longer in use.

## Validate in the Consuming Project

- Use the [tracking](../references/tracking-and-reproducibility.md) and
  [evaluation](../references/evaluation-and-selection.md) guides to define the actual data and split policy.
- Add project tests for leakage, baseline comparison, evidence completeness and metric-gate failure cases.
- Check fresh-process reload, invalid inputs, prediction parity and inference in a rebuilt target environment.
- Validate [R](../references/r-and-interoperability.md), [deep learning](../references/deep-learning.md),
  serving, cloud/cluster and external-provider integrations separately; local CPU evidence does not prove them.
- Record observed outcomes and approval boundaries in the [release record](../assets/release-record.md).
