---
id: "azure/azure_bicep_overview"
domain: azure
title: "Azure Bicep Overview"
type: reference
estimatedTokens: 2350
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Purpose"
    estimatedTokens: 13
    keywords: [purpose]
  - name: "What is Bicep?"
    estimatedTokens: 24
    keywords: [bicep]
  - name: "Why Bicep?"
    estimatedTokens: 52
    keywords: [bicep]
  - name: "Basic Bicep Syntax"
    estimatedTokens: 88
    keywords: [basic, bicep, syntax]
  - name: "Bicep File Structure"
    estimatedTokens: 204
    keywords: [bicep, file, structure]
  - name: "Bicep Parameters Files"
    estimatedTokens: 24
    keywords: [bicep, parameters, files]
  - name: "Common Bicep Patterns"
    estimatedTokens: 111
    keywords: [bicep, patterns]
  - name: "Bicep Project Structure"
    estimatedTokens: 70
    keywords: [bicep, project, structure]
  - name: "Bicep CLI Commands"
    estimatedTokens: 70
    keywords: [bicep, cli, commands]
  - name: "Bicep Decorators"
    estimatedTokens: 30
    keywords: [bicep, decorators]
  - name: "Best Practices"
    estimatedTokens: 72
    keywords: [best]
  - name: "Common Resource Types"
    estimatedTokens: 60
    keywords: [resource, types]
  - name: "Bicep vs ARM JSON Example"
    estimatedTokens: 66
    keywords: [bicep, arm, json, example]
  - name: "Detection Patterns"
    estimatedTokens: 48
    keywords: [detection, patterns]
  - name: "Official Resources"
    estimatedTokens: 13
    keywords: [official, resources]
tags: [azure, bicep, iac, arm, modules, parameters, deployment]
---

# Azure Bicep Overview

## Purpose

This context file provides an overview of Azure Bicep, Microsoft's domain-specific language (DSL) for deploying Azure resources declaratively.

## What is Bicep?

Bicep is a declarative language for describing and deploying Azure resources. It's a transparent abstraction over ARM (Azure Resource Manager) templates, providing simpler syntax while maintaining all ARM capabilities.

**Official Documentation**: https://learn.microsoft.com/azure/azure-resource-manager/bicep/

## Why Bicep?

| Feature | Bicep | ARM JSON |
|---------|-------|----------|
| Syntax | Simplified, readable | Verbose JSON |
| Type safety | Strong typing | Limited validation |
| Modularity | Native modules | Linked templates |
| Tooling | VS Code extension, linting | Basic JSON support |
| Learning curve | Easy for Azure users | Steeper |
| ARM compatibility | Compiles to ARM | Native |

## Basic Bicep Syntax

### Resource Declaration

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'mystorageacct'
  location: 'eastus'
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}
```

**Key Parts**:
- `resource` keyword
- Symbolic name (storageAccount)
- Resource type and API version
- Properties object

### Parameters

```bicep
@description('The name of the storage account')
@minLength(3)
@maxLength(24)
param storageAccountName string

@description('The location for resources')
param location string = resourceGroup().location

@description('The environment name')
@allowed([
  'dev'
  'staging'
  'prod'
])
param environment string = 'dev'
```

### Variables

```bicep
var storageAccountName = 'st${uniqueString(resourceGroup().id)}'
var tags = {
  environment: environment
  managedBy: 'bicep'
}
```

### Outputs

```bicep
output storageAccountId string = storageAccount.id
output storageAccountName string = storageAccount.name
output primaryEndpoints object = storageAccount.properties.primaryEndpoints
```

## Bicep File Structure

### Main Bicep File (main.bicep)

```bicep
targetScope = 'subscription'  // or 'resourceGroup', 'managementGroup', 'tenant'

// Parameters
@description('The environment name')
param environment string

@description('The Azure region for resources')
param location string = 'eastus'

// Variables
var resourceGroupName = 'myapp-${environment}-rg'
var tags = {
  environment: environment
  project: 'myapp'
  managedBy: 'bicep'
}

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

// Deploy resources to resource group using module
module appResources './modules/app-resources.bicep' = {
  name: 'appResources'
  scope: rg
  params: {
    location: location
    environment: environment
    tags: tags
  }
}

// Outputs
output resourceGroupName string = rg.name
output resourceGroupId string = rg.id
```

### Module File (modules/app-resources.bicep)

```bicep
@description('The Azure region for resources')
param location string

@description('The environment name')
param environment string

@description('Resource tags')
param tags object

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  sku: {
    name: environment == 'prod' ? 'Standard_GRS' : 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'plan-${environment}'
  location: location
  tags: tags
  sku: {
    name: environment == 'prod' ? 'P1v2' : 'B1'
    tier: environment == 'prod' ? 'PremiumV2' : 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// Function App
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'func-${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
      ]
    }
  }
}

// Outputs
output storageAccountName string = storageAccount.name
output functionAppName string = functionApp.name
output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
```

## Bicep Parameters Files

### Development Environment (.bicepparams)

```bicep
using './main.bicep'

param environment = 'development'
param location = 'eastus'
```

### Production Environment (.bicepparams)

```bicep
using './main.bicep'

param environment = 'production'
param location = 'eastus2'
```

## Common Bicep Patterns

### Conditional Resources

```bicep
resource publicIp 'Microsoft.Network/publicIPAddresses@2023-04-01' = if (createPublicIp) {
  name: 'myPublicIp'
  location: location
  properties: {
    publicIPAllocationMethod: 'Dynamic'
  }
}
```

### Loops

```bicep
@description('Array of storage account names')
param storageAccountNames array = [
  'storage1'
  'storage2'
  'storage3'
]

resource storageAccounts 'Microsoft.Storage/storageAccounts@2023-01-01' = [for name in storageAccountNames: {
  name: name
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}]
```

### Referencing Existing Resources

```bicep
// Reference existing resource in same scope
resource existingVnet 'Microsoft.Network/virtualNetworks@2023-04-01' existing = {
  name: 'my-existing-vnet'
}

// Reference existing resource in different resource group
resource existingStorage 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: 'existingstorage'
  scope: resourceGroup('otherResourceGroup')
}
```

### Dependency Management

```bicep
// Implicit dependency (referencing resource)
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'myFunctionApp'
  properties: {
    serverFarmId: appServicePlan.id  // Implicit dependency
  }
}

// Explicit dependency
resource deployment 'Microsoft.Resources/deployments@2022-09-01' = {
  name: 'deployment'
  dependsOn: [
    storageAccount
    appServicePlan
  ]
  properties: {
    // ...
  }
}
```

## Bicep Project Structure

### Recommended Directory Layout

```
.azure/
├── bicep/
│   ├── main.bicep                       # Main entry point
│   ├── main.development.bicepparams     # Dev parameters
│   ├── main.staging.bicepparams         # Staging parameters
│   ├── main.production.bicepparams      # Prod parameters
│   └── modules/                         # Reusable modules
│       ├── storage-account.bicep        # Storage module
│       ├── function-app.bicep           # Function App module
│       ├── app-service.bicep            # App Service module
│       ├── key-vault.bicep              # Key Vault module
│       └── networking.bicep             # Networking module
├── docs/                                # Documentation
│   └── infrastructure.md                # Infrastructure docs
└── pipelines/                           # Pipeline files
    └── iac-pipeline.yml                 # IAC deployment pipeline
```

## Bicep CLI Commands

### Build (compile to ARM)

```bash
az bicep build --file main.bicep
```

### Validate Deployment

```bash
az deployment sub validate \
  --location eastus \
  --template-file main.bicep \
  --parameters main.development.bicepparams
```

### Deploy to Subscription Scope

```bash
az deployment sub create \
  --location eastus \
  --template-file main.bicep \
  --parameters main.production.bicepparams \
  --name "deployment-$(date +%Y%m%d-%H%M%S)"
```

### Deploy to Resource Group Scope

```bash
az deployment group create \
  --resource-group myResourceGroup \
  --template-file main.bicep \
  --parameters main.development.bicepparams
```

### What-If (preview changes)

```bash
az deployment sub what-if \
  --location eastus \
  --template-file main.bicep \
  --parameters main.production.bicepparams
```

## Bicep Decorators

### Parameter Decorators

```bicep
@description('Description text')
@minLength(3)
@maxLength(24)
@allowed(['value1', 'value2'])
@secure()  // For passwords, secrets
param parameterName string
```

### Resource Decorators

```bicep
@description('Description of the resource')
@batchSize(5)  // For loop deployments
resource myResource 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  // ...
}
```

## Best Practices

1. **Use modules** - Break down into reusable components
2. **Use parameters files** - Environment-specific configurations
3. **Use descriptive names** - Clear symbolic names for resources
4. **Add descriptions** - Document parameters and resources
5. **Use variables for computed values** - Keep parameters simple
6. **Target appropriate scope** - Subscription, resource group, etc.
7. **Use existing resource references** - Don't recreate what exists
8. **Validate before deploying** - Use `az deployment validate` and `what-if`
9. **Version your API versions** - Use recent, stable API versions
10. **Use conditions sparingly** - Prefer separate modules for optional resources

## Common Resource Types

| Resource Type | Purpose | Module Example |
|---------------|---------|----------------|
| `Microsoft.Storage/storageAccounts` | Blob, Queue, Table storage | `modules/storage-account.bicep` |
| `Microsoft.Web/serverfarms` | App Service Plan | `modules/app-service-plan.bicep` |
| `Microsoft.Web/sites` | App Service, Function App | `modules/function-app.bicep` |
| `Microsoft.KeyVault/vaults` | Key Vault for secrets | `modules/key-vault.bicep` |
| `Microsoft.Sql/servers` | SQL Server | `modules/sql-server.bicep` |
| `Microsoft.Network/virtualNetworks` | Virtual Network | `modules/networking.bicep` |
| `Microsoft.ContainerRegistry/registries` | Container Registry | `modules/container-registry.bicep` |
| `Microsoft.Insights/components` | Application Insights | `modules/app-insights.bicep` |

## Bicep vs ARM JSON Example

### ARM JSON

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "storageAccountName": {
      "type": "string",
      "minLength": 3,
      "maxLength": 24
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2023-01-01",
      "name": "[parameters('storageAccountName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2"
    }
  ]
}
```

### Bicep (equivalent)

```bicep
@minLength(3)
@maxLength(24)
param storageAccountName string

param location string = resourceGroup().location

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}
```

**Reduction**: ~50% fewer lines, much more readable!

## Detection Patterns

### Identify Bicep Project

Look for:
- `.bicep` files in `.azure/bicep/` directory
- `main.bicep` as entry point
- `.bicepparams` files for environment parameters
- `modules/` directory with reusable components

### Identify Scope

Check `targetScope` in main.bicep:
- `subscription` - Deploys resource groups and subscription-level resources
- `resourceGroup` - Deploys resources to existing resource group
- `managementGroup` - Management group resources
- `tenant` - Tenant-level resources

## Official Resources

- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Bicep GitHub Repository](https://github.com/Azure/bicep)
- [Bicep Playground](https://aka.ms/bicepdemo)
- [Azure Resource Reference](https://learn.microsoft.com/azure/templates/)
- [Bicep Best Practices](https://learn.microsoft.com/azure/azure-resource-manager/bicep/best-practices)
