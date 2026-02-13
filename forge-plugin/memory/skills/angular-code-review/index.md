# Angular Code Review - Memory System

This file documents the memory structure for the `angular-code-review` skill. Memory is project-specific knowledge that accumulates over time through repeated reviews.

---

## Purpose

The memory system enables the skill to:
- **Learn project patterns** - Understand project-specific conventions
- **Avoid false positives** - Know documented technical debt
- **Track progress** - See improvements over time
- **Provide context** - Understand architectural decisions
- **Improve accuracy** - Better recommendations based on project history

---

## Memory vs Context

**Memory** (this directory):
- Project-specific
- Dynamic (changes with each review)
- Per-project subdirectories
- Example: "This project uses custom error handling"

**Context** (`../../context/angular/`):
- Universal Angular knowledge
- Static (changes rarely)
- Shared across all projects
- Example: "Angular best practices for change detection"

---

## Memory Structure

```
memory/skills/angular-code-review/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # CRITICAL - Framework, architecture, stack
    ├── common_patterns.md          # Project-specific patterns
    ├── known_issues.md             # CRITICAL - Documented technical debt
    └── review_history.md           # Past reviews and trends
```

---

## Per-Project Memory Files

### 1. project_overview.md (CRITICAL)

**Purpose**: High-level understanding of the project.

**Always Update On First Review**:
- Angular version (e.g., "Angular 17")
- Module system (standalone components vs NgModules)
- State management approach (NgRx, service-based, etc.)
- UI library (PrimeNG, Angular Material, none)
- CSS framework (TailwindCSS, Bootstrap, SCSS)
- TypeScript configuration (strict mode enabled/disabled)
- Project architecture (monorepo, single app, microfrontends)
- Routing strategy (lazy loading, preloading)
- Form approach (reactive, template-driven)
- Testing framework (Jasmine/Karma, Jest)

**Update Incrementally**:
- Add new observations
- Correct misunderstandings
- Document decisions

**Example Structure**:
```markdown
# Project Overview: MyApp

## Framework Stack
- **Angular**: 17.0.2
- **TypeScript**: 5.2.0 (strict mode enabled)
- **RxJS**: 7.8.0

## Architecture
- **Module System**: Standalone components (no NgModules)
- **State Management**: NgRx with Facade pattern
- **UI Library**: PrimeNG 17.x
- **CSS Framework**: TailwindCSS 3.x
- **Forms**: Reactive forms with custom validators

## Project Structure
- Monorepo managed by Nx
- Feature-based module organization
- Shared component library

## Conventions
- OnPush change detection default
- takeUntil pattern for subscriptions
- Facade services for state access
- Path aliases: @app, @shared, @core
```

### 2. common_patterns.md

**Purpose**: Document recurring code patterns specific to this project.

**What to Document**:
- Custom component patterns
- Service organization
- State management patterns
- Error handling approach
- API call patterns
- Form validation patterns
- Naming conventions
- File organization

**Example**:
```markdown
# Common Patterns: MyApp

## Component Patterns

### Loading States
All components use a consistent loading pattern:
\`\`\`typescript
isLoading$ = this.facade.loading$;
error$ = this.facade.error$;
\`\`\`

### Form Components
Forms follow this pattern:
1. Reactive forms with FormBuilder
2. Custom validators in @shared/validators
3. Error messages via shared ErrorMessageComponent
4. Submit with loading state

## Service Patterns

### API Services
All API services extend BaseApiService:
\`\`\`typescript
export class UserService extends BaseApiService<User> {
  constructor(http: HttpClient) {
    super(http, '/api/users');
  }
}
\`\`\`

### Caching
API responses cached using BehaviorSubject pattern.

## Naming Conventions
- Components: `{Feature}{Purpose}Component` (e.g., UserListComponent)
- Services: `{Feature}Service` (e.g., UserService)
- Facades: `{Feature}Facade` (e.g., UserFacade)
- Guards: `{Purpose}Guard` (e.g., AuthGuard)
```

### 3. known_issues.md (CRITICAL)

**Purpose**: Document technical debt and accepted limitations to prevent false positives.

**IMPORTANT**: This file prevents the skill from reporting the same issues repeatedly.

**What to Document**:
- Known technical debt
- Accepted workarounds
- Temporary solutions
- Planned refactoring
- Third-party library limitations

**Example**:
```markdown
# Known Issues: MyApp

## Technical Debt

### 1. Legacy User Service (Documented)
**Location**: `src/app/core/services/user.service.ts`
**Issue**: Uses deprecated HttpClient patterns
**Reason**: Waiting for backend API update
**Planned**: Refactor in Q2 2025
**Ticket**: JIRA-123

### 2. Manual Change Detection in Dashboard
**Location**: `src/app/dashboard/dashboard.component.ts:45`
**Issue**: Uses `ChangeDetectorRef.detectChanges()` manually
**Reason**: Third-party chart library doesn't trigger CD
**Workaround**: Acceptable - documented in component comments

### 3. Any Types in Legacy Code
**Location**: `src/app/legacy/**/*.ts`
**Issue**: Multiple `any` types
**Reason**: Legacy code not yet refactored
**Planned**: Gradual migration to strict types

## Accepted Limitations

### PrimeNG Table Performance
Virtual scrolling disabled due to PrimeNG bug #1234.
Using pagination instead. Acceptable tradeoff.

### RxJS Subscription in ngAfterViewInit
Component X requires data load in ngAfterViewInit due to ViewChild dependencies.
This is intentional and correct for this use case.
```

### 4. review_history.md

**Purpose**: Track review trends and progress over time.

**What to Document**:
- Summary of each review
- Key findings
- Trends (improving, declining, stable)
- Recurring issues
- Positive progress

**Example**:
```markdown
# Review History: MyApp

## 2025-01-14 - Feature/user-dashboard Review
**Scope**: User dashboard feature (12 files changed)
**Reviewer**: angular-code-review v1.0.0

### Key Findings
- 2 critical issues (subscription leaks)
- 3 important issues (missing trackBy functions)
- 5 minor suggestions

### Positive
- Good use of OnPush change detection
- Proper NgRx patterns throughout

### Actions Taken
- Fixed subscription leaks
- Added trackBy functions
- Updated known_issues.md with dashboard chart workaround

## 2025-01-10 - Auth System Review
**Scope**: Authentication refactor (8 files)

### Key Findings
- 1 critical security issue (JWT in localStorage)
- Excellent guard implementation

### Actions Taken
- Moved JWT to httpOnly cookie
- Documented auth patterns in common_patterns.md

## Trends
- **Subscription Management**: Improving (fewer leaks each review)
- **Type Safety**: Stable (strict mode consistently applied)
- **Performance**: Improving (OnPush adoption increasing)
```

---

## Workflow

### First Review of a Project

1. **Check for existing memory**: Does `{project-name}/` directory exist?
2. **If NO**: Create memory directory and all 4 files
3. **If YES**: Load existing memory files

### Subsequent Reviews

1. **Load all existing memory files** (Step 2 of skill workflow)
2. **Use memory to inform review** (understand project context)
3. **After review**: Update ALL memory files with new insights

---

## Memory Update Guidelines

### project_overview.md Updates
- **First review**: Create comprehensive overview
- **Subsequent reviews**: Add new tech stack items, correct misunderstandings
- **Update when**: New libraries added, architecture changes

### common_patterns.md Updates
- **Add patterns** observed in this review
- **Don't remove patterns** unless no longer used
- **Refine patterns** if understanding improves

### known_issues.md Updates (CRITICAL)
- **Add new known issues** identified in this review
- **Remove resolved issues** when fixed
- **Update status** of ongoing issues
- **This prevents false positives** in future reviews

### review_history.md Updates
- **Always add entry** after each review
- **Summarize findings** briefly
- **Note trends** over time
- **Track progress** toward improvements

---

## Benefits of Memory System

1. **Prevents False Positives**
   - Knows about documented technical debt
   - Won't report known issues repeatedly

2. **Contextual Recommendations**
   - Understands project conventions
   - Suggests improvements that fit project style

3. **Tracks Progress**
   - Shows improvement trends
   - Identifies recurring problems

4. **Onboarding**
   - New team members learn project patterns
   - Documents architectural decisions

5. **Efficiency**
   - Faster reviews (context already loaded)
   - More accurate (understands project)

---

## Memory File Size

**Keep memory files concise**:
- project_overview.md: ~200-400 lines
- common_patterns.md: ~300-500 lines
- known_issues.md: ~200-400 lines
- review_history.md: ~50 lines per review, summarize if >1000 lines

**If memory grows too large**:
- Archive old review history
- Consolidate similar patterns
- Remove resolved known issues

---

## Example Project Memory

See `example-project/` directory for reference implementation.

---

## Related Documentation

- **Skill Workflow**: `../../skills/angular-code-review/SKILL.md`
- **Context System**: `../../context/angular/index.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 0.3.0-alpha
**Last Updated**: 2025-01-14
