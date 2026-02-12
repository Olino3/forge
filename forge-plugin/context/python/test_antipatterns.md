---
id: "python/test_antipatterns"
domain: python
title: "Python Test Anti-Patterns"
type: pattern
estimatedTokens: 1700
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "What to Avoid When Writing Tests"
    estimatedTokens: 20
    keywords: [avoid, writing, tests]
  - name: "Testing Implementation Instead of Behavior"
    estimatedTokens: 54
    keywords: [testing, implementation, instead, behavior]
  - name: "Brittle Tests with Hard-Coded Values"
    estimatedTokens: 57
    keywords: [brittle, tests, hard-coded, values]
  - name: "Test Interdependence"
    estimatedTokens: 71
    keywords: [test, interdependence]
  - name: "Over-Mocking"
    estimatedTokens: 60
    keywords: [over-mocking]
  - name: "Testing Private Methods"
    estimatedTokens: 49
    keywords: [testing, private, methods]
  - name: "Generic Test Names"
    estimatedTokens: 46
    keywords: [generic, test, names]
  - name: "Multiple Unrelated Assertions"
    estimatedTokens: 65
    keywords: [multiple, unrelated, assertions]
  - name: "Ignoring Test Failures"
    estimatedTokens: 69
    keywords: [ignoring, test, failures]
  - name: "No Assertions"
    estimatedTokens: 44
    keywords: [assertions]
  - name: "Overly Complex Test Setup"
    estimatedTokens: 70
    keywords: [overly, complex, test, setup]
  - name: "Testing Frameworks Instead of Code"
    estimatedTokens: 48
    keywords: [testing, frameworks, instead, code]
  - name: "Sleep/Wait in Tests"
    estimatedTokens: 51
    keywords: [sleepwait, tests]
  - name: "Swallowing Exceptions in Tests"
    estimatedTokens: 54
    keywords: [swallowing, exceptions, tests]
  - name: "Not Testing Edge Cases"
    estimatedTokens: 54
    keywords: [not, testing, edge, cases]
  - name: "Quick Checklist"
    estimatedTokens: 68
    keywords: [quick, checklist]
  - name: "References"
    estimatedTokens: 12
    keywords: [references]
  - name: "Related Context Files"
    estimatedTokens: 12
    keywords: [related, context, files]
tags: [python, testing, antipatterns, code-quality, best-practices]
---

# Python Test Anti-Patterns

## What to Avoid When Writing Tests

This document catalogs common testing mistakes and how to fix them.

---

## 1. Testing Implementation Instead of Behavior

### Anti-Pattern

```python
def test_user_creation():
    # Testing internal implementation details
    assert user_service._validate_email.called
    assert user_service._hash_password.called
    assert user_service._database.insert.called
```

### Problem
- Tests break on refactoring (even if behavior unchanged)
- Couples tests to implementation
- Makes refactoring difficult

### Solution

```python
def test_should_create_user_with_valid_credentials():
    # Test observable behavior
    user = user_service.create_user("alice", "alice@example.com", "pass123")

    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.password_is_hashed is True
```

**Rule**: Test the "what", not the "how".

---

## 2. Brittle Tests with Hard-Coded Values

### Anti-Pattern

```python
def test_get_users():
    users = get_all_users()
    # Assumes specific database state
    assert len(users) == 47
    assert users[0].name == "Alice"
```

### Problem
- Fails when database changes
- Flaky in different environments
- Hard to maintain

### Solution

```python
def test_get_users():
    # Use controlled test data
    create_test_user("Alice")
    create_test_user("Bob")

    users = get_all_users()

    assert len(users) == 2
    assert any(u.name == "Alice" for u in users)
```

**Rule**: Control your test data, don't assume external state.

---

## 3. Test Interdependence

### Anti-Pattern

```python
class TestUserWorkflow:
    user_id = None

    def test_1_create_user(self):
        user = create_user("alice")
        TestUserWorkflow.user_id = user.id  # Storing state

    def test_2_update_user(self):
        # Depends on test_1 running first
        update_user(TestUserWorkflow.user_id, email="new@example.com")
```

### Problem
- Tests must run in specific order
- One failure causes cascade failures
- Can't run tests in isolation

### Solution

```python
class TestUserWorkflow:
    @pytest.fixture
    def user(self):
        return create_user("alice")

    def test_create_user(self):
        user = create_user("alice")
        assert user.username == "alice"

    def test_update_user(self, user):
        # Each test is independent
        updated = update_user(user.id, email="new@example.com")
        assert updated.email == "new@example.com"
```

**Rule**: Each test should be completely independent.

---

## 4. Over-Mocking

### Anti-Pattern

```python
@patch('module.calculate')
def test_something(mock_calculate):
    # Mocking the function we're trying to test!
    mock_calculate.return_value = 42

    result = calculate(2, 3)

    assert result == 42
```

### Problem
- Not actually testing the code
- False confidence
- Tests pass even if code is broken

### Solution

```python
@patch('module.external_api_call')
def test_something(mock_api):
    # Mock only external dependencies
    mock_api.return_value = {"data": "value"}

    result = process_data()  # Actual code runs

    assert result == expected_output
```

**Rule**: Mock external dependencies, not code under test.

---

## 5. Testing Private Methods

### Anti-Pattern

```python
def test_private_validation():
    service = UserService()
    # Testing private method directly
    assert service._validate_email("test@example.com") is True
```

### Problem
- Private methods are implementation details
- Couples tests to internal structure
- Makes refactoring harder

### Solution

```python
def test_should_reject_invalid_email():
    # Test through public interface
    service = UserService()

    with pytest.raises(ValidationError):
        service.create_user("alice", "invalid-email", "pass123")
```

**Rule**: Test only public interfaces. Private methods get tested indirectly.

---

## 6. Generic Test Names

### Anti-Pattern

```python
def test_user():
    # What does this test?
    ...

def test_function1():
    # Meaningless name
    ...

def test_edge_case():
    # Which edge case?
    ...
```

### Problem
- Unclear what's being tested
- Hard to understand failures
- Poor documentation

### Solution

```python
def test_should_create_user_when_valid_data_provided():
    ...

def test_should_raise_error_when_username_already_exists():
    ...

def test_should_handle_empty_string_in_description():
    ...
```

**Rule**: Names should describe expected behavior and conditions.

---

## 7. Multiple Unrelated Assertions

### Anti-Pattern

```python
def test_everything():
    # Tests multiple unrelated things
    assert create_user("alice") is not None
    assert delete_user(123) is True
    assert list_users() is not None
    assert update_password(1, "new") is True
```

### Problem
- First failure hides other issues
- Unclear what exactly failed
- Violates single responsibility

### Solution

```python
def test_should_create_user_successfully():
    user = create_user("alice")
    assert user is not None

def test_should_delete_user_when_exists():
    result = delete_user(123)
    assert result is True

def test_should_list_all_users():
    users = list_users()
    assert users is not None
```

**Rule**: One logical concept per test.

---

## 8. Ignoring Test Failures

### Anti-Pattern

```python
@pytest.mark.skip("Fails sometimes, will fix later")
def test_important_feature():
    ...

def test_something():
    try:
        result = flaky_function()
        assert result == expected
    except:
        pass  # Ignore failures
```

### Problem
- Technical debt accumulates
- Real issues get hidden
- False confidence

### Solution

```python
# Fix the test or the code
def test_important_feature():
    # Make deterministic
    with patch('module.random', return_value=0.5):
        result = previously_flaky_function()
        assert result == expected

# Or mark as expected to fail temporarily
@pytest.mark.xfail(reason="Known issue #123, fix in progress")
def test_known_issue():
    ...
```

**Rule**: Fix failing tests, don't ignore them.

---

## 9. No Assertions

### Anti-Pattern

```python
def test_process_data():
    # No assertions - just calling the function
    process_data(input_data)
```

### Problem
- Test always passes
- Not verifying anything
- Pointless test

### Solution

```python
def test_should_process_data_correctly():
    result = process_data(input_data)

    assert result is not None
    assert result.status == "success"
    assert len(result.items) == 3
```

**Rule**: Every test needs assertions (or expected exception).

---

## 10. Overly Complex Test Setup

### Anti-Pattern

```python
def test_user_workflow():
    # 50 lines of setup
    db = Database()
    db.connect()
    db.create_tables()
    db.insert(lots_of_data)
    user = User(...)
    role = Role(...)
    permission = Permission(...)
    # ... many more lines
    db.commit()

    # Actual test
    result = user.can_access(resource)
    assert result is True
```

### Problem
- Hard to understand
- Hard to maintain
- Hides actual test logic

### Solution

```python
@pytest.fixture
def setup_user_with_permissions():
    # Move complex setup to fixture
    user = create_test_user_with_role("admin")
    return user

def test_admin_should_access_resource(setup_user_with_permissions):
    user = setup_user_with_permissions

    result = user.can_access(resource)

    assert result is True
```

**Rule**: Extract complex setup to fixtures/helpers.

---

## 11. Testing Frameworks Instead of Code

### Anti-Pattern

```python
def test_django_orm():
    # Testing if Django ORM works
    user = User.objects.create(username="alice")
    assert User.objects.filter(username="alice").exists()
```

### Problem
- Testing third-party code
- Wasted effort
- No value added

### Solution

```python
def test_user_service_creates_user():
    # Test YOUR code's behavior
    service = UserService()
    user = service.create_user("alice", "alice@example.com")

    assert user.username == "alice"
    assert user.is_active is True
```

**Rule**: Test your code, not the framework/library.

---

## 12. Sleep/Wait in Tests

### Anti-Pattern

```python
import time

def test_async_process():
    start_background_task()
    time.sleep(5)  # Wait for completion
    assert task_completed()
```

### Problem
- Slow tests
- Flaky (timing-dependent)
- May not wait long enough

### Solution

```python
def test_async_process():
    # Use proper async testing
    result = await async_function()
    assert result == expected

# Or use polling with timeout
def test_with_polling():
    start_background_task()
    wait_until(lambda: task_completed(), timeout=5)
```

**Rule**: Use proper async testing, not sleep.

---

## 13. Swallowing Exceptions in Tests

### Anti-Pattern

```python
def test_function():
    try:
        result = might_raise_exception()
        assert result == expected
    except Exception:
        # Silently fail
        pass
```

### Problem
- Hides real errors
- Test passes when it should fail
- Makes debugging harder

### Solution

```python
def test_should_raise_exception_when_invalid():
    with pytest.raises(ValueError, match="expected message"):
        function_that_should_raise()

def test_should_succeed_with_valid_input():
    # Let exceptions propagate naturally
    result = function_with_valid_input()
    assert result == expected
```

**Rule**: Let exceptions fail tests unless specifically testing exception handling.

---

## 14. Not Testing Edge Cases

### Anti-Pattern

```python
def test_divide():
    # Only tests happy path
    assert divide(10, 2) == 5
```

### Problem
- Missing critical scenarios
- Bugs in edge cases
- Incomplete coverage

### Solution

```python
def test_divide_normal_numbers():
    assert divide(10, 2) == 5

def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_negative_numbers():
    assert divide(-10, 2) == -5

def test_divide_floats():
    assert abs(divide(10, 3) - 3.333) < 0.001
```

**Rule**: Test edge cases, boundaries, and error scenarios.

---

## Quick Checklist

Before committing tests, verify:

- [ ] Tests are independent (can run in any order)
- [ ] Test names describe behavior and conditions
- [ ] Mocking only external dependencies
- [ ] Testing behavior, not implementation
- [ ] Each test has clear assertions
- [ ] No hard-coded assumptions about external state
- [ ] Edge cases and errors tested
- [ ] No ignored/skipped tests without good reason
- [ ] Tests are fast (< 1 second each)
- [ ] Setup is clean (using fixtures)

---

## References

- [Test Smells Catalog](http://xunitpatterns.com/Test%20Smells.html)
- [Google Testing Blog: Test Smell](https://testing.googleblog.com/)
- [Martin Fowler: Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)

---

## Related Context Files

- `unit_testing_standards.md` - What TO do
- `testing_frameworks.md` - Framework-specific guidance
- `mocking_patterns.md` - Proper mocking techniques
