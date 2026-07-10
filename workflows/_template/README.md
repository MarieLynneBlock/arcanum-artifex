# `<workflow-name>` workflow

> Blank scaffold. Copy this folder, rename to your workflow's outcome (kebab-case, e.g. `4plus1-diagrams`), and fill in.

## What this workflow produces

[TODO] One paragraph describing the final outcome.

## Who this is for

[TODO] Primary audience and the trigger ("Use this when…").

## How to invoke

[TODO] One of: paste the prompt from `prompts/`, invoke the agent from `agents/`, or follow `WORKFLOW.md` manually.

## Inside this folder

- [WORKFLOW.md](WORKFLOW.md) — the orchestration playbook (source of truth).
- `skills/` — **bundled** copies of skills the workflow depends on.
- `instructions/` — **bundled** copies of instruction files the workflow needs.
- `agents/` — `.agent.md` files specific to this workflow (the thin orchestrators).
- `prompts/` — `.prompt.md` files that trigger the workflow.
- `templates/` — templates the workflow produces or consumes.
- `references/` — supplementary references too workflow-specific to belong in a skill.
- `examples/` — worked examples.

Bundle exact copies. Do not edit a bundled skill in place — update the source skill, record the mapping in `vendored-assets-manifest.json`, and refresh the copy.
