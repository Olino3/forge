# ASP.NET Core Patterns

This file documents best practices and patterns for ASP.NET Core web applications, including Web API, MVC, Razor Pages, and Minimal APIs.

## Purpose

Load this file when reviewing:
- Controllers and API endpoints
- Middleware components
- ASP.NET Core configuration
- Authentication and authorization
- Model validation
- Web application architecture

---

## 1. Controller Patterns

### 1.1 Controller Base Classes

**Best Practice**: Use `ControllerBase` for APIs, `Controller` for MVC with views.

```csharp
// ✅ Web API - use ControllerBase
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    // API-specific functionality
}

// ✅ MVC with views - use Controller
public class HomeController : Controller
{
    // View-related functionality (ViewBag, ViewData, View())
}
```

### 1.2 Route Patterns

**Best Practice**: Use attribute routing with consistent patterns.

```csharp
// ✅ Good routing patterns
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Product>>> GetAll()
    {
        // GET api/products
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Product>> GetById(int id)
    {
        // GET api/products/5
    }

    [HttpPost]
    public async Task<ActionResult<Product>> Create(CreateProductDto dto)
    {
        // POST api/products
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, UpdateProductDto dto)
    {
        // PUT api/products/5
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        // DELETE api/products/5
    }
}

// ❌ Bad - inconsistent routing
[Route("products")] // Missing api/ prefix
public class ProductsController : ControllerBase
{
    [HttpGet("all")] // Redundant
    [HttpGet("getproduct/{id}")] // Verbose, not RESTful
}
```

### 1.3 Action Return Types

**Best Practice**: Use appropriate return types for different scenarios.

```csharp
// ✅ Return ActionResult<T> for APIs
[HttpGet("{id}")]
public async Task<ActionResult<Product>> GetById(int id)
{
    var product = await _service.GetByIdAsync(id);
    if (product == null)
        return NotFound();
    
    return product; // Implicit conversion to ActionResult<Product>
}

// ✅ Return IActionResult for status-only responses
[HttpDelete("{id}")]
public async Task<IActionResult> Delete(int id)
{
    await _service.DeleteAsync(id);
    return NoContent(); // 204
}

// ✅ Return specific types for views
public IActionResult Index()
{
    return View();
}

// ❌ Bad - returning concrete types from API methods
[HttpGet("{id}")]
public async Task<Product> GetById(int id) // Can't return 404, 500, etc.
{
    return await _service.GetByIdAsync(id);
}
```

### 1.4 Status Code Usage

**Best Practice**: Use appropriate HTTP status codes.

```csharp
public async Task<ActionResult<Product>> Create(CreateProductDto dto)
{
    var product = await _service.CreateAsync(dto);
    
    // ✅ 201 Created with location header
    return CreatedAtAction(
        nameof(GetById),
        new { id = product.Id },
        product
    );
}

public async Task<ActionResult<Product>> GetById(int id)
{
    var product = await _service.GetByIdAsync(id);
    
    // ✅ 404 Not Found
    if (product == null)
        return NotFound();
    
    // ✅ 200 OK with data
    return Ok(product);
}

public async Task<IActionResult> Update(int id, UpdateProductDto dto)
{
    if (id != dto.Id)
        return BadRequest(); // ✅ 400 Bad Request
    
    var success = await _service.UpdateAsync(dto);
    if (!success)
        return NotFound(); // ✅ 404 Not Found
    
    return NoContent(); // ✅ 204 No Content
}

// ❌ Bad - always returning 200
public async Task<IActionResult> Delete(int id)
{
    await _service.DeleteAsync(id);
    return Ok(); // Should be NoContent (204) or NotFound if not exists
}
```

**Status Code Guide**:
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE, PUT with no response body
- `400 Bad Request`: Validation failure, malformed request
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource doesn't exist
- `409 Conflict`: Business rule violation, concurrency conflict
- `500 Internal Server Error`: Unhandled exception

### 1.5 Async Actions

**Best Practice**: All I/O operations should be async.

```csharp
// ✅ Good - async all the way
[HttpGet]
public async Task<ActionResult<IEnumerable<Product>>> GetAll()
{
    var products = await _service.GetAllAsync();
    return Ok(products);
}

// ❌ Bad - sync I/O blocks thread
[HttpGet]
public ActionResult<IEnumerable<Product>> GetAll()
{
    var products = _service.GetAll(); // Blocks thread
    return Ok(products);
}

// ❌ Bad - sync-over-async
[HttpGet]
public ActionResult<IEnumerable<Product>> GetAll()
{
    var products = _service.GetAllAsync().Result; // DEADLOCK RISK
    return Ok(products);
}
```

---

## 2. Middleware Patterns

### 2.1 Middleware Order

**Critical**: Middleware order matters. Use this standard order:

```csharp
var app = builder.Build();

// 1. Exception handling (must be first)
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}

// 2. HTTPS redirection
app.UseHttpsRedirection();

// 3. Static files
app.UseStaticFiles();

// 4. Routing
app.UseRouting();

// 5. CORS (after routing, before auth)
app.UseCors("MyPolicy");

// 6. Authentication (before authorization)
app.UseAuthentication();

// 7. Authorization
app.UseAuthorization();

// 8. Custom middleware
app.UseMiddleware<RequestLoggingMiddleware>();

// 9. Endpoints (must be last)
app.MapControllers();
```

### 2.2 Custom Middleware

**Best Practice**: Use middleware for cross-cutting concerns.

```csharp
// ✅ Good custom middleware
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        _logger.LogInformation("Request: {Method} {Path}", 
            context.Request.Method, 
            context.Request.Path);

        await _next(context); // Call next middleware

        _logger.LogInformation("Response: {StatusCode}", 
            context.Response.StatusCode);
    }
}

// Extension method for registration
public static class RequestLoggingMiddlewareExtensions
{
    public static IApplicationBuilder UseRequestLogging(this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<RequestLoggingMiddleware>();
    }
}

// Usage
app.UseRequestLogging();
```

### 2.3 Exception Handling Middleware

**Best Practice**: Centralize exception handling.

```csharp
// ✅ Global exception handler
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        context.Response.StatusCode = 500;
        context.Response.ContentType = "application/json";

        var exceptionHandlerFeature = context.Features.Get<IExceptionHandlerFeature>();
        var exception = exceptionHandlerFeature?.Error;

        var logger = context.RequestServices.GetRequiredService<ILogger<Program>>();
        logger.LogError(exception, "Unhandled exception");

        var response = new
        {
            error = "An error occurred processing your request.",
            requestId = Activity.Current?.Id ?? context.TraceIdentifier
        };

        await context.Response.WriteAsJsonAsync(response);
    });
});

// ❌ Bad - try-catch in every action
[HttpGet]
public async Task<ActionResult<Product>> GetById(int id)
{
    try // Don't do this in every action
    {
        var product = await _service.GetByIdAsync(id);
        return Ok(product);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error");
        return StatusCode(500);
    }
}
```

---

## 3. Dependency Injection in ASP.NET

### 3.1 Service Registration

**Best Practice**: Register services with appropriate lifetimes.

```csharp
// ✅ Good service registration
builder.Services.AddScoped<IProductService, ProductService>(); // Scoped to HTTP request
builder.Services.AddScoped<ApplicationDbContext>(); // DbContext always Scoped
builder.Services.AddSingleton<ICacheService, MemoryCacheService>(); // Singleton for cache
builder.Services.AddTransient<IEmailSender, EmailSender>(); // New instance each time

// ✅ Register HttpClient properly
builder.Services.AddHttpClient<IExternalApiClient, ExternalApiClient>();

// ❌ Bad - DbContext as Singleton (NEVER do this)
builder.Services.AddSingleton<ApplicationDbContext>(); // NOT THREAD-SAFE!
```

### 3.2 Constructor Injection

**Best Practice**: Use constructor injection for dependencies.

```csharp
// ✅ Good - constructor injection
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(
        IProductService productService,
        ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<Product>>> GetAll()
    {
        var products = await _productService.GetAllAsync();
        return Ok(products);
    }
}

// ❌ Bad - service locator pattern
public class ProductsController : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Product>>> GetAll(
        [FromServices] IProductService productService) // Anti-pattern
    {
        var products = await productService.GetAllAsync();
        return Ok(products);
    }
}
```

### 3.3 Avoiding Captive Dependencies

**Critical**: Longer-lived services cannot depend on shorter-lived services.

```csharp
// ❌ Bad - Singleton capturing Scoped dependency
public class NotificationService // Registered as Singleton
{
    private readonly ApplicationDbContext _context; // Scoped!

    public NotificationService(ApplicationDbContext context)
    {
        _context = context; // CAPTIVE DEPENDENCY - BUG!
    }
}

// ✅ Good - Use IServiceScopeFactory
public class NotificationService // Singleton
{
    private readonly IServiceScopeFactory _scopeFactory;

    public NotificationService(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }

    public async Task SendNotificationsAsync()
    {
        using var scope = _scopeFactory.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        
        // Use context safely
    }
}
```

---

## 4. Configuration

### 4.1 appsettings.json Structure

**Best Practice**: Use structured configuration with strong typing.

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=...;Database=...;Trusted_Connection=True;"
  },
  "AppSettings": {
    "JwtSecret": "UseUserSecretsOrKeyVault",
    "JwtExpirationMinutes": 60,
    "MaxUploadSizeMB": 10
  },
  "ExternalApis": {
    "PaymentApi": {
      "BaseUrl": "https://api.payment.com",
      "ApiKey": "UseUserSecretsOrKeyVault"
    }
  }
}
```

### 4.2 Options Pattern

**Best Practice**: Bind configuration to strongly-typed classes.

```csharp
// ✅ Good - Options pattern
public class AppSettings
{
    public string JwtSecret { get; set; }
    public int JwtExpirationMinutes { get; set; }
    public int MaxUploadSizeMB { get; set; }
}

// Registration
builder.Services.Configure<AppSettings>(builder.Configuration.GetSection("AppSettings"));

// Usage
public class TokenService
{
    private readonly AppSettings _settings;

    public TokenService(IOptions<AppSettings> options)
    {
        _settings = options.Value;
    }

    public string GenerateToken(User user)
    {
        // Use _settings.JwtSecret, _settings.JwtExpirationMinutes
    }
}

// ❌ Bad - reading config directly
public class TokenService
{
    private readonly IConfiguration _configuration;

    public TokenService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public string GenerateToken(User user)
    {
        var secret = _configuration["AppSettings:JwtSecret"]; // String-based, no validation
    }
}
```

### 4.3 Secrets Management

**Critical**: Never hardcode secrets.

```csharp
// ❌ CRITICAL - Never hardcode secrets
public class EmailService
{
    private const string ApiKey = "sk_live_51ABC..."; // SECURITY ISSUE!
}

// ✅ Good - User Secrets for development
// dotnet user-secrets set "SendGrid:ApiKey" "sk_live_..."

// ✅ Good - Azure Key Vault for production
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{keyVaultName}.vault.azure.net/"),
    new DefaultAzureCredential());

// ✅ Good - Environment variables
var apiKey = builder.Configuration["SendGrid:ApiKey"];
```

---

## 5. Authentication and Authorization

### 5.1 JWT Bearer Authentication

**Best Practice**: Configure JWT properly with validation.

```csharp
// ✅ Good JWT configuration
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Secret"]))
        };
    });

// ❌ Bad - no validation
options.TokenValidationParameters = new TokenValidationParameters
{
    ValidateIssuer = false, // Security issue
    ValidateAudience = false, // Security issue
    ValidateLifetime = false // Allows expired tokens!
};
```

### 5.2 Authorization Attributes

**Best Practice**: Use authorization attributes consistently.

```csharp
// ✅ Good - controller-level + action-level auth
[Authorize] // All actions require authentication
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet] // Requires authentication (inherited)
    public async Task<ActionResult<IEnumerable<Product>>> GetAll()
    {
    }

    [Authorize(Roles = "Admin")] // Requires Admin role
    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
    }

    [AllowAnonymous] // Override - allows anonymous access
    [HttpGet("public")]
    public async Task<ActionResult<IEnumerable<Product>>> GetPublicProducts()
    {
    }
}

// ❌ Bad - no authorization
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpDelete("{id}")] // Anyone can delete!
    public async Task<IActionResult> Delete(int id)
    {
    }
}
```

### 5.3 Policy-Based Authorization

**Best Practice**: Use policies for complex authorization rules.

```csharp
// ✅ Good - policy-based authorization
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => 
        policy.RequireRole("Admin"));
    
    options.AddPolicy("CanEditProducts", policy =>
        policy.RequireClaim("Permission", "EditProducts"));
    
    options.AddPolicy("MinimumAge", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(18)));
});

// Usage
[Authorize(Policy = "CanEditProducts")]
[HttpPut("{id}")]
public async Task<IActionResult> Update(int id, ProductDto dto)
{
}
```

---

## 6. Model Validation

### 6.1 DataAnnotations

**Best Practice**: Use validation attributes on DTOs.

```csharp
// ✅ Good - validated DTO
public class CreateProductDto
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; }

    [Range(0.01, double.MaxValue, ErrorMessage = "Price must be positive")]
    public decimal Price { get; set; }

    [Required]
    [EmailAddress]
    public string ContactEmail { get; set; }

    [Url]
    public string? Website { get; set; }
}

// ✅ Automatic validation with [ApiController]
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpPost]
    public async Task<ActionResult<Product>> Create(CreateProductDto dto)
    {
        // ModelState automatically validated by [ApiController]
        // Returns 400 Bad Request with validation errors if invalid
        
        var product = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }
}

// ❌ Bad - no validation
public class CreateProductDto
{
    public string Name { get; set; } // Could be null or empty
    public decimal Price { get; set; } // Could be negative
}
```

### 6.2 Custom Validation

**Best Practice**: Create custom validators for complex rules.

```csharp
// ✅ Good - custom validation attribute
public class FutureDateAttribute : ValidationAttribute
{
    protected override ValidationResult IsValid(object value, ValidationContext validationContext)
    {
        if (value is DateTime date)
        {
            if (date <= DateTime.UtcNow)
            {
                return new ValidationResult("Date must be in the future");
            }
        }
        return ValidationResult.Success;
    }
}

// Usage
public class CreateEventDto
{
    [Required]
    public string Title { get; set; }

    [FutureDate]
    public DateTime StartDate { get; set; }
}
```

### 6.3 FluentValidation

**Best Practice**: Use FluentValidation for complex scenarios.

```csharp
// ✅ Good - FluentValidation
public class CreateProductDtoValidator : AbstractValidator<CreateProductDto>
{
    public CreateProductDtoValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .Length(3, 100)
            .WithMessage("Name must be between 3 and 100 characters");

        RuleFor(x => x.Price)
            .GreaterThan(0)
            .WithMessage("Price must be positive");

        RuleFor(x => x.ContactEmail)
            .NotEmpty()
            .EmailAddress();

        When(x => !string.IsNullOrEmpty(x.Website), () =>
        {
            RuleFor(x => x.Website)
                .Must(BeAValidUrl)
                .WithMessage("Website must be a valid URL");
        });
    }

    private bool BeAValidUrl(string url)
    {
        return Uri.TryCreate(url, UriKind.Absolute, out _);
    }
}

// Registration
builder.Services.AddValidatorsFromAssemblyContaining<CreateProductDtoValidator>();
builder.Services.AddFluentValidationAutoValidation();
```

---

## 7. Web API Patterns

### 7.1 RESTful Design

**Best Practice**: Follow REST conventions.

```csharp
// ✅ Good RESTful API
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    // GET api/products - List all
    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetAll([FromQuery] ProductFilter filter)
    {
        var products = await _service.GetAllAsync(filter);
        return Ok(products);
    }

    // GET api/products/5 - Get one
    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        var product = await _service.GetByIdAsync(id);
        if (product == null) return NotFound();
        return Ok(product);
    }

    // POST api/products - Create
    [HttpPost]
    public async Task<ActionResult<ProductDto>> Create(CreateProductDto dto)
    {
        var product = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }

    // PUT api/products/5 - Update (full)
    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, UpdateProductDto dto)
    {
        if (id != dto.Id) return BadRequest();
        await _service.UpdateAsync(dto);
        return NoContent();
    }

    // PATCH api/products/5 - Update (partial)
    [HttpPatch("{id}")]
    public async Task<IActionResult> Patch(int id, JsonPatchDocument<ProductDto> patchDoc)
    {
        var product = await _service.GetByIdAsync(id);
        if (product == null) return NotFound();
        
        patchDoc.ApplyTo(product, ModelState);
        if (!ModelState.IsValid) return BadRequest(ModelState);
        
        await _service.UpdateAsync(product);
        return NoContent();
    }

    // DELETE api/products/5 - Delete
    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var success = await _service.DeleteAsync(id);
        if (!success) return NotFound();
        return NoContent();
    }
}

// ❌ Bad - not RESTful
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet("GetAllProducts")] // Redundant, not RESTful
    [HttpPost("DeleteProduct/{id}")] // Wrong verb
    [HttpGet("CreateProduct")] // Wrong verb
}
```

### 7.2 API Versioning

**Best Practice**: Version your APIs.

```csharp
// ✅ Good - API versioning
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
});

// Version 1
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class ProductsV1Controller : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDtoV1>>> GetAll()
    {
        // v1 implementation
    }
}

// Version 2 with breaking changes
[ApiController]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class ProductsV2Controller : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProductDtoV2>>> GetAll()
    {
        // v2 implementation with new fields
    }
}
```

### 7.3 Response Caching

**Best Practice**: Cache appropriate responses.

```csharp
// ✅ Good - response caching
builder.Services.AddResponseCaching();

app.UseResponseCaching();

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]
    [ResponseCache(Duration = 60)] // Cache for 60 seconds
    public async Task<ActionResult<IEnumerable<Product>>> GetAll()
    {
        var products = await _service.GetAllAsync();
        return Ok(products);
    }

    [HttpGet("{id}")]
    [ResponseCache(Duration = 300, VaryByHeader = "Accept-Language")]
    public async Task<ActionResult<Product>> GetById(int id)
    {
        var product = await _service.GetByIdAsync(id);
        if (product == null) return NotFound();
        return Ok(product);
    }

    [HttpPost]
    [ResponseCache(NoStore = true)] // Never cache POST responses
    public async Task<ActionResult<Product>> Create(CreateProductDto dto)
    {
        var product = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }
}
```

---

## 8. Minimal APIs (.NET 6+)

### 8.1 Minimal API Structure

**Best Practice**: Organize minimal APIs for clarity.

```csharp
// ✅ Good - organized minimal APIs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Group related endpoints
var productsGroup = app.MapGroup("/api/products")
    .RequireAuthorization();

productsGroup.MapGet("/", async (IProductService service) =>
{
    var products = await service.GetAllAsync();
    return Results.Ok(products);
});

productsGroup.MapGet("/{id}", async (int id, IProductService service) =>
{
    var product = await service.GetByIdAsync(id);
    return product is not null ? Results.Ok(product) : Results.NotFound();
});

productsGroup.MapPost("/", async (CreateProductDto dto, IProductService service) =>
{
    var product = await service.CreateAsync(dto);
    return Results.Created($"/api/products/{product.Id}", product);
});

app.Run();

// ❌ Bad - unorganized
app.MapGet("/GetProducts", async (IProductService service) => { });
app.MapGet("/Product/{id}", async (int id, IProductService service) => { });
app.MapPost("/CreateProduct", async (CreateProductDto dto, IProductService service) => { });
```

---

## 9. Razor Pages / MVC

### 9.1 View Models

**Best Practice**: Use view models, not domain entities.

```csharp
// ✅ Good - separate view model
public class ProductViewModel
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string FormattedPrice { get; set; }
    public bool IsAvailable { get; set; }
}

public class ProductsController : Controller
{
    public async Task<IActionResult> Index()
    {
        var products = await _service.GetAllAsync();
        var viewModels = products.Select(p => new ProductViewModel
        {
            Id = p.Id,
            Name = p.Name,
            FormattedPrice = p.Price.ToString("C"),
            IsAvailable = p.Stock > 0
        });
        
        return View(viewModels);
    }
}

// ❌ Bad - exposing domain entities to views
public async Task<IActionResult> Index()
{
    var products = await _context.Products.ToListAsync(); // Exposes EF entity
    return View(products);
}
```

### 9.2 Tag Helpers

**Best Practice**: Use tag helpers over HTML helpers.

```html
<!-- ✅ Good - tag helpers -->
<form asp-controller="Products" asp-action="Create" method="post">
    <label asp-for="Name"></label>
    <input asp-for="Name" class="form-control" />
    <span asp-validation-for="Name" class="text-danger"></span>
    
    <button type="submit">Create</button>
</form>

<!-- ❌ Bad - HTML helpers (legacy) -->
@using (Html.BeginForm("Create", "Products", FormMethod.Post))
{
    @Html.LabelFor(m => m.Name)
    @Html.TextBoxFor(m => m.Name, new { @class = "form-control" })
    @Html.ValidationMessageFor(m => m.Name)
}
```

---

## 10. Static Files

### 10.1 wwwroot Configuration

**Best Practice**: Configure static files properly.

```csharp
// ✅ Good - static file configuration
app.UseStaticFiles(new StaticFileOptions
{
    OnPrepareResponse = ctx =>
    {
        // Cache static files for 7 days
        ctx.Context.Response.Headers.Append("Cache-Control", "public,max-age=604800");
    }
});

// Serve files from additional locations
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(
        Path.Combine(Directory.GetCurrentDirectory(), "StaticFiles")),
    RequestPath = "/static"
});
```

---

## Common Anti-Patterns to Avoid

1. **Sync-over-Async in Controllers**: Never use `.Result` or `.Wait()`
2. **Fat Controllers**: Move business logic to services
3. **DbContext in Singleton**: Always Scoped
4. **Hardcoded Secrets**: Use User Secrets or Key Vault
5. **No Authorization**: Secure all endpoints except public ones
6. **Ignoring ModelState**: Validate input
7. **Wrong HTTP Verbs**: GET for queries, POST for creates, etc.
8. **Not Using [ApiController]**: Automatic model validation
9. **Exposing Domain Entities**: Use DTOs/ViewModels
10. **Global Error Swallowing**: Use exception middleware

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
