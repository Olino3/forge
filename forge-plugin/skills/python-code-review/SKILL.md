---
name: python-code-review
description: Deep Python code review of changed files using git diff analysis. Focuses on production quality, security vulnerabilities, performance bottlenecks, architectural issues, and subtle bugs in code changes. Analyzes correctness, efficiency, scalability, and production readiness of modifications. Use for pull request reviews, commit reviews, security audits of changes, and pre-deployment validation. Supports Django, Flask, FastAPI, pandas, and ML frameworks.
---

# Python Code Review Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY code review. Skipping steps or deviating from the procedure will result in incomplete and unreliable reviews. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Review scenarios with before/after examples
- **../../context/python/**: Framework patterns and detection logic
  - `context_detection.md`, `common_issues.md`, `{framework}_patterns.md`
- **../../context/security/**: Security guidelines and OWASP references
  - `security_guidelines.md`, `owasp_python.md`
- **../../memory/skills/python-code-review/**: Project-specific memory storage
  - `{project-name}/`: Per-project learned patterns and context
- **templates/**: `report_template.md`, `inline_comment_template.md`

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
   - **READ** `../../memory/skills/python-code-review/index.md` to understand the memory system
   - Check `../../memory/skills/python-code-review/{project-name}/` for existing project memory
   - If memory exists, read the memory files to understand previously learned patterns, frameworks, and project-specific context
   - If no memory exists, you will create it later in this process
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - **READ** `../../context/index.md` for overview of available context files
   - **READ** `../../context/python/index.md` to understand Python context files and when to use each
   - **READ** `../../context/security/index.md` to understand security context files
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

**Use the index files from Step 2 to determine which context files to load:**

1. **ALWAYS**: `../../context/python/common_issues.md` (universal anti-patterns and deep bugs)
2. **Based on framework detected** (refer to `../../context/python/index.md` for guidance):
   - **If Django detected**: Load `django_patterns.md`
   - **If Flask detected**: Load `flask_patterns.md`
   - **If FastAPI detected**: Load `fastapi_patterns.md`
   - **If data science detected**: Load `datascience_patterns.md`
   - **If ML detected**: Load `ml_patterns.md`
3. **For security-sensitive code** (refer to `../../context/security/index.md` for when to load):
   - Auth/authorization code: Load both security files
   - User input handling: Load `security_guidelines.md`
   - Database queries: Load `security_guidelines.md`
   - File operations: Load `security_guidelines.md`
   - Comprehensive audit: Load both `security_guidelines.md` AND `owasp_python.md`

**Progressive loading**: Only read files relevant to the detected framework and code type. The index files provide guidance on when each file is needed.

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

Create or update files in `../../memory/skills/python-code-review/{project-name}/`:

1. **project_overview.md**: Framework, architecture patterns, deployment info
2. **common_patterns.md**: Project-specific coding patterns and conventions discovered
3. **known_issues.md**: Recurring issues or anti-patterns found in this project
4. **review_history.md**: Summary of reviews performed with dates and key findings

This memory will be consulted in future reviews to provide context-aware analysis.

---

## Compliance Checklist

Before completing ANY review, verify:
- [ ] Step 1: Git diff analyzed using `get-git-diff` skill and changed Python files identified
- [ ] Step 2: Project memory checked in `../../memory/skills/python-code-review/{project-name}/` and context detected
- [ ] Step 3: All relevant pattern files read from `../../context/python/` and `../../context/security/`
- [ ] Step 4: Manual review completed for ALL categories on changed code only
- [ ] Step 5: Output generated with all required fields AND project memory updated

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

- v2.1.0 (2025-11-14): Refactored to use centralized context and project-specific memory system
  - Context files moved to `forge-plugin/context/python/` and `forge-plugin/context/security/`
  - Project memory stored in `forge-plugin/memory/skills/python-code-review/{project-name}/`
  - Added project memory loading and persistence in workflow
- v2.0.0 (2025-11-13): Changed to diff-based review using `get-git-diff` skill - reviews only changed code
- v1.1.0 (2025-11-13): Removed automated analysis and linting/formatting tools
- v1.0.0 (2025-11-13): Initial release
