# Agents

Custom agents organised by category so they are easier to browse and reuse.

## Library structure

This library is organised close to the `skills/` taxonomy:

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

Custom agents are `.agent.md` files that define a focused working mode for an AI assistant, such as a domain expert, reviewer, planner, or task-specific assistant.

In practice, an agent gives the assistant a narrower role with clearer boundaries than a general chat mode. A good agent usually defines:

- scope: what tasks it should handle
- boundaries: what it should avoid or hand back
- workflow: the steps it should follow
- quality bar: what a good result looks like
- output shape: how responses should be structured

Use an agent when you want repeatable behaviour for a task family. Use general instructions for broad project rules, and use skills for deep domain knowledge that can be reused across multiple agents.

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
