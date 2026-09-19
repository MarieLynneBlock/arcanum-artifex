# Deep Learning

Use this guide for PyTorch, Lightning, TensorFlow/Keras or another supported training framework.
Reuse the project's training loop and framework integration; MLflow should not become a replacement
trainer. These are integration recipes, not a GPU-tested example or a required framework installation.

## Establish the Training Contract

Record architecture/configuration, initial weights and provenance, data/tokeniser/augmentation
versions, optimiser, schedule, effective batch size, accumulation, precision, clipping, seed,
hardware, accelerator count, framework/runtime versions, and training budget. For fine-tuning,
include the base model identity, adapters, frozen layers, quantisation and licence restrictions.

Separate three artefacts: a resumable training checkpoint, the validation-selected checkpoint,
and the deployable inference model. They may share weights but have different purposes and contents.
Do not call a weight-only export a complete training-resume checkpoint.

## Framework Routing

| Training surface | Integration starting point | Required inspection |
| --- | --- | --- |
| Plain PyTorch loop | Manual MLflow metrics plus native or custom packaging | `train()`/`eval()`, no-gradient validation, device mapping |
| Lightning | Installed MLflow/Lightning logger or supported autologging | Callback/rank ownership, step semantics, checkpoint selection |
| TensorFlow/Keras | Supported native flavour and autologger for installed versions | Callback duplication, save format, custom layers and preprocessing |
| Transformers/fine-tuning | Existing trainer callback and supported flavour or pyfunc | Tokeniser/config/adapters, generation settings, device dependencies |
| Distributed/multi-node | One aggregate run owned by coordinator | Collective reduction, rank failure and restart/resume identity |

Choose one logger to own each metric and model. Do not combine callbacks, generic autologging and
manual final-model logging without checking the resulting runs. Verify current integration support
against the actual framework versions rather than copying an older framework-specific tutorial.

## Metric Logging Recipe

Use an explicit client/run ID when a coordinator or callback owns logging. This project integration
function assumes already-reduced loss sums and counts; it deliberately does not invent a trainer:

```python
from mlflow import MlflowClient

def log_epoch(client: MlflowClient, run_id: str, epoch: int, loss_sum: float, sample_count: int):
    if sample_count <= 0:
        raise ValueError("Validation requires at least one sample")
    client.log_metric(run_id, "validation_loss", loss_sum / sample_count, step=epoch)
```

All ranks must participate in the framework's required collectives before rank zero logs. Averaging
per-rank means is wrong when counts differ. Define whether loss is per sample, token or batch, and
whether ignored labels/padding contribute to the denominator. Use a global optimiser step or epoch
consistently; accumulation and restarts must not make the same step mean different things.

Log throughput, peak memory, elapsed time and learning rate at an appropriate cadence. Per-batch
network calls can dominate short steps; aggregate or use verified asynchronous support with a
shutdown flush. Record failed/pruned jobs and budget exhaustion, not only successful checkpoints.

## Selection and Resume

- Select the checkpoint using the frozen validation metric/direction and tie rule. Keep its step,
  path/URI, metric and parent run identity. Do not assume the run's last metric is the best checkpoint.
- Early stopping and learning-rate adaptation consume validation information. Do not drive them
  from the final test, and account for repeated tuning when reporting uncertainty.
- For resume, preserve model/optimiser/scheduler states, scaler state for mixed precision, RNG
  states, step/epoch, sampler position and any framework-required trainer state.
- Test an interrupted/resumed short job against the expected continuity of steps and metadata.
  Bitwise identity may not hold across hardware, kernels or distributed schedules; state the limit.
- Record a new run when a change materially alters the experiment, with a link/tag identifying the
  source checkpoint. Do not silently mutate the old run's hyperparameters.
- Retain only approved checkpoints, with explicit retention policy. Deletion of shared or registered
  artefacts requires authorisation and consideration of rollback, lineage and legal obligations.

## Determinism and Data Leakage

Set seeds for the libraries actually involved and record deterministic settings, worker seeding,
sampler behaviour, augmentations and hardware constraints. A seed alone is not determinism.
Document speed/availability costs of deterministic kernels rather than promising universal replay.

Keep subject/time leakage rules from the [evaluation guide](evaluation-and-selection.md). A random
image split can leak near-duplicates or the same subject. A language-model fine-tuning benchmark can
overlap training/pretraining data. Record contamination checks and unresolved limitations.

## Inference Package

1. Restore the selected checkpoint, not whichever weights happen to be in memory at process exit.
2. Put the framework in inference mode and disable training-only behaviour. Package preprocessing,
   tokeniser/vocabulary, output decoding and required custom code alongside the model.
3. Define batch/sequence/image dimensions, dtype, device and padding/truncation behaviour.
4. Verify CPU loading where promised; otherwise state the exact GPU/runtime requirement. Quantised
   and accelerator-specific models may not have a valid CPU fallback.
5. Compare predictions before/after packaging using the appropriate numerical tolerance and task
   metrics. Mixed precision, compiled graphs and quantisation can change outputs.
6. Test target batch sizes, warm-up, concurrency, memory limits, request timeouts and cancellation.
   A single successful small batch is not a capacity test.
7. Rebuild the target environment/image and record the result using the
   [release checklist](models-and-release.md), including streaming/token generation where relevant.

Minimum project acceptance: one short train/validate run, selected-checkpoint identity, interrupted
resume check where required, target-device reload/prediction parity, and a recorded resource bound.
No GPU or heavyweight framework needs to be installed merely to perform a tracking or document review.

Sources: [MLflow tutorials](https://mlflow.org/docs/latest/ml/tutorials-and-examples/),
[PyTorch integration](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pytorch.html),
[TensorFlow integration](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.tensorflow.html).
