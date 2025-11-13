# Inline Code Review Comments Template

This template provides examples of inline PR-style comments for different types of issues.

---

## Critical Issues

### Security Vulnerability

**File**: `auth.py:45`

```python
# Current code
user = db.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

**Issue**: SQL Injection Vulnerability

**Severity**: 🔴 Critical

**Description**:
User input is directly interpolated into the SQL query, allowing attackers to execute arbitrary SQL commands.

**Attack Vector**:
```python
username = "admin' OR '1'='1"
# Results in: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

**Fix**:
```python
# Use parameterized queries
user = db.execute("SELECT * FROM users WHERE username = %s", (username,))

# Or use ORM
user = User.query.filter_by(username=username).first()
```

**Reference**: OWASP A03:2021 - Injection

---

### Data Corruption Risk

**File**: `payment.py:123`

```python
# Current code
order.amount -= discount
order.save()
payment.process(order.amount)
```

**Issue**: Race Condition in Payment Processing

**Severity**: 🔴 Critical

**Description**:
If two requests process the same order simultaneously, the discount could be applied twice, leading to incorrect payment amounts.

**Fix**:
```python
from django.db import transaction

@transaction.atomic
def process_payment(order_id, discount):
    order = Order.objects.select_for_update().get(id=order_id)
    order.amount -= discount
    order.save()
    payment.process(order.amount)
```

---

## Important Issues

### Performance Bottleneck

**File**: `views.py:67`

```python
# Current code
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # N+1 query problem
```

**Issue**: N+1 Query Problem

**Severity**: 🟡 Important

**Impact**: For 100 posts, this executes 101 database queries instead of 1.

**Performance**: ~1000ms → ~10ms (100x improvement)

**Fix**:
```python
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.name)  # No additional queries
```

---

### Type Safety Issue

**File**: `utils.py:234`

```python
def calculate_total(prices):
    return sum(prices) * 1.1
```

**Issue**: Missing Type Hints

**Severity**: 🟡 Important

**Description**:
Function lacks type hints, making it unclear what types are expected and returned. Could lead to runtime errors.

**Fix**:
```python
def calculate_total(prices: list[float]) -> float:
    """Calculate total with 10% tax.

    Args:
        prices: List of item prices

    Returns:
        Total amount including tax
    """
    return sum(prices) * 1.1
```

---

### Architectural Concern

**File**: `api.py:89`

```python
@app.route('/process')
def process_data():
    # 150 lines of business logic mixed with HTTP handling
    data = request.get_json()
    # ... lots of processing ...
    return jsonify(result)
```

**Issue**: Fat Controller / Missing Service Layer

**Severity**: 🟡 Important

**Impact**:
- Hard to test business logic
- Violates Single Responsibility Principle
- Difficult to reuse logic elsewhere

**Recommendation**:
```python
# services/data_processor.py
class DataProcessor:
    def process(self, data: dict) -> dict:
        # Business logic here
        return result

# api.py
@app.route('/process')
def process_data():
    data = request.get_json()
    processor = DataProcessor()
    result = processor.process(data)
    return jsonify(result)
```

---

## Minor Issues

### Code Smell

**File**: `helpers.py:45`

```python
def append_to_list(item, items=[]):  # Mutable default argument!
    items.append(item)
    return items
```

**Issue**: Mutable Default Argument

**Severity**: 🔵 Minor

**Bug**: Default list is shared between all function calls, causing unexpected behavior.

**Example**:
```python
list1 = append_to_list('a')  # ['a']
list2 = append_to_list('b')  # ['a', 'b'] - UNEXPECTED!
```

**Fix**:
```python
def append_to_list(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

---

### Dead Code

**File**: `old_utils.py:123`

```python
def legacy_function():
    # This function is never called
    pass
```

**Issue**: Unused Code

**Severity**: 🔵 Minor

**Recommendation**: Remove to improve code maintainability and reduce cognitive load.

---

### Complexity

**File**: `calculator.py:56`

```python
def complex_calculation(x, y, z, mode, options):
    # 50 lines with nested if/else
    # Cyclomatic complexity: 23 (Rank D)
    ...
```

**Issue**: High Cyclomatic Complexity

**Severity**: 🔵 Minor

**Impact**: Hard to understand, test, and maintain.

**Recommendation**: Refactor into smaller, focused functions:
```python
def complex_calculation(x, y, z, mode, options):
    if mode == 'simple':
        return _simple_calc(x, y, z)
    elif mode == 'advanced':
        return _advanced_calc(x, y, z, options)
    else:
        return _default_calc(x, y)

def _simple_calc(x, y, z):
    ...

def _advanced_calc(x, y, z, options):
    ...
```

---

## Testing Issues

### Missing Test Coverage

**File**: `payment.py:200`

```python
def process_refund(order_id, amount):
    # Critical business logic with no tests!
    order = Order.objects.get(id=order_id)
    order.refund(amount)
    send_notification(order.user, f"Refunded ${amount}")
```

**Issue**: Missing Tests for Critical Path

**Severity**: 🟡 Important

**Recommendation**: Add comprehensive tests:
```python
# tests/test_payment.py
def test_process_refund_success():
    order = create_test_order(amount=100)
    process_refund(order.id, 50)
    assert order.amount == 50
    assert_notification_sent(order.user)

def test_process_refund_exceeds_amount():
    order = create_test_order(amount=100)
    with pytest.raises(ValueError):
        process_refund(order.id, 150)

def test_process_refund_invalid_order():
    with pytest.raises(Order.DoesNotExist):
        process_refund(99999, 50)
```

---

## Information / Suggestions

### Opportunity for Optimization

**File**: `data_processor.py:78`

```python
results = []
for item in large_dataset:
    results.append(transform(item))
```

**Suggestion**: Use list comprehension or generator for better performance

```python
# List comprehension (if all results needed in memory)
results = [transform(item) for item in large_dataset]

# Generator (if processing one at a time)
results = (transform(item) for item in large_dataset)
```

---

### Modern Python Pattern

**File**: `file_handler.py:34`

```python
f = open('data.txt', 'r')
data = f.read()
f.close()  # May not execute if read() raises exception
```

**Suggestion**: Use context manager

```python
with open('data.txt', 'r') as f:
    data = f.read()
# File automatically closed, even if exception occurs

# Or use pathlib
from pathlib import Path
data = Path('data.txt').read_text()
```

---

## Comment Format Guidelines

### Structure

```
**File**: path/to/file.py:line_number

[Code snippet if helpful]

**Issue**: Brief title

**Severity**: 🔴 Critical | 🟡 Important | 🔵 Minor | ⚪ Info

**Description**: Detailed explanation

**Impact/Why it matters**: Consequences

**Fix/Recommendation**: Concrete solution with code example

**Reference**: Links to docs, CVEs, etc. (if applicable)
```

### Severity Levels

- 🔴 **Critical**: Security vulnerabilities, data corruption, production failures
- 🟡 **Important**: Performance issues, type safety, architectural problems, missing tests
- 🔵 **Minor**: Code smells, complexity, dead code, minor bugs
- ⚪ **Info**: Suggestions, optimizations, style (only if blocking automation)

### Tone

- Be specific and actionable
- Explain the "why" not just the "what"
- Provide code examples
- Reference authoritative sources
- Acknowledge good code when present
- Be constructive, not critical
