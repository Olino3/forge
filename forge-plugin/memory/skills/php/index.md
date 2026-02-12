# Memory Structure: php

## Purpose

This directory stores project-specific PHP framework conventions, dependency maps, and deployment notes. Each project gets its own subdirectory to persist knowledge.

## Memory vs Context

- **Context** (`../../context/engineering/`): Shared architecture and workflow standards
- **Memory** (this directory): Project-specific PHP framework practices

## Directory Structure

```
memory/skills/php/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Stack, versions, deployment target
    ├── framework_conventions.md   # Laravel/Symfony conventions
    ├── dependency_map.md          # Composer dependencies and boundaries
    └── deployment_notes.md        # Hosting, env config, pipelines
```

## Usage Guidelines

- Track framework-specific rules in `framework_conventions.md`.
- Record dependency boundaries in `dependency_map.md`.
- Document deployment details in `deployment_notes.md`.
