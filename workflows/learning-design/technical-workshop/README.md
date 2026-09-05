---
name: 'Technical Workshop Design to Delivery'
description: 'Standalone workflow bundle that turns a topic, repository, or business need into an aligned technical workshop with runnable labs, a facilitator guide, an assessment, and an independent readiness review.'
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Technical Workshop Design to Delivery

Design a technical workshop, course, lab set, or onboarding path for software and data practitioners, then build, facilitate, assess, and independently review it — without any one agent quietly redesigning another's work.

## What this workflow produces

An aligned learning experience with measurable outcomes, a timed learning arc, runnable exercise specifications, implemented labs with verification and teardown, delivery-ready facilitator guidance, an assessment proportionate to the stakes, and a readiness verdict from an agent that did not design the material.

## Who this is for

Anyone building technical enablement: a workshop, a course, a train-the-trainer package, an onboarding path, or a lab set. Use it when the work spans design **and** implementation **and** delivery, and you want the handoffs to be explicit.

If you only need one of those stages, invoke that agent on its own instead — each vendored agent under `assets/agents/` also works standalone.

## Self-contained

This folder ships with **vendored copies** of all five agents under `assets/agents/`. Copy the entire `technical-workshop/` folder into any repo and it runs as-is — no other file in this repo is required at runtime.

This is a **frozen snapshot**. It has no sync contract with the repo-level agents; the two sets will drift, and that is intentional.

The vendored agents carry a `(technical-workshop)` name suffix so they never collide with repo-level or user-level agents of the same role.

## How to invoke

1. Copy `assets/agents/` into `.github/agents/` (repository scope) or a personal agents directory such as `~/.copilot/agents/`.
2. Select **Technical Coaching Designer (technical-workshop)** and describe the learners, desired performance, format, duration, and materials.
3. The designer delegates to the other four as subagents at the points described in [WORKFLOW.md](WORKFLOW.md).

If your host does not support subagents, follow [WORKFLOW.md](WORKFLOW.md) manually and invoke each agent in turn, passing the previous step's output.

## Inside this folder

- [WORKFLOW.md](WORKFLOW.md) — the orchestration playbook (source of truth for the sequence, handoffs, and validation).
- `assets/agents/` — the five vendored agents: designer, lab builder, facilitator guide producer, assessment specialist, and learning evaluator.

## Related

Live one-to-one learner coaching deliberately sits outside this workflow. It depends on a turn-by-turn exchange that a single delegated call cannot sustain, so use a dedicated coaching agent directly rather than orchestrating it here.
