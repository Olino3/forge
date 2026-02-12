---
name: react-native-expert
description: "Mobile app development with React Native. Build production-grade native mobile apps with React Native CLI or Expo, including New Architecture (Fabric, TurboModules), navigation, native modules, and platform-specific patterns."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 5
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, navigation_patterns.md, native_modules.md, platform_specifics.md]
    - type: "shared-project"
      usage: "reference"
tags: [react-native, mobile, expo, fabric, turbo-modules, navigation, native-modules, ios, android, new-architecture]
---

# skill:react-native-expert — Mobile App Development with React Native

## Version: 1.0.0

## Purpose

Build production-grade native mobile applications with React Native. This skill covers React Native CLI and Expo workflows, the New Architecture (Fabric renderer, TurboModules, Codegen), navigation (React Navigation, Expo Router), native module development, platform-specific code, performance optimization (Hermes, bridgeless mode), and testing strategies. Use when building new mobile apps, migrating to New Architecture, optimizing performance, or integrating native functionality.

## File Structure

```
skills/react-native-expert/
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

- Gather inputs: target platforms (iOS, Android), project type, existing codebase
- Detect React Native version and architecture (Old vs New Architecture)
- Identify toolchain: React Native CLI vs Expo (managed vs bare workflow)
- Detect navigation solution (React Navigation, Expo Router)
- Identify state management (Zustand, Redux Toolkit, Jotai, MobX, TanStack Query)
- Detect JavaScript engine (Hermes, JSC, V8)
- Identify build system (EAS Build, Fastlane, Bitrise)
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="react-native-expert"` and `domain="engineering"`.

Load per-project memory files if they exist:
- `project_overview.md` — RN version, Expo SDK, target platforms, key dependencies
- `navigation_patterns.md` — Navigation structure and deep linking configuration
- `native_modules.md` — Custom native modules and TurboModule specifications
- `platform_specifics.md` — Platform-specific code, configurations, and quirks

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: React Native Development Core

Apply expert-level React Native guidance across these dimensions:

1. **New Architecture (Fabric & TurboModules)**
   - Fabric renderer: concurrent rendering, synchronous layout
   - TurboModules: lazy loading, type-safe native modules via Codegen
   - Bridgeless mode configuration
   - Migration path from Old Architecture (Bridge) to New Architecture
   - Codegen spec files (TypeScript/Flow) for native interfaces

2. **Expo Ecosystem**
   - Expo SDK module selection and compatibility
   - EAS Build and EAS Submit workflows
   - Expo Router file-based routing
   - Config plugins for native configuration
   - Development builds vs Expo Go
   - Continuous Native Generation (CNG) patterns

3. **Navigation Architecture**
   - React Navigation: Stack, Tab, Drawer, Material Top Tabs
   - Deep linking: iOS Universal Links, Android App Links
   - Navigation state persistence and restoration
   - Type-safe navigation with TypeScript
   - Modal and nested navigator patterns
   - Expo Router: file-based routing, layouts, groups

4. **Native Module Development**
   - TurboModule spec authoring (TypeScript/Flow)
   - Fabric component specs (ViewManagers)
   - Platform-specific Swift/Kotlin/Java native code
   - Bridging patterns for third-party native SDKs
   - Autolinking and manual linking

5. **Performance Optimization**
   - Hermes engine optimization and bytecode precompilation
   - FlatList/FlashList optimization (getItemLayout, windowSize, keyExtractor)
   - Image optimization (FastImage, progressive loading)
   - JavaScript thread vs UI thread workload distribution
   - Reanimated 3 for jank-free animations (worklets, shared values)
   - Memory leak detection and prevention
   - Metro bundler configuration (tree shaking, inline requires)

6. **Platform-Specific Development**
   - Platform.select and Platform.OS patterns
   - Platform-specific file extensions (.ios.tsx, .android.tsx)
   - Native styling differences (shadows, elevation)
   - Permissions handling (react-native-permissions)
   - Push notifications (Expo Notifications, FCM, APNs)
   - Background tasks and services

7. **Testing & Quality**
   - Jest unit testing for components and hooks
   - React Native Testing Library
   - Detox/Maestro for E2E testing
   - Platform-specific testing considerations
   - EAS Update for OTA updates and staged rollouts
   - Crash reporting (Sentry, Crashlytics)

### Step 5: Generate Output

- Save output to `/claudedocs/react-native-expert_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="react-native-expert"`. Store any newly learned patterns, conventions, or project insights.

Update per-project memory:
- **project_overview.md**: RN version, Expo SDK, platforms, architecture type
- **navigation_patterns.md**: Navigation structure, deep link config
- **native_modules.md**: Custom modules, TurboModule specs
- **platform_specifics.md**: Platform quirks, workarounds, configurations

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] React Native version and architecture detected (Step 1)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — React Native mobile development |
