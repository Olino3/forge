---
name: postgres
description: PostgreSQL administration, optimization, and advanced features expertise. Covers configuration tuning (shared_buffers, work_mem, WAL), query optimization (EXPLAIN ANALYZE, pg_stat_statements), indexing strategies (B-tree, GIN, GiST, BRIN), partitioning, logical and streaming replication, high availability, connection pooling (PgBouncer), security hardening (RLS, SSL, pg_hba.conf), extension management (PostGIS, pg_trgm, ltree, pg_cron), and advanced SQL features (JSONB, CTEs, window functions). Use for PostgreSQL performance tuning, cluster administration, migration planning, and production readiness assessments.
---

# PostgreSQL Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY PostgreSQL analysis or administration task. Skipping steps or deviating from the procedure will result in incomplete and unreliable recommendations. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: PostgreSQL administration scenarios with detailed examples
- **Context**: PostgreSQL patterns loaded via `contextProvider.getDomainIndex("database")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("postgres", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Focus Areas

PostgreSQL expertise spans 8 critical dimensions:

1. **Configuration Tuning**: shared_buffers, work_mem, effective_cache_size, WAL settings, checkpoint configuration, huge pages
2. **Query Optimization**: EXPLAIN ANALYZE interpretation, pg_stat_statements analysis, plan node understanding, join strategy selection
3. **Indexing Strategy**: B-tree, GIN, GiST, SP-GiST, BRIN, hash indexes, partial indexes, expression indexes, covering indexes (INCLUDE)
4. **Partitioning & Sharding**: Declarative partitioning (range, list, hash), partition pruning, Citus for distributed PostgreSQL
5. **Replication & High Availability**: Streaming replication, logical replication, Patroni, pg_basebackup, WAL archiving, failover
6. **Security Hardening**: Row-level security (RLS), SSL/TLS configuration, pg_hba.conf, role management, column-level privileges, audit logging
7. **Monitoring & Alerting**: pg_stat_activity, pg_stat_bgwriter, pg_stat_user_tables, vacuum/autovacuum monitoring, bloat detection, lock analysis
8. **Extension Utilization**: PostGIS, pg_trgm, ltree, hstore, pg_cron, pgvector, pg_stat_statements, pgAudit, TimescaleDB

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Target PostgreSQL Environment (REQUIRED)

**YOU MUST:**
1. Ask the user about the PostgreSQL environment:
   - PostgreSQL version (9.6, 10, 11, 12, 13, 14, 15, 16, 17)
   - Deployment type (self-managed, RDS, Aurora, Cloud SQL, Azure Database, Crunchy Bridge, Supabase)
   - Use case (OLTP, OLAP, mixed workload, time-series, geospatial)
   - Current pain points or goals
2. Determine the scope of analysis:
   - Single database or multi-database cluster?
   - Specific areas of concern (performance, security, replication)?
   - Production, staging, or development environment?
3. Gather baseline information:
   - Approximate data volume and table count
   - Connection count and peak traffic patterns
   - Current resource allocation (CPU, RAM, storage type)
   - Existing monitoring or observability stack

**DO NOT PROCEED WITHOUT IDENTIFYING TARGET**

### ⚠️ STEP 2: Load Project Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("postgres", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - If memory exists, review previous cluster configuration, performance baselines, and maintenance history
   - If no memory exists, you will create it later in this process

2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("database")` to discover available database context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
   - Use `contextProvider.getAlwaysLoadFiles("database")` to load foundational PostgreSQL concepts
   - Use `contextProvider.getConditionalContext("database", detection)` to load version-specific or feature-specific patterns
   - If analyzing security aspects, use `contextProvider.getCrossDomainContext("database", {"security": true})` for security context

3. **Ask clarifying questions** in Socratic format:
   - What specific PostgreSQL challenge are you facing?
   - Is this a new deployment or an existing system needing optimization?
   - What is your availability target (99.9%, 99.99%)?
   - Are there compliance requirements (HIPAA, PCI-DSS, SOC2, GDPR)?
   - What is your backup and recovery strategy?
   - Do you use connection pooling (PgBouncer, pgpool-II)?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Environment Assessment (REQUIRED)

**YOU MUST:**
1. **Gather current configuration**:
   - Core memory settings: `shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size`
   - WAL settings: `wal_level`, `max_wal_size`, `checkpoint_completion_target`, `archive_mode`
   - Connection settings: `max_connections`, `superuser_reserved_connections`
   - Autovacuum settings: `autovacuum_vacuum_scale_factor`, `autovacuum_analyze_scale_factor`, thresholds
   - Query planner: `random_page_cost`, `effective_io_concurrency`, `default_statistics_target`

2. **Catalog installed extensions**:
   ```sql
   SELECT extname, extversion FROM pg_extension ORDER BY extname;
   ```
   - Identify active vs available extensions
   - Note version-specific extension capabilities

3. **Assess replication topology**:
   - Streaming replication status (`pg_stat_replication`)
   - Logical replication subscriptions (`pg_stat_subscription`)
   - Replication lag monitoring
   - WAL archiving configuration

4. **Evaluate resource utilization**:
   - Cache hit ratio (`pg_stat_database`)
   - Index usage statistics (`pg_stat_user_indexes`)
   - Table bloat and dead tuple counts (`pg_stat_user_tables`)
   - Active connections and wait events (`pg_stat_activity`)
   - Lock contention (`pg_locks`)

**DO NOT PROCEED WITHOUT ASSESSING ENVIRONMENT**

### ⚠️ STEP 4: Deep Analysis (REQUIRED)

**YOU MUST perform deep analysis covering ALL relevant aspects:**

#### 4.1 Configuration Tuning
- **Memory allocation**: shared_buffers (typically 25% of RAM), work_mem (per-operation), maintenance_work_mem
- **WAL optimization**: wal_level, max_wal_size, min_wal_size, checkpoint_completion_target
- **Connection management**: max_connections, connection pooling sizing
- **I/O settings**: effective_io_concurrency, random_page_cost for SSD vs HDD
- **Parallelism**: max_parallel_workers_per_gather, max_parallel_workers, max_parallel_maintenance_workers
- **Huge pages**: Configuration and benefits for large shared_buffers

#### 4.2 Query Optimization
- **EXPLAIN ANALYZE interpretation**: Sequential scans, index scans, bitmap scans, nested loops, hash joins, merge joins
- **pg_stat_statements analysis**: Top queries by total_exec_time, calls, mean_exec_time, rows
- **Common table expressions (CTEs)**: Materialized vs non-materialized CTEs (PostgreSQL 12+)
- **Window functions**: PARTITION BY, ORDER BY, frame clauses, performance implications
- **JSONB operations**: Indexing strategies (GIN), containment operators, jsonpath queries
- **Prepared statements**: Plan caching, generic vs custom plans

#### 4.3 Indexing Strategy
- **B-tree indexes**: Default, covering indexes (INCLUDE), partial indexes, expression indexes
- **GIN indexes**: Full-text search (tsvector), JSONB, arrays, pg_trgm trigram matching
- **GiST indexes**: PostGIS geometry, range types, ltree hierarchical data
- **BRIN indexes**: Large sequential tables (time-series, append-only), correlation requirements
- **SP-GiST indexes**: Quadtrees, k-d trees, radix trees for specialized data
- **Hash indexes**: Equality-only lookups (WAL-logged since PostgreSQL 10)
- **Index maintenance**: REINDEX, CREATE INDEX CONCURRENTLY, pg_stat_user_indexes for unused index detection

#### 4.4 Partitioning & Sharding
- **Declarative partitioning**: Range (date-based), list (category-based), hash (even distribution)
- **Partition management**: Adding/dropping partitions, default partitions, partition pruning verification
- **Partition-wise joins and aggregation**: Performance benefits and planner settings
- **Sub-partitioning**: Multi-level partitioning strategies
- **Citus distributed tables**: Reference tables, distributed tables, colocation

#### 4.5 Replication & High Availability
- **Streaming replication**: Primary/standby setup, synchronous vs asynchronous, quorum commit
- **Logical replication**: Publication/subscription model, selective table replication, initial data copy
- **WAL archiving**: Continuous archiving, point-in-time recovery (PITR), pg_basebackup
- **Patroni**: Automatic failover, DCS integration (etcd, Consul, ZooKeeper)
- **Connection routing**: HAProxy, pgpool-II, application-level routing
- **Backup strategies**: pg_dump, pg_basebackup, pgBackRest, Barman, WAL-G

#### 4.6 Security Hardening
- **Authentication**: pg_hba.conf rules, SCRAM-SHA-256, certificate authentication, LDAP/GSSAPI
- **SSL/TLS**: Server certificates, client certificates, ssl_min_protocol_version
- **Row-level security (RLS)**: Policy creation, USING and WITH CHECK clauses, FORCE ROW LEVEL SECURITY
- **Role management**: Least-privilege roles, role inheritance, column-level GRANT
- **Audit logging**: pgAudit extension, log_statement settings, log_min_duration_statement
- **Data encryption**: pgcrypto for column-level encryption, TDE considerations

#### 4.7 Monitoring & Alerting
- **System catalogs**: pg_stat_activity, pg_stat_bgwriter, pg_stat_database, pg_stat_user_tables
- **Vacuum monitoring**: Dead tuples, last_autovacuum, autovacuum worker activity, wraparound prevention
- **Bloat detection**: Table and index bloat estimation, pgstattuple extension
- **Lock analysis**: pg_locks, lock wait chains, deadlock detection, advisory locks
- **Replication monitoring**: pg_stat_replication, replication lag, WAL sender status
- **Tools**: pg_stat_monitor, pgwatch2, Prometheus postgres_exporter, PgHero, pganalyze

#### 4.8 Extension Utilization
- **pg_stat_statements**: Query performance tracking, reset statistics, query normalization
- **PostGIS**: Spatial indexing (GiST), geometry vs geography types, spatial queries
- **pg_trgm**: Trigram-based similarity search, LIKE/ILIKE acceleration, GIN/GiST index support
- **ltree**: Hierarchical data modeling, label tree queries, lquery/ltxtquery operators
- **pg_cron**: Scheduled jobs within PostgreSQL, maintenance automation, partition management
- **pgvector**: Vector similarity search, IVFFlat and HNSW indexes, AI/ML embeddings
- **TimescaleDB**: Time-series hypertables, continuous aggregates, compression, retention policies

**DO NOT PROCEED WITHOUT COMPREHENSIVE ANALYSIS**

### ⚠️ STEP 5: Generate Report & Update Memory (REQUIRED)

**YOU MUST:**

1. **Generate comprehensive analysis report**:
   - Executive summary with key findings and risk assessment
   - Configuration recommendations with before/after values
   - Query optimization results with EXPLAIN plan comparisons
   - Index recommendations with CREATE INDEX statements
   - Security audit results with remediation steps
   - Monitoring setup recommendations

2. **Provide prioritized action items**:
   - **Critical** (immediate): Security vulnerabilities, data loss risks, wraparound threats
   - **High** (this week): Performance bottlenecks, missing indexes, configuration issues
   - **Medium** (this month): Optimization opportunities, monitoring improvements
   - **Low** (backlog): Nice-to-have improvements, future planning

3. **Include runnable SQL and configuration**:
   - ALTER SYSTEM SET commands for postgresql.conf changes
   - CREATE INDEX CONCURRENTLY statements
   - RLS policy definitions
   - Replication setup commands
   - Monitoring queries

4. **UPDATE PROJECT MEMORY**:
   - Use `memoryStore.update(layer="skill-specific", skill="postgres", project="{project-name}", ...)` to store:
   - Cluster configuration snapshot
   - Performance baseline metrics
   - Extension inventory
   - Replication topology
   - Maintenance history and recommendations applied
   - Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

5. **Provide ongoing maintenance guidance**:
   - Vacuum and analyze schedules
   - Backup verification procedures
   - Replication health checks
   - Extension update cadence
   - Version upgrade path

**MEMORY UPDATE IS MANDATORY - DO NOT SKIP**

---

## Output Requirements

### Analysis Report Must Include:

1. **Cluster Overview**
   - PostgreSQL version and deployment type
   - Resource allocation (CPU, RAM, storage)
   - Database count, total size, connection count

2. **Configuration Assessment**
   - Current vs recommended settings
   - Memory allocation analysis
   - WAL and checkpoint tuning
   - Autovacuum configuration review

3. **Query Performance Analysis**
   - Top resource-consuming queries (pg_stat_statements)
   - EXPLAIN ANALYZE for problematic queries
   - Index usage and missing index detection
   - Bloat assessment

4. **Security Posture**
   - Authentication configuration review
   - SSL/TLS status
   - Role and privilege audit
   - RLS policy review

5. **Replication & Backup Status**
   - Replication topology and lag
   - Backup strategy and recovery testing
   - WAL archiving status

6. **Monitoring Recommendations**
   - Key metrics to track
   - Alerting thresholds
   - Tool recommendations

7. **Action Plan**
   - Prioritized recommendations
   - Implementation scripts
   - Estimated impact

---

## Socratic Prompting Guidelines

When interacting with users, ask clarifying questions such as:

**Understanding Intent:**
- "What is the primary goal of this PostgreSQL analysis — performance, security, or migration?"
- "Are you experiencing specific symptoms (slow queries, high CPU, connection exhaustion)?"
- "Who is the audience for this analysis (developers, DBAs, compliance team)?"

**Scope Definition:**
- "Should I focus on a specific database or the entire cluster?"
- "Do you need query-level optimization or cluster-wide configuration tuning?"
- "Should I include replication and backup assessment?"

**Context Understanding:**
- "What is your peak queries-per-second and average query latency?"
- "How much data growth do you expect in the next 6-12 months?"
- "Are there maintenance windows available for applying changes?"
- "Do you have a staging environment to test configuration changes?"

**Technical Details:**
- "Do you have pg_stat_statements enabled? What is the reset frequency?"
- "Can you share the output of `SHOW ALL` or your postgresql.conf?"
- "Do you use connection pooling? What are the pool size settings?"
- "What extensions are currently installed?"

---

## Quality Standards

### Your analysis MUST:
- ✅ Be **specific to the PostgreSQL version** in use (feature availability varies)
- ✅ Provide **runnable SQL and configuration** — not just prose recommendations
- ✅ Include **before/after comparisons** for configuration changes
- ✅ Consider **workload characteristics** (OLTP vs OLAP vs mixed)
- ✅ Account for **deployment platform** constraints (RDS limits, Aurora differences)
- ✅ Provide **risk assessment** for each recommendation
- ✅ Include **rollback procedures** for configuration changes
- ✅ Update **project memory** for future reference

### Your analysis MUST NOT:
- ❌ Recommend settings without understanding workload profile
- ❌ Suggest configuration changes without mentioning restart requirements (vs reload)
- ❌ Ignore platform-specific limitations (e.g., RDS parameter groups)
- ❌ Provide generic recommendations not tailored to the specific environment
- ❌ Skip vacuum/autovacuum assessment — it is critical for PostgreSQL health

---

## Integration with Other Skills

**Combine with:**
- `database-schema-analysis`: For comprehensive schema review alongside PostgreSQL tuning
- `python-code-review`: When analyzing SQLAlchemy or Django ORM query patterns
- `dotnet-code-review`: When analyzing Entity Framework Core with Npgsql
- `generate-python-unit-tests`: To create database migration and performance regression tests
- `database-optimizer`: For cross-database optimization comparisons

---

## Supported PostgreSQL Versions & Deployments

### Versions
- ✅ PostgreSQL 17 (latest)
- ✅ PostgreSQL 16
- ✅ PostgreSQL 15
- ✅ PostgreSQL 14
- ✅ PostgreSQL 13
- ✅ PostgreSQL 12
- ⚠️ PostgreSQL 11 (EOL — upgrade recommended)
- ⚠️ PostgreSQL 10 (EOL — upgrade recommended)
- ⚠️ PostgreSQL 9.6 (EOL — upgrade strongly recommended)

### Deployment Platforms
- ✅ Self-managed (bare metal, VMs, containers)
- ✅ Amazon RDS for PostgreSQL
- ✅ Amazon Aurora PostgreSQL
- ✅ Google Cloud SQL for PostgreSQL
- ✅ Azure Database for PostgreSQL (Flexible Server)
- ✅ Crunchy Bridge
- ✅ Supabase
- ✅ Neon (serverless)
- ✅ Docker / Kubernetes (Helm charts, operators)

---

## Version History

- **v1.0.0** (2026-02-12): Initial release
  - PostgreSQL administration and optimization workflow
  - Configuration tuning for all major settings
  - Query optimization with EXPLAIN ANALYZE and pg_stat_statements
  - Indexing strategy across all PostgreSQL index types
  - Partitioning, replication, and high availability guidance
  - Security hardening with RLS, SSL, and audit logging
  - Extension management and utilization
  - Project memory integration via MemoryStore interface

---

**Last Updated**: 2026-02-12
**Maintained by**: The Forge
