# Code-to-Coach: 4plus1-diagrams Workflow Analysis

This document deconstructs the current `workflows/4plus1-diagrams` bundle using the Code-to-Coach method.

The goal is not just to describe what the workflow does. The goal is to teach how to think about this kind of workflow: orchestration, standalone packaging, canonical sources, independent output tracks, and mechanical validation.

---

## Step 1: Orient - Scope and Context

### The Job

The `4plus1-diagrams` workflow produces a complete Kruchten 4+1 architecture documentation set with two layers of output:

1. Canonical diagram-as-code: Mermaid for most views and PlantUML for the Physical view.
2. Editable visual artefacts: draw.io files, Miro prompts, or both.

The workflow exists because architecture teams often need both durable source files and collaborative visuals. Mermaid and PlantUML are easy to version, diff, and review in git. draw.io and Miro are easier to edit with stakeholders. This bundle bridges those worlds while trying to keep all representations aligned.

### Who Calls It

- Architects producing end-to-end system documentation.
- Technical leads preparing architecture views for mixed technical and business audiences.
- Teams that need editable diagrams for workshops, reviews, or slide decks.
- Users who want one orchestrated 4+1 run instead of manually combining separate skills.
- Maintainers who need a standalone, copyable workflow bundle with no runtime dependency on other repo paths.

### The Problem It Solves

Without this workflow, a user would generate the 4+1 architecture views, then separately recreate each view in draw.io or Miro. That creates three risks:

- Names drift between the source diagram and the visual diagram.
- Visual diagrams acquire extra infrastructure or relationships that were never in the canonical source.
- The folder becomes hard to copy because it depends on skills, instructions, templates, or references elsewhere.

With this workflow, the canonical source is generated first, output tracks are selected explicitly, and each visual track is validated against the source.

### Design Signals To Notice

The workflow is designed around a few deliberate signals that make it easier to teach and maintain:

- The root agent is a thin launcher that points to the workflow-local orchestrator.
- `WORKFLOW.md` is the execution source of truth.
- draw.io and Miro are first-class output options, with support for either or both.
- Validation failure handling has a documented recovery loop.
- Vendored asset metadata and hash-based skew checks protect the standalone bundle.
- Output folders use typed subfolders: `diagrams/mermaid/`, `diagrams/drawio/`, and `diagrams/miro/`.
- The smoke test checks bundle integrity, frontmatter order, links, stale references, output path contracts, Miro template parity, draw.io XML, and vendored hashes.

For learners, these signals show the workflow's central teaching pattern: one source of truth, independent output tracks, and mechanical checks that keep the bundle copyable.

---

## Step 2: Deconstruct - Breaking Into Chunks

The current workflow is best understood as eight logical chunks.

### Chunk 1: Discoverable Launcher

**What:** `architecture-documentation.agent.md` at the workflow root.

**Job:** Make the whole folder discoverable when copied under `.github/agents/` or `~/.agents/`.

**Why it exists:** It lets the bundle be installed by copying one folder. The launcher does not own behaviour; it delegates to `agents/architecture-documentation.agent.md` and `WORKFLOW.md`.

**Teaching point:** This is a wrapper pattern. A wrapper is valuable when it gives users a stable entrypoint while keeping real logic somewhere else.

### Chunk 2: Thin Orchestrator Agent

**What:** `agents/architecture-documentation.agent.md`.

**Job:** Load the right skills, ask a compact intake question, route to draw.io, Miro, or both, and enforce guardrails.

**Why it exists:** The agent coordinates work across assets but deliberately avoids owning the 4+1 method, draw.io mechanics, or Miro prompt craft.

**Teaching point:** Good orchestration code should know sequencing and boundaries. It should not absorb the internals of every subsystem it coordinates.

### Chunk 3: Workflow Playbook

**What:** `WORKFLOW.md`.

**Job:** Define the canonical execution sequence, output contracts, validation expectations, troubleshooting loop, and maintenance notes.

**Why it exists:** It is the human-readable source of truth. The prompt, launcher, and agent should all defer to it.

**Teaching point:** In documentation-first systems, the playbook is the equivalent of application control flow. If the playbook drifts, every dependent entrypoint becomes suspect.

### Chunk 4: Core 4+1 Method Skill

**What:** `skills/4plus1-models/SKILL.md`.

**Job:** Own invocation mode, audience routing, context capture, concern routing, per-view generation, and canonical Mermaid/PlantUML outputs.

**Why it exists:** The 4+1 method is reusable without draw.io or Miro. Keeping it separate means the same architecture logic can be used standalone or inside this larger workflow.

**Teaching point:** This is the domain core. Output formats should depend on it; it should not depend on output formats.

### Chunk 5: Visual Track Decision

**What:** The track choice in the prompt, agent, and `WORKFLOW.md`.

**Job:** Decide whether to produce draw.io, Miro, or both.

**Why it exists:** The two tracks use different authoring models and validation rules. The workflow should branch explicitly rather than trying to hide those differences.

**Teaching point:** Branching is not a design smell when the branches represent genuinely different modes of work.

### Chunk 6: draw.io Output Track

**What:** `skills/draw-io-diagram-generator/`, `instructions/draw-io.instructions.md`, `templates/drawio/`, and `references/notation-drawio.md`.

**Job:** Convert each canonical view into valid mxGraph XML, starting from per-view skeletons and enforcing draw.io-specific notation.

**Why it exists:** draw.io generation is structured XML work. It needs exact cell ids, parent references, geometry, shape libraries, and validation.

**Teaching point:** This is a concrete-output track. Most bugs here are structural: malformed XML, invalid references, missing provenance, or a diagram that renders poorly.

### Chunk 7: Miro Output Track

**What:** `skills/miro-diagram-generator/`, `instructions/miro.instructions.md`, `templates/miro/`, and `references/notation-miro.md`.

**Job:** Convert each canonical view into a Miro prompt using RISEN sections, deterministic object lists, frame naming, and per-view layout rules.

**Why it exists:** Miro output is language-driven rather than XML-driven. It needs precise instructions so a collaborative board can be recreated without inventing extra objects.

**Teaching point:** This is a prompt-output track. Most bugs here are ambiguity bugs: missing counts, loose labels, unscoped instructions, or prompts that ask Miro to infer too much.

### Chunk 8: Validation and Maintenance

**What:** `scripts/smoke-test.py`, `scripts/sync-vendored-assets.py`, `vendored-assets-manifest.json`, `skills/4plus1-models/scripts/validate-views.py`, and `skills/draw-io-diagram-generator/scripts/validate-drawio.py`.

**Job:** Check that the bundle is self-contained, links resolve, output contracts are current, draw.io templates parse, Miro templates match, and vendored asset hashes are unchanged.

**Why it exists:** A standalone workflow only stays portable if there is a mechanical way to catch missing files, stale paths, and local drift.

**Teaching point:** Validation is where documentation becomes executable. The stronger the mechanical checks, the less the maintainer has to rely on memory.

---

## Step 3: Analyse - Quality Review By Chunk

### Chunk 1: Discoverable Launcher

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Clarity and naming | Strong | The launcher says it is a discoverable entrypoint and points to the local orchestrator, playbook, and prompt. |
| Single responsibility | Strong | It delegates instead of duplicating workflow logic. |
| Error handling | Adequate | It tells the agent to enforce a clean start, but it does not define recovery behaviour itself. That belongs in `WORKFLOW.md`. |
| Testability | Good | The smoke test checks required paths and agent frontmatter. |
| Cognitive load | Low | Users only need to know this is the entrypoint. |
| Smell | Minor | `tools: []` is correct for no MCP dependency, but users may misread it as the agent being unable to work. The README helps offset this. |

**Coaching insight:** The launcher is doing the right amount of work: enough to be discoverable, not enough to become a second workflow definition.

### Chunk 2: Thin Orchestrator Agent

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Clarity and naming | Strong | It names the three loaded skills and the authority boundary for each. |
| Single responsibility | Strong | It coordinates sequence and guardrails; it does not own rendering internals. |
| Error handling | Strong | It requires compact intake, assumptions for partial answers, and one follow-up at a time. |
| Testability | Medium | Humans can inspect routing rules, but there is no automated test that the agent and prompt remain semantically aligned with `WORKFLOW.md`. |
| Cognitive load | Low to medium | The guardrails are many, but they are grouped by concern and mostly non-overlapping. |
| Smell | Residual duplication | The agent includes a short workflow summary. That is useful for execution, but it still creates some drift risk with `WORKFLOW.md`. |

**Coaching insight:** Thin does not mean empty. A good orchestrator keeps the minimum useful mental model close at hand, then defers detail to the owner files.

### Chunk 3: Workflow Playbook

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Clarity and naming | Strong | Purpose, linked assets, preconditions, steps, output directories, validation, and troubleshooting are explicit. |
| Single responsibility | Strong | It defines the full run without embedding all skill internals. |
| Error handling | Strong | Section 7 defines a recovery loop for validation failures. |
| Testability | Strong | Many workflow claims are covered by `scripts/smoke-test.py`. |
| Cognitive load | Medium | The file is long, but the sections match the order of execution. |
| Smell | Contract mismatch | Section 7 says `validate-views.py` exits non-zero on mismatch, but the script returns `0` for warnings and only returns `1` for fatal setup errors. |

**Coaching insight:** A playbook is only as strong as its contract with scripts. If prose says one thing and code returns another, the user will trust whichever they encounter first.

### Chunk 4: Core 4+1 Method Skill

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Clarity and naming | Strong | The five views are named by audience, question answered, and notation. |
| Single responsibility | Strong | It explicitly says it does not own draw.io or Miro rendering. |
| Assumptions | Strong | It requires visible assumptions and targeted follow-ups. |
| Testability | Medium | The validator checks naming and concern visibility, but does not parse diagrams deeply. |
| Cognitive load | Manageable | The skill routes to references rather than embedding all per-view detail. |
| Smell | Heuristic validation | `validate-views.py` extracts bold text as component names. This is useful but approximate, so it can miss real drift or flag prose terms as components. |

**Coaching insight:** Heuristic validators are still valuable when they are labelled honestly. They should be treated as consistency prompts, not proof of correctness.

### Chunk 5: Visual Track Decision

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Clarity and naming | Strong | The choice is draw.io, Miro, or both. |
| Single responsibility | Strong | The decision only chooses selected outputs; each track owns its own mechanics. |
| Governance | Strong | The workflow says not to import style or mechanics from one track into the other. |
| Testability | Medium | The smoke test checks assets for both tracks, but does not simulate user track selection. |
| Cognitive load | Low | Users get a compact choice with concrete descriptions. |
| Smell | Drift surface | The prompt repeats some workflow details. The value proposition is balanced, but repeated execution rules still need maintenance care. |

**Coaching insight:** The track decision is a good example of user choice with architectural consequences. It is simple at the UI level but important at the implementation level.

### Chunk 6: draw.io Output Track

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Separation of concerns | Strong | Workflow-level notation is separate from generic mxGraph mechanics. |
| Testability | Strong | `validate-drawio.py` parses XML, checks root cells, title cells, parents, geometry, edge endpoints, and optional provenance. |
| Governance | Strong | Physical view provenance and `.puml` parity are documented. BPMN colour mapping is explicit. |
| Cognitive load | Medium to high | mxGraph XML is inherently detailed, but the skill and instruction file chunk it well. |
| Smell | Manual semantic parity | XML validity is automated, but exact component and relationship parity still requires careful human or agent comparison. |

**Coaching insight:** draw.io validation is strongest at structure and weaker at meaning. That is normal: XML can prove that a diagram is well-formed, but not that the architecture is true.

### Chunk 7: Miro Output Track

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Separation of concerns | Strong | Miro has its own skill, instruction file, templates, and notation reference. |
| Testability | Medium | The smoke test checks template parity and example names, but there is no Miro-specific validator script equivalent to `validate-drawio.py`. |
| Governance | Strong | RISEN sections, exact counts, labels, exclusions, and physical-view object manifests reduce ambiguity. |
| Cognitive load | Medium | Sidekick-specific physical-view guidance is detailed because it prevents common prompt failures. |
| Smell | Output location inconsistency | `instructions/miro.instructions.md` says prompts live in the same directory as the corresponding `.mmd` or `.puml`, while the workflow output contract says they live under `diagrams/miro/`. |

**Coaching insight:** Prompt artefacts need contracts too. The Miro track is not code, but naming, sections, source references, and scope boundaries are still executable design constraints.

### Chunk 8: Validation and Maintenance

| Quality Factor | Finding | Reasoning |
|---|---|---|
| Completeness | Strong | Smoke testing covers path presence, links, stale references, path contracts, templates, XML, and vendored metadata. |
| Error messages | Good | Smoke-test output names the failing contract and path. draw.io validation prints precise structural failures. |
| Rollback/recovery | Strong | The workflow tells the agent to stop, classify failure, regenerate affected artefacts, and re-run validators. |
| Testability | Strong | The smoke test is fast and mechanical. |
| Cognitive load | Medium | There are several validators with different scopes; the README helps explain when to run each. |
| Smell | Ambiguous sync model | The manifest uses `source.kind: bundle-path`, often with `source.path` equal to `local_path`. This detects local snapshot drift but does not fetch or compare against an external upstream source. |

**Coaching insight:** The maintenance model is intentionally standalone. That is good, but the word "sync" can overpromise. It is more like bundle-local integrity management unless a maintainer deliberately replaces assets and updates hashes.

---

## Step 4: Teach - Explain The Why

### Decision 1: Why Canonical Diagram-As-Code Comes First

The workflow treats Mermaid and PlantUML as the source of truth because they are reviewable text. A pull request can show exactly what changed in a relationship, component name, or deployment node.

draw.io and Miro are easier for humans to manipulate visually, but they are not the best place to establish architectural truth. If the editable visual becomes the source of truth, drift becomes harder to detect because diagrams can change spatially, stylistically, or semantically all at once.

The thinking pattern is: first define the model in a durable representation, then generate or describe visual surfaces from that model.

### Decision 2: Why The Root Agent Is Thin

The root agent is a discoverability adapter. Its job is to let the folder be copied into a standard agent location and still work. It should not repeat the workflow because repeated instructions become alternate sources of truth.

This is similar to a command-line shim: the shim helps users find the tool, but the actual behaviour lives in the real program.

The trade-off is that users may need one more hop to understand the system. The benefit is much larger: the bundle can evolve without updating the launcher every time.

### Decision 3: Why The Orchestrator Composes Skills Instead Of Merging Them

The three major responsibilities are different kinds of work:

- `4plus1-models` is architecture method work.
- `draw-io-diagram-generator` is XML and visual layout work.
- `miro-diagram-generator` is prompt and board-instruction work.

Combining them into one giant skill would hide the boundaries. Every change to Miro prompt style would risk touching 4+1 logic. Every draw.io XML rule would sit beside audience-routing guidance. That would make the system harder to teach, harder to test, and harder to extend.

The thinking pattern is: split by reason to change. If two parts change for different reasons, they probably deserve different ownership.

### Decision 4: Why draw.io And Miro Tracks Stay Independent

draw.io and Miro do not have the same mechanics. draw.io needs exact XML. Miro needs precise natural-language instructions. Trying to force one shared visual grammar across both would create hidden coupling.

The workflow instead shares only what needs to be shared:

- canonical component and relationship names
- source paths and provenance
- semantic palette expectations for BPMN-style process views
- physical-view parity with PlantUML

Everything else remains track-local. This is a good boundary because it lets each track improve without forcing the other to mimic it.

### Decision 5: Why Physical View Uses PlantUML As Canonical

Physical architecture needs deployment boundaries, cloud services, regions, network relationships, and sometimes provider-specific notation. PlantUML is a better source format for that than Mermaid in this workflow.

The workflow then imposes a strict rule: visual outputs can group and style physical elements, but they must not invent infrastructure. This prevents a common failure mode where a nice-looking deployment diagram gains an unstated CDN, cache, WAF, database, or protocol because the visual template happened to include one.

The thinking pattern is: for infrastructure, treat extra boxes as claims. If the canonical source does not claim a resource exists, the visual output should not show it.

### Decision 6: Why Vendoring Is A Feature, Not A Smell

This repo has a strict standalone packaging rule. A copied workflow must include everything it needs. That is why skills, instructions, templates, scripts, references, and examples are vendored under the workflow folder.

Vendoring has a cost: copied assets can become stale relative to their original sources. The current bundle handles this by treating the vendored assets as a frozen snapshot and checking local hash integrity.

The subtle point: this does not automatically tell you whether an external original has changed. It tells you whether this bundle's declared snapshot still matches the manifest. That is a valid design, but maintainers should describe it as snapshot integrity unless they add a real upstream comparison process.

### Decision 7: Why The Smoke Test Matters

The smoke test is the workflow's executable memory. It catches things humans forget:

- broken local links
- stale references to non-local or incorrect paths
- flat `diagrams/` outputs that bypass the typed folder contract
- Miro template drift between workflow and skill copies
- malformed draw.io templates
- vendored asset hash drift

This is especially important for documentation-first assets. There is no application build to fail. The smoke test becomes the build.

---

## Step 5: Advise - Prioritised Next Steps

### Priority 1: Fix The `validate-views.py` Exit-Code Contract

**Impact:** High  
**Effort:** Low to medium

**Issue:** `WORKFLOW.md` says `validate-views.py` exits non-zero on mismatch. The script documentation and implementation say it returns `0` after reporting warnings, and only returns `1` for fatal setup problems like a missing directory or no expected files.

**Why it matters:** Agents and maintainers use exit codes to decide whether to stop. If warnings return `0`, the workflow should not claim they fail the run.

**Recommendation:** Choose one contract and align both sides:

- Option A: Keep `validate-views.py` advisory and update `WORKFLOW.md` to say mismatches are warnings that require human review.
- Option B: Add a `--strict` mode that returns non-zero when consistency warnings are present, then update `WORKFLOW.md` to invoke strict mode when final validation is required.

### Priority 2: Fix The Miro Prompt Location Inconsistency

**Impact:** Medium  
**Effort:** Low

**Issue:** The workflow output contract writes Miro prompts under `diagrams/miro/`, but `instructions/miro.instructions.md` says the prompt location is the same directory as the corresponding `.mmd` or `.puml` file.

**Why it matters:** This is exactly the kind of small contract drift that causes generated artefacts to land in the wrong folder.

**Recommendation:** Update the Miro instruction file to use `diagrams/miro/<view>-miro-prompt.md`, matching `WORKFLOW.md`, `README.md`, and the Miro skill.

### Priority 3: Clarify The Vendored Asset Maintenance Model

**Impact:** Medium  
**Effort:** Low to medium

**Issue:** The manifest and sync script are bundle-local. They enforce local snapshot integrity, but they do not check an external upstream source.

**Why it matters:** "Sync" may imply that the script refreshes from an original skill source. In the current strict-standalone model, it does not.

**Recommendation:** Add a short note to the README maintenance SOP:

> This workflow does not automatically fetch upstream skill changes. To refresh a vendored asset, deliberately replace the local bundle copy, then run the sync/apply or hash update process and smoke test the result.

If the desired behaviour is true upstream comparison, add a separate, optional maintainer-only manifest outside the runtime bundle. Keep it out of the copied workflow if strict standalone packaging is required.

### Priority 4: Reduce Residual Prompt And Workflow Duplication

**Impact:** Medium  
**Effort:** Medium

**Issue:** The root launcher is thin, but the prompt still restates a condensed workflow sequence. Some repetition is useful for agent execution, but it remains a drift surface.

**Why it matters:** The smoke test can catch invalid paths and missing files, but it cannot prove that the prompt's behavioural summary matches `WORKFLOW.md`.

**Recommendation:** Keep the prompt executable but make each repeated item explicitly a summary of `WORKFLOW.md`, not a separate rule. Add one smoke-test check for a small number of high-risk statements, such as output track choices and typed output folders.

### Priority 5: Add A Worked End-To-End Example README

**Impact:** Medium  
**Effort:** Medium

**Issue:** The bundle includes core 4+1 example views and Miro examples, but the top-level workflow does not yet have a narrative example that shows intake, generated canonical views, selected visual tracks, validation, and final folder structure in one place.

**Why it matters:** First-time users understand workflow systems faster when they can see one complete run.

**Recommendation:** Add `examples/synth-claim/README.md` or a workflow-level example guide showing:

1. The initial user request.
2. The compact intake assumptions.
3. The five canonical views.
4. The selected draw.io and/or Miro outputs.
5. The validation commands and expected result.

### Priority 6: Consider A Miro Prompt Validator

**Impact:** Low to medium  
**Effort:** Medium

**Issue:** Miro validation is currently checklist-based. The smoke test checks template parity and file names, but does not parse generated Miro prompt content.

**Why it matters:** The Miro track has a strong contract: RISEN sections, canonical source reference, exact labels, counts, and narrowing. Some of that can be checked mechanically.

**Recommendation:** Add a lightweight `validate-miro-prompt.py` that checks required RISEN headings, `Canonical source reference`, view filename pattern, and absence of known cross-view leakage terms.

---

## Teaching Summary: How To Think About This Workflow

The deep pattern is orchestration over independent capabilities.

The workflow has a domain core (`4plus1-models`), two independent rendering tracks (draw.io and Miro), and a validation layer that protects the bundle contract. The orchestration works because coupling is mostly one-directional:

```text
4+1 method -> canonical Mermaid/PlantUML -> selected visual track(s) -> validation
```

draw.io does not depend on Miro. Miro does not depend on draw.io. Both depend on the same canonical source.

That is the part worth carrying to other systems. If you add a third output format later, the scalable move is not to edit every existing track. The scalable move is:

1. Create a new output skill.
2. Add a track choice branch.
3. Define its templates and notation reference.
4. Validate it against the canonical source.
5. Extend the smoke test for its folder and naming contract.

The current workflow is well-designed because it makes its contracts explicit: source of truth, output ownership, validation scope, and packaging rules. Its remaining issues are not architectural collapse; they are contract alignment problems. That is a good place for a documentation-first workflow to be.

---

## Success Criteria Check

- Learner understands the purpose: connect version-controlled 4+1 diagrams with editable draw.io and Miro outputs.
- Learner can name the numbered chunks: launcher, orchestrator, playbook, core skill, track decision, draw.io track, Miro track, validation and maintenance.
- Learner can explain the main design decisions: canonical source first, thin launcher, skill composition, independent tracks, PlantUML for Physical view, vendored snapshot packaging.
- Learner can identify remaining hard parts: script/prose contract drift, Miro output location mismatch, self-referential vendored sync, heuristic validation limits.
- Learner has actionable improvements ranked by impact and effort.

## Result

The `4plus1-diagrams` workflow is a strong example of documentation-first workflow design: a standalone bundle, a clear source of truth, independent output tracks, canonical-source parity, and mechanical validation. Its main teaching value is the way it turns architectural documentation into an explicit, testable set of contracts.
