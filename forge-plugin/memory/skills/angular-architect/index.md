# Angular Architect — Memory System

This file documents the memory structure for the `angular-architect` skill. Memory is project-specific knowledge that accumulates over time through repeated architectural consultations.

---

## Purpose

The memory system enables the skill to:
- **Recall architectural decisions** — Understand past ADRs and their rationale
- **Track module evolution** — Monitor module/library boundary changes
- **Maintain consistency** — Ensure new recommendations align with existing architecture
- **Learn project patterns** — Remember established conventions and team preferences
- **Avoid contradictions** — Prevent conflicting architectural guidance over time

---

## Memory Structure

```
memory/skills/angular-architect/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Framework stack, Angular version, team size
    ├── architecture_decisions.md  # ADRs and rationale for past choices
    ├── module_map.md              # Module/library boundaries and dependencies
    └── patterns_catalog.md        # Established patterns in this project
```

---

## Per-Project Memory Files

### 1. project_overview.md
- Angular version and key dependencies
- Team size and structure
- Monorepo tool (Nx, Turborepo, Angular CLI)
- State management approach
- UI component library
- Build and deployment target

### 2. architecture_decisions.md
- Architecture Decision Records (ADRs) from each session
- Rationale for major choices (state management, module system, routing)
- Trade-offs documented and accepted
- Decisions deferred and reasons

### 3. module_map.md
- Module/library dependency graph
- Team ownership assignments
- Build order and boundary rules
- Shared vs feature-specific libraries

### 4. patterns_catalog.md
- Established component patterns
- Service layer conventions
- State management patterns
- Error handling architecture
- Naming and file organization conventions

---

## Related Documentation

- **Skill Workflow**: `../../skills/angular-architect/SKILL.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
