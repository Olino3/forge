# Shared Project Memory

A shared memory layer that all skills contribute to and read from. This eliminates redundant project discovery across skills.

## Purpose

When `python-code-review` learns "this is a FastAPI project with PostgreSQL", that knowledge becomes available to `generate-python-unit-tests` without re-discovery.

## Directory Structure

```
memory/projects/
├── index.md (this file)
└── {project-name}/
    ├── project_profile.md    # Core project identity
    ├── technology_stack.md   # Dependencies and tools
    └── cross_skill_insights.md  # Patterns that benefit other skills
```

## Memory Files

### `project_profile.md` (Core Identity)

Created by the **first skill** that analyzes the project. Read by **all subsequent skills**.

Contents:
- Project name and purpose
- Primary language and version
- Framework and version
- Architecture pattern (monolith, microservices, clean architecture)
- Key conventions (naming, file organization, error handling)
- Repository structure overview

### `technology_stack.md` (Accumulated Knowledge)

Updated by **any skill** that discovers new technology details.

Contents:
- Dependencies and versions
- Build tools and package managers
- Database and ORM
- Cache, queue, and messaging systems
- CI/CD and deployment infrastructure
- Testing frameworks and tools

### `cross_skill_insights.md` (Cross-Skill Intelligence)

Patterns discovered by one skill that benefit others:
- Code review finds custom auth middleware → test generation knows to mock it
- Schema analysis finds specific validation rules → code review checks for enforcement
- Dependency management finds version constraints → pipeline generation uses correct versions

## Workflow for Skills

### On Start (Before Skill-Specific Memory)

```
1. Determine project name (from git remote, directory name, or repo root)
2. Check memory/projects/{project}/project_profile.md
   → If exists: Read it for project context
   → If not: Note this is a new project
3. Then proceed to skill-specific memory as usual
```

### On End (After Skill-Specific Memory Update)

```
1. If shared project memory doesn't exist:
   → Create project_profile.md with basics learned during this invocation
2. If shared project memory exists but skill learned new info:
   → Update technology_stack.md with new discoveries
   → Add cross-skill insights if applicable
3. Add freshness timestamp: <!-- Last Updated: YYYY-MM-DD -->
```

## Example

After first `python-code-review` invocation:

```markdown
<!-- Last Updated: 2026-02-10 -->
# Project Profile - my-api

## Identity
- **Language**: Python 3.11
- **Framework**: FastAPI 0.104
- **Architecture**: Clean Architecture with dependency injection

## Conventions
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **File Organization**: `app/{domain}/{layer}.py` (e.g., `app/users/service.py`)
- **Error Handling**: Custom exception hierarchy in `app/exceptions/`
```

Then `generate-python-unit-tests` reads this and immediately knows the project structure without re-discovery.

---

*Last Updated: 2026-02-10*
