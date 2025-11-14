
# Project Reference Memory: Example E-Commerce Platform

**Project**: `example-ecommerce-api`  
**Repository**: `https://github.com/example-org/ecommerce-api`  
**Last Updated**: 2025-01-15  
**Primary Language**: Python 3.11+  
**Framework**: FastAPI 0.104+

---

## Project Architecture

### Core Structure
```
src/
├── api/            # FastAPI route handlers
├── models/         # SQLAlchemy ORM models
├── services/       # Business logic layer
├── repositories/   # Data access layer
├── schemas/        # Pydantic validation models
└── utils/          # Shared utilities
```

### Key Technologies
- **Web Framework**: FastAPI with async/await
- **Database**: PostgreSQL 15 with asyncpg driver
- **ORM**: SQLAlchemy 2.0 (async engine)
- **Cache**: Redis 7.x for session and product cache
- **Message Queue**: RabbitMQ for order processing
- **Authentication**: JWT tokens with refresh mechanism
- **Payment**: Stripe API v2023-10-16

---

## Project-Specific Patterns

### Database Session Management
```python
# ALWAYS use dependency injection for db sessions
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

**Rule**: Never create database sessions manually. Always use `Depends(get_db_session)`.

### Error Handling Convention
```python
# Custom exception hierarchy
class EcommerceException(Exception):
    """Base exception - ALWAYS inherit from this"""
    pass

class ProductNotFoundException(EcommerceException):
    """404 errors"""
    pass

class InsufficientInventoryException(EcommerceException):
    """409 errors"""
    pass
```

**Rule**: All business logic exceptions must inherit from `EcommerceException`.

### Async Repository Pattern
```python
# ALL repositories must follow this pattern
class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, product_id: UUID) -> Product | None:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
```

**Rule**: Repositories are instantiated per-request, never as singletons.

---

## Security Requirements

### Authentication
- **JWT Expiry**: Access tokens expire in 15 minutes, refresh tokens in 7 days
- **Password Policy**: Minimum 12 characters, bcrypt cost factor 12
- **Rate Limiting**: 10 login attempts per IP per 15 minutes

### API Keys
- **Stripe Keys**: Stored in Azure Key Vault, rotated quarterly
- **Admin Endpoints**: Require `X-Admin-Token` header + JWT with `admin` role

### Data Protection
- **PII Fields**: `email`, `phone`, `address` must be encrypted at rest using Fernet
- **Payment Data**: NEVER store full credit card numbers, only Stripe tokens
- **Audit Logging**: All write operations to `orders`, `payments` tables logged to separate audit DB

---

## Performance Considerations

### Caching Strategy
```python
# Product catalog cached for 5 minutes
@cache(ttl=300, key_prefix="product")
async def get_product(product_id: UUID) -> Product:
    ...
```

**Rule**: Cache reads heavily, invalidate on writes. Use Redis `SCAN` instead of `KEYS *`.

### Query Optimization
- **Eager Loading**: Always use `selectinload()` for order→order_items relationships
- **Pagination**: Default page size is 20, max is 100
- **Index Strategy**: Composite indexes on `(tenant_id, created_at)` for all multi-tenant tables

### Known N+1 Issues
- **Order History Endpoint** (`GET /orders`): Previously had N+1 on `order.user` lookups → Fixed with `joinedload(Order.user)` in commit `a3f7b92`
- **Product Reviews**: Still has N+1 on review→product lookups → **WATCH FOR THIS**

---

## Testing Requirements

### Critical Test Coverage
- **Order Processing**: Must test race conditions on inventory deduction
- **Payment Flow**: Mock Stripe webhooks, test idempotency keys
- **Cart Operations**: Test concurrent cart updates from same user

### Test Data
- **Fixtures**: Use `tests/fixtures/sample_data.py` for consistent test products
- **Database**: Tests run against PostgreSQL in Docker, not SQLite
- **Cleanup**: All tests must clean up test data in teardown

---

## Deployment Context

### Environment
- **Production**: Azure App Service (P2v3), 3 instances behind Azure Front Door
- **Database**: Azure Database for PostgreSQL Flexible Server (8 vCores)
- **Scaling**: Autoscale triggers at 70% CPU, max 10 instances

### Configuration
- **Environment Variables**: Managed via Azure Key Vault references
- **Secrets Rotation**: Automated via Azure Managed Identity
- **Health Checks**: `/health` endpoint checked every 30s by AFD

### Monitoring
- **APM**: Application Insights with custom telemetry
- **Alerts**: 
  - Latency > 500ms on `/checkout` → PagerDuty
  - Error rate > 1% → Slack notification
  - Failed payments → Email to finance team

---

## Known Issues & Technical Debt

### Active Issues
1. **Inventory Race Condition** (Issue #234): Concurrent checkouts can oversell products
   - **Workaround**: Pessimistic locking on `inventory.quantity`
   - **Fix Planned**: Implement distributed lock via Redis in Q1 2025

2. **Search Performance** (Issue #189): Full-text search on product descriptions is slow
   - **Current**: PostgreSQL `tsvector` on 100k+ products
   - **Fix Planned**: Migrate to Azure Cognitive Search

3. **Order Export Memory Issue** (Issue #156): `/admin/orders/export` OOMs on large date ranges
   - **Workaround**: Limit exports to 30-day windows
   - **Fix Needed**: Implement streaming CSV response

### Historical Context
- **Migration from Django** (Nov 2024): Some code still has Django-isms (e.g., `objects.filter()` → must be `session.execute(select(...).where(...))`)
- **Stripe API Upgrade** (Dec 2024): Old code used deprecated `Charge` API → must use `PaymentIntent`

---

## Code Review Priorities for This Project

When reviewing git diffs for this project, prioritize:

1. **Inventory Management**: Any changes to `services/inventory.py` must be scrutinized for race conditions
2. **Payment Processing**: Changes to `services/payment.py` must maintain idempotency and webhook validation
3. **Authentication**: Changes to `api/auth.py` must not bypass rate limiting or token validation
4. **Database Queries**: Look for missing eager loading, especially in order/product endpoints
5. **Async/Await**: Ensure no blocking I/O in async functions (common mistake: `requests` instead of `httpx`)

---

## Key Contact & Documentation

- **Architecture Decision Records**: `docs/adr/` directory
- **API Documentation**: Auto-generated Swagger at `/docs`
- **Runbook**: `docs/runbook.md` for production incidents
- **Team Lead**: @alice (for architectural questions)
- **Security Contact**: @bob (for security-related changes)

---

## Review History

- **2025-01-15**: Added notes on Stripe API upgrade and async patterns
- **2024-12-10**: Documented known N+1 issues and caching strategy
- **2024-11-20**: Initial project reference created
