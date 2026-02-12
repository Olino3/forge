---
id: "azure/index"
domain: azure
title: "Azure Context Index"
type: index
estimatedTokens: 1550
loadingStrategy: always
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
indexedFiles:
  - id: "azure/azure_functions_overview"
    path: "azure_functions_overview.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/azure_pipelines_overview"
    path: "azure_pipelines_overview.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/azure_pipelines_cicd_patterns"
    path: "azure_pipelines_cicd_patterns.md"
    type: pattern
    loadingStrategy: onDemand
  - id: "azure/azure_bicep_overview"
    path: "azure_bicep_overview.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/azure_verified_modules"
    path: "azure_verified_modules.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/azurite_setup"
    path: "azurite_setup.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/docker_compose_reference"
    path: "docker_compose_reference.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/dockerfile_reference"
    path: "dockerfile_reference.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/local_development_setup"
    path: "local_development_setup.md"
    type: reference
    loadingStrategy: onDemand
  - id: "azure/tiltfile_reference"
    path: "tiltfile_reference.md"
    type: reference
    loadingStrategy: onDemand
sections:
  - name: "Purpose"
    estimatedTokens: 23
    keywords: [purpose]
  - name: "Conceptual Overview"
    estimatedTokens: 38
    keywords: [conceptual]
  - name: "Directory Structure"
    estimatedTokens: 87
    keywords: [directory, structure]
  - name: "Context Files"
    estimatedTokens: 421
    keywords: [context, files]
  - name: "Decision Matrix"
    estimatedTokens: 72
    keywords: [decision, matrix]
  - name: "Workflow: Generate Azure Functions Project"
    estimatedTokens: 44
    keywords: [workflow, generate, azure, functions, project]
  - name: "Workflow: Generate Azure Pipelines"
    estimatedTokens: 51
    keywords: [workflow, generate, azure, pipelines]
  - name: "Compact Approach"
    estimatedTokens: 25
    keywords: [compact, approach]
  - name: "Related Files"
    estimatedTokens: 24
    keywords: [related, files]
  - name: "Official Documentation"
    estimatedTokens: 32
    keywords: [official, documentation]
tags: [azure, index, navigation, functions, pipelines, bicep, azurite, docker, tilt]
---

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
├── dockerfile_reference.md          # Dockerfile patterns for function apps
├── azurite_setup.md                 # Azurite storage emulator setup
# Azure Pipelines Context
├── azure_pipelines_overview.md      # Azure Pipelines YAML syntax and structure
├── azure_pipelines_cicd_patterns.md # CI/CD pipeline patterns and best practices
└── azure_bicep_overview.md          # Bicep infrastructure as code
├── dockerfile_reference.md          # Dockerfile patterns
├── azurite_setup.md                 # Azurite storage emulator
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

**When to load**: Always load when generating Azure Pipelines

**Contains**:
- Azure Pipelines YAML syntax and structure
- Stages, jobs, steps, and tasks
- Triggers (branch, PR, scheduled)
- Variables and conditions
- Templates and reusability
- Environments and approvals

**Quick Reference**:
- Pipeline structure: Trigger → Pool → Stages → Jobs → Steps
- Use stages for major phases (Build, Test, Deploy)
- Use deployment jobs for environments with approval gates
- Links to official Azure Pipelines docs

---

### 8. `azure_pipelines_cicd_patterns.md`

**When to load**: When deciding on pipeline architecture

**Contains**:
- Separate CI/CD vs combined pipeline patterns
- Infrastructure as Code (IAC) pipeline patterns
- Multi-environment deployment strategies
- Pipeline organization for monorepos
- Common pipeline structures (Python, Node.js, .NET, Docker)
- Best practices and anti-patterns

**Quick Reference**:
- Separate CI/CD: Build once, deploy many times
- Combined CI/CD: Simpler for small projects
- IAC pipeline: Separate infrastructure from application deployments
- Decision matrix for choosing pipeline architecture

---

### 9. `azure_bicep_overview.md`

**When to load**: When generating infrastructure as code

**Contains**:
- Bicep syntax and structure
- Resource declarations and modules
- Parameters and parameter files (.bicepparams)
- Bicep CLI commands
- Common resource types
- Best practices for Bicep templates

**Quick Reference**:
- Bicep compiles to ARM templates
- Use modules for reusable components
- targetScope: subscription, resourceGroup, managementGroup, tenant
- Use parameters files for environment-specific configuration
- Links to official Bicep docs and resource references

---

## Decision Matrix

| Task | Load These Files |
|------|------------------|
| **Azure Functions** |
| Generate new Azure Functions project | `azure_functions_overview.md`, `local_development_setup.md` |
| Generate Tiltfile | `tiltfile_reference.md`, `local_development_setup.md` |
| Generate docker-compose.yml | `docker_compose_reference.md`, `local_development_setup.md` |
| Generate Dockerfile | `dockerfile_reference.md` |
| Setup Azurite | `azurite_setup.md`, `local_development_setup.md` |
| Full Functions project setup | All Azure Functions files |
| **Azure Pipelines** |
| Generate Azure Pipelines | `azure_pipelines_overview.md`, `azure_pipelines_cicd_patterns.md` |
| Generate Bicep infrastructure | `azure_bicep_overview.md` |
| Generate CI/CD with infrastructure | `azure_pipelines_overview.md`, `azure_pipelines_cicd_patterns.md`, `azure_bicep_overview.md` |
| Decide pipeline architecture | `azure_pipelines_cicd_patterns.md` |

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

1. **Read this index** to understand available context
2. **Load `azure_pipelines_cicd_patterns.md`** to understand architecture options
3. **Ask user** about pipeline structure (separate vs combined)
4. **Load `azure_pipelines_overview.md`** for pipeline syntax and patterns
5. **Load `azure_bicep_overview.md`** if infrastructure is needed
6. **Generate pipeline YAML files** (CI, CD, IAC or combined)
7. **Generate Bicep templates** with environment parameters
8. **Create pipeline templates** for reusability
9. **Store pipeline configuration** in memory

## Compact Approach

All context files follow the compact approach:
- Quick reference tables
- Links to official documentation
- Brief code examples (not exhaustive)
- "What to look for" guidance
- "When to use" decision trees

## Related Files

### Skills
- `../../skills/generate-azure-functions/SKILL.md` - Azure Functions generation workflow
- `../../skills/generate-azure-pipelines/SKILL.md` - Azure Pipelines generation workflow

### Memory
- `../../memory/skills/generate-azure-functions/index.md` - Azure Functions memory structure
- `../../memory/skills/generate-azure-pipelines/index.md` - Azure Pipelines memory structure

## Official Documentation

### Azure Functions
- [Azure Functions Overview](https://learn.microsoft.com/azure/azure-functions/functions-overview)
- [Azurite Emulator](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
- [Tilt Documentation](https://docs.tilt.dev/)

### Azure Pipelines
- [Azure Pipelines Documentation](https://learn.microsoft.com/azure/devops/pipelines/)
- [Azure Pipelines YAML Schema](https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/)
- [Pipeline Tasks Reference](https://learn.microsoft.com/azure/devops/pipelines/tasks/)

### Azure Bicep
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Bicep GitHub Repository](https://github.com/Azure/bicep)
- [Azure Resource Reference](https://learn.microsoft.com/azure/templates/)
