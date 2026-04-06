# GitHub Copilot — Visual Studio Setup Guide

Covers Visual Studio 2022 on Windows. Copilot is bundled from version 17.10+; earlier versions require a manual extension install.

---

## 1. Install

### Visual Studio 2022 17.10 and later (bundled)

1. Open **Visual Studio Installer**.
2. Click **Modify** on your VS 2022 installation.
3. Under **Individual components**, search **GitHub Copilot** and check it.
4. Click **Modify** to apply.

### Earlier versions

1. Go to **Extensions → Manage Extensions**.
2. Search **GitHub Copilot** in the Online marketplace.
3. Download and install, then restart Visual Studio.

### Sign in

Go to **Tools → Options → GitHub → Copilot** and sign in with your GitHub account.

---

## 2. Verify

- Status bar (bottom right): Copilot icon appears.
- Open a code file and start typing — inline suggestions appear in grey.

---

## 3. Settings

Go to **Tools → Options → GitHub → Copilot**.

Key options:
- Enable/disable Copilot.
- Enable/disable inline suggestions.
- Set suggestion display delay.

---

## 4. Keyboard shortcuts

| Action | Shortcut |
| --- | --- |
| Accept suggestion | `Tab` |
| Dismiss suggestion | `Esc` |
| Next suggestion | `Alt+]` |
| Previous suggestion | `Alt+[` |
| Open Copilot Chat | `Ctrl+\`, `Ctrl+C` |
| Inline chat | `Alt+/` |

> Shortcuts can be remapped in **Tools → Options → Environment → Keyboard**.

---

## 5. Chat

- Open via **View → GitHub Copilot Chat** or the chat icon in the toolbar.
- Supports `/` slash commands: `/explain`, `/fix`, `/tests`, `/doc`, `/optimize`.
- Supports `#` file references to attach context.

---

## 6. Feature availability vs VS Code

See the canonical IDE matrix: [ide-feature-matrix.md](../resources/ide-feature-matrix.md)

---

## 7. Notes

- Visual Studio is Windows-only. Mac developers use VS Code or Rider.
- Primarily used for C#, .NET, C++, and ASP.NET projects.
- Agent mode and MCP tools require Visual Studio 17.14 or later.
- The `.github/copilot-instructions.md` file is respected — keep it in every project.
