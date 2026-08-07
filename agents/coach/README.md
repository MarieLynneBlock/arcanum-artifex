# Coach Agents

Custom `.agent.md` definitions for technical learning design, lab building, assessment, facilitation, and one-to-one coaching.

## Agents

| Agent | Description |
| --- | --- |
| [Technical Coaching Designer](technical-coaching-designer.agent.md) | Designs or adapts technical workshops, courses, labs, onboarding paths, learning journeys, exercises, agendas, knowledge checks, and embedded formative assessments for software and data practitioners. |
| [Technical Lab Builder](technical-lab-builder.agent.md) | Implements and validates approved technical training labs, including starter repositories, fixtures, tests, synthetic data, setup scripts, solutions, verification commands, and teardown instructions. |
| [Technical Learning Evaluator](technical-learning-evaluator.agent.md) | Reviews technical workshops, courses, labs, exercises, assessments, and facilitator material for alignment, accuracy, accessibility, timing, and delivery readiness. |
| [Technical Assessment Specialist](technical-assessment-specialist.agent.md) | Designs or validates technical assessments, diagnostic tasks, scoring rubrics, performance standards, pass criteria, and evidence for high-stakes decisions. |
| [Facilitator Guide Producer](facilitator-guide-producer.agent.md) | Converts an approved learning design into a facilitator guide, timed run sheet, demonstration script, learner instructions, delivery prompts, and contingency plan. |
| [Socratic Technical Coach](socratic-technical-coach.agent.md) | Coaches a learner through an immediate technical problem using diagnosis, focused questions, progressive hints, reflection, and explanation without taking ownership of the task too early. |

## How the suite fits together

The first five agents form a design-to-delivery pipeline. Each hands the next a completed, approved artefact rather than a shared draft:

```text
Technical Coaching Designer  ──▶  Technical Lab Builder         (implement an approved exercise spec)
             │               ──▶  Facilitator Guide Producer    (produce delivery-ready guidance)
             │               ──▶  Technical Assessment Specialist (high-stakes assessment design)
             ▼
Technical Learning Evaluator ──▶  independent readiness review, feeding findings back upstream
```

- The **Technical Coaching Designer** is the usual entry point and the only agent that delegates to the others as subagents.
- The **Technical Learning Evaluator** reviews rather than redesigns, and returns design gaps to the Designer instead of resolving them.
- The **Socratic Technical Coach** sits outside the pipeline. Learner coaching depends on a turn-by-turn exchange that a single delegated call cannot sustain, so it is invoked directly by a user and is blocked from subagent invocation.

In VS Code, handoff buttons appear after a response completes so you can move along this pipeline with the conversation context preserved.

## Deploy

Copy an `.agent.md` file into `.github/agents/` (project) or a personal agents directory (`~/.claude/agents/`, `~/.copilot/agents/`, `~/.agents/`).
