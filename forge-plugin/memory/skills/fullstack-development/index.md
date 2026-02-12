# Full-Stack Development - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during full-stack development oversight sessions. Each project gets its own subdirectory containing stack inventories, architecture decisions, and integration patterns discovered during analysis.

## Directory Structure

```
memory/skills/fullstack-development/
├── index.md (this file)
└── {project-name}/
    ├── stack_overview.md
    ├── architecture_decisions.md
    └── integration_patterns.md
```

## Memory Files Per Project

### stack_overview.md
- Frontend framework, version, and key libraries
- Backend language, framework, and runtime
- Database type, version, and ORM/driver
- Infrastructure and deployment platform
- CI/CD pipeline and tooling
- Environment inventory (dev, staging, production)
- Last analyzed timestamp

### architecture_decisions.md
- Architectural style (monolith, microservices, serverless, etc.)
- Key design decisions with rationale and trade-offs
- Alternatives considered and reasons for rejection
- API versioning and contract strategy
- Authentication and authorization architecture
- Data modeling philosophy and database selection rationale
- Known technical debt and planned improvements

### integration_patterns.md
- Cross-layer data flow documentation
- Shared type definitions and contract locations
- Error propagation and handling conventions
- Validation rules and where they are enforced
- Caching strategy per layer (CDN, application, database)
- Event/message patterns for async communication
- Testing strategy across layer boundaries (contract tests, E2E)

## Usage

### Creation
Memory is created the FIRST time a project's full-stack architecture is analyzed. The project name is either:
1. Specified by the user
2. Derived from the repository name
3. Extracted from the primary configuration file (e.g., `package.json` name field)

### Updates
Memory is UPDATED every time the skill performs an analysis:
- Stack versions and dependencies are refreshed
- New architecture decisions are recorded with timestamps
- Integration patterns are refined as the system evolves
- Known issues and improvement opportunities are tracked
- Previous recommendations are marked as addressed or deferred

### Reads
Memory is READ at the START of every analysis:
- Provides historical context and continuity across sessions
- Shows architecture evolution over time
- Highlights previously identified issues and whether they were resolved
- Informs recommendations with project-specific knowledge
- Ensures consistency in naming conventions and patterns

## Evolution

As a project matures, its memory grows to reflect architectural evolution:

```
v1 (Initial)     → Stack inventory + first architecture decisions
v2 (Growth)      → Integration patterns emerge, scaling concerns noted
v3 (Maturity)    → Comprehensive patterns, tech debt tracked, migration plans
v4 (Scaling)     → Performance baselines, scaling thresholds, optimization history
```

## Related Documentation

- **Skill Definition**: `../../skills/fullstack-development/SKILL.md`
- **Usage Examples**: `../../skills/fullstack-development/examples.md`
- **MemoryStore Interface**: `../../interfaces/memory_store.md`
- **Memory Lifecycle**: `../../../memory/lifecycle.md`
- **Memory Quality Guidance**: `../../../memory/quality_guidance.md`

---

**Memory System Version**: 1.0.0
**Last Updated**: 2026-02-12
**Maintained by**: fullstack-development skill
