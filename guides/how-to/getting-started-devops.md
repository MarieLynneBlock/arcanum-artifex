# GitHub Copilot — Getting Started for DevOps & Infrastructure

You have been granted access to GitHub Copilot. This guide is for DevOps engineers, platform engineers, and infrastructure specialists working with scripts, pipelines, and configuration.

---

## Step 1 — Install the extension

- [VS Code](../setup/vscode.md) — recommended for scripts, pipelines, IaC

**Done when:** you see the Copilot icon in the status bar without a strikethrough.

---

## Step 2 — What Copilot can do for you

| Task | How |
| --- | --- |
| Writing Bash / PowerShell scripts | Describe the task in a comment, Copilot writes the script |
| Explaining shell commands | Paste the command into chat → ask what it does |
| Writing Dockerfiles | Describe the app and runtime, Copilot drafts the file |
| Writing GitHub Actions / CI pipelines | Describe the workflow steps |
| Writing Terraform / IaC | Describe the resource, Copilot generates the block |
| Debugging pipeline errors | Paste the error log into chat |
| Writing cron expressions | Describe the schedule in plain language |
| Writing regex for log parsing | Describe the pattern |

---

## Step 3 — Your first script

Open a `.sh` or `.ps1` file. Write a comment:

```bash
#!/bin/bash
# find all log files older than 30 days in /var/log and delete them
# log each deleted file to /tmp/cleanup.log
# dry-run mode if --dry-run flag is passed
```

Wait for the suggestion. Press `Tab` to accept. Review before running — always.

**Tip:** the more specific your comment (flags, paths, edge cases), the better the script.

---

## Step 4 — Use the `gh copilot` CLI

For quick terminal help without leaving the shell:

```bash
# explain a command
gh copilot explain "awk '{print $2}' access.log | sort | uniq -c | sort -rn"

# get a command suggestion
gh copilot suggest "find all docker containers using more than 1GB of memory"
```

Install: `gh extension install github/gh-copilot` (requires GitHub CLI).

---

## Step 5 — Try Copilot Chat

Open the chat panel. Try these:

1. Paste a pipeline error → `what is causing this GitHub Actions error and how do I fix it?`
2. Ask for a Dockerfile → `write a Dockerfile for a Python 3.12 FastAPI app, non-root user, multi-stage build`
3. Ask for a cron expression → `cron expression for every weekday at 6:30 AM CET`
4. Explain a command → `explain this awk command step by step: [paste command]`

---

## Step 6 — Read the privacy quick card

[privacy-quick-card.md](../resources/privacy-quick-card.md)

Key rules for infra:
- Never paste real credentials, tokens, or SSH keys into chat.
- Never paste production IP addresses, hostnames, or internal DNS names if they are sensitive.
- Anonymise log samples before pasting — replace real usernames, IPs, and IDs.

---

## Week 1 goals

- [ ] Generated a script or pipeline snippet with Copilot
- [ ] Used Copilot Chat to explain a command or error
- [ ] Tried `gh copilot explain` in the terminal
- [ ] Read the [privacy quick card](../resources/privacy-quick-card.md)

---

## Resources

| Resource | Link |
| --- | --- |
| Prompt library | [prompt-library.md](../resources/prompt-library.md) |
| Cheat sheet | [cheat-sheet.md](../resources/cheat-sheet.md) |
| Privacy quick card | [privacy-quick-card.md](../resources/privacy-quick-card.md) |
| FAQ | [faq.md](../resources/faq.md) |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |
