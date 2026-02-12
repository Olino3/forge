# FastAPI Skill Examples

This file provides sample usage scenarios for the `fastapi` skill.

---

## Example 1: Design a New User Service API

### Scenario
A team is starting a FastAPI-based user service and needs routing and model guidance.

### User Prompt
"Design the FastAPI structure for a user service with signup and login endpoints."

### Skill Execution
- **Step 1**: Confirm FastAPI version, OAuth2 needs, and database choice.
- **Step 2**: Load memory for `user-service` (none found).
- **Step 3**: Load FastAPI context and security references.
- **Step 4**: Review desired routes and authentication flow.
- **Step 5**: Recommend router layout, Pydantic models, and auth dependencies.
- **Step 6**: Output to `/claudedocs/fastapi_user-service_2026-02-12.md`.

### Generated Output
```markdown
# FastAPI Guidance - user-service

## API Structure
- `routers/auth.py`: /signup, /login
- `routers/users.py`: /users/me, /users/{id}
- `schemas/user.py`: UserCreate, UserRead, TokenResponse

## Auth Dependencies
- Use OAuth2PasswordBearer for token extraction
- Centralize auth in `dependencies/auth.py`

## Validation
- Enforce email validation with `EmailStr`
- Hash passwords with `passlib` before persistence
```

---

## Example 2: Async SQLAlchemy Integration

### Scenario
The team needs guidance for async DB usage and migrations.

### User Prompt
"How should we structure async SQLAlchemy sessions and migrations in FastAPI?"

### Skill Execution
- **Step 1**: Confirm SQLAlchemy 2.x async and Alembic usage.
- **Step 2**: Load memory for DB conventions.
- **Step 3**: Load FastAPI + Python context.
- **Step 4**: Inspect current dependency injection patterns.
- **Step 5**: Recommend session scope, repository pattern, and migrations.
- **Step 6**: Output to `/claudedocs/fastapi_db_2026-02-12.md`.

### Generated Output
```markdown
# FastAPI Guidance - db

## Session Pattern
- Create `AsyncSession` in dependency with `async with`
- Use `expire_on_commit=False`

## Migrations
- Use Alembic with `context.run_migrations()`
- Run migrations on deploy, not at startup

## Repository Layer
- Encapsulate queries in `repositories/` for testability
```

---

## Example 3: Secure Rate-Limited Public Endpoint

### Scenario
A public endpoint needs OAuth2 and rate limiting.

### User Prompt
"Secure our public `/reports` endpoint with OAuth2 and rate limiting."

### Skill Execution
- **Step 1**: Confirm auth provider and traffic expectations.
- **Step 2**: Load memory for security conventions.
- **Step 3**: Load FastAPI security context.
- **Step 4**: Review current route and dependencies.
- **Step 5**: Provide OAuth2/JWT and rate limiting approach.
- **Step 6**: Output to `/claudedocs/fastapi_reports_2026-02-12.md`.

### Generated Output
```markdown
# FastAPI Guidance - reports

## Security
- Require JWT bearer token with scope `reports:read`
- Validate audience and issuer in auth dependency

## Rate Limiting
- Apply Redis-backed limiter at 60 req/min per user
- Return 429 with `Retry-After` header
```
