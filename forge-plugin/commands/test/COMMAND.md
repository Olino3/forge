---
name: test
description: "Test execution, coverage analysis, and quality reporting with skill delegation"
category: utility
complexity: enhanced
skills: [test-cli-tools, generate-python-unit-tests, generate-jest-unit-tests]
context: [python, angular, commands/testing_strategies]
---

# /test - Test Execution and Validation

## Triggers
- Test execution requests for unit, integration, or e2e tests
- Coverage analysis and quality gate validation
- Test failure analysis and debugging
- Post-implementation validation

## Usage
```
/test [target] [--type unit|integration|e2e|all] [--coverage] [--fix] [--generate]
```

**Parameters**:
- `target`: File, directory, or test suite to run (default: all tests)
- `--type`: Test category to run (default: all)
- `--coverage`: Generate coverage report
- `--fix`: Attempt to fix simple test failures
- `--generate`: Generate missing tests before running (delegates to test generation skills)

## Workflow

### Step 1: Test Discovery

1. Detect test framework from project configuration:
   - Python: Check for `pytest.ini`, `pyproject.toml` [tool.pytest], `conftest.py`
   - JavaScript/TypeScript: Check for `jest.config.*`, `karma.conf.js`, `vitest.config.*`
   - .NET: Check `*.csproj` for test framework packages
2. Identify test directories and file patterns
3. Categorize available tests (unit, integration, e2e)
4. Determine test runner command

### Step 2: Load Context & Memory

**Context Loading** (via ContextProvider):
1. Load testing patterns: `contextProvider.getConditionalContext("commands", "testing_strategies")`
2. Based on detected framework, load domain-specific testing context:
   - **Python**: `contextProvider.getConditionalContext("python", "testing_frameworks")`, `contextProvider.getConditionalContext("python", "unit_testing_standards")`
   - **Angular**: `contextProvider.getConditionalContext("angular", "jest_testing_standards")`, `contextProvider.getConditionalContext("angular", "testing_utilities")`

**Memory Loading** (via MemoryStore):
1. Determine project name
2. Load historical results: `memoryStore.getCommandMemory("test", project)`
3. Load project-specific test patterns from skill memory if available

### Step 3: Generate Missing Tests (if --generate)

Delegate to test generation skills before running:

**Python projects**:
```
skill:generate-python-unit-tests --target [untested files]
```

**Angular projects**:
```
skill:generate-jest-unit-tests --target [untested components/services]
```

### Step 4: Execute Tests

1. Run tests in order: unit → integration → e2e
2. Capture output and results
3. Track timing per test suite

**Test execution commands** (detected automatically):
- **pytest**: `pytest [target] [-x] [--cov=src]`
- **Jest**: `npx jest [target] [--bail] [--coverage]`
- **dotnet**: `dotnet test [project] [--filter Category=Unit]`

### Step 5: Analyze Results

**For passing tests**:
- Report pass count and execution time
- Generate coverage report if `--coverage` flag set
- Identify untested areas

**For failing tests**:
- Analyze failure messages and stack traces
- Categorize failures (assertion, timeout, setup, environment)
- Identify patterns (all failures in one module, flaky tests)
- If `--fix`: Attempt simple fixes (missing imports, setup issues)

**For systematic CLI testing**, delegate to:
```
skill:test-cli-tools --target [commands to test]
```

### Step 6: Generate Output & Update Memory

**Output**:
Save results to `/claudedocs/test_results_{date}.md`:

```markdown
# Test Results - {Project}
**Date**: {date}
**Command**: /test {full invocation}
**Framework**: {detected framework}

## Summary
- **Total**: {count} tests
- **Passed**: {count} ({percentage}%)
- **Failed**: {count}
- **Skipped**: {count}
- **Duration**: {time}

## Coverage (if requested)
- **Line Coverage**: {percentage}%
- **Branch Coverage**: {percentage}%
- **Uncovered Areas**: {list}

## Failures (if any)
### {Test Name}
- **File**: {path}:{line}
- **Error**: {message}
- **Category**: {assertion|timeout|setup|environment}
- **Suggested Fix**: {recommendation}

## Trends (from memory)
- Previous run: {pass_rate}%
- Current run: {pass_rate}%
- Trend: {improving|stable|degrading}

## Next Steps
- {recommendations}
```

**Memory Updates** (via MemoryStore):
1. `memoryStore.append("commands", project, "command_history.md", entry)`
2. `memoryStore.update("commands", project, "test_results.md", content)`:
   - Test counts, coverage trends, recurring failures

## Tool Coordination
- **Bash**: Test runner execution and environment management
- **Glob**: Test file discovery and pattern matching
- **Grep**: Result parsing and failure analysis
- **Read**: Test file inspection for debugging
- **Write**: Coverage reports and test summaries

## Key Patterns
- **Framework Detection**: Config files → appropriate test runner and commands
- **Skill Delegation**: CLI testing → `skill:test-cli-tools`; test generation → specialized skills
- **Coverage Tracking**: Memory system tracks coverage trends across runs
- **Failure Analysis**: Categorize and diagnose test failures with actionable guidance

## Boundaries

**Will:**
- Execute existing test suites using detected test runner
- Generate coverage reports and quality metrics
- Provide intelligent test failure analysis with recommendations
- Delegate to test generation skills when `--generate` flag used
- Track test results in memory for trend analysis

**Will Not:**
- Modify test framework configuration without user approval
- Execute tests requiring external services without proper setup
- Delete or significantly modify existing test files
- Replace systematic skill invocations for deep testing

**Output**: Test results saved to `/claudedocs/test_results_{date}.md`

**Next Step**: If failures found, use `/improve` to fix issues. If coverage low, use `/test --generate` to add tests.
