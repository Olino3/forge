# Documentation Generator Examples

This file contains example scenarios demonstrating how to use the documentation-generator skill for various documentation tasks.

---

## Example 1: REST API Endpoint Documentation

### Scenario
Developer needs comprehensive API documentation for a user management service with CRUD endpoints.

### User Prompt
```
Document the REST API endpoints in src/api/users.py
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: REST API endpoints for user management
- Target audience: Frontend developers and API consumers
- Doc type: API Reference

**Step 2 - Analyze Source Material**:
```
Analyzed: src/api/users.py

Endpoints found:
- GET    /api/v1/users          → list_users(page, per_page, sort_by)
- GET    /api/v1/users/{id}     → get_user(user_id)
- POST   /api/v1/users          → create_user(body: UserCreate)
- PUT    /api/v1/users/{id}     → update_user(user_id, body: UserUpdate)
- DELETE /api/v1/users/{id}     → delete_user(user_id)

Models:
- UserCreate: name (str, required), email (str, required), role (str, default="viewer")
- UserUpdate: name (str, optional), email (str, optional), role (str, optional)
- UserResponse: id (int), name (str), email (str), role (str), created_at (datetime)

Authentication: Bearer token via Authorization header
Rate limiting: 100 requests/minute per API key
```

**Step 3 - Load Project Memory**:
- No existing memory found; will create after generation
- Existing docs found: OpenAPI spec at `docs/openapi.yaml` — adopting same naming conventions

**Step 4 - Generate Documentation**:
Using `templates/api_doc_template.md`.

### Generated Documentation

```markdown
# User Management API

## Overview

The User Management API provides CRUD operations for managing user accounts.
All endpoints require authentication via Bearer token.

**Base URL**: `https://api.example.com/api/v1`

## Authentication

Include a valid Bearer token in the `Authorization` header:

    Authorization: Bearer <your-api-token>

## Endpoints

### List Users

**GET** `/users`

Returns a paginated list of users.

| Parameter  | Type   | In    | Required | Default | Description              |
|------------|--------|-------|----------|---------|--------------------------|
| page       | int    | query | No       | 1       | Page number              |
| per_page   | int    | query | No       | 20      | Results per page (max 100) |
| sort_by    | string | query | No       | name    | Sort field (name, created_at) |

**Response** `200 OK`:
    {
      "data": [
        {"id": 1, "name": "Ada Lovelace", "email": "ada@example.com", "role": "admin", "created_at": "2025-01-15T10:30:00Z"}
      ],
      "pagination": {"page": 1, "per_page": 20, "total": 42}
    }

### Create User

**POST** `/users`

Creates a new user account.

**Request Body**:
    {
      "name": "Grace Hopper",
      "email": "grace@example.com",
      "role": "editor"
    }

**Response** `201 Created`:
    {
      "id": 2,
      "name": "Grace Hopper",
      "email": "grace@example.com",
      "role": "editor",
      "created_at": "2025-01-15T12:00:00Z"
    }

**Error Codes**:
| Status | Description                    |
|--------|--------------------------------|
| 400    | Invalid request body           |
| 409    | Email already exists           |
| 422    | Validation error               |

## Rate Limiting

- **Limit**: 100 requests per minute per API key
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Reset`
```

**Step 5 - Output**:
File: `/claudedocs/api_users.md`

---

## Example 2: Python Module Documentation

### Scenario
Developer wants full documentation for a caching utility module.

### User Prompt
```
Generate documentation for the cache module in src/utils/cache.py
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: Python module `src/utils/cache.py`
- Target audience: Internal developers
- Doc type: Module Guide

**Step 2 - Analyze Source Material**:
```
Analyzed: src/utils/cache.py

Classes:
- CacheBackend (abstract base class)
  - get(key: str) -> Optional[Any]
  - set(key: str, value: Any, ttl: int = 300) -> None
  - delete(key: str) -> bool
  - clear() -> None

- MemoryCache(CacheBackend)
  - __init__(max_size: int = 1000)
  - Implements LRU eviction

- RedisCache(CacheBackend)
  - __init__(url: str, prefix: str = "app:")
  - Supports key prefixing and serialization

Functions:
- get_cache(backend: str = "memory") -> CacheBackend  (factory function)

Constants:
- DEFAULT_TTL = 300
- MAX_KEY_LENGTH = 256
```

**Step 3 - Load Project Memory**:
- No existing memory; docstrings use Google style

**Step 4 - Generate Documentation**:
Using `templates/module_doc_template.md`.

### Generated Documentation

```markdown
# Cache Module

## Overview

The `cache` module provides a pluggable caching layer with support for
in-memory LRU caching and Redis-backed persistence. All backends implement
the `CacheBackend` interface for consistent usage across the application.

**Module**: `src/utils/cache.py`

## Quick Start

    from src.utils.cache import get_cache

    cache = get_cache("memory")
    cache.set("user:42", {"name": "Ada"}, ttl=600)
    user = cache.get("user:42")  # {"name": "Ada"}

## API Reference

### `get_cache(backend="memory")`

Factory function that returns a cache backend instance.

| Parameter | Type | Default  | Description                          |
|-----------|------|----------|--------------------------------------|
| backend   | str  | "memory" | Backend type: "memory" or "redis"    |

**Returns**: `CacheBackend` instance

**Raises**: `ValueError` if backend type is unknown

### Class: `CacheBackend` (ABC)

Abstract base class defining the cache interface.

#### `get(key: str) -> Optional[Any]`
Retrieve a value by key. Returns `None` if the key does not exist or has expired.

#### `set(key: str, value: Any, ttl: int = 300) -> None`
Store a value with an optional time-to-live in seconds.

#### `delete(key: str) -> bool`
Remove a key. Returns `True` if the key existed.

#### `clear() -> None`
Remove all entries from the cache.

### Class: `MemoryCache(CacheBackend)`

In-memory LRU cache with configurable maximum size.

    cache = MemoryCache(max_size=500)
    cache.set("key", "value", ttl=60)

### Class: `RedisCache(CacheBackend)`

Redis-backed cache with key prefixing and JSON serialization.

    cache = RedisCache(url="redis://localhost:6379", prefix="myapp:")
    cache.set("session:abc", {"user_id": 1})

## Constants

| Constant       | Value | Description                    |
|----------------|-------|--------------------------------|
| DEFAULT_TTL    | 300   | Default time-to-live (seconds) |
| MAX_KEY_LENGTH | 256   | Maximum allowed key length     |
```

**Step 5 - Output**:
File: `/claudedocs/module_cache.md`

---

## Example 3: Project README Generation

### Scenario
New open-source project needs a comprehensive README.

### User Prompt
```
Generate a README.md for this project
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: Entire project
- Target audience: Open-source community, potential contributors
- Doc type: README

**Step 2 - Analyze Source Material**:
```
Analyzed: Repository root

Project: forge-toolkit
Language: Python 3.11+
Framework: Click (CLI), FastAPI (server mode)
Package manager: Poetry
Test framework: pytest
CI: GitHub Actions

Entry point: src/cli/main.py
Key modules: src/parser/, src/analyzer/, src/reporter/
Config: pyproject.toml, .forge.yaml
```

**Step 3 - Load Project Memory**:
- Found existing CONTRIBUTING.md — will reference it
- No documentation tooling detected

**Step 4 - Generate Documentation**:

### Generated Documentation

```markdown
# Forge Toolkit

> A CLI tool for analyzing and transforming codebases with surgical precision.

[![CI](https://github.com/example/forge-toolkit/actions/workflows/ci.yml/badge.svg)]
[![PyPI](https://img.shields.io/pypi/v/forge-toolkit)]

## Features

- **Code Analysis**: Parse and analyze code structure across multiple languages
- **Transformation**: Apply automated refactoring patterns
- **Reporting**: Generate detailed reports in Markdown, JSON, or HTML
- **Server Mode**: Run as a local API server for IDE integration

## Installation

    pip install forge-toolkit

Or with Poetry:

    poetry add forge-toolkit

### Requirements
- Python 3.11 or higher
- Git 2.30+

## Quick Start

    # Analyze a project
    forge analyze ./my-project

    # Generate a report
    forge report ./my-project --format markdown --output report.md

    # Start server mode
    forge serve --port 8080

## Configuration

Create a `.forge.yaml` in your project root:

    analysis:
      ignore:
        - "vendor/**"
        - "**/*.generated.py"
      depth: 3

    reporting:
      format: markdown
      include_metrics: true

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
```

**Step 5 - Output**:
File: `README.md` (repository root)

---

## Example 4: Architecture Decision Record (ADR)

### Scenario
Team needs to document a decision to migrate from REST to GraphQL.

### User Prompt
```
Create an ADR for our decision to adopt GraphQL for the public API
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: Architecture decision — API technology choice
- Target audience: Internal developers, future team members
- Doc type: Architecture Doc (ADR)

**Step 2 - Analyze Source Material**:
```
Analyzed: Existing API layer

Current state:
- REST API with 47 endpoints across 8 resource types
- Average response includes 60% unused fields (over-fetching)
- Mobile clients make 4-6 requests per screen (under-fetching)
- 3 versions maintained simultaneously (v1, v2, v3)

Proposed state:
- Single GraphQL endpoint
- Schema-driven development
- Client-specified field selection
```

**Step 3 - Load Project Memory**:
- Found existing ADRs in `docs/adr/` using MADR format
- Adopting same template and numbering convention (next: ADR-0012)

**Step 4 - Generate Documentation**:

### Generated Documentation

```markdown
# ADR-0012: Adopt GraphQL for Public API

**Status**: Accepted
**Date**: 2025-01-15
**Deciders**: API Team, Platform Architect

## Context

The current REST API suffers from over-fetching (60% of response fields
unused by mobile clients) and under-fetching (4-6 requests per screen).
Maintaining 3 API versions simultaneously increases engineering burden.

## Decision

Adopt GraphQL as the primary public API technology, replacing versioned
REST endpoints over a 6-month migration period.

## Consequences

### Positive
- Clients request only needed fields, reducing payload size by ~60%
- Single endpoint eliminates API versioning overhead
- Strongly typed schema serves as living documentation
- Introspection enables automated client code generation

### Negative
- Team requires GraphQL training (estimated 2 weeks)
- Query complexity analysis needed to prevent abuse
- Caching strategy must change (no HTTP caching by default)

### Neutral
- REST endpoints maintained in read-only mode for 12 months
- Internal service-to-service communication remains gRPC

## Alternatives Considered

1. **REST with sparse fieldsets (JSON:API)**: Partial solution; doesn't
   address under-fetching or versioning burden.
2. **gRPC for all APIs**: Strong typing but poor browser support without
   a proxy layer.

## References
- [GraphQL Specification](https://spec.graphql.org/)
- [ADR-0003: REST API Versioning Strategy](docs/adr/0003-rest-versioning.md)
```

**Step 5 - Output**:
File: `docs/adr/0012-adopt-graphql.md`

---

## Example 5: Migration Guide for Breaking Changes

### Scenario
Library is releasing v3.0 with breaking changes and needs a migration guide.

### User Prompt
```
Write a migration guide from v2.x to v3.0 for our authentication library
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: Breaking changes between v2.x and v3.0
- Target audience: Library consumers upgrading their applications
- Doc type: Migration Guide

**Step 2 - Analyze Source Material**:
```
Analyzed: git diff v2.5.0...v3.0.0-rc1

Breaking changes identified:
1. AuthClient constructor signature changed
2. Token refresh callback is now async
3. verify_token() renamed to validate_token()
4. Config dict replaced with AuthConfig dataclass
5. Python 3.8 and 3.9 support dropped
```

**Step 3 - Load Project Memory**:
- Found previous migration guide: `docs/migration-v1-to-v2.md` — following same format

**Step 4 - Generate Documentation**:

### Generated Documentation

```markdown
# Migration Guide: v2.x → v3.0

This guide covers all breaking changes in v3.0 and provides step-by-step
instructions to update your application.

**Estimated migration time**: 30–60 minutes for typical applications.

## Prerequisites

- Python 3.10 or higher (3.8 and 3.9 are no longer supported)
- Update dependency: `pip install auth-lib>=3.0.0`

## Breaking Changes

### 1. AuthClient Constructor

**Before (v2.x)**:
    client = AuthClient("client-id", "client-secret", region="us-east-1")

**After (v3.0)**:
    from auth_lib import AuthConfig

    config = AuthConfig(
        client_id="client-id",
        client_secret="client-secret",
        region="us-east-1",
    )
    client = AuthClient(config)

**Reason**: Structured configuration enables validation at construction time
and supports loading from environment variables via `AuthConfig.from_env()`.

### 2. Async Token Refresh

**Before (v2.x)**:
    def on_refresh(old_token):
        save_token(old_token)
        return new_token

    client.set_refresh_callback(on_refresh)

**After (v3.0)**:
    async def on_refresh(old_token):
        await save_token(old_token)
        return new_token

    client.set_refresh_callback(on_refresh)

**Reason**: Async callbacks allow non-blocking I/O during token refresh.

### 3. Renamed: verify_token → validate_token

**Before (v2.x)**:
    result = client.verify_token(token_string)

**After (v3.0)**:
    result = client.validate_token(token_string)

**Find and replace**: Search your codebase for `verify_token` and rename
to `validate_token`. The return type and parameters are unchanged.

## Automated Migration

Run the provided codemod to handle straightforward renames:

    auth-lib migrate --from 2 --to 3 --path ./src

This handles renaming `verify_token` calls but does not convert sync
callbacks to async. Review the output and apply async changes manually.

## Troubleshooting

| Error                          | Cause                        | Fix                              |
|--------------------------------|------------------------------|----------------------------------|
| `TypeError: AuthClient()`      | Old positional args used     | Switch to `AuthConfig` object    |
| `RuntimeError: sync callback`  | Sync refresh callback        | Convert callback to `async def`  |
| `AttributeError: verify_token` | Old method name              | Rename to `validate_token`       |

## Need Help?

- [Changelog](CHANGELOG.md) — full list of changes
- [GitHub Discussions](https://github.com/example/auth-lib/discussions)
```

**Step 5 - Output**:
File: `docs/migration-v2-to-v3.md`

---

## Example 6: Function and Class Documentation with Examples

### Scenario
Developer needs thorough documentation for a data validation module with multiple classes.

### User Prompt
```
Document the Validator class and its subclasses in src/validation/validators.py
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: `Validator` base class and subclasses
- Target audience: Internal developers using the validation framework
- Doc type: Module Guide (class-focused)

**Step 2 - Analyze Source Material**:
```
Analyzed: src/validation/validators.py

Classes:
- Validator (ABC)
  - validate(value: Any) -> ValidationResult
  - chain(*validators) -> ChainedValidator  (classmethod)

- StringValidator(Validator)
  - __init__(min_length=0, max_length=None, pattern=None)

- NumberValidator(Validator)
  - __init__(min_value=None, max_value=None, allow_float=True)

- EmailValidator(StringValidator)
  - __init__(allow_plus_addressing=True)

- SchemaValidator(Validator)
  - __init__(schema: dict)

Data classes:
- ValidationResult: is_valid (bool), errors (list[str]), value (Any)
```

**Step 3 - Load Project Memory**:
- Docstring convention: Google style
- Existing docs reference in `docs/validation.md` — will update

**Step 4 - Generate Documentation**:

### Generated Documentation

```markdown
# Validation Framework

## Overview

The validation framework provides composable, type-safe validators for
input data. All validators extend the `Validator` base class and return
`ValidationResult` objects.

## Quick Start

    from src.validation.validators import StringValidator, EmailValidator

    validator = StringValidator(min_length=1, max_length=100)
    result = validator.validate("hello")
    assert result.is_valid

    email_validator = EmailValidator()
    result = email_validator.validate("user@example.com")
    assert result.is_valid

## Chaining Validators

Combine multiple validators with `Validator.chain()`:

    from src.validation.validators import Validator, StringValidator, NumberValidator

    username_validator = Validator.chain(
        StringValidator(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$"),
    )

    result = username_validator.validate("ada_lovelace")
    assert result.is_valid

    result = username_validator.validate("ab")
    assert not result.is_valid
    assert "Minimum length is 3" in result.errors

## API Reference

### `ValidationResult`

Data class returned by all validators.

| Field    | Type       | Description                          |
|----------|------------|--------------------------------------|
| is_valid | bool       | Whether validation passed            |
| errors   | list[str]  | List of error messages (empty if valid) |
| value    | Any        | The validated (possibly coerced) value |

### `Validator` (ABC)

Abstract base class for all validators.

#### `validate(value: Any) -> ValidationResult`
Validate a single value. Must be implemented by subclasses.

#### `chain(*validators) -> ChainedValidator` (classmethod)
Create a validator that runs multiple validators in sequence, short-circuiting on first failure.

### `StringValidator(Validator)`

Validates string values against length and pattern constraints.

    validator = StringValidator(min_length=1, max_length=255, pattern=r"^\w+$")

| Parameter  | Type         | Default | Description                |
|------------|--------------|---------|----------------------------|
| min_length | int          | 0       | Minimum string length      |
| max_length | Optional[int]| None    | Maximum string length      |
| pattern    | Optional[str]| None    | Regex pattern to match     |

### `NumberValidator(Validator)`

Validates numeric values against range constraints.

    validator = NumberValidator(min_value=0, max_value=100, allow_float=False)

| Parameter   | Type           | Default | Description              |
|-------------|----------------|---------|--------------------------|
| min_value   | Optional[float]| None    | Minimum allowed value    |
| max_value   | Optional[float]| None    | Maximum allowed value    |
| allow_float | bool           | True    | Whether to accept floats |

### `EmailValidator(StringValidator)`

Validates email address format.

    validator = EmailValidator(allow_plus_addressing=True)
    validator.validate("user+tag@example.com")  # is_valid: True

| Parameter            | Type | Default | Description                    |
|----------------------|------|---------|--------------------------------|
| allow_plus_addressing| bool | True    | Allow `+` aliases in local part|

### `SchemaValidator(Validator)`

Validates a dictionary against a schema definition.

    schema = {
        "name": StringValidator(min_length=1),
        "age": NumberValidator(min_value=0, max_value=150),
        "email": EmailValidator(),
    }
    validator = SchemaValidator(schema)
    result = validator.validate({"name": "Ada", "age": 36, "email": "ada@example.com"})
    assert result.is_valid
```

**Step 5 - Output**:
File: `docs/validation.md` (updated existing file)

---

## Summary of Use Cases

1. **REST API documentation** — Endpoint reference with parameters, responses, and error codes
2. **Python module documentation** — Classes, functions, constants with usage examples
3. **Project README** — Overview, installation, quick start, and contributing guide
4. **Architecture decision record** — Context, decision, consequences, and alternatives
5. **Migration guide** — Breaking changes with before/after comparisons and automation
6. **Function/class documentation** — Detailed API reference with chaining and composition examples

## Best Practices

- Always analyze source code before writing — never guess at interfaces
- Adopt the project's existing documentation style and conventions
- Include runnable examples for every public function and class
- Document error cases and edge conditions, not just the happy path
- Use tables for parameter lists and structured data
- Cross-reference related modules, types, and external resources
- Keep documentation close to the code it describes
- Update project memory after every generation for future consistency
