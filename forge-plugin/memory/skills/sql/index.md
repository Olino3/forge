# SQL Expert - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during SQL tasks. Each project gets its own subdirectory containing engine configuration, query patterns, schema conventions, and compatibility notes discovered during SQL analysis and construction.

## Directory Structure

```
memory/skills/sql/
├── index.md (this file)
└── {project-name}/
    ├── engine_config.md
    ├── query_patterns.md
    ├── schema_conventions.md
    ├── migration_notes.md
    └── compatibility_notes.md
```

## Project Memory Contents

### engine_config.md
- Database engine and version
- Engine-specific extensions or modules in use
- Connection and session configuration
- SQL mode or compatibility level settings
- Feature availability notes (e.g., CTE support, window functions, MERGE)

### query_patterns.md
- Common query shapes used in the project
- Window function patterns (ranking, running totals, pagination)
- CTE patterns (recursive hierarchies, series generation)
- JOIN patterns (preferred join style, anti-join approach)
- Aggregation patterns (ROLLUP, CUBE, GROUPING SETS usage)
- Parameterization approach (prepared statements, named parameters)

### schema_conventions.md
- Table naming patterns (plural, singular, prefixed)
- Column naming standards (snake_case, camelCase)
- Primary key strategy (SERIAL, UUID, IDENTITY)
- Foreign key naming conventions
- Index naming and strategy
- Constraint naming standards
- Partitioning approach
- JSON column usage patterns

### migration_notes.md
- Source and target engine details
- Syntax translations applied
- Data type mappings used
- Feature gaps and workarounds
- Migration scripts and rollback procedures
- Known breaking changes between engine versions

### compatibility_notes.md
- ANSI SQL compliance level
- Engine-specific syntax used with rationale
- Cross-engine portability decisions
- ORM compatibility notes (SQLAlchemy, Entity Framework, Django)
- Functions and operators that differ across engines
- NULL handling conventions for the project

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's SQL is analyzed or constructed. The project name is either:
1. Specified by the user
2. Derived from the repository name
3. Extracted from the database or schema name

### Updates
Memory is UPDATED every time the skill works with a project:
- New query patterns are recorded
- Engine configuration changes tracked
- Migration decisions documented
- Compatibility notes refined
- Schema conventions updated as they evolve

### Usage
Memory is READ at the START of every SQL task:
- Provides engine context (no need to re-ask about engine version)
- Shows established patterns (maintain consistency across queries)
- Informs optimization choices (known indexes, partitioning)
- Guides migration decisions (prior translation mappings)
- Ensures cross-engine consistency (documented compatibility choices)

## Best Practices

### DO:
- ✅ Update memory after every SQL task
- ✅ Record engine-specific decisions and rationale
- ✅ Track query patterns for consistency across the project
- ✅ Document migration translations for reference
- ✅ Note cross-engine compatibility choices
- ✅ Store index strategy and partitioning decisions

### DON'T:
- ❌ Store actual data values or query results
- ❌ Include connection strings or credentials
- ❌ Copy entire SQL dumps (summarize patterns instead)
- ❌ Store PII or sensitive business data
- ❌ Include environment-specific connection details
- ❌ Record temporary debugging queries

## Memory vs Context

### Context (`../../context/database/`)
- **Universal knowledge**: Applies to ALL database engines
- **Engine-specific syntax**: PostgreSQL, MySQL, SQL Server, Oracle, SQLite reference
- **ANSI SQL standards**: Standard-compliant patterns and best practices
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project's SQL work
- **Learned patterns**: Query shapes, conventions, and decisions discovered during tasks
- **Historical tracking**: Engine migrations, schema evolution, optimization history
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
ecommerce-api/
├── engine_config.md
│   - PostgreSQL 16.2
│   - Extensions: pg_trgm, btree_gin, pgcrypto
│   - Session: SET search_path = app, public
│   - Features: MERGE (15+), jsonb, lateral joins
│   - Last confirmed: 2026-02-12
│
├── query_patterns.md
│   - Pagination: keyset (WHERE id > $1 ORDER BY id LIMIT $2)
│   - Hierarchy: recursive CTEs for category tree
│   - Ranking: ROW_NUMBER() for leaderboards
│   - Upsert: INSERT ... ON CONFLICT (sku) DO UPDATE
│   - JSON: jsonb @> containment for metadata filtering
│   - Aggregation: materialized views for dashboard summaries
│
├── schema_conventions.md
│   - Tables: plural, snake_case (orders, order_items)
│   - PKs: UUID via gen_random_uuid()
│   - FKs: {referenced_table_singular}_id (product_id)
│   - Indexes: idx_{table}_{columns} (idx_orders_customer_id)
│   - Partitioning: orders by created_at (monthly range)
│   - JSON: settings stored as jsonb with GIN index
│
├── migration_notes.md
│   - Migrated from MySQL 8 → PostgreSQL 16 (2025-08)
│   - GROUP_CONCAT → STRING_AGG
│   - ON DUPLICATE KEY → ON CONFLICT
│   - TINYINT(1) → BOOLEAN
│   - JSON → JSONB with GIN indexes
│   - AUTO_INCREMENT → GENERATED ALWAYS AS IDENTITY
│
└── compatibility_notes.md
    - Must support PostgreSQL only (no cross-engine)
    - ORM: SQLAlchemy 2.0 with typed models
    - Raw SQL used for: reporting queries, bulk operations
    - COALESCE preferred over PostgreSQL-specific NULLIF patterns
    - All queries parameterized via $1, $2 placeholders
```

## Security Considerations

### DO Store:
- Query patterns and shapes (anonymized)
- Engine configuration and version
- Index strategies and schema conventions
- Migration mappings and translation rules
- Performance tuning decisions

### DON'T Store:
- Actual data values or query results
- Connection strings or passwords
- API keys or tokens
- PII or sensitive business data
- Production hostnames or IP addresses

## Integration with Tools

Memory can inform:
- **Query builders**: Consistent patterns for new queries
- **Migration tools**: Proven translation mappings between engines
- **ORM configuration**: Engine-specific settings and type mappings
- **Code review**: Verify queries follow established project patterns
- **Performance monitoring**: Baseline query shapes and expected plans

---

**Memory System Version**: 1.0.0
**Last Updated**: 2026-02-12
**Maintained by**: sql skill
