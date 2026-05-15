---
description: >
name: write-epic
version: 1.0.0
tags:
  - agile
  - epic
  - requirements
  - backlog
  - roadmap
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Produces a complete epic definition following Atlassian agile guidance. An epic captures a large initiative that is too big for a single sprint and must be decomposed into user stories. This skill writes the epic statement, defines in-scope and out-of-scope boundaries, identifies success metrics, and drafts an initial story map to guide decomposition.

**Reference:** Atlassian — [User stories with examples and a template](https://www.atlassian.com/agile/project-management/user-stories)

## When to use it

- User asks to "write an epic" or "define an initiative" for a feature area or product goal.
- User has a large, multi-sprint requirement and needs to frame it before decomposing it into stories.
- User wants to communicate a roadmap item to stakeholders before stories are written.
- User is decomposing an epic and needs the parent definition to stay aligned.

## Key concepts

### Epic vs. user story

| | Epic | User Story |
| --- | --- | --- |
| **Size** | Multiple sprints | Fits in one sprint |
| **Granularity** | Strategic intent | Specific capability |
| **Audience** | Stakeholders + team | Team |
| **Detail** | Goal + boundaries + metrics | Action + benefit + acceptance criteria |
| **Completeness** | Done when all child stories are done | Done when acceptance criteria pass |

### Epic goal statement

An epic does not use the Connextra ("As a … I want … so that …") template directly — it uses a **goal statement** that captures the initiative and its business value:

```
[Initiative name]: [what we are building or enabling] so that [business/user outcome].
```

Or, for epics that span multiple personas, use a plain statement:

```
Enable [capability] for [scope] to achieve [measurable outcome].
```

### Story map

An epic's initial story map is a flat list of the user stories (or story themes) that will together deliver the epic. It does not need to be exhaustive at the time of writing — it should cover the known scope and flag known unknowns.

## Instructions

1. **Name the epic.** A short, active-voice label (e.g., "Guest Checkout", "Multi-currency Support", "Admin Audit Logs").

2. **Write the goal statement.** State what the epic delivers and why it matters to the business or users. Avoid solution language at this stage.

3. **Define scope boundaries.**
   - **In scope:** capabilities or outcomes that will be part of this epic.
   - **Out of scope:** related things that will NOT be addressed — this prevents scope creep and sets stakeholder expectations.

4. **Identify personas.** List the user types who benefit from this epic.

5. **Define success metrics.** What measurable outcomes will confirm the epic delivered value? (Conversion rate, error rate, time-on-task, support tickets, etc.)

6. **Draft the story map.** List the major user stories or story themes this epic will be broken into. Use the user story format ("As a … I want … so that …") for each, or a theme label if stories are not yet written.

7. **Flag dependencies and risks.** List other epics, systems, or teams this epic depends on, and any known risks.

8. **Produce the output** using the format below.

## Output format

```markdown
# Epic: [Name]

**Goal:** [Initiative name]: [what we are building or enabling] so that [business/user outcome].

**Personas:** [Comma-separated list of user roles who benefit]

---

## Scope

### In scope

- [Capability or outcome 1]
- [Capability or outcome 2]

### Out of scope

- [Related thing explicitly excluded]
- [Related thing explicitly excluded]

---

## Success metrics

| Metric | Baseline | Target |
| --- | --- | --- |
| [metric name] | [current value or "unknown"] | [goal value] |

---

## Story map (initial)

> Stories to be written and refined during sprint planning. This is a scope guide, not a commitment.

1. As a [persona], I want to [action] so that [benefit].
2. As a [persona], I want to [action] so that [benefit].
3. [Story theme: more detail TBD]

---

## Dependencies

- [Epic / system / team this depends on]

## Risks

- [Known risk or open question]

## Notes

- [Assumptions, stakeholder constraints, or timeline context]
```

## Examples

### Example 1 — Guest checkout

**Input:** "Write an epic for allowing users to check out without creating an account."

**Expected output:**

```markdown
# Epic: Guest Checkout

**Goal:** Enable customers to complete a purchase without registering an account so that conversion rate improves for first-time buyers.

**Personas:** First-time shopper, returning customer who prefers not to log in.

## Scope

### In scope
- Checkout flow without mandatory account creation.
- Order confirmation email to the provided address.
- Option to create an account post-purchase.

### Out of scope
- Saving payment methods for guests.
- Guest order history (requires account).

## Success metrics

| Metric | Baseline | Target |
| --- | --- | --- |
| Checkout conversion rate (unauthenticated) | 18% | 28% |
| Account creation drop-off | 42% | < 20% |

## Story map (initial)

1. As a guest shopper, I want to enter my email and shipping details without registering, so that I can check out quickly.
2. As a guest shopper, I want to receive an order confirmation email, so that I have proof of purchase.
3. As a guest shopper, I want to be offered the option to create an account after purchase, so that I can track future orders if I choose to.
```

### Example 2 — Vague input requiring scoping

**Input:** "We need an epic for notifications."

**Expected output:** Skill flags that "notifications" is too broad to define as a single epic. It asks clarifying questions: Which notification channels (email, push, in-app)? Which events trigger notifications? Which personas? The output drafts a scoped epic (e.g., "In-app Notifications for Order Status") with explicit out-of-scope items (email campaigns, push notifications).

## Notes

- An epic is not a project plan; it should not prescribe implementation order or sprint assignments.
- The story map is a discovery tool, not a contract. Stories will be added, removed, and split during refinement.
- Success metrics must be measurable. "Improve UX" is not a metric; "reduce time-to-checkout by 30%" is.
- If the user describes something completable in one sprint, suggest writing a user story instead of an epic.
- Avoid nesting epics inside epics — if the scope is that large, consider a programme or initiative layer instead.
