# ASP.NET Core Patterns

Quick reference for ASP.NET Core (Web API, MVC, Razor Pages, Minimal APIs). For detailed examples, see [ASP.NET Core documentation](https://learn.microsoft.com/en-us/aspnet/core/).

---

## Common Anti-Patterns

| Anti-Pattern | Detection | Fix | Learn More |
|--------------|-----------|-----|------------|
| **Missing [ApiController]** | Controller without attribute | Add `[ApiController]` | [ApiController attribute](https://learn.microsoft.com/en-us/aspnet/core/web-api/#apicontroller-attribute) |
| **No model validation** | Direct use of model without check | Use `ModelState.IsValid` | [Model validation](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation) |
| **Missing [ValidateAntiForgeryToken]** | POST without CSRF token | Add attribute | [Anti-forgery](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery) |
| **Missing [Authorize]** | Sensitive endpoints public | Add authorization | [Authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/simple) |
| **Returning entities directly** | EF entities as API responses | Use DTOs with `response_model` | [DTOs](https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api#prevent-over-posting) |

---

## Controller Patterns

| Pattern | Use When | Base Class |
|---------|----------|------------|
| **API Controller** | REST APIs, JSON responses | `ControllerBase` |
| **MVC Controller** | Views, HTML responses | `Controller` |
| **Minimal API** | Simple endpoints (.NET 6+) | No controller |

```csharp
// ✅ API Controller
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        var product = await _service.GetByIdAsync(id);
        return product != null ? Ok(product) : NotFound();
    }
}

// ❌ Missing ApiController attribute
public class ProductsController : ControllerBase  // No [ApiController]
```

[Controllers](https://learn.microsoft.com/en-us/aspnet/core/web-api/)

---

## Action Return Types

| Return Type | Use When | Example |
|-------------|----------|---------|
| **ActionResult<T>** | API with typed response | `ActionResult<Product>` |
| **IActionResult** | Multiple return types | `Ok()`, `NotFound()`, `BadRequest()` |
| **T** | Always returns same type | `Product` (no flexibility) |

```csharp
// ✅ ActionResult<T> for type safety
[HttpGet("{id}")]
public async Task<ActionResult<Product>> GetById(int id)
{
    var product = await _repo.GetByIdAsync(id);
    return product != null ? Ok(product) : NotFound();
}

// ❌ No type safety
public async Task<IActionResult> GetById(int id)
{
    return Ok(product);  // No compile-time type check
}
```

[Action return types](https://learn.microsoft.com/en-us/aspnet/core/web-api/action-return-types)

---

## Status Codes

| Code | Method | Use When |
|------|--------|----------|
| **200 OK** | `Ok(data)` | Successful GET/PUT/PATCH |
| **201 Created** | `CreatedAtAction()` | Successful POST |
| **204 No Content** | `NoContent()` | Successful DELETE |
| **400 Bad Request** | `BadRequest(message)` | Invalid input |
| **401 Unauthorized** | `Unauthorized()` | Missing/invalid authentication |
| **403 Forbidden** | `Forbid()` | Authenticated but not authorized |
| **404 Not Found** | `NotFound()` | Resource doesn't exist |
| **500 Internal** | Exception handling | Server error |

```csharp
// ✅ Correct status codes
[HttpPost]
public async Task<ActionResult<Product>> Create(CreateProductDto dto)
{
    var product = await _service.CreateAsync(dto);
    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
}

[HttpDelete("{id}")]
public async Task<IActionResult> Delete(int id)
{
    await _service.DeleteAsync(id);
    return NoContent();
}
```

[HTTP status codes](https://learn.microsoft.com/en-us/aspnet/core/web-api/action-return-types#httpresults-type)

---

## Model Validation

```csharp
// ✅ DataAnnotations validation
public class CreateProductDto
{
    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; }

    [Range(0.01, double.MaxValue)]
    public decimal Price { get; set; }
}

// [ApiController] automatically validates ModelState
[HttpPost]
public async Task<ActionResult<Product>> Create(CreateProductDto dto)
{
    // No manual ModelState.IsValid check needed with [ApiController]
    var product = await _service.CreateAsync(dto);
    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
}

// ❌ No validation
[HttpPost]
public async Task<ActionResult<Product>> Create(CreateProductDto dto)
{
    // dto.Name could be null, empty, or 10,000 characters!
}
```

[Model validation](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation)

---

## Middleware Pipeline

| Middleware | Order | Purpose |
|------------|-------|---------|
| `UseExceptionHandler` | 1 | Global exception handling |
| `UseHsts` | 2 | HTTP Strict Transport Security |
| `UseHttpsRedirection` | 3 | Redirect HTTP → HTTPS |
| `UseStaticFiles` | 4 | Serve static files |
| `UseRouting` | 5 | Route matching |
| `UseCors` | 6 | CORS policy |
| `UseAuthentication` | 7 | Identify user |
| `UseAuthorization` | 8 | Authorize user |
| `UseEndpoints` / `MapControllers` | 9 | Execute endpoints |

```csharp
// ✅ Correct order
app.UseExceptionHandler("/error");
app.UseHsts();
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
```

[Middleware order](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/#middleware-order)

---

## CORS Configuration

```csharp
// ✅ Named CORS policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigin",
        policy => policy
            .WithOrigins("https://example.com")
            .AllowAnyMethod()
            .AllowAnyHeader());
});

app.UseCors("AllowSpecificOrigin");

// ❌ CRITICAL - Allow all origins in production
.AllowAnyOrigin()  // Security risk!
```

[CORS](https://learn.microsoft.com/en-us/aspnet/core/security/cors)

---

## Authentication & Authorization

```csharp
// ✅ JWT Bearer authentication
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = config["Jwt:Issuer"],
            ValidAudience = config["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(config["Jwt:Secret"]))
        };
    });

// ✅ Authorization on controllers
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase { }

// ✅ Role-based authorization
[Authorize(Roles = "Admin")]
[HttpDelete("{id}")]
public async Task<IActionResult> Delete(int id) { }
```

[Authentication](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/)

---

## Configuration

```csharp
// ✅ Strongly-typed configuration
public class JwtSettings
{
    public string Secret { get; set; }
    public string Issuer { get; set; }
    public int ExpirationMinutes { get; set; }
}

// appsettings.json
{
  "Jwt": {
    "Secret": "your-secret-key",
    "Issuer": "your-issuer",
    "ExpirationMinutes": 60
  }
}

// Register
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));

// Use
public class AuthService
{
    private readonly JwtSettings _settings;

    public AuthService(IOptions<JwtSettings> options)
    {
        _settings = options.Value;
    }
}
```

[Configuration](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/)

---

## Common Detection Patterns

```csharp
// ❌ Missing [ApiController]
public class ProductsController : ControllerBase

// ❌ No model validation
[HttpPost]
public IActionResult Create(Product product)
{
    _repo.Add(product);  // No validation!
}

// ❌ Missing [Authorize]
[HttpDelete("{id}")]
public IActionResult Delete(int id)  // Public delete!

// ❌ Returning entity directly
[HttpGet]
public async Task<List<Product>> GetAll()
{
    return await _context.Products.ToListAsync();  // EF entity exposed
}

// ❌ Wrong status code
[HttpPost]
public async Task<IActionResult> Create(Product product)
{
    await _repo.AddAsync(product);
    return Ok(product);  // Should be CreatedAtAction
}

// ❌ CORS allow all
.AllowAnyOrigin()
```

---

## ASP.NET Core Checklist

- ✅ `[ApiController]` on API controllers
- ✅ `ActionResult<T>` for typed responses
- ✅ `ModelState.IsValid` check (or [ApiController])
- ✅ DTOs for API responses (not EF entities)
- ✅ Correct HTTP status codes (201 for POST, 204 for DELETE)
- ✅ `[Authorize]` on protected endpoints
- ✅ `[ValidateAntiForgeryToken]` on forms
- ✅ CORS with specific origins (not AllowAnyOrigin)
- ✅ HTTPS enforcement in production
- ✅ Middleware in correct order

---

## Official Resources

- **ASP.NET Core Documentation**: https://learn.microsoft.com/en-us/aspnet/core/
- **Web API**: https://learn.microsoft.com/en-us/aspnet/core/web-api/
- **Security**: https://learn.microsoft.com/en-us/aspnet/core/security/
- **Performance**: https://learn.microsoft.com/en-us/aspnet/core/performance/performance-best-practices

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
