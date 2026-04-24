# Miro Prompt — Full 4+1 Architecture Board

## When to use this prompt

Use this when you want **all five views on a single Miro board** in a structured layout — ideal for architecture reviews, stakeholder presentations, and team onboarding. It creates a navigable board where all views are visible at a glance and cross-referenced.

For deep per-view detail, use the individual view prompts in this folder instead. The full board prompt optimises for orientation and cross-view navigation, trading some detail for coherence.

---

## Pre-flight Checklist

Before running this prompt, prepare the following on your Miro board as sticky notes or a Doc:

- [ ] System name and 2-sentence description
- [ ] List of 8–15 key domain abstractions with one-line responsibilities
- [ ] Package/subsystem groupings (3–6 packages)
- [ ] List of runtime services/processes with concurrency model
- [ ] Primary communication channels (sync/async) between services
- [ ] Repository structure (monorepo or polyrepo — top 2 levels)
- [ ] Module ownership table (module → team)
- [ ] Infrastructure platform and region
- [ ] List of 5–8 scenarios with actor and trigger

Attach ALL of the above as board context when running the prompt. More context = less hallucination.

---

## Prompt Template

```
You are a senior software architect producing a complete 4+1 architectural view model board for a formal architecture review. The board must be usable by five different stakeholder groups: end-users/analysts, developers, system integrators, infrastructure engineers, and project managers. Each view must be clearly labelled, self-contained, and visually distinct from the others.

CONTEXT FROM BOARD: [ATTACH ALL PRE-FLIGHT ITEMS LISTED ABOVE]

Create the following full-board layout. The board must have a top navigation banner, five view frames arranged in a consistent grid, and a cross-reference connector layer.

═══════════════════════════════════════════════════════
BOARD LAYOUT (top to bottom, left to right)
═══════════════════════════════════════════════════════

ROW 0 — NAVIGATION BANNER (full board width, 80px tall)
Create a full-width dark rectangle (#0D1B2A) as a header banner:
- Left: System name "[SYSTEM NAME] — 4+1 Architecture Views" in white bold 20px text
- Right: Five coloured pill-shaped labels side by side:
  [Logical #2D6A9F] [Process #2D9F6A] [Development #9F6A2D] [Physical #6A2D9F] [Scenarios #9F2D6A]
These pills act as a visual key — the same colours will appear on each view frame.

═══════════════════════════════════════════════════════

ROW 1 — FOUR MAIN VIEWS (arranged 2×2 grid)
Each frame is the same size: [CANVAS WIDTH/2 - 30]px wide × 700px tall.

FRAME 1 (top-left): LOGICAL VIEW
Frame background: #EBF3FB. Frame border: 3px solid #2D6A9F (blue). Frame title: "🔷 Logical View — Functional Structure" in #2D6A9F.
Inside this frame, create:
A — Package overview (top 30%):
[N] coloured rounded rectangles, one per package:
- Package "[PACKAGE 1]": #2D6A9F background, white text, 150px wide, containing class names as bullet list
- Package "[PACKAGE 2]": #3A7FC1 background
[repeat for each package]
Connect with directed arrows, labelled with dependency type.

B — Class relationship diagram (bottom 70%):
[N] white rounded rectangle cards for key classes:
- Each card: bold class name + italic one-line responsibility
- Connect with typed arrows using correct UML notation:
  ◆── Composition | ◇── Aggregation | ──> Association | --> Dependency | ──▷ Inheritance | --▷ Realisation
- Label every arrow with relationship name and multiplicity.

═══════════════════════════════════════

FRAME 2 (top-right): PROCESS VIEW
Frame background: #EBF7F1. Frame border: 3px solid #2D9F6A (green). Frame title: "🔶 Process View — Runtime Behaviour" in #2D9F6A.
Inside this frame, create:
A — Swimlane sequence diagram (left 65%):
[N] vertical swimlanes, one per runtime service:
- Swimlane headers: matching service colours (see process list in context)
- Vertical dashed lifelines in #CCCCCC
- Horizontal arrows:
  → Solid black = synchronous call (label: operation name)
  ⚡ → Orange solid = async event (label: event name with ⚡ prefix)
  --> Grey dashed = return value
Show the [PRIMARY BUSINESS SCENARIO NAME] end-to-end flow.

B — Failure annotations (right 35%):
[N] red (#FFEBEE border, red text) sticky cards, one per failure scenario:
"⚠ [FAILURE]: [response behaviour]"

═══════════════════════════════════════

FRAME 3 (bottom-left): DEVELOPMENT VIEW
Frame background: #FEF9EB. Frame border: 3px solid #9F6A2D (amber). Frame title: "🔸 Development View — Code Organisation" in #9F6A2D.
Inside this frame, create:
A — Layered architecture stack (left 50%):
Four horizontal coloured layers from top to bottom:
Layer 1 — "Presentation": #D6E8F7 background
Layer 2 — "Application": #D6F0E0 background
Layer 3 — "Domain": #FFF8E1 background
Layer 4 — "Infrastructure": #F3E8D6 background
Place component cards (white, rounded) inside each layer. Label each: "[COMPONENT NAME] — [TEAM]"
Draw dependency arrows pointing downward (allowed) or flag upward arrows as red violations.

B — Team ownership table (right 50%):
Table with: Module | Team | Type
[POPULATE FROM MODULE OWNERSHIP DATA]
Add a coloured team legend below the table.

═══════════════════════════════════════

FRAME 4 (bottom-right): PHYSICAL VIEW
Frame background: #0D1B2A (dark navy — intentionally dark). Frame border: 3px solid #6A2D9F (purple). Frame title: "🔹 Physical View — Deployment Topology" in #6A2D9F white text.
Inside this frame (all text white unless inside a white card):
Create nested infrastructure zones:
OUTER: Cloud provider boundary (dashed white border): "☁ [CLOUD PROVIDER] — [REGION]"
INNER: VPC boundary (solid white border, label with CIDR)
  ├── Public Subnet (dashed border, label): [ALB] [NAT Gateway]
  ├── App Tier Subnet (dashed border, label): [Container platform with [N] service boxes]
  └── Data Tier Subnet (dashed border, label): [Database] [Cache] [Message Broker]
Add [CDN] above the cloud boundary connected by HTTPS arrow.
Draw connection arrows with semantic colours:
- White → HTTPS
- Green → Database TCP
- Orange → Kafka/MQ
- Cyan → Cache
All arrows labelled with protocol and port.

═══════════════════════════════════════

ROW 2 — SCENARIOS VIEW (full board width)

FRAME 5 (full width): SCENARIOS VIEW
Frame background: #F9EBF5. Frame border: 3px solid #9F2D6A (pink). Frame title: "⬟ Scenarios (+1) — Architecture Validation".
Inside this frame, create a horizontal layout with [N+1] sections:

LEFT SECTION (25% width): Use Case Diagram
System boundary rectangle (dashed border, label "«system» [SYSTEM NAME]")
[N] use case ovals inside: one per scenario, colour #D4A0C0
[N] actor stick figures outside (left = primary, right = secondary)
Connect actors to use cases with solid lines.

RIGHT SECTIONS ([75/N]% width each): One per scenario
Each scenario section:
Header card (dark #9F2D6A background, white text): "SC[N]: [SCENARIO NAME]"
Flow card (white, compact):
"Actor → [STEP 1] → [STEP 2] → [STEP 3]... → [OUTCOME]
⚠ Failure: [FAILURE CASE]"
Cross-view trace card (light purple #F3E8F7, dark text, small font):
"L: [Logical elements] | P: [Process services] | D: [Dev modules] | Phy: [Nodes]"

═══════════════════════════════════════════════════════
CROSS-FRAME CONNECTORS (add after all frames are created)
═══════════════════════════════════════════════════════
Add thin dashed grey connector lines between frames to show cross-view relationships:
- Logical Frame → Development Frame: grey dashed line labelled "abstractions realised in →"
- Process Frame → Physical Frame: grey dashed line labelled "processes deployed on →"
- Scenarios Frame → all four view frames: grey dashed lines labelled "exercises →"
These connectors must run BETWEEN frames, not through them.

═══════════════════════════════════════════════════════
GLOBAL LEGEND (bottom-right corner, outside all frames)
═══════════════════════════════════════════════════════
Create a white card titled "4+1 View Guide":
🔷 Logical — what the system does (for: analysts, users)
🔶 Process — how it runs (for: integrators, SRE)
🔸 Development — how it's built (for: developers, managers)
🔹 Physical — where it runs (for: infra, security)
⬟ Scenarios — validates all views (for: everyone)

DO NOT include: real personal data, real IP addresses, real credentials, generic placeholder names (use actual system data from context), or decorative clip art. Do not merge any two view frames into one. Do not place any connector arrows THROUGH frames — route them around or between frames. Maintain the exact colour coding specified — these are semantic, not aesthetic choices.
```

---

## Calibration Notes

- **This prompt produces a complex board.** Expect Miro AI to take longer than for individual view prompts. If it times out, run each view frame separately using the individual view prompts.
- **Context is everything.** The more specific your attached board context, the less Miro AI will fill gaps with generic content. Run the pre-flight checklist before starting. Select and attach existing board content (sticky notes, docs, brainstorming output) — Miro AI analyses the selected content and incorporates those specific details.
- **Start with the happy path.** Generate the main flow per view first. Add failure paths and exception handling in a second pass — overcomplicating the first draft is the most common prompting error.
- **Iteration order.** If iterating, start with the frame that has the most stakeholder visibility (typically the Scenarios frame or Physical frame), not the Logical frame. Make one structural change per iteration — Miro AI handles single targeted edits more reliably than multi-change requests.
- **Cross-frame connectors.** These are the hardest part for Miro AI. If they are wrong or missing, add them manually — they take 5 minutes to draw by hand and are not worth fighting with AI generation.
- **Colour consistency.** The five frame border colours (blue, green, amber, purple, pink) are non-negotiable — they are the visual architecture of the board itself. If Miro AI deviates, edit frame borders manually.
- **Decision points matter.** Explicitly include conditions ("if deployment fails", "when approval is needed") and handoff points ("Ops triages → Dev fixes"). Without these, Miro AI produces overly linear diagrams.
- **For very complex boards.** Consider using Miro's Doc format first to outline the full architecture with all variables and outcomes, then use that doc as context input for this board prompt.
