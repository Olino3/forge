# Angular Code Review - Usage Examples

This document provides practical examples of how to use the `angular-code-review` skill in various scenarios.

---

## Example 1: Component Code Review

**Scenario**: Reviewing changes to a user profile component

**Command**:
```
skill:angular-code-review

Please review the changes to the user profile component between commits abc123 and def456
```

**What Happens**:
1. Skill invokes `skill:get-git-diff` to identify changed files
2. Identifies `user-profile.component.ts`, `user-profile.component.html`, `user-profile.component.scss`
3. Loads project memory to understand application conventions
4. Detects Angular version, PrimeNG usage, standalone components
5. Loads relevant context: component_patterns, primeng_patterns, common_issues
6. Reviews for:
   - Subscription leaks in observable subscriptions
   - Missing trackBy in *ngFor loops
   - Proper input/output usage
   - Change detection strategy (OnPush opportunities)
   - Template security (XSS via innerHTML)
   - PrimeNG component API usage
7. Generates report with findings organized by severity
8. Updates project memory with new patterns observed

**Expected Findings**:
- Subscription leak: Observable not unsubscribed in ngOnDestroy
- Performance: Missing trackBy in *ngFor iterating users
- Security: Unsafe use of innerHTML for user bio
- Best Practice: Could use OnPush change detection strategy

---

## Example 2: Service and API Integration Review

**Scenario**: Reviewing a new service that calls a backend API

**Command**:
```
skill:angular-code-review

Review the new UserService implementation in feature/user-management branch
```

**What Happens**:
1. Git diff identifies `user.service.ts`, `user.interceptor.ts`, `user.guard.ts`
2. Loads project memory: detects NgRx state management is used
3. Detects HTTP interceptor, auth guard, RxJS patterns
4. Loads context: service_patterns, rxjs_patterns, security_patterns, ngrx_patterns
5. Reviews for:
   - Proper dependency injection (providedIn: 'root')
   - HTTP error handling and retry logic
   - RxJS operator usage (switchMap vs mergeMap)
   - Security: JWT token handling in interceptor
   - State management: Integration with NgRx actions
   - Type safety: Proper TypeScript interfaces for API responses
6. Asks about error handling strategy if not found in memory
7. Generates inline comments for each issue found
8. Updates memory: documents API error handling pattern

**Expected Findings**:
- Missing error handling in HTTP calls (should use catchError)
- Interceptor doesn't handle token refresh on 401
- Using mergeMap instead of switchMap (race condition risk)
- Missing loading state management
- Type 'any' used for API response (should be typed interface)

---

## Example 3: State Management (NgRx) Review

**Scenario**: Reviewing NgRx store implementation for a new feature

**Command**:
```
skill:angular-code-review

Review the product catalog NgRx implementation (actions, reducers, effects, selectors)
```

**What Happens**:
1. Git diff identifies `product.actions.ts`, `product.reducer.ts`, `product.effects.ts`, `product.selectors.ts`
2. Detects NgRx state management pattern
3. Loads context: ngrx_patterns, rxjs_patterns, performance_patterns
4. Reviews for:
   - **Actions**: Proper action naming conventions, typed payloads
   - **Reducers**: Purity (no mutations), proper immutable updates
   - **Effects**: Error handling, proper RxJS operators, side effect management
   - **Selectors**: Memoization, composition, performance
   - **Architecture**: Proper separation of concerns, facade pattern usage
5. Checks for common NgRx mistakes:
   - Mutating state in reducers
   - Missing error actions in effects
   - Selector over-computation
   - Direct store access in components (should use selectors)
6. Generates comprehensive report with architectural recommendations
7. Updates memory: documents team's NgRx patterns

**Expected Findings**:
- Reducer mutates state directly (should use spread operator)
- Effect missing error handling (catchError)
- Selector recomputes on every call (needs memoization)
- Component subscribing to store directly (should use selector)
- Action payloads not typed (should use TypeScript interfaces)

---

## Example 4: Performance Optimization Review

**Scenario**: Reviewing performance improvements to a data table component

**Command**:
```
skill:angular-code-review

Review performance changes to the product table component
```

**What Happens**:
1. Git diff identifies `product-table.component.ts`, `product-table.component.html`
2. Loads project memory: understands this is a high-traffic component
3. Detects PrimeNG Table component usage, large data set rendering
4. Loads context: performance_patterns, component_patterns, primeng_patterns
5. Reviews for:
   - **Change Detection**: OnPush strategy implementation
   - **Rendering**: TrackBy function for *ngFor
   - **Virtual Scrolling**: For large lists
   - **Pagination**: Proper implementation
   - **Filtering/Sorting**: Client-side vs server-side
   - **Memory**: Observable cleanup, event listener removal
6. Checks PrimeNG-specific optimizations:
   - Lazy loading configuration
   - Virtual scroll settings
   - Custom trackBy functions
7. Measures potential impact of changes
8. Generates report with performance metrics and recommendations
9. Updates memory: documents performance baseline

**Expected Findings**:
- OnPush implemented correctly
- Missing trackBy function in nested *ngFor
- Virtual scrolling configured but with suboptimal buffer size
- Subscription cleanup implemented properly
- Recommendation: Consider server-side pagination for >10k rows

---

## Example 5: Security-Focused Review

**Scenario**: Reviewing authentication and authorization implementation

**Command**:
```
skill:angular-code-review

Security review of the new authentication system
```

**What Happens**:
1. Git diff identifies `auth.service.ts`, `auth.guard.ts`, `auth.interceptor.ts`, `login.component.ts`
2. Detects security-sensitive code (auth, JWT, guards)
3. Loads context: security_patterns (Angular), security_guidelines (general), common_issues
4. Reviews for:
   - **XSS**: Template security, DOM sanitization
   - **Authentication**: JWT storage (localStorage vs sessionStorage vs httpOnly cookie)
   - **Authorization**: Route guard implementation, role-based access
   - **CSRF**: Token implementation in forms
   - **API Security**: Interceptor token injection, CORS handling
   - **Sensitive Data**: Logging, error messages, console output
   - **Token Refresh**: Proper handling of expired tokens
5. Checks for OWASP Top 10 vulnerabilities specific to Angular
6. Generates security-focused report with severity ratings
7. Updates memory: documents security decisions and trade-offs

**Expected Findings**:
- 🔴 **CRITICAL**: JWT stored in localStorage (vulnerable to XSS)
- 🔴 **CRITICAL**: No CSRF protection on state-changing operations
- 🟡 **IMPORTANT**: Auth guard doesn't handle token expiration
- 🟡 **IMPORTANT**: Sensitive data logged to console in error handler
- 🔵 **MINOR**: Missing rate limiting consideration on login

---

## Example 6: TypeScript Best Practices Review

**Scenario**: Reviewing type safety improvements across multiple files

**Command**:
```
skill:angular-code-review

Review TypeScript type safety improvements in feature/strict-mode branch
```

**What Happens**:
1. Git diff identifies multiple `.ts` files with type changes
2. Detects TypeScript strict mode enabled in tsconfig.json
3. Loads context: typescript_patterns, common_issues
4. Reviews for:
   - **Type Safety**: Proper type annotations vs inference
   - **Strict Mode**: Compliance with strictNullChecks, noImplicitAny
   - **Generics**: Proper usage, constraints
   - **Utility Types**: Partial, Pick, Omit, Record usage
   - **Type Guards**: Custom type guards for narrowing
   - **Any Usage**: Elimination or justification
   - **Interface vs Type**: Consistency and appropriateness
5. Checks for TypeScript anti-patterns
6. Generates report with refactoring recommendations
7. Updates memory: documents team's TypeScript conventions

**Expected Findings**:
- Multiple 'any' types replaced with proper interfaces ✓
- Some functions still lack return type annotations
- Generic constraints could be more specific
- Utility type 'Partial' used incorrectly in one place
- Recommendation: Use type guard instead of type assertion

---

## Example 7: RxJS and Observable Pattern Review

**Scenario**: Reviewing reactive programming patterns in a data service

**Command**:
```
skill:angular-code-review

Review the RxJS patterns in the data synchronization service
```

**What Happens**:
1. Git diff identifies `data-sync.service.ts` with heavy RxJS usage
2. Detects complex observable chains, subjects, operators
3. Loads context: rxjs_patterns, service_patterns, performance_patterns
4. Reviews for:
   - **Subscription Management**: takeUntil, async pipe usage
   - **Operator Selection**: Appropriate operators (switchMap, mergeMap, concatMap, exhaustMap)
   - **Error Handling**: Proper catchError and retry logic
   - **Subject Usage**: BehaviorSubject vs ReplaySubject vs Subject
   - **Hot vs Cold**: Observable temperature understanding
   - **Memory Leaks**: Uncompleted streams, subscription leaks
   - **Performance**: Excessive subscriptions, operator chaining
5. Identifies complex patterns that could be simplified
6. Generates inline comments with RxJS refactoring suggestions
7. Updates memory: documents RxJS patterns used in project

**Expected Findings**:
- Using mergeMap when switchMap would prevent race condition
- Missing error handling in observable chain
- Manual subscription without unsubscribe (should use async pipe)
- BehaviorSubject used but initial value never needed (use Subject)
- Complex nested subscriptions (callback hell - should flatten)

---

## Example 8: TailwindCSS + PrimeNG Integration Review

**Scenario**: Reviewing styling and UI component changes

**Command**:
```
skill:angular-code-review

Review the TailwindCSS styling changes in the dashboard components
```

**What Happens**:
1. Git diff identifies component HTML and SCSS files with Tailwind classes
2. Detects TailwindCSS usage with PrimeNG components
3. Loads context: tailwind_patterns, primeng_patterns, component_patterns
4. Reviews for:
   - **TailwindCSS**: Class organization, dynamic class binding
   - **PrimeNG Integration**: Style overrides, theme customization
   - **Responsive Design**: Breakpoint usage
   - **Accessibility**: ARIA attributes, keyboard navigation
   - **Performance**: PurgeCSS configuration for production
   - **Maintainability**: Class extraction, component reusability
5. Checks for Tailwind anti-patterns with Angular
6. Validates PrimeNG component API usage
7. Generates report with UI/UX recommendations
8. Updates memory: documents styling conventions

**Expected Findings**:
- Dynamic class binding not using [class] properly
- TailwindCSS classes conflict with PrimeNG theme
- Missing responsive classes for mobile
- Accessibility: Missing ARIA labels on PrimeNG buttons
- Recommendation: Extract common Tailwind patterns to SCSS mixins

---

## Example 9: Full Feature Branch Review

**Scenario**: Comprehensive review before merging a feature branch

**Command**:
```
skill:angular-code-review

Comprehensive review of feature/user-dashboard branch before merge to main
```

**What Happens**:
1. Git diff compares entire feature branch to main
2. Identifies all changed files: components, services, guards, models, templates, styles
3. Loads complete project memory
4. Detects all patterns: Angular, NgRx, RxJS, TailwindCSS, PrimeNG, TypeScript
5. Loads all relevant context files based on detected patterns
6. Performs comprehensive review across ALL 8 focus areas
7. Reviews architectural consistency across multiple files
8. Checks for integration issues between components
9. Generates comprehensive report with:
   - Executive summary of changes
   - Critical issues requiring immediate attention
   - Architectural recommendations
   - Performance analysis
   - Security assessment
   - Testing coverage analysis
   - Priority matrix for addressing findings
10. Updates memory with feature-specific patterns and decisions

**Expected Output**:
- 50+ page comprehensive report
- Issues categorized by severity and focus area
- Architectural analysis of the feature's design
- Integration concerns with existing codebase
- Performance impact assessment
- Security vulnerability scan
- Testing recommendations
- Positive highlights (what was done well)
- Prioritized action items

---

## Example 10: Incremental Review (Post-Commit)

**Scenario**: Quick review of a single commit after push

**Command**:
```
skill:angular-code-review

Quick review of my last commit (HEAD~1..HEAD)
```

**What Happens**:
1. Git diff shows only the most recent commit's changes
2. Identifies 2-3 changed files
3. Loads project memory (quick lookup)
4. Detects patterns in changed files only
5. Loads minimal context files (efficient)
6. Performs focused review on specific changes
7. Generates concise inline comments
8. Quick memory update (incremental)

**Expected Output**:
- Short inline comment list (5-10 items)
- Focus on immediate issues in the commit
- Fast turnaround (under 1 minute)
- Lightweight memory update

---

## Common Usage Patterns

### Pattern 1: Pre-Merge Review
```
skill:angular-code-review
Review all changes in my feature branch before merging to main
```
Use before creating a pull request to catch issues early.

### Pattern 2: Security Audit
```
skill:angular-code-review
Security-focused review of the authentication changes
```
Use when reviewing security-sensitive code.

### Pattern 3: Performance Analysis
```
skill:angular-code-review
Performance review of the data table optimization changes
```
Use after making performance improvements to validate effectiveness.

### Pattern 4: Post-Refactor Review
```
skill:angular-code-review
Review the refactoring of the user service from commit abc to def
```
Use after major refactoring to ensure nothing was broken.

### Pattern 5: Learning Review
```
skill:angular-code-review
Review my implementation of NgRx for learning purposes
```
Use for educational feedback on Angular patterns.

---

## Tips for Effective Reviews

1. **Be Specific**: Provide commit hashes or branch names for precise scope
2. **Ask Questions**: Skill will ask Socratic questions if memory is incomplete
3. **Request Format**: Specify "report", "inline", or "both" if you have a preference
4. **Incremental Reviews**: Review small commits frequently rather than large branches
5. **Update Memory**: Let the skill update memory to improve future reviews
6. **Context Matters**: First review of a project takes longer (creates memory)
7. **Trust the Process**: Follow the 5-step workflow - it's comprehensive for a reason

---

## Output Examples

### Report Format (Excerpt)
```markdown
# Angular Code Review Report
**Project**: MyApp
**Date**: 2025-01-14
**Scope**: feature/user-dashboard (45 files changed)

## Executive Summary
This feature adds a user dashboard with real-time data updates...

## Critical Issues (🔴 Must Fix)

### 1. Memory Leak in Dashboard Component
**Location**: `src/app/dashboard/dashboard.component.ts:45`
**Severity**: Critical
**Category**: Deep Bugs / Performance
**Description**: Observable subscription not cleaned up in ngOnDestroy...
**Impact**: Memory leak grows with each component mount/unmount...
**Fix**:
\`\`\`typescript
private destroy$ = new Subject<void>();
ngOnDestroy() { this.destroy$.next(); this.destroy$.complete(); }
\`\`\`
**Reference**: ../../context/angular/rxjs_patterns.md#subscription-management
```

### Inline Format (Excerpt)
```markdown
## dashboard.component.ts:45

\`\`\`typescript
43: ngOnInit() {
44:   this.dataService.getData().subscribe(data => {
45:     this.data = data;
46:   });
47: }
\`\`\`

### 🔴 Critical: Memory Leak - Unmanaged Subscription

**Description**: Observable subscription is not cleaned up, causing a memory leak.

**Impact**: Every time this component is created and destroyed, a new subscription remains active...

**Fix**:
\`\`\`typescript
private destroy$ = new Subject<void>();

ngOnInit() {
  this.dataService.getData()
    .pipe(takeUntil(this.destroy$))
    .subscribe(data => this.data = data);
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}
\`\`\`

**Reference**: See `../../context/angular/rxjs_patterns.md#subscription-management`
```

---

## When to Use This Skill

**Ideal Scenarios**:
- Pre-pull request reviews
- Post-commit validation
- Security audits
- Performance optimization validation
- Learning and mentoring
- Architectural review
- Refactoring validation
- Technical debt identification

**Not Ideal For**:
- Reviewing entire codebase (use git diff for changed files)
- Style-only reviews (use ESLint/Prettier)
- Trivial changes (whitespace, comments)

---

## Advanced Usage

### Comparing Multiple Commits
```
skill:angular-code-review
Review changes from commit abc123 through def456 to ghi789
```

### Branch Comparison
```
skill:angular-code-review
Compare feature/new-feature branch with develop branch
```

### Specific File Focus
```
skill:angular-code-review
Review only the service files changed in the last 3 commits
```

The skill will adapt to your request and invoke `skill:get-git-diff` appropriately.

---

## Memory Evolution

First review of a project:
- Creates memory directory
- Documents initial observations
- Takes longer (creating baseline)

Subsequent reviews:
- Loads existing memory
- Builds on previous knowledge
- Faster (knows project context)
- More accurate (fewer false positives)
- Recognizes project conventions

After 5-10 reviews:
- Deep understanding of project
- Recognizes team patterns
- Minimal false positives
- Tailored recommendations
- Tracks trends over time
