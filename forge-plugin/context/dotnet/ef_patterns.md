---
id: "dotnet/ef_patterns"
domain: dotnet
title: "Entity Framework Patterns"
type: framework
estimatedTokens: 1250
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Critical Anti-Patterns"
    estimatedTokens: 81
    keywords: [critical, anti-patterns]
  - name: "DbContext Lifetime"
    estimatedTokens: 63
    keywords: [dbcontext, lifetime]
  - name: "N+1 Query Problem"
    estimatedTokens: 89
    keywords: [query, problem]
  - name: "Query Optimization"
    estimatedTokens: 84
    keywords: [query, optimization]
  - name: "SQL Injection Prevention"
    estimatedTokens: 42
    keywords: [sql, injection, prevention]
  - name: "Migrations"
    estimatedTokens: 62
    keywords: [migrations]
  - name: "Relationships"
    estimatedTokens: 45
    keywords: [relationships]
  - name: "Transactions"
    estimatedTokens: 27
    keywords: [transactions]
  - name: "Concurrency"
    estimatedTokens: 59
    keywords: [concurrency]
  - name: "Common Detection Patterns"
    estimatedTokens: 61
    keywords: [detection, patterns]
  - name: "EF Core Checklist"
    estimatedTokens: 52
    keywords: [core, checklist]
  - name: "Official Resources"
    estimatedTokens: 22
    keywords: [official, resources]
tags: [dotnet, entity-framework, dbcontext, queries, n-plus-one, migrations, concurrency]
---

# Entity Framework Patterns

Quick reference for Entity Framework Core and EF6 best practices. For detailed examples, see [EF Core documentation](https://learn.microsoft.com/en-us/ef/core/).

---

## Critical Anti-Patterns

| Anti-Pattern | Detection | Impact | Fix | Learn More |
|--------------|-----------|--------|-----|------------|
| **DbContext as Singleton** | `AddSingleton<DbContext>()` | 🔴 Not thread-safe | Use `AddDbContext` (Scoped) | [DbContext lifetime](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#dbcontext-in-dependency-injection) |
| **N+1 queries** | Loop accessing nav properties | 🔴 Performance | Use `.Include()` or `.Select()` | [Loading related data](https://learn.microsoft.com/en-us/ef/core/querying/related-data/) |
| **SQL injection** | String interpolation in `FromSqlRaw` | 🔴 Security | Use `FromSqlInterpolated` | [Raw SQL](https://learn.microsoft.com/en-us/ef/core/querying/sql-queries) |
| **Loading then projecting** | `.ToList()` then `.Select()` | 🟠 Performance | Project in database | [Projections](https://learn.microsoft.com/en-us/ef/core/querying/how-query-works) |
| **Tracking for read-only** | Default tracking for displays | 🟡 Memory | Use `.AsNoTracking()` | [No-tracking queries](https://learn.microsoft.com/en-us/ef/core/querying/tracking) |

---

## DbContext Lifetime

| Lifetime | Thread-Safe? | Use When |
|----------|--------------|----------|
| **Scoped** (✅ CORRECT) | ✅ Yes (per-request instance) | Web apps, per-request operations |
| **Transient** | ✅ Yes | Short-lived operations |
| **Singleton** (❌ NEVER) | ❌ NO | NEVER - not thread-safe |

```csharp
// ✅ Correct - Scoped (default with AddDbContext)
services.AddDbContext<AppDbContext>();

// ❌ CRITICAL - Singleton
services.AddSingleton<AppDbContext>();  // NOT THREAD-SAFE!

// ✅ Manual creation with using
using var context = new AppDbContext(options);
return await context.Products.ToListAsync();
```

[DbContext lifetime](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#dbcontext-in-dependency-injection)

---

## N+1 Query Problem

| Solution | When to Use | SQL Queries |
|----------|-------------|-------------|
| `.Include()` | Need full entities | 1 (with JOIN) |
| `.Select()` projection | Need specific fields | 1 (optimized SELECT) |
| `.AsSplitQuery()` | Multiple collections | 1 per Include |

```csharp
// ❌ N+1 problem (1 + N queries)
var orders = await _context.Orders.ToListAsync();  // 1 query
foreach (var order in orders)
{
    var customerName = order.Customer.Name;  // N queries!
}

// ✅ Include (single query with JOIN)
var orders = await _context.Orders
    .Include(o => o.Customer)
    .ToListAsync();

// ✅ Projection (most efficient)
var orders = await _context.Orders
    .Select(o => new OrderDto
    {
        OrderId = o.Id,
        CustomerName = o.Customer.Name
    })
    .ToListAsync();
```

[Loading related data](https://learn.microsoft.com/en-us/ef/core/querying/related-data/)

---

## Query Optimization

| Pattern | Bad | Good | Impact |
|---------|-----|------|--------|
| **Eager loading** | Loop accessing nav props | `.Include()` | 🔴 Critical |
| **Projection** | Load full entity for DTO | `.Select()` in DB | 🟠 High |
| **No-tracking** | Tracking for read-only | `.AsNoTracking()` | 🟡 Medium |
| **Filter early** | `.ToList().Where()` | `.Where().ToList()` | 🟠 High |

```csharp
// ✅ AsNoTracking for read-only
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();

// ✅ Projection loads only needed columns
var summary = await _context.Products
    .Select(p => new { p.Id, p.Name, p.Price })
    .ToListAsync();
// SQL: SELECT Id, Name, Price (not SELECT *)
```

[Performance](https://learn.microsoft.com/en-us/ef/core/performance/)

---

## SQL Injection Prevention

```csharp
// ❌ CRITICAL - SQL injection
_context.Products.FromSqlRaw($"SELECT * FROM Products WHERE Name = '{name}'");

// ✅ FromSqlInterpolated (auto-parameterized)
_context.Products.FromSqlInterpolated($"SELECT * FROM Products WHERE Name = {name}");

// ✅ FromSqlRaw with parameters
_context.Products.FromSqlRaw("SELECT * FROM Products WHERE Name = {0}", name);

// ✅ Best - use LINQ
_context.Products.Where(p => p.Name == name);
```

[Raw SQL queries](https://learn.microsoft.com/en-us/ef/core/querying/sql-queries)

---

## Migrations

| Command | Purpose |
|---------|---------|
| `dotnet ef migrations add <Name>` | Create migration |
| `dotnet ef database update` | Apply migrations |
| `dotnet ef migrations remove` | Remove last migration |
| `dotnet ef database drop` | Drop database |

```csharp
// ✅ Seed data in OnModelCreating
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Category>().HasData(
        new Category { Id = 1, Name = "Electronics" },
        new Category { Id = 2, Name = "Books" }
    );
}
```

[Migrations](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/)

---

## Relationships

| Relationship | Configuration Method |
|--------------|---------------------|
| **One-to-Many** | `.HasOne().WithMany().HasForeignKey()` |
| **Many-to-Many** | Auto (EF Core 5+) or explicit join entity |
| **One-to-One** | `.HasOne().WithOne()` |

```csharp
// ✅ One-to-Many
modelBuilder.Entity<Order>()
    .HasOne(o => o.Customer)
    .WithMany(c => c.Orders)
    .HasForeignKey(o => o.CustomerId)
    .OnDelete(DeleteBehavior.Restrict);

// ✅ Many-to-Many (EF Core 5+)
modelBuilder.Entity<Student>()
    .HasMany(s => s.Courses)
    .WithMany(c => c.Students);
```

[Relationships](https://learn.microsoft.com/en-us/ef/core/modeling/relationships)

---

## Transactions

```csharp
// ✅ Explicit transaction
using var transaction = await _context.Database.BeginTransactionAsync();
try
{
    _context.Orders.Add(order);
    await _context.SaveChangesAsync();

    await UpdateInventoryAsync(order.ProductId, order.Quantity);

    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}

// Note: SaveChangesAsync is automatically transactional
```

[Transactions](https://learn.microsoft.com/en-us/ef/core/saving/transactions)

---

## Concurrency

```csharp
// ✅ Add RowVersion for optimistic concurrency
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }

    [Timestamp]
    public byte[] RowVersion { get; set; }
}

// Handle conflicts
try
{
    await _context.SaveChangesAsync();
}
catch (DbUpdateConcurrencyException ex)
{
    var entry = ex.Entries.Single();
    var databaseValues = await entry.GetDatabaseValuesAsync();

    if (databaseValues == null)
    {
        // Entity was deleted
    }
    else
    {
        // Reload and retry
        entry.OriginalValues.SetValues(databaseValues);
    }
}
```

[Concurrency conflicts](https://learn.microsoft.com/en-us/ef/core/saving/concurrency)

---

## Common Detection Patterns

```csharp
// ❌ DbContext as Singleton
services.AddSingleton<DbContext>()

// ❌ N+1 queries
foreach (var order in orders)
    var customer = order.Customer.Name;  // Query per iteration

// ❌ SQL injection
FromSqlRaw($"... WHERE Name = '{name}'")

// ❌ Loading then filtering
.ToList().Where()

// ❌ Tracking for read-only
var products = _context.Products.ToList();  // Change tracking enabled

// ❌ No using for manual DbContext
var context = new AppDbContext();
// Missing using

// ❌ Cartesian explosion
.Include(o => o.Items)
.Include(o => o.Payments)
// Without AsSplitQuery
```

---

## EF Core Checklist

- ✅ DbContext is Scoped (via `AddDbContext`)
- ✅ `.Include()` or `.Select()` to prevent N+1
- ✅ `.AsNoTracking()` for read-only queries
- ✅ `.Select()` projection for DTOs (not full entities)
- ✅ Filter with `.Where()` before `.ToList()`
- ✅ Parameterized queries (no SQL injection)
- ✅ `[Timestamp]` for concurrency-sensitive data
- ✅ `.AsSplitQuery()` for multiple collection includes
- ✅ Migrations for schema changes
- ✅ Transactions for multi-step operations

---

## Official Resources

- **EF Core Documentation**: https://learn.microsoft.com/en-us/ef/core/
- **Performance**: https://learn.microsoft.com/en-us/ef/core/performance/
- **Querying data**: https://learn.microsoft.com/en-us/ef/core/querying/
- **Saving data**: https://learn.microsoft.com/en-us/ef/core/saving/
- **Migrations**: https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/

---

**Version**: 0.3.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
