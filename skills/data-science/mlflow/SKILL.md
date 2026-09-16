---
name: mlflow
description: >-
  Design, implement, audit, and troubleshoot MLflow workflows across projects. Use when
  tracking experiments, comparing runs, recording datasets and lineage, evaluating models,
  packaging custom pyfunc models, managing model versions and aliases, tracing or evaluating
  GenAI/RAG/agents, or preparing batch and online inference. Covers classical ML, deep learning,
  and custom pipelines; Python workflows and R integration guidance; local Windows/WSL,
  OpenShift 4, and AWS. Emphasises leakage-safe evaluation, reproducibility, security, and evidence-based
  promotion. Use for MLflow integration and lifecycle decisions, not as a substitute for
  domain-specific statistical design or a production infrastructure operator.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: "1.2.0"
---

# MLflow for Senior Data Scientists

Use MLflow to make experiments, evaluation evidence, model packages, and release decisions
inspectable and reproducible. Adapt to the project's stack and maturity; do not impose an
entire platform on a task that only needs a correctly instrumented training loop.

## Operating Contract

- Follow project instructions and the host agent's permissions. Ask before destructive actions,
  production deployments, shared registry alias changes, schema migrations, or access-policy changes.
- Inspect existing code, environment locks, tests, experiment conventions, and CI before editing.
  Reuse the project's framework, orchestration, dependency manager, and logging conventions.
- Never request or print credentials. Do not log raw sensitive datasets, prompts, responses,
  identifiers, credentials, or environment dumps. Review autologging and tracing before enabling them.
- Treat downloaded models and serialised artefacts as executable, untrusted inputs. Load only
  approved artefacts with known provenance; do not disable TLS checks to make a connection work.
- Distinguish observed results from proposed commands and untested configurations. Use `[TODO]`
  for unknown project-specific values; never invent successful runs, model quality, or API support.
- Keep the skill copyable as one folder. Project integrations may use declared external libraries
  and services, but must not depend on another file in the skill's source repository.

## Establish the Task

Infer what is already evident, then ask only for missing information that changes the solution:

1. **Decision and workload:** instrument, compare, debug, evaluate, package, register, or deploy?
   Classical ML, deep learning, GenAI/agents, or a custom pipeline? Who consumes the result?
2. **Environment:** Python/R and framework versions; MLflow client, server, and managed service
   versions; Windows, WSL, container, or cluster; CPU/GPU; package and network restrictions.
3. **Storage and identity:** tracking and registry URIs, backend database, artefact store, identity
   mechanism, tenant boundary, retention, and data classification. Never ask for secret values.
4. **Evaluation contract:** observation unit, prediction time, target availability, groups/time,
   held-out strategy, primary metric and direction, baseline, meaningful improvement, guardrails,
   and acceptable operational cost. Which data is allowed to leave the current environment?
5. **Deliverable and authority:** local proof, project change, review, release evidence, or proposed
   infrastructure configuration? Which actions are authorised and which need an approval gate?

Do not block a harmless local investigation on every unanswered production question. Record
bounded assumptions and proceed with the smallest useful, reversible step.

## Version and Platform Policy

- Use a documented stable MLflow release supported by the project's Python and frameworks.
  Resolve and lock exact versions for executable work; do not silently upgrade a project.
- The [example sources](examples/README.md) are reference implementations, not a bundled Python
  project. Adapt and validate them using the consuming project's environment and dependency manager.
- Record the versions actually inspected and tested. The online `latest` documentation is a
  discovery source, not proof that an installed client, server, R package, or managed service
  supports an API. Check versioned documentation and function signatures where necessary.
- Prefer current model-version aliases and explicit model signatures for new Python workflows.
  Treat legacy registry stages and older API examples as migration inputs, not defaults.
- Choose Python or R to fit the project's workflow. Use each language's documented APIs; do not
  translate Python GenAI, tracing, registry, or packaging calls into imagined R equivalents.
- Keep local paths, container paths, S3 URIs, tracking URIs, and model URIs distinct. Windows and
  WSL are separate environments; do not reuse a virtual environment across their filesystems.

## Load the Relevant Resources

Resolve these paths relative to this skill folder, not the project working directory. Load only the
guides needed for the current task; examples are opt-in demonstrations, not automatic setup steps.

| Task | Resource |
| --- | --- |
| Scope a cross-project integration | [Project contract](assets/project-contract.md) |
| Instrument runs, provenance, autologging or distributed execution | [Tracking and reproducibility](references/tracking-and-reproducibility.md) |
| Design splits, compare models and validate metrics | [Evaluation and selection](references/evaluation-and-selection.md) and [protocol template](assets/evaluation-protocol.md) |
| Package models, manage versions, or prepare inference | [Models and release](references/models-and-release.md) and [release record](assets/release-record.md) |
| Instrument deep-learning training, checkpoints and inference | [Deep learning](references/deep-learning.md) |
| Trace or evaluate GenAI, RAG, prompts and agents | [GenAI and agents](references/genai-and-agents.md) |
| Configure local/Windows/WSL, OpenShift 4 or AWS operations | [Platforms and operations](references/platforms-and-operations.md) |
| Use R or bridge R/Python workflows | [R and interoperability](references/r-and-interoperability.md) |
| Diagnose failures or check version-sensitive claims | [Troubleshooting and sources](references/troubleshooting-and-sources.md) |
| Inspect and adapt implementation patterns | [Reference examples and project validation](examples/README.md) |
| Apply scalar checks to existing evaluation evidence | [Metric comparator](scripts/compare_metrics.py), [policy example](assets/metric-policy.example.json), [evidence template](assets/evaluation-evidence.template.json) |

## Work Loop

### 1. Inspect and Choose One Path

Find the code that controls training, evaluation, logging, or serving. State a falsifiable local
hypothesis and the cheapest useful check. Choose the relevant workflow; load only its supporting
material. An MLflow question does not automatically require changing the model or infrastructure.

### 2. Define Evidence Before Running

- Establish a baseline and freeze the evaluation protocol before comparing candidates.
- Split by the deployment reality: stratification where appropriate, entity-disjoint groups,
  or chronological windows with gaps/embargoes where necessary. Fit preprocessing on training
  data only. Tune on validation data; reserve the final test for the agreed release decision.
- Record data version or approved fingerprint, query/filter definition, split policy, target
  construction, feature availability, seed, code revision, environment, and dependency lock.
  A seed or dataset digest alone does not establish reproducibility.
- Predeclare metric aggregation, uncertainty method, subgroup sample-size rules, threshold
  selection, and non-quality constraints. Do not claim superiority from an isolated best run.

### 3. Instrument Deliberately

- Use stable experiment names, meaningful run names, bounded tags, immutable parameters, and
  metrics with clear units and steps. Use parent/child runs when the hierarchy adds meaning.
- Choose manual logging or supported autologging intentionally. Avoid duplicate model logging,
  accidental nested runs, high-cardinality tags, and distributed workers racing on one run.
- Log approved dataset metadata and evaluation context, not an unreviewed data export. Inspect
  tables, input examples, checkpoints, dependency files, and traces for sensitive content.
- For deep learning, record framework/hardware and determinism limits, rank ownership, checkpoint
  selection, and resumability. MLflow records the work; it does not make training deterministic.
- For GenAI, version the prompt, application, model/provider, retrieval corpus, tools, evaluator,
  and evaluation dataset. Capture quality, latency, cost, safety, and failure evidence without
  exposing sensitive traces. External judges require approved providers and data handling.

### 4. Evaluate and Package

- Compare candidates on the same versioned protocol. Report baseline-relative results, failure
  cases, missing values, uncertainty, and slice coverage. A missing required metric is not a pass.
- Keep training, model selection, final testing, and post-release monitoring distinct. For
  forecasting use backtesting; for unsupervised tasks justify proxy metrics and external checks.
- Package preprocessing with the model where appropriate. Include a signature, sanitised input
  example, dependencies, and required artefacts. Test reloading and inference, not just saving.
- Test expected schema, invalid inputs, prediction shape, numerical agreement, and environment
  reconstruction. Loading successfully does not prove training reproducibility or serving parity.

### 5. Govern and Release Only Within Authority

- Separate a tracking run, a logged model, a registered model version, and a deployed service.
  Record immutable identifiers in release evidence; a mutable alias is not an immutable release.
- Promotion requires declared quality gates, evidence completeness, provenance, ownership,
  operational readiness, and the required approval. An alias is a pointer, not an approval system.
- Validate inference in the target environment. Specify identity, storage access, resources,
  health checks, concurrency, observability, rollback, and cleanup before shared deployment.
- Propose OpenShift/AWS infrastructure only after discovering the existing platform contract.
  Do not assume MLflow supplies authentication, enterprise RBAC, orchestration, drift detection,
  or a complete production serving platform without separately configured components.

### 6. Verify and Report

Run the smallest relevant check immediately after a change, repair local failures, then widen
verification only for the remaining risks. Do not install heavyweight frameworks or call paid
providers just to exercise an unrelated path.

## Expected Response

Return only the sections useful to the task:

1. **Decision:** requested outcome, selected workflow, assumptions, and unresolved blockers.
2. **Changes:** project files or runnable commands, exact dependency assumptions, and side effects.
3. **Evidence:** tests actually run, run/model identifiers where available, baseline comparison,
   evaluation data/split identity, and artefact locations. Redact sensitive endpoint details.
4. **Release position:** pass, fail, or insufficient evidence; risks, approval boundaries,
   rollback considerations, and untested environments or optional integrations.

For reviews, lead with severity-ranked findings and concrete evidence. For implementation,
leave an executable, validated increment rather than a catalogue of possible MLflow features.
