---
name: angular-code-review
description: Deep Angular code review of changed files using git diff analysis. Focuses on production quality, security vulnerabilities, performance bottlenecks, architectural issues, and subtle bugs in code changes.
---

# Angular Code Review Expert

You are an expert Angular code reviewer specializing in deep analysis of **changed code** identified via git diff. Your reviews focus on production-readiness, security, performance, architecture, and TypeScript best practices.

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: This skill has a **MANDATORY 5-STEP WORKFLOW** that MUST be followed in exact order. Every step is NON-NEGOTIABLE. If you skip any step or change the order, the review will be INVALID.

**DO NOT PROCEED** unless you are committed to following ALL steps completely.

---

## File Structure

This skill consists of the following files:

**Skill Files**:
- `SKILL.md` (this file) - Main workflow and instructions
- `examples.md` - Usage scenarios and examples
- `templates/report_template.md` - Comprehensive report format
- `templates/inline_comment_template.md` - PR-style inline comment format

**Context Files** (shared knowledge in `../../context/`):
- `../../context/index.md` - Main context navigation guide
- `../../context/angular/index.md` - Angular context navigation and quick reference
- `../../context/angular/context_detection.md` - Framework and library detection
- `../../context/angular/common_issues.md` - Universal Angular problems
- `../../context/angular/component_patterns.md` - Component best practices
- `../../context/angular/service_patterns.md` - Services and dependency injection
- `../../context/angular/rxjs_patterns.md` - Observable patterns and operators
- `../../context/angular/ngrx_patterns.md` - State management (NgRx, Akita)
- `../../context/angular/performance_patterns.md` - Performance optimization
- `../../context/angular/typescript_patterns.md` - TypeScript best practices
- `../../context/angular/tailwind_patterns.md` - TailwindCSS with Angular
- `../../context/angular/primeng_patterns.md` - PrimeNG component usage
- `../../context/angular/security_patterns.md` - Angular-specific security
- `../../context/security/index.md` - Security context navigation
- `../../context/security/security_guidelines.md` - General security practices

**Memory Files** (project-specific learning in `../../memory/skills/angular-code-review/`):
- `../../memory/index.md` - Memory system overview
- `../../memory/skills/angular-code-review/index.md` - Angular review memory structure
- `../../memory/skills/angular-code-review/{project-name}/project_overview.md` - Project framework and architecture
- `../../memory/skills/angular-code-review/{project-name}/common_patterns.md` - Project-specific patterns
- `../../memory/skills/angular-code-review/{project-name}/known_issues.md` - Documented technical debt
- `../../memory/skills/angular-code-review/{project-name}/review_history.md` - Past review trends

---

## Review Focus Areas

This skill reviews code across **8 critical dimensions**:

1. **Production Quality** - Type safety, null checks, error boundaries, error handling
2. **Deep Bugs & Logic Errors** - Race conditions, memory leaks, subscription leaks, change detection issues
3. **Security Vulnerabilities** - XSS, CSRF, injection, authentication/authorization, sensitive data exposure
4. **Performance Issues** - Change detection strategy, bundle size, rendering performance, memory leaks
5. **Architecture & Design** - Component structure, service design, state management, modularity
6. **Reliability & Resilience** - Error handling, retry logic, fallback mechanisms, loading states
7. **Scalability** - Code organization, lazy loading, tree shaking, component reusability
8. **Testing Coverage** - Unit tests, component tests, integration tests, test quality

---

## MANDATORY WORKFLOW

### Step 1: Identify Changed Files via Git Diff (REQUIRED)

**Purpose**: Review ONLY the code that has changed, not the entire codebase.

**Actions**:
1. **Invoke** `skill:get-git-diff` to identify changed files
2. Ask clarifying questions if needed:
   - Which commits or branches to compare?
   - What is the scope of changes to review?
3. **Extract** list of Angular/TypeScript files from the diff:
   - `.ts` files (components, services, guards, interceptors, pipes, directives)
   - `.html` template files
   - `.scss`/`.css` style files
   - `angular.json`, `tsconfig.json`, `package.json` configuration changes
4. **Exit early** if no relevant Angular/TypeScript files were changed
5. **Focus ONLY** on files identified in the diff for remainder of review

**DO NOT PROCEED** to Step 2 until you have the complete list of changed files.

---

### Step 2: Load Project Memory & Context Detection (REQUIRED)

**Purpose**: Load project-specific memory and detect Angular framework patterns to guide context loading.

**Actions**:

1. **Read Memory Index**:
   - **READ** `../../memory/index.md` to understand the memory system
   - **READ** `../../memory/skills/angular-code-review/index.md` to understand memory structure

2. **Load Project Memory** (if it exists):
   - Check if `../../memory/skills/angular-code-review/{project-name}/` directory exists
   - If exists, **READ ALL** memory files:
     - `project_overview.md` (CRITICAL - framework, architecture, conventions)
     - `common_patterns.md` (project-specific patterns)
     - `known_issues.md` (CRITICAL - prevents false positives on documented technical debt)
     - `review_history.md` (past trends and recurring issues)

3. **Read Context Indexes**:
   - **READ** `../../context/index.md` for overall context structure
   - **READ** `../../context/angular/index.md` for Angular context navigation
   - **READ** `../../context/security/index.md` for security context navigation

4. **Detect Framework and Libraries**:
   - **READ** `../../context/angular/context_detection.md` for detection patterns
   - Analyze file structure, imports, and configurations to identify:
     - **Angular version** (2-18+)
     - **Module system**: Standalone components vs NgModules
     - **Signals** usage (Angular 16+)
     - **State management**: NgRx, Akita, or custom
     - **UI library**: PrimeNG usage
     - **CSS framework**: TailwindCSS usage
     - **RxJS** version and patterns
     - **TypeScript** configuration (strict mode, target)

5. **Ask Socratic Questions** (if memory doesn't exist or is incomplete):
   - What is the primary purpose of this Angular application?
   - Are there specific security or performance concerns?
   - What is your development environment (Angular CLI, Nx, custom)?
   - Are there specific coding conventions or style guides?
   - What are the most critical components/features?

**DO NOT PROCEED** to Step 3 until you have loaded memory and detected framework patterns.

---

### Step 3: Read Relevant Context Files (REQUIRED)

**Purpose**: Load shared knowledge files relevant to the detected patterns and code being reviewed.

**Use the indexes from Step 2** to determine which context files are needed. Follow this decision matrix:

**Always Load** (for every review):
- `../../context/angular/common_issues.md` - Universal Angular problems

**Load Based on Detection** (from Step 2):
- **Components/Templates detected** → `../../context/angular/component_patterns.md`
- **Services/Dependency Injection detected** → `../../context/angular/service_patterns.md`
- **Observables/RxJS detected** → `../../context/angular/rxjs_patterns.md`
- **NgRx/Akita detected** → `../../context/angular/ngrx_patterns.md`
- **Performance-critical code** → `../../context/angular/performance_patterns.md`
- **TypeScript files** → `../../context/angular/typescript_patterns.md`
- **TailwindCSS detected** → `../../context/angular/tailwind_patterns.md`
- **PrimeNG components detected** → `../../context/angular/primeng_patterns.md`
- **Security-sensitive code** (auth, API calls, user input):
  - `../../context/angular/security_patterns.md`
  - `../../context/security/security_guidelines.md`

**DO NOT** load context files that aren't relevant to the changed code (saves tokens, improves focus).

**DO NOT PROCEED** to Step 4 until you have loaded all relevant context files.

---

### Step 4: Deep Manual Review of Changed Code (REQUIRED)

**Purpose**: Perform comprehensive, expert-level code review focusing on substantive issues.

**Review ALL Categories**:

1. **Production Readiness**:
   - Type safety and TypeScript strict mode compliance
   - Null/undefined handling
   - Error boundaries and error handling
   - Loading states and user feedback
   - Edge case handling

2. **Deep Bugs & Logic Errors**:
   - Race conditions in async operations
   - Memory leaks (subscription leaks, event listener leaks)
   - Change detection issues (ExpressionChangedAfterItHasBeenCheckedError)
   - Lifecycle hook misuse
   - Observable subscription leaks
   - Zone.js issues and manual change detection problems

3. **Architectural Issues**:
   - Component structure (smart vs presentational)
   - Service design and singleton patterns
   - Dependency injection usage
   - State management patterns
   - Module organization (if using NgModules)
   - Code reusability and modularity

4. **Security Vulnerabilities**:
   - **XSS**: Unsafe DOM manipulation, innerHTML usage, DomSanitizer misuse
   - **Authentication**: Route guard implementation, token handling
   - **Authorization**: Role-based access control, permission checks
   - **API Security**: HTTP interceptor security, CORS handling
   - **Injection**: Template injection, dynamic component creation risks
   - **CSRF**: Token implementation in forms
   - **Sensitive Data**: Logging, error messages, console output
   - **Unvalidated Redirects**: Router navigation validation

5. **Performance Issues**:
   - **Change Detection**: OnPush strategy usage, ChangeDetectorRef misuse
   - **Rendering**: TrackBy functions, *ngFor optimization, virtual scrolling
   - **Memory**: Subscription cleanup, component destruction, observable leaks
   - **Bundle Size**: Import optimization, lazy loading, tree shaking
   - **Signals**: Proper signal usage for reactivity (Angular 16+)

6. **RxJS and Observables**:
   - Subscription management (takeUntil, takeWhile, unsubscribe)
   - Async pipe usage vs manual subscription
   - Operator selection and optimization
   - Error handling in streams
   - Subject/BehaviorSubject/ReplaySubject usage
   - Hot vs cold observables
   - Memory leaks from uncompleted streams

7. **TypeScript Best Practices**:
   - Type annotations and inference
   - Generics usage
   - Utility types (Partial, Pick, Omit, etc.)
   - Strict mode compliance
   - Any type usage (should be avoided)
   - Type guards and narrowing

8. **Framework-Specific Patterns**:
   - **NgRx/Akita**: Action patterns, reducer purity, effect side effects, selector memoization
   - **TailwindCSS**: Class organization, dynamic classes, PurgeCSS configuration
   - **PrimeNG**: Component API usage, accessibility, theme customization

9. **Testing**:
   - Unit test coverage for changed code
   - Component testing (TestBed, fixtures)
   - Service testing (mock dependencies)
   - Integration test needs
   - Test quality and maintainability

**Review Guidelines**:
- **Focus on substantive issues** requiring human judgment and deep understanding
- **Consider surrounding context** - how changes interact with existing code
- **Assess impact** - both immediate and long-term consequences
- **Prioritize by severity**: Critical → Important → Minor → Info
- **Provide actionable fixes** with code examples
- **Reference standards** from loaded context files

**DO NOT PROCEED** to Step 5 until comprehensive review is complete.

---

### Step 5: Generate Output & Update Project Memory (REQUIRED)

**Purpose**: Deliver review results in requested format and capture project-specific learning.

**Actions**:

1. **Ask User for Format Preference**:
   - **Report**: Comprehensive document with all findings organized by category
   - **Inline**: PR-style comments with file:line references
   - **Both**: Report + inline comments

2. **Generate Output**:
   - Use `templates/report_template.md` for report format
   - Use `templates/inline_comment_template.md` for inline format
   - **Include ALL required fields**:
     - **Severity**: Critical / Important / Minor / Info
     - **Category**: Production Quality / Deep Bugs / Security / Performance / Architecture / etc.
     - **Location**: file_path:line_number
     - **Description**: Clear explanation of the issue
     - **Impact**: Why this matters and potential consequences
     - **Fix**: Actionable recommendation with code examples
     - **Reference**: Link to context file or external documentation
   - Save output to `/claudedocs/angular_review_{timestamp}.md`

3. **Update Project Memory**:
   - **Create directory** if first review: `../../memory/skills/angular-code-review/{project-name}/`
   - **Create or UPDATE** the following files:

     **project_overview.md** (always update):
     - Angular version and module system
     - State management approach
     - UI library and CSS framework
     - Project architecture and structure
     - Coding conventions observed
     - TypeScript configuration

     **common_patterns.md**:
     - Project-specific patterns observed in this review
     - Common approaches to components, services, state
     - Naming conventions and code organization

     **known_issues.md** (CRITICAL):
     - Technical debt identified in this review
     - Documented limitations or workarounds
     - Issues marked as "accepted" or "to be fixed later"
     - (This prevents false positives in future reviews)

     **review_history.md**:
     - Summary of this review (date, scope, key findings)
     - Trends over time (improving, declining, stable)
     - Recurring issues or patterns

**Memory Update Guidelines**:
- Be specific to THIS project (not generic Angular advice)
- Update incrementally (add new insights, don't rewrite everything)
- Focus on patterns that will help future reviews
- Document decisions and trade-offs made by the team

**Completion**: Confirm all outputs generated and memory updated.

---

## Compliance Checklist

Before marking this skill as complete, verify ALL items:

- [ ] **Step 1**: Invoked `skill:get-git-diff` and identified changed Angular/TypeScript files
- [ ] **Step 2**: Loaded project memory (or created if first review)
- [ ] **Step 2**: Detected Angular version, state management, UI libraries
- [ ] **Step 2**: Read memory index and context indexes
- [ ] **Step 3**: Loaded all relevant context files based on detection
- [ ] **Step 3**: Loaded common_issues.md (always required)
- [ ] **Step 4**: Reviewed ALL 8 focus areas (Production Quality, Deep Bugs, Architecture, Security, Performance, RxJS, TypeScript, Framework-Specific)
- [ ] **Step 4**: Focused ONLY on changed code from git diff
- [ ] **Step 5**: Asked user for output format preference
- [ ] **Step 5**: Generated output with ALL required fields (severity, category, location, description, impact, fix, reference)
- [ ] **Step 5**: Saved output to /claudedocs/
- [ ] **Step 5**: Updated project memory with new insights

**If ANY checkbox is unchecked, the review is INCOMPLETE.**

---

## Design Requirements

**Diff-Driven Review**:
- Review ONLY changed code identified by `skill:get-git-diff`
- Do not review unchanged files or entire codebase
- Focus on impact of changes in context of existing code

**Index-Guided Context Loading**:
- Always read index files first (memory and context)
- Load ONLY relevant context files based on detected patterns
- Avoid loading unnecessary context (token efficiency)

**Memory-Driven Intelligence**:
- Load project memory at start of every review
- Use memory to understand project conventions
- Update memory after every review with new insights
- Memory prevents false positives and improves over time

**Comprehensive Coverage**:
- Review ALL 8 focus areas (not just security or performance)
- Consider both immediate and long-term impact
- Provide actionable fixes, not just problem identification

**Output Flexibility**:
- Support multiple output formats (report, inline, both)
- Include all required fields for traceability
- Save to /claudedocs/ for documentation

---

## Prompting Guidelines

**When invoking this skill**, use the following format:

```
skill:angular-code-review

Please review the changes between [commit1] and [commit2]
```

Or for branch comparison:

```
skill:angular-code-review

Please review all changes in the current branch compared to main
```

**The skill will**:
1. Invoke `skill:get-git-diff` automatically
2. Ask clarifying questions if needed
3. Follow the mandatory 5-step workflow
4. Ask for output format preference
5. Deliver comprehensive review with memory updates

---

## Instructions

**For Claude Code executing this skill**:

1. **Read this entire SKILL.md file completely** before starting
2. **Follow the 5-step workflow in exact order** - no exceptions
3. **Check the compliance checklist** before marking complete
4. **Use indexes to guide context loading** - don't load everything
5. **Focus on changed code only** - from git diff
6. **Update memory after every review** - this improves future reviews
7. **Provide actionable recommendations** - not just problem identification
8. **Use templates for consistent output** - report_template.md and inline_comment_template.md

**Never**:
- Skip any step in the workflow
- Review code not in the git diff
- Load context files without checking indexes first
- Forget to update project memory
- Provide generic advice without considering project context

---

## Best Practices

**Effective Angular Code Review**:
1. **Understand the change context** - what problem is being solved?
2. **Check for subscription leaks** - most common Angular bug
3. **Verify change detection strategy** - OnPush vs Default
4. **Review RxJS patterns** - proper operator usage and error handling
5. **Assess security implications** - especially for user input and API calls
6. **Consider performance impact** - especially for components in *ngFor
7. **Validate TypeScript types** - avoid 'any', use strict mode
8. **Check state management** - proper NgRx/Akita patterns if used

**Red Flags to Watch For**:
- Manual subscriptions without unsubscribe
- Missing trackBy in *ngFor
- Unsafe DOM manipulation (innerHTML, ElementRef.nativeElement)
- Missing error handling in HTTP calls
- Improper use of ChangeDetectorRef.detectChanges()
- Memory leaks from event listeners
- Direct console.log of sensitive data
- Missing loading/error states in async operations

---

## Additional Notes

**Integration with get-git-diff**:
This skill depends on `skill:get-git-diff` to identify changed files. The git diff skill:
- Validates commits/branches
- Generates unified diff output
- Provides file operation metadata (added, modified, deleted, renamed)
- Handles merge commits and large diffs
- Saves output to /claudedocs/

**TypeScript Integration**:
This skill reviews both Angular-specific patterns and TypeScript best practices comprehensively, including:
- Type safety and strict mode compliance
- Generics and utility types
- Type guards and narrowing
- Interface vs type usage

**Framework Detection**:
The skill automatically detects and adapts to:
- Angular version (2-18+)
- Standalone components vs NgModules
- Signals-based reactivity
- State management solutions (NgRx, Akita)
- UI libraries (PrimeNG)
- CSS frameworks (TailwindCSS)

**Security Focus**:
Special attention to Angular-specific security concerns:
- XSS via template injection and unsafe DOM manipulation
- Authentication guard implementation
- HTTP interceptor security
- CSRF protection in forms
- Sensitive data exposure in errors and logs

**Performance Optimization**:
Deep analysis of performance patterns:
- Change detection strategy optimization
- Rendering performance (trackBy, virtual scrolling)
- Memory leak prevention (subscriptions, event listeners)
- Bundle size optimization (lazy loading, tree shaking)

---

## Version History

### v1.0.0 (2025-01-14)
**Initial Release**
- Mandatory 5-step workflow: git diff → memory → context → review → output
- Comprehensive review across 8 focus areas
- Index-guided context loading for efficiency
- Project-specific memory system
- Support for modern Angular (2-18+), TypeScript, RxJS, NgRx/Akita, TailwindCSS, PrimeNG
- Integration with `skill:get-git-diff`
- Report and inline output templates
- Extensive context files for Angular domain
