---
name: architecture-models-4plus1
description: Produce Philippe Kruchten's 4+1 architectural view model for a software system, with rendered diagrams (Mermaid primary, PlantUML fallback for deployment) AND Miro RISEN prompts for each view. Use this skill whenever the user mentions "4+1", "architecture views", "architectural documentation", "logical view", "process view", "development view", "physical view", or "deployment view" — and also whenever the user asks to document system architecture, produce architecture blueprints, generate architecture diagrams, or prepare architecture content for review with non-developer stakeholders, even if they don't say "4+1" explicitly. Works with zero-input (user gives a paragraph, skill drafts a full architecture), interview mode (user has detailed context), or partial mode (user wants only one or two views). Flexes notation to audience — UML-flavoured for dev-only audiences, BPMN-style swimlanes for cross-functional audiences, simplified C4 for executives.
---

# 4+1 Architecture Models

Generates Kruchten's 4+1 View Model for any software system. Each deliverable per view is two artefacts:

1. **A rendered architectural drawing** — Mermaid (primary) or PlantUML (for deployment-heavy physical views).
2. **A Miro RISEN prompt** — ready to paste into Miro AI Sidekick to recreate the same view on a Miro board.

Plus a prose view document that wraps both and explains the architecture decisions, quality attributes, and concerns.

This skill is portable by design: the same SKILL.md works natively in Claude Code, via a Cursor rule (`shims/cursor/`), and via a Copilot custom prompt (`shims/copilot/`). Change logic here; the shims will pick it up.

## The five views at a glance

| View | Who reads it | What it answers | Primary notation |
|------|-------------|-----------------|------------------|
| Logical | End-users, analysts, architects | What components exist and how they relate | Mermaid class / component / C4 Container |
| Process | Integrators, performance engineers, operations, BAs | How the system behaves at runtime | Mermaid sequenceDiagram (dev) / flowchart with swimlanes (cross-functional) |
| Development | Developers, software managers | How the codebase is organised | Mermaid flowchart / C4 Component |
| Physical | SRE, infrastructure engineers | How it's deployed and operated | PlantUML deployment + AWS/Azure/GCP stdlib (primary) / Mermaid C4Deployment (fallback) |
| Scenarios (+1) | All stakeholders | Key use cases that exercise the other four | Mermaid flowchart (use-case style) + mini sequences |

Reference files per view: `references/logical-view.md`, `references/process-view.md`, `references/development-view.md`, `references/physical-view.md`, `references/scenarios-view.md`. Read the relevant reference before generating that view — do not attempt any view from memory.

Notation cheatsheets: `references/notation-mermaid.md`, `references/notation-plantuml.md`, `references/notation-bpmn-in-mermaid.md`. Read these the first time you render in a given tool.

## Workflow

### Step 1 — Determine invocation mode

Decide which mode the user is in. If ambiguous, ask.

- **Zero-input mode** — user gives a short description (a paragraph or less) and expects you to draft a full 4+1 with flagged assumptions. Example: *"Do a 4+1 for a microservices e-commerce platform."*
- **Interview mode** — user has real context and wants rigour. Ask follow-ups for anything missing from the checklist in Step 3 before drafting.
- **Partial mode** — user wants only specific views. Example: *"Just the physical view with PlantUML."* Skip view-generation steps that weren't requested; still do the context gathering for the requested view(s).

### Step 2 — Determine audience (ALWAYS ASK unless user pre-stated it)

Audience drives notation. Ask this exact question if the user has not already told you:

> *"Who's the primary audience for this documentation?*
> *(a) **Dev-only** — developers, architects, SRE. UML-flavoured notation throughout.*
> *(b) **Cross-functional** — includes business analysts, product, operations. BPMN-style swimlanes for the process view; UML-flavoured elsewhere.*
> *(c) **Executive** — senior stakeholders, steering committees. Simplified C4 at context level only; skip low-level detail."*

Record the answer. It determines which notation each view uses. Each reference file has an **Audience routing** section that tells you exactly what to render for (a), (b), or (c).

### Step 3 — Gather system context

Before generating any view, confirm or extract these. If critical information is missing, **ask — do not invent silently**. If in zero-input mode, generate reasonable assumptions and mark each one with `> **Assumption:**` blockquotes so the architect can find and verify them.

Checklist:
- **System name and one-line purpose**
- **Key stakeholders and their primary concerns** (2–5 stakeholders, 1 concern each)
- **Technology stack** — languages, frameworks, datastores, infra provider(s)
- **Scale characteristics** — users, throughput, geographic distribution, data volume
- **Key quality attributes** — pick from: availability, latency, throughput, security, privacy, scalability, maintainability, portability, auditability, cost
- **Constraints** — regulatory (GDPR, HIPAA, PCI-DSS, AI Act, etc.), organisational, legacy-integration
- **Out of scope** — what the system deliberately does not do

### Step 4 — Route concerns into each view

Read `concerns/README.md` for the catalogue of concern modules. For each view, pull in the concerns that apply (by default: `gdpr-data-protection.md`, `security.md`, `bias-fairness.md` if ML is present, and `regulatory-compliance.md` if the system operates in a regulated sector).

Each concern module has a per-view **prompts** section telling you what to check for that view. Surface any genuine concerns as `> **Concern (GDPR):** …` blockquotes inside the view document. Do not boilerplate — only flag what actually applies to this system.

### Step 5 — Generate each view

Generate in this exact order. Scenarios go last because they validate the others.

1. **Logical view** — read `references/logical-view.md`, generate the Mermaid diagram, wrap in prose, flag concerns.
2. **Process view** — read `references/process-view.md`, generate the Mermaid diagram (sequence or swimlane-flowchart per audience), wrap in prose, flag concerns.
3. **Development view** — read `references/development-view.md`, generate the Mermaid diagram, wrap in prose, flag concerns.
4. **Physical view** — read `references/physical-view.md`, generate the PlantUML diagram (with cloud-provider stdlib where relevant), wrap in prose, flag concerns.
5. **Scenarios (+1)** — read `references/scenarios-view.md`, produce the scenario list with a diagram for each key scenario, verify that each scenario exercises elements from all four main views.

Each view document uses the structure in `templates/view-template.md`. Do not abbreviate — architectural documentation is a formal deliverable that must survive being read six months later by someone who wasn't in the conversation.

### Step 6 — Generate Miro prompts

After each view document, produce the corresponding Miro prompt using `templates/miro-prompt-template.md`. Miro prompt rules (non-negotiable, derived from the RISEN framework):

- **Role** — one line, stating Miro's role (e.g. "You are a senior solutions architect creating a physical view diagram on a Miro board…").
- **Input** — a tight summary of the view (what's being depicted, scope boundaries, key components). Reference board context explicitly if the user has uploaded sticky notes or docs.
- **Steps** — numbered, imperative, specific. Miro AI produces dramatically better results when you say "1. Create a frame titled X. 2. Place 5 sticky notes labelled A–E in the top-left corner. 3. Draw solid arrows from each sticky to the central component." than when you say "make it look like a process flow."
- **Expectation** — specify exact counts, exact colour semantics, exact connection types. E.g. "Output: 1 frame, 12 sticky notes (6 yellow for external systems, 6 blue for internal services), 14 solid arrows for sync calls, 4 dashed arrows for async events."
- **Narrowing** — state what to exclude. E.g. "Do NOT include authentication flows. Do NOT draw data flows — this is a deployment view only."

See `examples/synth-claim/miro-prompts/` for fully-worked examples.

### Step 7 — Cross-view consistency check

After all views are generated, verify:

- Components named in the logical view appear in the development view (with the same names).
- Processes in the process view map to deployable units in the physical view.
- Scenarios exercise elements from all four main views (each scenario should name components from at least three views).
- Naming is consistent — no synonyms for the same component. If there are synonyms, flag them explicitly; do not silently resolve them — the architect needs to decide.

`scripts/validate-views.py` performs mechanical checks on a generated view directory (same names used across views, no orphan components). Run it if you're outputting to disk and want a quick sanity check.

### Step 8 — Output format

Default output structure on disk:

```
[system-name]-architecture/
├── 00-system-context.md        # The gathered context from Step 3
├── 01-logical-view.md
├── 02-process-view.md
├── 03-development-view.md
├── 04-physical-view.md
├── 05-scenarios-view.md
├── diagrams/                   # Rendered diagram sources (edit these, regenerate prose)
│   ├── logical-view.mmd        # Mermaid source
│   ├── process-view.mmd
│   ├── development-view.mmd
│   ├── physical-view.puml      # PlantUML source
│   └── scenarios-view.mmd
└── miro-prompts/
    ├── logical-view-prompt.md
    ├── process-view-prompt.md
    ├── development-view-prompt.md
    ├── physical-view-prompt.md
    ├── scenarios-view-prompt.md
    └── full-board-prompt.md     # One megaprompt to regenerate the entire board
```

If the user wants a single consolidated document, combine all five views with a Table of Contents and put the diagram sources inline. Keep `miro-prompts/` as a separate folder regardless.

## Quality standards (hold the line on these)

- **No placeholder text.** Every section contains real architectural content. If you can't generate it, say so and ask.
- **Diagram + prose, always.** The diagram is the artefact; the prose explains the decisions. Neither alone is sufficient.
- **Rationale is mandatory.** Every significant architectural choice states the quality attribute or constraint that drove it. "We use an API gateway" is incomplete; "We use an API gateway to enforce uniform authN/authZ across services (security, maintainability)" is complete.
- **Audience statement.** Each view document opens with a one-line statement of its audience and the one thing they should take away.
- **Assumptions are visible.** Mark all assumptions with `> **Assumption:**` blockquotes so the architect can find and verify them.
- **Concerns are specific.** Do not boilerplate GDPR language into every view. Flag the actual concerns that apply.

## Partial mode shortcuts

- *"Just the physical view"* → Skip Steps 5.1–5.3 and 5.5. Do Step 5.4 only. Generate the corresponding Miro prompt.
- *"Regenerate the process view with BPMN swimlanes instead of sequence"* → Re-read `references/process-view.md`, switch audience to (b), regenerate just that view.
- *"Add a new concern module for FCA compliance"* → Ask the user for the concern content (or draft one based on their description), save to `concerns/fca-compliance.md`, add it to the concern catalogue in `concerns/README.md`.

## When this skill is not the right fit

- User wants low-level sequence diagrams for a specific API → that's an API design task, use their API-design skill if they have one.
- User wants code-level class diagrams for a single module → that's development-view territory but may not need the full 4+1; confirm scope.
- User wants a C4 model only (not 4+1) → mention that 4+1 and C4 are complementary, offer to produce both or just C4.

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

**Concerns (modular — add, remove, or swap as the company evolves):**
- `concerns/README.md` (catalogue)
- `concerns/gdpr-data-protection.md`
- `concerns/security.md`
- `concerns/bias-fairness.md`
- `concerns/regulatory-compliance.md`
- `concerns/sustainability-climate.md`
- `concerns/accessibility.md`

**Templates:**
- `templates/view-template.md`
- `templates/miro-prompt-template.md`

**Worked example (study this to calibrate tone and specificity):**
- `examples/synth-claim/` — a synthetic hybrid-cloud claims-processing platform with all five views rendered, GDPR concerns flagged, and Miro prompts generated.

**Scripts:**
- `scripts/validate-views.py` — cross-view consistency check.

**Shims (same skill, different tools):**
- `shims/cursor/architecture-models-4plus1.mdc` — Cursor rule
- `shims/copilot/architecture-models-4plus1.prompt.md` — Copilot custom prompt
