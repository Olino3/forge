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
- **Entity Framework Core 8.0** - Primary ORM
- **SQL Server 2022** - Production database
- **Connection Pooling** enabled (default)
- **Migrations** managed via EF Core CLI

### Patterns & Libraries
- **MediatR 12.0** - CQRS pattern implementation
- **FluentValidation 11.0** - Command/Query validation
- **AutoMapper 12.0** - DTO mapping
- **Serilog** - Structured logging (writes to Seq and Azure Application Insights)
- **Polly** - Resilience and transient fault handling

### Authentication & Authorization
- **ASP.NET Core Identity** - User management
- **JWT Bearer Tokens** - API authentication
- **Role-based authorization** - Admin, Customer, Guest roles
- **Custom claims** - Permissions system

### External Services
- **SendGrid** - Email notifications
- **Stripe** - Payment processing
- **Azure Blob Storage** - Product images
- **Azure Service Bus** - Async event processing

---

## Testing

### Frameworks
- **xUnit 2.6** - Test framework
- **Moq 4.20** - Mocking library
- **FluentAssertions 6.12** - Assertion library
- **Testcontainers** - Integration tests with real database
- **WebApplicationFactory** - API integration tests

### Test Structure
```
tests/
├── Domain.Tests/        (Domain logic unit tests)
├── Application.Tests/   (Use case unit tests)
├── Infrastructure.Tests/ (Integration tests with Testcontainers)
└── WebApi.Tests/        (API integration tests)
```

### Code Coverage Goal
- **Target**: 80% line coverage
- **Current**: ~75% (as of 2025-01)

---

## API Structure

### Versioning
- **URL versioning**: `/api/v1/products`, `/api/v2/products`
- **Current versions**: v1 (stable), v2 (preview)

### Common Endpoints
```
/api/v1/products         - Product catalog
/api/v1/orders           - Order management
/api/v1/customers        - Customer profiles
/api/v1/auth             - Authentication
/api/v1/cart             - Shopping cart
```

### Response Format
- Standard response wrapper with `success`, `data`, `errors` fields
- Problem Details (RFC 7807) for errors
- HATEOAS links for navigation

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

## Performance Characteristics

### Response Time Goals
- **GET /products**: < 100ms
- **POST /orders**: < 500ms
- **Payment processing**: < 2s

### Caching Strategy
- **IMemoryCache** - Product catalog (5 min expiration)
- **IDistributedCache (Redis)** - User sessions, shopping carts
- **Response caching** - Public product lists (1 min)

### Database Optimization
- **Indexes** on frequently queried columns
- **Compiled queries** for hot paths
- **AsNoTracking** for read-only queries
- **Batch operations** for bulk inserts

---

## Security

### Authentication Flow
1. User logs in with email/password
2. Server validates credentials (ASP.NET Core Identity)
3. JWT token issued (15 min expiration)
4. Refresh token stored (7 day expiration)

### Authorization Policies
- **IsAdmin** - Requires "Admin" role
- **IsCustomer** - Requires "Customer" role
- **CanEditOrder** - Resource-based authorization

### Security Headers
- HTTPS enforcement (HSTS)
- Content Security Policy
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff

---

## CI/CD

### Build Pipeline
1. Restore NuGet packages
2. Build solution
3. Run unit tests
4. Run integration tests (Testcontainers)
5. Code coverage report
6. Static analysis (Roslyn analyzers)

### Deployment
- **Environment**: Azure App Service
- **Database**: Azure SQL Database
- **Process**: Blue-green deployment
- **Monitoring**: Azure Application Insights + Seq

---

## Known Configuration

### appsettings.json Structure
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "..."
  },
  "Jwt": {
    "Issuer": "...",
    "Audience": "...",
    "Secret": "..." // In Azure Key Vault
  },
  "SendGrid": {
    "ApiKey": "..." // In Azure Key Vault
  },
  "Stripe": {
    "SecretKey": "..." // In Azure Key Vault
  }
}
```

### Environment-Specific
- **Development**: SQL Server LocalDB, User Secrets for API keys
- **Staging**: Azure SQL, Azure Key Vault
- **Production**: Azure SQL, Azure Key Vault, SSL enforcement

---

## Development Practices

### Coding Standards
- **Nullable reference types** enabled
- **File-scoped namespaces** (C# 10)
- **Primary constructors** for services (C# 12)
- **Async/await** everywhere (no sync-over-async)
- **CancellationToken** propagation mandatory

### Git Workflow
- **Main branch** protected
- **Feature branches** required
- **Pull requests** mandatory
- **Code reviews** required (2 approvals)
- **Squash merge** strategy

### PR Checklist
1. Tests written and passing
2. Code review completed
3. No warnings or errors
4. Migration scripts (if schema changes)
5. Documentation updated

---

## Pain Points & Technical Debt

### Current Issues
1. **Payment processing** - Not transactional, needs distributed transaction pattern
2. **Order cancellation** - Complex state machine, error-prone
3. **Inventory management** - Race conditions possible under high load
4. **Legacy code** - Some controllers still use direct DbContext access (bypassing CQRS)

### Future Improvements
1. Migrate to Minimal APIs (.NET 8 feature)
2. Add rate limiting (ASP.NET Core 7+ feature)
3. Implement output caching (.NET 7+ feature)
4. Background job processing (Hangfire or Quartz.NET)

---

## Team Notes

### Key Developers
- **Alice** - Lead, architecture decisions
- **Bob** - Payment processing, Stripe integration
- **Charlie** - Frontend integration, API design
- **Diana** - Testing, quality assurance
- **Eve** - DevOps, Azure infrastructure

### Code Review Focus Areas
1. Async/await usage (historically problematic)
2. N+1 query detection (recurring issue)
3. DI lifetime correctness
4. CancellationToken propagation
5. Security (SQL injection, XSS in error messages)

---

**This overview should be updated whenever**:
- Architecture changes
- Major dependencies added/removed
- Team composition changes
- Deployment process changes

---

**Last Updated**: 2025-01-14 by Alice (Lead Developer)
