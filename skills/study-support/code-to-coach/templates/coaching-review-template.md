# Coaching Review Template

## Purpose

A structured format for delivering coaching-style code feedback. This template ensures feedback is:
- **Clear**: Explained in plain language
- **Actionable**: Specific next steps
- **Pedagogical**: Teaches *why*, not just *what*
- **Prioritised**: Focuses on high-impact items first

---

## The Template

### Section 1: Orientation

**Goal**: Set context so the learner understands what you're reviewing and why.

```markdown
## Code Review: [Function/Class/Module Name]

**Context**: [2–3 sentences on what this code does and why you're reviewing it]

**Reviewer approach**: [How are you evaluating this? 
  e.g., "Looking at clarity, testability, and adherence to team standards"]
```

**Example**:
```markdown
## Code Review: `validate_user_email()`

**Context**: This function validates email format for user signup. 
It's called in the critical path, so clarity and performance matter.

**Reviewer approach**: I'm evaluating naming clarity, error handling, 
and whether the validation logic is sound.
```

---

### Section 2: Strengths

**Goal**: Acknowledge what's working well. This builds confidence and context for suggestions.

```markdown
## What's Working Well

- **[Strength 1]**: [Why this is good; what it enables]
- **[Strength 2]**: [Why this is good; what it enables]
- **[Strength 3]**: [Why this is good; what it enables]
```

**Example**:
```markdown
## What's Working Well

- **Clear error messages**: The validation errors tell the user *what* went wrong 
  ("Email must contain @"), not just "Invalid email". This improves UX.

- **Early validation**: You check for null inputs before processing, 
  preventing downstream crashes. Good defensive coding.

- **Test coverage**: The tests cover happy path and edge cases (no @, empty string). 
  That's thorough.
```

---

### Section 3: Observations (Deconstructed View)

**Goal**: Walk through the code piece by piece, showing how you're analysing it.

```markdown
## How This Code Works

**Phase 1: [Name]** (lines X–Y)
- What it does: [Plain English]
- Why: [The reason this phase is here]
- Observation: [What you notice; any questions?]

**Phase 2: [Name]** (lines Y–Z)
- What it does: [Plain English]
- Why: [The reason this phase is here]
- Observation: [What you notice; any questions?]
```

**Example**:
```markdown
## How This Code Works

**Phase 1: Extract parts** (lines 3–5)
```python
parts = email.split('@')
if len(parts) != 2:
    return False
```
- What it does: Split email into user and domain parts; return false if there's not exactly one @
- Why: An email must have exactly one @ symbol
- Observation: ✓ Good guard clause; fails fast

**Phase 2: Validate domain** (lines 6–8)
```python
domain = parts[1]
if '.' not in domain:
    return False
```
- What it does: Check that the domain has at least one dot (e.g., "example.com")
- Why: Valid domains have a TLD (top-level domain)
- Observation: Assumes domain is not empty. This is safe because of Phase 1, but a comment would help readers trace the dependency
```

---

### Section 4: Concerns (By Priority)

**Goal**: List issues in priority order (URGENT → IMPORTANT → NICE-TO-HAVE). Frame each as a teaching point.

```markdown
## Areas for Improvement

### 🔴 URGENT (High impact, low effort)

**[Concern 1]**: [Description]
- Impact: [Why this matters]
- How to fix: [Concrete suggestion]
- Teaching point: [What the learner should learn]

Example code:
\`\`\`
[Before]
\`\`\`

Refactored:
\`\`\`
[After]
\`\`\`

---

### 🟡 IMPORTANT (High impact, plan to tackle)

**[Concern 1]**: [Description]
- Impact: [Why this matters]
- How to fix: [Concrete suggestion]
- Teaching point: [What the learner should learn]

---

### 🟢 NICE-TO-HAVE (Low effort, polish)

**[Concern 1]**: [Description]
- How to fix: [Optional improvement]
- Why defer: [Not blocking; can do when time permits]
```

**Example**:
```markdown
## Areas for Improvement

### 🔴 URGENT (High impact, low effort)

**Email domain validation is incomplete**: Currently checks for `.` in domain, 
but `example.` or `.example` would pass. This could allow invalid emails.

- Impact: Invalid emails might slip through, causing downstream failures
- How to fix: Refine the check to ensure the dot is between characters:
  ```python
  domain_parts = domain.split('.')
  if len(domain_parts) < 2:
      return False
  # Ensure each part is non-empty
  if any(not part for part in domain_parts):
      return False
  ```
- Teaching point: Always think about edge cases. What's the minimal valid input? 
  What's the most malformed input that still matches your pattern?

---

### 🟡 IMPORTANT (High impact, plan to tackle)

**Needs a constants file**: The validation logic is hardcoded (@ character, . character, 
length limits). This should be configurable.

- Impact: If validation rules change (e.g., allow + in email), you'd have to update code in multiple places
- How to fix: Extract a config object:
  ```python
  EMAIL_VALIDATION = {
      'required_symbols': ['@'],
      'domain_delimiter': '.',
      'min_length': 5,
  }
  ```
- Teaching point: Think about what might change. What are the assumptions in your code? 
  Should those be constants or configuration?

---

### 🟢 NICE-TO-HAVE (Low effort, polish)

**Variable name**: `parts` is generic. Could be `email_parts` or `[user, domain] = email.split('@')` 
to make it clearer.

- How to fix: Unpack directly:
  ```python
  user, domain = email.split('@')
  ```
- Why defer: Already clear from context; not blocking. But good practice if you're refactoring anyway.
```

---

### Section 5: Recommended Next Steps

**Goal**: Give the learner a clear action plan.

```markdown
## Recommended Next Steps

1. **[Highest priority task]**: [Why this matters; estimated effort]
2. **[Second priority]**: [Why this matters; estimated effort]
3. **[Polish item]**: [Optional; do if time permits]

**Questions to explore**:
- [Open question about design choice]
- [Open question about trade-off]
- [Open question about testing]

**Resources**:
- [Link to relevant best practice guide]
- [Link to similar code you can learn from]
```

**Example**:
```markdown
## Recommended Next Steps

1. **Strengthen domain validation** (15 min): Ensure dots aren't at start/end of domain. 
   This prevents invalid emails from passing through.

2. **Extract validation rules to config** (30 min): If validation rules might change, 
   this makes the code more flexible.

3. **Add inline comment** (5 min): Explain the dependency between phases 
   (domain is safe to index because of the @ check).

**Questions to explore**:
- "What happens if someone passes `None` or a non-string to this function? Should we validate the type?"
- "Are there domain-specific rules you need to support? (e.g., allowing + in email addresses)"

**Resources**:
- RFC 5322 (official email standard) — describes the full spec
- [Best practices: Fail fast, fail explicitly](../reference/best-practices.md)
```

---

### Section 6: Closing

**Goal**: Summarise, encourage, and set expectations for next steps.

```markdown
## Summary

This code is [overall assessment]. The main opportunities are [1–2 key takeaways].

[Encouragement specific to the learner's level/context]

Next time we review, let's focus on [future learning goal].

---

**Next steps**: Please address the URGENT items above, then we can discuss IMPORTANT items 
in the next review. Let me know if you want to pair on any of these!
```

**Example**:
```markdown
## Summary

This validation function is solid and well-tested. The main opportunities are 
tightening edge cases and making the rules configurable.

You're thinking defensively (checking edge cases, failing fast), which is great. 
The next level is anticipating *what* might change and designing for flexibility.

Next time we review, let's focus on extracting configurable rules into a data structure.

---

**Next steps**: Please refine the domain validation and add the inline comment explaining 
the @ check. Once you've done that, let's pair for 15 min on the config extraction. 
Feel free to ask questions anytime!
```

---

## Tips for Using This Template

### Keep It Conversational
- Use "I notice" instead of "You should"
- Ask questions ("What happens if…?") instead of declaring problems
- Celebrate strengths genuinely

### Show the Work
- Show how you analysed the code (deconstruction)
- Explain *why* something is a concern, not just *what*
- Provide concrete refactoring examples

### Prioritise Ruthlessly
- Only 2–3 URGENT items per review
- If everything is urgent, nothing is
- This teaches decision-making, not perfectionism

### Teach Patterns, Not Rules
- "Here's the trade-off…" (not "This is wrong")
- "Think about what might change…" (not "You didn't think of…")
- "Let's look at how the team handles this…" (not "Everyone does it this way")

### Adapt to Learner Level

**For beginners**: Focus on URGENT items; provide more detailed examples; explain *why* each practice matters

**For intermediate**: Include IMPORTANT items; ask guiding questions; suggest resources

**For senior**: Focus on architecture and trade-offs; ask probing questions; discuss alternatives

---

## Template Checklist

Before sending your review, check:

- [ ] **Orientation**: Does the reader understand the context and your approach?
- [ ] **Strengths**: Did I acknowledge what's working? (Never skip this)
- [ ] **Deconstruction**: Did I walk through the code showing my analysis?
- [ ] **Priorities**: Are concerns sorted URGENT → IMPORTANT → NICE-TO-HAVE?
- [ ] **Actionable**: Can the learner take concrete next steps?
- [ ] **Teaching**: Did I explain *why*, not just *what*?
- [ ] **Tone**: Is this encouraging and collaborative, not critical?
- [ ] **Examples**: Did I show before/after for each concern?

---

## Example: Full Review Using This Template

[See coaching-review-example.md for a complete worked example]
