---
name: 'Technical Workshop Design to Delivery'
description: 'Workflow playbook for turning a topic, repository, or business need into an aligned technical workshop with runnable labs, a facilitator guide, an assessment, and an independent readiness review.'
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Workflow: Technical Workshop Design to Delivery

## 1. Purpose

Produce a deliverable technical learning experience for software or data practitioners: measurable outcomes, a timed learning arc, runnable exercise specifications, implemented labs, delivery-ready facilitator guidance, an assessment proportionate to the stakes, and an independent readiness verdict.

The workflow exists because these stages are separate responsibilities that hand each other completed, approved artefacts. Design decisions stay with the designer; implementation, facilitation, assessment, and review each get an agent that cannot silently redesign the course.

## 2. Linked assets

**This workflow is self-contained.** Every agent it needs is vendored under `assets/agents/`. Copy the whole `technical-workshop/` folder into another repo and it runs as-is.

The vendored copies are a **frozen snapshot**. There is no sync mechanism and no runtime dependency on any path outside this folder.

| Asset type | Path (inside this workflow) | Role |
| --- | --- | --- |
| Agent (entry point) | [assets/agents/technical-coaching-designer.agent.md](assets/agents/technical-coaching-designer.agent.md) | Owns backward design, outcomes, evidence, learning arc, and exercise specifications. Delegates to the four companions. **Source of truth for design decisions.** |
| Agent (subagent) | [assets/agents/technical-lab-builder.agent.md](assets/agents/technical-lab-builder.agent.md) | Implements an approved exercise specification into starter material, fixtures, verification, and teardown. |
| Agent (subagent) | [assets/agents/facilitator-guide-producer.agent.md](assets/agents/facilitator-guide-producer.agent.md) | Turns an approved design into a timed run sheet, misconception guide, and contingencies. |
| Agent (subagent) | [assets/agents/technical-assessment-specialist.agent.md](assets/agents/technical-assessment-specialist.agent.md) | Designs or validates assessment for high-stakes or technically complex decisions. |
| Agent (subagent) | [assets/agents/technical-learning-evaluator.agent.md](assets/agents/technical-learning-evaluator.agent.md) | Independently reviews the assembled material and returns a readiness decision. |

The vendored agents carry a `(technical-workshop)` name suffix so they can coexist with any repo-level or user-level agents of the same role.

## 3. Preconditions

- The five agent files are discoverable by the host. Copy `assets/agents/` into `.github/agents/` (repository scope) or a personal agents directory such as `~/.copilot/agents/` before starting.
- The host supports subagent invocation. If it does not, run steps 2 to 5 by invoking each agent directly and passing the previous step's output.
- The requester can state the audience, desired workplace performance, delivery format, and duration, or accept explicit assumptions in their place.
- Any repository, dataset, or draft course the design should build on is available in the workspace.

## 4. Steps

1. **Frame and design.** Invoke **Technical Coaching Designer (technical-workshop)** with the audience, desired performance, format, duration, materials, and requested deliverable. It produces the design brief, outcomes and evidence map, learning journey, exercise specifications, facilitator notes, assessment approach, and readiness gaps.
   - Input: topic or business need, plus any supplied repository or draft material.
   - Output: an approved design. Do not continue until the outcomes and evidence map are settled — every later stage treats them as fixed.
2. **Build the labs.** For each hands-on exercise, delegate to **Technical Lab Builder (technical-workshop)** with the exercise specification, target environment, learner starting point, and acceptance checks.
   - Output: starter material, fixtures, synthetic data, verification commands, teardown instructions, and a reference solution kept separate from learner material.
   - If the specification cannot produce its claimed evidence, the builder returns the design gap. Send it back to step 1 rather than building around it.
3. **Produce facilitator guidance.** Delegate to **Facilitator Guide Producer (technical-workshop)** with the approved design, cohort details, delivery mode, and facilitator constraints.
   - Output: delivery overview, timed run sheet, activity notes, misconception guide, contingencies, close, and readiness gaps.
4. **Design the assessment.** Delegate to **Technical Assessment Specialist (technical-workshop)** only when the decision is summative, selection, certification, or technically complex. Ordinary formative checks stay inside the design from step 1.
   - Output: assessment brief, blueprint, tasks, scoring, administration, and validation plan.
5. **Review readiness.** Invoke **Technical Learning Evaluator (technical-workshop)** on the assembled material with the intended learners, outcomes, duration, and the decision the review must support.
   - Output: severity-ranked findings, a readiness decision, an alignment summary, and recommended re-review checks.
   - Findings that require a design change return to step 1. The evaluator reviews rather than redesigns.
6. **Repair and re-review.** Apply the minimum coherent repair, then repeat step 5 for the affected material only.

Steps 2, 3, and 4 are independent of each other and may run in any order once step 1 is approved. Give each companion its own output location to avoid two agents writing the same files.

## 5. Outputs

```text
<course-directory>/
├── design/
│   ├── design-brief.md
│   ├── outcomes-and-evidence.md
│   └── learning-journey.md
├── exercises/
│   └── <exercise-name>/
│       ├── README.md              ← learner instructions
│       ├── starter/               ← intentionally incomplete material
│       ├── verification/          ← automated or manual checks
│       └── solution/              ← facilitator reference, kept separate
├── facilitation/
│   ├── run-sheet.md
│   ├── misconception-guide.md
│   └── contingencies.md
├── assessment/                    ← only when step 4 runs
│   ├── blueprint.md
│   ├── tasks.md
│   └── rubric.md
└── review/
    └── readiness-review.md
```

The agents respond in chat by default and write files only when asked. Name the output directory explicitly if you want the tree above.

## 6. Validation

- Every outcome traces to instruction, practice, and observable evidence in the outcomes and evidence map.
- Each hands-on exercise has a starting point, success criteria, verification, hint ladder, and debrief.
- Each lab has been run from its documented starting state, reaches its intended initial failure, and passes its acceptance checks.
- Learner material and reference solutions are in separate directories.
- The run sheet totals reconcile with the stated duration, including setup, transitions, breaks, technical friction, and contingency.
- The evaluator's readiness decision is `ready` or `ready with minor repairs`, and any remaining findings are recorded rather than silently accepted.
- No agent has reported an unresolved design gap.

## 7. Out of scope

- Immediate one-to-one learner support during delivery. That depends on a turn-by-turn exchange a delegated call cannot sustain; use a dedicated coaching agent directly.
- Production feature implementation. The lab builder builds teaching artefacts, not shipping code.
