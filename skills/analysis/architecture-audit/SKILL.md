---
description: >
name: architecture-audit
version: 1.0.0
tags:
  - architecture
  - audit
  - design
  - quality-attributes
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Provides a repeatable, evidence-based framework for reviewing software architectures. It evaluates a design against quality attributes (scalability, maintainability, security, reliability, performance, operability), checks for constraint violations, and produces a prioritised list of findings with actionable recommendations.

## When to use it

- User asks to "review", "audit", or "assess" an architecture, design document, or ADR.
- User shares a system diagram, architecture description, or tech-stack decision and wants structured feedback.
- User wants to identify risks or trade-offs in a design before committing to it.
- User needs a report suitable for a design review meeting.

## Instructions

1. **Understand scope.** Clarify what is in scope (components, boundaries, interfaces) and what quality attributes matter most to the stakeholder. If not stated, default to: scalability, maintainability, security, reliability, performance, and operability.

2. **Collect evidence.** Read any provided diagrams, ADRs, documentation, or code. Note what is explicit, what is implied, and what is missing.

3. **Evaluate each quality attribute.**
   For each attribute in scope:
   - State the current approach (how the architecture addresses it).
   - Rate the approach: `Strong` / `Adequate` / `Weak` / `Not addressed`.
   - Identify specific risks or gaps.

4. **Check constraints.** Identify whether known constraints (team size, budget, compliance requirements, existing systems) are respected or at risk.

5. **Identify trade-offs.** Call out explicit design trade-offs and assess whether they are intentional and well-reasoned.

6. **Prioritise findings.** Rank findings by impact × likelihood:
   - `Critical` — must address before proceeding.
   - `High` — address in the next iteration.
   - `Medium` — schedule for backlog.
   - `Low` / `Informational` — note for awareness.

7. **Write recommendations.** For each Critical/High finding, provide at least one concrete, actionable recommendation.

8. **Produce the report** using the output format below.

## Output format

```markdown
# Architecture Audit: [Subject]

**Date:** YYYY-MM-DD  
**Auditor:** [name or AI-assisted]  
**Scope:** [what was reviewed]

---

## Quality Attribute Summary

| Attribute       | Rating    | Key finding                          |
|-----------------|-----------|--------------------------------------|
| Scalability     | Adequate  | ...                                  |
| Maintainability | Weak      | ...                                  |
| Security        | Strong    | ...                                  |
| Reliability     | Weak      | ...                                  |
| Performance     | Adequate  | ...                                  |
| Operability     | Not addressed | ...                              |

---

## Findings

### [CRITICAL/HIGH/MEDIUM/LOW] Finding title

**Evidence:** [what in the architecture leads to this finding]  
**Risk:** [what could go wrong]  
**Recommendation:** [concrete action]

---

## Trade-off Register

| Decision | What was gained | What was sacrificed | Intentional? |
|----------|----------------|---------------------|--------------|
| ...      | ...            | ...                 | Yes / No / Unknown |

---

## Summary

[2–4 sentence overall assessment. Is the architecture fit for purpose? What is the single most important thing to address?]
```

## Examples

### Example 1 — Microservices migration proposal

**Input:** User shares an ADR proposing to migrate a monolith to 12 microservices.  
**Expected output:** Audit report rating each quality attribute, flagging operational complexity and distributed tracing gap as High findings, noting the trade-off between deployment independence and increased latency.

### Example 2 — Database technology choice

**Input:** User asks to review a decision to use a document store for a heavily relational dataset.  
**Expected output:** Report highlighting the data integrity (Critical) and query complexity (High) risks, recommending either a relational store or a hybrid approach with explicit join patterns.

## Notes

- If the user provides insufficient detail, ask one targeted clarifying question before proceeding — do not invent architecture details.
- Do not rate a quality attribute as `Strong` without citing specific evidence from the provided material.
- Keep findings to the most impactful items; a ten-page list of nitpicks is less useful than three actionable priorities.
