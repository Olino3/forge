# Power Debug Examples

This file contains example scenarios demonstrating how to use the power-debug skill for multi-agent investigation of stubborn bugs.

---

## Example 1: Intermittent API Timeout

### Scenario
An API endpoint returns 504 Gateway Timeout errors approximately 5% of the time, but the same request succeeds when retried immediately.

### User Prompt
```
I'm going in circles debugging this — our /api/orders endpoint times out randomly, about 5% of requests. Retrying always works. Help me investigate.
```

### Skill Execution

**Step 1 - Symptom Documentation**:
- **Expected**: All requests to `/api/orders` return within 2 seconds
- **Actual**: ~5% of requests timeout at 30 seconds, retry succeeds immediately
- **Error**: `504 Gateway Timeout` from nginx reverse proxy
- **Type**: Intermittent — race condition or resource contention suspected
- **Scope**: Cross-system (API → Database → Cache)
- **Reproduction**: Cannot reproduce deterministically; happens under moderate load

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("power-debug", "ecommerce-api")` → No previous debug sessions
- First investigation for this project

**Step 3 - Load Context**:
- `contextProvider.detectProjectType()` → FastAPI + PostgreSQL + Redis
- Loaded engineering context for async Python patterns

**Step 4 - Hypothesis Generation**:

| # | Hypothesis | Probability | Confirming Evidence | Refuting Evidence |
|---|-----------|-------------|--------------------|--------------------|
| 1 | Database connection pool exhaustion | High | Pool metrics show max connections hit during timeouts | Pool has available connections during timeout events |
| 2 | Redis cache miss causing slow DB query | Medium | Cache miss logs correlate with timeout events | Timeouts occur with cache hits too |
| 3 | GC pause in Python runtime | Low | GC logs show full collection during timeout windows | No GC activity during timeouts |

**Step 5 - Systematic Investigation**:
1. **Tested H1 (DB pool)**: Added connection pool monitoring
   - Result: **CONFIRMED** — Pool exhausted when timeouts occur
   - Found: Pool size = 5, concurrent requests during peak = 12
   - Long-running query in `/api/reports` holds connections for 10+ seconds
2. **Cross-layer trace**:
   ```
   Request → nginx (30s timeout) → [✓]
       → FastAPI handler → [✓]
           → await db.execute() → [✗ BLOCKED waiting for pool]
               → Connection pool → [✗ ALL 5 CONNECTIONS BUSY]
                   → Long query from /api/reports → [ROOT CAUSE]
   ```

**Step 6 - Root Cause**:
- **Cause**: `/api/reports` endpoint runs unoptimized aggregation query (10-15s)
- **Impact**: Holds database connections, exhausting the 5-connection pool
- **Fix options**:
  - **Quick**: Increase pool size to 20
  - **Proper**: Optimize reports query with materialized view + increase pool to 15
  - **Preventive**: Add query timeout (5s), connection pool monitoring alerts, per-endpoint pool isolation

**Step 7 - Output**:
- Saved to `/claudedocs/power-debug_ecommerce-api_2026-02-12_order-timeout.md`

**Step 8 - Update Memory**:
- Stored: "Connection pool exhaustion" as a known debug pattern
- Documented: Reports endpoint as a fragile area

---

## Example 2: Authentication Token Silently Fails

### Scenario
Users report being logged out randomly. The JWT token appears valid but the API returns 401 Unauthorized on some requests.

### User Prompt
```
Users get randomly logged out. JWT tokens look valid but we're getting 401s. Symptoms don't match expectations — the token hasn't expired.
```

### Skill Execution

**Step 1 - Symptom Documentation**:
- **Expected**: JWT tokens valid for 1 hour should authenticate all requests
- **Actual**: Some requests return 401 despite token being within validity period
- **Error**: `401 Unauthorized — Invalid token`
- **Type**: Logic error — token validation inconsistency
- **Scope**: Cross-module (auth middleware, token service, user service)
- **Reproduction**: Intermittent, more common after 30 minutes

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("power-debug", "saas-platform")` → No history
- Cross-skill: `memoryStore.getByProject("saas-platform")` → Found auth patterns from code review

**Step 3 - Load Context**:
- Loaded `security` domain context for JWT/auth patterns
- Identified auth middleware and token validation flow

**Step 4 - Hypothesis Generation**:

| # | Hypothesis | Probability | Confirming Evidence | Refuting Evidence |
|---|-----------|-------------|--------------------|--------------------|
| 1 | Clock skew between servers | High | Different servers reject same token; NTP sync issues | All servers have synchronized clocks |
| 2 | JWT secret rotation mid-session | Medium | Secret rotated between token issue and validation | Secret hasn't changed |
| 3 | Token blacklist race condition | Medium | Token appears in blacklist during failed requests | Token not in blacklist |

**Step 5 - Systematic Investigation**:
1. **Tested H1 (Clock skew)**: Compared server times → All synced within 1s. **REFUTED**
2. **Tested H2 (Secret rotation)**: Checked JWT_SECRET across pods
   - Result: **CONFIRMED** — Two deployments running simultaneously
   - Pod A uses secret v2 (deployed 2 hours ago)
   - Pod B uses secret v1 (old deployment, not terminated)
   - Tokens issued by Pod A fail validation on Pod B and vice versa
3. **Temporal analysis**:
   ```bash
   git log --since="3 days ago" -- k8s/deployment.yaml
   # Found: Deployment strategy changed from RollingUpdate to Recreate
   # But the old pods weren't terminated due to preStop hook timeout
   ```

**Step 6 - Root Cause**:
- **Cause**: Blue-green deployment left old pods running with different JWT secret
- **Evidence**: Two pods with different `JWT_SECRET` environment variables
- **Fix options**:
  - **Quick**: Terminate old pods manually, verify single secret
  - **Proper**: Use JWKS (JSON Web Key Sets) with key rotation support
  - **Preventive**: Add deployment validation hook that verifies all pods share the same secret version

**Step 7 - Output**:
- Saved to `/claudedocs/power-debug_saas-platform_2026-02-12_auth-401.md`

**Step 8 - Update Memory**:
- Stored: Deployment-related auth failures as a known pattern
- Documented: JWT secret management as a fragile area

---

## Example 3: Data Corruption in Background Job

### Scenario
A nightly batch job that syncs customer records occasionally produces corrupted data — some fields contain data from different customers.

### User Prompt
```
Our nightly sync job is mixing up customer data. Some records have the wrong email or phone number from a different customer. This is critical.
```

### Skill Execution

**Step 1 - Symptom Documentation**:
- **Expected**: Each customer record synced independently with correct data
- **Actual**: ~0.1% of records have fields from other customers (cross-contamination)
- **Error**: No error — data silently corrupted
- **Type**: Logic error — shared state corruption
- **Scope**: Background job processing module
- **Reproduction**: Happens only during nightly batch (not in single-record sync)

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("power-debug", "crm-sync")` → No history

**Step 3 - Load Context**:
- `contextProvider.detectProjectType()` → Python + Celery + PostgreSQL
- Loaded engineering context for concurrent processing patterns

**Step 4 - Hypothesis Generation**:

| # | Hypothesis | Probability | Confirming Evidence | Refuting Evidence |
|---|-----------|-------------|--------------------|--------------------|
| 1 | Shared mutable state across Celery workers | High | Workers reuse object with stale state | Each worker creates new objects |
| 2 | Database transaction isolation issue | Medium | Dirty reads during concurrent updates | Serializable isolation prevents cross-reads |
| 3 | Bug in batch chunking logic | Low | Adjacent records in same chunk get mixed | Corruption spans chunk boundaries |

**Step 5 - Systematic Investigation**:
1. **Tested H1 (Shared state)**: Reviewed Celery task code
   - Found: `CustomerMapper` class instantiated at **module level** (shared across tasks)
   - `self.current_customer` persists between task invocations
   - Result: **CONFIRMED** — Module-level singleton retains state between tasks
2. **Binary search isolation**:
   ```
   Batch start → [✓ data correct]
       → Chunk 1 processed → [✓ data correct]
           → Worker reused for Chunk 2 → [✗ STALE STATE from Chunk 1]
   ```

**Step 6 - Root Cause**:
- **Cause**: `CustomerMapper` instantiated at module level, `self.current_customer` not reset between task invocations
- **Evidence**: Adding `mapper = CustomerMapper()` inside the task function eliminates corruption
- **Fix options**:
  - **Quick**: Instantiate `CustomerMapper` inside each task function
  - **Proper**: Make `CustomerMapper` stateless — pass customer as parameter, don't store on `self`
  - **Preventive**: Add Celery `task_prerun` signal to clear shared state; add data validation post-sync

**Step 7 - Output**:
- Saved to `/claudedocs/power-debug_crm-sync_2026-02-12_data-corruption.md`

**Step 8 - Update Memory**:
- Stored: "Module-level mutable state in Celery" as critical anti-pattern
- Documented: Sync job as fragile area needing stateless refactor

---

## Summary of Debug Strategies

| Strategy | Best For | Example |
|----------|----------|---------|
| Hypothesis Testing | Unknown root cause | Generate and rank competing explanations |
| Binary Search | Narrowing code path | Isolate failure to specific line/function |
| Cross-Layer Tracing | Multi-system bugs | Follow request across API, DB, cache |
| Temporal Bisection | Regression bugs | Use git bisect to find breaking commit |
| Environmental Comparison | Environment-specific bugs | Diff configs across environments |

## Best Practices

- Always generate at least 3 hypotheses before investigating
- Test the most probable hypothesis first
- Record evidence for each hypothesis (confirmed or refuted)
- Don't accept the first plausible explanation — verify it explains ALL symptoms
- Distinguish between root cause and contributing factors
- Always propose preventive measures, not just fixes
- Update memory with resolved patterns to speed up future debugging
