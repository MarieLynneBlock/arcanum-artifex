# Security and Compliance Triage

Use this reference for Dynatrace vulnerability findings, compliance scan results, security events, CVE review, and prioritisation.

## Operating principles

- Latest-scan analysis is mandatory for compliance posture.
- Current vulnerability state requires deduplication by vulnerability and affected entity.
- Do not aggregate historical security findings and present them as current posture.
- Prioritise by severity, runtime use, exploitability/context, affected critical services, and ownership.
- For Runtime Vulnerability Analytics, distinguish what is running from what is merely deployed.
- State monitoring-mode limitations when Full-Stack Monitoring, deep monitoring, or language/runtime support affects coverage.
- Avoid exposing sensitive resource names or payloads in public reports.

## Runtime Vulnerability Analytics context

Dynatrace Runtime Vulnerability Analytics detects and evaluates vulnerabilities based on components that are actually running. It can reduce false positives by considering runtime use, topology, distributed tracing, data access paths, and production execution.

Before making a priority claim, check whether the available evidence supports:

- third-party vulnerability detection or code-level vulnerability detection;
- process deep monitoring for the relevant technology;
- Full-Stack Monitoring where exposure and sensitive-data context are needed;
- affected process, service, host, container, or Kubernetes scope;
- whether the vulnerability is still active after deployment, rollback, or remediation.

If monitoring is in Infrastructure Monitoring or Discovery mode, call out missing or reduced context for public internet exposure, reachable data assets, related services, or Dynatrace Security Score adaptation rather than overstating confidence.

## Latest compliance scan

Use `resources/dql/latest-compliance-scan.dql` as a two-step workflow.

Step 1: get the latest scan ID for the relevant object type.

```dql
fetch security.events, from:now() - 30d
| filter event.type == "COMPLIANCE_SCAN_COMPLETED"
| sort timestamp desc
| limit 1
| fields timestamp, scan.id, object.type
```

Step 2: query findings from that scan only.

```dql
fetch security.events, from:now() - 30d
| filter event.type == "COMPLIANCE_FINDING" and scan.id == "SCAN_ID"
| filter violation.detected == true
| summarize finding_count = count(), by: {compliance.rule.severity.level}
| sort finding_count desc
```

## Current vulnerability state

Use `resources/dql/open-vulnerabilities.dql`.

```dql
fetch security.events, from:now() - 7d
| filter event.type == "VULNERABILITY_STATE_REPORT_EVENT"
| dedup {vulnerability.display_id, affected_entity.id}, sort: {timestamp desc}
| filter vulnerability.resolution_status == "OPEN"
| filter vulnerability.severity in ["CRITICAL", "HIGH"]
| fields timestamp, vulnerability.display_id, vulnerability.title, vulnerability.severity, affected_entity.id, vulnerability.resolution_status
| sort vulnerability.severity desc, timestamp desc
```

## Prioritisation model

Rank findings by:

1. Severity: critical, high, medium, low.
2. Runtime relevance: affected component loaded or vulnerable code path observed.
3. Exposure: internet-facing, production, sensitive data path, privileged resource.
4. Affected business service or user journey.
5. Fix availability and blast radius.
6. Existing owner, ticket, or exception.

## Evidence checklist

For each material finding include:

- finding ID or vulnerability display ID;
- severity and status;
- affected entity identifiers;
- latest scan timestamp or state timestamp;
- affected service or business area if known;
- monitoring mode or coverage limitation if it changes confidence;
- remediation action or escalation path;
- whether this is new, recurring, or existing/tracked.

## Compliance reporting

Do not claim compliance status from partial data. State scope and limitations explicitly:

- object type scanned;
- latest scan ID and timestamp;
- frameworks or rule groups present in the data;
- excluded environments or missing data;
- whether results are latest-scan or current-state deduplicated.

## Issue creation guidance

Offer issue creation for:

- critical vulnerabilities;
- high vulnerabilities on production or external surfaces;
- findings with confirmed runtime use or sensitive data path exposure;
- repeated compliance violations;
- findings with clear owner and remediation path.

## Automation and API routing

Use Dynatrace API or Workflows when triage needs repeatable action:

- API endpoints exist for Application Security vulnerabilities, Davis Security Advisor, attacks, audit logs, events, problems, metrics, settings, SLOs, synthetic monitors, and tokens.
- API Explorer shows endpoint-specific OAuth token permissions; request only the scopes required for the action.
- Workflows can react to Dynatrace Intelligence events or security problems, send notifications, run approvals, retry actions, and provide an audit trail.
- Do not use Workflows for mass data ingestion or mass export.

Use `resources/templates/security-triage-report.md` for the report and include enough context for developers to act without embedding secrets or sensitive payloads.
