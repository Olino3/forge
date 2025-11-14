# Common Python Issues and Anti-Patterns

This file contains universal Python anti-patterns and common issues that apply regardless of the framework being used.

## Mutable Default Arguments

### Problem
Default arguments are evaluated once when the function is defined, not each time it's called.

```python
# WRONG
def append_to_list(item, items=[]):
    items.append(item)
    return items

list1 = append_to_list('a')  # ['a']
list2 = append_to_list('b')  # ['a', 'b'] - UNEXPECTED!
```

### Solution
```python
# CORRECT
def append_to_list(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Why It Matters
- Causes hard-to-debug state persistence between function calls
- Leads to unexpected behavior in production
- Common source of subtle bugs

---

## Late Binding Closures

### Problem
Python's closures bind to variables, not values.

```python
# WRONG
functions = []
for i in range(3):
    functions.append(lambda: i)

for f in functions:
    print(f())  # Prints: 2, 2, 2 (not 0, 1, 2!)
```

### Solution
```python
# CORRECT - Use default argument
functions = []
for i in range(3):
    functions.append(lambda i=i: i)

# CORRECT - Use functools.partial
from functools import partial
functions = [partial(lambda x: x, i) for i in range(3)]

# CORRECT - Use list comprehension (creates new scope)
functions = [lambda i=i: i for i in range(3)]
```

---

## Modifying List While Iterating

### Problem
```python
# WRONG
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Skips elements!
# Result: [1, 3, 5] - missed 4!
```

### Solution
```python
# CORRECT - List comprehension
numbers = [num for num in numbers if num % 2 != 0]

# CORRECT - Iterate over copy
for num in numbers[:]:
    if num % 2 == 0:
        numbers.remove(num)

# CORRECT - Filter
numbers = list(filter(lambda x: x % 2 != 0, numbers))
```

---

## Using `is` for Value Comparison

### Problem
```python
# WRONG
if value is 1000:  # May be True or False randomly!
    pass

if name is "John":  # May be True or False randomly!
    pass
```

### Solution
```python
# CORRECT
if value == 1000:
    pass

if name == "John":
    pass

# `is` is ONLY for identity checks, especially None
if value is None:
    pass

if value is True:  # Use sparingly; usually just `if value:` is better
    pass
```

### Why It Matters
- `is` checks object identity (same memory location)
- CPython caches small integers (-5 to 256) and short strings
- Code may work in testing but fail in production

---

## Exception Handling Anti-Patterns

### Bare Except
```python
# WRONG - Catches everything, including KeyboardInterrupt
try:
    do_something()
except:
    pass
```

### Solution
```python
# CORRECT - Catch specific exceptions
try:
    do_something()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except IOError as e:
    logger.error(f"IO error: {e}")

# If you must catch all, use Exception (not bare except)
try:
    do_something()
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise  # Re-raise after logging
```

### Exception Swallowing
```python
# WRONG - Silently ignores errors
try:
    result = risky_operation()
except Exception:
    pass  # Error is lost!
```

### Solution
```python
# CORRECT - Log and handle
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    result = default_value
```

---

## Resource Management

### Missing Context Managers
```python
# WRONG - File may not close if exception occurs
file = open('data.txt')
data = file.read()
process(data)  # If this raises, file never closes
file.close()
```

### Solution
```python
# CORRECT - Context manager ensures cleanup
with open('data.txt') as file:
    data = file.read()
    process(data)
# File automatically closed

# BETTER - pathlib
from pathlib import Path
data = Path('data.txt').read_text()
```

### Database Connections
```python
# WRONG
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(query)
conn.close()  # May not execute if error occurs

# CORRECT
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(query)
# Connection and cursor automatically closed
```

---

## String Concatenation in Loops

### Problem
```python
# WRONG - Creates new string object on each iteration (O(n²))
result = ''
for item in items:
    result += str(item)  # Inefficient!
```

### Solution
```python
# CORRECT - O(n)
result = ''.join(str(item) for item in items)

# For f-strings
result = ''.join(f"Item: {item}" for item in items)
```

---

## Using `==` for None/Boolean Comparison

### Problem
```python
# WRONG
if value == None:  # Works, but not idiomatic
    pass

if is_valid == True:  # Redundant
    pass
```

### Solution
```python
# CORRECT
if value is None:
    pass

if is_valid:  # Booleans are truthy/falsy
    pass

if not is_valid:
    pass
```

---

## Global State and Mutable Globals

### Problem
```python
# WRONG
counter = 0

def increment():
    counter += 1  # UnboundLocalError!
    return counter

# WRONG
CONFIG = {}

def set_config(key, value):
    CONFIG[key] = value  # Mutable global state!
```

### Solution
```python
# BETTER - Explicit global (still not ideal)
counter = 0

def increment():
    global counter
    counter += 1
    return counter

# BEST - Avoid global state
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

# For config, use a class or dataclass
from dataclasses import dataclass

@dataclass
class Config:
    api_key: str
    timeout: int = 30

config = Config(api_key="xyz")
```

---

## Class Variable vs Instance Variable

### Problem
```python
# WRONG
class Dog:
    tricks = []  # Class variable, shared by all instances!

    def add_trick(self, trick):
        self.tricks.append(trick)

dog1 = Dog()
dog1.add_trick('roll over')
dog2 = Dog()
print(dog2.tricks)  # ['roll over'] - UNEXPECTED!
```

### Solution
```python
# CORRECT
class Dog:
    def __init__(self):
        self.tricks = []  # Instance variable

    def add_trick(self, trick):
        self.tricks.append(trick)
```

---

## Not Using Enumerate

### Problem
```python
# WRONG
items = ['a', 'b', 'c']
i = 0
for item in items:
    print(f"{i}: {item}")
    i += 1

# ALSO WRONG
for i in range(len(items)):
    print(f"{i}: {items[i]}")
```

### Solution
```python
# CORRECT
for i, item in enumerate(items):
    print(f"{i}: {item}")

# With custom start index
for i, item in enumerate(items, start=1):
    print(f"{i}: {item}")
```

---

## Not Using zip

### Problem
```python
# WRONG
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]

for i in range(len(names)):
    print(f"{names[i]} is {ages[i]} years old")
```

### Solution
```python
# CORRECT
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# For dictionaries
data = dict(zip(names, ages))
```

---

## Type Checking Anti-Patterns

### Using type() Instead of isinstance()
```python
# WRONG
if type(value) == int:
    pass

if type(value) is int:
    pass
```

### Solution
```python
# CORRECT - Works with subclasses
if isinstance(value, int):
    pass

# Multiple types
if isinstance(value, (int, float)):
    pass
```

---

## Dictionary get() vs KeyError

### Problem
```python
# WRONG - Raises KeyError if missing
try:
    value = data['key']
except KeyError:
    value = default

# WRONG - Checks key twice
if 'key' in data:
    value = data['key']
else:
    value = default
```

### Solution
```python
# CORRECT
value = data.get('key', default)

# For setdefault
value = data.setdefault('key', default)  # Also sets if missing

# For defaultdict
from collections import defaultdict
data = defaultdict(list)
data['key'].append(item)  # No KeyError
```

---

## List Comprehension Over map/filter

### Problem
```python
# LESS PYTHONIC
result = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

### Solution
```python
# MORE PYTHONIC
result = [x**2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]

# Exception: When you already have a named function
result = list(map(str.upper, words))  # Acceptable
```

---

## Not Using Tuple Unpacking

### Problem
```python
# WRONG
def get_coordinates():
    return [10, 20]

coords = get_coordinates()
x = coords[0]
y = coords[1]
```

### Solution
```python
# CORRECT
def get_coordinates():
    return 10, 20  # Returns tuple

x, y = get_coordinates()

# Extended unpacking
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5
```

---

## Using `range(len())` Instead of Direct Iteration

### Problem
```python
# WRONG
for i in range(len(items)):
    process(items[i])
```

### Solution
```python
# CORRECT
for item in items:
    process(item)

# If you need the index
for i, item in enumerate(items):
    print(f"Item {i}: {item}")
```

---

## Checking Length for Empty Collections

### Problem
```python
# WRONG
if len(items) == 0:
    print("Empty")

if len(items) > 0:
    print("Not empty")

if len(text) == 0:
    print("Empty string")
```

### Solution
```python
# CORRECT - Truthy/falsy values
if not items:
    print("Empty")

if items:
    print("Not empty")

if not text:
    print("Empty string")
```

### Why It Matters
- More Pythonic and readable
- Works with any iterable (lists, sets, dicts, strings, etc.)
- Slightly more efficient

---

## Star Imports

### Problem
```python
# WRONG - Pollutes namespace
from module import *
```

### Solution
```python
# CORRECT - Explicit imports
from module import specific_function, specific_class

# For many imports
import module
# Use: module.function()

# Acceptable in interactive sessions only
```

---

## Using Lists as Sets

### Problem
```python
# WRONG - O(n) lookup
if item in items_list:  # Slow for large lists
    pass

# WRONG - O(n²) for duplicate removal
unique = []
for item in items:
    if item not in unique:
        unique.append(item)
```

### Solution
```python
# CORRECT - O(1) lookup
items_set = set(items_list)
if item in items_set:  # Fast!
    pass

# CORRECT - Duplicate removal
unique = list(set(items))

# If order matters
from collections import OrderedDict
unique = list(OrderedDict.fromkeys(items))

# Python 3.7+ (dict maintains insertion order)
unique = list(dict.fromkeys(items))
```

---

## Not Using Generators for Large Data

### Problem
```python
# WRONG - Loads entire dataset into memory
def get_all_records():
    results = []
    for record in database.query():
        results.append(process(record))
    return results

data = get_all_records()  # OOM for large datasets!
```

### Solution
```python
# CORRECT - Generator (lazy evaluation)
def get_all_records():
    for record in database.query():
        yield process(record)

# Use with iteration
for item in get_all_records():
    print(item)

# Or generator expression
data = (process(record) for record in database.query())
```

---

## Unnecessary Lambda Functions

### Problem
```python
# WRONG
result = map(lambda x: x.upper(), words)
result = sorted(items, key=lambda x: x.name)
```

### Solution
```python
# CORRECT - Method reference
result = map(str.upper, words)

# Use operator.attrgetter
from operator import attrgetter
result = sorted(items, key=attrgetter('name'))
```

---

## Circular Imports

### Problem
```python
# module_a.py
from module_b import func_b

def func_a():
    return func_b()

# module_b.py
from module_a import func_a  # Circular!

def func_b():
    return func_a()
```

### Solution
```python
# 1. Restructure to remove circular dependency
# 2. Use local imports
def func_b():
    from module_a import func_a  # Import only when needed
    return func_a()

# 3. Create a third module for shared code
# shared.py
def shared_function():
    pass
```

---

## Thread Safety Issues

### Problem
```python
# WRONG - Not thread-safe
counter = 0

def increment():
    global counter
    counter += 1  # Race condition!
```

### Solution
```python
# CORRECT - Use threading.Lock
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:
        counter += 1

# BETTER - Use queue.Queue or threading-safe collections
from queue import Queue
q = Queue()
```

---

## Common Performance Issues

### Unnecessary Copying
```python
# WRONG
import copy
new_list = copy.deepcopy(original_list)  # Expensive!
```

### List Concatenation in Loop
```python
# WRONG - O(n²)
result = []
for chunk in chunks:
    result = result + chunk  # Creates new list each time!

# CORRECT - O(n)
result = []
for chunk in chunks:
    result.extend(chunk)  # Modifies in-place
```

### Not Using Built-in Functions
```python
# WRONG - Slower
total = 0
for item in numbers:
    total += item

# CORRECT - Faster (C implementation)
total = sum(numbers)

# Similarly, use: min(), max(), any(), all()
```

---

## Anti-Pattern Checklist for Code Review

Check for these common issues:

- [ ] Mutable default arguments (def func(arg=[]):)
- [ ] Modifying list during iteration
- [ ] Using `is` for value comparison (except None)
- [ ] Bare except clauses
- [ ] Missing context managers for resources
- [ ] String concatenation in loops (use join)
- [ ] Using `==` for None comparison (use `is`)
- [ ] Class variables used as instance variables
- [ ] Using type() instead of isinstance()
- [ ] Not using dict.get() with default
- [ ] range(len()) instead of enumerate()
- [ ] Checking len() == 0 instead of truthiness
- [ ] Star imports (from x import *)
- [ ] Using lists where sets are appropriate
- [ ] Not using generators for large data
- [ ] Circular imports
- [ ] Thread safety issues
- [ ] Unnecessary copying or list concatenation

## References

- Python Anti-Patterns: https://docs.quantifiedcode.com/python-anti-patterns/
- Effective Python by Brett Slatkin
- Fluent Python by Luciano Ramalho
- Python Cookbook by David Beazley
