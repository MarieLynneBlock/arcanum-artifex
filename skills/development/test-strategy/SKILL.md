---
description: >
name: test-strategy
version: 1.0.0
tags:
  - testing
  - test-strategy
  - quality
  - tdd
  - ci
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Produces a test strategy document defining what to test, at which layer, with which tools, and to what coverage standard. It applies the test pyramid model, surfaces coverage gaps in existing codebases, and produces a concrete plan — not a generic "write more tests" recommendation.

## When to use it

- User asks to "define a test strategy", "how should we test this?", or "what tests do we need?".
- A new feature or system needs a testing approach defined before implementation.
- A codebase has poor or uneven test coverage and needs a plan to address it.
- A team is establishing testing standards and needs a reference document.
- User wants to review existing tests against a strategy.

## Key concepts

### Test pyramid

```
        ╱‾‾‾‾‾‾‾‾‾‾‾‾╲
       ╱  End-to-end   ╲     Few, slow, high confidence on critical paths
      ╱‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾╲
     ╱    Integration     ╲   Moderate, test component boundaries and contracts
    ╱‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾╲
   ╱         Unit            ╲  Many, fast, test logic in isolation
  ╲____________________________╱
```

| Layer | What it tests | Speed | Cost | Quantity |
| --- | --- | --- | --- | --- |
| **Unit** | Individual functions, classes, pure logic | Fast | Low | Many |
| **Integration** | Component interactions, DB queries, API calls, message handling | Medium | Medium | Moderate |
| **Contract** | API contracts between services (consumer-driven) | Fast | Low | As needed |
| **End-to-end** | Full user journeys through a running system | Slow | High | Few |
| **Performance** | Response times, throughput, load behaviour | Slow | High | Targeted |
| **Security** | Authentication, authorisation, injection, exposure | Variable | Medium | Targeted |

### Coverage goals

Coverage percentage is a floor, not a target. Define coverage by **risk area**, not by line count:

- **Critical paths** (payment, auth, data writes): high unit + integration coverage, at least one E2E.
- **Business logic**: high unit coverage.
- **Infrastructure/glue code**: integration coverage, minimal unit.
- **UI rendering**: smoke E2E, visual regression if applicable.

### Test quality signals

Good tests are:
- **Fast** — slow tests don't get run.
- **Isolated** — one reason to fail.
- **Deterministic** — same result every run.
- **Readable** — failure message explains what went wrong without reading the code.
- **Maintained** — treated as production code, not an afterthought.

## Instructions

1. **Understand the system.** What type of system is this (API, frontend, data pipeline, monolith, microservices)? What are the critical paths?

2. **Assess existing coverage** (if any). What layers are covered? What is missing? What is flaky or untrusted?

3. **Define the strategy per layer.** For each applicable layer: what to test, what tooling to use, and what the coverage goal is.

4. **Identify the highest-risk gaps.** Where would a bug cause the most damage? Those areas get the most test investment.

5. **Recommend tooling.** Suggest concrete tools appropriate to the language and stack. Do not be prescriptive about a tool the user has already chosen otherwise.

6. **Define CI integration.** Which layers run on every commit? Which run on PR? Which run nightly?

7. **Produce the document** using the output format below.

## Output format

```markdown
# Test Strategy: [System / Feature name]

**Date:** YYYY-MM-DD  
**Author:** [name]  
**Stack:** [language, framework, key dependencies]

---

## Objectives

- [What this strategy aims to achieve — e.g. "Catch regressions in the payment flow before deployment"]

## Scope

**In scope:** [What will be tested under this strategy]  
**Out of scope:** [What will not be — and why]

---

## Test layers

### Unit tests

**What:** [What logic is unit tested]  
**Tools:** [e.g. pytest, JUnit, Jest]  
**Coverage goal:** [e.g. 80% line coverage on business logic modules]  
**Mocking strategy:** [What is mocked and what is not]

### Integration tests

**What:** [What boundaries are tested — DB, external APIs, message queues]  
**Tools:** [e.g. Testcontainers, pytest-django, Supertest]  
**Coverage goal:** [e.g. all repository methods, all HTTP handlers]  
**Environment:** [e.g. real DB in Docker, stubbed external APIs]

### Contract tests

**What:** [Which service boundaries have contracts]  
**Tools:** [e.g. Pact]  
**Coverage goal:** [e.g. all consumer-defined contracts verified on provider CI]

### End-to-end tests

**What:** [Critical user journeys — keep this list short]  
**Tools:** [e.g. Playwright, Cypress, Selenium]  
**Coverage goal:** [e.g. 3–5 critical journeys: login, checkout, password reset]  
**Environment:** [e.g. staging with seeded data]

### Performance tests *(if applicable)*

**What:** [Endpoints or flows with performance NFRs]  
**Tools:** [e.g. k6, Locust, JMeter]  
**Thresholds:** [e.g. p95 < 200ms at 100 RPS]

### Security tests *(if applicable)*

**What:** [Auth flows, input validation, data exposure]  
**Tools:** [e.g. OWASP ZAP, Bandit, Semgrep]

---

## Coverage gaps (existing codebase)

| Area | Current state | Gap | Priority |
| --- | --- | --- | --- |
| [Module / feature] | [e.g. no tests] | [What is missing] | High / Medium / Low |

---

## CI integration

| Layer | Trigger | Blocking? |
| --- | --- | --- |
| Unit | Every commit | Yes |
| Integration | PR | Yes |
| E2E | PR / nightly | PR: smoke only; nightly: full suite |
| Performance | Nightly | No (alert on regression) |

---

## Definition of done for tests

- [ ] New code has unit tests covering the happy path and at least one edge case.
- [ ] New API endpoints have integration tests.
- [ ] New critical user journeys have an E2E smoke test.
- [ ] No new flaky tests introduced.
- [ ] Test names describe the scenario, not the implementation.
```

## Examples

### Example 1 — REST API test strategy

**Input:** "Define a test strategy for a Python FastAPI service with a PostgreSQL database."

**Expected output:** Unit layer covering service/business logic (pytest, no DB). Integration layer covering routers and repositories (pytest + Testcontainers with real Postgres). No contract tests (single consumer). E2E limited to two critical journeys. CI: unit + integration on every PR, E2E nightly.

### Example 2 — Frontend test strategy

**Input:** "What's the right test strategy for a React frontend with a REST API backend?"

**Expected output:** Unit layer for utility functions and hooks (Jest + Testing Library). Component tests for complex interactive components. No true unit tests for pure render — that's over-testing. E2E for critical user journeys (Playwright). Contract tests for API calls if the backend is separately deployed. Note on avoiding snapshot tests as a default.

### Example 3 — Coverage gap analysis

**Input:** "We have a Node.js service with 95% line coverage but bugs keep reaching production."

**Expected output:** Coverage gap analysis noting that line coverage measures execution, not correctness. Findings: likely over-mocked unit tests, missing integration tests on DB layer, no E2E on critical paths. Recommendations: reduce mocking at the service boundary, add Testcontainers integration tests, add two E2E smoke tests.

## Notes

- High unit coverage with heavy mocking often means the tests test the mocks, not the system. Integration tests on real dependencies catch more production bugs per test written.
- E2E tests are valuable but expensive to maintain. Keep the suite small and focused on the paths that, if broken, would cause the most user harm.
- Flaky tests are worse than no tests — they erode trust in the suite and lead teams to ignore failures. A strategy should include a flaky test policy (quarantine, fix within N days, or delete).
- This skill pairs with `acceptance-test-plan` (E2E and UAT scenarios) and `requirements-document` (NFRs drive performance and security test thresholds).
