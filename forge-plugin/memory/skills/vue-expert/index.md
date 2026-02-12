# Vue Expert — Memory System

This file documents the memory structure for the `vue-expert` skill. Memory is project-specific knowledge that accumulates over time through repeated Vue.js TypeScript development sessions.

---

## Purpose

The memory system enables the skill to:
- **Recall architecture patterns** — Understand module structure and layer conventions
- **Track TypeScript patterns** — Remember generic types, prop patterns, and augmentations
- **Maintain testing conventions** — Document test setup, mocking strategy, and coverage
- **Learn project ecosystem** — Remember Nuxt configuration, plugins, and modules
- **Improve consistency** — Ensure guidance aligns with established project patterns

---

## Memory Structure

```
memory/skills/vue-expert/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Vue/Nuxt versions, TypeScript config
    ├── architecture_patterns.md   # Module structure, layer architecture
    ├── type_patterns.md           # TypeScript patterns for Vue
    └── testing_patterns.md        # Testing conventions and coverage
```

---

## Per-Project Memory Files

### 1. project_overview.md
- Vue and Nuxt versions
- TypeScript configuration (strict mode, paths)
- Monorepo setup (if applicable)
- Key dependencies and versions
- Deployment target and rendering strategy (SSR/SSG/SPA)

### 2. architecture_patterns.md
- Module/package structure and boundaries
- Component architecture (headless, compound, polymorphic)
- API layer design and data fetching patterns
- Error handling architecture
- Internationalization setup

### 3. type_patterns.md
- Generic component patterns (`<script setup generic="T">`)
- Typed props, emits, slots, and provide/inject
- Utility types for Vue-specific patterns
- API response typing strategy
- Type augmentation (GlobalComponents, ComponentCustomProperties)

### 4. testing_patterns.md
- Vitest configuration and plugins
- Component testing utilities and helpers
- Store testing patterns (createTestingPinia)
- MSW handler organization
- E2E testing approach and page objects
- Coverage thresholds and requirements

---

## Related Documentation

- **Skill Workflow**: `../../skills/vue-expert/SKILL.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
