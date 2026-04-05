# GitHub Copilot — Getting Started (Developer Day 1)

You have been granted access to GitHub Copilot. This guide gets you set up and productive in under 30 minutes.

---

## Step 1 — Install the extension

Go to your IDE's setup guide and follow the install steps:

- [VS Code](../setup/vscode.md)
- [IntelliJ IDEA](../setup/intellij.md)
- [PyCharm](../setup/pycharm.md)
- [Visual Studio](../setup/visual-studio.md)
- [Eclipse](../setup/eclipse.md)

**Done when:** You see the Copilot icon in the status bar without a strikethrough.

---

## Step 2 — Try your first completion

1. Open a file in your primary language.
2. Write a comment describing what you want:

```python
# function that validates an email address
```

3. Press `Enter` and wait 1–2 seconds. A grey suggestion appears.
4. Press `Tab` to accept. Press `Esc` to dismiss.
5. Use `Alt+]` / `Option+]` to cycle through alternative suggestions.

**Tip:** Copilot works best when it has context. Existing code in the file, descriptive variable names, and comments all improve suggestion quality.

---

## Step 3 — Try Copilot Chat

Open the chat panel (see your IDE's shortcut in the [cheat sheet](../resources/cheat-sheet.md)).

Try these prompts:

1. `/explain` with a function selected — Copilot explains what it does.
2. `@workspace what are the main components of this project?`
3. Select some code → `/fix` — Copilot suggests a fix.
4. `/tests` with a function selected — Copilot generates unit tests.

---

## Step 4 — Read the responsible use guide

Before going further: [responsible-use.md](../guidelines/responsible-use.md)

Key rules:
- Review every suggestion before accepting.
- Never paste credentials or sensitive data into chat.
- AI-generated code goes through normal code review.

---

## Week 1 goals

By end of week 1, aim to have:

- [ ] Used inline completions for at least one real task
- [ ] Used `/explain` on unfamiliar code
- [ ] Used `/tests` to generate tests for a function
- [ ] Used `@workspace` to ask a question about the project
- [ ] Read [responsible-use.md](../guidelines/responsible-use.md)

---

## Tips for getting more out of Copilot

- **Be specific in comments.** `// validate email with regex, return bool` beats `// check email`.
- **Write the function signature first.** Copilot uses it as a strong signal.
- **Use chat for debugging.** Paste an error message and ask what it means.
- **Use `@workspace` for big picture questions.** It indexes the whole project.
- **Reject bad suggestions.** `Esc` dismisses. Keep typing if the suggestion is wrong.

---

## Resources

| Resource | Link |
| --- | --- |
| Cheat sheet | [cheat-sheet.md](../resources/cheat-sheet.md) |
| Feature reference | [copilot-guide.md](../resources/copilot-guide.md) |
| Prompt engineering | [prompt-engineering.md](../practices/prompt-engineering.md) |
| Responsible use | [responsible-use.md](../guidelines/responsible-use.md) |
| Security guidance | [security.md](../guidelines/security.md) |
