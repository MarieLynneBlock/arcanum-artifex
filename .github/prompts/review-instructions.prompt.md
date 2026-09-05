---
agent: Plan
description: Review one instruction file for applyTo glob accuracy, frontmatter conventions, overlap or conflict with sibling instructions and copilot-instructions.md, and current best practices.
argument-hint: "Instruction file or folder path, for example: instructions/development/python.instructions.md"
tools: [read, search, execute, web]
---

# Review Instructions

Review exactly one `*.instructions.md` file. The user will provide a file name, folder, or path, such as `python.instructions.md`, `instructions/development/python.instructions.md`, or `development`.

If the user does not provide an instructions target, ask for the file name or path before starting. Do not review every instruction file unless explicitly asked.

## Review Scope

Review the selected instruction file as a complete, copyable unit, including:

- the selected `*.instructions.md` file
- its `applyTo` glob and whether it matches real files in this repo
- sibling instruction files in the same domain folder (for overlap and conflict, not for a separate review)
- `.github/copilot-instructions.md` and any `AGENTS.md` at the repo root (for overlap and conflict with repo-wide guidance)
- relative links and file references used by the instructions

If the user points directly to a domain folder rather than a single file, ask which file inside it to review unless exactly one `*.instructions.md` file exists there.

## Standards

Treat the selected instruction file as a standalone asset that should continue to work after being copied into another repository's `.github/instructions/` (or equivalent) location.

Check that:

- YAML frontmatter is valid and includes `description`, `applyTo`, and `metadata` in that order, with `metadata.instruction-author` as the last field when metadata is present.
- The `description` states both what the instructions cover and when they apply.
- `applyTo` is a valid glob and actually matches files that exist in this repository; flag globs that are too broad (matching unrelated files), too narrow (missing files the instructions clearly intend to cover), or stale (referencing renamed or removed paths).
- The file does not duplicate guidance already stated in `.github/copilot-instructions.md` or a repo-root `AGENTS.md` unless the duplication is intentional and adds file-specific precision.
- The file does not contradict `.github/copilot-instructions.md`, a repo-root `AGENTS.md`, or sibling instruction files in the same domain folder — for example conflicting tool choices, naming conventions, spelling conventions, or process steps.
- Overlapping `applyTo` globs between sibling instruction files are flagged, especially when their guidance could conflict for the same file.
- Instructions are internally consistent and do not contain contradictory languages, tool names, file names, process steps, or behavioural requirements.
- All required extra resources are bundled or referenced correctly; relative markdown links and file references resolve.
- No absolute local paths, user-specific home folders, hidden repo dependencies, or machine-specific assumptions are required.
- Guidance is concise and scoped to files matched by `applyTo`; avoid restating general project philosophy that belongs in `copilot-instructions.md`.
- The instructions avoid speculative product behaviour. Use `[TODO]` in suggested replacement text where behaviour cannot be verified.
- The instructions follow current Copilot instruction-file best practices where applicable.

Use web search only when current best practice, product behaviour, or public documentation needs verification and local files are not enough. Prefer official documentation and clearly distinguish verified facts from recommendations.

## Process

1. Normalise the provided target to one `*.instructions.md` file and confirm it exists.
2. Read the selected file first, then read `.github/copilot-instructions.md`, any repo-root `AGENTS.md`, and sibling instruction files in the same domain folder.
3. Test the `applyTo` glob against the repository's actual file layout, mentally or with a search, to confirm it matches the intended files and nothing unintended.
4. Search the selected file for consistency risks, including:
   - Markdown links
   - `#file:` and `#folder:` references
   - relative paths using `../`
   - absolute paths beginning with `/`, `~`, drive letters, or user-specific home folders
   - language names, framework names, package managers, tool names, and file extensions that may contradict sibling files
   - promises such as "always", "guaranteed", "fully automated", "compliant", or "production-ready"
5. Compare the file's guidance against `.github/copilot-instructions.md`, any repo-root `AGENTS.md`, and sibling instruction files to identify duplication, gaps, and direct conflicts.
6. Validate local links, referenced files, and YAML frontmatter where practical. Prefer safe read-only commands.
7. Review the file against current best practices:
   - focused, file-scoped guidance rather than repo-wide philosophy
   - accurate and appropriately scoped `applyTo`
   - correct frontmatter field order
   - no unnecessary runtime dependency on other repo paths
   - concise, high-signal wording that keeps token usage low for the matched files
8. Identify optimisations separately from correctness issues so cosmetic improvements do not obscure real blockers.
9. Do not edit files unless the user explicitly asks for fixes. This prompt is review-first.

## Output Format

Return a review report with these sections:

**Findings**

List issues first, ordered by severity. For each finding include:

- Severity: `Critical`, `High`, `Medium`, or `Low`
- File path and line when practical
- What is wrong
- Why it matters for `applyTo` accuracy, frontmatter correctness, or repo-wide consistency
- Suggested fix

If no issues are found, say so clearly.

**Contradictions And Ambiguities**

List conflicting guidance, globs, paths, tools, or assumptions found against `.github/copilot-instructions.md`, any repo-root `AGENTS.md`, or sibling instruction files. If none are found, write `None`.

**Optimisations**

List optional improvements that would make the instructions clearer, more accurately scoped, or closer to current best practice. Keep these separate from defects.

**Resource And Packaging Checks**

Summarise what frontmatter fields, `applyTo` matches, links, and sibling files were checked.

**Validation Performed**

List searches, glob checks, syntax checks, documentation checks, web searches, or other commands run. If validation was skipped, explain why.

**Open Questions**

List only questions that block a confident recommendation. If there are none, write `None`.

**Summary**

Give a concise overall readiness assessment: `Ready`, `Ready with minor fixes`, `Needs fixes before reuse`, or `Not self-contained`.
