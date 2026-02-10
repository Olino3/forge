# /analyze Examples

## Example 1: Quick Project Analysis

```
/analyze
```

**What happens**:
1. Detects project language from config files (e.g., `pyproject.toml` → Python)
2. Loads Python context and analysis patterns
3. Scans project structure for quality, security, and architecture issues
4. Generates prioritized findings report
5. Saves to `/claudedocs/analyze_project_20260209.md`

## Example 2: Focused Security Assessment

```
/analyze src/auth --focus security --depth deep
```

**What happens**:
1. Scopes analysis to `src/auth` directory
2. Loads security context (`security_guidelines.md`, `owasp_python.md`)
3. Loads past analysis memory for the project
4. Performs deep security analysis of auth components
5. Delegates to `skill:python-code-review` for comprehensive security review
6. Generates detailed vulnerability report with remediation guidance
7. Saves to `/claudedocs/analyze_auth_20260209.md`
8. Updates project memory with security findings

## Example 3: Performance Analysis

```
/analyze src/api --focus performance
```

**What happens**:
1. Scopes to API directory
2. Identifies database queries, algorithm patterns, I/O operations
3. Checks for N+1 queries, missing indexes, blocking calls
4. Classifies performance issues by severity and impact
5. Generates optimization recommendations

## Example 4: Multi-Language Project

```
/analyze --depth deep
```

**What happens**:
1. Detects multiple languages (e.g., Python backend + Angular frontend)
2. Loads context for both Python and Angular domains
3. Delegates to `skill:python-code-review` for backend analysis
4. Delegates to `skill:angular-code-review` for frontend analysis
5. Aggregates findings into unified report with per-language sections
6. Identifies cross-cutting concerns (API contracts, security)

## Example 5: Quick Quality Check

```
/analyze src/components --focus quality --depth quick
```

**What happens**:
1. Scopes to components directory
2. Quick scan for code smells: long methods, duplication, complexity
3. Generates brief quality assessment without deep skill delegation
4. Identifies top 5 improvement opportunities
5. Recommends `/improve` for applying fixes

## Example 6: Architecture Review

```
/analyze --focus architecture --depth deep
```

**What happens**:
1. Analyzes project structure, module dependencies, import patterns
2. Evaluates SOLID principle adherence
3. Maps dependency direction (clean architecture compliance)
4. Identifies tight coupling and circular dependencies
5. Generates architecture assessment with improvement roadmap
