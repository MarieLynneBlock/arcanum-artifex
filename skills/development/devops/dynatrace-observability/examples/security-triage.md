# Example: Security Triage

## User request

"Summarise current critical and high vulnerabilities and tell us what to fix first."

## References to load

1. `references/security-compliance-triage.md`
2. `references/output-contracts.md`

## Resources to adapt

- `resources/dql/open-vulnerabilities.dql`
- `resources/dql/latest-compliance-scan.dql`
- `resources/templates/security-triage-report.md`

## Workflow

1. Decide whether the request is about current vulnerability state or latest compliance scan posture.
2. Use deduplication for current vulnerability state.
3. Use latest-scan ID first for compliance findings.
4. Prioritise by severity, production exposure, affected service, and remediation path.
5. Produce a triage report with limitations.

## Example finding text

```md
Priority 1: Critical vulnerability affecting an externally reachable production service.

Evidence: current deduplicated vulnerability state shows the finding is open for the affected entity. Recommended action is immediate patch or compensating control, followed by query re-run to confirm state change.
```
