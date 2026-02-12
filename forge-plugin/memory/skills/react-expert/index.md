# React Expert — Memory System

This file documents the memory structure for the `react-expert` skill. Memory is project-specific knowledge that accumulates over time through repeated React development sessions.

---

## Purpose

The memory system enables the skill to:
- **Recall component patterns** — Understand established component conventions
- **Track hook library** — Remember custom hooks and their interfaces
- **Maintain performance knowledge** — Document performance baselines and optimizations
- **Learn state architecture** — Remember state management decisions and patterns
- **Improve recommendations** — Build on past sessions for better guidance

---

## Memory Structure

```
memory/skills/react-expert/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # React version, framework, key dependencies
    ├── component_patterns.md      # Established component patterns
    ├── hooks_catalog.md           # Custom hooks library and usage
    └── performance_profile.md     # Performance characteristics and optimizations
```

---

## Per-Project Memory Files

### 1. project_overview.md
- React version and features in use
- Framework (Next.js, Remix, Vite, etc.)
- TypeScript configuration
- State management solution
- Styling approach
- Build and deployment setup

### 2. component_patterns.md
- Component composition patterns (compound, render prop, etc.)
- Naming and file organization conventions
- Error boundary strategy
- Form handling approach
- Data fetching patterns

### 3. hooks_catalog.md
- Custom hook library with interfaces
- Hook dependency patterns
- Composability guidelines
- Testing patterns for hooks
- Third-party hook integrations

### 4. performance_profile.md
- Bundle size baselines
- Known performance bottlenecks
- Optimization techniques applied
- Memoization strategy decisions
- Code splitting boundaries

---

## Related Documentation

- **Skill Workflow**: `../../skills/react-expert/SKILL.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
