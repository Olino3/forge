---
name: generate-azure-pipelines
description: Generate Azure DevOps pipelines with CI/CD workflows and Bicep infrastructure as code
version: "0.1.0-alpha"
context:
  primary: [azure]
  topics: [azure_pipelines_overview, azure_pipelines_cicd_patterns, azure_bicep_overview]
memory:
  scope: per-project
  files: [pipeline_config.md, generated_files.md, bicep_resources.md, customizations.md]
---

# Skill: generate-azure-pipelines

**Version**: 0.1.0-alpha
**Purpose**: Generate Azure DevOps pipelines with CI/CD workflows and Bicep infrastructure as code
**Author**: The Forge
**Last Updated**: 2025-11-18

---

## Title

**Generate Azure Pipelines** - Create production-ready Azure Pipelines with CI/CD workflows and Bicep infrastructure templates

---

## File Structure

```
forge-plugin/skills/generate-azure-pipelines/
├── SKILL.md                  # This file - mandatory workflow
├── examples.md               # Usage scenarios and examples
├── scripts/
│   └── pipeline_generator.py  # Helper script for pipeline generation
└── templates/
    ├── ci-pipeline-template.yml           # CI pipeline template
    ├── cd-pipeline-template.yml           # CD pipeline template
    ├── iac-pipeline-template.yml          # Infrastructure pipeline template
    ├── combined-cicd-template.yml         # Combined CI/CD template
    ├── main-bicep-template.bicep          # Main Bicep template
    ├── bicepparams-template.bicep         # Bicep parameters template
    ├── storage-module-template.bicep      # Storage Account module
    ├── function-app-module-template.bicep # Function App module
    ├── build-job-template.yml             # Reusable build job template
    └── deploy-job-template.yml            # Reusable deploy job template
```

---

## Interface References

- [ContextProvider](../../interfaces/context_provider.md) — `getDomainIndex("azure")`, `getConditionalContext("azure", topic)`
- [MemoryStore](../../interfaces/memory_store.md) — `getSkillMemory("generate-azure-pipelines", project)`, `update()`

**Context** (via ContextProvider):
- `contextProvider.getDomainIndex("azure")` — Azure context navigation
- `contextProvider.getConditionalContext("azure", "azure_pipelines_overview")` — Pipeline structure and syntax
- `contextProvider.getConditionalContext("azure", "azure_pipelines_cicd_patterns")` — CI/CD patterns and decision matrix
- `contextProvider.getConditionalContext("azure", "azure_bicep_overview")` — Bicep infrastructure as code

**Memory** (via MemoryStore):
- `memoryStore.getSkillMemory("generate-azure-pipelines", project)` returns per-project files:
  - `pipeline_config.md` — Previous pipeline configurations
  - `generated_files.md` — List of generated files
  - `bicep_resources.md` — Infrastructure resources
  - `customizations.md` — User-specific changes

---

## Design Requirements

### Core Functionality

This skill must:
1. **Ask user about pipeline structure** (separate CI/CD or combined)
2. **Ask about project requirements** (runtime, build tool, deployment targets)
3. **Generate `.azure/` directory** with pipelines, bicep, docs, templates, variables
4. **Create CI pipeline** for building and testing
5. **Create CD pipeline** for deploying to environments
6. **Create IAC pipeline** for deploying infrastructure
7. **Generate Bicep templates** with environment-specific parameters
8. **Create pipeline templates** for reusability
9. **Store pipeline configuration** in memory for future reference

### Output Requirements

Generate a **complete `.azure/` directory structure** with:
- Pipeline YAML files (CI, CD, IAC, or combined)
- Bicep infrastructure templates
- Environment-specific parameter files (.bicepparams)
- Pipeline templates for reusable jobs
- Variable files for environment-specific configuration
- Documentation explaining the setup

### Directory Structure

```
.azure/
├── bicep/
│   ├── modules/                        # Reusable Bicep modules
│   │   ├── storage-account.bicep
│   │   ├── function-app.bicep
│   │   └── app-service.bicep
│   ├── main.bicep                      # Main infrastructure template
│   ├── main.development.bicepparams    # Development parameters
│   ├── main.staging.bicepparams        # Staging parameters
│   └── main.production.bicepparams     # Production parameters
├── docs/
│   └── README.md                       # Pipeline and infrastructure docs
├── pipelines/
│   ├── templates/                      # Reusable pipeline templates
│   │   ├── build-job.yml
│   │   └── deploy-job.yml
│   └── variables/                      # Variable files
│       ├── dev-variables.yml
│       ├── staging-variables.yml
│       └── prod-variables.yml
├── ci-pipeline.yml                     # CI pipeline (if separate)
├── cd-pipeline.yml                     # CD pipeline (if separate)
├── iac-pipeline.yml                    # Infrastructure pipeline
└── combined-cicd-pipeline.yml          # Combined pipeline (if requested)
```

### Quality Requirements

Generated pipelines must:
- **Follow Azure Pipelines best practices** (stages, jobs, environments)
- **Use templates for reusability** (build and deploy jobs)
- **Support multiple environments** (development, staging, production)
- **Include proper triggers** (branch, PR, path filters)
- **Use variable groups** (environment-specific configuration)
- **Include approval gates** (production deployments)
- **Be well-documented** (inline comments, README)

---

## Prompting Guidelines

### User Questions Framework

Use **Socratic method** to gather requirements. Ask questions in this order:

#### 1. Pipeline Architecture

**Question**: "Do you want separate CI and CD pipelines, or a combined CI/CD pipeline?"

**Options**:
- **Separate**: CI builds/tests on all branches, CD deploys specific versions to environments
- **Combined**: Single pipeline handles build, test, and deploy in one workflow

**Follow-up**: "This affects pipeline structure and artifact management. Separate pipelines are better for complex projects with frequent deployments."

#### 2. Project Runtime

**Question**: "What runtime does your project use?"

**Options**:
- Python (specify version: 3.9, 3.10, 3.11, 3.12)
- Node.js (specify version: 16, 18, 20)
- .NET (specify version: 6.0, 7.0, 8.0)
- Docker (containerized application)

**Follow-up**: "This determines the agent pool and build tasks."

#### 3. Build Tool

**Question**: "What build tool do you use?"

**Options**:
- Python: pip, Poetry, pipenv
- Node.js: npm, yarn, pnpm
- .NET: dotnet CLI, MSBuild

**Follow-up**: "This affects dependency management and build steps."

#### 4. Deployment Target

**Question**: "Where do you want to deploy?"

**Options**:
- Azure Functions
- Azure App Service
- Azure Container Instances
- Azure Kubernetes Service (AKS)
- Azure Static Web Apps

**Follow-up**: "This determines deployment tasks and service connections needed."

#### 5. Environments

**Question**: "Which environments do you need?"

**Options** (can select multiple):
- Development (auto-deploy from develop branch)
- Staging (auto-deploy from main branch)
- Production (manual approval required)
- Custom environments

**Follow-up**: "This creates environment-specific parameter files and deployment stages."

#### 6. Infrastructure Requirements

**Question**: "What Azure resources does your application need?"

**Options** (can select multiple):
- Storage Account (Blob, Queue, Table)
- Function App
- App Service Plan
- Key Vault (for secrets)
- Application Insights (for monitoring)
- SQL Database
- Cosmos DB
- Virtual Network
- Custom resources

**Follow-up**: "This generates Bicep modules for your infrastructure."

#### 7. Existing Infrastructure

**Question**: "Do you have existing Azure resources to reference, or create everything new?"

**Options**:
- Create all new resources (full IaC)
- Reference existing resources (partial IaC)
- No infrastructure deployment (app-only pipelines)

**Follow-up**: "This affects Bicep template structure and existing resource references."

---

## Instructions

### Mandatory Workflow

**IMPORTANT**: Follow these steps **in order**. Do not skip steps.

---

#### Step 1: Initial Analysis

**Objective**: Understand the current project context

**Actions**:
1. Identify the current working directory
2. Check if `.azure/` directory already exists
3. Check if `azure-pipelines.yml` or similar files exist
4. Identify project structure (language, build files, dependencies)

**Verification**: Confirm project type detected before proceeding

---

#### Step 2: Load Index Files

**Objective**: Understand available context and memory structure

**Actions**:
1. Load Azure domain index via `contextProvider.getDomainIndex("azure")`
2. Identify which context topics will be needed based on requirements

**Verification**: Domain index loaded, know which context topics to load next

---

#### Step 3: Load Project Memory

**Objective**: Check for existing project-specific pipeline configurations

**Actions**:
1. Determine project name from current directory or user input
2. Load project memory via `memoryStore.getSkillMemory("generate-azure-pipelines", project)`
3. If memory exists, review all memory files:
   - `pipeline_config.md` - Previous pipeline structure
   - `generated_files.md` - List of generated files
   - `bicep_resources.md` - Infrastructure resources
   - `customizations.md` - User-specific changes

**Verification**: Memory loaded if exists; ready to use previous configurations

---

#### Step 4: Load Azure Pipelines Context

**Objective**: Load Azure Pipelines and Bicep knowledge

**Actions**:
1. Load `contextProvider.getConditionalContext("azure", "azure_pipelines_overview")` - Pipeline structure, stages, jobs, tasks
2. Load `contextProvider.getConditionalContext("azure", "azure_pipelines_cicd_patterns")` - CI/CD patterns and decision matrix
3. Load `contextProvider.getConditionalContext("azure", "azure_bicep_overview")` - Bicep templates and syntax

**Verification**: Context loaded, understand pipeline patterns and Bicep structure

---

#### Step 5: Gather Requirements

**Objective**: Ask user Socratic questions to gather all requirements

**Actions**:
1. Ask about **pipeline architecture** (separate vs combined)
2. Ask about **project runtime** (Python, Node.js, .NET, Docker)
3. Ask about **build tool** (pip/Poetry, npm/yarn, dotnet)
4. Ask about **deployment target** (Functions, App Service, AKS, etc.)
5. Ask about **environments** (dev, staging, prod)
6. Ask about **infrastructure requirements** (storage, databases, networking)
7. Ask about **existing infrastructure** (new or reference existing)

**Verification**: All requirements gathered, user confirmed ready to proceed

---

#### Step 6: Generate Pipeline Structure

**Objective**: Create `.azure/` directory with pipelines and Bicep templates

**Actions**:

1. **Create directory structure**:
   ```bash
   mkdir -p .azure/{bicep/modules,docs,pipelines/{templates,variables}}
   ```

2. **Generate pipeline files** based on user choice:
   - If **separate**: Create `ci-pipeline.yml`, `cd-pipeline.yml`, `iac-pipeline.yml`
   - If **combined**: Create `combined-cicd-pipeline.yml`, `iac-pipeline.yml`

3. **Generate Bicep templates**:
   - `bicep/main.bicep` - Main infrastructure template
   - `bicep/main.{environment}.bicepparams` - Environment-specific parameters
   - `bicep/modules/*.bicep` - Resource-specific modules

4. **Generate pipeline templates**:
   - `pipelines/templates/build-job.yml` - Reusable build job
   - `pipelines/templates/deploy-job.yml` - Reusable deployment job

5. **Generate variable files**:
   - `pipelines/variables/{environment}-variables.yml` - Environment-specific variables

6. **Generate documentation**:
   - `.azure/docs/README.md` - Explanation of pipeline structure and usage

**Verification**: All files created, no errors during generation

---

#### Step 7: Customize Templates

**Objective**: Populate templates with project-specific values

**Actions**:
1. Replace placeholders in pipeline YAML files:
   - `{{PROJECT_NAME}}` - Project name
   - `{{RUNTIME}}` - Runtime and version
   - `{{BUILD_COMMAND}}` - Build command
   - `{{TEST_COMMAND}}` - Test command
   - `{{DEPLOY_TARGET}}` - Deployment target

2. Replace placeholders in Bicep templates:
   - `{{RESOURCE_PREFIX}}` - Resource naming prefix
   - `{{LOCATION}}` - Azure region
   - `{{SKU}}` - Resource SKU per environment

3. Configure triggers based on requirements:
   - CI: Trigger on all branches
   - CD: Trigger on main/develop or manual
   - IAC: Trigger on changes to `.azure/bicep/**`

**Verification**: Templates customized with correct values

---

#### Step 8: Validate Generated Files

**Objective**: Ensure generated pipelines are syntactically correct

**Actions**:
1. Check YAML syntax for all pipeline files
2. Validate Bicep templates using `az bicep build` (if Azure CLI available)
3. Verify all referenced templates exist
4. Check that variable files are properly structured

**Verification**: No syntax errors, all files valid

---

#### Step 9: Present Results

**Objective**: Show user what was generated and next steps

**Actions**:
1. Display generated directory structure
2. List all created files with their purposes
3. Provide instructions for setting up Azure DevOps project:
   - Create service connections
   - Create variable groups
   - Create environments with approvals
   - Import pipeline YAML files

4. Explain how to customize further:
   - Add more environments
   - Add more resources to Bicep
   - Create custom pipeline templates

**Verification**: User understands what was generated and how to use it

---

#### Step 10: Update Project Memory

**Objective**: Store configuration for future reference

**Actions**:
1. Use `memoryStore.update("generate-azure-pipelines", project, "pipeline_config.md", content)` with:
   - Pipeline architecture (separate/combined)
   - Runtime and build tool
   - Deployment target
   - Environments

2. Use `memoryStore.update("generate-azure-pipelines", project, "generated_files.md", content)` with:
   - List all generated files with timestamps
   - Note which templates were used

3. Use `memoryStore.update("generate-azure-pipelines", project, "bicep_resources.md", content)` with:
   - List Azure resources in Bicep templates
   - Resource naming conventions
   - Environment-specific configurations

4. Use `memoryStore.update("generate-azure-pipelines", project, "customizations.md", content)` with:
   - User-specific requirements
   - Deviations from standard templates
   - Custom pipeline steps

**Verification**: Memory files created/updated with all relevant information

---

### Compliance Checklist

Before completing this skill, verify:

- [ ] User questions asked and answered (Step 5)
- [ ] `.azure/` directory created with correct structure (Step 6)
- [ ] Pipeline YAML files generated (CI, CD, IAC or combined) (Step 6)
- [ ] Bicep templates generated (main.bicep, modules, .bicepparams) (Step 6)
- [ ] Pipeline templates created (build-job, deploy-job) (Step 6)
- [ ] Variable files created for each environment (Step 6)
- [ ] Documentation generated (.azure/docs/README.md) (Step 6)
- [ ] Templates customized with project-specific values (Step 7)
- [ ] Generated files validated (YAML, Bicep syntax) (Step 8)
- [ ] Results presented to user with next steps (Step 9)
- [ ] Project memory updated (Step 10)

---

## Best Practices

### Pipeline Organization

1. **Separate concerns**: Keep CI, CD, and IAC pipelines separate for large projects
2. **Use templates**: Create reusable build and deploy job templates
3. **Use variable groups**: Store environment-specific configuration in Azure DevOps Library
4. **Use environments**: Track deployments and require approvals for production
5. **Use conditions**: Control when stages run based on branch or variables

### Bicep Templates

1. **Use modules**: Break down infrastructure into reusable components
2. **Use parameters files**: Environment-specific configurations
3. **Use descriptive names**: Clear resource and parameter names
4. **Add descriptions**: Document all parameters and outputs
5. **Use variables for computed values**: Keep parameters simple
6. **Validate before deploying**: Use `az deployment validate` and `what-if`

### Security

1. **Never hardcode secrets**: Use Azure Key Vault and variable groups
2. **Use service connections**: Secure Azure authentication
3. **Require approvals**: Production deployments need manual approval
4. **Use managed identities**: Avoid storing credentials
5. **Limit permissions**: Grant least privilege to service principals

### Documentation

1. **Document pipeline structure**: Explain stages, jobs, and dependencies
2. **Document Bicep resources**: Explain what each module creates
3. **Document setup steps**: How to configure Azure DevOps project
4. **Document customization**: How to add more environments or resources
5. **Keep README updated**: As pipelines evolve

---

## Additional Notes

### Service Connections

Users will need to create service connections in Azure DevOps for:
- Azure Resource Manager (for deploying resources)
- Docker Registry (if using containers)
- Other external services

### Variable Groups

Users should create variable groups in Azure DevOps Library for:
- Development environment variables
- Staging environment variables
- Production environment variables (with secrets)

### Environments

Users should create environments in Azure DevOps for:
- Development (no approval required)
- Staging (optional approval)
- Production (manual approval required)

### Triggers

Generated pipelines use:
- **CI**: Trigger on all branches, run build and test
- **CD**: Trigger on artifact from CI, deploy to environments
- **IAC**: Trigger on changes to `.azure/bicep/**`, deploy infrastructure

### Artifacts

- CI pipeline publishes build artifacts
- CD pipeline downloads artifacts from CI
- IAC pipeline doesn't use artifacts (uses Bicep files from repo)

---

## Version History

### v1.1.0 (2025-07-15)
- Phase 4 Migration: Replaced hardcoded `../../context/` and `../../memory/` paths with ContextProvider and MemoryStore interface calls
- Added YAML frontmatter with context/memory declarations
- Added Interface References section

### v1.0.0 (2025-11-18)

**Initial Release**
- Complete Azure Pipelines generation with CI/CD workflows
- Bicep infrastructure as code templates
- Support for separate or combined CI/CD pipelines
- Support for Python, Node.js, and .NET projects
- Multi-environment deployment (dev, staging, prod)
- Reusable pipeline templates
- Environment-specific Bicep parameters
- Memory system for configuration tracking
- Comprehensive context files for Azure Pipelines and Bicep
