---
name: requirements-document
description: >-
  Generates a Business Requirements Document (BRD) or Functional Requirements Specification (FRS)
  skeleton populated from the user's input. It structures requirements with unique IDs, priority,
  source, and acceptance notes — making them traceable and reviewable.
version: 1.0.0
tags:
  - requirements
  - brd
  - frs
  - functional-specification
  - documentation
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Generates a Business Requirements Document (BRD) or Functional Requirements Specification (FRS) skeleton populated from the user's input. It structures requirements with unique IDs, priority, source, and acceptance notes — making them traceable and reviewable.

## When to use it

- User asks to "write a requirements document", "produce a BRD", or "create a functional spec".
- A project needs formal requirements sign-off before design or build begins.
- Requirements must be traceable to use cases, test cases, or regulatory obligations.
- User wants to consolidate user stories, use cases, and constraints into a single document.

## Key concepts

### BRD vs. FRS

| | BRD — Business Requirements Document | FRS — Functional Requirements Specification |
| --- | --- | --- |
| **Audience** | Business stakeholders, project sponsors | Solution architects, developers, testers |
| **Focus** | What the business needs and why | What the system must do |
| **Language** | Business language | Technical/functional language |
| **Produced by** | Business analyst | Functional/technical analyst |
| **Input to** | FRS, project charter | Design specs, test plans |

This skill produces **both in a single document** unless the user specifies one type only.

### Requirement types

| Type | Description | Prefix |
| --- | --- | --- |
| Business requirement | High-level business need or goal | BR- |
| Functional requirement | Specific system behaviour | FR- |
| Non-functional requirement | Quality attributes (performance, security, etc.) | NFR- |
| Constraint | Fixed boundary (budget, regulation, tech stack) | CON- |
| Assumption | Stated truth that has not been verified | ASM- |

### Priority

Use MoSCoW: **Must have** / **Should have** / **Could have** / **Won't have (this release)**.

## Instructions

1. **Establish document metadata.** Project name, author, version, date, approvers.

2. **Write the business context.** Problem statement, business objectives, and scope. Draw from the user's input or the output of a `write-epic` or `gap-analysis`.

3. **Identify stakeholders.** Reference `stakeholder-map` output if available, or list roles.

4. **Document business requirements (BR-).** High-level needs expressed in business terms. Each BR maps to one or more FRs.

5. **Document functional requirements (FR-).** One behaviour per requirement. Each FR must be:
   - **Specific** — no ambiguous language ("the system shall display the order total" not "the system shall handle orders well").
   - **Measurable** — include a threshold where relevant ("within 2 seconds").
   - **Traceable** — reference the BR it satisfies.
   - **Testable** — a tester should be able to confirm it passes or fails.

6. **Document non-functional requirements (NFR-).** Cover relevant quality attributes: performance, scalability, security, availability, usability, maintainability, compliance.

7. **Document constraints (CON-).** Fixed boundaries the solution must operate within.

8. **Document assumptions (ASM-).** Statements assumed true; if proven false, requirements may change.

9. **Add open issues.** Requirements not yet agreed or information still needed.

10. **Produce the document** using the format below.

## Output format

```markdown
# Requirements Document: [Project / System name]

| Field | Detail |
| --- | --- |
| **Version** | 0.1 — Draft |
| **Date** | YYYY-MM-DD |
| **Author** | [name] |
| **Status** | Draft / In review / Approved |
| **Approvers** | [names or roles] |

---

## 1. Business context

### 1.1 Problem statement

[What problem is being solved and for whom.]

### 1.2 Business objectives

1. [Objective 1]
2. [Objective 2]

### 1.3 Scope

**In scope:** [What this project / system covers]  
**Out of scope:** [What is explicitly excluded]

---

## 2. Stakeholders

| Stakeholder | Role | Interest |
| --- | --- | --- |
| [Name / role] | [Team] | [What they need from this project] |

---

## 3. Business requirements

| ID | Requirement | Priority | Source |
| --- | --- | --- | --- |
| BR-001 | [The business need in business language] | Must have | [Stakeholder / regulation] |

---

## 4. Functional requirements

| ID | Requirement | Priority | Traces to | Notes |
| --- | --- | --- | --- | --- |
| FR-001 | The system shall [behaviour] [condition] [threshold]. | Must have | BR-001 | [Clarification or constraint] |
| FR-002 | The system shall [behaviour]. | Should have | BR-001 | |

---

## 5. Non-functional requirements

| ID | Category | Requirement | Priority |
| --- | --- | --- | --- |
| NFR-001 | Performance | [The system shall respond to [action] within [N] seconds under [load].] | Must have |
| NFR-002 | Security | [The system shall [security behaviour].] | Must have |
| NFR-003 | Availability | [The system shall achieve [N]% uptime per [period].] | Should have |

---

## 6. Constraints

| ID | Constraint |
| --- | --- |
| CON-001 | [Fixed boundary — technology, budget, regulation, timeline] |

---

## 7. Assumptions

| ID | Assumption | Impact if false |
| --- | --- | --- |
| ASM-001 | [Stated truth not yet verified] | [What changes if this is wrong] |

---

## 8. Open issues

| ID | Issue | Owner | Due |
| --- | --- | --- | --- |
| OI-001 | [Unresolved requirement or missing information] | [Role] | [Date or TBD] |

---

## Appendix: Traceability matrix

| BR | FR(s) | Use case(s) | Test case(s) |
| --- | --- | --- | --- |
| BR-001 | FR-001, FR-002 | UC-001 | TC-001, TC-002 |
```

## Examples

### Example 1 — Customer portal BRD

**Input:** "Write a BRD for a self-service customer portal where customers can view invoices, raise support tickets, and update their contact details."

**Expected output:** Business context with three objectives (reduce support calls, improve data accuracy, increase customer satisfaction). BR-001 to BR-003 per capability. FR-001 to FR-009 specifying system behaviours. NFRs covering session timeout (security), page load time (performance), and WCAG 2.1 AA (accessibility).

### Example 2 — Building from other skill outputs

**Input:** User provides output from `write-epic` and `gap-analysis`.

**Expected output:** Requirements document where BRs map to epic goals, FRs address the gaps, and constraints come from the epic's out-of-scope section. Traceability matrix pre-populated.

## Notes

- Write FRs using "The system shall…" (mandatory) or "The system should…" (desirable). Avoid "must", "will", or "can" — they have ambiguous force.
- Every FR must be testable. If you cannot write a test that would fail if the FR is not met, the FR is not specific enough.
- Version the document. Requirements change — v0.1 Draft → v0.2 In review → v1.0 Approved.
- This skill integrates with `use-case` (FRs and use cases should be mutually traceable), `acceptance-test-plan` (FRs drive test cases), and `gap-analysis` (gaps become requirements).
