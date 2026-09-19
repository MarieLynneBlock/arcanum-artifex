# Implementation

## Library Compatibility

Inspect the project's interpreter and installed package versions first. Use Python
primarily; preserve an established R analysis when appropriate. Verify API support
for the observation scheme before fitting. Report missing prerequisites rather
than installing them automatically.

For Python, `lifelines` provides descriptive and regression methods;
`scikit-survival` provides survival estimators and evaluation APIs. They are not
interchangeable for every censoring scheme. In R, `survival` provides `Surv`,
`survfit`, `coxph`, `cox.zph` and `survreg`. Verify support for the installed version,
particularly for interval censoring, entry, competing events and time-varying data.
The presence of a similarly named method does not establish estimator compatibility.

## How This Reference Names APIs

Guidance here states the capability an implementation must provide rather than a
class to call, so that it survives version changes and suits whichever libraries a
project has already standardised on. The few names that do appear are illustrative,
long-stable entry points offered as a starting point for a search, not a claim that
the installed version behaves as described. Always confirm the estimand, assumptions
and argument semantics in the installed version's own documentation before fitting.
Dependencies are deliberately unpinned: adopt the project's existing environment
manager rather than introducing one.

## Executable Python Example

From the skill folder, in an environment containing
`lifelines`, `scikit-survival`, `numpy` and `pandas`, run:

```shell
python scripts/synthetic_workflow.py
```

Adding `-W error` is the authoring-time check used when maintaining the script. It
turns any unrelated upstream deprecation warning into a failure, so a plain run is
the expected user invocation.

The bundled script:

- Generates independent training and test subjects from a known PH process,
  baseline features and independent dropout with administrative censoring at
  24 months. The domain labels are illustrative, not a churn definition.
- Checks the one-row-per-subject contract and selects predictor columns explicitly,
  excluding identifiers and outcomes from predictors.
- Rejects missing/invalid event codes, negative duration and an unsupported horizon;
  normalises validated `0/1` event flags to Boolean before scikit-survival calls.
- Checks censoring support before Brier evaluation and never edits outcomes to
  make the metric run. Positivity is only a numerical prerequisite; no universal
  stability threshold is inferred from the printed minimum.
- Fits a Cox model and a training-only KM baseline; reports Harrell concordance
  from both libraries and IPCW Brier scores at 3, 6 and 12 months.
- Checks score direction against both libraries and verifies probability bounds,
  monotonicity, dimensions and row alignment.
- Prints a rank-transformed Schoenfeld test and illustrative grouped calibration
  with KM confidence intervals and numbers at risk; it reports tied score groups
  or group-level unsupported horizons instead of fabricating a calibration estimate.

It writes no files and does not install packages. Its assertions are smoke checks,
not model-quality acceptance criteria. It does not establish causal effects,
validate real data, test every supported method or replace graphical diagnostics.

Tested with warnings treated as errors on Python 3.12.10, lifelines 0.30.3,
scikit-survival 0.28.0, pandas 2.3.3 and NumPy 2.5.3. These versions are a
compatibility reference, not a requirement to upgrade an existing project.

For a real project, replace the independent synthetic cohorts with an agreed
temporal/grouped design. Add the project's transformations within training folds,
the agreed uncertainty procedure and supported horizons. The synthetic example's
guard is deliberately limited to baseline, right-censored single-event data;
do not repurpose it as a general censoring or interval validator.

## Observation Scheme and API Route

Choose the data contract before selecting an API. The following are starting points,
not evidence that a particular installed version supports the required estimand.

| Observation scheme | Minimum data | Python starting point | R starting point |
| --- | --- | --- | --- |
| Baseline, right-censored single event | duration, event, baseline features | `KaplanMeierFitter`, `CoxPHFitter` | `Surv(duration, event)`, `survfit`, `coxph` |
| Delayed entry | entry, exit, event | `entry_col` where supported | `Surv(entry, exit, event)` |
| Changing covariates | ID, start, stop, event, features | `CoxTimeVaryingFitter` | `coxph(Surv(start, stop, event) ~ ...)` |
| Interval censoring | lower and upper bounds, features | a version-supported interval-censoring fitter | `Surv(lower, upper, type = "interval2")` with a compatible model |
| Competing events | duration, event type | CIF/Aalen-Johansen-capable library | an installed competing-risks package with a documented estimand |

Verify the installed API and its assumptions before fitting. Do not encode an
unsupported scheme as ordinary right-censored data merely to reuse a familiar call.

## Capability Checks for the Advanced Methods

Every method this skill covers needs an implementation with specific properties.
Establish these before writing code; a missing property is a reason to change
method or library, not to approximate.

| Method | The implementation must | Establish this by |
| --- | --- | --- |
| Delayed entry | Add a subject to risk sets only from entry | Comparing early at-risk counts against a hand calculation |
| Interval censoring | Carry both bounds into the likelihood | Confirming no midpoint substitution occurs internally |
| Competing-risks regression | State whether coefficients are cause-specific or subdistribution, and produce CIF predictions when the target is absolute risk | Reading the documented estimand, then checking predicted CIFs across causes do not exceed $1-S(t)$ when CIFs are produced |
| Recurrent events | Accept counting-process rows and handle within-subject dependence compatibly with the selected formulation | Confirming the dependence and variance approach, and that the risk-set rule matches the chosen formulation |
| Multi-state | Accept transition definitions and report transition-specific hazards | Checking state-occupancy output exists, not only first-event survival |
| AFT and time ratios | Expose the error distribution and scale, and predict quantiles | Checking whether coefficients are reported on the log-time scale |
| Discrete-time | Nothing survival-specific: any binary-outcome learner on at-risk person-period rows | Confirming a time effect is in the model and survival is formed as a product |
| Forests and boosting | Output survival or cumulative-hazard functions, not only a risk score | Looking for a survival-function prediction method before attempting calibration |
| Censoring-weighted metrics | Let you control where the censoring distribution is estimated | Identifying which argument supplies the training outcomes |

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Fit does not converge; step or delta contains NaN | Separation, collinearity, extreme scale, or a covariate that orders event times almost perfectly | Check for leakage first, then centre and scale, drop collinear columns; penalise only after excluding leakage |
| A coefficient is enormous with an enormous standard error | Complete or quasi-complete separation, usually in a sparse-event category | Collapse sparse categories on a documented rule, or use a penalised fit and report it |
| Singular matrix or linear-algebra error | Linearly dependent columns, often a full one-hot set with no reference level | Drop the redundant column |
| Metric rejects a requested time | The horizon exceeds evaluation follow-up support | Diagnose the exact support failure and report the original target as unsupported; change to a new horizon only by explicit agreement, never by clipping durations or dropping long-followed subjects |
| Censoring probabilities near zero; unstable weights | Little uncensored follow-up near the horizon | Report the target as unsupported or unstable and investigate its support; use another horizon only by explicit agreement |
| Calibration groups collapse | Tied or near-constant predicted risks | Report the tie; do not force bins |
| A subgroup curve stays flat at 1 | No observed events in that subgroup | Report follow-up, numbers at risk and uncertainty; distinguish zero observed events from lack of support before interpreting it |
| Memory error while expanding start-stop data | Rows are subjects multiplied by intervals | Coarsen intervals; see [scale and performance](./scale-and-performance.md) |
| Fit runs for hours | Many distinct event times, wide design matrix, or an unbudgeted tuning loop | Size the problem first; see [scale and performance](./scale-and-performance.md) |
| PH test is significant but the residual trend looks flat | Test power grows with event count | Judge by plot and effect magnitude, not the p-value alone |
| Predicted survival is not monotone or falls outside [0, 1] | Wrong output type, transposed array, or misaligned subject order | Check the prediction's orientation and index against the input |

For the visual review, use `KaplanMeierFitter.plot_survival_function` with censor
marks and `lifelines.plotting.add_at_risk_counts`. Inspect Cox residual plots using
the installed version's `check_assumptions` API, not just its printed verdict.
Plot predicted versus censoring-aware observed risk with uncertainty at the agreed
horizons; grouped calibration is illustrative, not a complete calibration study.
Use CIF plots instead of one minus KM for a competing-risk probability target.

## Quick Plotting Recipes

Use the project's plotting conventions and save or display figures according to its
existing workflow. This baseline right-censored example is intentionally small:

```python
from lifelines import KaplanMeierFitter
from lifelines.plotting import add_at_risk_counts

km = KaplanMeierFitter().fit(data["duration"], data["event"], label="All subjects")
axis = km.plot_survival_function(show_censors=True)
add_at_risk_counts(km, ax=axis)
```

For a Cox model, review graphical as well as numerical PH diagnostics:

```python
model.check_assumptions(training_data, p_value_threshold=0.05, show_plots=True)
```

Treat the printed threshold as a prompt for investigation, not an automatic model
decision. For competing-risk probabilities, plot a CIF rather than $1 - \widehat S(t)$
from a cause-specific Kaplan-Meier curve.

## Secondary R Example

The R path is deliberately secondary: it exists so an established R analysis can be
supported, and it does not reach parity with the Python path. This is a synthetic
baseline Cox and PH-diagnostic example, not a complete
prediction evaluation. It requires an installed `survival` package and does not
install anything. The APIs were checked against the official documentation, but
the code has not been execution-tested. Run and review it before reuse.

```r
if (!requireNamespace("survival", quietly = TRUE)) {
  stop("This example requires the survival package.")
}
library(survival)

set.seed(42)
sample_size <- 800L
monthly_contract <- rbinom(sample_size, 1L, 0.5)
baseline_usage <- rnorm(sample_size)
event_rate <- 0.055 * exp(0.7 * monthly_contract - 0.4 * baseline_usage)
event_time <- rexp(sample_size, rate = event_rate)
censor_time <- pmin(rexp(sample_size, rate = 1 / 36), 24)
cohort <- data.frame(
  duration = pmin(event_time, censor_time),
  event = as.integer(event_time <= censor_time),
  monthly_contract = monthly_contract,
  baseline_usage = baseline_usage
)
stopifnot(
  !anyNA(cohort),
  all(is.finite(as.matrix(cohort))),
  all(cohort$duration > 0),
  all(cohort$event %in% c(0L, 1L)),
  any(cohort$event == 1L)
)

model <- coxph(
  Surv(duration, event) ~ monthly_contract + baseline_usage,
  data = cohort,
  ties = "efron",
  x = TRUE,
  model = TRUE,
  na.action = na.fail,
  singular.ok = FALSE
)
print(summary(model))
ph_diagnostics <- cox.zph(model)
print(ph_diagnostics)
km_curve <- survfit(Surv(duration, event) ~ 1, data = cohort)
print(summary(km_curve, times = c(3, 6, 12)))
print(packageVersion("survival"))
if (interactive()) {
  plot(ph_diagnostics)
  plot(km_curve, xlab = "Months", ylab = "Event-free probability", mark.time = TRUE)
}
```

The concordance in this model summary is in-sample, not held-out performance.
The PH test does not prove proportionality; inspect plots and domain relevance.
For real prediction, add a separate validation design and censoring-aware
calibration/probability error. In `Surv`, verify numeric status coding explicitly;
factors and multi-state responses can change the interpretation of event codes.
Neither this example nor its 24-month follow-up definition applies automatically
to a project dataset.

## Sources

Official API documentation:

- [lifelines CoxPHFitter](https://lifelines.readthedocs.io/en/latest/fitters/regression/CoxPHFitter.html)
- [lifelines survival regression](https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html)
- [scikit-survival evaluation guide](https://scikit-survival.readthedocs.io/en/stable/user_guide/evaluating-survival-models.html)
- [scikit-survival Brier score API](https://scikit-survival.readthedocs.io/en/stable/api/generated/sksurv.metrics.brier_score.html)
- [R survival coxph](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html)
- [R survival cox.zph](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cox.zph.html)

Foundational references:

- Cox, D.R. (1972). Regression models and life-tables. *Journal of the Royal
  Statistical Society: Series B (Methodological)*, 34(2), 187-220.
- Fine, J.P. and Gray, R.J. (1999). A proportional hazards model for the
  subdistribution of a competing risk. *Journal of the American Statistical
  Association*, 94(446), 496-509.
- Harrell, F.E. (2015). *Regression Modeling Strategies*. 2nd edn. Springer.
- Kaplan, E.L. and Meier, P. (1958). Nonparametric estimation from incomplete
  observations. *Journal of the American Statistical Association*, 53(282), 457-481.
- Kleinbaum, D.G. and Klein, M. (2012). *Survival Analysis: A Self-Learning Text*.
  3rd edn. Springer.
- Therneau, T.M. and Grambsch, P.M. (2000). *Modeling Survival Data: Extending the
  Cox Model*. Springer.
