# Refactoring Priorities: What to Fix First

## What Is Refactoring Priority?

**Refactoring priority** is a framework for deciding which improvements to make first. Not all refactoring is equally valuable — some changes have high impact with low effort, while others require major work for minor gains.

> **Teaching angle**: Help learners understand trade-offs: "Why fix this now instead of that?" Prioritisation teaches decision-making, not just syntax.

---

## The Priority Matrix

**Impact** × **Effort** = **Priority**

```
High Impact,  ▄▄▄ URGENT    (Do first)
Low Effort    ███
              ▀▀▀

High Impact,  ▄▄▄ IMPORTANT (Do after urgent)
High Effort   ░░░
              ▀▀▀

Low Impact,   ▄▄▄ NICE-TO-HAVE (Do if time)
Low Effort    ░░░
              ▀▀▀

Low Impact,   ▄▄▄ DEFER    (Don't do)
High Effort   ░░░
              ▀▀▀
```

---

## The Priority Criteria

### Impact Factors

**High Impact if**:
- Fixes a bug that breaks functionality
- Makes code *significantly* clearer (reduces time for new readers by 50%+)
- Removes code duplication that affects 3+ places
- Improves performance by 10%+ or reduces resource use noticeably
- Enables a required feature that can't be added otherwise
- Addresses a code smell in a critical or frequently-used section

**Low Impact if**:
- Cosmetic change (style, comment rewording)
- Touches edge cases no one will hit
- Optimises a section that's 0.1% of runtime
- Affects code no one reads

### Effort Factors

**Low Effort if**:
- Change is mechanical (rename, extract function)
- Requires no external coordination
- Tests already exist (just refactor)
- Scope is small (<50 lines affected)
- No risk of regression

**High Effort if**:
- Requires significant restructuring
- Affects multiple modules or services
- Requires new external dependencies
- Needs extensive testing
- Touches legacy code with poor test coverage
- Risk of breaking existing clients

---

## Categorisation: Smells by Priority

### Category 1: URGENT (High Impact, Low Effort)

**Do these first.**

| Smell | Why Urgent | How to Fix |
|-------|-----------|-----------|
| **Misleading names** | Learners misunderstand intent immediately | Rename (1 line, high clarity gain) |
| **Obvious bugs** | Code doesn't work as intended | Fix the bug (clear impact) |
| **Unused parameters** | Confuses readers; suggests dead code | Remove (1 line, removes noise) |
| **Duplicated validation logic** | Maintenance risk across multiple places | Extract to shared function (low effort, prevents bugs) |
| **Missing error handling in critical path** | System crashes on recoverable errors | Add try/catch or validation (clear impact) |
| **Cryptic abbreviations** | Readers can't understand code | Expand to full names (1 line per variable) |

**Example**:
```python
# ✗ Urgent: Misleading name
def process_user(user):
    return user  # Does nothing; name suggests it does something

# ✓ Fixed (1 minute)
def validate_user_exists(user):
    return user  # Now the intent is clear
```

### Category 2: IMPORTANT (High Impact, High Effort)

**Do after urgent; plan these in sprints.**

| Smell | Why Important | How to Fix |
|-------|--------------|-----------|
| **Long functions (100+ lines)** | Hard to understand, test, change | Extract into smaller functions |
| **God objects** | Too many responsibilities | Split into smaller classes |
| **Deeply nested code (5+ levels)** | Very hard to follow; easy to introduce bugs | Refactor with guard clauses, extract helpers |
| **Scattered business logic** | Same logic in 5+ places | Consolidate into shared module |
| **Hidden dependencies** | Can't test; hard to reuse | Dependency inject; decouple |

**Example**:
```python
# ✗ Important: 200-line function, hard to test
def import_and_process_users(file_path, db, email_service):
    # Parsing, validation, DB operations, email sending all mixed

# ✓ Refactored: Separated concerns
def import_users(file_path) -> List[User]:
    # Just parsing and validation

def process_users(users, db) -> List[ProcessedUser]:
    # Just business logic

def send_notifications(users, email_service):
    # Just email sending
```

### Category 3: NICE-TO-HAVE (Low Impact, Low Effort)

**Do these if you have time; good learning opportunities.**

| Smell | Why Nice-to-Have | How to Fix |
|-------|-----------------|-----------|
| **Suboptimal variable names** | Slightly clearer; not blocking | Rename |
| **Unnecessary comments** | Reduce noise | Remove comments that restate code |
| **Minor inefficiencies** | 1% performance gain | Optimise |
| **Inconsistent formatting** | Slightly cleaner; not functional | Reformat |

**Example**:
```python
# Nice-to-have: Variable name could be clearer
result = [x for x in items if x > 5]

# After:
high_value_items = [item for item in items if item > 5]
```

### Category 4: DEFER (Low Impact, High Effort)

**Don't do these (unless they become IMPORTANT).**

| Smell | Why Defer | What to Do Instead |
|-------|----------|------------------|
| **Premature micro-optimisation** | 0.01% performance gain; code becomes cryptic | Measure first; optimise later if needed |
| **Rewriting in a "better" language** | Requires rewrite of entire system | Use current language; plan migration in future |
| **Gold-plating (over-engineering)** | Future flexibility that won't be needed | Keep it simple; refactor when requirements change |
| **Style consistency across entire codebase** | 1000s of lines to touch; low value | Use automated tools; refactor as you touch files |

---

## Prioritisation Framework: The Decision Tree

```
Does this block a required feature or fix a bug?
├─ YES → Do it (URGENT or IMPORTANT)
└─ NO → Continue...

Does this make code significantly clearer?
├─ YES → How much effort?
│   ├─ Low  → Do it (URGENT)
│   └─ High → Schedule it (IMPORTANT)
└─ NO → Continue...

Does this remove duplication in critical code?
├─ YES → How much effort?
│   ├─ Low  → Do it (URGENT)
│   └─ High → Schedule it (IMPORTANT)
└─ NO → Continue...

Does this improve performance or resource use by 10%+?
├─ YES → How much effort?
│   ├─ Low  → Do it (URGENT)
│   └─ High → Schedule it (IMPORTANT)
└─ NO → Continue...

Is this a learning opportunity with low risk?
├─ YES → Do it (NICE-TO-HAVE)
└─ NO → DEFER
```

---

## Real-World Example: Code Review Prioritisation

**Given this code:**

```python
def process_data(d):
    r = []
    for x in d:
        if x > 5:
            r.append(x * 2)
    return r

def process_data_v2(d):
    r = []
    for x in d:
        if x > 5:
            r.append(x * 2)
    return r
```

**Issues identified**:
1. ✗ Variable names (`d`, `r`, `x`)
2. ✗ Duplicated function
3. ✗ Could use list comprehension
4. ✗ Magic number (5)

**Prioritised refactoring**:

| Priority | Issue | Reasoning | Fix |
|----------|-------|-----------|-----|
| **1. URGENT** | Duplicated function | Maintenance risk; easy to fix | Delete `process_data_v2`, use `process_data` |
| **2. URGENT** | Vague names | High clarity gain, 1 minute | `d` → `values`, `r` → `results`, `x` → `value` |
| **3. NICE-TO-HAVE** | Magic number | Could extract constant | `THRESHOLD = 5` |
| **4. DEFER** | List comprehension | Not more readable for this case; premature micro-optimisation | Leave as-is |

**After prioritised fixes**:
```python
def process_data(values):
    """Return doubled values above threshold."""
    THRESHOLD = 5
    results = []
    for value in values:
        if value > THRESHOLD:
            results.append(value * 2)
    return results
```

---

## Teaching Prioritisation

When coaching on refactoring, frame it as decision-making:

**Instead of:** *"You should do X, Y, and Z to improve this code."*

**Say:**
> "Here are three improvements I see:
> 1. **Unclear names** (5 min, high clarity gain) — let's do this first
> 2. **Duplicated validation** (30 min, prevents bugs) — schedule this
> 3. **Could be more optimised** (2 hours, 1% performance gain) — defer unless it's a bottleneck
>
> Which should we tackle first?"

This teaches:
- Not all changes are equal
- Trade-offs matter
- Planning is part of engineering

---

## Prioritisation Checklist

For each refactoring opportunity:

- [ ] **What's the impact?** (Bug? Clarity? Performance? Duplication?)
- [ ] **How much is the impact?** (Blocks feature? 50% clarity gain? 2 places affected?)
- [ ] **What's the effort?** (10 min? 1 hour? 1 day?)
- [ ] **What's the risk?** (Tests exist? Affects many clients? Legacy code?)
- [ ] **Is there a requirement driving this?** (Product? Technical debt? Learning?)
- [ ] **Does it enable future work?** (If refactored, what becomes possible?)

---

## When to Ignore the Matrix

**Context matters.** Override the matrix if:

- **Technical debt is compounding** ("We keep tripping over this messy code")
- **Team morale** ("Let's make this code beautiful")
- **Learning is the goal** ("Let's practice refactoring")
- **Onboarding new team members** ("This confusing code slows everyone down")

In these cases, even DEFER items become URGENT.

---

## Next: Coaching Review Template

See [coaching-review-template.md](../templates/coaching-review-template.md) to structure your feedback using these priorities.
