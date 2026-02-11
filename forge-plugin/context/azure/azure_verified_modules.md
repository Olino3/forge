---
id: "azure/azure_verified_modules"
domain: azure
title: "Azure Verified Modules (AVM)"
type: reference
estimatedTokens: 1700
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Purpose"
    estimatedTokens: 15
    keywords: [purpose]
  - name: "What are Azure Verified Modules?"
    estimatedTokens: 21
    keywords: [azure, verified, modules]
  - name: "Key Benefits"
    estimatedTokens: 47
    keywords: [benefits]
  - name: "Module Types"
    estimatedTokens: 23
    keywords: [module, types]
  - name: "Using AVM Modules"
    estimatedTokens: 93
    keywords: [avm, modules]
  - name: "Module Parameters"
    estimatedTokens: 80
    keywords: [module, parameters]
  - name: "Finding Module Documentation"
    estimatedTokens: 27
    keywords: [finding, module, documentation]
  - name: "Standard Module Structure"
    estimatedTokens: 60
    keywords: [standard, module, structure]
  - name: "AVM Best Practices"
    estimatedTokens: 102
    keywords: [avm]
  - name: "Integration with bicepparams"
    estimatedTokens: 59
    keywords: [integration, bicepparams]
  - name: "Common Patterns"
    estimatedTokens: 55
    keywords: [patterns]
  - name: "Module Versioning"
    estimatedTokens: 34
    keywords: [module, versioning]
  - name: "Finding the Right Module"
    estimatedTokens: 33
    keywords: [finding, right, module]
  - name: "Troubleshooting"
    estimatedTokens: 33
    keywords: [troubleshooting]
  - name: "Official Resources"
    estimatedTokens: 20
    keywords: [official, resources]
tags: [azure, bicep, avm, modules, registry, infrastructure]
---

# Azure Verified Modules (AVM)

## Purpose

This context file provides guidance on using Azure Verified Modules (AVM) - Microsoft's official, standardized Bicep modules for deploying Azure resources.

## What are Azure Verified Modules?

Azure Verified Modules (AVM) are pre-built, tested, and maintained Bicep modules that follow Microsoft's best practices. They provide consistent, production-ready infrastructure as code.

**Official Repository**: https://github.com/Azure/bicep-registry-modules
**Official Documentation**: https://azure.github.io/Azure-Verified-Modules/

## Key Benefits

| Benefit | Description |
|---------|-------------|
| **Pre-tested** | Modules are validated and tested by Microsoft |
| **Best Practices** | Follow Azure Well-Architected Framework principles |
| **Consistent** | Standardized parameter names and module structure |
| **Maintained** | Regular updates for new Azure features |
| **Production-Ready** | Suitable for enterprise deployments |
| **Versioned** | Semantic versioning for stability |

## Module Types

### Resource Modules
Single Azure resource with best-practice configurations.

**Example**: Storage Account, Key Vault, Function App

### Pattern Modules
Multiple resources configured to work together.

**Example**: Hub-Spoke networking, Application Landing Zone

## Using AVM Modules

### Module Reference Syntax

```bicep
module storageAccount 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storageDeployment'
  params: {
    name: 'mystorageaccount'
    location: 'eastus'
    skuName: 'Standard_LRS'
  }
}
```

**Format**: `br/public:avm/{module-type}/{resource-provider}/{resource-type}:{version}`

### Common AVM Modules

| Module | Registry Path | Use For |
|--------|---------------|---------|
| Storage Account | `avm/res/storage/storage-account` | Blob, Queue, Table storage |
| Key Vault | `avm/res/key-vault/vault` | Secrets management |
| Function App | `avm/res/web/site` | Azure Functions hosting |
| App Service | `avm/res/web/site` | Web app hosting |
| Virtual Network | `avm/res/network/virtual-network` | Networking |
| SQL Database | `avm/res/sql/server` | Relational database |
| Cosmos DB | `avm/res/document-db/database-account` | NoSQL database |
| Container Registry | `avm/res/container-registry/registry` | Container images |
| Log Analytics | `avm/res/operational-insights/workspace` | Monitoring and logs |

## Module Parameters

### Required Parameters

All AVM modules have standard required parameters:

```bicep
module resource 'br/public:avm/res/...' = {
  params: {
    name: 'resourceName'        // Resource name
    location: 'eastus'          // Azure region (or use resourceGroup().location)
  }
}
```

### Optional Parameters

AVM modules provide extensive optional parameters:

```bicep
module storageAccount 'br/public:avm/res/storage/storage-account:0.9.0' = {
  params: {
    name: 'mystorageaccount'
    location: 'eastus'
    skuName: 'Standard_GRS'
    kind: 'StorageV2'

    // Tags
    tags: {
      environment: 'production'
      project: 'myapp'
    }

    // Managed Identity
    managedIdentities: {
      systemAssigned: true
    }

    // Networking
    publicNetworkAccess: 'Disabled'
    networkAcls: {
      defaultAction: 'Deny'
      virtualNetworkRules: []
    }

    // Diagnostic Settings
    diagnosticSettings: [
      {
        workspaceResourceId: '/subscriptions/.../log-analytics-workspace'
        logCategoriesAndGroups: [
          {
            categoryGroup: 'allLogs'
          }
        ]
      }
    ]
  }
}
```

## Finding Module Documentation

### Registry Browser
Browse modules at: https://aka.ms/avm

### Module Documentation
Each module has comprehensive docs:
- Parameter descriptions
- Output values
- Usage examples
- Best practices

### CLI Command
```bash
az bicep list-versions --module-path "br/public:avm/res/storage/storage-account"
```

## Standard Module Structure

All AVM modules follow this pattern:

```bicep
// Required parameters
@description('Name of the resource')
param name string

@description('Location for the resource')
param location string = resourceGroup().location

// Optional parameters with defaults
@description('Resource tags')
param tags object = {}

@description('Enable diagnostic logs')
param diagnosticSettings array = []

// Module implementation
resource myResource '...' = {
  name: name
  location: location
  tags: tags
  // ...
}

// Standard outputs
@description('Resource ID')
output resourceId string = myResource.id

@description('Resource name')
output name string = myResource.name
```

## AVM Best Practices

### 1. Use Latest Stable Versions
```bicep
// Good - Pinned to stable version
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  // ...
}

// Avoid - Using latest tag
module storage 'br/public:avm/res/storage/storage-account:latest' = {
  // ...
}
```

### 2. Leverage Module Outputs
```bicep
module storageAccount 'br/public:avm/res/storage/storage-account:0.9.0' = {
  // ...
}

module functionApp 'br/public:avm/res/web/site:0.3.0' = {
  params: {
    name: 'myfunctionapp'
    storageAccountResourceId: storageAccount.outputs.resourceId
  }
}
```

### 3. Use Diagnostic Settings
```bicep
module logAnalytics 'br/public:avm/res/operational-insights/workspace:0.3.0' = {
  params: {
    name: 'myloganalytics'
    location: location
  }
}

module storageAccount 'br/public:avm/res/storage/storage-account:0.9.0' = {
  params: {
    name: 'mystorageaccount'
    location: location
    diagnosticSettings: [
      {
        workspaceResourceId: logAnalytics.outputs.resourceId
      }
    ]
  }
}
```

### 4. Apply Tags Consistently
```bicep
var commonTags = {
  environment: environment
  project: projectName
  managedBy: 'bicep-avm'
}

module storageAccount 'br/public:avm/res/storage/storage-account:0.9.0' = {
  params: {
    name: 'mystorageaccount'
    tags: commonTags
  }
}
```

## Integration with bicepparams

AVM modules work seamlessly with .bicepparams files:

**main.bicep**:
```bicep
module storageAccount 'br/public:avm/res/storage/storage-account:0.9.0' = {
  params: {
    name: storageAccountName
    location: location
    skuName: storageAccountSku
    tags: tags
  }
}
```

**main.development.bicepparams**:
```bicep
using './main.bicep'

param storageAccountName = 'devstorageacct'
param location = 'eastus'
param storageAccountSku = 'Standard_LRS'
param tags = {
  environment: 'development'
  costCenter: 'dev-ops'
}
```

**main.production.bicepparams**:
```bicep
using './main.bicep'

param storageAccountName = 'prodstorageacct'
param location = 'eastus2'
param storageAccountSku = 'Standard_GRS'
param tags = {
  environment: 'production'
  costCenter: 'operations'
}
```

## Common Patterns

### Hub-Spoke Networking with AVM
```bicep
module hubVNet 'br/public:avm/res/network/virtual-network:0.1.0' = {
  params: {
    name: 'hub-vnet'
    addressPrefixes: ['10.0.0.0/16']
  }
}

module spokeVNet 'br/public:avm/res/network/virtual-network:0.1.0' = {
  params: {
    name: 'spoke-vnet'
    addressPrefixes: ['10.1.0.0/16']
    peerings: [
      {
        remotePeeringEnabled: true
        remoteVirtualNetworkId: hubVNet.outputs.resourceId
      }
    ]
  }
}
```

### Secure Storage with Private Endpoints
```bicep
module storageAccount 'br/public:avm/res/storage/storage-account:0.9.0' = {
  params: {
    name: 'securestorage'
    publicNetworkAccess: 'Disabled'
    privateEndpoints: [
      {
        privateDnsZoneResourceIds: [privateDnsZone.outputs.resourceId]
        subnetResourceId: subnet.outputs.resourceId
        service: 'blob'
      }
    ]
  }
}
```

## Module Versioning

AVM uses semantic versioning (SemVer):

- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.0.1): Bug fixes

**Recommendation**: Pin to minor version for stability:
```bicep
// Pin to 0.9.x (receive patch updates, no breaking changes)
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {}
```

## Finding the Right Module

### By Resource Type
1. Identify Azure resource type (e.g., "Storage Account")
2. Look up resource provider: `Microsoft.Storage`
3. Module path: `avm/res/storage/storage-account`

### By Use Case
1. Check AVM patterns: https://aka.ms/avm/patterns
2. Use pattern modules for common scenarios
3. Combine resource modules as needed

## Troubleshooting

### Module Not Found
```bash
# Check module exists
az bicep list-versions --module-path "br/public:avm/res/storage/storage-account"

# Update Bicep CLI
az bicep upgrade
```

### Version Conflicts
- Always pin to specific versions
- Test version updates in non-production first
- Review module changelog before upgrading

## Official Resources

- [AVM Repository](https://github.com/Azure/bicep-registry-modules)
- [AVM Documentation](https://azure.github.io/Azure-Verified-Modules/)
- [Module Registry](https://aka.ms/avm)
- [Bicep Registry](https://github.com/Azure/bicep-registry-modules)
