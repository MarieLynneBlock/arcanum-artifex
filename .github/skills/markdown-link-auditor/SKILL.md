---
name: markdown-link-auditor
description: Audit relative Markdown links, image references, and local anchors in documentation repositories. Use when reviewing documentation changes, moving assets, updating indexes, or investigating broken links.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 1.0.0
---

# Markdown Link Auditor

Check that Markdown references resolve to the intended local files or valid external destinations without changing the author's content.

## When to use

- A Markdown file or folder was added, moved, or renamed.
- An index, README, guide, prompt, skill, workflow, or agent links to another asset.
- A review needs evidence that documentation references remain usable.

## Scope

Inspect Markdown links in the requested files and their nearby indexes. Include:

- Inline links: `[label](target)`
- Reference links: `[label][id]` and `[id]: target`
- Images: `![alt](target)`
- Autolinks only when they are intended to be navigable documentation references
- Fragment identifiers such as `README.md#installation`

Treat code blocks and inline code as examples unless the user explicitly asks to audit examples too.

## Procedure

1. Establish the audit root and the files in scope.
2. Read each Markdown file as text and collect links with a Markdown-aware parser or careful tokenisation that ignores fenced code blocks.
3. For relative links:
   - Resolve the target from the directory containing the source file.
   - Separate the path from its fragment identifier.
   - Confirm the target exists with the correct case.
   - For a fragment, confirm a matching heading slug or an explicit HTML anchor exists.
4. For absolute `http` and `https` links, report them as external dependencies. Check them only when network access is available and the user requests external validation.
5. Leave anchors, `mailto:`, and tool-specific URIs alone unless the repository defines a validator for them.
6. Report each failure with the source file, displayed label, target, and a concise correction.
7. Group duplicate failures when the same target is broken from multiple files.

## Expected results

Report one of these outcomes:

- `PASS`: every in-scope local reference resolves.
- `WARN`: local references pass, but external links or intentionally deferred targets were not checked.
- `FAIL`: one or more local paths or fragments do not resolve.

Do not silently rewrite links. If fixes are requested, change only the affected Markdown targets and preserve the existing style, naming, and link text.

## Repository-specific checks

For documentation-first repositories, also verify that:

- Index links point to the asset's real folder rather than a copied template.
- Moved assets have no stale links in the nearest README files.
- Standalone assets do not depend on links to another repository for required instructions.
- Relative links use `/` separators and remain valid from the source file's directory.
