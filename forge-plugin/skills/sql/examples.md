# sql Examples

## Usage Scenarios

This document provides practical examples of using the `sql` skill in various contexts.

---

## Example 1: Complex Reporting Query with Window Functions

### Scenario
You need a monthly sales report showing each product's revenue, its rank within its category, the running total, and month-over-month growth percentage. The target is PostgreSQL 15.

### User Request
```
Please use skill:sql to build a monthly sales report for PostgreSQL. I need revenue by product, category ranking, running totals, and month-over-month growth.
```

### Skill Workflow

**Step 1**: Database Identification
- Identifies PostgreSQL 15
- Confirms reporting query (read-only)
- Notes that window functions and CTEs are fully supported

**Step 2**: Socratic Questions
```
Before I build this report, a few clarifications:

1. Which tables hold orders, products, and categories?
2. Should revenue be based on order_date or ship_date?
3. Do you need to filter by date range, or show all historical data?
4. Should the month-over-month growth compare to the immediately prior month?
5. How should months with zero sales for a product be handled — omit or show as $0?
```

**User Response**:
```
1. Tables: orders, order_items, products, categories
2. Use order_date
3. Last 12 months
4. Yes, compare to prior month
5. Show as $0 with 0% growth
```

**Step 3**: Requirements Analysis
- Tables: `orders` → `order_items` → `products` → `categories`
- Revenue = `order_items.quantity * order_items.unit_price`
- Need `generate_series` to fill gaps for months with zero sales
- Window functions: `RANK()` for category ranking, `SUM() OVER` for running total, `LAG()` for MoM growth

**Step 4-5**: SQL Construction & Report

```sql
-- Monthly Sales Report with Category Ranking, Running Totals, and MoM Growth
-- Engine: PostgreSQL 15+
-- Parameters: $1 = report_start_date

WITH months AS (
    -- Generate a continuous month series to handle zero-sale months
    SELECT DATE_TRUNC('month', d)::date AS month_start
    FROM generate_series(
        CURRENT_DATE - INTERVAL '12 months',
        CURRENT_DATE,
        INTERVAL '1 month'
    ) AS d
),
product_monthly_revenue AS (
    -- Aggregate revenue per product per month
    SELECT
        p.id                                      AS product_id,
        p.name                                    AS product_name,
        c.name                                    AS category_name,
        DATE_TRUNC('month', o.order_date)::date   AS month_start,
        SUM(oi.quantity * oi.unit_price)           AS revenue,
        SUM(oi.quantity)                           AS units_sold
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.id
    JOIN products p     ON p.id = oi.product_id
    JOIN categories c   ON c.id = p.category_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY p.id, p.name, c.name, DATE_TRUNC('month', o.order_date)
),
all_product_months AS (
    -- Cross join products with months, then left join revenue to fill gaps
    SELECT
        dp.product_id,
        dp.product_name,
        dp.category_name,
        m.month_start,
        COALESCE(pmr.revenue, 0)    AS revenue,
        COALESCE(pmr.units_sold, 0) AS units_sold
    FROM (
        SELECT DISTINCT product_id, product_name, category_name
        FROM product_monthly_revenue
    ) dp
    CROSS JOIN months m
    LEFT JOIN product_monthly_revenue pmr
        ON pmr.product_id = dp.product_id
        AND pmr.month_start = m.month_start
)
SELECT
    month_start,
    product_name,
    category_name,
    revenue,
    units_sold,

    -- Rank within category for the month
    RANK() OVER (
        PARTITION BY month_start, category_name
        ORDER BY revenue DESC
    ) AS category_rank,

    -- Running total of revenue across months for each product
    SUM(revenue) OVER (
        PARTITION BY product_id
        ORDER BY month_start
        ROWS UNBOUNDED PRECEDING
    ) AS cumulative_revenue,

    -- Month-over-month growth percentage
    CASE
        WHEN LAG(revenue) OVER (
            PARTITION BY product_id ORDER BY month_start
        ) = 0 THEN 0
        ELSE ROUND(
            (revenue - LAG(revenue) OVER (
                PARTITION BY product_id ORDER BY month_start
            )) * 100.0
            / NULLIF(LAG(revenue) OVER (
                PARTITION BY product_id ORDER BY month_start
            ), 0),
            2
        )
    END AS mom_growth_pct

FROM all_product_months
ORDER BY month_start DESC, category_name, category_rank;
```

### Index Recommendations
```sql
-- Support the date range filter and join pattern
CREATE INDEX idx_orders_order_date ON orders (order_date);
CREATE INDEX idx_order_items_order_product ON order_items (order_id, product_id);
```

---

## Example 2: Data Migration Between Engines (MySQL to PostgreSQL)

### Scenario
Migrating an application from MySQL 8 to PostgreSQL 16. Several queries use MySQL-specific syntax that needs translation, including UPSERT, JSON operations, and string aggregation.

### User Request
```
skill:sql - We're migrating from MySQL 8 to PostgreSQL 16. Help translate our key queries and highlight syntax differences.
```

### Skill Workflow

**Step 1**: Engine Identification
- Source: MySQL 8.0
- Target: PostgreSQL 16
- Task: SQL dialect migration

**Step 2**: Socratic Questions
```
To ensure a smooth migration:

1. How many distinct queries need translation?
2. Do you use MySQL-specific features like REPLACE INTO, GROUP_CONCAT, or JSON_TABLE?
3. Are stored procedures or triggers involved?
4. Do you rely on AUTO_INCREMENT behavior (e.g., retrieving last insert ID)?
5. Are there any MySQL-specific data types (ENUM, SET, TINYINT as boolean)?
```

**Step 3-5**: Migration Analysis & Translation

#### UPSERT Pattern

**MySQL (source)**:
```sql
INSERT INTO user_preferences (user_id, preference_key, preference_value, updated_at)
VALUES (?, ?, ?, NOW())
ON DUPLICATE KEY UPDATE
    preference_value = VALUES(preference_value),
    updated_at = NOW();
```

**PostgreSQL (target)**:
```sql
-- PostgreSQL uses ON CONFLICT instead of ON DUPLICATE KEY UPDATE
-- Requires a unique constraint or index on (user_id, preference_key)
INSERT INTO user_preferences (user_id, preference_key, preference_value, updated_at)
VALUES ($1, $2, $3, NOW())
ON CONFLICT (user_id, preference_key) DO UPDATE SET
    preference_value = EXCLUDED.preference_value,
    updated_at = NOW();
```

**Key difference**: MySQL uses `VALUES(col)` to reference the proposed row; PostgreSQL uses `EXCLUDED.col`.

#### JSON Operations

**MySQL (source)**:
```sql
SELECT
    id,
    JSON_EXTRACT(metadata, '$.theme') AS theme,
    JSON_UNQUOTE(JSON_EXTRACT(metadata, '$.locale')) AS locale,
    JSON_LENGTH(JSON_EXTRACT(metadata, '$.tags')) AS tag_count
FROM user_settings
WHERE JSON_CONTAINS(metadata, '"dark"', '$.theme');
```

**PostgreSQL (target)**:
```sql
-- PostgreSQL uses jsonb operators for concise, indexable JSON access
SELECT
    id,
    metadata->>'theme'                    AS theme,
    metadata->>'locale'                   AS locale,
    jsonb_array_length(metadata->'tags')  AS tag_count
FROM user_settings
WHERE metadata @> '{"theme": "dark"}';

-- Support the containment query with a GIN index
CREATE INDEX idx_user_settings_metadata ON user_settings USING GIN (metadata);
```

**Key difference**: PostgreSQL `jsonb` operators (`->`, `->>`, `@>`) replace MySQL's `JSON_EXTRACT`/`JSON_CONTAINS` functions, and GIN indexes provide native JSON search performance.

#### String Aggregation

**MySQL (source)**:
```sql
SELECT
    department_id,
    GROUP_CONCAT(employee_name ORDER BY employee_name SEPARATOR ', ') AS team_members
FROM employees
GROUP BY department_id;
```

**PostgreSQL (target)**:
```sql
-- PostgreSQL uses STRING_AGG instead of GROUP_CONCAT
SELECT
    department_id,
    STRING_AGG(employee_name, ', ' ORDER BY employee_name) AS team_members
FROM employees
GROUP BY department_id;
```

#### Data Type Migration Reference

| MySQL Type | PostgreSQL Type | Notes |
|------------|----------------|-------|
| `TINYINT(1)` | `BOOLEAN` | MySQL uses 0/1; PostgreSQL uses TRUE/FALSE |
| `AUTO_INCREMENT` | `GENERATED ALWAYS AS IDENTITY` | Or use `SERIAL` (legacy) |
| `DATETIME` | `TIMESTAMP` | Add `WITH TIME ZONE` for timezone awareness |
| `ENUM('a','b')` | `TEXT CHECK (col IN ('a','b'))` | Or create a custom enum type |
| `JSON` | `JSONB` | Use `jsonb` for indexable, binary JSON |
| `DOUBLE` | `DOUBLE PRECISION` | Identical IEEE 754 semantics |
| `MEDIUMTEXT` | `TEXT` | PostgreSQL TEXT has no size limit |

---

## Example 3: Multi-Tenant Schema with Row-Level Security

### Scenario
Designing a multi-tenant SaaS database on PostgreSQL 16 with row-level security (RLS), tenant isolation, and shared schema. Must support tenant-scoped queries that are transparent to the application.

### User Request
```
skill:sql - Design a multi-tenant schema with row-level security in PostgreSQL. We need complete tenant isolation with a shared database approach.
```

### Skill Workflow

**Step 1**: Engine Identification
- PostgreSQL 16 (RLS fully supported)
- Schema design + security task
- Shared-database, shared-schema multi-tenancy

**Step 2**: Socratic Questions
```
For the multi-tenant design:

1. How many tenants do you expect (10s, 1000s, millions)?
2. Should tenants share tables (row-level isolation) or have separate schemas?
3. How is the current tenant identified at the application level (JWT claim, session variable)?
4. Are there any cross-tenant queries needed (admin dashboards, analytics)?
5. Do you need tenant-specific customizations (custom fields, different limits)?
6. What entities need tenant scoping (all tables, or specific ones)?
```

**User Response**:
```
1. Hundreds of tenants, growing to thousands
2. Shared tables with row-level isolation
3. JWT claim passed as session variable (app.current_tenant_id)
4. Yes, admin users need cross-tenant access
5. Not initially, but we want flexibility
6. All application tables should be tenant-scoped
```

**Step 3-5**: Schema Design & RLS Implementation

```sql
-- ============================================================
-- Multi-Tenant Schema with Row-Level Security
-- Engine: PostgreSQL 16+
-- ============================================================

-- 1. Tenant Registry (not RLS-protected; managed by platform)
CREATE TABLE tenants (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    slug        TEXT NOT NULL UNIQUE,
    plan        TEXT NOT NULL DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'enterprise')),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Tenant-scoped application tables
CREATE TABLE projects (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id   UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE tasks (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id   UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    project_id  UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'done')),
    assigned_to UUID,
    due_date    DATE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Indexes for tenant-scoped queries (tenant_id always leads)
CREATE INDEX idx_projects_tenant ON projects (tenant_id);
CREATE INDEX idx_tasks_tenant ON tasks (tenant_id);
CREATE INDEX idx_tasks_tenant_project ON tasks (tenant_id, project_id);
CREATE INDEX idx_tasks_tenant_status ON tasks (tenant_id, status);

-- 4. Enable Row-Level Security on tenant-scoped tables
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owners (critical for security)
ALTER TABLE projects FORCE ROW LEVEL SECURITY;
ALTER TABLE tasks FORCE ROW LEVEL SECURITY;

-- 5. RLS Policies: tenant isolation
-- The application sets current_setting('app.current_tenant_id') on each connection

CREATE POLICY tenant_isolation_projects ON projects
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

CREATE POLICY tenant_isolation_tasks ON tasks
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- 6. Admin bypass policy (for cross-tenant dashboards)
-- Admins set current_setting('app.is_admin') = 'true'

CREATE POLICY admin_bypass_projects ON projects
    USING (current_setting('app.is_admin', TRUE)::boolean = TRUE);

CREATE POLICY admin_bypass_tasks ON tasks
    USING (current_setting('app.is_admin', TRUE)::boolean = TRUE);

-- 7. Application connection setup (run at the start of each request)
-- This is called by the connection pool / middleware:

-- For regular tenant users:
SET LOCAL app.current_tenant_id = '550e8400-e29b-41d4-a716-446655440000';
SET LOCAL app.is_admin = 'false';

-- For admin users:
SET LOCAL app.is_admin = 'true';

-- 8. Transparent tenant-scoped queries (no WHERE tenant_id = ... needed)
-- RLS automatically filters rows

-- Application query — RLS enforces tenant isolation transparently
SELECT p.name, COUNT(t.id) AS task_count, 
       COUNT(t.id) FILTER (WHERE t.status = 'done') AS completed
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id AND t.tenant_id = p.tenant_id
GROUP BY p.id, p.name
ORDER BY p.name;

-- 9. Recursive CTE example: task dependency chain (tenant-scoped)
-- Suppose tasks have a parent_task_id for subtask hierarchies
ALTER TABLE tasks ADD COLUMN parent_task_id UUID REFERENCES tasks(id);

WITH RECURSIVE task_tree AS (
    -- Anchor: top-level tasks (no parent)
    SELECT id, title, status, parent_task_id, 0 AS depth,
           ARRAY[title] AS path
    FROM tasks
    WHERE parent_task_id IS NULL

    UNION ALL

    -- Recurse into subtasks
    SELECT t.id, t.title, t.status, t.parent_task_id, tt.depth + 1,
           tt.path || t.title
    FROM tasks t
    JOIN task_tree tt ON tt.id = t.parent_task_id
)
SELECT
    REPEAT('  ', depth) || title AS indented_title,
    status,
    depth,
    array_to_string(path, ' > ') AS full_path
FROM task_tree
ORDER BY path;
```

### Security Verification Checklist
```
✅ RLS enabled and FORCED on all tenant tables
✅ Policies use session variables (not URL params or headers)
✅ SET LOCAL ensures variables are transaction-scoped
✅ Admin bypass requires explicit is_admin flag
✅ Foreign keys cascade deletes within tenant scope
✅ Indexes lead with tenant_id for partition-like performance
✅ No cross-tenant data leakage possible via JOINs (RLS applies to both sides)
```

---

## Common Patterns

### Pattern: Window Function Analytics
```
Build a query with ROW_NUMBER, RANK, or LAG/LEAD for ranking or time-series analysis
```

### Pattern: Recursive Hierarchy
```
Write a recursive CTE to traverse a parent-child hierarchy (org chart, categories, BOM)
```

### Pattern: Cross-Engine UPSERT
```
Translate an INSERT ... ON CONFLICT / ON DUPLICATE KEY / MERGE across database engines
```

### Pattern: JSON Querying
```
Query and filter JSON/JSONB columns with indexing recommendations for the target engine
```

### Pattern: Query Optimization
```
Analyze a slow query with EXPLAIN, recommend index changes, and rewrite for performance
```

### Pattern: Parameterized Dynamic SQL
```
Build safe dynamic SQL with parameterized queries to prevent SQL injection
```

---

**Last Updated**: 2026-02-12
**Maintained by**: The Forge
