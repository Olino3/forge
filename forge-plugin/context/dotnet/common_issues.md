---
id: "dotnet/common_issues"
domain: dotnet
title: ".NET Common Issues"
type: always
estimatedTokens: 1250
loadingStrategy: always
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Critical Anti-Patterns"
    estimatedTokens: 96
    keywords: [critical, anti-patterns]
  - name: "Async/Await Issues"
    estimatedTokens: 60
    keywords: [asyncawait, issues]
  - name: "IDisposable Issues"
    estimatedTokens: 55
    keywords: [idisposable, issues]
  - name: "LINQ Performance Issues"
    estimatedTokens: 54
    keywords: [linq, performance, issues]
  - name: "Exception Handling Issues"
    estimatedTokens: 51
    keywords: [exception, handling, issues]
  - name: "String Performance Issues"
    estimatedTokens: 31
    keywords: [string, performance, issues]
  - name: "Nullable Reference Types Issues"
    estimatedTokens: 44
    keywords: [nullable, reference, types, issues]
  - name: "Collection Issues"
    estimatedTokens: 36
    keywords: [collection, issues]
  - name: "Memory Leak Patterns"
    estimatedTokens: 52
    keywords: [memory, leak, patterns]
  - name: "Common Detection Patterns"
    estimatedTokens: 84
    keywords: [detection, patterns]
  - name: "Checklist"
    estimatedTokens: 66
    keywords: [checklist]
  - name: "Official Resources"
    estimatedTokens: 22
    keywords: [official, resources]
tags: [dotnet, common-issues, async, disposable, linq, exceptions, memory-leaks]
---

# .NET Common Issues

Quick reference for universal .NET problems. For detailed examples, see [.NET documentation](https://learn.microsoft.com/en-us/dotnet/).

**Always load this file** - it contains the most frequent and critical .NET issues across all frameworks.

---

## Critical Anti-Patterns

| Anti-Pattern | Detection | Impact | Fix | Learn More |
|--------------|-----------|--------|-----|------------|
| **Sync-over-async** | `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` | 🔴 Deadlock | Use `async`/`await` | [Async best practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming) |
| **Async void** | `async void` (not event handler) | 🔴 Unhandled exceptions | Use `async Task` | [Async void](https://learn.microsoft.com/en-us/dotnet/csharp/async#avoid-async-void) |
| **Missing using** | `new FileStream()` without `using` | 🔴 Resource leak | Use `using` statement | [IDisposable](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/using-objects) |
| **Multiple enumeration** | `IEnumerable<T>` used multiple times | 🟠 Performance | Call `.ToList()` once | [Deferred execution](https://learn.microsoft.com/en-us/dotnet/standard/linq/deferred-execution-lazy-evaluation) |
| **Exception swallowing** | Empty `catch` block | 🟠 Silent failures | Log or rethrow | [Exception handling](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/) |
| **String concatenation in loop** | `str += x` in loop | 🟡 Performance | Use `StringBuilder` | [StringBuilder](https://learn.microsoft.com/en-us/dotnet/api/system.text.stringbuilder) |

---

## Async/Await Issues

| Issue | Detection Pattern | Fix |
|-------|-------------------|-----|
| **Sync-over-async** | `.Result`, `.Wait()` | Make method `async`, use `await` |
| **Async void** | `async void Method()` | Change to `async Task` |
| **Missing ConfigureAwait** | No `.ConfigureAwait(false)` in library | Add in library code only |
| **Fire-and-forget** | `_ = SomeAsyncMethod()` | Await or use background service |
| **Task.Run for I/O** | `Task.Run(async () => ...)` | Direct `await` (no Task.Run) |

[Async/await best practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)

---

## IDisposable Issues

| Issue | Detection Pattern | Fix |
|-------|-------------------|-----|
| **Missing using** | `new FileStream()` without `using` | Use `using` or `using var` |
| **Not implementing IDisposable** | Unmanaged resources without IDisposable | Implement IDisposable pattern |
| **Dispose not in finally** | Try-catch without finally for Dispose | Use `using` or try-finally |
| **Disposing DI services** | Calling `.Dispose()` on injected service | Let container manage disposal |

[IDisposable pattern](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)

---

## LINQ Performance Issues

| Issue | Detection | Fix | Impact |
|-------|-----------|-----|--------|
| **Multiple enumeration** | `IEnumerable` used 2+ times | `.ToList()` once | 🟠 High |
| **Count() > 0** | Existence check with Count | Use `.Any()` | 🟡 Medium |
| **Client-side evaluation** | `.ToList()` before `.Where()` | Filter in database | 🟠 High |
| **N+1 queries** | Loop accessing navigation properties | Use `.Include()` | 🔴 Critical |

---

## Exception Handling Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| **Empty catch** | `catch { }` | Log exception or remove catch |
| **Catch Exception** | `catch (Exception)` too broad | Catch specific exceptions |
| **Throw ex** | `throw ex;` loses stack trace | Use `throw;` to preserve |
| **Exception for control flow** | Try-catch in normal flow | Use validation instead |

[Exception best practices](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions)

---

## String Performance Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| **Loop concatenation** | `str += x` in loop | `StringBuilder` |
| **ToLower comparison** | `.ToLower() ==` | `StringComparison.OrdinalIgnoreCase` |
| **Unnecessary allocation** | Multiple `.Substring()` | Use `Span<char>` or `ReadOnlySpan<char>` |

---

## Nullable Reference Types Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| **Null-forgiving abuse** | `user!.Name` without check | Add null check first |
| **Missing null checks** | `string? x` then `x.Length` | Check `if (x == null)` |
| **Non-nullable without init** | `public string Name { get; set; }` | Initialize or use `string?` |

[Nullable reference types](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references)

---

## Collection Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| **No capacity** | `new List<T>()` when size known | `new List<T>(capacity)` |
| **Wrong collection type** | `List.Contains()` for lookups | Use `HashSet` or `Dictionary` |
| **Boxing** | Value types in `ArrayList` | Use generic collections |

---

## Memory Leak Patterns

| Issue | Detection | Fix |
|-------|-----------|-----|
| **Event handler leak** | `+=` without `-=` | Unsubscribe in Dispose |
| **Static references** | Static field holding instances | Weak references or clear on dispose |
| **Timer not disposed** | `new Timer()` without dispose | Dispose timer |
| **Large object in field** | Large byte arrays | Use ArrayPool or clear reference |

[Detecting memory leaks](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-memory-leak)

---

## Common Detection Patterns

```csharp
// ❌ Sync-over-async
.Result
.Wait()
.GetAwaiter().GetResult()

// ❌ Async void
async void ProcessData()

// ❌ Missing using
var stream = new FileStream(...)
// No using

// ❌ Multiple enumeration
var data = GetData();  // IEnumerable
data.Count();
data.First();

// ❌ Empty catch
try { } catch { }

// ❌ String concatenation in loop
for (int i = 0; i < 100; i++)
    result += i.ToString();

// ❌ Count() > 0
if (list.Count() > 0)

// ❌ Null-forgiving without check
user!.Name

// ❌ Event handler leak
someEvent += Handler;
// No -= in Dispose

// ❌ throw ex (loses stack)
catch (Exception ex)
{
    throw ex;  // Use throw; instead
}
```

---

## Checklist

- ✅ No `.Result` or `.Wait()` (async all the way)
- ✅ No `async void` (except event handlers)
- ✅ `using` statements for IDisposable
- ✅ `.ToList()` to avoid multiple enumeration
- ✅ `.Any()` instead of `.Count() > 0`
- ✅ `StringBuilder` for string concatenation in loops
- ✅ Catch specific exceptions, log them
- ✅ `throw;` not `throw ex;`
- ✅ Unsubscribe event handlers in Dispose
- ✅ Dispose timers and resources
- ✅ Specify collection capacity when known
- ✅ Null checks before using nullable references

---

## Official Resources

- **.NET Fundamentals**: https://learn.microsoft.com/en-us/dotnet/fundamentals/
- **Async programming**: https://learn.microsoft.com/en-us/dotnet/csharp/async
- **Garbage collection**: https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/
- **Exception handling**: https://learn.microsoft.com/en-us/dotnet/standard/exceptions/
- **LINQ**: https://learn.microsoft.com/en-us/dotnet/csharp/linq/

---

**Version**: 0.2.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
