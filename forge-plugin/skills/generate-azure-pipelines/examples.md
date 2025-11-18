# generate-azure-pipelines: Usage Examples

## Example 1: Python Function App with Separate CI/CD

**Scenario**: Python Azure Function with separate build and deployment pipelines

**User Responses**:
- Pipeline architecture: Separate CI and CD
- Runtime: Python 3.11
- Build tool: Poetry
- Deployment target: Azure Functions
- Environments: Development, Production
- Infrastructure: Storage Account, Function App, Application Insights

**Generated Structure**:
```
.azure/
├── ci-pipeline.yml                    # Build + test
├── cd-pipeline.yml                    # Deploy to envs
├── iac-pipeline.yml                   # Deploy infrastructure
├── bicep/
│   ├── main.bicep                     # Function App + Storage + AppInsights
│   ├── main.development.bicepparams
│   ├── main.production.bicepparams
│   └── modules/
│       ├── storage-account.bicep
│       ├── function-app.bicep
│       └── app-insights.bicep
└── pipelines/
    ├── templates/
    │   ├── build-job.yml
    │   └── deploy-job.yml
    └── variables/
        ├── dev-variables.yml
        └── prod-variables.yml
```

**Key CI Pipeline Stages**: Build → Test → Publish Artifacts
**Key CD Pipeline Stages**: DeployDev → DeployProd (with approval)
**Key IAC Pipeline Stages**: Validate → DeployDev → DeployProd

---

## Example 2: Node.js Web App with Combined CI/CD

**Scenario**: Node.js React app with single pipeline

**User Responses**:
- Pipeline architecture: Combined CI/CD
- Runtime: Node.js 20
- Build tool: npm
- Deployment target: Azure App Service
- Environments: Development, Staging, Production
- Infrastructure: App Service Plan, App Service

**Generated Structure**:
```
.azure/
├── combined-cicd-pipeline.yml         # Build + test + deploy
├── iac-pipeline.yml
├── bicep/
│   ├── main.bicep
│   ├── main.development.bicepparams
│   ├── main.staging.bicepparams
│   ├── main.production.bicepparams
│   └── modules/
│       ├── app-service-plan.bicep
│       └── app-service.bicep
└── docs/
    └── README.md
```

**Combined Pipeline Flow**: Build → Test → DeployDev → DeployStaging → DeployProd

---

## Example 3: .NET Microservices with Infrastructure

**Scenario**: .NET 8 microservices requiring extensive Azure infrastructure

**User Responses**:
- Pipeline architecture: Separate CI and CD
- Runtime: .NET 8.0
- Build tool: dotnet CLI
- Deployment target: Azure Container Instances
- Environments: Development, Production
- Infrastructure: Storage, SQL Database, Key Vault, Container Registry, Virtual Network

**Generated Structure**:
```
.azure/
├── ci-pipeline.yml
├── cd-pipeline.yml
├── iac-pipeline.yml
├── bicep/
│   ├── main.bicep
│   ├── main.development.bicepparams
│   ├── main.production.bicepparams
│   └── modules/
│       ├── storage-account.bicep
│       ├── sql-server.bicep
│       ├── key-vault.bicep
│       ├── container-registry.bicep
│       └── networking.bicep
└── pipelines/
    ├── templates/
    │   ├── build-job.yml              # Docker build + push
    │   └── deploy-job.yml             # Container deployment
    └── variables/
        ├── dev-variables.yml
        └── prod-variables.yml
```

**Infrastructure First**: Run IAC pipeline before first deployment

---

## Example 4: Adding Pipelines to Existing Project

**Scenario**: Existing Python project needs pipelines, infrastructure already deployed

**User Responses**:
- Pipeline architecture: Separate CI and CD
- Runtime: Python 3.10
- Build tool: pip
- Deployment target: Azure Functions
- Environments: Staging, Production
- Infrastructure: Reference existing resources (no new IaC)

**Generated Structure**:
```
.azure/
├── ci-pipeline.yml                    # Build + test only
├── cd-pipeline.yml                    # Deploy to existing Functions
├── pipelines/
│   ├── templates/
│   │   ├── build-job.yml
│   │   └── deploy-job.yml
│   └── variables/
│       ├── staging-variables.yml      # References existing resources
│       └── prod-variables.yml
└── docs/
    └── README.md
```

**Note**: No `bicep/` directory generated, CD pipeline references existing resource names

---

## Example 5: Infrastructure-Only Pipeline

**Scenario**: Managing Azure infrastructure with Bicep, no application deployment

**User Responses**:
- Pipeline architecture: N/A (infrastructure only)
- Infrastructure: Storage Account, Function App, App Service Plan, Key Vault, Application Insights
- Environments: Development, Staging, Production

**Generated Structure**:
```
.azure/
├── iac-pipeline.yml                   # Only pipeline needed
├── bicep/
│   ├── main.bicep
│   ├── main.development.bicepparams
│   ├── main.staging.bicepparams
│   ├── main.production.bicepparams
│   └── modules/
│       ├── storage-account.bicep
│       ├── function-app.bicep
│       ├── app-service-plan.bicep
│       ├── key-vault.bicep
│       └── app-insights.bicep
└── docs/
    └── infrastructure-guide.md
```

**Use Case**: Infrastructure team manages Azure resources separately from application team

---

## Example 6: Multi-Runtime Monorepo

**Scenario**: Monorepo with Python API and Node.js frontend

**User Responses**:
- Pipeline architecture: Separate CI and CD per application
- Runtimes: Python 3.11 (API), Node.js 20 (Frontend)
- Deployment targets: Azure Functions (API), Azure Static Web Apps (Frontend)
- Environments: Development, Production

**Generated Structure**:
```
.azure/
├── api-ci-pipeline.yml                # Python API build
├── api-cd-pipeline.yml                # API deployment
├── frontend-ci-pipeline.yml           # Node.js build
├── frontend-cd-pipeline.yml           # Frontend deployment
├── iac-pipeline.yml                   # All infrastructure
├── bicep/
│   ├── main.bicep                     # Combined infrastructure
│   ├── main.development.bicepparams
│   ├── main.production.bicepparams
│   └── modules/
│       ├── function-app.bicep         # For API
│       └── static-web-app.bicep       # For frontend
└── pipelines/
    └── templates/
        ├── python-build-job.yml
        ├── nodejs-build-job.yml
        ├── function-deploy-job.yml
        └── static-web-deploy-job.yml
```

**Path Filters**: Each pipeline triggered by changes to specific directories

---

## Common Customizations

### Adding New Environment

1. Create `.azure/bicep/main.{environment}.bicepparams`
2. Create `.azure/pipelines/variables/{environment}-variables.yml`
3. Add deployment stage to CD pipeline
4. Create environment in Azure DevOps with approval gates

### Adding New Azure Resource

1. Create module in `.azure/bicep/modules/{resource}.bicep`
2. Reference module in `.azure/bicep/main.bicep`
3. Add resource parameters to all `.bicepparams` files
4. Update IAC pipeline if needed

### Adding Custom Build Steps

1. Edit `.azure/pipelines/templates/build-job.yml`
2. Add custom steps (linting, security scanning, etc.)
3. All pipelines using template automatically get new steps

### Changing Deployment Strategy

1. Edit `.azure/pipelines/templates/deploy-job.yml`
2. Change from `runOnce` to `canary`, `rolling`, or `blueGreen`
3. Update deployment configuration per strategy requirements

---

## Related Documentation

- [Azure Pipelines YAML Schema](https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/)
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Deployment Strategies](https://learn.microsoft.com/azure/devops/pipelines/process/deployment-jobs)
- [Pipeline Templates](https://learn.microsoft.com/azure/devops/pipelines/process/templates)
