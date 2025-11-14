# Modern C# Language Features

This file documents modern C# language features (C# 8-12) and best practices for their usage.

## Purpose

Load this file when reviewing:
- Modern C# syntax (C# 8+)
- Nullable reference types
- Pattern matching
- Records and value types

---

## 1. Nullable Reference Types (C# 8)

### 1.1 Enabling Nullable Context

**Best Practice**: Enable nullable reference types in new projects.

```xml
<!-- ✅ Good - enable in .csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>
```

### 1.2 Nullable Annotations

```csharp
// ✅ Good - explicit nullability
public class User
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty; // Non-nullable, must initialize
    public string? Email { get; set; } // Nullable
    public Address? Address { get; set; } // Nullable
}

// ❌ Bad - nullable warning
public class User
{
    public int Id { get; set; }
    public string Name { get; set; } // Warning: Non-nullable property must contain non-null value
    public string? Email { get; set; }
}
```

### 1.3 Null-Forgiving Operator (!)

**Rule**: Avoid null-forgiving operator unless you're certain.

```csharp
// ❌ Bad - null-forgiving operator abuse
public void ProcessUser(int userId)
{
    var user = _users.FirstOrDefault(u => u.Id == userId)!; // Could be null!
    Console.WriteLine(user.Name); // NullReferenceException if not found
}

// ✅ Good - proper null checking
public void ProcessUser(int userId)
{
    var user = _users.FirstOrDefault(u => u.Id == userId);
    if (user == null)
    {
        throw new ArgumentException($"User {userId} not found");
    }
    Console.WriteLine(user.Name);
}

// ✅ Acceptable - when you know it's not null
public void Initialize()
{
    // HttpContext is guaranteed to be non-null in middleware
    var userId = HttpContext.User.FindFirst(ClaimTypes.NameIdentifier)!.Value;
}
```

### 1.4 Nullable Value Types

```csharp
// ✅ Good - nullable value types
public class Order
{
    public int Id { get; set; }
    public DateTime OrderDate { get; set; }
    public DateTime? ShippedDate { get; set; } // Nullable, may not have shipped yet
    public decimal Total { get; set; }
}

// Checking nullable value types
if (order.ShippedDate.HasValue)
{
    Console.WriteLine($"Shipped on {order.ShippedDate.Value}");
}

// Or use null-conditional
Console.WriteLine($"Shipped: {order.ShippedDate?.ToString("yyyy-MM-dd") ?? "Not shipped"}");
```

---

## 2. Pattern Matching

### 2.1 Switch Expressions (C# 8)

**Best Practice**: Use switch expressions for exhaustive matching.

```csharp
// ✅ Good - switch expression
public decimal CalculateDiscount(Customer customer) => customer.Type switch
{
    CustomerType.Regular => 0.0m,
    CustomerType.Premium => 0.10m,
    CustomerType.VIP => 0.20m,
    _ => throw new ArgumentException($"Unknown customer type: {customer.Type}")
};

// ❌ Old style - switch statement
public decimal CalculateDiscount(Customer customer)
{
    switch (customer.Type)
    {
        case CustomerType.Regular:
            return 0.0m;
        case CustomerType.Premium:
            return 0.10m;
        case CustomerType.VIP:
            return 0.20m;
        default:
            throw new ArgumentException($"Unknown customer type: {customer.Type}");
    }
}
```

### 2.2 Property Patterns (C# 8)

```csharp
// ✅ Good - property patterns
public decimal CalculateShipping(Order order) => order switch
{
    { Total: > 100 } => 0, // Free shipping over $100
    { Country: "US", Weight: < 5 } => 5.99m,
    { Country: "US" } => 9.99m,
    { Country: "CA" } => 12.99m,
    _ => 19.99m
};

// ✅ Good - nested property patterns
public string GetCustomerStatus(Customer customer) => customer switch
{
    { Orders: { Count: > 100 }, TotalSpent: > 10000 } => "VIP",
    { Orders: { Count: > 10 } } => "Premium",
    _ => "Regular"
};
```

### 2.3 Type Patterns (C# 9)

```csharp
// ✅ Good - type patterns
public string FormatValue(object value) => value switch
{
    null => "null",
    int i => $"Integer: {i}",
    string s => $"String: {s}",
    DateTime dt => $"Date: {dt:yyyy-MM-dd}",
    IEnumerable<int> numbers => $"Numbers: {string.Join(", ", numbers)}",
    _ => value.ToString() ?? "unknown"
};
```

### 2.4 Relational Patterns (C# 9)

```csharp
// ✅ Good - relational patterns
public string ClassifyTemperature(int celsius) => celsius switch
{
    < 0 => "Freezing",
    >= 0 and < 10 => "Cold",
    >= 10 and < 20 => "Cool",
    >= 20 and < 30 => "Warm",
    >= 30 => "Hot"
};
```

---

## 3. Records (C# 9)

### 3.1 When to Use Records

**Best Practice**: Use records for immutable data transfer objects.

```csharp
// ✅ Good - record for DTO
public record ProductDto(int Id, string Name, decimal Price);

// Usage
var product = new ProductDto(1, "Widget", 29.99m);
var updated = product with { Price = 39.99m }; // Non-destructive mutation

// ✅ Good - record for value objects
public record Address(string Street, string City, string State, string ZipCode);

// ❌ Bad - class when record is more appropriate
public class ProductDto
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    
    // Must implement Equals, GetHashCode, ToString manually
}
```

### 3.2 Record Value Equality

```csharp
// ✅ Good - records have value equality
var address1 = new Address("123 Main St", "Springfield", "IL", "62701");
var address2 = new Address("123 Main St", "Springfield", "IL", "62701");

Console.WriteLine(address1 == address2); // True - value equality

// Classes have reference equality
public class AddressClass
{
    public string Street { get; set; }
    public string City { get; set; }
}

var addr1 = new AddressClass { Street = "123 Main" };
var addr2 = new AddressClass { Street = "123 Main" };

Console.WriteLine(addr1 == addr2); // False - different references
```

### 3.3 Record Inheritance

```csharp
// ✅ Good - record inheritance
public record Person(string FirstName, string LastName);
public record Employee(string FirstName, string LastName, int EmployeeId) : Person(FirstName, LastName);

// Usage
Employee emp = new("John", "Doe", 12345);
Person person = emp; // Covariant
```

---

## 4. Init-Only Properties (C# 9)

### 4.1 Immutable Objects

**Best Practice**: Use `init` for immutable properties.

```csharp
// ✅ Good - init-only properties
public class User
{
    public int Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
}

// Usage
var user = new User { Id = 1, Name = "John" };
// user.Id = 2; // Compiler error - init-only

// ❌ Bad - mutable when it should be immutable
public class User
{
    public int Id { get; set; } // Can be changed after construction
    public string Name { get; set; } = string.Empty;
}
```

---

## 5. Top-Level Statements (C# 9)

### 5.1 Program Entry Point

**Best Practice**: Use top-level statements for simple programs.

```csharp
// ✅ Good - top-level statements (Program.cs)
using Microsoft.AspNetCore.Builder;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

var app = builder.Build();

app.MapControllers();

app.Run();

// ❌ Old style - unnecessary ceremony
public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        // ...
    }
}
```

---

## 6. Global Using Directives (C# 10)

### 6.1 Global Usings

**Best Practice**: Centralize common usings in a single file.

```csharp
// ✅ Good - GlobalUsings.cs
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading.Tasks;
global using Microsoft.EntityFrameworkCore;
global using MyApp.Models;
global using MyApp.Services;

// Or in .csproj
<ItemGroup>
  <Using Include="System.Collections.Generic" />
  <Using Include="Microsoft.EntityFrameworkCore" />
</ItemGroup>
```

---

## 7. File-Scoped Namespaces (C# 10)

### 7.1 Reducing Indentation

**Best Practice**: Use file-scoped namespaces.

```csharp
// ✅ Good - file-scoped namespace (C# 10)
namespace MyApp.Services;

public class ProductService
{
    public async Task<List<Product>> GetAllAsync()
    {
        // Implementation
    }
}

// ❌ Old style - extra indentation
namespace MyApp.Services
{
    public class ProductService
    {
        public async Task<List<Product>> GetAllAsync()
        {
            // Implementation
        }
    }
}
```

---

## 8. Required Members (C# 11)

### 8.1 Required Properties

**Best Practice**: Use `required` for mandatory initialization.

```csharp
// ✅ Good - required members (C# 11)
public class CreateProductDto
{
    public required string Name { get; init; }
    public required decimal Price { get; init; }
    public string? Description { get; init; }
}

// Usage - compiler enforces required properties
var dto = new CreateProductDto
{
    Name = "Widget",
    Price = 29.99m
    // Description is optional
};

// var invalid = new CreateProductDto { Name = "Widget" }; // Compiler error: Price required
```

---

## 9. Raw String Literals (C# 11)

### 9.1 Multi-Line Strings

**Best Practice**: Use raw string literals for JSON, SQL, etc.

```csharp
// ✅ Good - raw string literal
string json = """
    {
        "name": "John",
        "email": "john@example.com",
        "address": {
            "city": "Springfield"
        }
    }
    """;

// ✅ Good - SQL queries
string sql = """
    SELECT p.Id, p.Name, p.Price
    FROM Products p
    WHERE p.CategoryId = @CategoryId
        AND p.IsActive = 1
    ORDER BY p.Name
    """;

// ❌ Old style - escaped quotes
string jsonOld = "{\r\n  \"name\": \"John\",\r\n  \"email\": \"john@example.com\"\r\n}";
```

### 9.2 Interpolated Raw Strings

```csharp
// ✅ Good - interpolated raw string literal
int categoryId = 5;
string sql = $$"""
    SELECT * FROM Products
    WHERE CategoryId = {{categoryId}}
    """;
```

---

## 10. List Patterns (C# 11)

### 10.1 Pattern Matching on Lists

```csharp
// ✅ Good - list patterns
public string DescribeList(int[] numbers) => numbers switch
{
    [] => "Empty",
    [var single] => $"Single element: {single}",
    [var first, var second] => $"Two elements: {first}, {second}",
    [var first, .., var last] => $"Multiple elements, first: {first}, last: {last}",
    _ => "Unknown"
};
```

---

## 11. Collection Expressions (C# 12)

### 11.1 Simplified Collection Initialization

```csharp
// ✅ Good - collection expressions (C# 12)
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];

// Spreading
int[] moreNumbers = [..numbers, 6, 7, 8];

// ❌ Old style
int[] numbersOld = new int[] { 1, 2, 3, 4, 5 };
List<string> namesOld = new List<string> { "Alice", "Bob", "Charlie" };
```

---

## 12. Primary Constructors (C# 12)

### 12.1 Simplified Dependency Injection

```csharp
// ✅ Good - primary constructor (C# 12)
public class ProductService(IProductRepository repository, ILogger<ProductService> logger)
{
    public async Task<Product?> GetByIdAsync(int id)
    {
        logger.LogInformation("Getting product {ProductId}", id);
        return await repository.GetByIdAsync(id);
    }
}

// ❌ Old style - explicit constructor
public class ProductService
{
    private readonly IProductRepository _repository;
    private readonly ILogger<ProductService> _logger;
    
    public ProductService(IProductRepository repository, ILogger<ProductService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
}
```

---

## Modern C# Checklist

1. **Nullable Reference Types**: ✅ Enable in new projects
2. **Null-Forgiving Operator**: ✅ Avoid unless certain
3. **Switch Expressions**: ✅ Use for exhaustive matching
4. **Records**: ✅ Use for immutable DTOs
5. **Init-Only Properties**: ✅ Use for immutability
6. **Top-Level Statements**: ✅ Use for simple programs
7. **File-Scoped Namespaces**: ✅ Reduce indentation
8. **Required Members**: ✅ Enforce mandatory initialization
9. **Raw String Literals**: ✅ Use for JSON, SQL, etc.
10. **Primary Constructors**: ✅ Simplify DI in services

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
