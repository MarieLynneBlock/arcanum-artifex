# Teaching Script Template

## Purpose

A structured skeleton for explaining code to a learner. This template helps you:
- **Chunk** the explanation into digestible pieces
- **Orient** the learner before diving into details
- **Explain why** before explaining how
- **Test** understanding along the way
- **Connect** to bigger concepts

---

## The Template

### Opening: Set the Stage

**Goal**: Help the learner know what's coming and why it matters.

```markdown
## Learning Goal

Today we're exploring [what they'll learn].

**Why this matters**: [What problem does this solve? How will they use it?]

**Complexity level**: [Beginner / Intermediate / Advanced]

**Time estimate**: [10 minutes / 30 minutes / 1 hour]

**Prerequisites**: [What should they already know?]
```

**Example**:
```markdown
## Learning Goal

Today we're exploring how to validate user input without crashing your program.

**Why this matters**: Invalid data causes bugs. Learning to validate early 
prevents problems downstream and makes your code more reliable.

**Complexity level**: Beginner

**Time estimate**: 20 minutes

**Prerequisites**: Basic understanding of functions, if statements, and strings
```

---

### Part 1: The Big Picture

**Goal**: Give the learner the 30-second version before the details.

```markdown
## The Big Picture

[1–2 sentences describing what this code does at a high level]

**The flow looks like this**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Think of it like: [Analogy that makes sense to the learner]
```

**Example**:
```markdown
## The Big Picture

This function checks if an email is valid. It doesn't send emails or look them up — 
it just checks the format.

**The flow looks like this**:
1. Check that there's exactly one @ symbol
2. Check that the domain part has a dot
3. Return true or false

Think of it like a bouncer checking ID at a club: "Does this look like a real email 
format?" not "Do I know this person?" or "Has this email actually been used?"
```

---

### Part 2: The Code, Chunk by Chunk

**Goal**: Walk through the code piece by piece, explaining intent for each chunk.

```markdown
## Let's Walk Through It

### Chunk 1: [Name]

**What this chunk does**: [Plain English description]

**The code**:
\`\`\`
[Code snippet, 3–10 lines max]
\`\`\`

**Breaking it down**:
- [Line/concept 1]: [Explanation and why]
- [Line/concept 2]: [Explanation and why]

**The teaching moment**: [What should they learn from this chunk?]

---

### Chunk 2: [Name]

[Same structure as Chunk 1]

---

### Chunk 3: [Name]

[Same structure as Chunk 1]
```

**Example**:
```markdown
## Let's Walk Through It

### Chunk 1: Split the Email

**What this chunk does**: Take the email and split it into two parts: 
the user part and the domain part.

**The code**:
\`\`\`python
parts = email.split('@')
if len(parts) != 2:
    return False
\`\`\`

**Breaking it down**:
- `parts = email.split('@')`: Split the string on the @ symbol. 
  If email is "alice@example.com", parts becomes ["alice", "example.com"]
- `if len(parts) != 2:` Check that we got exactly 2 parts. 
  Why? Because a valid email must have exactly one @ symbol. 
  If someone passes "alice@example@com" (two @), we get 3 parts and reject it.
- `return False`: Exit early and say "not valid". 
  This is called a "guard clause" — check preconditions first, fail fast.

**The teaching moment**: When validating, always ask: "What patterns should I accept? 
What patterns should I reject?" Here, the pattern is "exactly one @".

---

### Chunk 2: Validate the Domain

**What this chunk does**: Check that the domain (the part after @) looks valid.

**The code**:
\`\`\`python
domain = parts[1]
if '.' not in domain:
    return False
\`\`\`

**Breaking it down**:
- `domain = parts[1]`: Get the second part (the domain). 
  We know it exists because we checked in Chunk 1.
- `if '.' not in domain`: Check that the domain has a dot. 
  Why? Real domains have a TLD (top-level domain): ".com", ".org", ".co.uk", etc. 
  No dot means no TLD, so it's not a valid email domain.
- `return False`: Reject it.

**The teaching moment**: Notice how each chunk builds on the previous one. 
We only check the domain *after* we know the email has exactly one @. 
This is called "layered validation" — check one thing, then the next.

---

### Chunk 3: Accept It

**What this chunk does**: If we got this far, all checks passed. Return true.

**The code**:
\`\`\`python
return True
\`\`\`

**Breaking it down**:
- `return True`: We passed all checks, so the email format is valid.

**The teaching moment**: Notice we only return True at the end. 
We could return False many times (if any check fails), but we only return True once 
(if all checks pass). This is the "happy path" — the success case.
```

---

### Part 3: Tracing Through an Example

**Goal**: Show the code in action with concrete input.

```markdown
## Let's Trace Through an Example

**Input**: "alice@example.com"

**Step 1** (Chunk 1):
- `parts = "alice@example.com".split('@')` → parts = ["alice", "example.com"]
- `len(parts)` → 2 (✓ passes check)

**Step 2** (Chunk 2):
- `domain = "example.com"`
- `'.' in "example.com"` → True (✓ passes check)

**Step 3** (Chunk 3):
- All checks passed → `return True`

**Result**: alice@example.com is valid ✓

---

**Now let's trace through an invalid email**:

**Input**: "bob@invalid"

**Step 1** (Chunk 1):
- `parts = "bob@invalid".split('@')` → parts = ["bob", "invalid"]
- `len(parts)` → 2 (✓ passes check)

**Step 2** (Chunk 2):
- `domain = "invalid"`
- `'.' in "invalid"` → False (✗ fails check)
- `return False` ← We stop here and reject it

**Result**: bob@invalid is invalid ✗ (no TLD)
```

---

### Part 4: Common Questions & Edge Cases

**Goal**: Prepare the learner for questions and edge cases they might encounter.

```markdown
## Questions You Might Ask

**Q: Why exactly one @? Can't there be zero or more?**

A: An email address has the format `user@domain`. By definition, it needs exactly one @. 
If there's no @, it's not an email. If there's more than one, it's ambiguous (which part is the domain?).

---

**Q: What about emails like "alice+tag@example.com"? The + isn't checked.**

A: Good observation! This validation is a simplified check. It handles the most common case. 
A full RFC 5322 validation is much more complex. In real code, we'd probably use a library 
for the full spec. This function is intentionally simple to learn the concepts.

---

**Q: What if someone passes None or not a string?**

A: Great question! This function assumes the input is a string. 
In production code, we'd add a check: 
\`\`\`python
if not isinstance(email, str):
    return False
\`\`\`

---

**Q: Why do we check the domain part, not the user part?**

A: The domain is more tightly constrained (must have a dot, must be a known TLD). 
The user part can be almost anything. The domain is where most invalid emails fail.
```

---

### Part 5: The Pattern

**Goal**: Help the learner see the broader pattern, not just this one example.

```markdown
## The Pattern: Input Validation

This function follows a common pattern: **validate input before processing**.

**The pattern**:
1. Check preconditions (Is the input the right type? Does it have required parts?)
2. Check format (Does it match the expected pattern?)
3. Check constraints (Are values within acceptable ranges?)
4. Return early if any check fails (fail fast)
5. Proceed if all checks pass

**You'll see this pattern in**:
- Form validation (checking user input from web forms)
- API endpoint validation (checking data sent to your server)
- File parsing (checking headers before processing)
- Configuration parsing (checking config files are valid)

**When you write code**, ask: "What assumptions am I making about the input? 
Should I validate those, or document them?"
```

---

### Part 6: Reflection & Practice

**Goal**: Help the learner cement their understanding.

```markdown
## Stop & Reflect

**1. In your own words**: Explain what this function does in one sentence.

**2. Predict**: If someone passes "alice.example.com" (no @), what happens?
   (Work through it step by step before reading the answer)

**3. Design**: How would you modify this to also accept emails with subdomains like "alice@mail.example.com"?
   (Hint: How many dots should be allowed?)

---

## Answers & Discussion

**1. In your own words**: [Accept any answer that captures: checks if email has format user@domain]

**2. Predict**: 
- `parts = ["alice.example.com"]` (split finds no @, so no split happens)
- `len(parts) != 2` → True, so we return False immediately
- Result: Rejected ✗

**3. Design**: 
- Current code: `'.' in domain` checks for at least one dot ✓
- Subdomains: "mail.example.com" has two dots, which the current code accepts ✓
- So the code already works! It accepts 1+ dots in the domain.
```

---

### Closing: Next Steps

**Goal**: Connect what they learned to what's next.

```markdown
## What's Next?

**You've learned**: How to validate email format with a simple heuristic.

**Next steps**:
1. Try writing a similar validator for phone numbers
2. Look up RFC 5322 and see the full spec (you'll see why we keep it simple!)
3. When you see input validation in real code, trace through it like we did here
4. Think about: What assumptions is the code making? Are they documented?

**Additional resources**:
- [Best Practices: Fail Fast, Fail Explicitly](../reference/best-practices.md)
- [Code Smells: Missing Error Handling](../reference/code-smells.md)
- [Deconstruction Model: Breaking Code Into Chunks](../frameworks/deconstruction-model.md)

**Questions?** Ask anytime. This pattern shows up everywhere.
```

---

## Tips for Using This Template

### Make It Conversational
- Use "Let's" not "Here's"
- Ask questions rhetorically, then answer them
- Use analogies and comparisons

### Show Your Thinking
- Walk through every line, not just the interesting ones
- Explain *why* each line is there, not just what it does
- Trace through examples step-by-step

### Meet Learners Where They Are
- Use simpler analogies for beginners (bouncer checking ID)
- Use technical analogies for advanced learners (lazy evaluation, short-circuiting)
- Acknowledge the level: "At your level, this detail doesn't matter, but later you'll care"

### Chunk Ruthlessly
- Aim for 3–5 chunks per explanation
- Each chunk should fit on one screen
- Each chunk should take 2–3 minutes to explain

### Connect to Bigger Ideas
- Every explanation should point to a broader pattern or principle
- Help learners see the pattern, not just the code

---

## Example: Full Teaching Script

**Title**: Understanding Dependency Injection

### Opening: Set the Stage
```
## Learning Goal

Today we're learning dependency injection — a way to write code that's easier to test 
and reuse.

Why this matters: If your code is tightly coupled to specific implementations 
(database, email service), testing is hard. Dependency injection decouples them.

Complexity level: Intermediate

Time estimate: 30 minutes

Prerequisites: Understanding of functions, parameters, basic OOP
```

### The Big Picture
```
## The Big Picture

Dependency injection is a fancy term for a simple idea: 
**Pass dependencies as parameters instead of creating them inside your function.**

Think of it like: You don't create your own guitar before a concert; 
the concert hall provides one for you. This way, you can use any guitar, 
and you're not locked into one specific instrument.
```

[Continue with chunks, examples, questions, pattern, reflection...]

---

## Template Checklist

Before teaching, check:

- [ ] **Opening**: Does the learner know what they're learning and why?
- [ ] **Big Picture**: Does the 30-second version make sense?
- [ ] **Chunks**: Is each chunk 5–10 lines of code max?
- [ ] **Explanations**: Did I explain *why*, not just *what*?
- [ ] **Examples**: Did I trace through concrete input with output?
- [ ] **Questions**: Did I anticipate what they might wonder?
- [ ] **Pattern**: Did I connect to a broader idea?
- [ ] **Reflection**: Can they test their understanding?
- [ ] **Next Steps**: Do they know where to go from here?
- [ ] **Tone**: Is this encouraging and exploratory, not lecturing?

---

## Variations

### For Synchronous Teaching (Live)
- Use this as a script; read it out loud
- Pause after each chunk for questions
- Invite learners to predict before you explain

### For Asynchronous (Written/Video)
- Use code highlighting and formatting
- Include links to resources
- Add visual diagrams where helpful

### For Code Review
- Adapt chunks to match the code being reviewed
- Use the teaching script format to explain why a change is suggested

---

## Next: Analysis Rubric

Once you've taught the concepts, use the [analysis-rubric.md](../frameworks/analysis-rubric.md) 
to help learners evaluate code themselves.
