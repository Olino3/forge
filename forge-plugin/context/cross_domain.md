---
id: "engineering/cross_domain"
domain: engineering
title: "Cross-Domain Context References"
type: reference
estimatedTokens: 400
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Cross-Domain Trigger Matrix"
    estimatedTokens: 207
    keywords: [cross-domain, trigger, matrix]
  - name: "How to Use"
    estimatedTokens: 30
    keywords: [how]
  - name: "Priority Rules"
    estimatedTokens: 28
    keywords: [priority, rules]
  - name: "Token Budget Consideration"
    estimatedTokens: 21
    keywords: [token, budget, consideration]
tags: [context, cross-domain, triggers, loading, reference]
---

# Cross-Domain Context References

Maps when skills should load context from multiple domains. Consult this file during Step 5 of the [Context Loading Protocol](loading_protocol.md), or use `contextProvider.getCrossDomainContext(domain, triggers)` to resolve automatically. See [ContextProvider Interface](../interfaces/context_provider.md).

## Cross-Domain Trigger Matrix

| Primary Domain | Trigger Condition | Secondary Context to Load | Relevance Score | Token Impact |
|---|---|---|---|---|
| python/ | Auth, password, or input handling code detected | `security/security_guidelines.md` | 0.9 | ~250 |
| python/ | SQL queries, ORM usage, or database models detected | `security/security_guidelines.md` | 0.9 | ~250 |
| python/ | Schema/migration files in diff | `schema/common_patterns.md` | 0.6 | ~300 |
| dotnet/ | Auth, Identity, or JWT code detected | `security/security_guidelines.md` | 0.9 | ~250 |
| dotnet/ | Database queries, EF migrations present | `security/security_guidelines.md` | 0.8 | ~250 |
| dotnet/ | Schema or migration files in diff | `schema/common_patterns.md` | 0.6 | ~300 |
| angular/ | API integration, HTTP calls, or form input code | `security/security_guidelines.md` | 0.8 | ~250 |
| angular/ | API schema/contract files detected | `schema/common_patterns.md` | 0.5 | ~300 |
| schema/ | Database schema with PII or sensitive data | `security/security_guidelines.md` | 0.9 | ~250 |
| Any code review | Performance-critical code flagged | `{domain}/performance_patterns.md` | 0.7 | ~350 |
| Any code review | Schema/migration files in diff | `schema/common_patterns.md` | 0.5 | ~300 |
| Any code review | Infrastructure or deployment files | `azure/index.md` (for Azure projects) | 0.3 | ~200 |

### Relevance Score Guide

| Score Range | Loading Behavior |
|---|---|
| 0.8 - 1.0 | **Always materialize**: High-confidence trigger, load regardless of token budget |
| 0.5 - 0.7 | **Budget-dependent**: Load if token budget allows; skip if near the 4-6 file limit |
| 0.1 - 0.4 | **Reference only**: Use `contextProvider.getReference()` for metadata; only materialize if specifically relevant |

## How to Use

1. Determine your **primary domain** (the main language/framework being analyzed)
2. Scan the trigger conditions for your primary domain
3. If a trigger matches, load the specified secondary context file
4. Secondary context supplements but does not replace primary domain context

## Priority Rules

When multiple cross-domain triggers match:

1. **Security context** takes highest priority (always load if triggered)
2. **Schema context** when data structures are involved
3. **Performance context** when optimization is relevant
4. **Infrastructure context** when deployment files are present

## Token Budget Consideration

Cross-domain files count toward the 4-6 file budget per invocation (see `loading_protocol.md`). If already at the limit, prioritize security context over other cross-domain files.

---

*Last Updated: 2026-02-10*
