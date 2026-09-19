# Methods and Interpretation

## Method Selection

| Need | Starting method | Check before proceeding |
| --- | --- | --- |
| Describe single-event survival | Kaplan-Meier with confidence intervals and risk table | Censoring, entry and late follow-up support |
| Unadjusted group comparison | KM plus log-rank; consider RMST contrasts | Crossing hazards, confounding and agreed horizon |
| Adjusted association or transparent prediction | Cox PH, with penalisation/nonlinear terms when justified | PH, functional form, dependence and convergence |
| Time-ratio interpretation | Appropriate AFT model | Distribution, scale specification and estimable quantiles |
| Non-PH | Time interactions, stratification or flexible models | Which effects must be estimated; not every AFT model removes PH |
| Extrapolation | Defensible parametric or flexible parametric model | External evidence and sensitivity to tail assumptions |
| Cause-specific absolute risk | Aalen-Johansen/CIF; suitable regression | Preserve competing causes and align prediction estimand |
| Nonlinear prediction | Survival forests or boosting against a baseline | Tuning design, calibration and probability output support |
| Period-based decisions | Discrete-time survival | At-risk person-period rows, censoring within intervals and entity grouping |
| Repeated events or transitions | Recurrent-event or multi-state model | Risk-set definition, event order and terminal events |

## Kaplan-Meier, Log-Rank and Restricted Mean

At distinct event times $t_j$, with $d_j$ events and $n_j$ at risk just before:

$$
\widehat S(t)=\prod_{t_j\leq t}\left(1-\frac{d_j}{n_j}\right).
$$

Censoring changes later risk sets; it does not itself cause a survival drop.
Report confidence intervals, units, censoring marks and numbers at risk. The
estimated median is the first time the curve reaches or falls below 0.5, not
necessarily a time where it equals exactly 0.5. If it never reaches 0.5, report
"not reached within follow-up", not an infinite real-world lifetime.

Restricted mean survival time is
$\operatorname{RMST}(\tau)=\int_0^\tau S(t)\,dt$: expected event-free time up to a
specified supported horizon. It is not the unrestricted mean lifetime. Justify
$\tau$ before comparing groups and report uncertainty for the contrast.

The log-rank test assesses evidence against equal survival functions; failure to
reject does not establish equality. It is especially effective under PH, can lose
power when hazards cross, and does not quantify a treatment effect. If justified,
pre-specify a weighted test or an RMST contrast rather than choosing the most
significant test afterwards. Neither adjustment nor randomisation is supplied by
the test itself.

## Cox PH

$$
h(t\mid X)=h_0(t)\exp(X^\mathsf{T}\beta).
$$

The baseline hazard is unspecified in ordinary semi-parametric Cox regression.
Software may centre predictors, so its stored baseline need not correspond to
literal zero-valued predictors. Check the implementation before interpreting it.

For a one-unit contrast without relevant interactions, $\exp(\beta_j)$ is a
conditional hazard ratio. Report the unit, reference, adjustment set and confidence
interval. An HR of 0.70 describes a 30% lower instantaneous event rate under the
model, not 30% fewer events or 30% longer survival. Absolute risk also requires the
baseline survival and a horizon. An adjusted HR is not automatically causal.

Check scaled Schoenfeld residual trends and tests, functional form with suitable
residuals/plots, influential observations, collinearity and convergence. Consider
splines for continuous features rather than arbitrary categorisation. PH concerns
constant relative hazards for the specified contrasts, not a constant baseline
hazard. Crossing KM curves are a clue, not a complete diagnostic.

Choose remedies according to the question:

- Stratify on a nuisance factor to allow separate baseline hazards. This does not
  estimate an HR for that factor; other model assumptions still apply.
- Use time-dependent coefficients or justified time interactions for effects that
  change. Do not manufacture an interaction using each subject's final outcome
  time as a baseline feature.
- Consider alternative models and horizon-specific summaries when a constant HR
  is not useful. Robust standard errors or penalisation do not repair PH.
- Account for dependence when selecting variance estimates, resampling and models.
  A cluster-robust variance estimate and a frailty model answer different questions.

## Worked Contrast: One Model, Four Different Numbers

These values are the population truth of the process in the bundled synthetic
script, not fitted estimates from it: an exponential event time with rate
$0.055\exp(0.7\,\text{monthly\_contract}-0.4\,\text{baseline\_usage})$ per month.
Compare two customers with `baseline_usage` at its mean of 0, one on a monthly
contract and one not, so $S(t)=\exp(-\text{rate}\times t)$ exactly.

| Quantity | Monthly contract | Otherwise | Contrast |
| --- | --- | --- | --- |
| Monthly event rate | 0.1108 | 0.0550 | Hazard ratio 2.01 |
| Event probability by 3 months | 28.3% | 15.2% | Ratio 1.86, difference 13.1 points |
| Event probability by 12 months | 73.5% | 48.3% | Ratio 1.52, difference 25.2 points |
| Median time to event | 6.26 months | 12.60 months | Time ratio 0.50 |

One constant hazard ratio of 2.01 therefore produces a risk ratio of 1.86 at three
months and 1.52 at twelve, because the risk ratio must approach 1 as both
probabilities approach certainty. The hazard ratio is not a risk ratio, it is not a
risk difference, and it is not a ratio of survival times. Which of these four
numbers a stakeholder needs depends on the decision: a targeting rule needs the
absolute probability at an actionable horizon, a capacity plan often needs the
difference, and only an effect summary needs the ratio itself.

Because this generating process is exponential, it is simultaneously PH and AFT,
so the time ratio is exactly the reciprocal of the hazard ratio here. That identity
is a property of this distribution, not a general conversion rule.

## Parametric and AFT Models

| Distribution | Typical baseline hazard behaviour |
| --- | --- |
| Exponential | Constant |
| Weibull | Increasing, decreasing or constant |
| Gompertz | Exponentially increasing/decreasing; check parameter-domain implications |
| Log-normal | Rises and then falls |
| Log-logistic | Decreasing or rises then falls, depending on shape |

For an AFT model $\log T=\beta_0+X^\mathsf{T}\beta+\sigma\epsilon$ with a common
error distribution and scale, $\exp(\beta_j)$ multiplies corresponding event-time
quantiles for a one-unit contrast. It also scales a finite mean when that mean
exists under the model. Do not universally describe it as an expected-lifetime
ratio, especially for heavy tails or covariate-dependent ancillary parameters.

The usual Weibull regression form is both AFT and PH; selecting it does not by
itself solve a PH violation. A flexible baseline alone also does not create
time-varying effects. Compare plausible distributions and extrapolated tails,
validate within observed support, and distinguish evidence from extrapolation.

## Competing Risks

For event type $k$, the cause-specific hazard describes its instantaneous rate
among subjects still free of every event. A cause-specific Cox fit removes other
causes from its risk set at their event time, coded as censored for that fit.
This is appropriate for estimating that cause-specific hazard; independence of
hypothetical latent competing failure times is not required for this observed
hazard estimand. Independent observation censoring is a separate assumption.

Actual cause-specific probability is the cumulative incidence function:

$$
F_k(t)=P(T\leq t,J=k)=\int_0^t S(u-)\,d\Lambda_k(u),
$$

where $S$ is survival free of **all** causes. Aalen-Johansen estimates cumulative
incidence; cause-specific regression can yield CIF predictions by combining all
relevant cause hazards. One minus cause-specific KM instead estimates a net-risk
quantity, not the observed-world CIF, and generally overstates the latter.

Fine-Gray models the subdistribution hazard, using a modified risk set that
retains people with competing events in a weighted sense. Its hazard ratio is
neither a cause-specific HR nor a probability ratio. Check its proportionality
assumption and explain the estimand explicitly. Neither hazard model is
automatically a causal model; time-dependent covariates require particular care.

## Changing Covariates and Repeated Events

$X(t)$ changing over time differs from $\beta(t)$ changing over time. Start-stop
data represent the former; a time-varying coefficient specification addresses the
latter. Never use information measured after the start of an interval to predict
events in that interval unless the observation design explicitly justifies it.

For recurrent events, choose the risk process rather than merely duplicating rows:

- Andersen-Gill uses a counting-process formulation on total time, with appropriate
  dependence handling and assumptions about event history.
- Prentice-Williams-Peterson conditions risk sets on prior event occurrence; choose
  total-time or gap-time formulation and retain event order.
- Frailty introduces latent heterogeneity, often shared within a cluster. A
  positive multiplicative frailty can be expressed as $\exp(u)$; specify its
  distribution and distinguish conditional from population-level effects.
- Multi-state models represent transitions such as active, inactive and closed.
  State occupancy is not always the same target as time to first event.

A terminal event can stop recurrence. Do not assume ordinary censoring handles
that dependence; seek an appropriate joint or multi-state formulation.

## Discrete-Time and Machine Learning Models

For intervals $j$, model $q_j=P(T\text{ in interval }j\mid T\text{ not earlier},X)$
and form $S_j=\prod_{m\leq j}(1-q_m)$. Include interval/time effects and only
eligible at-risk rows. Do not create negative rows after censoring or an event.
Define how partially observed intervals are handled; separate people, not just
person-period rows, across validation folds. This formulation is also the most
practical route for a very large cohort; see
[scale and performance](./scale-and-performance.md).

Survival forests, boosting and neural models can capture nonlinearities and
interactions, but do not remove censoring assumptions or identify causal effects.
Verify each implementation's output: a risk score is not a probability, and some
models require extra fitting to obtain survival curves. Keep a transparent
baseline and scale model complexity to event information, not merely row count.
