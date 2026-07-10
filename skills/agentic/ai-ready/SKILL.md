---
name: ai-ready
description: 'Guide users to review and install the external ai-ready skill from its upstream repository. Use when the user asks to install or try John Papa''s ai-ready skill.'
metadata:
  skill-author: 'Marie-Lynne Block'
---

# AI Ready

This skill helps the user review and install the external [ai-ready](https://github.com/johnpapa/ai-ready) `SKILL.md` by [John Papa](https://github.com/johnpapa) into their personal skills directory.

*Why?*: The full ai-ready skill is maintained upstream and may change over time. This helper is a self-contained installer guide; the upstream repository remains an explicit external prerequisite.

## External prerequisite

This package does not vendor the upstream ai-ready skill. Before installing it, ask the user to review the source repository and confirm they are comfortable downloading that external content.

## Steps

1. Tell the user to download the latest `SKILL.md` to their personal skills directory by running one of these commands in their terminal. This will overwrite any existing local copy.

   **bash / zsh**
   ```bash
   mkdir -p ~/.copilot/skills/ai-ready
   curl -fsSL https://raw.githubusercontent.com/johnpapa/ai-ready/main/skills/ai-ready/SKILL.md \
     -o ~/.copilot/skills/ai-ready/SKILL.md
   ```

   **PowerShell**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$HOME/.copilot/skills/ai-ready" | Out-Null
   Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/johnpapa/ai-ready/main/skills/ai-ready/SKILL.md" -OutFile "$HOME/.copilot/skills/ai-ready/SKILL.md"
   ```

   For reproducible behaviour, the user can replace `main` in the URL with a specific tag or commit SHA.
2. Suggest the user review the downloaded skill before loading it to confirm it contains expected instructions:
   ```bash
   head -20 ~/.copilot/skills/ai-ready/SKILL.md
   ```
3. After the user confirms they've installed it, tell them to reload skills with `/skills reload` and then say `make this repo ai-ready`.
4. Do **not** run the install command on the user's behalf. The user must run it themselves.
