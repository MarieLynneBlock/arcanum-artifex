# OWASP ASI Review Checklist

Use this checklist to collect evidence for an agent security review. Mark controls as `covered`, `partial`, `missing`, `unknown`, or `not applicable`.

## Scope

- [ ] Identify every agent, subagent, workflow, and delegated execution path.
- [ ] Identify every tool, API, database, shell, MCP server, plugin, or external system the agent can call.
- [ ] Identify data classifications touched by agent inputs, tool calls, logs, and outputs.
- [ ] Identify human approval points and high-impact actions.
- [ ] Record files, configurations, logs, tests, and runbooks used as evidence.

## ASI-01 Prompt Injection Protection

- [ ] User input is validated before tool execution.
- [ ] Prompt injection tests cover tool-call paths.
- [ ] Denied requests are logged with structured reasons.
- [ ] Output-only filtering is not treated as sufficient evidence.

## ASI-02 Insecure Tool Use

- [ ] Tool access is explicitly allowlisted.
- [ ] Tool arguments are validated with schemas or typed validators.
- [ ] Dangerous tools require review or are blocked.
- [ ] Unknown tools and malformed arguments fail closed.

## ASI-03 Excessive Agency

- [ ] Agent capabilities are bounded by role, task, tenant, or environment.
- [ ] Agents do not receive all available tools by default.
- [ ] Access follows least privilege.
- [ ] Autonomy level is documented and enforced.

## ASI-04 Unauthorised Escalation

- [ ] Agents cannot change their own roles, scopes, policies, or trust scores.
- [ ] Privilege changes require out-of-band approval.
- [ ] Escalation attempts are logged and reviewed.
- [ ] Deployment and policy files are not agent-writeable unless explicitly approved.

## ASI-05 Trust Boundary Violation

- [ ] Inter-agent messages have authenticated sender identity.
- [ ] Delegated tasks are scoped no broader than the parent task.
- [ ] Trust checks occur before accepting delegated work.
- [ ] Shared secrets are not reused across agents.

## ASI-06 Insufficient Logging

- [ ] Tool calls record timestamp, agent id, tool name, policy decision, and outcome.
- [ ] Denied, reviewed, failed, and allowed actions are all logged.
- [ ] Logs redact secrets and unnecessary personal data.
- [ ] Audit records are append-only or tamper-evident where required.

## ASI-07 Insecure Identity

- [ ] Each agent has a unique authenticated identity.
- [ ] Credentials are scoped per agent and rotated.
- [ ] Tool calls bind identity to authorised capabilities.
- [ ] String display names are not treated as authentication.

## ASI-08 Policy Bypass

- [ ] Policy enforcement is deterministic and outside the LLM reasoning path.
- [ ] Prompts cannot override policy decisions.
- [ ] Policy evaluation errors deny actions.
- [ ] Bypass tests cover normal and error paths.

## ASI-09 Supply Chain Integrity

- [ ] Dependencies are pinned and reviewed.
- [ ] Plugins, tools, or MCP servers have integrity verification.
- [ ] CI or release checks verify dependency and plugin integrity.
- [ ] Third-party tools have provenance and ownership records.

## ASI-10 Behavioural Anomaly

- [ ] Monitoring detects repeated failures, unusual tool use, and policy-denial spikes.
- [ ] Circuit breakers or autonomy reduction activate on risky behaviour.
- [ ] A kill switch or emergency stop exists and is tested.
- [ ] Alerts have clear human ownership and response steps.
