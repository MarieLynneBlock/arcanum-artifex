# Best Practices: Language-Agnostic Principles

## What Are "Best Practices"?

**Best practices** are design principles that, when applied consistently, make code easier to understand, maintain, test, and extend. They're not rules to memorise; they're *patterns* that solve common problems.

> **Teaching angle**: The same problems appear in every programming language and domain. Learning these patterns helps a learner recognise and solve them anywhere.

---

## Practice 1: Single Responsibility Principle (SRP)

### Principle
A function, class, or module should have one reason to change. It should do one thing well.

### Why It Matters
- Easier to test (one behaviour = one test)
- Easier to reuse (clear purpose)
- Easier to change (modifying one thing doesn't break another)

### How to Recognise It

**✗ Violation**: Function with multiple reasons to change
```python
def save_user_and_send_welcome_email(user_data):
    # Reason 1: User data structure changes
    user = User(user_data['name'], user_data['email'])
    db.insert(user)  # Reason 2: Database changes
    email_service.send(user)  # Reason 3: Email service changes
    log_event('user_created', user)  # Reason 4: Logging format changes
    return user
```

**✓ Follows SRP**: Each function has one reason to change
```python
def create_user(user_data):
    """Transform data into User object."""
    return User(user_data['name'], user_data['email'])

def save_user(user):
    """Persist user to database."""
    db.insert(user)

def send_welcome_email(user):
    """Send welcome message."""
    email_service.send(user)

def user_created(user):
    """Log user creation."""
    log_event('user_created', user)

# Orchestration:
def onboard_user(user_data):
    user = create_user(user_data)
    save_user(user)
    send_welcome_email(user)
    user_created(user)
    return user
```

### Teaching Tip
Ask: *"What would have to change to modify this code? If the answer is 'multiple things,' it's probably doing too much."*

---

## Practice 2: Don't Repeat Yourself (DRY)

### Principle
Every piece of knowledge should have a single, unambiguous representation. If logic appears twice, it belongs in one place.

### Why It Matters
- Changes are made once, not multiple places (fewer bugs)
- Reduces code size (easier to understand the full codebase)
- Encourages thinking about shared patterns

### How to Recognise It

**✗ Violation**: Same logic in two places
```python
def validate_user_email(email):
    return '@' in email and '.' in email.split('@')[1]

def validate_admin_email(email):
    return '@' in email and '.' in email.split('@')[1]
```

**✓ Follows DRY**: Logic once, reused everywhere
```python
def is_valid_email(email):
    """Check if email has valid format."""
    parts = email.split('@')
    return len(parts) == 2 and '.' in parts[1]

def validate_user_email(email):
    return is_valid_email(email)

def validate_admin_email(email):
    return is_valid_email(email)

# Even better: just use is_valid_email directly
```

### Teaching Tip
Ask: *"If I had to change this logic, how many places would I need to edit?"*

---

## Practice 3: Fail Fast, Fail Explicitly

### Principle
Check preconditions early. If something is wrong, raise an error immediately instead of letting bad state propagate.

### Why It Matters
- Bugs are caught close to their source (easier to debug)
- Errors are explicit (not hidden silent failures)
- Defensive: prevents downstream damage

### How to Recognise It

**✗ Violation**: Fails silently or far from the source
```python
def process_users(users):
    results = []
    for user in users:
        try:
            result = risky_operation(user)
            results.append(result)
        except:
            pass  # Silent failure
    return results  # Caller doesn't know some items failed
```

**✓ Follows "Fail Fast"**: Checks preconditions, raises on error
```python
def process_users(users):
    """Process all users; raise if any fails.
    
    Args:
        users: List of User objects.
        
    Raises:
        ValueError: If users is empty or None.
        ProcessingError: If any user fails to process.
    """
    if not users:
        raise ValueError("users list is empty")
    
    results = []
    for user in users:
        if not isinstance(user, User):
            raise ValueError(f"Expected User, got {type(user)}")
        result = risky_operation(user)  # Let exceptions propagate
        results.append(result)
    
    return results
```

### Teaching Tip
Ask: *"What assumptions is this code making? Which ones should be checked?"*

---

## Practice 4: Dependency Injection

### Principle
A function should receive its dependencies as parameters, not create them internally or use globals.

### Why It Matters
- Easier to test (use fake dependencies in tests)
- Easier to reuse (caller chooses the implementation)
- Easier to understand (dependencies are explicit in the signature)

### How to Recognise It

**✗ Violation**: Implicit, hard-wired dependencies
```javascript
function saveUser(user) {
    const db = new Database();  // Hard-wired dependency
    db.insert(user);
}
```

**✓ Follows DI**: Dependencies injected
```javascript
function saveUser(user, db) {
    db.insert(user);
}

// In production:
saveUser(user, productionDb);

// In tests:
saveUser(user, mockDb);
```

### Teaching Tip
Ask: *"To test this function, what would I have to set up? If the answer is complicated, it probably has hidden dependencies."*

---

## Practice 5: Don't Mix Concerns (Separation of Concerns)

### Principle
Keep business logic, I/O, configuration, and error handling separate.

### Why It Matters
- Each layer is testable independently
- Easier to change one layer without affecting others
- Clearer to understand what each layer does

### How to Recognise It

**✗ Violation**: Business logic mixed with I/O and configuration
```python
def calculate_user_discount(user_id):
    # I/O: fetch from database
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    
    # Business logic
    if user.subscription == 'premium':
        discount = 0.2
    else:
        discount = 0.1
    
    # More I/O: update database
    db.query(f"UPDATE users SET discount = {discount} WHERE id = {user_id}")
    
    # I/O: logging
    logger.log(f"Calculated discount {discount} for user {user_id}")
    
    return discount
```

**✓ Follows SoC**: Each concern separate
```python
def calculate_discount(subscription_level):
    """Pure business logic, no I/O."""
    discount_map = {
        'premium': 0.2,
        'standard': 0.1,
    }
    return discount_map.get(subscription_level, 0)

class UserDiscountService:
    """Orchestrates business logic and I/O."""
    def __init__(self, user_repo, logger):
        self.user_repo = user_repo
        self.logger = logger
    
    def apply_discount(self, user_id):
        user = self.user_repo.get(user_id)
        discount = calculate_discount(user.subscription_level)
        user.discount = discount
        self.user_repo.save(user)
        self.logger.log(f"Applied discount {discount} to user {user_id}")
        return discount
```

### Teaching Tip
Ask: *"What would I have to do to test the business logic without touching the database?"*

---

## Practice 6: Name Things Well

### Principle
Names should reveal intent. A name should answer: "What is this?" or "What does it do?"

### Why It Matters
- Code is read far more than it's written
- Good names make code self-documenting
- Poor names hide intent, forcing readers to reverse-engineer it

### How to Recognise It

**✗ Violation**: Names hide intent
```python
def p(d):
    r = []
    for x in d:
        if x > 5:
            r.append(x)
    return r

u = User('alice@example.com')
u_data = {'a': 'Alice', 'e': 'alice@example.com', 'r': 'admin'}
```

**✓ Follows naming principle**: Names reveal intent
```python
def high_value_scores(scores):
    """Return all scores above the minimum threshold."""
    min_threshold = 5
    significant_scores = []
    for score in scores:
        if score > min_threshold:
            significant_scores.append(score)
    return significant_scores

admin_user = User('alice@example.com')
admin_profile = {
    'name': 'Alice',
    'email': 'alice@example.com',
    'role': 'admin'
}
```

### Naming Guidelines

| Category | Pattern | Examples |
|----------|---------|----------|
| **Functions** | Start with verb; describe action | `validate_email()`, `fetch_user()`, `calculate_total()` |
| **Variables/fields** | Noun; describe what it holds | `email_address`, `total_price`, `user_count` |
| **Booleans** | Answer a yes/no question | `is_active`, `has_errors`, `can_delete` |
| **Constants** | UPPERCASE; describe value | `MAX_RETRIES`, `DEFAULT_TIMEOUT_MS` |
| **Classes** | Noun; describe what it models | `User`, `EmailValidator`, `DatabaseConnection` |

---

## Practice 7: Document Why, Not What

### Principle
Comments should explain *why* a decision was made, not what the code does. The code itself shows what; comments explain why.

### Why It Matters
- Comments that explain what get out of sync with code
- Comments that explain why help future maintainers understand trade-offs
- Reduces time to understand design decisions

### How to Recognise It

**✗ Violation**: Comments explain what
```python
# Add 1 to counter
counter = counter + 1

# Check if user is over 18
if user.age > 18:
    proceed()
```

**✓ Follows documentation principle**: Comments explain why
```python
counter = counter + 1  # [No comment needed; it's clear]

# Users must be 18+ per legal requirement (see issue #4567)
if user.age > 18:
    proceed()
```

### Teaching Tip
Ask: *"Would a comment help someone understand *why* this code exists? Or does the code itself answer that?"*

---

## Practice 8: Prefer Immutability

### Principle
Avoid changing state. Prefer creating new objects over modifying existing ones.

### Why It Matters
- Easier to reason about (state doesn't unexpectedly change)
- Easier to test (no need to reset state between tests)
- Easier to debug (history is preserved)
- Thread-safe (no race conditions over state)

### How to Recognise It

**✗ Violation**: Heavy mutation
```python
def apply_discount(user):
    user.discount = 0.2  # Mutation
    user.updated_at = datetime.now()  # Mutation
    return user
```

**✓ Follows immutability**: New object returned
```python
def apply_discount(user, discount_rate):
    """Return a new user object with discount applied."""
    return User(
        name=user.name,
        email=user.email,
        discount=discount_rate,
        updated_at=datetime.now()
    )
```

### Teaching Tip
Ask: *"If I call this function twice, will the input change? If yes, is that the only way to achieve the goal?"*

---

## Practice 9: Composition Over Inheritance

### Principle
Build complex behaviour by combining simple objects (composition) rather than creating deep inheritance hierarchies.

### Why It Matters
- Inheritance hierarchies become brittle and hard to change
- Composition is more flexible (easier to combine and recombine)
- Easier to understand (clear relationships between objects)

### How to Recognise It

**✗ Violation**: Deep inheritance
```python
class Animal:
    def move(self): pass

class Dog(Animal):
    def move(self): print("Run")

class ServiceDog(Dog):
    def move(self): print("Run to owner")
    def assist(self): print("Help owner")

class GuideDog(ServiceDog):
    def move(self): print("Run carefully")
```

**✓ Follows composition**: Simple objects combined
```python
class Dog:
    def move(self): print("Run")

class Trainer:
    def __init__(self, dog):
        self.dog = dog
    
    def assist(self): print(f"{self.dog} helps owner")

class GuideTrainer(Trainer):
    def assist(self): print(f"{self.dog} guides owner safely")

# Usage:
my_dog = Dog()
my_service_dog = GuideTrainer(my_dog)
```

---

## Practice 10: Make Invalid States Unrepresentable

### Principle
Design your data structures so that invalid states are impossible to represent.

### Why It Matters
- Prevents bugs caused by invalid data
- Forces validation early (not deep in the code)
- Makes the code self-documenting (the structure shows what's valid)

### How to Recognise It

**✗ Violation**: Invalid state possible
```python
class User:
    def __init__(self, email, verified=False, verification_token=None):
        self.email = email
        self.verified = verified
        self.verification_token = verification_token
    
    # Invalid state: verified=True but token is None
    # Code has to check and handle this everywhere
```

**✓ Follows principle**: Invalid state impossible
```python
class UnverifiedUser:
    def __init__(self, email, token):
        self.email = email
        self.token = token

class VerifiedUser:
    def __init__(self, email):
        self.email = email
    
    # A VerifiedUser has no token; verified=True is implicit
    # Invalid state is impossible

# Usage:
unverified = UnverifiedUser('alice@example.com', token='xyz')
verified = unverified.verify_with_token('xyz')  # Returns VerifiedUser
```

---

## Practice 11: Premature Optimisation Is the Root of All Evil

### Principle
Optimise for clarity first. Only optimise for performance when you've measured and found a real bottleneck.

### Why It Matters
- Optimised code is often harder to understand
- Premature optimisation wastes time on non-bottlenecks
- Measurable problems are easier to solve

### How to Recognise It

**✗ Violation**: Optimising prematurely
```python
# Optimised for speed, but is it a bottleneck?
def get_user(user_id):
    # Caches aggressively, but what if users change?
    if user_id in _cache:
        return _cache[user_id]
    # ...
```

**✓ Follows principle**: Optimise for clarity, measure bottlenecks
```python
def get_user(user_id):
    """Get user by ID."""
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    if not user:
        raise UserNotFoundError(user_id)
    return user

# Later, if profiling shows this is slow, *then* add caching
```

---

## Practice 12: Explicit Is Better Than Implicit

### Principle
Make assumptions and side effects visible. Avoid hidden magic.

### Why It Matters
- Code is easier to understand and debug
- Prevents surprise behaviour
- Makes the cost of operations clear

### How to Recognise It

**✗ Violation**: Implicit behaviour
```python
# What does save() do? Validate? Persist? Log? Unclear.
user.save()

# Is this modifying user? Or creating a copy? Unclear.
updated = apply_discount(user, 0.2)
```

**✓ Follows principle**: Explicit behaviour
```python
# Clear what each step does
validated_user = validate_user(user)
saved_user = db.save(validated_user)
logged_user = logger.log_save_event(saved_user)

# Clear if modifying or copying
updated_user = User(
    name=user.name,
    email=user.email,
    discount=0.2
)
```

---

## Quick Reference: Principles and Their Benefits

| Principle | Helps With | Key Benefit |
|-----------|-----------|------------|
| SRP | Testing, reusability | One reason to change |
| DRY | Maintenance | Changes in one place |
| Fail Fast | Debugging | Errors near source |
| DI | Testing, reusability | Explicit dependencies |
| SoC | Testing, clarity | Each layer independent |
| Good Naming | Reading, understanding | Intent visible |
| Document Why | Maintainability | Design decisions preserved |
| Immutability | Reasoning, debugging | State predictable |
| Composition | Flexibility | Easy to combine |
| Invalid States | Preventing bugs | Structure enforces validity |
| Measure Before Optimising | Time, clarity | Optimise real bottlenecks |
| Explicit | Debugging, clarity | No hidden magic |

---

## Teaching Best Practices

When introducing a principle, don't lecture. Instead:

1. **Show the smell**: Point out what's hard to understand or maintain
2. **Explain the cost**: "This makes testing hard because…"
3. **Show the refactoring**: Demonstrate the principle in action
4. **Link to examples**: "You see this pattern in most production code"
5. **Practice**: Have them identify where the principle applies in real code

---

## Next: Cognitive Load

See [cognitive-load.md](./cognitive-load.md) for practical strategies to reduce mental friction in code.
