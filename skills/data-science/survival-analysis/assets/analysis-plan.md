# Survival Analysis Plan

Use only the sections and rows that resolve an unsettled design decision. This is
not compulsory paperwork for a settled analysis: copy relevant prompts into the
project's existing artefact, delete irrelevant rows, and leave unused prompts
behind. Use `[TODO]` only for a material unresolved item. An unresolved item that
changes the target or observation process blocks dependent modelling.

## Decision and Scope

| Item | Agreed definition or evidence |
| --- | --- |
| Requested work and intended users | [TODO] |
| Decision and action this analysis supports | [TODO] |
| Description, association, prediction or causal inference | [TODO] |
| Population, eligibility and unit of analysis | [TODO] |
| Estimand, conditioning population and time horizon(s) | [TODO] |
| Domain knowledge needed to resolve the question | [TODO] |
| Data sources and available schema | [TODO] |

## Cohort Contract

| Item | Agreed definition or evidence |
| --- | --- |
| Subject ID and episode ID, if applicable | [TODO] |
| Source/query version, extraction date and label freeze | [TODO] |
| Time zero, prediction time, time scale and units | [TODO] |
| Eligibility assessment time and delayed-entry rules | [TODO] |
| Event definition, coding and ascertainment source | [TODO] |
| Event occurrence date versus date it becomes known | [TODO] |
| Censoring sources, reasons and last observable event date | [TODO] |
| Competing events and why they preclude the target event | [TODO] |
| Right, left or interval censoring; truncation | [TODO] |
| Repeated episodes, reactivation and terminal events | [TODO] |
| Exclusions, missing outcomes and zero-time events | [TODO] |
| Feature measurement, availability and reporting delays | [TODO] |
| Dependence between people, accounts, sites or episodes | [TODO] |

For churn, resolve cancellation versus non-renewal versus inactivity. State
whether an upgrade changes eligibility or truly prevents the event. An inactivity
label needs enough future observation to confirm it; do not call recently inactive
customers churned or non-churned before their labels mature.

## Data Checks and Reconciliation

- Starting population, exclusions by reason and final subjects/episodes: [TODO]
- Events by type, censored observations and unresolved outcomes: [TODO]
- Timestamp order, durations, units, duplicates and missing values: [TODO]
- Entry/exit and start/stop risk-set checks, where relevant: [TODO]
- Follow-up and censoring distributions by relevant cohort: [TODO]
- Leakage checks, including labels available at each backtest cut-off: [TODO]
- Supported horizons, numbers at risk and sparse subgroups: [TODO]
- Failures found, resolutions and retained limitations: [TODO]

## Modelling and Assumptions

| Item | Planned method and justification |
| --- | --- |
| Descriptive estimator and uncertainty | [TODO] |
| Transparent baseline and limited alternatives | [TODO] |
| Events available and events per estimated parameter | [TODO] |
| Predictor specification, missingness handling and nonlinear terms | [TODO] |
| Independent-censoring assumption and plausible violations | [TODO] |
| PH, distributional or other model assumptions | [TODO] |
| Dependence, recurrent events or competing-risk handling | [TODO] |
| Diagnostics and actions if assumptions fail | [TODO] |
| Sensitivity analyses and any extrapolated range | [TODO] |
| Cohort size, expanded row count and any sampling design | [TODO] |
| Sampling inclusion rule/probabilities, compatible estimator and variance method | [TODO] |
| Libraries, installed versions and API support verified | [TODO] |

## Validation

For prediction, specify the deployment-matched split. For association, replace
predictive split items with the inferential design and uncertainty procedure.

| Item | Agreed approach |
| --- | --- |
| Training, tuning and held-out dates/populations | [TODO] |
| Entity/episode grouping and label-availability cut-offs | [TODO] |
| Training-only preprocessing and tuning | [TODO] |
| Discrimination estimator and score direction | [TODO] |
| Probability error, calibration and horizons | [TODO] |
| Censoring estimator, support checks and time grid | [TODO] |
| Competing-risk metric definition, if relevant | [TODO] |
| Uncertainty, subgroup and calendar-period analysis | [TODO] |
| Baseline comparison and decision usefulness | [TODO] |
| Decision-relevant evaluation criteria and rationale | [TODO] |

Do not invent acceptance thresholds from convention. When a decision needs one,
derive it from error costs, uncertainty and achievable data support.

## Open Decisions

| Question | Why it matters | Evidence needed | Blocks what? |
| --- | --- | --- | --- |
| [TODO] | [TODO] | [TODO] | [TODO] |
