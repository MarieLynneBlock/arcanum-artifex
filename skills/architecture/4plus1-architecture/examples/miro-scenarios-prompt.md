# Miro Prompt — Scenarios (+1) View

## How to use this file

Copy the prompt below, replace all `[PLACEHOLDER]` values, and paste into Miro AI Sidekick. Attach your scenario descriptions and use case list from the board as context.

---

## Prompt Template

```
You are a software architect creating the Scenarios ("+1") view of a 4+1 architectural model. This view validates the architecture by showing how selected use cases exercise all four other views. The audience includes all stakeholders: developers, product owners, QA, and management. Clarity and accessibility are essential — avoid implementation jargon in scenario descriptions.

CONTEXT FROM BOARD: [Select and attach: scenario inventory table, use case list, actor descriptions, and any existing flow notes from your board]

Create the following on this Miro board in a structured layout. Do NOT put everything in one frame — use the grid layout described below.

STEP 1 — MAIN CANVAS SETUP
The overall layout is a grid:
- Row 1 (top): One wide banner frame — "Use Case Overview"
- Row 2: [N] scenario frames arranged horizontally — one frame per scenario
- Row 3 (bottom): One wide banner frame — "Architecture Validation Matrix"
Leave 60px gap between all frames.

STEP 2 — USE CASE OVERVIEW FRAME (Row 1)
Create a wide frame (full canvas width) titled "Use Case Overview — [SYSTEM NAME]" with background #2D4A6A (dark blue), white text.

Inside this frame:

Left half — System boundary diagram:
Create a large rectangle with dashed border (#FFFFFF) labelled "«system» [SYSTEM NAME]" inside the frame.
Create actor icons — one per actor — outside the system boundary rectangle:
- Primary actors on the left: draw a stick figure (circle head + lines for body/arms/legs) with actor name below. Actors: [LIST PRIMARY ACTORS]
- Secondary actors on the right: draw stick figures for: [LIST SECONDARY ACTORS / EXTERNAL SYSTEMS]
Inside the system boundary rectangle, create oval shapes for use cases — one per scenario:
- UC1: "[SCENARIO 1 NAME]" — oval colour #4A9FD4 (blue)
- UC2: "[SCENARIO 2 NAME]" — oval colour #4A9FD4
[repeat for each scenario]
Connect actors to their use cases with solid white lines.
Connect use cases to each other with dashed white arrows where applicable:
- "«include»" relationship: dashed arrow pointing TO the included use case, labelled "«include»"
- "«extend»" relationship: dashed arrow pointing TO the extended use case, labelled "«extend» [extension point name]"

Right half — Scenario selection rationale table:
Create a white table card titled "Scenario Selection Rationale":
Headers: "Scenario | Views Exercised | Quality Attribute"
Rows: [POPULATE FROM YOUR SCENARIO INVENTORY TABLE]
Use alternating row colours: white and #EAF2FB.

STEP 3 — INDIVIDUAL SCENARIO FRAMES (Row 2)
Create [N] frames in a horizontal row. Each frame:
- Width: [CANVAS WIDTH / N] px
- Height: 600px
- Frame title: "SC[N]: [SCENARIO NAME]"
- Frame background: alternating #1A3A5C (dark blue) and #1A4A3C (dark green) for visual differentiation

Inside each scenario frame, create three sections:

TOP SECTION — Scenario header card (white, 15% frame height):
"Actor: [ACTOR NAME]
Trigger: [TRIGGER DESCRIPTION]
Quality Attribute: [QUALITY ATTRIBUTE TESTED]
Precondition: [PRECONDITION]"

MIDDLE SECTION — Sequence flow (65% frame height):
Create a compact horizontal swimlane diagram:
- Swimlane headers: one per participating component, coloured by view origin:
  - Logical view components: header #4A7FB5 (blue)
  - Process (runtime service): header #4AB57A (green)
  - Physical (infra node): header #B5944A (amber)
- Draw lifelines as thin white dashed vertical lines
- Draw messages as white horizontal arrows between lifelines:
  - Solid arrow = synchronous
  - Dashed arrow = asynchronous (label with ⚡)
  - Label every arrow with the operation or event name
- Mark the critical path with a yellow (#FFD700) highlight behind the critical arrows
- If there is a failure path, show it as a red dashed arrow returning to the initiating actor labelled "⚠ [FAILURE NAME]"

BOTTOM SECTION — Cross-view trace card (20% frame height):
Create a small white card with dark text:
"Logical: [LIST LOGICAL ABSTRACTIONS INVOLVED]
Process: [LIST RUNTIME SERVICES]
Development: [LIST CODE MODULES]
Physical: [LIST NODES / INFRA]"

STEP 4 — ARCHITECTURE VALIDATION MATRIX (Row 3)
Create a wide frame (full canvas width) titled "Architecture Validation Matrix" with background #F0F4F8 (light grey-blue).

Inside, create a matrix table:
- Rows = architectural elements (components, services, nodes)
- Columns = scenario names: SC1, SC2, SC3... SC[N]
- Cell content: coloured dot — ✅ green fill if the element is exercised by that scenario, grey if not
- Row colour alternation: white and #E8F0F8

Below the matrix, add a text card titled "Coverage Gaps":
List any architectural elements with zero or only one scenario covering them. Format:
"⚠ [ELEMENT NAME] — only covered by [N] scenario(s). Consider adding a scenario that tests [SPECIFIC CONCERN]."
If there are no gaps: add a green card saying "✅ All architectural elements exercised by 2+ scenarios."

STEP 5 — CONNECTING LINES (cross-frame)
Add thin grey connector arrows from the Use Case Overview frame to each Scenario frame — one arrow per scenario connecting the corresponding use case oval to its scenario frame header. Label each arrow "detail →".

DO NOT include: class diagrams, package structures, source code, deployment node specs, or build pipeline details — those belong in the other four views. Do not combine multiple scenarios into one frame. Do not use placeholder scenario names — use the actual scenario names from the board context.
```

---

## Calibration Notes

- **Grid layout.** The explicit row/grid instruction is essential — without it Miro AI tends to stack everything in one frame or produce a linear list.
- **Cross-view trace card.** This is the most important element — it is what makes the +1 view *validate* the other four views. Emphasise in your context notes which logical, process, development, and physical elements each scenario touches.
- **Scenario frame count.** Optimal for Miro: 4–6 scenarios. More than 6 makes the grid illegible. If you have 8+ scenarios, split into two rows and adjust the Row 2 instruction.
- **Include decision points in scenarios.** Explicitly mention conditions in each scenario flow — "if payment fails", "when approval is required" — so Miro AI generates branching decision diamonds rather than flat linear step sequences. Vague scenarios produce generic step lists.
- **Mention parallel actions.** If steps within a scenario happen simultaneously (e.g., "while the notification service sends the confirmation, the analytics service records the event"), state this explicitly. Without it, Miro AI defaults to purely sequential flows.
- **Specify actor handoffs.** Name who does what at each transition — "Customer submits → API Gateway authenticates → Order Service processes" — so Miro AI creates distinct swimlanes with clear responsibility boundaries.
- **Failure paths.** Explicitly mention "red dashed arrow" — Miro AI will omit failure paths if not explicitly instructed to include them. Miro AI does not invent failure scenarios; if you do not mention them, they will not appear.
- **Start with the happy path.** Generate the main success flow per scenario first. Add failure paths, edge cases, and alternative flows in a second iteration — overcomplicating the first draft is the most common prompting error.
- **Use existing board content.** If you have scenario descriptions, use case lists, or flow notes as sticky notes on the board, select and attach them before running the prompt. Miro AI analyses the selected content and builds diagrams incorporating those specific details — more context means less hallucination.
- **Validation matrix.** This only works well if you pre-populate the element list. Add your element names to the board as a sticky note list before running the prompt.
- **Iterating.** After generation, refine one scenario at a time: "In scenario SC2, add an exception path for when the authentication service is unavailable." Never request multiple structural changes in a single prompt — Miro AI handles single targeted edits more reliably.
- **Simplifying.** If a scenario frame looks cluttered, select that section and prompt: "Simplify this scenario flow while maintaining the core logic and decision points." Do not try to fix layout and content in the same edit.
- **For complex scenario trees.** Consider using Miro's Doc format first to outline the full decision tree for a scenario with all variables and outcomes, then use that doc as context for the visual flowchart showing the main path and key decision points.
