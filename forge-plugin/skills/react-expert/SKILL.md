---
name: react-expert
description: "Advanced React patterns, hooks, and architecture. Build production-grade React applications with modern patterns including Server Components, Suspense, concurrent features, and performance optimization."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 5
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, component_patterns.md, hooks_catalog.md, performance_profile.md]
    - type: "shared-project"
      usage: "reference"
## tags: [react, hooks, architecture, patterns, server-components, suspense, concurrent, performance, state-management, typescript]

# skill:react-expert — Advanced React Patterns, Hooks & Architecture

## Version: 1.0.0

## Purpose

Build and architect production-grade React applications using advanced patterns and modern features. This skill covers React 18/19 features (Server Components, Actions, Suspense, concurrent rendering), custom hook design, state management architecture (Zustand, Jotai, TanStack Query, Redux Toolkit), performance optimization, and component composition patterns. Use when building new React apps, reviewing React code, designing component libraries, or optimizing rendering performance.

## File Structure

```
skills/react-expert/
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

- Gather inputs: project type, React version, framework (Next.js, Remix, Vite, CRA)
- Detect React version features (Server Components, Actions, use() hook, useOptimistic)
- Identify state management (Zustand, Jotai, Redux Toolkit, TanStack Query, React Context)
- Identify styling approach (Tailwind, CSS Modules, styled-components, vanilla-extract)
- Detect TypeScript usage and strictness level
- Determine bundler (Vite, Webpack, Turbopack, Rspack)
- Identify project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="react-expert"` and `domain="engineering"`.

Load per-project memory files if they exist:
- `project_overview.md` — React version, framework, key dependencies
- `component_patterns.md` — Established component patterns and conventions
- `hooks_catalog.md` — Custom hooks library and usage patterns
- `performance_profile.md` — Known performance characteristics and optimizations

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: React Development Core

Apply expert-level React guidance across these dimensions:

1. **Component Patterns**
   - Compound components for flexible APIs
   - Render props and children-as-function patterns
   - Higher-order components (when still appropriate)
   - Polymorphic components with TypeScript (`as` prop)
   - Headless component pattern for logic reuse
   - Controlled vs uncontrolled components
   - Error boundaries with recovery strategies

2. **Hooks Architecture**
   - Custom hook design principles (single responsibility, composability)
   - useReducer for complex state logic
   - useSyncExternalStore for external store subscriptions
   - useTransition and useDeferredValue for concurrent rendering
   - useOptimistic for optimistic UI updates (React 19)
   - use() for promise/context reading (React 19)
   - Hook dependency management and stale closure prevention

3. **Server Components & Actions (React 19+)**
   - Server Component vs Client Component boundaries
   - "use server" and "use client" directives
   - Server Actions for form mutations
   - Streaming and Suspense for data loading
   - Serialization boundaries and prop constraints

4. **State Management**
   - **Zustand**: Store design, middleware (persist, devtools, immer), slices pattern
   - **Jotai**: Atomic state, derived atoms, async atoms
   - **TanStack Query**: Server state caching, optimistic updates, prefetching
   - **Redux Toolkit**: Slices, RTK Query, entity adapter
   - Selection criteria based on state scope and complexity

5. **Performance Optimization**
   - React.memo and useMemo/useCallback — when they help vs hurt
   - React Compiler (React 19) automatic memoization
   - Code splitting with React.lazy and Suspense
   - Virtualization for large lists (TanStack Virtual, react-window)
   - Bundle analysis and tree shaking
   - Profiler API for render measurement
   - Image optimization patterns

6. **TypeScript Integration**
   - Generic component patterns
   - Discriminated unions for component variants
   - Strict event handler typing
   - Utility types for props (ComponentProps, PropsWithChildren)
   - Type-safe context and custom hooks
   - Satisfies operator for configuration objects

7. **Testing Strategy**
   - React Testing Library best practices (user-centric testing)
   - Component integration testing
   - Hook testing with renderHook
   - MSW for API mocking
   - Playwright/Cypress for E2E
   - Vitest configuration for React projects

### Step 5: Generate Output

- Save output to `/claudedocs/react-expert_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="react-expert"`. Store any newly learned patterns, conventions, or project insights.

Update per-project memory:
- **project_overview.md**: React version, framework, key libs, TypeScript config
- **component_patterns.md**: Established patterns, component conventions
- **hooks_catalog.md**: Custom hooks documented with usage examples
- **performance_profile.md**: Performance baselines, optimizations applied

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] React version and framework detected (Step 1)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — advanced React patterns and architecture |
