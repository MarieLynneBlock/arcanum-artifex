---
name: markdown-link-auditor
description: Audit Markdown links, images, and local anchors for broken relative references. Use when reviewing documentation changes, moving or renaming assets, updating indexes, or investigating broken links.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 1.1.0
---

# Markdown Link Auditor

Verify that documentation references resolve without changing content unless the user explicitly requests fixes.

## Use this skill when

- Markdown files, folders, or assets were added, moved, or renamed.
- An index, README, guide, prompt, skill, workflow, or agent was changed.
- A review needs evidence that local documentation references still work.

## Audit workflow

1. **Define scope.** Use the files and folders named by the user. If none are named, inspect the changed Markdown files and the nearest relevant index files. State the scope before reporting results.
2. **Reuse repository tooling.** Prefer an existing Markdown link checker or parser. Otherwise, tokenise Markdown carefully and ignore fenced code blocks and inline code unless the user asks to audit examples.
3. **Collect references.** Check inline links, reference-style links and definitions, images, and intentionally navigable autolinks. Preserve the displayed label and source location.
4. **Resolve local targets.**
   - Resolve relative paths from the source file's directory.
   - Split query or fragment identifiers from the path before checking the file.
   - Check the target exists with the repository's expected case.
   - For a fragment, match the rendered heading slug or an explicit HTML `id`/anchor. Apply the repository's slug rules when they are documented; otherwise use common GitHub-style slugging and note the assumption.
   - Treat `/` as the portable separator; do not accept a platform-specific `\` separator in a Markdown target.
5. **Classify non-local targets.** Resolve fragment-only links such as `#anchor` against the source file. Leave `mailto:` and tool-specific URIs alone. Treat `http` and `https` links as external dependencies: check them only when network access is available and the user requests external validation.
6. **Apply repository checks.** For documentation-first repositories, confirm index links point to the real asset, moved assets have no stale nearby links, and standalone assets do not rely on another repository for required instructions.
7. **Report before editing.** Group identical failures, and do not rewrite links unless fixes were requested. If fixes are requested, change only affected targets and preserve link text, naming, and style.

## Result format

Start with exactly one status:

- `PASS` — every in-scope local reference resolves.
- `WARN` — local references resolve, but external links or deferred targets were not checked.
- `FAIL` — one or more local paths or fragments do not resolve.

Then include:

- **Scope:** files and validation mode.
- **Findings:** for each failure, source file, line when available, displayed label, target, reason, and suggested correction.
- **External/deferred checks:** any links intentionally not validated.
- **Changes:** files edited, or `none`.

Never claim `PASS` when any in-scope local path or fragment is unresolved.
