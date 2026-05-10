# copilot-lab

Personal collection of verified GitHub Copilot resources — instructions templates, prompt file templates, VS Code settings, and guides.

## Structure

```text
copilot-lab/
├── agents/                       ← curated custom agents, organized by category
├── .github/
│   ├── copilot-instructions.md   ← repo-level instructions (this lab's own)
│   └── prompts/                  ← reusable .prompt.md files
├── .vscode/
│   └── settings.json             ← Copilot VS Code settings reference
├── instructions/                 ← classified instruction files, organized like skills/
├── templates/                    ← blank templates to copy into projects
│   ├── instructions/             ← deploys to .github/copilot-instructions.md
│   ├── prompts/                  ← deploys to .github/prompts/
│   ├── skills/                   ← deploys to .github/skills/ (open standard)
│   └── copilotignore_blank       ← rename to .copilotignore on deploy
├── skills/                       ← proven skills ready to deploy
├── workshops/                    ← hands-on exercises for onboarding sessions
│   ├── 01-completions.md
│   ├── 02-chat-and-participants.md
│   └── 03-prompt-engineering.md
└── guides/
    ├── setup/                    ← IDE installation guides
    │   ├── vscode.md
    │   ├── intellij.md
    │   ├── pycharm.md
    │   ├── visual-studio.md
    │   └── eclipse.md
    ├── guidelines/               ← policy-level: admins, leads, compliance
    │   ├── responsible-use.md
    │   ├── security.md
    │   ├── admin.md
    │   ├── manager-guide.md
    │   └── pilot-guide.md
    ├── how-to/                   ← step-by-step guides for any role
    │   ├── getting-started.md
    │   ├── getting-started-analyst.md
    │   ├── getting-started-architect.md
    │   ├── getting-started-devops.md
    │   ├── workflow-integration.md
    │   └── troubleshooting.md
    ├── practices/                ← how to use Copilot well
    │   └── prompt-engineering.md
    └── resources/                ← evergreen reference material
        ├── copilot-guide.md
        ├── cheat-sheet.md
        ├── prompt-library.md
        ├── faq.md
        ├── privacy-quick-card.md
        └── measuring-impact.md
```

## Native Copilot concepts

| Concept | File/Location | Purpose |
| --- | --- | --- |
| Repo instructions | `.github/copilot-instructions.md` | Appended to every chat request |
| Prompt files | `.github/prompts/*.prompt.md` | Reusable prompts in the picker |
| VS Code settings | `.vscode/settings.json` | Enable and configure Copilot |
| Copilot ignore | `.copilotignore` | Exclude files from Copilot context |

## Custom agents

The [agents/](agents/) library is organized by category, similar to [skills/](skills/), so domain-specific agents are easier to find and maintain.

## Using templates

1. Copy the relevant file from `templates/` to your project.
2. Remove the `_blank` suffix from the filename.
3. Fill in `[TODO]` placeholders.

## Related labs

- [claude-lab](../claude-lab) — Claude Code resources
