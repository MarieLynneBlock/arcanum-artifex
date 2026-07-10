# Code Smells: Anti-Patterns and Their Signals

## What Is a Code Smell?

A **code smell** is a surface-level indicator that something might be wrong beneath the surface. It's not a bug (the code might work), but a symptom suggesting the code needs refactoring or reconsideration.

> **Teaching angle**: Code smells are like a doctor's symptoms. A fever doesn't tell you *what's* wrong, but it tells you to investigate. A code smell doesn't say "delete this," but "think about why this is here."

---

## Smell 1: Long Functions

**Signal**: A function is longer than 20–30 lines.

**Why it's a smell**:
- Hard to understand the whole function at once (cognitive overload)
- Hard to test (probably does multiple things)
- Hard to reuse (tied together with other logic)
- Hard to change (modifying one part risks breaking another)

**Questions to ask**:
- Can I split this into smaller functions, each with one job?
- Are there phases (setup, process, cleanup) that should be separate?
- Are there loops handling different concerns?

**Example**:

```python
# ✗ 50-line function
def import_users(file_path):
    with open(file_path) as f:
        lines = f.readlines()
    
    users = []
    errors = []
    
    for i, line in enumerate(lines):
        if line.startswith('#'):
            continue
        
        parts = line.split(',')
        if len(parts) < 3:
            errors.append(f"Line {i}: insufficient columns")
            continue
        
        name, email, role = parts[0], parts[1], parts[2]
        
        if not email.count('@') == 1:
            errors.append(f"Line {i}: invalid email")
            continue
        
        if role not in ['admin', 'user', 'guest']:
            errors.append(f"Line {i}: invalid role")
            continue
        
        if any(u.email == email for u in users):
            errors.append(f"Line {i}: duplicate email")
            continue
        
        user = User(name=name, email=email, role=role)
        users.append(user)
    
    if errors:
        print("Import failed:")
        for error in errors:
            print(f"  {error}")
        return None
    
    for user in users:
        db.insert(user)
    
    return users
```

**Refactored (breaking into chunks)**:

```python
def import_users(file_path):
    """High-level orchestration."""
    lines = read_file(file_path)
    records = parse_records(lines)
    users, errors = validate_records(records)
    
    if errors:
        report_errors(errors)
        return None
    
    save_users(users)
    return users

def parse_records(lines):
    """Extract raw data."""
    records = []
    for i, line in enumerate(lines):
        if line.startswith('#'):
            continue
        record = line.split(',')
        if len(record) >= 3:
            records.append((i, record[:3]))
    return records

def validate_records(records):
    """Check each record against rules."""
    users = []
    errors = []
    seen_emails = set()
    
    for line_no, (name, email, role) in records:
        error = validate_user(name, email, role, seen_emails)
        if error:
            errors.append(f"Line {line_no}: {error}")
        else:
            users.append(User(name=name, email=email, role=role))
            seen_emails.add(email)
    
    return users, errors

def validate_user(name, email, role, seen_emails):
    """Check one user; return error or None."""
    if not email.count('@') == 1:
        return "invalid email"
    if role not in ['admin', 'user', 'guest']:
        return "invalid role"
    if email in seen_emails:
        return "duplicate email"
    return None
```

**Why it's better**:
- Main function shows the flow at a glance
- Each sub-function has one job and is testable
- Learner can understand one piece without holding the whole file in mind

---

## Smell 2: Deeply Nested Conditionals

**Signal**: Code has 4+ levels of indentation; `if` inside `for` inside `if` inside `for`.

**Why it's a smell**:
- Cognitive overload; hard to trace which branch you're on
- Easy to introduce bugs (missing a case, wrong nesting)
- Hard to test (need many combinations of conditions)

**Questions to ask**:
- Can I extract the inner logic into a helper function?
- Can I invert conditions (return early) to reduce nesting?
- Are there distinct phases that should be separate?

**Example**:

```javascript
// ✗ Deep nesting
function process(users) {
  for (let user of users) {
    if (user.active) {
      if (user.verified) {
        for (let item of user.items) {
          if (item.valid) {
            if (item.priority > 5) {
              console.log(item);
            }
          }
        }
      }
    }
  }
}
```

**Refactored (early return + helper functions)**:

```javascript
function process(users) {
  return users
    .filter(user => user.active && user.verified)
    .flatMap(user => user.items)
    .filter(item => item.valid && item.priority > 5)
    .forEach(item => console.log(item));
}
```

---

## Smell 3: Magic Numbers

**Signal**: Numbers appear in code without explanation (e.g., `if (age > 18)`, `timeout = 5000`).

**Why it's a smell**:
- The "why" is hidden; a learner doesn't know the intent
- Hard to change; if you need to update the number, do you update it everywhere?
- Easy to copy the number wrong (`5000` vs `50000`)

**Questions to ask**:
- What does this number represent? (age threshold, timeout, retry limit?)
- Where else is this number used?
- Should it be a named constant or a configuration parameter?

**Example**:

```python
# ✗ Magic numbers
if user.age > 18:
    discount = price * 0.85
if response_time > 2000:
    log_warning()
```

**Refactored**:

```python
ADULT_AGE = 18
SENIOR_DISCOUNT_RATE = 0.85
RESPONSE_TIME_WARNING_THRESHOLD_MS = 2000

if user.age >= ADULT_AGE:
    discount = price * (1 - SENIOR_DISCOUNT_RATE)
if response_time > RESPONSE_TIME_WARNING_THRESHOLD_MS:
    log_warning()
```

---

## Smell 4: Duplicate Code

**Signal**: The same logic appears in 2+ places.

**Why it's a smell**:
- Violates DRY (Don't Repeat Yourself)
- When you fix a bug in one place, you might forget the other
- Maintenance burden (more places to change)

**Questions to ask**:
- Can I extract this into a shared function?
- If they look similar but are used differently, are they *really* the same?
- Why was this duplicated? (Accidentally? Different team? Didn't know it existed?)

**Example**:

```python
# ✗ Duplicated validation
def create_user(email, password):
    if not email.count('@') == 1:
        return None
    # ... rest ...

def update_user(user_id, email, password):
    if not email.count('@') == 1:
        return None
    # ... rest ...
```

**Refactored**:

```python
def is_valid_email(email):
    return email.count('@') == 1

def create_user(email, password):
    if not is_valid_email(email):
        return None
    # ... rest ...

def update_user(user_id, email, password):
    if not is_valid_email(email):
        return None
    # ... rest ...
```

---

## Smell 5: Unclear Variable Names

**Signal**: Variables are named `x`, `temp`, `data`, `result`, `obj`.

**Why it's a smell**:
- Intent is hidden; a learner must reverse-engineer what it means
- Easy to misuse (use it for the wrong purpose)
- Encourages the author to think vaguely ("just store it in x")

**Questions to ask**:
- What does this variable represent in the business domain?
- What is its role in this function?
- If I renamed it to something specific, would the code be clearer?

**Example**:

```python
# ✗ Vague names
def calc(data):
    r = []
    for x in data:
        if x > 10:
            r.append(x * 2)
    return r
```

**Refactored**:

```python
def double_significant_values(values, threshold=10):
    """Return all values above threshold, doubled."""
    significant_values = []
    for value in values:
        if value > threshold:
            significant_values.append(value * 2)
    return significant_values
```

---

## Smell 6: Hidden Dependencies

**Signal**: A function depends on global state, external services, or implicit preconditions.

**Why it's a smell**:
- Hard to test (can't control the dependencies)
- Hard to understand (the dependencies are invisible in the signature)
- Hard to reuse (locked into specific implementations)

**Questions to ask**:
- What does this function depend on? (database? network? time?)
- Are these dependencies explicit (parameters) or implicit (globals)?
- Could I pass the dependencies in instead?

**Example**:

```python
# ✗ Hidden dependency on global database
def get_user_posts(user_id):
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    posts = db.query(f"SELECT * FROM posts WHERE user_id = {user_id}")
    return {user: user, posts: posts}
```

**Refactored**:

```python
def get_user_posts(user_id, user_repo, post_repo):
    """Fetch user and posts; dependencies injected."""
    user = user_repo.get(user_id)
    posts = post_repo.get_by_user(user_id)
    return {user: user, posts: posts}

# In tests:
user_posts = get_user_posts(123, mock_user_repo, mock_post_repo)
```

---

## Smell 7: Inconsistent Error Handling

**Signal**: Some code paths handle errors gracefully, others crash; some catch exceptions, others let them propagate.

**Why it's a smell**:
- Unpredictable behaviour; unclear what's recoverable vs fatal
- Inconsistent developer experience (some calls need try/catch, others don't)
- Hard to debug (errors might be silently swallowed)

**Questions to ask**:
- What are *all* the ways this can fail?
- Which failures are recoverable, which are fatal?
- Are errors visible to the caller (raised) or hidden (caught and logged)?

**Example**:

```python
# ✗ Inconsistent error handling
def process_file(filename):
    try:
        with open(filename) as f:
            data = json.load(f)  # Can raise ValueError
    except:
        return None  # Silently fails
    
    for item in data:  # Assumes data is iterable
        result = risky_operation(item)  # Might raise
        if result:
            return result
    
    return []
```

**Refactored**:

```python
def process_file(filename):
    """Process JSON file; raise on error, return empty if no results.
    
    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If file isn't valid JSON.
    """
    with open(filename) as f:  # Raises FileNotFoundError
        data = json.load(f)  # Raises ValueError
    
    if not isinstance(data, list):
        raise ValueError(f"Expected list, got {type(data)}")
    
    for item in data:
        try:
            result = risky_operation(item)
        except RiskyOperationError as e:
            log_error(f"Skipping item: {e}")
            continue
        
        if result:
            return result
    
    return []
```

---

## Smell 8: Tight Coupling

**Signal**: A function is hard to test because it depends on other modules; changing one module breaks another.

**Why it's a smell**:
- Changes ripple through the codebase (changing A breaks B and C)
- Hard to test in isolation
- Hard to reuse (locked into specific implementations)

**Questions to ask**:
- What does this depend on directly?
- Can I replace those dependencies with interfaces or abstractions?
- If I made a fake version, could I test this function independently?

---

## Smell 9: Comments Explaining Obvious Code

**Signal**: Comments explain what the code does, not why (e.g., `i = i + 1 # increment i`).

**Why it's a smell**:
- Noise; clutters the code without adding insight
- Easy to get out of sync (comment says one thing, code does another)
- Suggests the code is too complex and needs better naming

**Questions to ask**:
- Does this comment explain *what* the code does (it should be code, not a comment)?
- Or does it explain *why* (good comment)?
- Could better naming replace the comment?

**Example**:

```python
# ✗ Obvious comment
def calculate_total(items):
    total = 0  # Initialize total
    for item in items:
        total = total + item.price  # Add price to total
    return total  # Return total

# ✓ Better: just the code (it's clear)
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item.price
    return total

# ✓ Or with a comment explaining *why*:
def calculate_total(items):
    # Iterative sum instead of sum() for compatibility with legacy systems
    total = 0
    for item in items:
        total = total + item.price
    return total
```

---

## Smell 10: God Objects

**Signal**: A class has many methods, handles many concerns, or is hard to name.

**Why it's a smell**:
- Violates single responsibility
- Hard to test (many dependencies, many behaviours)
- Hard to understand (too many moving parts)

**Questions to ask**:
- What is this class's *one* job?
- Can I split it into smaller classes, each with a clear purpose?
- If the name has "and" in it (`UserAndPostManager`), it's probably too big

**Example**:

```python
# ✗ God object
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def validate(self):
        # Validates email
        pass
    
    def send_email(self):
        # Sends email to user
        pass
    
    def save_to_database(self):
        # Persists to DB
        pass
    
    def generate_report(self):
        # Generates a report for this user
        pass
    
    def calculate_statistics(self):
        # Calculates user statistics
        pass
```

**Refactored**:

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class EmailValidator:
    def validate(self, email):
        # Just validation logic
        pass

class EmailService:
    def send(self, user):
        # Just sending
        pass

class UserRepository:
    def save(self, user):
        # Just persistence
        pass

class UserReporter:
    def generate_report(self, user):
        # Just reporting
        pass
```

---

## Quick Reference: Smell → Refactoring

| Smell | Refactoring Strategy |
|-------|----------------------|
| Long function | Extract sub-functions |
| Deep nesting | Invert conditions, use early returns |
| Magic numbers | Define named constants |
| Duplicate code | Extract shared function |
| Unclear names | Rename to specific, business-domain terms |
| Hidden dependencies | Inject dependencies as parameters |
| Inconsistent errors | Standardise: explicit errors, clear recovery paths |
| Tight coupling | Use abstractions, dependency injection |
| Obvious comments | Improve naming, keep strategic comments |
| God object | Split into smaller classes with clear roles |

---

## Teaching Smells vs. Fixing Them

As a coach, don't say: *"This is a long function, refactor it."*

Instead, say: *"This function does 4 things. Let's think about how to teach it:*
1. *First, show the high-level flow?*
2. *Then, explain each step separately?*
3. *A learner could understand it better if each step was its own function. Want to try?"*

The smell is the *entry point*; the teaching is the *work*.

---

## Next: Best Practices

See [best-practices.md](./best-practices.md) for language-agnostic principles to apply when refactoring.
