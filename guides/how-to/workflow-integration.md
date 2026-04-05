# GitHub Copilot — Workflow Integration Guide

Where Copilot fits in the software development lifecycle, and where it doesn't.

---

## 1. Where Copilot adds the most value

| Task | Value | Why |
| --- | --- | --- |
| Writing boilerplate | High | Repetitive, pattern-based — Copilot excels |
| Generating unit tests | High | Well-structured, predictable output |
| Writing documentation and docstrings | High | Consistent patterns, low risk |
| Explaining unfamiliar code | High | No output risk — just reading |
| Debugging with error messages | High | Copilot is good at interpreting errors |
| Scaffolding new files/classes | Medium | Good starting point, needs review |
| Writing complex business logic | Low | High risk — Copilot doesn't know your domain |
| Security-sensitive code | Low | Always review manually; use SAST tools |
| Architecture decisions | None | Not a design tool |

---

## 2. TDD with Copilot

Copilot integrates well with test-driven development:

**Write the test first (as usual), then use Copilot for the implementation:**
1. Write the failing test yourself — this defines the contract.
2. Open the implementation file alongside the test.
3. Write the function signature.
4. Let Copilot suggest the body.
5. Run the test. Iterate if it fails.

**Alternatively, use `/tests` to generate tests for existing code:**
- Select a function.
- Run `/tests` with constraints: framework, coverage targets, edge cases.
- Review and adjust — Copilot's tests often miss domain-specific edge cases.

**Copilot cannot:**
- Know your domain invariants.
- Write tests for untestable code (tight coupling, hidden state).
- Replace a thoughtful test strategy.

---

## 3. Pull request workflow

**Before opening a PR:**
```
Review my changes for:
- Missing error handling
- Hardcoded values that should be config
- Tests I might have missed
```
Paste the diff or attach changed files with `#file:`.

**PR descriptions (VS Code / GitHub.com):**
- GitHub Copilot can generate a PR summary — click the Copilot icon in the PR description field on github.com.
- Or use a prompt file: create `.github/prompts/pr-description.prompt.md` with your team's standard format.

**Code review:**
- Use `/explain` on unfamiliar sections before reviewing.
- Ask Copilot to identify potential issues in a diff — but make your own judgement call.
- Copilot Enterprise: automated code review adds inline suggestions directly to PRs.

---

## 4. Documentation workflow

| Task | How |
| --- | --- |
| Docstrings / Javadoc | Select function → `/doc` |
| README sections | Chat: "write a README section for this module" + `#file:` |
| API documentation | Chat: "document these endpoints in OpenAPI format" |
| Architecture decision records | Chat: describe the decision, ask Copilot to draft the ADR |
| Inline comments | Accept completions for comment lines, or ask "add a comment explaining why" |

**Tip:** run documentation tasks at end of sprint, not mid-feature. Copilot's output is better when the code is already stable.

---

## 5. Onboarding new developers

Copilot accelerates onboarding significantly when used deliberately:

- **Codebase exploration:** `@workspace explain the folder structure and main entry points`
- **Understanding existing code:** Select unfamiliar classes → `/explain`
- **Finding patterns:** `@workspace show me an example of how we handle errors in this codebase`
- **Writing first tickets:** Copilot can suggest implementations consistent with existing patterns

**Caution:** new developers who rely heavily on Copilot without reading the code it generates risk understanding the codebase less deeply. Pair Copilot use with code walkthroughs from senior developers.

---

## 6. What Copilot is NOT for

- **Architecture design.** Copilot has no knowledge of your system's constraints, team size, or operational requirements.
- **Security auditing.** It helps spot common patterns but is not a substitute for SAST tools or a security review.
- **Business logic decisions.** It doesn't know your domain rules, regulatory constraints, or product requirements.
- **Replacing code review.** Every suggestion needs a human decision. Code review is not optional because Copilot was used.
- **On-call diagnosis.** Copilot doesn't have access to your runtime, logs, or metrics. Use it to understand code, not to diagnose live systems.

---

## 7. Team conventions to establish early

Before rolling out widely, agree on:

1. **Does AI-generated code need to be labelled in commits?** (Many teams say no, but decide explicitly.)
2. **What goes in `.github/copilot-instructions.md`?** Who owns it, how is it updated?
3. **Is Copilot Chat allowed for discussing production incidents?** (Consider what context gets pasted.)
4. **What's the code review standard for AI-generated code?** (Same as all code, or higher scrutiny?)
5. **Are there files or directories that should be in `.copilotignore`?**
