# Keep this folder

Everything the workflow needs at runtime lives here so the workflow folder is portable (drop into any repo and run).

- `skills/` — **bundled** copies of skills the workflow depends on.
- `instructions/` — **bundled** copies of instruction files (`.instructions.md`) the workflow needs.
- `agents/` — `.agent.md` files specific to this workflow (the thin orchestrators).
- `prompts/` — `.prompt.md` files that trigger the workflow.
- `templates/` — templates the workflow produces or consumes.
- `references/` — supplementary references too workflow-specific to belong in a skill.

Bundle exact copies. Do not edit a bundled skill in place — update the source skill and then replace the bundled copy manually.
