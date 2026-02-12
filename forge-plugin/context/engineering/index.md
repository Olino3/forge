---
id: "engineering/index"
domain: engineering
title: "Engineering Context Index"
type: index
estimatedTokens: 250
loadingStrategy: always
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
indexedFiles:
  - id: "engineering/code_review_principles"
    path: "code_review_principles.md"
    type: reference
    loadingStrategy: onDemand
  - id: "engineering/api_design_patterns"
    path: "api_design_patterns.md"
    type: reference
    loadingStrategy: onDemand
  - id: "engineering/testing_principles"
    path: "testing_principles.md"
    type: reference
    loadingStrategy: onDemand
  - id: "engineering/architecture_patterns"
    path: "architecture_patterns.md"
    type: reference
    loadingStrategy: onDemand
  - id: "engineering/error_recovery"
    path: "error_recovery.md"
    type: reference
    loadingStrategy: onDemand
sections:
  - name: "Directory Contents"
    estimatedTokens: 60
    keywords: [directory, contents]
  - name: "When to Load"
    estimatedTokens: 36
    keywords: [load]
  - name: "Loading Guidance"
    estimatedTokens: 33
    keywords: [loading, guidance]
tags: [engineering, index, navigation, code-review, api, testing, architecture]
---

# Engineering Context Index

General software engineering best practices applicable across all languages and frameworks. Load these files when skills or commands need universal engineering guidance beyond language-specific context.

## Directory Contents

| File | Use For | Key Topics |
|------|---------|------------|
| `code_review_principles.md` | Universal code review standards | DRY, SOLID, KISS, YAGNI, PR sizing, severity classification |
| `api_design_patterns.md` | REST API design guidance | Conventions, error formats, pagination, versioning |
| `testing_principles.md` | Testing strategy decisions | Test pyramid, coverage, mocking, TDD/BDD |
| `architecture_patterns.md` | Architecture selection | Clean, Hexagonal, CQRS, Event-driven, Microservices |
| `error_recovery.md` | Skill failure handling | Git failures, memory errors, large diffs, permissions |

## When to Load

| Scenario | Files to Load |
|----------|--------------|
| Code review (any language) | `code_review_principles.md` |
| API endpoint review/implementation | `api_design_patterns.md` |
| Test generation or `/test` command | `testing_principles.md` |
| Architecture decisions or `/brainstorm` | `architecture_patterns.md` |
| Skill encounters an error | `error_recovery.md` |

## Loading Guidance

These files supplement domain-specific context. Load them **after** domain context, not instead of it:
1. Load primary domain context first (python/, dotnet/, angular/)
2. Load engineering context for cross-cutting guidance
3. Count toward the 4-6 file token budget (see `loading_protocol.md`)

---

*Last Updated: 2026-02-10*
