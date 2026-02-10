# Context Loading Protocol

A standardized protocol for all Forge skills and commands to load context efficiently. Reference this document in every skill/command workflow.

## Overview

Context loading follows a 5-step process to ensure skills load only what they need while maintaining thoroughness. This prevents both under-loading (missing critical guidance) and over-loading (wasting tokens on irrelevant files).

## Step 1: Read Domain Index

**Action**: Read `context/{domain}/index.md` for your primary domain.

- The index lists all available files with "Use For" descriptions
- It includes a context detection workflow specific to the domain
- Start here to understand what's available before loading anything else

**Example**: For a Python code review, start with `context/python/index.md`

## Step 2: Load "Always" Files

**Action**: Load files marked as "ALWAYS LOAD" in the domain index.

Each domain has files that should always be loaded regardless of project specifics:

| Domain | Always-Load File | Purpose |
|--------|-----------------|---------|
| python/ | `common_issues.md` | Universal Python problems |
| dotnet/ | `common_issues.md` | Universal .NET problems |
| angular/ | `common_issues.md` | Universal Angular problems |
| schema/ | `common_patterns.md` | Foundational schema concepts |

## Step 3: Detect Project Type

**Action**: Use the domain's `context_detection.md` (if available) to identify:

- Framework and version (e.g., FastAPI 0.100+, Angular 17, .NET 8)
- Key libraries and tools (e.g., SQLAlchemy, NgRx, Entity Framework)
- Architecture patterns (e.g., CQRS, microservices, monolith)
- Testing framework (e.g., pytest, Jest, xUnit)

Detection files exist for: `python/`, `dotnet/`, `angular/`

For domains without detection files (git/, security/, azure/, schema/), skip to Step 4 and use the domain index decision matrix directly.

## Step 4: Load Conditional Context

**Action**: Based on detection results, load only the files relevant to the detected project type.

Use the domain index's decision matrix or loading workflow to determine which files to load:

- **Detected framework** → Load framework-specific patterns (e.g., `fastapi_patterns.md`)
- **Detected library** → Load library-specific patterns (e.g., `ngrx_patterns.md`)
- **Detected concern** → Load cross-cutting patterns (e.g., `performance_patterns.md`)

**Token Budget**: Aim to load 4-6 context files maximum per invocation. If more are relevant, prioritize by:
1. Always-load files (mandatory)
2. Primary framework patterns (high priority)
3. Detected library patterns (medium priority)
4. Cross-cutting concerns (load if directly relevant)

## Step 5: Check Cross-Domain Context

**Action**: Consult `context/cross_domain.md` for secondary context needs.

Some code requires context from multiple domains:
- Python auth code → also load `security/security_guidelines.md`
- Database queries → also load `security/security_guidelines.md`
- Any code review with schema files → also load `schema/common_patterns.md`

See `cross_domain.md` for the complete trigger-to-context mapping.

## Quick Reference

```
1. Read {domain}/index.md
2. Load always-load files (common_issues.md, etc.)
3. Detect project type (if detection file exists)
4. Load conditional files (max 4-6 total)
5. Check cross_domain.md for secondary context
```

## For Skill Authors

When writing a new SKILL.md, reference this protocol in your "Load Context" step:

```markdown
### Step N: Load Context
- Follow `context/loading_protocol.md` for the `{domain}` domain
- Primary domain: {domain}/
- Secondary domains (if applicable): security/, schema/
```

## For Command Authors

Commands should follow the same protocol but may load from multiple domains simultaneously (e.g., `/analyze` may load both `python/` and `security/` context).

---

*Last Updated: 2026-02-10*
