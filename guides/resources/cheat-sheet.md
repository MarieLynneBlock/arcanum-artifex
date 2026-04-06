# GitHub Copilot — Cheat Sheet

Quick reference for keyboard shortcuts, commands, participants, and file locations.

---

## Keyboard shortcuts

### VS Code

| Action | Windows/Linux | macOS |
| --- | --- | --- |
| Accept suggestion | `Tab` | `Tab` |
| Dismiss suggestion | `Esc` | `Esc` |
| Next suggestion | `Alt+]` | `Option+]` |
| Previous suggestion | `Alt+[` | `Option+[` |
| Accept word (partial) | `Ctrl+Right` | `Cmd+Right` |
| Open Copilot Chat | `Ctrl+Alt+I` | `Ctrl+Cmd+I` |
| Inline chat | `Ctrl+I` | `Cmd+I` |

### IntelliJ IDEA & PyCharm

| Action | Windows/Linux | macOS |
| --- | --- | --- |
| Accept suggestion | `Tab` | `Tab` |
| Dismiss suggestion | `Esc` | `Esc` |
| Next suggestion | `Alt+]` | `Option+]` |
| Previous suggestion | `Alt+[` | `Option+[` |
| Open Copilot Chat | `Ctrl+Shift+C` | `Ctrl+Shift+C` |
| Inline chat | `Ctrl+I` | `Ctrl+I` |

### Visual Studio

| Action | Shortcut |
| --- | --- |
| Accept suggestion | `Tab` |
| Dismiss suggestion | `Esc` |
| Next suggestion | `Alt+]` |
| Previous suggestion | `Alt+[` |
| Open Copilot Chat | `Ctrl+\`, `Ctrl+C` |
| Inline chat | `Alt+/` |

### Eclipse

| Action | Shortcut |
| --- | --- |
| Accept suggestion | `Tab` |
| Dismiss suggestion | `Esc` |
| Next suggestion | `Alt+]` |
| Previous suggestion | `Alt+[` |
| Open Copilot Chat | `Ctrl+Shift+G` |

---

## Slash commands (chat)

| Command | What it does |
| --- | --- |
| `/explain` | Explains selected code |
| `/fix` | Suggests a fix for a bug or error |
| `/tests` | Generates tests for selected code |
| `/doc` | Generates documentation or a docstring |
| `/new` | Scaffolds a new file or project |
| `/newNotebook` | Creates a Jupyter notebook (VS Code only) |

---

## Chat participants (VS Code)

| Participant | Use for |
| --- | --- |
| `@workspace` | Questions spanning multiple files or the whole project |
| `@vscode` | VS Code settings, commands, extensions |
| `@terminal` | Explaining terminal output or errors |
| `@github` | GitHub repos, PRs, issues |
| `@docker` | Docker and container help (extension) |
| `@azure` | Azure services (extension) |

---

## `gh copilot` CLI

```bash
gh copilot explain "git rebase -i HEAD~3"
gh copilot suggest "compress a folder into a tar.gz"
```

Flags: `-t shell` · `-t git` · `-t gh`

---

## File locations

| File | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Repo-level instructions (all IDEs) |
| `.github/prompts/*.prompt.md` | Reusable prompts (VS Code 1.99+) |
| `.github/skills/<name>/SKILL.md` | Agent skills (open standard, cross-tool) |
| `.vscode/settings.json` | VS Code Copilot settings |
| `.copilotignore` | Files excluded from Copilot context |

---

## Feature availability by IDE

See the canonical matrix: [ide-feature-matrix.md](ide-feature-matrix.md)
