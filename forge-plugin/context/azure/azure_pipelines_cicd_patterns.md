# Azure Pipelines CI/CD Patterns

## Purpose

This context file provides patterns and best practices for structuring CI/CD pipelines in Azure DevOps, including when to use separate vs combined pipelines.

## CI/CD Pipeline Architectures

### 1. Combined CI/CD Pipeline

**When to use**:
- Small projects with simple deployment
- Single environment or few environments
- Infrequent deployments
- Single-tenant applications

**Pros**:
- Simpler to maintain
- Single source of truth
- Easier to understand flow

**Cons**:
- Rebuilds code for every deployment
- Harder to deploy specific versions
- Longer pipeline execution time

**Structure**:
```yaml
# ci-cd-pipeline.yml
trigger:
  branches:
    include:
      - main

stages:
  - stage: Build
    jobs:
      - job: BuildAndTest
        steps:
          - script: npm install
          - script: npm run build
          - script: npm test
          - task: PublishBuildArtifacts@1

  - stage: DeployDev
    dependsOn: Build
    jobs:
      - deployment: DeployDevJob
        environment: development
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                - script: deploy.sh dev

  - stage: DeployProd
    dependsOn: DeployDev
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    jobs:
      - deployment: DeployProdJob
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                - script: deploy.sh prod
```

### 2. Separate CI and CD Pipelines

**When to use**:
- Large projects with frequent deployments
- Need to deploy specific versions
- Multiple environments with different schedules
- Want to decouple build from deployment

**Pros**:
- Deploy any version without rebuilding
- Independent deployment cycles
- Faster deployment pipeline
- Better separation of concerns

**Cons**:
- More complex to set up
- Need artifact management strategy
- More pipelines to maintain

**CI Pipeline Structure** (ci-pipeline.yml):
```yaml
trigger:
  branches:
    include:
      - main
      - develop
      - feature/*

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'

stages:
  - stage: Build
    displayName: 'Build and Test'
    jobs:
      - job: BuildJob
        displayName: 'Build Application'
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
            displayName: 'Use Python 3.11'

          - script: |
              pip install -r requirements.txt
            displayName: 'Install dependencies'

          - script: |
              python -m pytest tests/
            displayName: 'Run unit tests'

          - script: |
              python setup.py sdist bdist_wheel
            displayName: 'Build package'

          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: '$(Build.SourcesDirectory)/dist'
              artifactName: 'python-package'
              publishLocation: 'Container'
            displayName: 'Publish artifacts'

          - task: PublishTestResults@2
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: '**/test-results.xml'
            condition: succeededOrFailed()
```

**CD Pipeline Structure** (cd-pipeline.yml):
```yaml
trigger: none  # Manual or triggered by CI completion

resources:
  pipelines:
    - pipeline: buildPipeline
      source: 'CI-Pipeline-Name'
      trigger:
        branches:
          include:
            - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: DeployDevelopment
    displayName: 'Deploy to Development'
    jobs:
      - deployment: DeployDev
        environment: development
        strategy:
          runOnce:
            deploy:
              steps:
                - download: buildPipeline
                  artifact: python-package

                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'dev-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az functionapp deployment source config-zip \
                        --resource-group myapp-dev-rg \
                        --name myapp-dev \
                        --src $(Pipeline.Workspace)/buildPipeline/python-package/app.zip

  - stage: DeployStaging
    displayName: 'Deploy to Staging'
    dependsOn: DeployDevelopment
    condition: succeeded()
    jobs:
      - deployment: DeployStaging
        environment: staging
        strategy:
          runOnce:
            deploy:
              steps:
                - download: buildPipeline
                  artifact: python-package

                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'staging-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az functionapp deployment source config-zip \
                        --resource-group myapp-staging-rg \
                        --name myapp-staging \
                        --src $(Pipeline.Workspace)/buildPipeline/python-package/app.zip

  - stage: DeployProduction
    displayName: 'Deploy to Production'
    dependsOn: DeployStaging
    condition: succeeded()
    jobs:
      - deployment: DeployProd
        environment: production  # Requires manual approval
        strategy:
          runOnce:
            deploy:
              steps:
                - download: buildPipeline
                  artifact: python-package

                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'prod-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az functionapp deployment source config-zip \
                        --resource-group myapp-prod-rg \
                        --name myapp-prod \
                        --src $(Pipeline.Workspace)/buildPipeline/python-package/app.zip
```

### 3. Infrastructure as Code (IAC) Pipeline

**When to use**:
- Infrastructure changes are separate from application changes
- Need to version infrastructure
- Want approval gates for infrastructure changes
- Using Bicep, ARM, or Terraform

**Structure** (iac-pipeline.yml):
```yaml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - .azure/bicep/**

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: infrastructure-variables

stages:
  - stage: ValidateBicep
    displayName: 'Validate Bicep Templates'
    jobs:
      - job: Validate
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'dev-service-connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az bicep build --file .azure/bicep/main.bicep
                az deployment sub validate \
                  --location eastus \
                  --template-file .azure/bicep/main.bicep \
                  --parameters .azure/bicep/main.development.bicepparams
            displayName: 'Validate Bicep syntax and deployment'

  - stage: DeployDevelopment
    displayName: 'Deploy Infrastructure to Development'
    dependsOn: ValidateBicep
    condition: succeeded()
    jobs:
      - deployment: DeployInfraDev
        environment: development-infrastructure
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self

                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'dev-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az deployment sub create \
                        --location eastus \
                        --template-file .azure/bicep/main.bicep \
                        --parameters .azure/bicep/main.development.bicepparams \
                        --name "infra-dev-$(Build.BuildId)"
                  displayName: 'Deploy Bicep to Development'

  - stage: DeployProduction
    displayName: 'Deploy Infrastructure to Production'
    dependsOn: DeployDevelopment
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployInfraProd
        environment: production-infrastructure
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self

                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'prod-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az deployment sub create \
                        --location eastus \
                        --template-file .azure/bicep/main.bicep \
                        --parameters .azure/bicep/main.production.bicepparams \
                        --name "infra-prod-$(Build.BuildId)"
                  displayName: 'Deploy Bicep to Production'
```

## Pipeline Organization Patterns

### Pattern 1: Monorepo with Path Filters

**Use case**: Multiple applications in one repository

```yaml
# api-ci-pipeline.yml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - api/**
      - shared/**

# web-ci-pipeline.yml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - web/**
      - shared/**
```

### Pattern 2: Template-Based Pipelines

**Use case**: Multiple similar pipelines with shared logic

**Main Pipeline**:
```yaml
# main-pipeline.yml
trigger:
  branches:
    include:
      - main

stages:
  - stage: Build
    jobs:
      - template: templates/build-job-template.yml
        parameters:
          projectPath: './src/MyApp'
          buildConfiguration: 'Release'

  - stage: Deploy
    dependsOn: Build
    jobs:
      - template: templates/deploy-job-template.yml
        parameters:
          environment: 'production'
          resourceGroup: 'myapp-prod-rg'
```

**Build Template** (templates/build-job-template.yml):
```yaml
parameters:
  - name: projectPath
    type: string
  - name: buildConfiguration
    type: string
    default: 'Release'

jobs:
  - job: BuildJob
    steps:
      - script: dotnet restore ${{ parameters.projectPath }}
        displayName: 'Restore NuGet packages'

      - script: dotnet build ${{ parameters.projectPath }} --configuration ${{ parameters.buildConfiguration }}
        displayName: 'Build project'

      - task: PublishBuildArtifacts@1
        inputs:
          pathToPublish: '${{ parameters.projectPath }}/bin/${{ parameters.buildConfiguration }}'
          artifactName: 'drop'
```

### Pattern 3: Multi-Environment with Variable Groups

**Use case**: Same pipeline, different configurations per environment

```yaml
stages:
  - stage: DeployDev
    variables:
      - group: dev-variables
      - name: environment
        value: 'development'
    jobs:
      - template: templates/deploy-template.yml
        parameters:
          environment: $(environment)

  - stage: DeployProd
    variables:
      - group: prod-variables
      - name: environment
        value: 'production'
    jobs:
      - template: templates/deploy-template.yml
        parameters:
          environment: $(environment)
```

## Common Pipeline Structures

### Python Application

```yaml
# CI Pipeline
stages:
  - stage: Build
    jobs:
      - job: BuildAndTest
        steps:
          - task: UsePythonVersion@0
          - script: pip install -r requirements.txt
          - script: pytest tests/
          - script: python setup.py sdist bdist_wheel
          - task: PublishBuildArtifacts@1
```

### Node.js Application

```yaml
# CI Pipeline
stages:
  - stage: Build
    jobs:
      - job: BuildAndTest
        steps:
          - task: UseNodeVersion@0
          - script: npm ci
          - script: npm run build
          - script: npm test
          - task: PublishBuildArtifacts@1
```

### .NET Application

```yaml
# CI Pipeline
stages:
  - stage: Build
    jobs:
      - job: BuildAndTest
        steps:
          - task: UseDotNet@2
          - script: dotnet restore
          - script: dotnet build --configuration Release
          - script: dotnet test
          - script: dotnet publish --configuration Release --output $(Build.ArtifactStagingDirectory)
          - task: PublishBuildArtifacts@1
```

### Docker Application

```yaml
# CI Pipeline
stages:
  - stage: Build
    jobs:
      - job: BuildAndPush
        steps:
          - task: Docker@2
            inputs:
              command: 'buildAndPush'
              repository: 'myapp'
              dockerfile: 'Dockerfile'
              containerRegistry: 'myContainerRegistry'
              tags: |
                $(Build.BuildId)
                latest
```

## Decision Matrix

| Requirement | Recommendation |
|-------------|----------------|
| Simple project, single environment | Combined CI/CD |
| Multiple environments, frequent deploys | Separate CI and CD |
| Infrastructure changes tracked separately | Separate IAC pipeline |
| Microservices architecture | Separate CI/CD per service + shared templates |
| Need to deploy specific versions | Separate CI and CD |
| Fast feedback on PRs | Separate CI (runs on all branches) |
| Complex approval workflows | Separate CD with environment gates |
| Monorepo with multiple apps | Multiple pipelines with path filters |

## Best Practices

1. **Separate concerns**: Build once, deploy many times
2. **Use templates**: Share common logic across pipelines
3. **Use variable groups**: Environment-specific configuration
4. **Use environments**: Track deployments and approvals
5. **Cache dependencies**: Speed up builds
6. **Use conditions**: Control when stages run
7. **Version artifacts**: Tag builds with semantic versions
8. **Run tests in CI**: Fail fast on code issues
9. **Use service connections**: Secure cloud credentials
10. **Monitor pipelines**: Set up alerts for failures

## Anti-Patterns to Avoid

1. ❌ Hardcoding credentials in YAML
2. ❌ Rebuilding for every environment
3. ❌ No approval gates for production
4. ❌ Single pipeline doing everything
5. ❌ No test stage
6. ❌ Deploying untested code
7. ❌ No rollback strategy
8. ❌ Ignoring pipeline failures

## Official Resources

- [Azure Pipelines Best Practices](https://learn.microsoft.com/azure/devops/pipelines/artifacts/artifacts-overview)
- [Multi-Stage Pipelines](https://learn.microsoft.com/azure/devops/pipelines/process/stages)
- [Deployment Jobs](https://learn.microsoft.com/azure/devops/pipelines/process/deployment-jobs)
- [Pipeline Templates](https://learn.microsoft.com/azure/devops/pipelines/process/templates)
