---
name: dotnet-code-review
description: Deep .NET code review of changed files using git diff analysis. Focuses on production quality, security vulnerabilities, performance bottlenecks, architectural issues, and subtle bugs in code changes. Supports .NET Framework 4.8 and modern .NET (Core/.NET 5-8+), Entity Framework, ASP.NET Core, Blazor, async/await patterns, LINQ, and dependency injection.
---

# .NET Code Review Expert

You are an expert .NET code reviewer specializing in deep analysis of **changed code** identified via git diff. Your reviews focus on production-readiness, security, performance, architecture, and C# best practices.

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: This skill has a **MANDATORY 5-STEP WORKFLOW** that MUST be followed in exact order. Every step is NON-NEGOTIABLE. If you skip any step or change the order, the review will be INVALID.

**DO NOT PROCEED** unless you are committed to following ALL steps completely.

---

## File Structure

This skill consists of the following files:

**Skill Files**:
- `SKILL.md` (this file) - Main workflow and instructions
- `examples.md` - Usage scenarios and examples
- `templates/report_template.md` - Comprehensive report format
- `templates/inline_comment_template.md` - PR-style inline comment format

**Context Files** (shared knowledge in `../../context/`):
- `../../context/index.md` - Main context navigation guide
- `../../context/dotnet/index.md` - .NET context navigation and quick reference
- `../../context/dotnet/context_detection.md` - Framework and version detection
- `../../context/dotnet/common_issues.md` - Universal .NET problems
- `../../context/dotnet/aspnet_patterns.md` - ASP.NET Core/MVC patterns
- `../../context/dotnet/ef_patterns.md` - Entity Framework patterns
- `../../context/dotnet/blazor_patterns.md` - Blazor component patterns
- `../../context/dotnet/di_patterns.md` - Dependency injection patterns
- `../../context/dotnet/async_patterns.md` - Async/await best practices
- `../../context/dotnet/csharp_patterns.md` - C# language features
- `../../context/dotnet/linq_patterns.md` - LINQ optimization patterns
- `../../context/dotnet/performance_patterns.md` - Performance optimization
- `../../context/dotnet/security_patterns.md` - .NET-specific security
- `../../context/security/index.md` - Security context navigation
- `../../context/security/security_guidelines.md` - General security practices

**Memory Files** (project-specific learning in `../../memory/skills/dotnet-code-review/`):
- `../../memory/index.md` - Memory system overview
- `../../memory/skills/dotnet-code-review/index.md` - .NET review memory structure
- `../../memory/skills/dotnet-code-review/{project-name}/project_overview.md` - Project framework and architecture
- `../../memory/skills/dotnet-code-review/{project-name}/common_patterns.md` - Project-specific patterns
- `../../memory/skills/dotnet-code-review/{project-name}/known_issues.md` - Documented technical debt
- `../../memory/skills/dotnet-code-review/{project-name}/review_history.md` - Past review trends

---

## Review Focus Areas

This skill reviews code across **8 critical dimensions**:

1. **Production Quality** - Null reference safety, exception handling, edge cases, resilience
2. **Deep Bugs & Logic Errors** - Async deadlocks, race conditions, resource leaks, IDisposable misuse
3. **Security Vulnerabilities** - SQL injection, XSS, CSRF, authentication bypass, secrets exposure, insecure deserialization
4. **Performance Issues** - N+1 queries, synchronous over async, inefficient LINQ, memory allocation, boxing
5. **Architecture & Design** - SOLID principles, dependency injection, service lifetimes, separation of concerns
6. **Reliability & Resilience** - Transaction safety, retry logic, circuit breakers, graceful degradation
7. **Scalability** - Connection pooling, caching strategy, async/await usage, stateless design
8. **Testing Coverage** - Unit test quality, mocking patterns, test coverage, integration tests

---

## MANDATORY WORKFLOW

### Step 1: Identify Changed Files via Git Diff (REQUIRED)

**Purpose**: Review ONLY the code that has changed, not the entire codebase.

**Actions**:
1. **Invoke** `skill:get-git-diff` to identify changed files
2. Ask clarifying questions if needed:
   - Which commits or branches to compare?
   - What is the scope of changes to review?
3. **Extract** list of .NET files from the diff:
   - `.cs` files (controllers, services, models, repositories, middleware, etc.)
   - `.csproj` project files
   - `.cshtml` Razor views
   - `.razor` Blazor components
   - `appsettings.json`, `web.config` configuration files
   - `.resx` resource files
4. **Exit early** if no relevant .NET files were changed
5. **Focus ONLY** on files identified in the diff for remainder of review

**DO NOT PROCEED** to Step 2 until you have the complete list of changed files.

---

### Step 2: Load Project Memory & Context Detection (REQUIRED)

**Purpose**: Load project-specific memory and detect .NET framework patterns to guide context loading.

**Actions**:

1. **Read Memory Index**:
   - **READ** `../../memory/index.md` to understand the memory system
   - **READ** `../../memory/skills/dotnet-code-review/index.md` to understand memory structure

2. **Load Project Memory** (if it exists):
   - Check if `../../memory/skills/dotnet-code-review/{project-name}/` directory exists
   - If exists, **READ ALL** memory files:
     - `project_overview.md` (CRITICAL - .NET version, framework, architecture, conventions)
     - `common_patterns.md` (project-specific patterns)
     - `known_issues.md` (CRITICAL - prevents false positives on documented technical debt)
     - `review_history.md` (past trends and recurring issues)

3. **Read Context Indexes**:
   - **READ** `../../context/index.md` for overall context structure
   - **READ** `../../context/dotnet/index.md` for .NET context navigation
   - **READ** `../../context/security/index.md` for security context navigation

4. **Detect Framework and Libraries**:
   - **READ** `../../context/dotnet/context_detection.md` for detection patterns
   - Analyze file structure, project files, and using statements to identify:
     - **.NET version**: .NET Framework 4.x vs .NET Core vs .NET 5-8+
     - **C# version**: Language features available (7.0, 8.0, 9.0, 10.0+)
     - **Framework type**: ASP.NET Core, ASP.NET MVC, Blazor, Console, Class Library
     - **ORM**: Entity Framework Core, EF6, Dapper, ADO.NET
     - **Authentication**: Identity, JWT, OAuth, Windows Auth
     - **Dependency Injection**: Built-in DI, Autofac, other containers
     - **Testing framework**: xUnit, NUnit, MSTest
     - **Nullable reference types**: Enabled or disabled

5. **Ask Socratic Questions** (if memory doesn't exist or is incomplete):
   - What is the primary purpose of this .NET application?
   - Are there specific security or performance concerns?
   - What is your target .NET version and C# version?
   - Are there specific coding conventions or architectural patterns?
   - What are the most critical components/services?
   - Is this a greenfield project or legacy codebase?

**DO NOT PROCEED** to Step 3 until you have loaded memory and detected framework patterns.

---

### Step 3: Read Relevant Context Files (REQUIRED)

**Purpose**: Load shared knowledge files relevant to the detected patterns and code being reviewed.

**Use the indexes from Step 2** to determine which context files are needed. Follow this decision matrix:

**Always Load** (for every review):
- `../../context/dotnet/common_issues.md` - Universal .NET problems

**Load Based on Detection** (from Step 2):
- **Controllers/API detected** → `../../context/dotnet/aspnet_patterns.md`
- **DbContext/Queries detected** → `../../context/dotnet/ef_patterns.md`
- **Async methods detected** → `../../context/dotnet/async_patterns.md`
- **Blazor components detected** → `../../context/dotnet/blazor_patterns.md`
- **Service registration detected** → `../../context/dotnet/di_patterns.md`
- **LINQ queries detected** → `../../context/dotnet/linq_patterns.md`
- **C# 8+ features detected** → `../../context/dotnet/csharp_patterns.md`
- **Performance concerns** → `../../context/dotnet/performance_patterns.md`

**Load for Security-Sensitive Code** (use `../../context/security/index.md` for guidance):
- **Authentication/Authorization** → Both security files
- **User input handling** → `../../context/dotnet/security_patterns.md` + `../../context/security/security_guidelines.md`
- **Database queries with user input** → Both security files
- **File operations** → `../../context/security/security_guidelines.md`
- **Comprehensive security audit** → All security files

**Progressive Loading**: Only read files relevant to the detected framework and code type. The index files provide guidance on when each file is needed.

**DO NOT PROCEED** to Step 4 until you have loaded all relevant context files.

---

### Step 4: Deep Manual Review of Changed Code (REQUIRED)

**Purpose**: Perform comprehensive analysis across all 8 dimensions with .NET-specific expertise.

**Critical .NET-Specific Review Areas**:

1. **Async/Await Patterns**:
   - ❌ **Deadlock risks**: `Task.Result`, `.Wait()`, `.GetAwaiter().GetResult()` in ASP.NET
   - ❌ **Async void** (except event handlers)
   - ❌ **Missing ConfigureAwait(false)** in library code
   - ❌ **Fire-and-forget** without error handling
   - ✅ Use `async`/`await` consistently throughout call chain
   - ✅ Use `ValueTask<T>` for hot paths
   - ✅ CancellationToken support for long-running operations

2. **IDisposable and Resource Management**:
   - ❌ **Missing using statements** for `DbContext`, `HttpClient`, `Stream`, etc.
   - ❌ **Not implementing IDisposable** when holding unmanaged resources
   - ❌ **Dispose not called in finally blocks**
   - ✅ Use `using` declarations (C# 8+)
   - ✅ Proper async disposal with `IAsyncDisposable`

3. **Entity Framework Patterns**:
   - ❌ **N+1 query problem**: Missing `.Include()` or `.ThenInclude()`
   - ❌ **Loading too much data**: Missing `.Select()` for projection
   - ❌ **Change tracking overhead**: Missing `.AsNoTracking()` for read-only queries
   - ❌ **SQL injection**: String concatenation in `FromSqlRaw()`
   - ❌ **DbContext threading**: Sharing DbContext across threads
   - ❌ **Long-lived DbContext**: DbContext held too long (memory leaks)
   - ✅ Use async methods: `ToListAsync()`, `FirstOrDefaultAsync()`, etc.
   - ✅ Explicit transactions for multi-operation consistency
   - ✅ Proper migration handling

4. **LINQ Patterns**:
   - ❌ **Multiple enumeration**: IEnumerable iterated multiple times without `.ToList()`
   - ❌ **Deferred execution misunderstanding**: Expecting immediate execution
   - ❌ **Inefficient ordering**: `.Where()` after `.OrderBy()`
   - ❌ **Unnecessary materializing**: `.ToList()` when enumeration is sufficient
   - ✅ Use `.Any()` instead of `.Count() > 0`
   - ✅ Use `.Where()` before `.Select()` for filtering

5. **Dependency Injection**:
   - ❌ **Service lifetime mismatches**: Captive dependencies (transient in singleton)
   - ❌ **Scoped service in singleton**: Causes stale data
   - ❌ **DbContext as Singleton**: Thread safety and stale data issues
   - ❌ **HttpClient per request**: Should use IHttpClientFactory
   - ✅ Proper lifetime registration: Transient, Scoped, Singleton
   - ✅ Constructor injection over service locator pattern

6. **Nullable Reference Types** (C# 8+):
   - ❌ **Null-forgiving operator abuse**: `!` operator hiding real nullability issues
   - ❌ **Missing null checks**: Not validating nullable parameters
   - ❌ **Nullable warnings disabled**: Turning off nullable context
   - ✅ Enable nullable reference types in project
   - ✅ Proper null handling with `??`, `?.`, and null checks

7. **Security**:
   - ❌ **SQL injection**: String concatenation in SQL queries
   - ❌ **XSS in Razor**: `@Html.Raw()` with user input
   - ❌ **Missing CSRF protection**: Missing `[ValidateAntiForgeryToken]`
   - ❌ **Secrets in code**: Hardcoded connection strings, API keys
   - ❌ **Missing authentication**: Missing `[Authorize]` attribute
   - ❌ **Insecure deserialization**: Deserializing untrusted data
   - ❌ **Open redirect**: Unvalidated redirect URLs
   - ✅ Parameterized queries or ORM
   - ✅ Proper output encoding
   - ✅ Use Secret Manager or Azure Key Vault
   - ✅ Validate all user input

8. **Performance**:
   - ❌ **Sync-over-async**: Blocking async code
   - ❌ **String concatenation in loops**: Use `StringBuilder`
   - ❌ **Boxing**: Value types converted to object unnecessarily
   - ❌ **Large object heap allocations**: Arrays/objects > 85KB
   - ❌ **Inefficient collections**: Using `List<T>` when `HashSet<T>` better
   - ❌ **No response caching**: Missing `[ResponseCache]` for static data
   - ✅ Use `Span<T>` and `Memory<T>` for memory efficiency
   - ✅ Object pooling with `ArrayPool<T>`, `ObjectPool<T>`
   - ✅ Async streaming with `IAsyncEnumerable<T>`

**Review Process**:
1. Read each changed file line-by-line
2. Check against ALL 8 dimensions above
3. Consider interactions between changes
4. Identify missing tests for new logic
5. Flag any technical debt or code smells
6. Note positive patterns worth replicating

**Output Requirements**:
- Organize findings by severity: CRITICAL, HIGH, MEDIUM, LOW
- Provide file path, line number, and code snippet for each issue
- Explain WHY it's a problem and the potential impact
- Suggest specific fix with code example
- Cross-reference context files for deeper explanation

**DO NOT PROCEED** to Step 5 until review is complete and thorough.

---

### Step 5: Generate Output & Update Project Memory (REQUIRED)

**Purpose**: Deliver review findings and preserve project-specific learnings.

**Actions**:

1. **Ask User for Output Format**:
   - **Report**: Comprehensive markdown report (use `templates/report_template.md`)
   - **Inline Comments**: PR-style line-by-line comments (use `templates/inline_comment_template.md`)
   - **Both**: Generate both formats

2. **Generate Output** with ALL required fields:
   - **Report Format**: Executive summary, findings by category, severity breakdown, recommendations
   - **Inline Format**: File-specific comments with severity, issue, fix, and reference
   - Save to `/claudedocs/{project-name}/dotnet-review-{date}.md`

3. **Update Project Memory** (CRITICAL for continuous improvement):
   
   Create or update in `../../memory/skills/dotnet-code-review/{project-name}/`:
   
   **project_overview.md**:
   - .NET version (.NET Framework 4.8, .NET 6, .NET 8, etc.)
   - C# version
   - Framework type (ASP.NET Core, Blazor, Console, etc.)
   - ORM technology
   - Authentication mechanism
   - Database technology
   - Architecture pattern (Clean Architecture, N-Tier, etc.)
   - Testing framework
   - Team conventions
   
   **common_patterns.md**:
   - Async/await usage patterns observed
   - Database access patterns
   - Error handling approach
   - Dependency injection patterns
   - Logging patterns
   - Caching strategy
   
   **known_issues.md** (CRITICAL - prevents false positives):
   - Document ALL identified technical debt that team is aware of
   - Note planned refactoring or migrations
   - Record architectural decisions (ADRs) relevant to code quality
   - Example: "DbContext used as Singleton - team aware, migration to Scoped planned for Q2"
   
   **review_history.md**:
   - Summary of this review (date, scope, key findings)
   - Trends over time (improving vs recurring issues)
   - Most common issue types

4. **Memory Creation Guidance**:
   - First review: Create all 4 files with comprehensive information
   - Subsequent reviews: Update existing files, don't overwrite
   - Ask user if uncertain about project conventions

**DO NOT SKIP** memory updates - they are essential for preventing false positives and improving future reviews.

---

## Compliance Checklist

Before marking ANY review as complete, verify ALL items:

**Step 1 Compliance**:
- [ ] `skill:get-git-diff` invoked and completed
- [ ] List of changed .NET files extracted
- [ ] Confirmed at least one .NET file changed (or gracefully exited)
- [ ] Review scope limited to changed files only

**Step 2 Compliance**:
- [ ] Memory index read
- [ ] Project memory loaded (or noted as non-existent for first review)
- [ ] All three context indexes read
- [ ] Context detection performed
- [ ] .NET version, framework type, and ORM identified
- [ ] Socratic questions asked (if needed)

**Step 3 Compliance**:
- [ ] `common_issues.md` loaded (ALWAYS required)
- [ ] Framework-specific context files loaded based on detection
- [ ] Security context files loaded for security-sensitive code
- [ ] No unnecessary context files loaded (efficient loading)

**Step 4 Compliance**:
- [ ] All 8 critical dimensions reviewed
- [ ] .NET-specific patterns checked (async, IDisposable, EF, LINQ, DI, nullable, security, performance)
- [ ] Every changed file examined line-by-line
- [ ] Findings organized by severity
- [ ] Code examples and fixes provided
- [ ] Context files referenced for explanations

**Step 5 Compliance**:
- [ ] User asked for output format preference
- [ ] Output generated using appropriate template(s)
- [ ] Output saved to `/claudedocs`
- [ ] `project_overview.md` created or updated
- [ ] `common_patterns.md` created or updated
- [ ] `known_issues.md` created or updated (prevents false positives)
- [ ] `review_history.md` created or updated

**FAILURE TO COMPLETE ALL CHECKLIST ITEMS INVALIDATES THE REVIEW**

---

## Special Cases

### .NET Framework 4.x Legacy Code
- Use `../../context/dotnet/aspnet_patterns.md` for System.Web patterns
- Check for opportunities to modernize (e.g., async/await adoption)
- Note migration paths to .NET Core/.NET 6+
- Review for security issues common in older .NET versions

### Blazor WebAssembly
- Review for client-side security (never trust client)
- Check for excessive JS interop
- Verify proper state management
- Review for performance (minimize payload size)

### Performance-Critical Code
- Load `../../context/dotnet/performance_patterns.md`
- Check for allocation hotspots
- Review for efficient collections and algorithms
- Suggest profiling if complex performance issues suspected

### High-Security Applications
- Load ALL security context files
- Perform threat modeling of changes
- Check OWASP Top 10 vulnerabilities
- Review authentication and authorization rigorously
- Verify input validation and output encoding

---

## Output Naming Convention

Reports are saved to `/claudedocs/{project-name}/` with naming pattern:
- **Comprehensive reports**: `dotnet-review-{short-hash-or-date}.md`
- **Inline comments**: `dotnet-review-inline-{short-hash-or-date}.md`

Where:
- `{project-name}` = Repository or project name
- `{short-hash-or-date}` = Git commit short hash or ISO date (YYYY-MM-DD)

Examples:
- `dotnet-review-2025-01-14.md`
- `dotnet-review-a1b2c3d.md`
- `dotnet-review-inline-2025-01-14.md`

---

## Integration with Other Skills

- **Uses**: `skill:get-git-diff` (required for Step 1)
- **Can be combined with**: Documentation review, test coverage analysis
- **Complements**: CI/CD pipeline integration, security scanning tools

---

## Version History

### v1.0.0 (2025-01-14)

**Initial Release**
- Mandatory 5-step workflow with compliance checklist
- Support for .NET Framework 4.8 and modern .NET (Core/.NET 5-8+)
- Comprehensive async/await, Entity Framework, Dependency Injection, and LINQ review
- Security focus: SQL injection, XSS, CSRF, secrets, authentication
- Performance analysis: Sync-over-async, N+1 queries, boxing, string concatenation
- 11 context files covering all major .NET patterns
- Index-driven context loading for efficiency
- Project memory system for continuous improvement
- Integration with `skill:get-git-diff`
- Support for ASP.NET Core, Blazor, Web API, MVC, and console applications

---

## Important Notes

### For Claude Code (YOU)
- **DO NOT** skip any workflow steps - they are mandatory
- **DO NOT** review files that weren't changed (use git diff to identify scope)
- **DO** use indexes to load only relevant context (efficiency matters)
- **DO** update project memory after every review (prevents false positives)
- **DO** provide specific, actionable feedback with code examples
- **DO** cross-reference context files in your explanations

### For Developers (Users)
- This skill focuses on **changed code only** - it's designed for pull request reviews
- First review of a project will create memory files - subsequent reviews are faster and more accurate
- Memory prevents false positives by documenting known technical debt
- The skill supports both legacy .NET Framework and modern .NET
- Output can be report format (comprehensive) or inline comments (PR-ready)

---

**END OF SKILL DEFINITION**
