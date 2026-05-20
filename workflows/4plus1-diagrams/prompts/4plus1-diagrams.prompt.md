---
description: Produce a complete Kruchten 4+1 architectural view model with diagram-as-code (Mermaid / PlantUML) and editable visual diagrams in draw.io, Miro, or both. Loads 4plus1-models for core logic and track-specific output skills. No MCP dependency.
name: '4plus1 Diagrams.prompt'
mode: agent
metadata:
  skill-author: 'Marie-Lynne Block'
---

# 4+1 Architecture Diagrams (Miro & draw.io)

Run the `4plus1-diagrams` workflow.

**Workflow source of truth:** `WORKFLOW.md`

All skills and instructions this workflow needs are bundled locally in top-level workflow folders. The workflow folder is self-contained.

**Skill loading (track-aware):**

1. Always load `skills/4plus1-models/SKILL.md` — the 4+1 method (authoritative).
2. Load output skills based on selected tracks:
   - draw.io selected: `skills/draw-io-diagram-generator/SKILL.md`
   - Miro selected: `skills/miro-diagram-generator/SKILL.md`

**Workflow-local assets:**

- draw.io track:
   - Per-view draw.io skeletons: `templates/drawio/`
   - Per-view draw.io conventions: `references/notation-drawio.md`
   - Instruction file: `instructions/draw-io.instructions.md`
- Miro track:
   - Miro prompt template: `templates/miro/miro-prompt-template.md`
   - Optional full-board Miro template: `templates/miro/full-board-prompt-template.md`
   - Per-view Miro conventions: `references/notation-miro.md`
   - Instruction file: `instructions/miro.instructions.md`

## What to do

1. Run `4plus1-models` Steps 1–4 (mode → audience → context → concerns) with a clear intake style:
   - Start with one compact question block (max 5 fields): system, audience, track, domain/regulatory context, constraints.
   - If answers are partial, proceed with explicit assumptions instead of asking many immediate follow-ups.
   - Ask follow-ups only when a missing value blocks the next artifact, one at a time.
2. Confirm visual output selection from intake. If it was not provided, ask once: **"How would you like to deliver editable diagrams? (A) draw.io - edit in VS Code/desktop/web and export PNG/SVG, (B) Miro - collaborate in real time with AI-assisted layout and export PNG/SVG, or (C) both."** Use only each selected track's rules and assets.
3. For each view (logical → process → development → physical → scenarios):
   - **For draw.io**: Generate the primary Mermaid/PlantUML per the skill's Step 5. Pick the matching draw.io skeleton, adapt it with real component names, apply conventions from `notation-drawio.md`. For BPMN process views, enforce the shared semantic palette mapping via `notation-drawio.md`. Defer mxGraph XML rules to `draw-io-diagram-generator`.
   - **For Miro**: Generate the primary Mermaid/PlantUML per the skill's Step 5. Use the Miro prompt template and `notation-miro.md` to generate a board setup prompt with component placement guidance. For BPMN swimlane process views, enforce the same shared semantic palette mapping via `notation-miro.md`.
   - Verify component names match between the primary Mermaid/PlantUML source and each selected track output.
   - For Physical view, treat the `.puml` as canonical and verify exact parity for node/container names, child elements, relationship endpoints, and relationship labels. Keep visual zones only as grouping around those canonical elements; remove skeleton placeholders that are not in the `.puml`.
4. If outputting to disk, run `python skills/4plus1-models/scripts/validate-views.py <output-directory>` (for example `python skills/4plus1-models/scripts/validate-views.py docs/architecture`).
5. **Format validation**:
   - draw.io: run `skills/draw-io-diagram-generator/scripts/validate-drawio.py <file>` or open in `hediet.vscode-drawio`.
   - Miro: confirm prompts are markdown-valid and reference correct view names.

## Guardrails

- **No MCP.** Write `.drawio` files as XML directly.
- **Keep tracks separate.** Do not map styles, structures, or mechanics from one track to the other.
- **Do not duplicate skill content.** Link out, don't restate.
- **One view at a time.** Do not generate all five in one go without showing intermediate output.
- **Clear questions.** Use numbered prompts with plain wording and options; avoid multi-round question dumps.
