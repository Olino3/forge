# React Native Expert — Memory System

This file documents the memory structure for the `react-native-expert` skill. Memory is project-specific knowledge that accumulates over time through repeated React Native development sessions.

---

## Purpose

The memory system enables the skill to:
- **Recall app architecture** — Understand navigation, state, and native integrations
- **Track native modules** — Remember custom TurboModules and Fabric components
- **Maintain platform knowledge** — Document iOS/Android-specific configurations and quirks
- **Learn navigation patterns** — Remember route structure and deep linking setup
- **Avoid regression** — Don't recommend patterns that conflicted with platform requirements

---

## Memory Structure

```
memory/skills/react-native-expert/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # RN version, Expo SDK, architecture type
    ├── navigation_patterns.md     # Navigation structure and deep linking
    ├── native_modules.md          # Custom modules and TurboModule specs
    └── platform_specifics.md      # Platform quirks and configurations
```

---

## Per-Project Memory Files

### 1. project_overview.md
- React Native version and architecture (Old/New)
- Expo SDK version (if applicable)
- Target platforms and minimum OS versions
- JavaScript engine (Hermes, JSC)
- State management solution
- Build and deployment pipeline

### 2. navigation_patterns.md
- Navigation library and version
- Route hierarchy and navigator nesting
- Deep linking configuration (Universal Links, App Links)
- Auth flow navigation pattern
- Modal and overlay patterns

### 3. native_modules.md
- Custom native module catalog
- TurboModule/Fabric component specs
- Platform channel interfaces
- Third-party native SDK integrations
- Codegen spec file locations

### 4. platform_specifics.md
- iOS-specific configurations and entitlements
- Android-specific manifest and Gradle settings
- Permission handling patterns per platform
- Platform-specific UI adaptations
- Known platform bugs and workarounds

---

## Related Documentation

- **Skill Workflow**: `../../skills/react-native-expert/SKILL.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
