# Quick Reference: Code-to-Coach Skill

## The Five-Step Workflow

```
1. ORIENT      → Understand purpose & context
                  Use: context-discovery.md

2. DECONSTRUCT → Break into logical chunks
                  Use: deconstruction-model.md

3. ANALYSE     → Evaluate against criteria
                  Use: analysis-rubric.md

4. TEACH       → Explain the why
                  Use: teaching-script.md, best-practices.md

5. ADVISE      → Prioritise improvements
                  Use: refactoring-priorities.md
```

---

## The Six Evaluation Dimensions

| Dimension | Key Question | Red Flags |
|-----------|--------------|-----------|
| **Clarity** | Can I understand intent without reading code? | Vague names, magic numbers, no context |
| **Responsibility** | Does this chunk have one clear job? | "and" in the name, mixed concerns |
| **Error Handling** | What can go wrong? Is it handled? | Unchecked inputs, swallowed exceptions |
| **Testability** | Can I test this independently? | Hidden dependencies, hard-to-mock I/O |
| **Cognitive Load** | How much mental effort to understand? | Deep nesting (>3), too many variables |
| **Performance** | Is it efficient at scale? | O(n²) where O(n) exists, wasted memory |

---

## The Ten Code Smells (+ Fix Strategy)

| # | Smell | Refactoring |
|---|-------|-------------|
| 1 | **Long functions** (>30 lines) | Extract into smaller functions |
| 2 | **Deep nesting** (>4 levels) | Use guard clauses, early returns |
| 3 | **Magic numbers** | Define named constants |
| 4 | **Duplicate code** | Extract shared function |
| 5 | **Unclear names** | Rename to specific terms |
| 6 | **Hidden dependencies** | Pass as parameters (dependency injection) |
| 7 | **Inconsistent error handling** | Standardise: explicit errors, clear recovery |
| 8 | **Tight coupling** | Use abstractions, inject dependencies |
| 9 | **Obvious comments** | Improve naming; keep strategic comments |
| 10 | **God objects** | Split into smaller, focused classes |

---

## The Twelve Best Practices

1. **SRP** — One reason to change
2. **DRY** — One place to change
3. **Fail Fast** — Check preconditions early
4. **Dependency Injection** — Pass dependencies in
5. **Separation of Concerns** — Each layer independent
6. **Good Naming** — Names reveal intent
7. **Document Why** — Comments explain decisions
8. **Immutability** — Prefer new objects over mutation
9. **Composition** — Combine simple objects
10. **Invalid States** — Structure prevents bad state
11. **Measure First** — Optimise real bottlenecks
12. **Explicit** — No hidden magic

---

## Nine Cognitive Load Strategies

| Strategy | How | Example |
|----------|-----|---------|
| **Limit nesting** | Keep depth <4 | Use filter().map() instead of nested loops |
| **Minimize mutations** | One change per variable | Use immutable transformations |
| **Reduce scope** | Declare near use | Move variable declaration down |
| **Chunked flow** | Clear phases with comments | // Phase 1: Validate, // Phase 2: Process |
| **Naming patterns** | `is_*`, `get_*`, `validate_*` | Learners predict function behaviour |
| **Separate concerns** | Business logic ≠ I/O | Testable business logic apart from plumbing |
| **Document assumptions** | Docstring: preconditions, postconditions | Explicit about what's required |
| **Abstractions** | Hide unnecessary detail | Use constants, domain terminology |
| **Limit parameters** | Max 3; group rest into objects | Pass `Config` object instead of 10 params |

---

## Refactoring Priority Matrix

```
URGENT (do first)      IMPORTANT (schedule)
├─ Bugs                ├─ Long functions (100+ lines)
├─ Misleading names    ├─ God objects
├─ Obvious smells      ├─ Hidden dependencies
└─ High-impact, low    └─ High-impact, high effort
  effort fixes

NICE-TO-HAVE (if time) DEFER (don't do)
├─ Suboptimal naming   ├─ Premature optimisation
├─ Formatting          ├─ Gold-plating
└─ Low-impact fixes    └─ Low-impact, high effort
```

---

## Template Quick Lookup

### Coaching Review Template (for giving feedback)
1. **Orientation** — What is this code? Why review it?
2. **Strengths** — What's working well?
3. **Observations** — Walk through deconstructed view
4. **Concerns** — Sorted: URGENT → IMPORTANT → NICE-TO-HAVE
5. **Next Steps** — Actionable, prioritised tasks

### Teaching Script Template (for explaining code)
1. **Opening** — Learning goal, why it matters, prerequisites
2. **Big Picture** — 30-second summary + analogy
3. **Chunks** — Walk through each logical piece
4. **Tracing** — Show concrete examples in action
5. **Questions** — Anticipate what they'll ask
6. **Pattern** — Connect to broader idea
7. **Reflection** — Test their understanding
8. **Closing** — Next steps, resources, encouragement

---

## Context Discovery Checklist

**Purpose**:
- [ ] What is this code's job?
- [ ] Who calls it?
- [ ] What's the business domain?
- [ ] Why does it exist?

**Scope**:
- [ ] What are inputs/outputs?
- [ ] What's out of scope?
- [ ] What assumptions exist?

**Constraints**:
- [ ] Performance requirements?
- [ ] Failure modes?
- [ ] Maintenance status?
- [ ] Organizational context?

**History**:
- [ ] When was it written?
- [ ] Recent changes?
- [ ] Team experience level?
- [ ] Known issues/TODOs?

---

## Deconstruction Checklist

For each chunk:
- [ ] Single responsibility — one clear job?
- [ ] Clear boundaries — start and end points?
- [ ] Verb phrase name — "Validate email", not "Email"
- [ ] Plain English — remove jargon
- [ ] Visibility — can I see the whole chunk?
- [ ] Dependencies — what does it rely on?
- [ ] Related logic — what comes before/after?

---

## File Structure

```
code-to-coach/
├── README.md                    ← Overview and usage guide
├── SKILL.md                     ← Full skill documentation
├── quick-reference.md           ← This file
├── frameworks/
│   ├── deconstruction-model.md
│   └── analysis-rubric.md
├── references/
│   ├── code-smells.md
│   ├── best-practices.md
│   ├── cognitive-load.md
│   ├── context-discovery.md
│   └── refactoring-priorities.md
└── templates/
    ├── coaching-review-template.md
    └── teaching-script.md
```

---

## One-Minute Decision Tree

**What's my immediate task?**

- **Review code** → coaching-review-template.md
- **Explain code** → teaching-script.md  
- **Understand unfamiliar code** → context-discovery.md
- **Find problems in code** → code-smells.md
- **Know what to fix first** → refactoring-priorities.md
- **Reduce complexity** → cognitive-load.md
- **Break code into pieces** → deconstruction-model.md
- **Evaluate code quality** → analysis-rubric.md

---

## Common Questions

**Q: How do I give constructive feedback without being critical?**
→ Use coaching-review-template.md structure: strengths first, concerns framed as teaching moments, prioritised next steps.

**Q: What if the code works but feels messy?**
→ Use deconstruction-model.md to break it down, then analysis-rubric.md to identify which dimension is weak (clarity? testability? cognitive load?).

**Q: How much should I comment code?**
→ Comments explain *why* (design decisions), not *what* (code already shows). See best-practices.md: "Document Why, Not What".

**Q: When should I refactor vs. leave it alone?**
→ Use refactoring-priorities.md. URGENT (high impact, low effort) should be done. Others are context-dependent.

**Q: How do I help someone learn to think about code?**
→ Use teaching-script.md + deconstruction-model.md. Teach the pattern (why code is structured this way), not just the code itself.

---

## Key Metrics

**Cognitive Load Markers**:
- Nesting depth: Aim for <4 levels
- Variable scope: Declare near use
- Local variables at once: <7 in memory
- Function parameters: Max 3
- Line length: <100 characters

**Code Quality Indicators**:
- ✓ Each function has one clear job (SRP)
- ✓ Logic is easy to trace (low cognitive load)
- ✓ Errors are explicit and handled (fail fast)
- ✓ Testable in isolation (loose coupling)
- ✓ Names reveal intent
- ✓ No duplication

---

## Principle Hierarchy

```
FOUNDATIONAL (Master These)
├─ Single Responsibility (one job = one reason to change)
├─ Clear Naming (names reveal intent)
└─ Error Handling (check preconditions, fail fast)

INTERMEDIATE (Build On These)
├─ DRY (eliminate duplication)
├─ Separation of Concerns (business logic ≠ plumbing)
├─ Testability (loose coupling, injectable)
└─ Cognitive Load (reduce mental effort)

ADVANCED (Optimise These)
├─ Immutability (reduce state change)
├─ Composition (build from simple parts)
├─ Abstractions (hide unnecessary detail)
└─ Performance (measure before optimising)
```

---

## Resource Links

- **Full workflow**: SKILL.md
- **Learning paths**: README.md (reading-paths section)
- **For reviewers**: coaching-review-template.md + analysis-rubric.md
- **For teachers**: teaching-script.md + deconstruction-model.md
- **For architects**: best-practices.md + refactoring-priorities.md
- **For debugging**: code-smells.md + cognitive-load.md

---

**Version**: 1.0 | **Updated**: May 2026 | **Status**: Production
