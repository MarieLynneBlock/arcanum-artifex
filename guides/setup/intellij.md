# GitHub Copilot — IntelliJ IDEA Setup Guide

IntelliJ IDEA is primarily used for Java, Kotlin, and JVM-based projects. Copilot is installed as a plugin — same plugin as all JetBrains IDEs.

---

## 1. Install

1. Open IntelliJ IDEA.
2. Go to **Settings / Preferences** → **Plugins** → **Marketplace**.
3. Search **GitHub Copilot** and install.
4. Restart the IDE when prompted.
5. Go to **Tools → GitHub Copilot → Login to GitHub** and authenticate.

> Alternatively, install from [plugins.jetbrains.com](https://plugins.jetbrains.com/plugin/17718-github-copilot).

---

## 2. Verify

- Status bar (bottom right): Copilot icon appears.
- Open a `.java` or `.kt` file and start typing — a grey inline suggestion should appear.

---

## 3. Settings

Go to **Settings / Preferences → Tools → GitHub Copilot**.

Key options:
- Enable/disable Copilot globally.
- Enable/disable per language.
- Configure proxy if needed.

There is no `settings.json` equivalent — configuration is IDE-native via the Settings UI.

---

## 4. Keyboard shortcuts

| Action | Windows/Linux | macOS |
| --- | --- | --- |
| Accept suggestion | `Tab` | `Tab` |
| Dismiss suggestion | `Esc` | `Esc` |
| Next suggestion | `Alt+]` | `Option+]` |
| Previous suggestion | `Alt+[` | `Option+[` |
| Accept word (partial) | `Ctrl+Right` | `Cmd+Right` |
| Open Copilot Chat | `Ctrl+Shift+C` | `Ctrl+Shift+C` |
| Inline chat | `Ctrl+I` | `Ctrl+I` |

> Shortcuts can be remapped in **Settings → Keymap → GitHub Copilot**.

---

## 5. Chat

- Open via **Tools → GitHub Copilot → Open Chat** or the chat icon in the toolbar.
- Supports `@` context references (e.g. `@file`, `@project`).
- Supports `/` slash commands: `/explain`, `/fix`, `/tests`, `/doc`.
- Supports Copilot Edits (including agent mode) and MCP tools in recent plugin versions.

---

## 6. Feature availability vs VS Code

See the canonical IDE matrix: [ide-feature-matrix.md](../resources/ide-feature-matrix.md)

The repo-level instructions file (`.github/copilot-instructions.md`) is respected — keep it in every project regardless of IDE.
