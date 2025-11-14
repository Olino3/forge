# .NET Performance Optimization Patterns

This file documents performance optimization techniques specific to .NET applications, including memory management, caching, and resource pooling.

## Purpose

Load this file when reviewing:
- Performance-critical code
- High-throughput applications
- Memory-intensive operations
- Caching implementations

---

## 1. String Performance

### 1.1 StringBuilder for Concatenation

**Rule**: Use StringBuilder for string concatenation in loops.

```csharp
// ❌ CRITICAL - string concatenation in loop
public string BuildReport(List<Item> items)
{
    string result = "";
    foreach (var item in items)
    {
        result += $"{item.Name}: {item.Value}\n"; // Creates new string each iteration
    }
    return result;
}
// Creates 1000 strings for 1000 items = massive allocations

// ✅ Good - StringBuilder
public string BuildReport(List<Item> items)
{
    var sb = new StringBuilder(items.Count * 50); // Pre-allocate capacity
    foreach (var item in items)
    {
        sb.AppendLine($"{item.Name}: {item.Value}");
    }
    return sb.ToString();
}
```

### 1.2 String Comparison

**Best Practice**: Use StringComparison for culture-aware comparisons.

```csharp
// ✅ Good - explicit StringComparison
if (name.Equals("admin", StringComparison.OrdinalIgnoreCase))
{
    // Case-insensitive comparison
}

// ❌ Bad - culture-dependent comparison
if (name.ToLower() == "admin") // Allocates new string + culture-dependent
{
}
```

### 1.3 String Interning

**Best Practice**: Understand string interning for repeated strings.

```csharp
// ✅ Understanding string interning
string s1 = "hello";
string s2 = "hello";
Console.WriteLine(ReferenceEquals(s1, s2)); // True - same reference (interned)

string s3 = new string("hello".ToCharArray());
Console.WriteLine(ReferenceEquals(s1, s3)); // False - different reference

string s4 = string.Intern(s3);
Console.WriteLine(ReferenceEquals(s1, s4)); // True - interned
```

---

## 2. Collections Performance

### 2.1 Specify Capacity

**Best Practice**: Set initial capacity for collections when size is known.

```csharp
// ✅ Good - pre-allocate capacity
public List<Product> ProcessProducts(int count)
{
    var results = new List<Product>(count); // Avoid resizing
    for (int i = 0; i < count; i++)
    {
        results.Add(new Product());
    }
    return results;
}

// ❌ Bad - default capacity (multiple reallocations)
public List<Product> ProcessProducts(int count)
{
    var results = new List<Product>(); // Default capacity = 4, resizes multiple times
    for (int i = 0; i < count; i++)
    {
        results.Add(new Product());
    }
    return results;
}
```

### 2.2 Choose Right Collection Type

**Best Practice**: Use appropriate collection for your access pattern.

```csharp
// ✅ Good - List<T> for sequential access
var items = new List<Product>(); // Fast iteration, indexed access

// ✅ Good - Dictionary<TKey, TValue> for key-based lookup
var productById = new Dictionary<int, Product>(); // O(1) lookup

// ✅ Good - HashSet<T> for uniqueness checks
var uniqueIds = new HashSet<int>(); // O(1) Contains

// ❌ Bad - List with Contains for lookups
var ids = new List<int>();
if (ids.Contains(productId)) // O(n) - scans entire list
{
}
```

### 2.3 Collection Reuse

**Best Practice**: Reuse collections instead of creating new ones.

```csharp
// ✅ Good - clear and reuse
private readonly List<Product> _buffer = new(1000);

public void ProcessBatch(IEnumerable<Product> products)
{
    _buffer.Clear(); // Reuse allocation
    _buffer.AddRange(products);
    // Process buffer
}

// ❌ Bad - create new list each time
public void ProcessBatch(IEnumerable<Product> products)
{
    var buffer = new List<Product>(); // New allocation every call
    buffer.AddRange(products);
    // Process buffer
}
```

---

## 3. Memory Optimization

### 3.1 Span<T> and Memory<T>

**Best Practice**: Use Span<T> for zero-allocation slicing.

```csharp
// ✅ Good - Span<T> (no allocation)
public void ProcessArray(int[] data)
{
    Span<int> span = data.AsSpan();
    Span<int> slice = span.Slice(10, 20); // No allocation, just pointer + length
    
    for (int i = 0; i < slice.Length; i++)
    {
        slice[i] *= 2;
    }
}

// ❌ Bad - LINQ on array (allocates)
public void ProcessArray(int[] data)
{
    var slice = data.Skip(10).Take(20).ToArray(); // Allocates new array
    
    for (int i = 0; i < slice.Length; i++)
    {
        slice[i] *= 2;
    }
}
```

### 3.2 ArrayPool<T>

**Best Practice**: Use ArrayPool for temporary arrays.

```csharp
// ✅ Good - ArrayPool (reuses arrays)
public byte[] ProcessData(byte[] input)
{
    byte[] buffer = ArrayPool<byte>.Shared.Rent(4096);
    try
    {
        // Use buffer
        Array.Copy(input, buffer, input.Length);
        // Process buffer
        return buffer.Take(input.Length).ToArray();
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}

// ❌ Bad - new array allocation
public byte[] ProcessData(byte[] input)
{
    byte[] buffer = new byte[4096]; // Allocates every time
    Array.Copy(input, buffer, input.Length);
    return buffer;
}
```

### 3.3 ObjectPool<T>

**Best Practice**: Pool expensive objects for reuse.

```csharp
// ✅ Good - ObjectPool
using Microsoft.Extensions.ObjectPool;

public class ExpensiveObjectPool
{
    private readonly ObjectPool<ExpensiveObject> _pool;
    
    public ExpensiveObjectPool()
    {
        var policy = new DefaultPooledObjectPolicy<ExpensiveObject>();
        _pool = new DefaultObjectPool<ExpensiveObject>(policy, maxRetained: 100);
    }
    
    public void ProcessRequest()
    {
        var obj = _pool.Get();
        try
        {
            // Use object
            obj.Process();
        }
        finally
        {
            _pool.Return(obj);
        }
    }
}

// ❌ Bad - create new expensive object every request
public void ProcessRequest()
{
    var obj = new ExpensiveObject(); // Heavy construction cost
    obj.Process();
}
```

---

## 4. Boxing and Unboxing

### 4.1 Avoid Boxing

**Rule**: Avoid boxing value types to object.

```csharp
// ❌ Bad - boxing
int value = 42;
object obj = value; // Boxing - heap allocation
int unboxed = (int)obj; // Unboxing

// ✅ Good - generic method (no boxing)
public void LogValue<T>(T value)
{
    Console.WriteLine(value);
}

LogValue(42); // No boxing

// ❌ Bad - non-generic method causes boxing
public void LogValue(object value)
{
    Console.WriteLine(value);
}

LogValue(42); // Boxing occurs
```

---

## 5. Large Object Heap (LOH)

### 5.1 Avoid LOH Allocations

**Best Practice**: Keep objects under 85KB to avoid LOH.

```csharp
// ❌ Bad - large array on LOH
public byte[] CreateBuffer()
{
    return new byte[100_000]; // > 85KB, goes to LOH
}

// ✅ Good - pool large arrays
private static readonly ArrayPool<byte> _pool = ArrayPool<byte>.Shared;

public byte[] CreateBuffer()
{
    return _pool.Rent(100_000); // Reuse from pool
}
```

### 5.2 LOH Compaction

**Best Practice**: Enable LOH compaction when needed.

```csharp
// ✅ Good - compact LOH
GCSettings.LargeObjectHeapCompactionMode = GCLargeObjectHeapCompactionMode.CompactOnce;
GC.Collect();
```

---

## 6. Async Performance

### 6.1 ValueTask<T> for Hot Paths

**Best Practice**: Use ValueTask<T> when results are often cached.

```csharp
// ✅ Good - ValueTask for cached results
public ValueTask<Product?> GetProductAsync(int id)
{
    if (_cache.TryGetValue(id, out var product))
    {
        return ValueTask.FromResult(product); // No allocation
    }
    
    return new ValueTask<Product?>(LoadProductAsync(id)); // Allocates Task
}

// ❌ Less optimal - Task for cached results
public Task<Product?> GetProductAsync(int id)
{
    if (_cache.TryGetValue(id, out var product))
    {
        return Task.FromResult(product); // Allocates Task
    }
    
    return LoadProductAsync(id);
}
```

---

## 7. Database Performance

### 7.1 Connection Pooling

**Best Practice**: Rely on connection pooling (enabled by default).

```csharp
// ✅ Good - connection pooling (default)
var connectionString = "Server=...;Database=...;Trusted_Connection=True;";
using var connection = new SqlConnection(connectionString);
await connection.OpenAsync();
// Connection returned to pool on disposal

// ❌ Bad - disable pooling
var connectionString = "Server=...;Database=...;Pooling=false;"; // Don't do this
```

### 7.2 Batch Operations

**Best Practice**: Batch database operations.

```csharp
// ✅ Good - batch insert
public async Task InsertProductsAsync(List<Product> products)
{
    _dbContext.Products.AddRange(products); // Single batch
    await _dbContext.SaveChangesAsync();
}

// ❌ Bad - one-by-one inserts
public async Task InsertProductsAsync(List<Product> products)
{
    foreach (var product in products)
    {
        _dbContext.Products.Add(product);
        await _dbContext.SaveChangesAsync(); // Database round-trip per item
    }
}
```

### 7.3 AsNoTracking

**Best Practice**: Use AsNoTracking for read-only queries.

```csharp
// ✅ Good - AsNoTracking for read-only
var products = await _dbContext.Products
    .AsNoTracking() // No change tracking overhead
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync();

// ❌ Less optimal - tracking when not needed
var products = await _dbContext.Products
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync(); // Tracks all entities
```

---

## 8. Caching

### 8.1 Memory Cache

**Best Practice**: Use IMemoryCache for in-process caching.

```csharp
// ✅ Good - IMemoryCache
public class ProductService
{
    private readonly IMemoryCache _cache;
    private readonly IProductRepository _repository;
    
    public async Task<Product?> GetProductAsync(int id)
    {
        return await _cache.GetOrCreateAsync($"product:{id}", async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
            return await _repository.GetByIdAsync(id);
        });
    }
}
```

### 8.2 Distributed Cache

**Best Practice**: Use IDistributedCache for multi-server scenarios.

```csharp
// ✅ Good - IDistributedCache
public class ProductService
{
    private readonly IDistributedCache _cache;
    
    public async Task<Product?> GetProductAsync(int id)
    {
        var cachedData = await _cache.GetStringAsync($"product:{id}");
        if (cachedData != null)
        {
            return JsonSerializer.Deserialize<Product>(cachedData);
        }
        
        var product = await _repository.GetByIdAsync(id);
        if (product != null)
        {
            await _cache.SetStringAsync(
                $"product:{id}",
                JsonSerializer.Serialize(product),
                new DistributedCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
                });
        }
        
        return product;
    }
}
```

### 8.3 Response Caching

**Best Practice**: Use response caching for HTTP endpoints.

```csharp
// ✅ Good - response caching
[HttpGet]
[ResponseCache(Duration = 60, VaryByQueryKeys = new[] { "categoryId" })]
public async Task<ActionResult<List<Product>>> GetProducts(int categoryId)
{
    var products = await _productService.GetByCategoryAsync(categoryId);
    return Ok(products);
}

// Register middleware
builder.Services.AddResponseCaching();
app.UseResponseCaching();
```

### 8.4 Output Caching (.NET 7+)

**Best Practice**: Use output caching for fine-grained control.

```csharp
// ✅ Good - output caching (.NET 7+)
builder.Services.AddOutputCache(options =>
{
    options.AddPolicy("ProductsPolicy", builder =>
    {
        builder.Expire(TimeSpan.FromMinutes(5))
               .VaryByQuery("categoryId");
    });
});

app.UseOutputCache();

[HttpGet]
[OutputCache(PolicyName = "ProductsPolicy")]
public async Task<ActionResult<List<Product>>> GetProducts(int categoryId)
{
    var products = await _productService.GetByCategoryAsync(categoryId);
    return Ok(products);
}
```

---

## 9. HTTP Client Performance

### 9.1 Reuse HttpClient

**Critical**: Use IHttpClientFactory, never create HttpClient manually.

```csharp
// ✅ Good - IHttpClientFactory
builder.Services.AddHttpClient<IProductClient, ProductClient>();

public class ProductClient
{
    private readonly HttpClient _httpClient;
    
    public ProductClient(HttpClient httpClient)
    {
        _httpClient = httpClient;
        _httpClient.BaseAddress = new Uri("https://api.example.com");
    }
}

// ❌ CRITICAL - creating HttpClient manually
public class ProductClient
{
    public async Task<Product> GetProductAsync(int id)
    {
        using var client = new HttpClient(); // Socket exhaustion!
        return await client.GetFromJsonAsync<Product>($"https://api.example.com/products/{id}");
    }
}
```

---

## 10. Compression

### 10.1 Response Compression

**Best Practice**: Enable response compression.

```csharp
// ✅ Good - response compression
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true;
    options.Providers.Add<GzipCompressionProvider>();
    options.Providers.Add<BrotliCompressionProvider>();
});

app.UseResponseCompression();
```

---

## 11. Profiling Tools

### 11.1 BenchmarkDotNet

**Best Practice**: Use BenchmarkDotNet for micro-benchmarks.

```csharp
// ✅ Good - BenchmarkDotNet
[MemoryDiagnoser]
public class StringConcatBenchmark
{
    [Benchmark]
    public string StringConcat()
    {
        string result = "";
        for (int i = 0; i < 100; i++)
        {
            result += i.ToString();
        }
        return result;
    }
    
    [Benchmark]
    public string StringBuilder()
    {
        var sb = new StringBuilder();
        for (int i = 0; i < 100; i++)
        {
            sb.Append(i);
        }
        return sb.ToString();
    }
}
```

---

## Performance Checklist

1. **Strings**: ✅ StringBuilder for loops, StringComparison for comparisons
2. **Collections**: ✅ Specify capacity, choose right type
3. **Memory**: ✅ Span<T>, ArrayPool, ObjectPool
4. **Boxing**: ✅ Avoid boxing value types
5. **LOH**: ✅ Keep objects under 85KB
6. **Async**: ✅ ValueTask for hot paths
7. **Database**: ✅ Connection pooling, batching, AsNoTracking
8. **Caching**: ✅ IMemoryCache, IDistributedCache, response caching
9. **HTTP**: ✅ IHttpClientFactory
10. **Compression**: ✅ Enable response compression

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
