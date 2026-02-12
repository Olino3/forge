# postgres Examples

## Usage Scenarios

This document provides practical examples of using the `postgres` skill in various contexts.

---

## Example 1: Performance Tuning for High-Traffic Application

### Scenario
A SaaS application running PostgreSQL 16 on AWS RDS is experiencing slow response times during peak hours. The database handles 5,000 queries/second with 200 concurrent connections.

### User Request
```
Please use skill:postgres to tune our PostgreSQL 16 RDS instance. We're seeing 95th percentile latency spike to 2 seconds during peak hours (9am-5pm). Database is 500GB with 200 concurrent connections.
```

### Skill Workflow

**Step 1**: Environment Identification
- PostgreSQL 16.2 on RDS db.r6g.2xlarge (8 vCPU, 64GB RAM)
- 500GB gp3 storage (3,000 IOPS, 125 MB/s throughput)
- Mixed OLTP workload, SaaS multi-tenant application
- PgBouncer in transaction pooling mode (pool_size=50)

**Step 2**: Socratic Questions
```
I've identified your PostgreSQL 16 RDS environment. Before deep analysis:

1. Do you have pg_stat_statements enabled? What's the reset frequency?
2. Are the latency spikes correlated with specific operations (reports, bulk imports)?
3. What are your current RDS parameter group overrides vs defaults?
4. Do you use read replicas for reporting or analytics queries?
5. What is your autovacuum configuration — have you tuned it from defaults?
6. Any compliance requirements affecting configuration choices?
```

**User Response**:
```
1. Yes, pg_stat_statements is enabled, reset weekly
2. Spikes happen during report generation and user dashboard loads
3. Only changed shared_buffers and max_connections
4. One read replica, but reports still hit primary
5. Default autovacuum settings
6. SOC2 compliance — need audit logging
```

**Step 3**: Environment Assessment
```sql
-- Current configuration snapshot
SHOW shared_buffers;          -- 16GB (default RDS for 64GB)
SHOW work_mem;                -- 4MB (default)
SHOW effective_cache_size;    -- 48GB
SHOW max_connections;         -- 400
SHOW random_page_cost;        -- 4 (HDD default, wrong for gp3)

-- Cache hit ratio
SELECT
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS ratio
FROM pg_statio_user_tables;
-- Result: 0.94 (below optimal 0.99+)

-- Top queries by total time
SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;

-- Autovacuum status
SELECT relname, n_dead_tup, last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;

-- Connection utilization
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
```

**Step 4**: Deep Analysis

Configuration issues identified:
- `work_mem` too low for report queries with large sorts
- `random_page_cost` set for HDD, should be 1.1 for gp3 SSD
- Autovacuum defaults insufficient for high-churn tables
- Reports running on primary instead of read replica
- Cache hit ratio 94% — needs improvement

**Step 5**: Report and Recommendations

```markdown
# PostgreSQL Performance Tuning Report

## Executive Summary
- **Environment**: PostgreSQL 16.2 on RDS db.r6g.2xlarge (64GB RAM)
- **Primary Issue**: Undersized work_mem causing disk-based sorts for reports
- **Secondary Issues**: Default autovacuum, incorrect random_page_cost, reports on primary
- **Expected Improvement**: 60-70% latency reduction during peak hours

## Configuration Changes (via RDS Parameter Group)

### Immediate (No Restart Required)
| Parameter | Current | Recommended | Reason |
|-----------|---------|-------------|--------|
| work_mem | 4MB | 32MB | Eliminate disk sorts for report queries |
| random_page_cost | 4.0 | 1.1 | gp3 SSD — reduce seq scan bias |
| effective_io_concurrency | 1 | 200 | gp3 supports parallel I/O |
| default_statistics_target | 100 | 200 | Better query plans for skewed data |
| checkpoint_completion_target | 0.9 | 0.9 | Already optimal |
| log_min_duration_statement | -1 | 1000 | Log queries over 1 second |

### Restart Required
| Parameter | Current | Recommended | Reason |
|-----------|---------|-------------|--------|
| shared_buffers | 16GB | 16GB | Already correct (25% of RAM) |
| max_connections | 400 | 100 | PgBouncer handles pooling, reduce overhead |
| shared_preload_libraries | pg_stat_statements | pg_stat_statements, pgAudit | SOC2 audit logging |

### Autovacuum Tuning (High-Churn Tables)
```sql
-- For tables with > 1M rows and high update rate
ALTER TABLE events SET (
  autovacuum_vacuum_scale_factor = 0.01,
  autovacuum_analyze_scale_factor = 0.005,
  autovacuum_vacuum_cost_delay = 2
);

ALTER TABLE user_sessions SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_analyze_scale_factor = 0.01
);
```

## Query Optimization

### Report Query (Before)
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT tenant_id, date_trunc('month', created_at), count(*), sum(amount)
FROM orders
WHERE created_at >= now() - interval '12 months'
GROUP BY 1, 2
ORDER BY 1, 2;
```
- Sort Method: **external merge Disk: 256MB** ← work_mem too low
- Execution Time: 4,200ms

### Report Query (After work_mem = 32MB)
- Sort Method: **quicksort Memory: 28MB**
- Execution Time: 890ms (79% improvement)

### Missing Index
```sql
-- Dashboard query scanning 2M rows without index
CREATE INDEX CONCURRENTLY idx_orders_tenant_created
ON orders (tenant_id, created_at DESC)
INCLUDE (amount, status);
```

## Architecture Recommendation
- Route all report/analytics queries to the read replica
- Configure application connection strings: primary (writes + OLTP), replica (reports)

## Action Plan
1. **Today**: Apply parameter group changes (no restart items)
2. **This week**: Create missing index, route reports to replica
3. **Maintenance window**: Restart for max_connections and pgAudit
4. **Next sprint**: Per-table autovacuum tuning, SOC2 audit policy
```

---

## Example 2: Migration from MySQL to PostgreSQL

### Scenario
A team is migrating a 200GB MySQL 8.0 database to PostgreSQL 16 for better JSONB support, full-text search, and advanced SQL features (CTEs, window functions).

### User Request
```
skill:postgres — We're migrating from MySQL 8.0 to PostgreSQL 16. Database is 200GB with 150 tables. We need JSONB for flexible metadata, full-text search for product catalog, and CTEs for reporting. Help us plan the migration.
```

### Skill Workflow

**Step 1**: Environment Identification
- Source: MySQL 8.0.35 on AWS RDS
- Target: PostgreSQL 16 on AWS RDS
- 200GB data, 150 tables, mixed workload
- Key drivers: JSONB, full-text search, advanced SQL

**Step 2**: Socratic Questions
```
Migration from MySQL to PostgreSQL — great choice for your use cases. Let me understand the scope:

1. Do you use MySQL-specific features (ENUM types, AUTO_INCREMENT, FULLTEXT indexes)?
2. Are there stored procedures or triggers to migrate?
3. What ORM/framework do you use (affects migration complexity)?
4. What is your downtime tolerance for the cutover?
5. Do you need to run MySQL and PostgreSQL in parallel during migration?
6. What character encoding does your MySQL database use?
```

**Step 3**: Assessment
- Schema extraction from MySQL information_schema
- Data type mapping analysis
- Query pattern inventory
- Dependency analysis (stored procedures, views, triggers)

**Step 4**: Migration Plan

```markdown
# MySQL → PostgreSQL Migration Plan

## Data Type Mapping

| MySQL Type | PostgreSQL Type | Notes |
|------------|----------------|-------|
| INT AUTO_INCREMENT | SERIAL / GENERATED ALWAYS AS IDENTITY | Prefer IDENTITY (SQL standard) |
| TINYINT(1) | BOOLEAN | Map 0/1 to false/true |
| DATETIME | TIMESTAMP WITHOUT TIME ZONE | Check timezone handling |
| TIMESTAMP | TIMESTAMP WITH TIME ZONE | MySQL TIMESTAMP is UTC-aware |
| JSON | JSONB | Binary JSON — faster queries, indexable |
| ENUM('a','b') | TEXT + CHECK constraint | Or create custom type |
| MEDIUMTEXT / LONGTEXT | TEXT | No length variants in PostgreSQL |
| DOUBLE | DOUBLE PRECISION | Equivalent |
| TINYINT / SMALLINT | SMALLINT | Equivalent |
| UNSIGNED INT | INTEGER + CHECK (col >= 0) | No unsigned types in PostgreSQL |

## Feature Migration

### JSONB (Replacing JSON Columns)
```sql
-- MySQL: Limited JSON queries
SELECT * FROM products WHERE JSON_EXTRACT(metadata, '$.color') = 'red';

-- PostgreSQL: Rich JSONB with indexing
CREATE INDEX idx_products_metadata ON products USING GIN (metadata);
SELECT * FROM products WHERE metadata @> '{"color": "red"}'::jsonb;
SELECT * FROM products WHERE metadata->>'color' = 'red';
```

### Full-Text Search (Replacing MySQL FULLTEXT)
```sql
-- Add tsvector column with GIN index
ALTER TABLE products ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'B')
  ) STORED;

CREATE INDEX idx_products_search ON products USING GIN (search_vector);

-- Query with ranking
SELECT name, ts_rank(search_vector, query) AS rank
FROM products, to_tsquery('english', 'wireless & headphones') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

### CTEs and Window Functions (New Capabilities)
```sql
-- Recursive CTE for category hierarchy
WITH RECURSIVE category_tree AS (
  SELECT id, name, parent_id, 0 AS depth
  FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, c.parent_id, ct.depth + 1
  FROM categories c
  JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY depth, name;

-- Window function for running totals
SELECT
  order_date,
  amount,
  sum(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total,
  row_number() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS recency_rank
FROM orders;
```

## Migration Tools & Process
1. **pgLoader**: Automated MySQL-to-PostgreSQL migration (schema + data)
2. **AWS DMS**: For continuous replication during parallel-run period
3. **pg_dump/pg_restore**: For PostgreSQL-native backup after migration

## Migration Steps
1. Convert schema using pgLoader (auto-maps types)
2. Review and adjust type mappings (ENUM → CHECK, JSON → JSONB)
3. Migrate data with pgLoader or AWS DMS
4. Convert stored procedures to PL/pgSQL
5. Rebuild indexes (GIN for JSONB, GIN for full-text search)
6. Update application queries (MySQL syntax → PostgreSQL)
7. Parallel run with dual writes (2 weeks)
8. Cutover with final data sync
9. Post-migration: Analyze all tables, tune autovacuum

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|
| Query syntax differences | HIGH | Comprehensive test suite |
| Stored procedure conversion | MEDIUM | Rewrite in PL/pgSQL or application code |
| Character encoding | LOW | Both use UTF-8 |
| Sequence gaps after migration | LOW | Reset sequences after data load |
```

---

## Example 3: Implementing Partitioning for Large Tables

### Scenario
An IoT platform stores 2 billion sensor readings in a single PostgreSQL table. Queries are slow, vacuum takes hours, and storage is growing at 50GB/month.

### User Request
```
skill:postgres — Our sensor_readings table has 2 billion rows (1.2TB) and queries are extremely slow. We need to implement partitioning. PostgreSQL 15 on self-managed servers. Queries are always filtered by timestamp range and device_id.
```

### Skill Workflow

**Step 1**: Environment Identification
- PostgreSQL 15.4, self-managed on dedicated servers
- 128GB RAM, 32 vCPU, NVMe storage
- sensor_readings: 2B rows, 1.2TB
- Query pattern: WHERE timestamp BETWEEN x AND y AND device_id = z

**Step 2**: Memory and Context Loading
- No existing project memory found — will create after analysis
- Loaded time-series and partitioning context

**Step 3**: Table Assessment
```sql
-- Current table structure
\d+ sensor_readings
-- Columns: id (bigint), device_id (int), timestamp (timestamptz),
--          value (numeric), unit (text), metadata (jsonb)
-- Indexes: btree(id), btree(timestamp), btree(device_id)
-- Size: 1.2TB data + 380GB indexes

-- Query patterns from pg_stat_statements
SELECT query, calls, mean_exec_time
FROM pg_stat_statements
WHERE query LIKE '%sensor_readings%'
ORDER BY total_exec_time DESC;

-- Vacuum status
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum,
       age(relfrozenxid) AS xid_age
FROM pg_stat_user_tables
WHERE relname = 'sensor_readings';
-- n_dead_tup: 45,000,000 — vacuum struggling
-- xid_age: 850,000,000 — approaching wraparound warning
```

**Step 4**: Partitioning Strategy

**Step 5**: Implementation Report

```markdown
# Partitioning Implementation Plan — sensor_readings

## Strategy: Range Partitioning by Month

### Why Range by Month?
- Queries always filter by timestamp range — perfect for partition pruning
- Monthly partitions of ~80M rows each are manageable for vacuum
- Easy to drop old partitions for data retention
- Combined with device_id index within each partition

## Implementation

### Step 1: Create Partitioned Table
```sql
-- Create new partitioned table structure
CREATE TABLE sensor_readings_partitioned (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    device_id   integer NOT NULL,
    timestamp   timestamptz NOT NULL,
    value       numeric NOT NULL,
    unit        text NOT NULL,
    metadata    jsonb,
    PRIMARY KEY (id, timestamp)  -- partition key must be in PK
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions (example: 2024-2025)
CREATE TABLE sensor_readings_y2024m01 PARTITION OF sensor_readings_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE sensor_readings_y2024m02 PARTITION OF sensor_readings_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
-- ... repeat for each month

-- Create default partition for out-of-range data
CREATE TABLE sensor_readings_default PARTITION OF sensor_readings_partitioned
    DEFAULT;
```

### Step 2: Create Indexes on Partitioned Table
```sql
-- Composite index for common query pattern (created on each partition automatically)
CREATE INDEX ON sensor_readings_partitioned (device_id, timestamp DESC);

-- BRIN index for timestamp range scans (very small, effective for sequential data)
CREATE INDEX ON sensor_readings_partitioned USING BRIN (timestamp)
    WITH (pages_per_range = 32);

-- GIN index for JSONB metadata queries
CREATE INDEX ON sensor_readings_partitioned USING GIN (metadata);
```

### Step 3: Migrate Data (Batched)
```sql
-- Migrate in batches to avoid long locks and WAL bloat
INSERT INTO sensor_readings_partitioned
    (device_id, timestamp, value, unit, metadata)
SELECT device_id, timestamp, value, unit, metadata
FROM sensor_readings
WHERE timestamp >= '2024-01-01' AND timestamp < '2024-02-01';
-- Repeat per month — can parallelize across months
```

### Step 4: Automate Partition Management with pg_cron
```sql
-- Install pg_cron
CREATE EXTENSION pg_cron;

-- Create next month's partition on the 25th of each month
SELECT cron.schedule('create-monthly-partition',
    '0 0 25 * *',
    $$
    SELECT create_next_month_partition('sensor_readings_partitioned');
    $$
);

-- Drop partitions older than 2 years on the 1st of each month
SELECT cron.schedule('drop-old-partitions',
    '0 0 1 * *',
    $$
    SELECT drop_old_partitions('sensor_readings_partitioned', interval '2 years');
    $$
);
```

### Step 5: Verify Partition Pruning
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT avg(value)
FROM sensor_readings_partitioned
WHERE timestamp >= '2024-06-01' AND timestamp < '2024-07-01'
  AND device_id = 42;

-- Expected: Scans ONLY sensor_readings_y2024m06
-- Before: Seq Scan on 1.2TB table → 45 seconds
-- After:  Index Scan on 50GB partition → 12ms
```

## Performance Comparison

| Metric | Before (Unpartitioned) | After (Monthly Partitions) |
|--------|----------------------|---------------------------|
| Monthly range query | 45,000 ms | 12 ms |
| Vacuum duration | 4+ hours | 5 minutes per partition |
| Index size | 380 GB (3 indexes) | ~15 GB per partition |
| Data retention | DELETE + VACUUM | DROP PARTITION (instant) |
| XID wraparound risk | HIGH (age 850M) | LOW (per-partition freeze) |

## Autovacuum Tuning for Partitions
```sql
-- Partitions are smaller — can use aggressive autovacuum
ALTER TABLE sensor_readings_y2024m01 SET (
    autovacuum_vacuum_scale_factor = 0.01,
    autovacuum_analyze_scale_factor = 0.005
);
```

## Monitoring Queries
```sql
-- Partition sizes
SELECT
    tableoid::regclass AS partition_name,
    count(*) AS row_count,
    pg_size_pretty(pg_relation_size(tableoid)) AS size
FROM sensor_readings_partitioned
GROUP BY tableoid
ORDER BY partition_name;

-- Verify partition pruning in queries
SET enable_partition_pruning = on;  -- ensure it is enabled (default)
```
```

---

## Common Patterns

### Pattern: Production Health Check
```
skill:postgres — Run a full health check on our PostgreSQL cluster. Check configuration, vacuum status, replication lag, bloat, and security.
```

### Pattern: Query Performance Troubleshooting
```
skill:postgres — This query takes 30 seconds. Here is the EXPLAIN ANALYZE output. Help me optimize it.
```

### Pattern: Replication Setup
```
skill:postgres — Set up streaming replication with automatic failover using Patroni for our PostgreSQL 16 cluster.
```

### Pattern: Security Audit
```
skill:postgres — Perform a security audit: review pg_hba.conf, SSL configuration, role privileges, and recommend row-level security policies for multi-tenant isolation.
```

### Pattern: Extension Evaluation
```
skill:postgres — We need full-text search with fuzzy matching. Compare pg_trgm + GIN vs tsvector + GIN for our product catalog (5M products).
```

### Pattern: Version Upgrade Planning
```
skill:postgres — Plan an upgrade from PostgreSQL 13 to 16. Identify breaking changes, new features to adopt, and a zero-downtime upgrade strategy using logical replication.
```

---

**Last Updated**: 2026-02-12
**Maintained by**: The Forge
