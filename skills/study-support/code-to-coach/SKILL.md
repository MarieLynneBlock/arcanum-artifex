---
name: code-to-coach
description: Deconstruct code into bite-sized, logical chunks from a coaching perspective. Remove abstraction, explain the "why" behind each concept, identify best practices, code smells, and cognitive load issues. Use structured frameworks to provide thorough, pedagogical analysis that teaches *how to think* about code, not just what it does.
metadata:
  skill-author: Arcanum Artifex
  version: "1.0"
  trigger-phrases:
    - "explain this code like I'm learning"
    - "coach me through this code"
    - "deconstruct this code"
    - "teaching perspective on code"
    - "code smell analysis"
    - "explain the why in this code"
    - "pedagogical code review"
    - "break down this into chunks"
    - "what's the anti-pattern here?"
    - "why is this structured this way?"
---

# Code-to-Coach Skill

## Overview

This skill transforms code analysis into a **teaching and coaching dialogue**. Instead of explaining *what* code does, it:

1. **Deconstructs** into logical units (functions, classes, patterns, business logic)
2. **Removes abstraction** by connecting to concrete examples and intent
3. **Explains intent** — the "why" behind each decision
4. **Identifies patterns** — recognises idioms, best practices, and smells
5. **Highlights cognitive load** — pinpoints confusing areas and suggests clearer structures
6. **Teaches thinking patterns** — helps the learner develop intuition about code structure

## When to Use This Skill

Use this skill when:
- A learner wants to understand how to *think* about a codebase, not just understand its current form
- You need to identify why code is difficult to maintain or extend
- You're reviewing code with an educational goal
- You want to recognise anti-patterns and suggest improvements with justification
- You need to break down complex logic into teachable chunks
- You're preparing code for code review, documentation, or mentoring

## Workflow: The Five-Step Coaching Cycle

### Step 1: Orient — Scope and Context
- **Ask**: What is this code's job? Who calls it? What problem does it solve?
- **Look for**: Business purpose, entry/exit points, dependencies
- **Output**: 1–2 sentences of clear context (remove jargon)
- **Tool**: Use [context-discovery.md](./reference/context-discovery.md)

### Step 2: Deconstruct — Break Into Chunks
- **Split** the code into logical units using the [deconstruction-model.md](./frameworks/deconstruction-model.md)
- **Identify**: Functions, loops, conditionals, state mutations, side effects, business rules
- **Name each chunk** with a verb phrase (e.g., "Validate email format", "Fetch user from database")
- **Remove jargon**: Translate technical terms to intent (e.g., "memoization" → "cache results to avoid recalculation")
- **Output**: Annotated code or flowchart showing chunks and their relationships

### Step 3: Analyse — Evaluate Quality Using the Rubric
- **Apply** the [analysis-rubric.md](./frameworks/analysis-rubric.md) to each chunk:
  - Clarity & naming
  - Single responsibility
  - Error handling & assumptions
  - Testability & dependencies
  - Performance & resource use
  - Cognitive load (nesting depth, variable scope, mutability)
- **Identify** code smells from [code-smells.md](./reference/code-smells.md)
- **Note** best practices from [best-practices.md](./reference/best-practices.md)
- **Output**: Strengths, concerns, and refactoring opportunities with rationale

### Step 4: Teach — Explain the Why
- **For each chunk**, answer:
  - *Why was this pattern chosen?*
  - *What problem does it solve?*
  - *What trade-offs were made?* (simplicity vs. performance, flexibility vs. maintainability, etc.)
  - *How would a learner *think* about this decision?*
- **Reference**: Use [cognitive-load.md](./reference/cognitive-load.md) to frame clarity issues
- **Suggest**: Better names, clearer logic flow, or simpler patterns with *rationale*, not just opinion
- **Output**: Coached explanation that builds intuition

### Step 5: Advise — Next Steps
- **Prioritise** refactoring opportunities using [refactoring-priorities.md](./reference/refactoring-priorities.md)
- **Provide** specific, actionable suggestions (with code examples if helpful)
- **Link** to [best-practices.md](./reference/best-practices.md) or language-specific resources
- **Output**: Numbered, actionable items ranked by impact and effort

## Templates & Guides

- **[Coaching Review Template](./templates/coaching-review-template.md)** — Structured format for delivering feedback
- **[Analysis Rubric](./frameworks/analysis-rubric.md)** — Criteria for evaluating code quality
- **[Deconstruction Model](./frameworks/deconstruction-model.md)** — How to break code into teachable units
- **[Teaching Script](./templates/teaching-script.md)** — Skeleton for explaining code to a learner

## Reference Materials

- **[Code Smells](./reference/code-smells.md)** — Anti-patterns and their symptoms
- **[Best Practices](./reference/best-practices.md)** — Language-agnostic principles for maintainability
- **[Cognitive Load](./reference/cognitive-load.md)** — How to spot and reduce mental friction
- **[Context Discovery](./reference/context-discovery.md)** — Questions to understand a codebase

## Key Principles

1. **No jargon without context** — Every technical term connects to intent and trade-offs
2. **Chunking first** — Before analysis, divide into logical units a learner can hold in their head
3. **Why over what** — Explain design decisions, not syntax
4. **Empathy** — Assume the code was written with good intent; surface the constraints
5. **Actionable** — Every suggestion includes rationale and effort estimate
6. **Teach thinking, not rules** — Help learners develop intuition, not memorise dos and don'ts

## Success Criteria

A successful coaching session:
- ✓ Learner understands the *purpose* of each chunk
- ✓ Learner can articulate *why* the code is structured this way
- ✓ Learner identifies *why* certain areas are hard to understand
- ✓ Learner has *actionable* suggestions for improvement, ranked by impact
- ✓ Learner can apply the same thinking to unfamiliar code

## Constraints & Limits

- **Language scope**: Apply coaching to any language; adjust examples and idioms accordingly
- **Scale**: Works best on functions or classes (up to 100–200 lines). For larger codebases, apply recursively to modules/services
- **Assumptions**: Assumes the code is the *real* implementation, not pseudocode or incomplete logic
- **No guessing**: If business context is missing, flag it and ask (don't assume intent)

## Next Steps

1. Choose a piece of code (function, class, or module)
2. Orient yourself using [context-discovery.md](./reference/context-discovery.md)
3. Deconstruct using the [deconstruction-model.md](./frameworks/deconstruction-model.md)
4. Analyse against the [analysis-rubric.md](./frameworks/analysis-rubric.md)
5. Teach using the [teaching-script.md](./templates/teaching-script.md) skeleton
6. Advise using the [coaching-review-template.md](./templates/coaching-review-template.md) format
