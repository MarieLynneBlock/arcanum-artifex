# Evaluation and Reporting

## Validation Design Comes First

For prediction, agree who will be scored, when, using which available information,
and over which future horizons. Use a calendar backtest for future deployment when
appropriate; use grouped validation for dependent entities. Random splits are
reasonable only when the intended generalisation and independence assumptions
justify them. A row split of start-stop or repeated-episode data leaks subjects.

Freeze preprocessing, feature selection and tuning inside training folds. For a
historical deployment date, training outcomes must have been available by that
date; a later label freeze can leak even with correctly timestamped features.
Keep a final evaluation set untouched by model or threshold selection.

For association or descriptive work, use design-appropriate inference, diagnostics
and sensitivity analysis. A held-out prediction score does not validate an
association estimate, and train/test splitting is not obligatory for every study.

## Use Complementary Metrics

| Metric | What it assesses | Main caution |
| --- | --- | --- |
| Harrell's C-index | Ranking among comparable pairs | Can be biased with substantial censoring; not calibration |
| IPCW / Uno-type concordance | Censoring-adjusted ranking over a defined range | Requires supported censoring weights and a named truncation horizon |
| Cumulative/dynamic AUC at time $t$ | Events by $t$ versus event-free beyond $t$ | Needs cases, controls and a specified censoring estimator |
| Time-dependent Brier score | Censoring-adjusted probability error | Depends on discrimination and calibration; not a pure calibration test |
| Integrated Brier score | Probability error over a specified interval | Compare the same grid, integration rule and interval |
| Horizon-specific calibration | Agreement between predicted and observed risk | Observed risk must account for censoring and competing events |
| Decision usefulness | Consequences of acting on predictions | Needs agreed costs, capacity and evidence relevant to the intervention |

Report the exact estimator, time units, horizon/grid, sample, event counts,
censoring model, software version and uncertainty. A C-index near 0.5 indicates
chance ranking in the usual setting; a value of 1 does not certify accurate risks.
Do not introduce a universal "good model" C-index, AUC or Brier threshold.

Metric APIs use different score directions. In scikit-survival, larger risk scores
mean earlier events for concordance and AUC. In `lifelines.utils.concordance_index`,
larger predicted scores mean longer survival; negate a partial-hazard score there.
Check the API instead of negating every score by convention. Brier APIs may expect
survival probabilities, not event probabilities or hazard scores.

## IPCW Support and Failure Handling

Let $G(t)$ be the probability of remaining uncensored through $t$. Inverse
probability of censoring weighting needs nonzero $G$ at all times used by the
estimator, and very small $G$ creates unstable weights. A pooled Kaplan-Meier
censoring model requires stronger independence assumptions than a correctly
specified conditional model. A library's pooled implementation does not solve
covariate-dependent censoring automatically.

Before calling an IPCW metric:

1. Confirm the estimator matches the observation scheme. Standard single-event,
   right-censored metrics are not automatically valid for competing risks, delayed
   entry or recurrent events.
2. Specify where the censoring distribution is estimated. Scikit-survival APIs use
   the training outcomes passed as their first argument; retain fold boundaries
   and justify transport of that censoring distribution to the evaluation cohort.
3. Verify all required follow-up times lie within supported ranges. Some APIs need
   support at evaluation subjects' observed times as well as requested horizons.
4. Inspect $\widehat G$, event/control counts and numbers at risk across the grid.
   Nonzero weights alone do not guarantee a useful or stable estimate.
5. Check prediction shape, subject alignment, ordering of times, finite values,
   bounds $[0,1]$ and non-increasing survival curves.

If support fails, report which population or horizon is unsupported. Do not drop
long-followed subjects, clip event times, pool held-out labels into a training
censoring estimator, or catch an exception and substitute an ordinary metric.
An explicitly agreed administrative truncation can define a different evaluation
target, but must consistently update duration and event status and be reported.
It is not an invisible numerical repair.

## Calibration at Actionable Horizons

For each agreed horizon, compare predicted risk with censoring-aware observed
risk on evaluation data. For a suitable single-event setting, KM within risk groups
can provide an illustrative comparison if censoring is independent within groups.
For competing events, use the appropriate CIF instead. Show uncertainty and
numbers contributing; do not treat people censored before the horizon as event-free.

Grouped plots depend on binning and can hide miscalibration. Prefer a justified
smooth calibration approach where support permits; report calibration-in-the-large
and slope when estimable with a survival-appropriate method. Recalibration is model
fitting: perform it on a separate calibration/training sample and evaluate it
independently. Do not correct and score on the same held-out observations.

Benchmark against a simple model fit on training data, such as a common KM curve
for ordinary single-event prediction. A KM estimator fit to the test outcomes is
an observed-risk estimate, not an independently trained predictive baseline.

## Uncertainty, Drift and Usefulness

Resample the independent unit or cluster, not individual start-stop rows. State
whether intervals condition on a fixed model or include model refitting and tuning.
For comparisons, use paired evaluation samples and report differences with
uncertainty. Do not present overlapping marginal intervals as a formal test.

Inspect calibration and discrimination by meaningful cohort, calendar period and
subgroup when supported. Report sparse groups without unreliable precision and
respect privacy rules for small cells. For deployment, record scoring eligibility,
feature freshness and event/label maturation. Delayed labels
mean recent apparent performance may be incomplete. A shift in features alone is
neither proof nor disproof of outcome-model failure.

If a business threshold selects whom to contact, distinguish risk calibration
from intervention effectiveness and cost. Do not infer uplift from a churn model.
Derive evaluation criteria from the intended decision rather than universal limits.

## Minimum Evidence by Task

| Task | Evidence to return |
| --- | --- |
| Cohort/design | Estimand, data contract, reconciliation and unresolved decisions |
| Descriptive analysis | Survival/CIF curves, confidence intervals, risk tables and supported summaries |
| Cox association | Effect units/references, uncertainty, diagnostics and censoring/dependence assumptions |
| Prediction | Leakage-safe validation, baseline, discrimination, probability error and calibration |
| Advanced observation scheme | Risk-set definition, compatible method/metrics and specialist limitations |
| Model handover | Data/query and label versions, split, runtime, reproducible code and limitations |
| Review | Severity-ranked findings, evidence, consequence and correction; checks actually performed |

The useful default visual set is survival or CIF curves, accompanying numbers at
risk, and horizon-specific calibration for prediction. For Cox work, include PH
diagnostic plots. Explain sparse tails and unsupported horizons in the report.
