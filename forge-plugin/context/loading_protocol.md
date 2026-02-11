---
id: "engineering/loading_protocol"
domain: engineering
title: "Context Loading Protocol"
type: reference
estimatedTokens: 600
loadingStrategy: always
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Overview"
    estimatedTokens: 23
    keywords: [overview]
  - name: "Step 1: Read Domain Index"
    estimatedTokens: 36
    keywords: [step, read, domain, index]
  - name: "Step 2: Load Always Files"
    estimatedTokens: 51
    keywords: [step, load, always, files]
  - name: "Step 3: Detect Project Type"
    estimatedTokens: 54
    keywords: [step, detect, project, type]
  - name: "Step 4: Load Conditional Context"
    estimatedTokens: 72
    keywords: [step, load, conditional, context]
  - name: "Step 5: Check Cross-Domain Context"
    estimatedTokens: 35
    keywords: [step, check, cross-domain, context]
  - name: "Loading Modes"
    estimatedTokens: 144
    keywords: [loading, modes]
  - name: "Quick Reference"
    estimatedTokens: 24
    keywords: [quick, reference]
  - name: "For Skill Authors"
    estimatedTokens: 28
    keywords: [skill, authors]
  - name: "For Command Authors"
    estimatedTokens: 19
    keywords: [command, authors]
tags: [context, loading, protocol, engineering, reference]
---

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

## Loading Modes

The protocol supports two loading modes:

### Traditional Mode (Default)

The existing 5-step process described above. Skills and commands manually follow each step by reading files directly. This is the default and requires no additional setup.

### Reference-First Mode (Opt-in)

An alternative approach using [ContextProvider](../interfaces/context_provider.md) methods for structured, metadata-aware loading:

1. **Catalog**: Call `contextProvider.getCatalog(domain)` to get a structured inventory of all context files with metadata (token costs, tags, loading strategy) -- zero content loaded
2. **Evaluate**: Inspect metadata to decide which files are worth loading based on relevance and token budget
3. **Materialize**: Call `contextProvider.materialize(reference)` to load full content, or `contextProvider.materializeSections(reference, sections)` to load only specific sections

**When to use Reference-First Mode**:
- Token-constrained scenarios where precise loading is critical
- Skills that need to inspect metadata before committing to loading
- Discovery-oriented workflows where you don't know which files are relevant

**When to use Traditional Mode**:
- Standard skill and command workflows
- When the 5-step process is well-understood and sufficient
- When the domain is familiar and file selection is straightforward

Both modes produce the same outcome (relevant context loaded); they differ only in how files are discovered and selected.

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
