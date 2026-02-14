---
name: database-optimizer
## description: Optimize SQL query performance through execution plan analysis, indexing strategies, and performance tuning. Analyzes slow queries, recommends index additions and removals, evaluates execution plans (EXPLAIN/EXPLAIN ANALYZE), identifies anti-patterns like full table scans and implicit conversions, and provides targeted rewrite suggestions. Supports PostgreSQL, MySQL, SQL Server, Oracle, and SQLite. Use for query optimization, index tuning, performance troubleshooting, and database workload analysis.

# Database Query Optimization Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY database optimization analysis. Skipping steps or deviating from the procedure will result in incomplete and unreliable recommendations. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Optimization scenarios with before/after examples
- **Context**: Optimization patterns loaded via `contextProvider.getDomainIndex("database")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("database-optimizer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Focus Areas

Database query optimization evaluates 7 critical dimensions:

1. **Execution Plan Analysis**: EXPLAIN/EXPLAIN ANALYZE output interpretation, cost estimation, row estimates, operator selection
2. **Index Strategy**: B-tree, hash, GIN, GiST, partial, covering, and composite index design and lifecycle management
3. **Query Rewriting**: Subquery elimination, JOIN reordering, predicate pushdown, CTE materialization control
4. **Statistics & Cardinality**: Table statistics freshness, histogram accuracy, cardinality misestimates
5. **Resource Consumption**: I/O cost, memory grants, temp disk usage, parallelism configuration
6. **Workload Patterns**: Read/write ratios, hot tables, peak-hour query profiles, connection pool sizing
7. **Configuration Tuning**: Buffer pool, work memory, query planner parameters, lock contention settings

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Optimization Target (REQUIRED)

**YOU MUST:**
1. Ask the user about the optimization scope:
   - Database system and version (PostgreSQL, MySQL, SQL Server, Oracle, SQLite)
   - Specific slow queries or general workload tuning?
   - Access to EXPLAIN/EXPLAIN ANALYZE output?
   - Access to slow query logs or performance monitoring data?
   - Production vs staging environment?
2. Gather query context:
   - The SQL queries to optimize (exact text)
   - Table sizes and row counts for involved tables
   - Current index definitions on involved tables
   - Expected vs actual execution time
   - Frequency of execution (queries/second)
3. Identify constraints:
   - Acceptable downtime for index creation?
   - Read-heavy vs write-heavy workload?
   - Disk space budget for new indexes?
   - Locking tolerance during optimization?

**DO NOT PROCEED WITHOUT IDENTIFYING TARGET**

### ⚠️ STEP 2: Load Project Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("database-optimizer", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - If memory exists, review previously optimized queries, index changes, and project-specific tuning history
   - If no memory exists, you will create it later in this process

2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("database")` to discover available database context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
   - Use `contextProvider.getAlwaysLoadFiles("database")` to load foundational optimization concepts
   - Use `contextProvider.getConditionalContext("database", detection)` to load engine-specific tuning guides
   - If analyzing application-level patterns, use `contextProvider.getCrossDomainContext("database", {"application": true})` for ORM context

3. **Ask clarifying questions** in Socratic format:
   - What is the primary performance goal (latency, throughput, resource reduction)?
   - Is this a one-time slow query fix or ongoing workload tuning?
   - Are there SLA targets or latency budgets for the queries?
   - What monitoring tools are in place (pg_stat_statements, Performance Schema, DMVs)?
   - Has anything changed recently (data volume growth, schema changes, traffic patterns)?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Extract Performance Data (REQUIRED)

**YOU MUST:**
1. **Collect execution plans** using the appropriate method:

   **For PostgreSQL**:
   ```sql
   EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <query>;
   SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
   SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
   ```

   **For MySQL**:
   ```sql
   EXPLAIN FORMAT=JSON <query>;
   SHOW STATUS LIKE 'Handler_%';
   SELECT * FROM sys.statements_with_full_table_scans;
   ```

   **For SQL Server**:
   ```sql
   SET STATISTICS IO ON; SET STATISTICS TIME ON;
   -- Execute query
   SELECT * FROM sys.dm_exec_query_stats ORDER BY total_worker_time DESC;
   SELECT * FROM sys.dm_db_missing_index_details;
   ```

2. **Collect index metadata**:
   - All indexes on tables involved in the query
   - Index usage statistics (scans, reads, writes)
   - Index sizes and fragmentation levels
   - Unused and duplicate index candidates

3. **Collect table statistics**:
   - Row counts and table sizes
   - Column cardinality and data distribution
   - Statistics freshness (last ANALYZE/UPDATE STATISTICS)
   - Partitioning scheme if applicable

**DO NOT PROCEED WITHOUT EXTRACTING PERFORMANCE DATA**

### ⚠️ STEP 4: Deep Optimization Analysis (REQUIRED)

**YOU MUST perform deep analysis covering ALL these aspects:**

#### 4.1 Execution Plan Interpretation
- **Identify expensive operators**: Sequential scans, nested loops on large sets, hash joins with spills
- **Check row estimate accuracy**: Compare estimated vs actual rows at each operator
- **Evaluate operator ordering**: Is the planner choosing the optimal join order?
- **Detect plan regressions**: Has the plan changed from a known-good state?
- **Assess parallelism**: Is parallel execution used where beneficial?

#### 4.2 Index Optimization
- **Missing index identification**: Columns in WHERE, JOIN, ORDER BY, GROUP BY without supporting indexes
- **Covering index opportunities**: Include columns to enable index-only scans
- **Composite index column ordering**: Selectivity-based ordering, equality before range
- **Partial index candidates**: Filtered indexes for skewed data distributions
- **Redundant index detection**: Indexes that are prefixes of other indexes or never used
- **Index type selection**: B-tree vs hash vs GIN vs GiST based on operator usage

#### 4.3 Query Rewriting
- **Subquery to JOIN conversion**: Correlated subqueries that can be flattened
- **EXISTS vs IN vs JOIN**: Choose the optimal semi-join strategy
- **CTE materialization**: Force or prevent CTE materialization (PostgreSQL 12+)
- **UNION vs UNION ALL**: Eliminate unnecessary deduplication
- **Predicate pushdown**: Move filters closer to base tables
- **Pagination optimization**: Keyset pagination vs OFFSET for large result sets
- **Selective column retrieval**: Replace SELECT * with explicit column lists

#### 4.4 Statistics and Planner Accuracy
- **Stale statistics**: Tables with outdated statistics causing plan misestimates
- **Custom statistics**: Multi-column statistics for correlated columns
- **Histogram boundaries**: Distribution skew not captured by default histograms
- **Planner hints**: When to guide the optimizer (pg_hint_plan, USE INDEX, query hints)

#### 4.5 Resource and Configuration Tuning
- **Memory allocation**: work_mem, sort_buffer_size, memory grants
- **I/O patterns**: Sequential vs random read costs, effective_cache_size
- **Temp space usage**: Queries spilling to disk, temp tablespace sizing
- **Connection pooling**: Pool size relative to active query concurrency
- **Lock contention**: Queries blocked by long-running transactions

#### 4.6 Workload-Level Analysis
- **Hot query identification**: Top queries by total time, frequency, and I/O
- **Read/write contention**: Write-heavy tables with too many indexes
- **Peak-hour patterns**: Queries that degrade during high traffic
- **Batch vs OLTP optimization**: Different tuning strategies per workload type

**DO NOT PROCEED WITHOUT COMPREHENSIVE ANALYSIS**

### ⚠️ STEP 5: Generate Optimization Report & Update Memory (REQUIRED)

**YOU MUST:**

1. **Generate optimization report** including:
   - Executive summary with estimated performance improvement
   - Original query and execution plan
   - Optimized query (if rewritten) with new execution plan
   - Index recommendations (CREATE/DROP statements)
   - Configuration changes (with before/after values)
   - Risk assessment for each recommendation

2. **Prioritize recommendations** using impact/effort matrix:
   - **Quick wins**: Index additions, statistics refresh (minutes)
   - **Medium effort**: Query rewrites, configuration changes (hours)
   - **Long-term**: Schema changes, partitioning, materialized views (days/weeks)

3. **Provide implementation scripts**:
   - Index creation DDL with CONCURRENTLY option where supported
   - Query rewrites with performance comparison
   - Configuration change commands
   - Rollback scripts for each change

4. **UPDATE PROJECT MEMORY**:
   - Use `memoryStore.update(layer="skill-specific", skill="database-optimizer", project="{project-name}", ...)` to store:
   - Optimized queries and their before/after metrics
   - Index changes applied and their measured impact
   - Configuration tuning history
   - Workload patterns and baselines
   - Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

5. **Define validation criteria**:
   - Expected execution time improvement per query
   - Metrics to monitor post-implementation
   - Regression detection approach
   - Follow-up analysis schedule

**MEMORY UPDATE IS MANDATORY - DO NOT SKIP**

---

### Step 6: Generate Output

Create deliverables and save to `/claudedocs/`:
- Follow OUTPUT_CONVENTIONS.md naming: `database-optimizer_{project}_{YYYY-MM-DD}.md`
- Include all required sections
- Provide clear, actionable recommendations

## Output Requirements

### Optimization Report Must Include:

1. **Performance Summary**
   - Current vs target execution time
   - Queries analyzed and optimized
   - Overall improvement estimate

2. **Execution Plan Analysis**
   - Annotated EXPLAIN output
   - Bottleneck identification
   - Operator cost breakdown

3. **Index Recommendations**
   - New indexes with DDL statements
   - Indexes to drop (unused/redundant)
   - Estimated space impact
   - Creation strategy (online vs offline)

4. **Query Rewrites**
   - Original and optimized SQL side by side
   - Explanation of each transformation
   - Expected plan change

5. **Configuration Changes**
   - Parameter name, current value, recommended value
   - Scope (session, database, global)
   - Restart requirements

6. **Implementation Plan**
   - Ordered steps with rollback procedures
   - Timing recommendations (off-peak)
   - Monitoring checkpoints

7. **Risk Assessment**
   - Impact on write performance (new indexes)
   - Regression potential
   - Lock/blocking duration estimates

---

## Socratic Prompting Guidelines

When interacting with users, ask clarifying questions such as:

**Understanding the Problem:**
- "What is the current execution time and what is your target?"
- "Is this query run interactively or as a batch process?"
- "How many times per second/minute is this query executed?"

**Scope Definition:**
- "Should I focus on a single query or analyze the full workload?"
- "Do you have EXPLAIN ANALYZE output, or should I suggest how to collect it?"
- "Are there write-performance concerns alongside read optimization?"

**Context Understanding:**
- "What is the table size and how fast is it growing?"
- "Have you recently changed schema, added data, or upgraded the database?"
- "Are there existing monitoring dashboards or query performance baselines?"

**Technical Details:**
- "Do you use an ORM, and can queries be modified at the SQL level?"
- "Is online (non-blocking) index creation acceptable, or is downtime available?"
- "Are there partitioning or sharding strategies already in place?"

---

## Quality Standards

### Your analysis MUST:
- ✅ Base recommendations on **actual execution plan data**, not guesswork
- ✅ Provide **exact DDL statements** for every index recommendation
- ✅ Show **before/after comparisons** for every query rewrite
- ✅ Consider **write performance impact** of new indexes
- ✅ Include **rollback procedures** for every change
- ✅ Validate **statistics freshness** before blaming the planner
- ✅ Use **database-specific syntax** matching the target engine
- ✅ Update **project memory** for future reference

### Your analysis MUST NOT:
- ❌ Recommend indexes without analyzing the execution plan
- ❌ Ignore write-side impact when adding indexes to write-heavy tables
- ❌ Suggest configuration changes without understanding the workload
- ❌ Provide generic advice not grounded in the specific query and data
- ❌ Overlook locking implications of index creation or schema changes

---

## Integration with Other Skills

**Combine with:**
- `database-schema-analysis`: For full schema understanding before optimization
- `python-code-review`: When optimizing SQLAlchemy or Django ORM queries
- `dotnet-code-review`: When optimizing Entity Framework or Dapper queries
- `file-schema-analysis`: For API query patterns that drive database load

---

## Supported Database Systems

### Fully Supported
- ✅ PostgreSQL (all versions, including EXPLAIN ANALYZE, pg_stat_statements)
- ✅ MySQL / MariaDB (EXPLAIN FORMAT=JSON, Performance Schema, sys schema)
- ✅ Microsoft SQL Server (execution plans, DMVs, Query Store)
- ✅ Oracle Database (EXPLAIN PLAN, AWR, ASH, SQL Tuning Advisor)
- ✅ SQLite (EXPLAIN QUERY PLAN, ANALYZE)

### Partial Support
- ⚠️ Amazon Aurora (PostgreSQL/MySQL compatible, Aurora-specific metrics)
- ⚠️ Google Cloud SQL (engine-specific with cloud console metrics)
- ⚠️ Azure SQL Database (SQL Server compatible with Azure DMVs)
- ⚠️ CockroachDB (PostgreSQL-compatible with distributed plan analysis)

---

## Version History

- **v1.0.0** (2025-02-06): Initial release
  - Execution plan analysis workflow
  - Index optimization recommendations
  - Query rewriting guidance
  - Configuration tuning support
  - Project memory integration
  - Interface-based patterns (ContextProvider + MemoryStore)

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
