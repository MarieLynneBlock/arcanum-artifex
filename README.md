# arcanum-artifex 🧙🏻‍♀️

> Prompts, skills, and agents that survive contact with real workflows.  
> No vendor loyalty. Occasionally heretical.

A curated library of AI assistant resources — skills, agents, instructions, and guides — tested in real projects across multiple tools. Built on the open Agent Skills standard, so the same assets work in GitHub Copilot, Claude Code, and anything else that follows the spec.

---

## What's in here

| Folder | Contents |
| --- | --- |
| [skills/](skills/) | 200+ reusable skills, organized by domain |
| [agents/](agents/) | Custom agent definitions, organized by specialty |
| [instructions/](instructions/) | Context files that shape AI behavior per stack or domain |
| [templates/](templates/) | Blank starters to copy into your own project |
| [guides/](guides/) | Setup, practices, policy, and reference material |
| [workshops/](workshops/) | Hands-on exercises for team onboarding |

---

## Skills

The largest section. Skills are folders of instructions and resources that AI tools load when the task matches — drop a skill folder into the right location for your tool and scope, and it activates automatically.

```text
skills/
├── scientific/          ← AlphaFold, PubMed, RDKit, scanpy, molecular dynamics, quantum computing, clinical data, financial APIs — 160+ skills
├── data-science/        ← pandas, polars, scikit-learn, SHAP, MLflow, gradient boosting, survival analysis, time series
├── development/         ← Python, Rust, Java, TypeScript, SQL, DevOps, API design, frontend, game dev, refactoring, test strategy
├── analysis/            ← architecture audit, gap analysis, risk analysis, stakeholder mapping, user stories, epics, trade-off analysis
├── architecture/        ← 4+1 architectural views, ADRs, technology stack blueprints
├── agentic/             ← agent governance, OWASP compliance for agents, MCP, supply chain, evaluation frameworks
├── security/            ← threat modeling, GDPR compliance, security review, data breach blast radius
├── document-production/ ← PPTX, DOCX, PDF, LaTeX posters, Mermaid diagrams, scientific slides
├── documentation/       ← doc standards, writing guides, changelog and release note templates
└── study-support/       ← learning aids, flashcard generation, concept explanation frameworks
```

Skills follow the open standard — the same folder works in Copilot, Claude Code, and other compliant tools.

---

## Agents

Custom agent definitions (`.agent.md` files) that give an AI a focused working mode: domain expert, reviewer, planner, task-specific assistant.

```text
agents/
├── agentic/       ← agent orchestration, evaluation, and governance agents
├── analysis/      ← gap analysis, risk, stakeholder, and trade-off agents
├── architecture/  ← 4+1 views, ADR, and tech stack agents
├── development/   ← code review, refactoring, test strategy, and DevOps agents
├── documentation/ ← doc writing, changelog, and release note agents
├── scientific/    ← research, literature review, and data pipeline agents
└── security/      ← threat modeling, compliance, and security review agents
```

Drop them into `.github/agents/` for project scope, or `~/.copilot/agents/` for personal use.

---

## Instructions

Context files that adjust AI behavior for a specific language, framework, or workflow. Load them as repo-level instructions or agent context.

```text
instructions/
├── agentic/      ← agent behavior, governance, and safety constraints
├── architecture/ ← architectural standards and design principles
├── data-science/ ← data analysis, ML workflows, and notebook conventions
├── development/  ← language- and framework-specific coding standards
└── documentation/← writing style, structure, and doc conventions
```

---

## Templates

Blank starters to fork into your own project. Remove the `_blank` suffix, fill in the `[TODO]` placeholders.

```text
templates/
├── instructions/    ← stack-specific AI instructions (Python, Java, .NET, R, and more)
├── prompts/         ← reusable .prompt.md files (VS Code 1.99+)
├── skills/          ← empty skill shell to fill in
└── copilotignore_blank  ← rename to .copilotignore to exclude files from AI context
```

---

## Guides

```text
guides/
├── setup/           ← install in VS Code, IntelliJ, PyCharm, Visual Studio, Eclipse
├── guidelines/      ← responsible use, security, admin setup, manager and pilot guides
├── how-to/          ← getting started by role: developer, analyst, architect, DevOps
├── practices/       ← prompt engineering
└── resources/       ← cheat sheet, FAQ, prompt library, privacy card, impact measurement
```

---

## Workshops

Three hands-on exercises for team onboarding:

1. [Completions](workshops/01-completions.md)
2. [Chat and participants](workshops/02-chat-and-participants.md)
3. [Prompt engineering](workshops/03-prompt-engineering.md)

---

## How to use a skill

```bash
# Copy any skill folder to your project
cp -r skills/development/test-strategy/ your-project/.agents/skills/

# The AI tool detects and loads it when the task matches — no wiring required
```

Where you copy it depends on tool and scope:

| Scope | Cross-tool (open standard) | GitHub Copilot | Claude Code |
| --- | --- | --- | --- |
| Project (repo) | `.agents/skills/` | `.github/skills/` | `.claude/skills/` |
| Personal (user) | `~/.agents/skills/` | `~/.copilot/skills/` | `~/.claude/skills/` |

Use `.agents/skills/` when you want a single location that works across all compliant tools.

---

## Philosophy

These resources are built for real work, not demos. If it only performs in controlled conditions, it doesn't belong here.

- **No vendor loyalty.** Built on the open Agent Skills standard — run it in whatever tool you're actually using.
- **Occasionally heretical.** When official docs and real behavior diverge, we document real behavior.
- **Documentation-level accuracy.** If a feature is described here, it exists and works as described.

---

## Community

- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic's official skill collection
- [github/awesome-copilot](https://github.com/github/awesome-copilot) — community Copilot resources
