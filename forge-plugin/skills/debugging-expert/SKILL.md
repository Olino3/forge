---
name: debugging-expert
description: Advanced debugging techniques across languages and platforms. Focuses on root cause analysis, systematic debugging methodology, log analysis, performance profiling, memory leak detection, concurrency debugging, stack trace analysis, and environment-specific debugging. Use for production incidents, intermittent failures, performance regressions, and complex multi-service debugging scenarios.
---

# Debugging Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY debugging session. Skipping steps or deviating from the procedure will result in incomplete and unreliable analysis. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Debugging scenarios with step-by-step resolution examples
- **Context**: Relevant domain context loaded via `contextProvider.getDomainIndex("{language}")` and `contextProvider.getDomainIndex("security")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("debugging-expert", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Debugging Focus Areas

Debugging sessions evaluate 8 critical dimensions:

1. **Root Cause Analysis**: Distinguish symptoms from underlying causes, trace causal chains, identify contributing factors
2. **Systematic Debugging Methodology**: Structured hypothesis-driven approach, divide-and-conquer, scientific method applied to code
3. **Log Analysis & Tracing**: Log correlation, distributed tracing, structured logging interpretation, trace ID propagation
4. **Performance Profiling & Bottleneck Identification**: CPU profiling, flame graphs, latency analysis, throughput measurement, resource utilization
5. **Memory Leak Detection**: Heap analysis, garbage collection behavior, object retention graphs, allocation tracking
6. **Concurrency & Race Condition Debugging**: Thread safety analysis, deadlock detection, lock contention, async/await pitfalls, atomicity violations
7. **Stack Trace Analysis**: Exception chain interpretation, frame analysis, symbol resolution, cross-service stack correlation
8. **Environment-Specific Debugging**: Dev/staging/prod differences, configuration drift, infrastructure dependencies, network issues

**Note**: Focus on systematic investigation and root cause identification, not superficial symptom treatment. Debugging must produce actionable findings with verified fixes.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify the Problem (REQUIRED)

**YOU MUST:**
1. **Gather symptoms**: Collect error messages, logs, stack traces, and user reports describing the issue
2. **Reproduce conditions**: Determine the steps, inputs, and environment needed to reproduce the bug
3. **Identify affected components**: Map which services, modules, or layers are involved
4. **Determine language/framework**: Identify the language, runtime, framework, and platform to load appropriate context
5. **Establish timeline**: When did the issue start? What changed? Check recent deployments, config changes, and dependency updates

**DO NOT PROCEED WITHOUT CLEARLY IDENTIFYING THE PROBLEM**

### ⚠️ STEP 2: Load Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("debugging-expert", "{project-name}")` to load project-specific debugging history
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for code review findings, schema analysis results, test findings, or other skill insights that may be relevant
   - If memory exists: Review previously encountered bugs, known fragile areas, and past debugging patterns
   - If no memory exists (empty result): Note this is first debugging session, you will create memory later
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("{language}")` to understand language-specific context files and debugging tools
   - Use `contextProvider.getDomainIndex("security")` if the issue may have security implications
   - Load only context files relevant to the detected language, framework, and issue type

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Systematic Investigation (REQUIRED)

**YOU MUST:**
1. **Formulate hypotheses**: Based on symptoms and context, list the most likely causes ranked by probability
2. **Test hypotheses systematically**: Verify or eliminate each hypothesis using evidence — do not guess
3. **Use binary search / bisection**: Narrow down the problem space by halving — use `git bisect`, toggle features, comment out code blocks, isolate services
4. **Analyze logs, traces, and stack traces**:
   - Correlate timestamps across log sources
   - Follow distributed trace IDs across service boundaries
   - Read stack traces bottom-up to identify the originating fault
   - Look for patterns in error frequency, timing, and affected users
5. **Inspect runtime state**: Examine variable values, memory usage, thread states, connection pools, and queue depths at the time of failure

**DO NOT SKIP HYPOTHESIS TESTING — GUESSING IS NOT DEBUGGING**

### ⚠️ STEP 4: Root Cause Analysis & Fix (REQUIRED)

**YOU MUST:**
1. **Identify the root cause, not symptoms**: Clearly articulate WHY the bug occurs, not just WHAT happens
2. **Propose fix with explanation**: Provide a concrete code fix that addresses the root cause, with a clear explanation of why it works
3. **Verify fix resolves issue without regressions**:
   - Confirm the fix addresses the original reproduction steps
   - Check for side effects on related functionality
   - Verify edge cases and boundary conditions
   - Ensure the fix does not introduce new issues in other environments

**DO NOT PROPOSE FIXES THAT ONLY MASK SYMPTOMS**

### ⚠️ STEP 5: Document & Update Memory (REQUIRED)

**YOU MUST:**
1. **Output debugging report** to `claudedocs/` containing:
   - **Problem Summary**: Symptoms, affected components, severity
   - **Investigation Timeline**: Hypotheses tested and evidence gathered
   - **Root Cause**: Clear explanation of the underlying issue
   - **Fix Applied**: Code changes with before/after comparison
   - **Prevention**: Recommendations to prevent recurrence (tests, monitoring, alerts)
2. **Update project memory** using `memoryStore.update("debugging-expert", "{project-name}", ...)`:
   - **known_issues**: Bug patterns and fragile areas discovered
   - **debugging_patterns**: Effective debugging approaches for this project
   - **environment_notes**: Environment-specific quirks and configuration details
   - **resolution_history**: Summary of bugs resolved with dates and root causes

Timestamps and staleness tracking are managed automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

---

## Interface References

- **ContextProvider**: [../../interfaces/context_provider.md](../../interfaces/context_provider.md) — Load context by domain, tags, or sections
- **MemoryStore**: [../../interfaces/memory_store.md](../../interfaces/memory_store.md) — Read/write project-specific memory with lifecycle automation
- **SkillInvoker**: [../../interfaces/skill_invoker.md](../../interfaces/skill_invoker.md) — Delegate to related skills (e.g., `get-git-diff` for bisection)

## Compliance Checklist

Before completing ANY debugging session, verify:
- [ ] Step 1: Problem clearly identified with symptoms, reproduction steps, and affected components
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()` and relevant context loaded via `contextProvider`
- [ ] Step 3: Systematic investigation completed with hypotheses tested and evidence gathered
- [ ] Step 4: Root cause identified (not symptoms) and fix verified without regressions
- [ ] Step 5: Debugging report generated AND project memory updated via `memoryStore.update()`

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DEBUGGING SESSION**

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Systematic debugging methodology with 5-step mandatory workflow
  - Interface-based context and memory access
  - Support for cross-language and cross-platform debugging
