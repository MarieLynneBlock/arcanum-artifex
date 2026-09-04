# Agents

Custom agents organised by category so they are easier to browse and reuse.

## Library structure

This library is organised close to the `skills/` taxonomy:

| Category | Focus | Agents |
| --- | --- | ---: |
| [agentic/](agentic/) | Agent customisation, teams, governance, and MCP | 24 |
| [analysis/](analysis/) | Assessment, planning, and critical review | 10 |
| [architecture/](architecture/) | Domain analysis and architecture review | 8 |
| [coach/](coach/) | Technical learning design, delivery, assessment, and agent review | 7 |
| [data/](data/) | Data storytelling review | 1 |
| [development/](development/) | Language, platform, DevOps, and tooling specialists | 30 |
| [documentation/](documentation/) | Accessibility and technical writing | 6 |
| [scientific/](scientific/) | Scientific literature research | 1 |
| [security/](security/) | Security review | 1 |

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
├── coach/
├── data/
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

- Agent files in this folder: **88** (`*.agent.md`)

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
