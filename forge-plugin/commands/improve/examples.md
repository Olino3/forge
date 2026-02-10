# /improve Examples

## Example 1: Code Quality Enhancement

```
/improve src/services --type quality --safe
```

**What happens**:
1. Reads all files in `src/services/`
2. Delegates to code review skill for comprehensive analysis
3. Identifies improvements: unused imports, naming inconsistencies, dead code
4. `--safe` flag: Only applies auto-fixable changes
5. Lists recommended changes requiring approval
6. Saves improvement report to `/claudedocs/improve_services_20260209.md`

## Example 2: Performance Optimization

```
/improve src/api/queries.py --type performance
```

**What happens**:
1. Reads the query file and related modules
2. Loads performance-related context
3. Identifies: N+1 queries, missing pagination, blocking I/O
4. Auto-fixes simple issues (import cleanup)
5. Prompts for approval on query restructuring
6. Validates changes don't break existing tests

## Example 3: Security Hardening

```
/improve src/auth --type security
```

**What happens**:
1. Loads security context and OWASP patterns
2. Delegates to code review skill with security focus
3. Identifies: Missing input validation, weak token handling
4. Applies safe fixes (adding validation)
5. Prompts for approval on authentication flow changes
6. Generates detailed security improvement report

## Example 4: Preview Mode

```
/improve src/models --type maintainability --preview
```

**What happens**:
1. Analyzes models directory for maintainability issues
2. Identifies: Long classes, code duplication, poor naming
3. `--preview`: Shows ALL proposed changes without applying any
4. Groups changes by risk level (auto-fix vs approval needed)
5. User can then re-run without `--preview` to apply

## Example 5: Full Directory Improvement

```
/improve src/ --type quality
```

**What happens**:
1. Scans entire source directory
2. Loads project memory for known issues and conventions
3. Applies auto-fixable improvements across all files
4. Skips known issues flagged in memory
5. Runs existing tests to verify no regressions
6. Reports all changes and remaining recommendations

## Example 6: Targeted Refactoring

```
/improve src/utils/helpers.py --type maintainability --safe
```

**What happens**:
1. Reads the specific file
2. Identifies: Long functions, duplicated logic, unclear naming
3. Auto-fixes: Import organization, unused variables
4. Lists recommended refactorings: Extract Method, Rename
5. Verifies test coverage exists for the file
6. Reports what was changed and what needs manual attention
