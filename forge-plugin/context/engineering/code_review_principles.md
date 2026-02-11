---
id: "engineering/code_review_principles"
domain: engineering
title: "Code Review Principles"
type: reference
estimatedTokens: 150
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Core Principles"
    estimatedTokens: 40
    keywords: [dry, solid, kiss, yagni]
  - name: "Severity Classification"
    estimatedTokens: 30
    keywords: [critical, high, medium, low, severity]
  - name: "Review Focus Areas"
    estimatedTokens: 30
    keywords: [correctness, security, performance, maintainability, testing]
tags: [engineering, code-review, principles, universal]
crossDomainTriggers: []
---

# Code Review Principles

Universal code review standards applicable to all languages and frameworks.

## Core Principles

| Principle | What to Check | Common Violations |
|-----------|--------------|-------------------|
| **DRY** (Don't Repeat Yourself) | Duplicated logic, copy-pasted code | Same validation in multiple places, repeated error handling |
| **SOLID** | Single responsibility, open/closed, LSP, ISP, DIP | God classes, tight coupling, interface pollution |
| **KISS** (Keep It Simple) | Unnecessary complexity, over-engineering | Premature abstraction, unnecessary patterns |
| **YAGNI** (You Aren't Gonna Need It) | Speculative features, unused code | Feature flags for non-existent features, unused parameters |

## Severity Classification

| Severity | Definition | Action Required |
|----------|-----------|-----------------|
| Critical | Security vulnerability, data loss risk, crash | Must fix before merge |
| High | Bug, significant performance issue, maintainability blocker | Should fix before merge |
| Medium | Code smell, minor performance issue, style inconsistency | Fix recommended, not blocking |
| Low | Nitpick, suggestion, minor improvement | Optional, author's discretion |

## PR Size Guidance

| Size | Files | Lines Changed | Review Time |
|------|-------|--------------|-------------|
| Small | 1-3 | < 200 | < 30 min |
| Medium | 4-10 | 200-500 | 30-60 min |
| Large | 10+ | 500+ | > 60 min, consider splitting |

## Review Focus Areas

1. **Correctness**: Does the code do what it claims?
2. **Security**: Input validation, auth checks, data exposure
3. **Performance**: Algorithmic complexity, resource usage, N+1 queries
4. **Maintainability**: Readability, naming, documentation
5. **Testing**: Adequate coverage, meaningful assertions, edge cases

## References

- [Google Engineering Practices - Code Review](https://google.github.io/eng-practices/review/)
- [Microsoft Code Review Best Practices](https://learn.microsoft.com/en-us/devops/develop/code-review)
- [Conventional Comments](https://conventionalcomments.org/)

---

*Last Updated: 2026-02-10*
