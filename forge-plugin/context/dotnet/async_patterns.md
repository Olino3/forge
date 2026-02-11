---
id: "dotnet/async_patterns"
domain: dotnet
title: "Async/Await Patterns"
type: pattern
estimatedTokens: 1000
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Critical Anti-Patterns"
    estimatedTokens: 76
    keywords: [critical, anti-patterns]
  - name: "Async Rules"
    estimatedTokens: 62
    keywords: [async, rules]
  - name: "Sync-over-Async Deadlock"
    estimatedTokens: 37
    keywords: [sync-over-async, deadlock]
  - name: "ConfigureAwait"
    estimatedTokens: 66
    keywords: [configureawait]
  - name: "ValueTask vs Task"
    estimatedTokens: 63
    keywords: [valuetask, task]
  - name: "CancellationToken Patterns"
    estimatedTokens: 45
    keywords: [cancellationtoken, patterns]
  - name: "IAsyncEnumerable"
    estimatedTokens: 32
    keywords: [iasyncenumerable]
  - name: "Task.WhenAll / WhenAny"
    estimatedTokens: 47
    keywords: [taskwhenall, whenany]
  - name: "Common Detection Patterns"
    estimatedTokens: 50
    keywords: [detection, patterns]
  - name: "Async Checklist"
    estimatedTokens: 45
    keywords: [async, checklist]
  - name: "Official Resources"
    estimatedTokens: 23
    keywords: [official, resources]
tags: [dotnet, async, await, cancellation, valuetask, deadlock, configureawait]
---

# Async/Await Patterns

Quick reference for async/await in .NET. For detailed examples, see [Async programming](https://learn.microsoft.com/en-us/dotnet/csharp/async).

---

## Critical Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|--------------|
| **Sync-over-async** | `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` | Use `async`/`await` all the way | [Async best practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming) |
| **Async void** | `async void` (not event handler) | Use `async Task` | [Async void handlers](https://learn.microsoft.com/en-us/dotnet/csharp/async#avoid-async-void) |
| **Missing CancellationToken** | Async method without cancellation | Add `CancellationToken` parameter | [Cancellation tokens](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads) |
| **Fire-and-forget** | `_ = SomeAsyncMethod()` | Await or use background service | [Background tasks](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/host/hosted-services) |
| **Task.Run for I/O** | `Task.Run(async () => await ...)` | Direct await (no Task.Run) | [Task.Run guidance](https://blog.stephencleary.com/2013/11/taskrun-etiquette-examples-dont-use.html) |

---

## Async Rules

| Rule | Detection Pattern | Fix |
|------|-------------------|-----|
| **Never block on async** | `.Result`, `.Wait()` in ASP.NET | Make caller `async` |
| **Never async void** | `async void Method()` not event handler | Use `async Task` |
| **Always propagate CancellationToken** | Missing `cancellationToken` in async call | Pass token through |
| **ConfigureAwait in libraries** | No `ConfigureAwait(false)` in library | Add `.ConfigureAwait(false)` |
| **Don't use Task.Run in ASP.NET** | `Task.Run` in controller | Remove Task.Run |

---

## Sync-over-Async Deadlock

```csharp
// ❌ CRITICAL - Deadlock in ASP.NET Framework, WPF, WinForms
GetDataAsync().Result;
GetDataAsync().Wait();
GetDataAsync().GetAwaiter().GetResult();

// ✅ Good - Async all the way
await GetDataAsync();

// Note: ASP.NET Core has no SynchronizationContext, so .Result won't deadlock
// BUT it's still bad practice (blocks thread pool thread)
```

[Understanding async/await deadlocks](https://blog.stephencleary.com/2012/07/dont-block-on-async-code.html)

---

## ConfigureAwait

| When to Use | When NOT to Use |
|-------------|-----------------|
| Library code | Application code |
| Class libraries | ASP.NET Core apps |
| NuGet packages | UI apps (need UI context) |
| Background services | When accessing HttpContext |

```csharp
// ✅ Library code
await _httpClient.GetAsync(url).ConfigureAwait(false);

// ✅ ASP.NET Core (no context, but ConfigureAwait(false) still ok)
await _service.GetDataAsync(); // No ConfigureAwait needed

// ❌ UI code with ConfigureAwait(false)
await GetDataAsync().ConfigureAwait(false);
TextBox.Text = data; // CRASH - not on UI thread
```

[ConfigureAwait FAQ](https://devblogs.microsoft.com/dotnet/configureawait-faq/)

---

## ValueTask vs Task

| Use Task | Use ValueTask |
|----------|---------------|
| Always async | Often synchronous (cached) |
| May await multiple times | Await once only |
| No performance constraints | Hot path optimization |

```csharp
// ✅ ValueTask for cache hits
public ValueTask<Product?> GetProductAsync(int id)
{
    if (_cache.TryGetValue(id, out var product))
        return ValueTask.FromResult(product); // No allocation

    return new ValueTask<Product?>(LoadFromDbAsync(id));
}

// ❌ Don't await ValueTask twice
var task = GetProductAsync(1);
await task;  // OK
await task;  // UNDEFINED BEHAVIOR
```

[Understanding ValueTask](https://devblogs.microsoft.com/dotnet/understanding-the-whys-whats-and-whens-of-valuetask/)

---

## CancellationToken Patterns

```csharp
// ✅ Accept and propagate
public async Task<List<Product>> GetProductsAsync(
    CancellationToken cancellationToken = default)
{
    return await _db.Products.ToListAsync(cancellationToken);
}

// ✅ Check cancellation in loops
foreach (var item in items)
{
    cancellationToken.ThrowIfCancellationRequested();
    await ProcessAsync(item, cancellationToken);
}

// ✅ ASP.NET Core automatic binding
[HttpGet]
public async Task<ActionResult> Get(CancellationToken cancellationToken)
{
    // Automatically cancelled when request aborts
}
```

[Cancellation best practices](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)

---

## IAsyncEnumerable

```csharp
// ✅ Async streaming
public async IAsyncEnumerable<Product> GetProductsStreamAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    await foreach (var product in _db.Products.AsAsyncEnumerable()
        .WithCancellation(cancellationToken))
    {
        yield return product;
    }
}

// Consumer
await foreach (var product in service.GetProductsStreamAsync())
{
    Console.WriteLine(product.Name);
}
```

[Async streams](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios#asynchronous-streams)

---

## Task.WhenAll / WhenAny

```csharp
// ✅ Parallel execution
var userTask = GetUserAsync(id);
var ordersTask = GetOrdersAsync(id);
var prefsTask = GetPreferencesAsync(id);

await Task.WhenAll(userTask, ordersTask, prefsTask);

var user = userTask.Result;      // Already completed
var orders = ordersTask.Result;  // Already completed
var prefs = prefsTask.Result;    // Already completed

// ✅ First to complete
var firstTask = await Task.WhenAny(task1, task2, task3);
var result = await firstTask;
```

[Task combinators](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.whenall)

---

## Common Detection Patterns

```csharp
// ❌ Sync-over-async
.Result
.Wait()
.GetAwaiter().GetResult()

// ❌ Async void (not event handler)
async void ProcessData()  // Should be async Task

// ❌ Missing cancellation
async Task GetDataAsync()  // Should accept CancellationToken

// ❌ Fire-and-forget
_ = SendEmailAsync();  // Errors swallowed

// ❌ Task.Run in controller
Task.Run(async () => await _service.GetAsync())

// ❌ Not awaiting async call
var task = GetDataAsync();
// Missing await
```

---

## Async Checklist

- ✅ Async all the way (no `.Result`/`.Wait()`)
- ✅ `async Task`, not `async void` (except events)
- ✅ `ConfigureAwait(false)` in libraries
- ✅ Propagate `CancellationToken`
- ✅ Use `ValueTask` for hot paths with sync completion
- ✅ Use `IAsyncEnumerable` for streaming
- ✅ Use `IAsyncDisposable` for async cleanup
- ✅ Use `Task.WhenAll` for parallelism
- ✅ Avoid fire-and-forget

---

## Official Resources

- **Async Programming**: https://learn.microsoft.com/en-us/dotnet/csharp/async
- **Task-based Async Pattern (TAP)**: https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap
- **Async Best Practices**: https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming
- **Stephen Cleary's Blog**: https://blog.stephencleary.com/

---

**Version**: 0.1.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
