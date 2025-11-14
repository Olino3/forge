# Dependency Injection Patterns

This file documents dependency injection best practices, service lifetimes, and common DI mistakes in .NET applications.

## Purpose

Load this file when reviewing:
- Service registration in Program.cs or Startup.cs
- Constructor injection patterns
- Service lifetime choices
- Factory patterns
- IHttpClientFactory usage

---

## 1. Service Lifetimes

### 1.1 Lifetime Types

**Three service lifetimes in .NET**:

1. **Transient**: New instance every time requested
2. **Scoped**: One instance per HTTP request (or scope)
3. **Singleton**: One instance for application lifetime

```csharp
// ✅ Good - appropriate lifetimes
builder.Services.AddTransient<IEmailSender, EmailSender>(); // New instance each time
builder.Services.AddScoped<IProductService, ProductService>(); // Per request
builder.Services.AddScoped<ApplicationDbContext>(); // DbContext always Scoped
builder.Services.AddSingleton<ICacheService, MemoryCacheService>(); // One instance
```

### 1.2 When to Use Each Lifetime

**Transient**:
- Lightweight, stateless services
- Services that perform a single operation
- Example: Email sender, SMS sender, validators

```csharp
// ✅ Transient - lightweight, stateless
public interface IEmailSender
{
    Task SendEmailAsync(string to, string subject, string body);
}

builder.Services.AddTransient<IEmailSender, EmailSender>();
```

**Scoped**:
- Services that should live for the duration of a request
- Services with per-request state
- Database contexts (DbContext)
- Unit of work patterns

```csharp
// ✅ Scoped - per HTTP request
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddScoped<ApplicationDbContext>();
```

**Singleton**:
- Expensive to create services
- Thread-safe services
- Caching services
- Configuration services

```csharp
// ✅ Singleton - thread-safe cache
public class MemoryCacheService : ICacheService
{
    private readonly IMemoryCache _cache;
    
    public MemoryCacheService(IMemoryCache cache)
    {
        _cache = cache; // IMemoryCache is thread-safe
    }
}

builder.Services.AddSingleton<ICacheService, MemoryCacheService>();
```

---

## 2. Captive Dependencies (Critical Issue)

### 2.1 Understanding Captive Dependencies

**Rule**: Longer-lived services CANNOT depend on shorter-lived services.

```csharp
// ❌ CRITICAL - Captive Dependency
public class NotificationService // Registered as Singleton
{
    private readonly ApplicationDbContext _context; // Scoped!

    public NotificationService(ApplicationDbContext context)
    {
        _context = context; // BUG - context captured by singleton
    }
    
    public async Task SendNotificationAsync()
    {
        // _context is disposed after first request but singleton keeps reference
        var users = await _context.Users.ToListAsync(); // CRASH!
    }
}

// Registration
builder.Services.AddSingleton<NotificationService>(); // WRONG
builder.Services.AddScoped<ApplicationDbContext>();
```

**What happens**: The singleton captures the scoped DbContext from the first request. After that request ends, the DbContext is disposed, but the singleton still holds a reference to it. Subsequent calls crash.

### 2.2 Fixing Captive Dependencies

**Solution 1**: Change service lifetime to match dependency.

```csharp
// ✅ Good - both Scoped
public class NotificationService // Now Scoped
{
    private readonly ApplicationDbContext _context;

    public NotificationService(ApplicationDbContext context)
    {
        _context = context; // Safe - same lifetime
    }
}

builder.Services.AddScoped<NotificationService>();
builder.Services.AddScoped<ApplicationDbContext>();
```

**Solution 2**: Use IServiceScopeFactory for manual scope creation.

```csharp
// ✅ Good - Singleton using IServiceScopeFactory
public class NotificationService // Singleton
{
    private readonly IServiceScopeFactory _scopeFactory;

    public NotificationService(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory; // Singleton safe
    }
    
    public async Task SendNotificationAsync()
    {
        using var scope = _scopeFactory.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        
        var users = await context.Users.ToListAsync(); // Safe!
    }
}

builder.Services.AddSingleton<NotificationService>();
```

### 2.3 Common Captive Dependency Scenarios

**Scenario 1**: Singleton capturing Scoped

```csharp
// ❌ Bad
builder.Services.AddSingleton<MyService>(); // Singleton
builder.Services.AddScoped<ApplicationDbContext>(); // Scoped

public class MyService
{
    private readonly ApplicationDbContext _context; // CAPTIVE
}
```

**Scenario 2**: Singleton capturing Transient with Scoped dependency

```csharp
// ❌ Bad - indirect captive dependency
builder.Services.AddSingleton<MyBackgroundService>(); // Singleton
builder.Services.AddTransient<IEmailSender, EmailSender>(); // Transient

public class MyBackgroundService
{
    private readonly IEmailSender _emailSender; // Transient captured by Singleton
}

public class EmailSender : IEmailSender
{
    private readonly ApplicationDbContext _context; // Scoped captured by Transient!
}
```

**Scenario 3**: Background service with scoped dependency

```csharp
// ❌ Bad
public class DataProcessingService : BackgroundService // Singleton
{
    private readonly ApplicationDbContext _context; // Scoped - CAPTIVE

    public DataProcessingService(ApplicationDbContext context)
    {
        _context = context;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await ProcessDataAsync(); // Uses disposed context
        }
    }
}

// ✅ Good - use IServiceScopeFactory
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
            await ProcessDataAsync(context);
        }
    }
}
```

---

## 3. Constructor Injection

### 3.1 Prefer Constructor Injection

**Best Practice**: Use constructor injection as the primary DI pattern.

```csharp
// ✅ Good - constructor injection
public class ProductService : IProductService
{
    private readonly ApplicationDbContext _context;
    private readonly ILogger<ProductService> _logger;
    private readonly ICacheService _cacheService;

    public ProductService(
        ApplicationDbContext context,
        ILogger<ProductService> logger,
        ICacheService cacheService)
    {
        _context = context;
        _logger = logger;
        _cacheService = cacheService;
    }

    public async Task<Product> GetByIdAsync(int id)
    {
        var cacheKey = $"product_{id}";
        var cached = _cacheService.Get<Product>(cacheKey);
        if (cached != null) return cached;

        var product = await _context.Products.FindAsync(id);
        _cacheService.Set(cacheKey, product, TimeSpan.FromMinutes(10));
        return product;
    }
}

// Registration
builder.Services.AddScoped<IProductService, ProductService>();
```

### 3.2 Avoid Service Locator Pattern

**Anti-Pattern**: Injecting `IServiceProvider` to resolve services manually.

```csharp
// ❌ Bad - service locator anti-pattern
public class ProductService
{
    private readonly IServiceProvider _serviceProvider;

    public ProductService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task<Product> GetByIdAsync(int id)
    {
        // Resolving dependencies manually
        var context = _serviceProvider.GetRequiredService<ApplicationDbContext>();
        var logger = _serviceProvider.GetRequiredService<ILogger<ProductService>>();
        
        return await context.Products.FindAsync(id);
    }
}

// ✅ Good - constructor injection (explicit dependencies)
public class ProductService
{
    private readonly ApplicationDbContext _context;
    private readonly ILogger<ProductService> _logger;

    public ProductService(ApplicationDbContext context, ILogger<ProductService> logger)
    {
        _context = context;
        _logger = logger;
    }
}
```

**When Service Locator is Acceptable**:
- IServiceScopeFactory in singletons (to create scopes)
- Factory classes that need to resolve services dynamically
- Middleware or filters with dynamic resolution needs

### 3.3 Avoid Action Injection

**Anti-Pattern**: Using `[FromServices]` in controller actions.

```csharp
// ❌ Bad - action injection
public class ProductsController : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<ActionResult<Product>> GetById(
        int id,
        [FromServices] IProductService productService, // Anti-pattern
        [FromServices] ILogger<ProductsController> logger)
    {
        logger.LogInformation("Getting product {Id}", id);
        var product = await productService.GetByIdAsync(id);
        return product != null ? Ok(product) : NotFound();
    }
}

// ✅ Good - constructor injection
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(IProductService productService, ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Product>> GetById(int id)
    {
        _logger.LogInformation("Getting product {Id}", id);
        var product = await _productService.GetByIdAsync(id);
        return product != null ? Ok(product) : NotFound();
    }
}
```

---

## 4. IHttpClientFactory

### 4.1 Never Create HttpClient Manually

**Critical**: Creating `HttpClient` per request exhausts sockets.

```csharp
// ❌ CRITICAL - Socket exhaustion
public class ExternalApiClient
{
    public async Task<string> GetDataAsync(string url)
    {
        using var client = new HttpClient(); // SOCKET LEAK!
        return await client.GetStringAsync(url);
    }
}

// Each call creates a new HttpClient, sockets not released immediately
// Can exhaust available sockets under load
```

### 4.2 Use IHttpClientFactory

**Best Practice**: Always use IHttpClientFactory.

```csharp
// ✅ Good - IHttpClientFactory basic usage
builder.Services.AddHttpClient();

public class ExternalApiClient
{
    private readonly IHttpClientFactory _httpClientFactory;

    public ExternalApiClient(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    public async Task<string> GetDataAsync(string url)
    {
        var client = _httpClientFactory.CreateClient();
        return await client.GetStringAsync(url);
    }
}
```

### 4.3 Named HttpClients

**Best Practice**: Use named clients for different APIs.

```csharp
// ✅ Good - named clients
builder.Services.AddHttpClient("PaymentApi", client =>
{
    client.BaseAddress = new Uri("https://api.payment.com");
    client.DefaultRequestHeaders.Add("Accept", "application/json");
    client.Timeout = TimeSpan.FromSeconds(30);
});

builder.Services.AddHttpClient("ShippingApi", client =>
{
    client.BaseAddress = new Uri("https://api.shipping.com");
    client.Timeout = TimeSpan.FromSeconds(15);
});

// Usage
public class OrderService
{
    private readonly IHttpClientFactory _httpClientFactory;

    public OrderService(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    public async Task ProcessPaymentAsync(Order order)
    {
        var client = _httpClientFactory.CreateClient("PaymentApi");
        var response = await client.PostAsJsonAsync("/payments", order);
        response.EnsureSuccessStatusCode();
    }
}
```

### 4.4 Typed HttpClients

**Best Practice**: Use typed clients for better testability.

```csharp
// ✅ Best - typed client
public interface IPaymentApiClient
{
    Task<PaymentResult> ProcessPaymentAsync(PaymentRequest request);
}

public class PaymentApiClient : IPaymentApiClient
{
    private readonly HttpClient _httpClient;

    public PaymentApiClient(HttpClient httpClient)
    {
        _httpClient = httpClient; // Injected by IHttpClientFactory
    }

    public async Task<PaymentResult> ProcessPaymentAsync(PaymentRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync("/payments", request);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<PaymentResult>();
    }
}

// Registration
builder.Services.AddHttpClient<IPaymentApiClient, PaymentApiClient>(client =>
{
    client.BaseAddress = new Uri("https://api.payment.com");
    client.DefaultRequestHeaders.Add("Accept", "application/json");
});

// Usage - inject IPaymentApiClient
public class OrderService
{
    private readonly IPaymentApiClient _paymentClient;

    public OrderService(IPaymentApiClient paymentClient)
    {
        _paymentClient = paymentClient;
    }

    public async Task ProcessOrderAsync(Order order)
    {
        var result = await _paymentClient.ProcessPaymentAsync(new PaymentRequest
        {
            Amount = order.Total,
            Currency = "USD"
        });
    }
}
```

### 4.5 HttpClient with Polly for Resilience

**Best Practice**: Add retry and circuit breaker policies.

```csharp
// ✅ Good - resilience with Polly
builder.Services.AddHttpClient<IPaymentApiClient, PaymentApiClient>(client =>
{
    client.BaseAddress = new Uri("https://api.payment.com");
})
.AddTransientHttpErrorPolicy(policy => 
    policy.WaitAndRetryAsync(3, retryAttempt => 
        TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)))) // Exponential backoff
.AddTransientHttpErrorPolicy(policy =>
    policy.CircuitBreakerAsync(5, TimeSpan.FromSeconds(30))); // Circuit breaker
```

---

## 5. Factory Pattern

### 5.1 Factory for Dynamic Service Resolution

**Best Practice**: Use factories when you need to resolve services dynamically.

```csharp
// ✅ Good - factory pattern
public interface INotificationSenderFactory
{
    INotificationSender Create(NotificationType type);
}

public class NotificationSenderFactory : INotificationSenderFactory
{
    private readonly IServiceProvider _serviceProvider;

    public NotificationSenderFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider; // Acceptable use of IServiceProvider
    }

    public INotificationSender Create(NotificationType type)
    {
        return type switch
        {
            NotificationType.Email => _serviceProvider.GetRequiredService<IEmailSender>(),
            NotificationType.Sms => _serviceProvider.GetRequiredService<ISmsSender>(),
            NotificationType.Push => _serviceProvider.GetRequiredService<IPushNotificationSender>(),
            _ => throw new ArgumentException($"Unknown notification type: {type}")
        };
    }
}

// Registration
builder.Services.AddTransient<IEmailSender, EmailSender>();
builder.Services.AddTransient<ISmsSender, SmsSender>();
builder.Services.AddTransient<IPushNotificationSender, PushNotificationSender>();
builder.Services.AddSingleton<INotificationSenderFactory, NotificationSenderFactory>();

// Usage
public class NotificationService
{
    private readonly INotificationSenderFactory _factory;

    public NotificationService(INotificationSenderFactory factory)
    {
        _factory = factory;
    }

    public async Task SendNotificationAsync(Notification notification)
    {
        var sender = _factory.Create(notification.Type);
        await sender.SendAsync(notification);
    }
}
```

### 5.2 Func<T> for Simple Factories

**Best Practice**: Register `Func<T>` for simple factory scenarios.

```csharp
// ✅ Good - Func<T> factory
builder.Services.AddTransient<IEmailSender, EmailSender>();
builder.Services.AddTransient<Func<IEmailSender>>(sp => () => sp.GetRequiredService<IEmailSender>());

// Usage
public class BatchEmailService
{
    private readonly Func<IEmailSender> _emailSenderFactory;

    public BatchEmailService(Func<IEmailSender> emailSenderFactory)
    {
        _emailSenderFactory = emailSenderFactory;
    }

    public async Task SendBatchEmailsAsync(List<Email> emails)
    {
        foreach (var email in emails)
        {
            var sender = _emailSenderFactory(); // New instance per email
            await sender.SendAsync(email);
        }
    }
}
```

---

## 6. Options Pattern

### 6.1 IOptions, IOptionsSnapshot, IOptionsMonitor

**Best Practice**: Use appropriate options interface.

```csharp
// Configuration
public class EmailSettings
{
    public string SmtpServer { get; set; }
    public int Port { get; set; }
    public string Username { get; set; }
    public string Password { get; set; }
}

// Registration
builder.Services.Configure<EmailSettings>(builder.Configuration.GetSection("EmailSettings"));

// ✅ IOptions<T> - Singleton, doesn't reload
public class EmailSender
{
    private readonly EmailSettings _settings;

    public EmailSender(IOptions<EmailSettings> options)
    {
        _settings = options.Value; // Read once
    }
}

// ✅ IOptionsSnapshot<T> - Scoped, reloads per request
public class EmailSender
{
    private readonly EmailSettings _settings;

    public EmailSender(IOptionsSnapshot<EmailSettings> options)
    {
        _settings = options.Value; // Reloads per request
    }
}

// ✅ IOptionsMonitor<T> - Singleton, reloads on change
public class EmailSender
{
    private readonly IOptionsMonitor<EmailSettings> _optionsMonitor;

    public EmailSender(IOptionsMonitor<EmailSettings> optionsMonitor)
    {
        _optionsMonitor = optionsMonitor;
        _optionsMonitor.OnChange(settings =>
        {
            // React to configuration changes
        });
    }

    public async Task SendAsync(Email email)
    {
        var settings = _optionsMonitor.CurrentValue; // Always current
    }
}
```

**When to use each**:
- `IOptions<T>`: Configuration rarely changes, Singleton services
- `IOptionsSnapshot<T>`: Configuration per request, Scoped services
- `IOptionsMonitor<T>`: Configuration changes at runtime, Singleton with reload

---

## 7. Service Registration Patterns

### 7.1 Interface-Based Registration

**Best Practice**: Register services by interface.

```csharp
// ✅ Good - interface-based
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IOrderService, OrderService>();

// ❌ Bad - concrete type registration
builder.Services.AddScoped<ProductService>();
```

### 7.2 Multiple Implementations

**Best Practice**: Register multiple implementations.

```csharp
// ✅ Good - multiple implementations
builder.Services.AddTransient<INotificationSender, EmailNotificationSender>();
builder.Services.AddTransient<INotificationSender, SmsNotificationSender>();

// Resolve all implementations
public class NotificationService
{
    private readonly IEnumerable<INotificationSender> _senders;

    public NotificationService(IEnumerable<INotificationSender> senders)
    {
        _senders = senders; // Gets all registered implementations
    }

    public async Task SendToAllAsync(Notification notification)
    {
        foreach (var sender in _senders)
        {
            await sender.SendAsync(notification);
        }
    }
}
```

### 7.3 Open Generic Registration

**Best Practice**: Register open generics for generic interfaces.

```csharp
// ✅ Good - open generic registration
public interface IRepository<T> where T : class
{
    Task<T> GetByIdAsync(int id);
    Task<List<T>> GetAllAsync();
}

public class Repository<T> : IRepository<T> where T : class
{
    private readonly ApplicationDbContext _context;

    public Repository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<T> GetByIdAsync(int id)
    {
        return await _context.Set<T>().FindAsync(id);
    }

    public async Task<List<T>> GetAllAsync()
    {
        return await _context.Set<T>().ToListAsync();
    }
}

// Register open generic
builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));

// Usage - automatically resolved for any T
public class ProductService
{
    private readonly IRepository<Product> _productRepository;

    public ProductService(IRepository<Product> productRepository)
    {
        _productRepository = productRepository; // Repository<Product> injected
    }
}
```

---

## Common Dependency Injection Anti-Patterns

1. **Captive Dependencies**: Singleton → Scoped (NEVER)
2. **Service Locator**: Injecting IServiceProvider everywhere
3. **Creating HttpClient**: Use IHttpClientFactory
4. **Action Injection**: Use constructor injection instead
5. **DbContext as Singleton**: Always Scoped
6. **Not Using Interfaces**: Register interfaces, not concrete types
7. **Circular Dependencies**: Refactor to break cycles
8. **Too Many Dependencies**: Constructor with 5+ parameters (violates SRP)
9. **Static Dependencies**: Use DI instead of static classes
10. **Not Disposing Scopes**: Use `using` with IServiceScopeFactory

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
