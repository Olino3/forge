# Code Review Report: [Project Name]

**Date**: [YYYY-MM-DD]
**Reviewer**: Claude Code
**Scope**: [Brief description of what was reviewed]

---

## Executive Summary

**Overall Assessment**: [Excellent | Good | Fair | Needs Improvement | Critical Issues Found]

**Key Findings**:
- Critical Issues: [N]
- Important Issues: [N]
- Performance Concerns: [N]
- Security Vulnerabilities: [N]

**Recommendation**: [Summary recommendation - e.g., "Address critical security issues before deployment" or "Code is production-ready with minor improvements recommended"]

---

## Critical Issues

### 1. [Issue Title]

**Severity**: Critical
**Category**: [Security | Data Corruption | Production Failure]
**Location**: `file.py:123`

**Description**:
[Detailed description of the issue]

**Impact**:
[What could go wrong if not fixed]

**Recommendation**:
```python
# Before (vulnerable)
[problematic code]

# After (fixed)
[corrected code]
```

**References**:
- [CWE-XXX](link) or [OWASP](link) if applicable

---

### 2. [Next Critical Issue]
...

---

## Important Issues

### Performance Bottleneck: [Description]

**Location**: `file.py:456`
**Impact**: [e.g., "O(n²) complexity causes slowdown with large datasets"]

**Analysis**:
[Explanation of the performance issue]

**Recommendation**:
```python
# Current implementation (slow)
[current code]

# Optimized implementation
[improved code]
```

**Expected Improvement**: [e.g., "100x faster for 10,000 items"]

---

### Security Concern: [Description]

**Location**: `file.py:789`
**Severity**: Important

**Details**:
[Description of security concern]

**Fix**:
```python
[corrected code]
```

---

## Architecture and Design

### Concerns

1. **Tight Coupling**: [Description]
   - Location: [files]
   - Recommendation: [architectural improvement]

2. **Missing Abstractions**: [Description]
   - Impact: [code duplication, hard to test, etc.]
   - Recommendation: [refactoring suggestion]

### Positive Patterns

- [Well-implemented pattern 1]
- [Good design choice 2]

---

## Performance Analysis

### CPU Profiling Results

**Top Hotspots**:
1. `function_name()` in `file.py`: [X]ms cumulative ([Y]% of total)
2. [Next hotspot]

### Memory Usage

**Peak Memory**: [X] MB
**Concerns**:
- [Memory leak in function X]
- [Inefficient data structure in Y]

### Recommendations

1. [Specific performance improvement 1]
2. [Specific performance improvement 2]

---

## Code Quality

### Complexity Analysis

**High Complexity Functions**:
- `function_name()` (file.py:123): Complexity 25 (Rank C)
  - Recommendation: Refactor into smaller functions

### Dead Code

**Unused Code Found**:
- `unused_function()` in utils.py
- Variable `UNUSED_CONSTANT` in config.py

**Recommendation**: Remove to improve maintainability

---

## Testing

### Coverage Analysis

**Current Coverage**: [X]%

**Missing Critical Tests**:
1. Edge case: [description]
2. Error path: [description]
3. Integration test: [description]

### Test Quality Issues

- [Issue with existing tests]
- [Recommendation for improvement]

---

## Dependencies

### Vulnerable Dependencies

| Package | Current | Vulnerability | Fix |
|---------|---------|---------------|-----|
| package-name | 1.0.0 | CVE-XXXX-XXXX | Upgrade to 1.1.0 |

### Outdated Dependencies

- [List of significantly outdated packages]

---

## Minor Issues and Suggestions

### Style and Conventions

**Note**: These should be handled by automated tools (ruff, isort, basedpyright) in CI/CD.

- [Only list if blocking automated tool adoption]

### Documentation

- Missing docstrings: [list key functions]
- Unclear variable names: [examples]

---

## Positive Highlights

**Well-Implemented Features**:
1. [Good pattern or implementation 1]
2. [Good practice observed 2]
3. [Security measure properly implemented]

---

## Recommendations Priority Matrix

### Immediate (Before Deployment)

1. [ ] Fix SQL injection vulnerability (file.py:123)
2. [ ] Address race condition in payment processing (payment.py:456)
3. [ ] Fix memory leak in upload handler (upload.py:789)

### High Priority (This Sprint)

1. [ ] Optimize N+1 query in user list (views.py:234)
2. [ ] Add missing authentication check (api.py:567)
3. [ ] Implement error handling in critical path (processor.py:890)

### Medium Priority (Next Sprint)

1. [ ] Refactor high complexity functions
2. [ ] Add integration tests for payment flow
3. [ ] Update vulnerable dependencies

### Low Priority (Backlog)

1. [ ] Remove dead code
2. [ ] Improve documentation
3. [ ] Consider architectural refactoring for module X

---

## Automated Tool Results Summary

- **Ruff**: [N] issues found
- **Basedpyright**: [N] type errors
- **Bandit**: [N] security issues
- **Safety**: [N] vulnerable dependencies
- **Performance Profiler**: [Summary of findings]

**Detailed reports**: See `review_results/` directory

---

## Conclusion

[Overall assessment paragraph summarizing the review, key takeaways, and next steps]

**Approval Status**: [Approved | Approved with Conditions | Requires Changes | Blocked]

**Next Steps**:
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

---

**Review Conducted By**: Claude Code Python Review Skill
**Tools Used**: ruff, basedpyright, isort, bandit, safety, performance_profiler
