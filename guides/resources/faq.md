# GitHub Copilot — FAQ

Short answers to common questions. For deeper detail, follow the links.

---

## Getting started

**Why isn't Copilot suggesting anything?**
Check that the Copilot icon in the status bar has no strikethrough. If it does, you're not signed in or your seat isn't active. If the icon looks fine, check that Copilot is enabled for the file type you're editing. See [troubleshooting.md](../how-to/troubleshooting.md).

**I accepted a suggestion but it's wrong. Did I do something wrong?**
No. Copilot generates suggestions based on patterns — it doesn't understand your system. Always review suggestions before accepting. Rejecting bad suggestions is correct use, not a failure.

**Does Copilot work in all file types?**
It works best in common programming languages (Python, Java, JavaScript, C#, SQL, etc.). It also works in Markdown, YAML, and JSON. It won't suggest in binary files or file types it doesn't recognise.

---

## Privacy and data

**Can Copilot see my entire repository?**
Not automatically. Inline completions use the current file and other open tabs as context. Copilot Chat only sees what you explicitly share — the current file, selections, or anything you attach with `#file:` or `@workspace`. See [privacy-quick-card.md](privacy-quick-card.md).

**Is it safe to paste an error message into chat?**
Usually yes — error messages themselves are not sensitive. Check first that the error doesn't contain internal hostnames, file paths with sensitive directory names, or data values. When in doubt, remove those parts before pasting.

**Does Copilot use my code to train the AI model?**
With Copilot Business and Enterprise: no. Prompts and suggestions are not used for training and are not retained after the request. Check with your admin which plan your organisation uses.

**Can my colleagues or my manager see what I type in Copilot Chat?**
No. Chat sessions are private. Admins can see aggregate usage metrics (acceptance rate, active users) but not individual conversations.

---

## Suggestions and quality

**How do I get better suggestions?**
Write more specific comments, use descriptive variable and function names, and have relevant files open in your editor. For chat, add context with `#file:` or `@workspace`. See [prompt-engineering.md](../practices/prompt-engineering.md).

**Copilot keeps suggesting the same wrong thing. What do I do?**
Press `Esc` to dismiss, then keep typing — even one more character changes the context. If it's consistently wrong for your project, a well-written `.github/copilot-instructions.md` can steer it in the right direction.

**Can Copilot write insecure code?**
Yes. Copilot is not a security tool — it suggests based on patterns, not security analysis. Always review generated code, especially for auth, input handling, and crypto. Run your normal SAST tools. See [security.md](../guidelines/security.md).

**Copilot suggested code that looks like it came from an open-source project. Is that a problem?**
It can be. With Copilot Business/Enterprise, enable Duplicate Detection in org settings — it suppresses suggestions that closely match public code. If you see a match, don't use it without checking the original licence.

---

## Features

**What is the difference between completions and chat?**
Completions appear inline as you type — grey text you accept with `Tab`. Chat is a conversation panel where you can ask questions, explain code, generate tests, and more. Both are part of Copilot but serve different purposes.

**What are slash commands?**
Built-in shortcuts in chat: `/explain`, `/fix`, `/tests`, `/doc`. Select some code, type one of these, and Copilot performs that specific task. See the [cheat sheet](cheat-sheet.md).

**What is `@workspace`?**
A chat participant that gives Copilot access to your entire project — not just the open file. Use it for questions that span multiple files: `@workspace how does authentication work in this project?` VS Code only.

**What is agent mode?**
Agent mode lets Copilot autonomously use tools — read files, run terminal commands, and iterate on a task. It asks for confirmation before running commands. VS Code only.

**Does Copilot work without an internet connection?**
No. Copilot requires a connection to GitHub's servers for every completion and chat message.

---

## IDE and setup

**I'm on a VPN and Copilot stopped working. Why?**
VPNs can block or re-route Copilot traffic. Try temporarily disabling the VPN to confirm. If that's the cause, your network team needs to whitelist Copilot endpoints or configure split tunnelling. See [troubleshooting.md](../how-to/troubleshooting.md).

**Do I need to do anything differently because we're behind a corporate proxy?**
Yes — you need to configure the proxy in your IDE settings. See [troubleshooting.md](../how-to/troubleshooting.md) section 4.

**I switched IDEs. Do I need a new licence?**
No. Your Copilot seat works across all supported IDEs. Just install the extension and sign in with the same GitHub account.
