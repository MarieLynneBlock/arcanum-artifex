# Miro Prompt — Development View

## How to use this file

Copy the prompt below, replace all `[PLACEHOLDER]` values, and paste into Miro AI Sidekick. Attach your module inventory table and dependency rules doc from the board as context.

---

## Prompt Template

```
You are a software architect and engineering manager creating a formal Development View (Implementation View) diagram for use in an architecture review and developer onboarding documentation. The audience is developers, engineering team leads, and DevSecOps engineers.

CONTEXT FROM BOARD: [Select and attach: module ownership table, repository structure notes, dependency rules doc, and build pipeline description from your board]

Create the following on this Miro board in a structured frame titled "Development View — [SYSTEM NAME]":

STEP 1 — FRAME SETUP
Create one large outer frame titled "Development View — [SYSTEM NAME]" with background #FAFAFA (near white). Divide into three vertical columns:
- Left column (30% width): "Repository Structure"
- Centre column (40% width): "Component & Package Diagram"
- Right column (30% width): "Team Ownership & Build Pipeline"

STEP 2 — REPOSITORY STRUCTURE (left column)
Create a file tree visualisation using:
- Folder nodes: grey rounded rectangles (#E8E8E8), 200px wide, 40px tall, left-aligned text with folder icon prefix (📁)
- File nodes: white rectangles, 180px wide, 30px tall, indented 20px from parent folder, with file icon prefix (📄)
Structure the tree to show:
📁 / (root)
  📁 services/
    📁 [SERVICE 1 NAME]/ — colour border: #2D6A9F (blue)
    📁 [SERVICE 2 NAME]/ — colour border: #2D6A9F (blue)
    [add one per service]
  📁 libs/
    📁 [LIB 1 NAME]/ — colour border: #2D9F6A (green)
    [add one per shared library]
  📁 infra/ — colour border: #9F6A2D (amber)
  📁 docs/ — colour border: #888888 (grey)
Connect parent folders to child folders with grey vertical lines.
Add a colour legend below the tree:
- Blue border = deployable service
- Green border = shared library
- Amber border = infrastructure
- Grey border = documentation

STEP 3 — COMPONENT & PACKAGE DIAGRAM (centre column)
Create an architectural layers stack:
Layer 1 (top): Rounded rectangle, background #D6E8F7 (light blue), label "Presentation / API Layer"
Layer 2: Rounded rectangle, background #D6F0E0 (light green), label "Application Layer"
Layer 3: Rounded rectangle, background #FFF8E1 (light yellow), label "Domain Layer"
Layer 4 (bottom): Rounded rectangle, background #F3E8D6 (light amber), label "Infrastructure Layer"
Each layer rectangle is 600px wide and [adjust height per number of components in that layer]px tall.

Inside each layer, place component cards:
- White rounded rectangle, 150px wide, 60px tall
- Bold component name on top line
- Italic owning team name on second line (smaller font)
- Small coloured dot in top-right corner = team colour

Place components in layers as follows:
Presentation Layer: [LIST COMPONENTS]
Application Layer: [LIST COMPONENTS]
Domain Layer: [LIST COMPONENTS]
Infrastructure Layer: [LIST COMPONENTS]

Draw dependency arrows between components:
- SOLID grey arrow pointing DOWNWARD = allowed dependency (layer rule respected)
- RED dashed arrow pointing UPWARD = VIOLATION — label "⚠ Violation: [reason]"
- Solid arrow with dashed border = interface dependency (component depends on interface, not concrete class)

Label each arrow with the dependency type: "uses", "implements", "imports", "injects"

STEP 4 — PACKAGE DIAGRAM INSET
In the bottom half of the centre column, create a separate inset frame titled "Package Dependencies":
Create [N] hexagonal or rounded-square shapes, one per package:
- Package name in bold
- Owning team in smaller text
- Colour-code by team: [ASSIGN ONE COLOUR PER TEAM]
Connect with directed arrows:
- Solid black arrow = compile-time dependency
- Dashed arrow = runtime-only dependency
- Arrow label = specific package/module imported
Add a text card: "Dependency Rule: [STATE YOUR DEPENDENCY DIRECTION RULE — e.g., 'Services → Libs allowed. Libs → Services FORBIDDEN. No circular dependencies.']"

STEP 5 — TEAM OWNERSHIP (right column, top half)
Create a table with columns: "Module | Team | Type | Key Dependencies"
Use alternating row colours: white and #F5F5F5
[POPULATE WITH YOUR MODULE OWNERSHIP DATA]
Add a colour swatch next to each team name matching the team colour used in Step 3.

STEP 6 — BUILD PIPELINE (right column, bottom half)
Create a vertical flowchart showing the CI/CD pipeline stages:
- Each stage: rounded rectangle, 200px wide, 50px tall
- Stage background colours:
  - Source stages: #E3F2FD (light blue)
  - Test stages: #E8F5E9 (light green)
  - Build stages: #FFF8E1 (light yellow)
  - Deploy stages: #FCE4EC (light pink)
  - Failure exits: #FFEBEE (red-tinted)
Stages in order (adjust to your pipeline):
1. [Source Push / PR opened]
2. [Lint + Static Analysis] → failure exit: "PR blocked"
3. [Unit Tests] → failure exit: "PR blocked"
4. [Build Container Image]
5. [Integration Tests] → failure exit: "Deploy halted"
6. [Push to Registry]
7. [Deploy to Staging]
8. [Smoke Tests] → failure exit: "Rollback triggered"
9. [Deploy to Production]
Connect stages with solid black downward arrows. Connect failure exits with red horizontal arrows pointing right with label "FAIL →".

STEP 7 — CODE QUALITY STANDARDS CARD
Below the pipeline, add a white card titled "Code Quality Gates":
- Coverage threshold: [X]% unit, [Y]% integration
- Linting: [TOOL NAME]
- SAST: [TOOL NAME]
- Required approvals: [N] reviewers
- Secret scanning: [enabled/tool name]

DO NOT include: deployment infrastructure, server specifications, runtime processes, or business domain logic. Do not create diagram elements that are not explicitly listed above. Do not add decorative elements. Keep all text readable at 100% zoom — minimum 12px font equivalent.
```

---

## Calibration Notes

- **Layer colours are intentional.** The blue-green-yellow-amber stack is a common convention for layered architecture. Keep these; they communicate hierarchy immediately.
- **Violation arrows.** If you have no dependency violations, omit the violation arrow from the legend but keep the instruction in the prompt — it ensures Miro AI doesn't invent violations.
- **Team colour assignment.** Assign hex codes per team before running the prompt. E.g., "Order Squad: #2D6A9F, Payments Squad: #9F2D2D". Miro AI needs explicit hex values to be consistent.
- **Build pipeline.** Keep stages to ≤ 9. If your pipeline is more complex, summarise to the most architecturally significant gates.
- **Use existing board content.** If you have module ownership tables, repository structure notes, or build pipeline descriptions as text or sticky notes on the board, select and attach them before running. Miro AI analyses selected content and incorporates those specific details.
- **Include decision points in the pipeline.** Explicitly mention conditions at quality gates — "if coverage < 80%, block merge" or "if security scan finds critical, halt deploy" — so Miro AI generates diamond-shaped decision nodes rather than a flat linear flow.
- **Iterating.** After generation, refine one section at a time. "Add a red violation arrow from [Component X] in the Presentation layer to [Component Y] in the Domain layer" is more reliable than requesting multiple changes. If a section looks cluttered, select it and prompt: "Simplify this portion while maintaining the core logic."
- **Start simple.** For the component diagram, start with the happy-path dependency structure. Add violation arrows, optional dependencies, and edge-case integrations in subsequent iterations.
