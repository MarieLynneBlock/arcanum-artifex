---
name: acceptance-test-plan
description: >
  Generate a structured acceptance test plan with test cases derived from user
  stories, use cases, or functional requirements — covering happy paths, edge
  cases, and negative scenarios. Use when a user needs to verify that a feature
  or system meets its stated requirements before sign-off.
version: 1.0.0
authors:
  - Marie-Lynne Block
tags:
  - testing
  - acceptance
  - test-plan
  - quality
  - requirements
---

## What this skill does

Produces a traceable acceptance test plan with individually numbered test cases. Each test case maps to a source requirement (user story, use case, or FR), specifies preconditions, steps, and expected results, and includes coverage of the happy path, edge cases, and negative scenarios.

## When to use it

- User asks to "write a test plan", "create acceptance tests", or "define test cases" for a feature or system.
- A sprint is nearing completion and the team needs acceptance criteria turned into formal tests.
- A stakeholder or client needs documented evidence that acceptance criteria have been verified.
- User is preparing for UAT (User Acceptance Testing) and needs a test script.
- Use cases or functional requirements from a `requirements-document` need test coverage.

## Key concepts

### Test case anatomy

| Field | Description |
| --- | --- |
| **ID** | Unique identifier (TC-NNN) |
| **Title** | Short description of what is being tested |
| **Source** | The story, use case, or FR this test covers |
| **Type** | Happy path / Edge case / Negative / Performance / Security |
| **Priority** | Critical / High / Medium / Low |
| **Preconditions** | State the system must be in before the test starts |
| **Test steps** | Numbered actions the tester performs |
| **Expected result** | What should happen if the system behaves correctly |
| **Pass / Fail** | To be filled in during test execution |

### Coverage types

| Type | Purpose |
| --- | --- |
| **Happy path** | The main success scenario — everything goes right |
| **Edge case** | Boundary values, limits, and unusual-but-valid inputs |
| **Negative** | Invalid inputs, missing data, unauthorised access — system must handle gracefully |
| **Performance** | Response times, load behaviour — only if NFRs specify thresholds |
| **Security** | Access control, injection, data exposure — only if security NFRs are in scope |

### Minimum coverage rule

For every acceptance criterion or FR: at least one happy path test **and** at least one negative or edge case test.

## Instructions

1. **Identify the source material.** User stories (with acceptance criteria), use cases, or functional requirements. If none are provided, ask before writing tests.

2. **Define the test scope.** Which stories, FRs, or use cases are in scope for this plan?

3. **Identify test types needed.** At minimum: happy path and negative. Add edge cases for inputs with boundaries, performance tests if NFRs specify thresholds, and security tests if access control is in scope.

4. **Write test cases.** For each acceptance criterion or FR:
   - Write the happy path test first.
   - Write at least one negative or edge case test.
   - Assign priority based on risk: Critical for core flows, High for error handling, Medium/Low for cosmetic or informational behaviour.

5. **Write preconditions precisely.** The tester must be able to set up the exact state without ambiguity.

6. **Write expected results precisely.** Not "it works" — describe the exact system response: message text, state change, data written, redirect destination.

7. **Build the traceability matrix.** Map each test case to its source requirement.

8. **Produce the report** using the format below.

## Output format

```markdown
# Acceptance Test Plan: [Feature / System name]

| Field | Detail |
| --- | --- |
| **Version** | 0.1 |
| **Date** | YYYY-MM-DD |
| **Author** | [name] |
| **Source requirements** | [Story IDs / UC IDs / FR IDs] |
| **Test environment** | [e.g., staging, QA environment] |
| **Tester** | [name or role] |

---

## Test summary

| Type | Count |
| --- | --- |
| Happy path | n |
| Edge case | n |
| Negative | n |
| Performance | n |
| Security | n |
| **Total** | **n** |

---

## Test cases

### TC-001 — [Title]

| Field | Detail |
| --- | --- |
| **Source** | [US-01 / UC-001 / FR-001] |
| **Type** | Happy path |
| **Priority** | Critical |
| **Preconditions** | [Exact system state required] |

**Steps:**

1. [Action the tester takes]
2. [Action the tester takes]
3. [Action the tester takes]

**Expected result:** [Precise description of what the system should do or display]

**Pass / Fail:** ___

---

### TC-002 — [Title]

| Field | Detail |
| --- | --- |
| **Source** | [US-01 / UC-001 / FR-001] |
| **Type** | Negative |
| **Priority** | High |
| **Preconditions** | [Exact system state required] |

**Steps:**

1. [Action]
2. [Action — with invalid/missing input]

**Expected result:** [Error message, rejection behaviour, or graceful degradation]

**Pass / Fail:** ___

---

## Traceability matrix

| Source | Test case(s) | Coverage |
| --- | --- | --- |
| US-01 AC1 | TC-001, TC-002 | Happy path + negative |
| US-01 AC2 | TC-003 | Happy path |
| FR-001 | TC-004, TC-005 | Happy path + edge case |

---

## Risks and assumptions

- [Any test environment limitations that may affect results]
- [Data dependencies or setup requirements]
- [Out-of-scope test types and why]
```

## Examples

### Example 1 — Login feature acceptance tests

**Input:** User story: "As a registered user, I want to log in with my email and password so that I can access my account." Acceptance criteria: valid credentials grant access; invalid credentials show an error; account locks after 5 failed attempts.

**Expected output:**
- TC-001 (Happy path): valid email + password → redirected to dashboard.
- TC-002 (Negative): invalid password → "Incorrect email or password" message shown, account not locked.
- TC-003 (Edge case): 5th consecutive failed attempt → account locked, user shown lockout message, email sent.
- TC-004 (Edge case): empty email field → form validation error before submission.

### Example 2 — From use case output

**Input:** Use case UC-001 (Place order) with main flow and 3 extensions.

**Expected output:** TC-001 covers main success scenario. TC-002 covers extension 4a (out of stock). TC-003 covers extension 5a (payment declined). TC-004 covers extension 5b (payment timeout). Traceability matrix links all TCs to UC-001 steps.

## Notes

- Test steps should be executable by someone unfamiliar with the system. Avoid "navigate to the order page" — write "open a browser, go to [URL], click 'My Orders'."
- Expected results must be deterministic. If the result varies by data state, specify the data setup in preconditions.
- Do not test implementation details (internal function calls, database queries). Test observable system behaviour only.
- This skill integrates with `use-case` (each extension → a test case), `requirements-document` (FRs → test cases in the traceability matrix), and `write-user-story` (acceptance criteria → test cases).
