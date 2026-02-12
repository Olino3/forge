# Flutter Expert — Memory System

This file documents the memory structure for the `flutter-expert` skill. Memory is project-specific knowledge that accumulates over time through repeated Flutter development sessions.

---

## Purpose

The memory system enables the skill to:
- **Recall project architecture** — Understand state management, navigation, and platform targets
- **Track widget patterns** — Remember established widget composition conventions
- **Maintain platform knowledge** — Document platform-specific quirks and workarounds
- **Learn dependency patterns** — Remember which packages and versions are in use
- **Avoid redundancy** — Don't re-explain patterns already established

---

## Memory Structure

```
memory/skills/flutter-expert/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Flutter/Dart versions, packages, targets
    ├── widget_patterns.md         # Widget composition and reuse patterns
    ├── state_management.md        # State management approach and conventions
    └── platform_integrations.md   # Platform channels, native integrations
```

---

## Per-Project Memory Files

### 1. project_overview.md
- Flutter and Dart SDK versions
- Target platforms (iOS, Android, Web, Desktop)
- Key packages and versions
- Project structure pattern (feature-first, layer-first)
- Build and deployment setup (EAS, Fastlane)

### 2. widget_patterns.md
- Custom widget library conventions
- Reusable widget composition patterns
- Theme and styling approach
- Animation patterns used
- Widget testing conventions

### 3. state_management.md
- Chosen solution (Riverpod, Bloc, Provider, GetX)
- Provider/store organization patterns
- Async data patterns
- Caching and persistence approach
- State testing conventions

### 4. platform_integrations.md
- Custom platform channels (MethodChannel/Pigeon)
- Native module specifications
- Permission handling patterns
- Platform-specific workarounds
- Third-party native SDK integrations

---

## Related Documentation

- **Skill Workflow**: `../../skills/flutter-expert/SKILL.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
