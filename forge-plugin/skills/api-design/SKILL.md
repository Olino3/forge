---
name: api-design
description: "Design RESTful and RPC APIs with consistent resource modeling, versioning strategies, error handling, pagination, and security patterns. Produces API design documents, OpenAPI specs, and endpoint inventories. Prevents common API anti-patterns including chatty interfaces, inconsistent naming, missing pagination, and improper status codes."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, api_conventions.md]
    - type: "shared-project"
      usage: "reference"
## tags: [api, rest, rpc, design, openapi, endpoints, versioning, http]

# skill:api-design — RESTful and RPC API Design Patterns

## Version: 1.0.0

## Purpose

Design production-grade APIs that are consistent, discoverable, and evolvable. This skill guides the creation and review of RESTful and RPC API surfaces — from resource modeling and URL structure to versioning, error contracts, pagination, and security. It produces structured API design documents and OpenAPI-compatible specifications.

Use when:
- Designing a new API from scratch
- Reviewing an existing API for consistency and best practices
- Migrating between API styles (REST, RPC, hybrid)
- Establishing organization-wide API design standards
- Generating OpenAPI/Swagger specifications from design decisions

## File Structure

```
skills/api-design/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Identify API Scope and Requirements

**YOU MUST:**
1. Determine the **API surface** to design:
   - New API (greenfield design)
   - Existing API audit and improvement
   - API versioning or migration strategy
   - Organization-wide API standards document
2. Identify the **API style**:
   - RESTful (resource-oriented)
   - RPC (action-oriented)
   - Hybrid (resources with custom actions)
3. Determine **consumers**:
   - Public (third-party developers)
   - Internal (team/organization)
   - Partner (B2B integrations)
   - Mobile-first (bandwidth and latency sensitive)
4. Clarify **constraints**:
   - Existing conventions or style guides
   - Authentication mechanism (API key, OAuth2, JWT)
   - Rate limiting and quota requirements
   - Compliance requirements (GDPR, PCI-DSS)

**DO NOT PROCEED WITHOUT A CLEAR SCOPE**

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="api-design"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("api-design", "{project-name}")` to load existing API conventions
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill insights
3. If memory exists, adopt previously established naming conventions, versioning strategy, and error formats
4. If no memory exists, proceed and create it in Step 7

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Design Resource Model

**YOU MUST:**
1. **Identify resources** (nouns, not verbs):
   - Primary resources (e.g., `/users`, `/orders`, `/products`)
   - Sub-resources (e.g., `/users/{id}/addresses`)
   - Singleton resources (e.g., `/users/{id}/profile`)
2. **Define URL structure**:
   - Use plural nouns for collections: `/users` not `/user`
   - Use kebab-case for multi-word resources: `/order-items`
   - Nest only when a strong parent-child relationship exists (max 2 levels)
   - Use query parameters for filtering, not path segments
3. **Map HTTP methods to operations**:
   - `GET` — Read (safe, idempotent)
   - `POST` — Create (not idempotent)
   - `PUT` — Full replace (idempotent)
   - `PATCH` — Partial update (idempotent)
   - `DELETE` — Remove (idempotent)
4. **For RPC-style actions** use `POST /resources/{id}/actions/{action}`:
   - `POST /orders/{id}/actions/cancel`
   - `POST /users/{id}/actions/deactivate`

### Step 5: Design API Contracts

**YOU MUST define:**
1. **Request/Response schemas**:
   - Input validation rules (required fields, types, constraints)
   - Response envelope: `{ "data": ..., "meta": ..., "errors": ... }`
   - Consistent date format (ISO 8601: `2025-01-15T10:30:00Z`)
   - Consistent ID format (UUID v4 or integer, pick one)
2. **Pagination**:
   - Cursor-based for real-time data: `?cursor=abc&limit=20`
   - Offset-based for static data: `?page=1&per_page=20`
   - Always include `total`, `has_more`, and navigation links
3. **Error responses** (RFC 7807 Problem Details):
   ```json
   {
     "type": "https://api.example.com/errors/validation",
     "title": "Validation Error",
     "status": 422,
     "detail": "The 'email' field must be a valid email address.",
     "instance": "/users",
     "errors": [
       { "field": "email", "message": "Invalid email format" }
     ]
   }
   ```
4. **Status codes** (use correctly):
   - `200` OK — Successful read/update
   - `201` Created — Successful creation (include `Location` header)
   - `204` No Content — Successful deletion
   - `400` Bad Request — Malformed syntax
   - `401` Unauthorized — Missing or invalid credentials
   - `403` Forbidden — Valid credentials, insufficient permissions
   - `404` Not Found — Resource does not exist
   - `409` Conflict — State conflict (duplicate, version mismatch)
   - `422` Unprocessable Entity — Valid syntax, invalid semantics
   - `429` Too Many Requests — Rate limit exceeded (include `Retry-After`)
5. **Versioning strategy**:
   - URL path versioning: `/api/v1/users` (recommended for public APIs)
   - Header versioning: `Accept: application/vnd.api+json;version=2`
   - Query parameter: `?api-version=2025-01-15` (for date-based)
6. **Security patterns**:
   - Authentication via `Authorization: Bearer <token>`
   - Rate limiting headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
   - CORS configuration for browser consumers
   - Request ID for tracing: `X-Request-ID`

### Step 6: Generate Output

- Save output to `/claudedocs/api-design_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Resource inventory table
  - Endpoint reference (method, path, description, auth required)
  - Request/response schemas per endpoint
  - Error catalog
  - Versioning strategy summary
  - OpenAPI 3.1 snippet (if applicable)

### Step 7: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="api-design"`.

Store:
1. **api_conventions.md**: Naming conventions, versioning strategy, error format, pagination style
2. **project_overview.md**: API scope, consumer types, authentication approach, base URL structure

---

## API Design Principles

| Principle | Guideline |
|-----------|-----------|
| **Consistency** | Same patterns for same operations across all resources |
| **Discoverability** | HATEOAS links, OPTIONS responses, OpenAPI spec |
| **Evolvability** | Additive changes are non-breaking; never remove fields without versioning |
| **Minimal surprise** | Follow HTTP semantics; `GET` never mutates, `DELETE` is idempotent |
| **Security by default** | All endpoints require auth unless explicitly public |

## Common Anti-Patterns to Prevent

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Verbs in URLs (`/getUsers`) | Use nouns: `GET /users` |
| Inconsistent pluralization | Always plural for collections |
| `200` for errors | Use appropriate 4xx/5xx status codes |
| Nested URLs > 2 levels | Flatten with query params or top-level resources |
| No pagination on lists | Always paginate collections |
| Returning internal IDs in errors | Use opaque error codes |
| Missing `Content-Type` header | Always set `application/json` |

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: API scope, style, consumers, and constraints identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Resource model designed with proper URL structure and HTTP method mapping
- [ ] Step 5: Contracts defined — schemas, pagination, errors, status codes, versioning, security
- [ ] Step 6: Output saved with standard naming convention
- [ ] Step 7: Standard Memory Update pattern followed

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DESIGN**

---

## Further Reading

- **OpenAPI Specification**: https://swagger.io/specification/
- **JSON:API Specification**: https://jsonapi.org/
- **RFC 7807 Problem Details**: https://datatracker.ietf.org/doc/html/rfc7807
- **Google API Design Guide**: https://cloud.google.com/apis/design
- **Microsoft REST API Guidelines**: https://github.com/microsoft/api-guidelines

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — resource modeling, contracts, error handling, versioning, security patterns |
