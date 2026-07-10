# Code-to-Coach: Comprehensive Skill Package

## Welcome

This skill transforms code analysis into a **coaching and teaching dialogue**. Instead of explaining *what* code does, it teaches *how to think* about code — breaking it down into chunks, explaining the "why" behind decisions, identifying patterns and smells, and teaching the reasoning that produces good code.

---

## 📚 What's in This Skill?

### Core Entry Point
- **[SKILL.md](./SKILL.md)** — The main entry point; read this first for the overall workflow

### Frameworks (Teaching Models)
- **[deconstruction-model.md](./frameworks/deconstruction-model.md)** — How to break code into bite-sized, teachable chunks
- **[analysis-rubric.md](./frameworks/analysis-rubric.md)** — Criteria for evaluating code quality (6 dimensions: clarity, responsibility, error handling, testability, cognitive load, performance)

### Reference Materials (Domain Knowledge)
- **[code-smells.md](./references/code-smells.md)** — 10 common anti-patterns (long functions, deep nesting, magic numbers, duplication, etc.) with refactoring strategies
- **[best-practices.md](./references/best-practices.md)** — 12 language-agnostic principles (SRP, DRY, fail fast, dependency injection, separation of concerns, naming, documentation, immutability, composition, invalid states, measurement, explicitness)
- **[cognitive-load.md](./references/cognitive-load.md)** — 9 strategies to reduce mental friction in code (limit nesting, minimize mutations, reduce scope, clear flow, naming patterns, separate concerns, document assumptions, abstractions, parameter limits)
- **[context-discovery.md](./references/context-discovery.md)** — Questions to ask when orienting yourself to unfamiliar code
- **[refactoring-priorities.md](./references/refactoring-priorities.md)** — Framework for prioritising improvements (impact × effort matrix, categorisation from URGENT to DEFER)

### Templates (Structured Formats)
- **[coaching-review-template.md](./templates/coaching-review-template.md)** — Structured format for delivering coaching-style feedback (strengths, observations, concerns by priority, next steps)
- **[teaching-script.md](./templates/teaching-script.md)** — Skeleton for explaining code to learners (big picture, chunk-by-chunk walkthrough, examples, questions, pattern connection, reflection)

---

## 🚀 How to Use This Skill

### Workflow: The Five-Step Coaching Cycle

**1. Orient** — Scope and context
   - Use [context-discovery.md](./references/context-discovery.md) to understand the code's purpose, constraints, and history
   - Answer: "What is this code's job? Why does it exist? What are the constraints?"

**2. Deconstruct** — Break into chunks
   - Use [deconstruction-model.md](./frameworks/deconstruction-model.md) to break code into logical units
   - Answer: "What are the distinct phases or operations?"
   - Name each chunk with a verb phrase

**3. Analyse** — Evaluate quality
   - Use [analysis-rubric.md](./frameworks/analysis-rubric.md) to evaluate each chunk:
     - Clarity & naming
     - Single responsibility
     - Error handling & assumptions
     - Testability & dependencies
     - Cognitive load
     - Performance & resource use
   - Cross-reference with [code-smells.md](./references/code-smells.md) for anti-patterns

**4. Teach** — Explain the why
   - For each chunk, answer:
     - *Why was this pattern chosen?*
     - *What problem does it solve?*
     - *What trade-offs were made?*
   - Use [cognitive-load.md](./references/cognitive-load.md) to frame clarity issues
   - Use [best-practices.md](./references/best-practices.md) to justify suggestions

**5. Advise** — Next steps
   - Use [refactoring-priorities.md](./references/refactoring-priorities.md) to rank opportunities
   - Use [coaching-review-template.md](./templates/coaching-review-template.md) to structure feedback

### Quick Start: Choose Your Path

**I need to review someone's code:**
→ Use [coaching-review-template.md](./templates/coaching-review-template.md)
→ Reference [analysis-rubric.md](./frameworks/analysis-rubric.md), [code-smells.md](./references/code-smells.md), [refactoring-priorities.md](./references/refactoring-priorities.md)

**I need to explain code to someone:**
→ Use [teaching-script.md](./templates/teaching-script.md)
→ Reference [deconstruction-model.md](./frameworks/deconstruction-model.md)

**I'm stuck understanding unfamiliar code:**
→ Use [context-discovery.md](./references/context-discovery.md)
→ Then use [deconstruction-model.md](./frameworks/deconstruction-model.md)

**I see code smells but not sure what to fix first:**
→ Use [refactoring-priorities.md](./references/refactoring-priorities.md)
→ Then reference [best-practices.md](./references/best-practices.md)

**I want to make code easier to understand:**
→ Use [cognitive-load.md](./references/cognitive-load.md)
→ Reference [best-practices.md](./references/best-practices.md)

---

## 🎓 Core Principles

1. **No jargon without context** — Every technical term connects to intent and trade-offs
2. **Chunking first** — Divide into logical units before analysis
3. **Why over what** — Explain design decisions, not syntax
4. **Empathy** — Assume good intent; surface constraints
5. **Actionable** — Every suggestion includes rationale and effort estimate
6. **Teach thinking, not rules** — Develop intuition, not memorisation

---

## 📋 Document Map

```
code-to-coach/
├── SKILL.md                          ← Start here: Overall workflow and entry point
├── frameworks/
│   ├── deconstruction-model.md       (How to break code into chunks)
│   └── analysis-rubric.md            (6 criteria for evaluating quality)
├── references/
│   ├── code-smells.md                (10 anti-patterns and fixes)
│   ├── best-practices.md             (12 language-agnostic principles)
│   ├── cognitive-load.md             (9 strategies to reduce mental friction)
│   ├── context-discovery.md          (Questions to understand code)
│   └── refactoring-priorities.md     (Prioritise improvements)
└── templates/
    ├── coaching-review-template.md   (Structured feedback format)
    └── teaching-script.md            (Skeleton for explaining code)
```

---

## 💡 Key Concepts at a Glance

### The Six Evaluation Dimensions (from analysis-rubric.md)

| Dimension | Question | Why It Matters |
|-----------|----------|----------------|
| **Clarity & Naming** | Can I understand intent without reading code? | Reduces time to understand; aids maintenance |
| **Single Responsibility** | Does this do one thing? | Easier to test, reuse, change |
| **Error Handling** | What happens if it fails? | Code is robust and debuggable |
| **Testability** | Can I write a unit test easily? | Code is decoupled and understandable |
| **Cognitive Load** | How much mental effort to understand? | Reduces bugs, aids maintenance |
| **Performance** | Is it efficient at scale? | Avoids surprises in production |

### The Ten Code Smells (from code-smells.md)

1. Long functions
2. Deeply nested conditionals
3. Magic numbers
4. Duplicate code
5. Unclear variable names
6. Hidden dependencies
7. Inconsistent error handling
8. Tight coupling
9. Comments explaining obvious code
10. God objects

### The Twelve Best Practices (from best-practices.md)

1. Single Responsibility Principle (SRP)
2. Don't Repeat Yourself (DRY)
3. Fail Fast, Fail Explicitly
4. Dependency Injection
5. Separation of Concerns
6. Name Things Well
7. Document Why, Not What
8. Prefer Immutability
9. Composition Over Inheritance
10. Make Invalid States Unrepresentable
11. Measure Before Optimising
12. Explicit Is Better Than Implicit

### The Nine Cognitive Load Strategies (from cognitive-load.md)

1. Limit nesting depth (<4 levels)
2. Minimize mutable state
3. Reduce variable scope
4. Use clear, chunked logic flow
5. Enforce consistent naming patterns
6. Separate business logic from plumbing
7. Document assumptions and invariants
8. Use meaningful abstractions
9. Limit function parameters (<3)

---

## 🎯 Success Criteria

A successful coaching session meets these criteria:

- ✓ Learner understands the *purpose* of each chunk
- ✓ Learner can articulate *why* the code is structured this way
- ✓ Learner identifies *why* certain areas are hard to understand
- ✓ Learner has *actionable* suggestions for improvement, ranked by impact
- ✓ Learner can apply the same thinking to unfamiliar code

---

## 📖 Reading Paths

### Path 1: Learn to Review Code (30 min)
1. Read [SKILL.md](./SKILL.md) (overview)
2. Read [analysis-rubric.md](./frameworks/analysis-rubric.md) (evaluation dimensions)
3. Read [coaching-review-template.md](./templates/coaching-review-template.md) (structured feedback)
4. Read [refactoring-priorities.md](./references/refactoring-priorities.md) (prioritisation)

### Path 2: Learn to Teach Code (40 min)
1. Read [SKILL.md](./SKILL.md) (overview)
2. Read [deconstruction-model.md](./frameworks/deconstruction-model.md) (breaking into chunks)
3. Read [teaching-script.md](./templates/teaching-script.md) (teaching structure)
4. Read [cognitive-load.md](./references/cognitive-load.md) (making it understandable)

### Path 3: Understand a Codebase (45 min)
1. Read [context-discovery.md](./references/context-discovery.md) (orientation questions)
2. Read [deconstruction-model.md](./frameworks/deconstruction-model.md) (break into chunks)
3. Read [analysis-rubric.md](./frameworks/analysis-rubric.md) (evaluate quality)
4. Read [code-smells.md](./references/code-smells.md) (identify patterns)

### Path 4: Improve Existing Code (60 min)
1. Read [code-smells.md](./references/code-smells.md) (identify issues)
2. Read [best-practices.md](./references/best-practices.md) (understand principles)
3. Read [refactoring-priorities.md](./references/refactoring-priorities.md) (prioritise)
4. Read [cognitive-load.md](./references/cognitive-load.md) (reduce friction)

---

## 🔗 Cross-References

Each document links to related materials:
- **analysis-rubric.md** → See code-smells.md for specific anti-patterns
- **code-smells.md** → See best-practices.md for principles behind fixes
- **cognitive-load.md** → See best-practices.md for patterns supporting these strategies
- **coaching-review-template.md** → Uses analysis-rubric.md, refactoring-priorities.md, best-practices.md
- **teaching-script.md** → Uses deconstruction-model.md, cognitive-load.md

---

## ✅ Constraints & Limits

- **Language scope**: Applies to any programming language; adjust examples and idioms
- **Scale**: Works best on functions/classes (50–200 lines). For larger codebases, apply recursively
- **Assumptions**: Assumes the code is the *real* implementation, not pseudocode
- **No guessing**: If context is missing, ask — don't assume intent

---

## 🎓 Teaching Philosophy

This skill is built on **cognitive science principles**:

- **Chunking**: Our working memory can hold ~7 items. Break code into logical chunks.
- **Mental models**: Help learners build intuition by explaining *why*, not just *what*.
- **Scaffolding**: Start simple, build complexity. Teach patterns, not rules.
- **Feedback loops**: Short cycles of "predict → observe → reflect" build understanding.
- **Transfer**: Teach principles so learners can apply them to unfamiliar code.

---

## 📝 Notes for Skill Adoption

This skill is **fully self-contained**. Every file is standalone and copyable:
- No external dependencies or links to other codebases
- All frameworks, templates, and references are included
- Examples are embedded in each document
- Cross-references use relative markdown links within the skill folder

To adopt this skill in your project:
1. Copy the entire `code-to-coach/` folder to your `.github/skills/` directory
2. Reference [SKILL.md](./SKILL.md) when invoking the skill
3. Use the templates and frameworks as-is or adapt for your context

---

## 🚀 Next Steps

- **To review code**: Start with [coaching-review-template.md](./templates/coaching-review-template.md)
- **To explain code**: Start with [teaching-script.md](./templates/teaching-script.md)
- **To understand a codebase**: Start with [context-discovery.md](./references/context-discovery.md)
- **To improve code**: Start with [code-smells.md](./references/code-smells.md)

---

**Version**: 1.0  
**Last updated**: May 2026  
**Status**: Production-ready  
**Maintenance**: Evergreen resource; update when best practices or teaching techniques evolve
