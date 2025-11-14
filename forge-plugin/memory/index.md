# Memory Directory Index

This directory contains **project-specific learned patterns** that improve over time as skills analyze code. Memory is dynamic, grows with each invocation, and provides context unique to each project.

## Purpose

Memory files enable:
- **Project Understanding**: Learn architecture, conventions, and patterns
- **Continuous Improvement**: Remember past findings and avoid false positives
- **Contextual Intelligence**: Apply project-specific knowledge, not just general rules
- **Efficiency**: Skip re-learning project details on each invocation

## Core Concept: Memory vs Context

| Aspect | Memory (This Directory) | Context (`../context/`) |
|--------|-------------------------|-------------------------|
| **Scope** | Project-specific | Universal, all projects |
| **Nature** | Dynamic, evolving | Static, reference |
| **Updates** | Every skill invocation | Rare (standards change) |
| **Content** | "This project uses X pattern" | "X pattern best practices" |
| **Growth** | Grows with each analysis | Stable size |
| **Location** | `memory/skills/{skill}/{project}/` | `context/{domain}/` |

**Example**:
- **Context** says: "FastAPI best practice: use dependency injection for auth"
- **Memory** says: "This project uses custom JWT middleware in `app/auth/middleware.py`, expires tokens after 15min, and stores user roles in Redis"

## Directory Structure

```
memory/
├── index.md (this file)
└── skills/                          # Organized by skill
    ├── angular-code-review/        # Angular code review memory
    │   └── {project-name}/         # Per-project directory (auto-created)
    │       ├── project_overview.md # Angular version, architecture, stack
    │       ├── common_patterns.md  # Project-specific patterns
    │       ├── known_issues.md     # Acknowledged tech debt
    │       └── review_history.md   # Past review summaries
    ├── get-git-diff/               # Git diff analysis memory
    │   └── {project-name}/         # Per-project directory (auto-created)
    │       ├── common_patterns.md  # Frequently changed files/patterns
    │       ├── commit_conventions.md # Project's commit message style
    │       └── merge_patterns.md   # Common merge/branch strategies
    └── python-code-review/         # Python code review memory
        └── {project-name}/         # Per-project directory (auto-created)
            ├── project_overview.md # Architecture, stack, conventions
            ├── common_patterns.md  # Project-specific code patterns
            ├── known_issues.md     # Acknowledged tech debt
            └── review_history.md   # Past review summaries
```

## Memory Lifecycle

### 1. First Invocation (New Project)

```markdown
# Skill encounters new project for first time

1. Check memory directory: memory/skills/{skill-name}/{project-name}/
   → Directory doesn't exist yet

2. Perform analysis using only context files
   → Load general best practices from context/

3. During analysis, learn about project:
   → Framework: FastAPI
   → Database: PostgreSQL
   → Patterns: Async everywhere, Redis caching
   → Conventions: Specific naming, structure

4. Create memory directory and initial files:
   → memory/skills/python-code-review/my-api-project/
   → Write project_overview.md with learned details
   → Write common_patterns.md with observed patterns
```

### 2. Subsequent Invocations (Existing Project)

```markdown
# Skill encounters known project

1. Check memory directory: memory/skills/{skill-name}/{project-name}/
   → Directory exists! Load existing memory

2. Load project-specific knowledge:
   → Read project_overview.md
   → Read known_issues.md (avoid false positives)
   → Read common_patterns.md (recognize patterns)

3. Perform analysis with enhanced context:
   → Apply general rules (from context/)
   → Apply project-specific understanding (from memory/)
   → Compare against known patterns

4. Update memory with new insights:
   → Add newly discovered patterns
   → Update known issues if resolved
   → Append to review history
```

### 3. Memory Growth Over Time

Each invocation makes the skill smarter about the project:

**Invocation 1**: "This looks like a FastAPI project"
**Invocation 2**: "FastAPI project with async SQLAlchemy and Redis caching"
**Invocation 3**: "FastAPI e-commerce API with specific rate limiting and cart patterns"
**Invocation 5**: "E-commerce API with documented race condition in inventory (don't flag), custom auth middleware, strict PII handling requirements"

---

## Memory Files by Skill

### dotnet-code-review Memory

Located in: `memory/skills/dotnet-code-review/{project-name}/`

**Purpose**: Remember .NET project architecture, patterns, conventions, and known issues across reviews.

#### Required Memory Files:

**`project_overview.md`** (ALWAYS CREATE FIRST):
- .NET version (.NET Framework 4.8, .NET Core 3.1, .NET 6/7/8)
- C# language version and enabled features (nullable reference types, file-scoped namespaces, etc.)
- Project type (ASP.NET Core Web API, Blazor Server/WASM, MVC, Razor Pages, Console, Class Library)
- Framework components in use (MVC, Minimal APIs, gRPC)
- ORM (Entity Framework Core, EF6, Dapper, NHibernate)
- State management approach (if Blazor: component state, services, Fluxor)
- Authentication/Authorization (ASP.NET Core Identity, JWT, Azure AD, IdentityServer, Duende)
- UI library (if applicable: MudBlazor, Radzen, Blazorise, Syncfusion)
- Testing framework (xUnit, NUnit, MSTest) and approaches
- Architecture pattern (Clean Architecture, N-tier, CQRS + MediatR, Vertical Slice)
- Dependency injection patterns and service registration approach
- Performance requirements and optimization strategies
- Security requirements and compliance needs

**Example snippet**:
```markdown
# Project Overview - EcommerceAPI

## Basic Information
- **Project Type**: ASP.NET Core 8 Web API
- **.NET Version**: .NET 8.0
- **C# Version**: C# 12 (primary constructors, collection expressions enabled)

## Architecture
- **Pattern**: Clean Architecture with CQRS (MediatR)
- **Layers**: API → Application (Commands/Queries) → Domain → Infrastructure

## Technology Stack
- **ORM**: Entity Framework Core 8.0
- **Auth**: ASP.NET Core Identity + JWT (15min expiration)
- **Validation**: FluentValidation
- **Mapping**: AutoMapper
- **Caching**: IMemoryCache + Redis (distributed)
```

**`common_patterns.md`** (UPDATE REGULARLY):
- Base controller/service classes used across project
- Result/Option pattern implementation (if used instead of exceptions)
- CQRS command/query structure (if applicable)
- Repository pattern implementation
- Validation approach (FluentValidation, DataAnnotations, custom validators)
- Error handling patterns (global exception handler, Result<T>, ProblemDetails)
- Async patterns (ConfigureAwait usage, CancellationToken propagation standards)
- Dependency injection registration patterns
- Naming conventions for controllers, services, DTOs
- File organization and folder structure conventions
- Database access patterns (repositories, direct DbContext, query objects)
- Domain event handling (if applicable)

**Example snippet**:
```markdown
# Common Patterns - EcommerceAPI

## Base Classes

### ApiControllerBase
All controllers inherit from `ApiControllerBase`:
- Injects `IMediator` and `ILogger<T>`
- Returns `Result<T>` wrapped in `IActionResult`
- DO NOT inject `IMediator` directly in controllers

## CQRS Pattern

### Command Structure
```csharp
// Primary constructors preferred (C# 12)
public record CreateProductCommand(string Name, decimal Price) : IRequest<Result<Guid>>;

public class CreateProductValidator : AbstractValidator<CreateProductCommand> { }

public class CreateProductHandler(ApplicationDbContext context) 
    : IRequestHandler<CreateProductCommand, Result<Guid>>
{
    public async Task<Result<Guid>> Handle(CreateProductCommand request, 
        CancellationToken cancellationToken)
    {
        // CancellationToken ALWAYS required
    }
}
```
```

**`known_issues.md`** (CRITICAL FOR ACCURACY):
- Acknowledged technical debt with context
- Documented N+1 queries with fix timeline
- Acceptable deviations (e.g., "Singleton DbContext for read-only cache - documented limitation")
- Pending .NET version upgrade issues
- Third-party library limitations (e.g., EF Core query translation issues)
- Performance bottlenecks under investigation
- **Purpose**: Prevent false positives on known issues

**Example snippet**:
```markdown
# Known Issues - EcommerceAPI

## 🟠 High Severity

### Missing CancellationToken (Persistent)
**Frequency**: Found in 8 of last 10 reviews (80%)
**Severity**: High
**Affected Areas**:
- `Application/Products/Queries/` - 5 query handlers
- `Application/Orders/Commands/` - 3 command handlers

**Status**: ⚠️ Ongoing - pattern being gradually addressed
**Root Cause**: Team learned CancellationToken pattern mid-project
**Action Items**:
1. Add to code review checklist
2. Update all new handlers (in progress)
3. Backfill existing handlers (scheduled Q2 2025)

### N+1 Query in Order History
**Frequency**: Reoccurred 3 times after fixes
**Severity**: High
**Location**: `Controllers/OrdersController.cs:GetOrderHistory()`
**Status**: 🔄 In Progress - optimization planned Q2 2025
**Impact**: <1% of users (those with 100+ orders)
**Workaround**: Pagination limits to 20 orders per page
**Review Guidance**: Can suggest `.Include()`, but note it's known low-priority issue

## 🟡 Medium Severity

### Direct DbContext Usage (Migration In Progress)
**Frequency**: Found in 6 of last 10 reviews
**Status**: 🔄 Migrating to repository pattern (40% complete)
**Review Guidance**: Flag NEW direct usage; existing usage being refactored
```

**`review_history.md`** (APPEND AFTER EACH REVIEW):
- Date and scope of each review
- Key findings summary
- Trends over time (async patterns improving, N+1 queries recurring)
- Improvements made (migration to .NET 8, adoption of primary constructors)
- Recurring issues with frequency tracking
- Metrics: issues by severity, test coverage changes, code quality trends

**Example snippet**:
```markdown
# Review History - EcommerceAPI

## Review #10 - 2025-01-14
**PR**: #289 - Add product recommendation feature
**Reviewer**: dotnet-code-review v1.0.0
**Files Changed**: 12 (+487 lines, -12 lines)
**Issues Found**: 8 total (0 🔴 Critical, 2 🟠 High, 4 🟡 Medium, 2 🟢 Low)

### Detailed Findings
1. 🟠 **Missing CancellationToken** - `GetRecommendationsHandler.cs:23`
2. 🟠 **N+1 Query** - Loading product reviews in loop
3. 🟡 **Missing null check** - `request.UserId` not validated

### Trends vs Previous Review
| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Total Issues | 12 | 8 | ✅ -33% |
| High Severity | 3 | 2 | ✅ -33% |
| CancellationToken Issues | 4 | 1 | ✅ -75% |

---

## Summary Statistics (Last 10 Reviews)
- **Total Issues Found**: 105 issues across 10 reviews (10.5 avg per review)
- **Recurring Patterns**:
  - Missing CancellationToken: 80% of reviews
  - N+1 Queries: 30% of reviews (3 recurrences)
  - Null checks: 50% of reviews

### Code Quality Trend
**Improvement**: 60% reduction in issues from Review #1 to Review #10
- Review #1: 20 issues
- Review #10: 8 issues

### Test Coverage Trend
- Review #1: 65%
- Review #10: 85%
```

#### .NET-Specific Memory Guidance

**Why .NET projects need memory**:
- **Captive dependency detection**: Some Singleton→Scoped patterns are intentional (e.g., cache)
- **N+1 query tracking**: EF Core makes these easy to introduce and hard to spot
- **Async pattern evolution**: Teams often learn `CancellationToken`/`ConfigureAwait` mid-project
- **Framework migration**: .NET Framework → .NET Core migrations have documented limitations
- **Third-party quirks**: EF Core, Blazor libraries have known translation/rendering issues

**What to track in .NET memory**:
- Which service lifetimes are intentional vs accidental
- Known EF Core query limitations (e.g., "GroupBy doesn't translate in this scenario")
- Documented sync-over-async code (e.g., "Migration code uses `.Result` - runs once on startup")
- Blazor component lifecycle patterns specific to this project
- Security exceptions (e.g., "Admin endpoints skip CSRF - documented in security review")

---

### get-git-diff Memory

Located in: `memory/skills/get-git-diff/{project-name}/`

**Purpose**: Remember project-specific commit and change patterns

#### Suggested Memory Files:

**`common_patterns.md`**:
- Frequently modified files (hotspots)
- Typical file groupings in commits
- Common change sizes and patterns
- Areas of active development

**`commit_conventions.md`**:
- Commit message format (Conventional Commits, custom, etc.)
- Typical commit scopes/categories
- PR/issue reference format
- Branch naming patterns

**`merge_patterns.md`**:
- Merge strategy (merge commits, squash, rebase)
- Typical merge conflict areas
- Release branch patterns
- Feature branch conventions

**Example content**:
```markdown
# Common Patterns - MyApp

## Hotspot Files (Updated in 80%+ of commits)
- `src/api/routes.py` - API endpoint definitions
- `tests/test_api.py` - Corresponding tests
- `README.md` - Documentation updates

## Typical Change Groups
Backend changes usually include:
- Route file + handler + schema + test
- All modified together in single commit

## Commit Size Patterns
- Small: 1-3 files, <100 lines (80% of commits)
- Medium: 4-10 files, 100-500 lines (15%)
- Large: 10+ files, 500+ lines (5%, usually refactoring)
```

---

### angular-code-review Memory

Located in: `memory/skills/angular-code-review/{project-name}/`

**Purpose**: Remember Angular project architecture, patterns, conventions, and known issues

#### Required Memory Files:

**`project_overview.md`** (ALWAYS CREATE FIRST):
- Angular version (e.g., Angular 17)
- Module system (standalone components vs NgModules)
- State management (NgRx, Akita, service-based)
- UI library (PrimeNG, Angular Material, etc.)
- CSS framework (TailwindCSS, Bootstrap, SCSS)
- TypeScript configuration (strict mode, target)
- RxJS version and patterns
- Testing framework (Jasmine/Karma, Jest)
- Build system (Angular CLI, Nx)
- Forms approach (reactive, template-driven)
- Routing strategy (lazy loading, preloading)

**`common_patterns.md`** (UPDATE REGULARLY):
- Component patterns (smart vs presentational)
- Service organization
- State management patterns
- Subscription management approach
- Change detection strategies used
- Error handling patterns
- Form validation patterns
- Naming conventions
- File organization

**`known_issues.md`** (CRITICAL FOR ACCURACY):
- Acknowledged technical debt
- Documented limitations
- Pending Angular/RxJS issues
- Acceptable deviations from best practices
- Third-party library issues (PrimeNG, etc.)
- **Purpose**: Prevent false positives on known issues

**`review_history.md`** (APPEND AFTER EACH REVIEW):
- Date and scope of review
- Key findings summary
- Trends over time (subscription leaks, OnPush adoption, etc.)
- Improvements made
- Recurring issues

**Example `known_issues.md`**:
```markdown
# Known Issues - MyAngularApp

## Manual Change Detection in Dashboard (Documented)
**Location**: `src/app/dashboard/dashboard.component.ts:89`
**Status**: Intentional - required for PrimeNG Chart with dynamic data
**Behavior**: Uses `ChangeDetectorRef.detectChanges()` in ngAfterViewInit
**Reason**: PrimeNG Chart doesn't trigger change detection with OnPush
**Review Guidance**: DO NOT flag as issue - this is correct pattern for this library

## Subscription in ngAfterViewInit (Intentional)
**Location**: `src/app/features/products/product-detail.component.ts:55`
**Status**: Correct lifecycle for this use case
**Reason**: Requires @ViewChild(ImageGallery) to be initialized first
**Review Guidance**: This is intentional and proper - do not suggest moving to ngOnInit
```

---

### python-code-review Memory

Located in: `memory/skills/python-code-review/{project-name}/`

**Purpose**: Remember project architecture, patterns, conventions, and known issues

#### Required Memory Files:

**`project_overview.md`** (ALWAYS CREATE FIRST):
- Project type and purpose
- Framework and key dependencies
- Architecture and design patterns
- Database, cache, queue technologies
- Authentication/authorization approach
- Deployment environment
- Performance requirements

**`common_patterns.md`** (UPDATE REGULARLY):
- Project-specific code patterns
- Naming conventions
- Module organization
- Dependency injection patterns
- Testing patterns
- Configuration management

**`known_issues.md`** (CRITICAL FOR ACCURACY):
- Acknowledged technical debt
- Documented limitations
- Pending fixes (with timeline)
- Acceptable deviations from best practices
- **Purpose**: Prevent false positives on known issues

**`review_history.md`** (APPEND AFTER EACH REVIEW):
- Date and scope of review
- Key findings summary
- Trends over time
- Improvements made
- Recurring issues

**Example `known_issues.md`**:
```markdown
# Known Issues - MyApp

## Inventory Race Condition (Documented)
**Location**: `app/services/inventory.py:87-102`
**Status**: Acknowledged, fix planned for Q2 2025
**Behavior**: Concurrent purchases may oversell by 1-2 units
**Workaround**: Manual reconciliation every 5 minutes
**Review Guidance**: DO NOT flag as new issue

## N+1 Query in Order History
**Location**: `app/api/v1/orders.py:get_order_history()`
**Status**: Low priority (affects <1% of users)
**Impact**: Slight delay for users with 100+ orders
**Review Guidance**: Suggest optimization if code touches order queries
```

---

## Working with Memory

### For Skills (Conceptual Workflow)

**STEP 1: Check Memory First**

At the start of skill execution:

1. Determine the project name (from git repo name, current directory, or repo root)
2. Construct memory path: `../../memory/skills/{skill_name}/{project_name}/`
3. Check if the memory directory exists:
   - **If exists**: Read existing memory files (`project_overview.md`, `common_patterns.md`, `known_issues.md`)
   - **If not exists**: Note this is the first analysis of this project

**STEP 2: Use Memory During Analysis**

While analyzing code:

1. **Check against known issues**: Before flagging a problem, verify it's not in `known_issues.md`
   - If it's documented tech debt: Skip flagging it
   - If it's marked as "acceptable": Don't suggest changes
   
2. **Recognize project patterns**: Compare code against `common_patterns.md`
   - If pattern matches project conventions: Accept it as intentional
   - If pattern differs from context guidelines but matches memory: Follow project convention

3. **Apply project context**: Use `project_overview.md` to understand:
   - Framework-specific expectations
   - Performance requirements
   - Security requirements
   - Team conventions

**STEP 3: Update Memory After Analysis**

At the end of skill execution:

**For first-time project analysis**:
1. Create memory directory: `../../memory/skills/{skill_name}/{project_name}/`
2. Create initial memory files based on what was learned:
   - `project_overview.md` - Architecture, framework, conventions discovered
   - `common_patterns.md` - Code patterns observed during analysis
   - `known_issues.md` - Initially empty or with any documented issues found
   - `review_history.md` (for code review) - Summary of this first review

**For subsequent analyses**:
1. Update existing memory files:
   - Append new patterns to `common_patterns.md`
   - Update `known_issues.md` if issues resolved or new ones documented
   - Append review summary to `review_history.md`
2. Refine understanding based on new code analyzed

---

### For Developers (Manual)

**Creating Memory Manually** (rarely needed):

If you want to seed memory before first skill invocation:

1. Create project directory: `memory/skills/{skill-name}/{project-name}/`
2. Add `project_overview.md` with key project details
3. Add `known_issues.md` with documented tech debt
4. Let skills update other files automatically

**Reviewing Memory**:

Periodically check memory files to:
- Verify accuracy of learned patterns
- Remove outdated information
- Consolidate similar patterns
- Update resolved issues

**Resetting Memory**:

If memory becomes stale or inaccurate:
```bash
# Delete project memory to start fresh
rm -rf memory/skills/python-code-review/old-project/

# Skill will rebuild from scratch on next invocation
```

---

## Memory Best Practices

### ✅ DO

- **Load memory first** before context in every skill invocation
- **Update memory after** every analysis with new insights
- **Document known issues** to prevent false positive flags
- **Record project conventions** even if they differ from best practices
- **Keep memory factual** - what the project actually does, not what it should do
- **Use specific locations** - file paths, line numbers, function names
- **Date entries** so memory can age out gracefully
- **Cross-reference** architecture docs if they exist in repo

### ❌ DON'T

- **Don't copy general knowledge** - that belongs in context/
- **Don't store code snippets** - store patterns and locations
- **Don't make memory too large** - keep it scannable (<500 lines per file)
- **Don't store transient info** - focus on stable patterns
- **Don't duplicate context** - memory supplements context, doesn't replace it
- **Don't hardcode assumptions** - verify patterns before recording

---

## Example: Memory Evolution

### Week 1 - Initial Analysis

`project_overview.md`:
```markdown
# Project Overview - API Project

**Framework**: FastAPI
**Database**: PostgreSQL
**Python Version**: 3.11+

Basic REST API with standard CRUD operations.
```

### Week 4 - Enhanced Understanding

`project_overview.md`:
```markdown
# Project Overview - E-Commerce API

**Framework**: FastAPI + SQLAlchemy (async)
**Database**: PostgreSQL 15 with read replicas
**Cache**: Redis Cluster for session/cart
**Queue**: Celery with RabbitMQ
**Python Version**: 3.11+

High-traffic e-commerce API (10M+ req/day) with:
- Microservices architecture
- JWT authentication with 15min expiry
- Cache-aside pattern for all product reads
- Custom rate limiting (100 req/min per endpoint)
```

### Week 8 - Deep Knowledge

`project_overview.md` + detailed `common_patterns.md` + `known_issues.md`:
- Complete architecture documentation
- All coding conventions mapped
- Known race conditions documented
- Performance budgets defined
- Security requirements explicit
- False positive patterns identified

**Result**: Skill provides highly accurate, context-aware reviews with minimal false positives.

---

## Troubleshooting

### Memory Not Loading

**Check**:
1. Project name detection (case-sensitive)
2. Path construction (relative to skill location)
3. File existence and permissions

### Memory Growing Too Large

**Solutions**:
- Archive old review history (keep last 10 reviews)
- Consolidate similar patterns
- Remove resolved known issues
- Split into multiple focused files

### Conflicting Patterns

**Resolution**:
1. Check recency - newer patterns override older
2. Verify pattern still exists in current codebase
3. Update or remove outdated patterns
4. Date all entries for age-based prioritization

### Memory Inconsistencies

**Prevention**:
- Always load memory before analysis
- Always update memory after analysis
- Use structured format (headers, lists, dates)
- Include "Last Updated" timestamps

---

## Integration with Context

Memory and context work together to provide complete understanding:

**Complete skill workflow:**

1. **Load project memory** (if exists)
   - Path: `memory/skills/python-code-review/myapp/`
   - Files: `project_overview.md`, `common_patterns.md`, `known_issues.md`

2. **Load relevant context**
   - General rules: `context/python/fastapi_patterns.md`
   - Security guidelines: `context/security/security_guidelines.md`

3. **Apply layered knowledge**:
   - **Context says**: "FastAPI should use dependency injection"
   - **Memory says**: "This project uses custom middleware instead (app/auth/middleware.py)"
   - **Result**: Don't flag middleware pattern as wrong, it's intentional for this project

4. **Update memory with new learnings**:
   - Discovered new pattern: background job conventions
   - Add to `common_patterns.md` for future reference

**Memory enhances context**, providing the project-specific layer that makes general rules actionable.

---

## Related Documentation

- **Context System**: See `../context/index.md` for shared knowledge
- **Skills**: See `../skills/` for skill implementations
- **Architecture**: See `/home/olino3/git/forge/CLAUDE.md` for full system overview

---

## Quick Start Guide

### For Skills

**Minimal memory workflow:**

1. Detect project name (from git repo, directory name, etc.)
2. Check if `memory/skills/{skill_name}/{project_name}/` exists
3. **If yes**: Read existing memory files to understand project
4. **If no**: Note this is the first time analyzing this project
5. Perform analysis (combining context knowledge + memory insights)
6. Save or update memory files with new insights learned

### For New Projects

**First-time analysis workflow:**

1. Skill detects it's a new project (no memory directory exists)
2. Performs analysis using only context files (general best practices)
3. Creates memory directory automatically
4. Saves learned patterns and project details to memory files
5. Next invocation will be smarter - will have project-specific understanding!

**No manual setup required** - memory builds automatically with each skill invocation!
