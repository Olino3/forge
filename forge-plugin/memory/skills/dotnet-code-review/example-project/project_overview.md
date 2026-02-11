# Project Overview: MyEcommerceApp

**Last Updated**: 2025-01-14

---

## Basic Information

- **Project Name**: MyEcommerceApp
- **Type**: ASP.NET Core Web API
- **Framework**: .NET 8
- **Repository**: https://github.com/example/my-ecommerce-app
- **Team Size**: 5 developers
- **Started**: 2023-06

---

## Architecture

### Overall Pattern
Clean Architecture with CQRS

```
src/
├── Domain/              (Entities, Value Objects, Domain Events)
├── Application/         (Use Cases, DTOs, Interfaces)
│   └── Features/
│       ├── Products/
│       │   ├── Commands/
│       │   └── Queries/
│       └── Orders/
│           ├── Commands/
│           └── Queries/
├── Infrastructure/      (EF Core, External Services, Email, etc.)
└── WebApi/             (Controllers, Middleware, Startup)
```

### Key Design Decisions
1. **CQRS** using MediatR - All business logic through commands/queries
2. **Domain Events** - For cross-aggregate communication
3. **Repository Pattern** - Abstraction over EF Core
4. **Specification Pattern** - For complex queries

---

## Technology Stack

### Core Framework
- **.NET 8** (upgraded from .NET 6 in 2024-09)
- **ASP.NET Core 8** Web API
- **C# 12** (using modern features: primary constructors, collection expressions)

### Data Access
- **Entity Framework Core 8.0** — Primary ORM, SQL Server 2022
- **Migrations** managed via EF Core CLI

### Patterns & Libraries
- **MediatR 12.0** — CQRS, **FluentValidation 11.0** — validation
- **AutoMapper 12.0** — mapping, **Serilog** — logging (Seq + App Insights)
- **Polly** — resilience and transient fault handling

### Authentication & Authorization
- **ASP.NET Core Identity** + **JWT Bearer Tokens** (15 min expiry, 7 day refresh)
- **Role-based**: Admin, Customer, Guest + custom claims permissions

### External Services
- **SendGrid** (email), **Stripe** (payments), **Azure Blob Storage** (images), **Azure Service Bus** (async events)

---

## Testing

- **xUnit 2.6** + **Moq 4.20** + **FluentAssertions 6.12**
- **Testcontainers** (integration), **WebApplicationFactory** (API)
- Coverage target: 80%, current: ~75%

---

## API Structure

- **URL versioning**: `/api/v1/...`, `/api/v2/...`
- **Endpoints**: products, orders, customers, auth, cart
- Standard response wrapper + Problem Details (RFC 7807) + HATEOAS

---

## Database Schema

### Key Tables
- **Products** - Product catalog (5000+ rows)
- **Orders** - Customer orders (50,000+ rows)
- **OrderItems** - Order line items
- **Customers** - Customer accounts
- **Inventory** - Stock levels
- **Categories** - Product categories

### Relationships
- Products → Categories (many-to-one)
- Orders → Customers (many-to-one)
- Orders → OrderItems (one-to-many)
- OrderItems → Products (many-to-one)

---

## Performance & Caching

- **Response targets**: GET /products < 100ms, POST /orders < 500ms, payments < 2s
- **Caching**: IMemoryCache (product catalog, 5 min), Redis (sessions, carts), Response caching (1 min)
- **DB optimization**: Indexes, compiled queries, AsNoTracking for reads, batch operations

---

## Security

- **Auth flow**: Login → Identity validation → JWT (15 min) + refresh token (7 days)
- **Policies**: IsAdmin, IsCustomer, CanEditOrder (resource-based)
- **Headers**: HSTS, CSP, X-Frame-Options: DENY, X-Content-Type-Options: nosniff

---

## CI/CD

- **Pipeline**: Restore → Build → Unit tests → Integration tests → Coverage → Roslyn analyzers
- **Deploy**: Azure App Service, Azure SQL, blue-green deployment, App Insights + Seq

---

## Configuration

- Secrets in Azure Key Vault (JWT, SendGrid, Stripe)
- Environments: Dev (LocalDB, User Secrets), Staging/Prod (Azure SQL, Key Vault)

---

## Development Practices

- Nullable reference types, file-scoped namespaces, primary constructors (C# 12)
- Async/await everywhere, CancellationToken propagation mandatory
- Git: protected main, feature branches, PRs with 2 approvals, squash merge

---

## Technical Debt

1. Payment processing — needs distributed transaction pattern
2. Order cancellation — complex state machine
3. Inventory — race conditions under high load
4. Legacy controllers bypassing CQRS

---

## Team & Review Focus

- **Team**: Alice (lead), Bob (payments), Charlie (API), Diana (QA), Eve (DevOps)
- **Review focus**: async/await, N+1 queries, DI lifetimes, CancellationToken, security

---

**Last Updated**: 2025-01-14 by Alice (Lead Developer)
