# GitHub Copilot — Manager & Lead Guide

For engineering managers and tech leads supporting a team through Copilot adoption.

---

## 1. What Copilot actually does

Copilot is an AI coding assistant that runs inside the developer's IDE. It does two things:

- **Inline completions** — suggests code as the developer types, accepted with `Tab`.
- **Chat** — answers questions, explains code, generates tests and documentation.

It does not write code autonomously, push commits, or make decisions. The developer stays in control of every keystroke.

---

## 2. What to expect during adoption

Adoption follows a predictable curve:

| Phase | Timeframe | What you'll see |
| --- | --- | --- |
| Novelty | Week 1–2 | High engagement, exploring features |
| Friction | Week 2–4 | Some frustration — suggestions aren't always right |
| Integration | Month 2–3 | Developers find their own workflow patterns |
| Habit | Month 3+ | Consistent use, measurable time savings |

The friction phase is normal. Developers who push through it become the strongest users.

---

## 3. How to support your team

**Do:**
- Share the [getting-started guide](getting-started.md) and [cheat sheet](cheat-sheet.md) on day 1.
- Give developers time to experiment — block 1–2 hours in week 1.
- Create space to share what's working (team chat channel, retro item).
- Ask "what did Copilot help you with this week?" in 1:1s.
- Normalise rejecting suggestions — accepting bad output is the risk, not using the tool.

**Don't:**
- Set acceptance rate targets or quotas. Gaming metrics produces bad code.
- Assume Copilot replaces code review. It doesn't — review standards stay the same.
- Judge adoption speed. Some developers take longer to integrate it into their workflow.
- Use Copilot metrics as a performance indicator for individuals.

---

## 4. Addressing common concerns

**"I don't want AI writing my code."**
Copilot is autocomplete, not autopilot. You accept or reject every suggestion. Most developers use it for the tedious parts — boilerplate, tests, documentation — and write the interesting logic themselves.

**"How do I know the suggestions are correct?"**
You don't, until you review them. The same way you'd review any code. Copilot is fast but not infallible — it's your job to verify.

**"What about my data? Is our code being shared?"**
With Copilot Business/Enterprise: prompts and suggestions are not used for model training and are not retained. See [responsible-use.md](responsible-use.md) for details.

**"Won't this make developers lazy/deskill?"**
Research is mixed. The risk is real for junior developers who accept suggestions without understanding them. Encourage understanding over acceptance. Use Copilot's `/explain` feature to learn from suggestions, not just take them.

---

## 5. What metrics to watch

| Metric | Where to find it | What it tells you |
| --- | --- | --- |
| Acceptance rate | GitHub Copilot dashboard | Quality of suggestions for this team/codebase |
| Active users | GitHub Copilot dashboard | Who is actually using it |
| Suggestions shown | GitHub Copilot dashboard | Copilot is active and triggering |
| Team sentiment | Your own surveys | Whether the tool is helping or creating friction |

See [measuring-impact.md](measuring-impact.md) for the full framework.

**Avoid:** tracking acceptance rate per individual. It creates incentives to accept bad suggestions.

---

## 6. 30-day check-in questions

Ask your team at the 30-day mark:

1. Which tasks has Copilot helped most with?
2. Where has it been unhelpful or frustrating?
3. Have you changed how you write comments or function signatures?
4. Is there anything you tried and stopped? Why?
5. What would make it more useful?

Feed the answers back into the team's `.github/copilot-instructions.md`.
