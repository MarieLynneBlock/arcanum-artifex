---
name: asset-frontmatter-check
description: Validate YAML frontmatter of Copilot customisation assets in this lab (SKILL.md, WORKFLOW.md, *.agent.md, *.instructions.md, *.prompt.md). Use when adding, reviewing, or fixing an asset's frontmatter, or when asked to check whether an asset follows repository conventions.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 1.0.0
---

# Asset Frontmatter Check

Check that a customisation asset carries the frontmatter this repository expects, then report or fix deviations.

## When to use

- A new asset was added under `skills/`, `workflows/`, `agents/`, `instructions/`, or `templates/`.
- An asset is ignored by VS Code and the frontmatter is the suspect.
- A review asks whether assets follow repository conventions.

## Required shapes

Field order matters where shown.

**`SKILL.md`**

```yaml
---
name: (kebab-case name matching the folder)
description: (what it does and when to use it)
metadata:
  skill-author: (author name)
  version: x.x.x
---
```

**`WORKFLOW.md`**

```yaml
---
name: (kebab-case name matching the folder)
description: (what it does and when to use it)
metadata:
  workflow-author: (author name)
  version: x.x.x
---
```

**`*.agent.md`**

```yaml
---
description: (discovery-friendly description)
metadata:
  agent-author: (author name)
  version: x.x.x
---
```

Keep `name`, `tools`, and `model` only when they add clear value.

**`*.instructions.md`**

```yaml
---
description: (description)
applyTo: (glob)
metadata:
  instruction-author: (author name)
  version: x.x.x
---
```

`metadata` is the last field when present.

## Procedure

1. Identify the asset type from the file name and location.
2. Read the frontmatter block only; do not rewrite body content.
3. Check, in order:
   - Frontmatter opens on line 1 with `---` and closes with `---`.
   - YAML parses: two-space indentation, quoted strings containing `:` or starting with a special character.
   - All required fields for the type are present and non-empty.
   - Field order matches the shape above.
   - `description` states both what the asset does and when to use it.
   - `name` (skills and workflows) is kebab-case and matches the containing folder name.
   - `applyTo` (instructions) is a glob that actually matches files in this repo.
4. Report findings as a short list: file, issue, suggested fix.
5. Apply fixes only to frontmatter, and only when the user asked for fixes.

## Notes

- The `_blank` suffix under `templates/` is a lab-only convention; template files are exempt from the `name`-matches-folder check.
- Do not invent authors or versions. Use `[TODO]` when a value is genuinely unknown.
