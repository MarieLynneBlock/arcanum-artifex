# Concerns catalogue

Concerns are modular markdown files that tell Claude what to check and flag during each view's generation. They're designed to be swapped, extended, and forked per-company without touching the view references.

## Default catalogue (shipped with the skill)

| Concern file | When it applies | Primary views affected |
|--------------|-----------------|------------------------|
| `gdpr-data-protection.md` | System processes personal data of EU/UK residents | Logical, Process, Physical |
| `security.md` | Always — every system has security concerns | All five views |
| `bias-fairness.md` | System uses ML models in decisioning | Logical, Process, Scenarios |
| `regulatory-compliance.md` | System operates in a regulated sector | All views, especially Scenarios |
| `sustainability-climate.md` | Apply for all production systems; mandatory for large-scale | Physical, Development |
| `accessibility.md` | System has human-facing interfaces | Logical (user-facing components), Scenarios |

## How Claude uses these

During Step 4 of the main workflow:
1. Identify which concerns apply to the system being documented.
2. For each applicable concern, read the relevant file.
3. As each view is generated, pull the per-view **prompts** section of each applicable concern and use them to probe for real issues.
4. Surface real issues (not boilerplate) as `> **Concern (X):** …` blockquotes in the view document.

## Adding a new concern module

To extend the catalogue — for a company-specific or sector-specific concern — create a new file in this folder following the template below, and add a row to the table above.

### Template

```markdown
# [Concern name]

**When this concern applies:** [one line — what makes a system subject to this concern]

**Why it matters:** [2–3 sentences — the stakes, the failure mode, who's harmed]

**Regulatory / standard reference:** [e.g. GDPR Art. 25, ISO 27001 A.8.3, AI Act Art. 10]

## Per-view prompts

### Logical view
- [What to check]
- [What to flag]

### Process view
- [What to check]
...

### Development view
...

### Physical view
...

### Scenarios view
- [Does at least one scenario cover this concern's main failure mode?]

## Common mitigations
- [Standard architectural pattern]
- [Typical technical control]
- [Typical organisational control]

## References
- [Regulatory text or standard]
- [Recognised guidance, e.g. NIST, ENISA, ICO, CNIL]
```

## Design principles for concerns

- **Be specific, not boilerplate.** A concern file should generate concrete questions for the view, not generic statements. "Does the diagram show where PII is stored?" is useful; "Consider privacy" is not.
- **Separate the what-to-check from the how-to-fix.** The per-view prompts tell Claude what to probe; the common mitigations are for the prose output when a concern is flagged.
- **Cite the source.** Every concern file should cite the regulation, standard, or guidance it derives from. This lets architects verify and update when the source changes.
- **Keep it short.** 200–400 lines per concern is ideal. Longer means it's probably two concerns that should be split.

## Deprecating a concern

If a concern no longer applies (regulation repealed, company pivots out of a sector), move the file to a `concerns/archived/` folder rather than deleting. Architectural decisions made under the old regime may still need to be audited against it.
