# .NET Code Review Memory System

This file explains the project memory system for dotnet-code-review skill. Memory provides project-specific, continuously improving knowledge that complements the universal context files.

---

## Memory vs Context

### Context Files (`context/dotnet/`)
- **Universal** patterns and best practices
- Apply to **all .NET projects**
- Examples: async patterns, EF N+1 queries, DI anti-patterns
- **Static** - rarely change
- **Always available** for reference

### Memory Files (`memory/skills/dotnet-code-review/`)
- **Project-specific** patterns and issues
- Apply to **this specific project**
- Examples: "This project uses custom BaseController", "AuthService has recurring null ref issues"
- **Dynamic** - continuously updated after each review
- **Learned** from actual code reviews

---

## Memory Structure

Each project gets its own memory directory:

```
memory/skills/dotnet-code-review/
├── index.md (this file)
├── example-project/
│   ├── project_overview.md
│   ├── common_patterns.md
│   ├── known_issues.md
│   └── review_history.md
├── my-ecommerce-app/
│   ├── project_overview.md
│   ├── common_patterns.md
│   ├── known_issues.md
│   └── review_history.md
└── another-project/
    ├── project_overview.md
    ├── common_patterns.md
    ├── known_issues.md
    └── review_history.md
```

---

## Four Required Files Per Project

### 1. `project_overview.md`

**Purpose**: High-level project information

**Contents**:
- Project name and type (ASP.NET Core Web API, Blazor Server, Console App, etc.)
- .NET version (.NET Framework 4.8, .NET 6, .NET 8, etc.)
- Major dependencies (EF Core, Identity, SignalR, Dapper, etc.)
- Architecture pattern (Clean Architecture, MVC, Minimal APIs, etc.)
- Testing framework (xUnit, NUnit, MSTest)
- Authentication/Authorization approach (JWT, Identity, Azure AD)
- Key characteristics ("heavy use of async", "legacy migration in progress", etc.)

**When to update**: 
- First review of the project
- When architecture changes
- When major dependencies added/removed

**Example snippet**:
```markdown
# Project: MyEcommerceApp

## Basic Info
- **Type**: ASP.NET Core 8 Web API
- **Framework**: .NET 8
- **Architecture**: Clean Architecture (Domain, Application, Infrastructure, WebApi)

## Key Dependencies
- Entity Framework Core 8.0
- ASP.NET Core Identity
- MediatR (CQRS pattern)
- FluentValidation
- Serilog

## Testing
- xUnit for unit tests
- Moq for mocking
- TestContainers for integration tests
```

---

### 2. `common_patterns.md`

**Purpose**: Project-specific coding patterns and conventions

**Contents**:
- Custom base classes used throughout project
- Project naming conventions
- Project-specific design patterns
- Common abstractions and interfaces
- Architectural decisions
- Project-specific extension methods

**When to update**:
- When you discover recurring patterns
- When team establishes new conventions
- When custom abstractions are created

**Example snippet**:
```markdown
# Common Patterns in MyEcommerceApp

## Base Classes

### ApiControllerBase
All controllers inherit from `ApiControllerBase`:
```csharp
public abstract class ApiControllerBase : ControllerBase
{
    protected readonly IMediator Mediator;
    protected ApiControllerBase(IMediator mediator) => Mediator = mediator;
}
```

## CQRS Pattern
- Commands in `Application/Features/{Feature}/Commands/`
- Queries in `Application/Features/{Feature}/Queries/`
- All use MediatR handlers

## Validation
- FluentValidation validators for all commands
- Registered automatically via assembly scanning
```

---

### 3. `known_issues.md`

**Purpose**: Recurring issues found in code reviews

**Contents**:
- Bugs that keep appearing
- Anti-patterns specific to this project
- Areas needing improvement
- Technical debt
- Performance bottlenecks
- Security vulnerabilities that recur

**When to update**:
- After every code review
- When same issue appears multiple times
- When new categories of problems emerge

**Example snippet**:
```markdown
# Known Issues in MyEcommerceApp

## Recurring Issues

### 1. Missing CancellationToken Propagation
**Issue**: Many async methods don't accept CancellationToken
**Frequency**: Found in 8 out of 10 reviews
**Affected Areas**: 
- `OrderService` methods
- `ProductService` methods
- Custom MediatR handlers

**Example**:
```csharp
// ❌ Missing CancellationToken
public async Task<Order> GetOrderAsync(int id)
{
    return await _dbContext.Orders.FindAsync(id);
}

// ✅ Should be
public async Task<Order> GetOrderAsync(int id, CancellationToken cancellationToken = default)
{
    return await _dbContext.Orders.FindAsync(id, cancellationToken);
}
```

### 2. DbContext Captive Dependency
**Issue**: `NotificationService` registered as Singleton but captures Scoped DbContext
**Status**: Fixed in PR #234, monitor for recurrence
**Root Cause**: Developer confusion about DI lifetimes
```

---

### 4. `review_history.md`

**Purpose**: Track review metrics and improvements over time

**Contents**:
- Review dates
- Number of issues found
- Severity breakdown
- Trends (improving/worsening)
- Notable fixes
- Review focus areas

**When to update**:
- After every code review
- Append new entry at top (reverse chronological)

**Example snippet**:
```markdown
# Review History for MyEcommerceApp

## Review #5 - 2025-01-14
**PR**: #289 - Add product recommendation feature
**Files Reviewed**: 12 (.cs files)
**Issues Found**: 8 (2 High, 4 Medium, 2 Low)

### Key Findings
- ✅ Good: Proper async/await usage improved
- ❌ Issue: Still missing CancellationToken in 3 methods
- ⚠️ Warning: New N+1 query in `ProductRecommendationService`

### Trends
- Async patterns: Improving (down from 10 issues in review #4)
- LINQ performance: New issue category emerged

---

## Review #4 - 2025-01-07
**PR**: #275 - Refactor order processing
**Files Reviewed**: 8 (.cs files)
**Issues Found**: 15 (1 Critical, 3 High, 7 Medium, 4 Low)

### Key Findings
- ❌ Critical: Sync-over-async in OrderProcessor.ProcessAsync
- ✅ Fixed: Previous captive dependency issue resolved
```

---

## Workflow

### First Review of a Project

1. **Create project directory**:
   ```
   memory/skills/dotnet-code-review/{project-name}/
   ```

2. **Create all 4 files**:
   - `project_overview.md` - Document project structure
   - `common_patterns.md` - Start documenting patterns as you discover them
   - `known_issues.md` - Leave empty initially
   - `review_history.md` - Create first entry

3. **During review**:
   - Reference memory to understand project context
   - Note new patterns in `common_patterns.md`
   - Track issues in `known_issues.md`

4. **After review**:
   - Update `known_issues.md` with recurring problems
   - Add entry to `review_history.md`
   - Update `common_patterns.md` if new patterns discovered

### Subsequent Reviews

1. **Load memory** in Step 2 (Load Memory & Context Detection):
   ```
   Read {project}/project_overview.md
   Read {project}/common_patterns.md
   Read {project}/known_issues.md
   Read {project}/review_history.md (last 3 entries)
   ```

2. **During review**:
   - Check if current code matches `common_patterns.md`
   - Look for issues listed in `known_issues.md`
   - Note if recurring issues are fixed or still present

3. **After review** (Step 5: Generate Output & Update Memory):
   - Add entry to `review_history.md`
   - Update `known_issues.md`:
     - Increment frequency for recurring issues
     - Add new issues
     - Mark resolved issues as fixed
   - Update `common_patterns.md` if patterns changed

---

## Benefits of Memory System

### 1. Continuous Learning
- Each review makes future reviews smarter
- Patterns learned once, applied forever
- Issues tracked until resolved

### 2. Project-Specific Context
- Understands project architecture
- Recognizes project conventions
- Knows project history

### 3. Trend Analysis
- Track improvement over time
- Identify persistent problem areas
- Measure code quality evolution

### 4. Efficiency
- Faster reviews (know what to look for)
- Focus on recurring issues
- Skip false positives (known patterns)

---

## Example: How Memory Improves Reviews

### Review #1 (No Memory)
```
Found 15 issues:
- 8 async/await problems
- 3 EF N+1 queries
- 2 DI lifetime issues
- 2 LINQ inefficiencies
```

### Review #3 (With Memory)
```
Loaded memory:
- Known issue: Missing CancellationToken (watch for this)
- Common pattern: Custom ApiControllerBase (don't flag as unusual)
- Project uses CQRS (expect command/query split)

Found 7 issues:
- 3 async/await problems (improving!)
- 2 EF N+1 queries (still recurring)
- 1 new issue: Captive dependency
- 1 LINQ inefficiency

Trend: Async patterns improving, N+1 queries need attention
```

---

## Memory Maintenance

### Keep Memory Updated
- Update after **every** review
- Don't let memory become stale
- Remove obsolete information

### Mark Resolved Issues
When issue is fixed:
```markdown
### 2. DbContext Captive Dependency ✅ RESOLVED
**Issue**: NotificationService registered as Singleton but captures Scoped DbContext
**Status**: ✅ Fixed in PR #234 (2025-01-10)
**Verify**: Check if pattern recurs in future reviews
```

### Archive Old History
Keep last 10 reviews in `review_history.md`, archive older entries:
```
review_history.md (last 10 reviews)
review_history_archive.md (older reviews)
```

---

## Summary

The memory system transforms dotnet-code-review from a **stateless** review tool into a **learning system** that:

1. **Remembers** project-specific patterns
2. **Tracks** recurring issues
3. **Improves** with each review
4. **Provides** project context
5. **Measures** code quality trends

This makes each review more accurate, efficient, and valuable than the last.

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
