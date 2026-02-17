---
name: vue-expert
description: "Comprehensive Vue.js application development. Build full-featured Vue.js applications with TypeScript, Composition API, Pinia, Nuxt 3, testing, and enterprise patterns."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 5
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, architecture_patterns.md, type_patterns.md, testing_patterns.md]
    - type: "shared-project"
      usage: "reference"
tags: [vue, vue3, typescript, composition-api, pinia, nuxt3, vitest, vite, enterprise, full-stack]
---

# skill:vue-expert — Comprehensive Vue.js Application Development

## Version: 1.0.0

## Purpose

Build full-featured, enterprise-grade Vue.js applications with TypeScript. This skill encompasses the complete Vue.js ecosystem: Composition API with TypeScript, Pinia state management, Vue Router 4, Nuxt 3 full-stack development, Vitest testing, and enterprise patterns (module federation, monorepos, design systems). Use when building TypeScript-based Vue apps, designing component libraries, setting up full-stack Nuxt applications, or establishing enterprise Vue architectures.

## File Structure

```
skills/vue-expert/
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

- Gather inputs: project scope, Vue version, framework (Nuxt 3, Quasar, standalone Vue)
- Detect TypeScript configuration (strict mode, volar, vue-tsc)
- Identify Composition API vs Options API usage
- Detect state management (Pinia, Vuex 4)
- Identify routing (Vue Router 4, Nuxt file-based routing)
- Detect build tool (Vite, Nuxt, Webpack)
- Determine testing framework (Vitest, Jest, Cypress, Playwright)
- Identify UI library (Vuetify 3, PrimeVue, Radix Vue, Naive UI)
- Determine monorepo setup (Turborepo, Nx, pnpm workspaces)
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="vue-expert"` and `domain="engineering"`.

Load per-project memory files if they exist:
- `project_overview.md` — Vue/Nuxt versions, TypeScript config, key dependencies
- `architecture_patterns.md` — Module structure, layer architecture, conventions
- `type_patterns.md` — TypeScript patterns for Vue: generics, prop types, emits
- `testing_patterns.md` — Testing conventions, mocking strategies, coverage targets

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Vue.js Comprehensive Development

Apply expert-level Vue.js guidance across these dimensions:

1. **TypeScript Integration**
   - `defineProps<T>()` with interface/type literal for typed props
   - `defineEmits<T>()` with call-signature syntax
   - `defineSlots<T>()` for typed slots (3.3+)
   - `defineModel<T>()` for typed v-model (3.4+)
   - Generic components with `<script setup generic="T">`
   - Augmenting global types (ComponentCustomProperties, GlobalComponents)
   - Type-safe provide/inject with InjectionKey
   - Volar and vue-tsc configuration for optimal DX

2. **Advanced Composition API**
   - Composable patterns with TypeScript generics
   - `effectScope()` for grouped effect cleanup
   - `customRef()` for debounced/throttled refs
   - `toValue()` utility for MaybeRefOrGetter
   - `useTemplateRef<T>()` for typed template refs (3.5+)
   - Reactivity transform migration (deprecated → alternatives)
   - SSR-compatible composables (isClient checks)

3. **Pinia with TypeScript**
   - Typed store definitions (setup stores recommended)
   - Store composition with cross-store typing
   - Plugin typing and middleware patterns
   - HMR and devtools integration
   - Serialization for SSR hydration
   - Testing stores in isolation

4. **Nuxt 3 Full-Stack**
   - Server routes with H3/Nitro (defineEventHandler)
   - Type-safe API calls with $fetch and useFetch
   - Server middleware and auth patterns
   - Database integration (Drizzle ORM, Prisma)
   - Nuxt Modules development
   - Deployment targets (Vercel, Cloudflare, Node, static)
   - Nuxt Layers for shared configuration

5. **Enterprise Architecture**
   - Module federation with Vite federation plugin
   - Monorepo library architecture (shared packages)
   - Design system development (headless components)
   - Micro-frontend patterns with Vue
   - Feature flags and progressive rollout
   - Internationalization (vue-i18n, @nuxtjs/i18n)
   - Error tracking and monitoring integration

6. **Testing Strategy**
   - **Vitest**: Configuration, component testing with @vue/test-utils
   - **Component Testing**: Mount options, stubs, mocks, user events
   - **E2E Testing**: Playwright or Cypress with Vue DevTools
   - **Snapshot Testing**: Component render snapshots
   - **Store Testing**: Pinia stores with createTestingPinia
   - **API Testing**: MSW for server route mocking
   - Test coverage configuration and thresholds

7. **Performance & Optimization**
   - Bundle analysis (rollup-plugin-visualizer)
   - Route-level code splitting
   - Component lazy loading and Suspense
   - Image optimization (Nuxt Image, @vueuse/core useImage)
   - SSR/SSG/ISR rendering strategies
   - Edge rendering with Cloudflare Workers
   - Web Vitals monitoring

### Step 5: Generate Output

- Save output to `/claudedocs/vue-expert_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="vue-expert"`. Store any newly learned patterns, conventions, or project insights.

Update per-project memory:
- **project_overview.md**: Vue/Nuxt versions, TypeScript config, key libs
- **architecture_patterns.md**: Module structure, established conventions
- **type_patterns.md**: TypeScript patterns used with Vue
- **testing_patterns.md**: Testing setup, conventions, coverage

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Vue version, TypeScript, and framework detected (Step 1)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — comprehensive Vue.js with TypeScript |
