# Miro prompt — SynthClaim — Full board (all 5 views)

Paste into Miro AI Sidekick to generate the **entire 4+1 board** in one run. Large prompts — Miro AI may chunk the work. If it does, accept and iterate.

---

## Role

You are a senior solutions architect working in Miro AI. You are creating a complete **4+1 architectural documentation board** for SynthClaim. The final board will have **5 view frames + 7 scenario frames + 1 coverage-matrix frame + 1 cover frame**. Audience: cross-functional steering committee.

## Input

See the individual view prompts (`logical-view-prompt.md`, `process-view-prompt.md`, `development-view-prompt.md`, `physical-view-prompt.md`, `scenarios-view-prompt.md`) for the exact element and relationship lists per view. This prompt orchestrates them into one coherent board and adds a **cover frame** plus **navigation links** between frames.

## Steps

1. Create a **Cover frame** at position (0, 0), approximately 1800 × 1000 px. Contents:
   - Large title: **"SynthClaim — Architectural documentation (4+1)"**
   - Subtitle: "v1.0 — 2026-04-18 — Cross-functional audience"
   - Overview paragraph (4–6 lines) summarising SynthClaim — "a hybrid cloud claims-processing platform that ingests insurance claims through portal, email and broker API, OCR-and-ML-classifies them, and routes to auto-approval or human adjudicator review. Mainframe remains system of record; all personal data in UK/EU. Regulatory context: GDPR, UK FCA, EU AI Act (high-risk classifier)."
   - A numbered list of frames on the board, each being a **clickable frame-link** — "Frame 1: Logical view", "Frame 2: Process view", "Frame 3: Development view", "Frame 4: Physical view", "Frame 5: Scenarios overview", "Frame 6–12: Scenarios S1–S7", "Frame 13: Coverage matrix".
   - Bottom: "Read in any order; the Scenarios overview frame is the best entry point for non-architects."

2. Create **Frame 1 — Logical view**. Follow the full `logical-view-prompt.md` spec.

3. Create **Frame 2 — Process view (Flow 1: Portal auto-approve)**. Follow `process-view-prompt.md`. Add a note at the bottom: "See frames 2a–2d for the other process flows (email, broker, uncertainty, mainframe-outage, DSAR)." Create these additional frames on a reduced-detail basis if time permits.

4. Create **Frame 3 — Development view**. Follow `development-view-prompt.md`.

5. Create **Frame 4 — Physical view**. Follow `physical-view-prompt.md`.

6. Create **Frame 5 — Scenarios overview**, and Frames 6–12 for individual scenarios S1–S7, and Frame 13 for the coverage matrix. Follow `scenarios-view-prompt.md` for all these.

7. Arrange frames in the board **in reading order left to right, top to bottom**, with the Cover frame first. Use Miro's "Add connector between frames" capability to create a reading-order arrow from each frame to the next at its top-right corner.

8. At each frame's top-left, add a small "Back to Cover" link (a frame link back to the Cover frame).

9. Apply **consistent colour coding across all frames**:
   - Internal subsystems — pale blue
   - External systems — grey
   - Human actors — stick figures
   - Data stores — dark blue cylinders
   - On-prem zone — grey dashed rectangle
   - Cloud zone — orange rectangle
   - Regulated components — red "(regulated)" badge
   - Happy-path / sequence flow — solid black arrows
   - Async / message flow — dashed arrows
   - Management / replication — dotted or thin arrows
   - Failure / error paths — red arrows
   - VPN / hybrid-integration paths — thick blue arrows

10. Add a **board-level sticker** (top-right of the whole canvas) showing: "Version 1.0 — 2026-04-18 — Owner: Solutions architecture — Status: Draft for steering committee review".

## Expectation

The final board must contain exactly:
- **1 Cover frame** with title, subtitle, overview, and frame index (with clickable links)
- **1 Logical-view frame** as per `logical-view-prompt.md`
- **1 primary Process-view frame** (Flow 1) + up to 4 additional reduced-detail process frames for the other flows
- **1 Development-view frame** as per `development-view-prompt.md`
- **1 Physical-view frame** as per `physical-view-prompt.md`
- **1 Scenarios-overview frame** + **7 scenario-detail frames** (S1–S7) + **1 coverage-matrix frame** as per `scenarios-view-prompt.md`
- **Reading-order connectors** between consecutive frames
- **"Back to Cover" links** on every non-cover frame
- **Consistent colour and shape semantics** across all frames
- **1 board-level version-and-owner sticker**

## Narrowing

Do **NOT**:
- Invent elements not listed in the individual view prompts.
- Introduce colour semantics beyond the 12 listed in Step 9.
- Merge the views into a single mega-diagram — the 4+1 discipline is about **separated views** each answering a specific question.
- Include any personal data, real names, real customer information, or real broker/vendor names — this is synthetic.
- Cross-reference frames beyond the explicit frame-links — e.g. don't draw an arrow from the logical view's "Lifecycle" box to the physical view's "ECS task" — they reference each other semantically, not visually.
- Attempt the full board in one pass if Miro rate-limits; deliver frame-by-frame and notify the user.
