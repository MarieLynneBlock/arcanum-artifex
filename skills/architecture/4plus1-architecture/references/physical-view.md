# Physical View Reference

## Purpose

The physical view (also called the deployment view) describes the system from a **systems/infrastructure engineer's perspective** — how software components are mapped onto hardware and network infrastructure, and how they communicate at the infrastructure level.

**Target audience:** System engineers, infrastructure/cloud architects, DevSecOps, SRE, security officers  
**Central question:** *Where does the software run, on what infrastructure, and how do the pieces connect at the network and platform level?*

---

## Core Concepts

### Node
A physical or virtual hardware unit that can execute software: a server, VM, container host, cloud region, edge device, mobile device, or managed service endpoint.

### Artefact
A deployable software unit: a container image, WAR file, Lambda function, Helm chart, static bundle, etc.

### Communication Path
A network connection between nodes: LAN, WAN, internet, VPC peering, VPN, service mesh.

### Deployment Target
The platform that manages artefact execution: Kubernetes cluster, ECS, AWS Lambda, bare metal, etc.

---

## Document Structure

### 1. Audience Statement
Who reads this and what infrastructure concern it addresses.

### 2. Infrastructure Topology Overview

Describe the top-level deployment environment: cloud provider(s), regions, availability zones, on-premises components, edge presence.

Example:
```
AWS Multi-Region (primary: eu-west-1, DR: eu-central-1)
├── VPC: production
│   ├── Public Subnet (ALB, NAT Gateway, Bastion)
│   ├── Private Subnet — App Tier (EKS Node Groups)
│   └── Private Subnet — Data Tier (RDS, ElastiCache, MSK)
└── CDN: CloudFront (global)
```

### 3. Deployment Diagram

The core artefact of this view. Map every software component from the development view to a node.

Format:
```
┌─────────────────────── AWS eu-west-1 ───────────────────────┐
│                                                              │
│  ┌─── EKS Cluster ───────────────────────────────────────┐  │
│  │                                                        │  │
│  │  [order-service:3 replicas]   [payment-service:2]     │  │
│  │  [notification-worker:1]      [api-gateway:3]          │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                │                                              │
│         ┌──────┴──────┐                                       │
│    [RDS PostgreSQL]  [Amazon MSK (Kafka)]                    │
│    (Multi-AZ)        (3 brokers, 3 AZs)                     │
│                                                              │
│  [ElastiCache Redis] [S3 (artefacts, logs)]                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
          │                    │
    [CloudFront CDN]    [Route 53 (DNS)]
          │
    [End Users — Internet]
```

### 4. Node Specifications

For each significant node or node class:

| Node | Type | Size / Config | Replicas / AZs | Managed By |
|------|------|---------------|----------------|------------|
| EKS worker nodes | EC2 c5.2xlarge | 8 vCPU, 16 GB | 3 AZs, auto-scale 3–12 | AWS EKS |
| RDS PostgreSQL | db.r6g.large | Multi-AZ standby | 1 primary + 1 standby | AWS RDS |
| MSK Kafka | kafka.m5.large | 3 brokers | 1 per AZ | AWS MSK |
| Redis | cache.r6g.large | Cluster mode | 3 shards | AWS ElastiCache |

### 5. Artefact-to-Node Mapping

| Artefact | Node / Platform | Runtime | Exposed Port / Protocol |
|----------|----------------|---------|------------------------|
| `api-gateway:v2.3` | EKS (Deployment) | Docker / JVM 17 | 8080 (HTTP) |
| `order-service:v1.8` | EKS (Deployment) | Docker / JVM 17 | 8081 (HTTP, internal) |
| `notification-worker:v1.2` | EKS (Deployment) | Docker / Python 3.12 | None (consumer only) |
| `frontend:v4.1` | S3 + CloudFront | Static | 443 (HTTPS) |

### 6. Network Topology and Security Boundaries

Describe security zones and traffic flows:

```
Internet
    │  HTTPS only
    ▼
[CloudFront] ── WAF ──> [ALB] (public subnet)
                              │  HTTP (internal)
                              ▼
                    [api-gateway pod] (private subnet)
                              │  HTTP (service mesh)
                              ▼
               [order-service] / [payment-service]
                              │
                       [Data Tier VPC subnet]
                  [RDS] [Redis] [MSK] — no internet egress
```

Security boundaries to document:
- TLS termination point
- Service mesh / mTLS scope
- Firewall / Security Group rules (high-level)
- Network policies (Kubernetes NetworkPolicy or equivalent)
- Data residency constraints

### 7. High Availability and Disaster Recovery

| Component | HA Strategy | RTO | RPO |
|-----------|-------------|-----|-----|
| Application tier | Multi-AZ EKS, rolling deploy | < 5 min | 0 (stateless) |
| Database | Multi-AZ RDS, read replica | < 2 min | < 1 min |
| Message broker | 3-broker MSK, replication factor 3 | < 1 min | 0 (durable) |

DR strategy: active-passive / active-active / pilot light — state which and describe the failover procedure at a high level.

### 8. Infrastructure as Code

| Component | IaC Tool | Repository Path |
|-----------|----------|----------------|
| VPC, RDS, MSK | Terraform | `/infra/terraform/` |
| EKS workloads | Helm charts | `/infra/helm/` |
| CI/CD pipeline | GitHub Actions | `.github/workflows/` |

### 9. Observability Infrastructure

| Concern | Tooling | Collection Point |
|---------|---------|-----------------|
| Metrics | Prometheus + Grafana | Pod scrape endpoints |
| Logs | Fluent Bit → CloudWatch Logs | Sidecar containers |
| Traces | OpenTelemetry → Jaeger | Application instrumentation |
| Alerting | PagerDuty via Alertmanager | On critical SLO breach |

### 10. Key Design Decisions

- **Decision / Rationale / Alternatives / Consequences** — same format as other views.

---

## Common Mistakes to Avoid

- **Showing logical components, not running artefacts.** The physical view shows what actually runs and where — not conceptual components.
- **Missing network paths.** Every arrow in the diagram needs a protocol, port, and directionality.
- **Ignoring managed services.** RDS, MSK, S3 are nodes in the deployment diagram.
- **No security boundaries.** The physical view is where security architects look. Omitting security zones makes this view incomplete.
- **Single-AZ diagrams.** Unless the system is explicitly single-AZ, show the HA topology.

---

## Miro Prompt Pointer

When generating a Miro prompt for this view, read `examples/miro-physical-view-prompt.md`. Use nested frames for VPC/subnet hierarchy. Cloud provider icons should be consistent; specify the icon library (AWS or generic).
