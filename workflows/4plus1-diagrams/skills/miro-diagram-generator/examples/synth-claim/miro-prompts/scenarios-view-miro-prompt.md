# Miro prompt — SynthClaim — Scenarios (+1) view

Paste into Miro AI Sidekick. Elements derived from `../05-scenarios-view.md`. This prompt produces (a) a use-case overview, (b) one frame per scenario, (c) a coverage matrix.

---

## Role

You are a senior solutions architect working in Miro AI. Your job is to produce the **Scenarios (+1) view** for SynthClaim — a unifying view showing how actors and components interact in seven key scenarios. Audience: all stakeholders.

## Input

**System:** SynthClaim.

**Scope:** Seven named scenarios, one overview diagram, and one coverage matrix. Scenarios listed below.

**Actors (7):**
Policyholder, Broker, Adjudicator, DPO, Auditor, SRE, Scheduler (+ Mainframe team, referenced).

**Scenarios (7, exact list):**
1. **S1 — Portal auto-approve** (happy) — Policyholder submits via portal, ML-classified auto-approve, decided and notified in < 10 min.
2. **S2 — Email human-review** (happy-ish) — Policyholder emails claim, OCR+classify, adjudicator decides.
3. **S3 — Broker submission** — Broker API submits on behalf of policyholder, mTLS-authenticated, routes to adjudicator.
4. **S4 — Classifier uncertainty** (edge) — Classifier confidence below threshold; routed to adjudicator; console shows low-confidence banner.
5. **S5 — Mainframe outage** (failure) — VPN / mainframe unavailable; lifecycle uses cached policy with staleness flag; parked claims for cache-misses; decisions queued for write-back; SRE paged.
6. **S6 — DSAR fulfilment** (regulatory) — DPO opens case; automated multi-store retrieval; manual ticket to mainframe; package delivered; audit logged.
7. **S7 — Model drift detected** (operational / AI governance) — Scheduled fairness eval breaches threshold; model reverted or threshold raised; incident logged for AI Act monitoring.

**Context on the board:** none assumed.

## Steps

### 1. Create the meta-frame (overview)

1. Create a frame titled **"Scenarios (+1) view — SynthClaim — Overview"**, approximately 2400 × 1400 px, landscape.
2. Place a legend (top-right, 280 × 220 px):
   - Stick figure = actor
   - Oval = scenario
   - Solid line = actor participates in scenario
   - Scenario colours: green = happy, amber = edge / operational, red = failure, purple = regulatory / AI governance
3. Place the **7 actors as stick figures** along the left edge of the frame, top-to-bottom: Policyholder, Broker, Adjudicator, DPO, Auditor, SRE, Scheduler.
4. In the centre, place the **7 scenarios as ovals** (colours per category):
   - S1 (green): Portal auto-approve
   - S2 (green): Email human-review
   - S3 (green): Broker submission
   - S4 (amber): Classifier uncertainty
   - S5 (red): Mainframe outage
   - S6 (purple): DSAR fulfilment
   - S7 (purple): Model drift detected
5. Draw **lines connecting each actor to the scenarios they participate in**:
   - Policyholder — S1, S2, S4, S6
   - Broker — S3
   - Adjudicator — S2, S3, S4, S7
   - DPO — S6
   - Auditor — S6, S7
   - SRE — S5, S7
   - Scheduler — S5, S7
6. Add a title at the top: **"SynthClaim — Scenarios view — Overview — v1.0 — 2026-04-18"**.

### 2. Create one frame per scenario (S1–S7)

For each scenario, create a separate frame titled **"Scenario [N] — [Scenario name]"** (approximately 2000 × 1100 px each). Inside each frame:

- **Scenario metadata block** (top-left, 400 × 160 px): category, trigger, actors, preconditions, postconditions, statutory / SLA notes where relevant.
- **Sequence diagram representation** of the scenario: arrange participants as vertical lifelines from left to right, with horizontal arrows between them representing interactions, numbered left-to-right / top-to-bottom.
- For failure / edge scenarios (S4, S5, S7), use **red arrows** for error paths.
- For async interactions (messages over event bus, notifications), use **dashed arrows**.
- For interactions that cross the on-prem / cloud boundary (especially in S5), use **thick blue arrows** and label "VPN".

Per-scenario essentials:
- **S1:** lifelines — Policyholder, Portal, API Edge, Intake, Docpipe, Classifier, Lifecycle, Mainframe, Decision, Audit. 12–15 interactions.
- **S2:** lifelines — Policyholder, Mail Gateway, Intake, Docpipe, Classifier, Lifecycle, Adjudicator (human), Console, Decision, Audit.
- **S3:** lifelines — Broker, API Gateway, Edge, Intake, Classifier, Lifecycle, Adjudicator, Decision.
- **S4:** lifelines similar to S2 but with explicit branch on "confidence < threshold"; annotate Adjudicator Console with "low-confidence banner required".
- **S5:** lifelines — HealthCheck, Lifecycle, Cache, Mainframe, SRE, Decision, RetryQueue. Show timeout arrows (X-mark at end), SRE paging, recovery and replay.
- **S6:** lifelines — Policyholder, DPO, DSAR, Claims DB, Doc Store, Audit, Mainframe (manual). Use a **par** block / parallel-retrieval swimlane for the three automated fetches.
- **S7:** lifelines — Scheduler, Eval suite, Data Science (human), Registry, Classifier, SRE, Adjudicator queue, Audit, Auditor.

### 3. Create the coverage matrix frame

1. Create a frame titled **"Coverage matrix — Scenarios × Components"**, approximately 1800 × 1100 px.
2. Inside, place a grid of sticky notes (1-cell header row + 1-cell header column + body):
   - **Rows** = components (17 rows, from the logical view): Claims Portal, Adjudicator Console, API Edge, Intake, Docpipe, Classifier, Lifecycle, Decision, DSAR, Audit, Claims DB, Doc Store, Feature Store, Model Registry, Mainframe, Mail Gateway, Broker API
   - **Columns** = scenarios S1–S7
   - **Body cells**: place a small green tick sticky (✓) where the scenario exercises the component (per the matrix in `../05-scenarios-view.md`). Leave other cells empty.
3. Add a legend note below the matrix: "✓ = component exercised in scenario. Empty = not touched. No empty rows → full coverage."

## Expectation

You will produce exactly **9 frames**:
- 1 overview frame (actors ↔ scenarios)
- 7 scenario-detail frames (S1–S7)
- 1 coverage-matrix frame

Overview frame:
- 1 legend (4 category colours + shape legend)
- 7 stick-figure actors
- 7 colour-coded scenario ovals
- ~17 actor-to-scenario lines

Each scenario frame:
- 1 metadata block (top-left)
- 1 title block
- ~8–10 vertical lifelines
- ~10–15 numbered interaction arrows (solid / dashed / red / blue thick as appropriate)
- Optional notes annotating key architectural properties (e.g. "low-confidence banner required", "decision durable regardless of mainframe availability")

Coverage-matrix frame:
- 1 title
- Grid of 17 rows × 7 columns
- ~75 tick stickies (per the matrix in the accompanying doc)
- 1 note below explaining the legend

All text readable at default zoom. Scenario frames are linkable from the overview frame (Miro supports frame-to-frame links) — set these up if Miro AI allows.

## Narrowing

Do **NOT** include:
- Full runtime detail from the process view (scenarios are concrete instantiations, not the general flows).
- Deployment topology (physical view territory).
- Repository / module maps (development view territory).
- More than 7 scenarios; if more scenarios are added in future, create a follow-up board.
- Decorative elements or logos.
- Colour variation within a category (all green scenarios exactly the same green, etc.).
- Sticky notes of any colour other than green for the coverage matrix.
