# GitHub Copilot — Measuring Impact

How to measure whether Copilot is delivering value in your organisation.

---

## 1. The metrics dashboard (Business & Enterprise)

GitHub provides a built-in metrics dashboard for org admins.

**Access:** GitHub org → Settings → Copilot → Usage

| Metric | What it means |
| --- | --- |
| **Acceptance rate** | % of shown suggestions accepted (via `Tab`) |
| **Suggestions shown** | Total completions Copilot offered |
| **Suggestions accepted** | Total completions accepted |
| **Active users** | Users with at least one suggestion shown in the period |
| **Lines of code accepted** | Volume of AI-generated code accepted |

**Filter by:** repository, team, language, editor, date range.

**API access:** Metrics are also available via the [GitHub REST API](https://docs.github.com/en/rest/copilot/copilot-metrics) for custom dashboards.

---

## 2. Benchmarks

| Metric | Low | Healthy | High |
| --- | --- | --- | --- |
| Acceptance rate | < 15% | 25–35% | > 40% |
| Active users / seats | < 40% | 60–80% | > 85% |

**Acceptance rate below 15%:** suggestions aren't relevant — review the `.github/copilot-instructions.md`, language settings, or whether the codebase is a good fit for Copilot.

**Active users below 40%:** adoption is stalling — run workshops, identify and address friction points.

---

## 3. What the dashboard doesn't tell you

The built-in metrics measure activity, not value. They don't tell you:

- Whether accepted code was correct.
- Whether accepted code passed review or caused bugs.
- How much time was saved.
- Developer satisfaction.

Pair dashboard metrics with qualitative data.

---

## 4. Qualitative measurement

### Pulse survey (monthly, 5 questions, < 3 minutes)

1. How often do you use Copilot? (Daily / Weekly / Rarely / Never)
2. Which tasks has it helped with most this month? (Free text)
3. Where has it been unhelpful or frustrating? (Free text)
4. On a scale of 1–5, how much does Copilot speed up your work?
5. Is there anything that would make it more useful? (Free text)

Run monthly for the first 6 months, quarterly after that.

### Retro items

Add a standing retro item: *"One thing Copilot helped with / one thing it didn't."*
Low-effort, high-signal — surfaces real workflow impact.

---

## 5. Time-saving estimation

A rough framework for estimating time saved:

```
Time saved per week =
  (suggestions accepted per week) × (avg time to write that code manually)
```

GitHub's own research suggests developers report completing tasks ~55% faster with Copilot. Use a conservative estimate (20–30%) for internal reporting.

For a team of 20 developers:
- 30 suggestions accepted/day × 5 days × 2 min saved each = **50 hours/week**
- At a blended rate of €80/hr: **~€4,000/week** in estimated value

Use these calculations to frame ROI conversations — but be honest about the assumptions.

---

## 6. Code quality indicators

Copilot's impact on quality is harder to measure but worth tracking:

| Indicator | How to measure |
| --- | --- |
| Bug rate | Defects per sprint / per 1000 lines — compare pre/post adoption |
| PR review cycles | Time from PR open to merge — faster may indicate cleaner first drafts |
| Test coverage | Coverage % over time — Copilot tends to increase test writing |
| SAST findings | New vulnerability findings — watch for increase after adoption |

**Important:** if defect rates or SAST findings increase after adoption, investigate whether code review standards for AI-generated code need strengthening.

---

## 7. Reporting to stakeholders

A simple monthly summary for leadership:

```
GitHub Copilot — Monthly Report [Month Year]

Usage
- Active users: [x] of [n] seats ([x]%)
- Acceptance rate: [x]%
- Lines accepted: [x]

Highlights
- [What the team reported as most useful]
- [Any friction points identified and addressed]

Estimated impact
- Estimated time saved: [x] hrs/week
- Estimated value: [€x]/week

Actions this month
- [e.g. Updated copilot-instructions.md for Java team]
- [e.g. Ran prompt engineering workshop with backend team]

Next month
- [Planned actions]
```
