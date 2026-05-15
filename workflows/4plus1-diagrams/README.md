---
name: 4+1 Architecture Diagrams (Miro & draw.io)
description: Standalone workflow bundle for producing Kruchten 4+1 architecture views with canonical diagram-as-code plus editable draw.io or Miro output.
metadata:
  skill-author: Marie-Lynne Block
---

# 4+1 Architecture Diagrams (Miro & draw.io)

Produce a complete Kruchten 4+1 architectural view model **with editable visual diagrams alongside the canonical Mermaid/PlantUML output**. Choose your preferred format:
- **draw.io** (`.drawio`) — editable in VS Code, draw.io desktop, or app.diagrams.net
- **Miro** (prompts) — editable in Miro for real-time team collaboration

## When to use this workflow

Run this workflow when **all** of the following are true:

- You need a 4+1 architecture documentation set (logical / process / development / physical / scenarios).
- The audience or downstream tooling needs **editable visual diagrams** in addition to Mermaid.
- You want either:
  - **draw.io** exports (PNG/SVG for slide decks, or interactive `.drawio` for desktop editing), or
  - **Miro** collaboration prompts (for real-time whiteboard editing and team discussion).

If Mermaid/PlantUML core views are enough → use the [`4plus1-models`](skills/4plus1-models/) skill on its own. If only one output track is needed without full 4+1 orchestration, use [`draw-io-diagram-generator`](skills/draw-io-diagram-generator/) or [`miro-diagram-generator`](skills/miro-diagram-generator/) directly.

## Self-contained

This folder ships with **vendored copies** of every skill and instruction it depends on, under `skills/` and `instructions/`. Copy the entire `4plus1-diagrams/` folder into any repo and it runs as-is — no other files in this repo are required at runtime.

This workflow is a **frozen snapshot**. It has no sync contract and no runtime dependency on any path outside this folder.

## Discoverable placement (no installer)

This bundle includes a discoverable entry agent at `architecture-documentation.agent.md`.

You can place this folder directly in either discoverable location, with no rewrite step:

- Repo scope: `.github/agents/4plus1-diagrams/`
- User scope: `~/.agents/4plus1-diagrams/`

The discoverable entrypoint delegates to local files in the same folder, so the bundle stays vendor-agnostic and standalone.

## How to invoke

Pick one entry point:

- **Prompt** — paste [`prompts/4plus1-diagrams.prompt.md`](prompts/4plus1-diagrams.prompt.md) into Copilot Chat (or the equivalent in Claude / Cursor).
- **Agent (discoverable)** — invoke [`architecture-documentation.agent.md`](architecture-documentation.agent.md) ("Architecture Documentation (4plus1-diagrams)").
- **Agent (workflow-local orchestrator)** — [`agents/architecture-documentation.agent.md`](agents/architecture-documentation.agent.md).
- **Manual** — follow [`WORKFLOW.md`](WORKFLOW.md) step by step.

## Inside this folder

- [WORKFLOW.md](WORKFLOW.md) — the orchestration playbook (source of truth for what the agent / prompt does).
- `skills/4plus1-models/` — core 4+1 method skill (authoritative for architecture logic).
- `skills/draw-io-diagram-generator/` — vendored copy of the draw.io generator skill (authoritative for mxGraph XML mechanics).
- `skills/miro-diagram-generator/` — vendored copy of the Miro generator skill (authoritative for Miro prompt mechanics).
- `instructions/` — vendored instruction files (draw.io and Miro).
- `architecture-documentation.agent.md` — discoverable root entrypoint for repo-level or user-level placement.
- `agents/` — the workflow-specific thin agent (no MCP servers).
- `prompts/` — Copilot/Cursor/Claude prompts that trigger the workflow.
- `templates/drawio/` — eight `.drawio` skeletons, one per view variant.
- `templates/miro/` — Miro prompt templates for per-view and full-board setup prompts.
- `references/notation-drawio.md` — per-view draw.io conventions (palette, shape libraries, layout discipline).
- `references/notation-miro.md` — per-view Miro conventions (frame naming, shape semantics, colour palette, layout discipline).
- `scripts/smoke-test.py` — bundle smoke test for internal links, required assets, stale references, Miro prompt names, and draw.io XML templates.
## Smoke test

Run this after changing files, folders, links, examples, templates, or skill boundaries:

```bash
python scripts/smoke-test.py
```

The smoke test validates that the workflow remains self-contained and that both output tracks still have resolvable local assets.

## What you get back

Choose your format:

**Option A: draw.io output** — editable `.drawio` files
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
        ├── logical-view.drawio         ← Edit in VS Code or draw.io
        ├── process-view.drawio
        ├── development-view.drawio
        ├── physical-view.drawio
        └── scenarios-view.drawio
```

**Option B: Miro output** — collaboration prompts
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
        ├── logical-view-miro-prompt.md     ← Paste into Miro
        ├── process-view-miro-prompt.md
        ├── development-view-miro-prompt.md
        ├── physical-view-miro-prompt.md
        └── scenarios-view-miro-prompt.md
```
