# Example: Ambiguous Input Resolution

## User request

"Payment looks unhealthy after the release. What happened?"

## References to load

1. `references/fallback-guidance.md`
2. `references/dtctl-setup-and-safety.md`
3. `references/dql-query-patterns.md`
4. `references/output-contracts.md`

## Resources to adapt

- `resources/dql/service-entity-discovery.dql`
- `resources/dql/deployment-before-after.dql`
- `resources/dql/service-golden-signals.dql`
- `resources/templates/deployment-health-report.md`

## Workflow

1. Check `dtctl` context and command capability before querying.
2. Identify the missing values: exact service/entity, environment, deployment timestamp, and comparison window.
3. If the service name is partial, run service discovery and present candidate entity IDs.
4. If deployment time is missing, ask for it before producing a deployment verdict.
5. If telemetry sources disagree, report a leading hypothesis with confidence instead of a confirmed root cause.
6. Include the next smallest check that would reduce uncertainty.

## Example response shape

```md
I found three candidate services for "payment" in the last 4 hours: [service candidates]. I cannot produce a deployment verdict yet because the deployment timestamp is missing.

The available evidence supports a possible latency regression in [service/entity], but root cause is not confirmed because logs and Davis problems do not yet corroborate the metric change. Confidence: medium.

Next check: provide the deployment timestamp or select the target entity ID, then run the before/after deployment comparison for matching windows.
```