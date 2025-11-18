# Azure Functions Context Index

## Purpose

This directory contains **shared, static** knowledge about Azure Functions development, local development environments, and deployment patterns. These files provide consistent guidance for generating and working with Azure Functions projects.

## Conceptual Overview

### Context vs Memory

- **Context** (this directory): **Shared, static** Azure Functions standards, templates, and best practices
- **Memory** (`../../memory/skills/generate-azure-functions/`): **Project-specific, dynamic** generated project configurations and customizations

**Example**:
- Context says: "Here's a template Tiltfile for Azure Functions with Azurite"
- Memory records: "In this project, we use 3 function apps with custom ports 7071, 7072, 7073"

## Directory Structure

```
azure/
├── index.md                          # This file - navigation guide
├── azure_functions_overview.md      # Azure Functions v1 vs v2 comparison
├── local_development_setup.md       # Tilt + Azurite setup guide
├── tiltfile_reference.md            # Tiltfile patterns for Azure Functions
├── docker_compose_reference.md      # Docker Compose patterns
├── dockerfile_reference.md          # Dockerfile patterns for function apps
└── azurite_setup.md                 # Azurite storage emulator setup
```

## Context Files

### 1. `azure_functions_overview.md`

**When to load**: Always load when generating Azure Functions

**Contains**:
- v1 vs v2 programming model comparison
- Project structure differences
- When to use each model
- Migration considerations

**Quick Reference**:
- v1: function.json + __init__.py per function
- v2: Single function_app.py with decorators
- Links to official docs

---

### 2. `local_development_setup.md`

**When to load**: Always load when setting up local development

**Contains**:
- Tilt + Azurite architecture overview
- Development workflow (live reload, debugging)
- Environment variable configuration
- Connection strings for local development

**Quick Reference**:
- Azurite ports: Blob (10000), Queue (10001), Table (10002)
- Function app ports: Start at 7071, increment per function
- Required environment variables

---

### 3. `tiltfile_reference.md`

**When to load**: When generating Tiltfile

**Contains**:
- Tiltfile structure and syntax
- docker_build() patterns for functions
- live_update configurations
- Resource dependencies
- Service selection patterns

**Quick Reference**:
- Use docker_build() for each function app
- Configure live_update for hot reload
- Set resource_deps for Azurite dependency
- Link to Tilt docs

---

### 4. `docker_compose_reference.md`

**When to load**: When generating docker-compose.yml

**Contains**:
- Docker Compose service definitions
- Environment variable patterns
- Port mapping conventions
- Volume configurations
- Azurite service setup

**Quick Reference**:
- Each function = one service
- Standard environment variables for local dev
- depends_on: azurite

---

### 5. `dockerfile_reference.md`

**When to load**: When generating Dockerfiles

**Contains**:
- Base image selection (Python, Node, .NET)
- Poetry/pip/npm setup patterns
- Azure Functions runtime configuration
- Working directory conventions
- Build optimization

**Quick Reference**:
- Base images: mcr.microsoft.com/azure-functions/*
- Install dependencies in Dockerfile
- Set AzureWebJobsScriptRoot

---

### 6. `azurite_setup.md`

**When to load**: When setting up Azurite

**Contains**:
- Azurite Dockerfile
- Initialization script patterns
- Container/table/queue creation
- Connection string format
- Test data population

**Quick Reference**:
- Default account: devstoreaccount1
- Use environment variable for account key
- Initialize storage resources on startup

---

## Decision Matrix

| Task | Load These Files |
|------|------------------|
| Generate new Azure Functions project | `azure_functions_overview.md`, `local_development_setup.md` |
| Generate Tiltfile | `tiltfile_reference.md`, `local_development_setup.md` |
| Generate docker-compose.yml | `docker_compose_reference.md`, `local_development_setup.md` |
| Generate Dockerfile | `dockerfile_reference.md` |
| Setup Azurite | `azurite_setup.md`, `local_development_setup.md` |
| Full project setup | All files |

## Workflow: Generate Azure Functions Project

1. **Read this index** to understand available context
2. **Load `azure_functions_overview.md`** to understand v1 vs v2
3. **Ask user** which programming model to use
4. **Load `local_development_setup.md`** for environment setup
5. **Load specific references** (Tiltfile, Dockerfile, etc.) as needed
6. **Generate project** using Azure Functions CLI
7. **Create development environment** (Tilt + Azurite)
8. **Store project-specific config** in memory

## Compact Approach

All context files follow the compact approach:
- Quick reference tables
- Links to official documentation
- Brief code examples (not exhaustive)
- "What to look for" guidance
- "When to use" decision trees

## Related Files

- `../../memory/skills/generate-azure-functions/index.md` - Memory structure
- `../../skills/generate-azure-functions/SKILL.md` - Skill workflow
- Official Azure Functions docs: https://learn.microsoft.com/azure/azure-functions/

## Official Documentation

- [Azure Functions Overview](https://learn.microsoft.com/azure/azure-functions/functions-overview)
- [Azure Functions Python Developer Guide](https://learn.microsoft.com/azure/azure-functions/functions-reference-python)
- [Azurite Emulator](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
- [Tilt Documentation](https://docs.tilt.dev/)
