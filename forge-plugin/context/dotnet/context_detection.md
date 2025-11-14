# .NET Context Detection

This guide explains how to identify .NET project characteristics to inform code review strategy and context loading decisions.

## Purpose

**Context detection** enables you to:
- Understand the .NET technology stack being used
- Load appropriate context files for the specific framework
- Tailor review focus to the project's architecture
- Detect version-specific patterns and issues

**Perform context detection at the start of your first review of any .NET project.**

---

## Detection Categories

### 1. .NET Version Detection
### 2. C# Language Version
### 3. Framework Type (ASP.NET, Blazor, Console, etc.)
### 4. ORM Detection
### 5. Authentication System
### 6. Testing Framework
### 7. Package Ecosystem

---

## 1. .NET Version Detection

### Key Files to Check

**Primary Source**: `.csproj` files

```xml
<!-- .NET Framework 4.8 -->
<Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <TargetFrameworkVersion>v4.8</TargetFrameworkVersion>
  </PropertyGroup>
</Project>

<!-- .NET Core 3.1 -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>netcoreapp3.1</TargetFramework>
  </PropertyGroup>
</Project>

<!-- .NET 5 -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net5.0</TargetFramework>
  </PropertyGroup>
</Project>

<!-- .NET 6 -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>
</Project>

<!-- .NET 7 -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net7.0</TargetFramework>
  </PropertyGroup>
</Project>

<!-- .NET 8 (LTS) -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
</Project>
```

### Version Characteristics

| Version | Characteristics | Review Focus |
|---------|----------------|--------------|
| **.NET Framework 4.x** | Legacy, Windows-only, System.Web, .NET Standard 2.0 | Check for migration opportunities, legacy patterns, sync code |
| **.NET Core 3.1** | Cross-platform, no System.Web, EF Core 3.1 | Nullable reference types, async patterns, EF Core 3 behaviors |
| **.NET 5** | Unified platform, C# 9, single-file apps | Records, top-level statements, init properties |
| **.NET 6 (LTS)** | Minimal APIs, global usings, file-scoped namespaces | Hot reload, DateOnly/TimeOnly, HTTP/3 |
| **.NET 7** | Performance improvements, regex source gen | Rate limiting, output caching, required members |
| **.NET 8 (LTS)** | Latest LTS, Blazor improvements, AOT | Native AOT, primary constructors (C# 12), Blazor United |

### Detection Algorithm

```
1. Look for TargetFramework in .csproj
2. If found:
   - net8.0 → .NET 8
   - net7.0 → .NET 7
   - net6.0 → .NET 6
   - net5.0 → .NET 5
   - netcoreapp3.1 → .NET Core 3.1
   - v4.8, v4.7.2 → .NET Framework 4.x
3. Record version and set review expectations accordingly
```

---

## 2. C# Language Version

### Detection Method

**Primary Source**: `.csproj` files

```xml
<!-- Explicit C# version -->
<PropertyGroup>
  <LangVersion>12.0</LangVersion> <!-- C# 12 -->
</PropertyGroup>

<!-- Implicit (default for .NET version) -->
<!-- .NET 8 → C# 12 -->
<!-- .NET 7 → C# 11 -->
<!-- .NET 6 → C# 10 -->
<!-- .NET 5 → C# 9 -->
<!-- .NET Core 3.1 → C# 8 -->
```

### C# Version Features to Check For

| C# Version | Key Features | Review Focus |
|------------|-------------|--------------|
| **C# 8** | Nullable reference types, async streams, ranges, switch expressions | Check for nullable context usage, proper null checks |
| **C# 9** | Records, init-only properties, top-level statements, pattern matching enhancements | Ensure proper record usage, immutability patterns |
| **C# 10** | Global usings, file-scoped namespaces, record structs, interpolated string handlers | Check for reduced boilerplate, consistent style |
| **C# 11** | Required members, list patterns, raw string literals, generic math | Validate required member usage, new pattern matching |
| **C# 12** | Primary constructors, collection expressions, default lambda parameters | Check for primary constructor usage, collection initializers |

### Detection Algorithm

```
1. Check for explicit <LangVersion> in .csproj
2. If not found, infer from .NET version:
   - .NET 8 → C# 12
   - .NET 7 → C# 11
   - .NET 6 → C# 10
   - .NET 5 → C# 9
   - .NET Core 3.1 → C# 8
3. Look for feature usage in code to confirm
```

---

## 3. Framework Type Detection

### Web Frameworks

#### ASP.NET Core Web API

**Indicators**:
```csharp
// .csproj
<Project Sdk="Microsoft.NET.Sdk.Web">

// Program.cs or Startup.cs
builder.Services.AddControllers();
app.MapControllers();

// Controller files
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
```

**Load Context**: `aspnet_patterns.md`, `async_patterns.md`, `security_patterns.md`

---

#### ASP.NET Core MVC / Razor Pages

**Indicators**:
```csharp
// Program.cs
builder.Services.AddRazorPages();
app.MapRazorPages();

// Or
builder.Services.AddControllersWithViews();
app.MapControllerRoute(...);

// Presence of Views/ or Pages/ directories
// .cshtml files
```

**Load Context**: `aspnet_patterns.md`, `security_patterns.md` (XSS, CSRF)

---

#### Blazor Server

**Indicators**:
```csharp
// .csproj
<Project Sdk="Microsoft.NET.Sdk.Web">

// Program.cs
builder.Services.AddServerSideBlazor();
app.MapBlazorHub();

// .razor files
@code {
    protected override async Task OnInitializedAsync()
}
```

**Load Context**: `blazor_patterns.md`, `async_patterns.md`, `di_patterns.md`

---

#### Blazor WebAssembly

**Indicators**:
```csharp
// .csproj
<Project Sdk="Microsoft.NET.Sdk.BlazorWebAssembly">

// Program.cs
builder.RootComponents.Add<App>("#app");
await builder.Build().RunAsync();

// wwwroot/index.html
<script src="_framework/blazor.webassembly.js"></script>
```

**Load Context**: `blazor_patterns.md`, `async_patterns.md`, `di_patterns.md`

---

#### Minimal APIs (.NET 6+)

**Indicators**:
```csharp
// Program.cs (no Startup.cs)
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/products", async (ProductService service) => 
{
    return await service.GetAllAsync();
});

// No controllers, direct route mapping
```

**Load Context**: `aspnet_patterns.md`, `async_patterns.md`, `di_patterns.md`

---

### Non-Web Frameworks

#### Console Application

**Indicators**:
```xml
<!-- .csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
  </PropertyGroup>
</Project>
```

```csharp
// Program.cs
static void Main(string[] args)
{
    // Entry point
}

// Or top-level statements (.NET 5+)
Console.WriteLine("Hello World");
```

**Load Context**: `common_issues.md`, `async_patterns.md` (if using async)

---

#### Class Library

**Indicators**:
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.1</TargetFramework>
    <!-- or -->
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
</Project>
```

**Load Context**: Depends on library purpose, generally `common_issues.md`, `async_patterns.md`

---

#### Worker Service / Background Service

**Indicators**:
```csharp
// .csproj
<Project Sdk="Microsoft.NET.Sdk.Worker">

// Worker.cs
public class Worker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // Long-running task
    }
}
```

**Load Context**: `async_patterns.md`, `di_patterns.md`, `performance_patterns.md`

---

## 4. ORM Detection

### Entity Framework Core

**Indicators**:
```xml
<!-- .csproj -->
<PackageReference Include="Microsoft.EntityFrameworkCore" />
<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Design" />
```

```csharp
// Code
public class ApplicationDbContext : DbContext
{
    public DbSet<Product> Products { get; set; }
}

// LINQ to Entities usage
await context.Products.Where(p => p.IsActive).ToListAsync();
```

**Load Context**: `ef_patterns.md`, `linq_patterns.md`, `async_patterns.md`, `di_patterns.md` (DbContext scoping)

---

### Entity Framework 6 (.NET Framework)

**Indicators**:
```xml
<PackageReference Include="EntityFramework" Version="6.x.x" />
```

```csharp
public class ApplicationDbContext : DbContext
{
    // EF6 patterns
}
```

**Load Context**: `ef_patterns.md` (note EF6 differences)

---

### Dapper (Micro-ORM)

**Indicators**:
```xml
<PackageReference Include="Dapper" />
```

```csharp
using Dapper;

var products = await connection.QueryAsync<Product>(
    "SELECT * FROM Products WHERE IsActive = @IsActive",
    new { IsActive = true }
);
```

**Load Context**: `security_patterns.md` (SQL injection risk), `async_patterns.md`, `performance_patterns.md`

---

### ADO.NET (Raw SQL)

**Indicators**:
```csharp
using System.Data.SqlClient;
// or
using Microsoft.Data.SqlClient;

using (var connection = new SqlConnection(connectionString))
{
    using (var command = new SqlCommand(sql, connection))
    {
        // Manual data access
    }
}
```

**Load Context**: `security_patterns.md` (SQL injection prevention), `common_issues.md` (IDisposable)

---

## 5. Authentication System Detection

### ASP.NET Core Identity

**Indicators**:
```xml
<PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" />
```

```csharp
// Identity DbContext
public class ApplicationDbContext : IdentityDbContext<ApplicationUser>

// Program.cs
builder.Services.AddDefaultIdentity<IdentityUser>()
    .AddEntityFrameworkStores<ApplicationDbContext>();
```

**Load Context**: `aspnet_patterns.md`, `security_patterns.md`, `ef_patterns.md`

---

### JWT Bearer Authentication

**Indicators**:
```xml
<PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" />
```

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => {
        options.TokenValidationParameters = new TokenValidationParameters { ... };
    });
```

**Load Context**: `aspnet_patterns.md`, `security_patterns.md` (token validation)

---

### OAuth / OpenID Connect

**Indicators**:
```xml
<PackageReference Include="Microsoft.AspNetCore.Authentication.OpenIdConnect" />
```

```csharp
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddOpenIdConnect(options => { ... });
```

**Load Context**: `aspnet_patterns.md`, `security_patterns.md`

---

### Azure AD / Microsoft Identity Platform

**Indicators**:
```xml
<PackageReference Include="Microsoft.Identity.Web" />
```

```csharp
builder.Services.AddMicrosoftIdentityWebAppAuthentication(configuration);
```

**Load Context**: `aspnet_patterns.md`, `security_patterns.md`

---

## 6. Testing Framework Detection

### xUnit

**Indicators**:
```xml
<PackageReference Include="xunit" />
<PackageReference Include="xunit.runner.visualstudio" />
```

```csharp
public class ProductTests
{
    [Fact]
    public void Test_Method()
    {
        // Test code
    }

    [Theory]
    [InlineData(1, 2, 3)]
    public void Test_WithData(int a, int b, int expected)
    {
        // Test code
    }
}
```

---

### NUnit

**Indicators**:
```xml
<PackageReference Include="NUnit" />
<PackageReference Include="NUnit3TestAdapter" />
```

```csharp
[TestFixture]
public class ProductTests
{
    [Test]
    public void Test_Method()
    {
        // Test code
    }

    [TestCase(1, 2, 3)]
    public void Test_WithData(int a, int b, int expected)
    {
        // Test code
    }
}
```

---

### MSTest

**Indicators**:
```xml
<PackageReference Include="MSTest.TestFramework" />
<PackageReference Include="MSTest.TestAdapter" />
```

```csharp
[TestClass]
public class ProductTests
{
    [TestMethod]
    public void Test_Method()
    {
        // Test code
    }
}
```

---

### Mocking Libraries

**Moq**:
```xml
<PackageReference Include="Moq" />
```

**NSubstitute**:
```xml
<PackageReference Include="NSubstitute" />
```

**FakeItEasy**:
```xml
<PackageReference Include="FakeItEasy" />
```

---

## 7. Package Ecosystem Detection

### Common Packages and Their Implications

| Package | Implication | Review Focus |
|---------|-------------|--------------|
| **Newtonsoft.Json** | JSON serialization | Check for deserialization security |
| **System.Text.Json** | .NET Core/5+ JSON | Check for proper serializer options |
| **Serilog** | Structured logging | Check for sensitive data in logs |
| **NLog** | Logging framework | Check for sensitive data in logs |
| **AutoMapper** | Object mapping | Check for proper configuration |
| **FluentValidation** | Validation library | Check validation rules |
| **MediatR** | CQRS / Mediator pattern | Check for proper command/query separation |
| **Polly** | Resilience / retry policies | Check for proper circuit breaker config |
| **Swashbuckle** | Swagger/OpenAPI | Check for proper API documentation |
| **IdentityServer4** | OAuth 2.0 / OpenID Connect | Check for secure configuration |
| **Hangfire** | Background job processing | Check for job persistence and failure handling |
| **SignalR** | Real-time communication | Check for connection lifetime management |
| **Refit** | REST client library | Check for error handling |
| **BenchmarkDotNet** | Performance benchmarking | Recognize performance-focused code |

---

## Detection Workflow

### Step-by-Step Process

**Step 1**: Identify .NET version from `.csproj`
```
Search for TargetFramework → Determine .NET version
```

**Step 2**: Identify C# version
```
Check <LangVersion> or infer from .NET version
```

**Step 3**: Identify framework type
```
Check Project SDK:
- Microsoft.NET.Sdk.Web → Web app
- Microsoft.NET.Sdk.BlazorWebAssembly → Blazor WASM
- Microsoft.NET.Sdk.Worker → Background service
- Microsoft.NET.Sdk → Library or console
```

**Step 4**: Identify ORM (if any)
```
Check PackageReferences for:
- EntityFrameworkCore → EF Core
- EntityFramework → EF6
- Dapper → Micro-ORM
```

**Step 5**: Identify authentication system
```
Check PackageReferences for:
- Microsoft.AspNetCore.Identity → ASP.NET Core Identity
- JwtBearer → JWT authentication
- Microsoft.Identity.Web → Azure AD
```

**Step 6**: Identify testing framework
```
Check test project PackageReferences:
- xunit → xUnit
- NUnit → NUnit
- MSTest → MSTest
```

**Step 7**: Identify key packages
```
Scan all PackageReferences for common libraries
Record logging, validation, HTTP client libraries
```

---

## Context Loading Decision Based on Detection

### Decision Tree

```
IF .NET version detected:
  IF .NET 8 or 7:
    → Load csharp_patterns.md (modern C# features)
  IF .NET 6+:
    → Load aspnet_patterns.md (Minimal APIs)
  IF .NET Framework 4.x:
    → Focus on legacy patterns, migration opportunities

IF ORM detected:
  IF Entity Framework Core or EF6:
    → Load ef_patterns.md, linq_patterns.md
  IF Dapper or ADO.NET:
    → Load security_patterns.md (SQL injection)

IF Framework type detected:
  IF ASP.NET Core Web API or MVC:
    → Load aspnet_patterns.md, security_patterns.md
  IF Blazor:
    → Load blazor_patterns.md
  IF Worker Service:
    → Load async_patterns.md, performance_patterns.md

IF Authentication system detected:
  → Load security_patterns.md, aspnet_patterns.md

ALWAYS load common_issues.md
```

---

## Example Detection Report

```markdown
# .NET Project Context Detection

**Project**: MyApp.Api

## Detected Stack

- **.NET Version**: .NET 8.0
- **C# Version**: C# 12 (inferred from .NET 8)
- **Framework Type**: ASP.NET Core Web API
- **ORM**: Entity Framework Core 8.0
- **Authentication**: JWT Bearer
- **Testing**: xUnit with Moq
- **Key Packages**:
  - Serilog (logging)
  - FluentValidation (validation)
  - Swashbuckle (Swagger)
  - Polly (resilience)

## Recommended Context Files

1. `common_issues.md` (always load)
2. `aspnet_patterns.md` (Web API)
3. `ef_patterns.md` (EF Core)
4. `async_patterns.md` (modern async patterns)
5. `security_patterns.md` (JWT, validation)
6. `di_patterns.md` (DI configuration)
7. `csharp_patterns.md` (C# 12 features)
8. `linq_patterns.md` (EF query optimization)

## Review Focus Areas

- Async/await patterns (modern .NET)
- Entity Framework N+1 queries
- JWT token validation
- API security (input validation, auth)
- Dependency injection lifetimes
- C# 12 primary constructors
```

---

## Common Detection Mistakes to Avoid

1. **Assuming .NET Core = Modern**: .NET Core 3.1 is EOL (2022-12-13), projects may still use it
2. **Mixing .NET Framework and .NET Core patterns**: Different threading models, different auth systems
3. **Ignoring SDK-style vs legacy .csproj**: SDK-style is cleaner, legacy has more XML
4. **Not checking for Nullable Reference Types**: Enabled by default in .NET 6+, but can be disabled
5. **Assuming all async code is correct**: Even modern .NET can have sync-over-async issues

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
