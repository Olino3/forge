---
id: "dotnet/linq_patterns"
domain: dotnet
title: "LINQ Optimization Patterns"
type: pattern
estimatedTokens: 1200
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 72
    keywords: [anti-patterns]
  - name: "Deferred Execution"
    estimatedTokens: 97
    keywords: [deferred, execution]
  - name: "IEnumerable vs IQueryable"
    estimatedTokens: 72
    keywords: [ienumerable, iqueryable]
  - name: "Query Optimization Patterns"
    estimatedTokens: 39
    keywords: [query, optimization, patterns]
  - name: "Common Performance Issues"
    estimatedTokens: 63
    keywords: [performance, issues]
  - name: "First vs Single vs FirstOrDefault"
    estimatedTokens: 90
    keywords: [first, single, firstordefault]
  - name: "Pagination Best Practices"
    estimatedTokens: 57
    keywords: [pagination]
  - name: "GroupBy Optimization"
    estimatedTokens: 45
    keywords: [groupby, optimization]
  - name: "Common Detection Patterns"
    estimatedTokens: 42
    keywords: [detection, patterns]
  - name: "LINQ Optimization Checklist"
    estimatedTokens: 56
    keywords: [linq, optimization, checklist]
  - name: "Official Resources"
    estimatedTokens: 23
    keywords: [official, resources]

tags: [dotnet, linq, deferred-execution, iqueryable, performance, pagination]
---
# LINQ Optimization Patterns

Quick reference for LINQ query optimization. For detailed examples, see [LINQ documentation](https://learn.microsoft.com/en-us/dotnet/csharp/linq/).

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|--------------|
| **Multiple enumeration** | `IEnumerable` used multiple times | Call `.ToList()` once | [Deferred execution](https://learn.microsoft.com/en-us/dotnet/standard/linq/deferred-execution-lazy-evaluation) |
| **Client-side filtering** | `.ToList()` before `.Where()` | Filter before materializing | [Query syntax](https://learn.microsoft.com/en-us/dotnet/csharp/linq/write-linq-queries) |
| **Count() > 0** | Checking count for existence | Use `.Any()` | [Quantifier operations](https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/quantifier-operations) |
| **Breaking IQueryable** | `.AsEnumerable()` too early | Keep IQueryable for DB queries | [IQueryable](https://learn.microsoft.com/en-us/dotnet/api/system.linq.iqueryable) |
| **Loading then projecting** | `.ToList()` then `.Select()` | Project in database with `.Select()` | [Projection operations](https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/projection-operations) |

---

## Deferred Execution

| Operation | Executes Immediately | Deferred |
|-----------|---------------------|----------|
| `.ToList()`, `.ToArray()`, `.ToDictionary()` | ✅ Yes | |
| `.Count()`, `.Sum()`, `.Average()`, `.Min()`, `.Max()` | ✅ Yes | |
| `.First()`, `.Single()`, `.FirstOrDefault()`, `.SingleOrDefault()` | ✅ Yes | |
| `.Where()`, `.Select()`, `.OrderBy()`, `.GroupBy()` | | ✅ Yes |

```csharp
// ❌ Multiple enumeration (executes 3 times)
var query = products.Where(p => p.Price > 100);
var count = query.Count();        // Execution 1
var first = query.First();        // Execution 2
foreach (var p in query) { }      // Execution 3

// ✅ Single enumeration
var list = products.Where(p => p.Price > 100).ToList();
var count = list.Count;           // No execution
var first = list.First();         // No execution
foreach (var p in list) { }       // No execution
```

[Understanding deferred execution](https://learn.microsoft.com/en-us/dotnet/standard/linq/deferred-execution-lazy-evaluation)

---

## IEnumerable vs IQueryable

| IEnumerable<T> | IQueryable<T> |
|----------------|---------------|
| LINQ to Objects | LINQ to Entities |
| Executes in memory | Translates to SQL |
| Func<T, bool> | Expression<Func<T, bool>> |
| Use for collections | Use for database queries |

```csharp
// ✅ Database filtering (IQueryable)
var products = await _db.Products
    .Where(p => p.Price > 100)  // WHERE Price > 100 in SQL
    .ToListAsync();

// ❌ Memory filtering (IEnumerable)
var products = await _db.Products.ToListAsync();  // SELECT * (all data)
var filtered = products.Where(p => p.Price > 100).ToList();  // Filter in C#
```

[IQueryable vs IEnumerable](https://learn.microsoft.com/en-us/dotnet/api/system.linq.iqueryable)

---

## Query Optimization Patterns

| Pattern | Bad | Good |
|---------|-----|------|
| **Filter early** | `.OrderBy().Where()` | `.Where().OrderBy()` |
| **Project early** | `.ToList().Select()` | `.Select().ToList()` |
| **Existence check** | `.Count() > 0` | `.Any()` |
| **Specific count** | `.Where().Count()` | `.Count(predicate)` |
| **Take before load** | `.ToList().Take(10)` | `.Take(10).ToList()` |

---

## Common Performance Issues

| Issue | Detection | Fix | Perf Impact |
|-------|-----------|-----|-------------|
| **N+1 queries** | Loop with navigation property access | Use `.Include()` or `.Select()` | 🔴 Critical |
| **Loading full entities** | `.ToList()` then project | `.Select()` projection in DB | 🟠 High |
| **Client-side ordering** | `.ToList().OrderBy()` | `.OrderBy().ToList()` | 🟠 High |
| **Client-side filtering** | `.ToList().Where()` | `.Where().ToList()` | 🟠 High |
| **Count instead of Any** | `.Count() > 0` | `.Any()` | 🟡 Medium |

---

## First vs Single vs FirstOrDefault

| Method | Use When | Throws If |
|--------|----------|-----------|
| `.First()` | Expect 1+ results, want first | 0 results |
| `.FirstOrDefault()` | Expect 0+ results, want first | Never |
| `.Single()` | Expect exactly 1 result | 0 or 2+ results |
| `.SingleOrDefault()` | Expect 0 or 1 result | 2+ results |

```csharp
// ✅ First - efficient (generates TOP 1)
var product = await _db.Products.FirstAsync(p => p.Id == id);
// SQL: SELECT TOP(1) * WHERE Id = @id

// ❌ Single - less efficient (loads all matching)
var product = await _db.Products.SingleAsync(p => p.Id == id);
// SQL: SELECT * WHERE Id = @id (fetches all to verify single)
```

[Element operations](https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/element-operations)

---

## Pagination Best Practices

```csharp
// ✅ Database pagination
public async Task<List<Product>> GetPageAsync(int page, int pageSize)
{
    return await _db.Products
        .OrderBy(p => p.Id)           // Must order for consistent results
        .Skip((page - 1) * pageSize)  // OFFSET in SQL
        .Take(pageSize)               // FETCH NEXT in SQL
        .ToListAsync();
}
// SQL: OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY

// ❌ Client-side pagination
var all = await _db.Products.ToListAsync();  // Loads everything
return all.Skip((page - 1) * pageSize).Take(pageSize).ToList();
```

[Paging through query results](https://learn.microsoft.com/en-us/ef/core/querying/pagination)

---

## GroupBy Optimization

```csharp
// ✅ Database grouping
var summary = await _db.Orders
    .GroupBy(o => o.CustomerId)
    .Select(g => new
    {
        CustomerId = g.Key,
        OrderCount = g.Count(),
        TotalSpent = g.Sum(o => o.Total)
    })
    .ToListAsync();
// SQL: SELECT CustomerId, COUNT(*), SUM(Total) GROUP BY CustomerId

// ❌ Client-side grouping
var orders = await _db.Orders.ToListAsync();  // Loads all
var summary = orders.GroupBy(o => o.CustomerId)...
```

[Grouping operations](https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/grouping-operations)

---

## Common Detection Patterns

```csharp
// ❌ Multiple enumeration
IEnumerable<T> query = ...;
query.Count();    // Execution 1
query.First();    // Execution 2

// ❌ Client-side operations
.ToList().Where()
.ToList().OrderBy()
.ToList().Select()
.ToList().Take()

// ❌ Inefficient existence check
.Count() > 0
.Count() >= 1
.Where().Count() > 0

// ❌ Breaking IQueryable
.AsEnumerable().Where()  // Filter in memory

// ❌ Loading then filtering
_db.Products.ToList().Where()
```

---

## LINQ Optimization Checklist

- ✅ Filter with `.Where()` before other operations
- ✅ Project with `.Select()` in database, not after `.ToList()`
- ✅ Use `.Any()` instead of `.Count() > 0`
- ✅ Use `.First()` instead of `.Single()` when appropriate
- ✅ Order after filtering: `.Where().OrderBy()`
- ✅ Materialize once with `.ToList()`, reuse result
- ✅ Use `.Include()` to prevent N+1 queries
- ✅ Keep IQueryable chain for database queries
- ✅ Use `.Skip()/.Take()` for pagination in database

---

## Official Resources

- **LINQ Overview**: https://learn.microsoft.com/en-us/dotnet/csharp/linq/
- **Standard Query Operators**: https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/
- **EF Core Query Performance**: https://learn.microsoft.com/en-us/ef/core/performance/
- **LINQ Performance Tips**: https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/ef/language-reference/query-execution

---

**Version**: 0.3.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
