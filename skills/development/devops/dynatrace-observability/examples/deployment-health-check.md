# Example: Deployment Health Check

## User request

"Check whether the deployment at 10:00 UTC made payment-service slower."

## References to load

1. `references/deployment-release-validation.md`
2. `references/performance-regression.md`
3. `references/output-contracts.md`

## Resources to adapt

- `resources/dql/deployment-before-after.dql`
- `resources/dql/service-golden-signals.dql`
- `resources/dql/active-problems.dql`
- `resources/templates/deployment-health-report.md`

## Workflow

1. Define baseline and post-deployment windows of equal duration.
2. Compare request rate, failure rate, P95, and P99 latency.
3. Check for new active problems after deployment.
4. Inspect exception patterns if errors increased.
5. Return a verdict: healthy, watch, degraded, rollback-candidate, or blocked.

## Example verdict text

```md
Verdict: watch

P95 latency increased by 14 percent after deployment, but failure rate and active problems did not increase. Continue monitoring for 30 minutes and re-run the comparison before broad rollout.
```
