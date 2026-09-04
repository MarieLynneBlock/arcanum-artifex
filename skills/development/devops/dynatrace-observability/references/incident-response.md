# Incident Response

Use this workflow for production failures, active Davis problems, service outages, elevated errors, and questions like "what is wrong?".

## Inputs to collect

- Incident start time or suspected timeframe.
- Service, application, endpoint, environment, or entity ID.
- Deployment or configuration change context if known.
- User impact signals: affected users, regions, tenants, request rate, error rate.
- Known identifiers: problem display ID, trace ID, error ID, release version.

If the user cannot provide these, begin with a narrow recent window such as the last 1-4 hours and state the assumption.

## Workflow

1. Validate `dtctl` context and access when live commands are needed.
2. Query active Davis problems and filter duplicates/frequent events where relevant.
3. Identify affected services/entities and timeframe.
4. Run mandatory failed-span exception expansion.
5. Correlate with logs using trace IDs, service/entity IDs, or exception phrases.
6. Check frontend user events when symptoms affect browser or user sessions.
7. Check metrics using `timeseries` when saturation, latency, or availability is suspected.
8. Quantify business impact.
9. State likely root cause, confidence, and next remediation.

## Active problems

Use `resources/dql/active-problems.dql` or this pattern:

```dql
fetch dt.davis.problems, from:now() - 2h
| filter not(dt.davis.is_duplicate)
| filter event.status == "ACTIVE"
| fields event.start, display_id, event.name, event.category, affected_entity_ids
| sort event.start desc
| limit 20
```

When the user provides a problem display ID, inspect that problem directly before broad discovery.

```dql
fetch dt.davis.problems, from:now() - 24h
| filter display_id == "PROBLEM_DISPLAY_ID"
| fields event.start, event.end, event.status, display_id, event.name, affected_entity_ids, root_cause_entity_id
| sort event.start desc
```

For active problem counts, use `countDistinct(event.id)` because problem records can be refreshed or updated during the same problem lifecycle.

```dql
fetch dt.davis.problems, from:now() - 4h
| filter event.status == "ACTIVE"
| filter dt.davis.is_duplicate == false
| summarize active_problem_count = countDistinct(event.id)
```

Use `resources/dql/davis-problem-trends.dql` to show stability trends and `resources/dql/davis-affected-entities.dql` to rank affected entities.

## Mandatory exception analysis

Use `resources/dql/exception-analysis.dql`. This step is required for service failures before root cause claims.

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

## Log correlation

Use `resources/dql/log-error-correlation.dql` after substituting timeframe and search phrase.

Correlate logs to traces when possible:

```dql
fetch logs, from:now() - 2h
| filter isNotNull(trace_id)
| filter contains(content, "ERROR")
| fields timestamp, trace_id, content
| sort timestamp desc
| limit 20
```

Prefer entity-scoped log filtering before `content` search when the process group, host, service, namespace, or bucket is known. Broad text search should be the fallback when entity scope is unknown.

When log content has a consistent format, parse first and then aggregate the parsed field. For example, parse status codes or user-action fields before summarising counts.

## Frontend and user impact

Use `resources/dql/frontend-error-id.dql` when a browser error ID is available. Otherwise query recent user event exceptions and group by error fields before drilling into specific IDs.

## Evidence standard

Do not stop at one symptom. Final incident analysis should include at least two of:

- Davis problem data.
- Failed span exception details.
- Log evidence.
- Trace or span correlation.
- RUM/user event impact.
- Metric change or saturation signal.
- Deployment or event correlation.
- Workflow execution or automation audit trail if a Dynatrace Workflow responded to the event.

## Report output

Use `resources/templates/incident-report.md`. Include:

- Root cause or leading hypothesis.
- Evidence with DQL snippets or command summaries.
- Impact and affected scope.
- Confidence level.
- Immediate mitigation.
- Follow-up actions and owner suggestions.

## Stop conditions

Stop and ask for clarification if:

- The user asks for live tenant access but no context or credentials are available.
- Results point to sensitive payloads that should not be echoed.
- The investigation requires a destructive or mutating command.
