# PostgreSQL Expert - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during PostgreSQL administration and optimization sessions. Each project gets its own subdirectory containing cluster configuration, performance baselines, extension inventories, and maintenance history discovered during analysis.

## Directory Structure

```
memory/skills/postgres/
├── index.md (this file)
└── {project-name}/
    ├── cluster_config.md
    ├── performance_baseline.md
    ├── extension_inventory.md
    ├── replication_topology.md
    └── maintenance_log.md
```

## Project Memory Contents

### cluster_config.md
- PostgreSQL version and deployment platform
- Core configuration settings (shared_buffers, work_mem, WAL settings)
- Connection pooling configuration (PgBouncer/pgpool-II settings)
- Resource allocation (CPU, RAM, storage type, IOPS)
- Parameter group overrides (for managed services)
- Custom postgresql.conf and pg_hba.conf highlights

### performance_baseline.md
- Cache hit ratio and buffer usage
- Top queries by total_exec_time (from pg_stat_statements)
- Index usage statistics and missing index candidates
- Table sizes, bloat estimates, and dead tuple counts
- Autovacuum effectiveness and timing
- Connection utilization patterns and peak metrics
- Query latency percentiles (p50, p95, p99)

### extension_inventory.md
- Installed extensions with versions
- Extension-specific configuration (e.g., pg_stat_statements.max, postgis settings)
- Extension usage patterns and dependencies
- Planned extensions and upgrade paths
- Custom functions and operators from extensions

### replication_topology.md
- Replication type (streaming, logical, or both)
- Primary and standby server inventory
- Synchronous vs asynchronous configuration
- Replication lag history and trends
- WAL archiving configuration and retention
- Failover strategy (Patroni, repmgr, manual)
- Backup strategy (pgBackRest, Barman, WAL-G, pg_basebackup)

### maintenance_log.md
- Configuration changes applied with dates and outcomes
- Index changes (created, dropped, rebuilt)
- Vacuum and reindex operations
- Version upgrades performed
- Incidents and resolutions
- Partitioning changes
- Security policy updates (RLS, role changes, pg_hba.conf edits)

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's PostgreSQL environment is analyzed. The project name is either:
1. Specified by the user
2. Derived from the database cluster name
3. Extracted from the repository name

### Updates
Memory is UPDATED every time the skill analyzes the PostgreSQL environment:
- Configuration changes are tracked with before/after values
- Performance baselines are refreshed with new metrics
- Extension inventory is updated when extensions are added or upgraded
- Replication topology changes are recorded
- Maintenance actions are appended to the log

### Usage
Memory is READ at the START of every analysis:
- Provides historical configuration context
- Shows performance trends over time
- Guides optimization based on previous findings
- Informs upgrade planning with known constraints
- Ensures consistency in recommendations across sessions

## Best Practices

### DO:
- ✅ Update memory after every analysis session
- ✅ Track configuration changes with before/after values
- ✅ Record performance baselines for trend analysis
- ✅ Document maintenance operations and their outcomes
- ✅ Note version-specific behaviors and workarounds

### DON'T:
- ❌ Store connection strings, passwords, or credentials
- ❌ Include actual data values or row samples
- ❌ Copy full postgresql.conf files (summarize key overrides only)
- ❌ Store PII or sensitive business data
- ❌ Include environment-specific hostnames or IP addresses

## Memory vs Context

### Context (`../../context/database/`)
- **Universal knowledge**: Applies to ALL PostgreSQL deployments
- **Version-specific features**: Feature matrices across versions
- **Best practices**: Industry-standard tuning guidelines
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE PostgreSQL cluster/project
- **Learned patterns**: Discovered during analysis sessions
- **Historical tracking**: Configuration and performance changes over time
- **Dynamic**: Updated by the skill automatically after each session

## Example Memory Structure

```
saas-platform/
├── cluster_config.md
│   - PostgreSQL 16.2 on RDS db.r6g.2xlarge
│   - shared_buffers: 16GB, work_mem: 32MB
│   - PgBouncer: transaction mode, pool_size=50
│   - max_connections: 100 (reduced from 400)
│   - Last tuned: 2026-01-15
│
├── performance_baseline.md
│   - Cache hit ratio: 99.2% (improved from 94%)
│   - Top query: tenant dashboard (890ms → 120ms after index)
│   - Autovacuum tuned for events table (scale_factor=0.01)
│   - p95 latency: 180ms (target: <200ms)
│
├── extension_inventory.md
│   - pg_stat_statements 1.10 (track_utility=on)
│   - pgAudit 16.0 (SOC2 compliance)
│   - pg_trgm 1.6 (product search)
│   - postgis 3.4.1 (store locations)
│
├── replication_topology.md
│   - 1 primary + 1 read replica (async streaming)
│   - Reports routed to replica
│   - Replication lag: <100ms typical
│   - Backup: RDS automated + manual pg_dump weekly
│
└── maintenance_log.md
    - 2026-01-15: Tuned work_mem 4MB→32MB (report queries 79% faster)
    - 2026-01-15: Reduced max_connections 400→100 (PgBouncer handles pooling)
    - 2026-01-20: Created idx_orders_tenant_created (dashboard 85% faster)
    - 2026-02-01: Enabled pgAudit for SOC2 compliance
    - 2026-02-10: Partitioned events table by month (vacuum 4h→5min)
```

## Security Considerations

### DO Store:
- Configuration parameter values and tuning history
- Performance metrics and trends (anonymized)
- Extension versions and usage patterns
- Replication topology (roles, not hostnames)
- Maintenance actions and outcomes

### DON'T Store:
- Database passwords or authentication tokens
- Connection strings with hostnames or IP addresses
- SSL certificates or private keys
- Actual data values or query results
- pg_hba.conf entries with IP addresses
- IAM credentials or API keys

## Integration with Tools

Memory can inform:
- **Monitoring tools**: Historical baselines for alerting thresholds
- **Migration tools**: Known configuration constraints and dependencies
- **CI/CD pipelines**: Expected performance regression thresholds
- **Capacity planning**: Growth trends and resource utilization patterns
- **Incident response**: Previous resolutions and known failure modes

---

**Memory System Version**: 1.0.0
**Last Updated**: 2026-02-12
**Maintained by**: postgres skill
