# Miro conventions for 4+1 views

Per-view conventions for the `4plus1-diagrams` workflow. **Mechanics of RISEN prompts (Role/Input/Steps/Expectation/Narrowing structure, template, validation rules) are owned by [`miro-diagram-generator`](../skills/miro-diagram-generator/SKILL.md) and the [Miro instruction file](../instructions/miro.instructions.md) (both vendored in top-level workflow folders).** This file only covers what is specific to each 4+1 view in Miro.

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

## Semantic colour palette (Miro track)

Use these fill colours for **sticky notes and shapes**. Miro renders colours by their hex value — apply consistently to encode the same meaning across all frames.

| Meaning | Hex | Use |
|---------|-----|-----|
| Primary / informational | `#dae8fc` | Services, APIs, domain objects, main system components |
| Success / entry point | `#d5e8d4` | Start events, entry points, happy path nodes |
| Warning / decision | `#fff2cc` | Decision points, gateways, conditional branches |
| Error / termination | `#f8cecc` | Error states, end events, failure paths |
| Neutral / container | `#f5f5f5` | Swimlane backgrounds, groups, UI containers |
| External / partner | `#e1d5e7` | Third-party systems, external actors, partner services |

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
| Task | Rounded rectangle | `#dae8fc` |
| Start event | Circle — small, filled | `#d5e8d4` |
| End event | Circle — bold border | `#f8cecc` |
| Decision gateway | Diamond | `#fff2cc` |
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

| Element | Miro shape | Colour |
|---------|------------|--------|
| Deployment zone / region | Large rectangle (outer container) | `#f5f5f5` |
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
- [ ] All element names match the canonical `.mmd` / `.puml` file exactly
- [ ] Shape semantics follow the per-view table above
- [ ] Colour values are from the Miro palette (exact hex codes)
- [ ] No shapes from other views appear in this frame
- [ ] No unlabelled arrows (except start/end markers)
- [ ] Grid-aligned, minimum spacing maintained
- [ ] Audience noted in the legend or frame subtitle
