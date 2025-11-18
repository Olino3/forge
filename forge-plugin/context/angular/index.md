# Angular Context Index

This directory contains shared contextual knowledge for Angular code review and development. These files provide reference materials, best practices, and standards applicable to all Angular projects.

## Purpose

**Context files** are static, shared knowledge that remains consistent across projects. They provide:
- Framework best practices and patterns
- Security guidelines specific to Angular
- Performance optimization techniques
- Common pitfalls and how to avoid them
- Reference materials for RxJS, TypeScript, state management, and UI libraries

**This is NOT project-specific memory** - for project-specific patterns, see `../../memory/skills/angular-code-review/{project-name}/`

---

## Directory Structure

```
angular/
├── index.md (this file)              - Navigation and usage guide
├── context_detection.md              - Framework and library detection patterns
├── common_issues.md                  - Universal Angular problems
├── component_patterns.md             - Component best practices
├── component_testing_patterns.md     - Component testing strategies
├── jest_testing_standards.md         - Jest/Jasmine testing principles
├── ngrx_patterns.md                  - State management (NgRx, Akita)
├── performance_patterns.md           - Performance optimization
├── primeng_patterns.md               - PrimeNG component usage
├── rxjs_patterns.md                  - Observable patterns and operators
├── security_patterns.md              - Angular-specific security
├── service_patterns.md               - Services and dependency injection
├── service_testing_patterns.md       - Service testing strategies
├── tailwind_patterns.md              - TailwindCSS with Angular
├── test_antipatterns.md              - Testing mistakes to avoid
├── testing_utilities.md              - TestBed, mocks, spies, async utilities
└── typescript_patterns.md            - TypeScript best practices
```

---

## Usage Guide

### When Performing Angular Code Reviews

**Step 1: Always Read This Index First**
- Understand available context files
- Determine which files are relevant to the code being reviewed

**Step 2: Load Context Selectively**
- Do NOT load all files automatically
- Use the decision matrix below to determine which files to load
- Loading only relevant files saves tokens and improves focus

**Step 3: Reference Context in Reviews**
- Cite specific sections from context files in review findings
- Provide file paths and section anchors for traceability

---

## Context Loading Decision Matrix

Use this matrix to determine which context files to load based on the code being reviewed:

| Code Type | Always Load | Conditionally Load | Rarely Load |
|-----------|-------------|-------------------|-------------|
| **Any Angular Code** | `common_issues.md` | `context_detection.md` (first review) | - |
| **Components (.ts/.html)** | `component_patterns.md` | `performance_patterns.md`, `security_patterns.md` | `primeng_patterns.md`, `tailwind_patterns.md` |
| **Services (.service.ts)** | `service_patterns.md`, `rxjs_patterns.md` | `typescript_patterns.md` | `ngrx_patterns.md` |
| **Guards/Interceptors** | `service_patterns.md`, `security_patterns.md` | `rxjs_patterns.md` | - |
| **State Management** | `ngrx_patterns.md`, `rxjs_patterns.md` | `typescript_patterns.md` | `performance_patterns.md` |
| **Templates (.html)** | `component_patterns.md` | `security_patterns.md`, `primeng_patterns.md`, `tailwind_patterns.md` | - |
| **Styles (.scss/.css)** | `tailwind_patterns.md` (if Tailwind used) | `primeng_patterns.md` (if PrimeNG used) | - |
| **Performance-Critical** | `performance_patterns.md` | `component_patterns.md`, `rxjs_patterns.md` | - |
| **Security-Sensitive** | `security_patterns.md` | `../../security/security_guidelines.md` | - |
| **Unit Tests (.spec.ts)** | `jest_testing_standards.md`, `testing_utilities.md`, `test_antipatterns.md` | `component_testing_patterns.md`, `service_testing_patterns.md` | - |

### File Descriptions and When to Load

#### **context_detection.md**
**Load When**: First review of a project, or when framework/library detection is needed
**Contains**:
- Angular version detection patterns
- Standalone components vs NgModules identification
- State management detection (NgRx, Akita)
- UI library detection (PrimeNG)
- CSS framework detection (TailwindCSS)
- RxJS version patterns
**Purpose**: Understand the project's tech stack to guide further context loading

#### **common_issues.md**
**Load When**: EVERY review (universal problems)
**Contains**:
- Subscription memory leaks
- Change detection errors (ExpressionChangedAfterItHasBeenCheckedError)
- Lifecycle hook misuse
- Observable subscription management
- Common template mistakes
- Zone.js issues
**Purpose**: Catch the most frequent Angular bugs

#### **component_patterns.md**
**Load When**: Reviewing components (.component.ts) or templates (.html)
**Contains**:
- Smart vs Presentational component patterns
- Input/Output best practices
- ViewChild/ContentChild usage
- Component lifecycle hooks
- Component communication strategies
- Template syntax best practices
**Purpose**: Ensure proper component architecture and implementation

#### **service_patterns.md**
**Load When**: Reviewing services, guards, interceptors, resolvers
**Contains**:
- Dependency injection patterns (`providedIn: 'root'`)
- Singleton service patterns
- Service communication via observables
- HTTP service best practices
- Service hierarchies and scope
**Purpose**: Ensure proper service design and DI usage

#### **rxjs_patterns.md**
**Load When**: Code uses observables, operators, or subjects (very common)
**Contains**:
- Subscription management (takeUntil, async pipe)
- Operator selection (switchMap, mergeMap, concatMap, exhaustMap)
- Error handling (catchError, retry)
- Subject types (BehaviorSubject, ReplaySubject, Subject)
- Hot vs cold observables
- Custom operators
**Purpose**: Prevent RxJS-related bugs and memory leaks

#### **ngrx_patterns.md**
**Load When**: Project uses NgRx or Akita for state management
**Contains**:
- Action patterns and naming conventions
- Reducer purity and immutability
- Effect side effect management
- Selector memoization and composition
- Facade pattern
- Entity adapter usage
**Purpose**: Ensure proper state management architecture

#### **performance_patterns.md**
**Load When**: Performance-critical code, or large lists/data sets
**Contains**:
- Change detection strategies (OnPush, signals)
- TrackBy functions for *ngFor
- Lazy loading and code splitting
- Virtual scrolling
- Zone optimization
- Bundle size optimization
- Memory leak prevention
**Purpose**: Identify and fix performance bottlenecks

#### **typescript_patterns.md**
**Load When**: Reviewing TypeScript code (most files)
**Contains**:
- Type safety and strict mode
- Generics and utility types (Partial, Pick, Omit, Record)
- Type guards and narrowing
- Interface vs type usage
- Avoiding 'any'
- Const assertions
**Purpose**: Ensure proper TypeScript usage and type safety

#### **tailwind_patterns.md**
**Load When**: Project uses TailwindCSS (detected in context_detection or templates)
**Contains**:
- Class organization in Angular templates
- Dynamic class binding ([class], [ngClass])
- Responsive design patterns
- PurgeCSS configuration
- Tailwind directives with Angular
- Component library conflicts
**Purpose**: Ensure proper Tailwind integration with Angular

#### **primeng_patterns.md**
**Load When**: Project uses PrimeNG components (detected in imports or templates)
**Contains**:
- PrimeNG component API best practices
- Table component optimization
- Form components with reactive forms
- Theme customization
- Accessibility (ARIA attributes)
- Performance with large data sets
**Purpose**: Ensure proper PrimeNG component usage

#### **security_patterns.md**
**Load When**: Reviewing security-sensitive code (auth, API calls, user input, routing)
**Contains**:
- XSS prevention (template security, DomSanitizer)
- Authentication and authorization (guards, JWT)
- HTTP interceptor security
- CSRF protection
- Injection prevention
- Sensitive data exposure
- Unvalidated redirects
**Purpose**: Identify and prevent security vulnerabilities

---

## Quick Reference: Loading Patterns by Scenario

### Scenario 1: First Review of New Project
**Load Order**:
1. `context_detection.md` - Identify tech stack
2. `common_issues.md` - Universal problems
3. Based on detection results, load relevant pattern files

### Scenario 2: Component Review
**Load**:
1. `common_issues.md`
2. `component_patterns.md`
3. `rxjs_patterns.md` (if observables used)
4. `performance_patterns.md` (if performance-critical)
5. `primeng_patterns.md` (if PrimeNG components used)
6. `tailwind_patterns.md` (if Tailwind classes used)

### Scenario 3: Service Review
**Load**:
1. `common_issues.md`
2. `service_patterns.md`
3. `rxjs_patterns.md`
4. `typescript_patterns.md`
5. `security_patterns.md` (if auth/API service)

### Scenario 4: State Management Review
**Load**:
1. `common_issues.md`
2. `ngrx_patterns.md`
3. `rxjs_patterns.md`
4. `typescript_patterns.md`

### Scenario 5: Security Audit
**Load**:
1. `security_patterns.md`
2. `../../security/security_guidelines.md`
3. `component_patterns.md` (for template security)
4. `service_patterns.md` (for API security)

### Scenario 6: Performance Optimization
**Load**:
1. `performance_patterns.md`
2. `component_patterns.md` (for change detection)
3. `rxjs_patterns.md` (for observable optimization)
4. `ngrx_patterns.md` (if state management is bottleneck)

---

## Integration with Other Context Domains

Angular context should be used in conjunction with:

### Security Context (`../security/`)
- **Load together when**: Reviewing authentication, authorization, user input, API calls
- **Primary**: `../security/security_guidelines.md`
- **Secondary**: `../security/index.md` (for navigation)

### Git Context (`../git/`)
- **Load together when**: Understanding diff patterns for review
- **Primary**: Used by `skill:get-git-diff` automatically
- **Rarely needed**: Direct loading by angular-code-review skill

---

## Evolution and Maintenance

### When to Update Context Files
- **Angular version updates**: New features, deprecated APIs
- **Security vulnerabilities discovered**: OWASP updates, new attack vectors
- **Framework best practices change**: Official Angular guidance updates
- **Common patterns emerge**: Across multiple projects

### What NOT to Put in Context
- Project-specific patterns → goes in `../../memory/skills/angular-code-review/{project-name}/`
- Temporary workarounds → goes in project memory as "known_issues"
- Team conventions → goes in project memory as "common_patterns"
- One-off solutions → not documented (only recurring patterns)

---

## Context File Standards

All context files in this directory follow these standards:

1. **Markdown Format**: Clear headings, code examples, references
2. **Anchors for Sections**: Use `## Section Title {#section-anchor}` for direct references
3. **Code Examples**: TypeScript/HTML examples for every pattern
4. **Anti-Patterns**: Show both good and bad examples
5. **External References**: Link to official Angular docs, OWASP, etc.
6. **Searchable**: Use consistent terminology for easy grepping

---

## Token Efficiency

**Loading Strategy**:
- **Index files (like this one)**: ~1-2KB → Always load first
- **Targeted context files**: ~5-10KB → Load only what's needed
- **Full context load**: ~50KB+ → Avoid unless comprehensive review

**Efficiency Tips**:
- Read index files first to determine relevance
- Load files progressively based on findings
- Reference sections by anchor (don't load entire file if not needed)
- Use decision matrix above to minimize unnecessary loading

---

## Related Documentation

- **Main Context Index**: `../index.md` - Overview of all context domains
- **Memory System**: `../../memory/index.md` - Project-specific learning
- **Angular Memory Index**: `../../memory/skills/angular-code-review/index.md` - Memory structure
- **Skill Documentation**: `../../skills/angular-code-review/SKILL.md` - Workflow and usage

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-01-14
**Angular Versions Covered**: 2-18+
**Maintained By**: forge-plugin angular-code-review skill

---

## Quick Start for Claude

When executing `skill:angular-code-review`:

1. **Step 1**: Get changed files from `skill:get-git-diff`
2. **Step 2**: Read THIS file (`index.md`) to understand available context
3. **Step 3**: Read `context_detection.md` if first review or framework unclear
4. **Step 4**: Use decision matrix above to determine which files to load
5. **Step 5**: Load ONLY relevant files (not everything)
6. **Step 6**: Perform review referencing loaded context
7. **Step 7**: Cite context files in review findings using relative paths

**Example Reference in Review**:
```
**Reference**: ../../context/angular/rxjs_patterns.md#subscription-management
```
