# Example Project Reference Memory

## Project: E-Commerce Platform API

**Last Updated**: 2025-01-15  
**Reviewer**: Claude (AI Assistant)  
**Framework**: FastAPI + SQLAlchemy + Redis + Celery  
**Python Version**: 3.11+

---

## Project Context

This is a high-traffic e-commerce API serving 10M+ requests/day with the following characteristics:

- **Architecture**: Microservices with async FastAPI endpoints
- **Database**: PostgreSQL 15 with read replicas
- **Cache**: Redis Cluster for session/cart data
- **Queue**: Celery with RabbitMQ for background jobs
- **Auth**: JWT tokens with refresh mechanism
- **Deployment**: Kubernetes on Azure AKS
- **Monitoring**: Application Insights + Prometheus

---

## Project-Specific Patterns & Conventions

### 1. Database Access Patterns

**Convention**: All database queries use async SQLAlchemy with explicit session management:

```python
# ✅ REQUIRED pattern
async def get_product(product_id: int, db: AsyncSession) -> Product:
    """All DB functions must be async and accept AsyncSession."""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()
```

**Anti-pattern to flag**:
- Sync SQLAlchemy queries (blocks event loop)
- Missing `await` on database operations
- No session cleanup in exception handlers

### 2. Cache-Aside Pattern

**Convention**: All product/catalog reads MUST check Redis first:

```python
# ✅ REQUIRED for product endpoints
async def get_product_cached(product_id: int) -> Product:
    cache_key = f"product:{product_id}"
    
    # Always check cache first
    cached = await redis_client.get(cache_key)
    if cached:
        return Product.parse_raw(cached)
    
    # Fetch from DB with cache warming
    product = await db_get_product(product_id)
    if product:
        await redis_client.setex(
            cache_key, 
            3600,  # 1 hour TTL
            product.json()
        )
    return product
```

**Watch for**: Missing cache invalidation on updates, cache stampede on popular items.

### 3. Rate Limiting (Custom Implementation)

**Convention**: All public endpoints use Redis-based sliding window rate limiter:

```python
# ✅ Applied to all /api/v1/* routes
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_identifier(request)
    key = f"ratelimit:{client_id}:{request.url.path}"
    
    # 100 requests per minute per endpoint per client
    if not await check_rate_limit(key, limit=100, window=60):
        raise HTTPException(429, "Rate limit exceeded")
    
    return await call_next(request)
```

**Watch for**: Missing rate limiting on new endpoints, incorrect client identification.

### 4. Background Job Patterns

**Convention**: All long-running operations (>2s) MUST be offloaded to Celery:

```python
# ✅ REQUIRED for email, exports, bulk operations
@celery_app.task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id: int):
    try:
        order = get_order_sync(order_id)  # Celery tasks use sync
        send_email(order.customer_email, render_template(order))
    except Exception as exc:
        # Exponential backoff: 1min, 5min, 25min
        raise self.retry(exc=exc, countdown=60 * (5 ** self.request.retries))
```

**Watch for**: Long-running sync operations in async endpoints, missing retry logic.

### 5. Cart Management (Stateful)

**Convention**: Shopping carts are Redis-only with expiration:

```python
# ✅ Cart operations never touch DB until checkout
async def add_to_cart(user_id: int, product_id: int, quantity: int):
    cart_key = f"cart:{user_id}"
    cart = await redis_client.hgetall(cart_key)
    
    cart[str(product_id)] = quantity
    
    # 7 day expiration
    await redis_client.hmset(cart_key, cart)
    await redis_client.expire(cart_key, 604800)
```

**Watch for**: Cart data leaking into DB prematurely, missing expiration, cart abandonment tracking.

---

## Known Issues & Technical Debt

### 1. Inventory Race Condition (Acknowledged)

**Location**: `app/services/inventory.py:87-102`  
**Status**: Documented limitation, fixing in Q2 2025

**Current behavior**: Two concurrent purchases can oversell inventory by 1-2 units during flash sales.

**Workaround**: Manual inventory reconciliation job runs every 5 minutes.

**Planned fix**: Implement PostgreSQL advisory locks or Redis distributed locks.

**Review guidance**: Do NOT flag this as a new issue. If changes touch inventory logic, verify they don't worsen the race condition.

### 2. N+1 Query in Order History (Performance)

**Location**: `app/api/v1/orders.py:get_order_history()`  
**Status**: Low priority (affects <1% of users with 100+ orders)

**Current behavior**: Fetches order items in a loop instead of eager loading.

**Workaround**: Only 20 most recent orders shown by default.

**Review guidance**: If changes touch order queries, suggest `selectinload(Order.items)` pattern.

---

## Security Requirements

### 1. PII Handling

**CRITICAL**: All endpoints returning user data MUST redact:
- Full credit card numbers (show last 4 digits only)
- Email addresses in public-facing responses (hash or truncate)
- Phone numbers (show last 4 digits only)

**Example**:
```python
# ✅ REQUIRED for user responses
class UserPublicResponse(BaseModel):
    id: int
    email_hash: str  # SHA256, not plaintext email
    phone_last4: str
    
    @validator('email_hash', pre=True)
    def hash_email(cls, v):
        return hashlib.sha256(v.encode()).hexdigest()[:16]
```

### 2. SQL Injection Protection

**CRITICAL**: All raw SQL MUST use parameterized queries (no f-strings):

```python
# ❌ NEVER ALLOW
query = f"SELECT * FROM products WHERE name = '{user_input}'"

# ✅ REQUIRED
query = "SELECT * FROM products WHERE name = :name"
result = await db.execute(text(query), {"name": user_input})
```

**Review guidance**: Flag ANY raw SQL with string interpolation as CRITICAL security issue.

---

## Performance Budgets

Flag violations of these budgets as **Important** issues:

- **API Response Time**: p95 < 200ms, p99 < 500ms
- **Database Query Time**: Individual queries < 50ms
- **Redis Operations**: < 5ms
- **Background Job Processing**: < 30s per task
- **Memory per Request**: < 50MB

**Example violation**:
```python
# ❌ Would violate query budget (full table scan)
products = await db.execute(select(Product))  # No WHERE clause

# ✅ Compliant (indexed lookup)
products = await db.execute(
    select(Product).where(Product.category_id == cat_id)
)
```

---

## Testing Standards

All new endpoint code MUST include:

1. **Unit tests**: Business logic in isolation
2. **Integration tests**: Database + Redis interactions
3. **E2E tests**: Full request/response cycle
4. **Load tests**: If endpoint is public-facing

**Flag as Important** if PR lacks tests for:
- New endpoints
- Authentication/authorization logic
- Payment processing
- Inventory updates

---

## Deployment Considerations

**Blue-Green Deployments**: Code must support running two versions simultaneously for 15 minutes during rollout.

**Watch for**:
- Database schema changes requiring migrations
- Breaking API changes (must maintain backward compatibility for 1 version)
- Cache key format changes (invalidate old keys explicitly)
- Feature flags for gradual rollout

---

## Review Priorities for This Project

When reviewing changes, prioritize in this order:

1. **CRITICAL**: Security (SQL injection, auth bypass, PII exposure)
2. **CRITICAL**: Data integrity (inventory, payments, orders)
3. **Important**: Performance (response time budgets, N+1 queries)
4. **Important**: Reliability (error handling, retry logic, idempotency)
5. **Minor**: Code quality (DRY, naming, documentation)

---

## Common False Positives to Avoid

**DO NOT flag these as issues**:

1. **Sync SQLAlchemy in Celery tasks**: This is intentional (Celery runs in separate workers)
2. **Global redis_client**: Shared across app, properly initialized at startup
3. **Missing type hints in tests**: Project allows relaxed typing in test files
4. **Long functions in migration scripts**: Auto-generated by Alembic

---

## Project-Specific Resources

- **Architecture Docs**: `docs/architecture/microservices.md`
- **API Conventions**: `docs/api-guidelines.md`
- **Runbook**: `docs/operations/runbook.md`
- **Security Policy**: `SECURITY.md`

---

## Changelog

- **2025-01-15**: Added inventory race condition to known issues
- **2025-01-10**: Updated performance budgets (tightened p95 to 200ms)
- **2025-01-05**: Initial reference memory created