# Memory Structure: dotnet-core

## Purpose

This directory stores project-specific .NET Core architecture decisions, API patterns, and deployment notes. Each project gets its own subdirectory to persist knowledge.

## Memory vs Context

- **Context** (`../../context/dotnet/`): Shared .NET standards and patterns
- **Memory** (this directory): Project-specific solution structure and conventions

## Directory Structure

```
memory/skills/dotnet-core/
├── index.md (this file)
└── {project-name}/
    ├── solution_overview.md       # Solution layout, project dependencies
    ├── api_patterns.md            # Controllers, DTOs, routing conventions
    ├── data_access.md             # EF Core, migrations, repository patterns
    └── deployment_notes.md        # Hosting, pipelines, environment settings
```

## Usage Guidelines

- Update `api_patterns.md` when new controller conventions are established.
- Track migration strategies and data access rules in `data_access.md`.
- Log hosting or pipeline changes in `deployment_notes.md`.
