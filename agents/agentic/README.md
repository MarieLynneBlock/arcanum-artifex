# Agentic Agents

Custom `.agent.md` definitions for agent governance, orchestration, evaluation, and safe agent design.

## Agents

| Agent | Description |
| --- | --- |
| [Agent Builder](agent-customisation/agent-builder.agent.md) | Agent customisation builder for creating, reviewing, and fixing single .agent.md files. |
| [Caveman Mode](agent-customisation/caveman-mode.agent.md) | Terse, low-token responses. Minimal words, no fluff. Task fidelity preserved. Use when: optimise token usage, low-token mode, concise output, caveman mode, reduce verbosity, token-efficient, brief responses. |
| [Customisation Debugger](agent-customisation/customisation-debugger.agent.md) | Customisation debugger for diagnosing why agents, prompts, instructions, or skills are not discovered, invoked, scoped, or followed as expected. |
| [Customisation Packager](agent-customisation/customisation-packager.agent.md) | Customisation packager for auditing and fixing standalone copyability of agents, prompts, instructions, skills, workflows, and related assets. |
| [Customisation Reviewer](agent-customisation/customisation-reviewer.agent.md) | Customisation quality reviewer for auditing agents, prompts, instructions, and skills for clarity, scope boundaries, trigger quality, and internal consistency. |
| [Instructions Builder](agent-customisation/instructions-builder.agent.md) | Instruction-file customisation builder for creating, reviewing, and fixing Copilot .instructions.md files. |
| [Prompt Builder](agent-customisation/prompt-builder.agent.md) | Prompt-file builder for creating, revising, and validating standalone prompts with practical test cases and clear output constraints. |
| [Prompt Engineer](agent-customisation/prompt-engineer.agent.md) | Prompt quality reviewer and refiner focused on analysis-first prompt improvement, structure clarity, and practical rewrite guidance. |
| [Settings Builder](agent-customisation/settings-builder.agent.md) | Settings customisation builder for designing, reviewing, and fixing Copilot and editor configuration that controls discovery, scope, and behaviour of custom assets. |
| [Skill Builder](agent-customisation/skill-builder.agent.md) | Agent skill builder for creating, reviewing, and packaging standalone SKILL.md folders. |
| [AI Data Team](agentic-dev-team/ai-data-team.agent.md) | AI data team agent (Ingrid, Tycho). Use when: designing data models, building ingestion or transformation pipelines, validating data quality, defining offline evaluation metrics, analysing model/prompt performance, or preparing datasets for production AI features. |
| [AI Dev Team](agentic-dev-team/ai-dev-team.agent.md) | AI development team agent (Linus, Bjarne, Tove). Use when: building features, writing application code, fixing bugs, implementing UI components, creating APIs, styling with CSS, writing database queries, or executing sprint plans. |
| [AI DevOps Team](agentic-dev-team/ai-devops-team.agent.md) | AI DevOps team agent (Niels, Anders). Use when: designing CI/CD for AI-enabled systems, writing deployment manifests, managing AWS environments, hardening runtime reliability, defining observability and rollback strategy, or operationalising release governance. |
| [AI Team Producer](agentic-dev-team/ai-team-producer.agent.md) | AI team producer agent (Astrid). Use when: planning sprints, creating PROJECT_BRIEF.md, triaging bugs, merging PRs, coordinating AI Dev Team, AI Team QA, AI Data Team, and AI DevOps Team, filing GitHub Issues, writing sprint plans, running brainstorms, or recovering project context. |
| [AI Team QA](agentic-dev-team/ai-team-qa.agent.md) | AI QA engineer agent (Sigrid). Use when: testing features, running E2E tests, playtesting, filing bug reports, writing test automation, creating QA sign-off documents, or verifying bug fixes. |
| [AI Team Mentor](agentic-dev-team/mentor.agent.md) | Socratic mentor agent (Mímir). Use when: guiding an engineer through a new feature or refactor, challenging assumptions, exploring trade-offs, or building critical thinking without giving direct answers. |
| [Agent Governance Reviewer](governance/agent-governance-reviewer.agent.md) | AI agent governance reviewer for auditing agent systems for policy gaps, trust boundary risks, and auditability weaknesses before release. |
| [Agent OWASP Compliance Reviewer](governance/agent-owasp-compliance-reviewer.agent.md) | OWASP ASI reviewer for auditing AI agent systems against OWASP ASI Top 10 controls and identifying agentic security compliance gaps. |
| [Agent Supply Chain Reviewer](governance/agent-supply-chain-reviewer.agent.md) | Agent supply-chain reviewer for auditing plugin, tool, and MCP dependency integrity, provenance, and tamper risks in agent ecosystems. |
| [Responsible AI Reviewer](governance/responsible-ai-reviewer.agent.md) | Responsible AI reviewer for auditing AI features for fairness, accessibility, privacy, and explainability risks before release. |
| [Java MCP Expert](mcp/java-mcp-expert.agent.md) | Java MCP expert for building, reviewing, and debugging Model Context Protocol servers with Java SDK, Reactor, and Spring Boot integration. |
| [M365 MCP Expert](mcp/m365-mcp-expert.agent.md) | M365 MCP expert for building and reviewing Microsoft 365 declarative agents with MCP server integration, response semantics, and secure deployment workflows. |
| [Power Platform MCP Expert](mcp/power-platform-mcp-expert.agent.md) | Power Platform MCP integration expert for designing, reviewing, and troubleshooting Copilot Studio custom connectors with MCP-compatible schemas and secure authentication. |
| [Python MCP Expert](mcp/python-mcp-expert.agent.md) | Python MCP expert for building, reviewing, and debugging Model Context Protocol servers with FastMCP, typed schemas, and production-ready transport setup. |

## Deploy

Copy an `.agent.md` file into `.github/agents/` (project) or a personal agents directory (`~/.claude/agents/`, `~/.copilot/agents/`, `~/.agents/`).
