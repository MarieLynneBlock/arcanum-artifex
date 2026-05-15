![Arcanum Artifex](assets/arcanum-artifex_banner.png)

# Arcanum Artifex 🧙🏻‍♀️

> Prompts, skills, and agents that survive contact with real workflows.  
> No vendor loyalty. Occasionally heretical.

Everything here has survived contact with real work. Skills, agents, instructions, and guides... tested across stacks, tools, and the kinds of projects that don't forgive sloppy prompts. Built on the open Agent Skills standard, so the same assets travel freely between Copilot, Claude Code, and anything else that follows the spec.

---

## What's in here

| Folder | Contents |
| --- | --- |
| [skills/](skills/) | 200+ reusable skills, organized by domain |
| [agents/](agents/) | Custom agent definitions, organized by specialty |
| [instructions/](instructions/) | Context files that shape AI behavior per stack or domain |
| [workflows/](workflows/) | Orchestrated playbooks that link skills, instructions, agents, prompts and tools end-to-end |
| [templates/](templates/) | Blank starters to copy into your own project |
| [guides/](guides/) | Setup, practices, policy, and reference material |
| [workshops/](workshops/) | Hands-on exercises for team onboarding |

---

## Skills

The main event. Skills are self-contained folders that AI tools pick up automatically when the task matches. Drop one into the right location and it activates. No wiring required.

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

Same folder, any compliant tool. Copilot, Claude Code, whatever's next.

---

## Agents

When a generalist isn't what you need. Each `.agent.md` gives an AI a tighter brief domain expert, stubborn reviewer or obsessive planner so it stops trying to be everything and starts being useful.

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

The invisible hand. Load one of these and the AI stops guessing about your stack, it knows it. Drop them as repo-level instructions or wire them directly into an agent.

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

Blank starters, ready to fork. Strip the `_blank` suffix, fill the `[TODO]` gaps, ship it.

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

## Philosophy

These resources are built for real work. If it only performs in controlled conditions, it doesn't belong here.

- **No vendor loyalty.** Built on the open Agent Skills standard — run it in whatever tool you're actually using.
- **Occasionally heretical.** When official docs and real behavior diverge, we document real behavior.
- **Documentation-level accuracy.** If a feature is described here, it exists and works as described.
