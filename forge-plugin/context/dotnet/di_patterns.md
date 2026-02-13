---
id: "dotnet/di_patterns"
domain: dotnet
title: "Dependency Injection Patterns"
type: pattern
estimatedTokens: 1100
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 68
    keywords: [anti-patterns]
  - name: "Service Lifetimes"
    estimatedTokens: 68
    keywords: [service, lifetimes]
  - name: "Critical Lifetime Rules"
    estimatedTokens: 84
    keywords: [critical, lifetime, rules]
  - name: "Background Services with Scoped Dependencies"
    estimatedTokens: 61
    keywords: [background, services, scoped, dependencies]
  - name: "IHttpClientFactory"
    estimatedTokens: 59
    keywords: [ihttpclientfactory]
  - name: "Options Pattern"
    estimatedTokens: 77
    keywords: [options, pattern]
  - name: "Service Registration Patterns"
    estimatedTokens: 36
    keywords: [service, registration, patterns]
  - name: "Common Detection Patterns"
    estimatedTokens: 63
    keywords: [detection, patterns]
  - name: "DI Checklist"
    estimatedTokens: 47
    keywords: [checklist]
  - name: "Official Resources"
    estimatedTokens: 24
    keywords: [official, resources]
tags: [dotnet, dependency-injection, service-lifetime, httpclient, options-pattern]
---

# Dependency Injection Patterns

Quick reference for DI in .NET. For detailed examples, see [Dependency injection in .NET](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection).

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|--------------|
| **DbContext as Singleton** | `AddSingleton<DbContext>()` | Use `AddScoped` (or `AddDbContext`) | [DbContext lifetime](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#dbcontext-in-dependency-injection) |
| **Captive dependency** | Scoped service in Singleton | Inject `IServiceScopeFactory` | [Captive dependency](https://blog.ploeh.dk/2014/06/02/captive-dependency/) |
| **New HttpClient per request** | `new HttpClient()` | Use `IHttpClientFactory` | [IHttpClientFactory](https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory) |
| **Service Locator** | Injecting `IServiceProvider` | Use constructor injection | [Service Locator anti-pattern](https://blog.ploeh.dk/2010/02/03/ServiceLocatorisanAnti-Pattern/) |
| **Manual disposal** | Disposing DI-injected services | Let container manage lifetime | [DI guidelines](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines) |

---

## Service Lifetimes

| Lifetime | Created | Disposed | Use When |
|----------|---------|----------|----------|
| **Transient** | Every request | After use | Stateless, lightweight services |
| **Scoped** | Once per HTTP request/scope | End of scope | DbContext, per-request state |
| **Singleton** | Once per application | App shutdown | Stateless, thread-safe, caching |

```csharp
// Transient - new instance every time
services.AddTransient<IEmailSender, EmailSender>();

// Scoped - one instance per HTTP request (or Blazor circuit)
services.AddScoped<ICartService, CartService>();

// Singleton - single instance for app lifetime
services.AddSingleton<IConfigurationCache, ConfigurationCache>();
```

[Service lifetimes](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection#service-lifetimes)

---

## Critical Lifetime Rules

| Rule | Why | Example |
|------|-----|---------|
| **Never Singleton → Scoped** | Singleton captures first scope | ❌ `Singleton(DbContext)` |
| **DbContext must be Scoped** | Not thread-safe | ✅ `AddDbContext<T>()` |
| **HttpClient must use Factory** | Socket exhaustion | ✅ `AddHttpClient<T>()` |
| **Background services with Scoped** | Use `IServiceScopeFactory` | ✅ Create manual scopes |

```csharp
// ❌ CRITICAL - DbContext as Singleton
services.AddSingleton<ApplicationDbContext>();  // NOT THREAD-SAFE!

// ✅ DbContext as Scoped (default with AddDbContext)
services.AddDbContext<ApplicationDbContext>();

// ❌ CRITICAL - Captive dependency
services.AddSingleton<ProductService>();  // Singleton
// ProductService depends on DbContext (Scoped) - CAPTIVE!

// ✅ Fix captive dependency
services.AddScoped<ProductService>();  // Match DbContext lifetime
```

[Captive dependencies](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines#captive-dependency)

---

## Background Services with Scoped Dependencies

```csharp
// ❌ CRITICAL - Scoped service in Singleton
public class Worker : BackgroundService
{
    private readonly AppDbContext _context;  // CAPTIVE!

    public Worker(AppDbContext context) => _context = context;
}

// ✅ Use IServiceScopeFactory
public class Worker : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;

    public Worker(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            using var scope = _scopeFactory.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

            await ProcessDataAsync(context);
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}
```

[Background services](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/host/hosted-services)

---

## IHttpClientFactory

```csharp
// ❌ CRITICAL - Manual HttpClient creation
public class ApiClient
{
    public async Task<string> GetDataAsync()
    {
        using var client = new HttpClient();  // SOCKET EXHAUSTION!
        return await client.GetStringAsync("https://api.example.com");
    }
}

// ✅ Typed client with IHttpClientFactory
services.AddHttpClient<IApiClient, ApiClient>(client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.Timeout = TimeSpan.FromSeconds(30);
});

public class ApiClient : IApiClient
{
    private readonly HttpClient _client;

    public ApiClient(HttpClient client) => _client = client;

    public async Task<string> GetDataAsync()
    {
        return await _client.GetStringAsync("/data");
    }
}
```

[HttpClientFactory](https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory)

---

## Options Pattern

| Type | Lifetime | Reloads Config | Use When |
|------|----------|----------------|----------|
| **IOptions<T>** | Singleton | ❌ No | Static config |
| **IOptionsSnapshot<T>** | Scoped | ✅ Yes (per request) | Config changes infrequently |
| **IOptionsMonitor<T>** | Singleton | ✅ Yes (real-time) | Config changes frequently |

```csharp
// Configuration binding
public class EmailSettings
{
    public string SmtpServer { get; set; }
    public int Port { get; set; }
}

// Register options
services.Configure<EmailSettings>(
    configuration.GetSection("Email"));

// Use in service
public class EmailSender
{
    private readonly EmailSettings _settings;

    public EmailSender(IOptions<EmailSettings> options)
    {
        _settings = options.Value;
    }
}
```

[Options pattern](https://learn.microsoft.com/en-us/dotnet/core/extensions/options)

---

## Service Registration Patterns

```csharp
// ✅ Interface-based
services.AddScoped<IProductRepository, ProductRepository>();

// ✅ Multiple implementations
services.AddScoped<INotificationService, EmailNotificationService>();
services.AddScoped<INotificationService, SmsNotificationService>();
// Resolves IEnumerable<INotificationService>

// ✅ Open generics
services.AddScoped(typeof(IRepository<>), typeof(Repository<>));

// ✅ Factory pattern
services.AddScoped<IProductService>(sp =>
{
    var repo = sp.GetRequiredService<IProductRepository>();
    var cache = sp.GetRequiredService<IMemoryCache>();
    return new ProductService(repo, cache, useCache: true);
});
```

[Service registration](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection#service-registration-methods)

---

## Common Detection Patterns

```csharp
// ❌ DbContext as Singleton
services.AddSingleton<DbContext>()

// ❌ New HttpClient
new HttpClient()
using var client = new HttpClient()

// ❌ Service Locator
public class MyService
{
    private readonly IServiceProvider _provider;  // Anti-pattern
}

// ❌ Captive dependency
services.AddSingleton<MyService>();
// Where MyService depends on scoped DbContext

// ❌ Disposing DI services
public void MyMethod(IMyService service)
{
    service.Dispose();  // Container owns disposal
}

// ❌ Scoped service in background worker constructor
public class Worker : BackgroundService
{
    public Worker(DbContext context)  // CAPTIVE
}
```

---

## DI Checklist

- ✅ DbContext is Scoped (via `AddDbContext`)
- ✅ HttpClient via `IHttpClientFactory`
- ✅ No captive dependencies (longer lifetime → shorter lifetime)
- ✅ Constructor injection, not Service Locator (`IServiceProvider`)
- ✅ Background services use `IServiceScopeFactory` for scoped deps
- ✅ Let container manage disposal (don't dispose injected services)
- ✅ Use `IOptions` pattern for configuration
- ✅ Interface-based registration for testability

---

## Official Resources

- **Dependency injection in .NET**: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection
- **DI guidelines**: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines
- **Service lifetimes**: https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection#service-lifetimes
- **IHttpClientFactory**: https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory
- **Options pattern**: https://learn.microsoft.com/en-us/dotnet/core/extensions/options

---

**Version**: 0.3.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
