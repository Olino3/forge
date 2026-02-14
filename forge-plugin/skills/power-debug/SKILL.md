---
name: power-debug
description: Multi-agent investigation for stubborn bugs. Orchestrates systematic debugging using divide-and-conquer strategies, parallel hypothesis testing, and cross-domain analysis. Use when going in circles debugging, need to investigate browser/API interactions, complex bugs resisting normal debugging, or when symptoms don't match expectations.
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [debug_patterns.md, resolved_bugs.md]
    - type: "shared-project"
      usage: "reference"
tags:
  - debugging
  - workflow
  - investigation
##   - multi-agent

# skill:power-debug - Multi-Agent Bug Investigation

## Version: 1.0.0

## Purpose

Orchestrate systematic, multi-agent investigation for stubborn bugs that resist normal debugging. This skill applies divide-and-conquer strategies, parallel hypothesis testing, and cross-domain analysis to resolve complex issues efficiently.

Use this skill when:
- Going in circles debugging the same issue
- Need to investigate browser/API interactions across layers
- Complex bugs resisting normal single-pass debugging
- Symptoms don't match expectations
- Multiple systems or components may be contributing to the issue
- Need to systematically narrow down root cause from a wide search space

## File Structure

```
skills/power-debug/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Investigation Dimensions

Power debugging evaluates 7 critical dimensions:

1. **Symptom Analysis**: Precise characterization of observed vs expected behavior
2. **Hypothesis Generation**: Multiple competing explanations for the bug
3. **Isolation Strategy**: Systematic narrowing of the search space
4. **Cross-Layer Tracing**: Following data flow across API, database, cache, and UI boundaries
5. **Temporal Analysis**: Understanding when the bug was introduced and what changed
6. **Environmental Factors**: Configuration, dependencies, platform, and runtime differences
7. **Root Cause Verification**: Confirming the fix addresses the actual cause, not just symptoms

**Note**: This skill focuses on investigation methodology, not on implementing fixes. It produces a diagnosis with actionable fix recommendations.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Symptom Documentation (REQUIRED)

**YOU MUST:**
1. **Capture the bug report precisely**:
   - What is the **expected** behavior?
   - What is the **actual** behavior?
   - What are the **exact** error messages, stack traces, or logs?
   - When did this start happening? (always, recently, intermittently)
2. **Classify the bug type**:
   - **Crash**: Application terminates unexpectedly
   - **Logic error**: Wrong results, incorrect state
   - **Performance**: Slow, hanging, resource exhaustion
   - **Intermittent**: Race condition, timing-dependent
   - **Integration**: Cross-system communication failure
   - **Configuration**: Environment-specific issues
3. **Identify the scope**:
   - Single file, single module, cross-module, cross-system
   - Which layers are involved? (UI, API, database, cache, external service)
4. **Gather reproduction steps**:
   - Minimal steps to reproduce
   - Environment details (OS, runtime version, dependencies)
   - Is it reproducible consistently or intermittently?

**DO NOT PROCEED WITHOUT CLEAR SYMPTOM DOCUMENTATION**

### ⚠️ STEP 2: Load Memory (REQUIRED)

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="power-debug"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("power-debug", "{project-name}")` to load existing debug history
2. Check for **previously resolved bugs** with similar symptoms
3. Review **known fragile areas** in the codebase
4. If no memory exists, note this is the first debug session for this project

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

**YOU MUST:**
1. Load relevant domain context based on the bug's technology stack
2. Use `contextProvider.detectProjectType()` to understand the project
3. Cross-reference with `memoryStore.getByProject("{project-name}")` for insights from other skills

**DO NOT PROCEED WITHOUT UNDERSTANDING PROJECT CONTEXT**

### ⚠️ STEP 4: Hypothesis Generation (REQUIRED)

**YOU MUST:**
1. **Generate at least 3 competing hypotheses** for the root cause:
   - Each hypothesis must be **specific and testable**
   - Each must explain **all observed symptoms**
   - Rank by probability based on available evidence
2. **For each hypothesis, define**:
   - What evidence would **confirm** it
   - What evidence would **refute** it
   - What test or investigation would distinguish it from other hypotheses
3. **Consider cross-cutting concerns**:
   - Could multiple causes be interacting?
   - Are there environmental factors at play?
   - Has anything changed recently? (deployments, dependencies, config)
4. **Document the hypothesis table**:

| # | Hypothesis | Probability | Confirming Evidence | Refuting Evidence |
|---|-----------|-------------|--------------------|--------------------|
| 1 | ... | High | ... | ... |
| 2 | ... | Medium | ... | ... |
| 3 | ... | Low | ... | ... |

**DO NOT SKIP HYPOTHESIS GENERATION**

### ⚠️ STEP 5: Systematic Investigation (REQUIRED)

**YOU MUST:**
1. **Test hypotheses in order of probability** (highest first):
   - Execute the minimal test that can confirm or refute each hypothesis
   - Record the result before moving to the next
2. **Use divide-and-conquer strategy**:
   - Binary search through the code path to isolate the failure point
   - Add logging/assertions at midpoints to narrow the search
   - Eliminate entire subsystems from consideration when possible
3. **Cross-layer tracing** (when the bug spans boundaries):
   - Trace the request/data from entry point to failure point
   - Check data transformations at each boundary
   - Verify serialization/deserialization at API boundaries
   - Check database queries and results
   - Inspect cache state if caching is involved
4. **Temporal analysis** (when the bug is recent):
   - Use `git log` and `git bisect` to find when the bug was introduced
   - Review recent changes to affected files
   - Check dependency updates
5. **Environmental investigation** (when environment-specific):
   - Compare configurations across environments
   - Check environment variables, feature flags, and runtime versions
   - Verify network connectivity and external service availability

**DO NOT ACCEPT FIRST PLAUSIBLE EXPLANATION WITHOUT VERIFICATION**

### ⚠️ STEP 6: Root Cause Determination (REQUIRED)

**YOU MUST:**
1. **Confirm the root cause**:
   - The identified cause must explain **all** observed symptoms
   - Fixing it must resolve the issue without creating new problems
   - If symptoms persist after a fix, the root cause was not found — return to Step 4
2. **Document the diagnosis**:
   - Root cause description (clear, specific, technical)
   - Evidence chain (how you arrived at this conclusion)
   - Affected components and files
   - Impact assessment (severity, blast radius)
3. **Propose fix options**:
   - **Quick fix**: Minimal change to resolve the immediate issue
   - **Proper fix**: Comprehensive solution addressing underlying design issue
   - **Preventive fix**: Changes that prevent similar bugs in the future (tests, assertions, logging)
4. **Assess fix risk**:
   - What could go wrong with each fix option?
   - What tests should be added or run?
   - Does the fix require coordination with other teams or systems?

**DO NOT SKIP ROOT CAUSE VERIFICATION**

### ⚠️ STEP 7: Generate Output (REQUIRED)

- Save output to `/claudedocs/power-debug_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Symptom summary
  - Hypothesis table with results
  - Investigation trail (what was tried, what was learned)
  - Root cause diagnosis
  - Fix recommendations (quick, proper, preventive)
  - Prevention recommendations

### ⚠️ STEP 8: Update Memory (REQUIRED)

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="power-debug"`. Store any newly learned patterns, conventions, or project insights.

**YOU MUST:**
1. Store the resolved bug pattern for future reference
2. Document the debugging strategy that was most effective
3. Record any fragile areas of the codebase discovered
4. Update known patterns that lead to this class of bugs

---

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] At least 3 hypotheses generated and tested
- [ ] Root cause confirmed with evidence chain
- [ ] Fix recommendations include quick, proper, and preventive options
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 8)

## Output File Naming Convention

**Format**: `power-debug_{project}_{YYYY-MM-DD}.md`

**Examples**:
- `power-debug_myapi_2026-02-12.md`
- `power-debug_myapi_2026-02-12_auth-timeout.md`

---

## Debugging Strategies Quick Reference

### Binary Search Isolation
```
1. Identify the full code path from input to failure
2. Add assertion/log at the midpoint
3. If data is correct at midpoint → bug is in second half
4. If data is wrong at midpoint → bug is in first half
5. Repeat until isolated to a few lines
```

### Temporal Bisection (git bisect)
```bash
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Test each commit git bisect suggests
git bisect good  # or git bisect bad
# Continue until the offending commit is found
git bisect reset
```

### Cross-Layer Trace Template
```
Entry Point → [✓/✗ Data correct?]
    → API Handler → [✓/✗ Data correct?]
        → Service Layer → [✓/✗ Data correct?]
            → Database Query → [✓/✗ Data correct?]
                → Response → [✓/✗ Data correct?]
```

---

## Further Reading

- **Debugging Methodology**: "How to Debug" by Andreas Zeller
- **Git Bisect**: https://git-scm.com/docs/git-bisect
- **Systematic Debugging**: https://www.debuggingbook.org/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — multi-agent investigation with hypothesis testing, cross-layer tracing, and temporal analysis |
