# Memory Structure: nestjs

## Purpose

This directory stores project-specific NestJS module maps, integration notes, and testing strategies. Each project gets its own subdirectory to persist knowledge.

## Memory vs Context

- **Context** (`../../context/engineering/`): Shared architecture and workflow standards
- **Memory** (this directory): Project-specific NestJS conventions and integrations

## Directory Structure

```
memory/skills/nestjs/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Stack, deployment, primary modules
    ├── module_map.md              # Module boundaries and dependencies
    ├── integration_notes.md       # Queues, caches, external services
    └── testing_strategy.md        # Unit/e2e testing patterns
```

## Usage Guidelines

- Keep `module_map.md` updated as modules are added or split.
- Capture messaging or cache decisions in `integration_notes.md`.
- Document testing tooling in `testing_strategy.md`.
