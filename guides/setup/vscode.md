# GitHub Copilot — VS Code Setup Guide

VS Code has the most complete Copilot feature set. All customization files (instructions, prompt files, MCP) are supported here first.

---

## 1. Install

1. Open VS Code.
2. Go to Extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`).
3. Search **GitHub Copilot** — install both:
   - `GitHub Copilot` — completions
   - `GitHub Copilot Chat` — chat panel and inline chat
4. Sign in with your GitHub account when prompted.

> Copilot requires an active Copilot license (Individual, Business, or Enterprise).

---

## 2. Verify

- Status bar (bottom): Copilot icon should show without a strikethrough.
- Open any code file and start typing — a grey inline suggestion should appear.

---

## 3. Key settings (`.vscode/settings.json`)

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "github.copilot.enable": {
    "*": true,
    "plaintext": false,
    "markdown": true
  },
  "github.copilot.editor.enableAutoCompletions": true,
  "github.copilot.nextEditSuggestions.enabled": true
}
```

`useInstructionFiles` must be `true` for `.github/copilot-instructions.md` to load.

---

## 4. Keyboard shortcuts

| Action | Windows/Linux | macOS |
| --- | --- | --- |
| Accept suggestion | `Tab` | `Tab` |
| Dismiss suggestion | `Esc` | `Esc` |
| Next suggestion | `Alt+]` | `Option+]` |
| Previous suggestion | `Alt+[` | `Option+[` |
| Accept word (partial) | `Ctrl+Right` | `Cmd+Right` |
| Open Copilot Chat | `Ctrl+Alt+I` | `Ctrl+Cmd+I` |
| Inline chat | `Ctrl+I` | `Cmd+I` |
| Quick chat | `Ctrl+Shift+Alt+L` | `Shift+Cmd+L` |

---

## 5. Chat modes

| Mode | How to activate | What it does |
| --- | --- | --- |
| Ask | Default | Answers in chat |
| Edit | `Ctrl+Shift+I` > Edit | Proposes file edits |
| Agent | Chat header dropdown | Uses tools, reads files, runs terminal |

---

## 6. Features specific to VS Code

- **Prompt files** — `.github/prompts/*.prompt.md` (VS Code 1.99+)
- **Agent mode** — autonomous multi-step task execution
- **MCP servers** — extend Copilot with external tools
- **Next Edit Suggestions (NES)** — predicts your next edit location

See [copilot-guide.md](../resources/copilot-guide.md) for full feature details.
For cross-IDE availability, use the canonical matrix: [ide-feature-matrix.md](../resources/ide-feature-matrix.md)
