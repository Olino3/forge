---
name: feature-forge
description: Orchestrates the complete feature development lifecycle from requirements analysis through delivery. Evaluates scope, plans architecture, drives incremental implementation with quality gates, and ensures documentation alignment. Like Hephaestus forging a new weapon from raw ore, this skill transforms user stories into well-crafted, production-ready features with deliberate structure and masterful precision.
---

# Feature Development Forge

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY feature development engagement. Skipping steps or deviating from the procedure will result in incomplete implementations, missed requirements, or poor integration. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different feature types and generated outputs
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("feature-forge", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **ContextProvider**: Load domain knowledge via `contextProvider.getIndex("{domain}")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **MemoryStore**: Read/write project memory via `memoryStore.getSkillMemory("feature-forge", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **Schemas**: Validate configurations against `agent_config.schema.json`, `context_metadata.schema.json`, `memory_entry.schema.json`. See [Interface Schemas](../../interfaces/schemas/).

## Focus Areas

Feature development workflow evaluates 7 critical dimensions:

1. **Requirements Analysis**: Understand user stories, acceptance criteria, edge cases, and non-functional requirements to establish a clear definition of done
2. **Architecture Planning**: Design component structure, identify integration points, define data flow, and select appropriate design patterns for the feature
3. **Implementation Strategy**: Plan branching strategy, incremental delivery milestones, TDD approach, and task decomposition for manageable progress
4. **Code Quality Gates**: Enforce linting standards, test coverage thresholds, review checklists, and static analysis before code advances through the pipeline
5. **Integration Validation**: Verify API contracts, backward compatibility, cross-service communication, and end-to-end data integrity
6. **Documentation Alignment**: Ensure feature documentation, changelog entries, API docs, and inline comments stay synchronized with implementation
7. **Delivery Orchestration**: Coordinate PR strategy, deployment readiness checks, feature flag configuration, and rollback planning

**Note**: The skill guides the full lifecycle from requirements to delivery. It does not replace project management tools but ensures technical completeness at every stage.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Analyze Feature Requirements (REQUIRED)

**YOU MUST:**
1. Gather the feature scope from the user prompt, issue description, or specification document
2. Identify acceptance criteria — what must be true for this feature to be considered complete
3. List functional and non-functional requirements (performance, security, accessibility)
4. Map dependencies on existing code, services, or third-party integrations
5. Identify edge cases, failure modes, and boundary conditions
6. Clarify ambiguities — ask the user targeted questions if requirements are unclear

**DO NOT PROCEED WITHOUT A CLEAR UNDERSTANDING OF WHAT THE FEATURE MUST DO**

### ⚠️ STEP 2: Plan Implementation Architecture (REQUIRED)

**YOU MUST:**
1. Identify components that need to be created or modified (models, services, controllers, UI)
2. Select appropriate design patterns (repository, factory, observer, strategy, etc.)
3. Define data flow from input to persistence and back to output
4. Plan the API surface — endpoints, request/response schemas, error responses
5. Assess impact on existing architecture — identify modules that will change
6. Document integration points with external systems or internal services
7. Determine the branching strategy (feature branch, feature flags, trunk-based)

**DO NOT PROCEED WITHOUT AN ARCHITECTURAL PLAN**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. Load project memory using `memoryStore.getSkillMemory("feature-forge", "{project-name}")`
2. Review `feature_patterns.md` for recurring patterns and conventions in this project
3. Review `implementation_conventions.md` for coding standards, naming conventions, and directory structure
4. Review `delivery_checklist.md` for project-specific quality gates and deployment requirements
5. If no memory exists, proceed without it — memory will be created in Step 5
6. Apply loaded conventions to the architecture plan from Step 2

See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 4: Implement Feature (REQUIRED)

**YOU MUST follow this implementation sequence:**
1. **Scaffolding**: Create file structure, stubs, interfaces, and type definitions
2. **Core Logic**: Implement business logic with unit tests following TDD where appropriate
3. **Integration Layer**: Wire components together — routes, dependency injection, event handlers
4. **Tests**: Write unit tests, integration tests, and edge case tests to meet coverage thresholds
5. **Documentation**: Update API docs, add inline comments for complex logic, update changelog
6. **Quality Checks**: Run linting, type checking, and existing test suites to ensure no regressions

**DO NOT SKIP TESTS OR DOCUMENTATION**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST:**
1. **Validate against acceptance criteria**: Verify every acceptance criterion from Step 1 is met
2. **Run integration validation**: Confirm API contracts, backward compatibility, and data integrity
3. **Generate output**: Write feature summary and implementation report to `/claudedocs/` following [OUTPUT_CONVENTIONS.md](../OUTPUT_CONVENTIONS.md)
4. **Update project memory**: Use `memoryStore.update("feature-forge", "{project-name}", ...)` to store:
   - Feature patterns discovered during implementation
   - Conventions established or reinforced
   - Delivery checklist items that proved valuable
5. **Present summary** to the user with:
   - Files created and modified
   - Test coverage summary
   - Remaining tasks or follow-up items
   - Deployment considerations

See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

**DO NOT SKIP VALIDATION OR MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY feature development engagement, verify:
- [ ] Step 1: Requirements analyzed — scope, acceptance criteria, and dependencies documented
- [ ] Step 2: Architecture planned — components, patterns, data flow, and integration points defined
- [ ] Step 3: Project memory loaded and conventions applied
- [ ] Step 4: Feature implemented — scaffolding, logic, tests, and documentation complete
- [ ] Step 5: Output validated, memory updated, and summary presented to user

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE FEATURE IMPLEMENTATION**

---

## Feature Development Lifecycle

```
Requirements ──► Architecture ──► Memory ──► Implementation ──► Review
    │                 │              │              │               │
    ▼                 ▼              ▼              ▼               ▼
 User Stories     Components     Conventions   Scaffolding      Validate
 Acceptance       Patterns       Standards     Core Logic       Output
 Dependencies     Data Flow      Checklist     Tests/Docs       Memory
 Edge Cases       API Surface    History       Quality Gates    Summary
```

Each stage feeds into the next. Memory provides continuity across feature development sessions within the same project.

---

## Output File Naming Convention

**Format**: `feature_{feature_name}_{date}.md`

Where:
- `{feature_name}` = kebab-case name of the feature (e.g., `user-auth`, `search-filter`)
- `{date}` = ISO date in YYYY-MM-DD format

**Examples**:
- `feature_user-auth_2026-02-12.md`
- `feature_search-filter_2026-02-12.md`
- `feature_notification-system_2026-02-12.md`

---

## Further Reading

Refer to official documentation:
- **Feature Development**:
  - Twelve-Factor App: https://12factor.net/
  - Martin Fowler — Feature Toggles: https://martinfowler.com/articles/feature-toggles.html
- **Architecture & Design**:
  - Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
  - Domain-Driven Design Reference: https://www.domainlanguage.com/ddd/reference/
- **Testing & Quality**:
  - Test-Driven Development by Example: https://www.kent-beck.com/
  - The Testing Trophy: https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow for feature development
  - Requirements analysis with acceptance criteria
  - Architecture planning with pattern selection
  - Project memory integration for convention persistence
  - Incremental implementation with quality gates
  - Delivery orchestration with validation and output
