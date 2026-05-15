# SynthClaim — Physical view

**Audience:** SRE / platform engineering, infrastructure engineers, security, operations. The simplified topology at the top is also suitable for the cross-functional steering committee.
**Takeaway:** Where SynthClaim runs in production, how the on-premises mainframe integrates, where data lives, how traffic flows, and where the security boundaries are.
**Version:** 1.0 (2026-04-18)
**Owner:** Platform Engineering
**Last reviewed:** 2026-04-18

---

## 1. Overview

SynthClaim is deployed in AWS `eu-west-1` (Ireland) as primary and `eu-west-2` (London) as disaster-recovery region. A site-to-site VPN connects both regions to the on-premises data centre where the policy mainframe lives. All personal data remains in UK/EU jurisdiction.

The cloud topology uses VPC-per-environment with public, private, and isolated subnets. Workloads run on ECS Fargate (stateless services) and SageMaker (ML inference). Data stores — RDS PostgreSQL, S3, MSK, OpenSearch — are managed services. A customer-managed KMS provides keys for all at-rest encryption of personal data.

## 2. Scope

- **Environments documented:** production (primary + DR). Staging is architecturally similar, sized smaller; dev is per-developer sandboxes and not covered here.

## 3. High-level topology (simplified — for executive / cross-functional audience)

```mermaid
C4Deployment
    title SynthClaim — High-level deployment topology

    Deployment_Node(onprem, "On-premises data centre", "Corporate DC (UK)") {
        Container(mf, "Policy Mainframe", "IBM Z — system of record")
        Container(docgw, "Document Gateway", "Mail + scan relay")
    }

    Deployment_Node(aws1, "AWS eu-west-1 (Ireland) — PRIMARY", "Cloud region") {
        Deployment_Node(vpc1, "prod-vpc", "VPC") {
            Container(svc1, "SynthClaim services", "ECS Fargate cluster")
            ContainerDb(data1, "Claims data stores", "RDS, S3, MSK, OpenSearch")
            Container(ml1, "ML inference", "SageMaker endpoint")
        }
    }

    Deployment_Node(aws2, "AWS eu-west-2 (London) — DR", "Cloud region") {
        Deployment_Node(vpc2, "dr-vpc", "VPC") {
            Container(svc2, "SynthClaim services", "ECS Fargate cluster — warm standby")
            ContainerDb(data2, "Claims data stores", "RDS replica, S3 CRR, MSK passive")
        }
    }

    Rel(onprem, aws1, "Site-to-site VPN", "IPsec")
    Rel(onprem, aws2, "Site-to-site VPN (DR)", "IPsec")
    Rel(aws1, aws2, "Cross-region replication", "VPC peering + managed replication")
```

## 4. Detailed production topology — eu-west-1

The detailed diagram is maintained in PlantUML at `diagrams/physical-view.puml` (rendered in `diagrams/physical-view.png` for GitHub viewing; the source is the editable artefact).

```plantuml
@startuml
!include <awslib/AWSCommon>
!include <awslib/Groups/AWSCloud>
!include <awslib/Groups/VPC>
!include <awslib/Groups/PrivateSubnet>
!include <awslib/Groups/PublicSubnet>
!include <awslib/Containers/ElasticContainerService>
!include <awslib/Containers/ElasticContainerRegistry>
!include <awslib/Database/RDS>
!include <awslib/Storage/SimpleStorageService>
!include <awslib/NetworkingContentDelivery/APIGateway>
!include <awslib/NetworkingContentDelivery/CloudFront>
!include <awslib/NetworkingContentDelivery/Route53>
!include <awslib/NetworkingContentDelivery/ElasticLoadBalancing>
!include <awslib/SecurityIdentityCompliance/KeyManagementService>
!include <awslib/SecurityIdentityCompliance/SecretsManager>
!include <awslib/SecurityIdentityCompliance/WAF>
!include <awslib/ManagementGovernance/CloudWatch>
!include <awslib/MachineLearning/SageMaker>
!include <awslib/Analytics/ManagedStreamingforApacheKafka>
!include <awslib/Analytics/OpenSearchService>

title SynthClaim — Physical view — Production eu-west-1

rectangle "On-premises data centre (UK)" as onprem {
    component "Policy Mainframe\n(IBM Z, SOAP)" as mf
    component "Document Gateway\n(mail + scan)" as docgw
    component "Post-room scan\nservice" as scan
}

AWSCloudGroup(aws, "AWS — eu-west-1") {
    Route53(dns, "Route 53", "claims.example.com")
    CloudFront(cdn, "CloudFront", "portal + console static")
    WAF(waf, "WAF", "OWASP rules")

    VPCGroup(vpc, "prod-vpc (10.0.0.0/16)") {
        PublicSubnetGroup(pub, "Public (AZ a, b, c)") {
            ElasticLoadBalancing(albPub, "ALB — public", "TLS, WAF attached")
            APIGateway(apigw, "API Gateway", "broker mTLS")
        }
        PrivateSubnetGroup(priv, "Private (AZ a, b, c)") {
            ElasticContainerService(ecsEdge, "ecs — api edge (Kong)", "Fargate")
            ElasticContainerService(ecsIntake, "ecs — intake", "Fargate")
            ElasticContainerService(ecsLifecycle, "ecs — lifecycle", "Fargate")
            ElasticContainerService(ecsDecision, "ecs — decision", "Fargate")
            ElasticContainerService(ecsDsar, "ecs — dsar", "Fargate")
            ElasticContainerService(ecsDocpipe, "ecs — docpipe (Airflow)", "Fargate")
            SageMaker(sm, "SageMaker endpoint", "classifier inference")
            ManagedStreamingforApacheKafka(msk, "MSK", "event bus")
            OpenSearchService(os, "OpenSearch", "claims search")
        }
        PrivateSubnetGroup(privData, "Private — data (AZ a, b, c)") {
            RDS(rds, "RDS PostgreSQL 16", "Multi-AZ, encrypted")
        }
        PrivateSubnetGroup(iso, "Isolated (AZ a, b, c)") {
            SimpleStorageService(s3docs, "s3 — claims-docs", "SSE-KMS, object-lock")
            SimpleStorageService(s3audit, "s3 — audit-log", "SSE-KMS, object-lock, 7y")
            SimpleStorageService(s3features, "s3 — features", "SSE-KMS")
        }
    }

    KeyManagementService(kms, "KMS", "customer-managed CMKs")
    SecretsManager(secrets, "Secrets Manager", "rotation enabled")
    CloudWatch(cw, "CloudWatch", "metrics + logs (90d hot, 7y cold via S3)")
    ElasticContainerRegistry(ecr, "ECR", "signed images")
}

dns --> cdn
cdn --> waf
waf --> albPub
apigw --> ecsEdge : mTLS
albPub --> ecsEdge
ecsEdge --> ecsIntake
ecsEdge --> ecsLifecycle
ecsEdge --> ecsDsar
ecsIntake --> msk : publish
ecsLifecycle --> msk : subscribe
ecsLifecycle --> rds
ecsDecision --> rds
ecsLifecycle --> mf : SOAP over VPN
ecsDecision --> mf : SOAP over VPN (retry queue)
ecsDocpipe --> s3docs
ecsDocpipe --> sm : inference
sm --> s3features
ecsDsar --> rds
ecsDsar --> s3docs
ecsDsar --> s3audit
ecsDecision --> s3audit : append
ecsIntake ..> kms : decrypt
ecsLifecycle ..> kms : decrypt
ecsDecision ..> kms : decrypt
ecsDsar ..> kms : decrypt
sm ..> kms : decrypt
ecsIntake ..> secrets : fetch
ecsLifecycle ..> secrets : fetch
ecsEdge ..> cw : logs
ecsIntake ..> cw : logs
ecsLifecycle ..> cw : logs

onprem -[#blue,bold]-> aws : Site-to-site VPN\n(IPsec, redundant)
docgw -.-> ecsIntake : webhook via VPN
scan --> docgw

@enduml
```

## 5. Compute inventory

| Component | Compute | Sizing (prod primary) | Scaling |
|-----------|---------|----------------------|---------|
| API Edge (Kong) | ECS Fargate | 3× `1 vCPU / 2 GB`, min 3 | Target-tracking (70% CPU), 3 → 20 |
| Intake | ECS Fargate | 4× `2 vCPU / 4 GB`, min 4 | 4 → 40; burst to 40 during Monday peaks |
| Lifecycle | ECS Fargate | 6× `2 vCPU / 4 GB`, min 6 | 6 → 30 |
| Decision | ECS Fargate | 4× `1 vCPU / 2 GB`, min 4 | 4 → 20 |
| Docpipe (Airflow workers) | ECS Fargate | 6× `2 vCPU / 8 GB`, min 2 | 2 → 20 by queue depth |
| Classifier (SageMaker) | `ml.m5.xlarge` | 2 instances, min 2 | 2 → 10 |
| DSAR | ECS Fargate | 2× `1 vCPU / 2 GB`, min 1 | 1 → 4 |

DR region: warm standby, same service list at min-capacity only (1–2 instances each); scales up on fail-over.

## 6. Data stores

| Store | Engine | Sizing | Backup / replication | Retention |
|-------|--------|--------|----------------------|-----------|
| Claims Datastore | RDS PostgreSQL 16 Multi-AZ | `db.r6g.xlarge`, 500 GB gp3 | Automated backups 35 d + cross-region read-replica to eu-west-2 | 7 years post-claim closure (then anonymised) |
| Document Store | S3 | ~30 TB, growing 2 TB/year | Cross-region replication to eu-west-2; object lock compliance mode | 7 years post-claim closure |
| Audit Log (cold) | S3 | ~5 TB, growing 500 GB/year | CRR to eu-west-2; object lock | 7 years (regulatory minimum) |
| Feature Store | S3 | ~500 GB | CRR; no object lock (rewritable features) | 3 years |
| OpenSearch | OpenSearch 2.x | 3× `r6g.large.search` | Snapshot to S3 hourly | 90 days hot, rebuilt from Claims DB if needed |
| MSK (Kafka) | MSK | 3× `kafka.m5.large` | Not replicated across region (events are ephemeral, 7 d retention); re-driven from source on DR |
| Model Registry | SageMaker Model Registry (S3-backed) | negligible | S3 versioning + CRR | 10 years (AI Act documentation lifespan) |

## 7. Ingress / egress paths

**Public ingress:**
- Route 53 → CloudFront → WAF → ALB (public subnet) → ECS Edge (private subnet) → downstream ECS services.
- Static portal and console assets served from CloudFront directly (origin: S3 with OAC).

**Broker mTLS ingress:**
- Route 53 → API Gateway (mTLS, certificate-based authN) → VPC Link → ECS Edge.

**On-premises ingress:**
- Corporate mail gateway → site-to-site VPN → private ALB (internal) → ECS Intake.
- Post-room scan service → Document Gateway → Mail Gateway (same path as above).

**Egress:**
- ECS services → Mainframe: via VPN, SOAP/XML over TLS.
- ECS services → AWS services: via VPC Endpoints (S3, KMS, Secrets Manager, CloudWatch, ECR) — no traffic leaves the VPC to reach AWS.
- No internet egress from private/isolated subnets except via a controlled NAT gateway for specific third-party integrations (listed in network-allowlist).

## 8. CI/CD pipeline infrastructure

- **Source:** GitLab self-hosted on-premises (separate repos per the development view).
- **Build:** Jenkins runners in a shared `build` AWS account (separate from production).
- **Image signing:** cosign + Sigstore (target: Q2 2026; currently signed by GPG with internal trust).
- **Artefact registry:** Nexus (on-prem) for libraries; ECR for container images.
- **Deploy:** Terraform Cloud for IaC; ArgoCD (for the Airflow Kubernetes workloads only); AWS CodeDeploy for ECS blue/green.
- **Deploy rights:** separate roles per environment; prod deploy requires a second human approval (four-eyes) for regulated services.

## 9. Observability

- **Metrics:** CloudWatch Metrics + Managed Prometheus, visualised in Managed Grafana.
- **Logs:** CloudWatch Logs (90 d hot), exported to S3 (7 y cold); structured JSON via `platform-observability` lib.
- **Traces:** AWS X-Ray; OpenTelemetry protocol into X-Ray endpoint.
- **Dashboards:** per-service dashboard, plus a cross-cutting "claims health" dashboard (submission rate, auto-approval rate, adjudicator queue depth, mainframe-degraded-mode indicator).
- **Alerting:** PagerDuty; severity 1 for availability breaches, severity 2 for SLO burn, severity 3 for drift or anomaly detections.

## 10. Security controls summary

- **Network segmentation:** public / private / isolated subnets; security groups scoped per service; WAF with OWASP managed rules; no direct internet egress from private/isolated tiers.
- **IAM:** roles scoped per service; no admin access in production except through break-glass (recorded, time-boxed, requires two approvers).
- **Secrets:** AWS Secrets Manager with automatic rotation for DB credentials; mainframe credentials rotated manually (quarterly) — documented gap.
- **Encryption:** TLS 1.3 everywhere in transit; SSE-KMS with customer-managed keys at rest for all personal-data stores; S3 object lock in compliance mode on audit and document stores.
- **Key management:** separate CMKs per environment and per regulated-data-type; rotation every 365 days; break-glass decryption requires two-person approval.
- **Runtime monitoring:** GuardDuty for anomalous API activity; Security Hub aggregating findings; Inspector for ECR image vulnerabilities; Macie enabled on S3 buckets with personal data.
- **Supply chain:** SBOM on every image, Grype scan in CI, quarantine on critical findings. Sigstore signing pending.

## 11. Non-functional properties (environment level)

- **Availability SLA (prod):** 99.9% for submission path; 99.5% for adjudicator path; 99% for DSAR.
- **RTO (DR):** 30 minutes to restore submission path; 4 hours to restore full service.
- **RPO:** 5 minutes for Claims DB (read-replica lag target); near-zero for S3 (CRR); 7 days for MSK events (acceptable because source is replayable from Claims DB and S3).
- **Capacity headroom:** designed for 3× Monday peak without scale (absorbed within burst ratio).
- **Cost envelope:** approximately £350k/year for primary region compute + managed services (steady state); DR ~20% of primary; mainframe VPN ~£12k/year (telco fees, ops).

## 12. Concerns

> **Concern (GDPR — data residency):** All personal data stores are in UK/EU jurisdiction. Verify that CloudWatch Logs do not contain personal data (they currently may, via exception stack traces with email addresses); add a log-redaction filter at the `platform-observability` level.

> **Concern (Security — mainframe credential rotation):** Mainframe credentials are rotated manually quarterly. This is the single largest security-posture gap. Target: automate credential rotation by Q3 2026.

> **Concern (Security — supply chain signing):** Images are not yet signed with Sigstore cosign. SLSA level 2 gap. Target: close by Q2 2026.

> **Concern (Regulatory — AI Act documentation):** Required artefacts (model card, data card, risk assessment, post-market monitoring plan) exist per model but are not yet versioned in a single inventory. Create a Model Governance repository with a canonical index; populate by Q2 2026.

> **Concern (Sustainability — region selection):** `eu-west-1` (Ireland) and `eu-west-2` (London) both have moderate grid carbon intensity. A Nordic region (`eu-north-1`, `eu-central-2`) would be lower-carbon but has weaker mainframe VPN latency. Recommendation: schedule ML training runs in `eu-north-1` (non-latency-sensitive), keep transactional workloads in the current regions.

> **Concern (Operational resilience — DORA):** Under the EU Digital Operational Resilience Act (DORA, in force from 2025), ICT third-party risk must be architecturally documented. AWS, GitLab, PagerDuty, LaunchDarkly are all in-scope vendors. Cross-check the physical view against the DORA register quarterly.

## 13. Assumptions

> **Assumption:** Both AWS regions (eu-west-1 and eu-west-2) remain in UK-accessible jurisdiction and do not introduce new transfer-mechanism requirements.

> **Assumption:** Mainframe VPN bandwidth (100 Mbps) is adequate for production load. Capacity review scheduled before go-live.

> **Assumption:** Airflow is the right orchestrator for docpipe. If ML-platform teams migrate docpipe to Step Functions / Prefect, the physical view simplifies (fewer long-running workers).

## 14. Open questions

- **Q9:** Should the DR region be hot (active/active) rather than warm standby? Owner: SRE + Finance. Impact: cost vs RTO trade-off.
- **Q10:** Do we fund the Nordic region for ML training, or stay single-region? Owner: Data Science + Finance + Sustainability lead.
- **Q11:** Can the on-prem Document Gateway be retired in favour of direct email → AWS SES → Intake? Owner: Platform Engineering.

## 15. Related views

- **Logical view (01):** the components deployed here.
- **Process view (02):** the flows exercising this topology.
- **Development view (03):** what gets built and how it gets to these environments.
- **Scenarios view (05):** scenarios that exercise DR, key rotation, and incident response.

## 16. Change log

| Date | Author | Change |
|------|--------|--------|
| 2026-04-18 | Architecture team | Initial version |
