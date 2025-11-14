# LINQ Optimization Patterns

This file documents LINQ query patterns, optimization strategies, and common pitfalls for efficient data processing in .NET.

## Purpose

Load this file when reviewing:
- LINQ queries (.Where, .Select, .OrderBy, etc.)
- IEnumerable and IQueryable usage
- Entity Framework query performance
- Data processing pipelines

---

## 1. Deferred Execution

### 1.1 Understanding Deferred Execution

**Critical**: LINQ queries don't execute until enumerated.

```csharp
// ✅ Understanding deferred execution
var query = products.Where(p => p.Price > 100); // Query NOT executed yet
Console.WriteLine("Query defined");
var results = query.ToList(); // NOW query executes
Console.WriteLine($"Found {results.Count} products");

// ❌ Assuming immediate execution
var expensiveProducts = products.Where(p => p.Price > 100); // NOT executed
Console.WriteLine(expensiveProducts.Count()); // Executes query
Console.WriteLine(expensiveProducts.First()); // Executes query AGAIN!
```

### 1.2 Force Execution with ToList/ToArray

**Best Practice**: Call `.ToList()` or `.ToArray()` when you need immediate execution.

```csharp
// ✅ Good - execute once and cache
var expensiveProducts = products.Where(p => p.Price > 100).ToList();
Console.WriteLine(expensiveProducts.Count); // No re-execution
Console.WriteLine(expensiveProducts.First()); // No re-execution

// ❌ Bad - multiple enumerations
var query = products.Where(p => p.Price > 100);
foreach (var product in query) { } // Executes
var count = query.Count(); // Executes again!
```

---

## 2. Multiple Enumeration (Critical Issue)

### 2.1 The Problem

**Rule**: Don't enumerate IEnumerable<T> multiple times.

```csharp
// ❌ CRITICAL - multiple enumeration
public void ProcessProducts(IEnumerable<Product> products)
{
    if (products.Any()) // Enumeration 1
    {
        Console.WriteLine($"Processing {products.Count()} products"); // Enumeration 2
        
        foreach (var product in products) // Enumeration 3
        {
            Console.WriteLine(product.Name);
        }
    }
}
// If products comes from a database query, this hits the database 3 times!

// ✅ Good - single enumeration
public void ProcessProducts(IEnumerable<Product> products)
{
    var productList = products.ToList(); // Enumerate once
    
    if (productList.Any())
    {
        Console.WriteLine($"Processing {productList.Count} products");
        
        foreach (var product in productList)
        {
            Console.WriteLine(product.Name);
        }
    }
}
```

### 2.2 Detection

**Tool**: Use analyzers to detect multiple enumerations.

```csharp
// ❌ Bad - multiple enumeration with EF
public async Task<decimal> CalculateAverageAsync(IQueryable<Product> products)
{
    var count = await products.CountAsync(); // Database query 1
    var sum = await products.SumAsync(p => p.Price); // Database query 2
    return sum / count;
}

// ✅ Good - single query
public async Task<decimal> CalculateAverageAsync(IQueryable<Product> products)
{
    return await products.AverageAsync(p => p.Price); // Single database query
}
```

---

## 3. IEnumerable vs IQueryable

### 3.1 Understanding the Difference

**Critical**: IQueryable translates to database queries, IEnumerable executes in memory.

```csharp
// ✅ Good - filtering in database (IQueryable)
public async Task<List<Product>> GetExpensiveProductsAsync()
{
    return await _dbContext.Products
        .Where(p => p.Price > 100) // SQL: WHERE Price > 100
        .ToListAsync();
}
// SQL: SELECT * FROM Products WHERE Price > 100

// ❌ Bad - filtering in memory (IEnumerable)
public async Task<List<Product>> GetExpensiveProductsAsync()
{
    var products = await _dbContext.Products.ToListAsync(); // Loads ALL products
    return products.Where(p => p.Price > 100).ToList(); // Filters in memory
}
// SQL: SELECT * FROM Products (loads entire table!)
```

### 3.2 Breaking IQueryable Chain

**Critical**: Don't break the IQueryable chain with methods that return IEnumerable.

```csharp
// ❌ CRITICAL - breaking IQueryable chain
public async Task<List<Product>> GetProductsAsync()
{
    return await _dbContext.Products
        .AsEnumerable() // Breaks IQueryable, switches to LINQ to Objects
        .Where(p => p.Price > 100) // Executes in memory!
        .ToListAsync(); // Compiler error - ToListAsync requires IQueryable
}

// ✅ Good - maintain IQueryable chain
public async Task<List<Product>> GetProductsAsync()
{
    return await _dbContext.Products
        .Where(p => p.Price > 100) // Translates to SQL
        .ToListAsync();
}
```

---

## 4. Select and Projection

### 4.1 Select Early

**Best Practice**: Project to DTOs as early as possible.

```csharp
// ✅ Good - project in database
public async Task<List<ProductDto>> GetProductsAsync()
{
    return await _dbContext.Products
        .Select(p => new ProductDto
        {
            Id = p.Id,
            Name = p.Name,
            Price = p.Price
        })
        .ToListAsync();
}
// SQL: SELECT Id, Name, Price FROM Products

// ❌ Bad - project after loading entire entity
public async Task<List<ProductDto>> GetProductsAsync()
{
    var products = await _dbContext.Products.ToListAsync(); // Loads all columns
    return products.Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name,
        Price = p.Price
    }).ToList();
}
// SQL: SELECT * FROM Products (unnecessary data transfer)
```

### 4.2 Anonymous Types for Internal Use

**Best Practice**: Use anonymous types when DTOs aren't needed.

```csharp
// ✅ Good - anonymous type projection
var summary = await _dbContext.Products
    .GroupBy(p => p.CategoryId)
    .Select(g => new
    {
        CategoryId = g.Key,
        Count = g.Count(),
        TotalValue = g.Sum(p => p.Price)
    })
    .ToListAsync();
```

---

## 5. Where Clauses

### 5.1 Filter Early

**Best Practice**: Apply filters before other operations.

```csharp
// ✅ Good - filter first
var products = await _dbContext.Products
    .Where(p => p.IsActive) // Filter early
    .Where(p => p.Price > 100)
    .OrderBy(p => p.Name)
    .ToListAsync();

// ❌ Bad - filter after sorting
var products = await _dbContext.Products
    .OrderBy(p => p.Name) // Sorts all products
    .Where(p => p.IsActive) // Then filters
    .Where(p => p.Price > 100)
    .ToListAsync();
```

### 5.2 Combine Where Clauses

**Best Practice**: Combine multiple Where clauses with &&.

```csharp
// ✅ Good - single WHERE clause
var products = await _dbContext.Products
    .Where(p => p.IsActive && p.Price > 100 && p.CategoryId == 5)
    .ToListAsync();
// SQL: WHERE IsActive = 1 AND Price > 100 AND CategoryId = 5

// ✅ Also good - multiple Where clauses (same result)
var products = await _dbContext.Products
    .Where(p => p.IsActive)
    .Where(p => p.Price > 100)
    .Where(p => p.CategoryId == 5)
    .ToListAsync();
// SQL: WHERE IsActive = 1 AND Price > 100 AND CategoryId = 5
```

---

## 6. First vs Single

### 6.1 Understanding the Difference

**Rule**: Use appropriate method based on expected results.

```csharp
// ✅ Good - First when expecting multiple matches
var product = await _dbContext.Products
    .Where(p => p.CategoryId == 5)
    .OrderBy(p => p.Price)
    .FirstAsync(); // Returns first, throws if none

// ✅ Good - Single when expecting exactly one
var product = await _dbContext.Products
    .SingleAsync(p => p.Id == 123); // Throws if 0 or > 1

// ✅ Good - FirstOrDefault when expecting 0 or more
var product = await _dbContext.Products
    .Where(p => p.CategoryId == 5)
    .FirstOrDefaultAsync(); // Returns null if none

// ❌ Bad - Single on non-unique results
var product = await _dbContext.Products
    .SingleAsync(p => p.CategoryId == 5); // Exception if multiple products
```

### 6.2 Performance Consideration

**Best Practice**: First is more efficient than Single.

```csharp
// ✅ Good - First with filter
var product = await _dbContext.Products
    .FirstAsync(p => p.Id == 123);
// SQL: SELECT TOP(1) * FROM Products WHERE Id = 123

// ❌ Less efficient - Single
var product = await _dbContext.Products
    .SingleAsync(p => p.Id == 123);
// SQL: SELECT * FROM Products WHERE Id = 123 (fetches all to verify single)
```

---

## 7. OrderBy and Sorting

### 7.1 Ordering

**Best Practice**: Apply ordering after filtering.

```csharp
// ✅ Good - filter then order
var products = await _dbContext.Products
    .Where(p => p.IsActive)
    .OrderBy(p => p.Name)
    .ThenBy(p => p.Price)
    .ToListAsync();

// ❌ Bad - order before filter
var products = await _dbContext.Products
    .OrderBy(p => p.Name) // Orders all products
    .Where(p => p.IsActive) // Then filters
    .ToListAsync();
```

### 7.2 Avoid Client-Side Ordering

**Critical**: Don't order after materialization.

```csharp
// ❌ CRITICAL - client-side ordering
var products = await _dbContext.Products
    .Where(p => p.IsActive)
    .ToListAsync(); // Materializes

var sorted = products.OrderBy(p => p.Name).ToList(); // Sorts in memory

// ✅ Good - database ordering
var products = await _dbContext.Products
    .Where(p => p.IsActive)
    .OrderBy(p => p.Name)
    .ToListAsync();
```

---

## 8. Join Operations

### 8.1 Use Navigation Properties

**Best Practice**: Prefer Include over manual joins.

```csharp
// ✅ Good - Include navigation property
var orders = await _dbContext.Orders
    .Include(o => o.Customer)
    .Where(o => o.OrderDate > cutoffDate)
    .ToListAsync();

// ❌ Bad - manual join when navigation exists
var orders = await _dbContext.Orders
    .Join(_dbContext.Customers,
        o => o.CustomerId,
        c => c.Id,
        (o, c) => new { Order = o, Customer = c })
    .Where(x => x.Order.OrderDate > cutoffDate)
    .ToListAsync();
```

### 8.2 Explicit Join

**Best Practice**: Use Join when navigation properties don't exist.

```csharp
// ✅ Good - explicit join
var result = await _dbContext.Products
    .Join(_dbContext.Categories,
        p => p.CategoryId,
        c => c.Id,
        (p, c) => new ProductWithCategory
        {
            ProductName = p.Name,
            CategoryName = c.Name,
            Price = p.Price
        })
    .ToListAsync();
```

---

## 9. GroupBy

### 9.1 Server-Side Grouping

**Best Practice**: Group in database, not in memory.

```csharp
// ✅ Good - database grouping
var summary = await _dbContext.Orders
    .GroupBy(o => o.CustomerId)
    .Select(g => new
    {
        CustomerId = g.Key,
        OrderCount = g.Count(),
        TotalSpent = g.Sum(o => o.Total)
    })
    .ToListAsync();
// SQL: SELECT CustomerId, COUNT(*), SUM(Total) FROM Orders GROUP BY CustomerId

// ❌ Bad - client-side grouping
var orders = await _dbContext.Orders.ToListAsync();
var summary = orders
    .GroupBy(o => o.CustomerId)
    .Select(g => new
    {
        CustomerId = g.Key,
        OrderCount = g.Count(),
        TotalSpent = g.Sum(o => o.Total)
    })
    .ToList();
```

---

## 10. Any, All, Contains

### 10.1 Existence Checks

**Best Practice**: Use Any instead of Count for existence checks.

```csharp
// ✅ Good - Any (efficient)
if (await _dbContext.Products.AnyAsync(p => p.Price > 1000))
{
    // Has expensive products
}
// SQL: SELECT CASE WHEN EXISTS(SELECT 1 FROM Products WHERE Price > 1000) THEN 1 ELSE 0 END

// ❌ Bad - Count > 0 (inefficient)
if (await _dbContext.Products.CountAsync(p => p.Price > 1000) > 0)
{
    // Has expensive products
}
// SQL: SELECT COUNT(*) FROM Products WHERE Price > 1000
```

### 10.2 Contains with Collections

**Best Practice**: Use Contains for IN queries.

```csharp
// ✅ Good - Contains translates to SQL IN
var categoryIds = new[] { 1, 2, 3 };
var products = await _dbContext.Products
    .Where(p => categoryIds.Contains(p.CategoryId))
    .ToListAsync();
// SQL: WHERE CategoryId IN (1, 2, 3)
```

---

## 11. Take and Skip (Pagination)

### 11.1 Efficient Pagination

**Best Practice**: Use Skip and Take for pagination.

```csharp
// ✅ Good - pagination
public async Task<List<Product>> GetPageAsync(int page, int pageSize)
{
    return await _dbContext.Products
        .OrderBy(p => p.Id) // Must order for consistent pagination
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();
}
// SQL: SELECT * FROM Products ORDER BY Id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY
```

---

## 12. Parallel LINQ (PLINQ)

### 12.1 When to Use PLINQ

**Best Practice**: Use PLINQ for CPU-intensive in-memory operations.

```csharp
// ✅ Good - PLINQ for CPU-bound work
var results = largeCollection
    .AsParallel()
    .Where(item => IsComplexCondition(item)) // CPU-intensive
    .Select(item => ProcessItem(item)) // CPU-intensive
    .ToList();

// ❌ Bad - PLINQ for I/O
var products = await _dbContext.Products
    .AsParallel() // WRONG - doesn't work with EF
    .Where(p => p.Price > 100)
    .ToListAsync();
```

---

## LINQ Optimization Checklist

1. **Deferred Execution**: ✅ Understand when queries execute
2. **Multiple Enumeration**: ✅ Call ToList() to avoid re-execution
3. **IQueryable**: ✅ Keep queries translatable to SQL
4. **Select Early**: ✅ Project to DTOs in database
5. **Filter Early**: ✅ Apply Where before other operations
6. **First vs Single**: ✅ Use appropriate method
7. **OrderBy**: ✅ Order after filtering
8. **Navigation Properties**: ✅ Use Include over manual joins
9. **GroupBy**: ✅ Group in database, not memory
10. **Any vs Count**: ✅ Use Any for existence checks

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
