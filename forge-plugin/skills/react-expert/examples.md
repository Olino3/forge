# React Expert — Usage Examples

This document provides practical examples of how to use the `react-expert` skill in various scenarios.

---

## Example 1: Server Components Architecture

**Scenario**: Designing a React 19 app with Server Components

**Command**:
```
skill:react-expert

We're building a Next.js 15 app with React 19. Help us design the Server Component vs Client Component boundaries for a dashboard with real-time data.
```

**What Happens**:
1. Detects React 19 + Next.js 15 with Server Components
2. Analyzes dashboard requirements (real-time data, interactive charts)
3. Designs component boundary strategy:
   - Server Components: data fetching, layout, static content
   - Client Components: interactive charts, real-time subscriptions, form inputs
   - Shared Components: components that work in both contexts
4. Addresses serialization boundaries and prop constraints
5. Recommends streaming patterns with Suspense

**Expected Output**:
- Component tree with Server/Client boundaries annotated
- Data fetching patterns (async Server Components + TanStack Query for client)
- Streaming strategy with nested Suspense boundaries
- Server Actions for form mutations
- Real-time data pattern (Server Component for initial, client WebSocket for updates)
- Code examples for each component type

---

## Example 2: Custom Hook Library Design

**Scenario**: Building a reusable hook library for the team

**Command**:
```
skill:react-expert

Design a custom hooks library for our React app. We need hooks for: API calls with caching, form validation, keyboard shortcuts, and responsive breakpoints.
```

**What Happens**:
1. Analyzes each hook requirement
2. Designs hook architecture with composability:
   - `useApi<T>()` — wrapping TanStack Query with project conventions
   - `useForm<T>()` — generic form state with Zod validation
   - `useHotkey()` — keyboard shortcut registration with cleanup
   - `useBreakpoint()` — responsive design hook with SSR safety
3. Ensures hooks follow single-responsibility principle
4. Provides TypeScript generics for type safety

**Expected Output**:
- Hook interface definitions with TypeScript
- Implementation code for each hook
- Composability examples (hooks using other hooks)
- Testing patterns with renderHook
- Documentation template for each hook
- Bundle size considerations

---

## Example 3: Performance Optimization Audit

**Scenario**: React app re-renders excessively causing poor performance

**Command**:
```
skill:react-expert

Our React app is sluggish. The user list page with 500 items re-renders the entire list on every keystroke in the search bar. Using React 18 with Zustand.
```

**What Happens**:
1. Loads project memory for existing performance profile
2. Identifies performance anti-patterns:
   - Zustand selector returning new object references
   - Missing list virtualization
   - Search input causing root-level state changes
3. Recommends targeted fixes:
   - Use `useShallow` or equality selectors in Zustand
   - Implement `useDeferredValue` for search input
   - Add TanStack Virtual for list virtualization
   - Extract search into isolated component tree
4. Provides React Profiler usage instructions

**Expected Output**:
- Root cause analysis of re-render cascade
- Zustand selector optimization code
- useDeferredValue implementation for search
- TanStack Virtual integration for the list
- React.memo usage analysis (where it helps/hurts)
- Before/after render count measurements
- Profiler-based verification strategy

---

## Example 4: Compound Component Pattern

**Scenario**: Building a flexible, reusable component API

**Command**:
```
skill:react-expert

Build a compound component pattern for a DataTable that supports sorting, filtering, pagination, and row selection. Needs to be flexible for different use cases.
```

**What Happens**:
1. Designs compound component API:
   - `<DataTable>` — context provider, data management
   - `<DataTable.Header>` — column definitions with sort controls
   - `<DataTable.Body>` — row rendering with selection
   - `<DataTable.Filter>` — filter controls
   - `<DataTable.Pagination>` — page navigation
2. Implements shared context with useContext
3. Provides TypeScript generics for type-safe row data
4. Handles accessibility (ARIA roles, keyboard navigation)

**Expected Output**:
- Complete compound component implementation
- Context-based state sharing
- TypeScript generic types for row data
- Usage examples for common configurations
- Accessibility compliance (ARIA grid pattern)
- Testing strategy for compound components

---

## Example 5: State Management Architecture

**Scenario**: Choosing and implementing state management for a complex app

**Command**:
```
skill:react-expert

We need state management for a React 19 project management app. Need to handle: user auth, project list, real-time board updates, and offline support. What's the best approach?
```

**What Happens**:
1. Analyzes state categories:
   - **Server state** (projects, boards): TanStack Query
   - **Client state** (UI, theme): Zustand
   - **Auth state**: Dedicated auth context
   - **Real-time state**: WebSocket + TanStack Query invalidation
   - **Offline state**: TanStack Query persistence
2. Designs state architecture with clear boundaries
3. Provides offline-first patterns with optimistic updates

**Expected Output**:
- State architecture diagram
- TanStack Query setup with optimistic mutations
- Zustand store design (slices pattern)
- WebSocket integration with query invalidation
- Offline persistence configuration
- Auth state management pattern
- Code examples for each state category

---

## Common Usage Patterns

### Pattern 1: Component Architecture
```
skill:react-expert
Design the component architecture for a complex form wizard
```

### Pattern 2: React 19 Features
```
skill:react-expert
How should we use Server Actions and useOptimistic in our form submissions?
```

### Pattern 3: Testing Strategy
```
skill:react-expert
Set up a testing strategy for our React component library
```

### Pattern 4: Migration
```
skill:react-expert
Migrate our class components to functional components with hooks
```

---

## When to Use This Skill

**Ideal Scenarios**:
- Advanced component pattern design
- State management architecture decisions
- Performance optimization and profiling
- React 18/19 feature adoption
- Custom hook library development
- Server Component boundary design

**Not Ideal For**:
- Next.js-specific features (use `skill:nextjs` for App Router, caching)
- React Native mobile development (use `skill:react-native-expert`)
- Basic React tutorials or getting started
