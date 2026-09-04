# Example: Incident Response

## User request

"Production checkout is failing. Find the likely root cause and impact."

## References to load

1. `references/dtctl-setup-and-safety.md`
2. `references/incident-response.md`
3. `references/output-contracts.md`

## Resources to adapt

- `resources/dql/active-problems.dql`
- `resources/dql/exception-analysis.dql`
- `resources/dql/log-error-correlation.dql`
- `resources/templates/incident-report.md`

## Workflow

1. Confirm context and timeframe.
2. Query active Davis problems.
3. Expand failed span exceptions.
4. Correlate exception messages with logs and trace IDs.
5. Check whether frontend user events indicate user impact.
6. Produce an incident report with confidence and assumptions.

## Example response shape

```md
## Summary

Checkout failures are most likely caused by [exception or dependency]. Evidence comes from active Davis problem [ID], failed spans in [service], and matching error logs in the same timeframe.

## Impact

- Affected service: checkout-service
- Timeframe: last 2 hours
- Affected users: [count or unknown]
- Error rate: [value]

## Immediate action

1. Mitigate [component/dependency/configuration].
2. Validate with the exception-analysis query.
3. Keep release rollback open until P95 latency and failure rate return to baseline.
```
