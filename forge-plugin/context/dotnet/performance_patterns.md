---
id: "dotnet/performance_patterns"
domain: dotnet
title: ".NET Performance Optimization Patterns"
type: pattern
estimatedTokens: 1050
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 76
    keywords: [anti-patterns]
  - name: "String Performance"
    estimatedTokens: 40
    keywords: [string, performance]
  - name: "Collection Performance"
    estimatedTokens: 35
    keywords: [collection, performance]
  - name: "Memory Optimization"
    estimatedTokens: 46
    keywords: [memory, optimization]
  - name: "Async Performance"
    estimatedTokens: 38
    keywords: [async, performance]
  - name: "Database Performance"
    estimatedTokens: 43
    keywords: [database, performance]
  - name: "Caching Patterns"
    estimatedTokens: 49
    keywords: [caching, patterns]
  - name: "HTTP Client Best Practices"
    estimatedTokens: 33
    keywords: [http, client]
  - name: "Large Object Heap (LOH)"
    estimatedTokens: 30
    keywords: [large, object, heap, loh]
  - name: "Common Detection Patterns"
    estimatedTokens: 72
    keywords: [detection, patterns]
  - name: "Performance Checklist"
    estimatedTokens: 54
    keywords: [performance, checklist]
  - name: "Profiling Tools"
    estimatedTokens: 21
    keywords: [profiling, tools]
  - name: "Official Resources"
    estimatedTokens: 22
    keywords: [official, resources]
tags: [dotnet, performance, strings, collections, memory, caching, httpclient]
---

# .NET Performance Optimization Patterns

Quick reference for performance optimization in .NET. For detailed examples, see [Performance best practices](https://learn.microsoft.com/en-us/dotnet/core/performance/).

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|--------------|
| **String concatenation in loops** | `result += str` in loop | Use `StringBuilder` | [StringBuilder](https://learn.microsoft.com/en-us/dotnet/api/system.text.stringbuilder) |
| **No collection capacity** | `new List<T>()` when size known | `new List<T>(capacity)` | [List capacity](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.-ctor#system-collections-generic-list-1-ctor(system-int32)) |
| **Boxing value types** | Value type to `object` | Use generics | [Boxing and unboxing](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing) |
| **Creating HttpClient per request** | `new HttpClient()` in method | Use `IHttpClientFactory` | [HttpClient best practices](https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory) |
| **Large object allocations** | Objects > 85KB | Use `ArrayPool` or split objects | [LOH](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/large-object-heap) |

---

## String Performance

| Issue | Detection | Fix | Learn More |
|-------|-----------|-----|------------|
| **Loop concatenation** | `str += x` in loop | `StringBuilder` | [String best practices](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings) |
| **ToLower comparison** | `.ToLower() ==` | `StringComparison.OrdinalIgnoreCase` | [String comparison](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings#choose-appropriate-comparison) |
| **Substring allocations** | Multiple `.Substring()` | Use `Span<char>` or `ReadOnlySpan<char>` | [Span<T>](https://learn.microsoft.com/en-us/dotnet/api/system.span-1) |

---

## Collection Performance

| Pattern | Bad | Good | Learn More |
|---------|-----|------|------------|
| **No capacity** | `new List<T>()` | `new List<T>(expectedSize)` | [List](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1) |
| **Wrong collection** | `List.Contains()` in loop | `HashSet.Contains()` | [Collections](https://learn.microsoft.com/en-us/dotnet/standard/collections/) |
| **Lookup with List** | `List.Find()` | `Dictionary[key]` | [Dictionary](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.dictionary-2) |

---

## Memory Optimization

| Feature | Use Case | Example | Learn More |
|---------|----------|---------|------------|
| **Span<T>** | Stack allocation, slicing | `Span<int> span = stackalloc int[100];` | [Span<T>](https://learn.microsoft.com/en-us/dotnet/api/system.span-1) |
| **Memory<T>** | Async operations on memory | `Memory<byte> memory` | [Memory<T>](https://learn.microsoft.com/en-us/dotnet/api/system.memory-1) |
| **ArrayPool<T>** | Temporary arrays | `ArrayPool<byte>.Shared.Rent(size)` | [ArrayPool](https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1) |
| **ObjectPool<T>** | Expensive object reuse | `ObjectPool<ExpensiveObj>` | [ObjectPool](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.objectpool.objectpool-1) |

---

## Async Performance

| Pattern | Use When | Benefit | Learn More |
|---------|----------|---------|------------|
| **ValueTask<T>** | Often synchronous result | Avoids Task allocation | [ValueTask](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask-1) |
| **IAsyncEnumerable** | Large datasets streaming | Memory efficient | [Async streams](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios#asynchronous-streams) |
| **ConfigureAwait(false)** | Library code | Avoids context capture | [ConfigureAwait](https://devblogs.microsoft.com/dotnet/configureawait-faq/) |

---

## Database Performance

| Pattern | Detection | Fix | Learn More |
|---------|-----------|-----|------------|
| **No connection pooling** | `Pooling=false` in connection string | Remove it (pooling default) | [Connection pooling](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql-server-connection-pooling) |
| **One-by-one inserts** | `SaveChanges()` in loop | `AddRange()` + single `SaveChanges()` | [Bulk operations](https://learn.microsoft.com/en-us/ef/core/performance/efficient-updating) |
| **Tracking read-only** | Default tracking | `AsNoTracking()` | [No-tracking queries](https://learn.microsoft.com/en-us/ef/core/querying/tracking) |

---

## Caching Patterns

| Cache Type | Scope | Use When | Learn More |
|------------|-------|----------|------------|
| **IMemoryCache** | In-process | Single-server apps | [Memory cache](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory) |
| **IDistributedCache** | Shared (Redis, SQL) | Multi-server apps | [Distributed cache](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/distributed) |
| **Response caching** | HTTP responses | Public content | [Response caching](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/response) |
| **Output caching** | Endpoint output (.NET 7+) | Fine-grained control | [Output caching](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/output) |

---

## HTTP Client Best Practices

```csharp
// ❌ CRITICAL - Socket exhaustion
using var client = new HttpClient();  // DON'T create per request

// ✅ Use IHttpClientFactory
services.AddHttpClient<IProductClient, ProductClient>();

public class ProductClient
{
    private readonly HttpClient _client;
    public ProductClient(HttpClient client) => _client = client;
}
```

[HttpClient best practices](https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory)

---

## Large Object Heap (LOH)

| Pattern | Detection | Fix | Learn More |
|---------|-----------|-----|------------|
| **Large allocations** | Objects > 85KB | Use `ArrayPool<T>` | [LOH](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/large-object-heap) |
| **Frequent LOH alloc** | Gen2 collections high | Pool large objects | [GC fundamentals](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals) |

---

## Common Detection Patterns

```csharp
// ❌ String concatenation
for (int i = 0; i < 1000; i++)
    result += i.ToString();

// ❌ No capacity
new List<Product>()
new Dictionary<int, Product>()

// ❌ Boxing
object obj = 42;
ArrayList list = new();  // Boxes value types

// ❌ HttpClient per request
using var client = new HttpClient();

// ❌ ToLower for comparison
if (name.ToLower() == "admin")

// ❌ List for lookups
if (list.Contains(id))  // O(n) instead of O(1)

// ❌ Not using ArrayPool
byte[] buffer = new byte[4096];

// ❌ Tracking for read-only
var products = _db.Products.ToList();  // Tracking enabled
```

---

## Performance Checklist

- ✅ `StringBuilder` for string concatenation in loops
- ✅ Specify collection capacity when size is known
- ✅ `HashSet` for uniqueness, `Dictionary` for lookups
- ✅ Use `Span<T>` for stack allocations
- ✅ `ArrayPool<T>` for temporary large arrays
- ✅ `ValueTask<T>` for often-synchronous operations
- ✅ `AsNoTracking()` for read-only EF queries
- ✅ `IHttpClientFactory` instead of creating HttpClient
- ✅ Enable caching (memory, distributed, response)
- ✅ Avoid boxing value types

---

## Profiling Tools

- **BenchmarkDotNet**: Micro-benchmarking - [BenchmarkDotNet](https://benchmarkdotnet.org/)
- **dotTrace**: JetBrains profiler - [dotTrace](https://www.jetbrains.com/profiler/)
- **PerfView**: Microsoft performance tool - [PerfView](https://github.com/microsoft/perfview)
- **Visual Studio Profiler**: Built-in profiler - [VS Profiler](https://learn.microsoft.com/en-us/visualstudio/profiling/)

---

## Official Resources

- **Performance best practices**: https://learn.microsoft.com/en-us/dotnet/core/performance/
- **Memory management**: https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/
- **ASP.NET Core performance**: https://learn.microsoft.com/en-us/aspnet/core/performance/performance-best-practices
- **EF Core performance**: https://learn.microsoft.com/en-us/ef/core/performance/

---

**Version**: 0.2.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
