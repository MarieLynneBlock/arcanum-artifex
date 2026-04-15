# Development View Reference

## Purpose

The development view describes the system from the **software developer and software manager's perspective** — how the codebase is organised, how teams own modules, and how the build and delivery pipeline is structured. It answers the question of what a developer navigates when working in the repository.

**Target audience:** Developers, software architects, engineering managers, DevSecOps  
**Central question:** *How is the software organised into modules, packages, and components, and how do teams own them?*

---

## Core Concepts

### Module
A unit of software that can be independently compiled, versioned, or tested. In practice: a library, a service, a package, a npm/pip/Maven module.

### Component
A coarser-grained unit that may contain multiple modules and exposes a defined interface. Corresponds to a deployable unit or a significant subsystem.

### Layer
A horizontal grouping by technical role (e.g., presentation, application, domain, infrastructure). Layers enforce dependency direction rules.

### Subsystem
A vertical slice of the architecture — a group of components that collaborate to deliver a bounded capability (e.g., "Order Management").

---

## Document Structure

### 1. Audience Statement
Who reads this and what development concern it addresses.

### 2. Repository / Monorepo Structure

Document the high-level source layout. If monorepo:
```
/
├── services/
│   ├── order-service/
│   ├── payment-service/
│   └── notification-service/
├── libs/
│   ├── common-events/
│   ├── auth-middleware/
│   └── observability/
├── infra/
│   ├── terraform/
│   └── helm/
└── docs/
```

If polyrepo, list repositories and their ownership.

### 3. Package Diagram

Show the primary packages/modules and their dependency relationships.

Dependency direction rule: state it explicitly. Example: "Domain packages must not depend on Infrastructure packages. Dependencies flow inward toward the domain."

```
[presentation-layer]
        │
        ▼
[application-layer]
        │
        ▼
  [domain-layer]
        ▲
        │
[infrastructure-layer]  ──> [external-libs]
```

For each package, document:
- Package name
- Owning team
- Primary responsibility
- External dependencies (third-party libraries worth naming)

### 4. Component Diagram

Show major deployable or reusable components, their exposed interfaces, and required interfaces.

Format:
```
┌──────────────────────────────┐
│       order-service          │
│                              │
│  [OrderController]           │
│       │                      │
│  [OrderApplicationService]   │
│       │                      │
│  [OrderRepository]──────────────> «interface» IOrderStore
│                              │
└──────────────────────────────┘
           │ requires
           ▼
    [PostgreSQL adapter]
```

### 5. Module Ownership Map

| Module / Package | Owning Team | Type | Key Dependencies |
|-----------------|-------------|------|-----------------|
| `order-service` | Order Squad | Service | `common-events`, `auth-middleware` |
| `payment-service` | Payments Squad | Service | `stripe-sdk`, `common-events` |
| `common-events` | Platform | Library | none |
| `auth-middleware` | Security | Library | `jwt-lib` |

### 6. Dependency Rules and Constraints

State the architectural constraints on dependencies:
- Allowed dependencies (e.g., "services may depend on libs; libs must not depend on services")
- Forbidden dependencies (e.g., "domain layer must not import from infrastructure layer")
- Version pinning policy (e.g., "all internal libs pinned to exact version; external libs allow patch bumps")
- Circular dependency policy (zero-tolerance / tooling enforced)

Name the tooling that enforces these rules (ArchUnit, Dependency Cruiser, deptry, etc.) if applicable.

### 7. Build and CI Pipeline Structure

Describe the build topology:
- Monorepo build tool (Nx, Turborepo, Bazel, Maven multi-module, etc.)
- Per-service build steps (lint → test → build → containerise → push)
- Shared build artefacts (base images, shared test fixtures)
- Cache strategy

```
[Source Push]
     │
     ▼
[Lint + Static Analysis] ──[fail]──> [PR blocked]
     │
     ▼
[Unit Tests]
     │
     ▼
[Build Container Image]
     │
     ▼
[Integration Tests]
     │
     ▼
[Push to Registry] ──> [Trigger CD pipeline]
```

### 8. Code Quality and Standards

Document the standards that govern this codebase:
- Code style enforcement (linter, formatter, pre-commit hooks)
- Test coverage thresholds (unit, integration, e2e)
- Static analysis tools (SAST, dependency scanning, secret detection)
- Review requirements (required approvers, automated checks)

### 9. Key Design Decisions

For each significant structural decision:
- **Decision:** (e.g., "monorepo over polyrepo")
- **Rationale:** (e.g., "atomic commits across shared libraries, single CI config")
- **Alternatives considered:**
- **Consequences:** (e.g., "requires Nx for selective builds; onboarding complexity increases")

---

## Common Mistakes to Avoid

- **Confusing development and physical views.** This view is about source code organisation, not runtime deployment. A `payment-service` component here is a codebase unit; in the physical view it is a running container.
- **Ignoring team ownership.** The development view should make clear who owns what. Ownership gaps are architectural risks.
- **Missing dependency direction rules.** Without explicit rules, dependency graphs become cyclic over time.
- **Over-detailing internal class structure.** That belongs in the logical view. This view operates at module and component granularity.

---

## Miro Prompt Pointer

When generating a Miro prompt for this view, read `examples/miro-development-view-prompt.md`. The component diagram layout and team ownership colour-coding are the most important visual elements.
