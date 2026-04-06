---
name: write-user-story
description: >
  Draft a well-formed agile user story following the Atlassian format: persona,
  want, and benefit — with acceptance criteria and a definition of done. Use
  when a user wants to write, refine, or validate a user story.
version: 1.0.0
authors:
  - Marie-Lynne Block
tags:
  - agile
  - user-story
  - requirements
  - backlog
---

## What this skill does

Produces a complete, ready-to-groom user story following the standard Atlassian/agile format. It applies the INVEST criteria and the 3 Cs framework (Card, Conversation, Confirmation) to ensure each story is well-scoped, valuable, and testable — not just syntactically correct.

**Reference:** Atlassian — [User stories with examples and a template](https://www.atlassian.com/agile/project-management/user-stories)

## When to use it

- User asks to "write a user story" or "create a story" for a feature or requirement.
- User wants to refine a rough idea, acceptance note, or bug description into a proper story.
- User needs to validate whether an existing story is well-formed.
- User is decomposing an epic into individual stories.

## Key concepts

### The standard format (Connextra template)

```
As a [persona],
I want to [action / capability],
so that [benefit / outcome].
```

- **Persona** — who benefits (not "user" generically — use a real role: "logged-in customer", "warehouse operator", "admin").
- **Want** — the capability or action, not the implementation ("I want to filter results" not "I want a dropdown").
- **Benefit** — the why; if the benefit is obvious, keep it short but never omit it.

### INVEST criteria

A well-formed story is:

| Letter | Criterion | What to check |
| --- | --- | --- |
| **I** | Independent | Can be developed without another story blocking it? |
| **N** | Negotiable | Is it a conversation-starter, not a contract? |
| **V** | Valuable | Does it deliver value to the persona? |
| **E** | Estimable | Is it specific enough for the team to size? |
| **S** | Small | Completable within a single sprint? |
| **T** | Testable | Do the acceptance criteria make pass/fail possible? |

### 3 Cs

- **Card** — the written story (brief; a reminder, not a spec).
- **Conversation** — the discussion between team and stakeholders that fills in detail.
- **Confirmation** — the acceptance criteria that confirm the story is done.

## Instructions

1. **Identify the persona.** Use the most specific role that benefits from this story. Avoid "user" alone.

2. **State the want.** Describe what the persona wants to do, not how the system implements it. Focus on the outcome, not the feature.

3. **State the benefit.** Explain why this matters to the persona or the business. If the user did not provide one, infer it from context and flag it for confirmation.

4. **Write the story card** using the Connextra template.

5. **Check INVEST.** Flag any criterion the story fails and suggest a fix:
   - Too large → split into smaller stories.
   - Too vague to estimate → add a constraint or scope note.
   - Not independently deliverable → identify the dependency.

6. **Write acceptance criteria** using Given/When/Then (Gherkin) or a plain bulleted list if Gherkin is too heavyweight:
   - Each criterion must be independently verifiable.
   - Cover the happy path and at least one edge case.
   - Avoid implementation details in criteria.

7. **Add a Definition of Done reminder** (standard checklist unless the user provides a custom one).

8. **Produce the output** using the format below.

## Output format

```markdown
## User Story: [short title]

**As a** [persona],  
**I want to** [action],  
**so that** [benefit].

---

### Acceptance Criteria

- [ ] Given [context], when [action], then [outcome].
- [ ] Given [context], when [action], then [outcome].
- [ ] [Edge case or negative path]

### Definition of Done

- [ ] Acceptance criteria all pass.
- [ ] Code reviewed and merged.
- [ ] Unit/integration tests written and passing.
- [ ] Documented (if applicable).
- [ ] Deployed to staging and smoke-tested.

### INVEST check

| Criterion | Status | Note |
| --- | --- | --- |
| Independent | Pass / Fail | ... |
| Negotiable | Pass / Fail | ... |
| Valuable | Pass / Fail | ... |
| Estimable | Pass / Fail | ... |
| Small | Pass / Fail | ... |
| Testable | Pass / Fail | ... |

### Notes

- [Dependencies, assumptions, or open questions]
```

## Examples

### Example 1 — Filter a product list

**Input:** "Write a story for filtering search results by price range."

**Expected output:**

```markdown
## User Story: Filter search results by price range

**As a** shopper,  
**I want to** filter product search results by a minimum and maximum price,  
**so that** I only see products I can afford and avoid scrolling through irrelevant results.

### Acceptance Criteria

- [ ] Given I am on a search results page, when I set a minimum price of $10 and a maximum of $50 and apply the filter, then only products priced between $10 and $50 are shown.
- [ ] Given I apply a price filter, when no products match, then a "No results found" message is shown and the filter values are preserved.
- [ ] Given I apply a price filter, when I clear it, then all results are restored.
```

### Example 2 — Vague input requiring a split

**Input:** "User can manage their account."

**Expected output:** Story flagged as failing **Small** (too broad) and **Estimable** (too vague). Skill proposes a split into: change email, change password, delete account — each as a separate story.

## Notes

- A story card should fit on an index card. If the "want" clause needs multiple sentences, the story is likely too large — split it.
- Do not write stories in the passive voice ("It should be possible to…") — keep the persona as the subject.
- Acceptance criteria are not a full test plan; they define the boundaries of done, not every test case.
- If the user does not provide a persona, ask for one before writing — guessing the wrong role produces the wrong story.
