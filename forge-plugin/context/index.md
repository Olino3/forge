---
id: "engineering/index"
domain: engineering
title: "Context Directory Index"
type: index
estimatedTokens: 1500
loadingStrategy: always
version: "1.0.0"
lastUpdated: "2026-02-10"
indexedFiles:
  - id: "engineering/index"
    path: "engineering/index.md"
    type: index
    loadingStrategy: always
  - id: "angular/index"
    path: "angular/index.md"
    type: index
    loadingStrategy: always
  - id: "azure/index"
    path: "azure/index.md"
    type: index
    loadingStrategy: always
  - id: "commands/index"
    path: "commands/index.md"
    type: index
    loadingStrategy: always
  - id: "dotnet/index"
    path: "dotnet/index.md"
    type: index
    loadingStrategy: always
  - id: "git/index"
    path: "git/index.md"
    type: index
    loadingStrategy: always
  - id: "python/index"
    path: "python/index.md"
    type: index
    loadingStrategy: always
  - id: "schema/index"
    path: "schema/index.md"
    type: index
    loadingStrategy: always
  - id: "security/index"
    path: "security/index.md"
    type: index
    loadingStrategy: always
sections:
  - name: "Purpose"
    estimatedTokens: 24
    keywords: [purpose]
  - name: "Directory Structure"
    estimatedTokens: 214
    keywords: [directory, structure]
  - name: "Quick Reference Guide"
    estimatedTokens: 1442
    keywords: [quick, reference, guide]
  - name: "Usage Patterns"
    estimatedTokens: 344
    keywords: [usage, patterns]
  - name: "Quick Reference Table"
    estimatedTokens: 20
    keywords: [quick, reference, table]
  - name: "Official Documentation"
    estimatedTokens: 20
    keywords: [official, documentation]
  - name: "Detection Patterns"
    estimatedTokens: 20
    keywords: [detection, patterns]
  - name: "Common Issues"
    estimatedTokens: 13
    keywords: [issues]
  - name: "Context vs Memory"
    estimatedTokens: 57
    keywords: [context, memory]
  - name: "Maintenance Guidelines"
    estimatedTokens: 98
    keywords: [maintenance, guidelines]
  - name: "Related Documentation"
    estimatedTokens: 24
    keywords: [related, documentation]
tags: [context, index, navigation, engineering]
---

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
├── loading_protocol.md          # Universal context loading protocol
├── cross_domain.md              # Cross-domain context trigger matrix
├── engineering/                  # General software engineering context
│   ├── index.md
│   ├── code_review_principles.md
│   ├── api_design_patterns.md
│   ├── testing_principles.md
│   ├── architecture_patterns.md
│   └── error_recovery.md
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
├── azure/
│   ├── index.md
│   ├── azure_functions_overview.md
│   ├── azure_pipelines_cicd_patterns.md
│   ├── azure_pipelines_overview.md
│   ├── azure_bicep_overview.md
│   ├── azurite_setup.md
│   ├── docker_compose_reference.md
│   ├── dockerfile_reference.md
│   ├── local_development_setup.md
│   └── tiltfile_reference.md
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
│   ├── index.md
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
├── schema/
│   ├── index.md
│   ├── common_patterns.md
│   ├── database_patterns.md
│   └── file_formats.md
├── security/
│   ├── index.md
│   ├── owasp_python.md
│   └── security_guidelines.md
└── commands/
    ├── index.md
    ├── analysis_patterns.md
    ├── implementation_strategies.md
    ├── refactoring_patterns.md
    ├── documentation_standards.md
    ├── testing_strategies.md
    ├── build_patterns.md
    └── brainstorming_patterns.md
```

**Note**: MCP server documentation lives in `forge-plugin/mcps/` (separate from context). See [MCP Index](../mcps/index.md) for the server catalog, activation protocol, and per-server docs.

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

### Azure Functions Context (`azure/`)

**When to use**: Generating or working with Azure Functions projects, local development setup with Tilt and Azurite

| File | Use For | Key Topics |
|------|---------|------------|
| `index.md` | Navigation and context loading guide | Quick reference, decision matrix for which files to load |
| `azure_functions_overview.md` | Understanding programming models | v1 vs v2, triggers, bindings, host.json, structure differences |
| `local_development_setup.md` | Setting up local development | Tilt + Azurite architecture, ports, environment variables, workflow |
| `tiltfile_reference.md` | Creating Tiltfiles | docker_build, live_update, resource dependencies, service selection |
| `docker_compose_reference.md` | Creating docker-compose files | Service definitions, environment variables, networking, volumes |
| `dockerfile_reference.md` | Creating Dockerfiles | Base images, dependency management (pip/Poetry/npm), multi-stage builds |
| `azurite_setup.md` | Setting up Azurite emulator | Dockerfile, initialization scripts, connection strings, storage resources |
| `azure_pipelines_overview.md` | Azure Pipelines basics | YAML syntax, stages, jobs, steps, triggers, variables, environments |
| `azure_pipelines_cicd_patterns.md` | CI/CD patterns | Separate vs combined pipelines, IAC patterns, multi-environment strategies |
| `azure_bicep_overview.md` | Bicep IaC | Bicep syntax, modules, parameters, resource declarations, deployment commands |

**Load when**:
- Azure Functions: `skill:generate-azure-functions` or setting up Azure Functions local development
- Azure Pipelines: `skill:generate-azure-pipelines` or creating CI/CD workflows and infrastructure

**Azure Functions generation workflow**:
1. Load `azure/index.md` for navigation guide
2. Load `azure_functions_overview.md` to understand programming models (always)
3. Load `local_development_setup.md` for environment setup (always)
4. Load `tiltfile_reference.md` when generating Tiltfile
5. Load `docker_compose_reference.md` when generating docker-compose.yml
6. Load `dockerfile_reference.md` when generating Dockerfiles
7. Load `azurite_setup.md` when setting up Azurite storage emulator

**Azure Pipelines generation workflow**:
1. Load `azure/index.md` for navigation guide
2. Load `azure_pipelines_cicd_patterns.md` to decide architecture (always)
3. Load `azure_pipelines_overview.md` for pipeline syntax (always)
4. Load `azure_bicep_overview.md` when generating infrastructure (if needed)

---

### Schema Analysis Context (`schema/`)

**When to use**: Analyzing file schemas (JSON Schema, Protobuf, GraphQL, OpenAPI, Avro, XML/XSD) or database schemas (SQL, NoSQL)

| File | Use For | Key Topics |
|------|---------|------------|
| `index.md` | Navigation and context loading guide | Quick reference, loading decision matrix, when to use each file |
| `common_patterns.md` | Universal schema concepts | Entities, relationships, constraints, normalization, documentation, evolution |
| `file_formats.md` | File-based schema patterns | JSON Schema, Protobuf, GraphQL, OpenAPI, Avro, XML/XSD, CSV inference |
| `database_patterns.md` | Database schema patterns | SQL (PostgreSQL, MySQL), NoSQL (MongoDB, Cassandra, Neo4j, Redis), indexes, normalization |

**Load when**:
- File schemas: `skill:file-schema-analysis` or analyzing API schemas, data formats, configuration files
- Database schemas: `skill:database-schema-analysis` or analyzing database structure, migrations, optimization

**File schema analysis workflow**:
1. Load `schema/index.md` for navigation guide
2. Load `common_patterns.md` for foundational concepts (always)
3. Load `file_formats.md` for format-specific patterns (always)
4. Load `security/security_guidelines.md` if analyzing sensitive data schemas

**Database schema analysis workflow**:
1. Load `schema/index.md` for navigation guide
2. Load `common_patterns.md` for foundational concepts (always)
3. Load `database_patterns.md` for database-specific patterns (always)
4. Load `security/security_guidelines.md` if analyzing PII or sensitive data

---

### Commands Context (`commands/`)

**When to use**: Executing commands (`/analyze`, `/implement`, `/improve`, `/document`, `/test`, `/build`, `/brainstorm`)

| File | Use For | Key Topics |
|------|---------|------------|
| `index.md` | Navigation and loading patterns | Context files per command, loading decision matrix |
| `analysis_patterns.md` | `/analyze` command | Static analysis, severity classification, multi-language strategies |
| `implementation_strategies.md` | `/implement` command | TDD/BDD, incremental development, testing integration |
| `refactoring_patterns.md` | `/improve` command | Safe refactoring, code smells, technical debt tracking |
| `documentation_standards.md` | `/document` command | API docs, docstrings, JSDoc, XML docs, ADRs, README standards |
| `testing_strategies.md` | `/test` command | Test pyramid, framework detection, coverage targets, failure debugging |
| `build_patterns.md` | `/build` command | Build system detection, Docker builds, caching, artifact optimization |
| `brainstorming_patterns.md` | `/brainstorm` command | Socratic questioning, requirements elicitation, MoSCoW, RICE |

**Load when**: Executing any `/command`. Each command loads its own context file plus relevant domain context.

**Command context loading workflow**:
1. Load `commands/index.md` for navigation
2. Load command-specific file (e.g., `analysis_patterns.md` for `/analyze`)
3. Load domain-specific context based on detected language/framework
4. Load `security/security_guidelines.md` for security-focused operations

---

### Engineering Context (`engineering/`)

**When to use**: Universal software engineering guidance applicable across all languages

| File | Use For | Key Topics |
|------|---------|------------|
| `index.md` | Navigation and loading guide | When to load which engineering files |
| `code_review_principles.md` | Universal code review | DRY, SOLID, KISS, severity classification, PR sizing |
| `api_design_patterns.md` | REST API design | Conventions, error formats, pagination, versioning |
| `testing_principles.md` | Testing strategy | Test pyramid, coverage, mock vs integrate, TDD/BDD |
| `architecture_patterns.md` | Architecture selection | Clean, Hexagonal, CQRS, Event-driven, Microservices |
| `error_recovery.md` | Skill failure handling | Git failures, memory errors, large diffs, permissions |

**Load when**: Code reviews (any language), API design, test strategy decisions, architecture planning, or when a skill encounters errors

**Note**: These files supplement domain-specific context. Load after domain context, not instead of it.

---

## Usage Patterns

### For Skills

Skills should follow the [Context Loading Protocol](loading_protocol.md):

1. **Check memory first** - Load project-specific knowledge from `../../memory/skills/{skill-name}/{project-name}/`
2. **Follow loading protocol** - See `loading_protocol.md` for the standardized 5-step process
3. **Check cross-domain needs** - See `cross_domain.md` for when to load from multiple domains
4. **Perform analysis** - Apply context knowledge to the specific task
5. **Update memory** - Store project-specific insights learned during analysis

### Loading Context Efficiently

For a standardized approach, follow the [Context Loading Protocol](loading_protocol.md). For cross-domain needs, consult [Cross-Domain References](cross_domain.md).

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

**For Azure Pipelines generation**:
```markdown
1. Load azure/index.md (navigation guide)
2. Load azure_pipelines_cicd_patterns.md (decide separate vs combined)
3. Load azure_pipelines_overview.md (pipeline YAML syntax)
4. If generating infrastructure:
   - Load azure_bicep_overview.md (Bicep templates)
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

---

*Last Updated: 2026-02-10*