---
name: code-review
description: >
  Perform a structured code review covering correctness, security, maintainability,
  performance, and test coverage — producing prioritised findings with inline
  suggestions. Use when asked to review a diff, PR, or code snippet regardless
  of language.
version: 1.0.0
authors:
  - Marie-Lynne Block
tags:
  - code-review
  - quality
  - security
  - pull-request
---

## What this skill does

Applies a consistent, language-agnostic review framework to any code change. It evaluates code across five dimensions, produces prioritised findings with inline suggestions, and distinguishes blockers (must fix before merge) from improvements (worth addressing but not blocking).

## When to use it

- User asks to "review this code", "review this PR", or "give feedback on this diff".
- User pastes a code snippet and wants quality feedback.
- User wants a second opinion before raising a PR.
- User needs a review checklist for a team standard.

## Review dimensions

| Dimension | What to check |
| --- | --- |
| **Correctness** | Logic errors, off-by-one, null/undefined handling, edge cases not covered |
| **Security** | Input validation, injection risks, secrets in code, insecure defaults, least-privilege violations |
| **Maintainability** | Naming clarity, function/class size, duplication, coupling, missing or misleading comments |
| **Performance** | N+1 queries, unnecessary allocations, blocking calls, inefficient algorithms for the scale |
| **Test coverage** | Happy path covered, edge cases tested, negative scenarios present, test quality (not just count) |

## Finding severity

| Severity | Meaning | Merge gate? |
| --- | --- | --- |
| **Blocker** | Must fix — correctness bug, security vulnerability, or missing critical test | Yes |
| **Major** | Should fix this PR — significant maintainability or performance issue | Recommended |
| **Minor** | Fix soon — small improvement, naming, formatting | No |
| **Nit** | Optional — style preference or very low impact | No |

## Instructions

1. **Understand the context.** What does this code do? What is the change trying to achieve? If not clear, state the assumption.

2. **Review each dimension.** Work through correctness → security → maintainability → performance → test coverage. Only flag genuine issues — do not manufacture findings.

3. **Write inline suggestions.** For each finding, reference the specific line or block and provide a concrete fix or alternative, not just a description of the problem.

4. **Classify severity.** Assign Blocker / Major / Minor / Nit to each finding.

5. **Write an overall summary.** Is this ready to merge? What is the dominant concern if any?

6. **Produce the report** using the output format below.

## Output format

```markdown
## Code review: [file name or PR title]

**Overall verdict:** Ready to merge / Merge after addressing blockers / Needs significant rework

**Summary:** [2–3 sentences: what the code does, overall quality impression, dominant concern.]

---

### Findings

#### [BLOCKER/MAJOR/MINOR/NIT] — [Short title]

**Location:** `file.ext:line` or `function name`

**Issue:** [What is wrong and why it matters.]

**Suggestion:**
\```language
// suggested fix or alternative
\```

---

### What works well

- [Specific thing done well — always include at least one]
- [Specific thing done well]

---

### Checklist

| Dimension | Status | Notes |
| --- | --- | --- |
| Correctness | Pass / Fail / Partial | |
| Security | Pass / Fail / Partial | |
| Maintainability | Pass / Fail / Partial | |
| Performance | Pass / Fail / Partial | |
| Test coverage | Pass / Fail / Partial | |
```

## Examples

### Example 1 — Security blocker in a web handler

**Input:** Python Flask route that concatenates user input into a SQL query string.

**Expected output:** Blocker finding for SQL injection with a parameterised query fix. Minor finding for missing input length validation. Checklist: Security Fail, Correctness Partial.

### Example 2 — Clean PR with minor nits

**Input:** Well-structured TypeScript utility function with tests.

**Expected output:** No blockers or majors. Two Nit findings (variable naming, unused import). "What works well" section highlighting test coverage and clear function boundaries. Verdict: Ready to merge.

## Notes

- Lead with blockers — a long list of nits before a blocker buries the most important information.
- Always include at least one "what works well" item. Reviews that only criticise reduce trust and miss knowledge-sharing opportunities.
- Do not flag style or formatting issues that a linter/formatter should enforce — note them once as "configure a linter" if they are pervasive.
- If the diff is too large to review in full, say so and ask the user to scope it (by file, by concern, or by risk area).
