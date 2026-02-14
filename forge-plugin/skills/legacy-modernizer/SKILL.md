---
name: legacy-modernizer
## description: Analyzes and modernizes legacy codebases through systematic technical debt reduction, migration planning, and incremental refactoring strategies. Evaluates code staleness, identifies architectural anti-patterns, maps dependency risks, and produces actionable modernization roadmaps. Like Hephaestus reforging ancient weapons with modern alloys, this skill transforms aging systems into maintainable, performant architectures while preserving battle-tested business logic.

# Legacy Code Modernizer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY legacy modernization task. Skipping steps or deviating from the procedure will result in incomplete analysis, risky migrations, or lost business logic. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different modernization types and strategies
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("legacy-modernizer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **ContextProvider**: Load modernization context via `contextProvider.getIndex("python")`, `contextProvider.getIndex("javascript")`, etc. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **MemoryStore**: Read/write project-specific modernization memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **Schemas**: Validate output against `context_metadata.schema.json` and `memory_entry.schema.json`. See [Schemas](../../interfaces/schemas/).

## Focus Areas

Legacy code modernization evaluates 7 critical dimensions:

1. **Technical Debt Assessment**: Identify code smells (long methods, god classes, deep nesting), measure cyclomatic complexity metrics, evaluate dependency staleness and end-of-life risk across the codebase
2. **Migration Planning**: Apply the strangler fig pattern for incremental modernization, design phased migration roadmaps, perform risk assessment for each migration stage with rollback strategies
3. **Dependency Modernization**: Audit outdated packages and transitive dependencies, identify known security vulnerabilities (CVEs), evaluate version pinning strategies and lockfile hygiene
4. **Code Pattern Evolution**: Transform callbacks to async/await, migrate class-based components to functional paradigms, evolve raw SQL to ORM patterns, upgrade framework-specific idioms to modern equivalents
5. **Testing Infrastructure**: Add tests to untested legacy code using characterization tests, build safety nets before refactoring, establish coverage baselines and regression detection
6. **Architecture Transformation**: Decompose monoliths to microservices, migrate MVC to hexagonal/clean architecture, extract bounded contexts, introduce event-driven patterns where appropriate
7. **Documentation Recovery**: Extract implicit knowledge embedded in code comments and commit history, document tribal knowledge before it is lost, reconstruct missing architectural decision records (ADRs)

**Note**: The skill analyzes existing codebases and produces modernization plans. It does not blindly rewrite — every transformation preserves existing business logic and is validated against characterization tests.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Assess Legacy Codebase (REQUIRED)

**YOU MUST:**
1. Scan the codebase for technical debt indicators:
   - Code smells: long methods (>50 lines), god classes, feature envy, shotgun surgery
   - Complexity metrics: cyclomatic complexity, cognitive complexity, coupling between objects
   - Outdated dependencies: packages behind major versions, deprecated APIs, EOL runtimes
2. Identify the technology stack, framework versions, and language runtime versions
3. Map the dependency tree and flag packages with known security vulnerabilities
4. Assess test coverage — identify untested critical paths and missing test infrastructure
5. Review architectural patterns in use and identify anti-patterns (circular dependencies, tight coupling, shared mutable state)

**DO NOT PROCEED WITHOUT A COMPLETE CODEBASE ASSESSMENT**

### ⚠️ STEP 2: Classify & Prioritize Debt (REQUIRED)

**YOU MUST:**
1. **Categorize each debt item** by type:
   - **Code debt**: Smells, duplication, complexity, naming
   - **Architecture debt**: Coupling, layering violations, missing abstractions
   - **Dependency debt**: Outdated packages, vulnerable libraries, deprecated APIs
   - **Test debt**: Missing tests, flaky tests, inadequate coverage
   - **Documentation debt**: Missing docs, outdated docs, tribal knowledge
   - **Infrastructure debt**: Manual deployments, missing CI/CD, outdated tooling
2. **Score each item** on three axes:
   - **Risk**: What is the probability and impact of this debt causing a production incident? (1-5)
   - **Effort**: How much work is required to address this debt? (1-5, where 1 = trivial, 5 = major project)
   - **Value**: How much does addressing this debt improve maintainability, performance, or developer experience? (1-5)
3. **Create a debt inventory** sorted by priority (high risk + high value + low effort first)
4. **Identify quick wins**: Items that are low effort but high value

**DO NOT PROCEED WITHOUT A PRIORITIZED DEBT INVENTORY**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. Load project-specific memory:
   ```
   memoryStore.getSkillMemory("legacy-modernizer", "{project-name}")
   ```
   See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.
2. If memory exists, review:
   - Previous debt inventory and what has been addressed
   - Migration progress and completed phases
   - Modernization patterns that worked well or failed for this project
3. If no memory exists, this is a first-time assessment — proceed to Step 4
4. Load relevant context for the technology stack:
   ```
   contextProvider.getIndex("{language}")
   contextProvider.getIndex("{framework}")
   ```

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 4: Plan & Execute Modernization (REQUIRED)

**YOU MUST:**
1. **Design the migration plan** based on the prioritized debt inventory:
   - Define clear phases with measurable milestones
   - Apply the appropriate modernization pattern (Strangler Fig, Branch by Abstraction, etc.)
   - Ensure each phase is independently deployable and reversible
2. **Build safety nets first**:
   - Write characterization tests for untested code before modifying it
   - Establish baseline metrics (performance, coverage, error rates)
   - Set up feature toggles for gradual rollout where appropriate
3. **Apply transformations incrementally**:
   - One pattern change at a time — never combine multiple refactoring types in one step
   - Validate behavior preservation after each transformation
   - Keep the system deployable at every intermediate step
4. **Document decisions**: Record why each transformation was chosen and what alternatives were considered

**DO NOT APPLY TRANSFORMATIONS WITHOUT SAFETY NETS**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST:**
1. **Validate all transformations**:
   - Run existing tests to confirm no regressions
   - Run new characterization tests to confirm behavior preservation
   - Verify dependency compatibility after upgrades
2. **Generate output** to `/claudedocs/` following output conventions:
   - Debt inventory report with prioritization
   - Migration plan with phases and milestones
   - Transformation log documenting each change and its rationale
3. **Update project memory**:
   ```
   memoryStore.update("legacy-modernizer", "{project-name}", ...)
   ```
   Store: updated debt inventory, migration progress, patterns that worked, lessons learned.
   See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

**DO NOT SKIP VALIDATION OR MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY legacy modernization task, verify:
- [ ] Step 1: Codebase assessed for tech debt, complexity, dependencies, coverage, and architecture
- [ ] Step 2: Debt classified by type, scored by risk/effort/value, and prioritized into inventory
- [ ] Step 3: Project memory loaded (or confirmed first-time assessment), context loaded for tech stack
- [ ] Step 4: Migration plan designed, safety nets built, transformations applied incrementally
- [ ] Step 5: Transformations validated, output generated to /claudedocs/, memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE MODERNIZATION**

---

## Output File Naming Convention

**Format**: `legacy_mod_{project}_{date}.md`

Where:
- `{project}` = Short project identifier
- `{date}` = ISO date (YYYY-MM-DD)

**Examples**:
- `legacy_mod_webapp_2026-02-12.md` (debt inventory and migration plan)
- `legacy_mod_webapp_migration_log.md` (ongoing transformation log)

---

## Modernization Patterns Reference

### Strangler Fig Pattern
Gradually replace legacy components by building new functionality alongside the old system. Route traffic incrementally to the new implementation until the legacy component can be safely removed.

**When to use**: Large monolithic systems where a full rewrite is too risky. Ideal when you can intercept requests at the edge (API gateway, reverse proxy, routing layer).

### Branch by Abstraction
Introduce an abstraction layer over the code you want to replace. Implement the new version behind the abstraction, then switch the underlying implementation without changing consumers.

**When to use**: Internal components with multiple consumers. Ideal for swapping database layers, service clients, or framework-specific code.

### Parallel Run
Run both the old and new implementations simultaneously, comparing their outputs. Use the old implementation's results while validating the new implementation in shadow mode.

**When to use**: Critical business logic where correctness must be proven before cutover. Financial calculations, data transformations, authorization decisions.

### Feature Toggle
Use feature flags to control which code path executes. Deploy new implementations behind toggles, enabling gradual rollout and instant rollback.

**When to use**: User-facing changes that need controlled rollout. Allows A/B testing of modernized paths and quick rollback if issues arise.

---

## Further Reading

Refer to official documentation and resources:
- **Modernization Strategies**:
  - Working Effectively with Legacy Code (Michael Feathers): https://www.oreilly.com/library/view/working-effectively-with/0131177052/
  - Refactoring (Martin Fowler): https://refactoring.com/
  - Strangler Fig Pattern: https://martinfowler.com/bliki/StranglerFigApplication.html
- **Technical Debt**:
  - Managing Technical Debt (Philippe Kruchten): https://www.sei.cmu.edu/our-work/technical-debt/
  - Code Smells Catalog: https://refactoring.guru/refactoring/smells
- **Testing Legacy Code**:
  - Characterization Tests: https://michaelfeathers.silvrback.com/characterization-testing

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow for legacy code modernization

### Step 1: Initial Analysis

Gather inputs and determine scope and requirements.

### Step 2: Load Memory

Load project-specific memory via MemoryStore interface.

### Step 3: Load Context

Load relevant context files via ContextProvider interface.

### Step 4: Core Implementation

Execute the skill-specific core action.

### Step 5: Generate Output

Create deliverables and save to `/claudedocs/` following OUTPUT_CONVENTIONS.md.

### Step 6: Update Memory

Update project memory with new patterns and decisions.
