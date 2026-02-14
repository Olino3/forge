---
name: python-code-review
## description: Deep Python code review of changed files using git diff analysis. Focuses on production quality, security vulnerabilities, performance bottlenecks, architectural issues, and subtle bugs in code changes. Analyzes correctness, efficiency, scalability, and production readiness of modifications. Use for pull request reviews, commit reviews, security audits of changes, and pre-deployment validation. Supports Django, Flask, FastAPI, pandas, and ML frameworks.

# Python Code Review Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY code review. Skipping steps or deviating from the procedure will result in incomplete and unreliable reviews. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Review scenarios with before/after examples
- **Context**: Python and security domain context loaded via `contextProvider.getDomainIndex("python")` and `contextProvider.getDomainIndex("security")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
  - `context_detection.md`, `common_issues.md`, `{framework}_patterns.md`
  - `security_guidelines.md`, `owasp_python.md`
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("python-code-review", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **templates/**: `report_template.md`, `inline_comment_template.md`


## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)

## Review Focus Areas

Deep reviews evaluate 8 critical dimensions **in the changed code**:

1. **Production Quality**: Correctness, edge cases, error recovery, resilience
2. **Deep Bugs**: Race conditions, memory leaks, resource exhaustion, subtle logic errors
3. **Security**: Injection flaws, auth bypasses, insecure deserialization, data exposure
4. **Performance**: Algorithmic complexity, N+1 queries, memory inefficiency, I/O blocking
5. **Architecture**: Tight coupling, missing abstractions, SOLID violations, circular deps
6. **Reliability**: Transaction safety, error handling, resource leaks, idempotency
7. **Scalability**: Concurrency issues, connection pooling, pagination, unbounded consumption
8. **Testing**: Missing critical tests, inadequate edge case coverage

**Note**: Focus on substantive issues requiring human judgment, not style/formatting details. Reviews are performed on changed code only, using the `get-git-diff` skill to identify modifications.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Changed Files via Git Diff (REQUIRED)

**YOU MUST:**
1. **Invoke the `get-git-diff` skill** to identify changed Python files
2. Ask clarifying questions to determine comparison scope:
   - Which commits/branches to compare? (e.g., `HEAD^ vs HEAD`, `main vs feature-branch`)
   - If not specified, default to comparing current changes against the default branch
   - Use the diff output to extract the list of modified Python files (`.py` extension)
3. If no Python files were changed, inform the user and exit gracefully
4. Focus subsequent review ONLY on the files identified in the diff

**DO NOT PROCEED WITHOUT GIT DIFF ANALYSIS**

### ⚠️ STEP 2: Load Project Memory & Context Detection (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("python-code-review", "{project-name}")` to load project-specific patterns
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for schema analysis results, test findings, or other skill insights
   - If memory exists: Review previously learned patterns, frameworks, and project-specific context
   - If no memory exists (empty result): Note this is first review, you will create memory later
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("python")` to understand Python context files and when to use each
   - Use `contextProvider.getDomainIndex("security")` to understand security context files

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.
3. Analyze changed files' structure and imports
4. Use `context_detection.md` to identify framework (as guided by the python index)
5. Determine which specific context files to load based on the indexes (don't load all files)
6. Ask clarifying questions in Socratic format:
   - What is the purpose of these changes?
   - Specific concerns to focus on?
   - Deployment environment?
   - Any project-specific conventions or patterns to be aware of?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Read Relevant Context Files (REQUIRED)

**YOU MUST use the indexes to load only relevant files**:

**Use the domain indexes from Step 2 to determine which context files to load:**

1. **ALWAYS**: Use `contextProvider.getAlwaysLoadFiles("python")` to load universal anti-patterns and deep bugs (e.g., `common_issues.md`)
2. **Based on framework detected**: Use `contextProvider.getConditionalContext("python", detection)` to load framework-specific patterns:
   - **If Django detected**: Loads `django_patterns.md`
   - **If Flask detected**: Loads `flask_patterns.md`
   - **If FastAPI detected**: Loads `fastapi_patterns.md`
   - **If data science detected**: Loads `datascience_patterns.md`
   - **If ML detected**: Loads `ml_patterns.md`
3. **For security-sensitive code**: Use `contextProvider.getCrossDomainContext("python", triggers)` where triggers include detected security concerns:
   - Auth/authorization code: Loads both security files
   - User input handling: Loads `security_guidelines.md`
   - Database queries: Loads `security_guidelines.md`
   - File operations: Loads `security_guidelines.md`
   - Comprehensive audit: Loads both `security_guidelines.md` AND `owasp_python.md`

**Progressive loading**: Only load files relevant to the detected framework and code type. The ContextProvider respects the 4-6 file token budget automatically.

**DO NOT SKIP LOADING RELEVANT CONTEXT FILES**

### ⚠️ STEP 4: Deep Manual Review of Changed Code (REQUIRED)

**YOU MUST examine ONLY the changed code for ALL categories below**:

**Important**: While reviewing changed lines, consider the surrounding context to understand:
- How changes interact with existing code
- Whether changes introduce regressions
- Impact on callers and dependent code
- Whether the change addresses the root cause or masks symptoms

**Review Categories**:

**Production Readiness**: Edge cases, input validation, error recovery, resource cleanup, timeouts
**Deep Bugs**: Race conditions, memory leaks, off-by-one errors, unhandled exceptions, state corruption, infinite loops, integer overflow, timezone issues
**Architecture**: Tight coupling, missing abstractions, SOLID violations, global state, circular dependencies
**Security**: SQL/NoSQL/Command injection, auth bypasses, insecure deserialization, SSRF, XXE, crypto weaknesses, data exposure, missing rate limiting
**Performance**: O(n²) complexity, N+1 queries, memory leaks, blocking I/O in async, missing indexes, inefficient data structures, cache stampede
**Scalability**: Connection pool exhaustion, lock contention, deadlocks, missing pagination, unbounded consumption
**Reliability**: Transaction boundaries, data races, resource leaks, missing idempotency

**DO NOT SKIP ANY CATEGORY**

### ⚠️ STEP 5: Generate Output & Update Project Memory (REQUIRED)

**YOU MUST ask user for preferred output format**:

- **Option A**: Structured report (`templates/report_template.md`) → executive summary, categorized findings, action items → output to `claudedocs/`
- **Option B**: Inline comments (`templates/inline_comment_template.md`) → file:line feedback, PR-style
- **Option C (Default)**: Both formats

**DO NOT CHOOSE FORMAT WITHOUT USER INPUT**

**For EVERY issue in the output, YOU MUST provide**:
1. **Severity**: Critical / Important / Minor
2. **Category**: Security / Performance / Code Quality / Architecture / Reliability
3. **Description**: What is wrong and why it matters
4. **Fix**: Concrete code example with improvement
5. **Reference**: Link to PEP, OWASP, or framework docs
6. **File:line**: Exact location (e.g., `auth.py:142`)

**Format guidelines**:
- Explain WHY (not just what)
- Show HOW to fix with examples
- Be specific with file:line references
- Be balanced (acknowledge good patterns)
- Educate, don't criticize

**DO NOT PROVIDE INCOMPLETE RECOMMENDATIONS**

**After completing the review, UPDATE PROJECT MEMORY**:

Use `memoryStore.update("python-code-review", "{project-name}", ...)` to create or update memory files:

1. **project_overview**: Framework, architecture patterns, deployment info
2. **common_patterns**: Project-specific coding patterns and conventions discovered
3. **known_issues**: Recurring issues or anti-patterns found in this project
4. **review_history**: Summary of reviews performed with dates and key findings

Timestamps and staleness tracking are managed automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

---

## Compliance Checklist

Before completing ANY review, verify:
- [ ] Step 1: Git diff analyzed using `get-git-diff` skill and changed Python files identified
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()` and context detected via `contextProvider`
- [ ] Step 3: All relevant context files loaded via `contextProvider.getAlwaysLoadFiles()`, `getConditionalContext()`, and `getCrossDomainContext()`
- [ ] Step 4: Manual review completed for ALL categories on changed code only
- [ ] Step 5: Output generated with all required fields AND project memory updated via `memoryStore.update()`

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE REVIEW**

## Further Reading

Refer to the official documentation:
- **Python Standards**:
  - Python PEPs: https://peps.python.org/
  - OWASP Python Security: https://owasp.org/www-project-python-security/
- **Frameworks**:
  - Django, Flask, FastAPI official documentation
- **Best Practices**:
  - Real Python: https://realpython.com/

## Version History

- v2.2.0 (2026-02-10): Migrated to interface-based context and memory access
  - Replaced hardcoded context paths with ContextProvider interface calls
  - Replaced hardcoded memory paths with MemoryStore interface calls
  - Added references to interface documentation
- v2.1.0 (2025-11-14): Refactored to use centralized context and project-specific memory system
  - Context files moved to `forge-plugin/context/python/` and `forge-plugin/context/security/`
  - Project memory stored in `forge-plugin/memory/skills/python-code-review/{project-name}/`
  - Added project memory loading and persistence in workflow
- v2.0.0 (2025-11-13): Changed to diff-based review using `get-git-diff` skill - reviews only changed code
- v1.1.0 (2025-11-13): Removed automated analysis and linting/formatting tools
- v1.0.0 (2025-11-13): Initial release
