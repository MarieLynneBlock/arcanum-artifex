# Miro prompt — [System name] — Full 4+1 board

Paste into Miro AI Sidekick to generate the complete 4+1 board. Large prompts may be chunked by Miro AI; if that happens, create the board frame-by-frame in the order below.

---

## Role

You are a senior [solutions architect / systems analyst / business architect] working in Miro AI. You are creating a complete **4+1 architectural documentation board** for **[system name]**. The board will be reviewed by **[audience — developers / cross-functional product team / executive steering committee]**.

## Input

**System under documentation:** [System name] — [one-line description].

**Source prompts to apply:**
- `logical-view-miro-prompt.md`
- `process-view-miro-prompt.md`
- `development-view-miro-prompt.md`
- `physical-view-miro-prompt.md`
- `scenarios-view-miro-prompt.md`

**Board-level context:** [version, owner, review status, constraints, or "none"].

## Steps

Perform these steps in order. Do not merge separate views into one diagram.

1. Create a **Cover frame** titled **"[System name] — Architectural documentation (4+1)"**, sized approximately [width × height]. Include:
   - System name and one-line purpose
   - Audience
   - Version / owner / review status
   - Frame index with links to each view frame
   - Short reading guidance for the target audience
2. Create **Frame 1 — Logical view**. Follow `logical-view-miro-prompt.md` exactly.
3. Create **Frame 2 — Process view**. Follow `process-view-miro-prompt.md` exactly. If the process view contains multiple major flows, create one primary process frame plus additional focused process frames.
4. Create **Frame 3 — Development view**. Follow `development-view-miro-prompt.md` exactly.
5. Create **Frame 4 — Physical view**. Follow `physical-view-miro-prompt.md` exactly.
6. Create **Frame 5 — Scenarios overview** and any scenario-detail or coverage-matrix frames required by `scenarios-view-miro-prompt.md`.
7. Arrange frames in reading order from left to right, top to bottom, with the Cover frame first.
8. Add reading-order connectors between consecutive frames.
9. Add a **Back to Cover** link at the top-left of every non-cover frame.
10. Add a board-level version / owner / status note in the top-right of the overall canvas.

## Expectation

The final Miro board must contain exactly:
- **1 Cover frame** with title, overview, audience, version / owner / status, and frame index
- **1 Logical-view frame** from `logical-view-miro-prompt.md`
- **[N] Process-view frame(s)** from `process-view-miro-prompt.md`
- **1 Development-view frame** from `development-view-miro-prompt.md`
- **1 Physical-view frame** from `physical-view-miro-prompt.md`
- **[N] Scenarios frame(s)** from `scenarios-view-miro-prompt.md`
- Reading-order connectors between frames
- Back-to-cover links on every non-cover frame
- Consistent shape, colour, arrow, and legend semantics from `references/notation-miro.md`

## Narrowing

Do **NOT**:
- Invent elements not listed in the individual view prompts.
- Merge all views into a single mega-diagram.
- Draw cross-frame implementation arrows between views; use links and labels instead.
- Introduce colour, shape, or arrow semantics outside `references/notation-miro.md` and the individual view prompts.
- Include personal data, real names, production secrets, customer data, or vendor-confidential information.
- Continue in one pass if Miro AI chunks or rate-limits the request; create frames incrementally instead.
