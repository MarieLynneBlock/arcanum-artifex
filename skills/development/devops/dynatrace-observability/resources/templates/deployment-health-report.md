# Deployment Health Report

## Verdict

- Verdict: [healthy | watch | degraded | rollback-candidate | blocked]
- Deployment window: [timestamp/window]
- Baseline window: [timestamp/window]
- Scope: [service/entity/environment]
- Confidence: [high | medium | low]

## Metric Comparison

| Metric | Baseline | Post-deployment | Change | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Request rate | [value] | [value] | [value] | [note] |
| Failure rate | [value] | [value] | [value] | [note] |
| P95 latency | [value] | [value] | [value] | [note] |
| P99 latency | [value] | [value] | [value] | [note] |

## Problems and Exceptions

- Active problems before deployment: [summary]
- New problems after deployment: [summary]
- New exception types after deployment: [summary]

## Recommendation

[Continue rollout, pause, watch, block, or rollback recommendation.]

## Incomplete Data and Watch Criteria

- Missing or restricted access: [none/details]
- Ambiguous deployment marker or scope: [none/details]
- Inconclusive comparisons: [none/details]
- Watch criteria: [metric/problem/exception threshold and timeframe]
- Next check to reduce uncertainty: [query/command/access request]

## Evidence

- DQL used: [query/resource summary]
- dtctl commands used: [command summary]

## Assumptions and Limitations

- [Assumption]
- [Missing data or comparison caveat]
