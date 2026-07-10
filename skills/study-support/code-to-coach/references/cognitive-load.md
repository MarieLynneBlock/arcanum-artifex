# Cognitive Load: Making Code Easy to Understand

## What Is Cognitive Load?

**Cognitive load** is the amount of mental effort required to understand code. High cognitive load means a learner has to hold many concepts in mind at once; low cognitive load means understanding flows naturally.

> **Teaching angle**: Our brains can hold about 7 things in working memory. Code that respects that limit is code that's easy to understand and debug.

---

## The Three Types of Cognitive Load

### 1. Intrinsic Load
The inherent complexity of the problem. *You can't reduce this* — some problems are just complex.

**Example**: Calculating compound interest is intrinsically complex (multiple steps, formula). There's no way to make it simple.

**What you can do**: Break it into smaller steps, explain each step independently.

### 2. Extraneous Load
Mental effort wasted on understanding the code itself, not the problem. *This you can reduce.*

**Examples**:
- Unclear variable names (`x` instead of `price`)
- Deep nesting (4 levels of `if` inside `for`)
- Scattered logic (validation in one place, the check in another)
- Inconsistent style (sometimes `camelCase`, sometimes `snake_case`)

### 3. Germane Load
Mental effort spent understanding the *relationships* between concepts — how parts fit together. *This you want to encourage.*

**Examples**:
- "First we validate, then we persist"
- "This class manages the lifecycle; these methods handle state transitions"
- "Each module solves one problem; they communicate via interfaces"

---

## Strategies to Reduce Cognitive Load

### Strategy 1: Limit Nesting Depth

**Principle**: Avoid code with 4+ levels of indentation.

**Why**: Each level of nesting adds a mental "stack" the reader has to maintain.

**Examples**:

**✗ High load (5 levels)**:
```javascript
for (let user of users) {
  if (user.active) {
    for (let order of user.orders) {
      if (order.status === 'pending') {
        for (let item of order.items) {
          if (item.quantity > 0) {
            processItem(item);
          }
        }
      }
    }
  }
}
```

**✓ Lower load (1 level)**:
```javascript
const activeUsers = users.filter(u => u.active);
const pendingOrders = activeUsers
  .flatMap(u => u.orders.filter(o => o.status === 'pending'));
const itemsToProcess = pendingOrders
  .flatMap(o => o.items.filter(i => i.quantity > 0));
itemsToProcess.forEach(processItem);
```

**Technique**: Use filtering, mapping, and extraction rather than nested loops.

---

### Strategy 2: Minimise Mutable State

**Principle**: Reduce the number of variables that change, and reduce how often they change.

**Why**: Tracking state changes requires mental energy. Each mutation is another thing to remember.

**Examples**:

**✗ High load (many mutations)**:
```python
result = []
for i, item in enumerate(items):
    value = item.value  # State 1
    if value > 10:
        value = value * 2  # State 2
        if value < 100:
            value = value + 1  # State 3
            result.append(value)  # State 4
return result
```

**✓ Lower load (immutable flow)**:
```python
return [
    item.value * 2 + 1
    for item in items
    if 10 < item.value * 2 < 100
]
```

**Technique**: Use functional operations (`map`, `filter`, `reduce`) that express intent without requiring mutation tracking.

---

### Strategy 3: Reduce Variable Scope

**Principle**: Variables should be as close to their use as possible; don't declare them at the function level if they're only used in one block.

**Why**: Wider scope means the variable is in play longer; reduces clarity about where it's used.

**Examples**:

**✗ High load (variable used far from declaration)**:
```python
def process_users(users, threshold):
    results = None  # Declared here
    errors = []
    
    for user in users:
        if user.age > threshold:
            # ... 50 lines of code ...
            results = transform(user)  # Used here
    
    return results  # Used again here
```

**✓ Lower load (variable close to use)**:
```python
def process_users(users, threshold):
    errors = []
    
    for user in users:
        if user.age > threshold:
            # ... 50 lines of code ...
            results = transform(user)  # Declared and used close by
            return results
    
    return None
```

**Technique**: Declare variables just before first use; consider extracting into separate functions if scope is large.

---

### Strategy 4: Use Clear, Chunked Logic Flow

**Principle**: Break code into clearly labelled phases or steps.

**Why**: When the reader understands "step 1, then step 2," they don't have to hold the whole function in mind.

**Examples**:

**✗ High load (mixed concerns)**:
```python
def process_order(order, db):
    if order.id and order.status == 'pending':
        items = [item for item in order.items if item.in_stock]
        if items:
            total = sum(item.price * item.qty for item in items)
            if total > 0:
                order.status = 'processing'
                db.update_order(order)
                return {'total': total, 'items': items}
    return None
```

**✓ Lower load (clear phases)**:
```python
def process_order(order, db):
    """Validate, calculate, and process order."""
    
    # Phase 1: Validate
    if not order.id or order.status != 'pending':
        return None
    
    # Phase 2: Check availability
    in_stock_items = [item for item in order.items if item.in_stock]
    if not in_stock_items:
        return None
    
    # Phase 3: Calculate
    total = sum(item.price * item.qty for item in in_stock_items)
    if total <= 0:
        return None
    
    # Phase 4: Persist
    order.status = 'processing'
    db.update_order(order)
    
    return {'total': total, 'items': in_stock_items}
```

**Technique**: Use comments or sub-functions to mark clear phases. Use guard clauses (early return) to reduce nesting.

---

### Strategy 5: Enforce Consistent Naming Patterns

**Principle**: Use naming conventions that help the reader predict what they'll see.

**Why**: Consistency reduces the need to "decode" names. Once you learn the pattern, all names follow it.

**Examples**:

**Naming patterns**:

| Category | Pattern | Examples |
|----------|---------|----------|
| **Boolean queries** | `is*` or `has*` | `is_valid`, `has_permission`, `can_delete` |
| **Getters** | `get_*` | `get_user`, `get_total` |
| **Setters** | `set_*` | `set_email`, `set_timeout` |
| **Factories** | `create_*` or `make_*` | `create_user`, `make_connection` |
| **Validators** | `validate_*` | `validate_email`, `validate_range` |
| **Calculators** | `calculate_*` or `compute_*` | `calculate_total`, `compute_average` |

**Consistency reduces cognitive load** because the reader can predict what a function does from its name.

---

### Strategy 6: Separate Business Logic from Plumbing

**Principle**: Keep the "what we're trying to do" separate from the "how we do it technically."

**Why**: Mixing concerns makes both harder to understand. A reader needs to switch contexts constantly.

**Examples**:

**✗ High load (mixed concerns)**:
```python
def get_user_summary(user_id):
    try:
        conn = db.get_connection()
        result = conn.query(f"SELECT * FROM users WHERE id = {user_id}")
        if not result:
            logger.warn(f"User {user_id} not found")
            return None
        user = User(**result)
        # Business logic mixed with logging and error handling
        if user.age > 18:
            user.category = 'adult'
        else:
            user.category = 'minor'
        logger.info(f"Categorized user {user_id}")
        conn.close()
        return {
            'id': user.id,
            'name': user.name,
            'category': user.category
        }
    except Exception as e:
        logger.error(f"Failed to summarise user: {e}")
        return None
```

**✓ Lower load (separation of concerns)**:
```python
# Pure business logic
def categorise_user(user):
    """Determine user category (no I/O, no logging)."""
    return 'adult' if user.age > 18 else 'minor'

# I/O layer
def get_user_summary(user_id):
    """Fetch and summarise user."""
    try:
        user = user_repository.get(user_id)
    except UserNotFoundError:
        logger.warn(f"User {user_id} not found")
        return None
    
    category = categorise_user(user)
    summary = {
        'id': user.id,
        'name': user.name,
        'category': category
    }
    logger.info(f"Summarised user {user_id}")
    return summary
```

**Technique**: Extract pure business logic into separate functions. Let the orchestration layer handle I/O and error handling.

---

### Strategy 7: Document Assumptions and Invariants

**Principle**: Clearly state what the code assumes about its inputs and what it guarantees about its outputs.

**Why**: Hidden assumptions create surprise; documenting them prevents surprises.

**Examples**:

**✗ High load (hidden assumptions)**:
```python
def average(values):
    return sum(values) / len(values)
```

**Assumptions**: `values` is not empty, all values are numbers. What if they're not? The error is unclear.

**✓ Lower load (explicit assumptions)**:
```python
def average(values):
    """Calculate mean of numeric values.
    
    Args:
        values: Non-empty sequence of numbers.
    
    Returns:
        Mean value (float).
    
    Raises:
        ValueError: If values is empty.
        TypeError: If any value is not numeric.
    """
    if not values:
        raise ValueError("Cannot average an empty list")
    
    return sum(values) / len(values)
```

**Technique**: Document preconditions, postconditions, and error cases in docstrings.

---

### Strategy 8: Use Meaningful Abstractions

**Principle**: Hide unnecessary detail; expose intent.

**Why**: Unnecessary detail adds cognitive load without adding understanding.

**Examples**:

**✗ High load (detail-heavy)**:
```javascript
// Is this for sorting? Searching? Why 47?
if (array[Math.floor(array.length / 2)] > 47) {
    // ...
}

// What is the relationship between these numbers?
const discount = 0.85;
const tax_rate = 0.08;
```

**✓ Lower load (meaningful abstraction)**:
```javascript
const MEDIAN = array[Math.floor(array.length / 2)];
const SIGNIFICANCE_THRESHOLD = 47;

if (MEDIAN > SIGNIFICANCE_THRESHOLD) {
    // ...
}

const EARLY_BIRD_DISCOUNT = 0.85;
const SALES_TAX_RATE = 0.08;
```

**Technique**: Extract constants with meaningful names; use domain terminology.

---

### Strategy 9: Limit Function Parameters

**Principle**: A function should take 0–3 parameters. More than that, and the cognitive load of remembering what each is increases.

**Why**: Each parameter is a thing the reader must understand. More parameters = more mental baggage.

**Examples**:

**✗ High load (many parameters)**:
```python
def create_order(user_id, items_list, shipping_address, billing_address, 
                 discount_code, coupon_code, gift_message, gift_wrap, 
                 express_shipping, insurance, payment_method, ...):
    # What do all these parameters mean?
    # Which are required vs optional?
```

**✓ Lower load (grouped parameters)**:
```python
class OrderRequest:
    user_id: int
    items: List[OrderItem]
    shipping: Address
    billing: Address
    discount: Discount
    gift: GiftOptions
    payment: PaymentMethod

def create_order(request: OrderRequest):
    # One parameter; its properties are self-documenting
```

**Technique**: Group related parameters into objects or data structures.

---

## The Cognitive Load Checklist

When reviewing code, ask:

- [ ] **Nesting**: Is there code with more than 3 levels of indentation? Can it be flattened?
- [ ] **Variables**: How many variables are "in play" at once? Can I reduce that?
- [ ] **Scope**: Is each variable as close to its use as possible?
- [ ] **Flow**: Are there clear phases or steps? Or is it a jumbled mix?
- [ ] **Naming**: Do names follow consistent patterns? Can I predict what a function does from its name?
- [ ] **Concerns**: Is business logic mixed with I/O, logging, error handling?
- [ ] **Assumptions**: Are preconditions and guarantees documented?
- [ ] **Abstractions**: Are unnecessary details hidden? Is intent clear?
- [ ] **Parameters**: Does the function take too many parameters to hold in mind?

---

## Teaching Cognitive Load

When pointing out high cognitive load, frame it as a teaching opportunity:

**Instead of:** *"This is too complicated."*

**Say:** *"To understand this function, I have to hold 5 variables in my head, track 3 nested loops, and remember what each variable does. Let's break it down so each part is easier to understand."*

Then:
1. Show which part is hard to understand
2. Explain why (e.g., "too many nesting levels")
3. Suggest a refactoring
4. Show how the refactored version is clearer

---

## Next: Context Discovery

See [context-discovery.md](./context-discovery.md) for questions to ask when orienting yourself to unfamiliar code.
