# React Native Expert — Usage Examples

This document provides practical examples of how to use the `react-native-expert` skill in various scenarios.

---

## Example 1: New Expo App with File-Based Routing

**Scenario**: Starting a new mobile app using Expo SDK 52

**Command**:
```
skill:react-native-expert

Starting a new social media app targeting iOS and Android. Want to use Expo SDK 52 with Expo Router. Need auth, push notifications, and camera access.
```

**What Happens**:
1. Detects Expo SDK 52 project with Expo Router
2. Designs project structure with file-based routing:
   - `app/(tabs)/` — Tab-based main navigation
   - `app/(auth)/` — Authentication flow
   - `app/[profile]/` — Dynamic profile routes
3. Recommends development build (not Expo Go) for native modules
4. Sets up feature integration plan:
   - Auth: expo-auth-session + secure store
   - Push: expo-notifications + EAS
   - Camera: expo-camera with permissions

**Expected Output**:
- Expo Router file structure
- Navigation architecture (tabs, stacks, modals)
- Deep linking configuration for iOS/Android
- Auth flow with secure token storage
- Push notification setup with EAS
- Camera integration with permissions handling
- Development build vs Expo Go decision rationale

---

## Example 2: Migrating to New Architecture

**Scenario**: Upgrading a React Native CLI app to New Architecture

**Command**:
```
skill:react-native-expert

We have a React Native 0.73 app using the old Bridge architecture with 3 custom native modules. Need to migrate to New Architecture (Fabric + TurboModules).
```

**What Happens**:
1. Loads project memory with existing native module catalog
2. Assesses New Architecture readiness:
   - Checks third-party library compatibility
   - Evaluates custom native module migration effort
   - Identifies bridgeless mode requirements
3. Designs migration plan:
   - Phase 1: Enable New Architecture flag (interop layer)
   - Phase 2: Migrate custom modules to TurboModules (Codegen specs)
   - Phase 3: Migrate custom views to Fabric components
   - Phase 4: Enable bridgeless mode
4. Provides Codegen spec files for each module

**Expected Output**:
- Compatibility audit of third-party dependencies
- TurboModule spec files (TypeScript) for each native module
- Fabric component specs for custom views
- Gradle/Podfile configuration changes
- Interop layer usage during migration
- Testing strategy for architecture validation
- Rollback plan if issues arise

---

## Example 3: Performance Optimization for FlatList

**Scenario**: Chat app has poor scrolling performance with large message history

**Command**:
```
skill:react-native-expert

Our chat app's message list with 5000+ messages has poor scrolling performance and high memory usage on Android. Using FlatList with Hermes.
```

**What Happens**:
1. Analyzes FlatList performance bottlenecks:
   - `getItemLayout` for fixed-height optimization
   - `windowSize` and `maxToRenderPerBatch` tuning
   - Image rendering in message bubbles
   - JavaScript thread saturation during scroll
2. Recommends FlashList migration for improved performance
3. Designs memory optimization strategy:
   - Image recycling and cache limits
   - Message pagination (load more on scroll up)
   - Reanimated-based scroll animations

**Expected Output**:
- FlashList migration code with configuration
- `estimatedItemSize` and `overrideItemLayout` setup
- Image optimization with FastImage
- Pagination implementation (cursor-based)
- Memory profiling instructions
- Android-specific optimization (large heap, Hermes GC tuning)
- Before/after performance comparison plan

---

## Example 4: Native Module with Pigeon

**Scenario**: Building a custom native module for Bluetooth communication

**Command**:
```
skill:react-native-expert

Need to build a custom native module for BLE (Bluetooth Low Energy) communication. Must work on both iOS (Swift) and Android (Kotlin). Using React Native CLI.
```

**What Happens**:
1. Designs TurboModule architecture for BLE:
   - Codegen spec with TypeScript types
   - Event emitter for scan results and connection state
   - Promise-based API for connect/disconnect/read/write
2. Platform-specific implementation guidance:
   - iOS: CoreBluetooth framework with Swift
   - Android: android.bluetooth with Kotlin coroutines
3. Handles platform differences:
   - Permission models (iOS vs Android 12+)
   - Background scanning limitations
   - Connection state management

**Expected Output**:
- TurboModule Codegen spec file
- iOS Swift implementation skeleton
- Android Kotlin implementation skeleton
- Permission handling for both platforms
- Event emitter patterns for real-time data
- Unit test and integration test approach
- Usage examples from React Native side

---

## Example 5: Offline-First App with Local Database

**Scenario**: Building an offline-capable app with sync

**Command**:
```
skill:react-native-expert

Building a field inspection app that needs to work offline. Inspectors capture photos, fill forms, then sync when back online. Using Expo.
```

**What Happens**:
1. Designs offline-first architecture:
   - Local database: expo-sqlite or WatermelonDB
   - File storage: expo-file-system for photos
   - Sync queue: background upload when connectivity returns
2. Handles edge cases:
   - Conflict resolution (server vs local changes)
   - Partial sync (large photo uploads)
   - Network state detection (NetInfo)
3. Recommends optimistic UI patterns

**Expected Output**:
- Database schema design (SQLite/WatermelonDB)
- Sync queue implementation
- Photo capture and local storage flow
- Background upload with expo-task-manager
- Conflict resolution strategy
- Network state management
- UI patterns for sync status indication
- Testing strategy for offline scenarios

---

## Common Usage Patterns

### Pattern 1: Expo vs CLI Decision
```
skill:react-native-expert
Should we use Expo or React Native CLI for our healthcare app?
```

### Pattern 2: Navigation Architecture
```
skill:react-native-expert
Design the navigation structure for an app with auth, tabs, and deep linking
```

### Pattern 3: Animation Performance
```
skill:react-native-expert
Implement smooth gesture-based animations with Reanimated 3
```

### Pattern 4: App Store Submission
```
skill:react-native-expert
Prepare our app for iOS App Store and Google Play submission
```

---

## When to Use This Skill

**Ideal Scenarios**:
- Building new React Native apps (CLI or Expo)
- Migrating to New Architecture
- Performance optimization (lists, animations, startup)
- Native module development
- Navigation architecture design
- Offline-first app architecture

**Not Ideal For**:
- React web applications (use `skill:react-expert`)
- Flutter mobile development (use `skill:flutter-expert`)
- Backend API design for mobile apps
