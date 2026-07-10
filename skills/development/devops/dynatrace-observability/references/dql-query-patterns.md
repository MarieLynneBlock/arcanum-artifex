# DQL Query Patterns

Use this reference before writing, fixing, or validating Dynatrace Query Language for incidents, release checks, performance analysis, or security triage.

## Query construction rules

1. Start with a bounded timeframe. If the UI or API does not provide one, Dynatrace defaults may apply, so state the window explicitly for reusable queries.
2. Filter early to reduce scan cost. Prefer exact field filters before broad text search.
3. Select fields early with `fields`, `fieldsKeep`, or `fieldsRemove` when large payloads are not needed.
4. Transform or parse only after the dataset is narrowed.
5. Aggregate with `summarize`, `makeTimeseries`, or `timeseries` after filtering; do not place `limit` before aggregation unless sampling is intentional.
6. Sort near the end of the query, then apply `limit` for result shaping.
7. Verify field names with a minimal query before building a long query.
8. Use stable entity identifiers for filtering where possible.
9. Use `entityName(dt.entity.service)`, `getNodeName(...)`, or `getNodeField(...)` for readable output after entity-scoped filtering.
10. Validate final syntax with `dtctl verify query '<DQL>'` when `dtctl` is available.

## Timeframes

```dql
fetch logs, from:now() - 1h
fetch spans, from:now() - 4h
fetch security.events, from:now() - 30d
fetch events, from:"2026-06-24T09:00:00Z", to:"2026-06-24T10:00:00Z"
```

Use double quotes for absolute timestamps. Keep default windows narrow, then widen only when evidence requires it.

For high-volume data, use the `fetch` options supported by the target tenant where appropriate: narrow buckets, `scanLimitGBytes`, or sampling for approximate exploration. Do not use sampled queries for final incident counts unless the report clearly states the approximation.

## Entity discovery before targeted queries

When the user provides a partial service name, environment label, or informal component name, discover candidate entities before running expensive incident or performance queries.

```dql
fetch spans, from:now() - 4h
| filter isNotNull(dt.entity.service)
| summarize
    request_count = count(),
    failed_requests = countIf(request.is_failed == true),
    latest_seen = max(timestamp),
  by: {dt.entity.service}
| fieldsAdd service_name = entityName(dt.entity.service)
| sort request_count desc
| limit 20
```

If the result contains multiple plausible matches, report the candidates and ask for a narrower service, entity ID, environment, or deployment marker. Use `resources/dql/service-entity-discovery.dql` when a reusable discovery query is enough. Use [fallback-guidance.md](fallback-guidance.md) when ambiguity affects the investigation conclusion.

## Core commands

```dql
fetch logs, from:now() - 1h
| filter loglevel == "ERROR"
| fields timestamp, content, trace_id
| sort timestamp desc
| limit 50
```

```dql
fetch spans, from:now() - 4h
| filter request.is_failed == true
| summarize failures = count(), by: {dt.entity.service}
| fieldsAdd service_name = entityName(dt.entity.service)
| sort failures desc
```

```dql
timeseries {
  p95_latency = percentile(dt.service.request.response_time, 95, scalar: true),
  request_rate = sum(dt.service.request.count, scalar: true, rate: 1s)
}, by: {dt.entity.service}, from:now() - 2h
| fieldsAdd service_name = entityName(dt.entity.service)
```

Use `timeseries` for metric data. Use `makeTimeseries` when converting event-like records, such as logs or Davis problems, into chartable time series.

## Mandatory exception expansion

Failure counts alone are not enough for service failures. Expand `span.events` and inspect exception fields.

```dql
fetch spans, from:now() - 4h
| filter request.is_failed == true and isNotNull(span.events)
| expand span.events
| filter span.events[span_event.name] == "exception"
| summarize exception_count = count(), by: {
    service_name = entityName(dt.entity.service),
    exception_type = span.events[exception.type],
    exception_message = span.events[exception.message]
}
| sort exception_count desc
```

## Problem queries

```dql
fetch dt.davis.problems, from:now() - 2h
| filter not(dt.davis.is_duplicate)
| filter event.status == "ACTIVE"
| fields event.start, display_id, event.name, event.category, affected_entity_ids
| sort event.start desc
| limit 20
```

Use `ACTIVE` or `CLOSED` status values. Do not use `OPEN` for Davis problem status unless confirmed by field discovery in the target tenant.

For current-state counting, use stable problem identifiers. Dynatrace examples use `event.id` as the unique problem ID that remains stable across refreshes and updates for the same problem.

```dql
fetch dt.davis.problems, from:now() - 24h
| summarize problem_count = countDistinct(event.id)
```

For affected-entity analysis, expand `affected_entity_ids` before aggregation.

```dql
fetch dt.davis.problems, from:now() - 24h
| filter event.status == "ACTIVE"
| filter dt.davis.is_duplicate == false
| expand affected_entity_ids
| summarize problem_count = countDistinct(event.id), by:{affected_entity_ids}
| sort problem_count desc
| limit 10
```

Use `resources/dql/davis-problem-trends.dql` for a trend view and `resources/dql/davis-affected-entities.dql` for affected-entity ranking.

## Log search

```dql
fetch logs, from:now() - 2h
| filter dt.entity.process_group == "PROCESS_GROUP_ID"
| filter content ~ "timeout" or contains(content, "Exception")
| fields timestamp, loglevel, content, trace_id, dt.entity.process_group
| sort timestamp desc
| limit 100
```

When possible, narrow logs by entity, process group, Kubernetes namespace, bucket, or another indexed/contextual field before searching `content`. Use `==` when a value is known exactly and `~` when a value is only partly known. Parse structured log fields before aggregating when the log format is known.

Avoid transformations inside filters when a direct field comparison is available. For example, prefer `k8s.namespace.name ~ "astro*"` over applying `lower(...)` inside the filter.

## Trace correlation

```dql
fetch logs, from:now() - 2h
| filter isNotNull(trace_id)
| filter contains(content, "ERROR")
| fields timestamp, trace_id, content
| sort timestamp desc
| limit 20
```

Then use the trace identifiers to inspect spans:

```dql
fetch spans, from:now() - 2h
| filter trace.id == toUid("TRACE_ID")
| fields start_time, trace.id, span.name, duration, dt.entity.service, span.events
| sort start_time asc
```

## Validation loop

1. Run a minimal query with `| limit 1`.
2. Add one filter or field at a time.
3. Validate with `dtctl verify query '<DQL>'`.
4. Run with a narrow timeframe.
5. Only then widen time or remove limits.

## Common pitfalls

- Filtering on `service.name` in environments where the data is not OpenTelemetry-only.
- Omitting timeframes on logs, spans, user events, or security events.
- Aggregating security findings over time instead of using latest scan or current deduplicated state.
- Sorting before filtering or projecting large payload fields unnecessarily.
- Applying `limit` before `summarize`, `makeTimeseries`, or `timeseries` and then treating the result as complete.
- Using broad `content` searches before narrowing by entity or scope.
- Forgetting backticks around field names that contain special characters or reserved words such as `true`, `false`, `null`, `and`, `or`, `not`, `xor`, or `mod`.
- Returning raw logs or span events in final reports without redaction.
