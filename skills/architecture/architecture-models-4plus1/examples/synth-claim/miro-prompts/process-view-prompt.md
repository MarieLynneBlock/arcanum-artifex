# Miro prompt — SynthClaim — Process view

Paste into Miro AI Sidekick. Elements derived from `../02-process-view.md`. This prompt covers the **Portal auto-approve** flow (flow 1); duplicate and adapt for the other flows in the process view.

---

## Role

You are a senior business analyst working in Miro AI. You are creating a **BPMN-style process diagram** for the **Portal submission with auto-approval** flow of SynthClaim on a clean Miro frame. The diagram will be reviewed by a cross-functional steering committee including claims operations — use BPMN shape semantics throughout.

## Input

**System under documentation:** SynthClaim — hybrid cloud claims-processing platform.

**Scope of this view:** Flow 1 — Portal submission leading to auto-approval. Does NOT cover email / broker ingestion, mainframe outage, or DSAR — those are separate diagrams.

**Swimlanes to create (top to bottom, in this order):**
1. Policyholder (human role)
2. Claims Portal (system)
3. Claim Intake Service (system)
4. Document Processing Pipeline (system)
5. Claim Classifier (system)
6. Claims Lifecycle Service (system)
7. Decision Service (system)
8. Audit Log (system)

**Activities per swimlane (exact list):**

Policyholder lane:
- Start event "Start"
- User task "Submit claim via portal"
- Message-receive event "See confirmation"

Claims Portal lane:
- Service task "Validate form & attachments"
- Service task "Upload documents to S3"

Claim Intake Service lane:
- Service task "Normalise to internal event"
- Service task "Publish ClaimSubmitted"

Document Processing Pipeline lane:
- Service task "OCR + field extraction"
- Service task "Classify document types"

Claim Classifier lane:
- Service task "Score claim"
- Exclusive gateway "Confidence ≥ threshold?"

Claims Lifecycle Service lane:
- Service task "Read policy from Mainframe"
- Exclusive gateway "Policy allows auto-approve?"
- Service task "Auto-approve"

Decision Service lane:
- Service task "Record decision"
- Service task "Write decision to Mainframe"
- Service task "Emit DecisionRecorded"

Audit Log lane:
- Intermediate event "Append-only log"
- End event "Audit entry written"

**Sequence flows (within a lane) and message flows (between lanes):**
- Start → Submit claim (sequence, within Policyholder)
- Submit claim → Validate form (message, Policyholder → Portal)
- Validate form → Upload documents (sequence, within Portal)
- Upload documents → Normalise (message, Portal → Intake)
- Normalise → Publish (sequence, within Intake)
- Publish → OCR (message, Intake → DocPipe)
- OCR → Classify (sequence, within DocPipe)
- Classify → Score (message, DocPipe → Classifier)
- Score → Confidence gateway (sequence, within Classifier)
- Confidence gateway YES → Read policy (message, Classifier → Lifecycle)
- Confidence gateway NO → "Route to adjudicator" (end-link event out of frame)
- Read policy → Policy rule gateway (sequence, within Lifecycle)
- Policy gateway YES → Auto-approve (sequence, within Lifecycle)
- Policy gateway NO → "Route to adjudicator" (end-link event out of frame)
- Auto-approve → Record decision (message, Lifecycle → Decision)
- Record decision → Write to Mainframe (sequence, within Decision)
- Record decision → Emit DecisionRecorded (sequence, within Decision — parallel with Write to Mainframe)
- Emit DecisionRecorded → Append-only log (message, Decision → Audit)
- Append-only log → End event (sequence, within Audit)
- Record decision → See confirmation (message, Decision → Policyholder)

**Context already on the board:** none assumed.

## Steps

1. Create a frame titled **"Process view — SynthClaim — Flow 1 Portal auto-approve"**, approximately 2800 × 1600 px, landscape.
2. Place a legend in the **top-right** (300 × 260 px):
   - Rounded rectangle (pale orange) = user task
   - Rounded rectangle (pale blue) = service task
   - Diamond = exclusive gateway
   - Circle (green thin) = start event
   - Circle (green double) = intermediate event
   - Circle (red thick) = end event
   - Solid arrow = sequence flow
   - Dashed arrow = message flow (between lanes)
3. Create **8 horizontal swimlanes** stacked top-to-bottom, each a rectangle spanning the full frame width (2400 px, excluding legend). Lane height ≈ 160 px each. Label each lane at its left edge with the swimlane name. Use alternating very-pale background shading to aid readability.
4. In the **Policyholder** lane:
   - Place a thin-bordered green **start circle** labelled "Start" at the far left.
   - Place a **pale-orange rounded rectangle** (user task) labelled "Submit claim via portal" next to it.
   - Place a thin-bordered green **intermediate circle** (envelope icon) labelled "Receive confirmation" at the far right.
5. In the **Claims Portal** lane:
   - Place **two pale-blue rounded rectangles** (service tasks): "Validate form & attachments", "Upload documents to S3", left-to-right.
6. In the **Claim Intake Service** lane:
   - **Two pale-blue rectangles**: "Normalise to internal event", "Publish ClaimSubmitted".
7. In the **Document Processing Pipeline** lane:
   - **Two pale-blue rectangles**: "OCR + field extraction", "Classify document types".
8. In the **Claim Classifier** lane:
   - **One pale-blue rectangle** "Score claim".
   - **One diamond** labelled "Confidence ≥ threshold?" — the exclusive gateway.
9. In the **Claims Lifecycle Service** lane:
   - **One pale-blue rectangle** "Read policy from Mainframe".
   - **One diamond** "Policy allows auto-approve?"
   - **One pale-blue rectangle** "Auto-approve".
10. In the **Decision Service** lane:
    - **Three pale-blue rectangles**: "Record decision", "Write decision to Mainframe", "Emit DecisionRecorded".
11. In the **Audit Log** lane:
    - **One green double-circle** "Append-only log" (intermediate event).
    - **One thick red circle** labelled "Audit entry written" (end event) at the far right.
12. Draw the **sequence flows** (solid arrows) within each lane horizontally connecting that lane's elements in the order listed in Input.
13. Draw the **message flows** (dashed arrows) between lanes, crossing lane boundaries vertically. Label key message flows with the event name (e.g. "ClaimSubmitted").
14. For each gateway diamond, draw **two out-going arrows**: one labelled "yes" (proceeds along the main flow) and one labelled "no" (terminates in a link-event circle labelled "Route to adjudicator" within the same lane, indicating the flow continues on the flow-2 diagram).
15. Add a title at the top of the frame: **"SynthClaim — Process view — Flow 1: Portal submission → auto-approve — v1.0 — 2026-04-18"**.
16. Align all elements to the grid; flows read left-to-right; minimise arrow crossings; use orthogonal elbow connectors.

## Expectation

The final frame must contain exactly:
- **1 frame**
- **1 title block**
- **1 legend** (8 entries)
- **8 swimlanes** with labels
- **1 start event** (thin green circle)
- **2 intermediate events** (double green circles)
- **1 end event** (thick red circle)
- **2 user tasks** (pale-orange rounded rectangles)
- **11 service tasks** (pale-blue rounded rectangles)
- **2 exclusive gateways** (diamonds)
- **2 link-event circles** labelled "Route to adjudicator" (out of main flow)
- **~14 sequence-flow arrows** (solid, within lanes)
- **~7 message-flow arrows** (dashed, between lanes)
- All text readable at default zoom; every arrow labelled where its purpose isn't obvious from position.

## Narrowing

Do **NOT** include:
- Email / broker / DSAR / mainframe-outage flows — these are separate diagrams.
- Infrastructure or deployment detail — that's the physical view.
- Internal component structure — that's the logical / development view.
- Error-handling branches beyond the two gateways' "no" exits.
- Decorative shapes, logos, emojis.
- Shapes not in the legend.
- Colour variation within a shape type (every service task the same pale-blue, every user task the same pale-orange).
