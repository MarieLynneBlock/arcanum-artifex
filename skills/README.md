# Skills

Proven agent skills ready to deploy. Each skill is a folder — copy the folder to your project's `.github/skills/` directory to use it.

## Library structure

This library is organised by category:

- [agentic/](agentic/)
- [analysis/](analysis/)
- [architecture/](architecture/)
- [data-science/](data-science/)
- [development/](development/)
- [document-production/](document-production/)
- [documentation/](documentation/)
- [scientific/](scientific/)
- [security/](security/)
- [study-support/](study-support/)

## What are agent skills?

Agent skills are folders of instructions, scripts, and resources that Copilot (and other AI tools) load when relevant to improve performance on specialised tasks. They are based on the **open Agent Skills standard** — the same skills work across Copilot, Claude Code, and other compliant tools.

## Skill locations

| Scope | Location |
| --- | --- |
| Project | `.github/skills/` · `.claude/skills/` · `.agents/skills/` |
| Personal | `~/.copilot/skills/` · `~/.claude/skills/` · `~/.agents/skills/` |

All three project paths are equivalent — AI tools check all of them.

## Using a skill from this lab

1. Copy the skill folder (for example `skills/development/test-strategy/`) to `.github/skills/` in your project.
2. The AI tool will detect and load it when the task matches the skill's description.
3. Remove the `_blank` suffix if present (lab convention — not part of the spec).

## Building a skill

Use the blank template: [../templates/skills/skill_blank/](../templates/skills/skill_blank/)

Community collections:
- [anthropics/skills](https://github.com/anthropics/skills)
- [github/awesome-copilot](https://github.com/github/awesome-copilot)
