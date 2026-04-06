---
name: stakeholder-map
description: >
  Identify and map stakeholders on an influence × interest grid, classify their
  engagement stance, and produce an engagement strategy per quadrant. Use when
  starting an initiative, change programme, or project and needing to understand
  who to involve, inform, and manage.
version: 1.0.0
authors:
  - Marie-Lynne Block
tags:
  - stakeholder
  - influence
  - interest
  - engagement
  - change-management
---

## What this skill does

Produces a stakeholder map structured around the classic influence × interest grid (also called a power/interest matrix). It classifies each stakeholder, recommends an engagement strategy per quadrant, and surfaces alignment risks — stakeholders who are high-influence but opposed or unengaged.

## When to use it

- User is starting a project, initiative, or change programme and needs to identify who to involve.
- User asks to "map stakeholders", "identify stakeholders", or "who do we need to engage?".
- User wants to plan communication and engagement activities before or during a project.
- User needs to feed stakeholder context into a `risk-analysis` or `write-epic`.

## Key concepts

### Influence × Interest grid

```
High influence │ MANAGE CLOSELY    │ KEEP SATISFIED
               │ (high interest)   │ (low interest)
───────────────┼───────────────────┼───────────────
Low influence  │ KEEP INFORMED     │ MONITOR
               │ (high interest)   │ (low interest)
```

| Quadrant | Strategy |
| --- | --- |
| **Manage closely** | High influence, high interest. Active partners — involve in decisions, seek input regularly, address concerns proactively. |
| **Keep satisfied** | High influence, low interest. Keep onside — brief regularly, avoid surprises, escalate issues early. |
| **Keep informed** | Low influence, high interest. Invested audience — share progress updates, invite feedback, manage expectations. |
| **Monitor** | Low influence, low interest. Peripheral — include in broad communications, revisit if their role changes. |

### Engagement stance

Classify each stakeholder's current stance toward the initiative:

| Stance | Symbol | Meaning |
| --- | --- | --- |
| Champion | ++ | Actively supports and promotes |
| Supporter | + | Supportive but not vocal |
| Neutral | = | No strong position |
| Sceptic | - | Has concerns, can be won over |
| Blocker | -- | Actively opposed |

### Alignment risk

A stakeholder is an **alignment risk** if they are in the "Manage closely" quadrant with a stance of Sceptic or Blocker.

## Instructions

1. **Identify the initiative.** State what the project or change is — this determines whose interests are relevant.

2. **Enumerate stakeholders.** From the user's description, list all individuals, roles, or groups who:
   - Are affected by the initiative.
   - Have decision-making or approval authority.
   - Control resources the initiative needs.
   - Have subject-matter expertise the initiative relies on.
   - Could block or accelerate progress.

3. **Rate each stakeholder.**
   - **Influence** (High / Medium / Low): their ability to affect the outcome.
   - **Interest** (High / Medium / Low): how much they care about the outcome.
   - **Stance** (++, +, =, -, --): their current position toward the initiative.

4. **Place stakeholders in the grid.** Treat Medium influence/interest as High for placement purposes (err toward more engagement, not less).

5. **Identify alignment risks.** Flag any "Manage closely" stakeholder with a Sceptic or Blocker stance. These require immediate attention.

6. **Write engagement actions.** For each alignment risk and each "Manage closely" stakeholder, suggest a specific engagement action.

7. **Produce the report** using the output format below.

## Output format

```markdown
# Stakeholder Map: [Initiative name]

**Date:** YYYY-MM-DD  
**Analyst:** [name or AI-assisted]  
**Initiative:** [brief description]

---

## Stakeholder Register

| Stakeholder | Role / Group | Influence | Interest | Stance | Quadrant | Alignment risk? |
| --- | --- | --- | --- | --- | --- | --- |
| [Name/Role] | [Team or org] | High | High | + | Manage closely | No |
| [Name/Role] | [Team or org] | High | Low | = | Keep satisfied | No |
| [Name/Role] | [Team or org] | Low | High | ++ | Keep informed | No |
| [Name/Role] | [Team or org] | High | High | -- | Manage closely | **YES** |

---

## Grid view

```
High influence │ [Names]           │ [Names]
───────────────┼───────────────────┼──────────────
Low influence  │ [Names]           │ [Names]
               │ High interest     │ Low interest
```

---

## Alignment risks

| Stakeholder | Concern | Recommended action |
| --- | --- | --- |
| [Name] | [What they are opposed to or concerned about] | [Specific engagement action] |

---

## Engagement strategy

### Manage closely

- **Cadence:** [e.g., weekly check-in, steering group attendance]
- **Channel:** [e.g., direct meeting, shared workspace]
- **Key actions:** [Decisions to involve them in, concerns to address]

### Keep satisfied

- **Cadence:** [e.g., fortnightly briefing]
- **Channel:** [e.g., executive summary email]
- **Key actions:** [Topics to cover proactively]

### Keep informed

- **Cadence:** [e.g., sprint review invite, monthly newsletter]
- **Channel:** [e.g., shared doc, demo invite]

### Monitor

- **Cadence:** [e.g., quarterly]
- **Channel:** [e.g., all-hands update]

---

## Open questions

- [Stakeholders not yet identified or whose stance is unknown]
```

## Examples

### Example 1 — Cloud migration initiative

**Input:** "Map stakeholders for our migration from on-prem to AWS. Key people: CTO (sponsor), CISO (concerned about security), Head of Ops (will run it), Finance director (budget approval), Dev team leads (affected users), external auditor (compliance)."

**Expected output:** Full stakeholder register. CISO and Finance director flagged as Keep satisfied. CISO marked as alignment risk if stance is Sceptic. Engagement strategy with weekly CTO/Head of Ops meeting and fortnightly CISO security briefing.

### Example 2 — Vague stakeholder list

**Input:** "We need to map stakeholders for our new data platform."

**Expected output:** Skill infers likely stakeholders (data engineering, data consumers, IT, security, finance) and asks the user to confirm names, roles, and stances before rating them. Does not assume influence or interest without input.

## Notes

- Do not assign a stance of Blocker without evidence — if the user has not stated a stakeholder's position, default to Neutral and flag it as unknown.
- Influence is about the current initiative, not seniority in general. A junior engineer who owns a critical dependency may have High influence on a technical project.
- Stakeholder maps go stale. Note the date and recommend revisiting at major project milestones.
- This skill pairs with `risk-analysis` (alignment risks become people risks) and `miro-board` (the grid maps directly to a 2×2 Miro frame).
