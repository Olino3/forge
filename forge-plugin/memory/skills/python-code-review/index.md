# python-code-review Memory

Project-specific memory for Python code review, including architecture, conventions, patterns, and known issues.

## Purpose

This memory helps the `skill:python-code-review` remember:
- Project architecture and technology stack
- Project-specific coding conventions and patterns
- Known technical debt and documented issues
- Past review findings and trends
- Framework-specific implementations

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md` ⭐ CRITICAL

**Purpose**: High-level project understanding - ALWAYS CREATE THIS FIRST

**Must contain**:
- **Project name and purpose**: What does this application do?
- **Framework and version**: Django, Flask, FastAPI, etc.
- **Python version**: Minimum supported version
- **Key dependencies**: Major libraries (SQLAlchemy, Celery, Redis, etc.)
- **Architecture pattern**: Monolith, microservices, layered, etc.
- **Database technology**: PostgreSQL, MySQL, MongoDB, etc.
- **Authentication approach**: JWT, session-based, OAuth, etc.
- **Deployment environment**: AWS, Azure, on-premise, containers, etc.
- **Performance requirements**: Request limits, response times, scale
- **Team conventions**: Style guide, review process, testing standards

**Example structure**:
```markdown
# Project Overview - E-Commerce API

**Last Updated**: 2025-01-15
**Project Type**: RESTful API for e-commerce platform
**Framework**: FastAPI 0.109+
**Python Version**: 3.11+

## Technology Stack

### Core Framework
- **API**: FastAPI with Pydantic v2
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic models for all I/O

### Infrastructure
- **Database**: PostgreSQL 15 with read replicas
- **Cache**: Redis Cluster (session, cart, product cache)
- **Message Queue**: Celery with RabbitMQ
- **Search**: Elasticsearch for product catalog

### Authentication & Security
- **Auth Method**: JWT tokens with refresh mechanism
- **Token Expiry**: Access 15min, Refresh 7 days
- **Session Storage**: Redis
- **Rate Limiting**: Custom Redis-based (100 req/min per endpoint)

### Deployment
- **Platform**: Azure AKS (Kubernetes)
- **Monitoring**: Application Insights + Prometheus
- **Logging**: Structured JSON logs to Azure Log Analytics
- **Scaling**: HPA based on CPU and request rate

## Architecture Patterns

### Async Throughout
- All endpoints are async
- AsyncSession for database
- Async Redis client
- Celery tasks are sync (separate workers)

### Cache-Aside Pattern
- All product reads check Redis first
- 1-hour TTL on product cache
- Explicit invalidation on updates

### Dependency Injection
- Database sessions injected per request
- Auth user injected via custom dependency
- Redis client injected for caching

## Performance Requirements

- **API Response**: p95 < 200ms, p99 < 500ms
- **Database Queries**: Individual queries < 50ms
- **Cache Operations**: < 5ms
- **Request Rate**: 10M+ requests/day
- **Concurrent Users**: 50K+ peak

## Code Conventions

### Module Structure
```
app/
├── api/v1/          # API routes by version
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── services/        # Business logic
├── dependencies/    # FastAPI dependencies
└── utils/           # Shared utilities
```

### Naming Conventions
- **Files**: snake_case
- **Classes**: PascalCase
- **Functions**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Private**: _leading_underscore

### Testing Standards
- **Coverage**: Minimum 80% for business logic
- **Test Structure**: Arrange-Act-Assert pattern
- **Fixtures**: Pytest fixtures for database, Redis
- **Mocking**: Use pytest-mock for external services

## Team & Process

- **Team Size**: 5 backend developers
- **Review Requirements**: Minimum 1 approval, CI must pass
- **Sprint Cycle**: 2-week sprints
- **Deployment**: Blue-green deployments, 2 versions run simultaneously for 15min
```

**When to update**: 
- First invocation: Create with all known details
- Version changes: Update framework/Python versions
- Architecture changes: Update patterns and infrastructure
- New patterns emerge: Add to conventions section

---

#### `common_patterns.md`

**Purpose**: Project-specific code patterns and implementations

**Should contain**:
- **Database access patterns**: How queries are structured
- **Caching patterns**: When and how caching is used
- **Error handling**: Project's approach to exceptions
- **Async patterns**: How async/await is used
- **Testing patterns**: Test structure and utilities
- **Configuration patterns**: How settings are managed
- **Dependency injection**: Common dependency patterns
- **Background tasks**: How long-running operations are handled

**Example structure**:
```markdown
# Common Patterns - E-Commerce API

## Database Access Pattern

ALL database operations follow this pattern:

```python
# ✅ REQUIRED: Async with explicit session
async def get_product(product_id: int, db: AsyncSession) -> Product:
    """All DB functions must be async and accept AsyncSession."""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()
```

**Anti-patterns to flag**:
- Sync SQLAlchemy queries (blocks event loop)
- Missing `await` on DB operations
- No session cleanup in exception handlers

## Caching Pattern

Cache-aside for all product/catalog reads:

```python
# ✅ REQUIRED for product endpoints
async def get_product_cached(product_id: int) -> Product:
    cache_key = f"product:{product_id}"
    
    # Always check cache first
    cached = await redis_client.get(cache_key)
    if cached:
        return Product.parse_raw(cached)
    
    # Fetch from DB and warm cache
    product = await db_get_product(product_id)
    if product:
        await redis_client.setex(cache_key, 3600, product.json())
    return product
```

**Watch for**: Missing cache invalidation on updates

## Error Handling Pattern

Structured error responses:

```python
# ✅ Consistent error structure
class APIError(Exception):
    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message

# Usage
raise APIError(400, "INVALID_QUANTITY", "Quantity must be positive")
```

## Background Task Pattern

All operations >2 seconds offloaded to Celery:

```python
# ✅ REQUIRED for email, exports, bulk operations
@celery_app.task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id: int):
    try:
        order = get_order_sync(order_id)  # Celery uses sync
        send_email(order.customer_email, render_template(order))
    except Exception as exc:
        # Exponential backoff: 1min, 5min, 25min
        raise self.retry(exc=exc, countdown=60 * (5 ** self.request.retries))
```

## Rate Limiting Pattern

Redis-based sliding window:

```python
# ✅ Applied to all /api/v1/* routes via middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_identifier(request)
    key = f"ratelimit:{client_id}:{request.url.path}"
    
    # 100 requests per minute per endpoint
    if not await check_rate_limit(key, limit=100, window=60):
        raise HTTPException(429, "Rate limit exceeded")
    
    return await call_next(request)
```

**Watch for**: Missing rate limiting on new endpoints
```

**When to update**: After each review when new patterns observed

---

#### `known_issues.md` ⭐ CRITICAL

**Purpose**: Documented technical debt and limitations - PREVENTS FALSE POSITIVES

**Must contain**:
- **Issue name and description**: Clear identification
- **Location**: File path and line numbers
- **Status**: Acknowledged, fix planned, acceptable limitation
- **Impact**: What problems does this cause?
- **Workaround**: Current mitigation if any
- **Timeline**: When will it be fixed (if planned)
- **Review guidance**: How should reviewers handle this?

**Example structure**:
```markdown
# Known Issues - E-Commerce API

## Inventory Race Condition (Documented Limitation)

**Location**: `app/services/inventory.py:87-102`
**Status**: Acknowledged, fix planned for Q2 2025
**Reported**: 2024-12-10

### Current Behavior
Two concurrent purchases can oversell inventory by 1-2 units during flash sales.

### Impact
- Occurs in <0.1% of transactions
- Only during high-concurrency periods (flash sales, new releases)
- Maximum oversell: 2 units per SKU

### Workaround
- Manual inventory reconciliation job runs every 5 minutes
- Alerting on negative inventory levels
- Customer service handles oversold cases

### Planned Fix
Implement PostgreSQL advisory locks or Redis distributed locks in Q2 2025 refactor.

### Review Guidance
**DO NOT flag this as a new issue.**
If changes touch inventory logic, verify they don't worsen the race condition.
If you see proper locking added, this issue can be marked resolved.

---

## N+1 Query in Order History (Low Priority)

**Location**: `app/api/v1/orders.py:get_order_history()`
**Status**: Low priority (affects <1% of users)
**Reported**: 2025-01-05

### Current Behavior
Fetches order items in a loop instead of eager loading with `selectinload()`.

### Impact
- Only affects users with 100+ orders (<1% of user base)
- Adds ~50ms per 10 orders to response time
- Not noticeable for typical users (5-20 orders)

### Workaround
- Endpoint limited to 20 most recent orders by default
- Pagination prevents excessive queries

### Review Guidance
If changes touch order queries, suggest using:
```python
query = select(Order).options(selectinload(Order.items))
```

---

## Hardcoded 15-Min Token Expiry (Intentional)

**Location**: `app/dependencies/auth.py:23`
**Status**: Acceptable design decision

### Current Behavior
JWT access tokens expire after exactly 15 minutes (hardcoded).

### Rationale
- Security requirement: short-lived tokens
- Refresh tokens provide long sessions
- 15 minutes is product requirement, not technical debt

### Review Guidance
**DO NOT suggest making this configurable.**
This is an intentional security decision documented in security policy.

---

## Missing CSRF Protection on Public API (Intentional)

**Location**: All API endpoints
**Status**: Acceptable for API-only service

### Rationale
- This is a pure API service (no browser-based UI)
- All access via API keys or JWT tokens
- No cookie-based authentication
- CSRF not applicable to bearer token auth

### Review Guidance
**DO NOT flag missing CSRF protection as a security issue.**
If session-based auth is added in future, then CSRF must be implemented.
```

**When to update**: 
- New known issues discovered
- Issues resolved (mark as resolved, keep record)
- Workarounds change
- Timeline updates

---

#### `review_history.md`

**Purpose**: Track reviews over time, identify trends

**Should contain**:
- **Date and reviewer**: When and who
- **Scope**: What was reviewed (files, feature, diff range)
- **Key findings**: Summary of issues found
- **Critical issues**: High-priority problems
- **Trends**: Patterns over time
- **Improvements**: Progress since last review

**Example structure**:
```markdown
# Review History - E-Commerce API

## Review: 2025-01-15
**Reviewer**: Claude AI Assistant
**Scope**: Payment processing module refactor (PR #456)
**Files**: 8 files, 450 lines changed

### Key Findings
- ✅ Excellent test coverage (95% on new code)
- ✅ Proper async patterns throughout
- ⚠️ One potential race condition in refund flow (flagged)
- ⚠️ Missing input validation on refund amount
- ℹ️ Could benefit from extracting payment gateway logic

### Critical Issues
None. All security-critical code properly validated.

### Resolved from Previous Review
- Fixed N+1 query in order endpoints (from 2025-01-05 review)
- Added rate limiting to new admin endpoints

---

## Review: 2025-01-10
**Reviewer**: Claude AI Assistant
**Scope**: Full security audit (all endpoints)
**Files**: 50+ files reviewed

### Key Findings
- ✅ No SQL injection vulnerabilities
- ✅ All user input properly validated
- ✅ Secrets properly managed (env vars, Azure Key Vault)
- ⚠️ Three endpoints missing rate limiting (flagged)
- ⚠️ PII logging in debug mode (flagged as CRITICAL)

### Critical Issues
1. **PII Logging**: Debug logs contained email addresses
   - **Fixed**: 2025-01-11 in PR #445

### Improvements
- Added rate limiting to 3 endpoints
- Implemented PII scrubbing in logs
- Updated error messages to prevent info disclosure

---

## Review: 2025-01-05
**Reviewer**: Claude AI Assistant
**Scope**: Order management feature (PR #432)
**Files**: 12 files, 600 lines

### Key Findings
- ✅ Feature complete with good test coverage
- ⚠️ N+1 query in get_order_history (flagged as known issue)
- ⚠️ Missing cache invalidation on order update
- ℹ️ Consider extracting order notification logic to service

### Trends Over Time
Third consecutive review with N+1 query issues. Recommend team training on SQLAlchemy eager loading patterns.

---

## Trends Analysis

### Common Issues (Last 5 Reviews)
1. **N+1 Queries** (3 occurrences) - Ongoing pattern
2. **Missing Cache Invalidation** (2 occurrences)
3. **Rate Limiting Gaps** (2 occurrences)

### Improvements
- Security posture: Excellent (no vulnerabilities in 3 months)
- Test coverage: Trending up (65% → 80% over 2 months)
- Async patterns: Now consistent across codebase

### Recommendations
- Team training: SQLAlchemy query optimization
- Checklist: Add cache invalidation to PR template
- Automation: Add rate limit detection to CI
```

**When to update**: After every review, append new entry

---

## Optional Files

#### `security_requirements.md`

**Purpose**: Project-specific security rules beyond general guidelines

**Should contain**:
- PII handling requirements
- Compliance requirements (GDPR, PCI-DSS, etc.)
- Data retention policies
- Encryption requirements
- Audit logging requirements

#### `performance_budgets.md`

**Purpose**: Specific performance targets for this project

**Should contain**:
- API response time targets
- Database query time limits
- Memory usage limits
- Concurrent user targets
- Rate limit definitions

---

## Usage in skill:python-code-review

### Loading Memory (Step 2)

```markdown
project_name = detect_project_name()
memory_path = f"../../memory/skills/python-code-review/{project_name}/"

if exists(memory_path):
    # ALWAYS load these first
    overview = read_file(f"{memory_path}/project_overview.md")
    patterns = read_file(f"{memory_path}/common_patterns.md")
    known_issues = read_file(f"{memory_path}/known_issues.md")
    history = read_file(f"{memory_path}/review_history.md")
    
    # Use throughout review
    - Apply project conventions from overview
    - Recognize patterns from common_patterns
    - Skip flagging known_issues
    - Check history for recurring problems
```

### Updating Memory (Step 5)

```markdown
# After generating review output

# First time reviewing project
if not exists(memory_path):
    create_directory(memory_path)
    write_file(f"{memory_path}/project_overview.md", create_overview())
    write_file(f"{memory_path}/common_patterns.md", observed_patterns())
    write_file(f"{memory_path}/known_issues.md", "# Known Issues\n\n(None documented yet)")
    write_file(f"{memory_path}/review_history.md", first_review_summary())

# Subsequent reviews
else:
    # Update patterns if new ones discovered
    if new_patterns_found:
        append_to_file(f"{memory_path}/common_patterns.md", new_patterns)
    
    # Update known issues if resolved or new ones documented
    if issues_resolved or new_documented_issues:
        update_file(f"{memory_path}/known_issues.md", updated_issues)
    
    # Always append to review history
    append_to_file(f"{memory_path}/review_history.md", current_review_summary)
```

---

## Memory Benefits for Code Review

### Prevents False Positives

**Without memory**:
> "⚠️ Race condition detected in inventory.py line 87"

**With memory**:
> "(Skipped: Known issue documented in `known_issues.md`, fix planned Q2 2025)"

### Recognizes Project Patterns

**Without memory**:
> "⚠️ Consider using async for database queries"

**With memory**:
> "✅ Database access follows project's required async pattern with AsyncSession"

### Provides Context

**Without memory**:
> "⚠️ Missing CSRF protection"

**With memory**:
> "(Skipped: API-only service, no browser-based auth, documented in project overview)"

### Tracks Progress

**Without memory**:
> Reports same issue in every review

**With memory**:
> "✅ N+1 query issue from previous review has been resolved. Test coverage improved from 65% to 80%."

---

## Memory Creation Checklist

### First Review of New Project

- [ ] Detect project name from git repo or directory
- [ ] Create project memory directory
- [ ] Analyze code to understand:
  - [ ] Framework and version
  - [ ] Architecture patterns
  - [ ] Database technology
  - [ ] Authentication approach
  - [ ] Coding conventions
- [ ] Create `project_overview.md` with findings
- [ ] Create `common_patterns.md` with observed patterns
- [ ] Create `known_issues.md` (empty initially)
- [ ] Create `review_history.md` with first review entry

### Subsequent Reviews

- [ ] Load all existing memory files
- [ ] Apply memory to enhance review accuracy
- [ ] Note new patterns discovered
- [ ] Note issues that were resolved
- [ ] Update `common_patterns.md` if needed
- [ ] Update `known_issues.md` if needed
- [ ] Append to `review_history.md`

---

## Related Documentation

- **Main Memory Index**: `../index.md` for memory system overview
- **Skill Documentation**: `../../skills/python-code-review/SKILL.md` for review workflow
- **Context Files**: `../../context/python/` and `../../context/security/` for general knowledge
- **Example Memory**: `example-project/reference.md` for a complete memory file example
