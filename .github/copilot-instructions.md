# Copilot Instructions

<!-- 
  This file applies to every Copilot Chat session in this repo.
  Keep instructions concise — Copilot appends this to every request.
  Specific context is better than generic rules.
-->

## Project

This is a personal lab for GitHub Copilot resources: verified templates, prompt files, and guides.

## Working Mode

- Prefer updating existing markdown and JSON content; this repository is documentation-first.
- Do not invent product capabilities or undocumented behavior.
- Use links to canonical docs instead of duplicating long guidance.

## Standards

- All content must reflect documented Copilot behaviour — no hallucinated features.
- Use `[TODO]` as a placeholder rather than inventing content.
- The `_blank` suffix on template files is a lab-only convention. Remove it when deploying to real projects.

## Repository Map

- [README.md](../README.md): source of truth for top-level structure.
- [skills/README.md](../skills/README.md): skill library conventions and deployment locations.
- [guides/how-to/workflow-integration.md](../guides/how-to/workflow-integration.md): workflow expectations and limits.
- [guides/practices/prompt-engineering.md](../guides/practices/prompt-engineering.md): prompt writing patterns.

## Conventions

- Prompt files use the `.prompt.md` extension and live in `.github/prompts/`.
- Repo-level instructions live in `.github/copilot-instructions.md` (this file).
- VS Code settings for Copilot go in `.vscode/settings.json`.
- Skills are folder-based assets intended to be copied into `.github/skills/` in target projects.

## Agent Guardrails

- Keep edits minimal and localized; preserve existing structure and naming.
- There is no build/test pipeline in this repo; validate changes by consistency and link correctness.
- When adding, removing, or renaming files/folders, update affected relative markdown links in the same change.
