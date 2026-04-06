# Development Skills

This category contains skills for software engineering workflows. Language-agnostic skills live at this level; language-specific skills are organised in sub-folders.

## Language-agnostic skills

| Skill | Description |
| --- | --- |
| [code-review](code-review/SKILL.md) | Structured code review across correctness, security, maintainability, performance, and test coverage — with prioritised findings and inline suggestions. |
| [git-workflow](git-workflow/SKILL.md) | Branch naming, Conventional Commits authoring, PR descriptions, and merge strategy advice. |
| [api-design](api-design/SKILL.md) | Design or review REST and GraphQL APIs: resource modelling, HTTP semantics, error contracts, versioning, and OpenAPI/schema output. |
| [test-strategy](test-strategy/SKILL.md) | Define a test strategy across the pyramid (unit, integration, contract, E2E, performance, security) with tooling recommendations and CI integration plan. |

## Language-specific skills

| Sub-folder | Languages / platforms |
| --- | --- |
| [bash/](bash/) | Bash / shell scripting |
| [dotnet/](dotnet/) | C#, F#, VB.NET (.NET / ASP.NET) |
| [frontend/](frontend/) | HTML, CSS, JavaScript |
| [java/](java/) | Java |
| [lua/](lua/) | Lua |
| [p5js/](p5js/) | p5.js |
| [processing/](processing/) | Processing |
| [python/](python/) | Python |
| [r/](r/) | R |
| [rust/](rust/) | Rust |
| [sql/](sql/) | SQL (all dialects) |
| [typescript/](typescript/) | TypeScript |

## Add a skill here

**Language-agnostic skill:**

1. Copy the template from `../../templates/skills/skill_blank/`.
2. Place the folder directly under `skills/development/`.
3. Name by workflow or outcome (e.g. `api-design`, `test-strategy`).

**Language-specific skill:**

1. Copy the template from `../../templates/skills/skill_blank/`.
2. Place the folder under the relevant language sub-folder (e.g. `skills/development/python/<skill-name>/`).
3. Name by library, pattern, or workflow (e.g. `async-patterns`, `dependency-injection`).
4. Update the sub-folder README.
