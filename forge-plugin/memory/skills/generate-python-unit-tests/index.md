# Memory Structure: generate-python-unit-tests

## Purpose

This directory stores **project-specific** testing patterns, expected behaviors, and conventions learned during unit test generation. Each project gets its own subdirectory to maintain isolated, project-specific knowledge.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/python/`): **Shared, static** testing standards (AAA pattern, pytest vs unittest, mocking best practices)
- **Memory** (this directory): **Project-specific, dynamic** testing patterns (this project's test location, fixtures, expected behaviors)

**Example**:
- Context says: "Use descriptive test names like `test_should_X_when_Y`"
- Memory records: "In this project, tests go in `tests/unit/`, use `conftest.py` for shared fixtures, and all API tests mock `requests` library"

## Directory Structure

```
generate-python-unit-tests/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── testing_patterns.md     # Test file conventions and framework setup
    ├── expected_behaviors.md   # User-clarified behaviors and business logic
    ├── common_fixtures.md      # Reusable test fixtures and test data
    └── framework_config.md     # Testing framework configuration details
```

## Memory Files

### 1. `testing_patterns.md`

**What to store**:
- Test file location pattern (e.g., `tests/unit/`, `tests/`, co-located with source)
- Test file naming convention (e.g., `test_*.py` vs `*_test.py`)
- Testing framework (pytest, unittest, specific version)
- Project conventions (class-based vs function-based tests)
- Common patterns observed (parametrization usage, fixture patterns)
- Test organization structure (by feature, by layer, etc.)

**Example content**:
```markdown
# Testing Patterns for {project-name}

## Test File Structure
- Location: `tests/unit/{module_path}/test_{module_name}.py`
- Mirror source structure: `app/services/user.py` → `tests/unit/services/test_user.py`

## Framework
- pytest 7.4.0
- Plugins: pytest-asyncio, pytest-cov, pytest-mock

## Conventions
- Function-based tests (not class-based)
- Heavy use of parametrization for multiple cases
- Fixtures in `conftest.py` at each level
- Markers: @pytest.mark.slow, @pytest.mark.integration
```

### 2. `expected_behaviors.md`

**What to store**:
- User-clarified expected behaviors from Socratic planning
- Business logic rules and constraints
- Edge case handling decisions
- Error scenarios and expected exceptions
- Input validation rules
- Output format specifications
- Domain-specific behaviors

**Example content**:
```markdown
# Expected Behaviors for {project-name}

## User Service

### create_user
- **Valid email**: Must match regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **Password requirements**: Min 8 chars, at least 1 uppercase, 1 number
- **Duplicate username**: Raise `UserExistsError` with message "Username already taken"
- **Side effects**: Send welcome email via EmailService (should be mocked)

### update_user
- **Allowed fields**: email, profile (name, bio, avatar_url)
- **Cannot change**: username, created_at
- **Not found**: Raise `NotFoundError` if user doesn't exist
- **Cache invalidation**: Should call `cache.invalidate(f"user:{user_id}")`

## Payment Processor

### process_refund
- **Time limit**: Refunds allowed within 30 days of payment
- **Status check**: Only COMPLETED payments can be refunded
- **Partial refunds**: Allowed, must be less than original amount
```

### 3. `common_fixtures.md`

**What to store**:
- Reusable test fixtures created for the project
- Test data factories and builders
- Mock object configurations
- Shared setup/teardown patterns
- Common test scenarios
- Database/API mocking patterns

**Example content**:
```markdown
# Common Fixtures for {project-name}

## User Fixtures

### sample_user
```python
@pytest.fixture
def sample_user():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at=datetime(2025, 1, 1)
    )
```

### admin_user
```python
@pytest.fixture
def admin_user():
    return User(
        id=999,
        username="admin",
        email="admin@example.com",
        role="admin"
    )
```

## Mock Services

### mock_database
```python
@pytest.fixture
def mock_database():
    db = Mock(spec=Database)
    db.query.return_value = []
    db.execute.return_value = True
    return db
```

### mock_email_service
```python
@pytest.fixture
def mock_email_service():
    service = Mock(spec=EmailService)
    service.send.return_value = {"status": "sent"}
    return service
```

## Test Data

### valid_user_data
```python
@pytest.fixture
def valid_user_data():
    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "SecurePass123"
    }
```
```

### 4. `framework_config.md`

**What to store**:
- pytest.ini / pyproject.toml test configuration
- conftest.py patterns and structure
- Plugin usage and settings
- Coverage configuration
- Test markers and their meanings
- Custom pytest hooks
- Test discovery patterns

**Example content**:
```markdown
# Framework Configuration for {project-name}

## pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    asyncio: marks tests as async
addopts = -ra -q --strict-markers --cov=app --cov-report=html
```

## conftest.py Structure

### Root conftest.py
- Database session fixture
- Application instance fixture
- Mock external services

### Module-level conftest.py
- `tests/services/conftest.py`: Service-specific fixtures
- `tests/api/conftest.py`: API client fixture, request fixtures

## Plugins
- pytest-asyncio: Auto-enable with `asyncio_mode = auto`
- pytest-cov: Coverage reporting
- pytest-mock: mocker fixture (used project-wide)

## Custom Hooks
```python
@pytest.fixture(autouse=True)
def reset_database(database):
    # Runs before each test
    database.reset()
    yield
    database.cleanup()
```
```

## Workflow

### When Creating Memory (First Time)

1. **During Step 1 (Initial Analysis)**:
   - Identify project name from repository/directory
   - Check if `{project-name}/` directory exists
   - If not exists, note that memory will be created in Step 8

2. **During Step 3 (Load Project Memory)**:
   - If directory doesn't exist: Note this is the first time
   - Continue with empty memory

3. **During Step 8 (Update Memory)**:
   - Create `{project-name}/` directory
   - Create all four memory files with initial content
   - Document patterns observed during generation
   - Store user-clarified behaviors from Socratic phase

### When Using Existing Memory (Subsequent Times)

1. **During Step 3 (Load Project Memory)**:
   - Read all existing memory files
   - Use patterns to guide test generation
   - Apply known expected behaviors

2. **During Step 8 (Update Memory)**:
   - **Append** new patterns discovered
   - **Update** existing patterns if they've evolved
   - **Add** new expected behaviors learned
   - **Expand** fixture library with new reusable fixtures
   - Keep memory files organized and up-to-date

## Memory Evolution

Memory should grow and improve over time:

### First Invocation
- Establish basic patterns (file location, framework)
- Document initial expected behaviors from user
- Create first fixtures

### Subsequent Invocations
- Refine patterns based on new code
- Add new expected behaviors
- Expand fixture library
- Update framework config as project evolves
- Consolidate common patterns

### Maintenance
- Keep memory files concise and relevant
- Remove outdated patterns
- Update when project conventions change
- Ensure consistency across all files

## Best Practices

1. **Be Specific**: "Tests in `tests/unit/`" not "Tests in tests folder"
2. **Include Examples**: Show actual code snippets, not just descriptions
3. **Date Decisions**: Note when behaviors were clarified and by whom (if relevant)
4. **Link to Source**: Reference specific files/modules where patterns apply
5. **Keep Current**: Update when project structure or conventions change
6. **Avoid Duplication**: Don't duplicate what's in context files
7. **Focus on Differences**: Store what makes THIS project unique

## Example Memory Usage

```python
# In Step 3: Load project memory
memory_files = [
    "testing_patterns.md",      # Load test location, framework info
    "expected_behaviors.md",    # Load known behaviors
    "common_fixtures.md",       # Load reusable fixtures
    "framework_config.md"       # Load pytest config
]

# Use memory during generation (Step 7)
# - Place test file according to testing_patterns.md
# - Apply expected behaviors from expected_behaviors.md
# - Reuse fixtures from common_fixtures.md
# - Follow framework config from framework_config.md

# In Step 8: Update memory with new learnings
# - Add new test location pattern (if different)
# - Document new expected behaviors clarified by user
# - Add new fixtures created
# - Update framework config if changed
```

## Related Files

- `../../../context/python/unit_testing_standards.md` - Universal testing principles
- `../../../context/python/testing_frameworks.md` - pytest/unittest patterns
- `../../../context/python/mocking_patterns.md` - Mocking strategies
- `../../../context/python/test_antipatterns.md` - What to avoid
- `../../index.md` - Overall memory system explanation
