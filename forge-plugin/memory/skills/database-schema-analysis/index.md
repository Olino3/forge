# Database Schema Analysis - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during database schema analysis sessions. Each project gets its own subdirectory containing patterns, conventions, and context discovered during analysis.

## Directory Structure

```
memory/skills/database-schema-analysis/
├── index.md (this file)
└── {project-name}/
    ├── schema_summary.md
    ├── naming_conventions.md
    ├── performance_patterns.md
    ├── migration_history.md
    └── query_patterns.md
```

## Project Memory Contents

### schema_summary.md
- Database type and version
- Schema/database inventory
- Table/collection count and sizes
- Relationship overview
- Index inventory

### naming_conventions.md
- Table naming patterns (plural, singular, prefix)
- Column naming patterns (snake_case, camelCase)
- Foreign key naming conventions
- Index naming patterns
- Constraint naming standards

### performance_patterns.md
- Query performance characteristics
- Common slow queries
- Index usage patterns
- Partitioning strategies
- Caching layers

### migration_history.md
- Schema version history
- Migration timestamps
- Breaking changes log
- Rollback procedures
- Data migration notes

### query_patterns.md
- Common query patterns
- JOIN patterns
- Aggregation patterns
- N+1 query occurrences
- Optimization opportunities

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's database is analyzed. The project name is either:
1. Extracted from the database name
2. Specified by the user
3. Derived from the repository name

### Updates
Memory is UPDATED every time the skill analyzes the database:
- Schema changes are tracked
- New patterns are recorded
- Performance characteristics updated
- Migration history appended
- Query patterns refined

### Usage
Memory is READ at the START of every analysis:
- Provides historical context
- Shows evolution over time
- Guides optimization focus
- Informs migration planning
- Ensures consistency in recommendations

## Best Practices

### DO:
- ✅ Update memory after every analysis
- ✅ Track schema evolution over time
- ✅ Document performance changes
- ✅ Record migration history
- ✅ Note query pattern changes

### DON'T:
- ❌ Store actual data or PII
- ❌ Include connection credentials
- ❌ Copy entire DDL dumps (summarize instead)
- ❌ Store temporary analysis reports
- ❌ Include environment-specific details

## Memory vs Context

### Context (`../../context/schema/`)
- **Universal knowledge**: Applies to ALL databases
- **Database-specific patterns**: PostgreSQL, MongoDB, etc.
- **Best practices**: Industry standards, normalization rules
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE database/project
- **Learned patterns**: Discovered during analysis
- **Historical tracking**: Changes over time
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
ecommerce-api/
├── schema_summary.md
│   - PostgreSQL 14.9
│   - 68 tables across 3 schemas (public, orders, inventory)
│   - 850M total rows
│   - Last analyzed: 2025-02-06
│
├── naming_conventions.md
│   - Tables: plural, snake_case (users, order_items)
│   - FKs: {table}_id (user_id, product_id)
│   - Indexes: idx_{table}_{columns}
│   - Constraints: {table}_{type} (users_email_unique)
│
├── performance_patterns.md
│   - Orders table partitioned by created_at (monthly)
│   - Product search uses GIN index on tsvector
│   - Redis cache for user sessions (1hr TTL)
│   - Read replicas for reporting queries
│
├── migration_history.md
│   - v1.0 (2023-01): Initial schema
│   - v1.5 (2023-06): Added inventory schema
│   - v2.0 (2024-01): Partitioned orders table
│   - v2.1 (2024-08): Added full-text search
│
└── query_patterns.md
    - 80% of queries JOIN users ⟷ orders
    - Product catalog uses CTEs for category hierarchy
    - Dashboard aggregations use materialized views
    - Known N+1: Order details loading (needs fix)
```

## Security Considerations

### DO Store:
- Schema structure and patterns
- Index strategies
- Query patterns (anonymized)
- Performance characteristics
- Migration history

### DON'T Store:
- Actual data values
- Connection strings or passwords
- PII or sensitive information
- Production data samples
- Access control credentials

## Integration with Tools

Memory can inform:
- **Migration tools**: Historical context for schema changes
- **Monitoring tools**: Expected performance baselines
- **Documentation generators**: Project-specific patterns
- **Code generators**: Naming conventions for ORM models

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-02-06
**Maintained by**: database-schema-analysis skill
