# Miro prompt — SynthClaim — Logical view

Paste the block below into Miro AI Sidekick. The system context and elements are taken directly from `../01-logical-view.md` — keep both in sync when the architecture changes.

---

## Role

You are a senior solutions architect working in Miro AI. Your job is to create a **Logical view** diagram for the system **SynthClaim** on a clean Miro frame. The diagram will be reviewed by a cross-functional steering committee including technology, compliance, claims operations, and a business sponsor — draw accordingly (plain-English labels, no implementation-specific jargon unless essential).

## Input

**System under documentation:** SynthClaim — a hybrid cloud claims-processing platform that ingests insurance claims through portal, email, and broker API; OCRs and classifies them with ML; routes to auto-approval or human adjudicator review; and writes decisions back to the on-premises policy mainframe.

**Scope of this view:** Logical decomposition — what components exist and how they relate. Not where they run (that's the physical view), not the sequence of calls (that's the process view), not the code layout (that's the development view).

**Key elements to include (exact list):**

Human actors (3):
- Policyholder — end user who submits and tracks claims
- Adjudicator — internal role reviewing claims requiring human judgement
- Auditor / DPO — handles regulator inquiries and GDPR data-subject requests

External systems (4):
- Broker API — third-party brokers submitting claims
- Corporate mail gateway — handles email-based intake
- Post-room scan service — digitises paper mail (upstream of mail gateway)
- Policy Mainframe — on-premises IBM Z system of record for policy, customer, and payment

Internal subsystems (9):
- Claims Portal — React SPA for policyholders
- Adjudicator Console — React SPA for adjudicators
- API Edge — Kong policy enforcement point
- Claim Intake Service — normalises multi-channel submissions
- Document Processing Pipeline — OCR, extraction, classification orchestration
- Claim Classifier — ML service (auto-approve / review / refer)
- Claims Lifecycle Service — workflow engine and mainframe integration
- Decision Service — records and emits decisions
- Data Subject Rights Service — GDPR Art. 15/17/20 handler
- Audit Log — append-only event store

Data stores (4):
- Claims Datastore — PostgreSQL
- Document Store — S3 encrypted
- Feature Store — S3 + Athena
- Model Registry — SageMaker

**Key relationships to depict (exact list):**
1. Policyholder → Claims Portal: uses (HTTPS)
2. Adjudicator → Adjudicator Console: reviews and decides (HTTPS)
3. Auditor / DPO → DSAR Service: issues data-subject requests (HTTPS)
4. Broker → API Edge: submits claim (REST/mTLS)
5. Mail Gateway → Intake: forwards email (webhook)
6. Scan Service → Mail Gateway: delivers scanned paper
7. Portal → API Edge: JSON/HTTPS
8. Console → API Edge: JSON/HTTPS
9. API Edge → Intake / Lifecycle / DSAR: routes
10. Intake → DocPipe: submits docs
11. DocPipe → Classifier: requests classification
12. DocPipe → Document Store: reads/writes
13. Classifier → Feature Store: reads features
14. Classifier → Model Registry: loads model
15. Intake → Lifecycle: publishes ClaimSubmitted (async)
16. Lifecycle → Claims DB: reads/writes
17. Lifecycle → Decision: requests decision recording
18. Decision → Claims DB: writes
19. Decision → Audit: publishes DecisionRecorded (async)
20. Lifecycle → Mainframe: reads policy; writes decision (SOAP/VPN)
21. DSAR → Claims DB, Document Store, Audit: reads across stores

**Context already on the board:** none assumed. If the user has placed a system-context document or prior sticky notes, read them first and reconcile.

## Steps

Perform these steps in order.

1. Create a new frame titled **"Logical view — SynthClaim"**, approximately 2400 × 1400 px. Landscape orientation.
2. Place a legend in the **top-right corner** (280 × 220 px) listing:
   - **Blue rounded rectangle** = internal subsystem
   - **Dark blue cylinder** = data store
   - **Grey rectangle with dashed border** = external system
   - **Grey stick figure** = human actor
   - **Solid arrow** = synchronous call
   - **Dashed arrow** = asynchronous message / event
   - **Dotted arrow** = data-access reference
3. Create a large **System_Boundary** as a rounded rectangle labelled "SynthClaim" occupying the centre of the frame (~1600 × 900 px). Internal subsystems and data stores go inside; actors and external systems go outside.
4. Place the **three human actors** as stick-figure icons along the **top edge outside the boundary**, left-to-right: Policyholder, Adjudicator, Auditor/DPO. Space evenly.
5. Place the **four external systems** as grey rectangles with dashed border:
   - Broker API — top-right outside the boundary
   - Corporate mail gateway — left outside the boundary (mid-height)
   - Post-room scan service — further left of mail gateway (daisy-chain indicator)
   - Policy Mainframe — **bottom outside the boundary** (visual cue that it's on-prem, separate tier)
6. Inside the SynthClaim boundary, place the **nine internal subsystems** as blue rounded rectangles, laid out left-to-right and top-to-bottom by flow position:
   - Top row (left to right): Claims Portal, Adjudicator Console
   - Second row: API Edge (centred)
   - Third row (left to right): Claim Intake, Document Processing Pipeline, Claim Classifier, Claims Lifecycle
   - Fourth row: Decision, Data Subject Rights Service
   - Bottom row: Audit Log (full-width)
7. Place the **four data stores** as dark-blue cylinders, positioned beside the subsystems that primarily own them:
   - Claims Datastore — beside Claims Lifecycle
   - Document Store — beside Document Processing Pipeline
   - Feature Store — beside Claim Classifier
   - Model Registry — beside Claim Classifier (slightly lower)
8. Draw the **21 relationship arrows** listed in the Input section. Use:
   - **Solid** for synchronous relationships (1, 2, 3, 4, 7, 8, 9, 10, 11, 13, 14, 17, 20, 21)
   - **Dashed** for asynchronous / event relationships (5, 15, 19)
   - **Dotted** for data-access references (12, 16, 18) — note: 12, 16, 18 can also be solid if readability suffers; preserve the dashed / dotted distinction primarily for 15 and 19.
9. Label every arrow with its purpose (e.g. "uses", "reads policy", "publishes ClaimSubmitted").
10. Ensure the mainframe arrow (20) is visually prominent — draw it with a **thick** line and label it "SOAP/XML over site-to-site VPN" to signal the hybrid-cloud boundary.
11. Apply colour consistency: all internal subsystems the same shade of blue; all data stores the same darker blue; all externals the same grey.
12. Add a title at the top of the frame: **"SynthClaim — Logical view — v1.0 — 2026-04-18"**.
13. Align all elements to the Miro grid; minimise arrow crossings.

## Expectation

The final Miro frame must contain exactly:
- **1 frame** titled "Logical view — SynthClaim"
- **1 title text block** with version and date
- **1 legend** (top-right, 7 entries)
- **1 System_Boundary** rounded rectangle labelled "SynthClaim"
- **3 human-actor stick figures** with labels
- **4 external-system rectangles** (grey, dashed border)
- **9 internal-subsystem rounded rectangles** (blue)
- **4 data-store cylinders** (dark blue)
- **21 labelled arrows** with correct style (solid / dashed / dotted) per the list
- All text readable at default Miro zoom; every arrow clearly labelled.

## Narrowing

Do **NOT** include:
- Deployment details (VPCs, subnets, AZs, servers, containers) — that's the physical view.
- Runtime sequence (who calls whom in what order, timing) — that's the process view.
- Code-level structure (repos, modules, libraries) — that's the development view.
- Internal fields / schemas of any component — out of scope for a container view.
- Decorative elements (logos, icons beyond the legend shapes, marketing imagery).
- Unlabelled arrows.
- Shapes not listed in the Expectation.
- Colour variation within a shape type (all subsystems the same blue — differentiating by colour would encode meaning not listed in the legend).
