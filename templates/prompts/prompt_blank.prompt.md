---
mode: ask
description: "[One sentence — what this prompt is for. Shown in the prompt picker.]"
# mode options: ask | edit | agent
# tools: optional list of MCP or VS Code tools this prompt may use
#   tools: ["github", "fetch"]
---

<!--
  FILE NAMING: Remove the "_blank" suffix when deploying to a project.
  Deploy to: .github/prompts/<name>.prompt.md

  Prompt files appear in the Copilot Chat prompt picker (VS Code 1.99+).
  Users invoke them with / in chat, or via the paperclip > Prompt... menu.

  Reference workspace files with #file: or #folder: to give Copilot context.
  Variables: ${workspaceFolder}, ${file}, ${selection}

  mode:
    ask    — Copilot answers in chat (default)
    edit   — Copilot proposes file edits
    agent  — Copilot uses tools and acts autonomously

  Docs: https://code.visualstudio.com/docs/copilot/copilot-customization#_reusable-prompt-files-experimental
-->

[Describe the task or context for this prompt. Be specific — Copilot uses this as the full instruction.]

## Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output format

[Describe the expected output: file edits, explanation, list, etc.]
