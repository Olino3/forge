# Apollo Agent Memory

This directory stores project-specific knowledge for the `@apollo` agent.

## Structure

```
apollo/
├── quality_issues/ # Track common code quality issues and solutions
├── optimizations/  # Record performance optimization patterns
├── refactorings/   # Store refactoring strategies and outcomes
└── metrics/        # Maintain quality metrics and baselines
```

## Usage

The `@apollo` agent automatically stores and retrieves:
- Common code quality issues and solutions
- Performance optimization patterns
- Refactoring strategies and outcomes
- Quality metrics and baselines
- Tool configurations and findings
- Best practices and anti-patterns

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores quality findings and optimizations
3. **Retrieval**: Agent loads relevant patterns before reviews
4. **Updates**: Memory is updated as patterns evolve
5. **Cleanup**: Outdated patterns can be archived or removed manually

## Example Memory Files

- `quality_issues/python-common-issues.md` - Python quality patterns
- `optimizations/database-query-optimization.md` - DB optimization patterns
- `refactorings/legacy-code-refactoring.md` - Refactoring strategies
- `metrics/code-coverage-baselines.md` - Quality metric baselines

## Best Practices

- Store quality issues with solutions
- Document optimization techniques with measurements
- Keep refactoring strategies actionable
- Update memory with quality trends
- Review and refine patterns periodically
