# generate-python-unit-tests Examples

## Usage Scenarios

This document provides practical examples of using the `generate-python-unit-tests` skill in various contexts.

## Example 1: Basic Function Testing

### Scenario
You have a new utility module with helper functions that need tests.

### User Request
```
Please use skill:generate-python-unit-tests to create tests for src/utils/string_helpers.py
```

### Skill Workflow

**Step 1-5**: Initial analysis and context loading
- Identifies `src/utils/string_helpers.py` has functions: `capitalize_words`, `truncate_string`, `remove_whitespace`
- Loads project memory (first time, so empty)
- Loads testing context (unit_testing_standards.md, testing_frameworks.md)
- Analyzes the source code

**Step 6**: Socratic Planning
```
I analyzed string_helpers.py and found 3 utility functions to test. Before generating tests,
I need to understand the expected behavior:

1. For capitalize_words(text):
   - Should it handle empty strings?
   - What about strings with numbers or special characters?
   - Should it preserve existing capitalization?

2. For truncate_string(text, max_length, suffix="..."):
   - What happens if text is shorter than max_length?
   - Should the suffix count toward max_length?
   - How should it handle None or empty strings?

3. For remove_whitespace(text, mode="all"):
   - What modes are supported (all, leading, trailing)?
   - Should it preserve single spaces between words in some modes?
   - How to handle tabs and newlines?

Also, I noticed you're using pytest. Should I use parametrized tests for multiple cases?
```

**User Response**:
```
1. capitalize_words should handle empty strings (return ""), preserve numbers/special chars,
   and capitalize each word regardless of existing case
2. truncate_string should return the original if shorter, suffix should NOT count toward
   max_length, raise ValueError for None
3. remove_whitespace modes: "all", "leading", "trailing", "normalize" (keeps single spaces)
4. Yes, use parametrized tests
```

**Step 7**: Generate tests based on clarified behavior
- Creates `tests/utils/test_string_helpers.py`
- Uses parametrized tests for multiple cases
- Implements all clarified behaviors

**Step 8**: Update memory
- Creates project memory documenting:
  - Test file location pattern: `tests/{module_path}/test_{module_name}.py`
  - Use pytest with parametrization
  - Functions raise ValueError for None inputs
  - Stores the clarified behaviors for future reference

---

## Example 2: Class with Dependencies

### Scenario
Testing a service class that interacts with a database and external API.

### User Request
```
I need tests for the UserService class in app/services/user_service.py. Use skill:generate-python-unit-tests
```

### Skill Workflow

**Step 1-5**: Analysis
- Identifies `UserService` class with methods: `create_user`, `get_user`, `update_user`, `delete_user`
- Detects dependencies: `DatabaseConnection`, `EmailService`, `CacheService`
- Loads existing project memory (second time using skill)
- Loads mocking_patterns.md context

**Step 6**: Socratic Planning
```
I analyzed UserService and found it has complex dependencies. Some clarifications needed:

1. Database interactions:
   - Should I mock the DatabaseConnection completely?
   - Or use an in-memory database for integration tests?
   - What's your preference?

2. For create_user:
   - What validations should I test (email format, password strength)?
   - Should it send a welcome email via EmailService?
   - How should it handle duplicate usernames?

3. For update_user:
   - Can users update their email address?
   - Should it invalidate cache?
   - What fields are allowed to be updated?

4. Error scenarios:
   - What exceptions should be raised for not found, duplicate, validation errors?
   - Should database errors be caught and wrapped?

I see from project memory you use pytest fixtures for common setup. Should I create a
UserService fixture with mocked dependencies?
```

**User Response**:
```
1. Mock DatabaseConnection - we have separate integration tests
2. create_user should validate email (regex), password (min 8 chars), send email,
   raise UserExistsError for duplicates
3. update_user allows email and profile fields, should invalidate cache,
   raise NotFoundError if user doesn't exist
4. Raise custom exceptions: UserExistsError, NotFoundError, ValidationError
5. Yes, create fixtures for mocked dependencies
```

**Step 7**: Generate tests
- Creates `tests/services/test_user_service.py`
- Creates fixtures for mocked dependencies
- Tests all CRUD operations
- Tests error scenarios with custom exceptions
- Uses patches for DatabaseConnection, EmailService, CacheService

**Step 8**: Update memory
- Documents custom exception types
- Stores that database mocking is preferred
- Records fixture pattern for service testing
- Updates expected_behaviors.md with validation rules

---

## Example 3: Async Code Testing

### Scenario
Testing async functions in a FastAPI application.

### User Request
```
Generate tests for the async handlers in api/endpoints/tasks.py using skill:generate-python-unit-tests
```

### Skill Workflow

**Step 1-5**: Analysis
- Identifies async functions: `create_task`, `get_task`, `list_tasks`, `update_task_status`
- Detects FastAPI dependency injection
- Loads async_patterns.md context
- Identifies pytest-asyncio needed

**Step 6**: Socratic Planning
```
I found async FastAPI endpoint handlers. Need to understand the behavior:

1. Testing approach:
   - Should I test the handlers directly (unit tests)?
   - Or use FastAPI TestClient (integration tests)?
   - Or both?

2. For create_task(task_data, db_session):
   - What validation is performed on task_data?
   - Should I mock the db_session?
   - What's returned on success?

3. For update_task_status(task_id, status, current_user):
   - What statuses are valid?
   - Should it check if current_user owns the task?
   - What if task doesn't exist?

4. Dependencies:
   - How should I handle FastAPI dependencies in tests?
   - Mock them or use override_dependency?

From project memory, you use pytest-asyncio. Should I use the @pytest.mark.asyncio decorator?
```

**User Response**:
```
1. Unit tests for handlers, mock db_session
2. create_task validates: title (required, max 200 chars), description (optional),
   returns Task model
3. Valid statuses: PENDING, IN_PROGRESS, COMPLETED, CANCELLED
   Should check ownership, raise PermissionError if not owner, NotFoundError if not exists
4. Mock dependencies with pytest fixtures
5. Yes, use @pytest.mark.asyncio
```

**Step 7**: Generate tests
- Creates `tests/api/endpoints/test_tasks.py`
- Uses pytest-asyncio for async test functions
- Mocks db_session with AsyncMock
- Tests all async handlers
- Includes permission and validation tests

**Step 8**: Update memory
- Documents FastAPI testing pattern
- Records valid task statuses
- Stores ownership check pattern
- Notes pytest-asyncio usage

---

## Example 4: Existing Tests with Gaps

### Scenario
Adding tests to improve coverage of partially tested code.

### User Request
```
The payment_processor.py module has some tests but coverage is only 60%.
Use skill:generate-python-unit-tests to fill the gaps.
```

### Skill Workflow

**Step 1-5**: Analysis
- Reads existing `tests/test_payment_processor.py`
- Identifies coverage gaps:
  - `process_refund` method has no tests
  - Error scenarios for `process_payment` not tested
  - `validate_payment_method` edge cases missing
- Loads project memory with existing patterns

**Step 6**: Socratic Planning
```
I analyzed the existing tests and found coverage gaps. Questions:

1. For process_refund (currently untested):
   - What conditions allow refunds (time limit, status)?
   - Should it validate the refund amount?
   - What happens for partial refunds?

2. For process_payment error scenarios (missing):
   - What happens if payment gateway is down?
   - How to handle insufficient funds?
   - Should it retry on timeout?

3. For validate_payment_method edge cases:
   - Current tests only check credit cards
   - Should I test PayPal, bank transfer, crypto?
   - What validation rules apply to each?

Should I add to the existing test file or create a new one?
```

**User Response**:
```
1. Refunds allowed within 30 days, only for COMPLETED status, can be partial or full
2. Gateway down: raise PaymentGatewayError (no retry)
   Insufficient funds: raise InsufficientFundsError
   Timeout: retry once, then raise TimeoutError
3. Add tests for PayPal (email validation), bank transfer (account number format)
   Skip crypto for now
4. Add to existing test file to keep all payment tests together
```

**Step 7**: Generate tests
- Adds new test methods to existing file
- Creates tests for process_refund (happy path + edge cases)
- Adds error scenario tests for process_payment
- Expands validate_payment_method tests
- Maintains consistency with existing test style

**Step 8**: Update memory
- Documents refund business rules
- Records payment error handling patterns
- Updates expected_behaviors.md with retry logic

---

## Example 5: Data Processing Pipeline

### Scenario
Testing a complex data transformation pipeline.

### User Request
```
Create comprehensive tests for data/pipeline/transform.py using skill:generate-python-unit-tests
```

### Skill Workflow

**Step 1-5**: Analysis
- Identifies pipeline stages: `extract`, `validate`, `transform`, `load`
- Each stage is a separate function
- Pipeline uses pandas DataFrames
- Detects complex transformations and data validation

**Step 6**: Socratic Planning
```
I found a multi-stage data pipeline. Need to understand the expected data flow:

1. Testing granularity:
   - Should I test each stage independently?
   - Or test the complete pipeline end-to-end?
   - Or both?

2. For validate stage:
   - What validation rules should I test?
   - How should it handle invalid data (skip, error, fix)?
   - Should I test with realistic data samples?

3. For transform stage:
   - What transformations are applied?
   - Are there edge cases (null values, duplicates, outliers)?
   - Should transformations be idempotent?

4. Test data:
   - Should I create fixtures with sample DataFrames?
   - Or generate test data programmatically?
   - Do you have real data samples I can anonymize?

From your project memory, I see you use pandas testing utilities. Should I use
pd.testing.assert_frame_equal for DataFrame comparisons?
```

**User Response**:
```
1. Test each stage independently AND end-to-end pipeline
2. Validation rules: no nulls in required columns, dates in valid range, amounts > 0
   Skip invalid rows and log warnings
3. Transformations: normalize dates, calculate derived fields, remove duplicates
   Should be idempotent
4. Create fixtures with small sample DataFrames
5. Yes, use pd.testing.assert_frame_equal and assert_series_equal
```

**Step 7**: Generate tests
- Creates `tests/data/pipeline/test_transform.py`
- Creates fixtures for sample DataFrames
- Tests each pipeline stage independently
- Tests complete pipeline end-to-end
- Uses pandas testing utilities
- Tests edge cases (nulls, duplicates, invalid dates)

**Step 8**: Update memory
- Documents pipeline testing pattern (stage + end-to-end)
- Records data validation rules
- Stores DataFrame fixture patterns
- Notes pandas testing utility usage

---

## Key Patterns

### Common Themes Across Examples

1. **Always ask before generating**: Socratic planning prevents assumptions
2. **Load project memory**: Maintain consistency with existing tests
3. **Context guides quality**: Testing standards ensure best practices
4. **Update memory after**: Each invocation improves future generations
5. **User collaboration**: Tests reflect actual expected behavior, not guessed behavior

### When to Use This Skill

- ✅ Creating new tests for untested code
- ✅ Expanding test coverage for partially tested code
- ✅ Refactoring tests to be more maintainable
- ✅ Standardizing test structure across a project
- ✅ Learning project-specific testing patterns

### When NOT to Use This Skill

- ❌ Just running existing tests (use bash directly)
- ❌ Debugging failing tests (use regular Claude Code interaction)
- ❌ Generating integration or E2E tests (different skill needed)
- ❌ Simple one-liner functions that don't need tests

---

## Tips for Best Results

1. **Be specific in your request**:
   - Good: "Generate tests for UserService.create_user method"
   - Better: "Generate tests for UserService including error scenarios"

2. **Provide context**:
   - Mention testing framework if not standard
   - Note any special requirements (mocking strategy, fixtures)
   - Share relevant documentation or specs

3. **Engage in Socratic planning**:
   - Answer questions thoroughly
   - Provide examples of expected behavior
   - Clarify edge cases

4. **Review generated tests**:
   - Ensure they match your understanding
   - Request adjustments if needed
   - Run tests and provide feedback

5. **Build project memory**:
   - Use the skill multiple times on the same project
   - Patterns will be learned and applied automatically
   - Tests will become more consistent over time
