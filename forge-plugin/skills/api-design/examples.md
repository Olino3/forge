# API Design Examples

This file contains example scenarios demonstrating how to use the api-design skill for various API design tasks.

---

## Example 1: E-Commerce REST API Design

### Scenario
A team is building a new e-commerce platform and needs a comprehensive REST API for product catalog, cart, and order management.

### User Prompt
```
Design a REST API for our e-commerce platform covering products, carts, and orders
```

### Skill Execution

**Step 1 — Identify API Scope**:
- Surface: New greenfield REST API
- Style: RESTful (resource-oriented)
- Consumers: Mobile apps (iOS/Android) and web SPA
- Constraints: OAuth2 auth, cursor-based pagination, 500 req/min rate limit

**Step 2 — Load Memory**:
- No existing memory; will create after generation

**Step 3 — Load Context**:
- Loaded engineering domain patterns

**Step 4 — Resource Model**:

| Resource | URL | Methods | Description |
|----------|-----|---------|-------------|
| Products | `/api/v1/products` | GET, POST | Product catalog |
| Product | `/api/v1/products/{id}` | GET, PUT, DELETE | Single product |
| Product Variants | `/api/v1/products/{id}/variants` | GET, POST | Size/color variants |
| Cart | `/api/v1/cart` | GET, PUT, DELETE | Current user's cart (singleton) |
| Cart Items | `/api/v1/cart/items` | GET, POST | Items in cart |
| Cart Item | `/api/v1/cart/items/{id}` | PATCH, DELETE | Single cart item |
| Orders | `/api/v1/orders` | GET, POST | Order history + place order |
| Order | `/api/v1/orders/{id}` | GET | Single order |
| Order Cancel | `/api/v1/orders/{id}/actions/cancel` | POST | Cancel an order (RPC action) |

**Step 5 — API Contracts**:

```markdown
## List Products

**GET** `/api/v1/products`

| Parameter | Type   | In    | Required | Description |
|-----------|--------|-------|----------|-------------|
| cursor    | string | query | No       | Pagination cursor |
| limit     | int    | query | No       | Results per page (default 20, max 100) |
| category  | string | query | No       | Filter by category slug |
| min_price | number | query | No       | Minimum price filter |
| max_price | number | query | No       | Maximum price filter |
| sort      | string | query | No       | Sort: price_asc, price_desc, newest |

**Response** `200 OK`:
    {
      "data": [
        {
          "id": "prod_a1b2c3",
          "name": "Wireless Headphones",
          "slug": "wireless-headphones",
          "price": { "amount": 7999, "currency": "USD" },
          "category": "electronics",
          "in_stock": true,
          "created_at": "2025-01-15T10:30:00Z"
        }
      ],
      "meta": {
        "cursor": "eyJpZCI6MTAwfQ==",
        "has_more": true,
        "total": 342
      }
    }

## Place Order

**POST** `/api/v1/orders`

**Request Body**:
    {
      "shipping_address_id": "addr_x1y2z3",
      "payment_method_id": "pm_a1b2c3",
      "notes": "Leave at door"
    }

**Response** `201 Created`:
    Location: /api/v1/orders/ord_m1n2o3

    {
      "data": {
        "id": "ord_m1n2o3",
        "status": "pending",
        "total": { "amount": 15998, "currency": "USD" },
        "items_count": 2,
        "created_at": "2025-01-15T12:00:00Z"
      }
    }

**Errors**:
| Status | Type | Detail |
|--------|------|--------|
| 400 | invalid_request | Cart is empty |
| 402 | payment_failed | Payment method declined |
| 409 | conflict | One or more items are out of stock |
```

**Step 6 — Output**:
File: `/claudedocs/api-design_ecommerce_2025-01-15.md`

---

## Example 2: Internal Microservices API Audit

### Scenario
A team has accumulated 47 REST endpoints across 3 microservices with inconsistent conventions. They need an audit and standardization guide.

### User Prompt
```
Audit our microservices APIs and create a consistency report with recommended standards
```

### Skill Execution

**Step 1 — Identify API Scope**:
- Surface: Existing API audit across 3 services (users, billing, notifications)
- Style: RESTful (currently inconsistent)
- Consumers: Internal services (service-to-service)
- Constraints: Must be backward-compatible; phased migration

**Step 2 — Load Memory**:
- Found existing API conventions from a previous review
- Adopted established naming patterns

**Step 3 — Load Context**:
- Loaded engineering domain patterns

**Step 4 — Audit Findings**:

```markdown
## Consistency Report

### Naming Inconsistencies (17 violations)

| Service | Endpoint | Issue | Recommended |
|---------|----------|-------|-------------|
| users | `GET /user` | Singular noun | `GET /users` |
| users | `POST /createUser` | Verb in URL | `POST /users` |
| billing | `GET /get-invoices` | Verb prefix | `GET /invoices` |
| billing | `GET /invoices/list` | Redundant /list | `GET /invoices` |
| notifications | `PUT /notification/update/{id}` | Verb + singular | `PUT /notifications/{id}` |

### Status Code Misuse (8 violations)

| Service | Endpoint | Current | Correct | Reason |
|---------|----------|---------|---------|--------|
| users | `POST /users` | 200 | 201 | Resource creation must return 201 |
| billing | `DELETE /invoices/{id}` | 200 | 204 | Deletion should return No Content |
| notifications | `POST /notifications` (duplicate) | 500 | 409 | Conflict, not server error |

### Missing Pagination (5 endpoints)

| Service | Endpoint | Record Count | Risk |
|---------|----------|-------------|------|
| users | `GET /users` | ~50K | Memory exhaustion |
| billing | `GET /invoices` | ~200K | Timeout |
| notifications | `GET /notifications` | ~1M | Critical |

### Recommended Standards

1. **URL Pattern**: `/{service}/api/v1/{resource}`
2. **Naming**: Plural nouns, kebab-case
3. **Pagination**: Cursor-based for all list endpoints
4. **Errors**: RFC 7807 Problem Details format
5. **Auth**: Service-to-service mTLS with JWT for user context
```

**Step 6 — Output**:
File: `/claudedocs/api-design_microservices-audit_2025-01-15.md`

---

## Example 3: API Versioning Strategy

### Scenario
A public API is approaching v2 with breaking changes. The team needs a versioning strategy that supports both old and new consumers during migration.

### User Prompt
```
Design a versioning strategy for our public API that minimizes disruption during the v1 to v2 migration
```

### Skill Execution

**Step 1 — Identify API Scope**:
- Surface: Versioning strategy for public API
- Consumers: ~200 third-party integrators
- Constraints: v1 must remain operational for 12 months minimum; no downtime during migration

**Step 4 — Versioning Design**:

```markdown
## Versioning Strategy: URL Path + Sunset Headers

### Approach
URL path versioning (`/api/v1/`, `/api/v2/`) with sunset lifecycle management.

### Why URL Path Versioning
- Explicit — consumers see the version in every request
- Cacheable — CDN can cache per version
- Debuggable — version visible in logs and monitoring
- Simple — no custom header parsing required

### Lifecycle Phases

| Phase | Duration | v1 Status | v2 Status |
|-------|----------|-----------|-----------|
| 1. Parallel launch | Month 0–3 | Active | Beta |
| 2. Migration | Month 3–9 | Deprecated | Active |
| 3. Sunset | Month 9–12 | Read-only | Active |
| 4. Retirement | Month 12+ | Removed | Active |

### Deprecation Headers (Phase 2+)

All v1 responses include:
    Deprecation: true
    Sunset: Sat, 15 Jan 2027 00:00:00 GMT
    Link: </api/v2/users>; rel="successor-version"

### Breaking Change Categories

| Change Type | v1 Handling | v2 Behavior |
|-------------|-------------|-------------|
| Renamed field | Both names returned | New name only |
| Removed endpoint | Returns 410 Gone with migration link | N/A |
| Changed auth | Both methods accepted | New method only |
| New required field | Optional in v1 | Required in v2 |

### Migration Support

1. **Migration guide**: Published at `/api/v2/docs/migration`
2. **Compatibility mode**: `?compat=v1` on v2 endpoints returns v1-shaped responses for 6 months
3. **Webhook notifications**: Notify integrators 90, 60, 30 days before sunset
4. **Usage dashboard**: Per-consumer v1 usage tracking to identify laggards
```

**Step 6 — Output**:
File: `/claudedocs/api-design_versioning-strategy_2025-01-15.md`

---

## Example 4: RPC-Style Action API for Workflow Engine

### Scenario
A workflow engine needs RPC-style actions for state transitions that don't map cleanly to CRUD operations.

### User Prompt
```
Design API endpoints for a document approval workflow with submit, review, approve, reject, and publish actions
```

### Skill Execution

**Step 4 — Resource + Action Model**:

```markdown
## Document Workflow API

### Resources (CRUD)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/documents` | List documents (filterable by status) |
| POST | `/api/v1/documents` | Create draft document |
| GET | `/api/v1/documents/{id}` | Get document with current status |
| PUT | `/api/v1/documents/{id}` | Update draft content |
| DELETE | `/api/v1/documents/{id}` | Delete draft (only in draft status) |

### Actions (RPC-style)

| Method | Path | Description | Valid From |
|--------|------|-------------|------------|
| POST | `/api/v1/documents/{id}/actions/submit` | Submit for review | draft |
| POST | `/api/v1/documents/{id}/actions/approve` | Approve document | in_review |
| POST | `/api/v1/documents/{id}/actions/reject` | Reject with reason | in_review |
| POST | `/api/v1/documents/{id}/actions/publish` | Publish approved doc | approved |
| POST | `/api/v1/documents/{id}/actions/archive` | Archive published doc | published |

### State Machine

    draft → submitted → in_review → approved → published → archived
                              ↓
                          rejected → draft (resubmit)

### Action Request/Response

**POST** `/api/v1/documents/{id}/actions/reject`

**Request**:
    {
      "reason": "Section 3 needs compliance review",
      "reviewer_notes": "Please add data retention policy"
    }

**Response** `200 OK`:
    {
      "data": {
        "id": "doc_a1b2c3",
        "status": "rejected",
        "previous_status": "in_review",
        "transitioned_at": "2025-01-15T14:30:00Z",
        "transitioned_by": "user_x1y2z3"
      }
    }

**Error** `409 Conflict` (invalid transition):
    {
      "type": "https://api.example.com/errors/invalid-transition",
      "title": "Invalid State Transition",
      "status": 409,
      "detail": "Cannot reject a document in 'draft' status. Must be 'in_review'.",
      "current_status": "draft",
      "allowed_actions": ["submit"]
    }
```

**Step 6 — Output**:
File: `/claudedocs/api-design_workflow-api_2025-01-15.md`

---

## Summary of Use Cases

1. **Greenfield API design** — Full resource model, contracts, pagination, and error catalog
2. **API consistency audit** — Identify violations and recommend standards across services
3. **Versioning strategy** — Plan backward-compatible migrations with sunset lifecycle
4. **RPC-style actions** — Design state machine transitions alongside CRUD resources

## Best Practices

- Always start with the resource model before defining endpoints
- Use consistent naming across all resources — never mix conventions
- Design error responses as carefully as success responses
- Include pagination from day one — retrofitting is painful
- Document every endpoint in OpenAPI format for discoverability
- Plan for versioning even if you think you won't need it
