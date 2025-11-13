---
name: python-code-review
description: Deep Python code review focusing on production quality, security vulnerabilities, performance bottlenecks, architectural issues, and subtle bugs. Analyzes correctness, efficiency, scalability, and production readiness. Use for critical code review, security audits, performance optimization, and production deployment validation. Supports Django, Flask, FastAPI, pandas, and ML frameworks.
---

# Python Code Review Expert

## File Structure

This skill is organized as follows:

- **SKILL.md** (this file): Main instructions and workflow
- **examples.md**: Review scenarios with before/after examples
- **context/**: Standards and reference material
  - `pep8_standards.md`: Python style guide reference (defer to automated tools)
  - `security_guidelines.md`: Security best practices and input validation
  - `owasp_python.md`: OWASP Top 10 vulnerabilities for Python
- **memory/**: Framework-specific patterns and common issues
  - `context_detection.md`: How to identify frameworks and select patterns
  - `common_issues.md`: Universal Python anti-patterns and deep bugs
  - `django_patterns.md`: Django-specific review criteria
  - `flask_patterns.md`: Flask best practices
  - `fastapi_patterns.md`: FastAPI async patterns
  - `datascience_patterns.md`: Pandas/numpy optimization patterns
  - `ml_patterns.md`: PyTorch/TensorFlow/sklearn patterns
- **scripts/**: Automated analysis tools
  - `review_runner.py`: Orchestrates security, complexity, and performance analysis
  - `parse_results.py`: Aggregates and formats tool outputs
  - `performance_profiler.py`: Performance profiling and benchmarking
  - `requirements.txt`: Required Python packages
- **templates/**: Output format templates
  - `report_template.md`: Structured review report
  - `inline_comment_template.md`: PR-style inline comments

## Required Reading

Read files progressively based on the review context:

1. **Always start with**: `memory/context_detection.md` to identify the framework/context
2. **For all reviews**: `memory/common_issues.md` for universal anti-patterns and deep bugs
3. **For security reviews**: `context/security_guidelines.md` and `context/owasp_python.md`
4. **For framework-specific code**: Read the corresponding `memory/*_patterns.md` file
5. **For examples**: Refer to `examples.md` when demonstrating improvements

**Note on Style**: PEP 8 style checking should be handled by automated tools (black, pylint, flake8). Focus manual review on substantive issues that tools cannot catch.

**Progressive loading strategy**: Only read framework-specific files when that framework is detected. Don't load all patterns upfront.

## Design Requirements

Conduct deep Python code reviews that evaluate:

1. **Production Quality**: Correctness, edge case handling, error recovery, resilience
2. **Deep Bugs**: Race conditions, memory leaks, resource exhaustion, subtle logic errors
3. **Security**: Critical vulnerabilities, injection flaws, authentication bypasses, data exposure
4. **Performance**: Algorithmic complexity, memory efficiency, database optimization, scalability bottlenecks
5. **Architecture**: Design flaws, tight coupling, missing abstractions, violation of SOLID principles
6. **Reliability**: Error handling, failure modes, data consistency, transaction safety
7. **Scalability**: Concurrency issues, database contention, caching strategies, load handling
8. **Testing**: Missing critical tests, inadequate edge case coverage, test quality issues

**Note**: Style and formatting issues (PEP 8, naming conventions, docstrings) should be handled by automated tools like black, pylint, flake8, mypy. Focus manual review on substantive issues that require human judgment and domain expertise.

## Prompting Guidelines

When conducting a code review:

1. **Ask clarifying questions** before starting:
   - What is the purpose of this code?
   - Are there specific concerns to focus on?
   - What is the deployment environment?
   - Are there existing style guidelines or linting configs?

2. **Provide actionable feedback**:
   - Explain WHY something is an issue
   - Show HOW to fix it with code examples
   - Prioritize issues (critical, important, minor)
   - Link to relevant documentation or PEPs

3. **Be balanced**:
   - Acknowledge good patterns and well-written code
   - Don't nitpick formatting if linters handle it
   - Consider the context (prototype vs production)
   - Suggest improvements, don't demand perfection

4. **Be specific**:
   - Reference exact file paths and line numbers (file.py:123)
   - Quote the problematic code
   - Provide concrete examples of fixes

## Instructions

### Step 1: Context Detection

1. Analyze the codebase structure and imports
2. Read `memory/context_detection.md` to identify the framework/context
3. Determine which framework-specific patterns file(s) to load

### Step 2: Run Automated Analysis

1. Use `scripts/review_runner.py` to run automated tools:
   - **bandit**: Security vulnerability scanning (critical)
   - **mypy**: Type checking and type safety
   - **radon**: Cyclomatic complexity and maintainability analysis
   - **vulture**: Dead code detection
   - **safety**: Dependency vulnerability check

2. Use `scripts/performance_profiler.py` for performance analysis:
   - **cProfile**: CPU profiling and hotspot detection
   - **memory_profiler**: Memory usage analysis
   - **py-spy**: Production-safe profiling
   - **locust/pytest-benchmark**: Load testing and benchmarking

3. Use `scripts/parse_results.py` to aggregate results

**Note**: Style tools (black, pylint for formatting) are assumed to run in CI/CD. Manual review focuses on what automated tools cannot catch.

### Step 3: Read Relevant Pattern Files

Based on detected context, read:
- `memory/common_issues.md` (always - deep bugs and anti-patterns)
- Relevant framework file from `memory/` (if detected)
- `context/security_guidelines.md` and `context/owasp_python.md` (for security reviews)

### Step 4: Deep Manual Code Review

Examine the code for substantive issues:

**Production Readiness**:
- Edge case handling and input validation
- Error recovery and graceful degradation
- Resource cleanup and connection management
- Timeout handling and circuit breakers

**Deep Bugs**:
- Race conditions and threading issues
- Memory leaks and resource exhaustion
- Off-by-one errors and boundary conditions
- Unhandled exception paths
- State corruption in concurrent operations
- Infinite loops or recursion without base case
- Integer overflow or underflow
- Timezone and datetime handling issues

**Architecture**:
- Tight coupling and lack of separation of concerns
- Missing abstraction layers
- Violation of SOLID principles
- Global state and mutable singletons
- Circular dependencies

**Security**:
- SQL/NoSQL/Command injection vulnerabilities
- Authentication and authorization bypasses
- Insecure deserialization (pickle)
- SSRF and XXE vulnerabilities
- Cryptographic weaknesses
- Sensitive data exposure
- Missing rate limiting and DoS protection

**Performance**:
- Algorithmic complexity issues (O(n²) where O(n) possible)
- N+1 query problems in ORMs
- Memory inefficiency and leaks
- Blocking I/O in async code
- Missing indexes and query optimization
- Inefficient data structures
- Cache stampede and thundering herd

**Scalability**:
- Database connection pool exhaustion
- Lock contention and deadlocks
- Missing pagination on large datasets
- Unbounded resource consumption
- State synchronization across instances

**Reliability**:
- Missing transaction boundaries
- Data race conditions
- Improper error handling and recovery
- Resource leaks (files, connections, memory)
- Missing idempotency in critical operations

### Step 5: Generate Output

Choose output format based on user preference:

**Option A: Structured Report** (use `templates/report_template.md`):
- Executive summary with metrics
- Categorized findings (critical, important, minor)
- Recommendations with code examples
- Action items prioritized

**Option B: Inline Comments** (use `templates/inline_comment_template.md`):
- File:line specific feedback
- GitHub PR comment style
- Each comment includes severity and fix suggestion

**Option C: Both formats** (default):
- Start with inline comments for specific issues
- Conclude with high-level report summarizing findings

### Step 6: Provide Recommendations

For each issue found:
1. **Severity**: Critical / Important / Minor
2. **Category**: Security / Performance / Code Quality / Style
3. **Description**: What is wrong and why it matters
4. **Fix**: Concrete code example showing the improvement
5. **Reference**: Link to PEP, OWASP, or framework documentation

## Best Practices

1. **Framework awareness**: Apply framework-specific best practices, not generic advice
2. **Tool integration**: Leverage automated tools for objective metrics, save manual review for nuanced issues
3. **Context matters**: Production code needs higher standards than prototypes
4. **Positive reinforcement**: Highlight good patterns to encourage best practices
5. **Educate, don't criticize**: Explain the reasoning behind recommendations
6. **Prioritize ruthlessly**: Focus on critical and important issues first
7. **Suggest incremental improvements**: Don't demand perfection immediately
8. **Update your knowledge**: Python and frameworks evolve; reference current best practices
9. **Check tool configurations**: Respect existing .pylintrc, pyproject.toml, or setup.cfg
10. **Consider team conventions**: Local style guides override generic recommendations

## Additional Notes

### Tool Installation

If review tools are not installed, recommend:

```bash
pip install pylint black mypy bandit safety
```

Or use the provided requirements file:

```bash
pip install -r scripts/requirements.txt
```

### Configuration Files

Respect existing configuration files:
- `.pylintrc` or `pylintrc` for pylint
- `pyproject.toml` for black, mypy, and other tools
- `setup.cfg` for legacy configurations
- `.bandit` for security scanning rules

### Running Tools Manually

If `scripts/review_runner.py` fails, run tools individually:

```bash
pylint path/to/code/
black --check path/to/code/
mypy path/to/code/
bandit -r path/to/code/
safety check
```

### Troubleshooting

- **Import errors**: Ensure virtual environment is activated
- **Tool conflicts**: Check for conflicting configs in pyproject.toml
- **False positives**: Use inline comments to disable specific warnings (# pylint: disable=rule-name)
- **Performance**: For large codebases, review specific files/modules rather than entire codebase

### Further Reading

Refer to the official documentation:
- Python PEPs: https://peps.python.org/
- OWASP Python Security: https://owasp.org/www-project-python-security/
- Framework documentation for Django, Flask, FastAPI
- Real Python for best practices: https://realpython.com/
