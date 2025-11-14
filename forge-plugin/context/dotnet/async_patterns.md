# Async/Await Patterns

This file provides comprehensive guidance on async/await patterns in .NET, including deadlock prevention, cancellation, and performance optimization.

## Purpose

Load this file when reviewing:
- Methods with `async`/`await` keywords
- Task-returning methods
- Async event handlers
- Background services

---

## 1. Sync-over-Async (Critical Anti-Pattern)

### 1.1 The Problem

**Rule**: NEVER block on async code with `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()`.

```csharp
// ❌ CRITICAL - Deadlock in ASP.NET (pre-.NET Core 3.0) or WPF/WinForms
public ActionResult Index()
{
    var data = GetDataAsync().Result; // DEADLOCK!
    return View(data);
}

private async Task<Data> GetDataAsync()
{
    await Task.Delay(100); // Tries to resume on captured context
    return new Data();     // But context is blocked by .Result
}

// ❌ CRITICAL - .Wait() causes same deadlock
public void ProcessData()
{
    var task = GetDataAsync();
    task.Wait(); // DEADLOCK!
}

// ❌ CRITICAL - .GetAwaiter().GetResult() also deadlocks
public Data GetData()
{
    return GetDataAsync().GetAwaiter().GetResult(); // DEADLOCK!
}
```

### 1.2 Solutions

```csharp
// ✅ Solution 1: Make caller async
public async Task<ActionResult> Index()
{
    var data = await GetDataAsync();
    return View(data);
}

// ✅ Solution 2: Use ConfigureAwait(false) in library
private async Task<Data> GetDataAsync()
{
    await Task.Delay(100).ConfigureAwait(false); // Don't capture context
    return new Data();
}

// ✅ Solution 3: Modern ASP.NET Core (no SynchronizationContext)
// In ASP.NET Core 3.0+, .Result is safe but still bad practice
public ActionResult Index()
{
    var data = GetDataAsync().Result; // No deadlock, but blocks thread
    return View(data);
}

// ✅ Best: Always async all the way
public async Task<ActionResult> Index()
{
    var data = await GetDataAsync();
    return View(data);
}
```

---

## 2. Async Void

### 2.1 The Problem

**Rule**: NEVER use `async void` except for event handlers.

```csharp
// ❌ CRITICAL - async void (exceptions can't be caught)
public async void ProcessDataAsync()
{
    await Task.Delay(100);
    throw new Exception("Unhandled!"); // Crashes the application!
}

public void Caller()
{
    try
    {
        ProcessDataAsync(); // Fire-and-forget
    }
    catch (Exception ex)
    {
        // Never catches the exception!
    }
}

// ✅ Good - async Task (exceptions propagate)
public async Task ProcessDataAsync()
{
    await Task.Delay(100);
    throw new Exception("Can be caught");
}

public async Task CallerAsync()
{
    try
    {
        await ProcessDataAsync();
    }
    catch (Exception ex)
    {
        // Exception caught here
    }
}
```

### 2.2 Event Handlers Exception

```csharp
// ✅ Good - async void for event handlers (only exception)
private async void Button_Click(object sender, EventArgs e)
{
    try
    {
        await ProcessDataAsync();
    }
    catch (Exception ex)
    {
        // Handle errors in event handler
        ShowError(ex.Message);
    }
}
```

---

## 3. ConfigureAwait

### 3.1 When to Use ConfigureAwait(false)

**Rule**: Use `ConfigureAwait(false)` in library code, not in application code.

```csharp
// ✅ Good - library code
public async Task<Data> GetDataAsync()
{
    var response = await _httpClient.GetAsync(url).ConfigureAwait(false);
    var content = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
    return Parse(content);
}

// ✅ Good - ASP.NET Core controller (no need for ConfigureAwait)
[ApiController]
public class ProductsController : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<List<Product>>> GetProducts()
    {
        var products = await _productService.GetAllAsync(); // No ConfigureAwait needed
        return Ok(products);
    }
}

// ❌ Bad - ConfigureAwait(true) is redundant
await GetDataAsync().ConfigureAwait(true); // Default behavior

// ❌ Bad - ConfigureAwait in UI code (WPF/WinForms/Blazor)
private async Task LoadDataAsync()
{
    var data = await GetDataAsync().ConfigureAwait(false);
    TextBox.Text = data.ToString(); // ERROR: Not on UI thread!
}
```

**When to use `ConfigureAwait(false)`**:
- Library code (NuGet packages)
- Background services
- When you don't need to resume on original context

**When NOT to use**:
- ASP.NET Core (no SynchronizationContext)
- UI code (WPF, WinForms, Blazor)
- When you need to access HttpContext, UI controls, etc.

---

## 4. CancellationToken

### 4.1 Propagate CancellationTokens

**Best Practice**: Always accept and propagate CancellationToken.

```csharp
// ✅ Good - CancellationToken propagation
public async Task<List<Product>> GetProductsAsync(CancellationToken cancellationToken = default)
{
    var response = await _httpClient.GetAsync("/api/products", cancellationToken);
    return await response.Content.ReadFromJsonAsync<List<Product>>(cancellationToken);
}

// ✅ Good - ASP.NET Core action with cancellation
[HttpGet]
public async Task<ActionResult<List<Product>>> GetProducts(CancellationToken cancellationToken)
{
    var products = await _productService.GetAllAsync(cancellationToken);
    return Ok(products);
}

// ❌ Bad - no CancellationToken
public async Task<List<Product>> GetProductsAsync()
{
    var response = await _httpClient.GetAsync("/api/products"); // Can't cancel
    return await response.Content.ReadFromJsonAsync<List<Product>>();
}
```

### 4.2 Check for Cancellation

**Best Practice**: Check cancellation in long-running operations.

```csharp
// ✅ Good - check cancellation in loop
public async Task ProcessItemsAsync(List<Item> items, CancellationToken cancellationToken)
{
    foreach (var item in items)
    {
        cancellationToken.ThrowIfCancellationRequested(); // Check before processing
        
        await ProcessItemAsync(item, cancellationToken);
    }
}

// ✅ Good - pass token to synchronous long-running work
public async Task ProcessDataAsync(CancellationToken cancellationToken)
{
    await Task.Run(() =>
    {
        for (int i = 0; i < 1000000; i++)
        {
            if (cancellationToken.IsCancellationRequested)
                break;
            
            // Process data
        }
    }, cancellationToken);
}
```

---

## 5. Task.Run

### 5.1 When to Use Task.Run

**Rule**: Use `Task.Run` to offload CPU-bound work, not for I/O.

```csharp
// ✅ Good - CPU-bound work on thread pool
public async Task<byte[]> ProcessImageAsync(byte[] imageData)
{
    return await Task.Run(() =>
    {
        // CPU-intensive image processing
        return ImageProcessor.Resize(imageData, 800, 600);
    });
}

// ❌ Bad - Task.Run for I/O (adds unnecessary overhead)
public async Task<Data> GetDataAsync()
{
    return await Task.Run(async () =>
    {
        return await _httpClient.GetFromJsonAsync<Data>("/api/data"); // Wastes a thread
    });
}

// ✅ Good - just await I/O directly
public async Task<Data> GetDataAsync()
{
    return await _httpClient.GetFromJsonAsync<Data>("/api/data");
}
```

### 5.2 Task.Run in ASP.NET Core

**Rule**: DON'T use Task.Run in ASP.NET Core controllers.

```csharp
// ❌ Bad - Task.Run in controller
[HttpGet]
public async Task<ActionResult<Data>> GetData()
{
    var data = await Task.Run(async () =>
    {
        return await _dataService.GetDataAsync(); // Wastes thread from thread pool
    });
    return Ok(data);
}

// ✅ Good - direct await
[HttpGet]
public async Task<ActionResult<Data>> GetData()
{
    var data = await _dataService.GetDataAsync();
    return Ok(data);
}
```

---

## 6. ValueTask and ValueTask<T>

### 6.1 When to Use ValueTask

**Best Practice**: Use `ValueTask<T>` for hot paths with synchronous completion.

```csharp
// ✅ Good - ValueTask for cached results
public ValueTask<Product?> GetProductAsync(int id)
{
    if (_cache.TryGetValue(id, out var product))
    {
        return ValueTask.FromResult(product); // Synchronous, no allocation
    }
    
    return new ValueTask<Product?>(LoadProductAsync(id)); // Async path
}

private async Task<Product?> LoadProductAsync(int id)
{
    var product = await _dbContext.Products.FindAsync(id);
    _cache[id] = product;
    return product;
}

// ❌ Bad - ValueTask for always-async operations
public ValueTask<Product> GetProductAsync(int id)
{
    return new ValueTask<Product>(_dbContext.Products.FindAsync(id)); // Always async, just use Task
}
```

### 6.2 ValueTask Restrictions

**Critical**: Don't await ValueTask multiple times.

```csharp
// ❌ CRITICAL - awaiting ValueTask twice
var task = GetProductAsync(1);
var product1 = await task;
var product2 = await task; // UNDEFINED BEHAVIOR!

// ✅ Good - await once
var product = await GetProductAsync(1);

// ✅ Good - convert to Task if needed multiple times
var task = GetProductAsync(1).AsTask();
var product1 = await task;
var product2 = await task;
```

---

## 7. IAsyncEnumerable<T>

### 7.1 Async Streaming

**Best Practice**: Use `IAsyncEnumerable<T>` for streaming data.

```csharp
// ✅ Good - async streaming
public async IAsyncEnumerable<Product> GetProductsStreamAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    await foreach (var product in _dbContext.Products.AsAsyncEnumerable()
        .WithCancellation(cancellationToken))
    {
        yield return product;
    }
}

// Consumer
await foreach (var product in productService.GetProductsStreamAsync())
{
    Console.WriteLine(product.Name);
}
```

---

## 8. Async Disposal

### 8.1 IAsyncDisposable

**Best Practice**: Implement `IAsyncDisposable` for async cleanup.

```csharp
// ✅ Good - IAsyncDisposable
public class AsyncResource : IAsyncDisposable
{
    private readonly HttpClient _httpClient;
    
    public async ValueTask DisposeAsync()
    {
        // Async cleanup
        await _httpClient.DeleteAsync("/api/sessions/close");
        _httpClient.Dispose();
    }
}

// Usage with await using
await using var resource = new AsyncResource();
```

---

## 9. Parallel Async Operations

### 9.1 Task.WhenAll

**Best Practice**: Use `Task.WhenAll` for concurrent operations.

```csharp
// ✅ Good - parallel execution
public async Task<(User user, Orders orders, Preferences prefs)> GetUserDataAsync(int userId)
{
    var userTask = _userService.GetUserAsync(userId);
    var ordersTask = _orderService.GetOrdersAsync(userId);
    var prefsTask = _preferenceService.GetPreferencesAsync(userId);
    
    await Task.WhenAll(userTask, ordersTask, prefsTask);
    
    return (userTask.Result, ordersTask.Result, prefsTask.Result);
}

// ❌ Bad - sequential execution
public async Task<(User user, Orders orders, Preferences prefs)> GetUserDataAsync(int userId)
{
    var user = await _userService.GetUserAsync(userId); // Wait
    var orders = await _orderService.GetOrdersAsync(userId); // Wait
    var prefs = await _preferenceService.GetPreferencesAsync(userId); // Wait
    
    return (user, orders, prefs);
}
```

### 9.2 Parallel Processing with Throttling

**Best Practice**: Limit concurrency for resource-intensive operations.

```csharp
// ✅ Good - throttled parallel processing
public async Task ProcessItemsAsync(List<Item> items)
{
    var semaphore = new SemaphoreSlim(10); // Max 10 concurrent
    
    var tasks = items.Select(async item =>
    {
        await semaphore.WaitAsync();
        try
        {
            await ProcessItemAsync(item);
        }
        finally
        {
            semaphore.Release();
        }
    });
    
    await Task.WhenAll(tasks);
}
```

---

## 10. Fire-and-Forget

### 10.1 Avoiding Fire-and-Forget

**Best Practice**: Don't fire-and-forget unless absolutely necessary.

```csharp
// ❌ Bad - fire-and-forget
public void ProcessOrder(Order order)
{
    _ = SendEmailAsync(order); // Exceptions swallowed, no tracking
}

// ✅ Good - await the task
public async Task ProcessOrderAsync(Order order)
{
    await SendEmailAsync(order);
}

// ✅ Acceptable - fire-and-forget with error handling
public void ProcessOrder(Order order)
{
    _ = SendEmailWithErrorHandlingAsync(order);
}

private async Task SendEmailWithErrorHandlingAsync(Order order)
{
    try
    {
        await _emailService.SendAsync(order);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Failed to send email for order {OrderId}", order.Id);
    }
}
```

---

## Async/Await Checklist

1. **Sync-over-Async**: ✅ Never use .Result, .Wait(), or .GetAwaiter().GetResult()
2. **Async Void**: ✅ Never use async void (except event handlers)
3. **ConfigureAwait**: ✅ Use ConfigureAwait(false) in library code
4. **CancellationToken**: ✅ Accept and propagate CancellationToken
5. **Task.Run**: ✅ Only for CPU-bound work, not I/O
6. **ValueTask**: ✅ Use for hot paths with sync completion
7. **IAsyncEnumerable**: ✅ Use for streaming data
8. **IAsyncDisposable**: ✅ Implement for async cleanup
9. **Task.WhenAll**: ✅ Use for parallel operations
10. **Fire-and-Forget**: ✅ Avoid or handle errors properly

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
