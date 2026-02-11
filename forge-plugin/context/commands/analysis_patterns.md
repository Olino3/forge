---
id: "commands/analysis_patterns"
domain: commands
title: "Analysis Patterns"
type: pattern
estimatedTokens: 700
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Analysis Methodologies"
    estimatedTokens: 57
    keywords: [analysis, methodologies]
  - name: "Severity Classification"
    estimatedTokens: 94
    keywords: [severity, classification]
  - name: "Multi-Language Analysis Strategy"
    estimatedTokens: 69
    keywords: [multi-language, analysis, strategy]
  - name: "Analysis Domains"
    estimatedTokens: 78
    keywords: [analysis, domains]
  - name: "Reporting Format"
    estimatedTokens: 39
    keywords: [reporting, format]
  - name: "Skill Integration"
    estimatedTokens: 30
    keywords: [skill, integration]
  - name: "Official References"
    estimatedTokens: 20
    keywords: [official, references]
tags: [commands, analysis, static-analysis, severity, multi-language, code-quality]
---

# Analysis Patterns

Reference patterns for the `/analyze` command. Covers static analysis methodologies, severity classification, and multi-language analysis strategies.

## Analysis Methodologies

### Static Analysis
- **Pattern matching**: Identify known anti-patterns, code smells, and vulnerabilities
- **Control flow analysis**: Trace execution paths for unreachable code, infinite loops
- **Data flow analysis**: Track variable usage for uninitialized reads, unused writes
- **Dependency analysis**: Map import graphs for circular dependencies, unused imports

### Heuristic Evaluation
- **Complexity assessment**: Cyclomatic complexity, cognitive complexity, nesting depth
- **Naming evaluation**: Consistency, clarity, convention adherence
- **Structure assessment**: File organization, module boundaries, separation of concerns

## Severity Classification

| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Security vulnerability, data loss risk, crash in production | Fix immediately |
| **High** | Performance bottleneck, logic error, significant code smell | Fix before merge |
| **Medium** | Maintainability concern, minor code smell, missing validation | Fix in next sprint |
| **Low** | Style inconsistency, minor naming issue, documentation gap | Fix when convenient |
| **Info** | Suggestion, optimization opportunity, best practice note | Consider for future |

### Severity Decision Guide
- **Could this cause data loss or security breach?** → Critical
- **Could this cause incorrect behavior?** → High
- **Does this make code harder to maintain?** → Medium
- **Is this a style or convention issue?** → Low

## Multi-Language Analysis Strategy

### Language Detection
1. Check file extensions (`.py`, `.cs`, `.ts`, `.js`, `.go`, `.java`)
2. Check configuration files (`pyproject.toml`, `*.csproj`, `package.json`, `go.mod`)
3. Check framework markers (Django `manage.py`, Angular `angular.json`, .NET `Program.cs`)

### Per-Language Focus Areas

**Python**: PEP8 compliance, type hints, exception handling, mutable defaults, import organization
**C#/.NET**: Async/await patterns, null safety, LINQ usage, DI patterns, EF queries
**TypeScript/Angular**: Type safety, RxJS patterns, change detection, memory leaks
**JavaScript**: Prototype pollution, callback hell, promise handling, scope issues
**Go**: Error handling, goroutine leaks, interface compliance, context propagation
**Java**: Null handling, resource management, generics usage, thread safety

## Analysis Domains

### Code Quality
- Complexity metrics (cyclomatic, cognitive)
- Code duplication detection
- Dead code identification
- Naming consistency
- File organization

### Security
- OWASP Top 10 vulnerability scanning
- Input validation completeness
- Authentication/authorization patterns
- Secrets exposure detection
- SQL injection, XSS, CSRF patterns

See: `../security/security_guidelines.md` for detailed security patterns

### Performance
- Algorithm complexity (O notation)
- Database query patterns (N+1, missing indexes)
- Memory management (leaks, large allocations)
- I/O patterns (blocking, buffering)
- Caching opportunities

### Architecture
- SOLID principle adherence
- Dependency direction (clean architecture)
- Module cohesion and coupling
- API design consistency
- Error handling strategy

## Reporting Format

### Finding Structure
```
**[SEVERITY]** Brief description
- **Location**: file:line
- **Issue**: What's wrong
- **Impact**: Why it matters
- **Recommendation**: How to fix
```

### Summary Metrics
- Total findings by severity
- Files analyzed vs files with issues
- Top recurring patterns
- Comparison with previous analysis (if memory exists)

## Skill Integration

When deep analysis is needed, delegate to specialized skills:
- **Python code**: `skill:python-code-review` for comprehensive Python analysis
- **.NET code**: `skill:dotnet-code-review` for .NET-specific patterns
- **Angular code**: `skill:angular-code-review` for Angular-specific patterns
- **Security focus**: Load `../security/` context for OWASP patterns

## Official References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SonarQube Rules](https://rules.sonarsource.com/)
- [CWE Database](https://cwe.mitre.org/)
