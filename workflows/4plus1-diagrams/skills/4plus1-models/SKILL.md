---
name: 4plus1-models
description: Produce Philippe Kruchten's 4+1 architectural view model for a software system. This is the core method skill: audience routing, concerns, per-view generation, and cross-view consistency. It outputs canonical diagram-as-code (Mermaid / PlantUML) plus view prose, and does not own draw.io or Miro rendering.
metadata:
  skill-author: 'Marie-Lynne Block'
---

# 4+1 Models (Core)

Generates Kruchten's 4+1 View Model for any software system.

This skill owns method logic only:
- invocation mode and audience routing
- context and concern capture
- per-view architecture content
- canonical diagram-as-code (Mermaid / PlantUML)
- cross-view consistency

It does not own output-track rendering mechanics for draw.io or Miro.

## The five views at a glance

| View | Who reads it | What it answers | Primary notation |
|------|-------------|-----------------|------------------|
| Logical | End-users, analysts, architects | What components exist and how they relate | Mermaid class / component / C4 Container |
| Process | Integrators, performance engineers, operations, BAs | How the system behaves at runtime | Mermaid sequenceDiagram (dev) / flowchart with swimlanes (cross-functional) |
| Development | Developers, software managers | How the codebase is organised | Mermaid flowchart / C4 Component |
| Physical | SRE, infrastructure engineers | How it's deployed and operated | PlantUML deployment + AWS/Azure/GCP stdlib (primary) / Mermaid C4Deployment (fallback) |
| Scenarios (+1) | All stakeholders | Key use cases that exercise the other four | Mermaid flowchart (use-case style) + mini sequences |

Reference files per view: `references/logical-view.md`, `references/process-view.md`, `references/development-view.md`, `references/physical-view.md`, `references/scenarios-view.md`.

## Workflow

### Step 1 — Determine invocation mode

Decide which mode the user is in. If ambiguous, ask.

- **Zero-input mode** — user gives a short description and expects a draft with explicit assumptions.
- **Interview mode** — user has real context and wants rigor.
- **Partial mode** — user wants only one or a subset of views.

### Step 2 — Determine audience (ALWAYS ASK unless user pre-stated it)

Ask if missing:

> "Who's the primary audience for this documentation?
> (a) Dev-only
> (b) Cross-functional
> (c) Executive"

Audience determines notation choice per view.

### Step 3 — Gather system context

Gather context with one concise checklist first, then only targeted follow-ups if needed.

Start with at most these fields:
- System name and purpose
- Stakeholders and concerns
- Tech stack
- Scale profile
- Quality attributes
- Constraints
- Out of scope

Mark assumptions explicitly using `> **Assumption:**`.

Questioning rules:
- Keep the first interaction to one grouped question block.
- If the user gives partial info, proceed with assumptions rather than asking every missing detail immediately.
- Ask one follow-up at a time only when a missing answer blocks the next deliverable.
- Use plain wording and provide concise options where possible.

### Step 4 — Route concerns into each view

Use `concerns/README.md` to select relevant concern modules.

Default concerns:
- `gdpr-data-protection.md`
- `security.md`
- `bias-fairness.md` (if ML present)
- `regulatory-compliance.md` (if regulated domain)

### Step 5 — Generate each view

Generate in order:
1. Logical
2. Process
3. Development
4. Physical
5. Scenarios (+1)

Use `templates/view-template.md`.

### Step 6 — Cross-view consistency check

Verify:
- consistent naming across views
- process behaviors map to deployable units
- scenarios exercise elements from core views

If writing to disk, run:

```bash
python scripts/validate-views.py <output-directory>
```

For example:

```bash
python scripts/validate-views.py docs/architecture
```

### Step 7 — Output format (core)

```text
[system-name]-architecture/
├── 00-system-context.md
├── 01-logical-view.md
├── 02-process-view.md
├── 03-development-view.md
├── 04-physical-view.md
├── 05-scenarios-view.md
└── diagrams/
    └── mermaid/
        ├── logical-view.mmd
        ├── process-view.mmd
        ├── development-view.mmd
        ├── physical-view.puml
        └── scenarios-view.mmd
```

When used inside the `4plus1-diagrams` workflow, the visual-format skill adds a `diagrams/drawio/` or `diagrams/miro/` sibling folder alongside `diagrams/mermaid/`.

## Quality standards

- No placeholders
- Diagram + prose for every view
- Rationale tied to quality attributes/constraints
- Audience statement at top of each view
- Visible assumptions
- Specific concerns only

## Reference index

**Per-view detail:**
- `references/logical-view.md`
- `references/process-view.md`
- `references/development-view.md`
- `references/physical-view.md`
- `references/scenarios-view.md`

**Notation cheatsheets:**
- `references/notation-mermaid.md`
- `references/notation-plantuml.md`
- `references/notation-bpmn-in-mermaid.md`

**Concerns:**
- `concerns/README.md`
- `concerns/gdpr-data-protection.md`
- `concerns/security.md`
- `concerns/bias-fairness.md`
- `concerns/regulatory-compliance.md`
- `concerns/sustainability-climate.md`
- `concerns/accessibility.md`

**Template:**
- `templates/view-template.md`

**Worked example (core views):**
- `examples/synth-claim/`

**Scripts:**
- `scripts/validate-views.py`
