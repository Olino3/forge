# .NET Context Index

This directory contains shared contextual knowledge for .NET code review and development. These files provide reference materials, best practices, and standards applicable to all .NET projects.

## Purpose

**Context files** are static, shared knowledge that remains consistent across projects. They provide:
- .NET Framework and C# best practices
- Security guidelines specific to .NET
- Entity Framework patterns and optimization
- Async/await and concurrency patterns
- Common pitfalls and how to avoid them
- Reference materials for ASP.NET, Blazor, LINQ, and dependency injection

**This is NOT project-specific memory** - for project-specific patterns, see `../../memory/skills/dotnet-code-review/{project-name}/`

---

## Directory Structure

```
dotnet/
├── index.md (this file)            - Navigation and usage guide
├── context_detection.md            - .NET version and framework detection
├── common_issues.md                - Universal .NET problems
├── aspnet_patterns.md              - ASP.NET Core/MVC patterns
├── ef_patterns.md                  - Entity Framework patterns
├── blazor_patterns.md              - Blazor component patterns
├── di_patterns.md                  - Dependency injection patterns
├── async_patterns.md               - Async/await best practices
├── csharp_patterns.md              - C# language features (8+)
├── linq_patterns.md                - LINQ optimization patterns
├── performance_patterns.md         - Performance optimization
└── security_patterns.md            - .NET-specific security
```

---

## Usage Guide

### When Performing .NET Code Reviews

**Step 1: Always Read This Index First**
- Understand available context files
- Determine which files are relevant to the code being reviewed

**Step 2: Load Context Selectively**
- Do NOT load all files automatically
- Use the decision matrix below to determine which files to load
- Loading only relevant files saves tokens and improves focus

**Step 3: Reference Context in Reviews**
- Cite specific sections from context files in review findings
- Provide file paths and section anchors for traceability

---

## Context Loading Decision Matrix

Use this matrix to determine which context files to load based on the code being reviewed:

| Code Type | Always Load | Conditionally Load | Rarely Load |
|-----------|-------------|-------------------|-------------|
| **Any .NET Code** | `common_issues.md` | `context_detection.md` (first review) | - |
| **Controllers/API** | `aspnet_patterns.md` | `security_patterns.md`, `async_patterns.md` | `performance_patterns.md` |
| **DbContext/Queries** | `ef_patterns.md` | `linq_patterns.md`, `performance_patterns.md`, `async_patterns.md` | `security_patterns.md` |
| **Async Methods** | `async_patterns.md` | `common_issues.md`, `performance_patterns.md` | - |
| **Services/Repositories** | `di_patterns.md` | `async_patterns.md`, `ef_patterns.md` | `linq_patterns.md` |
| **Blazor Components** | `blazor_patterns.md` | `async_patterns.md`, `di_patterns.md` | `security_patterns.md` |
| **LINQ Queries** | `linq_patterns.md` | `ef_patterns.md`, `performance_patterns.md` | - |
| **C# 8+ Features** | `csharp_patterns.md` | `common_issues.md` | - |
| **Startup/Program.cs** | `di_patterns.md`, `aspnet_patterns.md` | `security_patterns.md` | - |
| **Performance-Critical** | `performance_patterns.md` | `async_patterns.md`, `ef_patterns.md`, `linq_patterns.md` | - |
| **Security-Sensitive** | `security_patterns.md` | `../../security/security_guidelines.md`, `aspnet_patterns.md` | - |

---

## File Descriptions and When to Load

### **context_detection.md**
**Load When**: First review of a project, or when framework/version detection is needed

**Contains**:
- .NET version detection (.NET Framework 4.x vs .NET Core vs .NET 5-8+)
- C# version identification
- Framework type detection (ASP.NET Core, Blazor, Console)
- ORM detection (EF Core, EF6, Dapper)
- Authentication system identification
- Testing framework detection

**Purpose**: Understand the project's .NET stack to guide further context loading

**Example Detection Patterns**:
- `TargetFramework` in .csproj → .NET version
- `using` statements → Framework type
- NuGet packages → Libraries and tools used

---

### **common_issues.md**
**Load When**: EVERY review (universal problems)

**Contains**:
- **Async/Await Anti-Patterns**:
  - Sync-over-async (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`)
  - Async void (except event handlers)
  - Missing ConfigureAwait in libraries
  - Fire-and-forget patterns
- **IDisposable Misuse**:
  - Missing using statements
  - Not implementing IDisposable for resources
  - Dispose not called in finally
- **LINQ Pitfalls**:
  - Deferred execution misunderstanding
  - Multiple enumeration
  - N+1 queries with EF
  - Performance issues
- **Exception Handling**:
  - Swallowing exceptions
  - Throwing System.Exception
  - Catching too broad
- **String Performance**:
  - Concatenation in loops
  - Not using StringBuilder
  - String comparison without StringComparison
- **Nullable Reference Types** (C# 8+):
  - Null-forgiving operator misuse
  - Missing null checks
- **Collection Misuse**:
  - Wrong collection type
  - Not specifying capacity
  - Boxing in collections
- **Memory Leaks**:
  - Event handler leaks
  - Static references
  - Timer not disposed

**Purpose**: Catch the most frequent .NET bugs that apply to all projects

---

### **aspnet_patterns.md**
**Load When**: Reviewing controllers, middleware, Razor views, or Web API code

**Contains**:
- **Controller Patterns**:
  - Action methods and routing
  - Model binding and validation
  - `IActionResult` return types
  - Status code usage (200, 201, 400, 404, 500)
  - `[Authorize]` attributes
- **Middleware Pipeline**:
  - Middleware order and configuration
  - Exception handling middleware
  - CORS configuration
- **Dependency Injection in ASP.NET**:
  - Service registration patterns
  - Scoped services in HTTP context
- **Configuration**:
  - appsettings.json usage
  - Environment-specific config
  - Secrets management
- **Authentication/Authorization**:
  - JWT bearer authentication
  - Cookie authentication
  - Role-based authorization
  - Policy-based authorization
- **Model Validation**:
  - DataAnnotations
  - FluentValidation
  - Custom validators
- **Web API Patterns**:
  - RESTful design
  - API versioning
  - Response caching
- **Razor Pages/MVC**:
  - View models
  - Tag helpers
  - Partial views
- **Static Files**:
  - wwwroot configuration
  - File serving

**Purpose**: Ensure proper ASP.NET Core web application patterns

---

### **ef_patterns.md**
**Load When**: Reviewing code that uses Entity Framework (Core or 6)

**Contains**:
- **DbContext Lifetime Management**:
  - Should be Scoped, never Singleton
  - Using statements for manual creation
  - Thread safety considerations
- **Query Patterns**:
  - LINQ to Entities best practices
  - `.Include()` for eager loading
  - `.ThenInclude()` for nested relationships
  - `.Select()` for projection
  - `.AsNoTracking()` for read-only queries
- **N+1 Problem Solutions**:
  - Detecting N+1 queries
  - Fixing with `.Include()`
  - Using projections
- **Raw SQL**:
  - `FromSqlRaw()` vs `FromSqlInterpolated()`
  - SQL injection prevention
  - When to use raw SQL
- **Migrations**:
  - Creating migrations
  - Applying migrations
  - Data seeding
- **Relationships**:
  - One-to-many configuration
  - Many-to-many configuration
  - Navigation properties
- **Change Tracking**:
  - Tracking vs no-tracking queries
  - Detaching entities
  - Change tracker performance
- **Transactions**:
  - Explicit transactions
  - Transaction scope
  - Rollback scenarios
- **Concurrency Handling**:
  - Optimistic concurrency
  - Row versioning
  - Conflict resolution
- **Performance Optimization**:
  - Query splitting
  - Compiled queries
  - Batch operations

**Purpose**: Prevent common Entity Framework mistakes and optimize database access

---

### **blazor_patterns.md**
**Load When**: Reviewing Blazor (Server or WebAssembly) components

**Contains**:
- **Component Lifecycle**:
  - `OnInitialized` vs `OnInitializedAsync`
  - `OnParametersSet` vs `OnParametersSetAsync`
  - `OnAfterRender` and `OnAfterRenderAsync`
  - When to use each lifecycle method
- **State Management**:
  - Component state
  - Cascading parameters
  - App state patterns
- **Event Handling**:
  - `@onclick`, `@onchange`, etc.
  - Event callbacks
  - EventCallback vs Action
- **Rendering Optimization**:
  - `StateHasChanged()` usage
  - `ShouldRender()` override
  - Avoiding unnecessary re-renders
- **JavaScript Interop**:
  - `IJSRuntime` usage
  - Invoking JS from C#
  - Invoking C# from JS
  - Module loading
- **Dependency Injection in Blazor**:
  - `@inject` directive
  - Service lifetimes for Blazor Server
  - Scoped services in Blazor WASM
- **Forms and Validation**:
  - `EditForm` component
  - `InputText`, `InputNumber`, etc.
  - `DataAnnotationsValidator`
  - Custom validation
- **Component Parameters**:
  - `[Parameter]` attribute
  - `[CascadingParameter]` attribute
  - Parameter validation
- **Component Disposal**:
  - Implementing `IDisposable`
  - Unsubscribing from events
  - Cleaning up JS interop
- **Blazor Server Specific**:
  - Circuit lifetime
  - SignalR connection management
- **Blazor WASM Specific**:
  - Client-side security considerations
  - HttpClient configuration
  - PWA features

**Purpose**: Ensure proper Blazor component implementation and avoid memory leaks

---

### **di_patterns.md**
**Load When**: Reviewing service registration, dependency injection, or service classes

**Contains**:
- **Service Lifetimes**:
  - **Transient**: Created every time requested
  - **Scoped**: Once per HTTP request (or Blazor circuit)
  - **Singleton**: Once for application lifetime
  - When to use each lifetime
- **Lifetime Rules**:
  - Longer-lived services can only depend on same or longer-lived
  - Captive dependency anti-pattern
- **Service Registration**:
  - `AddTransient`, `AddScoped`, `AddSingleton`
  - Interface-based registration
  - Multiple implementations
  - Open generic registration
- **Constructor Injection**:
  - Primary DI pattern in .NET
  - Dependency resolution
- **Service Locator Anti-Pattern**:
  - Why to avoid
  - When it's acceptable (rare cases)
- **IServiceScopeFactory**:
  - Creating scopes manually
  - Background services needing scoped dependencies
- **Common Lifetime Issues**:
  - DbContext as Singleton (NEVER)
  - Scoped service in Singleton (captive dependency)
  - HttpClient per request (use IHttpClientFactory)
- **HttpClient Best Practices**:
  - IHttpClientFactory usage
  - Named clients
  - Typed clients
  - Polly integration for resilience
- **Factory Pattern**:
  - When to use factories
  - Func<T> injection
- **Options Pattern**:
  - IOptions<T>, IOptionsSnapshot<T>, IOptionsMonitor<T>
  - Configuration binding

**Purpose**: Ensure correct service lifetime management and prevent subtle DI bugs

---

### **async_patterns.md**
**Load When**: Reviewing code with async/await (very common in modern .NET)

**Contains**:
- **Async All the Way**:
  - Full async call chain
  - Why mixing sync and async is dangerous
- **Sync-over-Async Anti-Patterns**:
  - `.Result` in ASP.NET = deadlock
  - `.Wait()` blocking
  - `.GetAwaiter().GetResult()` blocking
  - When blocking might be acceptable (console apps only)
- **Async Void**:
  - Only for event handlers
  - Why async void is dangerous elsewhere
  - Use async Task instead
- **ConfigureAwait**:
  - `ConfigureAwait(false)` in library code
  - Not needed in ASP.NET Core (no sync context)
  - When to use it
- **CancellationToken**:
  - Propagating cancellation through call chain
  - User-initiated cancellations
  - Timeout scenarios
- **ValueTask vs Task**:
  - When to use ValueTask<T>
  - Performance benefits
  - Constraints on ValueTask
- **IAsyncEnumerable<T>**:
  - Async streaming
  - `await foreach`
  - When to use for large datasets
- **Task.Run**:
  - When to use (CPU-bound work)
  - When NOT to use (I/O operations)
- **Fire-and-Forget**:
  - Why it's dangerous
  - Proper patterns for background work
- **Async Disposal**:
  - IAsyncDisposable
  - `await using` statement
- **Common Deadlock Scenarios**:
  - ASP.NET sync-over-async
  - UI thread blocking
  - Prevention strategies

**Purpose**: Prevent async/await bugs and deadlocks, ensure performant async code

---

### **csharp_patterns.md**
**Load When**: Reviewing code using modern C# features (C# 8+)

**Contains**:
- **Nullable Reference Types** (C# 8):
  - Enabling nullable context
  - `?` for nullable reference types
  - `!` null-forgiving operator (use sparingly)
  - Null validation patterns
- **Pattern Matching**:
  - Switch expressions
  - Property patterns
  - Positional patterns
  - Relational patterns (C# 9)
- **Records** (C# 9):
  - When to use records vs classes
  - Value semantics
  - With-expressions
- **Init-only Properties** (C# 9):
  - Immutability
  - Object initializers
- **Top-level Statements** (C# 9):
  - Program.cs simplification
- **Global Using Directives** (C# 10):
  - Reducing boilerplate
- **File-scoped Namespaces** (C# 10):
  - Reduced indentation
- **Required Members** (C# 11):
  - `required` keyword
  - Constructor enforcement
- **String Interpolation**:
  - `$""` syntax
  - Performance considerations
- **Span<T> and Memory<T>**:
  - Stack allocation
  - Memory efficiency
  - When to use
- **Tuples**:
  - Value tuples
  - Deconst ruction
  - Named tuples
- **Local Functions**:
  - When to use vs lambda
- **Expression-bodied Members**:
  - Concise syntax

**Purpose**: Ensure proper use of modern C# language features

---

### **linq_patterns.md**
**Load When**: Reviewing code with significant LINQ usage

**Contains**:
- **Deferred Execution**:
  - Understanding lazy evaluation
  - When queries execute
  - `.ToList()` to materialize
- **Multiple Enumeration**:
  - Detecting the anti-pattern
  - Performance impact
  - When to materialize
- **Query Optimization**:
  - Filter early (`.Where()` before `.Select()`)
  - Use `.Any()` instead of `.Count() > 0`
  - Avoid unnecessary `.ToList()`
- **Entity Framework Integration**:
  - LINQ to Entities vs LINQ to Objects
  - Client-side evaluation
  - Expression tree translation
- **Performance Patterns**:
  - Efficient filtering and projection
  - Avoiding N+1 queries
  - Index usage considerations
- **Method Syntax vs Query Syntax**:
  - When to use each
  - Combining both
- **Common Methods**:
  - `.Select()`, `.Where()`, `.OrderBy()`, `.GroupBy()`
  - `.First()` vs `.Single()` vs `.FirstOrDefault()`
  - `.Any()`, `.All()`, `.Contains()`
  - `.Skip()`, `.Take()` for pagination
- **Parallel LINQ (PLINQ)**:
  - `.AsParallel()`
  - When parallelization helps
  - Thread safety considerations

**Purpose**: Write efficient LINQ queries and avoid performance pitfalls

---

### **performance_patterns.md**
**Load When**: Performance is a concern or performance-critical code is being reviewed

**Contains**:
- **String Performance**:
  - StringBuilder for loops
  - `StringComparison` for comparisons
  - String interpolation vs concatenation
- **Collection Performance**:
  - Choosing the right collection (List, HashSet, Dictionary)
  - Capacity hints
  - Collection initialization
- **Memory Efficiency**:
  - Stack vs heap allocation
  - Span<T> and Memory<T>
  - ArrayPool<T>
  - ObjectPool<T>
- **Boxing and Unboxing**:
  - Value types in object context
  - Generic constraints to avoid boxing
- **Large Object Heap (LOH)**:
  - Objects > 85KB
  - Avoiding LOH allocations
  - LOH compaction
- **Async Performance**:
  - ValueTask<T> for hot paths
  - Avoiding state machine overhead
- **Database Performance**:
  - Connection pooling
  - Query optimization
  - Caching strategies
- **Caching**:
  - IMemoryCache
  - IDistributedCache
  - Response caching
  - Output caching (.NET 7+)
- **API Performance**:
  - Response compression
  - HTTP/2 and HTTP/3
  - Minimal APIs (.NET 6+)
- **Profiling**:
  - dotTrace, PerfView
  - BenchmarkDotNet
  - ETW tracing

**Purpose**: Identify and fix performance issues, write efficient code

---

### **security_patterns.md**
**Load When**: Reviewing security-sensitive code (auth, data access, user input)

**Contains**:
- **SQL Injection**:
  - Parameterized queries
  - ORM usage (EF Core)
  - Avoiding string concatenation in SQL
- **Cross-Site Scripting (XSS)**:
  - Razor automatic encoding
  - `@Html.Raw()` dangers
  - Content Security Policy
- **Cross-Site Request Forgery (CSRF)**:
  - `[ValidateAntiForgeryToken]`
  - Anti-forgery tokens in forms
- **Authentication**:
  - ASP.NET Core Identity
  - JWT bearer authentication
  - OAuth/OpenID Connect
- **Authorization**:
  - `[Authorize]` attribute
  - Role-based authorization
  - Claims-based authorization
  - Policy-based authorization
- **Secrets Management**:
  - User Secrets for development
  - Azure Key Vault for production
  - Environment variables
  - NEVER hardcode secrets
- **Password Security**:
  - Identity password hashing
  - BCrypt, PBKDF2, Argon2
  - Salt and iterations
- **HTTPS Enforcement**:
  - HSTS (HTTP Strict Transport Security)
  - Redirect HTTP to HTTPS
- **Input Validation**:
  - DataAnnotations
  - FluentValidation
  - Whitelist vs blacklist
- **Output Encoding**:
  - HTML encoding
  - JavaScript encoding
  - URL encoding
- **Insecure Deserialization**:
  - JSON.NET security
  - Type validation
  - Trusted sources only
- **Security Headers**:
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
  - Permissions-Policy
- **Logging Sensitive Data**:
  - Never log passwords, tokens, PII
  - Redaction techniques

**Purpose**: Prevent common security vulnerabilities in .NET applications

---

## Quick Reference: Loading Patterns by Scenario

### Scenario 1: ASP.NET Core API Review
**Load**:
1. `common_issues.md` (always)
2. `aspnet_patterns.md` (controllers, routing, auth)
3. `async_patterns.md` (API methods should be async)
4. `security_patterns.md` (if handling sensitive data)
5. `ef_patterns.md` (if database access)

### Scenario 2: Entity Framework Repository Review
**Load**:
1. `common_issues.md` (always)
2. `ef_patterns.md` (DbContext, queries)
3. `linq_patterns.md` (LINQ query optimization)
4. `async_patterns.md` (async database operations)
5. `di_patterns.md` (DbContext lifetime)

### Scenario 3: Blazor Component Review
**Load**:
1. `common_issues.md` (always)
2. `blazor_patterns.md` (lifecycle, state, JSInterop)
3. `async_patterns.md` (async lifecycle methods)
4. `di_patterns.md` (service injection)

### Scenario 4: Security Audit
**Load**:
1. `security_patterns.md` (.NET-specific security)
2. `../../security/security_guidelines.md` (general security)
3. `aspnet_patterns.md` (if web app)
4. `ef_patterns.md` (if database access)
5. `common_issues.md` (always)

### Scenario 5: Performance Optimization
**Load**:
1. `performance_patterns.md` (optimization techniques)
2. `async_patterns.md` (async efficiency)
3. `ef_patterns.md` (query optimization)
4. `linq_patterns.md` (LINQ efficiency)
5. `common_issues.md` (always)

---

## Loading Efficiency Tips

1. **Always load `common_issues.md`** - it's small and catches universal problems
2. **Use `context_detection.md` on first review** to understand the tech stack
3. **Load based on code type** - use the decision matrix above
4. **Don't load everything** - selective loading saves tokens and maintains focus
5. **Reference context files in findings** - helps users learn patterns
6. **Update this index** if new patterns emerge that should be documented

---

## When to Add New Context Files

Add a new context file when:
- A pattern applies to **multiple projects** (not project-specific)
- The pattern is **.NET/C# specific** (not general programming)
- There's **enough content** to warrant a separate file (>100 lines)
- The pattern doesn't fit in existing files

Don't add a new context file for:
- Project-specific patterns (use memory instead)
- General programming practices (use existing security/general files)
- Thin content that could fit in an existing file

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
