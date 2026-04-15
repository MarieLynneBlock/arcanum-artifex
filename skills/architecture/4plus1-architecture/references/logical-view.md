# Logical View Reference

## Purpose

The logical view describes **what the system does** from the perspective of end-users and business analysts. It captures functional decomposition — the key abstractions that the system is built around — without concern for how they are implemented or where they run.

**Target audience:** End-users, business analysts, product owners, QA engineers  
**Central question:** *What are the key responsibilities of the system and how are they organised?*

---

## Core Concepts

### Key Abstractions

Identify the 5–15 most important domain objects or service clusters. These are the nouns that stakeholders use in conversation. They are not database tables or API endpoints — they are conceptual entities.

Examples: `Order`, `Customer`, `PaymentGateway`, `InventoryManager`, `NotificationService`

### Mechanisms

Mechanisms are reusable design patterns applied across the system. Document them here so they don't get re-explained in every class:
- **Observer / Event pattern** — how domain events propagate
- **Strategy pattern** — pluggable algorithms (e.g., pricing rules)
- **Repository pattern** — data access abstraction

---

## Document Structure

Every Logical View document MUST include all of the following sections.

### 1. Audience Statement
One sentence: who reads this and what decision it supports.

### 2. System Overview
2–3 sentences describing the system's domain and primary function.

### 3. Key Abstractions Table

| Abstraction | Responsibility | Collaborators |
|-------------|---------------|---------------|
| `ClassName` | What it owns and does | Other classes it talks to |

Aim for 8–15 abstractions. If fewer than 5, the decomposition is too coarse. If more than 20, split into sub-packages.

### 4. Package / Subsystem Decomposition

Group abstractions into logical packages or domains. Describe each package's bounded responsibility. Draw or describe the package diagram:

```
[PackageA] ──uses──> [PackageB]
[PackageA] ──uses──> [PackageC]
[PackageB] ──inherits── [PackageD]
```

For text representation use: `──uses──>`, `──inherits──>`, `──realizes──>`, `──depends──>`

### 5. Class Diagram (key relationships)

Select the 10 most important classes. For each relationship, state:
- Relationship type (association, aggregation, composition, inheritance, realisation, dependency)
- Multiplicity (1, 0..*, 1..*)
- Role names if meaningful

Format:
```
[Order] 1 ──contains──> * [OrderLine]
[OrderLine] * ──references──> 1 [Product]
[Order] ──realizes──> [Purchasable]
```

### 6. State Diagrams (for stateful entities)

For any entity with meaningful lifecycle states, document:
- Initial state
- Terminal state(s)
- All transitions with trigger events and guard conditions

Format:
```
[Created] ──payment_received──> [Confirmed]
[Confirmed] ──items_allocated──> [Processing]
[Processing] ──shipped──> [Dispatched]
[Dispatched] ──delivered / [7 days elapsed]──> [Completed]
[Confirmed | Processing] ──cancel_requested──> [Cancelled]
```

### 7. Architectural Mechanisms Applied

List which system-wide mechanisms (from the mechanisms catalogue) apply to this view, with a brief note on how.

### 8. Key Design Decisions

For each significant decision, document:
- **Decision:** What was decided
- **Rationale:** Why (reference quality attributes if applicable)
- **Alternatives considered:** What else was evaluated
- **Consequences:** Trade-offs accepted

---

## Common Mistakes to Avoid

- **Confusing logical and development views.** Packages here are domain concepts, not source code modules. A `payments` package is a business domain, not a directory.
- **Including infrastructure.** Databases, message brokers, and servers belong in the physical view. The logical view has none.
- **Over-specifying methods.** Class diagrams in this view show responsibilities and relationships, not every getter/setter.
- **Single monolithic diagram.** Large systems need layered diagrams: one overview + one per major subsystem.

---

## UML Notation Quick Reference

| Relationship | Arrow | Meaning |
|---|---|---|
| Association | `──────>` | Knows about / uses |
| Aggregation | `◇──────>` | Has (weak ownership) |
| Composition | `◆──────>` | Owns (strong, lifecycle-coupled) |
| Inheritance | `──────▷` | Is-a (generalisation) |
| Realisation | `- - - -▷` | Implements interface |
| Dependency | `- - - ->` | Uses temporarily |

---

## Miro Prompt Pointer

When generating a Miro prompt for this view, read `examples/miro-logical-view-prompt.md`. Pay particular attention to the colour scheme for relationship types and the frame layout for packages.
