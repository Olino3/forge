# Common Python Issues and Anti-Patterns

Quick reference for universal Python anti-patterns and common issues. For detailed examples and explanations, see official Python docs and community resources.

---

## Core Language Issues

| Issue | What to Look For | Quick Fix | Learn More |
|-------|------------------|-----------|------------|
| **Mutable default arguments** | `def func(arg=[]):` or `def func(arg={}):` | Use `None` and initialize inside function | [Python FAQ](https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects) |
| **Late binding closures** | Lambda/function in loop referencing loop variable | Use default argument: `lambda i=i:` | [Python closures](https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result) |
| **Modifying list while iterating** | `for item in list:` with `list.remove()` | Iterate over copy `list[:]` or use list comprehension | [Python tutorial](https://docs.python.org/3/tutorial/controlflow.html#for-statements) |
| **Using `is` for values** | `if x is 5:` or `if name is "John":` | Use `==` for value comparison | [Python operators](https://docs.python.org/3/reference/expressions.html#is) |
| **Bare `except:`** | `except:` without exception type | Catch specific exceptions or use `except Exception:` | [PEP 8](https://peps.python.org/pep-0008/#programming-recommendations) |
| **Using `eval()`/`exec()`** | `eval(user_input)` | Use `ast.literal_eval()` or safer alternatives | [Security best practices](https://docs.python.org/3/library/ast.html#ast.literal_eval) |

---

## Memory and Performance

| Issue | What to Look For | Quick Fix | Learn More |
|-------|------------------|-----------|------------|
| **Circular references** | Objects referencing each other | Use weak references or explicit cleanup | [gc module](https://docs.python.org/3/library/gc.html) |
| **Unclosed resources** | File handles, connections without `close()` | Use context managers (`with` statement) | [Context managers](https://docs.python.org/3/reference/compound_stmts.html#with) |
| **String concatenation in loops** | `s += str` in loop | Use `''.join(list)` or `io.StringIO` | [Performance tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips#String_Concatenation) |
| **Using `+` for list concatenation** | `list1 + list2` in loop | Use `list.extend()` or list comprehension | [Python lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists) |
| **Not using generators** | Loading entire dataset into memory | Use generators/iterators for large data | [Generators](https://docs.python.org/3/howto/functional.html#generators) |
| **Inefficient imports** | `from module import *` | Import specific names or use qualified imports | [PEP 8 imports](https://peps.python.org/pep-0008/#imports) |

---

## Exception Handling

| Issue | What to Look For | Quick Fix | Learn More |
|-------|------------------|-----------|------------|
| **Swallowing exceptions** | `except: pass` | Log exceptions, only catch what you can handle | [Python exceptions](https://docs.python.org/3/tutorial/errors.html) |
| **Using exceptions for flow control** | `try/except` for expected conditions | Use conditionals for control flow | [EAFP vs LBYL](https://docs.python.org/3/glossary.html#term-EAFP) |
| **Raising generic exceptions** | `raise Exception("error")` | Raise specific exception types | [Built-in exceptions](https://docs.python.org/3/library/exceptions.html) |
| **Not chaining exceptions** | Catching and raising new exception without context | Use `raise NewException() from e` | [PEP 3134](https://peps.python.org/pep-3134/) |

---

## Import Issues

| Issue | What to Look For | Quick Fix | Learn More |
|-------|------------------|-----------|------------|
| **Circular imports** | ModuleA imports ModuleB, ModuleB imports ModuleA | Restructure code, use local imports, or dependency injection | [Import system](https://docs.python.org/3/reference/import.html) |
| **Relative imports in scripts** | `from . import module` in `__main__` | Use absolute imports or run as module with `-m` | [PEP 328](https://peps.python.org/pep-0328/) |
| **Import order issues** | Random import order | Follow PEP 8: stdlib, third-party, local | [PEP 8 imports](https://peps.python.org/pep-0008/#imports) |

---

## Concurrency Issues

| Issue | What to Look For | Quick Fix | Learn More |
|-------|------------------|-----------|------------|
| **GIL assumptions** | Expecting thread parallelism for CPU-bound work | Use multiprocessing for CPU-bound tasks | [GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) |
| **Race conditions** | Shared mutable state without locks | Use `threading.Lock` or `queue.Queue` | [threading module](https://docs.python.org/3/library/threading.html) |
| **Mixing sync/async** | Regular functions called in async context | Use `asyncio.to_thread()` or proper async libraries | [asyncio](https://docs.python.org/3/library/asyncio.html) |
| **Not using ThreadPoolExecutor** | Manual thread management | Use `concurrent.futures.ThreadPoolExecutor` | [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) |

---

## Type and Attribute Issues

| Issue | What to Look For | Quick Fix | Learn More |
|-------|------------------|-----------|------------|
| **Mutable class attributes** | Class-level lists/dicts shared across instances | Use instance attributes in `__init__` | [Class variables](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) |
| **Name shadowing** | Variable/function name same as builtin (`list`, `dict`) | Use different names | [Built-in functions](https://docs.python.org/3/library/functions.html) |
| **Using `type()` for type checking** | `if type(x) == int:` | Use `isinstance(x, int)` | [Built-in functions](https://docs.python.org/3/library/functions.html#isinstance) |
| **Missing `__init__`** | Instance attributes set outside `__init__` | Initialize all attributes in `__init__` | [Python classes](https://docs.python.org/3/tutorial/classes.html) |

---

## Common Gotchas

| Issue | What to Look For | Quick Fix | Learn More |
|-------|------------------|-----------|------------|
| **Integer division in Python 2 style** | `5 / 2` expecting 2 | Use `//` for floor division, `/` for float division | [PEP 238](https://peps.python.org/pep-0238/) |
| **Truth value testing** | `if len(list) > 0:` | Use `if list:` (empty containers are falsy) | [Truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing) |
| **Dict key order assumptions (Python <3.7)** | Relying on dict order | Use `OrderedDict` or Python 3.7+ | [Dict order](https://docs.python.org/3/library/stdtypes.html#dict) |
| **Float equality** | `if 0.1 + 0.2 == 0.3:` (False!) | Use `math.isclose()` or `decimal` module | [Floating point](https://docs.python.org/3/tutorial/floatingpoint.html) |

---

## Detection Patterns

Use these code patterns to identify issues during review:

```python
# Mutable defaults
def func(arg=[]): ...
def func(arg={}): ...
def func(arg=set()): ...

# Bare except
try:
    ...
except:  # Missing exception type

# Resource leaks
f = open('file.txt')
# Missing: with statement or close()

# String concatenation
result = ""
for item in items:
    result += str(item)  # Inefficient

# Using eval
eval(user_input)  # Security risk

# Type checking
if type(x) == int:  # Should use isinstance()

# Shadowing builtins
list = [1, 2, 3]  # Shadows built-in 'list'
```

---

## Tools for Detection

- **pylint**: Comprehensive linter - [pylint docs](https://pylint.readthedocs.io/)
- **flake8**: Style + error checker - [flake8 docs](https://flake8.pycqa.org/)
- **ruff**: Fast Python linter - [ruff docs](https://github.com/astral-sh/ruff)
- **mypy**: Static type checker - [mypy docs](https://mypy.readthedocs.io/)
- **bandit**: Security issues - [bandit docs](https://bandit.readthedocs.io/)

---

## Best Practices Resources

- **PEP 8** (Style Guide): https://peps.python.org/pep-0008/
- **Python Anti-Patterns**: https://docs.quantifiedcode.com/python-anti-patterns/
- **Effective Python** (Book): https://effectivepython.com/
- **Python FAQ**: https://docs.python.org/3/faq/programming.html
- **Real Python** (Tutorials): https://realpython.com/

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
