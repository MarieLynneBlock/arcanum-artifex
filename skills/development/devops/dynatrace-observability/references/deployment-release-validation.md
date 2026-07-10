# Deployment and Release Validation

Use this reference for pre-deployment checks, post-deployment health gates, release validation, rollback decisions, and CI/CD quality gates backed by Dynatrace evidence.

## Required inputs

- Deployment timestamp or release window.
- Service, application, or entity scope.
- Target environment and context.
- Expected traffic pattern or baseline window.
- SLO or release criteria if available.

If no deployment timestamp is provided, ask for it or state the default analysis window before continuing.

## Pre-deployment health check

Before release, verify that the target environment is already stable:

```dql
fetch dt.davis.problems, from:now() - 30m
| filter not(dt.davis.is_duplicate)
| filter event.status == "ACTIVE"
| fields event.start, display_id, event.name, event.category, affected_entity_ids
| sort event.start desc
| limit 20
```

Check current golden signals for the target service:

```dql
timeseries {
  p95_response_time = percentile(dt.service.request.response_time, 95, scalar: true),
  requests_per_second = sum(dt.service.request.count, scalar: true, rate: 1s),
  failed_requests_per_minute = sum(dt.service.request.failure_count, scalar: true, rate: 1m)
}, by: {dt.entity.service}, from:now() - 30m
| fieldsAdd service_name = entityName(dt.entity.service)
```

## Post-deployment comparison

Use `resources/dql/deployment-before-after.dql` as a starting point. Compare before and after windows of similar length.

Minimum comparison dimensions:

- request volume and throughput;
- failed request count and failure rate;
- P50, P95, and P99 latency;
- active Davis problems created after deployment;
- Davis event changes such as CPU saturation or high-memory events when relevant;
- exception types newly appearing after deployment;
- infrastructure saturation where relevant.

Use `timeseries` for metric comparisons and keep baseline and post-deployment windows representative. For endpoint-specific checks, filter on the endpoint name or stable service/entity identifier before calculating rates.

## Health verdicts

Use one of these verdicts:

| Verdict | Meaning | Action |
| --- | --- | --- |
| `healthy` | Metrics and problems are within expected range | Continue rollout or approve release. |
| `watch` | Minor changes or inconclusive evidence | Continue with monitoring and a time-bound follow-up. |
| `degraded` | Clear regression without severe user impact | Pause rollout and remediate before expansion. |
| `rollback-candidate` | Severe regression, active critical problem, or high user impact | Initiate rollback decision process. |
| `blocked` | Pre-deployment environment is already unhealthy | Do not deploy until baseline is clean or exception is approved. |

## CI/CD command pattern

Use `dtctl` validation commands in pipeline steps where available:

```bash
dtctl verify query 'fetch logs | limit 1'
dtctl query 'fetch dt.davis.problems, from:now() - 30m | filter event.status == "ACTIVE" | limit 20' --plain
```

Prefer fail-fast queries with bounded timeframes. Use structured output for automated gates.

```bash
dtctl query 'fetch dt.davis.problems, from:now() - 30m | limit 20' -o json --plain
```

For automation hand-off, prefer the Dynatrace API or Workflows when the action must be repeatable or scheduled. Workflows are suitable for reacting to Dynatrace Intelligence events or security problems, scheduled reports, notifications, approvals, retries, and audit trails. They are not intended for mass data ingestion or mass export; use platform ingestion/export mechanisms or extensions for large-scale data movement.

## Output

Use `resources/templates/deployment-health-report.md`. Include:

- deployment window;
- baseline window;
- metrics compared;
- active or new problems;
- verdict;
- rollback or follow-up recommendation;
- assumptions and confidence.

## Pitfalls

- Comparing a low-traffic window with a peak-traffic window without noting the mismatch.
- Reporting raw failed request counts without request volume or rate context.
- Ignoring pre-existing problems that make post-deployment attribution unreliable.
- Treating absence of data as proof of health.
- Triggering an automated rollback from a single query without checking problem state, user impact, and deployment scope.
