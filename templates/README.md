# Templates

Blank starters to copy into your own project. Strip the `_blank` suffix (a lab-only marker), fill the `[TODO]` gaps, and deploy.

## Contents

| Template | Deploys to | Purpose |
| --- | --- | --- |
| [instructions/](instructions/) | `.github/copilot-instructions.md` | Stack-specific AI instructions (Python, Java, .NET, R, and more) |
| [prompts/](prompts/) | `.github/prompts/` | Reusable `.prompt.md` files (VS Code 1.99+) |
| [skills/](skills/) | `.github/skills/`, `.claude/skills/`, `.agents/skills/` | Empty skill shell to fill in (open Agent Skills standard) |
| [copilotignore_blank](copilotignore_blank) | `.copilotignore` | Exclude files from AI context |

## Conventions

- The `_blank` suffix marks a template as lab-only. Remove it when deploying.
- Prompt files require the `.prompt.md` extension and use the `agent:` frontmatter convention — see `../.github/prompts/` for working examples.
- Skills follow the house frontmatter schema (`name`, `description`, `version`, `tags`, `metadata.skill-author`); see `skills/skill_blank/SKILL.md`.
