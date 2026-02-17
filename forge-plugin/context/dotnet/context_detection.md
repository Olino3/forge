---
id: "dotnet/context_detection"
domain: dotnet
title: ".NET Context Detection"
type: detection
estimatedTokens: 700
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: ".NET Version Detection"
    estimatedTokens: 67
    keywords: [net, version, detection]
  - name: "C# Version Detection"
    estimatedTokens: 61
    keywords: [version, detection]
  - name: "Framework Type Detection"
    estimatedTokens: 50
    keywords: [framework, type, detection]
  - name: "ORM Detection"
    estimatedTokens: 36
    keywords: [orm, detection]
  - name: "Authentication System Detection"
    estimatedTokens: 29
    keywords: [authentication, system, detection]
  - name: "Testing Framework Detection"
    estimatedTokens: 22
    keywords: [testing, framework, detection]
  - name: "Common Package Ecosystem"
    estimatedTokens: 43
    keywords: [package, ecosystem]
  - name: "Detection Checklist"
    estimatedTokens: 36
    keywords: [detection, checklist]
  - name: "Official Resources"
    estimatedTokens: 21
    keywords: [official, resources]

tags: [dotnet, detection, version, framework, orm, authentication, testing]
---
# .NET Context Detection

Quick reference for identifying .NET project characteristics. For detailed version info, see [.NET documentation](https://learn.microsoft.com/en-us/dotnet/).

---

## .NET Version Detection

| TargetFramework in .csproj | Version | Characteristics |
|----------------------------|---------|-----------------|
| `<TargetFramework>net8.0</TargetFramework>` | .NET 8 (LTS) | C# 12, primary constructors, Blazor improvements |
| `<TargetFramework>net7.0</TargetFramework>` | .NET 7 | C# 11, rate limiting, output caching |
| `<TargetFramework>net6.0</TargetFramework>` | .NET 6 (LTS) | C# 10, minimal APIs, global usings |
| `<TargetFramework>net5.0</TargetFramework>` | .NET 5 | C# 9, unified platform, records |
| `<TargetFramework>netcoreapp3.1</TargetFramework>` | .NET Core 3.1 (LTS) | C# 8, nullable reference types |
| `<TargetFrameworkVersion>v4.8</TargetFrameworkVersion>` | .NET Framework 4.8 | Legacy, Windows-only |

[.NET versions](https://learn.microsoft.com/en-us/dotnet/core/versions/)

---

## C# Version Detection

| .NET Version | Default C# Version | Key Features |
|--------------|-------------------|--------------|
| .NET 8 | C# 12 | Primary constructors, collection expressions |
| .NET 7 | C# 11 | Required members, raw string literals |
| .NET 6 | C# 10 | Global usings, file-scoped namespaces, record structs |
| .NET 5 | C# 9 | Records, top-level statements, init properties |
| .NET Core 3.1 | C# 8 | Nullable reference types, async streams |

[C# language versioning](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version)

---

## Framework Type Detection

| File/Folder | Framework Type |
|-------------|----------------|
| `Controllers/`, `[ApiController]` | ASP.NET Core Web API |
| `.razor`, `@page` | Blazor Server or WebAssembly |
| `Program.cs` with `builder.Build().Run()` | ASP.NET Core (6+) |
| `Startup.cs` | ASP.NET Core (< 6) |
| `views/`, `.cshtml` | ASP.NET Core MVC/Razor Pages |
| `Main()` method only | Console application |
| `appsettings.json` | ASP.NET Core configuration |

---

## ORM Detection

| NuGet Package / Using Statement | ORM |
|---------------------------------|-----|
| `Microsoft.EntityFrameworkCore` | EF Core |
| `System.Data.Entity` | Entity Framework 6 |
| `Dapper` | Dapper (micro-ORM) |
| `NHibernate` | NHibernate |

```xml
<!-- .csproj detection -->
<PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
<PackageReference Include="Dapper" Version="2.1.0" />
```

---

## Authentication System Detection

| Using Statement / Package | Authentication Type |
|----------------------------|---------------------|
| `Microsoft.AspNetCore.Identity` | ASP.NET Core Identity |
| `JwtBearerDefaults.AuthenticationScheme` | JWT Bearer |
| `AddOpenIdConnect` | OpenID Connect / OAuth |
| `[Authorize]` attribute | Authorization enabled |

---

## Testing Framework Detection

| NuGet Package | Test Framework |
|---------------|----------------|
| `Microsoft.NET.Test.Sdk` + `xunit` | xUnit |
| `Microsoft.NET.Test.Sdk` + `NUnit` | NUnit |
| `Microsoft.NET.Test.Sdk` + `MSTest.TestFramework` | MSTest |

---

## Common Package Ecosystem

| Package | Purpose |
|---------|---------|
| `Newtonsoft.Json` | JSON serialization (legacy) |
| `System.Text.Json` | JSON serialization (modern) |
| `Serilog` or `NLog` | Logging |
| `AutoMapper` | Object mapping |
| `FluentValidation` | Validation |
| `MediatR` | CQRS/Mediator pattern |
| `Polly` | Resilience (retry, circuit breaker) |
| `Swashbuckle.AspNetCore` | Swagger/OpenAPI |

---

## Detection Checklist

1. ✅ Read `.csproj` for `<TargetFramework>`
2. ✅ Check for framework-specific files (`.razor`, `Controllers/`)
3. ✅ Identify ORM from `PackageReference` or `using` statements
4. ✅ Detect authentication from Identity packages
5. ✅ Note testing framework for review context
6. ✅ Review `Program.cs` for minimal API patterns (.NET 6+)

---

## Official Resources

- **.NET Versions**: https://learn.microsoft.com/en-us/dotnet/core/versions/
- **C# Language Versions**: https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/
- **ASP.NET Core**: https://learn.microsoft.com/en-us/aspnet/core/
- **Project SDKs**: https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview

---

**Version**: 0.3.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: dotnet-code-review skill
