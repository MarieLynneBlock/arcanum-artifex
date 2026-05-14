# Mermaid notation cheatsheet

Mermaid is the primary diagram language for this skill. It renders natively in GitHub, VS Code, Claude artefacts, Obsidian, Notion, Confluence (with the plugin), and every major IDE. Text-based, diff-friendly, LLM-authorable.

Mermaid version assumed: **10+**. Earlier versions lack the C4 diagrams and some flowchart features.

## Which Mermaid diagram for which view

| View | Audience (a) dev | Audience (b) cross-fn | Audience (c) exec |
|------|-----------------|-----------------------|-------------------|
| Logical | `classDiagram` or `C4Container` | `C4Container` | `C4Context` |
| Process | `sequenceDiagram` | `flowchart` w/ swimlane subgraphs | `flowchart LR` (high-level) |
| Development | `flowchart TB` | `flowchart TB` w/ team labels | (usually skip) |
| Physical | `C4Deployment` (fallback — see `notation-plantuml.md` for primary) | `C4Deployment` simplified | `C4Deployment` at environment level |
| Scenarios | `sequenceDiagram` per scenario | `flowchart` per scenario | prose + overview `flowchart` |

## Essential flowchart syntax

```
flowchart TB     # top-to-bottom
flowchart LR     # left-to-right
flowchart RL     # right-to-left
flowchart BT     # bottom-to-top
```

**Node shapes:**
```
A[Rectangle]
B(Rounded rectangle)
C([Stadium — for start/end events])
D[[Subroutine]]
E[(Database / cylinder)]
F((Circle — for events))
G{Diamond / gateway}
H{{Hexagon}}
I>Asymmetric / flag]
J[/Parallelogram — for I/O/]
K[\Reverse parallelogram\]
```

**Edges:**
```
A --> B          # solid arrow
A --- B          # solid line, no arrow
A -.-> B         # dashed arrow (use for async / message flow)
A ==> B          # thick arrow (use sparingly for emphasis)
A -->|label| B   # labelled arrow
A == text ==> B  # thick labelled
```

**Subgraphs (use for swimlanes and layers):**
```
subgraph lane1["Swimlane name"]
    A --> B
end
subgraph lane2["Another lane"]
    C --> D
end
B -.-> C          # cross-lane message flow
```

**Styling (keep minimal — colours should be semantic, not decorative):**
```
classDef external fill:#e0e0e0,stroke:#666,stroke-dasharray:5 5
classDef critical fill:#fff4e6,stroke:#d46b08
class A,B external
class C critical
```

## Sequence diagram syntax

```
sequenceDiagram
    autonumber
    actor User
    participant Web as Web Application
    participant API as API Gateway
    participant Svc as Service
    participant DB as Datastore

    User->>Web: HTTP request
    Web->>API: forward (JWT)
    activate API
    API->>Svc: route
    Svc->>DB: query
    DB-->>Svc: result
    Svc-->>API: response
    deactivate API
    API-->>Web: response
    Web-->>User: render

    Note over Svc,DB: Query latency target p99 < 50 ms

    alt success
        Svc-->>API: 200
    else validation error
        Svc-->>API: 400
    else upstream failure
        Svc-->>API: 503
    end

    loop every 30s
        Svc->>DB: healthcheck
    end

    opt feature flag enabled
        Svc-)Q: publish event
    end
```

**Arrow types:**
- `->>` solid with arrowhead — synchronous call
- `-->>` dashed with arrowhead — synchronous response
- `-)` solid with open arrow — async / fire-and-forget
- `--)` dashed open arrow — async response

## Class diagram syntax

```
classDiagram
    class ClaimSubmission {
        +UUID id
        +DateTime submittedAt
        +ClaimStatus status
        +submit()
        +validate() bool
    }
    class Claim {
        +UUID id
        +Customer customer
        +Money amount
    }
    class Customer {
        +UUID id
        +String name
    }

    ClaimSubmission "1" --> "1" Claim : creates
    Claim "*" --> "1" Customer : belongs to
```

Relationships:
- `<|--` inheritance
- `*--` composition
- `o--` aggregation
- `-->` directed association
- `--` association (undirected)
- `..>` dependency (dashed)
- `..|>` realisation / implements

## C4 diagram syntax

Mermaid supports three C4 levels: `C4Context`, `C4Container`, `C4Component`. Also `C4Deployment`.

```
C4Context
    title System Context — [System]

    Person(customer, "Customer", "End user who submits claims")
    Person(adjudicator, "Adjudicator", "Internal role reviewing claims")

    System(sys, "Claims Platform", "Handles the full claims lifecycle")

    System_Ext(payment, "Payment gateway", "Third-party")
    System_Ext(idp, "Identity provider", "SSO")

    Rel(customer, sys, "Submits and tracks claims")
    Rel(adjudicator, sys, "Reviews and approves")
    Rel(sys, payment, "Initiates payments", "REST/HTTPS")
    Rel(sys, idp, "Authenticates users", "OIDC")
```

```
C4Container
    title Container — [System]

    Person(user, "User")

    System_Boundary(sys, "Claims Platform") {
        Container(web, "Web App", "React", "SPA for users")
        Container(api, "API Gateway", "Kong", "AuthZ and rate-limit")
        Container(svc, "Claims Service", "Java/Spring", "Business logic")
        ContainerDb(db, "Claims DB", "PostgreSQL", "Claims and adjudication state")
        ContainerQueue(q, "Event bus", "Kafka", "Domain events")
    }

    System_Ext(pay, "Payment gateway")

    Rel(user, web, "Uses", "HTTPS")
    Rel(web, api, "JSON/HTTPS")
    Rel(api, svc, "gRPC")
    Rel(svc, db, "SQL/TLS")
    Rel(svc, q, "publishes")
    Rel(svc, pay, "REST", "mTLS")
```

```
C4Deployment
    title Deployment — [System] — Production

    Deployment_Node(aws, "AWS eu-west-1", "Cloud region") {
        Deployment_Node(vpc, "prod-vpc", "VPC") {
            Deployment_Node(ecs, "ECS Fargate", "Container runtime") {
                Container(svc, "Claims Service", "Java/Spring")
            }
            ContainerDb(db, "RDS", "PostgreSQL 16 Multi-AZ")
        }
    }
    Rel(svc, db, "TLS, 5432")
```

## State diagram syntax (for business-state transitions)

```
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted : submit
    Submitted --> UnderReview : assign
    UnderReview --> Approved : approve
    UnderReview --> Rejected : reject
    UnderReview --> NeedsInfo : request info
    NeedsInfo --> UnderReview : info supplied
    Approved --> Paid : payment executed
    Paid --> [*]
    Rejected --> [*]
```

## Rendering notes

- GitHub renders all of the above in Markdown fenced blocks tagged `mermaid` or in `.mmd` files.
- VS Code needs the "Markdown Preview Mermaid Support" or "Mermaid Preview" extension.
- Claude.ai renders Mermaid natively in artefacts.
- For CI-time rendering to PNG/SVG, use `mermaid-cli` (`mmdc`).
- Keep diagrams under ~30 nodes. Over that, split into multiple diagrams.

## Common mistakes

- **Inconsistent participant/container names across diagrams.** Use the same name for the same thing in every view.
- **Using sequence diagrams for static structure.** Sequence is runtime only.
- **Overusing colour.** Colours should encode meaning (external vs internal, critical vs normal). Random colouring is noise.
- **Too wide.** For left-to-right flowcharts, break into stacked sections if the diagram exceeds ~10 nodes horizontally.
