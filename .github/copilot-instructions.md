# Copilot Instructions

<!--
  This file applies to every Copilot Chat session in this repo.
  Keep instructions concise — Copilot appends this to every request.
  Specific context is better than generic rules.
-->

## Project

This is a documentation-first lab for GitHub Copilot resources: verified templates, prompt files, skills, agents, workflows, and guides. Treat every asset as vendor-agnostic and copyable on its own.

## Working Mode

- Prefer updating existing markdown and JSON content over creating new structures.
- Do not invent product capabilities or undocumented behavior.
- Use `[TODO]` rather than filling gaps with speculation.
- There is no build or test pipeline; validate changes by checking Markdown links, JSON syntax, YAML frontmatter, and nearby consistency.
- Use British spelling in prose for customisation-related terms; preserve existing file and folder names even when they use US spelling.

## Standards

- All content must reflect documented Copilot behavior.
- Every skill, workflow, instruction, prompt, and agent must stand alone without runtime links to other repo paths.
- When an asset depends on other material, vendor the needed files into the asset folder instead of linking outward.
- The `_blank` suffix on template files is a lab-only convention. Remove it when deploying to real projects.

## Repository Map

- [README.md](../README.md): top-level source of truth for the repo layout and philosophy.
- [skills/README.md](../skills/README.md): skill library conventions and deployment locations.
- [instructions/README.md](../instructions/README.md): instruction-file organization and indexing.
- [workflows/README.md](../workflows/README.md): workflow packaging rules and vendored asset expectations.
- [guides/how-to/workflow-integration.md](../guides/how-to/workflow-integration.md): workflow expectations and limits.
- [guides/practices/prompt-engineering.md](../guides/practices/prompt-engineering.md): prompt-writing patterns.

## Conventions

- Prompt files use the `.prompt.md` extension and live in `.github/prompts/`.
- Repo-level instructions live in `.github/copilot-instructions.md` or `AGENTS.md`.
- VS Code settings for Copilot go in `.vscode/settings.json`.
- Skills are folder-based assets intended to be copied into `.github/skills/` in target projects.
- Workflows are self-contained folders; keep their runtime dependencies under `assets/`.
- Workflow and skill entry files (`SKILL.md`, `WORKFLOW.md`, `*.agent.md`) must include YAML frontmatter with `name`, `description`, and `metadata` — in that order:

  ```yaml
  ---
  name: (name)
  description: (description)
  metadata:
     skill-author: (author name)
  ---
  ```

## Agent Guardrails

- Keep edits minimal and localized; preserve existing structure and naming.
- When adding, removing, or renaming files or folders, update affected relative markdown links in the same change.
- Validate changes by consistency, link correctness, and frontmatter shape.
- Prefer packaging over linking: duplicate required local assets so the target folder remains fully standalone.
