# GitHub Copilot — Getting Started for Architects

You have been granted access to GitHub Copilot. This guide is for software architects, solution architects, and technical leads whose work involves documentation, review, and design as much as code.

---

## Step 1 — Install the extension

- [VS Code](../setup/vscode.md) — recommended for documentation and multi-language work
- [IntelliJ IDEA](../setup/intellij.md) — if you review JVM-based codebases

**Done when:** you see the Copilot icon in the status bar without a strikethrough.

---

## Step 2 — What Copilot can do for you

| Task | How |
| --- | --- |
| Writing ADRs | Describe the decision context, Copilot drafts the record |
| Reviewing existing code | Select code → ask for a structural or pattern review |
| Explaining unfamiliar codebases | `@workspace` questions about structure and patterns |
| Writing technical documentation | Describe the system, Copilot drafts prose |
| Identifying anti-patterns | Ask Copilot to review for SOLID violations, coupling, etc. |
| Generating interface / contract stubs | Describe the contract, Copilot generates the skeleton |
| Writing RFC or design doc sections | Give the context, ask Copilot to draft a section |
| Reviewing a PR for architectural concerns | Paste the diff, ask for a structural review |

---

## Step 3 — Explore an unfamiliar codebase

Open the codebase in VS Code. Use `@workspace` in chat:

```
@workspace what are the main architectural layers of this project?
@workspace how does data flow from the API to the database?
@workspace are there any obvious violations of separation of concerns?
@workspace what patterns are used for error handling across the codebase?
```

`@workspace` indexes the full project — no need to open individual files first.

---

## Step 4 — Write an ADR

In chat:

```
Write an Architecture Decision Record for the following decision:

Context: [describe the problem and forces at play]
Decision: [what was decided]
Alternatives considered: [what else was evaluated]
Consequences: [trade-offs and implications]

Use the MADR format.
```

Copilot will draft the full document. Review and adjust — it won't know your specific constraints.

---

## Step 5 — Review code for architectural concerns

Select a module or paste a diff into chat:

```
Review this code for:
1. Violations of single responsibility principle
2. Tight coupling between layers
3. Missing abstractions that would aid testability
4. Patterns that will not scale beyond current load

For each finding: state the concern, the location, and a suggested improvement.
```

---

## Step 6 — Read the privacy quick card

[privacy-quick-card.md](../resources/privacy-quick-card.md) — what not to paste into Copilot Chat.

---

## Week 1 goals

- [ ] Used `@workspace` to explore a codebase
- [ ] Asked Copilot to review code for architectural concerns
- [ ] Drafted or improved one piece of technical documentation with Copilot
- [ ] Read the [privacy quick card](../resources/privacy-quick-card.md)

---

## Resources

| Resource | Link |
| --- | --- |
| Prompt library | [prompt-library.md](../resources/prompt-library.md) |
| Cheat sheet | [cheat-sheet.md](../resources/cheat-sheet.md) |
| Privacy quick card | [privacy-quick-card.md](../resources/privacy-quick-card.md) |
| FAQ | [faq.md](../resources/faq.md) |
| Feature reference | [copilot-guide.md](../resources/copilot-guide.md) |
