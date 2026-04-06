# GitHub Copilot — Eclipse Setup Guide

Eclipse supports inline completions, Copilot Chat, agent mode, and MCP tools. Some capabilities require newer Eclipse and extension versions.

---

## 1. Install

1. Open Eclipse.
2. Go to **Help → Eclipse Marketplace**.
3. Search **GitHub Copilot** and click **Install**.
4. Accept the license and restart Eclipse when prompted.

> Requires Eclipse 2024-09 (4.33) or later for current Copilot Chat, agent mode, and MCP workflows.

---

## 2. Sign in

1. After restart, go to **Window → Preferences → GitHub Copilot**.
2. Click **Sign in with GitHub** and complete the device code flow in your browser.

---

## 3. Verify

- Status bar (bottom right): Copilot icon appears.
- Open a Java (or other supported) file and start typing — inline suggestions appear.

---

## 4. Keyboard shortcuts

| Action | Shortcut |
| --- | --- |
| Accept suggestion | `Tab` |
| Dismiss suggestion | `Esc` |
| Next suggestion | `Alt+]` |
| Previous suggestion | `Alt+[` |
| Open Copilot Chat | `Ctrl+Shift+G` |

> Shortcuts may vary by Eclipse version and keymap. Check **Window → Preferences → General → Keys** and search "Copilot".

---

## 5. Chat

- Open via **Window → Show View → GitHub Copilot Chat**.
- Supports natural language questions, slash commands, plan mode, and agent mode.
- Supports MCP tools when configured.
- Less context-aware than VS Code or JetBrains — attach files manually when needed.

---

## 6. Feature availability vs VS Code

See the canonical IDE matrix: [ide-feature-matrix.md](../resources/ide-feature-matrix.md)

---

## 7. Notes

- Eclipse Copilot support is newer and less mature than VS Code or JetBrains.
- Feature availability changes frequently — check the [GitHub Copilot changelog](https://github.blog/changelog/label/copilot/) for updates.
- Primarily used in Java/.NET enterprise environments.
- If a team member has issues, try restarting Eclipse or re-authenticating via **Window → Preferences → GitHub Copilot → Sign out**, then sign in again.
