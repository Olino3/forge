# Artemis Agent Memory

This directory stores project-specific knowledge for the `@artemis` agent.

## Structure

```
artemis/
├── test_strategies/   # Track test strategies and patterns
├── bug_patterns/      # Record common bug patterns and fixes
├── coverage_reports/  # Store test coverage reports and trends
└── test_configs/      # Maintain testing tool configurations
```

## Usage

The `@artemis` agent automatically stores and retrieves:
- Test strategies and patterns
- Common bug patterns and fixes
- Test coverage reports and trends
- Testing tools and configurations
- Edge cases and corner cases
- Regression test patterns

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores test strategies and bug patterns
3. **Retrieval**: Agent loads relevant patterns before testing
4. **Updates**: Memory is updated as tests evolve
5. **Cleanup**: Outdated patterns can be archived or removed manually

## Example Memory Files

- `test_strategies/api-testing-strategy.md` - API test strategy
- `bug_patterns/race-condition-bugs.md` - Race condition patterns
- `coverage_reports/baseline-coverage.md` - Coverage baselines
- `test_configs/pytest-configuration.md` - pytest setup

## Best Practices

- Store test strategies with examples
- Document bug patterns with reproduction steps
- Keep coverage trends for comparison
- Update memory with new test patterns
- Review and refine strategies periodically
