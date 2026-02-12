# Memory Structure: rails

## Purpose

This directory stores project-specific Rails conventions, domain models, and performance notes. Each project gets its own subdirectory to persist knowledge.

## Memory vs Context

- **Context** (`../../context/engineering/`): Shared architecture and workflow standards
- **Memory** (this directory): Project-specific Rails patterns and decisions

## Directory Structure

```
memory/skills/rails/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # Stack, versions, deployment target
    ├── domain_models.md           # ActiveRecord models and associations
    ├── job_queue_notes.md         # Background jobs, queues, retries
    └── performance_notes.md       # Caching, query optimizations
```

## Usage Guidelines

- Capture domain model changes in `domain_models.md`.
- Track job processing conventions in `job_queue_notes.md`.
- Record caching strategies and query tuning in `performance_notes.md`.
