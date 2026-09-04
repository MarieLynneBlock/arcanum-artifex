---
name: agent-owasp-compliance
description: >
    Assess tool-using and multi-agent AI systems against OWASP ASI-style controls, mapping evidence to prompt injection, tool governance, agency, escalation, trust boundaries, audit, identity, policy integrity, supply chain, and behavioural monitoring risks.
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Agent OWASP ASI Compliance Review

Assess AI agent systems against OWASP Agentic Security Initiative (ASI)-style controls and produce evidence-based gap reports.

## Overview

This skill reviews autonomous or tool-using AI agent systems — agents that call tools, access systems, delegate work, or act on behalf of users. It maps observable evidence to ten ASI-style control areas and reports whether each area is covered, partial, missing, unknown, or not applicable.

This is a review and reporting skill. It does not implement controls, generate supply-chain manifests, or claim compliance without evidence.

```
System Evidence → Map each ASI control:
  ASI-01: Prompt Injection Protection
  ASI-02: Tool Use Governance
  ASI-03: Agency Boundaries
  ASI-04: Escalation Controls
  ASI-05: Trust Boundary Enforcement
  ASI-06: Logging & Audit
  ASI-07: Identity Management
  ASI-08: Policy Integrity
  ASI-09: Supply Chain Verification
  ASI-10: Behavioral Monitoring
→ Produce Evidence-Based Compliance Gap Report
```

## Use This Skill When

- Auditing an existing agent system before production, procurement, or security sign-off
- Mapping code, configuration, tests, logs, and architecture evidence to ASI-01 through ASI-10
- Producing a compliance gap report with covered, partial, missing, unknown, or not applicable statuses
- Reviewing tool governance, escalation controls, trust boundaries, auditability, agent identity, or behavioural monitoring
- Re-assessing an agent system after architecture, policy, tool, or deployment changes

## Do Not Use This Skill For

- Implementing new governance controls or runtime enforcement code
- Generating supply-chain manifests, signatures, SBOMs, or plugin provenance artefacts
- Broad application security reviews that are not agentic or ASI-focused
- Declaring formal compliance when evidence is incomplete or controls are only described in comments

## Evidence-First Review Workflow

1. Define scope: identify agents, tools, data stores, external systems, delegated execution paths, and human approval points.
2. Gather evidence: inspect code, configuration, policy files, test cases, logs, runbooks, deployment settings, and architecture notes.
3. Map evidence to ASI-01 through ASI-10. Record file paths, control points, tests, and operational evidence where available.
4. Classify each control as `covered`, `partial`, `missing`, `unknown`, or `not applicable`.
5. Prioritise gaps by exploitability, blast radius, data sensitivity, autonomy level, and ease of remediation.
6. Produce a report with findings first, then a control matrix, open questions, and recommended next review checkpoint.

## Review Resources

This skill includes local, copyable review assets:

- [resources/asi-review-checklist.md](resources/asi-review-checklist.md) — evidence checklist for all ten control areas
- [resources/compliance-report-template.md](resources/compliance-report-template.md) — standalone report template with status definitions

## The 10 Risks

| Risk | Name | What to Look For |
|------|------|-----------------|
| ASI-01 | Prompt Injection | Input validation before tool calls, not just LLM output filtering |
| ASI-02 | Insecure Tool Use | Tool allowlists, argument validation, no raw shell execution |
| ASI-03 | Excessive Agency | Capability boundaries, scope limits, principle of least privilege |
| ASI-04 | Unauthorized Escalation | Privilege checks before sensitive operations, no self-promotion |
| ASI-05 | Trust Boundary Violation | Trust verification between agents, signed credentials, no blind trust |
| ASI-06 | Insufficient Logging | Structured audit trail for all tool calls, tamper-evident logs |
| ASI-07 | Insecure Identity | Cryptographic agent identity, not just string names |
| ASI-08 | Policy Bypass | Deterministic policy enforcement, no LLM-based permission checks |
| ASI-09 | Supply Chain Integrity | Signed plugins/tools, integrity verification, dependency auditing |
| ASI-10 | Behavioural Anomaly | Drift detection, circuit breakers, kill switch capability |

---

## Check ASI-01: Prompt Injection Protection

Look for input validation that runs **before** tool execution, not after LLM generation.

Automated keyword scanning is a triage aid only. Do not mark this control covered unless there is observable validation before tool execution and tests or runtime evidence showing unsafe instructions are blocked.

**Evidence to collect:** input-processing code, policy evaluators, prompt-injection tests, tool-dispatch paths, denial logs.
**Positive signals:** deterministic validation before tool calls, structured denial paths, tests for injected instructions.
**Negative signals:** raw user input reaches tools, only output filtering exists, prompts tell the model to ignore attacks without enforcement.
**Common false positives:** functions named `sanitize` or `validate` that do not run in the tool execution path.

```python
import re
from pathlib import Path

def triage_asi_01(project_path: str) -> dict:
    """Triage ASI-01 signals. Manual evidence review is still required."""
    positive_patterns = [
        "input_validation", "validate_input", "sanitize",
        "classify_intent", "prompt_injection", "threat_detect",
        "PolicyEvaluator", "PolicyEngine", "check_content",
    ]
    negative_patterns = [
        r"eval\(", r"exec\(", r"subprocess\.run\(.*shell=True",
        r"os\.system\(",
    ]

    # Scan Python files for signals
    root = Path(project_path)
    positive_matches = []
    negative_matches = []

    for py_file in root.rglob("*.py"):
        content = py_file.read_text(errors="ignore")
        for pattern in positive_patterns:
            if pattern in content:
                positive_matches.append(f"{py_file.name}: {pattern}")
        for pattern in negative_patterns:
            if re.search(pattern, content):
                negative_matches.append(f"{py_file.name}: {pattern}")

    positive_found = len(positive_matches) > 0
    negative_found = len(negative_matches) > 0

    return {
        "risk": "ASI-01",
        "name": "Prompt Injection",
        "triage_status": "review_likely" if positive_found and not negative_found else "review_required",
        "controls_found": positive_matches,
        "vulnerabilities": negative_matches,
        "recommendation": "Confirm validation runs before tool execution; do not treat keyword matches as compliance evidence."
    }
```

**What passing looks like:**
```python
# GOOD: Validate before tool execution
result = policy_engine.evaluate(user_input)
if result.action == "deny":
    return "Request blocked by policy"
tool_result = await execute_tool(validated_input)
```

**What failing looks like:**
```python
# BAD: User input goes directly to tool
tool_result = await execute_tool(user_input)  # No validation
```

---

## Check ASI-02: Insecure Tool Use

Verify tools have allowlists, argument validation, and no unrestricted execution.

**Evidence to collect:** tool registry, dispatcher code, argument schemas, permission policy, denial tests, shell/network execution wrappers.
**Positive signals:** explicit allowlists, typed argument validation, default-deny behaviour, human review for high-impact tools.
**Negative signals:** dynamic tool names from model output, raw shell execution, unvalidated tool arguments, broad wildcard permissions.
**Common false positives:** documented allowlists that are not enforced in the runtime dispatch path.

**What to search for:**
- Tool registration with explicit allowlists (not open-ended)
- Argument validation before tool execution
- No `subprocess.run(shell=True)` with user-controlled input
- No `eval()` or `exec()` on agent-generated code without sandbox

**Passing example:**
```python
ALLOWED_TOOLS = {"search", "read_file", "create_ticket"}

def execute_tool(name: str, args: dict):
    if name not in ALLOWED_TOOLS:
        raise PermissionError(f"Tool '{name}' not in allowlist")
    # validate args...
    return tools[name](**validated_args)
```

---

## Check ASI-03: Excessive Agency

Verify agent capabilities are bounded — not open-ended.

**Evidence to collect:** capability definitions, execution rings, tenant/data scopes, tool assignments, deployment permissions.
**Positive signals:** least-privilege scopes, bounded objectives, fixed tool sets, explicit maximum autonomy levels.
**Negative signals:** all-tools access, unrestricted filesystem/network access, broad cloud roles, unclear task boundaries.
**Common false positives:** UI labels like "limited mode" without enforceable permission boundaries.

**What to search for:**
- Explicit capability lists or execution rings
- Scope limits on what the agent can access
- Principle of least privilege applied to tool access

**Failing:** Agent has access to all tools by default.
**Passing:** Agent capabilities defined as a fixed allowlist, unknown tools denied.

---

## Check ASI-04: Unauthorized Escalation

Verify agents cannot promote their own privileges.

**Evidence to collect:** role-change code, approval workflows, identity provider policies, deployment permissions, audit records for privilege changes.
**Positive signals:** out-of-band approval, separation of duties, immutable role assignments for agent identities.
**Negative signals:** self-editable policy files, self-managed trust scores, agent-writeable deployment configuration.
**Common false positives:** human approval mentioned in documentation but absent from the actual escalation path.

**What to search for:**
- Privilege level checks before sensitive operations
- No self-promotion patterns (agent changing its own trust score or role)
- Escalation requires external attestation (human or SRE witness)

**Failing:** Agent can modify its own configuration or permissions.
**Passing:** Privilege changes require out-of-band approval (e.g., Ring 0 requires SRE attestation).

---

## Check ASI-05: Trust Boundary Violation

In multi-agent systems, verify that agents verify each other's identity before accepting instructions.

**Evidence to collect:** inter-agent protocol, identity verification, message signatures, delegation policies, trust registry, scoped credentials.
**Positive signals:** verified sender identity, delegation narrowing, per-agent credentials, trust checks before accepting delegated work.
**Negative signals:** string-only agent names, shared secrets, blind trust of messages, child agents receiving broader scope than parent agents.
**Common false positives:** a trust score exists but is not consulted before delegation or tool execution.

**What to search for:**
- Agent identity verification (DIDs, signed tokens, API keys)
- Trust score checks before accepting delegated tasks
- No blind trust of inter-agent messages
- Delegation narrowing (child scope <= parent scope)

**Passing example:**
```python
def accept_task(sender_id: str, task: dict):
    trust = trust_registry.get_trust(sender_id)
    if not trust.meets_threshold(0.7):
        raise PermissionError(f"Agent {sender_id} trust too low: {trust.current()}")
    if not verify_signature(task, sender_id):
        raise SecurityError("Task signature verification failed")
    return process_task(task)
```

---

## Check ASI-06: Insufficient Logging

Verify all agent actions produce structured, tamper-evident audit entries.

**Evidence to collect:** audit schema, log storage, sample logs, retention policy, redaction rules, incident review process.
**Positive signals:** structured records for allowed, denied, reviewed, and failed tool calls; append-only or tamper-evident storage where needed.
**Negative signals:** print-only logs, missing denial records, logs stored in agent-writeable directories, secrets written to logs.
**Common false positives:** observability exists for model calls but not for tool execution or policy decisions.

**What to search for:**
- Structured logging for every tool call (not just print statements)
- Audit entries include: timestamp, agent ID, tool name, args, result, policy decision
- Append-only or hash-chained log format
- Logs stored separately from agent-writable directories

**Failing:** Agent actions logged via `print()` or not logged at all.
**Passing:** Structured JSONL audit trail with chain hashes, exported to secure storage.

---

## Check ASI-07: Insecure Identity

Verify agents have cryptographic identity, not just string names.

**Evidence to collect:** identity provider configuration, credential issuance, rotation policy, signing keys, authentication middleware.
**Positive signals:** per-agent credentials, signed requests, credential rotation, identity bound to capabilities.
**Negative signals:** shared tokens, static names as identity, no authentication between agents and tools.
**Common false positives:** agent display names or labels treated as authenticated identity.

**Failing indicators:**
- Agent identified by `agent_name = "my-agent"` (string only)
- No authentication between agents
- Shared credentials across agents

**Passing indicators:**
- DID-based identity (`did:web:`, `did:key:`)
- Ed25519 or similar cryptographic signing
- Per-agent credentials with rotation
- Identity bound to specific capabilities

---

## Check ASI-08: Policy Bypass

Verify policy enforcement is deterministic — not LLM-based.

**Evidence to collect:** policy engine, policy files, enforcement call sites, bypass tests, fail-closed error handling.
**Positive signals:** deterministic allow/deny/review decisions, no LLM in the enforcement path, policy cannot be skipped by prompts.
**Negative signals:** the model decides whether an action is allowed, policy checks are optional, errors fall back to allow.
**Common false positives:** policy text in the system prompt without runtime enforcement.

**What to search for:**
- Policy evaluation uses deterministic logic (YAML rules, code predicates)
- No LLM calls in the enforcement path
- Policy checks cannot be skipped or overridden by the agent
- Fail-closed behaviour (if policy check errors, action is denied)

**Failing:** Agent decides its own permissions via prompt ("Am I allowed to...?").
**Passing:** PolicyEvaluator.evaluate() returns allow/deny in <0.1ms, no LLM involved.

---

## Check ASI-09: Supply Chain Integrity

Verify agent plugins and tools have integrity verification.

**Evidence to collect:** dependency lockfiles, plugin manifests, hashes, signatures, SBOMs, provenance metadata, review records.
**Positive signals:** pinned dependencies, integrity manifests, signature verification, dependency scanning in CI.
**Negative signals:** unpinned packages, plugin installation from arbitrary URLs, no review of tool or MCP server changes.
**Common false positives:** package-lock files exist but are not enforced in CI or deployment.

**What to search for:**
- `INTEGRITY.json` or manifest files with SHA-256 hashes
- Signature verification on plugin installation
- Dependency pinning (no `@latest`, `>=` without upper bound)
- SBOM generation

---

## Check ASI-10: Behavioural Anomaly

Verify the system can detect and respond to agent behavioural drift.

**Evidence to collect:** circuit breaker configuration, anomaly rules, kill-switch procedure, monitoring dashboards, alert history, incident runbooks.
**Positive signals:** thresholds for repeated failures, kill switch tested, trust decay or anomaly scoring, alerts tied to response ownership.
**Negative signals:** no emergency stop, monitoring only tracks uptime, repeated unsafe actions do not reduce autonomy.
**Common false positives:** metrics dashboards without automated or operational response paths.

**What to search for:**
- Circuit breakers that trip on repeated failures
- Trust score decay over time (temporal decay)
- Kill switch or emergency stop capability
- Anomaly detection on tool call patterns (frequency, targets, timing)

**Failing:** No mechanism to stop a misbehaving agent automatically.
**Passing:** Circuit breaker trips after N failures, trust decays without activity, kill switch available.

---

## Compliance Report Format

```markdown
# OWASP ASI Compliance Review Report
Generated: 2026-04-01
Project: my-agent-system

## Summary: 5 covered, 2 partial, 3 missing, 0 unknown

| Risk | Status | Evidence Summary |
|------|--------|------------------|
| ASI-01 Prompt Injection | covered | PolicyEngine validates input before tool calls; prompt-injection tests exist |
| ASI-02 Insecure Tool Use | covered | Tool allowlist enforced in governance.py with argument validation |
| ASI-03 Excessive Agency | covered | Execution rings limit capabilities by agent role |
| ASI-04 Unauthorised Escalation | partial | Ring promotion requires attestation, but deployment policy is not tested |
| ASI-05 Trust Boundary | missing | No identity verification between agents |
| ASI-06 Insufficient Logging | covered | AuditChain records tool calls and policy decisions with hash chaining |
| ASI-07 Insecure Identity | missing | Agents use string names, no cryptographic identity |
| ASI-08 Policy Bypass | covered | Deterministic PolicyEvaluator, no LLM in path |
| ASI-09 Supply Chain | missing | No integrity manifests or plugin signing |
| ASI-10 Behavioural Anomaly | partial | Circuit breakers exist, but kill-switch procedure is untested |

## Critical Gaps
- ASI-05: Add agent identity verification using DIDs or signed tokens
- ASI-07: Replace string agent names with cryptographic identity
- ASI-09: Generate INTEGRITY.json manifests for all plugins

## Unknowns
- Confirm whether ASI-04 escalation controls are exercised in CI or production tests
- Confirm whether ASI-10 kill-switch ownership is documented and rehearsed

## Recommendation
Prioritise ASI-05 and ASI-07 first because unverified agent identity can undermine delegation, audit, and tool governance controls. Treat ASI-09 as a separate supply-chain workstream with clear ownership.

## Open Questions
- Which agents can delegate work to other agents?
- Which tools can perform irreversible or external actions?
- Which controls have runtime evidence rather than design intent only?
```

---

## Quick Assessment Questions

Use these to rapidly assess an agent system:

1. **Does user input pass through validation before reaching any tool?** (ASI-01)
2. **Is there an explicit list of what tools the agent can call?** (ASI-02)
3. **Can the agent do anything, or are its capabilities bounded?** (ASI-03)
4. **Can the agent promote its own privileges?** (ASI-04)
5. **Do agents verify each other's identity before accepting tasks?** (ASI-05)
6. **Is every tool call logged with enough detail to replay it?** (ASI-06)
7. **Does each agent have a unique cryptographic identity?** (ASI-07)
8. **Is policy enforcement deterministic (not LLM-based)?** (ASI-08)
9. **Are plugins/tools integrity-verified before use?** (ASI-09)
10. **Is there a circuit breaker or kill switch?** (ASI-10)

If you answer "no" to any of these, that's a gap to address.

---

## Related Resources

- [TODO: verify official OWASP ASI reference URL]
- Use the local review checklist and report template in this skill folder before relying on external references.