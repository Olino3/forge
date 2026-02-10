# /test Examples

## Example 1: Run All Tests

```
/test
```

**What happens**:
1. Detects test framework (e.g., pytest from `pyproject.toml`)
2. Discovers all test files
3. Runs full test suite: `pytest`
4. Reports pass/fail summary with execution time
5. Saves results to `/claudedocs/test_results_20260209.md`

## Example 2: Targeted Test with Coverage

```
/test src/auth --type unit --coverage
```

**What happens**:
1. Scopes to auth-related unit tests
2. Runs: `pytest tests/unit/auth/ --cov=src/auth --cov-report=html`
3. Generates detailed coverage report
4. Identifies untested code paths in auth module
5. Saves coverage data and test results

## Example 3: Fix Failing Tests

```
/test --fix
```

**What happens**:
1. Runs all tests, captures failures
2. Analyzes failure patterns:
   - Missing imports → auto-fix
   - Setup errors → suggest fix
   - Logic failures → explain root cause
3. Applies simple fixes automatically
4. Re-runs tests to verify fixes
5. Reports remaining failures that need manual attention

## Example 4: Generate and Run Tests

```
/test src/services --generate --coverage
```

**What happens**:
1. Identifies untested files in `src/services/`
2. Delegates to `skill:generate-python-unit-tests` for test generation
3. Runs all tests including newly generated ones
4. Reports coverage improvement
5. Saves comprehensive test report

## Example 5: Angular Component Testing

```
/test src/app/components --type unit --coverage
```

**What happens**:
1. Detects Jest from `jest.config.ts`
2. Runs: `npx jest --testPathPattern=components --coverage`
3. Reports component test results
4. Shows coverage for tested components
5. Identifies components missing tests

## Example 6: CLI Tool Testing

```
/test --type integration
```

**What happens**:
1. Detects CLI tool project
2. Delegates to `skill:test-cli-tools` for systematic testing
3. Tests each command with various inputs
4. Reports command-level pass/fail
5. Documents failures with root cause analysis
6. Saves detailed report to `/claudedocs`

## Example 7: Trend Analysis

```
/test --coverage
```

**What happens** (with existing memory):
1. Loads previous test results from memory
2. Runs full suite with coverage
3. Compares against previous run:
   - Coverage: 78% → 82% (improving)
   - Tests: 120 → 135 (15 new tests)
   - Failures: 3 → 1 (2 fixed)
4. Reports trends alongside current results
