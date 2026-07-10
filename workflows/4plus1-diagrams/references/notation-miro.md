# Miro conventions for 4+1 views

Per-view conventions for the `4plus1-diagrams` workflow. **Mechanics of RISEN prompts (Role/Input/Steps/Expectation/Narrowing structure, template, validation rules) are owned by [`miro-diagram-generator`](../skills/miro-diagram-generator/SKILL.md) and the [Miro instruction file](../instructions/miro.instructions.md) (both bundled in top-level workflow folders).** This file only covers what is specific to each 4+1 view in Miro.

---

## Per-view frame naming

Each view occupies exactly one Miro frame. Use these exact frame titles so cross-view references stay consistent.

| View | Frame title pattern |
|------|---------------------|
| Logical | `Logical view — [System name]` |
| Process (sequence) | `Process view — [System name] (sequence)` |
| Process (swimlane) | `Process view — [System name] (swimlane)` |
| Development | `Development view — [System name]` |
| Physical | `Physical view — [System name]` |
| Scenarios | `Scenarios view — [System name]` |

---

## Semantic colour palette (shared across all views)

Use this single palette table consistently across every Miro frame, including process swimlane/BPMN-style views.

| Meaning / element | Fill | Stroke | Use |
|-------------------|------|--------|-----|
| Primary / informational | `#dae8fc` | `#6c8ebf` | Services, APIs, domain objects, main system components, user tasks |
| Success / start event | `#d5e8d4` | `#82b366` | Start events, entry points, happy-path service tasks |
| Warning / decision | `#fff2cc` | `#d6b656` | Decision points and gateways |
| Error / end / alternate path | `#f8cecc` | `#b85450` | End events, failure paths, alternate outcomes |
| Neutral / container | `#f5f5f5` | `#666666` | Swimlane backgrounds, groups, frame containers |
| External / partner | `#e1d5e7` | `#9673a6` | Third-party systems, external actors, partner services |

Notes:
- For Process view (swimlane): user task = primary, service task = success, gateway = warning, start event = success, end event = error.
- Keep end events distinct by using a thicker border.

---

## Shape semantics by view

### Logical view

| Element | Miro shape | Colour |
|---------|------------|--------|
| Domain component / service | Rounded rectangle | `#dae8fc` |
| External system | Rectangle (dashed border) | `#e1d5e7` |
| Interface / API | Hexagon | `#dae8fc` |
| Inheritance / realisation | Arrow — solid, no label | — |
| Association / call | Arrow — solid, labelled | — |
| Asynchronous / event | Arrow — dashed, labelled | — |

### Process view — sequence (dev-only audience)

| Element | Miro shape | Colour |
|---------|------------|--------|
| Human actor | Sticky note — person icon or star | `#d5e8d4` |
| System participant | Rectangle | `#dae8fc` |
| Synchronous call | Arrow — solid | — |
| Response | Arrow — dashed | — |
| Async event / message | Arrow — dotted | — |
| Lifeline | Thin vertical rectangle | `#f5f5f5` |

### Process view — swimlane (cross-functional / executive audience)

| Element | Miro shape | Colour |
|---------|------------|--------|
| Lane (actor or role) | Horizontal swimlane group | `#f5f5f5` |
| User task | Rounded rectangle | `#dae8fc` (stroke `#6c8ebf`) |
| Service task | Rounded rectangle | `#d5e8d4` (stroke `#82b366`) |
| Start event | Circle — small, filled | `#d5e8d4` (stroke `#82b366`) |
| End event | Circle — bold border | `#f8cecc` (stroke `#b85450`, thicker border) |
| Decision gateway | Diamond | `#fff2cc` (stroke `#d6b656`) |
| Sequence flow | Arrow — solid | — |
| Message flow | Arrow — dashed | — |

### Development view

| Element | Miro shape | Colour |
|---------|------------|--------|
| Layer (UI / App / Data / Infra) | Horizontal swimlane group | `#f5f5f5` |
| Module / package | Rectangle | `#dae8fc` |
| Shared library | Rectangle (dashed border) | `#e1d5e7` |
| Depends-on | Arrow — solid, labelled | — |
| Optional dependency | Arrow — dashed, labelled | — |

### Physical view

Before writing layout instructions for a Physical view prompt, treat the canonical `.puml` as the source of truth and copy its element names and relationship labels into the prompt. The Miro prompt is a Sidekick-optimised drawing brief derived from PlantUML; it must not ask Miro to parse raw PlantUML syntax. Zones are visual grouping aids; they must be derived from the PlantUML deployment boundaries and must not introduce CDN/WAF, load balancers, caches, databases, runners, or protocols that are absent from the canonical source.

For cloud-agnostic Physical views, prefer a Draw.io-like lane layout: three or more tall vertical zone containers with visible headers, nested boundary containers inside each lane, and components placed inside those boundaries. These are ordinary visual lane containers, not BPMN lanes. Show containment through placement, not `contains` arrows. Do not add `Start` or `End` nodes to a physical deployment view.

When generating a Miro prompt for Physical view, expand the canonical PlantUML into one compact Sidekick prompt instead of asking Miro to parse or interpret the `.puml`. Preserve the `.puml` path and title as source-of-truth provenance, then provide the manifest as the drawing source. The prompt should define the frame, zone panels, parent boundary containers, child elements, connectors, approximate coordinates, shape types, fill colours, and stroke colours. Keep the prompt focused on what to draw and what not to draw; avoid optional objects that Sidekick may turn into flowchart nodes.

| Element | Miro shape | Colour |
|---------|------------|--------|
| Deployment zone / region | Tall vertical lane container with header | `#f5f5f5` |
| Node / server / VM | Rectangle | `#dae8fc` |
| Cloud service / managed service | Rounded rectangle | `#dae8fc` |
| Datastore | Cylinder sticky note or stacked rect | `#dae8fc` |
| Network link | Arrow — solid | — |
| Secure / encrypted channel | Arrow — dotted | — |
| External / internet boundary | Dashed outer rectangle | `#e1d5e7` |

### Scenarios (+1) view

| Element | Miro shape | Colour |
|---------|------------|--------|
| Actor (user / system) | Star or circle | `#d5e8d4` |
| Use case / scenario step | Rounded rectangle | `#dae8fc` |
| Decision / branch | Diamond | `#fff2cc` |
| Start | Circle — filled | `#d5e8d4` |
| End | Circle — bold border | `#f8cecc` |
| Flow | Arrow — solid | — |
| Alternative / exception | Arrow — dashed | — |

---

## Legend

Every Miro frame **must** include a legend in the top-right corner of the frame. The legend must list:
- All shape types used in that frame (shape + colour → meaning)
- All arrow types used in that frame (style → meaning)
- The audience the frame is designed for

Exception: for Physical view prompts intended for Miro Sidekick, omit the legend unless the user explicitly asks for one. Sidekick may otherwise generate the legend as a connected flowchart node. If included, the legend must be unconnected and outside the diagram flow.

---

## Frame layout discipline

- **Orientation**: Use landscape layout inside each frame (wider than tall).
- **Reading direction**: Left-to-right for component / data flow; top-to-bottom for layers and time sequences.
- **Swimlane stacking**: Stack swimlane groups vertically (top-to-bottom) inside the frame.
- **Spacing**: Minimum 40 px between sibling shapes; minimum 20 px padding inside groups.
- **Grid alignment**: Align all shapes to the Miro grid (16 px recommended). No orphan shapes off-grid.
- **Arrow routing**: Prefer orthogonal (right-angle) routing. Avoid diagonal edges across swimlanes.
- **No crossing arrows**: Reposition shapes rather than accept crossing arrows.
- **Text**: All labels must be readable at 100% zoom (minimum 14 pt equivalent).

---

## Miro frame validation checklist (per view)

- [ ] Frame title matches the pattern above (with the correct system name)
- [ ] Legend present in top-right with shape + colour + arrow type index
- [ ] Prompt includes a `Canonical source reference` section with the source path and inline Mermaid/PlantUML source or an expanded manifest derived from it
- [ ] All element names match the canonical `.mmd` / `.puml` file exactly
- [ ] For Physical view, all relationship endpoints and labels match the canonical `.puml` file exactly
- [ ] For Physical view, zones are visible lane containers and containment is shown by nesting, not `contains` arrows
- [ ] For Physical view, prompt includes one compact object manifest with zone-panel, parent-boundary, child-element, connector, and title counts
- [ ] For Physical view, prompt names the `.puml` as source of truth but does not ask Miro to parse PlantUML syntax
- [ ] Shape semantics follow the per-view table above
- [ ] Colour values are from the Miro palette (exact hex codes)
- [ ] No shapes from other views appear in this frame
- [ ] No unlabelled arrows (except start/end markers)
- [ ] Grid-aligned, minimum spacing maintained
- [ ] Audience noted in the legend or frame subtitle
