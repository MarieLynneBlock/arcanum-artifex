# GitHub Copilot — Troubleshooting Guide

Common issues and how to resolve them, organised by IDE and symptom.

---

## 1. General checks (all IDEs)

Before diagnosing a specific issue:

- [ ] Copilot icon in the status bar — is it present and without a strikethrough?
- [ ] GitHub account is signed in and has an active Copilot seat.
- [ ] IDE extension is up to date.
- [ ] Internet connection is active (Copilot requires outbound HTTPS).

---

## 2. "Copilot isn't suggesting anything"

**Check 1 — Is Copilot enabled for this language?**
- VS Code: `github.copilot.enable` in settings — check the language key.
- JetBrains: Settings → Tools → GitHub Copilot → check language list.
- Visual Studio: Tools → Options → GitHub → Copilot.

**Check 2 — Is the file type recognised?**
Copilot works with most programming languages but not all file types. Plain text, binary files, and some config formats may not trigger suggestions.

**Check 3 — Is the file in `.copilotignore` or a content exclusion?**
If the file path matches an org-level content exclusion or `.copilotignore`, Copilot will silently skip it.

**Check 4 — Is `enableAutoCompletions` set to false?**
VS Code: check `github.copilot.editor.enableAutoCompletions` in settings.

**Check 5 — Is there enough context?**
Very short files or files with no imports/comments give Copilot little to work with. Try adding a comment describing the task.

---

## 3. Authentication issues

**"Sign in" prompt keeps appearing:**
1. Sign out completely: IDE menu → GitHub Copilot → Sign out.
2. Clear any cached credentials.
3. Sign in again via the IDE prompt.

**"Your organisation has not enabled Copilot":**
- Contact your GitHub org admin — your account may not have a seat assigned.

**"Copilot is not available for your account":**
- Check your GitHub account has an active Copilot subscription or has been granted a seat by the org admin.

---

## 4. Proxy and network issues (enterprise)

Enterprise environments often route traffic through a proxy. Copilot requires HTTPS access to `copilot-proxy.githubusercontent.com` and related GitHub endpoints.

**VS Code:**
```json
{
  "http.proxy": "http://your-proxy:port",
  "http.proxyStrictSSL": false
}
```

**JetBrains:**
Settings → Appearance & Behavior → System Settings → HTTP Proxy.

**Visual Studio:**
Tools → Options → Environment → Network → Proxy settings.

**Check with your network team:**
- Is `*.githubcopilot.com` whitelisted?
- Is `copilot-proxy.githubusercontent.com` whitelisted?
- Is SSL inspection intercepting Copilot traffic? (Certificate pinning issues)

---

## 5. VPN issues

Copilot may stop working or degrade when a VPN is active if the VPN routes GitHub traffic differently.

- Test with VPN on vs VPN off.
- If VPN is the issue, work with your network team to split-tunnel GitHub endpoints.
- Some enterprises require Copilot traffic to go through their proxy even when VPN is active — configure the proxy setting above.

---

## 6. VS Code specific

**Chat panel not appearing:**
- Ensure both `GitHub Copilot` and `GitHub Copilot Chat` extensions are installed.
- Try: View → GitHub Copilot Chat.

**`copilot-instructions.md` not being applied:**
- Confirm `github.copilot.chat.codeGeneration.useInstructionFiles` is `true` in settings.
- The file must be at exactly `.github/copilot-instructions.md` in the repo root.

**Prompt files not appearing in picker:**
- Requires VS Code 1.99+. Check your VS Code version.
- File must have `.prompt.md` extension (not `.md`).
- File must be in `.github/prompts/`.

**Next Edit Suggestions not working:**
- Requires `github.copilot.nextEditSuggestions.enabled: true`.
- Feature may not be available in all VS Code versions — check the Copilot changelog.

---

## 7. JetBrains specific

**Plugin installed but no suggestions:**
1. Restart the IDE after install.
2. Check: Tools → GitHub Copilot → Show Copilot Status.
3. Try invalidating caches: File → Invalidate Caches → Invalidate and Restart.

**Shortcut conflicts:**
JetBrains keymaps may conflict with Copilot shortcuts (especially `Tab` and `Alt+]`).
Remap in: Settings → Keymap → GitHub Copilot.

---

## 8. Performance issues

**Suggestions are slow:**
- Copilot requires a round-trip to GitHub's servers. Latency depends on network quality.
- On a VPN or proxy, extra hops add latency.
- Very large files slow down context processing — consider splitting large files.

**IDE becomes sluggish with Copilot:**
- JetBrains: increase heap size in Help → Change Memory Settings.
- VS Code: check extension host memory in Help → Open Process Explorer.

---

## 9. Escalation path

If none of the above resolves the issue:

1. Check [GitHub Copilot status](https://githubstatus.com) — there may be a service incident.
2. Check the IDE's Copilot extension GitHub issues for known bugs.
3. Collect: IDE version, extension version, OS, error message or screenshot.
4. Report to: GitHub Support (for account/access issues) or your internal IT helpdesk (for network/proxy issues).
