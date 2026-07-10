---
name: dynatrace-observability
description: 'Use when investigating Dynatrace incidents, validating releases, writing DQL, triaging security findings, or operating Dynatrace with dtctl.'
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 0.0.2
---

# Dynatrace Observability with dtctl

## What this skill does

Use this skill to investigate Dynatrace telemetry and security findings with reproducible DQL and `dtctl` workflows. It is a standalone package: copy the whole folder when deploying it to another project.

The skill favours progressive disclosure: start here, then load only the reference, example, template, or DQL resource needed for the task.

## When to use it

Use this skill for:

- production incident response and root cause analysis;
- deployment impact and release health validation;
- production error triage across Davis problems/events, spans, logs, traces, metrics, and user events;
- performance regression checks against baseline behaviour;
- vulnerability and compliance finding review;
- DQL query writing, validation, and troubleshooting;
- Dynatrace terminal workflows with `dtctl`;
- evidence hand-off into Dynatrace Workflows, dashboards, notebooks, or API automation.

## When not to use it

Do not use this skill for:

- generic DevOps advice with no Dynatrace evidence source;
- product marketing, licensing, or procurement questions;
- architecture-only discussions with no operational validation;
- non-Dynatrace observability platforms.

## Operating rules

- Evidence first: state what was queried and what the result supports.
- Always set a bounded timeframe before querying high-volume data.
- Optimise DQL in this order: narrow timeframe, filter early, select fields early, transform/parse, aggregate, then sort/limit.
- For service failures, expand `span.events` and inspect exception records before concluding.
- For Davis analysis, prefer `dt.davis.problems` and `dt.davis.events` examples over guessed problem fields.
- For security and compliance posture, use latest-scan or deduplicated current-state patterns, not broad historical counts.
- For Runtime Vulnerability Analytics, state monitoring-mode and deep-monitoring limitations when evidence is incomplete.
- Use `entityName(dt.entity.service)` for readable service names while filtering by stable entity identifiers where possible.
- Check `dtctl` context, safety level, and required scopes before running mutating operations.
- If access fails, diagnose context, command capability, token scopes, and safety level before changing the query or conclusion.
- If service, entity, environment, timeframe, or deployment markers are ambiguous, discover candidates or narrow scope before querying high-volume telemetry.
- If correlations are incomplete or contradictory, state evidence gaps and confidence instead of claiming confirmed root cause.
- Prefer `--plain`, `--output json`, or `--output yaml` for automation; do not parse formatted tables.
- Do not include secrets, platform tokens, tenant-specific URLs, or private trace/log payloads in reports.

## Reference routing

Load the smallest matching file first:

| Task | Load |
| --- | --- |
| Set up or validate `dtctl`, contexts, safety levels, scopes, command discovery | [references/dtctl-setup-and-safety.md](references/dtctl-setup-and-safety.md) |
| Resolve missing access, scope errors, ambiguous telemetry, or inconclusive correlations | [references/fallback-guidance.md](references/fallback-guidance.md) |
| Write, fix, validate, or optimise DQL | [references/dql-query-patterns.md](references/dql-query-patterns.md) |
| Investigate an incident, outage, active Davis problem, or unknown failure | [references/incident-response.md](references/incident-response.md) |
| Validate a deployment, release gate, or rollback decision | [references/deployment-release-validation.md](references/deployment-release-validation.md) |
| Analyse latency, throughput, saturation, or regression against baseline | [references/performance-regression.md](references/performance-regression.md) |
| Triage vulnerabilities, compliance findings, or security events | [references/security-compliance-triage.md](references/security-compliance-triage.md) |
| Produce a structured incident, deployment, or security report | [references/output-contracts.md](references/output-contracts.md) |

## Bundled resources

- Reusable DQL templates live in [resources/dql/](resources/dql/).
- Report templates live in [resources/templates/](resources/templates/).
- Worked examples live in [examples/](examples/).
- A portable context check helper lives at [scripts/validate-dtctl-context.sh](scripts/validate-dtctl-context.sh).

## Validated source areas

This package is aligned to the public Dynatrace documentation areas below. Treat external docs as verification sources, not runtime dependencies.

- Dynatrace Query Language guide, reference, commands, and best practices.
- Logs on Grail examples and DQL timeseries examples.
- Dynatrace Intelligence DQL examples for Davis problems and events.
- Application Security and Runtime Vulnerability Analytics guidance.
- Dynatrace Workflows overview and Dynatrace API reference.

## Default workflow

1. Identify the user's intent and select the reference file from the routing table.
2. Establish context: environment, timeframe, service/entity, deployment time, or finding type.
3. Validate access and command capability if `dtctl` is needed.
4. If access, scope, entity, timeframe, or correlation evidence is incomplete, use [references/fallback-guidance.md](references/fallback-guidance.md).
5. Build or adapt DQL from the relevant reference and `resources/dql/` template.
6. Run the smallest safe query first, usually with `| limit 1` or a narrow timeframe.
7. Correlate at least two relevant sources before stating root cause.
8. Produce an evidence-based report using the relevant template.

## Minimal setup

Before deep analysis, establish command and access context.

```bash
# Install dtctl (macOS/Linux)
brew install dynatrace-oss/tap/dtctl

# Authenticate (OAuth recommended)
dtctl auth login --context my-env --environment "https://<env>.apps.dynatrace.com"

# Verify config, context, token, connectivity, auth
dtctl doctor
```

For token-based contexts (for CI/CD or headless runs):

```bash
dtctl config set-context my-env \
  --environment "https://<env>.apps.dynatrace.com" \
  --token-ref my-token \
  --safety-level readwrite-mine

dtctl config set-credentials my-token --token "$DT_API_TOKEN"
```
