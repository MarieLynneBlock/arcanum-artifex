# Performance Regression

Use this reference when latency, throughput, saturation, or responsiveness appears worse than baseline.

## Inputs to collect

- Service, endpoint, entity ID, or workload scope.
- Regression start time or suspected deployment timestamp.
- Baseline window for comparison.
- SLO or threshold if known.
- User-visible symptom such as slow checkout, timeout, or page load delay.

## RED and golden signals

Start with `resources/dql/service-golden-signals.dql`.

```dql
timeseries {
  p95_response_time = percentile(dt.service.request.response_time, 95, scalar: true),
  requests_per_second = sum(dt.service.request.count, scalar: true, rate: 1s),
  failed_requests_per_minute = sum(dt.service.request.failure_count, scalar: true, rate: 1m)
}, by: {dt.entity.service}, from:now() - 2h
| fieldsAdd service_name = entityName(dt.entity.service)
```

Infrastructure saturation such as `dt.host.cpu.usage` has no `dt.entity.service` dimension, so query it separately by host or process group and correlate by topology rather than grouping it by service:

```dql
timeseries {
  avg_cpu = avg(dt.host.cpu.usage, scalar: true)
}, by: {dt.entity.host}, from:now() - 2h
| fieldsAdd host_name = entityName(dt.entity.host)
```

For rate calculations, prefer metric `timeseries` with `rate:` or explicit array arithmetic. Use defaults for missing failure series only when a zero value is semantically correct.

```dql
timeseries {
  requests = sum(dt.service.request.count, default: 0),
  failures = sum(dt.service.request.failure_count, default: 0)
}, by:{dt.entity.service}, from:now() - 2h
| fieldsAdd failure_rate = if(requests[] > 0, 100 * failures[] / requests[], else: 0)
| fieldsAdd service_name = entityName(dt.entity.service)
```

Use `resources/dql/metric-failure-rate.dql` for a reusable failure-rate starting point.

## Regression heuristics

Use heuristics as triage signals, not absolute truth:

- P95 or P99 latency increase greater than 20 percent compared with a representative baseline.
- Failure rate more than doubles while traffic remains comparable.
- Throughput drops while demand remains stable.
- CPU, memory, network, queue depth, or dependency latency increases alongside request latency.
- New exceptions or timeouts appear after deployment.

## Workflow

1. Establish the baseline and suspect window.
2. Compare service latency, traffic, and errors.
3. Use `timeseries` for metric data and `makeTimeseries` for event records that need charting.
4. Check active problems and Davis events in the suspect window.
5. Inspect failed spans and exceptions for slow or failing operations.
6. Correlate with deployment, configuration, dependency, or infrastructure events.
7. State whether evidence supports a regression, baseline mismatch, traffic shift, or no finding.

## Endpoint or operation drilldown

If service-level metrics show a regression, drill down by span name, endpoint, or operation where fields are available:

```dql
fetch spans, from:now() - 2h
| filter dt.entity.service == "SERVICE_ID"
| summarize count = count(), p95_duration = percentile(duration, 95), by: {span.name}
| sort p95_duration desc
| limit 20
```

## Correlation checklist

Check at least two of:

- service request metrics;
- span duration and failed spans;
- exception patterns;
- dependency spans;
- host/container saturation;
- Davis problems;
- Davis events such as CPU saturation, high memory, process restarts, or garbage collection where available;
- deployment events or release window.

## Output

Report:

- regression verdict: `confirmed`, `likely`, `inconclusive`, or `not observed`;
- baseline and comparison windows;
- top changed metrics;
- suspected component or operation;
- supporting DQL;
- recommended mitigation and follow-up measurement.
