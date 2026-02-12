# Memory Structure: fastapi

## Purpose

This directory stores project-specific FastAPI design decisions, API contracts, and performance notes. Each project gets its own subdirectory to persist knowledge.

## Memory vs Context

- **Context** (`../../context/python/`): Shared FastAPI/Python standards and patterns
- **Memory** (this directory): Project-specific routers, dependencies, and API conventions

## Directory Structure

```
memory/skills/fastapi/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Service scope, stack, deployment
    ├── api_contracts.md           # Endpoint contracts and schemas
    ├── dependency_patterns.md     # DI conventions and shared dependencies
    └── performance_notes.md       # Latency, caching, async constraints
```

## Usage Guidelines

- Capture OpenAPI contract changes in `api_contracts.md`.
- Update `dependency_patterns.md` when new shared dependencies emerge.
- Track latency or scaling constraints in `performance_notes.md`.
