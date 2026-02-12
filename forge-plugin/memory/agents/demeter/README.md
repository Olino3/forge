# Demeter Agent Memory

This directory stores project-specific knowledge for the `@demeter` agent.

## Structure

```
demeter/
├── pipelines/     # Track data pipeline architectures and patterns
├── schemas/       # Store schema designs and evolution strategies
├── quality_rules/ # Record data quality rules and validation logic
└── analytics/     # Maintain analytics patterns and dashboards
```

## Usage

The `@demeter` agent automatically stores and retrieves:
- Data pipeline architectures and patterns
- Schema designs and evolution strategies
- Data quality rules and validation logic
- Analytics patterns and dashboards
- Performance optimization techniques
- Data governance policies

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores data patterns and quality rules
3. **Retrieval**: Agent loads relevant patterns before data work
4. **Updates**: Memory is updated as data evolves
5. **Cleanup**: Outdated patterns can be archived or removed manually

## Example Memory Files

- `pipelines/etl-pipeline-architecture.md` - ETL pipeline design
- `schemas/dimensional-model.md` - Data warehouse schema
- `quality_rules/validation-rules.md` - Data quality rules
- `analytics/sales-dashboard.md` - Analytics patterns

## Best Practices

- Store pipeline architectures with diagrams
- Document schema evolution strategies
- Keep quality rules with examples
- Update memory with analytics patterns
- Review and refine data strategies periodically
