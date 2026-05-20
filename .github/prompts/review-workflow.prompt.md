---
agent: Plan
description: Review one workflow folder for standalone packaging, Copilot customization quality, local link correctness, and current best practices.
argument-hint: "Workflow folder name or path, for example: workflows/4plus1-diagrams"
tools: [read, search, execute]
---

# Review Workflow Folder

Review exactly one workflow folder from `workflows/`. The user will provide a workflow folder name or path, such as `4plus1-diagrams` or `workflows/4plus1-diagrams`.

If the user does not provide a workflow folder, ask for the folder name before starting. Do not review every workflow unless explicitly asked.

## Review Scope

Review the entire selected workflow folder recursively, including:

- `README.md`
- `WORKFLOW.md`
- `skills/**/SKILL.md`
- `instructions/**/*.instructions.md`
- `prompts/**/*.prompt.md`
- `agents/**/*.agent.md`
- `templates/**`
- `references/**`
- `scripts/**`
- examples or generated sample assets, when present

## Standards

Treat the selected workflow folder as a fully contained, copyable unit. It must work after being copied into another repository without relying on any file outside its own folder.

Check that:

- All runtime dependencies are bundled inside the workflow folder.
- Relative markdown links resolve to files inside the selected workflow folder.
- No instructions, prompts, agents, skills, scripts, templates, or examples require repo-level assets outside the selected workflow folder.
- No absolute local paths, machine-specific paths, or hidden cross-repo assumptions are required.
- References to agents, prompts, instructions, skills, templates, scripts, and examples point to files that exist.
- Markdown files expected by the workflow are present and named consistently.
- `WORKFLOW.md` identifies purpose, linked assets, preconditions, steps, outputs, and validation.
- `README.md` explains when to use the workflow and how to invoke it without needing outside context.
- Skills are build tool-agnostic unless the workflow explicitly requires a documented tool.
- Instructions, prompts, agents, and skills are vendor-agnostic where possible and avoid undocumented product behavior.
- Customization frontmatter follows current Copilot conventions and has useful discovery descriptions.
- Skill entry files include YAML frontmatter with `name`, `description`, and `metadata` in that order when this repository's workflow packaging convention requires it.
- Prompt files use `.prompt.md`; instruction files use `.instructions.md`; agent files use `.agent.md`; skill entry files are named `SKILL.md`.
- Scripts are optional, local, documented, and invoked with paths inside the workflow folder.
- Validation steps are realistic for the assets in the folder and do not assume unavailable services.

Use `[TODO]` for gaps only when proposing replacement text. Do not invent undocumented capabilities or claim a tool can do something unless the workflow assets document that behavior.

## Process

1. Normalize the provided folder name to a path under `workflows/` and confirm the folder exists.
2. Inventory the folder recursively before judging it.
3. Read the top-level `README.md` and `WORKFLOW.md` first, then inspect linked assets and nested markdown files.
4. Search all files in the selected folder for links and references that might leave the folder, including:
   - Markdown links
   - `#file:` and `#folder:` references
   - Relative paths using `../`
   - Absolute paths beginning with `/`, `~`, drive letters, or user-specific home folders
   - References to repo-level folders such as `.github/`, `skills/`, `instructions/`, `agents/`, `prompts/`, or `templates/` that are not inside the selected workflow folder
5. Check local markdown links and referenced files. Prefer `rg` and simple path checks. Run local validation scripts only when they are documented, safe, and do not modify files.
6. Review customization files against current Copilot best practices:
   - Skills: focused purpose, strong discovery description, self-contained procedure, local references, progressive loading.
   - Prompts: single focused task, clear argument expectations, output format, no unnecessary tool requirements.
   - Instructions: concise task or file guidance, useful discovery description, no overly broad `applyTo` unless justified.
   - Agents: clear role, minimal tools, boundaries, keyword-rich description, no circular or missing handoffs.
7. Do not edit files unless the user explicitly asks for fixes. This prompt is review-first.

## Output Format

Return a review report with these sections:

**Findings**

List issues first, ordered by severity. For each finding include:

- Severity: `Critical`, `High`, `Medium`, or `Low`
- File path and line when practical
- What is wrong
- Why it matters for standalone workflow packaging or Copilot customization quality
- Suggested fix

If no issues are found, say so clearly.

**Link And Packaging Checks**

Summarize what was checked and whether all links/references stayed inside the selected workflow folder.

**Customization Checks**

Summarize the state of skills, instructions, prompts, and agents.

**Validation Performed**

List searches, path checks, scripts, or other commands run. If validation was skipped, explain why.

**Open Questions**

List only questions that block a confident recommendation. If there are none, write `None`.

**Summary**

Give a concise overall readiness assessment: `Ready`, `Ready with minor fixes`, `Needs fixes before reuse`, or `Not self-contained`.