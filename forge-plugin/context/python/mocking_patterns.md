---
id: "python/mocking_patterns"
domain: python
title: "Python Mocking Patterns"
type: pattern
estimatedTokens: 1150
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "When to Mock"
    estimatedTokens: 57
    keywords: [mock]
  - name: "unittest.mock (Standard Library)"
    estimatedTokens: 187
    keywords: [unittestmock, standard, library]
  - name: "pytest-mock (pytest Plugin)"
    estimatedTokens: 51
    keywords: [pytest-mock, pytest, plugin]
  - name: "AsyncMock (Python 3.8+)"
    estimatedTokens: 22
    keywords: [asyncmock, python]
  - name: "Common Patterns"
    estimatedTokens: 100
    keywords: [patterns]
  - name: "Anti-Patterns"
    estimatedTokens: 78
    keywords: [anti-patterns]
  - name: "MagicMock vs Mock"
    estimatedTokens: 28
    keywords: [magicmock, mock]
  - name: "Quick Reference"
    estimatedTokens: 57
    keywords: [quick, reference]
  - name: "Related Context Files"
    estimatedTokens: 15
    keywords: [related, context, files]
tags: [python, testing, mocking, patch, unittest-mock, pytest-mock]
---

# Python Mocking Patterns

## When to Mock

### DO Mock

- ✅ External APIs/services
- ✅ Database connections
- ✅ File system operations
- ✅ Time/date operations (`datetime.now()`, `time.time()`)
- ✅ Random operations (`random.random()`)
- ✅ Environment variables
- ✅ Network calls
- ✅ Expensive computations
- ✅ Non-deterministic operations

### DON'T Mock

- ❌ Code under test
- ❌ Simple data structures (lists, dicts)
- ❌ Language built-ins (unless necessary)
- ❌ Everything (over-mocking makes tests fragile)
- ❌ Internal implementation details

## unittest.mock (Standard Library)

### Basic Mock Object

```python
from unittest.mock import Mock

# Create mock
mock_service = Mock()

# Configure return value
mock_service.get_user.return_value = {"id": 1, "name": "Alice"}

# Call it
result = mock_service.get_user(123)

# Verify
mock_service.get_user.assert_called_once_with(123)
```

### patch Decorator

**Patch where it's used, not where it's defined**:

```python
# In module: app/services/user_service.py
from app.database import DatabaseConnection

def get_user(user_id):
    db = DatabaseConnection()
    return db.fetch(user_id)

# In test: Patch where DatabaseConnection is used
from unittest.mock import patch

@patch('app.services.user_service.DatabaseConnection')
def test_get_user(mock_db_class):
    mock_db_instance = mock_db_class.return_value
    mock_db_instance.fetch.return_value = {"id": 1}

    result = get_user(1)

    assert result["id"] == 1
    mock_db_instance.fetch.assert_called_once_with(1)
```

### patch.object

Mock a specific method/attribute:

```python
@patch.object(MyClass, 'method_to_mock')
def test_something(mock_method):
    mock_method.return_value = "mocked"
```

### patch.multiple

Mock multiple things at once:

```python
@patch.multiple('app.services.user_service',
                DatabaseConnection=Mock(),
                EmailService=Mock())
def test_create_user(DatabaseConnection, EmailService):
    # Both are mocked
```

### Context Manager

```python
def test_with_context_manager():
    with patch('module.function') as mock_func:
        mock_func.return_value = 42
        result = function_under_test()
        assert result == 42
```

### Mock Side Effects

**Different returns on successive calls**:
```python
mock.side_effect = [1, 2, 3]
assert mock() == 1
assert mock() == 2
assert mock() == 3
```

**Raise exception**:
```python
mock.side_effect = ValueError("error message")
mock()  # Raises ValueError
```

**Custom function**:
```python
def custom_behavior(arg):
    return arg * 2

mock.side_effect = custom_behavior
assert mock(5) == 10
```

### Assertions

```python
# Called?
mock.assert_called()
mock.assert_called_once()
mock.assert_not_called()

# Called with specific args?
mock.assert_called_with(arg1, arg2, kwarg=value)
mock.assert_called_once_with(arg1, arg2)

# Any calls with these args?
mock.assert_any_call(arg1, arg2)

# Check call list
assert mock.call_count == 3
assert mock.call_args_list == [call(1), call(2), call(3)]
```

Reference: [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

---

## pytest-mock (pytest Plugin)

### mocker Fixture

Simpler syntax for pytest:

```python
def test_with_mocker(mocker):
    # Patch
    mock = mocker.patch('module.function')
    mock.return_value = 42

    result = function_under_test()

    assert result == 42
    mock.assert_called_once()
```

### spy

Monitor real object calls:

```python
def test_with_spy(mocker):
    spy = mocker.spy(MyClass, 'method')

    obj = MyClass()
    obj.method(123)  # Real method is called

    spy.assert_called_once_with(123)
```

### stub

Return value without calling real code:

```python
def test_with_stub(mocker):
    mocker.patch('module.expensive_function', return_value=42)
```

Reference: [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)

---

## AsyncMock (Python 3.8+)

For async functions:

```python
from unittest.mock import AsyncMock, patch

@patch('module.async_function', new_callable=AsyncMock)
async def test_async(mock_async):
    mock_async.return_value = {"result": "success"}

    result = await function_under_test()

    assert result == {"result": "success"}
    mock_async.assert_awaited_once()
```

---

## Common Patterns

### Mock Database

```python
@patch('app.database.Database')
def test_with_mock_db(mock_db_class):
    # Mock the class and instance
    mock_db = mock_db_class.return_value
    mock_db.query.return_value = [{"id": 1}]

    result = service.get_all_users()

    assert len(result) == 1
    mock_db.query.assert_called_once()
```

### Mock datetime.now()

```python
from datetime import datetime
from unittest.mock import patch

@patch('module.datetime')
def test_with_fixed_time(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)

    result = function_that_uses_datetime_now()

    assert result.hour == 12
```

### Mock File Operations

```python
from unittest.mock import mock_open, patch

@patch('builtins.open', new_callable=mock_open, read_data='file content')
def test_file_read(mock_file):
    result = function_that_reads_file('path/to/file')

    assert 'file content' in result
    mock_file.assert_called_once_with('path/to/file')
```

### Mock Environment Variables

```python
@patch.dict('os.environ', {'API_KEY': 'test-key'})
def test_with_env_var():
    result = function_using_env_var()
    assert result == 'test-key'
```

### Mock requests (HTTP)

```python
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"data": "value"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = fetch_from_api()

    assert result["data"] == "value"
```

---

## Anti-Patterns

### Over-Mocking

**Bad** - Mocks too much:
```python
@patch('module.list')
@patch('module.dict')
@patch('module.str')
def test_something(mock_str, mock_dict, mock_list):
    # Mocking built-ins unnecessarily
```

**Good** - Mock only external dependencies:
```python
@patch('module.external_api_call')
def test_something(mock_api):
    # Mock only what's necessary
```

### Mocking What You're Testing

**Bad**:
```python
@patch('module.function_under_test')
def test_function(mock_func):
    mock_func.return_value = "expected"
    # Not actually testing anything!
```

### Not Resetting Mocks

Use `@patch` decorator or context manager to auto-cleanup.

### Tight Coupling to Implementation

**Bad** - Tests internal calls:
```python
def test_internal_implementation():
    mock_helper.assert_called_with(internal_arg)
    # Brittle - breaks on refactoring
```

**Good** - Tests public behavior:
```python
def test_public_behavior():
    result = public_function()
    assert result == expected
```

---

## MagicMock vs Mock

**MagicMock**: Supports magic methods (`__len__`, `__str__`, etc.)

```python
from unittest.mock import MagicMock

mock = MagicMock()
len(mock)  # Works
str(mock)  # Works

regular_mock = Mock()
len(regular_mock)  # Raises TypeError
```

Use `MagicMock` when mocking objects with magic methods.

---

## Quick Reference

| Task | Code |
|------|------|
| Basic mock | `mock = Mock()` |
| Return value | `mock.return_value = value` |
| Side effect | `mock.side_effect = exception` |
| Patch function | `@patch('module.func')` |
| Patch method | `@patch.object(Class, 'method')` |
| Mock file | `@patch('builtins.open', mock_open(...))` |
| Mock datetime | `@patch('module.datetime')` |
| Mock env var | `@patch.dict('os.environ', {...})` |
| Async mock | `AsyncMock()` |
| Assert called | `mock.assert_called_once_with(args)` |

---

## Related Context Files

- `unit_testing_standards.md` - Core testing principles
- `testing_frameworks.md` - pytest vs unittest mocking
- `test_antipatterns.md` - Mocking mistakes to avoid
