---
id: "commands/testing_strategies"
domain: commands
title: "Testing Strategies"
type: pattern
estimatedTokens: 900
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Test Pyramid"
    estimatedTokens: 67
    keywords: [test, pyramid]
  - name: "Test Framework Detection"
    estimatedTokens: 107
    keywords: [test, framework, detection]
  - name: "Test Execution Strategy"
    estimatedTokens: 120
    keywords: [test, execution, strategy]
  - name: "Coverage Targets"
    estimatedTokens: 75
    keywords: [coverage, targets]
  - name: "Test Failure Debugging"
    estimatedTokens: 98
    keywords: [test, failure, debugging]
  - name: "Skill Integration"
    estimatedTokens: 18
    keywords: [skill, integration]
  - name: "Official References"
    estimatedTokens: 20
    keywords: [official, references]
tags: [commands, testing, test-pyramid, coverage, debugging, pytest, jest, xunit]
---

# Testing Strategies

Reference patterns for the `/test` command. Covers test pyramid, coverage targets, test framework detection, and failure debugging strategies.

## Test Pyramid

```
        /‾‾‾‾‾‾‾\
       /   E2E    \        Few, slow, expensive
      /‾‾‾‾‾‾‾‾‾‾‾‾\
     / Integration   \     Moderate count, moderate speed
    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
   /    Unit Tests      \   Many, fast, cheap
  /______________________\
```

| Level | Count | Speed | Scope | Tools |
|-------|-------|-------|-------|-------|
| **Unit** | Many (70-80%) | Fast (<1ms each) | Single function/class | pytest, Jest, xUnit |
| **Integration** | Moderate (15-20%) | Medium (<1s each) | Multiple components | pytest, Supertest, TestServer |
| **E2E** | Few (5-10%) | Slow (seconds each) | Full user flow | Playwright, Cypress, Selenium |

## Test Framework Detection

### Python
| Indicator | Framework | Config File |
|-----------|-----------|-------------|
| `import pytest` | pytest | `pyproject.toml`, `pytest.ini`, `setup.cfg` |
| `import unittest` | unittest | N/A (stdlib) |
| `conftest.py` | pytest | N/A (convention) |
| `@pytest.fixture` | pytest | N/A |
| `self.assertEqual` | unittest | N/A |

### JavaScript/TypeScript
| Indicator | Framework | Config File |
|-----------|-----------|-------------|
| `jest.config` | Jest | `jest.config.js`, `jest.config.ts` |
| `karma.conf` | Karma/Jasmine | `karma.conf.js` |
| `cypress.config` | Cypress | `cypress.config.ts` |
| `playwright.config` | Playwright | `playwright.config.ts` |
| `vitest.config` | Vitest | `vitest.config.ts` |

### .NET
| Indicator | Framework | Config File |
|-----------|-----------|-------------|
| `using Xunit` | xUnit | `*.csproj` with xunit package |
| `using NUnit` | NUnit | `*.csproj` with NUnit package |
| `using Microsoft.VisualStudio.TestTools` | MSTest | `*.csproj` with MSTest package |

## Test Execution Strategy

### Discovery
1. Detect test framework from config files
2. Identify test directories and file patterns
3. Categorize tests (unit, integration, e2e)
4. Determine test runner command

### Execution Order
1. **Unit tests first** (fast feedback)
2. **Integration tests** (if units pass)
3. **E2E tests** (if integration passes)
4. **Coverage report** (after all tests)

### Common Test Runner Commands

**Python (pytest)**:
```bash
pytest                          # All tests
pytest tests/unit/              # Unit tests only
pytest -x                       # Stop on first failure
pytest --cov=src --cov-report=html  # With coverage
pytest -k "test_auth"           # Filter by name
```

**JavaScript (Jest)**:
```bash
npx jest                        # All tests
npx jest --testPathPattern=unit # Unit tests
npx jest --bail                 # Stop on first failure
npx jest --coverage             # With coverage
npx jest --testNamePattern=auth # Filter by name
```

**.NET (dotnet test)**:
```bash
dotnet test                     # All tests
dotnet test --filter "Category=Unit"  # Unit tests
dotnet test --blame              # Stop on first failure
dotnet test --collect:"XPlat Code Coverage"  # Coverage
```

## Coverage Targets

| Project Type | Minimum | Target | Stretch |
|-------------|---------|--------|---------|
| **Library/SDK** | 80% | 90% | 95% |
| **API/Backend** | 70% | 80% | 90% |
| **Web Frontend** | 60% | 75% | 85% |
| **CLI Tool** | 70% | 85% | 90% |
| **Data Pipeline** | 60% | 75% | 85% |

### Coverage Interpretation
- **Line coverage**: Which lines were executed (basic metric)
- **Branch coverage**: Which conditional branches were taken (better metric)
- **Path coverage**: Which execution paths were taken (best but impractical)
- **Mutation coverage**: Which mutations were caught (quality metric)

## Test Failure Debugging

### Failure Analysis Flow
1. **Read error message** - What failed and where
2. **Check test isolation** - Does it fail independently or only with other tests?
3. **Check environment** - Missing dependencies, wrong config?
4. **Check recent changes** - What changed since last green build?
5. **Reproduce minimally** - Smallest test case that fails

### Common Failure Patterns
| Pattern | Symptom | Likely Cause |
|---------|---------|-------------|
| Flaky test | Passes sometimes, fails sometimes | Race condition, time dependency, shared state |
| All tests fail | Every test in suite fails | Environment issue, missing setup |
| One test fails | Specific test consistently fails | Logic bug, changed behavior |
| Tests pass locally, fail in CI | Environment-specific failure | Missing dependency, path issue |

## Skill Integration

Delegate to specialized skills for test generation and systematic testing:
- **Generate Python tests**: `skill:generate-python-unit-tests`
- **Generate Angular tests**: `skill:generate-jest-unit-tests`
- **Systematic CLI testing**: `skill:test-cli-tools`

## Official References

- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [xUnit Documentation](https://xunit.net/)
- [Playwright Documentation](https://playwright.dev/)
