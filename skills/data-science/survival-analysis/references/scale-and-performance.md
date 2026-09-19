# Scale and Performance

Load this when cohort size, expanded row count or runtime constrains the analysis.
Two tiers are covered: a single workstation, typically up to a few hundred thousand
subjects, which is the common case; and a warehouse or cluster for millions of
subjects. Most of the material addresses the first, because that is where a
tractable problem is most often made intractable by an avoidable choice.

Nothing here changes the estimand rules in the design reference. A design that
makes a fit affordable by changing what is observed or modelled must be reported as
an explicit design decision, not applied silently as an optimisation.

## Size the Problem Before Optimising

Record these before changing anything, because they identify which cost dominates:

| Quantity | Why it drives cost |
| --- | --- |
| Subjects | Sets the upper bound on independent information |
| Events, by type | Governs precision, estimable parameters and supported horizons |
| Distinct event times | Affects tie handling and the number of event-time updates |
| Expanded rows | Start-stop and person-period rows, not subjects, size the fit |
| Design-matrix width | High-cardinality categorical encodings multiply memory |
| Prediction and metric grid points | Multiply evaluation and output size |

Fit once on a random subsample of subjects to obtain a runtime and memory reading,
then extrapolate. A subsample used for timing is not a subsample used for
estimation; discard the timing fit.

## What Actually Grows

- **Risk sets.** Cox partial likelihood cost is implementation-dependent. Efficient
  implementations update cumulative risk-set sums instead of rescanning every full
  risk set, but each iteration still depends on row count, design-matrix width and
  Hessian work. Delayed entry and start-stop data add bookkeeping. Tie handling can
  add further cost, and exact methods on heavily tied data are far more expensive
  than the usual approximations.
- **Start-stop expansion.** Rows equal subjects multiplied by intervals per subject.
  A daily time-varying covariate over three years of tenure for 200,000 subjects is
  of the order of 200 million rows. Compute this product before expanding.
- **Design matrix.** Dense memory is roughly rows times columns times the element
  size. One-hot encoding a high-cardinality categorical feature can dominate both
  memory and fit time.
- **Prediction output.** Predicting survival functions for $n$ subjects over a
  $k$-point grid returns $n \times k$ values. Requesting the full event-time grid
  makes $k$ the number of distinct event times.
- **Evaluation.** Censoring-weighted metrics cost grid size times evaluation size.
  Pairwise concordance is quadratic in the worst case unless the implementation
  uses a sorted or tree-based algorithm; check before assuming it is cheap.

## Single-Workstation Performance Choices

Separate computational representation from a change to the observation or model
specification. The latter can change an estimate, prediction or decision scope and
needs scientific justification before it is used to save runtime.

| Choice | Computational effect | Analytical boundary |
| --- | --- | --- |
| Use the implementation's documented efficient or batched fit path | May reduce runtime with many ties | Confirm that it preserves the selected estimator and tie method |
| Use a sparse representation where supported | Can reduce design-matrix memory | Representation alone does not change the model |
| Select columns explicitly | Reduces matrix width | Omitted predictors change an adjusted association or prediction model; choose them from the estimand and training-only process |
| Restrict prediction or metric grids | Reduces output and evaluation cost | Changes only reported horizons when horizons were agreed before fitting; do not replace an unsupported target silently |
| Round event time | Reduces distinct times but creates ties | Changes observed event times and risk sets; justify the resolution and assess tie handling |
| Coarsen covariate intervals | Reduces start-stop rows | Changes exposure measurement unless intervals are already bounded by the same covariate changes; preserve availability at interval start |
| Group rare categories | Reduces matrix width | Changes contrasts and may hide heterogeneity; define the rule without looking at held-out outcomes |
| Stratify rather than interact | Avoids estimating interaction terms | Changes estimable effects: stratification gives separate baseline hazards and no hazard ratio for that factor |

Budget tuning explicitly as folds multiplied by path length multiplied by fit cost.
Penalisation is not free, and a tuning loop is usually the largest cost.

## Sampling Designs Need a Design-Specific Estimator

Use a sampling design when the full cohort will not fit or finish. Sampling does
not inherently change the scientific estimand, but it changes what is observed and
requires an estimator and variance procedure designed for that sampling scheme.
Do not transfer an offset, a weight or a correction from one design or learner to
another by analogy. Document the inclusion rule, inclusion probabilities, seed,
analysis estimator, variance method and any absolute-risk recovery.

| Design | Idea | Typical target | Required analysis decision |
| --- | --- | --- | --- |
| Event-enriched cohort sample | Retain all events and sample non-events | Depends on the model and correction | Match the sampling rule to an estimator that supports its weights or sampling mechanism; establish separately whether absolute risk is recoverable |
| Nested case-control | Sample controls from each event's risk set | Cause-specific relative effects | Use risk-set-matched sampling and its corresponding partial-likelihood analysis; derive absolute risks only with an appropriate additional procedure |
| Case-cohort | Random subcohort plus all cases | Relative effects, potentially across outcomes | Use a case-cohort estimator with the required subcohort indicators, cohort sizes and design-based variance |
| Person-period aggregation | Collapse the risk process to periods | Discrete-time hazard and survival | Choose period length and a binary-outcome likelihood that represent the interval hazard; handle any row sampling using a method documented for that learner |

Randomly sampling subjects may discard rare events and is not a default substitute
for one of these designs. Prefer a design that retains every event when that fits
the question.

Never reduce cost by dropping censored subjects, silently truncating follow-up,
deduplicating start-stop rows, or removing subjects whose follow-up makes a metric
inconvenient. Those change the answer without changing a stated design.

## Discrete-Time Person-Period as the Scalable Route

Aggregate the cohort to rows of one subject in one period while at risk, carrying
the period indicator, the features known at the period start, and a binary event
flag for that period. Model the interval hazard
$q_j = P(T \text{ in interval } j \mid T \text{ not earlier}, X)$ with any
binary-outcome learner, then form survival as $S_j = \prod_{m \le j}(1 - q_m)$.

This scales for practical rather than statistical reasons: the aggregation can run
where the data already lives, the fit becomes an ordinary binary problem with
mature large-scale tooling, and period granularity is a direct cost control. Any
row sampling remains a sampling design that needs a learner-specific correction
and validation; it is not an automatic offset.

The cautions in the methods reference still apply in full. Include period or time
effects, keep only at-risk rows, create no rows after an event or censoring, and
split by subject rather than by row. Row count remains subjects multiplied by
periods, so choose the period length as a modelling decision.

## Escalating to a Warehouse or Cluster

- Build the cohort, event and person-period tables where the data resides, and
  export only the columns the analysis uses.
- Prefer moving an aggregated or designed sample over moving every row. The
  export step, not the fit, is usually the bottleneck.
- Kaplan-Meier and cumulative incidence need only a risk table of times, numbers at
  risk and event counts. Both can be computed from grouped aggregates, so
  descriptive work scales by aggregation without moving row-level data.
- Keep a single-node replication on a sample for diagnostics that need per-subject
  residuals or influence measures, which do not aggregate.
- Score in batch, partition by scoring date, and record feature freshness so the
  prediction-time information rule in the design reference still holds.

## Evaluating at Scale

- Evaluate on a few decision-relevant horizons rather than a dense grid.
- Subsample the evaluation cohort for pairwise metrics, and report the subsample
  size and seed. Do not subsample the training outcomes that define the censoring
  distribution; that changes the estimator rather than its cost.
- Bootstrap cost is replicates multiplied by fit cost. Resample the independent
  unit, and consider a cheaper fixed-model interval when refitting is unaffordable.
  State which one was used.
- Subgroup and calendar-period reporting multiplies evaluation cost by the number
  of cells, and small cells remain unreliable however large the parent cohort is.

## What Scale Does Not Fix

More rows are not more events. Precision, the number of estimable parameters and
the range of supported horizons are governed by event count and follow-up. A
50-million-row start-stop table containing 3,000 events supports roughly the model
complexity that a 200,000-row baseline table with 3,000 events supports. Growth in
row count also has no bearing on leakage, informative censoring or the validity of
the observation schema: a larger cohort makes a design error more expensive, not
less likely.
