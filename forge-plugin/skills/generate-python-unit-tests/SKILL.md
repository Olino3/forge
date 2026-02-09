# generate-python-unit-tests

## Title

**Python Unit Test Generator** - Intelligent unit test generation with Socratic planning and project-specific memory.

## Version

**v1.0.0** - Initial release

## File Structure

```
forge-plugin/
├── context/
│   └── python/
│       ├── index.md                          # Context navigation (READ FIRST)
│       ├── unit_testing_standards.md         # Unit testing best practices
│       ├── testing_frameworks.md             # pytest, unittest, etc.
│       ├── mocking_patterns.md               # Mock/patch patterns
│       └── test_antipatterns.md              # What to avoid
├── memory/
│   ├── index.md                              # Memory system guide (READ FIRST)
│   └── skills/
│       └── generate-python-unit-tests/
│           ├── index.md                      # Memory structure for this skill
│           └── {project-name}/               # Per-project memory
│               ├── testing_patterns.md       # Project's testing conventions
│               ├── expected_behaviors.md     # Known expected behaviors
│               ├── common_fixtures.md        # Reusable test fixtures
│               └── framework_config.md       # Testing framework setup
└── skills/
    └── generate-python-unit-tests/
        ├── SKILL.md                          # This file
        ├── examples.md                       # Usage examples
        ├── scripts/
        │   └── test_analyzer.py              # Helper for analyzing existing tests
        └── templates/
            ├── test_file_template.txt        # Standard test file structure
            └── test_case_template.txt        # Individual test case template
```

## Required Reading

### Mandatory Reads (Always Load These)

**Before starting any test generation, you MUST read these files in order:**

1. **Memory System Navigation**:
   - `../../memory/index.md` - Understand memory vs context
   - `../../memory/skills/generate-python-unit-tests/index.md` - Memory structure for this skill

2. **Context System Navigation**:
   - `../../context/index.md` - Context system overview
   - `../../context/python/index.md` - Python context navigation and framework detection

3. **Project-Specific Memory** (if exists):
   - `../../memory/skills/generate-python-unit-tests/{project-name}/testing_patterns.md`
   - `../../memory/skills/generate-python-unit-tests/{project-name}/expected_behaviors.md`
   - `../../memory/skills/generate-python-unit-tests/{project-name}/common_fixtures.md`
   - `../../memory/skills/generate-python-unit-tests/{project-name}/framework_config.md`

4. **Python Testing Context** (load based on context/python/index.md guidance):
   - `../../context/python/unit_testing_standards.md` - Core testing principles
   - `../../context/python/testing_frameworks.md` - Framework-specific patterns
   - `../../context/python/mocking_patterns.md` - Mocking best practices
   - `../../context/python/test_antipatterns.md` - What to avoid

5. **Additional Context** (conditional, based on code analysis):
   - Load other context files from `../../context/python/` as needed for the specific code being tested

### File Reading Order

**CRITICAL**: Files must be read in this exact order:

```
1. Memory indexes (understand what memory exists)
2. Context indexes (understand what context is available)
3. Project memory (load project-specific patterns)
4. Core context (testing standards, frameworks)
5. Conditional context (based on code being tested)
```

## Design Requirements

### Core Principles

1. **Practical Tests**: Generate tests that validate real behavior, not implementation details
2. **Maintainability**: Tests should be easy to understand and update
3. **Non-Brittleness**: Tests should not break on refactoring unless behavior changes
4. **Socratic Planning**: Collaborate with user to understand expected behavior
5. **Project Memory**: Learn and apply project-specific testing patterns
6. **Framework Awareness**: Support pytest, unittest, and other frameworks
7. **Comprehensive Coverage**: Include happy paths, edge cases, and error scenarios

### Test Quality Criteria

Generated tests must:

- ✅ Test behavior, not implementation
- ✅ Have clear, descriptive names (test_should_X_when_Y)
- ✅ Follow AAA pattern (Arrange, Act, Assert)
- ✅ Be independent and isolated
- ✅ Use appropriate mocking/patching
- ✅ Include meaningful assertions
- ✅ Document complex test scenarios
- ✅ Follow project conventions from memory

### What NOT to Do

- ❌ Test private methods directly
- ❌ Create brittle tests tied to implementation
- ❌ Generate tests without understanding expected behavior
- ❌ Ignore existing project testing patterns
- ❌ Over-mock or under-mock
- ❌ Skip error/edge case scenarios
- ❌ Use generic test names

## Prompting Guidelines

### User Interaction Phases

**Phase 1: Initial Analysis**
- Identify files to test
- Analyze existing test structure
- Detect testing framework

**Phase 2: Socratic Planning** (MANDATORY)
- Ask targeted questions about expected behavior
- Clarify edge cases and error scenarios
- Understand business logic and constraints
- Confirm testing approach

**Phase 3: Test Generation**
- Generate tests based on planning
- Apply project memory patterns
- Follow testing standards

### Socratic Questions Framework

Ask questions in these categories:

1. **Behavior Understanding**:
   - "What should happen when [normal input]?"
   - "How should the function behave when [edge case]?"
   - "What errors should be raised when [invalid input]?"

2. **Dependencies & Integration**:
   - "Should I mock [dependency] or use real instances?"
   - "What external services need to be mocked?"
   - "Are there database/file system interactions to consider?"

3. **Business Logic**:
   - "What business rules govern [functionality]?"
   - "Are there constraints or validations I should test?"
   - "What are the success/failure criteria?"

4. **Test Approach**:
   - "Do you prefer parameterized tests or individual test cases?"
   - "Should I include integration tests or focus on unit tests?"
   - "Are there specific scenarios you're concerned about?"

## Instructions

### Mandatory Workflow (8 Steps)

This workflow is **MANDATORY** and **NON-NEGOTIABLE**. Every step must be completed in order.

---

#### Step 1: Initial Analysis

**Purpose**: Gather information about what needs to be tested.

**Actions**:
1. Identify the Python file(s) or module(s) to test
2. Determine the project name from git repository or directory structure
3. Check if tests already exist for the target files
4. Identify the testing framework (pytest, unittest, etc.)
5. List the functions/classes/methods that need test coverage

**Validation**:
- [ ] Target files identified
- [ ] Project name determined
- [ ] Testing framework detected
- [ ] Functions/classes to test listed

---

#### Step 2: Load Index Files

**Purpose**: Understand what memory and context is available.

**Actions**:
1. Read `../../memory/index.md` to understand memory system
2. Read `../../memory/skills/generate-python-unit-tests/index.md` for skill-specific memory structure
3. Read `../../context/index.md` for context system overview
4. Read `../../context/python/index.md` for Python context navigation

**Validation**:
- [ ] Memory system understood
- [ ] Skill memory structure known
- [ ] Context system understood
- [ ] Python context map loaded

---

#### Step 3: Load Project Memory

**Purpose**: Load project-specific testing patterns and conventions.

**Actions**:
1. Check if `../../memory/skills/generate-python-unit-tests/{project-name}/` exists
2. If exists, read all memory files:
   - `testing_patterns.md` - Project's testing conventions
   - `expected_behaviors.md` - Known expected behaviors
   - `common_fixtures.md` - Reusable test fixtures
   - `framework_config.md` - Testing framework setup
3. If doesn't exist, note that this is a new project (memory will be created later)

**Validation**:
- [ ] Project memory checked
- [ ] Existing patterns loaded (if available)
- [ ] Ready to create new memory (if needed)

---

#### Step 4: Load Context

**Purpose**: Load testing standards and best practices.

**Actions**:
1. **Always load**:
   - `../../context/python/unit_testing_standards.md`
   - `../../context/python/testing_frameworks.md`
   - `../../context/python/mocking_patterns.md`
   - `../../context/python/test_antipatterns.md`

2. **Conditionally load** (based on code analysis):
   - If async code: load async patterns
   - If Django/Flask/FastAPI: load framework-specific context
   - If database code: load data testing patterns
   - Use `../../context/python/index.md` as guide

**Validation**:
- [ ] Core testing context loaded
- [ ] Framework-specific context loaded (if needed)
- [ ] Ready to apply testing standards

---

#### Step 5: Analyze Files to Test

**Purpose**: Understand the code structure and dependencies.

**Actions**:
1. Read the target Python file(s) completely
2. Identify:
   - Public functions/methods (primary test targets)
   - Function signatures and parameters
   - Dependencies (imports, external services)
   - Error handling (exceptions raised)
   - Complexity and edge cases
3. Read existing tests (if any) to understand coverage gaps
4. Analyze project structure to determine test file location

**Validation**:
- [ ] Target code thoroughly understood
- [ ] Dependencies identified
- [ ] Edge cases noted
- [ ] Test file location determined

---

#### Step 6: Socratic Planning Phase

**Purpose**: Collaborate with the user to understand expected behavior.

**CRITICAL**: This step is MANDATORY. You MUST ask the user questions before generating tests.

**Actions**:
1. Present a summary of what you analyzed
2. Ask targeted questions using the Socratic Questions Framework:
   - **Behavior questions**: Expected outputs, edge cases, errors
   - **Dependency questions**: What to mock, external services
   - **Business logic questions**: Rules, constraints, validations
   - **Testing approach questions**: Style preferences, test types
3. Wait for user responses
4. Use AskUserQuestion tool for structured multi-choice questions when appropriate
5. Clarify ambiguities and confirm understanding

**Example Questions**:
```
I analyzed `user_service.py` and found 3 functions to test:
- create_user(username, email, password)
- authenticate_user(username, password)
- delete_user(user_id)

Before generating tests, I need to understand the expected behavior:

1. **For create_user**:
   - What should happen if username already exists?
   - Should it validate email format?
   - What password requirements should I test?

2. **For authenticate_user**:
   - Should I mock the database lookup?
   - What happens with invalid credentials?
   - Are there rate limiting or security concerns?

3. **For delete_user**:
   - What happens if user doesn't exist?
   - Should it handle cascade deletions?
   - Are there permission checks to test?

4. **General**:
   - Do you prefer pytest or unittest?
   - Should I use fixtures for common setup?
```

**Validation**:
- [ ] Summary presented to user
- [ ] At least 3-5 meaningful questions asked
- [ ] User responses received
- [ ] Expected behaviors clarified
- [ ] Testing approach confirmed

---

#### Step 7: Generate Unit Tests

**Purpose**: Create comprehensive, maintainable unit tests.

**Actions**:
1. Create test file following project conventions:
   - File naming: `test_{module_name}.py` or `{module_name}_test.py`
   - Location: Based on project structure (e.g., `tests/`, `test/`, same directory)
2. Apply templates from `./templates/test_file_template.txt`
3. For each function/method:
   - Generate happy path tests
   - Generate edge case tests
   - Generate error scenario tests
   - Use AAA pattern (Arrange, Act, Assert)
4. Include:
   - Descriptive test names (test_should_X_when_Y)
   - Appropriate mocks/patches
   - Fixtures for common setup
   - Docstrings for complex tests
5. Apply project memory patterns and user's clarified behaviors
6. Follow framework-specific conventions (pytest vs unittest)

**Validation**:
- [ ] Test file created in correct location
- [ ] All functions have test coverage
- [ ] Happy paths tested
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] Project conventions followed
- [ ] User's expected behaviors implemented

---

#### Step 8: Update Project Memory

**Purpose**: Store learned patterns for future test generation.

**Actions**:
1. If project memory doesn't exist, create:
   - `../../memory/skills/generate-python-unit-tests/{project-name}/`
2. Create or update memory files:
   - **testing_patterns.md**: Document testing conventions observed/established
     - Test file location pattern
     - Naming conventions
     - Testing framework and version
     - Common patterns used
   - **expected_behaviors.md**: Document clarified behaviors from Socratic phase
     - Function behaviors confirmed with user
     - Edge case handling rules
     - Error scenarios and expected exceptions
   - **common_fixtures.md**: Document reusable test fixtures created
     - Shared setup code
     - Common mock objects
     - Test data factories
   - **framework_config.md**: Document testing framework configuration
     - pytest.ini / setup.cfg settings
     - Conftest.py patterns
     - Plugin usage

**Validation**:
- [ ] Project memory directory exists
- [ ] testing_patterns.md created/updated
- [ ] expected_behaviors.md created/updated
- [ ] common_fixtures.md created/updated
- [ ] framework_config.md created/updated

---

## Compliance Checklist

Before completing the skill invocation, verify ALL items:

### Workflow Compliance
- [ ] Step 1: Initial Analysis completed
- [ ] Step 2: Index files loaded
- [ ] Step 3: Project memory loaded
- [ ] Step 4: Context loaded
- [ ] Step 5: Files analyzed
- [ ] Step 6: Socratic planning completed (questions asked and answered)
- [ ] Step 7: Tests generated
- [ ] Step 8: Memory updated

### Test Quality
- [ ] Tests follow AAA pattern
- [ ] Test names are descriptive
- [ ] Appropriate mocking used
- [ ] Edge cases covered
- [ ] Error scenarios covered
- [ ] Tests are independent
- [ ] Project conventions followed

### Memory & Context
- [ ] Project memory checked and loaded
- [ ] New patterns documented in memory
- [ ] User-clarified behaviors stored
- [ ] Testing context applied

### User Collaboration
- [ ] Socratic questions asked (minimum 3-5)
- [ ] User responses incorporated
- [ ] Expected behaviors confirmed

## Best Practices

### Test Organization

1. **File Structure**:
   - Mirror source code structure in tests
   - One test file per source file (generally)
   - Group related tests in classes

2. **Test Naming**:
   - `test_should_{expected_behavior}_when_{condition}`
   - Be specific and descriptive
   - Use underscores for readability

3. **Test Independence**:
   - Each test should run independently
   - Use fixtures for setup/teardown
   - Avoid test interdependencies

### Mocking Strategy

1. **What to Mock**:
   - External services (APIs, databases)
   - File system operations
   - Time/date operations
   - Random number generation
   - Expensive computations

2. **What NOT to Mock**:
   - Code under test
   - Simple data structures
   - Language built-ins (unless necessary)

### Coverage Strategy

1. **Priority Order**:
   - Happy path (normal operation)
   - Common edge cases
   - Error scenarios
   - Boundary conditions
   - Integration points

2. **Sufficiency**:
   - Aim for meaningful coverage, not 100%
   - Focus on critical business logic
   - Test public interfaces

## Additional Notes

### Testing Frameworks

**pytest** (preferred):
- Use fixtures for setup
- Parametrize tests for multiple cases
- Use markers for categorization
- Leverage pytest plugins

**unittest**:
- Use setUp/tearDown for fixtures
- Subclass unittest.TestCase
- Use self.assert* methods
- Mock with unittest.mock

### Integration with Other Skills

- **Before testing**: Use `skill:python-code-review` to understand code quality
- **After testing**: Review generated tests with `skill:python-code-review`
- **For changes**: Use `skill:get-git-diff` to see what changed and needs new tests

### Common Patterns

1. **Fixtures**:
```python
@pytest.fixture
def sample_user():
    return User(username="test", email="test@example.com")
```

2. **Parameterization**:
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

3. **Mocking**:
```python
@patch('module.external_api_call')
def test_function(mock_api):
    mock_api.return_value = {'status': 'success'}
    result = function_using_api()
    assert result == expected
```

### Memory Evolution

Project memory should grow with each invocation:
- First time: Establish basic patterns
- Subsequent times: Refine and expand patterns
- Always: Store user-clarified behaviors

### Context Usage

Context files provide stable guidance:
- Testing standards (what makes a good test)
- Framework patterns (how to use pytest/unittest)
- Antipatterns (what to avoid)
- Mocking strategies (when and how to mock)

## Version History

### v1.0.0 (2025-11-18)
- Initial release
- Mandatory 8-step workflow
- Socratic planning phase
- Project-specific memory system
- Centralized context integration
- Support for pytest and unittest
- Template-based test generation
