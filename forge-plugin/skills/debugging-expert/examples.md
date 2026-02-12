# Debugging Expert Examples

This file contains example debugging scenarios demonstrating the systematic 5-step debugging workflow.

## Example 1: Memory Leak in Node.js Application

### User Prompt

> "Our Node.js API server's memory usage keeps growing in production. It starts at ~200MB and reaches 1.5GB within 24 hours, at which point the container gets OOM-killed. No errors in the logs."

### Skill Execution

**Step 1 — Identify the Problem**:
- Symptoms: Gradual memory growth (~55MB/hour), eventual OOM after ~24 hours
- Reproduction: Observed in production under normal traffic; not reproduced in dev
- Affected components: API server (Express.js), runs in Docker container with 2GB limit
- Language/framework: Node.js 18, Express, PostgreSQL via `pg` pool

**Step 2 — Load Memory & Context**:
- `memoryStore.getSkillMemory("debugging-expert", "payment-api")` → no prior memory
- `contextProvider.getDomainIndex("javascript")` → loaded Node.js debugging context
- Cross-skill: `memoryStore.getByProject("payment-api")` → found code review noting unclosed event listeners

**Step 3 — Systematic Investigation**:
- Hypothesis 1: Database connection pool leak → checked `pg` pool stats, connections stable at 10 → eliminated
- Hypothesis 2: Unclosed event listeners accumulating → took heap snapshots at T=0h, T=4h, T=8h
- Heap snapshot comparison revealed growing `EventEmitter` listener arrays attached to request objects
- Bisected to recent commit adding request-scoped logging middleware
- The middleware attaches `res.on('finish', callback)` but also stores a reference to the request in a module-level `Map` for correlation, never cleaning it up

**Step 4 — Root Cause Analysis & Fix**:
- Root cause: Request correlation `Map` in logging middleware retains references to completed request/response objects indefinitely
- The `Map` grows by one entry per request and entries are never removed

**Step 5 — Document & Update Memory**:
- Debugging report output to `claudedocs/`
- Memory updated with known fragile area: logging middleware lifecycle

### Debugging Report Output

**Problem Summary**: Production memory leak in Express API server causing OOM after ~24 hours.

**Root Cause**: Logging middleware (`src/middleware/requestLogger.js:15`) stores request references in a module-level `Map` for log correlation but never removes entries after the response completes.

**Before (Leaking Code)**:

```javascript
// src/middleware/requestLogger.js:12
const activeRequests = new Map();

function requestLogger(req, res, next) {
  const requestId = crypto.randomUUID();
  activeRequests.set(requestId, { req, res, startTime: Date.now() });

  res.on('finish', () => {
    const duration = Date.now() - activeRequests.get(requestId).startTime;
    logger.info({ requestId, duration, status: res.statusCode });
    // BUG: never calls activeRequests.delete(requestId)
  });

  next();
}
```

**After (Fixed Code)**:

```javascript
// src/middleware/requestLogger.js:12
const activeRequests = new Map();

function requestLogger(req, res, next) {
  const requestId = crypto.randomUUID();
  const startTime = Date.now();
  activeRequests.set(requestId, { startTime });

  res.on('finish', () => {
    const duration = Date.now() - startTime;
    logger.info({ requestId, duration, status: res.statusCode });
    activeRequests.delete(requestId);
  });

  next();
}
```

**Prevention**: Add a monitoring alert for heap size growth > 100MB/hour. Add a unit test asserting `activeRequests.size === 0` after response completes.

---

## Example 2: Race Condition in Python Async Code

### User Prompt

> "Our Python asyncio service intermittently returns stale data. About 5% of requests return the previous user's data instead of the current user's. It only happens under load."

### Skill Execution

**Step 1 — Identify the Problem**:
- Symptoms: 5% of responses contain incorrect (stale) user data; only under concurrent load
- Reproduction: Requires 50+ concurrent requests; not reproducible with sequential testing
- Affected components: User profile service, async Python (FastAPI + httpx)
- Language/framework: Python 3.11, FastAPI, asyncio, httpx for downstream calls

**Step 2 — Load Memory & Context**:
- `memoryStore.getSkillMemory("debugging-expert", "profile-service")` → no prior memory
- `contextProvider.getDomainIndex("python")` → loaded async patterns, common issues
- `contextProvider.getConditionalContext("python", detection)` → loaded FastAPI patterns

**Step 3 — Systematic Investigation**:
- Hypothesis 1: Database returning wrong rows → added query logging, queries are correct → eliminated
- Hypothesis 2: Response caching returning wrong cached entry → no caching layer configured → eliminated
- Hypothesis 3: Shared mutable state across async tasks → inspected service layer code
- Found: `UserService` class uses a module-level instance with an instance variable `self.current_user` set during request processing
- Under concurrency, Task A sets `self.current_user`, then Task B sets `self.current_user`, then Task A reads `self.current_user` — getting Task B's data
- Confirmed by adding task ID logging: interleaved task execution correlates with incorrect responses

**Step 4 — Root Cause Analysis & Fix**:
- Root cause: Shared mutable instance state (`self.current_user`) on a singleton service object is not safe for concurrent async access
- Fix: Remove shared state; pass user context as function parameters instead of storing on instance

**Step 5 — Document & Update Memory**:
- Debugging report output to `claudedocs/`
- Memory updated with pattern: "singleton service objects must not store per-request state"

### Debugging Report Output

**Problem Summary**: Intermittent data leakage between concurrent requests in FastAPI async service.

**Root Cause**: `UserService` singleton stores per-request state in `self.current_user`, causing data races between concurrent async tasks sharing the same event loop.

**Before (Racy Code)**:

```python
# src/services/user_service.py:8
class UserService:
    def __init__(self, db: Database):
        self.db = db
        self.current_user = None  # Shared across all concurrent requests!

    async def get_profile(self, user_id: int):
        self.current_user = await self.db.fetch_user(user_id)
        enriched = await self._enrich_profile()  # May yield to event loop here
        return enriched

    async def _enrich_profile(self):
        # By this point, self.current_user may have been overwritten
        # by another concurrent request
        prefs = await self.db.fetch_preferences(self.current_user.id)
        return {**self.current_user.dict(), "preferences": prefs}

# Singleton instance — shared across all requests
user_service = UserService(db)
```

**After (Fixed Code)**:

```python
# src/services/user_service.py:8
class UserService:
    def __init__(self, db: Database):
        self.db = db

    async def get_profile(self, user_id: int):
        user = await self.db.fetch_user(user_id)
        enriched = await self._enrich_profile(user)
        return enriched

    async def _enrich_profile(self, user):
        prefs = await self.db.fetch_preferences(user.id)
        return {**user.dict(), "preferences": prefs}

user_service = UserService(db)
```

**Prevention**: Add a linting rule or code review checklist item to flag instance variables set inside async request handlers on singleton objects. Add a concurrent load test asserting response data matches the requesting user.

---

## Example 3: Performance Regression in Database Queries

### User Prompt

> "After a schema migration last week, our order listing endpoint went from 50ms to 3 seconds. We added an index on the new column but it didn't help."

### Skill Execution

**Step 1 — Identify the Problem**:
- Symptoms: 60x latency increase (50ms → 3000ms) on `/api/orders` endpoint
- Reproduction: Consistent on all environments after migration `20240115_add_order_status`
- Affected components: Orders API, PostgreSQL database, Django ORM
- Timeline: Started immediately after deploying migration; adding index on `order_status` did not improve

**Step 2 — Load Memory & Context**:
- `memoryStore.getSkillMemory("debugging-expert", "ecommerce-api")` → previous session noted orders table has 2M rows
- `contextProvider.getDomainIndex("python")` → loaded Django patterns
- Cross-skill: `memoryStore.getByProject("ecommerce-api")` → schema analysis skill noted the migration added a nullable `TEXT` column

**Step 3 — Systematic Investigation**:
- Hypothesis 1: Missing index on new column → index exists, confirmed via `\di` → but is it being used?
- Ran `EXPLAIN ANALYZE` on the ORM-generated query → sequential scan on `orders` table, index not used
- Hypothesis 2: Query plan changed due to schema change → compared `EXPLAIN` before/after
- Found: The ORM query includes `ORDER BY order_status` on the new nullable `TEXT` column — PostgreSQL cannot use a standard B-tree index for sorting nullable columns with default `NULLS LAST` behavior when the query has `NULLS FIRST`
- Additionally: The migration set `default=''` but existing 2M rows have `NULL`, causing mixed null/non-null sort behavior
- Hypothesis 3: Table bloat after migration → checked `pg_stat_user_tables`, `dead_tup` count is normal → eliminated

**Step 4 — Root Cause Analysis & Fix**:
- Root cause: Two compounding issues — (1) ORM `order_by('order_status')` on a nullable column forces `NULLS LAST` sort, incompatible with the default B-tree index, and (2) 2M existing rows have `NULL` values while new rows have `''`, causing inconsistent sort behavior
- Fix: Backfill `NULL` values, add `NOT NULL` constraint, and create a proper index

**Step 5 — Document & Update Memory**:
- Debugging report output to `claudedocs/`
- Memory updated with pattern: "always backfill data before adding NOT NULL constraint; verify index usage with EXPLAIN ANALYZE after migrations"

### Debugging Report Output

**Problem Summary**: 60x performance regression on order listing endpoint after schema migration.

**Root Cause**: Migration added nullable `order_status TEXT` column. The 2M existing rows have `NULL` values. The ORM sorts by this column, but PostgreSQL's query planner cannot use the B-tree index for sorting when `NULL` handling is inconsistent, falling back to a sequential scan.

**Before (Slow Migration)**:

```python
# migrations/20240115_add_order_status.py
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.TextField(default='', null=True, blank=True),
            # BUG: null=True leaves 2M existing rows as NULL
            # Index won't help with mixed NULL/non-NULL sorting
        ),
    ]
```

**After (Fixed Migration + Data Backfill)**:

```python
# migrations/20240120_fix_order_status.py
from django.db import migrations

def backfill_order_status(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.filter(order_status__isnull=True).update(order_status='pending')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(backfill_order_status, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.TextField(default='pending', null=False, blank=False),
        ),
    ]
```

```sql
-- Verify index is now used
EXPLAIN ANALYZE SELECT * FROM orders ORDER BY order_status LIMIT 50;
-- Expected: Index Scan using idx_orders_order_status
```

**Prevention**: Add a pre-migration checklist requiring `EXPLAIN ANALYZE` verification on queries touching modified columns. Ensure nullable columns intended for sorting have explicit `NULLS FIRST/LAST` index definitions.

---

## Summary of Debugging Patterns

1. **Memory Leaks**: Take heap snapshots at intervals, compare object retention, look for growing collections that never shrink
2. **Race Conditions**: Add concurrency to reproduction, log task/thread IDs, look for shared mutable state across concurrent execution contexts
3. **Performance Regressions**: Use `EXPLAIN ANALYZE` for database queries, profile before/after, correlate with recent changes using `git bisect`
4. **Intermittent Failures**: Increase logging, correlate with timing/load patterns, look for non-deterministic behavior (concurrency, caching, DNS, network)
5. **Environment Differences**: Compare configurations, dependency versions, OS/runtime versions, and infrastructure between environments

Use these examples as reference when conducting debugging sessions. Adapt the investigation depth and tools to the specific language, platform, and issue type.
