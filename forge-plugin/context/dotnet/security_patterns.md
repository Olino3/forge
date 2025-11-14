# .NET Security Patterns

This file documents security best practices specific to .NET applications, including OWASP Top 10 mitigations, authentication, authorization, and secure coding patterns.

## Purpose

Load this file when reviewing:
- Authentication and authorization code
- User input handling
- Data access with user-provided input
- API security
- Configuration and secrets management

---

## 1. SQL Injection Prevention

### 1.1 Parameterized Queries (Critical)

**Rule**: NEVER concatenate user input into SQL queries.

```csharp
// ❌ CRITICAL - SQL Injection vulnerability
public async Task<List<Product>> SearchProductsAsync(string searchTerm)
{
    var sql = $"SELECT * FROM Products WHERE Name LIKE '{searchTerm}%'";
    return await _context.Products.FromSqlRaw(sql).ToListAsync();
}
// If searchTerm = "'; DROP TABLE Products; --", database destroyed!

// ✅ Good - FromSqlInterpolated (auto-parameterized)
public async Task<List<Product>> SearchProductsAsync(string searchTerm)
{
    return await _context.Products
        .FromSqlInterpolated($"SELECT * FROM Products WHERE Name LIKE {searchTerm + "%"}")
        .ToListAsync();
}

// ✅ Good - FromSqlRaw with parameters
public async Task<List<Product>> SearchProductsAsync(string searchTerm)
{
    return await _context.Products
        .FromSqlRaw("SELECT * FROM Products WHERE Name LIKE {0}", searchTerm + "%")
        .ToListAsync();
}

// ✅ Best - use LINQ (automatic parameterization)
public async Task<List<Product>> SearchProductsAsync(string searchTerm)
{
    return await _context.Products
        .Where(p => p.Name.StartsWith(searchTerm))
        .ToListAsync();
}
```

### 1.2 ORM Usage

**Best Practice**: Prefer Entity Framework or Dapper with parameterization.

```csharp
// ✅ Good - Entity Framework (safe by default)
public async Task<Product> GetProductAsync(int id)
{
    return await _context.Products.FindAsync(id);
}

// ✅ Good - Dapper with parameters
public async Task<Product> GetProductAsync(int id)
{
    using var connection = new SqlConnection(_connectionString);
    return await connection.QueryFirstOrDefaultAsync<Product>(
        "SELECT * FROM Products WHERE Id = @Id",
        new { Id = id }
    );
}

// ❌ CRITICAL - Dapper with string interpolation
public async Task<Product> GetProductAsync(string name)
{
    using var connection = new SqlConnection(_connectionString);
    return await connection.QueryFirstOrDefaultAsync<Product>(
        $"SELECT * FROM Products WHERE Name = '{name}'" // VULNERABLE!
    );
}
```

---

## 2. Cross-Site Scripting (XSS)

### 2.1 Razor Automatic Encoding

**Best Practice**: Razor automatically HTML-encodes output.

```html
<!-- ✅ Good - automatic encoding -->
<p>@Model.UserInput</p>
<!-- If UserInput = "<script>alert('XSS')</script>", rendered as:
     &lt;script&gt;alert('XSS')&lt;/script&gt; -->

<!-- ❌ CRITICAL - Html.Raw bypasses encoding -->
<p>@Html.Raw(Model.UserInput)</p>
<!-- <script> executes! -->
```

### 2.2 When to Use Html.Raw

**Rule**: Only use `Html.Raw` with trusted content.

```html
<!-- ✅ Good - trusted admin-generated content -->
@{
    var adminGeneratedHtml = await _contentService.GetPageContentAsync();
    // Content is created by admins in CMS, sanitized on save
}
<div>@Html.Raw(adminGeneratedHtml)</div>

<!-- ❌ CRITICAL - user input with Html.Raw -->
<div>@Html.Raw(Model.UserComment)</div> <!-- XSS!!! -->

<!-- ✅ Good - user input without Html.Raw -->
<div>@Model.UserComment</div> <!-- Safe, auto-encoded -->
```

### 2.3 JavaScript Context

**Best Practice**: Use JSON encoding for JavaScript contexts.

```html
<!-- ✅ Good - JSON encoding -->
<script>
    var userData = @Html.Raw(Json.Serialize(Model.User));
</script>

<!-- ❌ Bad - direct interpolation in JavaScript -->
<script>
    var userName = "@Model.UserName"; // Can break out of string
</script>
```

### 2.4 Content Security Policy

**Best Practice**: Implement CSP headers.

```csharp
// ✅ Good - CSP middleware
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("Content-Security-Policy",
        "default-src 'self'; " +
        "script-src 'self'; " +
        "style-src 'self' 'unsafe-inline'; " +
        "img-src 'self' https:; " +
        "font-src 'self'; " +
        "connect-src 'self'; " +
        "frame-ancestors 'none';");
    
    await next();
});
```

---

## 3. Cross-Site Request Forgery (CSRF)

### 3.1 Anti-Forgery Tokens

**Best Practice**: Use `[ValidateAntiForgeryToken]` on POST/PUT/DELETE actions.

```csharp
// ✅ Good - CSRF protection
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> DeleteAccount(int userId)
{
    await _userService.DeleteAccountAsync(userId);
    return RedirectToAction("Index");
}

// ❌ CRITICAL - no CSRF protection
[HttpPost]
public async Task<IActionResult> DeleteAccount(int userId)
{
    await _userService.DeleteAccountAsync(userId); // Can be triggered from malicious site
    return RedirectToAction("Index");
}
```

### 3.2 Anti-Forgery in Forms

**Best Practice**: Include anti-forgery token in forms.

```html
<!-- ✅ Good - anti-forgery token -->
<form asp-action="DeleteAccount" asp-controller="Account" method="post">
    @Html.AntiForgeryToken()
    <button type="submit">Delete Account</button>
</form>

<!-- Or with tag helper -->
<form asp-action="DeleteAccount" method="post">
    <!-- Token automatically included with asp-action -->
    <button type="submit">Delete Account</button>
</form>
```

### 3.3 CSRF for APIs

**Best Practice**: Use SameSite cookies or custom headers for APIs.

```csharp
// ✅ Good - SameSite cookie configuration
builder.Services.AddAntiforgery(options =>
{
    options.Cookie.SameSite = SameSiteMode.Strict;
    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
});

// For APIs, use custom headers
[HttpPost]
public async Task<IActionResult> ApiEndpoint()
{
    // Validate custom header
    if (!Request.Headers.ContainsKey("X-CSRF-Token"))
    {
        return BadRequest("CSRF token missing");
    }
    // Process request
}
```

---

## 4. Authentication

### 4.1 ASP.NET Core Identity

**Best Practice**: Use Identity for password management.

```csharp
// ✅ Good - ASP.NET Core Identity handles hashing
builder.Services.AddDefaultIdentity<ApplicationUser>(options =>
{
    options.Password.RequireDigit = true;
    options.Password.RequiredLength = 12;
    options.Password.RequireNonAlphanumeric = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireLowercase = true;
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
})
.AddEntityFrameworkStores<ApplicationDbContext>();

// ❌ CRITICAL - never store passwords in plain text
public async Task CreateUserAsync(string username, string password)
{
    var user = new User
    {
        Username = username,
        Password = password // PLAINTEXT PASSWORD!!!
    };
    await _context.Users.AddAsync(user);
    await _context.SaveChangesAsync();
}

// ❌ CRITICAL - weak hashing (MD5, SHA1)
public string HashPassword(string password)
{
    using var md5 = MD5.Create();
    var hash = md5.ComputeHash(Encoding.UTF8.GetBytes(password));
    return Convert.ToBase64String(hash); // MD5 is broken!
}
```

### 4.2 JWT Configuration

**Best Practice**: Configure JWT securely.

```csharp
// ✅ Good - secure JWT configuration
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true, // Check expiration
            ValidateIssuerSigningKey = true,
            ValidIssuer = configuration["Jwt:Issuer"],
            ValidAudience = configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(configuration["Jwt:Secret"])),
            ClockSkew = TimeSpan.FromMinutes(5) // Acceptable clock skew
        };
    });

// ❌ CRITICAL - weak JWT configuration
options.TokenValidationParameters = new TokenValidationParameters
{
    ValidateIssuer = false, // Accepts tokens from anyone
    ValidateAudience = false, // Tokens can be used anywhere
    ValidateLifetime = false, // Expired tokens still valid
    RequireExpirationTime = false // No expiration required
};
```

### 4.3 Token Expiration

**Best Practice**: Set appropriate token expiration.

```csharp
// ✅ Good - short-lived access tokens
var token = new JwtSecurityToken(
    issuer: _configuration["Jwt:Issuer"],
    audience: _configuration["Jwt:Audience"],
    claims: claims,
    expires: DateTime.UtcNow.AddMinutes(15), // 15-minute expiration
    signingCredentials: signingCredentials
);

// ❌ Bad - long-lived tokens
expires: DateTime.UtcNow.AddYears(1) // Token valid for a year!
```

---

## 5. Authorization

### 5.1 Role-Based Authorization

**Best Practice**: Use `[Authorize(Roles = "...")]` consistently.

```csharp
// ✅ Good - role-based authorization
[Authorize(Roles = "Admin")]
[HttpDelete("{id}")]
public async Task<IActionResult> DeleteUser(int id)
{
    await _userService.DeleteAsync(id);
    return NoContent();
}

// ❌ CRITICAL - no authorization
[HttpDelete("{id}")]
public async Task<IActionResult> DeleteUser(int id)
{
    await _userService.DeleteAsync(id); // Anyone can delete users!
    return NoContent();
}
```

### 5.2 Policy-Based Authorization

**Best Practice**: Use policies for complex authorization logic.

```csharp
// ✅ Good - policy-based authorization
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("CanEditProducts", policy =>
        policy.RequireClaim("Permission", "EditProducts"));
    
    options.AddPolicy("CanDeleteUsers", policy =>
        policy.RequireRole("Admin")
              .RequireClaim("Permission", "DeleteUsers"));
});

[Authorize(Policy = "CanEditProducts")]
[HttpPut("{id}")]
public async Task<IActionResult> UpdateProduct(int id, ProductDto dto)
{
    await _productService.UpdateAsync(id, dto);
    return NoContent();
}
```

### 5.3 Resource-Based Authorization

**Best Practice**: Check authorization for specific resources.

```csharp
// ✅ Good - resource-based authorization
[HttpPut("{id}")]
public async Task<IActionResult> UpdateOrder(int id, UpdateOrderDto dto)
{
    var order = await _orderService.GetByIdAsync(id);
    if (order == null) return NotFound();
    
    // Check if user owns the order
    var authResult = await _authorizationService.AuthorizeAsync(
        User, order, "CanEditOrder");
    
    if (!authResult.Succeeded)
    {
        return Forbid();
    }
    
    await _orderService.UpdateAsync(order, dto);
    return NoContent();
}
```

---

## 6. Secrets Management

### 6.1 Never Hardcode Secrets

**Critical**: Never commit secrets to source control.

```csharp
// ❌ CRITICAL - hardcoded secrets
public class EmailService
{
    private const string ApiKey = "sk_live_51ABC..."; // LEAKED TO SOURCE CONTROL
    private const string SmtpPassword = "MyP@ssw0rd"; // LEAKED TO SOURCE CONTROL
}

// ✅ Good - User Secrets (development)
// dotnet user-secrets set "SendGrid:ApiKey" "sk_live_..."
// dotnet user-secrets set "Email:SmtpPassword" "MyP@ssw0rd"

public class EmailService
{
    private readonly string _apiKey;
    
    public EmailService(IConfiguration configuration)
    {
        _apiKey = configuration["SendGrid:ApiKey"]; // From secrets
    }
}
```

### 6.2 Azure Key Vault (Production)

**Best Practice**: Use Key Vault for production secrets.

```csharp
// ✅ Good - Azure Key Vault
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{keyVaultName}.vault.azure.net/"),
    new DefaultAzureCredential());

// Secrets automatically loaded from Key Vault
var apiKey = builder.Configuration["SendGrid-ApiKey"];
```

### 6.3 Environment Variables

**Best Practice**: Use environment variables for configuration.

```csharp
// ✅ Good - environment variables
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? Environment.GetEnvironmentVariable("DB_CONNECTION_STRING");
```

---

## 7. Input Validation

### 7.1 Model Validation

**Best Practice**: Validate all user input.

```csharp
// ✅ Good - validated DTO
public class CreateProductDto
{
    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; }

    [Range(0.01, double.MaxValue)]
    public decimal Price { get; set; }

    [Required]
    [Url]
    public string ImageUrl { get; set; }
}

[ApiController]
[HttpPost]
public async Task<ActionResult<Product>> Create(CreateProductDto dto)
{
    // ModelState automatically validated by [ApiController]
    var product = await _productService.CreateAsync(dto);
    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
}

// ❌ Bad - no validation
public class CreateProductDto
{
    public string Name { get; set; } // Could be null, empty, or 10,000 characters
    public decimal Price { get; set; } // Could be negative
}
```

### 7.2 Whitelist vs Blacklist

**Best Practice**: Use whitelist validation, not blacklist.

```csharp
// ✅ Good - whitelist allowed characters
public bool IsValidUsername(string username)
{
    return Regex.IsMatch(username, @"^[a-zA-Z0-9_-]{3,20}$");
}

// ❌ Bad - blacklist dangerous characters (incomplete)
public bool IsValidUsername(string username)
{
    return !username.Contains("<") && !username.Contains(">");
    // What about ', ", ;, --, etc.?
}
```

### 7.3 File Upload Validation

**Best Practice**: Validate file uploads thoroughly.

```csharp
// ✅ Good - file upload validation
[HttpPost("upload")]
public async Task<IActionResult> UploadFile(IFormFile file)
{
    // Validate file size
    if (file.Length > 10 * 1024 * 1024) // 10 MB
    {
        return BadRequest("File too large");
    }
    
    // Validate file extension (whitelist)
    var allowedExtensions = new[] { ".jpg", ".jpeg", ".png", ".pdf" };
    var extension = Path.GetExtension(file.FileName).ToLowerInvariant();
    if (!allowedExtensions.Contains(extension))
    {
        return BadRequest("Invalid file type");
    }
    
    // Validate MIME type
    var allowedMimeTypes = new[] { "image/jpeg", "image/png", "application/pdf" };
    if (!allowedMimeTypes.Contains(file.ContentType))
    {
        return BadRequest("Invalid MIME type");
    }
    
    // Generate safe filename
    var safeFileName = $"{Guid.NewGuid()}{extension}";
    var filePath = Path.Combine(_uploadPath, safeFileName);
    
    using var stream = new FileStream(filePath, FileMode.Create);
    await file.CopyToAsync(stream);
    
    return Ok(new { fileName = safeFileName });
}

// ❌ CRITICAL - no validation
[HttpPost("upload")]
public async Task<IActionResult> UploadFile(IFormFile file)
{
    var filePath = Path.Combine(_uploadPath, file.FileName); // Path traversal!
    using var stream = new FileStream(filePath, FileMode.Create);
    await file.CopyToAsync(stream);
    return Ok();
}
```

---

## 8. Logging and Error Handling

### 8.1 Never Log Sensitive Data

**Critical**: Don't log passwords, tokens, PII.

```csharp
// ❌ CRITICAL - logging sensitive data
_logger.LogInformation("User {Username} logged in with password {Password}", 
    username, password); // PASSWORD IN LOGS!

_logger.LogInformation("JWT token: {Token}", jwtToken); // TOKEN IN LOGS!

// ✅ Good - don't log sensitive data
_logger.LogInformation("User {Username} logged in successfully", username);

// ✅ Good - log masked data
_logger.LogInformation("Credit card ending in {Last4} processed", 
    creditCard.Substring(creditCard.Length - 4));
```

### 8.2 Don't Expose Stack Traces

**Best Practice**: Hide implementation details in production.

```csharp
// ✅ Good - custom error responses
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        context.Response.StatusCode = 500;
        context.Response.ContentType = "application/json";

        var error = context.Features.Get<IExceptionHandlerFeature>();
        var logger = context.RequestServices.GetRequiredService<ILogger<Program>>();
        
        logger.LogError(error.Error, "Unhandled exception"); // Log full details
        
        // Return generic error to client
        await context.Response.WriteAsJsonAsync(new
        {
            error = "An error occurred processing your request.",
            requestId = Activity.Current?.Id ?? context.TraceIdentifier
        });
    });
});

// ❌ CRITICAL - exposing stack traces in production
app.UseDeveloperExceptionPage(); // Shows full stack trace to users!
```

---

## 9. HTTPS and Security Headers

### 9.1 HTTPS Enforcement

**Best Practice**: Enforce HTTPS in production.

```csharp
// ✅ Good - HTTPS enforcement
app.UseHttpsRedirection();
app.UseHsts(); // HTTP Strict Transport Security

// HSTS configuration
builder.Services.AddHsts(options =>
{
    options.MaxAge = TimeSpan.FromDays(365);
    options.IncludeSubDomains = true;
    options.Preload = true;
});
```

### 9.2 Security Headers

**Best Practice**: Add security headers.

```csharp
// ✅ Good - security headers middleware
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    context.Response.Headers.Add("Referrer-Policy", "strict-origin-when-cross-origin");
    context.Response.Headers.Add("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
    
    await next();
});
```

---

## 10. Deserialization Security

### 10.1 Type Validation

**Best Practice**: Validate types when deserializing.

```csharp
// ✅ Good - System.Text.Json (safe by default)
var product = JsonSerializer.Deserialize<Product>(json);

// ❌ Risky - Newtonsoft.Json with TypeNameHandling
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.All // DANGEROUS!
};
var obj = JsonConvert.DeserializeObject(json, settings);
// Attacker can specify arbitrary types to instantiate

// ✅ If you must use TypeNameHandling, limit it
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.Auto,
    SerializationBinder = new SafeSerializationBinder() // Custom binder
};
```

---

## Security Checklist

1. **SQL Injection**: ✅ Parameterized queries, ORM usage
2. **XSS**: ✅ Automatic encoding, avoid Html.Raw with user input
3. **CSRF**: ✅ Anti-forgery tokens on state-changing operations
4. **Authentication**: ✅ ASP.NET Core Identity, secure JWT config
5. **Authorization**: ✅ [Authorize] on sensitive endpoints
6. **Secrets**: ✅ Never hardcode, use Key Vault or User Secrets
7. **Input Validation**: ✅ DataAnnotations, whitelist validation
8. **File Uploads**: ✅ Validate size, extension, MIME type
9. **Logging**: ✅ Never log passwords, tokens, PII
10. **HTTPS**: ✅ Enforce HTTPS, HSTS, security headers

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
