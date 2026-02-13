---
id: "dotnet/csharp_patterns"
domain: dotnet
title: "Modern C# Language Features"
type: pattern
estimatedTokens: 1150
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 76
    keywords: [anti-patterns]
  - name: "C# Version Features"
    estimatedTokens: 268
    keywords: [version, features]
  - name: "Pattern Matching Quick Reference"
    estimatedTokens: 60
    keywords: [pattern, matching, quick, reference]
  - name: "Records vs Classes"
    estimatedTokens: 39
    keywords: [records, classes]
  - name: "Nullable Reference Types"
    estimatedTokens: 51
    keywords: [nullable, reference, types]
  - name: "Common Detection Patterns"
    estimatedTokens: 82
    keywords: [detection, patterns]
  - name: "Tools"
    estimatedTokens: 16
    keywords: [tools]
  - name: "Official Resources"
    estimatedTokens: 23
    keywords: [official, resources]
tags: [dotnet, csharp, nullable, records, pattern-matching, primary-constructors]
---

# Modern C# Language Features

Quick reference for modern C# features (C# 8-12) and best practices. For detailed examples, see [C# documentation](https://learn.microsoft.com/en-us/dotnet/csharp/).

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|--------------|
| **No nullable context** | Missing `<Nullable>enable</Nullable>` | Enable in .csproj | [Nullable reference types](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references) |
| **Null-forgiving abuse** | `user!.Name` without validation | Check for null first | [Null-forgiving operator](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/null-forgiving) |
| **Using classes instead of records** | Mutable DTOs | Use records for immutable data | [Records](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record) |
| **Traditional namespaces** | Block-scoped namespaces | Use file-scoped (C# 10+) | [File-scoped namespaces](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/namespace) |
| **Missing required members** | Optional properties that should be required | Use `required` keyword (C# 11+) | [Required members](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/required) |

---

## C# Version Features

### C# 8

| Feature | Usage | Example |
|---------|-------|---------|
| **Nullable reference types** | Explicit nullability | `string?` nullable, `string` non-nullable |
| **Switch expressions** | Pattern matching | `customer.Type switch { ... }` |
| **Using declarations** | Simplified disposal | `using var stream = ...;` |
| **Default interface methods** | Interface implementations | Add methods to interfaces |
| **Async streams** | IAsyncEnumerable | `await foreach` |

[C# 8 features](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-8)

### C# 9

| Feature | Usage | Example |
|---------|-------|---------|
| **Records** | Immutable data | `public record Person(string Name);` |
| **Init-only properties** | Immutability | `public string Name { get; init; }` |
| **Top-level statements** | Simplified Program.cs | No Main method needed |
| **Pattern matching enhancements** | Relational/logical patterns | `>= 0 and < 10` |
| **Target-typed new** | Simplified initialization | `List<int> numbers = new();` |

[C# 9 features](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-9)

### C# 10

| Feature | Usage | Example |
|---------|-------|---------|
| **Global using directives** | Reduce boilerplate | `global using System;` |
| **File-scoped namespaces** | Less indentation | `namespace MyApp.Services;` |
| **Record structs** | Value-type records | `public record struct Point(int X, int Y);` |
| **Extended property patterns** | Nested patterns | `{ Address.City: "Seattle" }` |

[C# 10 features](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-10)

### C# 11

| Feature | Usage | Example |
|---------|-------|---------|
| **Required members** | Mandatory initialization | `public required string Name { get; init; }` |
| **Raw string literals** | Multi-line strings | `"""JSON content"""` |
| **List patterns** | Pattern matching lists | `[var first, .., var last]` |
| **Generic math** | Generic numeric constraints | `T : INumber<T>` |

[C# 11 features](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-11)

### C# 12

| Feature | Usage | Example |
|---------|-------|---------|
| **Primary constructors** | Simplified DI | `public class Service(IRepo repo)` |
| **Collection expressions** | Unified syntax | `int[] nums = [1, 2, 3];` |
| **Default lambda parameters** | Optional parameters | `var f = (int x = 0) => x;` |
| **Alias any type** | Using aliases | `using Point = (int x, int y);` |

[C# 12 features](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-12)

---

## Pattern Matching Quick Reference

| Pattern Type | Syntax | Use Case |
|--------------|--------|----------|
| **Type pattern** | `obj is string s` | Type check with variable |
| **Property pattern** | `{ Length: > 5 }` | Match on properties |
| **Relational pattern** | `>= 0 and < 10` | Numeric ranges |
| **Logical pattern** | `is > 0 or < -5` | Combine patterns |
| **List pattern** | `[1, 2, ..]` | Match list elements |

[Pattern matching](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/functional/pattern-matching)

---

## Records vs Classes

| Use Case | Choose |
|----------|--------|
| Immutable DTOs | Record |
| Value equality needed | Record |
| With-expressions desired | Record |
| Inheritance with modification | Record |
| Mutable state | Class |
| Reference equality | Class |
| Performance-critical | Class (sometimes) |

---

## Nullable Reference Types

| Pattern | Detection | Fix |
|---------|-----------|-----|
| **Missing null checks** | `string? input` then `input.Length` | Check `if (input == null)` first |
| **Null-forgiving abuse** | `user!.Name` without validation | Add null check or use `?.` |
| **Non-nullable without init** | `public string Name { get; set; }` | Initialize with `= string.Empty` or `{ get; init; }` |

[Nullable reference types tutorial](https://learn.microsoft.com/en-us/dotnet/csharp/tutorials/nullable-reference-types)

---

## Common Detection Patterns

```csharp
// ❌ Missing nullable context
// Look for: No <Nullable>enable</Nullable> in .csproj

// ❌ Null-forgiving without validation
user!.Name  // No null check before !

// ❌ Class instead of record for DTO
public class ProductDto { get; set; }  // Should be record

// ❌ Block namespace
namespace MyApp.Services
{
    public class ProductService { }
}

// ✅ File-scoped namespace
namespace MyApp.Services;
public class ProductService { }

// ❌ Missing required on mandatory properties
public class CreateUserDto
{
    public string Email { get; init; }  // Should be required
}

// ✅ With required
public class CreateUserDto
{
    public required string Email { get; init; }
}
```

---

## Tools

- **Roslyn Analyzers**: Built-in code analysis - [Analyzers](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview)
- **StyleCop**: Code style enforcement - [StyleCop](https://github.com/DotNetAnalyzers/StyleCopAnalyzers)
- **Roslynator**: Additional analyzers - [Roslynator](https://github.com/JosefPihrt/Roslynator)

---

## Official Resources

- **C# Documentation**: https://learn.microsoft.com/en-us/dotnet/csharp/
- **What's New in C#**: https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/
- **C# Language Reference**: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/
- **C# Programming Guide**: https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/

---

**Version**: 0.3.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
