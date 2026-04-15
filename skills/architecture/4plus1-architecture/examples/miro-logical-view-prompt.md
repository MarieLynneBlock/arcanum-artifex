# Miro Prompt — Logical View

## How to use this file

Copy the prompt below and paste it into Miro AI Sidekick. Replace every `[PLACEHOLDER]` with your system's actual values before running. Do NOT run the placeholder text — Miro AI will interpret it literally.

This prompt uses the RISEN framework: Role, Input, Steps, Expectation, Narrowing.

---

## Prompt Template

```
You are a senior software architect and UML diagram specialist creating a formal Logical View diagram for a software system architecture review. Your output will be added directly to an architecture documentation board.

CONTEXT FROM BOARD: [Select and attach your system context sticky notes or doc before submitting — include: system name, list of key domain abstractions with their responsibilities, and the package groupings you have identified]

Create the following on this Miro board in a single structured frame titled "Logical View — [SYSTEM NAME]":

STEP 1 — FRAME SETUP
Create one large outer frame titled "Logical View — [SYSTEM NAME]" with a dark navy (#0D1B2A) background. Divide the frame into three horizontal zones:
- Top zone (25% height): "Package Overview" label in white
- Middle zone (55% height): "Class Relationships" label in white  
- Bottom zone (20% height): "Architectural Mechanisms" label in white

STEP 2 — PACKAGE OVERVIEW (top zone)
Create [N] coloured rounded rectangles representing packages:
- Package 1: "[PACKAGE NAME]" — colour #2D6A9F (blue), white text, contains list of class names as a text block inside the rectangle
- Package 2: "[PACKAGE NAME]" — colour #2D9F6A (green), white text
- Package 3: "[PACKAGE NAME]" — colour #9F6A2D (amber), white text
[repeat for each package]
Connect packages with directional arrows:
- Solid dark arrow (→) = "uses / depends on"
- Label each arrow with the dependency type
- Arrows point from dependent package to dependency

STEP 3 — CLASS RELATIONSHIPS (middle zone)
Create white rounded rectangle cards for each of the following [N] classes:
[LIST EACH CLASS AS: "ClassName — [one-line responsibility]"]
Arrange in a left-to-right dependency flow. Connect with lines:
- Solid black line with filled diamond (◆) at source = composition
- Solid black line with open diamond (◇) at source = aggregation  
- Solid black arrow (→) = association / uses
- Dashed arrow (-->) = dependency
- Solid line with open triangle (▷) at target = inheritance
- Dashed line with open triangle (▷) at target = realisation
Label every connection with: relationship name AND multiplicity (e.g., "1" on source side, "*" on target side). Do not leave any connection unlabelled.

STEP 4 — STATE DIAGRAM (include only if [SYSTEM NAME] has stateful entities)
In the bottom-left of the middle zone, create a state diagram for [ENTITY NAME]:
- Black filled circle = initial state
- Double-circle = terminal state
- Rounded rectangles for states, coloured #E8F4F8
- Arrow between states labelled with: [event / guard condition]
States: [LIST STATE NAMES]
Transitions: [LIST AS: FROM STATE → TO STATE : trigger [guard]]

STEP 5 — ARCHITECTURAL MECHANISMS (bottom zone)
Create [N] yellow (#FFF3CD) sticky notes, one per mechanism:
- Sticky 1: "[MECHANISM NAME]: [one-sentence description of how it is applied]"
- Sticky 2: "[MECHANISM NAME]: [description]"
[repeat]
Arrange in a horizontal row.

STEP 6 — LEGEND
In the bottom-right corner of the frame, create a small white legend card titled "Legend" containing:
- ◆── Composition
- ◇── Aggregation  
- ──> Association
- --> Dependency
- ──▷ Inheritance
- --▷ Realisation
- Blue rectangle = Presentation package
- Green rectangle = Domain package
- Amber rectangle = Infrastructure package

DO NOT include: database schemas, deployment nodes, server configurations, API endpoint listings, or code-level method signatures. Do not add any elements outside the main frame.
```

---

## Calibration Notes

- **Specificity is mandatory.** Miro AI will default to a generic diagram if you do not name every class, every package, every connection.
- **Colour codes matter.** Use hex codes, not colour names — Miro's colour picker is more reliable with hex values.
- **Package zone sizing.** If you have more than 4 packages, increase the top zone to 35%.
- **State diagrams.** Only include if you have identified at least one stateful entity. If not, replace Step 4 with: "Create a text card in the bottom-left of the middle zone summarising the primary design pattern used (e.g., Repository Pattern, Observer, Strategy)."
- **Iterating.** After the initial generation, use the Miro AI edit function for one change at a time — e.g., "Add an inheritance arrow between [ClassA] and [ClassB]" rather than requesting multiple changes simultaneously.
