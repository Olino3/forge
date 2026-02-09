# .NET Code Review - Usage Examples

This document provides practical examples of how to use the `dotnet-code-review` skill in various scenarios.

---

## Example 1: ASP.NET Core Web API Review

**Scenario**: Reviewing changes to a user management API controller

**Command**:
```
skill:dotnet-code-review

Please review the changes to the UserController between commits abc123 and def456
```

**What Happens**:
1. Skill invokes `skill:get-git-diff` to identify changed files
2. Identifies `UserController.cs`, `UserService.cs`, `UserRepository.cs`
3. Loads project memory to understand application conventions
4. Detects .NET 8, ASP.NET Core, Entity Framework Core 8
5. Loads relevant context: `aspnet_patterns.md`, `ef_patterns.md`, `di_patterns.md`, `async_patterns.md`, `common_issues.md`
6. Reviews for:
   - Missing `[Authorize]` attributes for sensitive endpoints
   - SQL injection risks in raw queries
   - Async/await deadlock patterns
   - Missing model validation
   - Proper status code usage (200, 201, 400, 404, 500)
   - Exception handling and logging
   - Service lifetime issues
7. Generates report with findings organized by severity
8. Updates project memory with API patterns observed

**Expected Findings**:
- CRITICAL: Missing `[Authorize]` on DELETE endpoint
- HIGH: SQL injection risk in `FromSqlRaw()` with string concatenation
- HIGH: `Task.Result` blocking in controller action (deadlock risk)
- MEDIUM: Missing `[ValidateAntiForgeryToken]` for state-changing operations
- MEDIUM: Not using `IActionResult` return type for better status code control
- LOW: Missing XML documentation comments

---

## Example 2: Entity Framework DbContext Review

**Scenario**: Reviewing a new DbContext with complex queries

**Command**:
```
skill:dotnet-code-review

Review the ApplicationDbContext changes in feature/order-management branch
```

**What Happens**:
1. Git diff identifies `ApplicationDbContext.cs`, `Order.cs`, `OrderRepository.cs`, `OrderService.cs`
2. Loads project memory: detects EF Core 8, repository pattern in use
3. Detects DbContext, entity configurations, LINQ queries
4. Loads context: `ef_patterns.md`, `linq_patterns.md`, `async_patterns.md`, `di_patterns.md`, `common_issues.md`
5. Reviews for:
   - N+1 query problems (missing `.Include()`)
   - DbContext lifetime issues (should be scoped, not singleton)
   - Missing `.AsNoTracking()` for read-only queries
   - SQL injection in raw SQL
   - Proper async method usage
   - Transaction handling
   - Relationship configuration
   - Migration files
6. Asks about repository pattern usage if not found in memory
7. Generates inline comments for each issue found
8. Updates memory: documents entity relationship patterns

**Expected Findings**:
- CRITICAL: N+1 query - loading Orders without including OrderItems
- HIGH: DbContext registered as Singleton (should be Scoped)
- HIGH: Using `.ToList()` before `.Where()` (client-side evaluation)
- MEDIUM: Missing `.AsNoTracking()` on read-only report query
- MEDIUM: Not using async methods (`.ToList()` instead of `.ToListAsync()`)
- LOW: Could use `.Select()` projection to reduce data transfer

---

## Example 3: Async/Await Pattern Review

**Scenario**: Reviewing async refactoring of synchronous methods

**Command**:
```
skill:dotnet-code-review

Review the async refactoring in pull request #234
```

**What Happens**:
1. Git diff identifies multiple service and repository files converted to async
2. Detects widespread async/await pattern changes
3. Loads context: `async_patterns.md`, `common_issues.md`, `ef_patterns.md`, `aspnet_patterns.md`
4. Reviews for:
   - Sync-over-async anti-patterns (`.Result`, `.Wait()`, `.GetAwaiter().GetResult()`)
   - Async void methods (should be async Task except event handlers)
   - Missing `ConfigureAwait(false)` in library code
   - Incomplete async conversion (mixing sync and async)
   - Proper cancellation token propagation
   - ValueTask vs Task usage
5. Checks for deadlock scenarios in ASP.NET context
6. Generates comprehensive report with async best practices
7. Updates memory with async patterns being adopted

**Expected Findings**:
- CRITICAL: Async deadlock risk - using `.Result` in ASP.NET Core controller
- CRITICAL: Async void method in business logic (should be async Task)
- HIGH: Fire-and-forget pattern without error handling
- MEDIUM: Missing ConfigureAwait(false) in library method
- MEDIUM: Not propagating CancellationToken through call chain
- LOW: Could use ValueTask<T> for hot path with likely synchronous completion

---

## Example 4: Security Audit Review

**Scenario**: Security-focused review before production deployment

**Command**:
```
skill:dotnet-code-review

Perform a security audit on the authentication changes in release/v2.0 branch
```

**What Happens**:
1. Git diff identifies authentication, authorization, and user input handling files
2. Loads project memory and detects JWT authentication, ASP.NET Core Identity
3. Loads ALL security context: `security_patterns.md`, `security_guidelines.md`, `aspnet_patterns.md`, `common_issues.md`
4. Performs comprehensive security review:
   - **SQL Injection**: Raw SQL with user input
   - **XSS**: Unencoded output in Razor views
   - **CSRF**: Missing anti-forgery tokens
   - **Authentication bypass**: Missing [Authorize] attributes
   - **Secrets exposure**: Hardcoded connection strings, API keys
   - **Insecure deserialization**: Untrusted data deserialization
   - **Open redirect**: Unvalidated redirect URLs
   - **Weak crypto**: Outdated hashing algorithms
   - **Mass assignment**: Over-posting vulnerabilities
   - **Path traversal**: Unvalidated file paths
5. Cross-references OWASP Top 10
6. Generates detailed security report with severity levels
7. Updates known_issues.md with security technical debt

**Expected Findings**:
- CRITICAL: SQL injection - `FromSqlRaw($"SELECT * FROM Users WHERE Id = {userId}")`
- CRITICAL: Hardcoded JWT secret in appsettings.json
- CRITICAL: Missing [Authorize] on sensitive admin endpoints
- HIGH: XSS risk - using `@Html.Raw()` with user-provided content
- HIGH: Password stored without hashing
- HIGH: Missing HTTPS enforcement (no HSTS)
- MEDIUM: Missing rate limiting on login endpoint
- MEDIUM: Weak password requirements
- LOW: Missing security headers (X-Frame-Options, X-Content-Type-Options)

---

## Example 5: Performance Optimization Review

**Scenario**: Reviewing performance improvements for slow endpoints

**Command**:
```
skill:dotnet-code-review

Review performance optimizations in feature/query-optimization branch. Focus on performance issues.
```

**What Happens**:
1. Git diff identifies query optimization changes
2. Loads context: `performance_patterns.md`, `ef_patterns.md`, `linq_patterns.md`, `async_patterns.md`, `common_issues.md`
3. Reviews for:
   - Efficient LINQ queries
   - Proper database indexing hints
   - Caching strategy implementation
   - String concatenation in loops (should use StringBuilder)
   - Boxing/unboxing of value types
   - Large object allocation (>85KB = LOH)
   - Response caching with [ResponseCache]
   - Memory pooling with ArrayPool<T>
   - Span<T> and Memory<T> usage
4. Checks for async streaming with IAsyncEnumerable<T>
5. Suggests profiling areas if complex performance issues detected
6. Generates report with performance metrics and improvements
7. Updates memory with performance patterns

**Expected Findings**:
- HIGH: Sync-over-async blocking on I/O operations
- HIGH: N+1 query loading related entities in loop
- MEDIUM: String concatenation in loop (use StringBuilder)
- MEDIUM: Missing response caching on static data endpoint
- MEDIUM: Using List<T> Add() in loop without capacity hint
- LOW: Boxing of int values in logging
- LOW: Could use Span<T> for string manipulation
- RECOMMENDATION: Add IAsyncEnumerable<T> for streaming large result sets

---

## Example 6: Dependency Injection Review

**Scenario**: Reviewing service registration and lifetime management

**Command**:
```
skill:dotnet-code-review

Review the new dependency injection configuration in Startup.cs and Program.cs
```

**What Happens**:
1. Git diff identifies service registration files
2. Detects DI container configuration, service lifetimes
3. Loads context: `di_patterns.md`, `aspnet_patterns.md`, `ef_patterns.md`, `common_issues.md`
4. Reviews for:
   - Service lifetime correctness (Transient, Scoped, Singleton)
   - Captive dependency anti-pattern (longer-lived service depending on shorter-lived)
   - DbContext registered as Singleton (NEVER do this)
   - HttpClient registered per request (use IHttpClientFactory)
   - Scoped service injected into Singleton
   - Proper interface-based registration
   - Constructor injection vs service locator
5. Checks for thread safety in singleton services
6. Generates inline comments for lifetime issues
7. Updates memory with DI patterns used

**Expected Findings**:
- CRITICAL: DbContext registered as Singleton (causes stale data, thread safety issues)
- CRITICAL: Captive dependency - Scoped service injected into Singleton
- HIGH: HttpClient created per request (use IHttpClientFactory)
- HIGH: Transient service with expensive initialization (should be Singleton with proper thread safety)
- MEDIUM: Service locator pattern used instead of constructor injection
- LOW: Missing interface for service (harder to test)

---

## Example 7: Blazor Component Review

**Scenario**: Reviewing new Blazor Server components

**Command**:
```
skill:dotnet-code-review

Review the Blazor components in feature/dashboard-redesign
```

**What Happens**:
1. Git diff identifies `.razor` component files, code-behind `.cs` files
2. Detects Blazor Server, component lifecycle, state management
3. Loads context: `blazor_patterns.md`, `async_patterns.md`, `di_patterns.md`, `csharp_patterns.md`, `common_issues.md`
4. Reviews for:
   - Component lifecycle method usage (OnInitialized, OnAfterRender)
   - Proper async lifecycle methods (OnInitializedAsync)
   - StateHasChanged() usage and rendering optimization
   - Event handler memory leaks
   - JavaScript interop patterns
   - Parameter validation and cascading parameters
   - Dispose implementation for IDisposable components
   - Scoped service lifetime in components
5. Checks for client-side security (Blazor WASM)
6. Generates report with Blazor-specific findings
7. Updates memory with Blazor patterns

**Expected Findings**:
- HIGH: Missing Dispose() implementation - component subscribes to event but never unsubscribes
- HIGH: Using OnInitialized instead of OnInitializedAsync for async operations
- MEDIUM: Calling StateHasChanged() too frequently (performance impact)
- MEDIUM: JSInterop not checking for null before disposal
- MEDIUM: Missing [Parameter] validation attributes
- LOW: Could use ShouldRender() override to optimize rendering
- LOW: Component parameters not marked as [Parameter]

---

## Example 8: Legacy .NET Framework 4.8 Migration Review

**Scenario**: Reviewing partial migration from .NET Framework to .NET 6

**Command**:
```
skill:dotnet-code-review

Review the .NET 6 migration changes for the API layer
```

**What Happens**:
1. Git diff identifies ported files and configuration changes
2. Detects migration from System.Web to ASP.NET Core
3. Loads context: `aspnet_patterns.md`, `async_patterns.md`, `di_patterns.md`, `common_issues.md`
4. Reviews for:
   - HttpContext access patterns (IHttpContextAccessor vs HttpContext.Current)
   - Configuration migration (web.config to appsettings.json)
   - Built-in DI vs Autofac/Unity
   - Async/await opportunities (previously sync)
   - Middleware replacement for HttpModules
   - Kestrel-specific considerations
   - Breaking changes in .NET 6 vs Framework 4.8
5. Identifies modernization opportunities
6. Generates migration report with recommendations
7. Updates memory with migration patterns and lessons learned

**Expected Findings**:
- HIGH: Still using HttpContext.Current (not available in ASP.NET Core - use IHttpContextAccessor)
- HIGH: Session state access needs refactoring (ASP.NET Core has different session model)
- MEDIUM: Opportunity to use async/await instead of synchronous I/O
- MEDIUM: Web.config transforms not migrated to appsettings.{Environment}.json
- MEDIUM: Legacy error handling (Application_Error) needs middleware replacement
- LOW: Could replace custom membership provider with ASP.NET Core Identity
- RECOMMENDATION: Migrate remaining .NET Framework dependencies to .NET 6 equivalents

---

## Example 9: Unit Testing and Test Coverage Review

**Scenario**: Reviewing test coverage for new feature

**Command**:
```
skill:dotnet-code-review

Review the unit tests for the order processing feature
```

**What Happens**:
1. Git diff identifies test files (xUnit/NUnit/MSTest)
2. Detects testing framework, mocking library (Moq, NSubstitute)
3. Loads context: `common_issues.md`, `aspnet_patterns.md`, `ef_patterns.md`
4. Reviews for:
   - Test coverage of happy path and edge cases
   - Proper test naming (MethodName_Scenario_ExpectedResult)
   - Arrange-Act-Assert pattern
   - Mocking done correctly (don't mock what you don't own)
   - Async test methods using proper async patterns
   - Test isolation (no shared state)
   - Testing error conditions and exceptions
   - Integration vs unit test appropriateness
5. Identifies missing tests for critical paths
6. Generates report with test coverage gaps
7. Updates memory with testing patterns

**Expected Findings**:
- HIGH: Missing tests for null input validation
- HIGH: No tests for error handling paths
- MEDIUM: Tests not using async properly (test method not async)
- MEDIUM: Mocking DbContext (anti-pattern - use in-memory database)
- MEDIUM: Tests have shared state (class-level fields causing flaky tests)
- LOW: Test naming doesn't follow convention
- LOW: Missing [Theory] for parameterized tests
- RECOMMENDATION: Add integration tests for database operations

---

## Example 10: Full Feature Branch Comprehensive Review

**Scenario**: Complete review of a large feature branch before merge

**Command**:
```
skill:dotnet-code-review

Comprehensive review of feature/payment-integration branch (80+ files changed) before merging to main
```

**What Happens**:
1. Git diff identifies all changed files across multiple layers (controllers, services, repositories, models, tests, configs)
2. Loads complete project memory with full context
3. Detects: .NET 8, ASP.NET Core, EF Core, xUnit, third-party payment API integration
4. Loads ALL relevant context files based on comprehensive detection
5. Performs exhaustive review across:
   - API layer: Controllers, routing, model validation, error responses
   - Business logic: Services, domain models, business rules
   - Data access: DbContext, repositories, queries, migrations
   - Security: Payment data handling, PCI compliance, secrets
   - Performance: Async patterns, caching, query optimization
   - Testing: Unit tests, integration tests, edge cases
   - Configuration: appsettings, environment variables
   - Error handling: Exception handling, logging, retry logic
6. Checks interactions between layers
7. Validates architectural consistency
8. Generates comprehensive 20-page report with executive summary
9. Updates all 4 memory files with extensive learnings

**Expected Findings**:
- CRITICAL: Payment API key hardcoded in controller (use Azure Key Vault)
- CRITICAL: Credit card data logged in plain text (PCI violation)
- CRITICAL: Missing transaction handling in payment processing (data inconsistency risk)
- HIGH: No retry logic for payment API failures
- HIGH: Async deadlock risk in payment webhook handler
- HIGH: Missing idempotency key for payment operations (duplicate charge risk)
- HIGH: No circuit breaker for external payment API
- MEDIUM: Missing comprehensive logging for payment audit trail
- MEDIUM: Payment validation in controller instead of service layer
- MEDIUM: Integration tests missing for payment failure scenarios
- MEDIUM: No timeout configured for payment API HTTP client
- LOW: Could use FluentValidation for payment request validation
- LOW: Magic strings for payment status (use enum)
- RECOMMENDATION: Add health check endpoint for payment API connectivity
- RECOMMENDATION: Implement webhook signature verification for security
- RECOMMENDATION: Add payment reconciliation background job

---

## Common Usage Patterns

### Pattern 1: Quick PR Review
```
skill:dotnet-code-review

Quick review of PR #456 - focus on critical issues only
```

### Pattern 2: Security-Focused Review
```
skill:dotnet-code-review

Security audit of authentication changes. Check for OWASP Top 10 vulnerabilities.
```

### Pattern 3: Performance-Focused Review
```
skill:dotnet-code-review

Performance review of API endpoints. Focus on database queries and async patterns.
```

### Pattern 4: Specific File Review
```
skill:dotnet-code-review

Review only the UserService.cs changes between main and feature/user-updates
```

### Pattern 5: Architecture Review
```
skill:dotnet-code-review

Architectural review of new microservice. Check SOLID principles and separation of concerns.
```

---

## Output Format Examples

### Report Format (Comprehensive)
- Saved to `/claudedocs/{project-name}/dotnet-review-2025-01-14.md`
- Executive summary with key metrics
- Findings organized by category (Security, Performance, etc.)
- Severity breakdown (Critical: 3, High: 7, Medium: 12, Low: 5)
- Detailed recommendations with code examples
- Reference to context files for deeper learning

### Inline Comment Format (PR-Ready)
- Saved to `/claudedocs/{project-name}/dotnet-review-inline-2025-01-14.md`
- File-by-file, line-by-line comments
- Each comment includes: severity, issue description, fix suggestion, context reference
- Ready to paste into GitHub/Azure DevOps PR

---

## Tips for Effective Reviews

1. **Be Specific About Scope**: Clearly define which commits/branches to compare
2. **State Your Priorities**: Mention if you want focus on security, performance, or architecture
3. **Provide Context**: Share information about deployment environment, scale, criticality
4. **Use Memory**: Subsequent reviews of the same project will be faster and more accurate
5. **Review Regularly**: Smaller, frequent reviews are better than large, infrequent ones
6. **Act on Findings**: Update code based on critical and high-severity findings
7. **Update Memory**: If the skill identifies false positives, correct them in known_issues.md

---

**These examples demonstrate the comprehensive capabilities of the `dotnet-code-review` skill across various .NET scenarios.**
