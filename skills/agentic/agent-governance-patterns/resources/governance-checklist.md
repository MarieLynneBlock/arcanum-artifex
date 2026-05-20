# Agent Governance Checklist

Use this checklist when adding governance controls to a tool-using or multi-agent system.

## Policy Design

- [ ] Define the agent's allowed tools explicitly.
- [ ] Block destructive, privileged, or out-of-scope tools by default.
- [ ] Require human approval for irreversible, external, financial, legal, or privileged actions.
- [ ] Set per-request or per-session call limits.
- [ ] Store policy in configuration rather than hardcoding it into business logic.

## Pre-Execution Controls

- [ ] Classify user intent before any tool call.
- [ ] Validate tool arguments with structured validators.
- [ ] Treat pattern matching as a baseline control, not complete sensitive-data detection.
- [ ] Fail closed when policy loading or evaluation fails.

## Runtime Enforcement

- [ ] Wrap every tool entry point with deterministic allow, deny, or review checks.
- [ ] Scope rate counters to the request, session, tenant, or actor as appropriate.
- [ ] Enforce path, network, and data-boundary checks inside the tool implementation.
- [ ] Keep governance logic separate from agent task logic.

## Auditability

- [ ] Log every allowed, denied, reviewed, and failed tool call.
- [ ] Include policy name, tool name, actor or agent id, timestamp, and structured denial reason.
- [ ] Redact secrets, credentials, and unnecessary personal data from logs.
- [ ] Use append-only or tamper-evident storage where audit integrity matters.
- [ ] Define retention, access, and review responsibilities for audit records.

## Multi-Agent Trust

- [ ] Track trust or reliability per delegate agent.
- [ ] Decay trust over time when no successful activity occurs.
- [ ] Gate delegation and sensitive operations on trust thresholds.
- [ ] Require identity verification before accepting tasks from another agent.

## Validation

- [ ] Test blocked tools are denied.
- [ ] Test approval-gated tools cannot run without review.
- [ ] Test content filters and structured validators.
- [ ] Test rate-limit behaviour across concurrent requests.
- [ ] Test audit records for allowed, denied, error, and review paths.
- [ ] Test composed policies use most-restrictive-wins semantics.