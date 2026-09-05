---
name: asset-self-containment-check
description: Check that a Copilot customisation asset (skill, workflow, agent, instruction, or prompt folder) stays standalone and copyable, with no runtime dependency on paths outside its own folder. Use when packaging an asset for reuse, reviewing whether an asset can be copied out of this repo, or investigating why a copied asset breaks elsewhere.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 1.0.0
---

# Asset Self-Containment Check

Check one asset folder for hidden dependencies on the rest of this repository, then report or fix deviations. This is distinct from [markdown-link-auditor](../markdown-link-auditor/SKILL.md), which checks whether links *resolve*; this skill checks whether an asset's references *escape its own package* — the "packaging over linking" rule stated in this repo's `.github/copilot-instructions.md`.

## Use this skill when

- An asset is being prepared for copying into another repository or a personal customisation folder.
- A review needs evidence that an asset does not silently depend on sibling repo paths.
- An asset behaves correctly here but is suspected to break once extracted.

## What counts as an asset

A single self-contained unit: a `SKILL.md` folder, a `WORKFLOW.md` folder, one `*.agent.md` file (plus any folder it bundles resources in), one `*.instructions.md` file, or one `*.prompt.md` file.

## Audit workflow

1. **Define scope.** Identify the one asset folder or file to check. If the user names a parent folder containing multiple assets, ask which asset to check unless exactly one exists there.
2. **Inventory the asset.** List every file inside the asset folder (or the single file, for agents/instructions/prompts without a bundled folder).
3. **Scan for escaping references.** Search the asset's content for:
   - relative paths using `../` that resolve outside the asset folder
   - absolute paths beginning with `/`, `~`, a drive letter (e.g. `C:\`), or a user-specific home folder
   - `#file:` or `#folder:` references that point outside the asset folder
   - markdown links or file references targeting `skills/`, `workflows/`, `agents/`, `instructions/`, `templates/`, or other top-level repo folders from outside the asset's own tree
4. **Check referenced-but-unbundled resources.** For every script, template, schema, example, or data file the asset's instructions mention, confirm the file actually exists inside the asset folder. Flag any resource that is described but not bundled.
5. **Check prose assumptions.** Look for language that assumes another repo path exists or another asset is present at runtime, such as "see the shared template in `templates/`" or "run the script in `scripts/common/`" without vendoring it locally. A reference to another asset for inspiration or cross-linking in documentation (e.g. "see also") is acceptable; a runtime dependency for the asset to function is not.
6. **Distinguish acceptable exceptions.** Repo-root context files (`.github/copilot-instructions.md`, root `README.md`) may be referenced as background reading without being a packaging violation, but only if the asset does not require them to function correctly once copied elsewhere. Note these explicitly rather than silently passing or failing them.
7. **Report before editing.** Group identical issues by type. Do not rewrite content unless fixes were requested. If fixes are requested, vendor the missing resource into the asset folder or remove the outward dependency, preserving the asset's intent and style.

## Result format

Start with exactly one status:

- `PASS` — the asset has no references that escape its own folder, and all mentioned resources are bundled.
- `WARN` — the asset references repo-root context files as background reading only, or has deferred/external (e.g. `http`/`https`) references not checked for reachability.
- `FAIL` — the asset requires a path, file, or resource outside its own folder to function correctly.

Then include:

- **Scope:** the asset folder or file checked.
- **Findings:** for each issue, file, line when available, the escaping reference or missing resource, why it breaks standalone packaging, and a suggested fix (vendor the file, remove the reference, or convert to documented external prerequisite).
- **Acceptable exceptions:** repo-root or background references noted as non-blocking, with justification.
- **Changes:** files edited, or `none`.

Never claim `PASS` when the asset requires an unbundled path outside its own folder to work.
