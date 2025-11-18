# Azure Context Index

## Purpose

This directory contains **shared, static** knowledge about Azure development, including Azure Functions, Azure Pipelines, Bicep infrastructure as code, and Azure Verified Modules. These files provide consistent guidance for Azure-related project generation.

## Conceptual Overview

### Context vs Memory

- **Context** (this directory): **Shared, static** Azure standards, AVM modules, templates, and best practices
- **Memory** (`../../memory/skills/`): **Project-specific, dynamic** generated configurations and customizations

**Example**:
- Context says: "Use AVM module avm/res/storage/storage-account for Storage Accounts"
- Memory records: "This project uses Storage Account with GRS and private endpoints"

## Directory Structure

```
azure/
├── index.md                          # This file - navigation guide
# Azure Functions Context
├── azure_functions_overview.md      # Azure Functions v1 vs v2 comparison
├── local_development_setup.md       # Tilt + Azurite setup guide
├── tiltfile_reference.md            # Tiltfile patterns
├── docker_compose_reference.md      # Docker Compose patterns
├── dockerfile_reference.md          # Dockerfile patterns
├── azurite_setup.md                 # Azurite storage emulator
# Azure Pipelines Context
├── azure_pipelines_overview.md      # Pipelines YAML syntax
├── azure_pipelines_cicd_patterns.md # CI/CD patterns
# Azure Bicep Context
├── azure_bicep_overview.md          # Bicep syntax and structure
└── azure_verified_modules.md        # Azure Verified Modules (AVM)
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

### 7. `azure_pipelines_overview.md`

**When to load**: When generating Azure Pipelines

**Contains**: Pipelines YAML syntax, stages, jobs, steps, triggers, variables, templates

**Quick Reference**: Pipeline flow: Trigger → Pool → Stages → Jobs → Steps

---

### 8. `azure_pipelines_cicd_patterns.md`

**When to load**: When deciding pipeline architecture

**Contains**: Separate vs combined CI/CD, IAC patterns, multi-environment strategies

**Quick Reference**: Separate CI/CD = build once, deploy many; Combined = simpler for small projects

---

### 9. `azure_bicep_overview.md`

**When to load**: When generating Bicep infrastructure

**Contains**: Bicep syntax, resource declarations, modules, parameters, bicepparams files

**Quick Reference**: Bicep compiles to ARM; use modules for reusability; targetScope sets deployment level

---

### 10. `azure_verified_modules.md`

**When to load**: Always load when generating Bicep infrastructure

**Contains**: Azure Verified Modules (AVM) usage, module registry paths, standard parameters, best practices

**Quick Reference**: AVM modules: `br/public:avm/res/{provider}/{type}:{version}`; always pin versions; use for production-ready infrastructure

---

## Decision Matrix

| Task | Load These Files |
|------|------------------|
| **Azure Functions** |
| Generate Azure Functions project | `azure_functions_overview.md`, `local_development_setup.md` |
| Generate Tiltfile | `tiltfile_reference.md`, `local_development_setup.md` |
| Generate docker-compose.yml | `docker_compose_reference.md`, `local_development_setup.md` |
| **Azure Pipelines** |
| Generate Azure Pipelines | `azure_pipelines_overview.md`, `azure_pipelines_cicd_patterns.md` |
| **Azure Bicep** |
| Generate Bicep infrastructure | `azure_bicep_overview.md`, `azure_verified_modules.md` |

## Workflow: Generate Azure Functions Project

1. **Read this index** to understand available context
2. **Load `azure_functions_overview.md`** to understand v1 vs v2
3. **Ask user** which programming model to use
4. **Load `local_development_setup.md`** for environment setup
5. **Load specific references** (Tiltfile, Dockerfile, etc.) as needed
6. **Generate project** using Azure Functions CLI
7. **Create development environment** (Tilt + Azurite)
8. **Store project-specific config** in memory

## Workflow: Generate Azure Pipelines

1. Read this index
2. Load `azure_pipelines_cicd_patterns.md` for architecture decisions
3. Load `azure_pipelines_overview.md` for YAML syntax
4. Load `azure_bicep_overview.md` if generating infrastructure pipelines
5. Generate pipeline YAML files and Bicep templates
6. Store configuration in memory

## Workflow: Generate Bicep Infrastructure

1. Read this index
2. Load `azure_verified_modules.md` for AVM module patterns (always)
3. Load `azure_bicep_overview.md` for Bicep syntax
4. Map requirements to AVM modules
5. Generate main.bicep with AVM module references
6. Generate bicepparams files for environments
7. Store configuration in memory

## Compact Approach

All context files follow the compact approach:
- Quick reference tables
- Links to official documentation
- Brief code examples (not exhaustive)
- "What to look for" guidance
- "When to use" decision trees

## Related Files

### Skills
- `../../skills/generate-azure-functions/SKILL.md` - Azure Functions skill
- `../../skills/generate-azure-pipelines/SKILL.md` - Azure Pipelines skill
- `../../skills/generate-azure-bicep/SKILL.md` - Azure Bicep skill

### Memory
- `../../memory/skills/generate-azure-functions/index.md` - Functions memory
- `../../memory/skills/generate-azure-pipelines/index.md` - Pipelines memory
- `../../memory/skills/generate-azure-bicep/index.md` - Bicep memory

## Official Documentation

### Azure Functions
- [Azure Functions Overview](https://learn.microsoft.com/azure/azure-functions/functions-overview)
- [Azurite Emulator](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
- [Tilt Documentation](https://docs.tilt.dev/)

### Azure Pipelines
- [Azure Pipelines](https://learn.microsoft.com/azure/devops/pipelines/)
- [YAML Schema](https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/)

### Azure Bicep
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
- [AVM Registry](https://aka.ms/avm)
