---
id: "commands/refactoring_patterns"
domain: commands
title: "Refactoring Patterns"
type: pattern
estimatedTokens: 1000
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Safe Refactoring Techniques"
    estimatedTokens: 156
    keywords: [safe, refactoring, techniques]
  - name: "Code Smell Identification"
    estimatedTokens: 150
    keywords: [code, smell, identification]
  - name: "Auto-Fix vs Approval-Required"
    estimatedTokens: 75
    keywords: [auto-fix, approval-required]
  - name: "Technical Debt Tracking"
    estimatedTokens: 84
    keywords: [technical, debt, tracking]
  - name: "Pre-Improvement Checklist"
    estimatedTokens: 40
    keywords: [pre-improvement, checklist]
  - name: "Skill Integration"
    estimatedTokens: 18
    keywords: [skill, integration]
  - name: "Official References"
    estimatedTokens: 20
    keywords: [official, references]
tags: [commands, refactoring, code-smells, technical-debt, extract-method, safe-refactoring]
---

# Refactoring Patterns

Reference patterns for the `/improve` command. Covers safe refactoring techniques, code smell identification, and technical debt management.

## Safe Refactoring Techniques

### Extract Method
- **When**: Long method with identifiable sub-tasks
- **Risk**: Low - preserves behavior, improves readability
- **Steps**: Identify code block, extract to new method, replace with call

### Rename (Variable, Method, Class)
- **When**: Name doesn't convey intent or is misleading
- **Risk**: Low-Medium - may affect public API
- **Steps**: Find all references, rename consistently, update docs

### Extract Class/Module
- **When**: Class has too many responsibilities
- **Risk**: Medium - changes dependencies and imports
- **Steps**: Identify separate responsibility, extract to new class, delegate

### Inline Method
- **When**: Method body is as clear as the name, or method is only called once
- **Risk**: Low - simplifies code
- **Steps**: Replace call with body, remove method

### Replace Conditional with Polymorphism
- **When**: Switch/if-else chains selecting behavior based on type
- **Risk**: Medium - architectural change
- **Steps**: Create interface, implement per type, replace conditional

### Introduce Parameter Object
- **When**: Method has 3+ related parameters
- **Risk**: Low-Medium - changes method signature
- **Steps**: Create data class, replace parameters, update callers

### Move Method/Field
- **When**: Method uses more data from another class than its own
- **Risk**: Medium - changes class boundaries
- **Steps**: Move to target class, update references

## Code Smell Identification

### Complexity Smells
| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Long Method | >20 lines or multiple indent levels | Extract Method |
| Large Class | >300 lines or >10 methods | Extract Class |
| Long Parameter List | >3 parameters | Introduce Parameter Object |
| Deep Nesting | >3 levels of indentation | Extract Method, Guard Clauses |
| Complex Conditional | Compound boolean expressions | Extract to named boolean method |

### Duplication Smells
| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Duplicated Code | Similar code blocks in 2+ places | Extract Method/Class |
| Parallel Inheritance | Subclass in one hierarchy requires subclass in another | Merge hierarchies |
| Feature Envy | Method accessing another object's data heavily | Move Method |

### Coupling Smells
| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Inappropriate Intimacy | Classes accessing each other's internals | Move Method, Extract Class |
| Middle Man | Class delegating all work | Inline Class |
| Shotgun Surgery | One change requires editing many classes | Move Method, Inline Class |
| Divergent Change | One class changed for multiple reasons | Extract Class |

## Auto-Fix vs Approval-Required

### Auto-Fix (Safe to Apply Automatically)
- Import organization and cleanup
- Unused variable/import removal
- Whitespace and formatting fixes
- Simple type annotation additions
- Consistent naming convention application (within file)

### Approval Required (Prompt User First)
- Architectural changes (class extraction, module reorganization)
- Logic refactoring (algorithm changes, control flow changes)
- Public API changes (method signatures, return types)
- Removing functionality (even if seemingly unused)
- Changes affecting multiple files
- Database schema changes

### Never Auto-Apply
- Removing code used by external consumers
- Changing error handling behavior
- Modifying security-related code
- Altering test behavior

## Technical Debt Tracking

### Debt Classification
| Type | Example | Priority |
|------|---------|----------|
| **Design Debt** | Missing abstraction, tight coupling | High (compounds quickly) |
| **Code Debt** | Duplicated code, complex methods | Medium (maintenance cost) |
| **Test Debt** | Missing tests, flaky tests | High (blocks confidence) |
| **Documentation Debt** | Outdated docs, missing API docs | Low (unless onboarding) |
| **Infrastructure Debt** | Old dependencies, missing CI | Medium (security risk) |

### Improvement Prioritization
1. **Security issues** - Fix immediately
2. **Bug-prone code** - Fix in current sprint
3. **Frequently modified code** - Improve next time it's touched
4. **Rarely touched code** - Schedule for dedicated refactoring

## Pre-Improvement Checklist

Before applying improvements:
- [ ] Tests exist for code being changed (or write them first)
- [ ] All existing tests pass
- [ ] Changes are reversible (git commit before refactoring)
- [ ] Impact radius is understood (who calls this code?)
- [ ] No public API changes without user approval

## Skill Integration

Before improving, analyze first:
- **Python code**: `skill:python-code-review` for comprehensive review
- **.NET code**: `skill:dotnet-code-review` for .NET-specific issues
- **Angular code**: `skill:angular-code-review` for framework patterns

## Official References

- [Refactoring Catalog](https://refactoring.com/catalog/)
- [Code Smells](https://refactoring.guru/refactoring/smells)
- [Martin Fowler - Refactoring](https://martinfowler.com/books/refactoring.html)
