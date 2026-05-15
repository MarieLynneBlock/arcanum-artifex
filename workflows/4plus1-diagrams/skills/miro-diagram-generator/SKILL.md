---
name: miro-diagram-generator
description: Generate Miro board prompts for architecture diagrams. Use this skill to produce per-view Miro prompts from canonical 4+1 diagram sources, with RISEN structure, strict scope boundaries, and track-specific validation.
metadata:
  skill-author: Marie-Lynne Block
---

# Miro Diagram Generator

Generates Miro prompt artifacts for architecture views.

This skill is output-track specific:
- consumes canonical architecture view content
- produces Miro prompts only
- does not own 4+1 method logic

## Inputs required

For each view, provide:
- view name (`logical`, `process`, `development`, `physical`, `scenarios`)
- audience (`dev-only`, `cross-functional`, `executive`)
- exact component list
- exact relationship list
- canonical source path (`.mmd` or `.puml`)

## Workflow

### Step 1 — Load template

Use `templates/miro-prompt-template.md` as the base.

### Step 2 — Fill RISEN sections

The prompt must include:
- **Role**
- **Input**
- **Steps**
- **Expectation**
- **Narrowing**

### Step 3 — Enforce deterministic specificity

All prompts must include:
- explicit frame title
- explicit counts of shapes and arrows
- explicit labels for all entities and connectors
- explicit arrow semantics (solid/dashed/dotted)
- explicit exclusions in Narrowing
- for BPMN/swimlane process views, explicit shared semantic mapping: user task = primary, service task/start event = success, gateway = warning, end event = error, lane = neutral

### Step 4 — Validate against canonical source

Check that names and relationships in the prompt match the canonical source exactly.

### Step 5 — Write per-view output

Output files:

```text
diagrams/miro/
  <view>-miro-prompt.md
```

Optional aggregate output:

```text
diagrams/miro/full-board-prompt.md
```

Use `templates/full-board-prompt-template.md` when the user wants one aggregate board prompt that orchestrates all per-view Miro prompts.

## Output contract

Each output must be:
- valid markdown
- one view per file
- scoped to the target view only
- free of cross-view leakage

## Validation checklist

- naming pattern: `<view>-miro-prompt.md`
- template sections present (Role, Input, Steps, Expectation, Narrowing)
- all component names match canonical source
- all relationship labels match canonical source
- no unlabeled arrows in instructions
- no unsupported decorative elements
- BPMN/swimlane process prompts include the shared semantic mapping above

## References

- `templates/miro-prompt-template.md`
- `templates/full-board-prompt-template.md`
- `examples/synth-claim/miro-prompts/`
