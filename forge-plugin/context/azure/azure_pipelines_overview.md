---
id: "azure/azure_pipelines_overview"
domain: azure
title: "Azure Pipelines Overview"
type: reference
estimatedTokens: 2250
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Purpose"
    estimatedTokens: 15
    keywords: [purpose]
  - name: "What are Azure Pipelines?"
    estimatedTokens: 26
    keywords: [azure, pipelines]
  - name: "Pipeline Structure"
    estimatedTokens: 123
    keywords: [pipeline, structure]
  - name: "Pipeline Execution Flow"
    estimatedTokens: 240
    keywords: [pipeline, execution, flow]
  - name: "Triggers"
    estimatedTokens: 47
    keywords: [triggers]
  - name: "Variables"
    estimatedTokens: 48
    keywords: [variables]
  - name: "Conditions"
    estimatedTokens: 31
    keywords: [conditions]
  - name: "Templates"
    estimatedTokens: 49
    keywords: [templates]
  - name: "Environments and Approvals"
    estimatedTokens: 36
    keywords: [environments, approvals]
  - name: "Service Connections"
    estimatedTokens: 24
    keywords: [service, connections]
  - name: "Artifacts"
    estimatedTokens: 25
    keywords: [artifacts]
  - name: "Multi-Stage Pipeline Example"
    estimatedTokens: 93
    keywords: [multi-stage, pipeline, example]
  - name: "Best Practices"
    estimatedTokens: 60
    keywords: [best]
  - name: "Detection Patterns"
    estimatedTokens: 52
    keywords: [detection, patterns]
  - name: "When to Use"
    estimatedTokens: 39
    keywords: [when]
  - name: "Official Resources"
    estimatedTokens: 12
    keywords: [official, resources]
tags: [azure, pipelines, cicd, yaml, stages, jobs, triggers, templates]
---

# Azure Pipelines Overview

## Purpose

This context file provides a comprehensive overview of Azure Pipelines YAML syntax, structure, and core concepts for building CI/CD workflows.

## What are Azure Pipelines?

Azure Pipelines is a cloud service that automatically builds, tests, and deploys code projects. It supports continuous integration (CI) and continuous delivery (CD) to test, build, and ship code to any target.

**Official Documentation**: https://learn.microsoft.com/azure/devops/pipelines/

## Pipeline Structure

### Basic YAML Structure

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - script: echo "Building..."
            displayName: 'Build Step'
```

### Key Components

| Component | Purpose | Required | Notes |
|-----------|---------|----------|-------|
| `trigger` | Define when pipeline runs | No | Branch triggers, PR triggers, path filters |
| `pool` | Agent pool for running jobs | Yes | Self-hosted or Microsoft-hosted |
| `stages` | Logical grouping of jobs | No | Use for complex workflows (Build → Test → Deploy) |
| `jobs` | Collection of steps | Yes | Run in parallel by default |
| `steps` | Individual tasks/scripts | Yes | Executed sequentially within a job |
| `variables` | Define reusable values | No | Pipeline, stage, or job level |
| `parameters` | Runtime inputs | No | Template parameters |
| `resources` | External resources | No | Repositories, containers, pipelines |

## Pipeline Execution Flow

```
Trigger → Pool Assignment → Stages → Jobs → Steps
```

### Stages

Stages represent major phases of your pipeline (e.g., Build, Test, Deploy).

```yaml
stages:
  - stage: Build
    displayName: 'Build Application'
    jobs:
      - job: CompileBuild
        steps:
          - script: npm run build

  - stage: Test
    displayName: 'Run Tests'
    dependsOn: Build
    jobs:
      - job: UnitTests
        steps:
          - script: npm test

  - stage: Deploy
    displayName: 'Deploy to Production'
    dependsOn: Test
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployProd
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying..."
```

**Key Points**:
- Stages run sequentially by default
- Use `dependsOn` to control stage order
- Use `condition` to conditionally run stages
- Deployment jobs require `environment` for approval gates

### Jobs

Jobs run on an agent and contain steps.

```yaml
jobs:
  - job: BuildWeb
    displayName: 'Build Web Application'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
      - script: npm install
      - script: npm run build

  - job: BuildAPI
    displayName: 'Build API'
    pool:
      vmImage: 'windows-latest'
    steps:
      - script: dotnet build
```

**Job Types**:
- **job**: Standard job for build/test tasks
- **deployment**: Special job for deployments with environment tracking
- **template**: Reusable job template

### Steps

Steps are the smallest unit of work in a pipeline.

```yaml
steps:
  # Task step (predefined task from marketplace)
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'

  # Script step (inline shell command)
  - script: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
    displayName: 'Install dependencies'

  # Bash step (bash-specific)
  - bash: |
      echo "Running on $(uname -s)"
      ./run-tests.sh
    displayName: 'Run tests'

  # PowerShell step
  - pwsh: |
      Write-Host "PowerShell script"
      Get-ChildItem
    displayName: 'PowerShell step'

  # Checkout step (fetch repository)
  - checkout: self
    displayName: 'Checkout repository'
```

**Common Tasks**:
- `UsePythonVersion@0`, `UseNodeVersion@0`, `UseDotNet@2` - Setup runtime
- `Docker@2` - Build/push Docker images
- `AzureCLI@2` - Run Azure CLI commands
- `AzureResourceManagerTemplateDeployment@3` - Deploy ARM/Bicep templates
- `PublishBuildArtifacts@1` - Publish build outputs
- `DownloadBuildArtifacts@0` - Download artifacts from previous stages

## Triggers

### Branch Triggers

```yaml
trigger:
  branches:
    include:
      - main
      - releases/*
    exclude:
      - experimental/*
  paths:
    include:
      - src/*
    exclude:
      - docs/*
```

### Pull Request Triggers

```yaml
pr:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - README.md
```

### Scheduled Triggers

```yaml
schedules:
  - cron: "0 0 * * *"  # Midnight UTC daily
    displayName: Nightly build
    branches:
      include:
        - main
```

## Variables

### Pipeline Variables

```yaml
variables:
  buildConfiguration: 'Release'
  pythonVersion: '3.11'

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - script: echo "Building $(buildConfiguration)"
```

### Variable Groups (from Azure DevOps Library)

```yaml
variables:
  - group: production-secrets
  - name: customVariable
    value: 'myValue'
```

### Runtime Variables

```yaml
steps:
  - script: echo "##vso[task.setvariable variable=myVar]myValue"
    displayName: 'Set variable'

  - script: echo "Value is $(myVar)"
    displayName: 'Use variable'
```

## Conditions

Control when stages/jobs/steps run:

```yaml
# Run only on main branch
condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')

# Run only if previous stage succeeded
condition: succeeded()

# Run even if previous stage failed
condition: always()

# Complex condition
condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'), eq(variables['deployToProduction'], 'true'))
```

## Templates

### Template File (templates/build-template.yml)

```yaml
parameters:
  - name: buildConfiguration
    type: string
    default: 'Release'
  - name: projectPath
    type: string

steps:
  - script: dotnet restore ${{ parameters.projectPath }}
    displayName: 'Restore dependencies'

  - script: dotnet build ${{ parameters.projectPath }} --configuration ${{ parameters.buildConfiguration }}
    displayName: 'Build project'
```

### Using Template

```yaml
stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - template: templates/build-template.yml
            parameters:
              buildConfiguration: 'Release'
              projectPath: './src/MyApp.csproj'
```

## Environments and Approvals

```yaml
stages:
  - stage: DeployProduction
    jobs:
      - deployment: DeployProdJob
        environment: production  # Requires approval in Azure DevOps
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying to production"
```

**Environments** in Azure DevOps:
- Track deployment history
- Require manual approvals
- Define checks (e.g., run gates before deployment)

## Service Connections

For deploying to Azure, define service connections in Azure DevOps:

```yaml
steps:
  - task: AzureCLI@2
    inputs:
      azureSubscription: 'my-service-connection'  # Defined in project settings
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az group list
```

## Artifacts

### Publishing Artifacts

```yaml
steps:
  - task: PublishBuildArtifacts@1
    inputs:
      pathToPublish: '$(Build.ArtifactStagingDirectory)'
      artifactName: 'drop'
      publishLocation: 'Container'
```

### Downloading Artifacts

```yaml
steps:
  - task: DownloadBuildArtifacts@0
    inputs:
      buildType: 'current'
      downloadType: 'single'
      artifactName: 'drop'
      downloadPath: '$(System.ArtifactsDirectory)'
```

## Multi-Stage Pipeline Example

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'

stages:
  - stage: Build
    displayName: 'Build and Test'
    jobs:
      - job: BuildJob
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'

          - script: |
              pip install -r requirements.txt
              python -m pytest
            displayName: 'Install and test'

          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: '$(Build.SourcesDirectory)'
              artifactName: 'app'

  - stage: DeployDev
    displayName: 'Deploy to Development'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
    jobs:
      - deployment: DeployDevJob
        environment: development
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: app
                - script: echo "Deploy to dev"

  - stage: DeployProd
    displayName: 'Deploy to Production'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployProdJob
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: app
                - script: echo "Deploy to prod"
```

## Best Practices

1. **Use stages for major phases** - Separate Build, Test, Deploy
2. **Use templates for reusability** - Share common steps across pipelines
3. **Use variable groups for secrets** - Never hardcode credentials
4. **Use service connections** - Secure Azure authentication
5. **Use environments for tracking** - Deployment history and approvals
6. **Use conditions wisely** - Control when stages/jobs run
7. **Cache dependencies** - Speed up builds with caching tasks
8. **Use matrix jobs** - Test across multiple configurations in parallel

## Detection Patterns

### Identify CI Pipeline

Look for:
- Build tasks (compile, package)
- Test execution
- Artifact publishing
- No deployment steps

### Identify CD Pipeline

Look for:
- Artifact downloads
- Deployment jobs with `environment`
- Azure CLI/ARM deployment tasks
- Multiple stages for different environments

### Identify Combined CI/CD

Look for:
- Both build and deployment stages
- Conditional deployments based on branch
- Multiple environments (dev, staging, prod)

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Simple project | Combined CI/CD pipeline |
| Microservices | Separate CI/CD pipelines per service |
| Infrastructure changes | Separate IAC pipeline |
| Frequent deployments | Separate CD pipeline triggered by CI artifact |
| Multiple environments | Multi-stage pipeline with environment gates |

## Official Resources

- [Azure Pipelines Documentation](https://learn.microsoft.com/azure/devops/pipelines/)
- [YAML Schema Reference](https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/)
- [Pipeline Tasks](https://learn.microsoft.com/azure/devops/pipelines/tasks/)
- [Predefined Variables](https://learn.microsoft.com/azure/devops/pipelines/build/variables)
- [Expressions](https://learn.microsoft.com/azure/devops/pipelines/process/expressions)
