# architecture-models-4plus1

A portable Claude skill for producing Philippe Kruchten's **4+1 Architectural View Model** for any software system — with rendered diagrams (Mermaid primary, PlantUML fallback for deployment) and **Miro RISEN prompts** for each view.

One skill, three hosts:
- **Claude Code / Claude.ai** — invoke natively; Claude reads `SKILL.md` automatically.
- **Cursor** — install `shims/cursor/architecture-models-4plus1.mdc` into your `.cursor/rules/` folder.
- **GitHub Copilot** — install `shims/copilot/architecture-models-4plus1.prompt.md` into your `.github/prompts/` folder.

The logic lives in one place: `SKILL.md`. The shims point at it.

## What you get per run

For a system you describe (from one paragraph to a full interview):

- **Five view documents** in Markdown with inline Mermaid diagrams:
  - Logical view
  - Process view
  - Development view
  - Physical view (PlantUML alongside Mermaid for deployment depth)
  - Scenarios (+1) view with coverage matrix
- **Five (+1) Miro prompts** — one per view plus a full-board orchestrator, each following the **RISEN framework** (Role / Input / Steps / Expectation / Narrowing) with exact counts, colours, and connection semantics.
- **Concerns surfaced** — GDPR, security, bias/fairness (for ML), regulatory, sustainability, and accessibility — as specific flagged issues, not boilerplate.
- **Assumptions and open questions** — visible `> **Assumption:** …` and `> **Q:** …` blockquotes rather than silent inferences.

## Three invocation modes

- **Zero-input** — you give a paragraph, the skill drafts a full 4+1 with every inference flagged.
- **Interview** — the skill asks for context (stakeholders, stack, scale, quality attributes, constraints) before generating.
- **Partial** — just one or two views, or a single regeneration with a different audience.

In every mode, the skill asks the **audience question** unless you've pre-stated it:

> (a) Dev-only — UML-flavoured notation throughout
> (b) Cross-functional — BPMN-style swimlanes for the process view, UML-flavoured elsewhere
> (c) Executive — simplified C4 at context level only

## Folder map

```
architecture-models-4plus1/
├── SKILL.md                           ← entry point; the canonical workflow
├── README.md                          ← this file
├── references/                        ← per-view and per-notation detail
│   ├── logical-view.md
│   ├── process-view.md
│   ├── development-view.md
│   ├── physical-view.md
│   ├── scenarios-view.md
│   ├── notation-mermaid.md            ← Mermaid cheatsheet
│   ├── notation-plantuml.md           ← PlantUML cheatsheet
│   └── notation-bpmn-in-mermaid.md    ← BPMN-style swimlanes
├── concerns/                          ← modular concerns, swappable per-company
│   ├── README.md                      ← catalogue and add-a-concern template
│   ├── gdpr-data-protection.md
│   ├── security.md
│   ├── bias-fairness.md
│   ├── regulatory-compliance.md
│   ├── sustainability-climate.md
│   └── accessibility.md
├── templates/
│   ├── view-template.md               ← view-document blank
│   └── miro-prompt-template.md        ← RISEN prompt blank
├── examples/
│   └── synth-claim/                   ← synthetic hybrid-cloud claims platform
│       ├── 00-system-context.md
│       ├── 01-logical-view.md
│       ├── 02-process-view.md
│       ├── 03-development-view.md
│       ├── 04-physical-view.md
│       ├── 05-scenarios-view.md
│       └── miro-prompts/              ← one per view + full-board orchestrator
├── scripts/
│   └── validate-views.py              ← mechanical cross-view consistency check
└── shims/
    ├── cursor/architecture-models-4plus1.mdc
    └── copilot/architecture-models-4plus1.prompt.md
```

## Install

### Claude Code
Place the whole folder where your Claude Code setup looks for skills (commonly `~/.claude/skills/` or a project-local `.claude/skills/`). Claude picks it up automatically. No further config.

### Cursor
Copy `shims/cursor/architecture-models-4plus1.mdc` into your repo's `.cursor/rules/` folder. Ensure the canonical `SKILL.md` is accessible from the same repo (or adjust the path in the `.mdc` to wherever you installed the skill).

### GitHub Copilot
Copy `shims/copilot/architecture-models-4plus1.prompt.md` into your repo's `.github/prompts/` folder. Ensure the canonical `SKILL.md` and `references/` / `concerns/` / `templates/` / `examples/` folders are accessible from the workspace (Copilot can inline-reference them with `#file:`).

## Extending the skill

### Add a company-specific concern
Drop a new markdown file into `concerns/` following the template in `concerns/README.md`. Add a row to the catalogue table. The skill picks it up on next use.

### Add a sector-specific variant of an existing concern
Fork the relevant concern file (e.g. `concerns/gdpr-data-protection.md` → `concerns/gdpr-healthcare.md`) and specialise the per-view prompts. Both can coexist; the skill uses whichever applies to the system.

### Tune notation defaults
The audience-to-notation mapping lives in each view's reference file under "Audience routing". Change those sections if your organisation has a different convention (e.g. PlantUML throughout, or proper BPMN tooling required).

### Retire outdated concerns
Move the file to `concerns/archived/` rather than deleting — decisions made under the old regime may still need auditing against it.

## Worked example

The `examples/synth-claim/` folder contains a complete worked example: a synthetic fictional insurer's hybrid cloud claims-processing platform. Hybrid on-prem + AWS, multi-channel document intake, OCR + ML classification, human adjudicators, GDPR + FCA + EU AI Act exposure. Five view documents, six Miro prompts, concerns flagged, assumptions surfaced, coverage matrix complete.

Study it to calibrate specificity and tone — then replace with your system.

## Validator

After generating a set of views, run:

```bash
python scripts/validate-views.py path/to/views/
```

It checks:
- Components named in the logical view appear in at least one other view
- Naming consistency across views (flags close-but-not-identical variants for review)
- Scenarios view contains a coverage matrix and no orphan rows
- Each view has at least one concern flagged (visibility check, not an assertion)
- Assumption and open-question counts (visibility)

The validator flags potential issues; it never fails the build. Human review required.

## Portability notes

This skill deliberately does **not** use:
- Sub-agents (Claude Code-only, breaks Cursor and Copilot portability)
- Hooks (same reason)
- Platform-specific tool-use beyond what all three hosts support

If you want to extend the skill with Claude-Code-only capabilities, do it in a separate fork — keep the canonical skill portable.

## Design philosophy

- **Rationale is mandatory.** Every architectural decision states what quality attribute drove it and what was considered and rejected.
- **Concerns are specific.** No boilerplate GDPR or security language; only real, concrete findings.
- **Assumptions are visible.** If the skill inferred something, it says so, so you can verify and override.
- **Audience determines notation, not the other way round.** The view is for the reader; notation follows.
- **Miro prompts are engineering artefacts, not suggestions.** RISEN with exact counts produces reproducible boards.
- **Portability over cleverness.** One SKILL.md, three hosts. No platform lock-in.

## Licence / provenance

Built on Philippe Kruchten's 4+1 View Model ("Architectural Blueprints — The '4+1' View Model of Software Architecture", IEEE Software, 1995). Adapted for contemporary cloud-native, ML-inclusive, regulated-industry architectures and for LLM-authored documentation workflows.

## Change log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-18 | Initial release. Replaces the earlier `4plus1-architecture` and `4plus1-architecture-bpmn` skills, consolidating them into one skill that asks the audience at invocation. Mermaid primary, PlantUML for deployment. Modular concerns. Cursor and Copilot shims included. Worked synthetic example (SynthClaim) with full board and all Miro prompts. |
