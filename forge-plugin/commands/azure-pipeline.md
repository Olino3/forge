---
name: azure-pipeline
description: "Orchestrate Azure DevOps CI/CD pipelines with build, test, and deployment automation"
category: orchestration
complexity: intermediate
skills: [generate-azure-pipelines, generate-azure-bicep]
context: [azure, commands/pipeline_patterns]
---

# /azure-pipeline - Azure DevOps CI/CD Orchestration

## Triggers
- Setting up continuous integration for new projects
- Configuring deployment pipelines to Azure services
- Implementing build, test, and release automation
- Creating multi-stage pipelines with approvals

## Usage
```
/azure-pipeline [pipeline-name] [--type ci|cd|ci-cd] [--target webapp|function|container|aks] [--stages build,test,deploy]
```

**Parameters**:
- `pipeline-name`: Name of the pipeline (default: project name)
- `--type`: Pipeline type (default: ci-cd)
  - `ci`: Continuous Integration only (build + test)
  - `cd`: Continuous Deployment only (deploy to environments)
  - `ci-cd`: Full CI/CD pipeline
- `--target`: Deployment target (default: detect from project)
  - `webapp`: Azure App Service (Web Apps)
  - `function`: Azure Functions
  - `container`: Azure Container Registry + Container Instances
  - `aks`: Azure Kubernetes Service
- `--stages`: Comma-separated stages (default: build,test,deploy)

## Workflow

### Step 1: Analyze Project

1. Detect project type and language:
   - Check for `package.json`, `requirements.txt`, `*.csproj`, etc.
   - Identify runtime and dependencies
   - Determine build and test commands
2. Identify deployment target:
   - Existing Azure resources or new deployment
   - Environment configuration (dev, staging, prod)
3. Determine pipeline requirements:
   - Security scanning needed?
   - Database migrations required?
   - Infrastructure deployment (Bicep/ARM)?

### Step 2: Load Context & Memory

**Context Loading** (via ContextProvider):
1. Load pipeline best practices: `contextProvider.getConditionalContext("commands", "pipeline_patterns")`
2. Load Azure-specific patterns: `contextProvider.getConditionalContext("azure", "index")`
3. Load pipeline configuration: `contextProvider.getConditionalContext("azure", "azure_pipelines")`

**Memory Loading** (via MemoryStore):
1. Determine project name
2. Load existing Azure setup: `memoryStore.getCommandMemory("azure-pipeline", project)`
3. Load pipeline patterns: `memoryStore.getSkillMemory("generate-azure-pipelines", project)`
4. Check for existing infrastructure as code (Bicep files)

### Step 3: Gather Pipeline Configuration

If configuration not clear from project, gather interactively:

**Questions**:
- What Azure subscription and resource group?
- What environments? (dev, staging, prod)
- Manual approval required for production?
- What tests to run? (unit, integration, e2e)
- Any pre-deployment steps? (migrations, seed data)
- Service principal or managed identity for deployment?

### Step 4: Delegate to Skills

**Generate Azure Pipeline**:
```
skill:generate-azure-pipelines --pipeline-name {name} --type {type} --language {detected} --target {target}
```

**Generate Infrastructure (if needed)**:
```
skill:generate-azure-bicep --resource-type {target} --environment {env}
```

Skills handle:
- YAML pipeline configuration
- Build and test stages
- Deployment stages with environment gates
- Variable groups and secrets configuration
- Infrastructure as Code (Bicep templates)
- Service connection setup instructions

### Step 5: Configure Pipeline Security

1. Identify required secrets and variables:
   - Azure service principal credentials
   - Database connection strings
   - API keys and tokens
2. Create variable group recommendations
3. Configure branch policies:
   - Require PR for main/master
   - Require build validation
   - Code review requirements
4. Set up environment approvals for production

### Step 6: Generate Output & Update Memory

**Output**:
Save pipeline documentation to `/claudedocs/azure-pipeline_{name}_{date}.md`:

```markdown
# Azure Pipeline - {Pipeline Name}
**Date**: {date}
**Command**: /azure-pipeline {full invocation}
**Type**: {ci|cd|ci-cd}
**Target**: {deployment target}

## Pipeline Overview
**File**: `azure-pipelines.yml`
**Trigger**: Push to main, PRs
**Stages**: {list of stages}

## Stages

### Build Stage
- Restore dependencies
- Compile/build application
- Run linters and static analysis
- Create build artifacts

### Test Stage
- Unit tests with coverage
- Integration tests
- Security scanning (dependency check, SAST)
- Code quality gates

### Deploy Stage (Dev)
- Deploy to development environment
- Run smoke tests
- Auto-deployment (no approval)

### Deploy Stage (Staging)
- Deploy to staging environment
- Run full integration test suite
- Require approval from QA team

### Deploy Stage (Production)
- Deploy to production environment
- Blue-green or canary deployment
- Require approval from release manager
- Automated rollback on failure

## Setup Instructions

### 1. Azure DevOps Setup
1. Create new pipeline in Azure DevOps
2. Connect to repository
3. Use existing `azure-pipelines.yml`

### 2. Service Connections
Create service connections in Azure DevOps:
- **Azure Resource Manager**: For deployment
- **Docker Registry**: For container images (if applicable)

### 3. Variable Groups
Create variable group `{pipeline-name}-variables`:
- `AZURE_SUBSCRIPTION_ID`: {subscription-id}
- `RESOURCE_GROUP_DEV`: {dev-rg}
- `RESOURCE_GROUP_PROD`: {prod-rg}
- Add secrets: Database passwords, API keys

### 4. Environments
Create environments in Azure DevOps:
- `development`: Auto-deploy
- `staging`: Approval required
- `production`: Approval + manual validation

### 5. Branch Policies
Configure branch protection on `main`:
- Require pull request
- Require build validation
- Require 1+ code review

## Infrastructure Deployment
Infrastructure templates: `infrastructure/bicep/`
- `main.bicep`: Main template
- `parameters.{env}.json`: Per-environment parameters

Deploy infrastructure:
```bash
az deployment group create \
  --resource-group {rg} \
  --template-file infrastructure/bicep/main.bicep \
  --parameters infrastructure/bicep/parameters.dev.json
```

## Monitoring & Alerts
- Pipeline run history: Azure DevOps > Pipelines
- Application logs: Azure Portal > App Service/Function logs
- Application Insights: Configured for {target}

## Next Steps
- Run initial pipeline: Commit and push `azure-pipelines.yml`
- Monitor first run and adjust as needed
- Set up notifications (email, Slack)
- Use `/test` to validate deployment
```

**Memory Updates** (via MemoryStore):
1. `memoryStore.append("commands", project, "command_history.md", entry)`
2. `memoryStore.update("commands", project, "azure_config.md", content)`:
   - Pipeline configuration, environments, deployment targets
3. `memoryStore.update("skills", project, "generate-azure-pipelines", pipelinePatterns)` — update skill memory with pipeline patterns

## Tool Coordination
- **Read**: Existing configuration files, Azure resources
- **Grep/Glob**: Find existing pipelines, infrastructure code
- **Write**: Pipeline YAML, Bicep templates, documentation
- **Bash**: Azure CLI commands for setup and validation
- **Skills**: generate-azure-pipelines, generate-azure-bicep

## Key Patterns
- **Infrastructure as Code**: Bicep templates for reproducible deployments
- **Multi-Stage**: Separate build, test, and deployment stages
- **Environment Gates**: Approvals for production deployments
- **Security First**: Secrets in variable groups, security scanning

## Boundaries

**Will:**
- Generate complete Azure DevOps pipeline YAML configurations
- Create multi-stage pipelines with environment gates
- Generate infrastructure as code (Bicep) for Azure resources
- Provide setup instructions for service connections and variables
- Delegate to specialized skills for pipeline and infrastructure generation

**Will Not:**
- Create Azure resources directly (provides templates and instructions)
- Store secrets in pipeline files (uses variable groups)
- Replace manual testing and validation
- Configure Azure DevOps project (provides setup steps)

**Output**: Pipeline documentation saved to `/claudedocs/azure-pipeline_{name}_{date}.md`

**Next Step**: Use `/test` to validate pipeline, or `/deploy` to trigger deployment.
