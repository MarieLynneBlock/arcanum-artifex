---
name: 'Draw Io.instructions'
description: "Use when creating, editing, or reviewing draw.io diagrams and mxGraph XML in .drawio, .drawio.svg, or .drawio.png files."
applyTo: "**/*.drawio,**/*.drawio.svg,**/*.drawio.png"
metadata:
  skill-author: 'Marie-Lynne Block'
---

# draw.io Diagram Standards

> **Skill**: Load `skills/draw-io-diagram-generator/SKILL.md` for full workflow, XML recipes, and troubleshooting before generating or editing any `.drawio` file.

---

## Required Workflow

Follow these steps for every draw.io task:

1. **Identify** the diagram type (flowchart / architecture / sequence / ER / UML / network / BPMN)
2. **Select** the matching template from `skills/draw-io-diagram-generator/assets/templates/` and adapt it, or start from the minimal skeleton. For 4+1 views, use `templates/drawio/` plus `references/notation-drawio.md` instead.
3. **Plan** the layout on paper before writing XML — define tiers, actors, or entities first
4. **Generate** valid mxGraph XML following the rules below
5. **Validate** using `python skills/draw-io-diagram-generator/scripts/validate-drawio.py <file>`
6. **Confirm** the file renders by opening it in VS Code with the draw.io extension (`hediet.vscode-drawio`)

---

## XML Structure Rules (Non-Negotiable)

```xml
<!-- Set modified to the current ISO 8601 timestamp when generating a new file -->
<mxfile host="Electron" modified="" version="26.0.0">
  <diagram id="unique-id" name="Page Name">
    <mxGraphModel ...>
      <root>
        <mxCell id="0" />                          <!-- REQUIRED: always first -->
        <mxCell id="1" parent="0" />               <!-- REQUIRED: always second -->
        <!-- all other cells go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- `id="0"` and `id="1"` **must** be present and must be the first two cells — no exceptions
- Every cell `id` must be **unique** within the diagram
- Every vertex (`vertex="1"`) must have a child `<mxGeometry x y width height as="geometry">`
- Every edge (`edge="1"`) must have `source`/`target` pointing to existing vertex ids — **exception**: floating edges (sequence diagram lifelines) use `<mxPoint as="sourcePoint">` and `<mxPoint as="targetPoint">` inside `<mxGeometry>` instead of `source`/`target` attributes
- Every cell except id=0 must have `parent` pointing to an existing id
- Children of a container (swimlane) use **coordinates relative to their parent**, not the canvas

---

## Mandatory Style Conventions

### Semantic Colour Palette — Use consistently across the project

| Role | fillColor | strokeColor |
|---|---|---|
| Primary / Info (default) | `#dae8fc` | `#6c8ebf` |
| Success / Start / Positive | `#d5e8d4` | `#82b366` |
| Warning / Decision | `#fff2cc` | `#d6b656` |
| Error / End / Danger | `#f8cecc` | `#b85450` |
| Neutral / Interface | `#f5f5f5` | `#666666` |
| External / Partner | `#e1d5e7` | `#9673a6` |

### BPMN Colour Override — Process view only

When generating BPMN process diagrams (including `process-view-bpmn.drawio` in this workflow), map BPMN elements to the semantic palette above using this table:

| BPMN element | fillColor | strokeColor |
|---|---|---|
| User task (primary/informational) | `#dae8fc` | `#6c8ebf` |
| Service task (success path) | `#d5e8d4` | `#82b366` |
| Gateway (warning/decision) | `#fff2cc` | `#d6b656` |
| Event (start/success) | `#d5e8d4` | `#82b366` |
| Event (end/error/alternate) | `#f8cecc` | `#b85450` |

Keep lane/pool containers neutral (`#f5f5f5` / `#666666`) and use thicker border for end events.

### Always include on vertex shapes

```
whiteSpace=wrap;html=1;
```

### Use `html=1` whenever a label contains HTML tags (`<b>`, `<i>`, `<br>`)

### Standard connectors

```
edgeStyle=orthogonalEdgeStyle;html=1;
```

---

## Diagram-Type Quick Reference

| Type | Container | Key shapes | Connector style |
|---|---|---|---|
| Flowchart | None | `ellipse` (start/end), `rounded=1` (process), `rhombus` (decision) | `orthogonalEdgeStyle` |
| Architecture | `swimlane` per tier | `rounded=1` services, cloud/DB shapes | `orthogonalEdgeStyle` with labels |
| Sequence | None | `mxgraph.uml.actor`, dashed lifeline edges | `endArrow=block` (sync), `endArrow=open;dashed=1` (return) |
| ER Diagram | `shape=table;childLayout=tableLayout` | `shape=tableRow`, `shape=partialRectangle` | `entityRelationEdgeStyle;endArrow=ERmany;startArrow=ERone` |
| UML Class | `swimlane` per class | text rows for attributes/methods | `endArrow=block;endFill=0` (inherit), `dashed=1` (realise) |

---

## Layout Best Practices

- Align all coordinates to the **10 px grid** (values divisible by 10)
- **Horizontal**: 40–60 px gap between same-row shapes
- **Vertical**: 80–120 px gap between tier rows
- Standard shape size: `120 × 60` px (process), `200 × 100` px (decision diamond)
- Default canvas: A4 landscape `1169 × 827` px
- Maximum **40 cells per page** — split into multiple pages for larger diagrams
- Add a **title text cell** at top of every page:
  ```
  style="text;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;align=center;"
  ```

---

## File and Naming Conventions

- Extension: `.drawio` for version-controlled diagrams, `.drawio.svg` for files embedded in Markdown
- Naming: `kebab-case` — e.g. `order-flow.drawio`, `database-schema.drawio`
- Location: `docs/` or `architecture/` alongside the code they document
- Multi-page: use one `<diagram>` element per logical view within the same `<mxfile>`

---

## Validation Checklist (run before every commit)

- [ ] `<mxCell id="0" />` and `<mxCell id="1" parent="0" />` are the first two cells
- [ ] All cell ids are unique within their diagram
- [ ] All edge `source`/`target` ids resolve to existing vertices
- [ ] All vertex cells have `<mxGeometry as="geometry">`
- [ ] All cells (except id=0) have a valid `parent`
- [ ] XML is well-formed — no unclosed tags, no bare `&`, `<`, `>` in attribute values
- [ ] Semantic colour palette used consistently
- [ ] Title cell present on every page

```bash
# Run automated validation
python skills/draw-io-diagram-generator/scripts/validate-drawio.py <file.drawio>
```

---

## Reference Files

| File | Use For |
|---|---|
| `skills/draw-io-diagram-generator/SKILL.md` | Full agent workflow, XML recipes, troubleshooting |
| `skills/draw-io-diagram-generator/references/drawio-xml-schema.md` | Complete mxCell attribute reference |
| `skills/draw-io-diagram-generator/references/style-reference.md` | All style keys, shape names, edge types |
| `skills/draw-io-diagram-generator/references/shape-libraries.md` | Shape library catalogue with style strings |
| `skills/draw-io-diagram-generator/assets/templates/` | Ready-to-use `.drawio` templates per diagram type |
| `skills/draw-io-diagram-generator/scripts/validate-drawio.py` | XML structure validator |
| `skills/draw-io-diagram-generator/scripts/add-shape.py` | CLI: add a shape to an existing diagram |
| `references/notation-drawio.md` | Per-view draw.io conventions for the draw.io track |
