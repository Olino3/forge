# Django Skill Examples

This file provides sample usage scenarios for the `django` skill.

---

## Example 1: Orders API with Django REST Framework

### Scenario
An e-commerce team needs a new Orders API with filtering and pagination.

### User Prompt
"Design Django REST Framework endpoints for orders with filters for status and date range."

### Skill Execution
- **Step 1**: Confirm Django 4.2 + DRF, API-only, PostgreSQL, target endpoints.
- **Step 2**: Load memory for `shop-api` (none found).
- **Step 3**: Load Python domain index and Django-specific context.
- **Step 4**: Review existing apps for Orders, Users, Inventory.
- **Step 5**: Recommend serializers, viewsets, permissions, and filter setup.
- **Step 6**: Output report to `/claudedocs/django_shop-api_2026-02-12.md`.

### Generated Output
```markdown
# Django Guidance - shop-api

## Orders API Plan
- Create `OrderSerializer` with nested read-only `OrderItem` data
- Use `ModelViewSet` with `DjangoFilterBackend` for `status` and `created_at`
- Add `OrderingFilter` for `created_at` and `total`
- Pagination: `PageNumberPagination` (page size 25)

## Security & Permissions
- Require `IsAuthenticated`
- Add `IsOrderOwner` custom permission for detail routes
```

---

## Example 2: Fix N+1 Queries in Product Listing

### Scenario
The product list endpoint is slow due to N+1 queries.

### User Prompt
"Our /products endpoint is slow. Diagnose and propose Django ORM fixes."

### Skill Execution
- **Step 1**: Confirm DRF viewset and product/category relations.
- **Step 2**: Load memory; note prior caching decisions.
- **Step 3**: Load Django ORM optimization context.
- **Step 4**: Inspect queryset usage and serializer relations.
- **Step 5**: Recommend `select_related`, `prefetch_related`, and caching.
- **Step 6**: Output remediation steps to `/claudedocs/django_catalog_2026-02-12.md`.

### Generated Output
```markdown
# Django Guidance - catalog

## Query Optimization
- Replace `Product.objects.all()` with:
  `Product.objects.select_related("category").prefetch_related("tags")`
- Add DB indexes on `category_id` and `is_active`

## Caching
- Cache the product list for 5 minutes using per-view caching
- Invalidate cache on product update via signals
```

---

## Example 3: Secure Custom Authentication Flow

### Scenario
A team needs to implement a custom user model and JWT authentication.

### User Prompt
"Help us migrate to a custom user model and secure JWT auth."

### Skill Execution
- **Step 1**: Confirm current auth backend, migration window, and DRF usage.
- **Step 2**: Load memory for auth conventions.
- **Step 3**: Load Django auth and security context.
- **Step 4**: Review existing models and settings.
- **Step 5**: Provide migration plan and JWT security guidance.
- **Step 6**: Output plan to `/claudedocs/django_auth_2026-02-12.md`.

### Generated Output
```markdown
# Django Guidance - auth

## Custom User Model Migration
- Create `User` model extending `AbstractBaseUser`
- Set `AUTH_USER_MODEL = "accounts.User"` before first migration
- Implement `UserManager` with `create_user`/`create_superuser`

## JWT Security
- Use `djangorestframework-simplejwt` with rotating refresh tokens
- Set access token TTL to 15 minutes
- Enforce `IsAuthenticated` and role-based permissions
```
