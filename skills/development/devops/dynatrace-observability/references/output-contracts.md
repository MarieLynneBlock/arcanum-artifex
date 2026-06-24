# Output Contracts

Use this reference whenever the skill produces an incident, deployment, performance, or security report.

## General reporting rules

- Put findings before narrative background.
- Include timeframe, environment/context, and scope.
- Include DQL or command summaries sufficient for reproducibility.
- Separate facts, interpretation, and assumptions.
- State confidence: `high`, `medium`, or `low`.
- Include evidence gaps, ambiguous scope, missing access, and inconclusive correlations when present.
- Redact secrets, tokens, personal data, and sensitive payloads.
- Do not claim full root cause when evidence only supports a hypothesis.

## Incident report structure

Use `resources/templates/incident-report.md`.

Required sections:

1. Summary.
2. Impact.
3. Evidence.
4. Root cause or leading hypothesis.
5. Immediate actions.
6. Follow-up actions.
7. Evidence gaps, confidence, and assumptions.

## Deployment health report structure

Use `resources/templates/deployment-health-report.md`.

Required sections:

1. Verdict.
2. Deployment and baseline windows.
3. Metric comparison.
4. Problems and exceptions.
5. Rollback or continuation recommendation.
6. Incomplete data, watch criteria, confidence, and assumptions.

## Security triage report structure

Use `resources/templates/security-triage-report.md`.

Required sections:

1. Scope and latest scan/current-state basis.
2. Severity summary.
3. Top prioritised findings.
4. Affected entities.
5. Recommended actions.
6. Tracking and ownership.
7. Access, scan, monitoring, and evidence limitations.

## Issue body fields

When offering to create a GitHub issue, include:

- title with category and impacted component;
- severity;
- environment;
- timeframe;
- evidence query summaries;
- reproduction or validation command;
- recommended remediation;
- owner or team if known;
- acceptance criteria for closure.

## Confidence language

Use this language consistently:

| Confidence | Meaning |
| --- | --- |
| `high` | Multiple independent data sources agree and timeframe aligns. |
| `medium` | Evidence is consistent but missing one corroborating source or exact attribution. |
| `low` | Evidence is partial, exploratory, or depends on unverified assumptions. |

When confidence is `low` or `medium`, include the next smallest check that would reduce uncertainty, such as a narrower entity query, an additional source, a required token scope, or a deployment timestamp.

## Avoid

- Large raw logs in final answers.
- Tenant-specific URLs or tokens.
- Claiming all systems are healthy when only one service was queried.
- Treating no results as proof without checking timeframe, permissions, and data availability.
