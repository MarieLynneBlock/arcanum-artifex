# Design and Observation Process

## Start With the Decision

| Objective | Target | Important boundary |
| --- | --- | --- |
| Describe retention | Event-free survival in a defined cohort | Not a causal treatment comparison |
| Estimate associations | Conditional hazard or time ratios | Adjustment alone does not remove confounding |
| Predict | Absolute risk or survival at an actionable horizon | Requires deployment-matched validation and calibration |
| Evaluate an intervention | A specified causal contrast | Requires an identification strategy, not just a Cox fit |

For retention targeting, high churn risk does not imply high response to an offer.
Agree whether the action needs risk, expected event-free time, or incremental
intervention benefit. Distinguish the population at enrolment from customers who
have already remained active for several years.

## Core Quantities

For ordinary right-censored data, observe duration $Y=\min(T,C)$ and event
indicator $\delta=I(T\leq C)$, where $T$ is event time and $C$ is censoring time.
An event flag of zero means the event was not observed through $Y$, not that the
event will never happen. Define how equal recorded timestamps are adjudicated.

The survival function is $S(t)=P(T>t)$. For a continuous event-time distribution,

$$
h(t)=\lim_{\Delta t\downarrow0}
\frac{P(t\leq T<t+\Delta t\mid T\geq t)}{\Delta t},\qquad
H(t)=\int_0^t h(u)\,du,\qquad S(t)=\exp[-H(t)].
$$

Hazard is a rate with inverse-time units, not a probability. For discrete time,
use interval event probabilities and their survival product rather than assuming
the continuous-time identity applies unchanged to hazard jumps.

## Choose the Correct Observation Schema

| Observation process | Minimal information | Required handling |
| --- | --- | --- |
| Right censoring | ID, duration, event | Keep event-free follow-up; do not drop censored rows |
| Left censoring | Event known to precede a bound | Use a likelihood/estimator supporting left censoring |
| Interval censoring | Lower and upper event-time bounds | Preserve the interval; do not substitute its midpoint as an exact event |
| Delayed entry / left truncation | Entry and exit on the same time scale, event | Include a subject in risk sets only after entry |
| Competing events | Duration and event type, including a censoring code | Preserve all event types; choose the estimand first |
| Changing covariates | ID, start, stop, event, features | Features must be known at the interval start |
| Recurrent events | ID, episode/event order, risk intervals | Define reset rules, dependence and terminal events |

Truncation is a sampling restriction: some people never enter the dataset.
Censoring leaves a person in the dataset with incomplete event-time information.
Right truncation, where only events before a cut-off are sampled, is not ordinary
administrative right censoring. Obtain specialist input for an unsupported scheme.

Example baseline schema, with time measured in months:

| subject_id | duration | event | baseline_feature |
| --- | --- | --- | --- |
| A | 4 | 1 | 1.2 |
| B | 8 | 0 | 0.7 |

Example changing-covariate schema using intervals $(\text{start},\text{stop}]$:

| subject_id | start | stop | feature_known_at_start | event |
| --- | --- | --- | --- | --- |
| A | 0 | 3 | 120 | 0 |
| A | 3 | 7 | 140 | 0 |
| A | 7 | 9 | 160 | 1 |

Do not propagate the terminal event flag to earlier intervals. Validate positive
interval lengths, ordering and overlaps within each subject. Explain gaps as
periods outside observation or outside the risk set; do not silently fill them.
For first-event analysis, no at-risk rows may follow the terminal event. Row count
here is subjects multiplied by intervals per subject, so compute that product
before expanding a large cohort; see [scale and performance](./scale-and-performance.md).

## Cohort Checks That Change the Answer

1. Reconcile raw subjects, eligibility exclusions, episodes and final counts.
2. Verify event codes from the data dictionary. Missing is neither zero nor false.
3. Check finite durations, units, duplicates and timestamp ordering. Investigate
   zero-time events: rounding, prevalent cases and same-day events need different
   handling. Do not add an arbitrary epsilon to make a model run.
4. Establish the last observable event date for each source and subject. Database
   extraction time is not necessarily the end of reliable outcome ascertainment.
5. Align entry, exit and prediction time to the same origin. A cohort of existing
   customers may require delayed entry on an account-age time scale.
6. Count events and censoring by type, subgroup and calendar cohort. Examine risk
   tables before interpreting a long tail. Report follow-up explicitly; reverse
   Kaplan-Meier is an option for describing potential follow-up, not event survival.

## Churn Definitions Need Particular Care

- **Cancellation:** distinguish request date, confirmation and contract end.
- **Non-renewal:** define the renewal opportunity, grace period and when the label
  becomes known. Annual and monthly contracts may have different event opportunities.
- **Inactivity:** if churn means 90 days without activity, confirm the full window.
  Decide whether event time is the threshold date or a retrospectively inferred
  date. Do not leak the later confirmation into earlier backtests.
- **Reactivation:** decide between first churn, repeated churn and transitions
  between active/inactive states. These are different analyses.
- **Upgrade:** not automatically a competing event. It competes only if it
  precludes the defined event in the defined episode. Otherwise it may change
  a covariate, state or eligibility rule.

## Censoring Is an Assumption About Observation

Unadjusted Kaplan-Meier needs an appropriate independent-censoring assumption
within the analysed population or groups. Independence conditional on predictors
may justify regression or conditional weighting without justifying pooled KM.
Administrative censoring is not automatically harmless if calendar changes relate
entry time to event risk. Entry itself also needs an appropriate independent
truncation assumption; adjusting risk sets is necessary but not always sufficient.

Compare censoring patterns by reason and known predictors, investigate dropout
using domain knowledge, and assess whether unrecorded events can still be ascertained.
No plot or significance test proves independent censoring. Plausible informative
dropout may require conditional inverse-probability weighting, joint models or
scenario sensitivity analyses. State positivity and model assumptions; weights
cannot identify risk where nobody remains observable.

## Temporal Leakage and Immortal Time

Keep measurement time, availability time, prediction time and outcome-label
availability separate. Exclude later support contacts, final account tenure,
post-event laboratory values and future-derived aggregates from baseline features.

An "ever received treatment/offer" baseline flag assigns pre-treatment survival to
the treated group. This can create immortal-time bias. Use an appropriate
time-varying exposure, landmark or causal design; do not simply relabel everyone
who eventually receives treatment as treated at time zero.

For dynamic prediction, specify the landmark, eligible event-free population and
history available then. A time-varying Cox model does not magically supply future
covariate trajectories. Predicting forward requires an explicit trajectory
assumption or a model designed for that prediction target.

## Glossary

One line each, with the section or file that develops the term.

| Term | Plain meaning |
| --- | --- |
| Right censoring | Follow-up ended before the event; the event is still possible later. See Core Quantities above |
| Left censoring | The event is known to have happened before a bound, without an exact time |
| Interval censoring | The event happened between two known times; the midpoint is not an observed event |
| Truncation | A sampling restriction: some subjects never enter the data at all |
| Delayed entry (left truncation) | A subject joins the risk set after time zero and contributes nothing before entry |
| Risk set | The subjects still event-free and under observation just before a given time |
| Hazard | An instantaneous event rate among those still at risk; a rate with inverse-time units, never a probability |
| Survival function | The probability of remaining event-free beyond a time |
| Cause-specific hazard | The rate of one event type among subjects free of every event type. See the competing-risks section of the methods reference |
| Subdistribution hazard | The Fine-Gray quantity, using a modified risk set that retains competing-event subjects; its ratio is neither cause-specific nor a probability ratio |
| CIF (cumulative incidence function) | The actual probability of a specific event type by a time, accounting for competing events |
| RMST | Expected event-free time up to a stated horizon; not an unrestricted mean lifetime. See the methods reference |
| Time ratio | An AFT model's multiplier on event-time quantiles for a one-unit contrast |
| Immortal time | A period in which a subject could not have had the event by construction, usually created by using future information to assign a baseline group. See above |
| Landmark | A fixed later time from which prediction starts, using only history available then, among subjects still event-free |
| IPCW | Inverse probability of censoring weighting: reweighting observed cases to stand in for those censored. See the evaluation reference |
| Positivity | Every relevant subject must have a nonzero chance of remaining observed; weights cannot recover information from a region with no observable subjects |
| Concordance | The share of comparable pairs the model ranks in the correct order; a ranking measure, not a calibration measure |
| Calibration-in-the-large | Whether average predicted risk matches average observed risk |
| Calibration slope | Whether predicted risks are too extreme or too compressed across the range |
| Events per parameter | Event count divided by estimated parameters; the practical limit on model complexity |

## Before Implementation

Use the bundled analysis plan to capture unresolved decisions. If the observation
scheme, event definition or label timing is unknown, ask about it before fitting.
A synthetic example can illustrate an API, but cannot resolve those definitions.
