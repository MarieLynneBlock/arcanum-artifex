# SynthClaim — system context

*This is the synthetic example shipped with the `architecture-models-4plus1` skill. It is deliberately fictional but inherits the main characteristics of real hybrid enterprise platforms: hybrid on-prem + cloud, multi-channel human intake, ML-assisted decisioning, human adjudicators in the loop, encrypted data flows, and regulatory exposure.*

## System at a glance

**Name:** SynthClaim

**One-line purpose:** A hybrid cloud claims-processing platform that ingests insurance claims through multiple channels, extracts and classifies their content using OCR and ML, and routes them to human adjudicators or to auto-approval for low-risk cases.

## Stakeholders and concerns

| Stakeholder | Primary concern |
|-------------|-----------------|
| Policyholders (end users) | Submit claims easily through any channel; receive a decision quickly and transparently |
| Adjudicators (internal role) | Clear queue, supporting evidence surfaced, auditable decisions |
| Compliance / DPO | Data protection by design, auditability, GDPR Art. 22 compliance for automated decisions |
| SRE / platform engineering | Availability, cost efficiency, secure hybrid integration with the on-prem core policy system |
| Data science team | Reliable training data, feature parity between training and inference, drift monitoring |
| CFO / executive steering | Cost per claim, straight-through-processing rate, regulatory risk posture |

## Technology stack

- **On-prem core policy system** — legacy IBM mainframe exposing a SOAP/XML interface; authoritative source for policy, customer, and payment data.
- **On-prem document gateway** — receives paper (post-scan) and email-attached documents; forwards to cloud via site-to-site VPN.
- **Cloud platform** — AWS, primary region `eu-west-1` (Ireland), DR in `eu-west-2` (London).
- **Primary languages** — Java 21 (Spring Boot 3.x) for services, Python 3.12 for data and ML pipelines, TypeScript (React) for portal and adjudicator UI.
- **Data stores** — Amazon RDS PostgreSQL 16 for transactional claims data, S3 for document objects (SSE-KMS with customer-managed keys), OpenSearch for claims search, a feature store on S3+Athena.
- **Event bus** — Amazon MSK (managed Kafka).
- **ML platform** — Amazon SageMaker for training and model registry; inference served via SageMaker real-time endpoints behind an internal API.
- **CI/CD** — GitLab (self-hosted on-prem) for source; Jenkins runners in a shared build account for packaging; Terraform + Ansible for deployment; ArgoCD for Kubernetes workloads (where used).

## Scale characteristics

- **Active policies** — ~3 million
- **Claims per month** — ~80,000 submitted; ~55,000 auto-routed, ~25,000 reviewed by adjudicators
- **Channels** — portal (55%), email (30%), paper/scan (10%), broker API (5%)
- **Peak load** — Monday mornings, typically 3× average submission rate for 2 hours
- **Geography** — UK and Ireland customers only
- **Document volume** — ~150,000 documents per month, avg 2 MB, max 50 MB per document

## Key quality attributes (ranked)

1. **Privacy / data protection** — personal and health-category data under GDPR; failure here is existential.
2. **Auditability** — every claim decision must be reconstructible for the ombudsman or regulator 7 years later.
3. **Availability** — 99.9% for the submission path (customers can submit 24×7); 99.5% for the adjudicator path (business hours primary).
4. **Latency** — submission confirmation < 3 s at p99; auto-classification decision < 30 s at p99; end-to-end decision on auto-approvable claims < 10 min.
5. **Security** — claims carry sensitive medical and financial data; threat model includes external attackers, vendor access, and insider threat.
6. **Fairness** — ML-assisted decisions must be monitored for fairness across demographic groups; decisions must be appealable.
7. **Cost efficiency** — straight-through-processing rate is the main cost driver; architecture must support continuous improvement of this metric.

## Constraints

- **Regulatory** — GDPR (data protection), UK FCA / PRA (insurance conduct and operational resilience), EU AI Act (the claims-classification model is a high-risk AI system if used for eligibility decisions — legal has confirmed high-risk classification).
- **Organisational** — the mainframe team is separate and changes there follow a different cadence (quarterly releases); the cloud platform must tolerate mainframe unavailability.
- **Legacy** — the mainframe cannot be replaced in this programme; it's the system of record and must remain authoritative.
- **Data residency** — all personal data must remain in UK/EU jurisdiction; no transfers to the US except through SCCs with documented necessity.

## Out of scope

- Policy sales, underwriting, pricing, and renewal — handled by separate systems.
- Fraud investigation post-decision — handled by a separate investigations team and platform.
- Reinsurance claim recoveries — downstream of this platform.
- Customer communication other than claim-status updates (marketing, servicing).

## Audience chosen for this documentation

**Cross-functional (audience b)** — the documentation will be shared with the programme's mixed steering committee, which includes technology, compliance, claims operations, and a business sponsor. UML-flavoured notation where appropriate; BPMN-style swimlanes for the process view so the operations people can read it.

## Notation chosen

- Logical, development, scenarios — Mermaid (C4 container / flowchart / sequence+flowchart)
- Process — Mermaid flowchart with swimlane subgraphs (approximating BPMN)
- Physical — PlantUML with AWS stdlib for detail; Mermaid C4Deployment for the executive summary
