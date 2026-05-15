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

## Current subfolders

Key subfolders currently in use:

```text
agents/
├── agentic/
│   ├── agent-customisation/
│   ├── agentic-dev-team/
│   ├── governance/
│   └── mcp/
├── analysis/
│   ├── assessment/
│   ├── planning/
│   └── review/
├── architecture/
│   ├── domain/
│   └── review/
├── development/
│   ├── cpp/
│   ├── devops/
│   ├── dotnet/
│   ├── frontend/
│   ├── java/
│   ├── power-platform/
│   ├── python/
│   └── tooling/
├── documentation/
│   ├── accessibility/
│   └── writing/
├── scientific/
│   └── research/
└── security/
    └── review/
```

## Current size

- Agent files in this folder: **80** (`*.agent.md`)

## What are custom agents?

Custom agents are `.agent.md` files that define a focused working mode for GitHub Copilot, such as a domain expert, reviewer, planner, or task-specific assistant.

## Agent locations

```text
Project (portable default): .github/agents/
Personal (portable default): ~/.agents/
Personal (GitHub Copilot): ~/.copilot/agents/
Personal (Claude Code): ~/.claude/agents/
Personal (OpenCode): ~/.opencode/agents/
...
```

In this lab, the agents are grouped by domain for curation and discovery.
