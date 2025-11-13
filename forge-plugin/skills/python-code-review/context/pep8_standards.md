# PEP 8 Style Guide Reference

This file contains Python style conventions based on PEP 8 - Style Guide for Python Code.

## Naming Conventions

### Variables and Functions
- **snake_case** for variable names and function names
  ```python
  user_count = 10
  def calculate_total_price():
      pass
  ```

### Classes
- **PascalCase** for class names
  ```python
  class UserProfile:
      pass

  class HTTPConnection:
      pass
  ```

### Constants
- **UPPER_CASE_WITH_UNDERSCORES** for module-level constants
  ```python
  MAX_RETRY_COUNT = 3
  DEFAULT_TIMEOUT = 30
  API_BASE_URL = "https://api.example.com"
  ```

### Private Members
- **Single leading underscore** for internal use (weak "internal use" indicator)
  ```python
  def _internal_helper():
      pass

  class MyClass:
      def __init__(self):
          self._internal_state = None
  ```

- **Double leading underscore** for name mangling (avoid unless necessary)
  ```python
  class MyClass:
      def __init__(self):
          self.__private_attr = None  # Becomes _MyClass__private_attr
  ```

### Special Methods
- **Double underscore before and after** for magic methods
  ```python
  def __init__(self):
      pass

  def __str__(self):
      pass
  ```

## Code Layout

### Indentation
- Use **4 spaces** per indentation level
- Never mix tabs and spaces
- Continuation lines should align wrapped elements vertically or use hanging indent

```python
# Good - aligned with opening delimiter
result = some_function(argument_one, argument_two,
                      argument_three, argument_four)

# Good - hanging indent
result = some_function(
    argument_one,
    argument_two,
    argument_three
)
```

### Maximum Line Length
- Limit lines to **79 characters** for code
- Limit docstrings/comments to **72 characters**
- For teams using modern editors, **99 characters** is acceptable (PEP 8 allows this)

```python
# Good - use parentheses for continuation
if (condition_one and condition_two and
        condition_three and condition_four):
    do_something()

# Good - backslash for long strings
long_string = "This is a very long string that " \
              "continues on the next line"
```

### Blank Lines
- **Two blank lines** around top-level functions and classes
- **One blank line** between methods inside a class
- Use blank lines sparingly inside functions to indicate logical sections

```python
class MyClass:
    """A simple class."""

    def __init__(self):
        self.value = 0

    def method_one(self):
        pass


def top_level_function():
    pass


class AnotherClass:
    pass
```

### Imports
- Imports should be on separate lines
- Group imports in order: standard library, third-party, local
- Use absolute imports over relative imports

```python
# Good
import os
import sys
from subprocess import Popen, PIPE

# Avoid
import os, sys

# Import grouping
import os           # Standard library
import sys

import requests     # Third-party
import django

from myapp import models  # Local
```

## Whitespace

### Expressions and Statements
```python
# Good
spam(ham[1], {eggs: 2})
if x == 4:
    print(x, y)
x, y = y, x

# Bad
spam( ham[ 1 ], { eggs: 2 } )
if x == 4 :
    print( x , y )
x , y = y , x
```

### Operators
- Surround binary operators with single space on each side
```python
# Good
i = i + 1
submitted += 1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)

# Bad
i=i+1
submitted +=1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```

- Don't use spaces around `=` for keyword arguments or default parameter values
```python
# Good
def complex(real, imag=0.0):
    return magic(r=real, i=imag)

# Bad
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

## Comments and Docstrings

### Inline Comments
- Use sparingly
- Separate from code by at least two spaces
- Start with `#` and a single space

```python
# Good
x = x + 1  # Compensate for border

# Bad - obvious comment
x = x + 1  # Increment x
```

### Block Comments
- Apply to code that follows
- Indent to the same level as code
- Start each line with `#` and a single space

```python
# This is a block comment that explains
# the following complex algorithm.
# It spans multiple lines.
result = complex_algorithm()
```

### Docstrings
- Write docstrings for all public modules, functions, classes, and methods
- Use triple double quotes: `"""`
- One-line docstrings for simple functions
- Multi-line docstrings for complex functions

```python
def simple_function():
    """Return the answer to life, the universe, and everything."""
    return 42


def complex_function(arg1, arg2):
    """
    Perform complex operation on arguments.

    Args:
        arg1: Description of first argument
        arg2: Description of second argument

    Returns:
        Description of return value

    Raises:
        ValueError: If arguments are invalid
    """
    if not arg1:
        raise ValueError("arg1 cannot be empty")
    return process(arg1, arg2)
```

## String Quotes
- Use single quotes `'` or double quotes `"` consistently
- For triple-quoted strings, always use double quotes: `"""`
- Use the other quote type to avoid backslashes

```python
# Good - avoid backslashes
message = "Don't do that"
sql = 'SELECT * FROM users WHERE name = "John"'

# Bad - unnecessary escaping
message = 'Don\'t do that'
```

## Trailing Commas
- Use trailing commas in multi-line constructs for easier version control

```python
# Good
FILES = [
    'setup.cfg',
    'tox.ini',
]

# Also good for tuples
values = (
    1,
    2,
)
```

## Programming Recommendations

### Comparisons
- Use `is` and `is not` for comparisons with `None`
- Don't compare boolean values with `True` or `False`

```python
# Good
if value is None:
    pass

if greeting:
    pass

# Bad
if value == None:
    pass

if greeting == True:
    pass
```

### Use `in` for Membership
```python
# Good
if item in collection:
    pass

# Bad
if collection.count(item) > 0:
    pass
```

### Type Checking
- Use `isinstance()` instead of comparing types directly

```python
# Good
if isinstance(obj, int):
    pass

# Bad
if type(obj) is int:
    pass
```

### Empty Sequences
- Empty sequences are false

```python
# Good
if not seq:
    pass
if seq:
    pass

# Bad
if len(seq) == 0:
    pass
if len(seq):
    pass
```

### String Handling
- Use `''.join()` for string concatenation in loops
- Use f-strings (Python 3.6+) for formatting

```python
# Good
result = ''.join(items)
message = f"Hello, {name}!"

# Bad
result = ''
for item in items:
    result += item

message = "Hello, " + name + "!"
```

### Context Managers
- Use context managers (`with` statement) for resource management

```python
# Good
with open('file.txt') as f:
    data = f.read()

# Bad
f = open('file.txt')
data = f.read()
f.close()
```

### List Comprehensions
- Use list comprehensions for simple transformations
- Don't overuse - readability matters

```python
# Good
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]

# Too complex - use regular loop
# Bad
result = [x**2 if x % 2 == 0 else x**3
          for x in range(10)
          if x > 5 or x < 2]
```

## Function and Method Arguments

### Argument Order
1. Positional arguments
2. `*args`
3. Keyword arguments with defaults
4. `**kwargs`

```python
def function(pos1, pos2, *args, kwarg1=None, kwarg2=None, **kwargs):
    pass
```

### Type Hints (PEP 484)
- Use type hints for function signatures (Python 3.5+)

```python
def greeting(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[int]) -> dict[str, int]:
    return {'count': len(items), 'sum': sum(items)}
```

## Common PEP 8 Violations to Check

1. **E501**: Line too long (>79 characters)
2. **E302**: Expected 2 blank lines, found 1
3. **E303**: Too many blank lines
4. **E231**: Missing whitespace after `,`
5. **E225**: Missing whitespace around operator
6. **E251**: Unexpected spaces around keyword / parameter equals
7. **W291**: Trailing whitespace
8. **W293**: Blank line contains whitespace
9. **E711**: Comparison to None should be `if cond is None:`
10. **E712**: Comparison to True should be `if cond:` or `if cond is True:`

## Tools for PEP 8 Compliance

- **pylint**: Comprehensive code quality checker
- **flake8**: Fast PEP 8 checker (combines pycodestyle, pyflakes, mccabe)
- **black**: Uncompromising code formatter (auto-fixes)
- **autopep8**: Automatically formats code to conform to PEP 8

## When to Ignore PEP 8

PEP 8 states: "A Foolish Consistency is the Hobgoblin of Little Minds"

Ignore PEP 8 when:
1. Applying the guideline would make code less readable
2. Maintaining consistency with surrounding code that breaks the rule
3. The code predates PEP 8 and there's no reason to change it
4. Code needs to remain compatible with older Python versions

Use `# noqa` comments to suppress warnings:
```python
example = lambda: 'example'  # noqa: E731
```

## References

- PEP 8: https://peps.python.org/pep-0008/
- PEP 257: Docstring Conventions
- PEP 484: Type Hints
- Google Python Style Guide
- Black Code Style
