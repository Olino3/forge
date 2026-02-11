---
id: "python/fastapi_patterns"
domain: python
title: "FastAPI Patterns and Best Practices"
type: framework
estimatedTokens: 400
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2025-11-14"
maintainedFor: "python-code-review"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 90
    keywords: [response-model, async, dependencies, validation]
  - name: "Pydantic Models"
    estimatedTokens: 50
    keywords: [pydantic, validation, field, schema]
  - name: "Async/Await Issues"
    estimatedTokens: 50
    keywords: [async, await, blocking, sync]
  - name: "Dependency Injection"
    estimatedTokens: 50
    keywords: [depends, dependency, injection, state]
  - name: "Security Issues"
    estimatedTokens: 60
    keywords: [auth, cors, sql-injection, rate-limiting]
tags: [python, fastapi, pydantic, async, api]
crossDomainTriggers: ["security/security_guidelines"]
detectionTriggers: ["from fastapi import", "@router.get", "BaseModel"]
---

# FastAPI Patterns

Quick reference for FastAPI best practices and common issues. For detailed examples, see [FastAPI documentation](https://fastapi.tiangolo.com/).

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|------------|
| **Missing response models** | No `response_model` parameter | Always specify `response_model` for type safety | [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/) |
| **Synchronous database calls** | Sync SQLAlchemy in async endpoints | Use async database libraries (databases, sqlalchemy async) | [Async SQL](https://fastapi.tiangolo.com/advanced/async-sql-databases/) |
| **Not using dependencies** | Repeated code in endpoints | Use `Depends()` for reusable logic | [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) |
| **Missing validation** | Using dict instead of Pydantic models | Always use Pydantic `BaseModel` for validation | [Request Body](https://fastapi.tiangolo.com/tutorial/body/) |
| **Blocking operations in async** | `requests.get()` in async function | Use `httpx` or `asyncio.to_thread()` | [Async](https://fastapi.tiangolo.com/async/) |
| **Global database connections** | DB connection at module level | Use dependency injection for connections | [SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) |
| **No error handling** | Endpoints without try/except | Use `HTTPException` for proper error responses | [Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) |

---

## Pydantic Models

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **Missing field validation** | No `Field()` with validators | Use `Field()` with `min_length`, `max_length`, `ge`, `le`, etc. |
| **Mutable defaults** | `list` or `dict` as default | Use `Field(default_factory=list)` |
| **No example values** | No `Config.schema_extra` | Add examples for API docs |
| **Accepting extra fields** | No `Config.extra = "forbid"` | Explicitly forbid extra fields for security |

[Pydantic docs](https://docs.pydantic.dev/)

---

## Async/Await Issues

| Issue | Detection Pattern | Recommended Fix |
|-------|-------------------|-----------------|
| **Mixing sync/async** | `requests` library in async function | Use `httpx.AsyncClient` |
| **Blocking I/O** | File I/O in async function | Use `aiofiles` or `asyncio.to_thread()` |
| **Not awaiting** | Async function called without `await` | Always `await` async functions |
| **Database blocking** | Sync SQLAlchemy in async | Use async SQLAlchemy or databases library |

[Concurrency and async](https://fastapi.tiangolo.com/async/)

---

## Dependency Injection

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **Not using `Depends()`** | Repeated logic across endpoints | Extract to dependency function |
| **Global state** | Mutable global variables | Use dependencies for state management |
| **No database session mgmt** | Manual session creation | Use `Depends(get_db)` pattern |
| **No authentication** | Direct JWT parsing in endpoints | Use OAuth2 dependency |

[Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

## Common Detection Patterns

```python
# ❌ No response model
@app.post("/users/")
async def create_user(user: UserCreate):
    return some_dict  # No type safety

# ✅ With response model
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate) -> User:
    return user

# ❌ Sync code in async
@app.get("/data/")
async def get_data():
    response = requests.get("https://api.example.com")  # Blocking!
    return response.json()

# ✅ Async client
@app.get("/data/")
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
    return response.json()

# ❌ No dependency injection
@app.get("/items/")
async def get_items():
    db = SessionLocal()  # Manual session
    # ... use db ...
    db.close()

# ✅ With dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def get_items(db: Session = Depends(get_db)):
    # ... use db ...

# ❌ Missing Pydantic validation
@app.post("/items/")
async def create_item(item: dict):  # No validation
    return item

# ✅ With Pydantic model
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

---

## Security Issues

| Issue | Detection Pattern | Recommended Fix |
|-------|-------------------|-----------------|
| **No authentication** | Public endpoints with sensitive data | Add OAuth2/JWT dependencies |
| **Missing CORS** | No CORS middleware | Add `CORSMiddleware` with specific origins |
| **SQL injection** | String formatting in SQL | Use SQLAlchemy ORM or parameterized queries |
| **No rate limiting** | Endpoints without throttling | Add slowapi or similar middleware |
| **Secrets in code** | Hardcoded keys | Use environment variables with pydantic Settings |

[Security](https://fastapi.tiangolo.com/tutorial/security/)

---

## Tools

- **pytest**: Testing - [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- **SQLModel**: ORM with Pydantic - [SQLModel](https://sqlmodel.tiangolo.com/)
- **httpx**: Async HTTP client - [httpx](https://www.python-httpx.org/)
- **slowapi**: Rate limiting - [slowapi](https://github.com/laurents/slowapi)

---

## Official Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **FastAPI Best Practices**: https://github.com/zhanymkanov/fastapi-best-practices
- **Awesome FastAPI**: https://github.com/mjhea0/awesome-fastapi

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
