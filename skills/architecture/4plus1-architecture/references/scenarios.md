# Scenarios (+1) View Reference

## Purpose

The scenarios view (the "+1") is the architectural glue that validates the other four views. A small, carefully chosen set of use cases demonstrates that the architecture can support the system's most critical and architecturally significant behaviours. These scenarios are not a full requirements specification — they are **architectural probes** that exercise the key elements across all views.

**Target audience:** All stakeholders — this is the most accessible view and the one used in architectural reviews and presentations.  
**Central question:** *Do the four architectural views, working together, support the scenarios that matter most?*

---

## Core Concepts

### Architecturally Significant Scenario
A use case or interaction that:
- Exercises a cross-cutting concern (security, caching, async processing)
- Tests a quality attribute (performance, resilience, scalability)
- Involves multiple processes or components in non-trivial coordination
- Represents a primary business flow that the architecture must not fail

Not every use case belongs here. Choose 5–10 scenarios that collectively exercise all major architectural elements.

### Scenario Selection Criteria
Select scenarios that hit at least two of the following:
- Involves 3+ architectural components
- Tests a quality attribute requirement
- Involves an async or distributed flow
- Has a non-trivial failure mode
- Is on the critical path for business continuity

---

## Document Structure

### 1. Audience Statement
Who reads this, and what it validates.

### 2. Scenario Selection Rationale

A paragraph explaining how scenarios were chosen and what they collectively cover. Map scenarios to architectural concerns:

| Scenario | Views Exercised | Quality Attribute Tested |
|----------|----------------|--------------------------|
| Place Order (happy path) | All four | Correctness, latency |
| Place Order under load | Process, Physical | Scalability, throughput |
| Payment service failure | Process, Physical | Resilience, fault tolerance |
| New product onboarding | Logical, Development | Extensibility, modularity |
| Audit log query | Logical, Physical | Security, data integrity |

### 3. Use Case Diagram

Show the actors and their primary use cases:

```
          ┌─────────────────────────────────────────┐
          │              E-Commerce System           │
          │                                         │
 Customer ─┤─► Place Order                          │
          │   ► Track Order                         │
          │   ► Return Item                         │
          │                                         │
  Merchant─┤─► Manage Inventory                     │
          │   ► View Reports                        │
          │                                         │
 Payment  │                                         │
 Gateway ─┤─► Process Payment (extend: Place Order) │
          │                                         │
          └─────────────────────────────────────────┘
```

### 4. Individual Scenario Descriptions

For each scenario, produce a structured narrative. Use this template:

---

#### Scenario N: [Name]

**Actor(s):** Who initiates this interaction  
**Preconditions:** System state before the scenario begins  
**Trigger:** What starts the flow  
**Quality Attributes Tested:** Latency / Resilience / Security / Scalability / Extensibility  

**Flow (numbered steps):**
1. Actor does X
2. System component A does Y
3. System component B responds with Z
4. ...

**Architectural Elements Exercised:**
- *Logical:* Which abstractions participate
- *Process:* Which processes are invoked and how they communicate
- *Development:* Which modules/components are involved
- *Physical:* Which nodes and communication paths are traversed

**Failure Path / Edge Cases:**
- What happens if step 3 times out?
- What happens if the data store is unavailable?

**Validation:** How this scenario can be tested / how the architecture demonstrates it supports this scenario

---

### 5. Interaction Overview Diagram

For complex scenarios with branching, produce an interaction overview — a hybrid of activity and sequence diagrams showing which sequence fragments are composed and in what order.

```
[Start]
  │
  ▼
[ref: Authenticate Customer] ──[auth fails]──> [Return 401]
  │
  ▼
[ref: Validate Cart and Reserve Inventory]
  │
  ├──[stock unavailable]──> [Notify: Out of Stock] ──> [End]
  │
  ▼
[ref: Process Payment]
  │
  ├──[payment declined]──> [Release Inventory] ──> [Return 402]
  │
  ▼
[ref: Create and Confirm Order]
  │
  ▼
[ref: Trigger Fulfilment and Notifications]
  │
  ▼
[End]
```

### 6. Architecture Validation Matrix

After all scenarios are documented, produce a matrix confirming coverage:

| Architectural Element | Scenarios That Exercise It |
|----------------------|---------------------------|
| `OrderService` | 1, 2, 3, 5 |
| `PaymentService` | 1, 2, 3 |
| `NotificationWorker` | 1, 4 |
| Kafka event bus | 1, 2, 3, 4 |
| Redis cache | 2 |
| RDS database | 1, 2, 3, 4, 5 |
| CloudFront CDN | 1, 2 |

Gaps in coverage are architectural risks — flag them.

### 7. Prototype / Testing Notes

For each scenario, note:
- Whether a performance test exists or is planned
- Whether a chaos engineering test covers the failure path
- Whether the scenario is part of the acceptance test suite

---

## Common Mistakes to Avoid

- **Treating this as a requirements catalogue.** The +1 view is a *sample*, not a complete list. 5–10 scenarios is the right scope.
- **Happy-path only.** Every scenario needs at least one documented failure path.
- **Not cross-referencing the other views.** Each scenario must explicitly name the logical abstractions, processes, components, and nodes it involves. Otherwise this view cannot validate the architecture.
- **Choosing low-risk scenarios.** The scenarios should stress the architecture. Picking easy flows provides no architectural validation.

---

## Miro Prompt Pointer

When generating a Miro prompt for this view, read `examples/miro-scenarios-prompt.md`. Each scenario should be its own frame. The use case diagram sits on the main canvas; individual scenario flows are in sub-frames laid out in a grid.
