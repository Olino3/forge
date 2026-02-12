---
id: "python/testing_frameworks"
domain: python
title: "Python Testing Frameworks"
type: pattern
estimatedTokens: 900
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Framework Detection"
    estimatedTokens: 30
    keywords: [framework, detection]
  - name: "pytest (Recommended)"
    estimatedTokens: 156
    keywords: [pytest, recommended]
  - name: "unittest (Standard Library)"
    estimatedTokens: 101
    keywords: [unittest, standard, library]
  - name: "nose2 (Less Common)"
    estimatedTokens: 15
    keywords: [nose2, less]
  - name: "Framework Comparison"
    estimatedTokens: 55
    keywords: [framework, comparison]
  - name: "Choosing a Framework"
    estimatedTokens: 42
    keywords: [choosing, framework]
  - name: "Related Context Files"
    estimatedTokens: 13
    keywords: [related, context, files]
tags: [python, testing, pytest, unittest, fixtures, assertions]
---

# Python Testing Frameworks

## Framework Detection

**Auto-detect from**:
1. `pytest.ini`, `pyproject.toml [tool.pytest]`, or `setup.cfg` → pytest
2. Imports: `import pytest` → pytest
3. Imports: `import unittest` or `from unittest import TestCase` → unittest
4. Test class inherits `unittest.TestCase` → unittest
5. Standalone `test_*.py` functions → likely pytest

## pytest (Recommended)

### Why pytest?

- Less boilerplate than unittest
- Better assertion introspection
- Powerful fixtures system
- Parametrization built-in
- Rich plugin ecosystem

### Key Features

**1. Simple Function-Based Tests**
```python
def test_addition():
    assert add(2, 3) == 5
```

**2. Fixtures for Setup**
```python
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

**3. Parametrization**
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert square(input) == expected
```

**4. Markers**
```python
@pytest.mark.slow
@pytest.mark.integration
def test_full_workflow():
    # Long-running test
```

**5. Fixture Scopes**
- `scope="function"` - Default, per test
- `scope="class"` - Per test class
- `scope="module"` - Per file
- `scope="session"` - Once per test run

### pytest Assertions

```python
assert value == expected
assert value is True
assert value is None
assert item in collection
assert "substring" in string
with pytest.raises(ValueError):
    function_that_raises()
with pytest.raises(ValueError, match="expected message"):
    function_that_raises()
```

### Async Support

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == expected
```

Requires: `pip install pytest-asyncio`

### Common pytest Plugins

- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking helpers
- `pytest-asyncio` - Async test support
- `pytest-xdist` - Parallel execution

Reference: [pytest Documentation](https://docs.pytest.org/)

---

## unittest (Standard Library)

### When to Use

- No external dependencies allowed
- Legacy codebase already using it
- Team preference for xUnit-style testing

### Key Features

**1. Class-Based Tests**
```python
import unittest

class TestMathOperations(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add(2, 3), 5)
```

**2. Setup/Teardown**
```python
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.connect()

    def tearDown(self):
        self.db.disconnect()

    def test_query(self):
        result = self.db.query("SELECT * FROM users")
        self.assertGreater(len(result), 0)
```

**3. Class-Level Setup**
```python
@classmethod
def setUpClass(cls):
    # Run once before all tests in class
    cls.shared_resource = expensive_setup()

@classmethod
def tearDownClass(cls):
    # Run once after all tests in class
    cls.shared_resource.cleanup()
```

### unittest Assertions

```python
self.assertEqual(a, b)
self.assertNotEqual(a, b)
self.assertTrue(x)
self.assertFalse(x)
self.assertIsNone(x)
self.assertIsNotNone(x)
self.assertIn(item, container)
self.assertRaises(ValueError, func, args)
self.assertRaisesRegex(ValueError, "pattern", func, args)
```

### Context Manager for Exceptions

```python
with self.assertRaises(ValueError) as context:
    function_that_raises()

self.assertIn("expected message", str(context.exception))
```

Reference: [unittest Documentation](https://docs.python.org/3/library/unittest.html)

---

## nose2 (Less Common)

Compatible with unittest, extends it with:
- Test discovery
- Plugins
- Parametrization

**Note**: Consider pytest instead for new projects.

---

## Framework Comparison

| Feature | pytest | unittest |
|---------|--------|----------|
| Syntax | Simple functions | Classes with methods |
| Assertions | Plain `assert` | `self.assert*()` methods |
| Setup | Fixtures | setUp/tearDown |
| Parametrization | Built-in decorator | Manual or 3rd party |
| Async support | Via plugin | Built-in (Python 3.8+) |
| Dependencies | Requires install | Standard library |
| Boilerplate | Minimal | More verbose |

---

## Choosing a Framework

**Use pytest if**:
- Starting new project
- Want modern, clean syntax
- Need powerful features (fixtures, parametrization)
- Team is comfortable with pytest

**Use unittest if**:
- Cannot install dependencies
- Maintaining existing unittest codebase
- Team prefers xUnit-style testing
- Need only standard library

**Migration path**: pytest can run unittest tests, enabling gradual migration.

---

## Related Context Files

- `unit_testing_standards.md` - Core testing principles
- `mocking_patterns.md` - Framework-specific mocking
- `test_antipatterns.md` - Framework-agnostic mistakes to avoid
