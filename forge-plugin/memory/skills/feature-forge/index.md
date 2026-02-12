# feature-forge Memory

Project-specific memory for feature development patterns, implementation conventions, and delivery checklists.

## Purpose

This memory helps the `skill:feature-forge` remember:
- Which architectural patterns and conventions each project follows
- Implementation standards for code structure, naming, and testing
- Delivery checklist items that are project-specific quality gates
- Feature development patterns that have proven effective

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `feature_patterns.md`

**Purpose**: Track recurring feature development patterns specific to this project

**Should contain**:
- **Architectural layers**: How the project structures features (controllers, services, repositories, etc.)
- **Common patterns**: Design patterns frequently used (repository, observer, strategy, etc.)
- **Feature structure**: Typical file and directory layout for new features
- **Integration patterns**: How features connect to existing systems (event-driven, direct calls, message queues)
- **Data flow conventions**: Standard patterns for request → processing → response

**Example structure**:
```markdown
# Feature Patterns - MyProject

## Architectural Layers
Features follow a 4-layer pattern:
- Router/Controller (input validation, HTTP concerns)
- Service (business logic, orchestration)
- Repository (data access, queries)
- Schema/Model (data structures, validation)

## Common Design Patterns
- Repository pattern for all data access
- Strategy pattern for interchangeable algorithms
- Observer/event pattern for cross-cutting concerns
- Factory pattern for complex object creation

## Typical Feature Structure
```
src/features/{feature-name}/
├── router.py
├── service.py
├── repository.py
├── schemas.py
├── models.py
├── events.py (if event-driven)
└── tests/
    ├── test_service.py
    └── test_router.py
```

## Integration Patterns
- Domain events dispatched via EventBus for cross-feature communication
- Direct service injection for same-domain operations
- REST API calls for external service integration

## Recent Features Built
- User Preferences (2026-01-15): 4-layer, 12 files, repository + observer
- Billing Integration (2026-01-28): 4-layer, 18 files, strategy + adapter
```

**When to update**: After each feature development session, if new patterns emerge

---

#### `implementation_conventions.md`

**Purpose**: Document project's coding standards and implementation conventions

**Should contain**:
- **Language and framework**: Primary tech stack and version constraints
- **Naming conventions**: Files, functions, classes, variables, database columns
- **Directory structure**: Where new code should live
- **Testing standards**: Framework, coverage thresholds, test naming patterns
- **Code style**: Formatting rules, import ordering, documentation standards
- **Error handling**: How errors are structured, logged, and returned to clients

**Example structure**:
```markdown
# Implementation Conventions - MyProject

## Tech Stack
- Python 3.12+ with FastAPI
- PostgreSQL 16 with SQLAlchemy 2.0
- React 18 with TypeScript 5.x
- Pydantic v2 for validation

## Naming Conventions
- Files: snake_case (Python), camelCase (TypeScript)
- Classes: PascalCase
- Functions: snake_case (Python), camelCase (TypeScript)
- Database tables: snake_case, plural (e.g., `user_preferences`)
- API endpoints: kebab-case (e.g., `/api/user-preferences`)

## Testing
- Framework: pytest (backend), Vitest (frontend)
- Coverage threshold: 80% minimum per module
- Test naming: `test_{method}_{scenario}_{expected_result}`
- Integration tests use TestClient with real database

## Error Handling
- All errors return structured JSON: { "detail": "...", "code": "..." }
- Business errors use custom exception classes
- Unhandled errors logged with full stack trace
```

**When to update**: When conventions change or new standards are adopted

---

#### `delivery_checklist.md`

**Purpose**: Track project-specific quality gates and deployment requirements

**Should contain**:
- **Pre-merge checklist**: Steps required before a PR can be merged
- **Testing requirements**: What tests must pass, coverage thresholds
- **Documentation requirements**: What docs must be updated with each feature
- **Deployment steps**: Environment-specific deployment procedures
- **Rollback plan**: How to revert a feature if issues arise in production
- **Monitoring**: What to watch after a feature ships

**Example structure**:
```markdown
# Delivery Checklist - MyProject

## Pre-Merge
- [ ] All unit and integration tests pass
- [ ] Code coverage meets 80% threshold
- [ ] Linting passes with zero warnings
- [ ] Type checking passes (mypy/tsc)
- [ ] At least 1 code review approval
- [ ] API documentation updated (OpenAPI spec)
- [ ] Changelog entry added

## Deployment
- [ ] Database migrations tested on staging
- [ ] Environment variables documented and configured
- [ ] Feature flag created (if gradual rollout)
- [ ] Monitoring alerts configured for new endpoints
- [ ] Load test passed for performance-sensitive features

## Post-Deploy
- [ ] Smoke test core user flows
- [ ] Monitor error rates for 24 hours
- [ ] Verify metrics collection for new feature
- [ ] Update feature flag to 100% after validation

## Rollback
- Feature flag: Set to 0% to disable instantly
- Database: Reversible migrations required for all schema changes
- Code: Revert PR and redeploy from main branch
```

**When to update**: When deployment processes change or new quality gates are added

---

## Usage in skill:feature-forge

### Loading Memory

```markdown
# In skill workflow Step 3

project_name = detect_project_name()
memory = memoryStore.getSkillMemory("feature-forge", project_name)

if memory exists:
    feature_patterns = read("feature_patterns.md")
    conventions = read("implementation_conventions.md")
    checklist = read("delivery_checklist.md")

    # Apply to current feature
    - Structure files following feature_patterns
    - Name and style code per conventions
    - Validate delivery against checklist
```

### Updating Memory

```markdown
# In skill workflow Step 5 (Review & Output)

After completing feature implementation:

1. Check if new patterns emerged:
   - Did the feature introduce a new architectural pattern?
   - Were new conventions established?
   - Did the delivery checklist need new items?

2. If yes, update relevant memory file:
   memoryStore.update("feature-forge", project_name, updates)

3. If first time developing a feature for this project:
   - Create directory and all memory files
   - Populate with observations from this implementation
```

---

## Memory Benefits for Feature Development

### Consistent Architecture

**Without memory**:
> "Created a new feature module with ad-hoc structure"

**With memory**:
> "Created feature module following project's 4-layer pattern (router/service/repository/schema) with event integration, matching the structure used in User Preferences and Billing features"

### Faster Implementation

**Without memory**:
> "Spent time discovering project conventions through trial and error"

**With memory**:
> "Applied known conventions immediately: snake_case files, Pydantic v2 schemas, pytest with 80% coverage target, structured error responses"

### Reliable Delivery

**Without memory**:
> "Feature deployed but missed staging migration test and monitoring setup"

**With memory**:
> "Completed all 12 delivery checklist items including staging migration test, feature flag setup, and monitoring alert configuration"

---

## Memory Lifecycle

### Creation (First Feature)

1. Skill runs on project for first time
2. Develops feature without existing memory
3. Creates `{project-name}/` directory
4. Generates initial memory files based on observations
5. Saves patterns, conventions, and checklist for future use

### Growth (Ongoing Features)

1. Skill runs on subsequent features
2. Loads existing memory
3. Uses memory to ensure consistency and speed
4. Updates memory if new patterns or conventions observed
5. Memory becomes more comprehensive and accurate over time

### Maintenance (Periodic Review)

1. Review memory files every few months
2. Remove outdated patterns or deprecated conventions
3. Consolidate overlapping entries
4. Verify patterns still match current project architecture

---

## Example: Memory Evolution

### After 1st Feature
```markdown
# feature_patterns.md

## Architectural Layers
- Router + Service + Repository observed
- Pydantic schemas for validation

## Recent Features
- User Auth (2026-02-12): 3-layer, 9 files
```

### After 5 Features
```markdown
# feature_patterns.md

## Architectural Layers (Confirmed Pattern)
- Router → Service → Repository → Model (100% of features)
- Events module added for cross-feature features (60%)
- Background workers for async processing (40%)

## Integration Patterns
- EventBus for notifications and audit logging
- Direct injection for same-domain services
- Celery tasks for scheduled/async work

## Recent Features
- User Auth (2026-02-12): 3-layer, 9 files
- Search & Filter (2026-02-20): 3-layer + indexes, 11 files
- Notifications (2026-03-01): 4-layer + workers, 21 files
- Billing (2026-03-15): 4-layer + external adapter, 18 files
- Reports (2026-04-01): 3-layer + Celery worker, 14 files
```

### After 15+ Features
```markdown
# Comprehensive patterns, reliable conventions, battle-tested checklist
# Memory now provides high-value project-specific guidance for any feature
```

---

## Related Documentation

- **Main Memory Index**: `../index.md` for memory system overview
- **Skill Documentation**: `../../skills/feature-forge/SKILL.md` for skill workflow
- **Memory Lifecycle**: `../lifecycle.md` for freshness, pruning, and archival policies
- **Memory Quality**: `../quality_guidance.md` for memory validation standards
