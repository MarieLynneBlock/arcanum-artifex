---
name: [skill-name]
description: >
  [One sentence — what this skill enables the AI to do.
  This is used to decide when to load the skill, so be specific.]
version: 1.0.0
authors:
  - [your name or team]
tags:
  - [tag1]
  - [tag2]
---

<!--
  FILE NAMING: This folder is named skill_blank/ to distinguish it in the lab.
  When deploying to a project, copy this folder to:
    .github/skills/<skill-name>/
    .claude/skills/<skill-name>/        ← also works for Claude Code
    .agents/skills/<skill-name>/
  Remove the "_blank" suffix from the folder name.

  The Agent Skills specification is an open standard — this skill works with:
    - GitHub Copilot cloud agent
    - GitHub Copilot CLI
    - Agent mode in VS Code
    - Claude Code

  The AI loads this skill when the task matches the description above,
  or when the user explicitly references the skill name.

  FOLDER STRUCTURE:
    <skill-name>/
    ├── SKILL.md          ← this file (required)
    ├── scripts/          ← executable scripts the skill can call (optional)
    ├── resources/        ← reference files, templates, docs (optional)
    └── assets/           ← static files used by scripts (optional)
-->

## What this skill does

[Describe the specialised knowledge or behaviour this skill provides. What can the AI do
with this skill loaded that it cannot do without it?]

## When to use it

[Describe the task types or triggers that should activate this skill.
Be specific — this helps the AI decide whether to load it.]

## Instructions

[Step-by-step instructions the AI should follow when this skill is active.]

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output format

[Describe the expected output: file edits, terminal commands, a report, etc.]

## Examples

### Example 1 — [scenario]

**Input:** [describe the trigger or task]
**Expected output:** [describe what the AI should produce]

## Notes

- [Any constraints, limitations, or caveats]
- [Dependencies the skill assumes are available]
