# GitHub Copilot — Feature Guide

A practical reference for configuring and customizing GitHub Copilot in VS Code.

---

## 1. Repo-level instructions

**File:** `.github/copilot-instructions.md`

Applied to every Copilot Chat request in the repo. Copilot appends the contents automatically — no user action needed.

- Keep under ~500 words; it's prepended to every turn.
- Scoped to the repository. Does not affect Copilot completions in the editor.
- Requires `github.copilot.chat.codeGeneration.useInstructionFiles: true` in settings.

**When to use:** project conventions, stack context, anti-patterns to avoid.

---

## 2. Prompt files (reusable prompts)

**Location:** `.github/prompts/*.prompt.md`
**Extension:** `.prompt.md` (required)
**VS Code version:** 1.99+

Reusable, shareable prompts that appear in the Copilot Chat prompt picker (`/` in chat, or paperclip > Prompt...).

### Frontmatter fields

| Field | Values | Description |
| --- | --- | --- |
| `mode` | `ask`, `edit`, `agent` | How Copilot responds |
| `description` | string | Shown in the picker |
| `tools` | list | MCP/VS Code tools available to `agent` mode |

### Referencing files in prompts

- `#file:path/to/file.ts` — attach a specific file
- `#folder:src/` — attach a folder
- `${workspaceFolder}`, `${file}`, `${selection}` — dynamic variables

---

## 3. VS Code settings

> Settings in this section apply to VS Code only. For other IDEs, settings are configured via the IDE's native UI — see the setup guides:
> [IntelliJ IDEA](../setup/intellij.md) · [PyCharm](../setup/pycharm.md) · [Visual Studio](../setup/visual-studio.md) · [Eclipse](../setup/eclipse.md)

Key Copilot settings in `.vscode/settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "github.copilot.enable": { "*": true },
  "github.copilot.editor.enableAutoCompletions": true,
  "github.copilot.nextEditSuggestions.enabled": true
}
```

`useInstructionFiles` must be `true` for `.github/copilot-instructions.md` to be loaded.

### Additional instruction files

You can stack extra instruction files or inline text on top of the main instructions file:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": ".github/instructions/typescript.md" },
    { "text": "Always prefer named exports over default exports." }
  ]
}
```

Useful for layering team-wide rules with project-specific ones.

---

## 4. .copilotignore

Works like `.gitignore` — tells Copilot which files to exclude from its context.

```
# Exclude secrets and generated files
.env
dist/
*.generated.ts
```

Place at repo root. Copilot will not read or suggest content from matched files.

See template: [templates/copilotignore_blank](../templates/copilotignore_blank)

---

## 5. Chat participants

Participants are scoped AI assistants invoked with `@` in chat. They give Copilot access to specific context.

| Participant | Context provided | Available in |
| --- | --- | --- |
| `@workspace` | Entire project — files, structure, symbols | VS Code |
| `@vscode` | VS Code settings, commands, extensions | VS Code |
| `@terminal` | Current terminal session and output | VS Code |
| `@github` | GitHub repos, PRs, issues, code search | VS Code, github.com |

**Example:** `@workspace what does the AuthService do?`

`@workspace` is the most important — use it whenever a question spans multiple files.

---

## 6. Slash commands

Built-in commands invoked with `/` in chat. Work across most IDEs.

| Command | What it does |
| --- | --- |
| `/explain` | Explains selected code |
| `/fix` | Suggests a fix for a bug or error |
| `/tests` | Generates tests for selected code |
| `/doc` | Generates documentation or a docstring |
| `/new` | Scaffolds a new file or project |
| `/newNotebook` | Creates a Jupyter notebook (VS Code only) |

Slash commands can be combined with participants: `@workspace /explain the auth flow`

---

## 7. Copilot Extensions

Third-party chat participants installed as VS Code extensions. Invoked with `@` like built-in participants, but backed by external services.

| Extension | What it does |
| --- | --- |
| `@docker` | Docker image, compose, and Dockerfile help |
| `@azure` | Azure service guidance and deployment help |

Extensions are installed from the VS Code Marketplace. They differ from MCP servers: extensions are VS Code-native, MCP is a protocol that works across tools.

---

## 8. Copilot agent mode

In VS Code, Copilot can run in **agent mode**: it autonomously uses tools, reads files, runs terminal commands, and iterates on a task.

- Activate: set `mode: agent` in a prompt file, or switch mode in the chat header.
- Tools available: file system, terminal, extensions, MCP servers.
- Copilot will ask for confirmation before running terminal commands.

---

## 9. MCP servers

Copilot supports **Model Context Protocol (MCP)** servers for extending tool access in agent mode.

Configure in VS Code user or workspace settings:

```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "command": "npx",
        "args": ["-y", "@my-org/mcp-server"],
        "env": { "API_KEY": "${env:MY_API_KEY}" }
      }
    }
  }
}
```

MCP tools appear in agent mode and in prompt files with `tools` frontmatter.

---

## 10. Agent Skills

Agent Skills are folders of instructions, scripts, and resources that Copilot loads when relevant to improve its performance on specialised tasks.

> The Agent Skills specification is an **open standard** — the same skills work with Copilot cloud agent, GitHub Copilot CLI, agent mode in VS Code, and Claude Code. A skill written once is reusable across tools.

### Where skills live

| Scope | Location |
| --- | --- |
| Project (any AI tool) | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` |
| Personal (across projects) | `~/.copilot/skills/`, `~/.claude/skills/`, or `~/.agents/skills/` |
| Organisation / Enterprise | Coming soon |

### What a skill contains

A skill is a folder with a `SKILL.md` file and optionally scripts and resource files:

```text
.github/skills/
└── my-skill/
    ├── SKILL.md        ← instructions Copilot reads when loading the skill
    ├── scripts/        ← executable scripts the skill can call
    └── resources/      ← reference files, templates, config
```

### When skills activate

Copilot loads a skill when the task matches the skill's description, or when the user explicitly references it. Skills are not always active — they are loaded on demand.

### Community skill collections

- [`anthropics/skills`](https://github.com/anthropics/skills) — Anthropic's published skills (cross-tool)
- [`github/awesome-copilot`](https://github.com/github/awesome-copilot) — community-curated Copilot skills and resources

### Availability

Works with: Copilot cloud agent, GitHub Copilot CLI, agent mode in VS Code.
Plan required: Pro, Pro+, Business, or Enterprise (for cloud agent). All plans (for CLI).

See the blank skill template: [templates/skills/skill_blank/SKILL.md](../../templates/skills/skill_blank/SKILL.md)

---

## 11. `gh copilot` CLI

Copilot is available in the terminal via the GitHub CLI extension.

### Install

```bash
gh extension install github/gh-copilot
```

Requires the [GitHub CLI](https://cli.github.com/) (`gh`) with an active session.

### Commands

| Command | What it does |
| --- | --- |
| `gh copilot explain "command"` | Explains what a shell command does |
| `gh copilot suggest "task"` | Suggests a shell command for a task |

**Examples:**

```bash
gh copilot explain "git rebase -i HEAD~3"
gh copilot suggest "find all files modified in the last 7 days"
```

Use `-t shell`, `-t git`, or `-t gh` to scope suggestions to a specific command type.

---

## 12. GitHub.com Copilot

Features available at github.com — no IDE required.

| Feature | What it does | Plan required |
| --- | --- | --- |
| Copilot Chat | Chat in the browser, `@github` context | Individual+ |
| PR summaries | Auto-generated pull request descriptions | Individual+ |
| Code review | Copilot reviews PRs and adds inline comments | Business/Enterprise |
| Knowledge bases | Index internal docs for Copilot context | Enterprise |

PR summaries are triggered from the PR description field — look for the Copilot icon next to the description box.

---

## 13. Known limitations

- `.github/copilot-instructions.md` does not affect inline completions — chat only.
- Prompt files require VS Code 1.99+; not available in github.com Copilot Chat.
- Agent mode requires user confirmation before running terminal commands.
- Copilot Extensions (`@docker`, `@azure`) are VS Code only.
- `gh copilot` CLI is terminal only — not connected to IDE chat sessions.
- Agent Skills require agent mode or the Copilot CLI — they do not activate in standard chat or inline completions.
