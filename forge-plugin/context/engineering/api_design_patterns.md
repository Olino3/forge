---
id: "engineering/api_design_patterns"
domain: engineering
title: "API Design Patterns"
type: reference
estimatedTokens: 350
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "REST Conventions Quick Reference"
    estimatedTokens: 50
    keywords: [rest, conventions, quick, reference]
  - name: "Error Response Format"
    estimatedTokens: 18
    keywords: [error, response, format]
  - name: "Pagination Patterns"
    estimatedTokens: 29
    keywords: [pagination, patterns]
  - name: "Versioning Strategies"
    estimatedTokens: 31
    keywords: [versioning, strategies]
  - name: "What to Check in Reviews"
    estimatedTokens: 34
    keywords: [check, reviews]
  - name: "References"
    estimatedTokens: 15
    keywords: [references]
tags: [engineering, api, rest, pagination, versioning, error-handling]
---

# API Design Patterns

REST API conventions and patterns for consistent API design across projects.

## REST Conventions Quick Reference

| Method | Purpose | Idempotent | Status Codes |
|--------|---------|------------|-------------|
| GET | Retrieve resource(s) | Yes | 200, 404 |
| POST | Create resource | No | 201, 400, 409 |
| PUT | Replace resource | Yes | 200, 404 |
| PATCH | Partial update | No | 200, 404 |
| DELETE | Remove resource | Yes | 204, 404 |

## Error Response Format

Standard error structure (RFC 7807 Problem Details):

```json
{
  "type": "https://example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "detail": "Email field is required",
  "instance": "/api/users"
}
```

## Pagination Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| Offset-based | Simple lists, UI pages | `?page=2&limit=20` |
| Cursor-based | Large datasets, real-time feeds | `?cursor=abc123&limit=20` |
| Keyset | Sorted results, high performance | `?after_id=100&limit=20` |

## Versioning Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| URL path (`/v1/`) | Simple, explicit | URL pollution |
| Header (`Accept: v1`) | Clean URLs | Less discoverable |
| Query param (`?v=1`) | Easy to use | Caching issues |

## What to Check in Reviews

- Consistent resource naming (plural nouns: `/users`, not `/user`)
- Proper HTTP method usage (GET for reads, POST for creates)
- Meaningful status codes (not just 200 for everything)
- Error responses include actionable detail
- Pagination for list endpoints
- Input validation at API boundary

## References

- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [JSON:API Specification](https://jsonapi.org/)
- [RFC 7807 - Problem Details for HTTP APIs](https://tools.ietf.org/html/rfc7807)

---

*Last Updated: 2026-02-10*
