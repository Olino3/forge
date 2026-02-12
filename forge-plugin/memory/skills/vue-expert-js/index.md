# Vue Expert JS — Memory System

This file documents the memory structure for the `vue-expert-js` skill. Memory is project-specific knowledge that accumulates over time through repeated Vue.js JavaScript development sessions.

---

## Purpose

The memory system enables the skill to:
- **Recall composable patterns** — Understand established composable conventions
- **Track component conventions** — Remember naming, structure, and communication patterns
- **Maintain state patterns** — Document Pinia store design and data flow
- **Learn project structure** — Remember Nuxt/Vue configuration and conventions
- **Improve accuracy** — Build on past sessions for contextual guidance

---

## Memory Structure

```
memory/skills/vue-expert-js/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Vue version, framework, dependencies
    ├── composable_patterns.md     # Custom composables and VueUse usage
    ├── component_conventions.md   # Naming, structure, communication patterns
    └── state_patterns.md          # Pinia store design, data flow
```

---

## Per-Project Memory Files

### 1. project_overview.md
- Vue version and Composition API adoption level
- Framework (Nuxt 3, Quasar, standalone Vue)
- Build tool (Vite, Webpack)
- UI library and styling approach
- Key dependencies and versions

### 2. composable_patterns.md
- Custom composable library and interfaces
- VueUse composables in use
- Cleanup and lifecycle patterns
- Async composable patterns
- Composable testing conventions

### 3. component_conventions.md
- Component naming and file organization
- Props and emits patterns (runtime validation)
- Provide/inject usage
- Slot patterns and dynamic components
- Form handling approach

### 4. state_patterns.md
- Pinia store organization (setup vs options style)
- Cross-store communication patterns
- Persistence and caching approach
- Action patterns for async operations
- Store testing conventions

---

## Related Documentation

- **Skill Workflow**: `../../skills/vue-expert-js/SKILL.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
