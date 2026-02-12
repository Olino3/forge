---
name: code-reviewer
description: Language-agnostic code review framework for best practices and quality assessment. Covers correctness, error handling, maintainability, SOLID principles, DRY/KISS, naming conventions, test coverage, and documentation completeness. Works across any language or framework by detecting the technology stack and loading relevant context. Use for cross-language PR reviews, architecture assessments, legacy code audits, and quality gate enforcement.
---

# Code Reviewer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY code review. Skipping steps or deviating from the procedure will result in incomplete and unreliable reviews. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Review scenarios demonstrating cross-language reviews, architecture assessments, and legacy code audits
- **Context**: Language and domain context loaded dynamically via `contextProvider.getDomainIndex("{detected-language}")` and `contextProvider.getDomainIndex("security")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("code-reviewer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Review Focus Areas

This skill evaluates 8 critical dimensions **in the changed code**, independent of language or framework:

1. **Correctness & Logic**: Algorithm correctness, boundary conditions, off-by-one errors, null/nil handling, type mismatches, logic flow
2. **Error Handling**: Exception strategies, graceful degradation, error propagation, resource cleanup, failure recovery
3. **Maintainability & Readability**: Code clarity, function length, cognitive complexity, comments quality, consistent style
4. **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
5. **DRY / KISS**: Code duplication, unnecessary abstractions, over-engineering, premature optimization
6. **Naming Conventions**: Variable, function, class, and module naming clarity and consistency with language idioms
7. **Test Coverage Assessment**: Missing tests for changed code, edge case coverage, test quality and isolation
8. **Documentation Completeness**: API docs, inline comments for complex logic, README updates, changelog entries

**Note**: Focus on substantive issues requiring human judgment, not style/formatting details. Reviews are performed on changed code only, using the `get-git-diff` skill to identify modifications.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Review Scope (REQUIRED)

**YOU MUST:**
1. **Invoke the `get-git-diff` skill** to identify changed files, OR analyze user-specified files directly
2. Determine comparison scope:
   - Which commits/branches to compare? (e.g., `HEAD^ vs HEAD`, `main vs feature-branch`)
   - If not specified, default to comparing current changes against the default branch
3. Classify changed files by language and framework:
   - Detect languages from file extensions (`.py`, `.js`, `.ts`, `.go`, `.java`, `.cs`, `.rb`, etc.)
   - Identify frameworks from imports, config files, and project structure
4. If no reviewable files were changed, inform the user and exit gracefully
5. Focus subsequent review ONLY on the files identified in the diff

**DO NOT PROCEED WITHOUT IDENTIFYING REVIEW SCOPE**

### ⚠️ STEP 2: Load Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("code-reviewer", "{project-name}")` to load project-specific patterns
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for related skill results (e.g., `python-code-review`, `dotnet-code-review`, `database-schema-analysis`)
   - If memory exists: Review previously learned patterns, conventions, and project-specific context
   - If no memory exists (empty result): Note this is first review, you will create memory later
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - For each detected language, use `contextProvider.getDomainIndex("{language}")` to understand available context
   - Use `contextProvider.getDomainIndex("security")` for security-related context
   - Use `contextProvider.getCrossDomainContext("{language}", triggers)` for cross-cutting concerns

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Load Relevant Context (REQUIRED)

**YOU MUST use the indexes to load only relevant files**:

Based on languages and frameworks detected in Step 1:

1. **ALWAYS**: Use `contextProvider.getAlwaysLoadFiles("{language}")` for each detected language to load universal patterns and common issues
2. **Based on framework detected**: Use `contextProvider.getConditionalContext("{language}", detection)` to load framework-specific patterns
3. **For security-sensitive code**: Use `contextProvider.getCrossDomainContext("{language}", triggers)` where triggers include:
   - Authentication/authorization code
   - User input handling and validation
   - Database queries and data access
   - File system operations
   - Network/API calls
   - Cryptographic operations
4. **For multi-language PRs**: Load context for EACH language present in the changeset, respecting the file token budget

**Progressive loading**: Only load files relevant to the detected languages, frameworks, and code type. The ContextProvider respects the 4-6 file token budget automatically.

**DO NOT SKIP LOADING RELEVANT CONTEXT FILES**

### ⚠️ STEP 4: Deep Review (REQUIRED)

**YOU MUST examine ONLY the changed code for ALL categories below**:

**Important**: While reviewing changed lines, consider the surrounding context to understand:
- How changes interact with existing code
- Whether changes introduce regressions
- Impact on callers and dependent code
- Whether the change addresses the root cause or masks symptoms

**Review Categories** (language-agnostic):

**Correctness & Logic**: Algorithm correctness, boundary conditions, null safety, type correctness, edge cases, off-by-one errors, integer overflow, state corruption
**Error Handling**: Missing error handling, swallowed exceptions, improper error propagation, resource leaks, missing cleanup/finally blocks, inconsistent error strategies
**Maintainability**: Function/method length, cognitive complexity, deep nesting, code duplication, magic numbers/strings, dead code, unclear control flow
**SOLID Principles**: God classes, mixed responsibilities, rigid hierarchies, interface bloat, concrete dependencies, violation of contracts
**DRY / KISS**: Repeated logic, unnecessary abstractions, over-engineering, premature optimization, complex solutions for simple problems
**Naming & Conventions**: Unclear names, inconsistent naming style, misleading identifiers, language-idiomatic naming violations
**Test Coverage**: Missing tests for new/changed code, untested edge cases, brittle tests, missing integration tests, poor test isolation
**Documentation**: Missing/outdated API docs, undocumented public interfaces, missing changelog entries, misleading comments

**DO NOT SKIP ANY CATEGORY**

### ⚠️ STEP 5: Generate Report & Update Memory (REQUIRED)

**YOU MUST ask user for preferred output format**:

- **Option A**: Structured report → executive summary, categorized findings, action items → output to `claudedocs/`
- **Option B**: Inline comments → file:line feedback, PR-style
- **Option C (Default)**: Both formats

**DO NOT CHOOSE FORMAT WITHOUT USER INPUT**

**For EVERY issue in the output, YOU MUST provide**:
1. **Severity**: Critical / Important / Minor
2. **Category**: Correctness / Error Handling / Maintainability / SOLID / DRY-KISS / Naming / Testing / Documentation
3. **Description**: What is wrong and why it matters
4. **Fix**: Concrete code example with improvement
5. **File:line**: Exact location (e.g., `handler.go:142`)

**Format guidelines**:
- Explain WHY (not just what)
- Show HOW to fix with examples
- Be specific with file:line references
- Be balanced (acknowledge good patterns)
- Educate, don't criticize
- Note language-specific idioms and conventions

**DO NOT PROVIDE INCOMPLETE RECOMMENDATIONS**

**After completing the review, UPDATE PROJECT MEMORY**:

Use `memoryStore.update("code-reviewer", "{project-name}", ...)` to create or update memory files:

1. **project_overview**: Languages, frameworks, architecture patterns, deployment info
2. **common_patterns**: Project-specific coding patterns and conventions discovered
3. **known_issues**: Recurring issues or anti-patterns found in this project
4. **review_history**: Summary of reviews performed with dates and key findings

Timestamps and staleness tracking are managed automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

---

## Interface References

| Interface | Usage in This Skill |
|-----------|-------------------|
| [ContextProvider](../../interfaces/context_provider.md) | Load language/framework context dynamically based on detected stack |
| [MemoryStore](../../interfaces/memory_store.md) | Persist project review patterns, conventions, and history |
| [SkillInvoker](../../interfaces/skill_invoker.md) | Delegate to `get-git-diff` for change identification |
| [ExecutionContext](../../interfaces/execution_context.md) | Receive context from chained commands |

## Compliance Checklist

Before completing ANY review, verify:
- [ ] Step 1: Review scope identified using `get-git-diff` skill or user-specified files; languages and frameworks detected
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()` and context detected via `contextProvider`
- [ ] Step 3: All relevant context files loaded via `contextProvider.getAlwaysLoadFiles()`, `getConditionalContext()`, and `getCrossDomainContext()` for each detected language
- [ ] Step 4: Deep review completed for ALL categories on changed code only
- [ ] Step 5: Output generated with all required fields AND project memory updated via `memoryStore.update()`

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE REVIEW**

## Further Reading

- **Quality Principles**:
  - SOLID Principles: https://en.wikipedia.org/wiki/SOLID
  - Clean Code (Robert C. Martin)
  - Refactoring (Martin Fowler)
- **Security**:
  - OWASP Top 10: https://owasp.org/www-project-top-ten/
  - CWE Top 25: https://cwe.mitre.org/top25/
- **Testing**:
  - Test Pyramid: https://martinfowler.com/bliki/TestPyramid.html

## Version History

- v1.0.0 (2026-02-12): Initial release — language-agnostic code review framework
  - Covers 8 review dimensions: correctness, error handling, maintainability, SOLID, DRY/KISS, naming, testing, documentation
  - Dynamic language/framework detection with contextProvider integration
  - Cross-skill discovery via memoryStore for related review insights
