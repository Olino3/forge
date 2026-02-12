---
name: angular-architect
description: "Enterprise Angular application architecture and patterns. Design scalable, maintainable Angular apps with modular architecture, state management strategies, lazy loading, micro-frontends, and monorepo patterns."
version: "1.0.0"
context:
  primary_domain: "angular"
  always_load_files: []
  detection_required: true
  file_budget: 6
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, architecture_decisions.md, module_map.md, patterns_catalog.md]
    - type: "shared-project"
      usage: "reference"
tags: [angular, architecture, enterprise, patterns, modules, state-management, lazy-loading, monorepo, micro-frontends, standalone-components]
---

# skill:angular-architect — Enterprise Angular Architecture & Patterns

## Version: 1.0.0

## Purpose

Design and implement scalable enterprise Angular application architectures. This skill guides decisions on module organization, state management strategy, component hierarchy, lazy loading, micro-frontend boundaries, monorepo structure (Nx/Turborepo), and standalone component migration. Use when starting new Angular projects, refactoring existing architectures, or evaluating architectural trade-offs.

## File Structure

```
skills/angular-architect/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather inputs: project type, team size, expected scale, existing codebase (if any)
- Detect Angular version (standalone components vs NgModules)
- Determine monorepo usage (Nx, Turborepo, Angular CLI workspaces)
- Identify current state management (NgRx, NGXS, Akita, Elf, signals-based, service-based)
- Identify UI component library (Angular Material, PrimeNG, Taiga UI, custom)
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="angular-architect"` and `domain="angular"`.

Load per-project memory files if they exist:
- `project_overview.md` — Framework stack, Angular version, key dependencies
- `architecture_decisions.md` — ADRs and rationale for past choices
- `module_map.md` — Module/library boundaries and dependency graph
- `patterns_catalog.md` — Established patterns in this project

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `angular` domain. Stay within the file budget declared in frontmatter.

**Always Load**:
- `contextProvider.getConditionalContext("angular", "common_issues")` — Universal Angular problems

**Load Based on Detection**:
- **Standalone migration** → `contextProvider.getConditionalContext("angular", "component_patterns")`
- **State management** → `contextProvider.getConditionalContext("angular", "ngrx_patterns")`
- **Service architecture** → `contextProvider.getConditionalContext("angular", "service_patterns")`
- **Performance concerns** → `contextProvider.getConditionalContext("angular", "performance_patterns")`
- **TypeScript architecture** → `contextProvider.getConditionalContext("angular", "typescript_patterns")`

### Step 4: Architectural Assessment

Evaluate the project across these architectural dimensions:

1. **Module Organization**
   - Feature modules vs domain modules vs shared modules
   - Standalone components migration path (Angular 15+)
   - Library boundaries in monorepo setups
   - Circular dependency detection and resolution

2. **State Management Strategy**
   - Global state (NgRx/NGXS/Akita/Elf) vs local component state
   - Signal-based reactive state (Angular 16+)
   - Server state vs client state separation
   - State hydration for SSR/SSG

3. **Component Architecture**
   - Smart (container) vs presentational (dumb) component separation
   - Component communication patterns (Input/Output, services, state)
   - Component granularity and reusability
   - Dynamic component loading patterns

4. **Routing & Lazy Loading**
   - Route-based code splitting
   - Preloading strategies (PreloadAllModules, custom)
   - Guard architecture (functional guards in Angular 15+)
   - Resolver patterns and data prefetching

5. **Dependency Injection Architecture**
   - Provider scope hierarchy (root, module, component)
   - Multi-provider patterns
   - Injection token design
   - Abstract service patterns for testability

6. **Scalability Patterns**
   - Micro-frontend boundaries (Module Federation, Native Federation)
   - Monorepo library architecture (Nx buildable/publishable libs)
   - Shared component libraries
   - API layer abstraction

7. **Build & Deploy Architecture**
   - Build optimization (budgets, tree-shaking, chunk strategy)
   - Environment configuration
   - CI/CD pipeline considerations
   - SSR/SSG with Angular Universal or Analog

### Step 5: Generate Architectural Recommendations

Produce actionable recommendations including:
- Architecture diagrams (described in text/mermaid)
- Module/library dependency graph
- Migration path for incremental adoption
- Decision records (ADRs) for key choices
- Risk assessment for proposed changes

### Step 6: Generate Output

- Save output to `/claudedocs/angular-architect_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`

### Step 7: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="angular-architect"`. Store any newly learned patterns, conventions, or project insights.

Update per-project memory:
- **project_overview.md**: Angular version, dependencies, team size, scale
- **architecture_decisions.md**: ADRs from this session's recommendations
- **module_map.md**: Updated module/library boundaries
- **patterns_catalog.md**: New patterns introduced or validated

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] All 7 architectural dimensions assessed (Step 4)
- [ ] Recommendations include migration path (Step 5)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 7)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — enterprise Angular architecture patterns |
