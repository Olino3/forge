# Vue Expert JS — Usage Examples

This document provides practical examples of how to use the `vue-expert-js` skill in various scenarios.

---

## Example 1: Migrating from Options API to Composition API

**Scenario**: Migrating a Vue 3 JavaScript app from Options API to Composition API

**Command**:
```
skill:vue-expert-js

We have a Vue 3.4 app still using Options API in most components. Want to migrate to Composition API with <script setup>. What's the best approach?
```

**What Happens**:
1. Detects Vue 3.4 with Options API components
2. Assesses migration scope and component complexity
3. Designs incremental migration strategy:
   - Phase 1: New components use `<script setup>` exclusively
   - Phase 2: Extract shared logic into composables
   - Phase 3: Migrate complex components (mixins → composables)
   - Phase 4: Migrate simple components
4. Provides pattern mapping: Options API → Composition API
5. Creates composable extraction guidelines

**Expected Output**:
- Options API to Composition API mapping table
- Mixin-to-composable conversion examples
- `<script setup>` patterns for props, emits, expose
- Component migration priority list
- Testing strategy during migration
- Code examples for each conversion pattern

---

## Example 2: Building Composables for Common Patterns

**Scenario**: Creating reusable composables for a Vue JavaScript project

**Command**:
```
skill:vue-expert-js

Build reusable composables for our Vue 3 app: data fetching with loading/error states, form validation, infinite scrolling, and local storage persistence.
```

**What Happens**:
1. Designs composable architecture following Vue conventions:
   - `useFetch(url, options)` — reactive data fetching
   - `useFormValidation(rules)` — validation with error messages
   - `useInfiniteScroll(fetchFn)` — paginated loading on scroll
   - `useLocalStorage(key, defaultValue)` — persistent reactive state
2. Ensures all composables handle cleanup with `onUnmounted`
3. Follows naming conventions and return value patterns

**Expected Output**:
- Complete composable implementations in JavaScript
- Usage examples for each composable
- Composition examples (combining composables)
- Error handling and edge case patterns
- Integration with VueUse where appropriate
- Testing strategy for each composable

---

## Example 3: Pinia Store Architecture

**Scenario**: Designing Pinia stores for a medium-complexity JavaScript app

**Command**:
```
skill:vue-expert-js

Design a Pinia store architecture for our e-commerce app. Need stores for: auth, products, cart, and user preferences. Using Vue 3 with JavaScript.
```

**What Happens**:
1. Designs store architecture with setup store syntax:
   - `useAuthStore` — authentication state and token management
   - `useProductStore` — product catalog with filtering
   - `useCartStore` — shopping cart with persistence
   - `usePreferencesStore` — user settings with localStorage
2. Implements cross-store communication patterns
3. Sets up Pinia plugins (persistence, devtools)

**Expected Output**:
- Setup store implementations for each store
- Cross-store composition examples
- Persistence plugin configuration
- StoreToRefs usage patterns
- Store testing patterns with createTestingPinia
- Action patterns for async operations

---

## Example 4: Nuxt 3 Full-Stack with JavaScript

**Scenario**: Building a Nuxt 3 app without TypeScript

**Command**:
```
skill:vue-expert-js

Setting up a Nuxt 3 blog platform in JavaScript. Need file-based routing, server API routes, and SEO. No TypeScript.
```

**What Happens**:
1. Detects Nuxt 3 JavaScript project
2. Designs Nuxt 3 project structure:
   - `pages/` — File-based routing (blog, [slug], categories)
   - `server/api/` — REST endpoints for blog CRUD
   - `composables/` — Auto-imported composables
   - `components/` — Auto-imported components
3. Configures SEO with useHead and useSeoMeta
4. Sets up content fetching with useFetch

**Expected Output**:
- Nuxt 3 directory structure
- Page components with data fetching (useFetch, useAsyncData)
- Server API routes (H3 event handlers)
- SEO configuration (useHead, useSeoMeta, OG tags)
- Layout system (default, blog, auth)
- Middleware for auth and redirects
- Deployment configuration (Vercel/Netlify)

---

## Example 5: Performance Optimization

**Scenario**: A Vue 3 JavaScript app has slow rendering on large data sets

**Command**:
```
skill:vue-expert-js

Our Vue 3 app renders a dashboard with multiple charts and a table of 10,000 rows. Page load is slow and interactions are laggy.
```

**What Happens**:
1. Analyzes performance bottlenecks:
   - Deep reactivity on large data arrays
   - Unnecessary component re-renders
   - Chart library initialization cost
   - Large table without virtualization
2. Recommends targeted optimizations:
   - `shallowRef` for large data arrays
   - `v-memo` for expensive template sections
   - Virtual scrolling for the table
   - Lazy-loaded chart components with Suspense
3. Provides Vue DevTools profiling guidance

**Expected Output**:
- shallowRef/shallowReactive usage for large data
- v-memo directive application
- Virtual scrolling implementation
- Component lazy loading with defineAsyncComponent
- Computed property optimization
- Vue DevTools performance profiling guide
- Before/after performance metrics targets

---

## Common Usage Patterns

### Pattern 1: Options to Composition Migration
```
skill:vue-expert-js
Convert this Options API component to Composition API with script setup
```

### Pattern 2: Composable Design
```
skill:vue-expert-js
Build a composable for WebSocket real-time updates
```

### Pattern 3: Vue Router Setup
```
skill:vue-expert-js
Set up Vue Router with auth guards and lazy loading
```

### Pattern 4: Component Library
```
skill:vue-expert-js
Build a reusable component library with Vite library mode
```

---

## When to Use This Skill

**Ideal Scenarios**:
- Vue 3 projects using JavaScript (not TypeScript)
- Composition API adoption and migration
- Composable library development
- Pinia store architecture
- Nuxt 3 full-stack development (JS)
- Performance optimization

**Not Ideal For**:
- Vue 3 with TypeScript (use `skill:vue-expert`)
- Vue 2 maintenance (Options API only, no Composition API)
- Angular or React projects
