---
name: gap-analysis
description: >
  Produce a structured gap analysis comparing current state to a desired target
  state across defined dimensions, with prioritised gaps and recommended
  actions. Use when a user needs to identify what is missing or insufficient
  before planning a change, migration, or improvement initiative.
version: 1.0.0
authors:
  - Marie-Lynne Block
tags:
  - analysis
  - gap-analysis
  - current-state
  - target-state
  - planning
---

## What this skill does

Provides a repeatable framework for identifying and prioritising gaps between where things are now and where they need to be. It structures the analysis by dimension (process, data, technology, people, compliance, etc.), scores each gap by severity, and produces actionable recommendations with ownership.

## When to use it

- User asks to "identify gaps", "do a gap analysis", or "compare current to target state".
- User is preparing for a migration, transformation, audit, or initiative and needs to understand what needs to change.
- User needs evidence to justify a project or roadmap item.
- User wants to feed results into a `miro-board`, `risk-analysis`, or `tradeoff-analysis`.

## Key concepts

### Dimensions

A gap analysis is organised by **dimension** — the aspect of the system or organisation being assessed. Choose dimensions that are relevant to the subject:

| Dimension | What it covers |
| --- | --- |
| Process | How work is done; workflows, steps, handoffs |
| Data | Data availability, quality, structure, lineage |
| Technology | Tools, systems, integrations, infrastructure |
| People | Skills, roles, capacity, knowledge |
| Compliance | Regulatory, policy, or audit requirements |
| Performance | SLAs, KPIs, benchmarks |
| Documentation | Specs, runbooks, architecture records |

### Severity

| Severity | Meaning |
| --- | --- |
| Critical | Blocks the target state; must close before proceeding |
| High | Significant risk or rework if not addressed early |
| Medium | Important but manageable; schedule in backlog |
| Low | Nice to fix; low impact if deferred |

## Instructions

1. **Define the subject.** Confirm what is being compared: a system, a process, a team capability, a product area.

2. **Establish the target state.** If the user has not defined it, ask. The target state must be specific enough to measure against — not "be more agile" but "deploy to production daily with zero manual steps".

3. **Select dimensions.** Choose the dimensions relevant to the subject. Do not include dimensions where there is nothing to compare.

4. **Assess each dimension.**
   For each dimension:
   - Describe the **current state** in one or two sentences with evidence.
   - Describe the **target state** for that dimension.
   - Identify the **gap** — what is missing, insufficient, or misaligned.
   - Assign a **severity**.

5. **Identify root causes** for Critical/High gaps where the cause is not obvious.

6. **Write recommendations.** For each Critical/High gap, provide a concrete action, an owner role, and an indication of whether it is a quick fix or a larger initiative.

7. **Produce the report** using the output format below.

## Output format

```markdown
# Gap Analysis: [Subject]

**Date:** YYYY-MM-DD  
**Analyst:** [name or AI-assisted]  
**Subject:** [what is being assessed]  
**Target state:** [one-sentence definition of the desired end state]

---

## Summary

| Severity | Count | Top gap |
| --- | --- | --- |
| Critical | n | ... |
| High | n | ... |
| Medium | n | ... |
| Low | n | ... |

**Overall readiness:** [Not ready / Partially ready / Mostly ready / Ready]

[2–3 sentence narrative: what is the dominant gap theme and what single action would most accelerate progress toward the target state?]

---

## Gap Register

### [Dimension] — [Severity]

| | Detail |
| --- | --- |
| **Current state** | [Evidence-based description] |
| **Target state** | [What good looks like for this dimension] |
| **Gap** | [What is missing or insufficient] |
| **Root cause** | [Why the gap exists — if known] |
| **Recommendation** | [Concrete action] |
| **Owner** | [Role or team] |
| **Effort** | Quick fix / Sprint / Initiative |

---

## Recommended actions (priority order)

1. [Action] — Owner: [role] — Effort: [size]
2. [Action] — Owner: [role] — Effort: [size]
```

## Examples

### Example 1 — CI/CD maturity gap analysis

**Input:** "We want to move to daily deployments. Currently we deploy manually once a month."

**Expected output:** Gap register covering: Technology (no pipeline — Critical), Process (no deployment runbook — High), People (no on-call rotation — High), Documentation (no rollback procedure — Medium). Recommended actions in priority order with owner roles.

### Example 2 — Data readiness for ML project

**Input:** "We want to build a churn prediction model. Assess whether our data is ready."

**Expected output:** Dimensions: Data (label availability, data quality, historical coverage), Technology (feature store, training infrastructure), People (ML engineering capacity). Each dimension assessed against ML-ready target state.

## Notes

- Never describe the current state in terms of the gap ("current state: no monitoring" — that is the gap, not the state). Describe what does exist, then state what is missing.
- If evidence for the current state is not provided, flag it as an assumption rather than stating it as fact.
- A gap analysis is not a project plan — do not assign dates or sprint numbers unless the user requests it.
- This skill integrates naturally with `risk-analysis` (gaps often surface risks) and `miro-board` (gap columns map directly to a three-column Miro board).
