---
description: >
name: git-workflow
version: 1.0.0
tags:
  - git
  - version-control
  - conventional-commits
  - branching
  - pull-request
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Covers the full git workflow for a software project: branch naming conventions, commit message authoring (Conventional Commits standard), PR description templates, and merge strategy advice. It produces ready-to-use git artefacts, not generic advice.

## When to use it

- User wants to write a commit message for a set of changes.
- User asks about branch naming, PR conventions, or merge strategy.
- User wants to set up or document a git workflow for a project.
- User wants a PR description written from a diff or change summary.

## Key concepts

### Conventional Commits

Format: `<type>(<scope>): <description>`

| Type | When to use |
| --- | --- |
| `feat` | A new feature visible to users or consumers |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Code restructure with no behaviour change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build, tooling, dependency updates |
| `ci` | CI/CD pipeline changes |
| `revert` | Reverts a previous commit |

Rules:
- Description is lowercase, imperative mood, no trailing period: `fix: handle null session token` not `Fixed the null session token issue.`
- Scope is optional but recommended for multi-module repos: `feat(auth): add OAuth2 login`
- Breaking changes: append `!` after type/scope and add `BREAKING CHANGE:` footer: `feat(api)!: remove v1 endpoint`
- Body and footer are separated from subject by a blank line.

### Branch naming

Pattern: `<type>/<short-description>` using the same type vocabulary as Conventional Commits.

Examples: `feat/guest-checkout`, `fix/null-session-token`, `chore/upgrade-dependencies`, `docs/api-reference`

Rules:
- Use hyphens, not underscores or slashes within the description.
- Keep it short enough to read in a terminal (under 50 characters total).
- Include a ticket reference if the team uses one: `feat/PROJ-123-guest-checkout`.

### Merge strategies

| Strategy | When to use |
| --- | --- |
| **Merge commit** | Preserves full branch history; good for long-lived feature branches |
| **Squash and merge** | Clean linear history; good for small features or fix PRs |
| **Rebase and merge** | Linear history without squashing; good when individual commits are meaningful |

## Instructions

### Writing a commit message

1. Identify the type from the change description.
2. Identify the scope if the repo has modules or packages.
3. Write the subject line: `<type>(<scope>): <imperative description>`.
4. If the change needs explanation (why, not what), add a body paragraph.
5. Add a footer for breaking changes, issue references (`Closes #123`), or co-authors.

### Writing a PR description

1. State what the PR does in one sentence (mirrors the commit subject if squashing).
2. Add a "Why" section if the motivation is not obvious from the title.
3. List the key changes as bullet points.
4. Add a test plan: what was tested and how.
5. Note any follow-up work or known limitations.

### Advising on workflow setup

1. Recommend a branching model based on team size and release cadence:
   - Small team / continuous deployment → trunk-based development with short-lived feature branches.
   - Larger team / scheduled releases → Gitflow or a simplified variant.
2. Recommend a merge strategy consistent with the model.
3. Suggest protected branch rules (require PR, require review, require CI pass).

## Output format

### Commit message

```
<type>(<scope>): <description>

[optional body — explain why, not what]

[optional footer — BREAKING CHANGE, Closes #NNN, Co-authored-by]
```

### PR description

```markdown
## What

[One sentence: what this PR does.]

## Why

[Why this change is needed — link to issue or ticket if applicable.]

## Changes

- [Key change 1]
- [Key change 2]

## Test plan

- [ ] [What was tested and how]
- [ ] [Edge case verified]

## Notes

- [Follow-up work, known limitations, or deployment considerations]
```

### Branch name

```
<type>/<short-description>
```

## Examples

### Example 1 — Commit message from a change description

**Input:** "I added a price filter to the search results page. It filters by min and max price and preserves the filter when navigating back."

**Expected output:**
```
feat(search): add price range filter to results page

Preserves min/max values on browser back navigation so users
do not lose their filter context between page visits.
```

### Example 2 — PR description from a diff summary

**Input:** "Fixed a bug where the session token was not cleared on logout, leaving users authenticated after clicking sign out."

**Expected output:**
```markdown
## What
Fix session token not cleared on logout.

## Why
Users remained authenticated after signing out because the token cookie
was not explicitly expired. Closes #412.

## Changes
- Expire session cookie with `Max-Age=0` on logout handler
- Add integration test for post-logout authenticated request

## Test plan
- [ ] Log in, click sign out, attempt to access protected route — expect 401
- [ ] Verify cookie is absent in browser DevTools after logout
```

## Notes

- Commit messages are read by humans in `git log` and by tools (changelogs, release notes, semantic versioning). Write for both audiences.
- Never include "WIP" or "temp" in a commit that will land on the main branch.
- If the user's repo has an existing commit style, match it — do not impose Conventional Commits without noting the deviation.
- For monorepos, the scope is the package or service name, not a file path.
