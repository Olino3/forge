# .NET Common Issues

This file documents **universal .NET problems** that apply to all .NET projects, regardless of framework type, version, or architecture.

## Purpose

**Always load this file** during .NET code reviews. It contains the most frequent and critical issues found in .NET codebases:

- Async/await anti-patterns causing deadlocks
- IDisposable resource leaks
- LINQ performance pitfalls
- Exception handling mistakes
- String performance issues
- Nullable reference type misuse
- Collection inefficiencies
- Memory leaks

These issues are framework-agnostic and represent fundamental .NET programming errors.

---

## 1. Async/Await Anti-Patterns

### 1.1 Sync-over-Async (Blocking on Async Code)

**Problem**: Calling `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` on async operations causes **deadlocks in ASP.NET and UI apps**.

**❌ Bad**:
```csharp
// DEADLOCK RISK in ASP.NET Core / WPF / WinForms
public IActionResult GetProducts()
{
    var products = _productService.GetAllAsync().Result; // ⚠️ DEADLOCK!
    return Ok(products);
}

public void OnButtonClick()
{
    var data = FetchDataAsync().Wait(); // ⚠️ DEADLOCK!
}

// Also dangerous
var result = SomeAsyncMethod().GetAwaiter().GetResult(); // ⚠️ DEADLOCK!
```

**✅ Good**:
```csharp
// Async all the way
public async Task<IActionResult> GetProducts()
{
    var products = await _productService.GetAllAsync();
    return Ok(products);
}

public async Task OnButtonClick()
{
    var data = await FetchDataAsync();
}
```

**Why**: Sync-over-async captures the synchronization context, causing a deadlock when the continuation tries to resume on the blocked thread.

**Exception**: Console applications (.NET 5+) have no synchronization context, so blocking on async is less dangerous but still not recommended.

**Detection**:
- Search for `.Result` on Task/Task<T>
- Search for `.Wait()` on Task/Task<T>
- Search for `.GetAwaiter().GetResult()`

**Severity**: 🔴 **CRITICAL** (causes production deadlocks)

---

### 1.2 Async Void (Except Event Handlers)

**Problem**: `async void` methods can't be awaited, making error handling impossible and causing unhandled exceptions.

**❌ Bad**:
```csharp
public async void ProcessData() // ⚠️ Exceptions can't be caught!
{
    await _service.ProcessAsync();
    throw new Exception("This will crash the app!");
}

// Caller can't await or catch exceptions
ProcessData(); // Fire and forget, no error handling
```

**✅ Good**:
```csharp
// Use async Task
public async Task ProcessDataAsync()
{
    await _service.ProcessAsync();
}

// Caller can await and handle errors
try
{
    await ProcessDataAsync();
}
catch (Exception ex)
{
    _logger.LogError(ex, "Processing failed");
}
```

**Exception**: Event handlers MUST be `async void`:
```csharp
// This is correct for event handlers
private async void Button_Click(object sender, EventArgs e)
{
    try
    {
        await ProcessDataAsync();
    }
    catch (Exception ex)
    {
        // Handle exceptions within the event handler
    }
}
```

**Detection**:
- Search for `async void` methods
- Verify they are event handlers (parameters: `object sender, EventArgs e`)
- Flag any non-event-handler `async void` methods

**Severity**: 🔴 **CRITICAL** (unhandled exceptions crash the app)

---

### 1.3 Missing ConfigureAwait in Library Code

**Problem**: Not using `ConfigureAwait(false)` in library code can cause deadlocks when consumed by ASP.NET or UI apps.

**❌ Bad** (in library code):
```csharp
// Library method
public async Task<string> FetchDataAsync()
{
    var response = await _httpClient.GetAsync(url); // ⚠️ Captures sync context
    return await response.Content.ReadAsStringAsync(); // ⚠️ Can cause deadlock
}
```

**✅ Good** (in library code):
```csharp
public async Task<string> FetchDataAsync()
{
    var response = await _httpClient.GetAsync(url).ConfigureAwait(false);
    return await response.Content.ReadAsStringAsync().ConfigureAwait(false);
}
```

**Note**: In **ASP.NET Core**, there is NO synchronization context, so `ConfigureAwait(false)` is technically not needed. However, it's still good practice for library code that might be consumed by other frameworks.

**When to use**:
- ✅ Always in library code
- ✅ Always in .NET Framework ASP.NET or WinForms/WPF
- ⚠️ Optional in ASP.NET Core (but still recommended for libraries)
- ❌ Not needed in application code that doesn't need to resume on original context

**Detection**:
- Check if code is in a library project
- Look for `await` without `.ConfigureAwait(false)`

**Severity**: 🟡 **MEDIUM** (can cause issues in specific contexts)

---

### 1.4 Fire-and-Forget Patterns

**Problem**: Starting async operations without awaiting them can lead to unhandled exceptions and incomplete operations.

**❌ Bad**:
```csharp
public void ProcessOrder(Order order)
{
    // Fire and forget - no error handling, no completion tracking
    _ = _orderService.ProcessAsync(order); // ⚠️ Dangerous!
}
```

**✅ Good**:
```csharp
public async Task ProcessOrder(Order order)
{
    try
    {
        await _orderService.ProcessAsync(order);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Order processing failed");
        throw;
    }
}

// Or use background service for true fire-and-forget
public void ProcessOrder(Order order)
{
    _backgroundTaskQueue.QueueBackgroundWorkItem(async token =>
    {
        try
        {
            await _orderService.ProcessAsync(order);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Background order processing failed");
        }
    });
}
```

**Detection**:
- Look for `_ = SomeAsyncMethod()` patterns
- Look for async methods called without `await`
- Check for `#pragma warning disable CS4014` (disabling async warnings)

**Severity**: 🟠 **HIGH** (can lose operations and errors)

---

### 1.5 CancellationToken Not Propagated

**Problem**: Not passing `CancellationToken` through async call chains prevents graceful cancellation.

**❌ Bad**:
```csharp
public async Task<Product> GetProductAsync(int id, CancellationToken cancellationToken)
{
    // CancellationToken not passed to database call
    var product = await _context.Products.FirstOrDefaultAsync(p => p.Id == id);
    return product;
}
```

**✅ Good**:
```csharp
public async Task<Product> GetProductAsync(int id, CancellationToken cancellationToken)
{
    var product = await _context.Products
        .FirstOrDefaultAsync(p => p.Id == id, cancellationToken);
    return product;
}
```

**Detection**:
- Method has `CancellationToken` parameter
- Async method calls inside don't pass it along

**Severity**: 🟡 **MEDIUM** (prevents request cancellation)

---

## 2. IDisposable Resource Leaks

### 2.1 Missing Using Statements

**Problem**: Not disposing `IDisposable` resources causes memory leaks, file handle leaks, and connection leaks.

**❌ Bad**:
```csharp
public void ReadFile(string path)
{
    var stream = new FileStream(path, FileMode.Open); // ⚠️ LEAK!
    // File handle never closed
}

public async Task<string> CallApiAsync()
{
    var client = new HttpClient(); // ⚠️ SOCKET LEAK!
    return await client.GetStringAsync(url);
}
```

**✅ Good**:
```csharp
public void ReadFile(string path)
{
    using var stream = new FileStream(path, FileMode.Open); // C# 8+ syntax
    // Stream disposed automatically
}

// Or traditional syntax
public void ReadFile(string path)
{
    using (var stream = new FileStream(path, FileMode.Open))
    {
        // Stream disposed at end of block
    }
}

// For HttpClient, use IHttpClientFactory (DI)
public class MyService
{
    private readonly HttpClient _httpClient;

    public MyService(IHttpClientFactory httpClientFactory)
    {
        _httpClient = httpClientFactory.CreateClient();
    }

    public async Task<string> CallApiAsync()
    {
        return await _httpClient.GetStringAsync(url);
    }
}
```

**Common IDisposable Types**:
- `FileStream`, `StreamReader`, `StreamWriter`
- `HttpClient` (use IHttpClientFactory instead)
- `DbContext`, `DbConnection`, `DbCommand`
- `SqlConnection`, `SqlCommand`, `SqlDataReader`
- `Timer`, `CancellationTokenSource`
- `Bitmap`, `Image`, `Graphics`
- `MemoryStream`, `BufferedStream`
- `HttpResponseMessage`, `HttpContent`

**Detection**:
- Look for `new` instantiation of IDisposable types without `using`
- Check for `Dispose()` not being called
- Look for `HttpClient` being created per request

**Severity**: 🔴 **CRITICAL** (causes memory and resource leaks)

---

### 2.2 Not Implementing IDisposable for Managed Resources

**Problem**: Classes that hold IDisposable resources should implement IDisposable themselves.

**❌ Bad**:
```csharp
public class DataRepository // ⚠️ Should implement IDisposable
{
    private readonly FileStream _logStream = new FileStream("log.txt", FileMode.Append);

    public void WriteLog(string message)
    {
        // _logStream never disposed
    }
}
```

**✅ Good**:
```csharp
public class DataRepository : IDisposable
{
    private readonly FileStream _logStream = new FileStream("log.txt", FileMode.Append);
    private bool _disposed = false;

    public void WriteLog(string message)
    {
        if (_disposed) throw new ObjectDisposedException(nameof(DataRepository));
        // Use stream
    }

    public void Dispose()
    {
        if (_disposed) return;

        _logStream?.Dispose();
        _disposed = true;
    }
}
```

**Best Practice**: Use dependency injection for DbContext and other IDisposable services instead of manual management.

**Detection**:
- Class has private fields of IDisposable types
- Class does not implement IDisposable

**Severity**: 🟠 **HIGH** (resource leaks)

---

### 2.3 Dispose Not Called in Finally Block

**Problem**: If an exception occurs before `Dispose()`, resources leak.

**❌ Bad**:
```csharp
public void ProcessFile(string path)
{
    var stream = new FileStream(path, FileMode.Open);
    // If exception here, stream never closed
    ProcessData(stream);
    stream.Dispose();
}
```

**✅ Good**:
```csharp
public void ProcessFile(string path)
{
    FileStream stream = null;
    try
    {
        stream = new FileStream(path, FileMode.Open);
        ProcessData(stream);
    }
    finally
    {
        stream?.Dispose();
    }
}

// Better: use using statement
public void ProcessFile(string path)
{
    using var stream = new FileStream(path, FileMode.Open);
    ProcessData(stream);
}
```

**Detection**:
- Dispose() called outside try-finally
- Missing using statement

**Severity**: 🟠 **HIGH** (resource leaks on exception)

---

## 3. LINQ Pitfalls

### 3.1 Deferred Execution Misunderstanding

**Problem**: LINQ queries don't execute until enumerated, leading to unexpected behavior.

**❌ Bad**:
```csharp
public IEnumerable<Product> GetActiveProducts()
{
    // Query not executed yet
    var query = _context.Products.Where(p => p.IsActive);

    // DbContext disposed here (if scoped)
    return query; // ⚠️ Query executes AFTER DbContext is disposed!
}
```

**✅ Good**:
```csharp
public async Task<List<Product>> GetActiveProductsAsync()
{
    // Execute query immediately
    return await _context.Products
        .Where(p => p.IsActive)
        .ToListAsync();
}
```

**Detection**:
- Returning `IEnumerable<T>` or `IQueryable<T>` from methods with scoped resources
- Not materializing queries with `.ToList()`, `.ToArray()`, `.ToDictionary()`

**Severity**: 🟠 **HIGH** (runtime errors)

---

### 3.2 Multiple Enumeration

**Problem**: Enumerating `IEnumerable<T>` multiple times can be expensive or cause side effects.

**❌ Bad**:
```csharp
public void ProcessProducts(IEnumerable<Product> products)
{
    // First enumeration - hits database
    var count = products.Count();

    // Second enumeration - hits database AGAIN!
    foreach (var product in products)
    {
        // Process
    }

    // Third enumeration - hits database AGAIN!
    var firstProduct = products.First();
}
```

**✅ Good**:
```csharp
public void ProcessProducts(IEnumerable<Product> products)
{
    // Materialize once
    var productList = products.ToList();

    var count = productList.Count; // No re-query
    foreach (var product in productList) // No re-query
    {
        // Process
    }
    var firstProduct = productList.First(); // No re-query
}
```

**Detection**:
- `IEnumerable<T>` parameter or variable
- Multiple uses of the same variable (Count, Any, foreach, First, etc.)
- Especially dangerous with `IQueryable<T>` from EF Core (multiple database hits)

**Severity**: 🟠 **HIGH** (performance issue, especially with databases)

---

### 3.3 N+1 Queries with Entity Framework

**Problem**: Lazy loading or accessing navigation properties in loops causes N+1 database queries.

**❌ Bad**:
```csharp
public async Task<List<OrderDto>> GetOrdersAsync()
{
    var orders = await _context.Orders.ToListAsync(); // 1 query

    var result = new List<OrderDto>();
    foreach (var order in orders) // N queries!
    {
        result.Add(new OrderDto
        {
            OrderId = order.Id,
            CustomerName = order.Customer.Name // ⚠️ N+1 problem!
        });
    }
    return result;
}
```

**✅ Good**:
```csharp
public async Task<List<OrderDto>> GetOrdersAsync()
{
    // Single query with eager loading
    return await _context.Orders
        .Include(o => o.Customer)
        .Select(o => new OrderDto
        {
            OrderId = o.Id,
            CustomerName = o.Customer.Name
        })
        .ToListAsync();
}
```

**Detection**:
- `foreach` loop with database entities
- Accessing navigation properties without `.Include()`
- Missing `.Select()` projections

**Severity**: 🔴 **CRITICAL** (performance disaster)

---

### 3.4 Inefficient Query Patterns

**Problem**: Using `.Count() > 0` instead of `.Any()`, or inefficient filtering.

**❌ Bad**:
```csharp
// Loads entire collection to count
if (products.Count() > 0) { }

// Filters after loading
var activeProducts = products.ToList().Where(p => p.IsActive);

// Loads all data before taking
var firstTen = products.ToList().Take(10);
```

**✅ Good**:
```csharp
// Efficient existence check
if (await products.AnyAsync()) { }

// Filter before materializing
var activeProducts = await products.Where(p => p.IsActive).ToListAsync();

// Take before materializing
var firstTen = await products.Take(10).ToListAsync();
```

**Detection**:
- `.Count() > 0` or `.Count() >= 1` → Use `.Any()`
- `.Where().Count() > 0` → Use `.Any(predicate)`
- `.ToList()` before `.Where()`, `.Take()`, `.Skip()`

**Severity**: 🟡 **MEDIUM** (performance issue)

---

## 4. Exception Handling Mistakes

### 4.1 Swallowing Exceptions

**Problem**: Catching exceptions without logging or rethrowing hides errors.

**❌ Bad**:
```csharp
try
{
    await ProcessDataAsync();
}
catch (Exception ex)
{
    // ⚠️ Exception silently ignored!
}
```

**✅ Good**:
```csharp
try
{
    await ProcessDataAsync();
}
catch (Exception ex)
{
    _logger.LogError(ex, "Failed to process data");
    throw; // Rethrow to propagate
}

// Or handle and return error
catch (Exception ex)
{
    _logger.LogError(ex, "Failed to process data");
    return Result.Failure(ex.Message);
}
```

**Detection**:
- Empty catch blocks
- Catch blocks without logging or rethrowing

**Severity**: 🟠 **HIGH** (hides bugs)

---

### 4.2 Throwing System.Exception

**Problem**: Throwing generic exceptions makes error handling difficult.

**❌ Bad**:
```csharp
if (product == null)
{
    throw new Exception("Product not found"); // ⚠️ Too generic
}
```

**✅ Good**:
```csharp
if (product == null)
{
    throw new ProductNotFoundException($"Product with ID {id} not found");
}

// Or use built-in exceptions
if (id <= 0)
{
    throw new ArgumentException("ID must be positive", nameof(id));
}

if (product == null)
{
    throw new InvalidOperationException("Product not found");
}
```

**Detection**:
- `throw new Exception(...)` statements
- Not using specific exception types

**Severity**: 🟡 **MEDIUM** (makes error handling harder)

---

### 4.3 Catching Too Broad

**Problem**: Catching all exceptions can hide specific errors that should be handled differently.

**❌ Bad**:
```csharp
try
{
    await _dbContext.SaveChangesAsync();
}
catch (Exception ex) // ⚠️ Catches everything, including OutOfMemoryException!
{
    _logger.LogError(ex, "Database error");
}
```

**✅ Good**:
```csharp
try
{
    await _dbContext.SaveChangesAsync();
}
catch (DbUpdateConcurrencyException ex)
{
    // Handle concurrency conflict
    _logger.LogWarning(ex, "Concurrency conflict");
    throw;
}
catch (DbUpdateException ex)
{
    // Handle database update error
    _logger.LogError(ex, "Database update failed");
    throw;
}
```

**Detection**:
- `catch (Exception ex)` without rethrowing
- Not catching specific exception types

**Severity**: 🟡 **MEDIUM** (can hide critical errors)

---

## 5. String Performance Issues

### 5.1 String Concatenation in Loops

**Problem**: String concatenation creates new strings on each iteration, wasting memory.

**❌ Bad**:
```csharp
string result = "";
foreach (var item in items)
{
    result += item.ToString(); // ⚠️ Creates new string each time
}
```

**✅ Good**:
```csharp
var sb = new StringBuilder();
foreach (var item in items)
{
    sb.Append(item.ToString());
}
string result = sb.ToString();
```

**Detection**:
- `+=` on strings inside loops
- Repeated concatenation with `+`

**Severity**: 🟡 **MEDIUM** (performance issue with large data)

---

### 5.2 String Comparison Without StringComparison

**Problem**: Not specifying `StringComparison` can cause culture-specific issues.

**❌ Bad**:
```csharp
if (username.ToLower() == "admin") // ⚠️ Culture-dependent, slow
{
    // Grant access
}
```

**✅ Good**:
```csharp
if (username.Equals("admin", StringComparison.OrdinalIgnoreCase))
{
    // Culture-independent, faster
}

// Or
if (string.Equals(username, "admin", StringComparison.OrdinalIgnoreCase))
{
    // Culture-independent, faster
}
```

**Detection**:
- `.ToLower()` or `.ToUpper()` for comparison
- String comparison without `StringComparison` parameter

**Severity**: 🟡 **MEDIUM** (culture issues, performance)

---

## 6. Nullable Reference Types (C# 8+)

### 6.1 Null-Forgiving Operator Misuse

**Problem**: Using `!` (null-forgiving operator) suppresses warnings without null checks.

**❌ Bad**:
```csharp
public void ProcessUser(User? user)
{
    // Suppressing warning without validation
    var name = user!.Name; // ⚠️ NullReferenceException if user is null!
}
```

**✅ Good**:
```csharp
public void ProcessUser(User? user)
{
    if (user == null)
    {
        throw new ArgumentNullException(nameof(user));
    }

    var name = user.Name; // Safe, compiler knows user is not null
}

// Or use null-conditional operator
public void ProcessUser(User? user)
{
    var name = user?.Name ?? "Unknown";
}
```

**Detection**:
- `!` operator usage
- Missing null checks before `!`

**Severity**: 🟠 **HIGH** (potential NullReferenceException)

---

### 6.2 Missing Null Checks

**Problem**: Not checking for null on nullable parameters or fields.

**❌ Bad**:
```csharp
public int GetLength(string? input)
{
    return input.Length; // ⚠️ NullReferenceException if input is null
}
```

**✅ Good**:
```csharp
public int GetLength(string? input)
{
    if (input == null)
    {
        throw new ArgumentNullException(nameof(input));
    }
    return input.Length;
}

// Or use null-conditional
public int? GetLength(string? input)
{
    return input?.Length;
}
```

**Detection**:
- Methods with nullable parameters (`?`)
- Accessing members without null checks

**Severity**: 🟠 **HIGH** (potential NullReferenceException)

---

## 7. Collection Misuse

### 7.1 Wrong Collection Type

**Problem**: Using inefficient collection types for the use case.

**❌ Bad**:
```csharp
// Using List for lookups (O(n) search)
var userList = new List<User>();
var user = userList.FirstOrDefault(u => u.Id == targetId); // Slow!

// Using List for uniqueness checks
if (!userList.Contains(newUser)) // O(n)
{
    userList.Add(newUser);
}
```

**✅ Good**:
```csharp
// Use Dictionary for lookups (O(1) search)
var userDict = new Dictionary<int, User>();
var user = userDict.TryGetValue(targetId, out var foundUser) ? foundUser : null;

// Use HashSet for uniqueness (O(1) contains)
var userSet = new HashSet<User>();
userSet.Add(newUser); // Automatically handles duplicates
```

**Collection Guide**:
- `List<T>`: Ordered, allow duplicates, indexed access
- `HashSet<T>`: Unordered, unique items, fast Contains()
- `Dictionary<K, V>`: Key-value pairs, fast lookup by key
- `Queue<T>`: FIFO operations
- `Stack<T>`: LIFO operations

**Severity**: 🟡 **MEDIUM** (performance issue)

---

### 7.2 Not Specifying Capacity

**Problem**: Collections grow by reallocating, wasting memory and CPU.

**❌ Bad**:
```csharp
var list = new List<int>(); // Default capacity: 4, then doubles
for (int i = 0; i < 10000; i++)
{
    list.Add(i); // Multiple reallocations
}
```

**✅ Good**:
```csharp
var list = new List<int>(10000); // Pre-allocate
for (int i = 0; i < 10000; i++)
{
    list.Add(i); // No reallocations
}
```

**Detection**:
- Collection initialized without capacity
- Large loops adding items

**Severity**: 🟡 **MEDIUM** (performance issue for large collections)

---

## 8. Memory Leaks

### 8.1 Event Handler Leaks

**Problem**: Not unsubscribing from events keeps objects alive.

**❌ Bad**:
```csharp
public class Subscriber
{
    public Subscriber(Publisher publisher)
    {
        publisher.SomethingHappened += OnSomethingHappened; // ⚠️ LEAK!
    }

    private void OnSomethingHappened(object sender, EventArgs e)
    {
        // Handle event
    }

    // No unsubscribe = Subscriber never garbage collected
}
```

**✅ Good**:
```csharp
public class Subscriber : IDisposable
{
    private readonly Publisher _publisher;

    public Subscriber(Publisher publisher)
    {
        _publisher = publisher;
        _publisher.SomethingHappened += OnSomethingHappened;
    }

    private void OnSomethingHappened(object sender, EventArgs e)
    {
        // Handle event
    }

    public void Dispose()
    {
        _publisher.SomethingHappened -= OnSomethingHappened; // Unsubscribe
    }
}
```

**Detection**:
- `+=` to events without corresponding `-=`
- Missing Dispose() when subscribing to events

**Severity**: 🟠 **HIGH** (memory leak)

---

### 8.2 Static References Keeping Objects Alive

**Problem**: Static fields hold references indefinitely, preventing garbage collection.

**❌ Bad**:
```csharp
public static class Cache
{
    private static readonly List<User> _users = new List<User>(); // ⚠️ LEAK!

    public static void AddUser(User user)
    {
        _users.Add(user); // Never removed, grows forever
    }
}
```

**✅ Good**:
```csharp
public class CacheService
{
    private readonly IMemoryCache _cache;

    public CacheService(IMemoryCache cache)
    {
        _cache = cache;
    }

    public void AddUser(User user)
    {
        _cache.Set($"user_{user.Id}", user, TimeSpan.FromMinutes(30)); // Expires
    }
}
```

**Detection**:
- Static collections that grow
- Static fields holding references to large objects

**Severity**: 🟠 **HIGH** (memory leak)

---

### 8.3 Timer Not Disposed

**Problem**: Timers hold references and keep objects alive.

**❌ Bad**:
```csharp
public class Worker
{
    private readonly System.Timers.Timer _timer = new System.Timers.Timer(1000);

    public Worker()
    {
        _timer.Elapsed += OnTimerElapsed;
        _timer.Start();
    }

    private void OnTimerElapsed(object sender, ElapsedEventArgs e)
    {
        // Do work
    }

    // ⚠️ Timer never disposed = memory leak
}
```

**✅ Good**:
```csharp
public class Worker : IDisposable
{
    private readonly System.Timers.Timer _timer = new System.Timers.Timer(1000);

    public Worker()
    {
        _timer.Elapsed += OnTimerElapsed;
        _timer.Start();
    }

    private void OnTimerElapsed(object sender, ElapsedEventArgs e)
    {
        // Do work
    }

    public void Dispose()
    {
        _timer?.Dispose();
    }
}
```

**Detection**:
- Timer instantiation without Dispose()
- Missing IDisposable implementation for classes with Timers

**Severity**: 🟠 **HIGH** (memory leak)

---

## Summary: Always Check For

1. **Async/Await**:
   - ✅ Async all the way (no `.Result`, `.Wait()`)
   - ✅ `async Task`, not `async void` (except event handlers)
   - ✅ `ConfigureAwait(false)` in library code
   - ✅ `CancellationToken` propagated

2. **IDisposable**:
   - ✅ `using` statements for all IDisposable types
   - ✅ HttpClient via IHttpClientFactory
   - ✅ IDisposable implemented for classes with resources

3. **LINQ**:
   - ✅ Materialize queries (`.ToList()`) before returning
   - ✅ Avoid multiple enumeration
   - ✅ Use `.Include()` to prevent N+1 queries
   - ✅ Use `.Any()` instead of `.Count() > 0`

4. **Exceptions**:
   - ✅ Log before rethrowing
   - ✅ Use specific exception types
   - ✅ Catch specific exceptions, not `Exception`

5. **Strings**:
   - ✅ StringBuilder in loops
   - ✅ StringComparison for comparisons

6. **Nullable**:
   - ✅ Validate before using `!`
   - ✅ Null checks on nullable parameters

7. **Collections**:
   - ✅ Right collection type for use case
   - ✅ Specify capacity for large collections

8. **Memory**:
   - ✅ Unsubscribe from events
   - ✅ Avoid static references to large objects
   - ✅ Dispose timers

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
