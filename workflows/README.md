# Workflows

Orchestrated playbooks that link together skills, instructions, agents, prompts, templates, and external tools to deliver a complete outcome.

**A workflow is a self-contained, drop-in folder.** Every skill and instruction it depends on is **vendored** under `assets/` so the entire workflow folder can be copied into any other repo and run without dragging the rest of this repo along. That portability is the whole point.

A workflow is the right home for any sequence of work that:

- Spans **two or more** existing assets in this repo (e.g. a skill + an instruction + an agent), AND
- Has its **own glue** — a prompt, a thin agent, a template, or a script — that doesn't naturally belong inside any single one of those assets.

If a single skill or single agent is enough on its own, keep it there. Workflows exist to compose, not to duplicate.

---

## When to build a workflow vs. just a skill

| Build a... | When |
|------------|------|
| **Skill** | The procedure is self-contained, owned by one domain, and reusable across many contexts. |
| **Instruction** | A file-type or path needs an always-on convention (e.g. all `.drawio` files). |
| **Agent** | A persona/role with a stable identity needs to be invokable on demand. |
| **Workflow** | You need to combine several of the above into a sequenced playbook for a specific outcome, and need a place to keep workflow-only assets (prompts, agents, templates) that no single skill should own. |

---

## Folder convention

Every workflow lives in its own folder under `workflows/`:

```text
workflows/
├── README.md                              ← this file
├── _template/                             ← blank scaffold (underscore = not a workflow itself)
│   ├── README.md
│   ├── WORKFLOW.md
│   └── assets/
└── <workflow-name>/
    ├── README.md                          ← human-facing summary, when to use, how to invoke
    ├── WORKFLOW.md                        ← the orchestration playbook (the "source of truth")
    ├── assets/                            ← everything the workflow needs at runtime
    │   ├── skills/                        ← vendored copies of skills the workflow depends on
    │   ├── instructions/                  ← vendored copies of instruction files
    │   ├── agents/                        ← .agent.md files specific to this workflow
    │   ├── prompts/                       ← .prompt.md files specific to this workflow
    │   ├── templates/                     ← templates produced or consumed by the workflow
    │   └── references/                    ← supplementary reference material
    └── examples/                          ← worked examples / sample outputs
```

Naming rules:

- Workflow folders use `kebab-case` and start with the **outcome**, not the tool (`architecture-4plus1-with-drawio`, not `drawio-and-skills`).
- A folder prefixed with `_` (e.g. `_template/`) is scaffolding, not a workflow — runners should ignore it.
- `WORKFLOW.md` is the canonical orchestration document. `README.md` is for humans browsing the folder.

---

## What a `WORKFLOW.md` must contain

1. **Purpose** — one paragraph: what outcome does running this workflow produce?
2. **Linked assets** — explicit table of every skill / instruction / agent / prompt / template / external tool the workflow references, with relative paths.
3. **Preconditions** — what must be true before starting (extensions installed, files open, audience known, etc.).
4. **Steps** — numbered, sequenced. Each step says **which asset is invoked**, **what input it needs**, and **what output it produces**.
5. **Outputs** — the final file tree the workflow leaves behind.
6. **Validation** — how to verify the workflow ran correctly.

Keep `WORKFLOW.md` short. Push detail down into the linked skills and references — do not duplicate.

---

## Index

| Workflow | Outcome | Status |
|----------|---------|--------|
| [architecture-4plus1-with-drawio](architecture-4plus1-with-drawio/) | Produce a 4+1 architectural view model with both Mermaid (primary) and editable drawio & miro diagrams per view. | Active |

---

## Conventions

- **Self-contained.** Every skill and instruction the workflow needs at runtime is vendored under `assets/skills/` and `assets/instructions/`. The workflow folder must run after being copied to any other repo, with no other files from this repo present.
- **Strict snapshot.** Workflows are shipped as complete snapshots. No sync scripts, no manifests, and no update contract to repo-level assets.
- **No invented capabilities.** Workflows must only reference assets that actually exist (vendored locally or genuinely installed external tools). Verify paths.
- **No MCP requirement** unless every linked tool is documented as MCP-only. Where an MCP server would be the natural choice but is unavailable (e.g. restricted environments), the workflow generates the artefact directly (e.g. write `.drawio` XML to disk instead of calling a draw.io MCP).
