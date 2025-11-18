# Context Directory Index

This directory contains **shared contextual knowledge** that provides consistent guidance across all skills. Context files are organized by domain and serve as reference materials for standards, patterns, and best practices.

## Purpose

Context files provide:
- **Standards and References**: Language specifications, format definitions
- **Best Practices**: Recommended patterns and approaches
- **Common Patterns**: Recurring code structures and idioms
- **Guidelines**: Security, quality, and compliance rules

## Directory Structure

```
context/
├── index.md (this file)
├── angular/
│   ├── index.md
│   ├── common_issues.md
│   ├── component_patterns.md
│   ├── component_testing_patterns.md
│   ├── context_detection.md
│   ├── jest_testing_standards.md
│   ├── ngrx_patterns.md
│   ├── performance_patterns.md
│   ├── primeng_patterns.md
│   ├── rxjs_patterns.md
│   ├── security_patterns.md
│   ├── service_patterns.md
│   ├── service_testing_patterns.md
│   ├── tailwind_patterns.md
│   ├── test_antipatterns.md
│   ├── testing_utilities.md
│   └── typescript_patterns.md
├── dotnet/
│   ├── index.md
│   ├── aspnet_patterns.md
│   ├── async_patterns.md
│   ├── blazor_patterns.md
│   ├── common_issues.md
│   ├── context_detection.md
│   ├── csharp_patterns.md
│   ├── di_patterns.md
│   ├── ef_patterns.md
│   ├── linq_patterns.md
│   ├── performance_patterns.md
│   └── security_patterns.md
├── git/
│   ├── diff_patterns.md
│   └── git_diff_reference.md
├── python/
│   ├── common_issues.md
│   ├── context_detection.md
│   ├── datascience_patterns.md
│   ├── dependency_management.md
│   ├── django_patterns.md
│   ├── fastapi_patterns.md
│   ├── flask_patterns.md
│   ├── ml_patterns.md
│   ├── mocking_patterns.md
│   ├── test_antipatterns.md
│   ├── testing_frameworks.md
│   ├── unit_testing_standards.md
│   └── virtual_environments.md
└── security/
    ├── owasp_python.md
    └── security_guidelines.md
```

## Quick Reference Guide

### Git Context (`git/`)

**When to use**: Analyzing diffs, commits, version control changes

| File | Use For | Key Topics |
|------|---------|------------|
| `git_diff_reference.md` | Understanding diff format | Unified diff syntax, hunks, metadata, special cases |
| `diff_patterns.md` | Identifying change types | Feature additions, bug fixes, refactoring, security fixes, breaking changes |

**Load when**: Working with `skill:get-git-diff` or analyzing version control changes

---

### Angular Context (`angular/`)

**When to use**: Reviewing Angular/TypeScript code, understanding Angular patterns

| File | Use For | Key Topics |
|------|---------|------------|
| `index.md` | Navigation and context loading guide | Quick reference, loading decision matrix |
| `common_issues.md` | Universal Angular problems (ALWAYS LOAD) | Memory leaks, change detection, lifecycle hooks, observables |
| `component_patterns.md` | Component best practices | Smart vs presentational, Input/Output, lifecycle, ViewChild |
| `context_detection.md` | Framework detection | Angular version, NgRx/Akita, PrimeNG, TailwindCSS detection |
| `ngrx_patterns.md` | State management | Actions, reducers, effects, selectors, facades, entity adapters |
| `performance_patterns.md` | Performance optimization | OnPush, trackBy, lazy loading, virtual scrolling, memory |
| `primeng_patterns.md` | PrimeNG components | Table, forms, dialogs, accessibility |
| `rxjs_patterns.md` | RxJS observables | Subscription management, operators, subjects, error handling |
| `security_patterns.md` | Angular security | XSS, auth/authz, route guards, HTTP interceptors, CSRF |
| `service_patterns.md` | Service design | Dependency injection, HTTP, state management, interceptors |
| `tailwind_patterns.md` | TailwindCSS integration | Configuration, dynamic classes, responsive design |
| `typescript_patterns.md` | TypeScript best practices | Type safety, generics, utility types, strict mode |

**Load when**: Using `skill:angular-code-review`, `skill:generate-jest-unit-tests`, or analyzing Angular projects

**Context detection workflow (code review)**:
1. Start with `angular/index.md` for navigation guide
2. Use `context_detection.md` to identify framework version and libraries
3. Always load `common_issues.md` (universal Angular problems)
4. Load specific files based on detected patterns (components, services, state management)
5. Load `security_patterns.md` for auth/API/input handling code

**Unit test generation workflow**:
1. Load `jest_testing_standards.md` for core testing principles (always)
2. Load `testing_utilities.md` for TestBed, mocks, spies (always)
3. Load `test_antipatterns.md` for what to avoid (always)
4. Load `component_testing_patterns.md` if testing components
5. Load `service_testing_patterns.md` if testing services
6. Load `ngrx_patterns.md` if testing NgRx state management
7. Load `rxjs_patterns.md` if testing observables heavily

---

### .NET/C# Context (`dotnet/`)

**When to use**: Reviewing .NET, C#, ASP.NET Core, Entity Framework code

| File | Use For | Key Topics |
|------|---------|------------|
| `index.md` | Navigation and decision matrix | Quick reference, context loading patterns, file selection guide |
| `common_issues.md` | Universal .NET problems (ALWAYS LOAD) | Async/await, IDisposable leaks, LINQ pitfalls, exception handling, nullable types |
| `context_detection.md` | .NET version and framework detection | Detecting .NET Framework vs Core/.NET 5-8+, C# version, ASP.NET/Blazor, EF Core/EF6 |
| `aspnet_patterns.md` | ASP.NET Core web applications | Controllers, middleware, DI, configuration, authentication, validation, Web API |
| `ef_patterns.md` | Entity Framework patterns | DbContext lifetime, N+1 queries, eager loading, raw SQL, migrations, relationships |
| `di_patterns.md` | Dependency injection | Service lifetimes, captive dependencies, IHttpClientFactory, factory patterns, options pattern |
| `blazor_patterns.md` | Blazor components | Component lifecycle, state management, JSInterop, rendering optimization, forms |
| `async_patterns.md` | Comprehensive async/await | Sync-over-async, ConfigureAwait, CancellationToken, ValueTask, IAsyncEnumerable, deadlocks |
| `csharp_patterns.md` | Modern C# language features | Nullable reference types, pattern matching, records, init-only, top-level statements, C# 8-12 |
| `linq_patterns.md` | LINQ optimization | Deferred execution, IEnumerable vs IQueryable, multiple enumeration, query optimization |
| `performance_patterns.md` | .NET performance optimization | String performance, collections, Span<T>, ArrayPool, boxing, LOH, caching, HttpClient |
| `security_patterns.md` | .NET security patterns | SQL injection, XSS, CSRF, authentication, authorization, secrets management, input validation |

**Load when**: Using `skill:dotnet-code-review` or analyzing .NET projects

**Context detection workflow**:
1. Start with `dotnet/index.md` for navigation and decision matrix
2. Use `context_detection.md` to identify .NET version, framework type, and ORM
3. Always load `common_issues.md` (universal .NET problems)
4. Load specific files based on detected patterns:
   - ASP.NET controllers/APIs → `aspnet_patterns.md`
   - DbContext/queries → `ef_patterns.md` + `linq_patterns.md`
   - DI configuration → `di_patterns.md`
   - Blazor components → `blazor_patterns.md`
   - Async methods → `async_patterns.md`
   - Modern C# features → `csharp_patterns.md`
   - Performance-critical code → `performance_patterns.md`
   - Auth/input handling → `security_patterns.md`

---

### Python Context (`python/`)

**When to use**: Reviewing Python code, understanding frameworks

| File | Use For | Key Topics |
|------|---------|------------|
| `common_issues.md` | Identifying typical problems | Mutable defaults, exception handling, import issues, performance |
| `context_detection.md` | Identifying project type | Detecting Django/Flask/FastAPI/ML frameworks from code patterns |
| `datascience_patterns.md` | Data science code review | Pandas, NumPy, data validation, memory management |
| `dependency_management.md` | Package management operations | uv, poetry, conda, pip commands, version constraints, config files |
| `django_patterns.md` | Django best practices | Models, views, querysets, middleware, signals |
| `fastapi_patterns.md` | FastAPI best practices | Pydantic models, dependency injection, async patterns, routing |
| `flask_patterns.md` | Flask best practices | Blueprints, application factory, extensions, context |
| `ml_patterns.md` | Machine learning code | Model training, data pipelines, evaluation, deployment |
| `mocking_patterns.md` | Mocking and patching in tests | When to mock, unittest.mock, pytest-mock, common patterns, anti-patterns |
| `test_antipatterns.md` | Common testing mistakes | What to avoid, brittle tests, bad patterns, quality issues |
| `testing_frameworks.md` | pytest and unittest patterns | Framework detection, features, comparison, migration |
| `unit_testing_standards.md` | Core testing principles | AAA pattern, naming, test independence, coverage strategy |
| `virtual_environments.md` | Virtual environment management | venv, virtualenv, poetry, conda creation, activation, best practices |

**Load when**: Using `skill:python-code-review`, `skill:python-dependency-management`, `skill:generate-python-unit-tests`, or analyzing Python projects

**Context detection workflow (code review)**:
1. Start with `context_detection.md` to identify framework
2. Load framework-specific patterns file
3. Load `common_issues.md` for universal Python problems

**Dependency management workflow**:
1. Load `dependency_management.md` for package manager commands and reference
2. Load `virtual_environments.md` for venv creation and activation
3. Use for all package installation, removal, and update operations

**Unit test generation workflow**:
1. Load `unit_testing_standards.md` for core testing principles (always)
2. Load `testing_frameworks.md` for framework-specific patterns (always)
3. Load `mocking_patterns.md` for mocking strategies (always)
4. Load `test_antipatterns.md` for what to avoid (always)
5. Load framework-specific files if testing framework code (django_patterns.md for Django tests, etc.)
6. Use for all unit test generation tasks

---

### Security Context (`security/`)

**When to use**: Security-focused reviews, vulnerability assessment

| File | Use For | Key Topics |
|------|---------|------------|
| `owasp_python.md` | OWASP Top 10 vulnerabilities | Injection, auth, XSS, insecure design, security misconfiguration |
| `security_guidelines.md` | Secure coding practices | Input validation, SQL injection, XSS, CSRF, crypto, secrets |

**Load when**: Security review requested or high-risk code detected (auth, data handling, user input)

**Always load for**: Authentication code, database queries, user input handling, file operations

---

## Usage Patterns

### For Skills

Skills should load context files in this order:

1. **Check memory first** - Load project-specific knowledge from `../../memory/skills/{skill-name}/{project-name}/`
2. **Load relevant context** - Use this index to identify which context files are needed
3. **Perform analysis** - Apply context knowledge to the specific task
4. **Update memory** - Store project-specific insights learned during analysis

### Loading Context Efficiently

**Instead of reading all files**, use this index to target specific files:

```markdown
# Example: Angular code review for NgRx project with PrimeNG

1. Load angular/index.md (navigation guide)
2. Load angular/context_detection.md (detect Angular 17, NgRx, PrimeNG)
3. Load angular/common_issues.md (always load - universal issues)
4. Load angular/component_patterns.md (reviewing components)
5. Load angular/ngrx_patterns.md (state management detected)
6. Load angular/primeng_patterns.md (PrimeNG components detected)
7. Load angular/security_patterns.md (if auth/input handling present)
```

```markdown
# Example: Python code review for FastAPI project

1. Load context_detection.md (detect it's FastAPI)
2. Load fastapi_patterns.md (framework-specific)
3. Load common_issues.md (universal Python)
4. Load security_guidelines.md (if auth/input handling present)
```

**For git diff analysis**:
```markdown
1. Load git_diff_reference.md (understand format)
2. Load diff_patterns.md (classify changes)
```

**For Python unit test generation**:
```markdown
1. Load python/unit_testing_standards.md (core principles)
2. Load python/testing_frameworks.md (pytest vs unittest)
3. Load python/mocking_patterns.md (mocking strategies)
4. Load python/test_antipatterns.md (what to avoid)
5. If testing framework-specific code, also load:
   - python/django_patterns.md (for Django code)
   - python/fastapi_patterns.md (for FastAPI code)
   - python/datascience_patterns.md (for pandas/numpy code)
```

### When to Add New Context

Add new context files when:
- ✅ Knowledge applies to **multiple projects** (not project-specific)
- ✅ Information is **reference material** (standards, patterns, guidelines)
- ✅ Content is **relatively stable** (doesn't change frequently per project)

**Don't add to context** if:
- ❌ Information is **project-specific** (belongs in memory/)
- ❌ Content is **dynamic** (changes with each analysis)
- ❌ Knowledge is **temporary** (belongs in skill output)

### How to Write Context Files (Compact Approach)

**Use links over duplication** to reduce maintenance burden:

✅ **DO**:
- Keep quick reference tables (command equivalents, comparisons)
- Keep detection patterns and decision matrices (unique to our use case)
- Provide brief summaries with links to official docs
- Link to PEPs, RFCs, official documentation
- Include "what to look for" and "when to use" guidance

❌ **DON'T**:
- Duplicate content from official documentation
- Write long explanations that will become outdated
- Copy-paste API references or full command syntax
- Include extensive examples (link to official docs instead)

**Example structure**:
```markdown
## Quick Reference Table
[Keep: Command comparisons, syntax table]

## Official Documentation
[Link: Official docs for details]

## Detection Patterns
[Keep: How to identify this pattern in code]

## Common Issues
[Brief: Issue + link to solution]
```

See `python/dependency_management.md` and `python/virtual_environments.md` for examples of the compact approach.

---

## Context vs Memory

| Aspect | Context | Memory |
|--------|---------|--------|
| **Location** | `forge-plugin/context/` | `forge-plugin/memory/skills/{skill-name}/{project-name}/` |
| **Scope** | Universal, all projects | Project-specific |
| **Nature** | Static reference | Dynamic learning |
| **Updates** | Rare (when standards change) | Frequent (each skill invocation) |
| **Examples** | PEP8 rules, OWASP Top 10 | This project's naming conventions |
| **Read by** | All skills, all projects | Specific skill for specific project |

---

## Maintenance Guidelines

### For Developers

- **Update context** when standards or best practices evolve
- **Use compact approach** - link to official docs instead of duplicating content
- **Keep quick references** - tables, patterns, detection logic (unique to our use case)
- **Version context files** if major changes occur
- **Keep context focused** - one domain per directory
- **Document changes** in version history
- **Review links periodically** - ensure official documentation links are still valid

### For Skills

- **Load context explicitly** - reference files by path
- **Don't modify context** - it's read-only reference
- **Combine with memory** - context + project memory = complete understanding
- **Cache if needed** - context rarely changes within a session
- **Expect links** - context may link to official docs for detailed information

---

## Related Documentation

- **Skills**: See `forge-plugin/skills/` for skill implementations
- **Memory**: See `forge-plugin/memory/` for project-specific learning
- **Plugin**: See `forge-plugin/.claude-plugin/plugin.json` for plugin metadata
- **Architecture**: See `/home/olino3/git/forge/CLAUDE.md` for system overview