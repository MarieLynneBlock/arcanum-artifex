---
description: Workflow playbook for producing Kruchten 4+1 architecture views with canonical diagram-as-code plus editable draw.io or Miro output.
name: 4+1 Architecture Diagrams (Miro & draw.io)
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Workflow: 4+1 Architecture Diagrams (Miro & draw.io)

## 1. Purpose

Produce a complete Kruchten 4+1 view model where **every view is delivered in two formats**:
1. **Canonical diagram-as-code**: Mermaid/PlantUML (per the `4plus1-models` skill).
2. **Editable visual format**: Either **draw.io** (interactive `.drawio` files) or **Miro** (collaboration prompts).

The canonical format and the selected visual track are kept consistent — same component names, same relationships, same scope.

## 2. Linked assets

**This workflow is self-contained.** Everything it needs is vendored in top-level workflow folders. Copy the whole `4plus1-diagrams/` folder into another repo and it works as-is.

The vendored copies are a **frozen snapshot**. This workflow has no sync mechanism and no dependency on any path outside this folder.

| Asset type | Path (inside this workflow) | Role |
|------------|------------------------------|------|
| Skill (primary, vendored) | [skills/4plus1-models/](skills/4plus1-models/) | Owns the 4+1 method, audience routing, per-view references, and Mermaid/PlantUML output. **Source of truth for core architecture logic.** |
| Skill (secondary, vendored) | [skills/draw-io-diagram-generator/](skills/draw-io-diagram-generator/) | Owns the mxGraph XML mechanics, validation script, and shape-library knowledge. Needed only for draw.io path. |
| Skill (secondary, vendored) | [skills/miro-diagram-generator/](skills/miro-diagram-generator/) | Owns Miro prompt mechanics, RISEN formatting, and track-specific validation. Needed only for Miro path. |
| Instructions (vendored) | [instructions/](instructions/) | Auto-applies to `.drawio` files (draw.io path) or Miro prompts (Miro path). |
| Agent (discoverable entrypoint) | [architecture-documentation.agent.md](architecture-documentation.agent.md) | Drop-in entrypoint for placement under `.github/agents/` or `~/.agents/` with no install step. |
| Agent | [agents/architecture-documentation.agent.md](agents/architecture-documentation.agent.md) | Thin orchestrator. Loads the two skills and runs the steps below. **No `mcp-servers` block.** |
| Prompt | [prompts/4plus1-diagrams.prompt.md](prompts/4plus1-diagrams.prompt.md) | Single-shot prompt that triggers the workflow. |
| Templates | [templates/drawio/](templates/drawio/) | Eight per-view `.drawio` skeletons. |
| Templates | [templates/miro/](templates/miro/) | Miro prompt templates for per-view and full-board setup prompts. |
| Reference | [references/notation-drawio.md](references/notation-drawio.md) | Per-view draw.io conventions: shape library per view, palette, layout, edge style. |
| Reference | [references/notation-miro.md](references/notation-miro.md) | Per-view Miro conventions: frame naming, shape semantics, colour palette, layout discipline. |
| External tool | VS Code extension `hediet.vscode-drawio` | Renders the produced `.drawio` files inside VS Code. |

## 3. Preconditions

- The vendored skills and instruction are present in top-level workflow folders (they ship with the workflow).
- For the user: VS Code with `hediet.vscode-drawio` installed (or draw.io desktop / app.diagrams.net) to view/edit the output.
- The agent / user has confirmed the **audience** before starting (dev-only / cross-functional / executive — the `4plus1-models` skill, Step 2, asks this).

## 4. Steps

The workflow extends — does **not** replace — the `4plus1-models` skill workflow. Run that skill end-to-end, then choose your visual format.

1. **Run skill steps 1–4** (mode → audience → context → concerns) from `skills/4plus1-models/SKILL.md`. No changes.
2. **Confirm visual format.** Take the visual track from intake. If it was not provided, ask once: *"How would you like to deliver the diagrams? (A) draw.io or (B) Miro?"* Treat the selected path as an independent track; do not import style/mechanics from the other track.
3. **For each view (logical → process → development → physical → scenarios)**:
   1. Generate the Mermaid (or PlantUML for physical) diagram per the skill's Step 5. Write to `diagrams/mermaid/<view>.mmd` (or `.puml`).
      - For Physical view, treat the generated `.puml` as canonical. Extract its node/container names, child elements, relationship endpoints, and relationship labels before creating draw.io or Miro output.
   2. **If draw.io**:
      - Pick the matching `.drawio` skeleton from `templates/drawio/` (routing table in §4a).
      - Adapt the skeleton — replace placeholders with real component names, apply semantic palette and conventions from `references/notation-drawio.md`.
      - Add hidden source provenance to the XML: canonical source path, source format, and enough inline Mermaid/PlantUML source content or extracted facts for the `.drawio` file to remain understandable when copied outside the repository.
      - For Physical view, keep useful visual zones only when they group canonical `.puml` elements. Do not keep placeholder infrastructure from the skeleton if it is absent from the `.puml`.
      - For BPMN process views, apply the shared semantic palette mapping from `references/notation-drawio.md`.
      - For mxGraph XML mechanics, defer to `skills/draw-io-diagram-generator/SKILL.md` and `instructions/draw-io.instructions.md`.
      - Write to `diagrams/drawio/<view>.drawio`.
   3. **If Miro**:
      - Use Miro rules from `skills/miro-diagram-generator/SKILL.md`, workflow templates from `templates/miro/`, and per-view conventions from `references/notation-miro.md`.
      - Add a `Canonical source reference` section with the source path and the canonical Mermaid/PlantUML content, so the prompt remains usable when copied outside the repository.
      - For Physical view, keep the `.puml` as source of truth, then expand its exact elements and relationships into a Sidekick-optimized object manifest before layout instructions. Do not ask Miro to parse raw PlantUML. Zones are allowed as visual grouping only; they must not introduce new infrastructure.
      - For BPMN swimlane process views, enforce the same shared semantic palette mapping via `references/notation-miro.md`.
      - Generate a Miro board setup prompt.
      - Write to `diagrams/miro/<view>-miro-prompt.md`.
   4. Verify component names are consistent across Mermaid/PlantUML and the chosen visual format. For Physical view, also verify every relationship endpoint and label from the `.puml` is represented in the draw.io file or Miro prompt.
4. **Cross-view consistency check.** If outputting to disk, run `python skills/4plus1-models/scripts/validate-views.py <output-directory>` (for example `python skills/4plus1-models/scripts/validate-views.py docs/architecture`).
5. **Format-specific validation**:
   - **draw.io**: Run `python skills/draw-io-diagram-generator/scripts/validate-drawio.py <file>` or open in VS Code with `hediet.vscode-drawio`.
   - **Miro**: Confirm prompts are markdown-valid and reference the correct view names.

### 4a. draw.io per-view skeleton routing

(Only used if draw.io format is chosen.)

| View | Audience | Skeleton |
|------|----------|----------|
| Logical | any | `logical-view.drawio` |
| Process | dev-only | `process-view-sequence.drawio` |
| Process | cross-functional / executive | `process-view-bpmn.drawio` |
| Development | any | `development-view.drawio` |
| Physical | AWS-heavy | `physical-view-aws.drawio` |
| Physical | Azure-heavy | `physical-view-azure.drawio` |
| Physical | cloud-agnostic / multi-cloud | `physical-view-generic.drawio` |
| Scenarios | any | `scenarios-view.drawio` |

### 4b. Miro board structure (reference)

(Only used if Miro format is chosen.) The generated prompt should describe:
- One Miro frame per view (logical, process, development, physical, scenarios).
- Frame titles from the naming table in `references/notation-miro.md`.
- Shape semantics and colour palette from `references/notation-miro.md` (per-view tables and shared palette mapping for process swimlane views).
- Layout discipline (orientation, spacing, grid, legend) from `references/notation-miro.md`.
- RISEN prompt structure from `skills/miro-diagram-generator/SKILL.md` and its template.

## 5. Outputs

**Option A: draw.io format**
```text
docs/architecture/
├── 00-system-context.md
├── 01-logical-view.md
├── 02-process-view.md
├── 03-development-view.md
├── 04-physical-view.md
├── 05-scenarios-view.md
└── diagrams/
    ├── mermaid/
    │   ├── logical-view.mmd
    │   ├── process-view.mmd
    │   ├── development-view.mmd
    │   ├── physical-view.puml
    │   └── scenarios-view.mmd
    └── drawio/
        ├── logical-view.drawio
        ├── process-view.drawio
        ├── development-view.drawio
        ├── physical-view.drawio
        └── scenarios-view.drawio
```

**Option B: Miro format**
```text
docs/architecture/
├── 00-system-context.md
├── 01-logical-view.md
├── 02-process-view.md
├── 03-development-view.md
├── 04-physical-view.md
├── 05-scenarios-view.md
└── diagrams/
    ├── mermaid/
    │   ├── logical-view.mmd
    │   ├── process-view.mmd
    │   ├── development-view.mmd
    │   ├── physical-view.puml
    │   └── scenarios-view.mmd
    └── miro/
        ├── logical-view-miro-prompt.md
        ├── process-view-miro-prompt.md
        ├── development-view-miro-prompt.md
        ├── physical-view-miro-prompt.md
        ├── scenarios-view-miro-prompt.md
        └── full-board-prompt.md        ← optional aggregate
```

**Option A+B: All formats**
```text
docs/architecture/
├── 00-system-context.md
├── 01-logical-view.md
├── 02-process-view.md
├── 03-development-view.md
├── 04-physical-view.md
├── 05-scenarios-view.md
└── diagrams/
    ├── mermaid/
    │   ├── logical-view.mmd
    │   ├── process-view.mmd
    │   ├── development-view.mmd
    │   ├── physical-view.puml
    │   └── scenarios-view.mmd
    ├── drawio/
    │   ├── logical-view.drawio
    │   ├── process-view.drawio
    │   ├── development-view.drawio
    │   ├── physical-view.drawio
    │   └── scenarios-view.drawio
    └── miro/
        ├── logical-view-miro-prompt.md
        ├── process-view-miro-prompt.md
        ├── development-view-miro-prompt.md
        ├── physical-view-miro-prompt.md
        ├── scenarios-view-miro-prompt.md
        └── full-board-prompt.md        ← optional aggregate
```

## 6. Validation

**For draw.io output:**
1. Every view has both a primary diagram in `diagrams/mermaid/` (`.mmd` / `.puml`) and a `.drawio` file in `diagrams/drawio/`.
2. Component names, scope, and key relationships match between the two formats per view.
3. Each `.drawio` file includes hidden canonical-source provenance with enough inline source content or extracted facts to stand alone when copied outside the repository.
4. Each `.drawio` file is well-formed XML (parses with `xml.etree.ElementTree`) and renders in VS Code's `hediet.vscode-drawio` without manual fixes.

**For Miro output:**
1. Every view has both a primary diagram in `diagrams/mermaid/` (`.mmd` / `.puml`) and a `-miro-prompt.md` file in `diagrams/miro/`.
2. Component names, scope, and key relationships match between the two formats per view.
3. Each prompt includes a canonical-source reference section with enough source content or extracted manifest details to stand alone when copied outside the repository.
4. Each prompt is valid markdown and references the correct view names.

**Shared:**
- Physical view visual outputs must preserve the canonical `.puml` element list and relationship labels before adding zones, styling, or collaboration-layout guidance.
- The skill's own checks pass (`python skills/4plus1-models/scripts/validate-views.py <output-directory>`).
- The bundle smoke test passes: `python scripts/smoke-test.py`.

## 7. Change log

| Date | Change |
|------|--------|
| 2026-05-10 | Created. |
| 2026-05-10 | Vendored the initial architecture-model assets, `draw-io-diagram-generator`, and `draw-io.instructions.md` in top-level workflow folders so the workflow folder is self-contained and portable. |
| 2026-05-10 | Removed all sync/re-vendor mechanics; workflow is now a strict standalone snapshot. |
| 2026-05-10 | Made Miro and draw.io equal first-class options. Workflow now includes format-choice step (Step 2), supports both paths in Step 3, presents both output options in Section 5, and uses conditional validation per format. Prompt renamed to `4plus1-diagrams.prompt.md`. Agent guardrail updated to offer both formats equally. |
| 2026-05-10 | Split skills by responsibility: added `4plus1-models` (core method), retained `draw-io-diagram-generator` (draw.io output), and added `miro-diagram-generator` (Miro output). Updated workflow, prompt, agent, and instructions to load core + selected output skill. Removed legacy combined skill. |
| 2026-05-10 | Added `notation-miro.md` reference file (Miro-track parity with `notation-drawio.md`). Updated §4b to point to it for per-view conventions. |
| 2026-05-10 | Added root-level `architecture-documentation.agent.md` as a no-installer discoverable entrypoint so the same folder can be placed directly under `.github/agents/` or `~/.agents/`. |
| 2026-05-14 | Split flat `diagrams/` output folder into typed subfolders: `diagrams/mermaid/` (`.mmd`/`.puml`), `diagrams/drawio/` (`.drawio`), `diagrams/miro/` (`-miro-prompt.md`, `full-board-prompt.md`). Only the subfolders for the chosen format track are created. |
