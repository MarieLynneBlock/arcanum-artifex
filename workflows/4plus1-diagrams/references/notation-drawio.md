# draw.io conventions for 4+1 views

Per-view conventions for the `4plus1-diagrams` workflow. **Mechanics of mxGraph XML (cell ids, geometry, edges) are owned by [`draw-io-diagram-generator`](../skills/draw-io-diagram-generator/SKILL.md) and the [draw.io instruction file](../instructions/draw-io.instructions.md) (both bundled in top-level workflow folders).** This file only covers what is specific to each 4+1 view.

---

## Per-view skeleton routing

Each view has a starting skeleton in [`../templates/drawio/`](../templates/drawio/). Pick by view + audience:

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

---

## Semantic colour palette (shared across all views)

Use this single palette table consistently across every draw.io view, including BPMN process diagrams.

| Meaning / element | Fill | Stroke | Applies to |
|-------------------|------|--------|------------|
| Primary / informational | `#dae8fc` | `#6c8ebf` | General components and user tasks |
| Success / start event | `#d5e8d4` | `#82b366` | Start/success events and service tasks on happy path |
| Warning / decision | `#fff2cc` | `#d6b656` | Gateways and conditional branches |
| Error / end / alternate path | `#f8cecc` | `#b85450` | End/error/alternate outcomes |
| Neutral / container | `#f5f5f5` | `#666666` | Pools, lanes, groups, frame containers |
| External / partner system | `#e1d5e7` | `#9673a6` | External actors and partner systems |

Notes:
- For Process — BPMN: user task = primary, service task = success, gateway = warning, start event = success, end event = error.
- Keep end events visually distinct with a thicker border (`strokeWidth=3`).

---

## Shape libraries by view

| View | Library / shapes |
|------|------------------|
| Logical | Rounded rectangles for components; dashed rounded rectangles for external systems. |
| Process — sequence | `shape=umlActor` for human actors; rectangles for participants; dashed lines for lifelines (use floating-point edges). |
| Process — BPMN | Vertical pool (`swimlane;horizontal=0`) with horizontal lanes. Ellipses for events (thin stroke = start, thick stroke = end) use success colours for start and error colours for end. Rounded rectangles for tasks split as user task `#dae8fc/#6c8ebf` and service task `#d5e8d4/#82b366`. Rhombus for gateways in `#fff2cc/#d6b656`. |
| Development | Horizontal swimlanes for layers (UI / Application / Infrastructure). Plain rounded rectangles inside for modules. |
| Physical (AWS) | `mxgraph.aws4.group_*` containers (region, vpc, security_group); `mxgraph.aws4.resourceIcon` for services. |
| Physical (Azure) | `mxgraph.azure.*` shapes (e.g. `application_gateway`, `kubernetes_services`, `sql_database`, `storage_accounts`). |
| Physical (generic) | Swimlanes for zones derived from the canonical PlantUML boundaries. Use local/platform/runtime-style zones only when they match the system. Use `shape=cylinder3` only for actual datastores named in the canonical source. |
| Scenarios | Use-case-style flowchart: `shape=umlActor` actor on the left, ellipses for start/end, rounded rectangles for steps, rhombus for decisions. |

---

## Layout discipline

- **Canvas:** A4 landscape (`pageWidth="1169" pageHeight="827"`), 10 px grid, snap to grid.
- **Title cell:** First non-required cell. Plain text style, 18 pt bold, centred, full canvas width.
- **Spacing:** Minimum 40 px between sibling shapes; minimum 20 px padding inside containers.
- **Reading order:** Left-to-right for component / data flow; top-to-bottom for layers / time. BPMN lanes stack top-to-bottom inside a vertical pool.
- **Avoid crossing edges.** Use `edgeStyle=orthogonalEdgeStyle` and reposition shapes if needed.

---

## Edge conventions per view

| View | Solid edge | Dashed edge |
|------|-----------|-------------|
| Logical | uses / depends on (synchronous) | external dependency |
| Process — sequence | synchronous call (`endArrow=block`) | response / async (`endArrow=open;dashed=1`) |
| Process — BPMN | sequence flow | message flow / conditional fallback |
| Development | compile-time dependency | runtime / optional dependency |
| Physical | network connection (label with protocol + port) | replication / async / out-of-band |
| Scenarios | happy-path step | alternate / error path |

Always label edges with their meaning when ambiguous (protocol, port, condition).

For Physical view, prefer the relationship labels from the canonical PlantUML source even when they are workflow labels rather than network protocols. Do not replace `push commits`, `source assets`, or similar canonical labels with generic protocols unless the `.puml` uses those protocols.

---

## Validation

1. Parses with `xml.etree.ElementTree` (well-formed).
2. First two cells are `id="0"` and `id="1"` (per `draw-io-diagram-generator` rules).
3. Renders in VS Code `hediet.vscode-drawio` without manual fixes.
4. Includes hidden canonical-source provenance, preferably an invisible `mxCell` named `canonical-source-ref` with the source path, source format, and enough inline source content or extracted facts to understand the diagram without access to the repository.
5. Component names match the corresponding Mermaid/PlantUML diagram for the same view.
6. For Physical view, relationship endpoints and labels match the corresponding PlantUML diagram exactly.
7. If `<draw-io-diagram-generator>/scripts/validate-drawio.py` exists, it passes.

---

## Anti-patterns

- Inventing shape library prefixes that don't exist (e.g. `mxgraph.gcp.*` is not in the standard libs at the time of writing — use generic shapes instead).
- Mixing AWS and Azure icon sets in the same physical view — pick one or use the cloud-agnostic skeleton.
- Sequence diagrams without lifelines (a flat row of arrows is a flowchart, not a sequence diagram).
- BPMN lanes without a containing pool.
- Replicating mxGraph XML rules from `draw-io-diagram-generator` here — link instead.
