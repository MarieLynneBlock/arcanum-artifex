---
name: risk-analysis
description: >
  Identify, classify, and prioritise risks for a project, system, decision, or
  change, and produce a risk register with mitigation strategies. Use when a
  user wants to surface and manage risks before or during a project or
  architectural change.
version: 1.0.0
authors:
  - Marie-Lynne Block
tags:
  - risk
  - risk-register
  - mitigation
  - planning
---

## What this skill does

Provides a structured framework for risk identification and assessment. It surfaces risks across relevant categories (technical, operational, security, compliance, delivery, people), scores them by likelihood and impact, and produces a prioritised risk register with mitigation and contingency strategies.

## When to use it

- User asks to "identify risks", "assess risks", or "what could go wrong" for a project, system, or decision.
- User is planning a migration, release, architectural change, or new initiative.
- User needs a risk register for a project plan or design review.
- User wants to prepare for a pre-mortem exercise.

## Instructions

1. **Define the subject.** Confirm what is being assessed: a project, a system, a specific change, or a decision.

2. **Set the scope.** Identify which risk categories are in scope. Default categories:
   - **Technical** — complexity, unknown unknowns, integration points, technical debt.
   - **Operational** — deployment, monitoring, incident response, runbook gaps.
   - **Security** — attack surface, data exposure, credential management, third-party dependencies.
   - **Compliance** — regulatory, audit, data residency, licensing.
   - **Delivery** — timeline, dependencies, resource constraints, scope creep.
   - **People** — key-person dependency, skill gaps, team bandwidth.

3. **Identify risks.** For each category, enumerate plausible risks. Use "If X happens, then Y" framing to keep risks concrete.

4. **Score each risk.**
   - **Likelihood:** `High` (likely to occur) / `Medium` (possible) / `Low` (unlikely but plausible).
   - **Impact:** `Critical` (project/system-threatening) / `High` (significant disruption) / `Medium` (manageable) / `Low` (minor).
   - **Priority score** = Likelihood × Impact (use the matrix below).

   | | Critical | High | Medium | Low |
   |---|---|---|---|---|
   | **High likelihood** | P1 | P1 | P2 | P3 |
   | **Medium likelihood** | P1 | P2 | P3 | P4 |
   | **Low likelihood** | P2 | P3 | P4 | P4 |

5. **Define responses.** For each P1/P2 risk:
   - **Mitigation** — action taken now to reduce likelihood or impact.
   - **Contingency** — action taken if the risk materialises.
   - **Owner** — role or team responsible.

6. **Produce the report** using the output format below.

## Output format

```markdown
# Risk Analysis: [Subject]

**Date:** YYYY-MM-DD  
**Analyst:** [name or AI-assisted]  
**Subject:** [what is being assessed]

---

## Risk Register

| ID  | Category   | Risk description                       | Likelihood | Impact   | Priority | Mitigation                    | Contingency                   | Owner     |
|-----|------------|----------------------------------------|------------|----------|----------|-------------------------------|-------------------------------|-----------|
| R01 | Technical  | [If X happens, Y consequence]          | High       | Critical | P1       | [action to reduce risk]       | [action if risk occurs]       | [role]    |
| R02 | Delivery   | [If X happens, Y consequence]          | Medium     | High     | P2       | [action to reduce risk]       | [action if risk occurs]       | [role]    |
| ...  | ...        | ...                                    | ...        | ...      | ...      | ...                           | ...                           | ...       |

---

## P1 Risks — Immediate attention required

### R01 — [Risk title]

**Description:** [Full description of the risk and its trigger.]  
**Why it matters:** [Consequence if it materialises.]  
**Mitigation:** [Concrete steps to take now.]  
**Contingency:** [Plan B if mitigation fails.]  

---

## Risk summary

| Priority | Count | Top concern |
|----------|-------|-------------|
| P1       | n     | ...         |
| P2       | n     | ...         |
| P3       | n     | ...         |
| P4       | n     | ...         |

**Overall risk level:** [Low / Moderate / High / Critical]

[2–3 sentence narrative: what is the dominant risk theme and what single action would most reduce overall exposure?]
```

## Examples

### Example 1 — Database migration risk analysis

**Input:** "We're migrating from PostgreSQL 12 to 16. What are the risks?"  
**Expected output:** Risk register covering technical risks (query plan changes, deprecated syntax), operational risks (rollback window, replication lag), delivery risks (timeline), and security risks (new default settings). P1 risks expanded with concrete mitigation steps.

### Example 2 — New third-party API integration

**Input:** "Assess the risks of integrating with a new payment provider."  
**Expected output:** Risk register with security (P1: credential exposure, API key rotation), compliance (P1: PCI scope expansion), technical (P2: rate limits, outage handling), and delivery (P3: integration timeline) risks.

## Notes

- A risk must have a plausible trigger — do not list generic concerns without grounding them in the specific subject.
- "No risks identified" in a category is a valid finding; state it explicitly rather than omitting the category.
- When the user has not specified an owner role, leave the Owner field as `[TBD]` rather than inventing one.
- Keep the risk register as a single source of truth — do not duplicate risk details in multiple places in the report.
