# .NET Core Skill Examples

This file provides sample usage scenarios for the `dotnet-core` skill.

---

## Example 1: Layered API Architecture

### Scenario
A minimal API needs to evolve into a layered architecture with services and repositories.

### User Prompt
"Refactor our .NET 8 minimal API into a layered architecture."

### Skill Execution
- **Step 1**: Confirm .NET 8, existing endpoints, and hosting target.
- **Step 2**: Load memory for `billing-api`.
- **Step 3**: Load dotnet domain context and architecture patterns.
- **Step 4**: Inspect current Program.cs and route handlers.
- **Step 5**: Recommend controller/service/repository split.
- **Step 6**: Output to `/claudedocs/dotnet-core_billing-api_2026-02-12.md`.

### Generated Output
```markdown
# .NET Core Guidance - billing-api

## Target Architecture
- API layer: Controllers with DTOs
- Application layer: Services for business logic
- Data layer: Repositories with EF Core

## Migration Steps
1. Move handlers into `Controllers/InvoicesController`
2. Add `InvoiceService` for business rules
3. Create `InvoiceRepository` with EF Core
```

---

## Example 2: JWT Authentication with Policies

### Scenario
The API needs JWT auth and fine-grained authorization.

### User Prompt
"Add JWT auth and policy-based authorization for admin-only routes."

### Skill Execution
- **Step 1**: Confirm auth provider and token format.
- **Step 2**: Load memory for security conventions.
- **Step 3**: Load dotnet security context.
- **Step 4**: Review current middleware pipeline.
- **Step 5**: Provide policy setup and validation guidance.
- **Step 6**: Output to `/claudedocs/dotnet-core_auth_2026-02-12.md`.

### Generated Output
```markdown
# .NET Core Guidance - auth

## JWT Setup
- Configure `AddAuthentication().AddJwtBearer(...)`
- Validate issuer, audience, and signing key

## Policies
- Add policy `RequireAdmin` with role claim
- Apply `[Authorize(Policy = "RequireAdmin")]` to admin controllers
```

---

## Example 3: Performance & Caching Strategy

### Scenario
A high-traffic endpoint needs caching and health checks.

### User Prompt
"Improve performance for our /reports endpoint and add health checks."

### Skill Execution
- **Step 1**: Confirm SLA and current latency.
- **Step 2**: Load memory for infrastructure patterns.
- **Step 3**: Load dotnet performance context.
- **Step 4**: Inspect current controller and data access.
- **Step 5**: Recommend caching and health probe setup.
- **Step 6**: Output to `/claudedocs/dotnet-core_reports_2026-02-12.md`.

### Generated Output
```markdown
# .NET Core Guidance - reports

## Caching
- Add IMemoryCache with 5-minute TTL
- Use cache-aside in ReportsService

## Health Checks
- `AddHealthChecks().AddSqlServer(...)`
- Map `/health` endpoint for readiness probes
```
