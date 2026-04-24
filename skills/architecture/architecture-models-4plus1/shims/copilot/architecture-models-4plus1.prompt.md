---
mode: agent
description: Produce a 4+1 architectural view model (logical, process, development, physical, scenarios) for a software system, with Mermaid diagrams (primary), PlantUML for deployment-heavy physical views, and a Miro RISEN prompt per view.
---

# architecture-models-4plus1 — GitHub Copilot shim

This Copilot prompt is a thin pointer to the canonical skill documentation. The canonical `SKILL.md` is the single source of truth for workflow and output structure. **Do not duplicate logic here.**

## Where to find the canonical skill

The skill is installed alongside this prompt file. Look for:

- `architecture-models-4plus1/SKILL.md` — the entry point
- `architecture-models-4plus1/references/` — per-view detail
- `architecture-models-4plus1/concerns/` — modular concerns (GDPR, security, bias/fairness, regulatory, sustainability, accessibility)
- `architecture-models-4plus1/templates/` — view and Miro prompt templates
- `architecture-models-4plus1/examples/synth-claim/` — worked example

In Copilot, you can inline-reference these files with `#file:` (e.g. `#file:SKILL.md`) if they're in the workspace.

## When to invoke this prompt

Invoke via `/architecture-models-4plus1` (or whatever slash command maps to this file in your setup) when the user asks to:

- Produce Kruchten's 4+1 architectural view model for a system.
- Generate architecture documentation (logical, process, development, physical, scenarios views).
- Create Mermaid, PlantUML, or Miro prompts for architecture diagrams.
- Document a system's architecture for a developer, cross-functional, or executive audience.

## Required behaviour (summary — see canonical SKILL.md for detail)

1. **Determine mode:** zero-input (user gives a paragraph), interview (gather detail first), or partial (specific views only).
2. **Determine audience:** dev-only / cross-functional / executive — **ask explicitly** if the user hasn't said. This drives the notation per view.
3. **Gather system context:** name, stakeholders, stack, scale, quality attributes, constraints, out-of-scope. Flag assumptions inline with `> **Assumption:** …`.
4. **Pull in concerns:** GDPR, security, bias/fairness (if ML), regulatory (if in a regulated sector), sustainability, accessibility (if human-facing). Surface real findings as `> **Concern (X):** …` — do not boilerplate.
5. **Generate views in order:** logical → process → development → physical → scenarios. For each:
   - Read the reference file (`references/<view>-view.md`).
   - Generate diagram + prose using `templates/view-template.md`.
   - Generate the Miro RISEN prompt using `templates/miro-prompt-template.md`.
6. **Cross-view consistency:** component names must match across views. Run `scripts/validate-views.py` if outputting to disk.
7. **Output:** default folder structure in `SKILL.md` Step 8.

## Notation defaults

- **Mermaid** is the primary notation (renders in GitHub, VS Code, Claude, everywhere).
- **PlantUML** is the primary notation for the physical view (cloud-provider stdlibs are much richer).
- **Audience (b) cross-functional:** process view uses Mermaid flowchart with swimlane subgraphs approximating BPMN; elsewhere uses C4-flavoured Mermaid.
- **Audience (c) executive:** C4 Context only for logical; skip or abbreviate development view; Mermaid C4Deployment at zone level for physical.

## Worked example

Read `examples/synth-claim/` end-to-end to calibrate tone, specificity, and assumption-flagging. It's a synthetic hybrid-cloud claims-processing platform with five views, six Miro prompts, concerns flagged, assumptions surfaced.

## Anti-patterns to avoid

- Filling templates with placeholder text. If context is missing, ask or flag as an assumption.
- Dumping all five views into a single response without the context-gathering step.
- Repeating information between views (each view answers a specific question; cross-reference, don't duplicate).
- Boilerplate concern blocks. Only flag real, specific concerns.
- Omitting rationale for architectural decisions.
