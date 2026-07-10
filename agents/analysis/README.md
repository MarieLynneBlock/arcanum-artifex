# Analysis Agents

Custom `.agent.md` definitions for gap, risk, stakeholder, and trade-off analysis.

## Agents

| Agent | Description |
| --- | --- |
| [AI Readiness Reporter](assessment/ai-readiness-reporter.agent.md) | Runs the AgentRC readiness assessment on the current repository and writes a self-contained Markdown readiness report at reports/ai-readiness-report.md. |
| [ADR Generator](planning/adr-generator.agent.md) | Enterprise-grade agent for authoring Architectural Decision Records (ADRs) with governance, compliance, security, and lifecycle controls, formatted for both AI consumption and human review. |
| [Atlassian Requirements to Jira](planning/atlassian-requirements-to-jira.agent.md) | Enterprise-grade agent that transforms requirements documents into governed Jira epics, stories, and sub-tasks via the Atlassian Rovo MCP Server — with metadata discovery, duplicate detection, traceability, and human-approved create/update gates. |
| [PRD Generator](planning/prd.agent.md) | Enterprise-grade agent for authoring comprehensive Product Requirements Documents (PRDs) — user stories, acceptance criteria, non-functional requirements, security, privacy, compliance, dependencies, risks, success metrics, and a defined approval lifecycle. |
| [SE: Product Manager](planning/se-product-manager-advisor.agent.md) | Product management guidance for creating GitHub issues, aligning business value with user needs, and making data-driven product decisions |
| [Idea Generator](planning/simple-app-idea-generator.agent.md) | Brainstorm and develop new application ideas through fun, interactive questioning until ready for specification creation. |
| [Critical thinking mode instructions](review/critical-thinking.agent.md) | Challenge assumptions and encourage critical thinking to ensure the best possible solution and outcomes. |
| [Devils Advocate](review/devils-advocate.agent.md) | I play the devil's advocate to challenge and stress-test your ideas by finding flaws, risks, and edge cases |
| [Technical Debt Remediation Plan](review/tech-debt-remediation-plan.agent.md) | Generate technical debt remediation plans for code, tests, and documentation. |
| [technical-content-evaluator](review/technical-content-evaluator.agent.md) | Elite technical content editor and curriculum architect for evaluating technical training materials, documentation, and educational content. |

## Deploy

Copy an `.agent.md` file into `.github/agents/` (project) or a personal agents directory (`~/.claude/agents/`, `~/.copilot/agents/`, `~/.agents/`).
