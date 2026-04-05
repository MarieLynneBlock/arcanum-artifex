# GitHub Copilot — Eclipse Setup Guide

Copilot support in Eclipse is more limited than in VS Code or JetBrains. Inline completions and basic chat are available; advanced features (agent mode, prompt files, MCP) are not.

---

## 1. Install

1. Open Eclipse.
2. Go to **Help → Eclipse Marketplace**.
3. Search **GitHub Copilot** and click **Install**.
4. Accept the license and restart Eclipse when prompted.

> Requires Eclipse 2023-03 (4.27) or later and Java 17+.

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
- Supports basic natural language questions about code.
- Supports `/explain` and `/fix` slash commands.
- Less context-aware than VS Code or JetBrains — attach files manually when needed.

---

## 6. Feature availability vs VS Code

| Feature | Eclipse |
| --- | --- |
| Inline completions | Yes |
| Copilot Chat | Basic |
| `.github/copilot-instructions.md` | Partial — verify per version |
| Prompt files (`.prompt.md`) | No |
| Agent mode | No |
| MCP servers | No |
| Next Edit Suggestions | No |

---

## 7. Notes

- Eclipse Copilot support is newer and less mature than VS Code or JetBrains.
- Feature availability changes frequently — check the [GitHub Copilot changelog](https://github.blog/changelog/label/copilot/) for updates.
- Primarily used in Java/.NET enterprise environments.
- If a team member has issues, try restarting Eclipse or re-authenticating via **Window → Preferences → GitHub Copilot → Sign out**, then sign in again.
