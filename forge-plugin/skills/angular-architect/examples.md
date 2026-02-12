# Angular Architect — Usage Examples

This document provides practical examples of how to use the `angular-architect` skill in various scenarios.

---

## Example 1: Greenfield Enterprise Application Setup

**Scenario**: Starting a new enterprise Angular application for a large team

**Command**:
```
skill:angular-architect

We're starting a new Angular app for our internal HR portal. Team of 12 developers, expected to grow. Need to support micro-frontends in the future. Using Angular 18.
```

**What Happens**:
1. Skill detects greenfield project with Angular 18
2. Loads engineering context for architecture patterns
3. No existing memory — asks Socratic questions about requirements
4. Assesses all 7 architectural dimensions:
   - Recommends standalone components (no NgModules) for Angular 18
   - Proposes Nx monorepo with buildable libraries
   - Recommends NgRx with Facade pattern for state management
   - Designs lazy-loaded route-per-feature structure
   - Plans Module Federation boundaries for future micro-frontends
5. Generates architecture document with diagrams and ADRs
6. Creates initial project memory

**Expected Output**:
- Module/library dependency diagram (Mermaid)
- Nx workspace structure recommendation
- State management architecture (global vs local)
- Route hierarchy with lazy loading strategy
- 5+ Architecture Decision Records (ADRs)
- Migration path for adding micro-frontends later

---

## Example 2: NgModule to Standalone Component Migration

**Scenario**: Migrating a large Angular 15 app from NgModules to standalone components

**Command**:
```
skill:angular-architect

We have a large Angular 15 app (200+ components) using NgModules. We want to migrate to standalone components incrementally. What's the safest migration path?
```

**What Happens**:
1. Loads project memory (Angular 15, NgModule-based)
2. Detects module dependency graph from existing architecture
3. Assesses migration complexity per module
4. Produces phased migration plan:
   - Phase 1: Leaf components (no dependencies) → standalone
   - Phase 2: Shared module components → standalone with importProvidersFrom
   - Phase 3: Feature modules → standalone with route providers
   - Phase 4: Remove NgModules, update bootstrapApplication
5. Identifies breaking changes and risk areas
6. Updates architecture decisions memory

**Expected Output**:
- Component dependency analysis
- Migration priority matrix (low-risk → high-risk)
- Step-by-step migration for each phase
- Code examples for bootstrapApplication transition
- Testing strategy for validating each phase
- Rollback plan for each phase

---

## Example 3: State Management Architecture Review

**Scenario**: Evaluating whether to adopt NgRx or switch to signals-based state management

**Command**:
```
skill:angular-architect

Our Angular 17 app uses a mix of BehaviorSubject services and some NgRx stores. It's getting messy. Should we standardize on NgRx, move to signals, or use something else?
```

**What Happens**:
1. Loads project memory for existing state management patterns
2. Analyzes current state management usage across the codebase
3. Evaluates options against project requirements:
   - **Full NgRx**: Best for complex async flows, time-travel debugging, team consistency
   - **Signals + simple stores**: Best for simpler state, less boilerplate, Angular-native
   - **NgRx + SignalStore**: Hybrid approach with NgRx for global, signals for local
4. Considers team experience and migration cost
5. Produces recommendation with migration path

**Expected Output**:
- Current state analysis (what's using what)
- Comparison matrix: NgRx vs Signals vs Hybrid
- Recommended approach with rationale
- Migration plan from BehaviorSubject services
- Code examples for the recommended pattern
- ADR documenting the decision

---

## Example 4: Monorepo Architecture with Nx

**Scenario**: Restructuring a single Angular CLI workspace into an Nx monorepo

**Command**:
```
skill:angular-architect

We need to restructure our Angular 17 app into an Nx monorepo. We have a customer portal, admin dashboard, and shared component library. Multiple teams will own different parts.
```

**What Happens**:
1. Analyzes existing project structure and team boundaries
2. Designs Nx workspace architecture:
   - `apps/customer-portal` — Customer-facing SPA
   - `apps/admin-dashboard` — Internal admin tool
   - `libs/shared/ui` — Shared component library (publishable)
   - `libs/shared/data-access` — Shared API services
   - `libs/shared/util` — Shared utilities
   - `libs/customer/feature-*` — Customer domain features
   - `libs/admin/feature-*` — Admin domain features
3. Defines module boundary rules (enforce-module-boundaries)
4. Sets up build pipeline with affected commands

**Expected Output**:
- Nx workspace structure diagram
- Library categorization (feature, ui, data-access, util)
- Module boundary rules configuration
- Team ownership mapping
- CI/CD pipeline using Nx affected
- Migration steps from Angular CLI to Nx

---

## Example 5: Performance Architecture Audit

**Scenario**: An Angular app has poor initial load times and needs architectural improvements

**Command**:
```
skill:angular-architect

Our Angular 16 app takes 8 seconds to load on mobile. Bundle size is 2.5MB. We need architectural changes to improve performance.
```

**What Happens**:
1. Loads project memory for existing architecture
2. Analyzes architectural performance bottlenecks:
   - Bundle composition and chunk strategy
   - Lazy loading opportunities
   - SSR/SSG potential
   - Change detection architecture
3. Produces performance-focused architecture recommendations
4. Prioritizes changes by impact vs effort

**Expected Output**:
- Bundle analysis interpretation
- Lazy loading route redesign
- Preloading strategy recommendation
- SSR/SSG feasibility assessment
- Change detection optimization plan (OnPush migration)
- Tree-shaking improvements (import patterns)
- Target metrics and measurement plan

---

## Common Usage Patterns

### Pattern 1: Architecture Review
```
skill:angular-architect
Review our current Angular architecture and suggest improvements
```
Use for periodic architectural health checks.

### Pattern 2: Migration Planning
```
skill:angular-architect
Plan the migration from Angular 15 to Angular 18
```
Use when planning major version upgrades.

### Pattern 3: New Feature Architecture
```
skill:angular-architect
Design the architecture for adding real-time collaboration to our app
```
Use when a new feature requires architectural decisions.

### Pattern 4: Team Scaling
```
skill:angular-architect
How should we restructure our app to support 3 independent teams?
```
Use when team growth requires architectural boundaries.

---

## When to Use This Skill

**Ideal Scenarios**:
- Starting a new enterprise Angular project
- Migrating between Angular architectures (NgModules → standalone)
- Evaluating state management strategies
- Restructuring for team scaling (monorepo)
- Performance architecture optimization
- Micro-frontend boundary design

**Not Ideal For**:
- Single-component code review (use `skill:angular-code-review`)
- Unit test generation (use `skill:generate-jest-unit-tests`)
- Quick bug fixes or small feature implementations
