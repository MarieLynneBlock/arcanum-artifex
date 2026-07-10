# Architecture Agents

Custom `.agent.md` definitions for 4+1 views, ADRs, and technology-stack blueprints.

## Agents

| Agent | Description |
| --- | --- |
| [CAST Imaging Impact Analysis Agent](domain/cast-imaging-impact-analysis.agent.md) | Specialized agent for comprehensive change impact assessment and risk analysis in software systems using CAST Imaging |
| [CAST Imaging Software Discovery Agent](domain/cast-imaging-software-discovery.agent.md) | Specialized agent for comprehensive software application discovery and architectural mapping through static code analysis using CAST Imaging |
| [CAST Imaging Structural Quality Advisor Agent](domain/cast-imaging-structural-quality-advisor.agent.md) | Specialized agent for identifying, analyzing, and providing remediation guidance for code quality issues using CAST Imaging |
| [API Architect](review/api-architect.agent.md) | Your role is that of an API architect. Help mentor the engineer by providing guidance, support, and working code. |
| [Senior Cloud Architect](review/arch.agent.md) | Expert in modern architecture design patterns, NFR requirements, and creating comprehensive architectural diagrams and documentation |
| [.NET Self-Learning Architect](review/dotnet-self-learning-architect.agent.md) | Senior .NET architect for complex delivery: designs .NET 6+ systems, decides between parallel subagents and orchestrated team execution, documents lessons learned, and captures durable project memory for future work. |
| [High-Level Big Picture Architect (HLBPA)](review/hlbpa.agent.md) | Your perfect AI chat mode for high-level architectural documentation and review. |
| [SE: Architect](review/se-system-architecture-reviewer.agent.md) | System architecture review specialist with Well-Architected frameworks, design validation, and scalability analysis for AI and distributed systems |

## Deploy

Copy an `.agent.md` file into `.github/agents/` (project) or a personal agents directory (`~/.claude/agents/`, `~/.copilot/agents/`, `~/.agents/`).
