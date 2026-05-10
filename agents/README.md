# Agents

Custom agents organized by category so they are easier to browse and reuse.

## Library structure

This library is organized close to the `skills/` taxonomy:

- [agentic/](agentic/)
- [analysis/](analysis/)
- [architecture/](architecture/)
- [development/](development/)
- [documentation/](documentation/)
- [scientific/](scientific/)
- [security/](security/)

Where useful, categories also have subfolders to keep related agents together, for example `development/dotnet/`, `development/frontend/`, and `agentic/mcp/`.

## What are custom agents?

Custom agents are `.agent.md` files that define a focused working mode for GitHub Copilot, such as a domain expert, reviewer, planner, or task-specific assistant.

## Agent locations

| Scope | Location |
| --- | --- |
| Project | `.github/agents/` |
| Personal | `~/.copilot/agents/` |

In this lab, the agents are grouped by domain for curation and discovery.
