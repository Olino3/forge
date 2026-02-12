# Database Optimizer - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during database optimization sessions. Each project gets its own subdirectory containing query performance baselines, index change history, tuning decisions, and workload patterns discovered during optimization.

## Directory Structure

```
memory/skills/database-optimizer/
├── index.md (this file)
└── {project-name}/
    ├── optimization_history.md
    ├── index_inventory.md
    ├── query_baselines.md
    ├── configuration_tuning.md
    └── workload_patterns.md
```

## Project Memory Contents

### optimization_history.md
- Queries optimized with before/after metrics
- Index changes applied and measured impact
- Configuration changes and their effects
- Date and context of each optimization session
- Rollback events and lessons learned

### index_inventory.md
- Current index state (added, removed, modified)
- Index usage statistics snapshots over time
- Redundant/unused index candidates tracked
- Covering index opportunities identified
- Space budget and actual consumption

### query_baselines.md
- Top queries by execution time and frequency
- Established performance baselines per query
- Execution plan fingerprints for regression detection
- SLA targets and current compliance
- Seasonal or time-based performance variations

### configuration_tuning.md
- Database configuration parameters changed
- Before/after values with rationale
- Workload-specific parameter profiles
- Memory allocation history (work_mem, buffer pool, etc.)
- Connection pool sizing decisions

### workload_patterns.md
- Read/write ratio and trends
- Peak-hour query mix
- Batch vs OLTP workload characteristics
- Hot tables and their access patterns
- Growth projections and scaling triggers

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's database queries are optimized. The project name is either:
1. Extracted from the database or application name
2. Specified by the user
3. Derived from the repository name

### Updates
Memory is UPDATED every time the skill optimizes queries or indexes:
- New optimization results are appended to history
- Index inventory is refreshed with current state
- Query baselines are updated with latest metrics
- Configuration changes are recorded
- Workload patterns are refined with new observations

### Usage
Memory is READ at the START of every optimization session:
- Provides historical performance baselines for comparison
- Shows which indexes were previously added or removed
- Reveals past tuning decisions and their outcomes
- Identifies recurring problem queries
- Prevents re-recommending changes that were already tried and reverted

## Best Practices

### DO:
- ✅ Record before/after metrics for every optimization
- ✅ Track index additions AND removals over time
- ✅ Store execution plan fingerprints for regression detection
- ✅ Document configuration change rationale
- ✅ Note workload pattern shifts between sessions

### DON'T:
- ❌ Store actual query result data or row contents
- ❌ Include connection strings or credentials
- ❌ Copy full EXPLAIN output verbatim (summarize key metrics)
- ❌ Store temporary benchmarking artifacts
- ❌ Include environment-specific hostnames or IPs

## Memory vs Context

### Context (`../../context/database/`)
- **Universal knowledge**: Applies to ALL database optimization
- **Engine-specific patterns**: PostgreSQL tuning, MySQL optimization, etc.
- **Best practices**: Index design principles, query anti-patterns
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE database/project
- **Learned baselines**: Discovered during optimization sessions
- **Historical tracking**: Performance changes over time
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
ecommerce-api/
├── optimization_history.md
│   - 2025-01-15: Product search query 4200ms → 35ms (GIN trigram index)
│   - 2025-01-22: N+1 on order items eliminated (joinedload, 81 queries → 1)
│   - 2025-02-01: Index cleanup, dropped 12 unused indexes, saved 2.1GB
│   - 2025-02-06: Report dashboard regression fixed (forced plan via pg_hint_plan)
│
├── index_inventory.md
│   - Added: idx_products_name_trgm (GIN, 180MB) — active, 12K scans/day
│   - Added: idx_orders_user_created (B-tree, 95MB) — active, 8K scans/day
│   - Dropped: idx_orders_legacy_status (unused 90 days)
│   - Candidate: idx_shipments_tracking — only 3 scans/week, monitor
│
├── query_baselines.md
│   - Product search: 35ms p50 / 82ms p99 (target: <200ms) ✅
│   - Order history: 12ms p50 / 28ms p99 (target: <100ms) ✅
│   - Dashboard aggregate: 1.8s p50 / 3.2s p99 (target: <2s) ⚠️
│   - Plan fingerprint: product_search=0x4A2F, order_history=0x8B1C
│
├── configuration_tuning.md
│   - work_mem: 4MB → 16MB (2025-01-15, sort spills eliminated)
│   - effective_cache_size: 4GB → 12GB (2025-01-22, matches actual RAM)
│   - random_page_cost: 4.0 → 1.1 (SSD storage, 2025-02-01)
│
└── workload_patterns.md
    - Read/write ratio: 85/15
    - Peak hours: 10am-2pm UTC (3x baseline traffic)
    - Hot tables: products (60% of reads), orders (70% of writes)
    - Growth: orders table +500K rows/month
    - Batch: nightly report aggregation at 3am UTC
```

## Security Considerations

### DO Store:
- Query patterns and performance metrics
- Index definitions and usage statistics
- Configuration parameter names and values
- Workload characteristics and baselines
- Optimization decisions and rationale

### DON'T Store:
- Actual query result data or row contents
- Connection strings, passwords, or API keys
- PII or sensitive business data
- Production hostnames or IP addresses
- Access control credentials or tokens

## Integration with Tools

Memory can inform:
- **Monitoring dashboards**: Baseline metrics for alert thresholds
- **CI/CD pipelines**: Regression detection in query performance
- **Capacity planning**: Growth projections from workload patterns
- **Incident response**: Historical context for performance degradations
- **Code reviews**: Known slow patterns to watch for in ORM queries

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-02-06
**Maintained by**: database-optimizer skill
