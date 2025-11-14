---
name: python-code-review
description: Deep Python code review focusing on production quality, security vulnerabilities, performance bottlenecks, architectural issues, and subtle bugs. Analyzes correctness, efficiency, scalability, and production readiness. Use for critical code review, security audits, performance optimization, and production deployment validation. Supports Django, Flask, FastAPI, pandas, and ML frameworks.
---

# Python Code Review Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 4-step workflow outlined in this document MUST be followed in exact order for EVERY code review. Skipping steps or deviating from the procedure will result in incomplete and unreliable reviews. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Review scenarios with before/after examples
- **context/**: `security_guidelines.md`, `owasp_python.md`
- **memory/**: `context_detection.md`, `common_issues.md`, `{framework}_patterns.md`
- **templates/**: `report_template.md`, `inline_comment_template.md`

## Review Focus Areas

Deep reviews evaluate 8 critical dimensions:

1. **Production Quality**: Correctness, edge cases, error recovery, resilience
2. **Deep Bugs**: Race conditions, memory leaks, resource exhaustion, subtle logic errors
3. **Security**: Injection flaws, auth bypasses, insecure deserialization, data exposure
4. **Performance**: Algorithmic complexity, N+1 queries, memory inefficiency, I/O blocking
5. **Architecture**: Tight coupling, missing abstractions, SOLID violations, circular deps
6. **Reliability**: Transaction safety, error handling, resource leaks, idempotency
7. **Scalability**: Concurrency issues, connection pooling, pagination, unbounded consumption
8. **Testing**: Missing critical tests, inadequate edge case coverage

**Note**: Focus on substantive issues requiring human judgment, not style/formatting details.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Context Detection (REQUIRED)

**YOU MUST:**
1. Analyze codebase structure and imports
2. **READ** `memory/context_detection.md` to identify framework
3. Determine which framework-specific patterns file(s) to load
4. Ask clarifying questions in Socratic format:
   - What is the code's purpose?
   - Specific concerns to focus on?
   - Deployment environment?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 2: Read Pattern Files (REQUIRED)

**YOU MUST read these files based on context**:

1. **ALWAYS**: `memory/common_issues.md` (universal anti-patterns and deep bugs)
2. **If Django detected**: `memory/django_patterns.md`
3. **If Flask detected**: `memory/flask_patterns.md`
4. **If FastAPI detected**: `memory/fastapi_patterns.md`
5. **If data science detected**: `memory/datascience_patterns.md`
6. **If ML detected**: `memory/ml_patterns.md`
7. **For security reviews**: `context/security_guidelines.md` AND `context/owasp_python.md`

**Progressive loading**: Only read framework files when detected. Don't load all upfront.

**DO NOT SKIP PATTERN FILE READING**

### ⚠️ STEP 3: Deep Manual Review (REQUIRED)

**YOU MUST examine code for ALL categories below**:

**Production Readiness**: Edge cases, input validation, error recovery, resource cleanup, timeouts
**Deep Bugs**: Race conditions, memory leaks, off-by-one errors, unhandled exceptions, state corruption, infinite loops, integer overflow, timezone issues
**Architecture**: Tight coupling, missing abstractions, SOLID violations, global state, circular dependencies
**Security**: SQL/NoSQL/Command injection, auth bypasses, insecure deserialization, SSRF, XXE, crypto weaknesses, data exposure, missing rate limiting
**Performance**: O(n²) complexity, N+1 queries, memory leaks, blocking I/O in async, missing indexes, inefficient data structures, cache stampede
**Scalability**: Connection pool exhaustion, lock contention, deadlocks, missing pagination, unbounded consumption
**Reliability**: Transaction boundaries, data races, resource leaks, missing idempotency

**DO NOT SKIP ANY CATEGORY**

### ⚠️ STEP 4: Generate Output (REQUIRED)

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

---

## Compliance Checklist

Before completing ANY review, verify:
- [ ] Step 1: Context detected and pattern files identified
- [ ] Step 2: All relevant pattern files read
- [ ] Step 3: Manual review completed for ALL categories
- [ ] Step 4: User preference obtained for output format and all recommendations include severity, category, description, fix, and reference

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

- v1.1.0 (2025-11-13): Removed automated analysis and linting/formatting tools
- v1.0.0 (2025-11-13): Initial release
