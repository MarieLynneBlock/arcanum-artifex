---
description: "Use when creating, editing, or reviewing Miro board setup prompts in -miro-prompt.md files for 4+1 architecture diagrams."
name: 'Miro.instructions'
applyTo: "**/*miro-prompt*.md"
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Miro Board Setup Standards

> **Skill**: Load `skills/miro-diagram-generator/SKILL.md` for full Miro prompt methodology, rules, and validation. **Templates**: Use `templates/miro/miro-prompt-template.md` for individual view prompts and `templates/miro/full-board-prompt-template.md` for an aggregate Miro board prompt. **Examples**: See `skills/miro-diagram-generator/examples/synth-claim/miro-prompts/` for worked examples.

---

## Quick Reference

Miro is an independent output track in this workflow. Do not map or translate draw.io mechanics into Miro prompts.

### Miro Prompt Format

Every prompt **must follow the RISEN framework** (from SKILL.md):
- **Role** — One line: "You are a [title] creating a [view] on a Miro board for [system], reviewed by [audience]."
- **Input** — Bulleted lists: Key elements, connections, context already on the board.
- **Steps** — Numbered, imperative, specific (count shapes, positions, labels, colours).
- **Expectations** — Exact deliverable: frame name, shape counts, arrow types, legend.
- **Narrowing** — What NOT to include (other views, decorative elements, unlabeled arrows).

### File naming and location

- **Extension**: `-miro-prompt.md`
- **Pattern**: `<view-name>-miro-prompt.md` (e.g. `logical-view-miro-prompt.md`)
- **Location**: `diagrams/miro/` subfolder relative to the view output root (e.g. `diagrams/miro/logical-view-miro-prompt.md`) — see output structure in `WORKFLOW.md` §5
- **One prompt per view** — do not combine multiple views

### Semantic colour palette and per-view shape rules

Use `references/notation-miro.md` as the source of truth for Miro colour values, frame naming, shape semantics, layout discipline, and per-view validation. Do not duplicate those values in prompt files; copy only the subset needed for the target Miro frame legend.

For **Process view (swimlane/BPMN style)**, use the same shared semantic palette from `references/notation-miro.md`: user task = primary, service task/start event = success, gateway = warning, end event = error.

---

## Validation Checklist

Before committing a `-miro-prompt.md` file:

- [ ] File follows naming pattern: `<view>-miro-prompt.md`
- [ ] Prompt follows RISEN structure (Role, Input, Steps, Expectations, Narrowing — see template)
- [ ] All component names **exactly match** the corresponding `.mmd`/`.puml` file
- [ ] Steps are numbered, imperative, and include specific counts/positions/labels
- [ ] Colour palette uses hex codes from `references/notation-miro.md` (shared palette mapping applied for swimlane process views)
- [ ] No references to other views (Narrowing section enforces scope)
- [ ] Markdown is valid (no syntax errors)

---

## Reference Files

| File | Use For |
|---|---|
| `references/notation-miro.md` | Per-view frame naming, shape semantics, colour palette, layout discipline |
| `skills/miro-diagram-generator/SKILL.md` | Full Miro methodology and RISEN framework rules |
| `templates/miro/miro-prompt-template.md` | Workflow Miro template for one view — copy and fill in |
| `templates/miro/full-board-prompt-template.md` | Workflow Miro template for an aggregate board prompt |
| `skills/miro-diagram-generator/examples/synth-claim/miro-prompts/` | Real worked examples per view |
