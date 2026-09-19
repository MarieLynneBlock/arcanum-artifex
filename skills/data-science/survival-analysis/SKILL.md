---
name: survival-analysis
description: >-
  Expert-standard support for survival and time-to-event analysis at any experience
  level: cohort design, code, diagnostics, evaluation, interpretation and review.
  Use for customer churn, retention, failure, readmission or other censored outcomes;
  Kaplan-Meier, Cox proportional hazards, AFT, competing risks, delayed entry,
  recurrent events, time-varying covariates, discrete-time models, survival forests,
  calibration, temporal leakage, immortal time, large-cohort runtime or survival-model
  audits. Python first, with a secondary R path. Adapt explanations to the user's
  experience, ask about unresolved estimands and observation rules, and distinguish
  hazards from event probabilities.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 1.2.0
---

# Survival Analysis

Provide expert-standard support for data scientists at any experience level. Cover
description, association, prediction and analysis review across domains, with
customer churn as a recurring example. Briefly define unfamiliar concepts in plain
language, connect them to the immediate decision, then offer deeper technical detail
when it helps. Prioritise the estimand, observation process, executable work and
evidence over a tutorial or paperwork.

## Request Routing

| Request | Steps that apply | Reference to load |
| --- | --- | --- |
| Define a cohort, event or estimand | 1-2 | Design and assumptions |
| Choose or justify a method | 1, 5 | Methods and interpretation |
| Write or adapt code | 2, 5, 6 | Implementation |
| Diagnose a failing or suspect fit | 2, 6 | Implementation, methods |
| Design or repair validation | 3, 7 | Evaluation and reporting |
| Interpret or explain a result | 4, 8 | Methods and interpretation |
| Review someone else's analysis | 1-8 as evidence allows | All, as the findings require |
| Cohort too large or too slow | 2, 5, 7 | Scale and performance |

## Working Agreement

- Establish whether the request is to design, implement, diagnose, evaluate,
  interpret or review. Do the requested slice; do not restart a settled analysis.
- Inspect the existing schema, code, environment and documented decisions first.
  Ask only questions whose answers change the next step. Never invent event
  definitions, censoring rules, business thresholds or results.
- Separate confirmed facts, proposed choices and unresolved questions. Mark
  material unknowns `[TODO]` only when recording them is useful. Explain why a
  material unknown blocks fitting or interpretation and what evidence resolves it.
  A clearly labelled synthetic example may proceed without real data.
- Use Python primarily and R when requested or already established. Preserve the
  project's libraries, versions and environment manager where suitable. Confirm
  API support for the installed version before writing library-specific code.
- Ask before installing, upgrading or removing dependencies. Do not auto-install
  on import failure; report the missing prerequisite.
- Work with the project's existing data-access constraints. Prefer schemas,
  aggregate diagnostics or synthetic examples over sensitive row-level output.

## Workflow

### 1. Define the Question and Estimand

Confirm the population, unit of analysis, decision, event and meaningful time
horizons. Distinguish describing event-free survival, estimating adjusted
associations, predicting absolute risk, and estimating a causal intervention
effect. A predictive model or adjusted hazard ratio alone does not identify a
causal effect. Retention targeting needs evidence of intervention benefit, not
only a ranking of churn risk.

Record time zero, prediction time, eligibility, time scale and units, event coding,
observation end, censoring reasons, competing events, delayed entry, repeated
episodes and feature-availability timestamps. Ask whether churn is cancellation,
non-renewal or a confirmed inactivity rule, and whether reactivation is possible.
Do not fit while these definitions materially change the target or risk sets.

### 2. Validate the Cohort and Observation Process

Reconcile cohort counts and exclusions. Check IDs, event-code meanings, missing
outcomes, non-finite or negative durations, zero-time events, timestamp order,
duplicates, time units and the last date at which events can genuinely be observed.
Never turn a missing event flag into censoring or drop censored rows by default.

Use the correct schema: duration/event for ordinary right censoring; entry/exit
for delayed entry; lower/upper bounds for interval censoring; event types for
competing risks; ID/start/stop/event for changing covariates or repeated episodes.
Check non-overlapping, positive-length intervals and events at the correct stops.
Do not force unsupported observation schemes into a two-column right-censored API.

Examine censoring by reason, cohort and predictors. Independent censoring is an
assumption, not something a diagnostic can certify. Distinguish assumptions for
unadjusted Kaplan-Meier from those conditional on covariates in a regression model.
Escalate plausible informative dropout with sensitivity analyses and limitations.

### 3. Establish a Leakage-Safe Validation Design

For prediction, agree training, tuning and held-out evaluation populations and
calendar cut-offs before fitting. Match validation to the intended deployment.
Keep dependent entities and episodes together unless an explicit existing-customer
backtest justifies otherwise; preserve temporal order and label availability.
Fit preprocessing, feature selection and tuning only within training folds.

At prediction time, use only information already available, including ingestion
and reporting delays. For time-varying analysis, covariates must be available at
each interval start. Do not use final tenure, later cancellations or future
behaviour as predictors. A later training-label freeze can leak into an earlier
deployment backtest even when feature timestamps are correct.

For an association study, use a justified inferential design, diagnostics and
sensitivity analyses; do not impose a predictive train/test split automatically.

### 4. Describe Before Modelling

Report subjects, events by type, censoring, follow-up and numbers at risk. Use
Kaplan-Meier with confidence intervals and a risk table for suitable single-event
data; use cumulative incidence for cause-specific probabilities with competing
events. Do not call one minus cause-specific Kaplan-Meier an observed event risk.

Report the median only if the curve reaches 0.5; otherwise say "not reached within
follow-up". Consider restricted mean survival over an agreed supported horizon.
An unadjusted log-rank comparison is neither an effect size nor a causal result.

### 5. Select the Simplest Suitable Model

Start with a transparent baseline compatible with the estimand and observation
scheme, often Cox PH for baseline covariates and ordinary right censoring. Consider
penalisation and nonlinear terms where justified. Compare a limited set of
alternatives rather than conducting an unbounded algorithm search.

Route competing probabilities to cumulative-incidence methods; changing
covariates to start-stop methods or a justified landmark design; non-PH effects to
time interactions, stratification or suitable alternatives; time ratios to AFT;
repeated events to an explicit recurrent-event or multi-state design. Consider
survival forests, boosting or discrete-time models when prediction warrants them.
Do not assume a Weibull AFT model resolves PH violations: its usual form is also PH.

When cohort size, expanded row count or runtime constrains the choice, size the
problem before abandoning a method. Treat any sampling design as an explicit
observation and estimator choice: report the inclusion rule, compatible estimator
and variance procedure rather than applying it as a silent shortcut.

### 6. Check Fit and Assumptions

For Cox models, combine scaled Schoenfeld diagnostics and plots with effect size,
functional form and domain knowledge. Non-significance is not proof of PH. Check
convergence, separation, collinearity, sparse events, influential observations and
dependence. Do not silence warnings or use penalisation to hide a broken cohort.

Explain how each material violation changes the conclusion or model. Stratifying
on a variable does not estimate its hazard ratio. Time-varying covariates do not
automatically create time-varying coefficients. Extrapolation needs explicit
distributional assumptions, sensitivity analysis and a labelled extrapolated range.

### 7. Evaluate What Will Be Used

For prediction, assess held-out discrimination, censoring-aware probability error
and calibration at agreed horizons, with uncertainty and a simple baseline. Name
the concordance estimator, AUC definition, time grid, censoring estimator and
integration interval. A high C-index is not evidence of calibrated probabilities.

Verify follow-up and censoring support before IPCW metrics. Do not silently remove
long-followed subjects, clip their outcomes or change horizons to make a metric
run. Use competing-risk metrics for a competing-risk estimand. Review subgroup and
calendar-period performance where sample support permits; report unsupported
horizons and unstable estimates instead of inventing thresholds or precision.

### 8. Interpret and Hand Over

Distinguish survival probability, event probability, hazard ratio, subdistribution
hazard ratio and time ratio. State units, reference categories, conditioning,
uncertainty and limitations. Keep association, prediction and causation separate.

For work that will be rerun, retain the cohort/query version, extraction and label
cut-offs, split membership, feature specification, seeds, package versions,
transformations and model settings in the project's existing artefact. Provide
reproducible code plus evidence appropriate to the requested slice.
For prediction use, state scoring time, eligible population, feature freshness and
outcome maturation so the analysis can be reproduced and evaluated over time.

## Response Contract

Return the decision or finding first, then only the supporting evidence relevant to
the request:

1. Objective, estimand and scope; unresolved blocking questions when applicable.
2. Method choice and observation-scheme fit when selecting or reviewing a method.
3. Code or analysis changes when requested, using the project's established stack.
4. Checks actually run, results, remaining assumptions and unavailable validation.
5. Interpretation, limitations and the next analytical decision when needed.

For reviews, lead with severity-ranked findings tied to the supplied code or
analysis, consequences and suggested corrections. Never claim that documentation
review, code generation or a synthetic smoke test validates a real-world model.

## Bundled Resources

Load only the resources needed for the current task. Prefer the project's existing
notebook, code comments, analysis document or issue context. Use a template only
when it helps resolve material decisions or the user asks for one; copy only the
relevant sections and omit the rest without justification.

- [Design and assumptions](./references/design-and-assumptions.md): estimands,
  observation schemas, churn definitions, leakage and informative censoring.
- [Methods and interpretation](./references/methods-and-interpretation.md): method
  selection, equations, diagnostics, advanced designs and interpretation traps.
- [Evaluation and reporting](./references/evaluation-and-reporting.md): validation
  design, metric contracts, calibration, uncertainty and evidence by task.
- [Scale and performance](./references/scale-and-performance.md): load when cohort
  size, expanded row count or runtime constrains the work. Single-workstation
  choices, design-specific sampling and warehouse escalation.
- [Implementation](./references/implementation.md): library compatibility, capability
  checks, troubleshooting, Python usage and sources, plus a secondary R example that
  is not execution-tested. Read before running the bundled script.
- [Synthetic Python workflow](./scripts/synthetic_workflow.py): single-event
  example with input guards, Cox diagnostics, held-out metrics and calibration.
  Requires the documented dependencies; it never installs or accesses real data.
- [Analysis plan](./assets/analysis-plan.md): optional prompts for unresolved
  estimand, cohort, leakage, assumption and validation decisions.
- [Evidence report](./assets/analysis-report.md): optional prompts for findings,
  diagnostics, validation limits and reproducibility evidence.
