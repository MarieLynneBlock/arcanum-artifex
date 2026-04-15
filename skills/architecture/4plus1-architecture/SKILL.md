---
name: 4plus1-architecture
description: Generate complete 4+1 architectural view model documents for software systems. Use this skill whenever the user wants to document system architecture, create architectural blueprints, produce the Kruchten 4+1 view model, describe a system from multiple stakeholder perspectives (logical, process, development, physical, scenarios/use cases), or generate Miro board prompts for architecture diagrams. Trigger for requests like "document this architecture", "create architecture views", "generate 4+1 views", "make an architecture diagram in Miro", "architectural documentation for this system", "describe the system architecture", or any request involving UML views across logical/process/development/physical/scenario dimensions. Also trigger when the user has described a system design and wants to formalise it.
---

# 4+1 Architecture View Model Skill

Generates structured architectural documentation using Philippe Kruchten's 4+1 View Model. Each view targets a different stakeholder group; together they constitute a complete architectural blueprint.

## View Summary

| View | Stakeholder | Primary UML Artefacts | Reference |
|------|-------------|----------------------|-----------|
| Logical | End-users, analysts | Class diagrams, state diagrams | `references/logical-view.md` |
| Process | System integrators, performance engineers | Sequence, activity, communication diagrams | `references/process-view.md` |
| Development | Developers, software managers | Package diagrams, component diagrams | `references/development-view.md` |
| Physical | System/infrastructure engineers | Deployment diagrams | `references/physical-view.md` |
| Scenarios (+1) | All stakeholders | Use case diagrams, interaction overviews | `references/scenarios.md` |

## Workflow

### Step 1 — Gather System Context

Before generating any view, collect or confirm:
- **System name and purpose** (1–2 sentences)
- **Key stakeholders and their concerns**
- **Technology stack** (languages, frameworks, infra)
- **Scale characteristics** (users, throughput, geographic distribution)
- **Key quality attributes** (availability, latency, security, scalability)
- **Existing constraints** (regulatory, organisational, legacy)

If the user has provided a description, extract these from it and confirm before proceeding. If critical information is missing, ask — don't invent.

### Step 2 — Determine Scope

Ask the user which deliverables they need:

1. **All 5 views** — full 4+1 documentation suite
2. **Specific views only** — e.g., just logical + physical
3. **Miro board prompts** — ready-to-paste prompts for each view in Miro AI
4. **Both documents + Miro** — full package

Default to all 5 views + Miro prompts unless the user specifies otherwise.

### Step 3 — Generate Each View

Read the relevant reference file before generating each view. Generate views in this order (scenarios last, as they validate the others):

1. Read `references/logical-view.md` → generate Logical View document
2. Read `references/process-view.md` → generate Process View document
3. Read `references/development-view.md` → generate Development View document
4. Read `references/physical-view.md` → generate Physical View document
5. Read `references/scenarios.md` → generate Scenarios (+1) document

Each view document must follow the structure defined in its reference file. Do not abbreviate — architectural documentation is a formal deliverable.

### Step 4 — Generate Miro Prompts (if requested)

After generating each view document, produce a corresponding Miro board prompt. Read the example prompts in `examples/` to calibrate the level of specificity required.

Miro prompt rules (non-negotiable):
- Use the RISEN framework (Role, Input, Steps, Expectation, Narrowing)
- Be hyper-specific about layout, shapes, colours, and connections
- Specify exact sticky note counts where possible
- Name every swimlane, frame, or section
- Include colour semantics (e.g., "yellow stickies = external systems")
- Specify connection arrow types (solid = synchronous call, dashed = async/event)
- State what to EXCLUDE explicitly

See `examples/miro-full-board-prompt.md` for a complete worked example. Individual view examples are in `examples/miro-[view-name]-prompt.md`.

### Step 5 — Cross-View Consistency Check

After all views are generated, verify:
- Components in the logical view appear in the development view
- Processes in the process view map to deployable units in the physical view
- Scenarios exercise elements from all four main views
- Naming is consistent across all views (no synonyms for the same component)

Flag any inconsistencies explicitly. Do not silently resolve them — the user needs to make architectural decisions.

### Step 6 — Output Format

Default output per view: a Markdown `.md` file, named `[system-name]-[view-name]-view.md`.

If the user wants a single consolidated document, combine all views with a Table of Contents.

If saving to disk, use this structure:
```
[system-name]-architecture/
├── logical-view.md
├── process-view.md
├── development-view.md
├── physical-view.md
├── scenarios.md
└── miro-prompts/
    ├── miro-logical-view-prompt.md
    ├── miro-process-view-prompt.md
    ├── miro-development-view-prompt.md
    ├── miro-physical-view-prompt.md
    ├── miro-scenarios-prompt.md
    └── miro-full-board-prompt.md
```

## Quality Standards

- **No placeholder text.** Every section must contain real architectural content derived from the system context.
- **Diagrams as prose.** Where you cannot render a UML diagram, describe it precisely enough that a developer could draw it: name every node, every edge, every label.
- **Attribute-driven.** Every architectural decision should be traceable to a quality attribute or constraint. State the rationale.
- **Audience-aware.** Each view document should open with a one-line statement of its target audience and what they should take from it.

## When System Context Is Thin

If the user gives you very little to work with (e.g., "do the 4+1 for a microservices e-commerce platform"), make reasonable, explicitly-stated assumptions and flag them. Generate a complete draft — it is easier for an architect to correct a draft than to start from blank. Mark all assumptions with `> **Assumption:**` blockquotes so they are easy to find and verify.
