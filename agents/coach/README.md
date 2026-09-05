# Coach Agents

Custom `.agent.md` definitions for technical learning design, lab building, assessment, facilitation, one-to-one coaching, agentic asset review, and delivery-metrics analysis.

## Structure

```text
coach/
├── learning-design/  design-to-delivery agents for technical learning
├── metrics/          delivery-performance measurement and improvement
└── review/           review agents for agent and skill definitions
```

## Learning design

| Agent | Description |
| --- | --- |
| [Technical Lab Builder](learning-design/technical-lab-builder.agent.md) | Implements and validates approved technical training labs, including starter repositories, fixtures, tests, synthetic data, setup scripts, solutions, verification commands, and teardown instructions. |
| [Technical Learning Evaluator](learning-design/technical-learning-evaluator.agent.md) | Reviews technical workshops, courses, labs, exercises, assessments, and facilitator material for alignment, accuracy, accessibility, timing, and delivery readiness. |
| [Technical Assessment Specialist](learning-design/technical-assessment-specialist.agent.md) | Designs or validates technical assessments, diagnostic tasks, scoring rubrics, performance standards, pass criteria, and evidence for high-stakes decisions. |
| [Facilitator Guide Producer](learning-design/facilitator-guide-producer.agent.md) | Converts an approved learning design into a facilitator guide, timed run sheet, demonstration script, learner instructions, delivery prompts, and contingency plan. |
| [Socratic Technical Coach](learning-design/socratic-technical-coach.agent.md) | Coaches a learner through an immediate technical problem using diagnosis, focused questions, progressive hints, reflection, and explanation without taking ownership of the task too early. |

## Metrics

| Agent | Description |
| --- | --- |
| [DORA Metrics Analyst](metrics/dora-metrics-analyst.agent.md) | Calculates and interprets the five DORA software delivery metrics from delivery, incident, Jira, and contextual Copilot adoption data. |

## Review

| Agent | Description |
| --- | --- |
| [Agent Reviewer](review/agent-reviewer.agent.md) | Reviews AI agent definitions and multi-agent workflows for configuration correctness, tool feasibility, safety boundaries, portability, and interoperability. |
| [Skill Reviewer](review/skill-reviewer.agent.md) | Reviews agent skill packages (`SKILL.md` plus bundled scripts, references, and assets) for standard conformance, discovery quality, workflow coherence, standalone packaging, portability, and safety. |

## How the suite fits together

Every agent here is a standalone artefact with no runtime dependency on another file in this repository. Each can be copied out and invoked on its own.

- The **learning design** agents each own one stage of technical enablement: building labs, producing facilitator guidance, designing assessment, and reviewing readiness. Invoke whichever stage you need.
- The **Technical Learning Evaluator** reviews rather than redesigns, and returns design gaps to whoever called it instead of resolving them.
- The **Socratic Technical Coach** is user-invoked only. Learner coaching depends on a turn-by-turn exchange that a single delegated call cannot sustain, so it sets `disable-model-invocation: true`.
- The **review** agents audit agent and skill definitions, report severity-ranked findings, and do not modify the assets they review.
- The **metrics** agent analyses delivery performance data independently of the rest.

Sequencing these agents into a design-to-delivery pipeline is a workflow concern, not an agent concern. The orchestrating Technical Coaching Designer and vendored copies of its companions live in [workflows/learning-design/technical-workshop/](../../workflows/learning-design/technical-workshop/).

## Deploy

Copy an `.agent.md` file into `.github/agents/` (project) or a personal agents directory (`~/.claude/agents/`, `~/.copilot/agents/`, `~/.agents/`).
