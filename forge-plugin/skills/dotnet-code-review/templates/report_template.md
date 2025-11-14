# .NET Code Review Report

**Project**: [Project Name]
**Date**: [Review Date]
**Reviewer**: .NET Code Review Expert (Claude Code skill:dotnet-code-review)
**.NET Version**: [.NET Framework 4.8 / .NET 6 / .NET 8]
**Scope**: [Branch/Commit Range Reviewed]
**Files Changed**: [Number] files ([Number] .cs, [Number] .csproj, [Number] .cshtml/.razor, [Number] config)

---

## Executive Summary

### Overall Assessment
[Brief overall assessment of code quality - Excellent / Good / Needs Improvement / Critical Issues Found]

### Key Findings
- **Critical Issues**: [Number] 🔴
- **High Priority Issues**: [Number] 🟡
- **Medium Priority Issues**: [Number] 🔵
- **Low Priority Issues**: [Number] ⚪
- **Positive Highlights**: [Number] ✅

### Recommendation
[Overall recommendation - Approve / Approve with Changes / Request Changes / Block Merge]

### Summary
[2-3 sentence summary of the changes and their impact]

---

## Critical Issues (🔴 Must Fix Before Merge)

### [Number]. [Issue Title]

**Location**: `file_path:line_number`
**Severity**: Critical
**Category**: [Production Quality / Deep Bugs / Security / Performance / Architecture / Reliability / Scalability / Testing]

**Description**:
[Clear description of the issue]

**Impact**:
[Why this is critical - what will happen if not fixed]

**Current Code**:
```csharp
[Code snippet showing the problem]
```

**Fix**:
```csharp
[Code snippet showing the solution]
```

**Reference**:
- Context: `../../context/dotnet/[relevant_file].md`
- [External documentation link if applicable]

---

## High Priority Issues (🟡 Should Fix Soon)

### [Number]. [Issue Title]

**Location**: `file_path:line_number`
**Severity**: High
**Category**: [Category]

**Description**:
[Description]

**Impact**:
[Impact]

**Current Code**:
```csharp
[Problem code]
```

**Fix**:
```csharp
[Solution code]
```

**Reference**:
- [Documentation link]

---

## Medium Priority Issues (🔵 Should Address)

[Follow same format as high priority]

---

## Low Priority Issues (⚪ Consider Addressing)

[Follow same format]

---

## Architecture and Design

### Overall Architecture
[Assessment of architectural decisions in the changes]

**Strengths**:
- [What was done well architecturally]
- [Good design patterns used]
- [SOLID principles followed]

**Concerns**:
- [Architectural issues or anti-patterns]
- [Design improvements needed]
- [Tight coupling identified]

### Dependency Injection
- **Service Lifetimes**: [Assessment - correct usage of Transient/Scoped/Singleton]
- **Captive Dependencies**: [None found / Issues identified]
- **Constructor Injection**: [Proper usage / Service locator anti-pattern found]
- **Interface Abstraction**: [Well abstracted / Missing abstractions]

### Separation of Concerns
- **Controller Responsibility**: [Thin vs fat controllers]
- **Business Logic Location**: [In services vs leaking into controllers]
- **Repository Pattern**: [If applicable - proper usage]
- **Domain Models**: [Anemic vs rich domain models]

### Exception Handling Strategy
- **Global Error Handling**: [Middleware/filters configured]
- **Exception Propagation**: [Proper exception boundaries]
- **Logging**: [Adequate logging of errors]

---

## Async/Await Analysis

### Async Pattern Usage
- **Async All the Way**: [Assessment - full async chain vs mixed sync/async]
- **Deadlock Risks**: [None found / Issues identified]
- **ConfigureAwait Usage**: [Appropriate for library code]

### Issues Found
- **Sync-over-Async**: [Count] occurrences of `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`
- **Async Void**: [Count] occurrences (except event handlers)
- **Missing CancellationToken**: [Methods that should support cancellation]
- **Fire-and-Forget**: [Unhandled async operations]

**Async/Await Score**: [Excellent / Good / Needs Improvement / Critical Issues]

---

## Entity Framework Analysis

[Only include if EF is used in changed files]

### Query Patterns
- **N+1 Problems**: [Count] potential N+1 queries identified
- **Eager Loading**: [Proper use of `.Include()` / Missing includes]
- **Projection**: [Use of `.Select()` for efficient data retrieval]
- **AsNoTracking**: [Used for read-only queries]

### Performance
- **Query Efficiency**: [Assessment]
- **Materialization**: [Proper use of `.ToListAsync()` / Client-side evaluation issues]
- **Batch Operations**: [Single inserts vs batch operations]

### DbContext Lifetime
- **Registration**: [Properly registered as Scoped / Incorrect lifetime]
- **Thread Safety**: [DbContext not shared across threads]
- **Disposal**: [Proper using statement / disposal patterns]

### Data Integrity
- **Transactions**: [Explicit transactions for multi-operation consistency]
- **Concurrency Handling**: [Optimistic concurrency / Row versioning]
- **Migrations**: [New migrations proper / Schema changes handled]

**Entity Framework Score**: [Excellent / Good / Needs Improvement / Critical Issues]

---

## Security Analysis

### OWASP Top 10 Assessment

#### A01:2021 - Broken Access Control
- **Authorization**: [`[Authorize]` attributes present / Missing authorization]
- **Role-Based Access**: [Proper role checks / Issues]
- **Resource Authorization**: [Authorize access to specific resources]

#### A02:2021 - Cryptographic Failures
- **Secrets Management**: [Using Key Vault / Secrets in code]
- **Password Hashing**: [Proper hashing with salt / Weak hashing]
- **HTTPS Enforcement**: [HSTS configured / Missing HTTPS]
- **Sensitive Data Logging**: [No sensitive data logged / Issues found]

#### A03:2021 - Injection
- **SQL Injection**: [Parameterized queries / String concatenation in SQL]
- **Command Injection**: [Input validation present / Vulnerabilities]
- **LDAP Injection**: [If applicable]

#### A04:2021 - Insecure Design
- **Threat Modeling**: [Proper security design / Design flaws]
- **Input Validation**: [Comprehensive validation / Missing validation]
- **Business Logic**: [Secure business logic / Bypass vulnerabilities]

#### A05:2021 - Security Misconfiguration
- **Default Configurations**: [Security hardened / Default configs used]
- **Error Messages**: [No sensitive data in errors / Information disclosure]
- **Security Headers**: [HSTS, CSP, X-Frame-Options configured]

#### A06:2021 - Vulnerable and Outdated Components
- **NuGet Packages**: [No known vulnerabilities / Vulnerable packages found]
- **Package Versions**: [Up-to-date / Outdated dependencies]

#### A07:2021 - Identification and Authentication Failures
- **Authentication**: [Proper JWT/Identity usage / Issues]
- **Session Management**: [Secure session handling / Vulnerabilities]
- **Password Requirements**: [Strong requirements / Weak requirements]

#### A08:2021 - Software and Data Integrity Failures
- **Deserialization**: [Safe deserialization / Insecure deserialization]
- **CI/CD Pipeline**: [Secure pipeline / Vulnerabilities]

#### A09:2021 - Security Logging and Monitoring Failures
- **Audit Logging**: [Comprehensive logging / Missing security logs]
- **Monitoring**: [Alerting configured / No monitoring]

#### A10:2021 - Server-Side Request Forgery (SSRF)
- **URL Validation**: [Validated external URLs / SSRF vulnerability]

**Security Score**: [Excellent / Good / Needs Improvement / Critical Vulnerabilities]

---

## Performance Analysis

### Database Performance
- **Query Optimization**: [Efficient queries / Slow queries identified]
- **Connection Management**: [Connection pooling / Connection leaks]
- **Caching**: [Appropriate caching strategy / No caching]
- **Indexing Hints**: [Database indexes considered]

### String Performance
- **StringBuilder**: [Used in loops / String concatenation in loops]
- **String Comparison**: [StringComparison specified / Culture issues]
- **String Allocation**: [Efficient string handling / Excessive allocations]

### Collection Performance
- **Collection Types**: [Appropriate types (List, HashSet, Dictionary)]
- **Capacity Hints**: [Capacity specified when known / Missing capacity]
- **Enumeration**: [Single enumeration / Multiple enumeration of IEnumerable]

### Memory Efficiency
- **Boxing**: [Avoided / Boxing of value types found]
- **Large Objects**: [LOH allocations avoided / Large allocations (>85KB)]
- **Object Pooling**: [ArrayPool, ObjectPool used where appropriate]
- **Span<T>/Memory<T>**: [Modern memory APIs used]

### API Performance
- **Response Caching**: [`[ResponseCache]` used appropriately]
- **Compression**: [Response compression configured]
- **Pagination**: [Large result sets paginated]
- **Async Streaming**: [`IAsyncEnumerable<T>` for large data streams]

**Performance Score**: [Excellent / Good / Needs Improvement / Critical Issues]

---

## LINQ Patterns Analysis

[Only include if LINQ is used significantly]

### LINQ Usage
- **Deferred Execution**: [Understood / Misunderstandings found]
- **Multiple Enumeration**: [Avoided / IEnumerable enumerated multiple times]
- **Query Optimization**: [Efficient queries / Inefficient patterns]

### Common Issues
- **Client-Side Evaluation**: [Avoided / Database query executed client-side]
- **Premature Materialization**: [`.ToList()` used appropriately / Unnecessary materialization]
- **Inefficient Filtering**: [`.Where()` before `.Select()` / Poor ordering]

**LINQ Score**: [Excellent / Good / Needs Improvement]

---

## Dependency Injection Patterns

[Only include if DI is used in changed files]

### Service Lifetimes
| Service | Current Lifetime | Recommended | Issue |
|---------|-----------------|-------------|-------|
| [ServiceName] | [Transient/Scoped/Singleton] | [Recommended] | [Issue description if any] |

### Issues Identified
- **Captive Dependencies**: [None / List issues]
- **DbContext Lifetime**: [Scoped (correct) / Singleton (CRITICAL)]
- **HttpClient**: [IHttpClientFactory used / Created per request]

---

## C# Language Features

[Only include if C# 8+ features are used]

### Nullable Reference Types
- **Enabled**: [Yes / No]
- **Null Handling**: [Proper null checks / Missing null checks]
- **Null-Forgiving Operator**: [Used appropriately / Overused]

### Modern C# Features
- **Pattern Matching**: [Good use / Could be improved]
- **Records**: [Used where appropriate]
- **Init-only Properties**: [Immutability considerations]
- **Switch Expressions**: [Modern syntax used]

---

## Testing Coverage

### Unit Tests
- **Test Coverage**: [Percentage] of changed code
- **Test Quality**: [Well-structured / Needs improvement]
- **Test Naming**: [Follows convention / Inconsistent]
- **AAA Pattern**: [Arrange-Act-Assert followed]

### Test Issues
- **Missing Tests**: [Critical paths without tests]
- **Async Tests**: [Proper async test patterns]
- **Mocking**: [Proper mocking / Anti-patterns (e.g., mocking DbContext)]
- **Test Isolation**: [Tests isolated / Shared state issues]

### Integration Tests
- **Present**: [Yes / No / Needed for this feature]
- **Database Tests**: [In-memory database / Real database]

**Testing Score**: [Excellent / Good / Needs Improvement / Critical Gaps]

---

## Configuration and Deployment

### Configuration Management
- **Secrets**: [Secure (Key Vault, User Secrets) / Hardcoded]
- **Environment-Specific**: [appsettings.{Environment}.json used]
- **Connection Strings**: [Secure / Exposed]

### Deployment Readiness
- **Migrations**: [Ready for deployment / Manual steps needed]
- **Breaking Changes**: [None / List breaking changes]
- **Backwards Compatibility**: [Maintained / Breaking]

---

## Positive Highlights ✅

[List things done really well]
1. [Well-implemented async patterns]
2. [Excellent exception handling]
3. [Strong security practices]
4. [Comprehensive test coverage]
5. [Clean architecture]

---

## Recommendations

### Immediate Actions (Before Merge)
1. [Fix critical security vulnerability X]
2. [Resolve deadlock risk in Y]
3. [Add missing authorization to Z]

### Short-Term Improvements (Next Sprint)
1. [Refactor service X for better testability]
2. [Add caching to frequently-accessed endpoint]
3. [Improve error handling in module Y]

### Long-Term Considerations
1. [Consider migrating to .NET 8 for performance benefits]
2. [Evaluate implementing CQRS pattern for complex queries]
3. [Plan for horizontal scaling considerations]

---

## Context Files Referenced

This review used the following context files for guidance:
- `../../context/dotnet/common_issues.md` - Universal .NET problems
- `../../context/dotnet/async_patterns.md` - Async/await best practices
- `../../context/dotnet/ef_patterns.md` - Entity Framework patterns
- `../../context/dotnet/aspnet_patterns.md` - ASP.NET Core patterns
- `../../context/dotnet/security_patterns.md` - .NET security
- `../../context/security/security_guidelines.md` - General security

For deeper understanding of issues, refer to these files.

---

## Project Memory Updated

The following memory files were updated:
- `project_overview.md` - Updated with framework and architecture details
- `common_patterns.md` - Documented async and database patterns observed
- `known_issues.md` - Recorded technical debt to prevent future false positives
- `review_history.md` - Added summary of this review

---

## Appendix: File-by-File Summary

### [FileName.cs]
- **Lines Changed**: [Added/Modified/Deleted]
- **Issues Found**: [Count by severity]
- **Key Changes**: [Brief description]

[Repeat for each file]

---

**Review Completed**: [Timestamp]
**Next Review Recommended**: [Date or milestone]
