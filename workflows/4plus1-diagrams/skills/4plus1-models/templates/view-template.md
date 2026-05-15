# [System name] — [View name] view

**Audience:** [who reads this]
**Takeaway:** [the one thing the audience should understand after reading]
**Version:** [semver or date]
**Owner:** [team or individual accountable for keeping this accurate]
**Last reviewed:** [date]

---

## 1. Overview

[3–5 sentences. What the view shows and what it does NOT show. Link to the other views.]

## 2. Scope

**In scope:**
- [Bullet list]

**Out of scope (covered elsewhere):**
- [Bullet list — link to the other view that does cover it]

## 3. Diagram

```mermaid
[Diagram source here]
```

*[Or for PlantUML-based views, link to the .puml file and embed a rendered image.]*

## 4. [View-specific content section]

*This section varies by view. See the view's reference file (`references/[view-name]-view.md`) for the exact structure.*

Typical sections:
- **Components** / **Processes** / **Modules** / **Deployment units** / **Scenarios** — one subsection per element, with name, responsibility, relationships.
- **Interfaces / Relationships / Dependencies** — tabulated.
- **Non-functional properties** — availability, latency, throughput, security posture.

## 5. Rationale

Document the architectural decisions made for this view. For each significant decision:

**Decision:** [the choice made]
**Driver:** [the quality attribute or constraint that drove it]
**Alternatives considered:** [what was rejected, and why]
**Consequences:** [what this decision forces on the rest of the system]

## 6. Concerns

Flag each concern that applies, using a blockquote. Only flag real issues — not boilerplate.

> **Concern (GDPR):** [specific issue detected in this view, plus recommended mitigation]

> **Concern (Security):** [specific issue, mitigation]

> **Concern (Bias/fairness):** [specific issue, mitigation]

## 7. Assumptions

If this view was generated from partial context, mark every inference:

> **Assumption:** [what was inferred, and on what basis]

## 8. Open questions

Explicit list of decisions not yet made, with the stakeholders who need to make them.

- **Q1:** [question]
  - Owner: [role / team]
  - Deadline: [date]
  - Impact if unresolved: [what breaks or gets risky]

## 9. Related views

- **[Other view name]:** [one line — what that view covers that supplements this one]
- **[Another view]:** [one line]

## 10. Change log

| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | [name] | Initial version |
