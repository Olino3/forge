# Entity Framework Patterns

This file documents best practices for Entity Framework Core and Entity Framework 6, including query optimization, relationship management, and performance patterns.

## Purpose

Load this file when reviewing:
- DbContext usage
- LINQ to Entities queries
- Database migrations
- Entity relationships
- Data access patterns
- Repository implementations

---

## 1. DbContext Lifetime Management

### 1.1 DbContext Lifetime (Critical)

**Rule**: DbContext should ALWAYS be **Scoped** in web applications, NEVER Singleton.

```csharp
// ✅ Good - Scoped DbContext
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));
// Default lifetime is Scoped

// ✅ Explicit scoped registration
builder.Services.AddScoped<ApplicationDbContext>();

// ❌ CRITICAL - NEVER use Singleton
builder.Services.AddSingleton<ApplicationDbContext>(); // NOT THREAD-SAFE!
```

**Why**: DbContext is not thread-safe. In web apps, each HTTP request should have its own DbContext instance.

### 1.2 Using Statements for Manual DbContext

**Best Practice**: Use `using` statements when manually creating DbContext instances.

```csharp
// ✅ Good - using statement ensures disposal
public async Task<Product> GetProductAsync(int id)
{
    using var context = new ApplicationDbContext(options);
    return await context.Products.FindAsync(id);
}

// ✅ Traditional using syntax
public async Task<Product> GetProductAsync(int id)
{
    using (var context = new ApplicationDbContext(options))
    {
        return await context.Products.FindAsync(id);
    }
}

// ❌ Bad - DbContext not disposed
public async Task<Product> GetProductAsync(int id)
{
    var context = new ApplicationDbContext(options); // MEMORY LEAK
    return await context.Products.FindAsync(id);
}
```

### 1.3 DbContext in Background Services

**Best Practice**: Create scopes manually in background services.

```csharp
// ✅ Good - manual scope creation
public class DataProcessingService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;

    public DataProcessingService(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            using var scope = _scopeFactory.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
            
            // Use context safely within scope
            await ProcessDataAsync(context);
            
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}

// ❌ Bad - injecting scoped DbContext into singleton
public class DataProcessingService : BackgroundService
{
    private readonly ApplicationDbContext _context; // CAPTIVE DEPENDENCY

    public DataProcessingService(ApplicationDbContext context)
    {
        _context = context; // BUG - context disposed after first use
    }
}
```

---

## 2. Query Patterns

### 2.1 Eager Loading with Include

**Best Practice**: Use `.Include()` to load related data and prevent N+1 queries.

```csharp
// ✅ Good - eager loading prevents N+1
public async Task<List<Order>> GetOrdersWithCustomersAsync()
{
    return await _context.Orders
        .Include(o => o.Customer)
        .ToListAsync();
}

// ✅ Multiple levels with ThenInclude
public async Task<List<Order>> GetOrdersWithDetailsAsync()
{
    return await _context.Orders
        .Include(o => o.Customer)
        .Include(o => o.OrderItems)
            .ThenInclude(oi => oi.Product)
        .ToListAsync();
}

// ❌ Bad - N+1 query problem
public async Task<List<Order>> GetOrdersWithCustomersAsync()
{
    var orders = await _context.Orders.ToListAsync(); // 1 query
    
    foreach (var order in orders)
    {
        // N queries - one per order!
        var customer = order.Customer.Name; // Lazy load or null reference
    }
    
    return orders;
}
```

### 2.2 Projection with Select

**Best Practice**: Use `.Select()` to load only needed data.

```csharp
// ✅ Good - projection loads only necessary columns
public async Task<List<ProductSummaryDto>> GetProductSummariesAsync()
{
    return await _context.Products
        .Select(p => new ProductSummaryDto
        {
            Id = p.Id,
            Name = p.Name,
            Price = p.Price,
            CategoryName = p.Category.Name // No explicit Include needed
        })
        .ToListAsync();
}

// ✅ Projection is more efficient than Include when you don't need full entities
public async Task<List<OrderDto>> GetOrdersAsync()
{
    return await _context.Orders
        .Select(o => new OrderDto
        {
            OrderId = o.Id,
            CustomerName = o.Customer.Name, // Only loads Name column
            Total = o.OrderItems.Sum(oi => oi.Quantity * oi.UnitPrice)
        })
        .ToListAsync();
}

// ❌ Bad - loading full entities when only a few fields are needed
public async Task<List<ProductSummaryDto>> GetProductSummariesAsync()
{
    var products = await _context.Products
        .Include(p => p.Category) // Loads all Category columns
        .ToListAsync(); // Loads all Product columns
    
    return products.Select(p => new ProductSummaryDto
    {
        Id = p.Id,
        Name = p.Name,
        Price = p.Price,
        CategoryName = p.Category.Name
    }).ToList();
}
```

### 2.3 AsNoTracking for Read-Only Queries

**Best Practice**: Use `.AsNoTracking()` for queries that don't need change tracking.

```csharp
// ✅ Good - no tracking for read-only data
public async Task<List<Product>> GetProductsForDisplayAsync()
{
    return await _context.Products
        .AsNoTracking() // Faster, less memory
        .Where(p => p.IsActive)
        .ToListAsync();
}

// ✅ Use AsNoTracking for reports
public async Task<decimal> GetTotalSalesAsync()
{
    return await _context.Orders
        .AsNoTracking()
        .SumAsync(o => o.Total);
}

// ❌ Bad - unnecessary change tracking
public async Task<List<Product>> GetProductsForDisplayAsync()
{
    return await _context.Products
        .Where(p => p.IsActive)
        .ToListAsync(); // Change tracking enabled by default (overhead)
}

// ✅ When to use tracking (default)
public async Task UpdateProductPriceAsync(int productId, decimal newPrice)
{
    var product = await _context.Products.FindAsync(productId); // Tracking needed
    product.Price = newPrice;
    await _context.SaveChangesAsync(); // Saves tracked changes
}
```

### 2.4 Filtering Before Materializing

**Best Practice**: Filter with `.Where()` before calling `.ToList()` or `.ToArray()`.

```csharp
// ✅ Good - filter in database
public async Task<List<Product>> GetActiveProductsAsync()
{
    return await _context.Products
        .Where(p => p.IsActive && p.Stock > 0) // SQL WHERE clause
        .ToListAsync();
}

// ❌ Bad - loads all data then filters in memory
public async Task<List<Product>> GetActiveProductsAsync()
{
    var allProducts = await _context.Products.ToListAsync(); // Loads everything
    return allProducts.Where(p => p.IsActive && p.Stock > 0).ToList(); // Filters in C#
}
```

---

## 3. N+1 Query Problem

### 3.1 Detecting N+1 Queries

**Problem**: Accessing navigation properties in loops causes additional database queries.

```csharp
// ❌ CRITICAL - N+1 problem
public async Task<List<OrderDto>> GetOrdersAsync()
{
    var orders = await _context.Orders.ToListAsync(); // 1 query
    
    var result = new List<OrderDto>();
    foreach (var order in orders) // N queries
    {
        result.Add(new OrderDto
        {
            OrderId = order.Id,
            CustomerName = order.Customer.Name, // Query per order!
            ProductCount = order.OrderItems.Count // Query per order!
        });
    }
    
    return result;
}

// If there are 100 orders, this makes 201 queries (1 + 100 + 100)!
```

### 3.2 Solving N+1 with Include

**Solution 1**: Use `.Include()` for eager loading.

```csharp
// ✅ Good - single query with Include
public async Task<List<OrderDto>> GetOrdersAsync()
{
    var orders = await _context.Orders
        .Include(o => o.Customer)
        .Include(o => o.OrderItems)
        .ToListAsync(); // Single query (or query per Include with split queries)
    
    return orders.Select(o => new OrderDto
    {
        OrderId = o.Id,
        CustomerName = o.Customer.Name,
        ProductCount = o.OrderItems.Count
    }).ToList();
}
```

### 3.3 Solving N+1 with Projection

**Solution 2**: Use `.Select()` projection (often better).

```csharp
// ✅ Best - single efficient query with projection
public async Task<List<OrderDto>> GetOrdersAsync()
{
    return await _context.Orders
        .Select(o => new OrderDto
        {
            OrderId = o.Id,
            CustomerName = o.Customer.Name,
            ProductCount = o.OrderItems.Count
        })
        .ToListAsync(); // Single optimized query
}
```

### 3.4 Split Queries for Multiple Includes

**Best Practice**: Use split queries for multiple collection includes.

```csharp
// ✅ Good - split queries to avoid cartesian explosion
public async Task<List<Order>> GetOrdersWithDetailsAsync()
{
    return await _context.Orders
        .Include(o => o.OrderItems)
        .Include(o => o.Payments)
        .AsSplitQuery() // Multiple queries instead of one large JOIN
        .ToListAsync();
}

// ❌ Bad - cartesian explosion without AsSplitQuery
// If an order has 10 items and 3 payments, single query returns 30 rows
public async Task<List<Order>> GetOrdersWithDetailsAsync()
{
    return await _context.Orders
        .Include(o => o.OrderItems) // Cartesian product
        .Include(o => o.Payments)   // Multiplies rows
        .ToListAsync(); // Inefficient
}
```

---

## 4. Raw SQL

### 4.1 Parameterized Queries

**Critical**: Always use parameterized queries to prevent SQL injection.

```csharp
// ✅ Good - FromSqlInterpolated (parameterized automatically)
public async Task<List<Product>> SearchProductsAsync(string searchTerm)
{
    return await _context.Products
        .FromSqlInterpolated($"SELECT * FROM Products WHERE Name LIKE {searchTerm + "%"}")
        .ToListAsync();
}

// ✅ Good - FromSqlRaw with explicit parameters
public async Task<List<Product>> SearchProductsAsync(string searchTerm)
{
    return await _context.Products
        .FromSqlRaw("SELECT * FROM Products WHERE Name LIKE {0}", searchTerm + "%")
        .ToListAsync();
}

// ❌ CRITICAL - SQL injection vulnerability
public async Task<List<Product>> SearchProductsAsync(string searchTerm)
{
    return await _context.Products
        .FromSqlRaw($"SELECT * FROM Products WHERE Name LIKE '{searchTerm}%'") // VULNERABLE!
        .ToListAsync();
}
// If searchTerm = "'; DROP TABLE Products; --", database is destroyed!
```

### 4.2 When to Use Raw SQL

**Best Practice**: Use raw SQL only when LINQ can't express the query.

```csharp
// ✅ Good use case - complex SQL that LINQ can't express
public async Task<List<SalesReport>> GetMonthlySalesReportAsync()
{
    return await _context.SalesReports
        .FromSqlRaw(@"
            SELECT 
                YEAR(OrderDate) AS Year,
                MONTH(OrderDate) AS Month,
                SUM(Total) AS TotalSales,
                COUNT(*) AS OrderCount
            FROM Orders
            GROUP BY YEAR(OrderDate), MONTH(OrderDate)
            ORDER BY Year DESC, Month DESC
        ")
        .ToListAsync();
}

// ❌ Bad - using raw SQL for simple queries
public async Task<List<Product>> GetActiveProductsAsync()
{
    return await _context.Products
        .FromSqlRaw("SELECT * FROM Products WHERE IsActive = 1") // Use LINQ instead
        .ToListAsync();
}

// ✅ Better - use LINQ
public async Task<List<Product>> GetActiveProductsAsync()
{
    return await _context.Products
        .Where(p => p.IsActive)
        .ToListAsync();
}
```

---

## 5. Migrations

### 5.1 Creating Migrations

**Best Practice**: Create focused migrations with descriptive names.

```bash
# ✅ Good - descriptive migration name
dotnet ef migrations add AddProductCategoryRelationship

# ✅ Good - focused change
dotnet ef migrations add AddCreatedDateToOrder

# ❌ Bad - vague name
dotnet ef migrations add Update1
```

### 5.2 Reviewing Migrations

**Best Practice**: Always review generated migrations before applying.

```csharp
// ✅ Good - review Up and Down methods
public partial class AddProductCategoryRelationship : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<int>(
            name: "CategoryId",
            table: "Products",
            type: "int",
            nullable: false,
            defaultValue: 0); // Check default value

        migrationBuilder.CreateIndex(
            name: "IX_Products_CategoryId",
            table: "Products",
            column: "CategoryId"); // Ensure index is created

        migrationBuilder.AddForeignKey(
            name: "FK_Products_Categories_CategoryId",
            table: "Products",
            column: "CategoryId",
            principalTable: "Categories",
            principalColumn: "Id",
            onDelete: ReferentialAction.Cascade); // Check cascade behavior
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        // Ensure Down properly reverses Up
    }
}
```

### 5.3 Data Seeding

**Best Practice**: Use `HasData` for seed data.

```csharp
// ✅ Good - seeding in OnModelCreating
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Category>().HasData(
        new Category { Id = 1, Name = "Electronics", CreatedDate = DateTime.UtcNow },
        new Category { Id = 2, Name = "Clothing", CreatedDate = DateTime.UtcNow },
        new Category { Id = 3, Name = "Books", CreatedDate = DateTime.UtcNow }
    );
}

// ❌ Bad - seeding in application code (runs every time)
public async Task InitializeDatabaseAsync()
{
    if (!await _context.Categories.AnyAsync())
    {
        _context.Categories.AddRange(
            new Category { Name = "Electronics" },
            new Category { Name = "Clothing" }
        );
        await _context.SaveChangesAsync();
    }
}
```

---

## 6. Relationships

### 6.1 One-to-Many Configuration

**Best Practice**: Configure relationships explicitly with Fluent API.

```csharp
// ✅ Good - explicit configuration
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Order>()
        .HasOne(o => o.Customer)
        .WithMany(c => c.Orders)
        .HasForeignKey(o => o.CustomerId)
        .OnDelete(DeleteBehavior.Restrict); // Don't cascade delete
}

// ✅ Alternative - conventions with navigation properties
public class Order
{
    public int Id { get; set; }
    public int CustomerId { get; set; }
    public Customer Customer { get; set; } // Navigation property
}

public class Customer
{
    public int Id { get; set; }
    public ICollection<Order> Orders { get; set; } // Navigation property
}
```

### 6.2 Many-to-Many Configuration

**Best Practice**: Configure many-to-many relationships (EF Core 5+).

```csharp
// ✅ Good - automatic join table (EF Core 5+)
public class Student
{
    public int Id { get; set; }
    public string Name { get; set; }
    public ICollection<Course> Courses { get; set; }
}

public class Course
{
    public int Id { get; set; }
    public string Title { get; set; }
    public ICollection<Student> Students { get; set; }
}

// EF Core automatically creates join table

// ✅ Good - explicit join entity with additional properties
public class Student
{
    public int Id { get; set; }
    public ICollection<StudentCourse> StudentCourses { get; set; }
}

public class Course
{
    public int Id { get; set; }
    public ICollection<StudentCourse> StudentCourses { get; set; }
}

public class StudentCourse
{
    public int StudentId { get; set; }
    public Student Student { get; set; }
    
    public int CourseId { get; set; }
    public Course Course { get; set; }
    
    public DateTime EnrollmentDate { get; set; } // Additional property
    public int Grade { get; set; }
}

protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<StudentCourse>()
        .HasKey(sc => new { sc.StudentId, sc.CourseId }); // Composite key
}
```

### 6.3 Navigation Property Patterns

**Best Practice**: Initialize collection navigation properties.

```csharp
// ✅ Good - initialized collections
public class Order
{
    public int Id { get; set; }
    public ICollection<OrderItem> OrderItems { get; set; } = new List<OrderItem>();
}

// ❌ Bad - null collection
public class Order
{
    public int Id { get; set; }
    public ICollection<OrderItem> OrderItems { get; set; } // NullReferenceException risk
}

// Usage
var order = new Order();
order.OrderItems.Add(new OrderItem()); // No null check needed
```

---

## 7. Change Tracking

### 7.1 Tracking vs No-Tracking

**Best Practice**: Understand when tracking is enabled.

```csharp
// Tracking enabled by default
var product = await _context.Products.FindAsync(id); // Tracked
product.Price = newPrice;
await _context.SaveChangesAsync(); // Saves changes

// No tracking for read-only
var products = await _context.Products.AsNoTracking().ToListAsync(); // Not tracked
products[0].Price = newPrice;
await _context.SaveChangesAsync(); // Nothing saved!
```

### 7.2 Detaching Entities

**Best Practice**: Detach entities when needed.

```csharp
// ✅ Good - detach entity
var product = await _context.Products.FindAsync(id);
_context.Entry(product).State = EntityState.Detached;

// Now product changes won't be saved
product.Price = newPrice;
await _context.SaveChangesAsync(); // Nothing saved
```

### 7.3 Change Tracker Performance

**Best Practice**: Disable auto-detect changes for bulk operations.

```csharp
// ✅ Good - disable auto-detect for bulk inserts
public async Task BulkInsertProductsAsync(List<Product> products)
{
    _context.ChangeTracker.AutoDetectChangesEnabled = false;
    
    try
    {
        _context.Products.AddRange(products);
        await _context.SaveChangesAsync();
    }
    finally
    {
        _context.ChangeTracker.AutoDetectChangesEnabled = true;
    }
}
```

---

## 8. Transactions

### 8.1 Explicit Transactions

**Best Practice**: Use transactions for multiple operations.

```csharp
// ✅ Good - explicit transaction
public async Task TransferInventoryAsync(int fromWarehouseId, int toWarehouseId, int productId, int quantity)
{
    using var transaction = await _context.Database.BeginTransactionAsync();
    
    try
    {
        var fromWarehouse = await _context.Warehouses.FindAsync(fromWarehouseId);
        var toWarehouse = await _context.Warehouses.FindAsync(toWarehouseId);
        
        fromWarehouse.RemoveStock(productId, quantity);
        toWarehouse.AddStock(productId, quantity);
        
        await _context.SaveChangesAsync();
        await transaction.CommitAsync();
    }
    catch
    {
        await transaction.RollbackAsync();
        throw;
    }
}

// ✅ SaveChanges is automatically transactional for single context
public async Task CreateOrderAsync(Order order)
{
    _context.Orders.Add(order);
    await _context.SaveChangesAsync(); // Atomic transaction
}
```

### 8.2 Transaction Scope

**Best Practice**: Use TransactionScope for distributed transactions.

```csharp
// ✅ Good - distributed transaction
public async Task ProcessOrderAsync(Order order)
{
    using var scope = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled);
    
    await _orderContext.Orders.AddAsync(order);
    await _orderContext.SaveChangesAsync();
    
    await _inventoryContext.ReduceStock(order.ProductId, order.Quantity);
    await _inventoryContext.SaveChangesAsync();
    
    scope.Complete();
}
```

---

## 9. Concurrency Handling

### 9.1 Optimistic Concurrency

**Best Practice**: Use `RowVersion` for concurrency detection.

```csharp
// ✅ Good - RowVersion property
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    
    [Timestamp]
    public byte[] RowVersion { get; set; }
}

// Handling concurrency conflicts
public async Task<bool> UpdateProductAsync(Product product)
{
    try
    {
        _context.Entry(product).State = EntityState.Modified;
        await _context.SaveChangesAsync();
        return true;
    }
    catch (DbUpdateConcurrencyException ex)
    {
        var entry = ex.Entries.Single();
        var databaseValues = await entry.GetDatabaseValuesAsync();
        
        if (databaseValues == null)
        {
            // Entity was deleted
            return false;
        }
        
        // Resolve conflict (e.g., refresh from database)
        entry.OriginalValues.SetValues(databaseValues);
        return false; // Let user retry
    }
}
```

### 9.2 Concurrency Tokens

**Best Practice**: Configure concurrency tokens.

```csharp
// ✅ Good - concurrency token configuration
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Product>()
        .Property(p => p.RowVersion)
        .IsRowVersion();
    
    // Or use IsConcurrencyToken
    modelBuilder.Entity<Product>()
        .Property(p => p.LastModified)
        .IsConcurrencyToken();
}
```

---

## 10. Performance Optimization

### 10.1 Compiled Queries

**Best Practice**: Use compiled queries for frequently executed queries.

```csharp
// ✅ Good - compiled query
private static readonly Func<ApplicationDbContext, int, Task<Product>> 
    GetProductByIdQuery = EF.CompileAsyncQuery(
        (ApplicationDbContext context, int id) => 
            context.Products.FirstOrDefault(p => p.Id == id)
    );

public async Task<Product> GetProductByIdAsync(int id)
{
    return await GetProductByIdQuery(_context, id);
}
```

### 10.2 Batch Operations

**Best Practice**: Use `AddRange` and `RemoveRange` for bulk operations.

```csharp
// ✅ Good - batch insert
public async Task AddProductsAsync(List<Product> products)
{
    _context.Products.AddRange(products); // Single SQL INSERT with multiple values
    await _context.SaveChangesAsync();
}

// ❌ Bad - individual inserts
public async Task AddProductsAsync(List<Product> products)
{
    foreach (var product in products)
    {
        _context.Products.Add(product); // N INSERT statements
    }
    await _context.SaveChangesAsync();
}
```

### 10.3 Query Performance Monitoring

**Best Practice**: Enable sensitive data logging in development.

```csharp
// ✅ Good - detailed logging in development
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseSqlServer(connectionString);
    
    if (builder.Environment.IsDevelopment())
    {
        options.EnableSensitiveDataLogging(); // Shows parameter values
        options.EnableDetailedErrors();
        options.LogTo(Console.WriteLine, LogLevel.Information);
    }
});
```

---

## Common Entity Framework Anti-Patterns

1. **DbContext as Singleton**: NEVER - not thread-safe
2. **N+1 Queries**: Use `.Include()` or `.Select()` projection
3. **Loading Full Entities for DTOs**: Use `.Select()` projection
4. **Not Using AsNoTracking**: Use for read-only queries
5. **SQL Injection in Raw Queries**: Always parameterize
6. **Loading Everything**: Filter with `.Where()` before `.ToList()`
7. **Multiple Enumeration**: Materialize with `.ToList()` once
8. **Ignoring Concurrency**: Use `[Timestamp]` for critical data
9. **Not Disposing DbContext**: Use `using` statements
10. **Cartesian Explosion**: Use `.AsSplitQuery()` for multiple includes

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
