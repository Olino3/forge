# Flutter Expert — Usage Examples

This document provides practical examples of how to use the `flutter-expert` skill in various scenarios.

---

## Example 1: New Flutter App with Riverpod

**Scenario**: Building a new cross-platform app targeting iOS and Android

**Command**:
```
skill:flutter-expert

Starting a new e-commerce app with Flutter 3.24. Need state management recommendation and project structure. Targeting iOS and Android.
```

**What Happens**:
1. Detects greenfield Flutter 3.24 project
2. No existing memory — asks questions about app complexity and team experience
3. Recommends Riverpod 2 for state management (best for new projects)
4. Designs feature-first project structure:
   - `lib/features/` — Feature modules (auth, products, cart, orders)
   - `lib/core/` — Shared services, models, utils
   - `lib/shared/` — Reusable widgets
5. Sets up GoRouter for declarative navigation
6. Creates project memory with chosen patterns

**Expected Output**:
- Project structure recommendation
- Riverpod provider architecture (providers per feature)
- GoRouter route definitions with guards
- Recommended packages (freezed, json_serializable, dio)
- Code examples: feature module with provider, screen, and widget

---

## Example 2: Migrating to New Architecture (Fabric + TurboModules)

**Scenario**: Existing Flutter app using platform channels needs modernization

**Command**:
```
skill:flutter-expert

We have a Flutter app with 5 custom platform channels for native iOS/Android features. How should we structure these for maintainability and performance?
```

**What Happens**:
1. Loads project memory with existing platform channel catalog
2. Analyzes current MethodChannel implementations
3. Recommends Pigeon for type-safe platform communication
4. Designs plugin architecture for each native integration:
   - Federated plugin structure for each platform
   - Pigeon spec files for type-safe interfaces
   - Platform-specific implementation patterns
5. Produces migration plan from raw MethodChannel to Pigeon

**Expected Output**:
- Platform channel audit and categorization
- Pigeon spec file examples for each channel
- iOS (Swift) and Android (Kotlin) implementation templates
- Testing strategy for platform channels
- Migration plan from MethodChannel to Pigeon

---

## Example 3: Performance Optimization for Large Lists

**Scenario**: A Flutter app has janky scrolling with 10,000+ items

**Command**:
```
skill:flutter-expert

Our product listing screen has 10,000+ items and scrolling is janky, especially on older Android devices. Using ListView.builder already.
```

**What Happens**:
1. Loads project memory for performance profile
2. Analyzes scrolling performance patterns:
   - ListView.builder configuration (itemExtent, cacheExtent)
   - Widget build cost per item
   - Image loading and caching strategy
3. Recommends optimizations:
   - Switch to `SliverList` with `SliverChildBuilderDelegate` for fine control
   - Use `const` constructors for static widget subtrees
   - Implement image caching with `cached_network_image`
   - Consider `RepaintBoundary` for complex list items
   - Run heavy filtering/sorting in isolates
4. Provides DevTools profiling instructions

**Expected Output**:
- Optimized list implementation code
- Image caching setup
- Isolate usage for data processing
- DevTools profiling checklist
- Before/after performance metrics targets
- Widget rebuild analysis strategy

---

## Example 4: Bloc Pattern for Complex Business Logic

**Scenario**: Implementing a multi-step checkout flow with Bloc

**Command**:
```
skill:flutter-expert

Need to implement a 4-step checkout flow (cart → shipping → payment → confirmation) using Bloc. Each step has validation and can go back/forward.
```

**What Happens**:
1. Detects Bloc state management usage
2. Designs multi-step flow architecture:
   - `CheckoutBloc` managing overall flow state
   - Step-specific Cubits for local validation
   - Navigation events for step transitions
   - State preservation across steps
3. Handles edge cases:
   - Network failures during payment
   - Cart modification during checkout
   - Deep linking to specific steps
4. Provides testing strategy for each step

**Expected Output**:
- CheckoutBloc with events and states
- Step-specific Cubit implementations
- Navigation integration with flow state
- Form validation patterns per step
- Unit tests for each Bloc/Cubit
- Widget tests for step transitions

---

## Example 5: Expo-like Development with Flutter

**Scenario**: Setting up a monorepo for a Flutter app with shared packages

**Command**:
```
skill:flutter-expert

We have 3 Flutter apps (customer, driver, restaurant) sharing common code. How should we set up a monorepo?
```

**What Happens**:
1. Analyzes shared code requirements across apps
2. Recommends Melos for monorepo management
3. Designs package structure:
   - `packages/core` — Shared models, services, utils
   - `packages/ui` — Shared widget library
   - `packages/api` — API client and DTOs
   - `apps/customer` — Customer-facing app
   - `apps/driver` — Driver app
   - `apps/restaurant` — Restaurant management app
4. Configures shared dependency management

**Expected Output**:
- Melos configuration file
- Package dependency graph
- Shared widget library structure
- CI/CD pipeline for monorepo
- Version management strategy
- Code sharing patterns and boundaries

---

## Common Usage Patterns

### Pattern 1: State Management Selection
```
skill:flutter-expert
Help me choose between Riverpod, Bloc, and Provider for my app
```

### Pattern 2: Widget Architecture
```
skill:flutter-expert
Design a reusable widget library for our design system
```

### Pattern 3: Native Integration
```
skill:flutter-expert
Integrate a native iOS camera SDK with our Flutter app
```

### Pattern 4: Testing Strategy
```
skill:flutter-expert
Set up a comprehensive testing strategy for our Flutter app
```

---

## When to Use This Skill

**Ideal Scenarios**:
- Starting a new Flutter project
- Choosing state management solution
- Optimizing performance
- Platform channel development
- Monorepo setup and shared packages
- Migration planning between Flutter versions

**Not Ideal For**:
- Pure Dart library development (no Flutter UI)
- Backend API development
- Web-only projects without mobile targets
