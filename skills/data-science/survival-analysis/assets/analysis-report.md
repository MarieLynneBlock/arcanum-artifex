# Survival Analysis Evidence Report

Use only the sections that communicate the requested evidence. This is not a
required report: copy relevant prompts into the project's existing artefact and
remove irrelevant sections. Do not imply that unperformed checks passed. Use
`[TODO]` only for material unresolved items.

## Decision Summary

- Question, intended decision and analysis scope: [TODO]
- Population, event, time origin, units and estimand: [TODO]
- Main finding with uncertainty and supported horizon: [TODO]
- Recommendation, limitations and remaining decision: [TODO]
- Strength of evidence and unresolved analysis questions: [TODO]

## Cohort and Observation Evidence

| Item | Evidence |
| --- | --- |
| Data/query version, extraction and label cut-offs | [TODO] |
| Subjects, episodes, exclusions and reconciliation | [TODO] |
| Events by type, censoring reasons and follow-up | [TODO] |
| Competing events, delayed entry and dependence | [TODO] |
| Cohort size, expanded rows and any sampling design applied | [TODO] |
| Sampling inclusion rule/probabilities, estimator and variance method | [TODO] |
| Data-quality failures and resolutions | [TODO] |
| Leakage and outcome-availability checks | [TODO] |
| Remaining censoring/selection assumptions | [TODO] |

## Model and Diagnostics

- Method, rationale and baseline comparison: [TODO]
- Predictor specification, transformations and tuning: [TODO]
- Convergence warnings, PH/functional-form checks and resulting action: [TODO]
- Sensitivity analyses, including any extrapolation: [TODO]
- Effect interpretation, reference groups and uncertainty: [TODO]
- Association, prediction or causal claim and its justification: [TODO]

## Prediction Evidence

Omit this section when prediction is outside scope. Name the validation design,
censoring estimator, integration interval and support checks before quoting scores.

| Population / horizon | Subjects / events / at risk | Baseline | Model | Uncertainty / limitations |
| --- | --- | --- | --- | --- |
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

- Discrimination estimator and result: [TODO]
- Probability error and calibration evidence: [TODO]
- Subgroup/calendar-period results and unsupported horizons: [TODO]
- Decision usefulness and decision criteria, when applicable: [TODO]

## Reproduction and Handover

- Code revision, execution command and runtime: [TODO]
- Package versions, seed, split membership and model settings: [TODO]
- Figures/tables and aggregate output locations: [TODO]
- Checks actually run, failures and checks not run: [TODO]
- Scoring time, eligibility, feature freshness and label maturation: [TODO]

## Review Findings

| Severity | Evidence / location | Consequence | Suggested correction |
| --- | --- | --- | --- |
| [TODO] | [TODO] | [TODO] | [TODO] |

Separate blockers from suggestions. A successful synthetic smoke test establishes
that example code runs in one environment; it does not validate the real cohort,
scientific assumptions or model quality.
