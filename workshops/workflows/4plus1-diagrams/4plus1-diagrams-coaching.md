# Code-to-Coach: the `4plus1-diagrams` agentic workflow

A teaching document for coaches who use the `4plus1-diagrams` workflow as a worked example of a *complex agentic workflow bundle*. The aim is not to describe what each file does. The aim is to teach **how to think about agentic workflows that orchestrate multiple skills, output tracks, and validation surfaces inside a strictly standalone package**.

This bundle is large enough to expose every interesting design tension, but small enough to hold in a learner's head in one session. Use it to coach the underlying patterns; the specific architecture domain is incidental.

---

## How to use this document

Coach in five passes, mirroring the Code-to-Coach cycle:

1. **Orient** — situate the workflow: what it produces, who triggers it, and what failure modes it prevents.
2. **Deconstruct** — break the bundle into eight teachable chunks; name each by its job.
3. **Analyse** — evaluate each chunk against an agentic-workflow rubric (clarity, single responsibility, contract strength, drift surface, mechanical testability).
4. **Teach** — surface the seven design decisions that make this bundle behave the way it does, and the trade-offs behind each.
5. **Advise** — give learners the reusable questions and patterns they can apply to any agentic workflow they design or review next.

Each pass builds intuition. Resist the temptation to jump to "what would you change?" before the learner can articulate what the bundle is *trying to protect*.

---

## Step 1 — Orient: scope and context

### What the workflow produces

A complete Kruchten 4+1 architecture documentation set, in two synchronised layers:

1. **Canonical diagram-as-code**: Mermaid for logical, process, development, and scenarios views; PlantUML for the physical view.
2. **Editable visual artefacts**: `.drawio` files, Miro board prompts, or both — generated *from* the canonical source, never replacing it.

Five view files (`01-logical-view.md` … `05-scenarios-view.md`) and a system-context overview (`00-system-context.md`) sit alongside, written in prose with embedded references to the diagrams.

Output lands under typed subfolders: `diagrams/mermaid/`, `diagrams/drawio/`, `diagrams/miro/`. Only the subfolders for selected tracks are created.

### Who triggers it

- Architects producing end-to-end system documentation.
- Technical leads preparing views for mixed technical and non-technical stakeholders.
- Teams running architecture workshops who need editable visuals on a Miro board *and* durable text in git.
- Maintainers who need a copyable bundle that runs in any repo with no install step.

### What problem it solves

Without this workflow, a team typically generates Mermaid diagrams once, then manually recreates each view in draw.io or Miro for stakeholders. Three failure modes follow:

- **Name drift** — a service is "Claims API" in Mermaid and "ClaimSvc" in the Miro board. The two diagrams describe different systems within a week.
- **Invented infrastructure** — the visual editor's template ships with a CDN, cache, or load balancer; nobody removes it; the deployment diagram now claims components that do not exist.
- **Bundle decay** — the working assets live across `.github/skills/`, `.github/instructions/`, internal templates, and the user's own notes. Copying the workflow to another repo means hunting six places.

The workflow defends against all three: canonical first, tracks generated from canonical with parity checks, everything bundled under one folder.

### Design signals worth pointing out before deconstructing

These are the signals that show this workflow was designed deliberately — not assembled. Coaches should name them early so learners notice them recurring through the analysis:

- A **discoverable root launcher** (`architecture-documentation.agent.md`) that delegates rather than executes.
- A **thin orchestrator agent** (`agents/architecture-documentation.agent.md`) that composes skills but does not absorb their internals.
- A **playbook** (`WORKFLOW.md`) that is the single execution source of truth.
- **Three skills** with non-overlapping ownership: method, draw.io output, Miro output.
- **Independent output tracks** chosen at intake, never blended.
- A **bundled asset manifest** with hash-tracked snapshots (`vendored-assets-manifest.json`).
- **Mechanical validation** at three layers: bundle integrity (`scripts/smoke-test.py`), cross-view consistency (`skills/4plus1-models/scripts/validate-views.py`), and per-format validity (`skills/draw-io-diagram-generator/scripts/validate-drawio.py`).
- **Typed output subfolders** enforced by smoke-test rules.
- **Frontmatter order discipline** enforced across every entry file (`name`, `description`, `metadata`).

The teaching pattern under all of these is the same: **one source of truth per concern, independent tracks where the work is genuinely different, and machine-checkable contracts at every join**.

---

## Step 2 — Deconstruct: eight chunks

Use these chunks as the unit of teaching. Each chunk has one job. The relationships between chunks are where most of the design lessons live.

### Chunk 1 — Discoverable launcher

**File:** [`architecture-documentation.agent.md`](../../../workflows/4plus1-diagrams/architecture-documentation.agent.md) at the bundle root.

**Job:** Make the bundle discoverable when the folder is dropped under `.github/agents/` (repo scope) or `~/.agents/` (user scope), with no install step. Tell the agent runtime that the *real* orchestration lives one folder down.

**What to notice:** It explicitly names the orchestrator, the playbook, and the prompt. It declares `tools: []`. It enforces a "clean start, compact intake" rule and stops there.

**Teaching point:** This is a wrapper. Wrappers earn their cost when they give the user a stable entrypoint while keeping behaviour somewhere reusable.

### Chunk 2 — Thin orchestrator agent

**File:** [`agents/architecture-documentation.agent.md`](../../../workflows/4plus1-diagrams/agents/architecture-documentation.agent.md).

**Job:** Coordinate a run. Load the right skills, ask the smallest useful intake, branch on track choice, enforce cross-cutting guardrails (no MCP, both formats equal, tracks independent, physical-view source parity, audience always asked).

**What to notice:** It names the *authority boundary* of each loaded skill ("authoritative for everything 4+1 core logic", "authoritative for everything draw.io"). It refuses to paraphrase the playbook from memory and tells the agent to read `WORKFLOW.md`.

**Teaching point:** A good orchestrator owns sequencing and boundaries. It does not own the internals of any subsystem it composes. When you find an orchestrator absorbing domain detail, that is the symptom of a missing skill.

### Chunk 3 — Workflow playbook

**File:** [`WORKFLOW.md`](../../../workflows/4plus1-diagrams/WORKFLOW.md).

**Job:** Be the human-readable source of truth for the full run. Define preconditions, the per-view loop, output contracts (Option A / B / A+B), routing tables (per-view skeleton selection by audience), validation expectations, the recovery loop, and the change log.

**What to notice:** The playbook contains a **per-view skeleton routing table** (§4a) and a **Miro board structure reference** (§4b) so that branching decisions are explicit, not implicit. §7 documents the *expected exit-code contract* of each script — including that `validate-views.py` always returns 0 when it ran (warnings are advisory) and only returns 1 on fatal setup errors.

**Teaching point:** In documentation-first systems, the playbook plays the role of application control flow. Every dependent surface (launcher, orchestrator, prompt) defers to it. Drift between any of them and the playbook is a bug.

### Chunk 4 — Core 4+1 method skill

**Folder:** [`skills/4plus1-models/`](../../../workflows/4plus1-diagrams/skills/4plus1-models/).

**Job:** Own the 4+1 method end-to-end *up to but not including* output rendering: invocation mode, audience routing, context capture, concern routing, per-view content generation, canonical Mermaid/PlantUML output, cross-view consistency.

**What to notice:** The skill explicitly disclaims ownership of draw.io and Miro mechanics. Its references folder carries the per-view detail (`logical-view.md`, `process-view.md`, …) and notation cheatsheets (`notation-mermaid.md`, `notation-plantuml.md`, `notation-bpmn-in-mermaid.md`). Its `concerns/` folder contains pluggable concern modules (GDPR, security, bias, regulatory, sustainability, accessibility) routed in by Step 4.

**Teaching point:** This is the **domain core**. Output formats depend on it; it depends on no output format. When you can pull a skill out of a workflow and run it standalone, you have evidence the boundary is clean.

### Chunk 5 — Track decision

**Surfaces:** Step 2 in the prompt, agent, and `WORKFLOW.md`.

**Job:** Choose draw.io, Miro, or both, exactly once, at intake. Treat each chosen track as independent for the rest of the run.

**What to notice:** The decision is asked as a single question with three options. The agent guardrail says *do not import style or mechanics from one track into the other*. Only the typed subfolders for the chosen tracks are created.

**Teaching point:** Branching is not a design smell when the branches represent genuinely different *modes of work*. draw.io is an XML authoring problem; Miro is a prompt authoring problem. A unified abstraction would hide that difference and make both worse.

### Chunk 6 — draw.io output track

**Files:** [`skills/draw-io-diagram-generator/`](../../../workflows/4plus1-diagrams/skills/draw-io-diagram-generator/), [`instructions/draw-io.instructions.md`](../../../workflows/4plus1-diagrams/instructions/draw-io.instructions.md), [`templates/drawio/`](../../../workflows/4plus1-diagrams/templates/drawio/) (eight per-view skeletons), [`references/notation-drawio.md`](../../../workflows/4plus1-diagrams/references/notation-drawio.md).

**Job:** Convert each canonical view into a valid mxGraph XML file, starting from a per-view skeleton, applying view-specific shape libraries, palette, layout, edge style, and embedding hidden canonical-source provenance.

**What to notice:**

- The eight skeletons cover the per-view variants the routing table refers to (process sequence vs. process BPMN; physical AWS vs. Azure vs. generic).
- Each workflow-level template carries a `canonical-source-ref` provenance cell so the file remains traceable when copied outside the repo.
- `scripts/validate-drawio.py` checks XML well-formedness, root cells `0` and `1`, parent references, geometry presence, edge endpoints, and (when invoked with `--require-provenance`) the provenance cell.
- The skill keeps generic templates (flowchart, ER, UML class, sequence, architecture) for non-4+1 use, separate from the workflow-level per-view skeletons.

**Teaching point:** Most failures here are structural — malformed XML, dangling parent ids, missing provenance, geometry typos. Structural validators catch them cheaply. Semantic parity (does the diagram actually mean what the canonical source says?) is still a human or agent responsibility.

### Chunk 7 — Miro output track

**Files:** [`skills/miro-diagram-generator/`](../../../workflows/4plus1-diagrams/skills/miro-diagram-generator/), [`instructions/miro.instructions.md`](../../../workflows/4plus1-diagrams/instructions/miro.instructions.md), [`templates/miro/`](../../../workflows/4plus1-diagrams/templates/miro/) (per-view + full-board), [`references/notation-miro.md`](../../../workflows/4plus1-diagrams/references/notation-miro.md).

**Job:** Convert each canonical view into a precise Miro board prompt — RISEN structure (Role, Input, Steps, Expectation, Narrowing), exact frame title, exact shape and arrow counts, exact labels, explicit exclusions, and a canonical-source reference section so the prompt stands alone when copied.

**What to notice:**

- The skill keeps two template files duplicated: one workflow copy under `templates/miro/`, one skill-internal copy under `skills/miro-diagram-generator/templates/`. The smoke test enforces byte-equality between the pair.
- Per-view conventions live in `references/notation-miro.md` (frame naming, shape semantics, palette, layout discipline).
- Validation is checklist-driven, not script-driven: naming pattern (`<view>-miro-prompt.md`), template sections present, names matching canonical source, no unlabelled arrows, no decorative elements outside scope.
- For Physical view, the prompt expands the `.puml` into an explicit object manifest before layout instructions, because asking Miro to "parse PlantUML" produces drift.

**Teaching point:** This is a prompt-output track. Failures here are *ambiguity bugs*: missing counts, vague labels, scope leak, asking the consumer to infer too much. The mitigation is determinism — say exactly what objects, exactly what labels, exactly what is out of scope.

### Chunk 8 — Validation and maintenance

**Files:**

- [`scripts/smoke-test.py`](../../../workflows/4plus1-diagrams/scripts/smoke-test.py) — bundle integrity.
- [`skills/4plus1-models/scripts/validate-views.py`](../../../workflows/4plus1-diagrams/skills/4plus1-models/scripts/validate-views.py) — cross-view consistency.
- [`skills/draw-io-diagram-generator/scripts/validate-drawio.py`](../../../workflows/4plus1-diagrams/skills/draw-io-diagram-generator/scripts/validate-drawio.py) — per-file draw.io validity.
- [`scripts/inject-and-validate-provenance.py`](../../../workflows/4plus1-diagrams/scripts/inject-and-validate-provenance.py) — idempotent provenance-cell injector for workflow-level draw.io templates, followed by validator run with `--require-provenance`.
- [`scripts/sync-vendored-assets.py`](../../../workflows/4plus1-diagrams/scripts/sync-vendored-assets.py) and [`vendored-assets-manifest.json`](../../../workflows/4plus1-diagrams/vendored-assets-manifest.json) — bundle snapshot integrity.

**Job:** Make the bundle's correctness *executable*. The smoke test alone enforces:

| Check | Why it matters |
|---|---|
| Required paths exist | Missing files break copy-and-run portability. |
| Entry frontmatter order (`name`, `description`, `metadata` last; `skill-author` under metadata) | Discoverability tooling and downstream parsers depend on the order. |
| Markdown links resolve and never escape the bundle root | Standalone packaging guarantee. |
| Forbidden stale text absent (e.g. `.github/skills/`, legacy skill name, flat per-view prompt names) | Catches half-done refactors. |
| Output contract: no flat `diagrams/<file>` paths in scope files; trees show typed subfolders | Enforces the typed-subfolder convention everywhere it is documented. |
| Canonical view filenames (`00-system-context.md`, `01..05-<view>.md`) | Prevents naming drift between WORKFLOW.md, prompts, agents, and skill output specs. |
| `validate-views.py` invocations include the positional directory argument | Catches docs that show the wrong invocation. |
| Miro template parity (workflow vs. skill copy) | The deliberate duplication is allowed only while bytes match. |
| draw.io templates parse and pass the validator (workflow templates also require provenance) | Skeletons cannot ship broken. |
| Bundled asset hashes match the manifest (with `--check-skew`) | Snapshot integrity. |

**Teaching point:** Documentation-first projects have no application build to fail. The smoke test *is* the build. A learner who internalises this stops thinking of validators as optional.

---

## Step 3 — Analyse: chunk-by-chunk quality rubric

Use this table format with learners. The columns generalise to any agentic workflow.

### Chunk 1 — Discoverable launcher

| Quality factor | Finding | Why |
|---|---|---|
| Clarity & naming | Strong | The file states it is a launcher and names the three things it delegates to. |
| Single responsibility | Strong | No workflow logic is duplicated. |
| Contract strength | Strong | "Required behavior" is four bullets. |
| Drift surface | Low | Almost nothing here can drift — there is almost nothing here. |
| Mechanical testability | Good | `smoke-test.py` requires the file path and validates frontmatter. |

**Coach this:** the launcher exists *only* to win one moment — discoverability. Wrappers should be smaller than the thing they wrap.

### Chunk 2 — Thin orchestrator agent

| Quality factor | Finding | Why |
|---|---|---|
| Clarity & naming | Strong | Each loaded skill is named with its authority boundary. |
| Single responsibility | Strong | Coordinates; does not absorb. |
| Contract strength | Strong | Intake protocol, guardrails, and skill-authority statements are all explicit. |
| Drift surface | Medium | The agent restates a short workflow summary. Useful for execution; still a place to keep aligned with `WORKFLOW.md`. |
| Mechanical testability | Medium | Frontmatter and existence are tested. Behavioural alignment with the playbook is not automated. |

**Coach this:** "thin" is not "empty". A useful orchestrator carries the *minimum execution mental model* and defers the rest. The drift surface is the price of usability.

### Chunk 3 — Workflow playbook

| Quality factor | Finding | Why |
|---|---|---|
| Clarity & naming | Strong | Section numbering matches execution order. |
| Single responsibility | Strong | The playbook owns the run; it does not own skill internals. |
| Contract strength | Strong | Includes routing tables, output trees per option, validation steps, and explicit script exit-code expectations. |
| Drift surface | Medium | Several surfaces (prompt, agent, README) reproduce parts of the playbook. |
| Mechanical testability | Strong | Output paths, link integrity, forbidden text, and canonical view filenames are smoke-tested directly out of the playbook. |

**Coach this:** the playbook is application control flow. Every overlap with the prompt or agent should ask one question: *if these disagree, who wins?* The answer here is always the playbook.

### Chunk 4 — Core 4+1 method skill

| Quality factor | Finding | Why |
|---|---|---|
| Clarity & naming | Strong | Each view is described by audience, question answered, and primary notation. |
| Single responsibility | Strong | Explicitly disclaims output-track ownership. |
| Contract strength | Strong | Workflow steps 1–7 are linear; concerns are pluggable. |
| Drift surface | Low | Per-view detail is in `references/`, so the SKILL.md stays slim. |
| Mechanical testability | Medium | `validate-views.py` performs heuristic component-name extraction (bold tokens, minus a noise list). Useful as a consistency prompt; not proof of correctness. |

**Coach this:** heuristic validators are still valuable when their limits are stated honestly. The skill labels them as advisory and the playbook says so too. That alignment is the lesson.

### Chunk 5 — Track decision

| Quality factor | Finding | Why |
|---|---|---|
| Clarity & naming | Strong | Three options, single question. |
| Single responsibility | Strong | The decision only selects outputs; tracks own their mechanics. |
| Contract strength | Strong | Workflow guardrail: do not import style or mechanics across tracks. |
| Drift surface | Low | The branch logic appears identically in playbook, agent, and prompt. |
| Mechanical testability | Medium | Required assets for both tracks are checked; user selection itself is not simulated. |

**Coach this:** simple branches at the UI can carry significant architectural weight. Make the branch explicit; let each branch own its world.

### Chunk 6 — draw.io output track

| Quality factor | Finding | Why |
|---|---|---|
| Separation of concerns | Strong | Workflow notation lives in `references/notation-drawio.md`; mxGraph mechanics live in the skill. |
| Contract strength | Strong | Eight per-view skeletons, provenance cell required at workflow level, validation script with `--require-provenance` flag. |
| Drift surface | Medium | Skeleton inventory and the routing table in `WORKFLOW.md` §4a must stay aligned (smoke test enforces required paths). |
| Mechanical testability | Strong | `validate-drawio.py` parses XML, checks root cells, parents, geometry, edge endpoints, provenance. Smoke test runs it across all templates. |
| Semantic correctness | Manual | Structural validity does not prove the diagram says the right thing. |

**Coach this:** XML can prove a diagram is well-formed. It cannot prove the architecture is true. Always pair structural automation with semantic review.

### Chunk 7 — Miro output track

| Quality factor | Finding | Why |
|---|---|---|
| Separation of concerns | Strong | Skill, instruction, templates, and notation reference all distinct. |
| Contract strength | Strong | RISEN sections, exact counts, exact labels, exclusions, source-reference section, physical-view object manifest. |
| Drift surface | Medium | Two copies of the Miro templates (workflow vs. skill); kept honest by byte-equality smoke check. |
| Mechanical testability | Medium | No prompt-validation script analogous to `validate-drawio.py`; checks are filename pattern, template parity, and example naming. |
| Semantic correctness | Manual | Same as draw.io: parity with canonical source is checklist-driven. |

**Coach this:** prompts are artefacts with contracts too. Naming, sections, source references, and explicit scope boundaries are this track's equivalent of XML schema.

### Chunk 8 — Validation and maintenance

| Quality factor | Finding | Why |
|---|---|---|
| Completeness | Strong | Three validators address three distinct concerns: bundle integrity, cross-view consistency, per-format validity. |
| Error messages | Good | Smoke-test errors include path and the failing contract. draw.io validation prints precise structural failures. |
| Recovery model | Strong | `WORKFLOW.md` §7 defines a stop-classify-regenerate-revalidate loop and states each script's exit-code contract. |
| Drift surface | Low | The manifest treats the bundle as a frozen snapshot; `--check-skew` detects local drift against recorded hashes. |
| Honest scope | Strong | The README and manifest describe sync as bundle-local integrity, not upstream fetch. |

**Coach this:** "sync" easily overpromises. Naming the operation accurately ("snapshot integrity, not upstream pull") prevents users from trusting it for the wrong job.

---

## Step 4 — Teach: seven design decisions and their trade-offs

These are the decisions worth slowing down on. For each, ask the learner what they would have done before showing what the bundle did.

### Decision 1 — Canonical diagram-as-code first, visual artefacts second

**The choice:** Mermaid and PlantUML are the source of truth. draw.io and Miro are *generated from* canonical sources, never the reverse.

**Why:** Canonical formats are reviewable text. A pull request shows exactly which component name, relationship, or deployment node changed. Visual editors let humans change spatial layout, style, and meaning at the same time, which makes drift invisible.

**Trade-off:** The first run of each view is slower because two artefacts are produced. Long-term, audit and review costs collapse.

**Pattern to teach:** *Define the model in a durable representation; generate or describe visual surfaces from that model.*

### Decision 2 — Discoverable launcher separate from orchestrator

**The choice:** A root `architecture-documentation.agent.md` exists only to make the bundle discoverable. The real orchestration lives in `agents/architecture-documentation.agent.md`.

**Why:** Agent runtimes look in fixed places (`.github/agents/`, `~/.agents/`). The bundle must be installable by copy. The root file is a shim. The orchestrator is the real program.

**Trade-off:** One more hop for the reader. In return, the bundle can evolve internally without touching the discoverability surface.

**Pattern to teach:** *Discoverability is an interface. Behaviour is an implementation. Keep them separate.*

### Decision 3 — Compose three skills instead of one big skill

**The choice:** `4plus1-models` (method), `draw-io-diagram-generator` (XML output), `miro-diagram-generator` (prompt output) are three separate skills, each authoritative for its own world.

**Why:** They change for different reasons. A new BPMN palette change affects both output skills but not the method. A new view variant affects the method but not the output mechanics. Putting them in one skill would hide those reasons.

**Trade-off:** Three skills means three sets of frontmatter, three reference folders, three places a learner has to look. The orchestrator and playbook do the navigation work.

**Pattern to teach:** *Split skills by reason to change. Cohesion is about why code changes together, not about what it does together.*

### Decision 4 — draw.io and Miro tracks stay independent

**The choice:** Each track has its own skill, instructions, templates, references, validation surface. The orchestrator forbids importing style or mechanics across tracks.

**Why:** draw.io is structured XML. Miro is structured prompts. A shared abstraction would have to leak both worlds and would weaken both.

**What is shared (deliberately):** canonical component and relationship names; canonical-source paths and provenance; the BPMN semantic palette mapping for process views; the rule that physical-view visuals must not invent infrastructure beyond the `.puml`.

**Trade-off:** Some duplicated effort across tracks. In return, each track can improve independently and a new track (Lucidchart, Excalidraw, …) can be added without touching the others.

**Pattern to teach:** *Share the model; do not share the rendering.*

### Decision 5 — Physical view uses PlantUML as canonical

**The choice:** Physical view uses PlantUML (`.puml`); the other four views use Mermaid (`.mmd`).

**Why:** Physical architecture needs deployment boundaries, cloud-provider stdlib shapes, network topology, regions, and provider-specific notation. PlantUML handles this better than Mermaid in this workflow.

**The strict rule downstream:** visual outputs (draw.io, Miro) may *group and style* physical elements, but must not *invent* infrastructure. Every node, container, child element, relationship endpoint, and relationship label in the `.puml` must be represented; nothing else may appear.

**Why the rule matters:** the most common deployment-diagram failure is a CDN, cache, WAF, queue, or replica that "looked right" in the visual template and was never removed. Such elements are claims; if the canonical source does not claim them, the diagram lies.

**Trade-off:** Mixing notations in one workflow adds a learning step. The cost buys deployment-diagram honesty.

**Pattern to teach:** *For infrastructure, treat extra boxes as claims. Visual editors are very good at producing claims you didn't make.*

### Decision 6 — Vendoring is the packaging contract

**The choice:** Skills, instructions, templates, scripts, references, examples are all bundled under the workflow folder. The bundle has no runtime dependency on any path outside itself.

**Why:** The repository's standalone-packaging rule says every workflow, skill, instruction, prompt, and agent must be copyable on its own. A workflow that links outward is not portable.

**The cost:** bundled copies can drift from upstream. The bundle handles this honestly with two ideas:

- The bundled manifest tracks **bundle-local integrity** (hashes match the recorded snapshot). It does *not* fetch from upstream.
- A `--check-skew` mode tells the maintainer whether the local snapshot still matches the manifest.

**Trade-off:** Larger bundle, manual upstream refresh. In return, copy-to-deploy is real.

**Pattern to teach:** *Standalone is a guarantee. Manifests with hashes are how you keep the guarantee true.*

### Decision 7 — The smoke test is executable memory

**The choice:** A single `scripts/smoke-test.py` enforces every contract the bundle relies on for portability and consistency: required paths, frontmatter order, link resolution and bundle containment, forbidden stale text, output-path conventions, canonical view filenames, validator invocation form, Miro template parity, draw.io template validity, and (with `--check-skew`) bundled asset hashes.

**Why:** Documentation-first projects have no compiler. Without mechanical checks, every refactor relies on memory. Memory loses to large bundles.

**Trade-off:** Maintainers must update the smoke test when contracts change. In return, breaking changes are loud.

**Pattern to teach:** *In a documentation-first system, every contract you care about needs a check that fails when it breaks. The smoke test is your build.*

---

## Step 5 — Advise: questions to take to the next agentic workflow

Coaches: when learners move from this workflow to design or review their own, give them this question set. Each question maps to a decision above.

1. **What is the single source of truth?** If a view, prompt, or output disagrees with another, which one wins? Is that documented?
2. **Where is the orchestration thin and where is it thick?** Does the orchestrator absorb domain logic? If yes, which skill is missing?
3. **How is the bundle discovered?** Is the discoverability surface separate from the behaviour surface, or are they tangled?
4. **How many skills, and why those?** Could one skill be split because it changes for two different reasons? Could two be merged because they always change together?
5. **Where are the genuine branches?** Track choice, audience, view, environment. Are branches explicit and named, or implicit and inferred?
6. **What is shared across branches and what is not?** Share the model; do not share the rendering.
7. **What can be invented downstream?** For every artefact the workflow produces, ask: what could a generator add that the canonical source does not claim? Where is that prevented?
8. **Is the bundle copy-to-deploy?** Are skills, instructions, templates, references bundled locally? Are external links forbidden? Is there a manifest with integrity hashes?
9. **What contracts have machine checks?** Required files, frontmatter order, link resolution, naming conventions, output paths, format validity, parity between duplicated files, bundled hashes. If a contract has no check, it will drift.
10. **What is the recovery loop on validation failure?** Stop, classify, regenerate the affected artefact only, re-run the failing validator first, then re-run the full set. Is it documented?

If a learner can apply this question set to an unfamiliar workflow and produce a useful review, the coaching has worked.

---

## Appendix — Map from chunk to file (for facilitators)

| Chunk | Primary file(s) | Secondary surfaces |
|---|---|---|
| 1. Discoverable launcher | `architecture-documentation.agent.md` (root) | — |
| 2. Thin orchestrator agent | `agents/architecture-documentation.agent.md` | `prompts/4plus1-diagrams.prompt.md` |
| 3. Workflow playbook | `WORKFLOW.md` | `README.md` |
| 4. Core 4+1 method skill | `skills/4plus1-models/SKILL.md` | `references/`, `concerns/`, `templates/view-template.md`, `examples/synth-claim/` |
| 5. Track decision | `WORKFLOW.md` §2, agent guardrails, prompt step 2 | — |
| 6. draw.io track | `skills/draw-io-diagram-generator/SKILL.md`, `templates/drawio/`, `references/notation-drawio.md`, `instructions/draw-io.instructions.md` | `skills/draw-io-diagram-generator/scripts/validate-drawio.py` |
| 7. Miro track | `skills/miro-diagram-generator/SKILL.md`, `templates/miro/`, `references/notation-miro.md`, `instructions/miro.instructions.md` | `skills/miro-diagram-generator/examples/synth-claim/miro-prompts/` |
| 8. Validation & maintenance | `scripts/smoke-test.py`, `vendored-assets-manifest.json`, `scripts/sync-vendored-assets.py`, `scripts/inject-and-validate-provenance.py` | `skills/4plus1-models/scripts/validate-views.py`, `skills/draw-io-diagram-generator/scripts/validate-drawio.py` |

Use this table when the workshop asks "where do I look?" — but resist letting learners read top-to-bottom. The coaching value comes from the chunk-to-decision-to-question chain, not the file list.
