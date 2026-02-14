---
name: flutter-expert
description: "Cross-platform mobile development with Flutter/Dart. Build performant, maintainable Flutter apps with proper widget architecture, state management, platform channels, and testing patterns."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, widget_patterns.md, state_management.md, platform_integrations.md]
    - type: "shared-project"
      usage: "reference"
## tags: [flutter, dart, mobile, cross-platform, widgets, state-management, riverpod, bloc, platform-channels, testing]

# skill:flutter-expert — Cross-Platform Mobile Development with Flutter/Dart

## Version: 1.0.0

## Purpose

Build and architect high-quality cross-platform mobile applications with Flutter and Dart. This skill covers widget composition, state management selection (Riverpod, Bloc, Provider, GetX), navigation patterns (GoRouter, auto_route), platform channel integration, performance optimization, and comprehensive testing strategies. Use when building new Flutter apps, reviewing Flutter code, or migrating between state management solutions.

## File Structure

```
skills/flutter-expert/
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

- Gather inputs: target platforms (iOS, Android, Web, Desktop), project type, existing codebase
- Detect Flutter version and Dart SDK version
- Identify state management solution (Riverpod, Bloc/Cubit, Provider, GetX, signals)
- Identify navigation approach (GoRouter, auto_route, Navigator 2.0)
- Detect dependency injection (get_it, injectable, riverpod)
- Determine project structure (feature-first, layer-first, clean architecture)
- Identify project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="flutter-expert"` and `domain="engineering"`.

Load per-project memory files if they exist:
- `project_overview.md` — Flutter/Dart versions, target platforms, key packages
- `widget_patterns.md` — Established widget composition and reuse patterns
- `state_management.md` — State management approach and conventions
- `platform_integrations.md` — Platform channel usage and native integrations

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Flutter Development Core

Apply expert-level Flutter/Dart guidance across these dimensions:

1. **Widget Architecture**
   - Composition over inheritance
   - Stateless vs StatefulWidget selection criteria
   - Custom RenderObject for performance-critical widgets
   - Widget key management (ValueKey, ObjectKey, GlobalKey)
   - BuildContext usage and InheritedWidget patterns
   - Sliver-based scrolling for complex layouts

2. **State Management**
   - **Riverpod**: Provider types (Provider, StateProvider, FutureProvider, StreamProvider, NotifierProvider), family/autoDispose modifiers, ref patterns
   - **Bloc/Cubit**: Event-driven patterns, BlocObserver, multi-repository patterns, Bloc-to-Bloc communication
   - **Provider**: ChangeNotifier patterns, ProxyProvider, multi-provider setup
   - Selection guidance based on project complexity and team experience

3. **Navigation & Routing**
   - GoRouter declarative routing, ShellRoute for nested navigation
   - Deep linking configuration (iOS Universal Links, Android App Links)
   - Route guards and redirect logic
   - Navigation state restoration

4. **Platform Integration**
   - MethodChannel/EventChannel for native communication
   - Pigeon for type-safe platform channels
   - Platform-specific UI adaptation (Cupertino vs Material)
   - FFI for direct native library calls
   - Plugin development patterns

5. **Performance Optimization**
   - Widget rebuild minimization (const constructors, selective rebuilds)
   - Image caching and optimization (cached_network_image)
   - List performance (ListView.builder, SliverList)
   - Isolate usage for heavy computation
   - DevTools profiling and performance overlay
   - Shader compilation jank mitigation

6. **Testing Strategy**
   - Widget testing with WidgetTester
   - Golden (snapshot) testing
   - Integration testing with patrol or integration_test
   - Mocking with mocktail/mockito
   - State management testing (Bloc test, Riverpod testing)

7. **Project Structure**
   - Feature-first vs layer-first organization
   - Clean Architecture implementation
   - Monorepo with Melos
   - Code generation (freezed, json_serializable, build_runner)

### Step 5: Generate Output

- Save output to `/claudedocs/flutter-expert_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="flutter-expert"`. Store any newly learned patterns, conventions, or project insights.

Update per-project memory:
- **project_overview.md**: Flutter/Dart versions, packages, target platforms
- **widget_patterns.md**: Custom widgets, composition patterns established
- **state_management.md**: Chosen approach, conventions, patterns
- **platform_integrations.md**: Native integrations, platform channels documented

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Flutter/Dart version and state management detected (Step 1)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — Flutter/Dart cross-platform development |
