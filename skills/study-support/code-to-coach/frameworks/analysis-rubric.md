# Analysis Rubric

## What is This Rubric?

A **criteria framework** for evaluating code quality in a coaching context. It moves beyond "does it work?" to "is it *maintainable*, *testable*, *clear*, and *efficient*?" — and more importantly, it explains *why each criterion matters* for a learner.

## How to Use This Rubric

For each deconstructed chunk, score it against each criterion:
- **✓ Excellent** — Exemplary; helps a learner understand best practice
- **◐ Adequate** — Acceptable; room for improvement but no blockers
- **✗ Needs work** — Has issues; impacts clarity, maintainability, or testability

Then ask: **"What's the teaching point here?"**

---

## Criterion 1: Clarity & Naming

### Question
Can a learner understand what this chunk does *without* reading the implementation?

### What to Evaluate
- **Function/variable names** are verb phrases (for functions) or noun phrases (for variables)
- **Names match intent** — a function called `process()` is too vague; `validateEmailFormat()` is clear
- **Abbreviations are defined** — `usr` vs `user`; `cfg` vs `config`
- **Comments explain why, not what** — "// Loop through items" is noise; "// Sort by priority so we process urgent items first" explains intent
- **No misleading names** — `getUser()` should not modify state; `tempVar` should not be permanent

### Teaching Frame
> Naming is the bridge between intent and implementation. A good name says "why we're doing this"; a bad name forces the reader to reverse-engineer intent from the code.

### Red Flags
- ✗ Single-letter variables outside of loops (e.g., `p = process()`)
- ✗ Names that don't match behaviour (e.g., `getUserIfActive()` that fetches all users)
- ✗ Magic numbers without context (e.g., `if (age > 18)` instead of `if (age > ADULT_AGE)`)
- ✗ Acronyms without explanation (e.g., `UWCS` without a comment)

### Refactoring Example

**Before:**
```python
def p(d):
    r = []
    for x in d:
        if x > 5:
            r.append(x * 2)
    return r
```

**After (with explanation):**
```python
def double_values_above_threshold(data):
    """Return all values from data that exceed 5, doubled.
    
    Used in report generation to emphasize significant items.
    """
    threshold = 5
    significant_values = []
    for value in data:
        if value > threshold:
            significant_values.append(value * 2)
    return significant_values
```

**Why it's better:**
- Learner can guess what the function does without reading code
- The variable names form a story: threshold → check → significant → return
- Comment explains *context* (report generation), not the obvious loop logic

---

## Criterion 2: Single Responsibility

### Question
Does this chunk have one clear job, or does it mix concerns?

### What to Evaluate
- **Does the chunk do one thing well?** (validation only, not validation + storage)
- **Is the "why" separated from the "how"?** (business logic separate from plumbing)
- **Could you extract sub-chunks into functions?** (if yes, maybe it's doing too much)
- **If renamed, would the name be accurate?** (if you need "and" in the name, split it)

### Teaching Frame
> A chunk with one responsibility is easier to test, reuse, and change. It's also easier to explain: "This function does X. Here's why X matters."

### Red Flags
- ✗ Function name has "and" in it (e.g., `validateAndSave()`)
- ✗ One function handles multiple error cases in different ways
- ✗ Chunks mix business logic with infrastructure concerns (e.g., validation + logging + database)
- ✗ State changes scattered throughout (variable modified in 5 different places)

### Refactoring Example

**Before:**
```javascript
function processUserSignup(email, password) {
  if (!email.includes('@')) return false;
  const hash = crypto.hash(password);
  const user = { email, hash, created: Date.now() };
  db.insert(user);
  sendWelcomeEmail(email);
  console.log(`User ${email} signed up`);
  return true;
}
```

**Deconstructed into separate responsibilities:**
```javascript
function validateEmail(email) {
  return email.includes('@');
}

function createUser(email, password) {
  const hash = crypto.hash(password);
  return { email, hash, created: Date.now() };
}

function processUserSignup(email, password) {
  if (!validateEmail(email)) return false;
  const user = createUser(email, password);
  db.insert(user);
  sendWelcomeEmail(email);
  return true;
}
```

**Why it's better:**
- Each function has one job (validate, create, or orchestrate)
- The orchestration function is now easier to test (you can swap out database or email)
- A learner can understand each part independently

---

## Criterion 3: Error Handling & Assumptions

### Question
Does the chunk handle failures gracefully, or does it assume the happy path?

### What to Evaluate
- **What can go wrong here?** (null input, network failure, permission denied, etc.)
- **Does the code handle these cases?** (or does it crash/silently fail?)
- **Are assumptions documented?** (e.g., "assumes email is already validated")
- **Are error messages helpful?** (or do they hide the real problem?)

### Teaching Frame
> Code that handles errors is code that's ready for the real world. A learner needs to know: what can break, and what happens then?

### Red Flags
- ✗ Unchecked array access (e.g., `items[0]` without checking length)
- ✗ Null/undefined not handled (especially in chained calls)
- ✗ Exceptions swallowed silently (e.g., `try { ... } catch (e) {}`)
- ✗ Assumptions not documented (e.g., function assumes input is pre-validated but doesn't check)

### Refactoring Example

**Before:**
```python
def get_user_age(user_id):
    user = db.query(f"SELECT * FROM users WHERE id={user_id}")
    return user['age']
```

**Concerns:**
- What if `user_id` is invalid? What if the user doesn't exist?
- What if the database query fails?
- What if `user['age']` is None?

**After (with error handling):**
```python
def get_user_age(user_id):
    """Retrieve user age by ID.
    
    Args:
        user_id: Must be a positive integer.
        
    Returns:
        Age in years, or None if user not found.
        
    Raises:
        ValueError: If user_id is invalid.
        DatabaseError: If query fails.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")
    
    try:
        user = db.query_by_id(user_id)  # parameterized, not string interpolation
    except DatabaseError as e:
        raise DatabaseError(f"Failed to fetch user {user_id}") from e
    
    if user is None:
        return None
    
    age = user.get('age')
    if age is None:
        raise ValueError(f"User {user_id} has no age set")
    
    return age
```

**Why it's better:**
- Learner can see all the ways this can fail
- Error messages tell you *what* went wrong and (sometimes) *why*
- The docstring sets expectations

---

## Criterion 4: Testability & Dependencies

### Question
Could a learner write a unit test for this chunk, or are there hidden dependencies?

### What to Evaluate
- **Does the chunk depend on external state?** (global variables, database, network)
- **Can you call it with sample inputs and predict outputs?** (or does it depend on setup/teardown?)
- **Are dependencies explicit (passed in) or implicit (hidden)?**
- **How many things would you need to mock to test this?** (1 is good; 5+ is a smell)

### Teaching Frame
> Testable code is code you understand. If you can't write a test without ten lines of setup, the chunk is probably too coupled.

### Red Flags
- ✗ Calls global functions or variables (e.g., `logger.log()` hidden from parameters)
- ✗ Creates dependencies internally (e.g., `db = Database()` inside the function)
- ✗ Side effects mixed with computation (e.g., modifies database and returns a value)
- ✗ No way to inject alternatives (can't test with fake database)

### Refactoring Example

**Before (hard to test):**
```python
def calculate_discount(cart):
    total = sum(item.price for item in cart)
    if total > 100:
        return total * 0.9  # 10% discount if over $100
    return total
```

**Problem**: You can test this, but what if business rules change? What if you need A/B testing?

**After (dependency injection):**
```python
def calculate_discount(cart, discount_rules):
    """Apply discount rules to cart total.
    
    Args:
        cart: List of items with price.
        discount_rules: Function that takes total and returns final price.
    
    Returns:
        Final price after discount.
    """
    total = sum(item.price for item in cart)
    return discount_rules(total)

# Now you can test with different rule sets:
def threshold_discount(threshold, rate):
    def apply(total):
        if total > threshold:
            return total * (1 - rate)
        return total
    return apply

# Test:
rules = threshold_discount(100, 0.1)
assert calculate_discount([Item(150)], rules) == 135.0
```

**Why it's better:**
- Learner can see: the function logic is separated from the rules
- You can test with any discount rule, not just hardcoded logic
- Adding new rules doesn't require changing the function

---

## Criterion 5: Cognitive Load

### Question
How much mental effort does it take to understand this chunk?

### What to Evaluate
- **Nesting depth** — how many levels of indentation? (>3 is often hard to follow)
- **Variable scope** — how many variables are in play at once?
- **State mutations** — how many times does state change? (more mutations = harder to trace)
- **Side effects** — does the chunk do I/O, logging, or other external effects?
- **Line length** — can you see a line on screen without scrolling? (>80–100 chars is risky)

### Teaching Frame
> Our brains can hold about 7 things in working memory at once. Code that respects that limit is code that's easier to understand, test, and change.

### Red Flags
- ✗ Nested loops within conditionals within more loops (nesting > 3)
- ✗ 10+ local variables in one function (hard to track what changes)
- ✗ A variable used, modified, used again in different ways (confusing trace)
- ✗ Long chains of method calls with side effects (e.g., `obj.method1().method2().method3()` where each has effects)

### Refactoring Example

**Before (high cognitive load):**
```javascript
function processData(data, config) {
  let result = [];
  for (let i = 0; i < data.length; i++) {
    if (data[i].active) {
      for (let j = 0; j < data[i].items.length; j++) {
        if (data[i].items[j].value > config.threshold) {
          let processed = transform(data[i].items[j]);
          if (processed.valid) {
            result.push(processed);
          } else {
            console.log(`Invalid: ${processed.error}`);
          }
        }
      }
    }
  }
  return result;
}
```

**Problems:**
- 4 levels of nesting (loop → if → loop → if)
- 6 variables (result, i, j, processed, config.threshold, processed.valid)
- Hard to trace: which items are included? What does "active" mean?

**After (lower cognitive load, clearer flow):**
```javascript
function processData(data, config) {
  return data
    .filter(user => user.active)
    .flatMap(user => user.items)
    .filter(item => item.value > config.threshold)
    .map(item => transform(item))
    .filter(processedItem => {
      if (!processedItem.valid) {
        console.log(`Invalid: ${processedItem.error}`);
        return false;
      }
      return true;
    });
}
```

**Why it's better:**
- Flat structure (no nested loops to hold in memory)
- Each step does one thing (filter, map, filter)
- Learner can read top-to-bottom: "Get active users, then their items, then filter by value, then transform, then remove invalid"

---

## Criterion 6: Performance & Resource Use

### Question
Does this chunk waste resources (CPU, memory, network), or is it efficient?

### What to Evaluate
- **Algorithmic efficiency** — O(n²) vs O(n)? Will it break at scale?
- **Memory allocation** — does it create huge temporary arrays?
- **I/O operations** — does it make one network call or ten?
- **Caching** — does it recompute when it could cache?
- **Is it premature optimisation?** — (optimised for performance that doesn't matter)

### Teaching Frame
> Performance matters, but so does clarity. A learner needs to know: what trade-off is acceptable here? When should we optimise, and when should we keep it simple?

### Red Flags
- ✗ O(n²) loop where O(n) is possible (especially common: nested loops fetching data)
- ✗ Creating a new object/array for every iteration (when one could be reused)
- ✗ Fetching the same data multiple times (when one fetch + cache would work)
- ✗ Optimising a bottleneck that's 0.01% of execution time

### Refactoring Example

**Before (inefficient):**
```python
def find_user_by_email(email, users):
    """O(n) search every time."""
    for user in users:
        if user.email == email:
            return user
    return None

# Called repeatedly in a loop:
for email in emails_to_check:
    user = find_user_by_email(email, users)  # O(n * m) overall
    process(user)
```

**After (efficient):**
```python
def build_email_index(users):
    """Pre-compute a dict for fast lookup. O(n) once, then O(1) per lookup."""
    return {user.email: user for user in users}

# Called once:
email_to_user = build_email_index(users)
for email in emails_to_check:
    user = email_to_user.get(email)  # O(1)
    process(user)
```

**Why it's better:**
- Overall complexity drops from O(n × m) to O(n + m)
- Learner sees the trade-off: a bit more setup code upfront, but much faster at scale
- The teaching point: "When you're doing repeated lookups, build an index first"

---

## How to Apply This Rubric

### Step 1: Score Each Criterion
For each chunk, give it a score:
- ✓ Excellent
- ◐ Adequate
- ✗ Needs work

### Step 2: Identify the Top Teaching Points
Pick the 1–3 most important issues. Prioritise:
1. Clarity & naming (if learners can't understand it, nothing else matters)
2. Single responsibility (if it does too much, it's hard to test and change)
3. Error handling (if it crashes, the code isn't production-ready)
4. Testability (if it's hard to test, it's probably over-coupled)

### Step 3: Frame It as Learning
Instead of "This is bad," try:
- "Here's what's hard to understand: the nested loops. Let's simplify it."
- "This function does 4 things. If we split it, each piece is easier to test."
- "If this fails, we don't know why. Let's add error handling so we can debug."

### Step 4: Suggest, Don't Demand
Provide alternatives with rationale:
- "Consider using a dict for lookups instead of a list. Here's why it matters at scale: ..."
- "One approach is to separate validation from storage. That makes each testable independently."

---

## Summary Table

| Criterion | Key Question | Why It Matters | Red Flags |
|-----------|--------------|----------------|-----------|
| **Clarity** | Can I understand the intent without reading code? | Reduces time to understand; aids maintenance | Vague names, magic numbers, no comments on why |
| **Single Responsibility** | Does this chunk do one thing? | Easier to test, reuse, change | "and" in the name; mixed concerns |
| **Error Handling** | What happens if it fails? | Code is robust and debuggable | Unchecked assumptions; swallowed exceptions |
| **Testability** | Can I write a unit test easily? | Code is decoupled and understandable | Hidden dependencies; globals; hard-to-mock I/O |
| **Cognitive Load** | How much mental effort to understand? | Reduces bugs, aids maintenance | Deep nesting; too many variables; long lines |
| **Performance** | Is it efficient at scale? | Avoids surprises in production | O(n²) where O(n) exists; repeated I/O; wasted memory |

---

## Next: Code Smells Reference

Use the [code-smells.md](../references/code-smells.md) to identify specific anti-patterns, then return here to refactor them.
