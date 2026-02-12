# Vue Expert — Usage Examples

This document provides practical examples of how to use the `vue-expert` skill in various scenarios.

---

## Example 1: Enterprise Vue 3 + TypeScript Architecture

**Scenario**: Architecting a large-scale Vue 3 application with TypeScript

**Command**:
```
skill:vue-expert

We're building an enterprise project management tool with Vue 3.5 and TypeScript. 8 developers, need monorepo, design system, and full test coverage. Using Nuxt 3 for SSR.
```

**What Happens**:
1. Detects Vue 3.5 + TypeScript + Nuxt 3
2. Designs enterprise architecture:
   - Monorepo with pnpm workspaces or Turborepo
   - Nuxt Layers for shared configuration
   - Headless component library package
   - Feature packages with clear boundaries
3. TypeScript-first patterns:
   - Generic components for data tables, forms
   - Typed Pinia stores with setup syntax
   - Type-safe API layer with $fetch
4. Testing architecture with Vitest + Playwright

**Expected Output**:
- Monorepo structure with packages
- Nuxt 3 application configuration
- TypeScript configuration (tsconfig paths, strict mode)
- Design system component library architecture
- Pinia store architecture with TypeScript
- API layer with typed endpoints
- CI/CD pipeline configuration
- Testing strategy (unit, component, E2E)

---

## Example 2: Type-Safe Component Library

**Scenario**: Building a generic component library with Vue 3 and TypeScript

**Command**:
```
skill:vue-expert

Build a type-safe DataTable component that supports generic row types, sortable columns, row selection, and pagination. Must be fully typed with TypeScript generics.
```

**What Happens**:
1. Designs generic component with `<script setup generic="T">`:
   - `DataTable<T>` — main table component
   - Typed column definitions `ColumnDef<T>`
   - Type-safe sort and filter callbacks
   - Generic row selection with Set<T>
2. Implements compound component pattern with TypeScript
3. Provides slot typing for custom cell rendering
4. Handles accessibility (ARIA table roles)

**Expected Output**:
- Generic DataTable component implementation
- TypeScript types/interfaces for all props
- Typed slots (defineSlots) for custom rendering
- Column definition builder utility
- Usage examples with different data types
- Vitest component tests
- Storybook story examples (if applicable)

---

## Example 3: Nuxt 3 Full-Stack with Drizzle ORM

**Scenario**: Building a full-stack Nuxt 3 app with database integration

**Command**:
```
skill:vue-expert

Set up a Nuxt 3 full-stack app with Drizzle ORM, PostgreSQL, authentication, and deploy to Vercel. Need type safety from database to frontend.
```

**What Happens**:
1. Designs full-stack architecture:
   - Nuxt 3 with server routes (Nitro)
   - Drizzle ORM with PostgreSQL (Neon/Supabase)
   - Type-safe API: Drizzle schema → server routes → useFetch
2. Auth implementation:
   - nuxt-auth-utils or better-auth
   - Session management with server middleware
   - Protected routes with route middleware
3. Deployment configuration for Vercel

**Expected Output**:
- Drizzle schema definitions
- Server API routes with typed handlers
- Database migration setup
- Authentication flow (login, register, session)
- Protected route middleware
- useFetch composables with type inference
- Vercel deployment configuration
- Environment variable management

---

## Example 4: Vue 3 Testing Strategy with Vitest

**Scenario**: Setting up comprehensive testing for a Vue 3 TypeScript project

**Command**:
```
skill:vue-expert

Set up a complete testing strategy for our Vue 3 + Pinia + Vue Router app. Need unit tests, component tests, and E2E tests. Using Vitest.
```

**What Happens**:
1. Designs layered testing architecture:
   - Unit tests: Composables, utilities, Pinia stores
   - Component tests: @vue/test-utils with Vitest
   - Integration tests: Multi-component flows
   - E2E tests: Playwright with Page Object Model
2. Configures testing infrastructure:
   - Vitest configuration with Vue plugin
   - Test utilities and helpers
   - MSW for API mocking
   - createTestingPinia for store mocking
3. Provides coverage thresholds and CI integration

**Expected Output**:
- Vitest configuration with coverage
- Test utility setup (render helpers, store mocks)
- Composable testing patterns (renderHook equivalent)
- Component testing examples with user events
- Pinia store testing with createTestingPinia
- MSW handler setup for API mocking
- Playwright E2E test examples
- CI/CD test pipeline configuration
- Coverage threshold recommendations

---

## Example 5: Micro-Frontend with Vue 3

**Scenario**: Implementing micro-frontends with Vue 3 and Module Federation

**Command**:
```
skill:vue-expert

We need to split our monolithic Vue 3 app into micro-frontends. Three teams own different domains: billing, analytics, and user management.
```

**What Happens**:
1. Evaluates micro-frontend approaches:
   - Vite Module Federation (vite-plugin-federation)
   - Single-SPA with Vue 3 parcels
   - Nuxt Layers for lighter isolation
2. Designs federation architecture:
   - Shell app (navigation, auth, shared state)
   - Remote apps per domain
   - Shared dependencies (Vue, Pinia, router)
3. Handles cross-MFE communication:
   - Custom events for loose coupling
   - Shared Pinia store (exposed from shell)
   - Route synchronization

**Expected Output**:
- Module Federation configuration
- Shell app architecture
- Remote app structure per domain
- Shared dependency management
- Cross-MFE communication patterns
- Build and deploy pipeline
- Local development setup
- Testing strategy for federated apps

---

## Common Usage Patterns

### Pattern 1: TypeScript Patterns
```
skill:vue-expert
Show me advanced TypeScript patterns for Vue 3 (generic components, typed provide/inject)
```

### Pattern 2: Full-Stack Nuxt
```
skill:vue-expert
Build a REST API with Nuxt 3 server routes and Drizzle ORM
```

### Pattern 3: Migration
```
skill:vue-expert
Migrate our Vue 2 Options API + Vuex app to Vue 3 Composition API + Pinia
```

### Pattern 4: Enterprise Architecture
```
skill:vue-expert
Design a scalable architecture for a Vue 3 app with 50+ developers
```

---

## When to Use This Skill

**Ideal Scenarios**:
- Vue 3 with TypeScript projects
- Enterprise-scale Vue applications
- Full-stack Nuxt 3 development
- Component library development with generics
- Testing architecture design
- Micro-frontend implementation

**Not Ideal For**:
- Vue 3 JavaScript-only projects (use `skill:vue-expert-js`)
- Vue 2 legacy maintenance
- React or Angular projects
