# Deconstruction Model

## What is Deconstruction?

Deconstruction breaks code into **logical chunks** — units that serve a single purpose and can be understood independently before seeing how they fit together. This mirrors how learners actually process code: piece by piece, building understanding incrementally.

## Why Deconstruct?

- **Reduces cognitive load**: A learner can hold one function's logic in their head; a file is overwhelming
- **Surfaces intent**: Each chunk should have a clear "job" — if it doesn't, it's a smell
- **Enables teaching**: Explain one chunk well, then show how chunks connect
- **Reveals structure**: Messy dependencies and unclear responsibilities become visible

## The Deconstruction Hierarchy

Think of code as a **nested structure of concerns**:

```
Codebase
├── Module/Class (high-level concern: e.g., "User authentication")
│   ├── Function A (mid-level: e.g., "Validate credentials")
│   │   ├── Loop (tactical: e.g., "Check each field")
│   │   │   ├── Conditional (e.g., "If password is empty, error")
│   │   │   └── Side effect (e.g., "Log attempt")
│   │   └── Loop (e.g., "Format error messages")
│   └── Function B (mid-level: e.g., "Create session token")
└── Module/Class (high-level: e.g., "User data persistence")
```

At each level, ask: **"What is this chunk's single responsibility?"**

## Deconstruction Checklist

For a given code block (function, class, module), apply this checklist:

### Level 1: Identify Boundaries
- [ ] Where does this unit start and end?
- [ ] What are its inputs (parameters, state, external calls)?
- [ ] What are its outputs (return value, side effects, state changes)?
- [ ] Does it have a single, clear purpose?

### Level 2: Find the Chunks Within
- [ ] Are there distinct phases (setup, processing, cleanup)?
- [ ] Are there loops or conditionals that handle different cases?
- [ ] Are there state mutations (variables changing)?
- [ ] Are there side effects (I/O, logging, external calls)?
- [ ] Are there nested structures (loops within loops, if-else chains)?

### Level 3: Name Each Chunk
Use a **verb phrase** that describes the action:
- ✓ "Validate email format"
- ✓ "Fetch user from database"
- ✓ "Build response object"
- ✗ "Email" (noun, not action)
- ✗ "Processing" (too vague)
- ✗ "Do stuff" (not specific)

### Level 4: Remove Abstraction
Translate each chunk into human terms:
- "Memoization" → "Cache results to avoid recalculation"
- "Lazy loading" → "Only fetch data when needed"
- "Dependency injection" → "Let the caller decide where data comes from"
- "Higher-order function" → "A function that returns a customised function"

### Level 5: Check Relationships
- [ ] Does Chunk A depend on Chunk B?
- [ ] Is that dependency clear in the code (parameter passing, not implicit)?
- [ ] Could chunks be reordered or are they tightly coupled?
- [ ] Are there hidden dependencies (shared state, mutable references)?

## Examples

### Example 1: Simple Function

**Original code:**
```python
def process_user(data):
    user = User(data['name'], data['email'])
    if not validate_email(user.email):
        return None
    db.insert(user)
    return user
```

**Deconstructed:**
```
Chunk 1: Parse input
  - Extract name and email from dict
  - Create User object (just structure, no validation)

Chunk 2: Validate
  - Check email format
  - If invalid, stop and return None

Chunk 3: Persist
  - Write User to database
  - Return the User object
```

**Why this matters**: The learner can see three distinct operations. They can then ask:
- "What if validation fails? Do we create a User first or after?"
- "Why does validating happen after creating the User object?"
- "What happens if the database write fails?"

### Example 2: Loop with Conditional

**Original code:**
```javascript
for (let i = 0; i < items.length; i++) {
  if (items[i].active) {
    const result = fetch(items[i].url);
    console.log(result);
  }
}
```

**Deconstructed:**
```
Outer loop: Iterate through each item

  Chunk 1: Filter
    - Check if item is marked as active
    
  Chunk 2: Fetch data
    - Request data from the URL
    - Log the result (side effect: for debugging?)
```

**Coaching questions**:
- "Why log here? Is this for debugging or production?"
- "What if the fetch fails? Should we continue or stop?"
- "The name `items` is vague. What are they really?"
- "Could we separate the filtering and fetching into two steps?"

## Deconstruction Templates

### Template 1: Function-Level Deconstruction

```markdown
**Function**: [name]
**Purpose**: [one sentence]
**Inputs**: [parameters, state, external data]
**Outputs**: [return value, side effects]

**Chunks**:
1. **[Chunk name]** (lines X–Y)
   - What it does: [plain English]
   - Why: [reason it's here]
   - Concerns: [any smells or questions]

2. **[Chunk name]** (lines Y–Z)
   - What it does: [plain English]
   - Why: [reason it's here]
   - Concerns: [any smells or questions]
```

### Template 2: Class-Level Deconstruction

```markdown
**Class**: [name]
**Purpose**: [one sentence]
**Responsibility**: [what does it model or manage?]

**Public methods**:
- [method 1]: [one-liner purpose]
- [method 2]: [one-liner purpose]

**State** (instance variables):
- [variable 1]: [what it represents]
- [variable 2]: [what it represents]

**Dependencies**:
- [dependency 1]: [why needed]
- [dependency 2]: [why needed]
```

## Red Flags: When Deconstruction Fails

If you *can't* deconstruct a chunk, that's a smell:

| Flag | What it means | Example |
|------|---------------|---------|
| "This chunk does 3 things" | Single responsibility violated | A function that validates, fetches, and stores |
| "I don't know why this line is here" | Intent is unclear | Obscure logic with no comment |
| "It depends on 5 other chunks" | High coupling | Function needs half the codebase to work |
| "The inputs and outputs are all over the place" | Implicit dependencies | Uses global state, modifies caller's data |
| "I need to scroll up to see what this variable means" | Poor naming or scope | Loop variable `d` appears 10 lines later |

## Deconstruction as a Teaching Tool

When teaching, use deconstruction to answer:

1. **"Why is it structured this way?"**
   - Show how each chunk has a clear job
   - Explain why that order matters (e.g., validate before persist)

2. **"Where would I add a new feature?"**
   - Identify which chunk needs modification
   - Show what *wouldn't* need to change

3. **"Why is this hard to test?"**
   - Point to chunks with hidden dependencies
   - Explain how to untangle them

4. **"How do I explain this to someone else?"**
   - Start with the deconstruction, not the code
   - Build understanding chunk by chunk

## Next: Analysis Rubric

Once you've deconstructed code, use the [analysis-rubric.md](./analysis-rubric.md) to evaluate quality against best practices.
