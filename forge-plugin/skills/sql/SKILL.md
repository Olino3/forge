---
name: sql
description: Expert SQL across multiple database engines including PostgreSQL, MySQL, SQL Server, Oracle, and SQLite. Constructs optimized queries, designs schemas, writes migrations, and ensures cross-engine compatibility. Covers ANSI SQL standards, advanced JOINs, window functions, CTEs (recursive and non-recursive), MERGE/UPSERT patterns, JSON operations, temporal tables, stored procedures, query plan analysis, and parameterized queries for security. Use for query construction, performance tuning, schema design, data migration, and cross-engine SQL translation.
---

# SQL Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY SQL task. Skipping steps or deviating from the procedure will result in incorrect, insecure, or non-portable SQL. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: SQL scenarios with detailed walkthroughs and code output
- **Context**: SQL and database patterns loaded via `contextProvider.getDomainIndex("database")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("sql", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Focus Areas

SQL expertise evaluates 8 critical dimensions:

1. **Query Construction**: SELECT, INSERT, UPDATE, DELETE with ANSI SQL compliance and engine-specific optimizations
2. **Joins & Subqueries**: INNER, LEFT/RIGHT/FULL OUTER, CROSS, LATERAL joins; correlated subqueries; anti-join patterns; semi-joins
3. **Aggregation & Window Functions**: GROUP BY, HAVING, ROLLUP, CUBE; ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, NTILE, FIRST_VALUE, LAST_VALUE
4. **CTEs & Recursive Queries**: Common Table Expressions for readability; recursive CTEs for hierarchies, graphs, and series generation
5. **DDL & Schema Design**: CREATE/ALTER/DROP with constraints, indexes, partitioning, and normalization best practices
6. **Cross-Engine Compatibility**: ANSI SQL vs dialect-specific syntax; MERGE/UPSERT variations; JSON operations across engines; temporal table implementations
7. **Security & Parameterization**: Prepared statements, parameterized queries, SQL injection prevention, row-level security, dynamic SQL safety
8. **Performance & Query Plans**: EXPLAIN/EXPLAIN ANALYZE interpretation, index strategy, query rewriting, materialized views, statistics management

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Target Database Engine & SQL Task (REQUIRED)

**YOU MUST:**
1. Ask the user about the target environment:
   - Database engine (PostgreSQL, MySQL/MariaDB, SQL Server, Oracle, SQLite)
   - Engine version (critical for feature availability)
   - Use case (query writing, schema design, migration, optimization, debugging)
2. Clarify the SQL task:
   - Writing a new query from scratch?
   - Optimizing an existing slow query?
   - Designing tables and relationships?
   - Migrating SQL between engines?
   - Writing stored procedures or functions?
   - Building reports with complex aggregations?
3. Identify constraints:
   - Must the SQL be ANSI-compatible across engines?
   - Are there ORM restrictions (e.g., Django, SQLAlchemy, Entity Framework)?
   - Performance requirements (latency, throughput)?
   - Data volume and growth projections?

**DO NOT PROCEED WITHOUT IDENTIFYING TARGET**

### ⚠️ STEP 2: Load Project Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("sql", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - If memory exists, review engine configuration, query patterns, schema conventions, and compatibility notes
   - If no memory exists, you will create it later in this process

2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("database")` to discover available database context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
   - Use `contextProvider.getAlwaysLoadFiles("database")` to load foundational SQL concepts
   - Use `contextProvider.getConditionalContext("database", detection)` to load engine-specific patterns
   - If cross-engine compatibility is needed, use `contextProvider.getCrossDomainContext("database", {"compatibility": true})` for dialect comparison context

3. **Ask clarifying questions** in Socratic format:
   - What is the business goal behind this SQL task?
   - What tables and relationships are involved?
   - What data volumes are we working with?
   - Are there existing queries I should reference or improve?
   - What indexing strategy is currently in place?
   - Are there cross-engine portability requirements?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Analyze Requirements (REQUIRED)

**YOU MUST:**
1. **Understand the data model**:
   - Review table definitions, column types, and constraints
   - Map relationships (foreign keys, junction tables, implicit references)
   - Identify relevant indexes and their coverage
   - Note partitioning, sharding, or replication details

2. **Clarify query goals**:
   - Expected result set shape (columns, rows, ordering)
   - Filtering criteria and edge cases (NULLs, empty sets, duplicates)
   - Aggregation requirements (totals, averages, running calculations)
   - Pagination or limiting requirements
   - Temporal considerations (point-in-time, date ranges, time zones)

3. **Assess engine-specific capabilities**:
   - Feature availability in the target engine version
   - Syntax differences for the planned approach
   - Known limitations or gotchas
   - Available extensions or modules (e.g., pg_trgm, PostGIS)

**DO NOT PROCEED WITHOUT ANALYZING REQUIREMENTS**

### ⚠️ STEP 4: Deep SQL Analysis & Construction (REQUIRED)

**YOU MUST perform thorough SQL work covering ALL relevant aspects:**

#### 4.1 Query Construction
- **SELECT statements**: Column selection, expressions, aliases, DISTINCT
- **Filtering**: WHERE clauses, IN/EXISTS, BETWEEN, LIKE/ILIKE, regex
- **Ordering**: ORDER BY with NULLS FIRST/LAST, collation-aware sorting
- **Limiting**: LIMIT/OFFSET, FETCH FIRST, TOP (engine-specific)
- **Set operations**: UNION, INTERSECT, EXCEPT with ALL variants

#### 4.2 Joins & Subqueries
- **Standard joins**: INNER, LEFT/RIGHT/FULL OUTER with ON conditions
- **Advanced joins**: LATERAL joins (PostgreSQL/MySQL 8+), CROSS APPLY (SQL Server)
- **Anti-join patterns**: LEFT JOIN ... WHERE IS NULL vs NOT EXISTS vs NOT IN (NULL safety)
- **Semi-join patterns**: EXISTS vs IN for existence checks
- **Self-joins**: Hierarchical data, row comparison
- **Correlated subqueries**: Row-by-row evaluation, performance implications

#### 4.3 Aggregation & Window Functions
- **Grouping**: GROUP BY, HAVING, GROUPING SETS, ROLLUP, CUBE
- **Ranking**: ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE()
- **Offset functions**: LAG(), LEAD(), FIRST_VALUE(), LAST_VALUE(), NTH_VALUE()
- **Aggregate windows**: SUM/AVG/COUNT OVER (PARTITION BY ... ORDER BY ...)
- **Frame specifications**: ROWS vs RANGE vs GROUPS, UNBOUNDED PRECEDING/FOLLOWING
- **Running totals and moving averages**: Cumulative calculations with proper frames

#### 4.4 CTEs & Recursive Queries
- **Non-recursive CTEs**: Query decomposition, readability, reuse
- **Recursive CTEs**: WITH RECURSIVE for hierarchies (org charts, categories, BOMs)
- **Graph traversal**: Path finding, cycle detection with recursive CTEs
- **Series generation**: Generate date series, number sequences
- **CTE materialization**: PostgreSQL MATERIALIZED/NOT MATERIALIZED hints

#### 4.5 DDL & Schema Design
- **Table creation**: Data types, constraints, defaults, generated columns
- **Indexes**: B-tree, hash, GIN, GiST, BRIN; partial indexes; expression indexes
- **Constraints**: PRIMARY KEY, FOREIGN KEY (CASCADE/SET NULL/RESTRICT), UNIQUE, CHECK, EXCLUDE
- **Partitioning**: Range, list, hash partitioning; partition pruning
- **Normalization**: 1NF through BCNF; strategic denormalization

#### 4.6 DML Operations
- **INSERT**: Single-row, multi-row, INSERT ... SELECT, INSERT ... RETURNING
- **UPDATE**: Standard, UPDATE ... FROM (PostgreSQL), UPDATE with JOIN (MySQL/SQL Server)
- **DELETE**: Targeted deletion, DELETE with JOIN, cascading implications
- **MERGE/UPSERT**: INSERT ... ON CONFLICT (PostgreSQL), INSERT ... ON DUPLICATE KEY (MySQL), MERGE (SQL Server/Oracle)
- **TRUNCATE**: Fast table clearing vs DELETE, foreign key implications

#### 4.7 Stored Procedures & Functions
- **Functions**: Scalar, table-valued, aggregate (engine-specific syntax)
- **Procedures**: Transaction control, error handling, output parameters
- **Triggers**: BEFORE/AFTER, row-level vs statement-level, NEW/OLD references
- **Dynamic SQL**: EXECUTE IMMEDIATE (Oracle), EXECUTE (PostgreSQL), sp_executesql (SQL Server)
- **Error handling**: TRY/CATCH (SQL Server), EXCEPTION blocks (PostgreSQL/Oracle), HANDLER (MySQL)

#### 4.8 Cross-Engine Compatibility
- **Data type mapping**: VARCHAR/NVARCHAR, INTEGER/BIGINT, BOOLEAN, TIMESTAMP/DATETIME
- **JSON operations**: PostgreSQL jsonb vs MySQL JSON vs SQL Server JSON_VALUE/JSON_QUERY
- **Temporal tables**: SQL Server system-versioned vs PostgreSQL temporal extensions
- **Identity columns**: SERIAL/IDENTITY (PostgreSQL), AUTO_INCREMENT (MySQL), IDENTITY (SQL Server), SEQUENCE (Oracle)
- **String functions**: CONCAT, SUBSTRING, string_agg/GROUP_CONCAT/STRING_AGG/LISTAGG
- **Date/time functions**: EXTRACT, DATE_TRUNC, DATEADD/DATEDIFF, interval arithmetic
- **NULL handling**: COALESCE, NULLIF, IFNULL/ISNULL/NVL engine differences

**USE parameterized queries and avoid SQL injection vulnerabilities in ALL generated SQL**

**DO NOT PROCEED WITHOUT COMPREHENSIVE ANALYSIS**

### ⚠️ STEP 5: Generate Report & Update Memory (REQUIRED)

**YOU MUST:**

1. **Deliver the SQL solution**:
   - Complete, tested SQL code with comments explaining logic
   - Engine-specific syntax highlighted where applicable
   - Alternative approaches with trade-off analysis
   - EXPLAIN plan interpretation if optimizing

2. **Provide supporting analysis**:
   - Index recommendations for the queries
   - Performance characteristics and expected behavior
   - Edge case handling (NULLs, empty results, large datasets)
   - Security notes (parameterization, permissions)

3. **Cross-engine notes** (if applicable):
   - Syntax differences across target engines
   - Feature availability matrix
   - Migration path if porting SQL

4. **UPDATE PROJECT MEMORY**:
   - Use `memoryStore.update(layer="skill-specific", skill="sql", project="{project-name}", ...)` to store:
   - Engine type and version
   - Query patterns used in this project
   - Schema conventions and naming standards
   - Cross-engine compatibility notes
   - Performance tuning decisions
   - Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

5. **Provide actionable next steps**:
   - Testing recommendations
   - Index creation scripts
   - Migration scripts if changing engines
   - Monitoring queries for ongoing performance tracking

**MEMORY UPDATE IS MANDATORY - DO NOT SKIP**

---

## Output Requirements

### SQL Deliverables Must Include:

1. **Complete SQL Code**
   - Fully functional, copy-paste ready
   - Comments explaining non-obvious logic
   - Parameterized (no inline literals for user input)

2. **Engine Specification**
   - Target engine and minimum version
   - Required extensions or modules
   - Compatibility notes for other engines

3. **Performance Analysis**
   - Expected query plan behavior
   - Index requirements
   - Estimated cost or row counts where applicable

4. **Security Considerations**
   - Parameterized query format
   - Required permissions (SELECT, INSERT, EXECUTE)
   - Row-level security implications

5. **Testing Guidance**
   - Edge cases to verify
   - Sample test data
   - Expected results for validation

---

## Socratic Prompting Guidelines

When interacting with users, ask clarifying questions such as:

**Understanding Intent:**
- "What business question does this query need to answer?"
- "Is this for a one-time report or a recurring application query?"
- "Who consumes the output — an application, a dashboard, or a person?"

**Technical Scope:**
- "Which database engine and version are you targeting?"
- "What tables and columns are involved?"
- "What's the approximate data volume (row counts, table sizes)?"
- "Are there existing indexes on the columns you'll filter or join on?"

**Constraints & Requirements:**
- "Does this need to run under a specific latency target?"
- "Must the SQL be portable across multiple database engines?"
- "Are there ORM constraints I should account for?"
- "How should NULLs and missing data be handled?"

**Optimization Context:**
- "Do you have the current EXPLAIN output for a slow query?"
- "What's the query frequency (once daily, thousands per second)?"
- "Are materialized views or caching layers available?"

---

## Quality Standards

### Your SQL MUST:
- ✅ Be **syntactically correct** for the target engine and version
- ✅ Use **parameterized queries** — never concatenate user input
- ✅ Handle **NULL values** explicitly and correctly
- ✅ Include **appropriate indexes** for the query patterns
- ✅ Follow **ANSI SQL standards** where possible for portability
- ✅ Include **comments** for complex logic
- ✅ Be **properly formatted** with consistent indentation
- ✅ Update **project memory** for future reference

### Your SQL MUST NOT:
- ❌ Contain **SQL injection vulnerabilities** (no string concatenation of user input)
- ❌ Use **SELECT \*** in production queries (specify columns explicitly)
- ❌ Ignore **NULL semantics** (three-valued logic)
- ❌ Recommend **unnecessary cursors** when set-based operations work
- ❌ Use **engine-specific syntax without disclosure** of portability impact
- ❌ Produce **Cartesian products** without explicit intent

---

## Integration with Other Skills

**Combine with:**
- `database-schema-analysis`: For understanding existing schema before writing queries
- `python-code-review`: When reviewing SQLAlchemy queries or raw SQL in Python
- `dotnet-code-review`: When reviewing Entity Framework LINQ-to-SQL or Dapper queries
- `generate-python-unit-tests`: To create tests for SQL-backed data access layers
- `file-schema-analysis`: For API schemas that drive database queries

---

## Supported Database Engines

### Primary Engines (Full Support)
- ✅ PostgreSQL (12+) — jsonb, CTEs, window functions, lateral joins, MERGE (15+)
- ✅ MySQL (8.0+) — CTEs, window functions, JSON, lateral derived tables
- ✅ Microsoft SQL Server (2016+) — MERGE, JSON, temporal tables, CROSS APPLY
- ✅ Oracle Database (19c+) — MERGE, analytic functions, hierarchical queries, JSON
- ✅ SQLite (3.35+) — CTEs, window functions, RETURNING, UPSERT

### Cloud-Managed Variants
- ✅ Amazon Aurora (PostgreSQL/MySQL compatible)
- ✅ Azure SQL Database
- ✅ Google Cloud SQL
- ✅ Amazon RDS

### ANSI SQL Standards
- ✅ SQL:2016 — JSON operations, row pattern matching
- ✅ SQL:2011 — Temporal tables, FETCH FIRST
- ✅ SQL:2003 — Window functions, MERGE, sequences
- ✅ SQL:1999 — CTEs, recursive queries, triggers

---

## Version History

- **v1.0.0** (2026-02-12): Initial release
  - Cross-engine SQL expertise (PostgreSQL, MySQL, SQL Server, Oracle, SQLite)
  - Advanced query construction with CTEs, window functions, and MERGE/UPSERT
  - JSON operations and temporal table support across engines
  - Query plan analysis and optimization guidance
  - Parameterized query patterns for security
  - Interface-based context and memory integration

---

**Last Updated**: 2026-02-12
**Maintained by**: The Forge
