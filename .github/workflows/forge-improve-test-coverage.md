---
description: "Analyze test coverage gaps and generate missing test files"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 9 * * 2"
  workflow_dispatch:
engine:
  id: copilot
  model: gpt-4.1
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "testing", "coverage-improvement"]
    title-prefix: "[test-coverage] "
    expires: 14
    draft: true
    if-no-changes: "ignore"
---

# Forge Test Coverage Improver

Analyze test coverage gaps in the Microsoft Skills test harness and generate missing test files to systematically improve coverage over time.

## Objective

Improve test coverage for the Microsoft Skills test harness by:
1. Identifying files with coverage below 80% threshold
2. Generating test files that follow established patterns
3. Creating a draft PR with comprehensive before/after metrics

## Coverage Analysis

### Step 1: Run Coverage Analysis

Navigate to the test directory and execute coverage analysis:

```bash
cd /root/forge/microsoft/skills/tests
npm run test:coverage
```

This generates coverage reports in the `coverage/` directory:
- `coverage/coverage-final.json` - Detailed per-file metrics
- `coverage/index.html` - HTML report for human review
- Console output - Summary text report

### Step 2: Identify Coverage Gaps

Parse `coverage/coverage-final.json` to extract files with coverage below 80%:

**Check these metrics**:
- **Line coverage** (statementMap)
- **Function coverage** (fnMap)
- **Branch coverage** (branchMap)

**Priority order**:
1. Core harness files: `harness/runner.ts`, `harness/evaluator.ts`, `harness/criteria-loader.ts`
2. Utility modules: `harness/feedback-builder.ts`, `harness/pattern-matcher.ts`
3. Recently added files without tests
4. Support utilities: helpers, validators, builders

**Skip**:
- Type definition files (`*.d.ts`)
- Test files themselves (`*.test.ts`)
- Configuration files (`vitest.config.ts`, `tsconfig.json`)
- Files already at or above 80% coverage

### Step 3: Analyze Existing Test Patterns

Before generating new tests, read existing test files to understand conventions:

**Reference Test Files**:
- `harness/feedback-builder.test.ts` - Comprehensive unit test example
- `harness/ralph-loop.test.ts` - Integration test example
- `harness/plugin-validator.test.ts` - Validation logic example

**Extract these patterns**:
1. **Test structure**: Vitest `describe/it/expect` blocks
2. **Factory functions**: Import from `types.ts` (createFinding, createEvaluationResult, createAcceptanceCriteria)
3. **Naming convention**: `{source-file}.test.ts` in same directory as source
4. **Test organization**:
   - Top-level `describe` block for the module/class
   - Nested `describe` blocks for each method/function
   - `it` blocks for specific test cases
5. **AAA pattern**: Arrange (setup), Act (execute), Assert (verify)
6. **Edge case coverage**: Happy path, edge cases (empty/null/boundaries), error handling

### Step 4: Generate Missing Tests

For each file below 80% coverage, create a corresponding test file:

**Test File Requirements**:
1. Match existing code style exactly
2. Use factory functions from `types.ts` for test data
3. Target specific uncovered lines from coverage JSON
4. Include:
   - **Happy path scenarios** - Normal expected usage
   - **Edge cases** - Empty inputs, null values, boundary conditions
   - **Error handling** - Exceptions, invalid inputs, malformed data
5. Follow Vitest conventions:
   - Import `describe`, `it`, `expect`, `beforeEach` from "vitest"
   - Use `.js` extensions for imports (TypeScript convention)
   - Group related tests in `describe` blocks
   - Use descriptive test names (what behavior is being verified)

**Example Test Structure**:

```typescript
/**
 * Tests for {ModuleName}
 *
 * {Brief description of what this module does}
 */

import { describe, it, expect, beforeEach } from "vitest";
import { /* imports from types.ts */ } from "./types.js";
import { /* module under test */ } from "./{source}.js";

describe("{ModuleName}", () => {
  let instance: ModuleType;

  beforeEach(() => {
    instance = new ModuleClass();
  });

  describe("methodName", () => {
    it("handles normal case correctly", () => {
      // Arrange
      const input = createTestData();

      // Act
      const result = instance.methodName(input);

      // Assert
      expect(result).toBe(expectedValue);
    });

    it("handles edge case: empty input", () => {
      // Test empty input scenario
    });

    it("throws error for invalid input", () => {
      // Test error handling
      expect(() => instance.methodName(null)).toThrow();
    });
  });
});
```

### Step 5: Validate Generated Tests

After generating test files, validate they compile and pass:

**Validation Steps**:

1. **Syntax check** (compile TypeScript):
   ```bash
   cd /root/forge/microsoft/skills/tests
   npm run typecheck
   ```

2. **Run new tests** (verify they pass):
   ```bash
   npx vitest run {test-file-path}
   ```

3. **Re-run coverage** (verify improvement):
   ```bash
   npm run test:coverage
   ```

4. **Compare metrics**:
   - Extract before/after coverage from JSON reports
   - Verify coverage increased for target files
   - Ensure no regressions in other files

**If validation fails**:
- Review test code for TypeScript errors
- Check import paths (use `.js` extensions)
- Verify factory functions are used correctly
- Ensure test assertions are accurate
- Fix issues and re-validate

### Step 6: Create Pull Request

Create a draft PR with comprehensive before/after metrics:

**PR Title Format**:
```
[test-coverage] Improve test coverage for harness utilities (+X% overall coverage)
```

**PR Body Template**:

```markdown
## Summary

This PR adds comprehensive test coverage for previously untested code in the skills test harness.

**Triggered By**: Weekly coverage analysis workflow
**Run Date**: {YYYY-MM-DD}
**Overall Coverage Improvement**: {before}% → {after}% (+{delta}%)

---

## Coverage Analysis

### Before This PR

| File | Lines | Functions | Branches | Status |
|------|-------|-----------|----------|--------|
{for each file with <80% coverage:}
| {file-path} | {line%} | {fn%} | {branch%} | 🔴 Below threshold |

### After This PR

| File | Lines | Functions | Branches | Status |
|------|-------|-----------|----------|--------|
{for each improved file:}
| {file-path} | {line%} | {fn%} | {branch%} | {🟢 Meets threshold / 🟡 Improved} |

---

## Changes

{for each new test file:}

### {test-file-name}

**Tests Added**: {count}
**Coverage Improvement**: {before}% → {after}% (+{delta}%)

**Test Cases**:
{list test case descriptions from the test file}

---

## Validation

- ✅ All {N} new tests pass
- ✅ TypeScript compilation clean
- ✅ Overall coverage increased by {X}%
- ✅ {N} files now meet 80% threshold

---

## Review Checklist

- [ ] Generated tests accurately reflect code behavior
- [ ] Edge cases are realistic and valuable
- [ ] Test names are clear and descriptive
- [ ] Tests follow existing patterns from reference tests
- [ ] No brittle tests (testing implementation details)
- [ ] Coverage improvement is meaningful (not just trivial assertions)

---

## Next Steps

1. Review the generated tests for accuracy
2. Merge this PR to integrate improved coverage
3. Monitor coverage metrics in future runs
```

## Constraints

### DO Generate Tests For

✅ **Files to target**:
- Files with <80% line, function, or branch coverage
- Core harness files (runner, evaluator, criteria-loader)
- Utility modules with business logic (feedback-builder, pattern-matcher)
- Recently added files with no test coverage
- Support utilities (helpers, validators, builders)

✅ **Test quality standards**:
- Follow existing patterns exactly (read reference tests first)
- Use factory functions from `types.ts`
- Target specific uncovered lines from coverage JSON
- Test behavior, not implementation details
- Ensure tests are deterministic (no flaky tests)
- Include meaningful assertions (not trivial checks)

### DON'T Generate Tests For

❌ **Files to skip**:
- Type definition files (`*.d.ts`)
- Files already above 80% coverage
- Test files themselves (`*.test.ts`)
- Configuration files (`vitest.config.ts`, `tsconfig.json`)
- Files with only type exports (no runtime code)

❌ **Quality anti-patterns**:
- Generic assertions that don't verify behavior
- Brittle tests coupled to implementation details
- Tests that require extensive mocking (indicates bad design)
- Flaky tests with timing dependencies
- Tests without clear purpose or assertions

### When to Skip PR Creation

Skip creating a PR if:
- All files already meet 80% coverage threshold
- Coverage gaps are only in untestable code (type definitions, configs)
- Recent coverage PR is still open and unreviewed (within last 14 days)
- Generated tests don't compile or fail validation
- Coverage improvement would be <5% (too small to be meaningful)

## Success Criteria

A successful coverage improvement PR:

1. ✅ All generated tests compile without TypeScript errors
2. ✅ All generated tests pass on first run
3. ✅ Coverage increased by at least 5% overall
4. ✅ At least one file moved from <80% to ≥80% coverage
5. ✅ Tests follow existing patterns exactly (factory functions, AAA pattern)
6. ✅ PR body includes comprehensive before/after metrics
7. ✅ Tests are deterministic and meaningful
8. ✅ No regressions in existing test coverage

## Notes

**Coverage Configuration** (from `vitest.config.ts`):
- Provider: v8
- Reports: text, json, html
- Include: `harness/**/*.ts`
- Exclude: `harness/**/*.test.ts`, `**/*.d.ts`

**Test Scripts** (from `package.json`):
- `npm run test` - Run all tests
- `npm run test:coverage` - Run tests with coverage
- `npm run typecheck` - TypeScript compilation check

**Coverage Threshold**: 80% (line/function/branch)
- This is the target for systematic improvement
- Files below 80% are prioritized for test generation
- This aligns with industry best practices for production code
