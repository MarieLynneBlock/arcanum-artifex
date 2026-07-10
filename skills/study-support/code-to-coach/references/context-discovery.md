# Context Discovery: Questions to Orient Yourself

## What Is Context Discovery?

**Context discovery** is the process of understanding a piece of code's *purpose, constraints, and history* before analysing it. You need context to coach effectively — otherwise, you're just describing syntax.

---

## The Context Discovery Questions

### About Purpose

- **What is this code's job?** (What problem does it solve?)
- **Who calls it?** (Callers? Tests? External systems?)
- **What's the business domain?** (Is it billing? Authentication? Analytics?)
- **Why does this code exist?** (New feature? Bug fix? Performance improvement?)

### About Scope

- **What are the inputs?** (Parameters, state, external data?)
- **What are the outputs?** (Return value, side effects, mutations?)
- **What can it not do?** (Explicitly out of scope?)
- **What are the assumptions?** (What must be true for this code to work?)

### About Constraints

- **What are the performance requirements?** (Must be fast? Memory-constrained?)
- **What are the failure modes?** (What can go wrong? How critical?)
- **What are the maintenance constraints?** (Legacy system? Active development?)
- **What's the organisational context?** (Startup vs enterprise? Stable vs fast-moving team?)

### About History

- **When was this written?** (Recent? Legacy?)
- **What's changed recently?** (New refactoring? Recent bug fixes?)
- **What's the team's experience?** (Senior developers? Learning team?)
- **Are there known issues or TODOs?** (Incomplete? Deferred work?)

---

## How to Discover Context

### From the Code Itself

**Look for clues**:
- **Docstrings/comments**: Explain intent, constraints, or history
- **Test files**: Show how the code is used and what it should do
- **Error handling**: Reveals what can go wrong
- **Naming**: Reveals domain language and assumptions
- **Version control history**: Shows changes over time (git blame, git log)

**Example**:
```python
def validate_email(email):
    """Check if email is valid format per RFC 5322.
    
    Note: This is a simplified check. For full compliance,
    use an external library. See issue #1234.
    
    Args:
        email: String to check.
    
    Returns:
        True if valid, False otherwise.
    """
    # Quick heuristic; not guaranteed correct
    return '@' in email and '.' in email.split('@')[1]
```

**Context clues**:
- "Simplified check" → not production-grade; acceptable trade-off
- "RFC 5322" → formal specification; can look up requirements
- "See issue #1234" → known limitation; deferred work
- "Not guaranteed correct" → understands limitations

### From Tests

**Good tests reveal**:
- What the code is supposed to do (test name)
- What inputs are valid (happy path tests)
- What inputs are invalid (error cases)
- What edge cases matter (boundary tests)

**Example**:
```python
def test_validate_email_accepts_valid():
    assert validate_email('alice@example.com') == True

def test_validate_email_rejects_no_at():
    assert validate_email('alice.example.com') == False

def test_validate_email_rejects_no_domain():
    assert validate_email('alice@') == False

def test_validate_email_accepts_subdomain():
    assert validate_email('alice@mail.example.com') == True
```

**Context clues**:
- The function accepts standard emails, subdomains
- It rejects emails without `@` or domain
- The test author cared about these specific cases

### From Related Code

**Look at**:
- **Callers**: How is this code used? What do they expect?
- **Dependencies**: What does this code depend on? Why?
- **Similar code**: Are there similar functions? What pattern do they follow?

### From Documentation

**Check**:
- **README**: What does the module/system do?
- **Architecture docs**: How does this fit into the larger system?
- **API docs**: What's the public contract?
- **Design docs**: Why were decisions made?

---

## Questions to Ask the Code Author (or Colleague)

If you're stuck, ask:

1. **"What was the trigger for creating this code?"** (Feature request? Bug fix? Performance issue?)
2. **"What are the top 3 things this code must do?"**
3. **"What's the most confusing part to new readers?"**
4. **"What would break if we changed [specific part]?"**
5. **"What would you change if you rewrote this today?"**
6. **"Are there edge cases I should know about?"**
7. **"Is this code actively maintained or legacy?"**

---

## Context Discovery Template

Use this template when orienting yourself to new code:

```markdown
## Code: [Function/Class name]

### Purpose
- **What**: [One sentence on what this does]
- **Why**: [What problem does it solve? Why is it needed?]
- **Who uses it**: [Callers, external systems, tests]

### Scope
- **Inputs**: [Parameters, state, dependencies]
- **Outputs**: [Return value, side effects, mutations]
- **Out of scope**: [What it doesn't do]

### Constraints
- **Performance**: [Speed, memory, throughput requirements]
- **Reliability**: [Failure modes, error handling]
- **Maintenance**: [Active? Legacy? Experimental?]

### History
- **Created**: [When and why?]
- **Changes**: [Recent refactors? Known issues?]
- **Tech debt**: [TODOs, deferred work, known limitations]

### Key Takeaways
- [1–3 most important things to understand]

### Questions for Author
- [List questions if context is unclear]
```

---

## Red Flags: Context is Missing

- [ ] No docstring or comments explaining intent
- [ ] No tests (unclear what it should do)
- [ ] Vague function names (what is `process()` really doing?)
- [ ] No indication of performance requirements
- [ ] No version control history (or file is brand new)
- [ ] Code looks defensive but no explanation why

---

## Context-Driven Coaching

Once you have context, you can coach effectively:

**With context**, you can say:
> "This function validates email against a simplified RFC 5322 heuristic (not full compliance). The trade-off is speed for correctness. If we need full compliance, we'd use a library. For now, this is an intentional choice."

**Without context**, you might say:
> "This validation is incorrect. It doesn't handle all edge cases."

The first respects the design decision; the second misses the context.

---

## Next: Deconstruction and Analysis

Once you understand the context, use the [deconstruction-model.md](../frameworks/deconstruction-model.md) to break the code into teachable chunks.
