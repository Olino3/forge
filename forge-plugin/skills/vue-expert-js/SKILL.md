---
name: vue-expert-js
description: "Vue.js 3 Composition API and JavaScript patterns. Build modern Vue applications using Composition API, script setup, composables, and JavaScript-first patterns without TypeScript."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, composable_patterns.md, component_conventions.md, state_patterns.md]
    - type: "shared-project"
      usage: "reference"
tags: [vue, vue3, javascript, composition-api, composables, pinia, nuxt, vite, script-setup]
---

# skill:vue-expert-js — Vue.js 3 Composition API & JavaScript Patterns

## Version: 1.0.0

## Purpose

Build modern Vue.js 3 applications using the Composition API with JavaScript (non-TypeScript). This skill focuses on script setup syntax, composable design patterns, Pinia state management, Vue Router 4, Nuxt 3 integration, and Vite-based tooling — all with JavaScript-first patterns. Use when building Vue 3 apps in JavaScript, creating reusable composables, migrating from Options API, or when TypeScript is not adopted.

## File Structure

```
skills/vue-expert-js/
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

- Gather inputs: project type, Vue version, framework (Nuxt 3, Quasar, plain Vue)
- Detect Vue 3 vs Vue 2 and migration status
- Identify Composition API vs Options API usage
- Detect state management (Pinia, Vuex 4)
- Identify build tool (Vite, Webpack, Nuxt)
- Determine CSS approach (Tailwind, UnoCSS, scoped styles, CSS Modules)
- Identify UI library (Vuetify, PrimeVue, Naive UI, Element Plus)
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="vue-expert-js"` and `domain="engineering"`.

Load per-project memory files if they exist:
- `project_overview.md` — Vue version, framework, key dependencies
- `composable_patterns.md` — Established composable patterns and conventions
- `component_conventions.md` — Component naming, structure, communication patterns
- `state_patterns.md` — Pinia store design and data flow patterns

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Vue.js JavaScript Development Core

Apply expert-level Vue.js guidance across these dimensions:

1. **Composition API Patterns (JavaScript)**
   - `<script setup>` syntax for concise SFCs
   - Reactive primitives: `ref()`, `reactive()`, `computed()`, `watch()`, `watchEffect()`
   - Lifecycle hooks: `onMounted()`, `onUnmounted()`, `onBeforeUpdate()`
   - `defineProps()`, `defineEmits()`, `defineExpose()`, `defineModel()` (3.4+)
   - Template refs with `useTemplateRef()` (3.5+)
   - `toRefs()` and `toRef()` for destructuring reactive objects

2. **Composable Design**
   - Naming convention: `use` prefix (e.g., `useFetch`, `useAuth`)
   - Input arguments via refs or getters for reactivity
   - Return values: object of refs (not reactive) for destructurability
   - Cleanup with `onUnmounted` and `onScopeDispose`
   - Async composables with Suspense support
   - Composable composition (composing composables together)
   - VueUse library integration for common utilities

3. **State Management with Pinia**
   - Setup stores vs Options stores (prefer setup for JS flexibility)
   - Store composition and cross-store references
   - Actions for async operations
   - Plugins (persistence, logging, devtools)
   - StoreToRefs for reactive destructuring
   - HMR support configuration

4. **Component Architecture**
   - SFC (Single File Component) structure and naming
   - Props with runtime validation (no TypeScript)
   - Emits declaration with validation functions
   - Provide/inject for dependency injection
   - Dynamic components and KeepAlive
   - Async components and Suspense
   - Teleport for portal-like rendering

5. **Vue Router 4**
   - Route definitions with named routes
   - Navigation guards (per-route, global, in-component)
   - Route meta fields for auth and layout
   - Dynamic routing and route matching
   - Scroll behavior customization
   - Lazy loading routes with `defineAsyncComponent`

6. **Performance in Vue.js**
   - `v-once`, `v-memo` directives for render optimization
   - `shallowRef` and `shallowReactive` for large objects
   - Virtual scrolling for large lists
   - Component lazy loading and code splitting
   - Template compilation optimization
   - Avoiding unnecessary reactivity

7. **Nuxt 3 Integration (when applicable)**
   - File-based routing and layouts
   - Server routes and API endpoints
   - `useFetch`, `useAsyncData`, `useLazyFetch`
   - Auto-imports and module system
   - SEO with `useHead` and `useSeoMeta`
   - Nitro server engine configuration

### Step 5: Generate Output

- Save output to `/claudedocs/vue-expert-js_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="vue-expert-js"`. Store any newly learned patterns, conventions, or project insights.

Update per-project memory:
- **project_overview.md**: Vue version, framework, build tool, dependencies
- **composable_patterns.md**: Custom composables, VueUse usage
- **component_conventions.md**: Naming, structure, communication patterns
- **state_patterns.md**: Pinia store design, data flow established

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Vue version and Composition API usage detected (Step 1)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — Vue.js 3 JavaScript patterns |
