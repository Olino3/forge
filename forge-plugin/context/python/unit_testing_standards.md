---
id: "python/unit_testing_standards"
domain: python
title: "Python Unit Testing Standards"
type: pattern
estimatedTokens: 600
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Core Principles"
    estimatedTokens: 124
    keywords: [core, principles]
  - name: "Quick Reference"
    estimatedTokens: 51
    keywords: [quick, reference]
  - name: "Testing Patterns"
    estimatedTokens: 74
    keywords: [testing, patterns]
  - name: "References"
    estimatedTokens: 15
    keywords: [references]
  - name: "Related Context Files"
    estimatedTokens: 14
    keywords: [related, context, files]
tags: [python, testing, unit-tests, aaa-pattern, naming, coverage]
---

# Python Unit Testing Standards

## Core Principles

### Test Quality Fundamentals

1. **Test Behavior, Not Implementation**
   - Focus on what the code does, not how it does it
   - Tests should survive refactoring if behavior unchanged
   - Reference: [Testing on the Toilet: Test Behavior, Not Implementation](https://testing.googleblog.com/)

2. **AAA Pattern** (Arrange-Act-Assert)
   - Arrange: Set up test data and conditions
   - Act: Execute the function/method under test
   - Assert: Verify expected outcome
   - Clear separation improves readability

3. **Test Independence**
   - Each test runs in isolation
   - No shared state between tests
   - Order of execution doesn't matter
   - Use fixtures/setUp for common initialization

### Naming Conventions

**Function-based tests**:
```
test_should_{expected_behavior}_when_{condition}
```

**Examples**:
- `test_should_return_user_when_valid_id_provided`
- `test_should_raise_error_when_username_duplicate`
- `test_should_filter_results_when_query_string_given`

### Test Coverage Strategy

**Priority order**:
1. Happy path (normal expected usage)
2. Common edge cases (boundaries, empty inputs)
3. Error scenarios (exceptions, invalid inputs)
4. Integration points (external dependencies)

**Coverage goals**:
- Critical business logic: Aim for high coverage
- Simple getters/setters: Low priority
- Third-party code: Don't test
- Focus on value, not percentage

## Quick Reference

### Good Test Characteristics

- ✅ **Fast**: Runs in milliseconds
- ✅ **Isolated**: No external dependencies
- ✅ **Repeatable**: Same result every time
- ✅ **Self-validating**: Clear pass/fail
- ✅ **Timely**: Written close to code

### Bad Test Characteristics

- ❌ **Slow**: Takes seconds or minutes
- ❌ **Brittle**: Breaks on refactoring
- ❌ **Flaky**: Intermittent failures
- ❌ **Obscure**: Unclear what's being tested
- ❌ **Coupled**: Tests interdependent

## Testing Patterns

### Single Assertion (Preferred)

Each test should verify one logical concept:

```python
def test_should_create_user_with_hashed_password():
    user = create_user("alice", "password123")
    assert is_password_hashed(user.password)

def test_should_create_user_with_correct_username():
    user = create_user("alice", "password123")
    assert user.username == "alice"
```

### Multiple Assertions (When Grouped Logically)

Acceptable when testing related properties of same operation:

```python
def test_should_transform_user_data_correctly():
    result = transform_user_data(raw_data)

    # Structure assertions
    assert isinstance(result, dict)
    assert "user" in result

    # Value assertions
    assert result["user"]["name"] == "Alice"
    assert result["user"]["active"] is True
```

### Test Fixtures

**Reusable test data or setup**:

pytest:
```python
@pytest.fixture
def sample_user():
    return User(username="test", email="test@example.com")
```

unittest:
```python
def setUp(self):
    self.user = User(username="test", email="test@example.com")
```

## References

- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Effective Python Testing with Pytest](https://realpython.com/pytest-python-testing/)
- [Google Testing Blog](https://testing.googleblog.com/)
- [Martin Fowler on Testing](https://martinfowler.com/testing/)

## Related Context Files

- `testing_frameworks.md` - Framework-specific patterns
- `mocking_patterns.md` - Mocking and patching strategies
- `test_antipatterns.md` - Common mistakes to avoid
