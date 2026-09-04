# Agentic Skills

This category contains skills for agent governance, orchestration, evaluation, and safe agent design.

## Skills

| Skill | Description |
| --- | --- |
| [agent-governance-patterns](agent-governance-patterns/SKILL.md) | Design and implement governance controls for tool-using and multi-agent AI systems, including policy enforcement, approval gates, audit trails, trust scoring, rate limits, and safe tool execution. |
| [agent-owasp-compliance](agent-owasp-compliance/SKILL.md) | Assess tool-using and multi-agent AI systems against OWASP ASI-style controls, mapping evidence to prompt injection, tool governance, agency, escalation, trust boundaries, audit, identity, policy integrity, supply chain, and behavioural monitoring risks. |
| [agent-supply-chain](agent-supply-chain/SKILL.md) | Review, generate, and verify supply-chain integrity controls for AI agent tools, plugins, MCP servers, skills, prompts, and custom agents, including SHA-256 manifests, dependency pinning, provenance evidence, promotion gates, and CI verification. |
| [agentic-eval](agentic-eval/SKILL.md) | Use when designing and implementing evaluation loops for AI agents, including reflection, evaluator-optimiser patterns, rubric scoring, LLM-as-judge review, test-driven refinement, convergence checks, and iteration logging. |
| [ai-ready](ai-ready/SKILL.md) | Guide users to review and install the external ai-ready skill from its upstream repository. |
| [copilot-cli-quickstart](copilot-cli-quickstart/SKILL.md) | Beginner-friendly interactive tutorial for GitHub Copilot CLI concepts, slash commands, permissions, file context, planning, and custom instructions. |
| [first-ask](first-ask/SKILL.md) | Interactive task-refinement workflow that clarifies scope, deliverables, and constraints before carrying out the task. |
| [generate-custom-instructions-from-codebase](generate-custom-instructions-from-codebase/SKILL.md) | Generate GitHub Copilot migration instructions by comparing two project versions and extracting conventions for framework upgrades, refactoring, dependency changes, or technology migrations. |
| [github-copilot-starter](github-copilot-starter/SKILL.md) | Set up a GitHub Copilot customisation starter pack for a new project based on its technology stack, including instructions, skills, agents, and optional setup workflow files. |
| [nano-banana-pro-openrouter](nano-banana-pro-openrouter/SKILL.md) | Generate or edit images via OpenRouter with the Gemini 3 Pro Image model. Use for prompt-only image generation, image edits, and multi-image compositing; supports 1K/2K/4K output. |
| [noob-mode](noob-mode/SKILL.md) | Plain-English response style for non-technical Copilot CLI users. Explains approval prompts, errors, command output, and technical choices with clear risk indicators. |
| [prompt-builder](prompt-builder/SKILL.md) | Guide users through creating high-quality GitHub Copilot prompt files with clear structure, appropriate tools, validation criteria, and maintainable instructions. |
| [remember](remember/SKILL.md) | Transform lessons learned into domain-organised memory instructions for global or workspace scope. |
| [remember-interactive-programming](remember-interactive-programming/SKILL.md) | Micro-skill that reminds the agent to use an available REPL or live runtime as the source of truth during interactive programming tasks. |
| [tldr-prompt](tldr-prompt/SKILL.md) | Create tldr-style summaries for GitHub Copilot customisation files, MCP server documentation, or Copilot documentation from files, URLs, or focused queries. |
| [what-context-needed](what-context-needed/SKILL.md) | Identify which files or folders Copilot needs to inspect before answering a user question, including required context, helpful context, and uncertainties. |

## Add a skill here

1. Copy the template from `../../templates/skills/skill_blank/`.
2. Use a scope-first, kebab-case name.
3. Define expected outputs and evidence standards.
