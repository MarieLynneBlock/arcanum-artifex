---
agent: Plan
description: Review one skill for standalone packaging, instruction quality, contradictory guidance, resource correctness, and current best practices.
argument-hint: "Skill folder or SKILL.md path, for example: skills/agentic/agent-supply-chain"
tools: [read, search, execute, web]
---

# Review Skill

Review exactly one skill folder or one `SKILL.md` file. The user will provide a skill name, folder, or path, such as `agent-supply-chain`, `skills/agentic/agent-supply-chain`, or `skills/agentic/agent-supply-chain/SKILL.md`.

If the user does not provide a skill target, ask for the skill name or path before starting. Do not review every skill unless explicitly asked.

## Review Scope

Review the selected skill as a complete, copyable unit, including:

- `SKILL.md`
- bundled references, templates, examples, scripts, manifests, schemas, prompts, instructions, agents, or other resources in the skill folder
- generated sample assets, when present
- relative links and file references used by the skill
- dependency declarations or setup instructions used by bundled scripts or examples

If the user points directly to a `SKILL.md`, review the parent folder as the skill package unless they explicitly ask for file-only feedback.

## Standards

Treat the selected skill folder as a standalone asset that should continue to work after being copied into another repository or supported agent-skills location.

Check that:

- The skill has a focused purpose and a clear trigger surface.
- YAML frontmatter is valid and includes `name`, `description`, and `metadata` in that order when repository conventions require it.
- The `description` is discovery-friendly, specific, and free of unsupported capability claims.
- Instructions are internally consistent and do not contain contradictory languages, tool names, file names, process steps, or behavioural requirements.
- The skill does not mix incompatible vendor assumptions unless clearly labelled as alternatives.
- All required extra resources are bundled inside the skill folder or explicitly identified as external prerequisites.
- Relative markdown links and file references resolve inside the skill folder unless an external reference is intentional and documented.
- No absolute local paths, user-specific home folders, hidden repo dependencies, or machine-specific assumptions are required.
- Procedures are practical, ordered, and scoped to the skill's stated purpose.
- Examples, templates, scripts, commands, and output formats match the instructions that reference them.
- Code snippets are syntactically plausible for their declared language and do not contain obvious indentation, truncation, or copy-paste corruption.
- Security, privacy, compliance, and operational warnings are proportionate to the skill's domain.
- The skill avoids speculative product behaviour. Use `[TODO]` in suggested replacement text where behaviour cannot be verified.
- The skill follows current agent-skill and Copilot customisation best practices where applicable.

Use web search only when current best practice, product behaviour, or public documentation needs verification and local files are not enough. Prefer official documentation and clearly distinguish verified facts from recommendations.

## Process

1. Normalise the provided target to a skill folder and confirm it exists.
2. Inventory the skill folder recursively before judging it.
3. Read `SKILL.md` first, then inspect all linked or bundled resources.
4. Search the selected folder for consistency risks, including:
   - Markdown links
   - `#file:` and `#folder:` references
   - relative paths using `../`
   - absolute paths beginning with `/`, `~`, drive letters, or user-specific home folders
   - language names, framework names, package managers, tool names, and file extensions that may contradict each other
   - promises such as "always", "guaranteed", "fully automated", "compliant", or "production-ready"
5. Validate local links, referenced files, JSON, YAML frontmatter, and obvious code-block structure where practical. Prefer safe read-only commands.
6. Review the skill against current best practices:
   - focused task boundary
   - high-signal discovery description
   - progressive loading of optional detail
   - standalone packaging
   - clear inputs and outputs
   - concrete validation steps
   - no unnecessary runtime dependency on other repo paths
7. Identify optimisations separately from correctness issues so cosmetic improvements do not obscure real blockers.
8. Do not edit files unless the user explicitly asks for fixes. This prompt is review-first.

## Output Format

Return a review report with these sections:

**Findings**

List issues first, ordered by severity. For each finding include:

- Severity: `Critical`, `High`, `Medium`, or `Low`
- File path and line when practical
- What is wrong
- Why it matters for standalone skill packaging, instruction quality, or current best practice
- Suggested fix

If no issues are found, say so clearly.

**Contradictions And Ambiguities**

List conflicting languages, tools, paths, instructions, assumptions, or output formats. If none are found, write `None`.

**Optimisations**

List optional improvements that would make the skill clearer, more reusable, more discoverable, or closer to current best practice. Keep these separate from defects.

**Resource And Packaging Checks**

Summarise what bundled resources, links, paths, scripts, schemas, examples, and external prerequisites were checked.

**Validation Performed**

List searches, path checks, syntax checks, documentation checks, web searches, or other commands run. If validation was skipped, explain why.

**Open Questions**

List only questions that block a confident recommendation. If there are none, write `None`.

**Summary**

Give a concise overall readiness assessment: `Ready`, `Ready with minor fixes`, `Needs fixes before reuse`, or `Not self-contained`.