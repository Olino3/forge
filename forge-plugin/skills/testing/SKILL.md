---
name: testing
description: Comprehensive testing strategies covering test strategy design, test planning, coverage analysis, and best practices across all testing levels. Supports unit testing, integration testing, end-to-end (E2E) testing, performance testing, test data management, and mocking strategies. Use for designing testing pyramids, increasing coverage on legacy code, establishing test conventions, and implementing robust test suites across any language or framework.
---

# Testing

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY testing engagement. Skipping steps or deviating from the procedure will result in incomplete and unreliable test strategies. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Testing strategy scenarios with detailed examples
- **Context**: Testing and quality domain context loaded via `contextProvider.getDomainIndex("testing")` and `contextProvider.getDomainIndex("security")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("testing", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Testing Focus Areas

Comprehensive testing evaluates 8 key dimensions:

1. **Test Strategy & Planning**: Testing pyramid design, risk-based test prioritization, coverage goals, framework selection
2. **Unit Testing Best Practices**: Isolation, single responsibility per test, meaningful assertions, deterministic behavior, fast execution
3. **Integration Testing Patterns**: API contract testing, database integration, service-to-service communication, message queue verification
4. **End-to-End (E2E) Testing**: User journey validation, cross-browser testing, visual regression, accessibility testing
5. **Test Coverage Analysis**: Line/branch/path coverage measurement, identifying untested critical paths, coverage gap remediation
6. **Test Data Management**: Fixtures, factories, seed data, test isolation, data cleanup strategies
7. **Mocking & Stubbing Strategies**: Dependency isolation, mock vs stub vs fake selection, avoiding over-mocking, contract verification
8. **Performance & Load Testing**: Baseline benchmarks, load profiles, stress testing, latency budgets, resource utilization monitoring

**Note**: Focus on actionable testing strategies tailored to the project's architecture, risk profile, and existing test infrastructure. This skill covers test methodology and strategy — for generating specific unit tests, see `generate-jest-unit-tests` or `generate-python-unit-tests`.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Assess Testing Scope (REQUIRED)

**YOU MUST:**
1. **Identify the codebase** and its primary language(s) and frameworks
2. **Determine current test coverage**: Examine existing test files, test configuration, and CI pipelines
3. **Detect test framework(s)** in use (e.g., Jest, pytest, JUnit, Playwright, Cypress, Vitest, xUnit)
4. **Identify untested critical paths**: Business logic, authentication flows, data transformations, error handling
5. **Assess existing test quality**: Are tests meaningful or superficial? Do they cover edge cases? Are they maintainable?
6. Ask clarifying questions:
   - What is the testing goal? (new test suite, increase coverage, add E2E, fix flaky tests)
   - Which areas of the codebase are highest risk?
   - Are there existing CI/CD constraints or time budgets for test execution?

**DO NOT PROCEED WITHOUT ASSESSING THE TESTING SCOPE**

### ⚠️ STEP 2: Load Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("testing", "{project-name}")` to load project-specific testing patterns
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for code review findings, schema analysis results, or other skill insights that inform test strategy
   - If memory exists: Review previously learned testing conventions, frameworks, and coverage baselines
   - If no memory exists (empty result): Note this is first engagement, you will create memory later
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("testing")` to understand testing context files and when to use each
   - Use `contextProvider.getDomainIndex("security")` for security testing context if applicable
   - Load only context files relevant to the detected frameworks and testing goals

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Design Test Strategy (REQUIRED)

**YOU MUST:**
1. **Determine testing pyramid balance**: Define the appropriate ratio of unit, integration, and E2E tests based on the project's architecture and risk profile
2. **Identify which tests to write**:
   - **Unit tests**: Pure business logic, utility functions, data transformations, edge cases
   - **Integration tests**: API endpoints, database queries, service interactions, middleware
   - **E2E tests**: Critical user journeys, authentication flows, checkout processes, data workflows
3. **Define test data requirements**: Fixtures, factories, mocks, and seed data needed
4. **Select testing patterns**: Arrange-Act-Assert, Given-When-Then, test doubles strategy, parameterized tests
5. **Establish naming and organization conventions**: File naming, test grouping, describe/it structure

**DO NOT PROCEED WITHOUT A CLEAR TEST STRATEGY**

### ⚠️ STEP 4: Generate Tests (REQUIRED)

**YOU MUST:**
1. **Write tests following framework conventions**: Use idiomatic patterns for the detected test framework
2. **Ensure edge cases are covered**: Null/undefined inputs, boundary values, error conditions, empty collections, concurrent access
3. **Verify assertions are meaningful**: Tests should fail for the right reasons and validate behavior, not implementation
4. **Apply proper test isolation**: Each test should be independent, deterministic, and not depend on execution order
5. **Include test documentation**: Describe what is being tested and why, especially for complex scenarios

**For EVERY test generated, ensure**:
- Clear test name describing the behavior under test
- Proper setup and teardown (fixtures, beforeEach/afterEach)
- Meaningful assertions with descriptive failure messages
- Edge case coverage alongside happy path
- Mock/stub usage only where necessary for isolation

**DO NOT GENERATE SUPERFICIAL OR TRIVIAL TESTS**

### ⚠️ STEP 5: Validate & Update Memory (REQUIRED)

**YOU MUST:**
1. **Run tests to verify they pass**: Execute the test suite and confirm all new tests are green
2. **Report coverage metrics**: Measure and report line, branch, and function coverage improvements
3. **Identify remaining gaps**: Note any areas still lacking coverage that require follow-up
4. **Ask user for preferred output format**:
   - **Option A**: Test strategy document → testing pyramid, conventions, coverage targets → output to `claudedocs/`
   - **Option B**: Generated test files only → directly in the codebase
   - **Option C (Default)**: Both strategy document and generated tests

**After completing the engagement, UPDATE PROJECT MEMORY**:

Use `memoryStore.update("testing", "{project-name}", ...)` to create or update memory files:

1. **test_conventions**: Testing frameworks, naming patterns, file organization
2. **coverage_baseline**: Current coverage metrics and targets
3. **test_patterns**: Project-specific testing patterns and utilities discovered
4. **engagement_history**: Summary of testing work performed with dates and key outcomes

Timestamps and staleness tracking are managed automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

---

## Interface References

- **ContextProvider**: [../../interfaces/context_provider.md](../../interfaces/context_provider.md) — Load context by domain, tags, or sections
- **MemoryStore**: [../../interfaces/memory_store.md](../../interfaces/memory_store.md) — Read/write project-specific memory with lifecycle automation
- **SkillInvoker**: [../../interfaces/skill_invoker.md](../../interfaces/skill_invoker.md) — Delegate to related skills (e.g., `generate-jest-unit-tests`, `generate-python-unit-tests`)

## Compliance Checklist

Before completing ANY testing engagement, verify:
- [ ] Step 1: Testing scope assessed — codebase identified, current coverage determined, test frameworks detected, critical untested paths identified
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()` and context loaded via `contextProvider`
- [ ] Step 3: Test strategy designed — pyramid balance defined, test types identified, data requirements established
- [ ] Step 4: Tests generated following framework conventions with edge cases, meaningful assertions, and proper isolation
- [ ] Step 5: Tests validated, coverage metrics reported, and project memory updated via `memoryStore.update()`

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE ENGAGEMENT**

## Version History

- v1.0.0 (2026-02-12): Initial release — comprehensive testing strategy skill with interface-based context and memory access
