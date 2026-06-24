# Fallback Guidance

Use this reference when Dynatrace evidence cannot be gathered cleanly because access is missing, the telemetry scope is ambiguous, or the available signals do not agree.

## Missing access or scope

Do not work around permission failures by widening scope, changing tenant context, or lowering safety expectations. Diagnose access in this order:

1. Confirm the active `dtctl` context.
2. Confirm the target environment and tenant URL are the intended ones.
3. Run `dtctl doctor` to check local configuration and connectivity.
4. Inspect the command catalogue, then check the required scopes for the command using its `--help` or the dtctl token-scopes reference.
5. Compare the required scopes with the authenticated token or OAuth identity.
6. Check safety level only after permission scope is understood.

```bash
dtctl config current-context
dtctl config describe-context "$(dtctl config current-context)"
dtctl doctor
dtctl commands --brief -o json
```

If access is still missing, stop and report the blocker with:

- command attempted;
- active context name, without tenant secrets;
- required scope or capability if known;
- whether the operation was read-only or mutating;
- the safest next action for the user or platform owner.

Do not ask the user to paste tokens, bearer headers, private tenant URLs, or raw trace/log payloads into chat.

## Ambiguous telemetry scope

When the service, entity, environment, timeframe, or deployment marker is unclear, narrow the investigation before querying high-volume telemetry.

Use this order:

1. Ask for the missing critical value if it changes the query shape, such as production versus staging or before versus after deployment.
2. If the user gave a partial service name, discover candidate services or entities before running incident queries.
3. If the timeframe is absent, use a small exploratory window and state it explicitly.
4. If multiple candidates match, present the candidates and continue only with the safest narrow query.
5. Keep broad log or span searches exploratory and label them as incomplete.

Default exploratory windows:

| Scenario | Initial window |
| --- | --- |
| Active incident or outage | last 1 hour |
| Recent service failure | last 4 hours |
| Deployment validation | explicit deployment timestamp required |
| Security latest scan | last 30 days |
| Performance baseline | compare matching windows, such as previous 2 hours versus current 2 hours |

Use stable entity identifiers for final evidence. Human-readable service names are acceptable for discovery and reporting, but not as the only filter for destructive, sensitive, or final attribution work.

## Inconclusive correlations

Do not claim root cause when the evidence only supports a hypothesis.

Treat a correlation as inconclusive when:

- only one telemetry source supports the finding;
- metrics changed but spans, logs, or Davis problems do not identify a cause;
- signals disagree, such as elevated latency without errors or exceptions without user impact;
- time windows do not overlap the incident or deployment marker;
- sampling, retention, monitoring mode, or missing permissions may hide relevant data;
- entity names are ambiguous or map to multiple services.

When evidence is inconclusive, produce a low- or medium-confidence finding with:

1. what the available evidence supports;
2. what evidence is missing;
3. the next smallest query or access request that would reduce uncertainty;
4. whether the operational recommendation is continue, watch, mitigate, block, or escalate.

Use this language pattern:

```text
The available evidence supports [finding], but root cause is not confirmed because [gap]. Confidence is [low|medium]. The next check is [specific query, command, access request, or owner action].
```

## Stop conditions

Stop and ask for user or owner input when:

- the next step requires new credentials, token scopes, or tenant access;
- the user must choose between multiple matching services or environments;
- a mutating `dtctl` command is required;
- available telemetry is too incomplete to support a responsible recommendation;
- raw sensitive payloads would be needed to continue.