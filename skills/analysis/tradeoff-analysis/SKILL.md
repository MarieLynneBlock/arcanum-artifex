---
name: tradeoff-analysis
description: >-
  Provides a structured framework for comparing options under uncertainty. It surfaces criteria,
  weights them by stated priorities, scores each option, and produces a transparent recommendation
  — including the conditions under which a different option would be the right call.
version: 1.0.0
tags:
  - decision-making
  - trade-offs
  - comparison
  - options-analysis
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Provides a structured framework for comparing options under uncertainty. It surfaces criteria, weights them by stated priorities, scores each option, and produces a transparent recommendation — including the conditions under which a different option would be the right call.

## When to use it

- User asks "should we use X or Y?", "which approach is better?", or "help me decide between…".
- User needs to document a decision and its rationale for a team or stakeholder.
- User wants to understand the trade-offs before committing to a direction.
- User is revisiting a past decision to validate or challenge it.

## Instructions

1. **Name the decision.** State the decision being made in one sentence as a question (e.g., "Which message broker should we use for the order pipeline?").

2. **Enumerate the options.** List all options under consideration. If the user has provided fewer than two, ask for alternatives before proceeding.

3. **Elicit criteria.** Identify the decision criteria from the user's context. Group into:
   - **Must-haves** (constraints that disqualify options if not met)
   - **Optimisation criteria** (factors to weigh and compare)

   Common criteria to consider: cost, performance, operational complexity, team expertise, vendor lock-in, time to implement, scalability, security, ecosystem maturity.

4. **Weight the criteria.** If the user has stated priorities, assign relative weights (High / Medium / Low or a 1–5 scale). Make weights explicit, not hidden.

5. **Score each option.** For each optimisation criterion, rate each option (`Strong` / `Adequate` / `Weak`) with a brief justification. Apply must-haves as pass/fail gates first.

6. **Identify the dominant option.** Summarise which option scores best overall. Note any criteria where a different option clearly wins.

7. **State the recommendation** with explicit conditions: "We recommend X. If [condition], Y becomes the better choice."

8. **Produce the report** using the output format below.

## Output format

```markdown
# Trade-off Analysis: [Decision question]

**Date:** YYYY-MM-DD  
**Decision owner:** [name or team]  
**Options considered:** [Option A, Option B, …]

---

## Must-haves (pass/fail)

| Criterion         | Option A | Option B |
|-------------------|----------|----------|
| [constraint]      | Pass / Fail | Pass / Fail |

*Options that fail any must-have are eliminated from further analysis.*

---

## Comparison

**Criteria weights:** [High = 3, Medium = 2, Low = 1]

| Criterion         | Weight | Option A | Option B | Notes |
|-------------------|--------|----------|----------|-------|
| [criterion]       | High   | Strong   | Adequate | ...   |
| [criterion]       | Medium | Weak     | Strong   | ...   |

---

## Summary scores

| Option   | Weighted score | Strengths                  | Weaknesses              |
|----------|---------------|----------------------------|-------------------------|
| Option A | [n/total]     | ...                        | ...                     |
| Option B | [n/total]     | ...                        | ...                     |

---

## Recommendation

**Recommended:** [Option]

**Reasoning:** [2–3 sentences explaining the dominant factors.]

**Choose differently if:**
- [Condition 1] → prefer [alternative]
- [Condition 2] → prefer [alternative]

---

## Risks of the recommended option

- [Risk 1]
- [Risk 2]

## Open questions

- [Any unknowns that could change the recommendation]
```

## Examples

### Example 1 — Message broker selection

**Input:** "Should we use Kafka or RabbitMQ for our order pipeline? We need high throughput, the team knows RabbitMQ, and we can't afford a large ops burden."  
**Expected output:** Trade-off report weighting throughput (High), ops burden (High), and team expertise (Medium). Recommendation section stating which wins and under what conditions the other is better.

### Example 2 — Build vs. buy

**Input:** "We're deciding whether to build our own auth system or use an existing provider."  
**Expected output:** Report identifying must-haves (compliance requirements), scoring options on security, time to market, long-term cost, and control. Clear recommendation with the condition that triggers the alternative.

## Notes

- If criteria are missing or ambiguous, ask one targeted clarifying question before scoring.
- Do not hide weights or scoring inside a narrative — keep them in the table so the reasoning is auditable.
- Avoid the recommendation being purely score-mechanical: note qualitative factors that override the numbers if relevant.
- A "no clear winner" result is a valid output when options are genuinely close — state what new information would break the tie.
