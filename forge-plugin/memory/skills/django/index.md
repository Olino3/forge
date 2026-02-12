# Memory Structure: django

## Purpose

This directory stores project-specific Django architecture notes, model patterns, and deployment decisions learned during engagements. Each project gets its own subdirectory to persist knowledge over time.

## Memory vs Context

- **Context** (`../../context/python/`): Shared Django/Python standards and best practices
- **Memory** (this directory): Project-specific conventions, decisions, and known issues

## Directory Structure

```
memory/skills/django/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Project scope, versions, architecture
    ├── architecture_notes.md      # App structure, settings, middleware
    ├── data_model_patterns.md     # ORM conventions and query patterns
    └── deployment_notes.md        # Hosting, ASGI/WSGI, static/media
```

## Usage Guidelines

- Create `{project-name}/project_overview.md` on first engagement.
- Update `data_model_patterns.md` whenever new ORM conventions are discovered.
- Log deployment or environment changes in `deployment_notes.md`.
