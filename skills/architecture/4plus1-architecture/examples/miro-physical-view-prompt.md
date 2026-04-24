# Miro Prompt — Physical View

## How to use this file

Copy the prompt below, replace all `[PLACEHOLDER]` values, and paste into Miro AI Sidekick. Attach your infrastructure topology description and node specification table from the board as context.

---

## Prompt Template

```
You are a cloud infrastructure architect and systems engineer creating a formal Physical View (Deployment View) diagram for an architecture review. The audience is infrastructure engineers, SREs, and security officers. Every node, network path, and security boundary must be explicitly and accurately represented.

CONTEXT FROM BOARD: [Select and attach: infrastructure topology description, node specification table, artefact-to-node mapping, and security boundary notes from your board]

Create the following on this Miro board in a frame titled "Physical View — [SYSTEM NAME]":

STEP 1 — FRAME SETUP
Create one large outer frame titled "Physical View — [SYSTEM NAME]" with background #0D1B2A (dark navy). All text in this frame must be white or light-coloured for contrast. Divide into:
- Main area (80% width): deployment topology diagram
- Right sidebar (20% width): specifications panel

STEP 2 — INTERNET AND CDN LAYER (top of main area)
At the very top, create:
- A wide light-grey (#E0E0E0) rounded rectangle labelled "🌐 Internet / Public Users", full width of diagram area, 60px tall
- Below it, a blue rectangle (#1565C0) labelled "CloudFront CDN (or [YOUR CDN NAME])" — full width, 50px tall — connected to the internet rectangle with a solid white downward arrow labelled "HTTPS 443"
- To the right of the CDN box, a small grey rectangle labelled "[DNS PROVIDER] — Route 53" connected with a grey dashed arrow

STEP 3 — CLOUD PROVIDER OUTER BOUNDARY
Create a large rounded-rectangle region with:
- Dashed white border (2px)
- Label in top-left: "☁ [CLOUD PROVIDER] — [PRIMARY REGION]" in white bold text
- Background: transparent (show navy through)
- This region contains ALL the following infrastructure elements

STEP 4 — VPC BOUNDARY
Inside the cloud region, create a rounded-rectangle for the VPC:
- Solid white border (1px)  
- Label: "VPC: [VPC NAME] ([CIDR BLOCK e.g., 10.0.0.0/16])" in white
- Background: #1A2F45 (slightly lighter than frame background)

STEP 5 — SUBNET ZONES (inside the VPC)
Create the following subnet zones as labelled rectangles inside the VPC:

PUBLIC SUBNET (top of VPC):
- Background: #1A3A5C (dark blue), dashed border
- Label: "Public Subnet — [AZ list e.g., eu-west-1a, 1b, 1c]"
- Place inside it:
  - White rectangle: "ALB — Application Load Balancer" with annotation "Listens: HTTPS 443 → HTTP 8080 internal"
  - White rectangle: "NAT Gateway" (for outbound-only egress)
  - Small white rectangle: "Bastion Host (SSH)" — labelled "admin access only — port 22 from VPN only"

PRIVATE SUBNET — APP TIER (middle of VPC):
- Background: #1A4A3C (dark green), dashed border
- Label: "Private Subnet — App Tier — [AZ list]"
- Place inside it a large white-bordered rectangle labelled "🐳 [CONTAINER PLATFORM e.g., EKS Cluster / ECS]"
  - Inside the cluster rectangle, create [N] small coloured rounded rectangles — one per service:
    - Service 1: background #2D6A9F, label "[SERVICE NAME] × [REPLICA COUNT] replicas"
    - Service 2: background #2D9F6A, label "[SERVICE NAME] × [REPLICA COUNT] replicas"
    [repeat for each service]
  - Add a small text annotation below the cluster: "Auto-scale: [MIN]–[MAX] nodes | Instance type: [TYPE]"

PRIVATE SUBNET — DATA TIER (bottom of VPC):
- Background: #4A1A3C (dark purple), dashed border
- Label: "Private Subnet — Data Tier — NO INTERNET EGRESS"
- Place inside it:
  - White rectangle: "[DATABASE] — [e.g., RDS PostgreSQL Multi-AZ]" with annotation "Port [PORT] | [SIZE] | Standby in [SECONDARY AZ]"
  - White rectangle: "[MESSAGE BROKER] — [e.g., Amazon MSK Kafka]" with annotation "[N] brokers | replication factor [N]"
  - White rectangle: "[CACHE] — [e.g., ElastiCache Redis]" with annotation "[CONFIG] | [SIZE]"
  - White rectangle: "[OBJECT STORE] — [e.g., S3]" with annotation "versioned | encrypted at rest"

STEP 6 — NETWORK CONNECTIONS (inside the VPC)
Draw arrows between the zones with the following styling:
- Internet → CDN → ALB: solid white arrows, labelled "HTTPS 443"
- ALB → App Tier services: solid white arrow, labelled "HTTP 8080 (internal)"
- App Tier services → Database: solid green arrow, labelled "TCP [PORT] | TLS"
- App Tier services → Message Broker: solid orange arrow, labelled "Kafka protocol [PORT] | TLS"
- App Tier services → Cache: solid cyan arrow, labelled "Redis [PORT] | TLS"
- App Tier services → Object Store: dashed grey arrow, labelled "HTTPS 443 (AWS SDK)"
- NAT Gateway → Internet: dashed grey arrow, labelled "Outbound only (egress)"
Do NOT draw any arrow from the data tier directly to the internet.

STEP 7 — SECONDARY REGION / DR (if applicable)
Create a second smaller cloud region to the right of the main region:
- Label: "☁ [CLOUD PROVIDER] — [DR REGION] (Disaster Recovery)"
- Inside: show only the key components (database replica, minimal app tier)
- Connect primary to DR with a wide dashed blue arrow labelled "Cross-region replication | [FREQUENCY/LAG]"
- Add annotation: "RTO: [VALUE] | RPO: [VALUE]"

STEP 8 — OBSERVABILITY STACK (small section below the VPC, inside cloud boundary)
Create a dark rectangle labelled "Observability" containing:
- Small white card: "📊 Metrics: [TOOL] — scrape every [INTERVAL]"
- Small white card: "📋 Logs: [TOOL] → [DESTINATION]"
- Small white card: "🔍 Traces: [TOOL] → [DESTINATION]"
- Small white card: "🔔 Alerts: [TOOL] → [NOTIFICATION CHANNEL]"

STEP 9 — SPECIFICATIONS PANEL (right sidebar)
Create a white sidebar with dark text containing:
Section 1 — "Node Specifications" table:
Headers: "Node | Type | Size | HA Config"
Rows: [POPULATE FROM YOUR NODE SPEC TABLE]

Section 2 — "Artefact Versions" table:
Headers: "Artefact | Tag | Node"
Rows: [POPULATE FROM YOUR ARTEFACT-TO-NODE MAPPING]

Section 3 — "Security Boundaries" text card:
"TLS termination: [WHERE]
mTLS scope: [WHICH SERVICES]
Network policies: [TOOL / ENFORCEMENT]
Data residency: [CONSTRAINT]"

STEP 10 — LEGEND (bottom-left of main area)
Create a white card titled "Legend":
→ White arrow = primary traffic flow
→ Green arrow = database connection
→ Orange arrow = message broker
→ Cyan arrow = cache
→ Dashed grey arrow = outbound egress / async
→ Dashed blue arrow = cross-region replication
🔒 = TLS/mTLS enforced
Dashed rectangle border = subnet boundary
Solid rectangle border = cluster/platform boundary

DO NOT include: class names, package structures, UML class notation, source code references, business logic, or sequence of calls. Do not add decorative cloud icons that are not from a consistent icon set. Do not draw any direct connection between the data tier subnet and the internet layer. Do not place any element outside the outer frame.
```

---

## Calibration Notes

- **Dark background is intentional.** Infrastructure diagrams are conventionally dark. The contrast between background and subnet zones conveys network hierarchy visually.
- **Subnet nesting.** Miro AI handles nested frames reasonably well when you specify background colours — the nested rectangle colours must all be visually distinct from each other.
- **Arrow colours matter.** Infrastructure diagrams need coloured arrows by protocol/destination type. Without specifying colours, Miro AI will use a uniform grey which loses all semantic meaning.
- **Include decision points for traffic flow.** Explicitly mention routing decisions ("if health check fails, ALB routes to healthy instances", "if rate limit exceeded, return 429") to produce diamond-shaped decision nodes rather than flat linear flows.
- **Do not over-cluster.** If you have more than 8 services in the app tier, group them into named groups (e.g., "Order Cluster", "Payment Cluster") and show the groups rather than individual replicas.
- **Use existing board content.** If you have infrastructure topology notes, node specification tables, or security boundary descriptions on the board, select and attach them before running. Miro AI will incorporate those specific details rather than generating generic placeholders.
- **Start with the happy path.** Generate the primary deployment topology first (the main region, standard traffic flow). Add the DR region, failover paths, and edge cases in a second iteration.
- **Mention failure modes explicitly.** "What happens when the database is unavailable" or "show the failover path when the primary region goes down" — Miro AI will not invent failure scenarios. If you do not mention them, they will not appear.
- **Iteration.** After generation, use the edit function to: "Move the Observability section inside the VPC boundary" or "Add a red lock icon (🔒) to the database connection arrow." One change at a time. Never request multiple structural changes in a single prompt.
- **For complex topologies.** Consider using Miro's Doc format first to outline the full infrastructure with all zones, services, and network paths, then use that doc as context input for a simplified visual diagram showing the main topology and critical decision points.
