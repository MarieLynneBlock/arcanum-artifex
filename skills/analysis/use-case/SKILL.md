---
description: >
name: use-case
version: 1.0.0
tags:
  - use-case
  - requirements
  - uml
  - specification
  - functional-analysis
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Produces a complete use case following the Cockburn/RUP format. A use case describes a goal-directed interaction between an actor and the system — capturing not just the happy path, but the extension flows (error, alternative, and exception paths) that user stories typically omit.

## When to use it

- User asks to "write a use case" or needs more rigorous specification than a user story.
- The interaction involves complex branching, multiple actors, or system-to-system calls.
- The requirement must satisfy a compliance, audit, or contractual standard that demands formal documentation.
- User is breaking down a user story that is too complex to estimate because its edge cases are unknown.
- Use cases are being collected for a system specification or `requirements-document`.

## Key concepts

### Use case vs. user story

| | User story | Use case |
| --- | --- | --- |
| **Format** | Persona / want / benefit | Goal / actors / flows |
| **Scope** | One sprint | One interaction goal |
| **Detail** | Acceptance criteria | Full flow + all extensions |
| **Audience** | Agile team | Analyst, architect, tester |
| **Best for** | Feature cards, backlog | Complex interactions, specs |

### Use case components

| Component | Description |
| --- | --- |
| **Use case ID** | Unique identifier (e.g., UC-001) |
| **Name** | Active verb + noun (e.g., "Place order", "Reset password") |
| **Goal** | The outcome the primary actor wants to achieve |
| **Primary actor** | Who initiates the interaction |
| **Secondary actors** | Other systems or roles involved |
| **Preconditions** | What must be true before the use case can start |
| **Postconditions (success)** | System state after successful completion |
| **Postconditions (failure)** | System state if the use case fails |
| **Main success scenario** | The happy path — numbered steps |
| **Extensions** | Deviations from the main flow (errors, alternatives) |
| **Business rules** | Constraints that govern the flow |
| **Notes / open questions** | Assumptions or items needing clarification |

### Extension notation

Extensions are written as `[step number][condition]`:

```
3a. Payment is declined:
    3a1. System displays "Payment failed" message.
    3a2. User is offered the option to retry or cancel.
    3a3. If user cancels, go to step 9 (failure).
```

## Instructions

1. **Assign an ID and name.** Use the format UC-NNN. Name with active verb + object.

2. **State the goal.** One sentence: what the primary actor wants to achieve.

3. **Identify actors.**
   - Primary actor: who triggers the use case.
   - Secondary actors: systems, services, or roles that participate but don't initiate.

4. **Write preconditions.** List the conditions that must be true for the use case to start. Be specific — not "user is logged in" but "user has an active session with at least Reader role".

5. **Write the main success scenario.** Numbered steps, each in the form "Actor does something" or "System does something". Include all steps from trigger to goal achieved.
   - Keep steps at the same level of abstraction.
   - One action per step.
   - Do not embed conditions in the main flow — move them to extensions.

6. **Write extensions.** For each step that can deviate, write the condition and the sub-flow. Reference back to the main flow where it resumes.

7. **Write postconditions.** What is true after success? What is true after failure/cancellation?

8. **List business rules.** Numbered, referenced from the relevant steps.

9. **Produce the output** using the format below.

## Output format

```markdown
## Use Case: [UC-NNN] — [Name]

| Field | Detail |
| --- | --- |
| **ID** | UC-NNN |
| **Name** | [Active verb + noun] |
| **Goal** | [What the primary actor wants to achieve] |
| **Primary actor** | [Role or persona] |
| **Secondary actors** | [System / service / role] |
| **Preconditions** | [Numbered list] |
| **Postconditions (success)** | [System state after success] |
| **Postconditions (failure)** | [System state after failure or cancellation] |

---

### Main success scenario

1. [Actor] [action].
2. System [response].
3. [Actor] [action].
4. System validates [X] against [BR-01].
5. System [response].
6. Goal achieved: [outcome].

---

### Extensions

**3a.** [Condition at step 3]:
  - 3a1. System [response].
  - 3a2. [Actor] [option]. Use case resumes at step 3 / ends in failure.

**4a.** [Condition at step 4]:
  - 4a1. System displays [error].
  - 4a2. Use case ends in failure.

---

### Business rules

| ID | Rule |
| --- | --- |
| BR-01 | [Rule text] |

---

### Notes

- [Assumptions, open questions, or related use cases]
```

## Examples

### Example 1 — Place order

**Input:** "Write a use case for placing an order on an e-commerce site."

**Expected output:** UC-001 with primary actor "Authenticated customer", secondary actors "Payment gateway", "Inventory service". Main scenario: browse → add to cart → checkout → enter payment → confirm. Extensions: 4a (out of stock), 5a (payment declined), 5b (payment timeout). Business rule: order total must not exceed credit limit.

### Example 2 — Reset password

**Input:** "Use case for password reset via email link."

**Expected output:** UC-002. Precondition: user has a registered email. Main flow: request → email sent → link clicked → new password entered → confirmed. Extensions: 3a (link expired), 4a (password does not meet policy). Postcondition (success): user session active with new credentials. Postcondition (failure): password unchanged.

## Notes

- Use cases describe what the system does, not how. Avoid implementation detail in steps ("System calls the `/auth/reset` endpoint" → "System sends a password reset email").
- Keep the main success scenario to 10 steps or fewer. If it is longer, the use case is likely two use cases — split at the natural boundary.
- Extension steps that lead to the same outcome as another extension can share a reference (e.g., "3a3. Use case ends as per 4a.").
- This skill pairs with `write-user-story` (a use case can be decomposed into stories), `acceptance-test-plan` (each extension is a test scenario), and `requirements-document` (use cases are listed in the functional requirements section).
