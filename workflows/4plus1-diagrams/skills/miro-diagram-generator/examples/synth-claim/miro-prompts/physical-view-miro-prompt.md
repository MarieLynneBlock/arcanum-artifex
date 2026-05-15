# Miro prompt — SynthClaim — Physical view

Paste into Miro AI Sidekick. Elements derived from `../04-physical-view.md`. Miro has built-in AWS icon packs — use them.

---

## Role

You are a senior SRE / cloud architect working in Miro AI. Your job is to produce the **Physical view** deployment topology for SynthClaim on a clean Miro frame, using Miro's built-in AWS icon library for cloud resources. Audience: SRE, infrastructure engineers, security engineers.

## Input

**System:** SynthClaim — hybrid cloud claims-processing platform.

**Scope:** Production topology in AWS eu-west-1 (primary region). Shows compute, network segmentation, data stores, ingress paths, on-premises integration, and cross-cutting security/observability. Does NOT show the DR region in detail (reference only), the development view's repos, or runtime call sequences.

**Zones (top to bottom, as horizontal bands):**
1. **On-premises datacentre (UK)** — contains Policy Mainframe, Document Gateway, Post-room scan service.
2. **AWS eu-west-1 public tier** — Route53, CloudFront, WAF, ALB (public), API Gateway.
3. **AWS eu-west-1 private tier (services)** — ECS Fargate for 6 services (API Edge, Intake, Lifecycle, Decision, DSAR, Docpipe), SageMaker endpoint, MSK, OpenSearch.
4. **AWS eu-west-1 private tier (data)** — RDS PostgreSQL Multi-AZ.
5. **AWS eu-west-1 isolated tier** — S3 (docs), S3 (audit), S3 (features).
6. **AWS eu-west-1 security & operations** — KMS, Secrets Manager, CloudWatch, ECR.
7. **AWS eu-west-2 (DR region)** — single collapsed box labelled "DR — warm standby (see separate DR diagram)".

**Key connections (exact list):**
- Route53 → CloudFront → WAF → ALB (public) → API Edge (private)
- API Gateway (public) → (mTLS) → API Edge (private, via VPC Link)
- API Edge → Intake / Lifecycle / DSAR
- Intake → MSK (publish); Lifecycle → MSK (subscribe)
- Lifecycle → RDS; Decision → RDS
- Lifecycle → Mainframe (SOAP, site-to-site VPN)
- Decision → Mainframe (write-back, VPN)
- Docpipe → S3 (docs); Docpipe → SageMaker endpoint
- SageMaker → S3 (features)
- DSAR → RDS, S3 (docs), S3 (audit)
- Decision → S3 (audit) — append
- All services → KMS (decrypt), Secrets Manager (fetch), CloudWatch (logs)
- All container images come from ECR
- Mail Gateway (on-prem) → Intake via VPN (webhook)
- Post-room scan → Mail Gateway (on-prem internal)
- eu-west-1 → eu-west-2 (DR) via VPC peering and managed replication (RDS read-replica, S3 CRR)

**Context on the board:** none assumed.

## Steps

1. Create a frame titled **"Physical view — SynthClaim — Production eu-west-1"**, approximately 3200 × 2000 px, landscape.
2. Place a legend in the **top-right** (340 × 320 px):
   - **Grey dashed-border rectangle** = on-premises zone
   - **Orange rectangle with AWS logo** = AWS region / VPC
   - **Green subnet rectangle** = public subnet
   - **Amber subnet rectangle** = private subnet
   - **Red subnet rectangle** = isolated subnet
   - **AWS service icons** (from Miro's AWS icon pack)
   - **Solid arrow** = primary traffic path
   - **Dashed arrow** = management / replication path
   - **Thick blue arrow** = site-to-site VPN (on-prem ↔ cloud)
   - **Lock icon** = KMS-encrypted at rest
3. Create a large **grey dashed-border rectangle** on the left half of the frame labelled **"On-premises datacentre (UK)"**. Inside, place three AWS-style components (use generic server/database icons):
   - Policy Mainframe (server icon, labelled "IBM Z — SOAP")
   - Document Gateway (server icon, labelled "Mail + scan relay")
   - Post-room scan service (server icon)
4. Create a large **orange rectangle** on the right two-thirds of the frame labelled **"AWS eu-west-1"**. Inside, nest a second orange rectangle labelled **"prod-vpc (10.0.0.0/16)"**.
5. Inside the VPC, stack **four horizontal subnet bands** top-to-bottom:
   - **Green band** titled "Public subnets (AZ a, b, c)" — place AWS icons: ALB (public), API Gateway.
   - **Amber band** titled "Private subnets — services" — place AWS icons: ECS cluster (as a group) containing 6 ECS-task icons labelled: API Edge (Kong), Intake, Lifecycle, Decision, DSAR, Docpipe (Airflow). Also: SageMaker endpoint, MSK, OpenSearch.
   - **Amber band** titled "Private subnets — data" — place RDS icon labelled "Claims DB (PostgreSQL 16 Multi-AZ)".
   - **Red band** titled "Isolated subnets" — place three S3 icons: "claims-docs (SSE-KMS, object-lock)", "audit-log (SSE-KMS, object-lock, 7y)", "features". Add a **lock icon** beside each.
6. To the **right of the VPC, inside the AWS region but outside the VPC**, place cross-cutting AWS icons:
   - Route53 (DNS), CloudFront (CDN), WAF — place above the VPC public band to signal they're in front of it.
   - KMS, Secrets Manager, CloudWatch, ECR — stacked on the right-hand side.
7. Below the AWS region rectangle, place a **small collapsed box** labelled **"AWS eu-west-2 (DR) — warm standby — see DR diagram"**.
8. Draw the connections:
   - **Solid arrows** for primary traffic paths (Route53 → CloudFront → WAF → ALB → API Edge; API Edge → 3 services; Docpipe → S3/SageMaker; Lifecycle → RDS; Decision → RDS + S3 audit; etc.).
   - **Dashed arrows** for management / logging paths (services → CloudWatch; services → KMS; services → Secrets Manager; services → ECR for image pulls).
   - **Thick blue arrow** for the site-to-site VPN between the on-prem zone and the VPC. Label it "IPsec, redundant".
   - **Dashed arrow** from the VPC to the DR box labelled "replication (RDS + S3 CRR + MSK passive)".
9. Draw the **mail-path connection** from the on-prem Document Gateway across the VPN to the Intake ECS task, using a dashed arrow (it's webhook / asynchronous) labelled "webhook via VPN".
10. Label every primary-path arrow with a protocol (e.g. "HTTPS/TLS 1.3", "SOAP/XML over VPN").
11. Add a **title at the top**: "SynthClaim — Physical view — Production eu-west-1 — v1.0 — 2026-04-18".
12. At the bottom of the frame, add a small text block with **key numbers**: "Availability SLA: 99.9% (submission), 99.5% (adjudicator). RTO 30m, RPO 5m. Data residency: UK/EU only."
13. Align everything to the grid; avoid arrow crossings through the subnet band boundaries where possible.

## Expectation

The final frame must contain exactly:
- **1 frame** with title
- **1 legend** (10 entries)
- **1 on-premises grey dashed zone** with 3 component icons
- **1 AWS eu-west-1 orange region rectangle** containing **1 VPC rectangle**
- **3 subnet bands** (1 green, 2 amber, 1 red) — note this is actually 4 bands total as listed; adjust colour if clearer
- **AWS icons** placed as listed — roughly: 2 in public band, 9 in private-services band, 1 in private-data band, 3 in isolated band, 4 in cross-cutting region-level, 3 in front of VPC (Route53 / CloudFront / WAF)
- **1 thick blue VPN arrow**
- **1 small DR region box** with a replication dashed arrow to it
- **~25 primary and management arrows** total, labelled with protocol where relevant
- **3 lock icons** on the isolated S3 buckets
- **1 bottom text block** with SLA / RTO / RPO / residency
- All AWS icons are from Miro's built-in AWS pack — do not substitute custom shapes
- All text readable at default zoom

## Narrowing

Do **NOT** include:
- Logical component responsibilities (that's the logical view).
- Runtime call sequences / flows (that's the process view).
- Code / repo organisation (that's the development view).
- Full DR topology (reference only — a separate diagram).
- Staging or dev environments.
- IAM role detail (represent as "least-privilege roles" in the legend; leave specifics for a separate IAM diagram).
- Security-group numeric port rules (too granular for this view).
- Instance sizes beyond what's shown in the accompanying doc (keep the diagram readable).
- Decorative elements.
- Shapes or colours not in the legend.
