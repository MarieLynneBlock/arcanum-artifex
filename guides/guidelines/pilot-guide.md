# GitHub Copilot — Pilot Guide

How to run a structured 60-day pilot before a full enterprise rollout.

---

## 1. Why run a pilot

A pilot lets you:

- Validate that Copilot works in your environment (proxy, network, IDE mix).
- Identify team-specific friction before it affects everyone.
- Build internal advocates who can support wider rollout.
- Gather baseline metrics to demonstrate ROI.
- Surface governance issues (data handling, acceptable use) at small scale.

---

## 2. Pilot structure

| Phase | Duration | Focus |
| --- | --- | --- |
| Setup | Week 1 | Access, install, baseline metrics |
| Exploration | Week 2–3 | Guided use, workshops, Q&A |
| Integration | Week 4–6 | Unguided use in real work |
| Evaluation | Week 7–8 | Metrics review, feedback, decision |

---

## 3. Who to include

**Target group size:** 10–30 developers.

**Include:**

- A mix of experience levels (senior, mid, junior).
- At least one representative from each IDE in use.
- A mix of willing adopters and skeptics — you need honest feedback, not just enthusiasm.
- At least one tech lead or architect.

**Avoid:**

- Selecting only volunteers — you'll get survivorship bias.
- Teams under immediate delivery pressure — they won't have time to experiment.

---

## 4. Baseline metrics (collect before day 1)

Before the pilot starts, record:

- Time spent per week on: writing boilerplate, writing tests, writing documentation.
- Developer satisfaction score (simple 1–5 survey).
- Code review cycle time (PR open → merged).
- Bug rate or defect escape rate (if measurable).

Use the same measures at the end of the pilot for comparison.

---

## 5. Week-by-week plan

### Week 1 — Setup

- Grant seats and confirm access for all participants.
- Share [getting-started.md](../how-to/getting-started.md) and [responsible-use.md](responsible-use.md).
- Run IDE setup session (30 min, by IDE type).
- Record baseline metrics.
- Create a shared channel for questions and sharing.

### Week 2–3 — Exploration

- Run the [completions workshop](../../workshops/01-completions.md).
- Run the [chat and participants workshop](../../workshops/02-chat-and-participants.md).
- Run the [prompt engineering workshop](../../workshops/03-prompt-engineering.md).
- Weekly 15-min check-in: what worked, what didn't.

### Week 4–6 — Integration

- No structured sessions — developers use Copilot in real work.
- Coach available for questions.
- Encourage sharing wins in the shared channel.
- Mid-pilot survey at week 5 (5 questions, 5 minutes).

### Week 7–8 — Evaluation

- Collect end metrics (same as baseline).
- Run end-of-pilot survey.
- Hold a retrospective: wins, friction points, changes needed.
- Prepare rollout recommendation.

---

## 6. Mid-pilot survey (week 5)

Send to all participants:

1. How often are you using Copilot? (Daily / A few times a week / Rarely / Not at all)
2. Which tasks has it helped with most? (Free text)
3. Where has it been unhelpful or frustrating? (Free text)
4. How confident are you reviewing AI-generated code before accepting? (1–5)
5. Would you recommend Copilot to a colleague? (Yes / No / Maybe)

---

## 7. Go / no-go criteria

Recommend full rollout if:

- Acceptance rate is above 25% (industry benchmark for healthy use).
- Majority of participants report time savings on at least one task type.
- No unresolved governance or security issues.
- No significant negative impact on code quality (from review data or defect rates).

Flag for further review if:

- Proxy or network issues affected more than 20% of participants.
- Acceptance rate is below 15% (suggestions aren't relevant — may need better instructions).
- Security or data handling concerns were raised and not resolved.

---

## 8. Rollout recommendation template

At pilot close, produce a one-page summary:

```text
Pilot summary — GitHub Copilot
Period: [dates]
Participants: [n] developers across [IDE list]

Key findings:
- Acceptance rate: [x]%
- Active users at week 8: [x] of [n]
- Top use cases: [list]
- Main friction points: [list]

Metrics delta:
- [Metric]: before [x] → after [y]

Governance:
- Responsible use guide shared: Yes/No
- Security guide shared: Yes/No
- Content exclusions configured: Yes/No

Recommendation: [Full rollout / Phased rollout / Hold]
Next steps: [list]
```
