---
id: "dotnet/security_patterns"
domain: dotnet
title: ".NET Security Patterns"
type: pattern
estimatedTokens: 1550
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "OWASP Top 10 for .NET"
    estimatedTokens: 95
    keywords: [owasp, top, net]
  - name: "SQL Injection Prevention"
    estimatedTokens: 34
    keywords: [sql, injection, prevention]
  - name: "Cross-Site Scripting (XSS)"
    estimatedTokens: 39
    keywords: [cross-site, scripting, xss]
  - name: "CSRF Protection"
    estimatedTokens: 24
    keywords: [csrf, protection]
  - name: "Authentication"
    estimatedTokens: 67
    keywords: [authentication]
  - name: "Authorization"
    estimatedTokens: 72
    keywords: [authorization]
  - name: "Secrets Management"
    estimatedTokens: 69
    keywords: [secrets, management]
  - name: "Input Validation"
    estimatedTokens: 58
    keywords: [input, validation]
  - name: "File Upload Security"
    estimatedTokens: 92
    keywords: [file, upload, security]
  - name: "Logging Security"
    estimatedTokens: 37
    keywords: [logging, security]
  - name: "HTTPS and Security Headers"
    estimatedTokens: 33
    keywords: [https, security, headers]
  - name: "JWT Security"
    estimatedTokens: 69
    keywords: [jwt, security]
  - name: "Common Detection Patterns"
    estimatedTokens: 63
    keywords: [detection, patterns]
  - name: "Security Checklist"
    estimatedTokens: 66
    keywords: [security, checklist]
  - name: "Official Resources"
    estimatedTokens: 23
    keywords: [official, resources]
tags: [dotnet, security, owasp, sql-injection, xss, csrf, authentication, jwt, secrets]
---

# .NET Security Patterns

Quick reference for .NET security best practices (OWASP Top 10). For detailed guidance, see [ASP.NET Core security](https://learn.microsoft.com/en-us/aspnet/core/security/).

---

## OWASP Top 10 for .NET

| Vulnerability | Detection Pattern | Fix | Learn More |
|---------------|-------------------|-----|------------|
| **SQL Injection** | String concat in SQL | Use parameterized queries or EF | [SQL injection prevention](https://learn.microsoft.com/en-us/ef/core/querying/sql-queries) |
| **XSS** | `@Html.Raw(userInput)` | Remove `Html.Raw`, auto-encode | [XSS prevention](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting) |
| **CSRF** | POST without `[ValidateAntiForgeryToken]` | Add token validation | [Anti-forgery](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery) |
| **Broken auth** | Weak password policy | Use ASP.NET Core Identity | [Identity](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity) |
| **Sensitive data** | Hardcoded secrets | Use User Secrets/Key Vault | [Secrets management](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) |
| **Missing auth** | No `[Authorize]` | Add authorization | [Authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/introduction) |
| **Insecure deserialization** | `TypeNameHandling.All` | Avoid or use custom binder | [Deserialization](https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide) |
| **Logging sensitive data** | Password/token in logs | Sanitize logs | [Logging](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/logging/) |

---

## SQL Injection Prevention

```csharp
// ❌ CRITICAL - SQL injection
_context.Products.FromSqlRaw($"SELECT * FROM Products WHERE Name = '{name}'");

// ✅ Parameterized with FromSqlInterpolated
_context.Products.FromSqlInterpolated($"SELECT * FROM Products WHERE Name = {name}");

// ✅ Best - Use LINQ (automatic parameterization)
_context.Products.Where(p => p.Name == name);
```

[SQL injection prevention](https://learn.microsoft.com/en-us/ef/core/querying/sql-queries#passing-parameters)

---

## Cross-Site Scripting (XSS)

| Pattern | Safe? | Recommendation |
|---------|-------|----------------|
| `@Model.UserInput` | ✅ Safe | Razor auto-encodes |
| `@Html.Raw(userInput)` | ❌ UNSAFE | Remove Html.Raw |
| `<script>var x = "@Model.Data";</script>` | ❌ UNSAFE | Use JSON encoding |
| `@Html.Raw(Json.Serialize(model))` | ✅ Safe | JSON context |

[XSS prevention in ASP.NET](https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting)

---

## CSRF Protection

```csharp
// ✅ POST/PUT/DELETE with anti-forgery
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> Delete(int id) { }

// Razor form automatically includes token with asp-action
<form asp-action="Delete" method="post">
    <button type="submit">Delete</button>
</form>
```

[Anti-forgery tokens](https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery)

---

## Authentication

| Pattern | Use Case | Configuration |
|---------|----------|---------------|
| **Identity** | Password-based auth | `AddDefaultIdentity<User>()` |
| **JWT Bearer** | API authentication | `AddJwtBearer()` |
| **OAuth/OpenID** | Third-party auth | `AddOAuth()`, `AddOpenIdConnect()` |
| **Cookies** | Traditional web apps | `AddCookie()` |

```csharp
// ✅ ASP.NET Core Identity with secure password policy
services.AddDefaultIdentity<User>(options =>
{
    options.Password.RequiredLength = 12;
    options.Password.RequireNonAlphanumeric = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireDigit = true;
    options.Lockout.MaxFailedAccessAttempts = 5;
}).AddEntityFrameworkStores<AppDbContext>();

// ❌ NEVER store plain-text passwords
user.Password = password;  // CRITICAL VULNERABILITY
```

[ASP.NET Core Identity](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity)

---

## Authorization

| Level | Attribute | Use When |
|-------|-----------|----------|
| **Anonymous** | `[AllowAnonymous]` | Public endpoints |
| **Authenticated** | `[Authorize]` | Logged-in users only |
| **Role-based** | `[Authorize(Roles = "Admin")]` | Specific roles |
| **Policy-based** | `[Authorize(Policy = "CanEdit")]` | Complex rules |
| **Resource-based** | `IAuthorizationService` | Per-resource checks |

```csharp
// ✅ Authorize attribute on sensitive endpoints
[Authorize(Roles = "Admin")]
[HttpDelete("{id}")]
public async Task<IActionResult> Delete(int id) { }

// ❌ CRITICAL - Missing authorization
[HttpDelete("{id}")]
public async Task<IActionResult> Delete(int id) { }  // Anyone can delete!
```

[Authorization in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/introduction)

---

## Secrets Management

| Environment | Storage | Access Method |
|-------------|---------|---------------|
| **Development** | User Secrets | `dotnet user-secrets set` |
| **Production** | Azure Key Vault | `AddAzureKeyVault()` |
| **CI/CD** | Environment variables | `Environment.GetEnvironmentVariable()` |

```csharp
// ❌ CRITICAL - Hardcoded secrets
private const string ApiKey = "sk_live_ABC123...";  // LEAKED!

// ✅ Configuration-based
private readonly string _apiKey;
public Service(IConfiguration config)
{
    _apiKey = config["ApiKeys:SendGrid"];  // From User Secrets/Key Vault
}

// Development: dotnet user-secrets set "ApiKeys:SendGrid" "sk_..."
// Production: Azure Key Vault or environment variables
```

[Safe storage of app secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets)

---

## Input Validation

```csharp
// ✅ DataAnnotations for validation
public class CreateUserDto
{
    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string Username { get; set; }

    [Required]
    [EmailAddress]
    public string Email { get; set; }

    [Required]
    [Range(0.01, double.MaxValue)]
    public decimal Price { get; set; }
}

// [ApiController] automatically validates ModelState

// ❌ No validation
public class CreateUserDto
{
    public string Username { get; set; }  // Could be null, empty, or 10,000 chars
}
```

[Model validation in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation)

---

## File Upload Security

```csharp
// ✅ Secure file upload
[HttpPost("upload")]
public async Task<IActionResult> Upload(IFormFile file)
{
    // Validate size
    if (file.Length > 10 * 1024 * 1024)
        return BadRequest("File too large");

    // Whitelist extensions
    var allowedExts = new[] { ".jpg", ".png", ".pdf" };
    var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
    if (!allowedExts.Contains(ext))
        return BadRequest("Invalid file type");

    // Validate MIME type
    var allowedMimes = new[] { "image/jpeg", "image/png", "application/pdf" };
    if (!allowedMimes.Contains(file.ContentType))
        return BadRequest("Invalid MIME type");

    // Generate safe filename (prevent path traversal)
    var safeFileName = $"{Guid.NewGuid()}{ext}";
    var path = Path.Combine(_uploadPath, safeFileName);

    using var stream = new FileStream(path, FileMode.Create);
    await file.CopyToAsync(stream);

    return Ok(new { fileName = safeFileName });
}

// ❌ CRITICAL - No validation
var path = Path.Combine(_uploadPath, file.FileName);  // Path traversal!
```

[Upload files in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/file-uploads)

---

## Logging Security

```csharp
// ❌ CRITICAL - Logging sensitive data
_logger.LogInformation("User {Email} logged in with password {Password}",
    email, password);  // PASSWORD IN LOGS!

// ✅ Don't log sensitive data
_logger.LogInformation("User {Email} logged in successfully", email);

// ✅ Mask sensitive data if needed
_logger.LogInformation("Card ending in {Last4} charged",
    card.Substring(card.Length - 4));
```

---

## HTTPS and Security Headers

```csharp
// ✅ Enforce HTTPS
app.UseHttpsRedirection();
app.UseHsts();

services.AddHsts(options =>
{
    options.MaxAge = TimeSpan.FromDays(365);
    options.IncludeSubDomains = true;
    options.Preload = true;
});

// ✅ Security headers
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    context.Response.Headers.Add("Referrer-Policy", "strict-origin-when-cross-origin");
    await next();
});
```

[Enforce HTTPS](https://learn.microsoft.com/en-us/aspnet/core/security/enforcing-ssl)

---

## JWT Security

```csharp
// ✅ Secure JWT configuration
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,           // ✅ Validate issuer
            ValidateAudience = true,         // ✅ Validate audience
            ValidateLifetime = true,         // ✅ Check expiration
            ValidateIssuerSigningKey = true, // ✅ Validate signature
            ValidIssuer = config["Jwt:Issuer"],
            ValidAudience = config["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(config["Jwt:Secret"])),
            ClockSkew = TimeSpan.FromMinutes(5)
        };
    });

// ❌ CRITICAL - Insecure JWT
ValidateIssuer = false,      // Accepts tokens from anyone
ValidateLifetime = false,    // Expired tokens work
ValidateIssuerSigningKey = false  // No signature check
```

[JWT bearer authentication](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/jwt-authn)

---

## Common Detection Patterns

```csharp
// ❌ SQL injection
FromSqlRaw($"SELECT * WHERE Name = '{name}'")

// ❌ XSS
@Html.Raw(userInput)

// ❌ Missing CSRF
[HttpPost] without [ValidateAntiForgeryToken]

// ❌ No authorization
[HttpDelete] without [Authorize]

// ❌ Hardcoded secrets
private const string Secret = "...";
connectionString = "Server=...;Password=hardcoded;";

// ❌ Weak password config
RequiredLength = 6
RequireNonAlphanumeric = false

// ❌ Logging sensitive data
_logger.Log("Password: {0}", password)
_logger.Log("Token: {0}", jwtToken)

// ❌ TypeNameHandling.All (deserialization)
TypeNameHandling = TypeNameHandling.All

// ❌ No file upload validation
Path.Combine(folder, file.FileName)  // Path traversal
```

---

## Security Checklist

- ✅ Parameterized queries (no SQL injection)
- ✅ Razor auto-encoding (no XSS with user input)
- ✅ `[ValidateAntiForgeryToken]` on POST/PUT/DELETE
- ✅ ASP.NET Core Identity with strong password policy
- ✅ `[Authorize]` on sensitive endpoints
- ✅ Secrets in User Secrets/Key Vault (never hardcoded)
- ✅ Input validation with DataAnnotations
- ✅ File upload validation (size, extension, MIME)
- ✅ HTTPS enforcement with HSTS
- ✅ Security headers (X-Frame-Options, CSP, etc.)
- ✅ JWT validation (issuer, audience, lifetime, signature)
- ✅ Never log passwords, tokens, or PII

---

## Official Resources

- **ASP.NET Core Security**: https://learn.microsoft.com/en-us/aspnet/core/security/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Authentication**: https://learn.microsoft.com/en-us/aspnet/core/security/authentication/
- **Authorization**: https://learn.microsoft.com/en-us/aspnet/core/security/authorization/
- **Data Protection**: https://learn.microsoft.com/en-us/aspnet/core/security/data-protection/

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
