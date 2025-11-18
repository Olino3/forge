# generate-azure-bicep: Usage Examples

## Example 1: Simple Storage Account with AVM

**Scenario**: Single Storage Account for blob storage

**User Responses**:
- Resources: Storage Account
- Environments: Development, Production
- Naming: Standard Azure (`st-{env}-{region}`)
- Region: eastus (both environments)
- Scope: Resource Group
- Custom: Enable diagnostic logs

**Generated main.bicep**:
```bicep
targetScope = 'resourceGroup'

param environment string
param location string = resourceGroup().location

module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storage-deployment'
  params: {
    name: 'st${environment}${uniqueString(resourceGroup().id)}'
    location: location
    skuName: environment == 'production' ? 'Standard_GRS' : 'Standard_LRS'
  }
}
```

**main.development.bicepparams**:
```bicep
using './main.bicep'
param environment = 'development'
param location = 'eastus'
```

---

## Example 2: Function App with Dependencies

**Scenario**: Azure Function with Storage, App Insights, Key Vault

**User Responses**:
- Resources: Function App, Storage Account, Application Insights, Key Vault
- Environments: Development, Staging, Production
- Naming: Custom prefix `myapp-`
- Region: eastus (dev/staging), eastus2 (prod)
- Scope: Subscription (creates resource groups)

**Generated Structure**:
```
.azure/bicep/
├── main.bicep                      # Composes all AVM modules
├── main.development.bicepparams    # Dev: B1 plan, LRS storage
├── main.staging.bicepparams        # Staging: B1 plan, LRS storage
├── main.production.bicepparams     # Prod: P1v2 plan, GRS storage
└── docs/
    └── infrastructure.md           # Documentation
```

**Key Pattern**: AVM modules referenced with outputs passed between them:
```bicep
module storage 'br/public:avm/res/storage/storage-account:0.9.0' = { /*...*/ }
module appInsights 'br/public:avm/res/operational-insights/workspace:0.3.0' = { /*...*/ }
module functionApp 'br/public:avm/res/web/site:0.3.0' = {
  params: {
    storageAccountResourceId: storage.outputs.resourceId
    appInsightsInstrumentationKey: appInsights.outputs.instrumentationKey
  }
}
```

---

## Example 3: Secure Infrastructure with VNet Integration

**Scenario**: Storage and Function App with private endpoints and VNet

**User Responses**:
- Resources: Storage, Function App, Virtual Network, Private DNS Zones
- Environments: Production only
- Custom: Private endpoints, managed identity, VNet integration

**Generated main.bicep** highlights:
```bicep
module vnet 'br/public:avm/res/network/virtual-network:0.1.0' = {
  params: {
    name: 'vnet-prod'
    addressPrefixes: ['10.0.0.0/16']
    subnets: [
      { name: 'functions-subnet', addressPrefix: '10.0.1.0/24' }
      { name: 'pe-subnet', addressPrefix: '10.0.2.0/24' }
    ]
  }
}

module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  params: {
    name: 'stprod${uniqueString(resourceGroup().id)}'
    publicNetworkAccess: 'Disabled'
    privateEndpoints: [
      {
        subnetResourceId: vnet.outputs.subnetResourceIds[1]  // pe-subnet
        service: 'blob'
      }
    ]
  }
}
```

---

## Example 4: Multi-Region Deployment

**Scenario**: Application deployed to multiple regions for redundancy

**User Responses**:
- Resources: Storage, Function App (per region)
- Environments: Production
- Regions: Multiple (eastus, westus, northeurope)
- Custom: Traffic Manager for routing

**Pattern**: Loop over regions using Bicep arrays:
```bicep
param regions array = ['eastus', 'westus', 'northeurope']

module storageAccounts 'br/public:avm/res/storage/storage-account:0.9.0' = [for region in regions: {
  name: 'storage-${region}'
  params: {
    name: 'st${region}${uniqueString(resourceGroup().id)}'
    location: region
    skuName: 'Standard_GRS'
  }
}]
```

---

## Example 5: Existing Infrastructure with New Resources

**Scenario**: Add Application Insights to existing Function App setup

**User Responses**:
- Resources: Application Insights only
- Environments: All (development, staging, production)
- Custom: Reference existing Function App

**Pattern**: Reference existing resources, add new AVM module:
```bicep
resource existingFunctionApp 'Microsoft.Web/sites@2023-01-01' existing = {
  name: functionAppName
}

module appInsights 'br/public:avm/res/operational-insights/workspace:0.3.0' = {
  params: {
    name: 'appi-${environment}'
    location: location
  }
}

// Update function app settings (separate deployment or ARM)
```

---

## Example 6: Custom Wrapper Module

**Scenario**: Project needs specific Storage Account configuration used everywhere

**Generated Custom Wrapper** (`.azure/bicep/modules/project-storage.bicep`):
```bicep
// Wrapper for project-standard storage account using AVM

param name string
param location string
param environment string

module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  name: 'storage-${name}'
  params: {
    name: name
    location: location
    skuName: environment == 'production' ? 'Standard_GRS' : 'Standard_LRS'
    kind: 'StorageV2'

    // Project-specific defaults
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false

    // Standard project tags
    tags: {
      project: 'myapp'
      managedBy: 'bicep-avm'
      environment: environment
    }
  }
}

output resourceId string = storage.outputs.resourceId
output name string = storage.outputs.name
```

**Usage in main.bicep**:
```bicep
module rawStorage './modules/project-storage.bicep' = {
  params: {
    name: 'straw${uniqueString(resourceGroup().id)}'
    location: location
    environment: environment
  }
}
```

---

## Common Customizations

### Updating AVM Module Versions
```bash
# Check available versions
az bicep list-versions --module-path "br/public:avm/res/storage/storage-account"

# Update in main.bicep
module storage 'br/public:avm/res/storage/storage-account:0.10.0' = { /*...*/ }
```

### Adding New Environment
1. Create `main.uat.bicepparams` with UAT-specific parameters
2. Deploy: `az deployment group create --parameters main.uat.bicepparams`

### Changing Resource SKUs
Edit environment-specific .bicepparams files:
```bicep
// main.production.bicepparams
param storageSkuName = 'Standard_GZRS'  // Change from GRS to GZRS
```

### Adding Diagnostic Settings
```bicep
module logAnalytics 'br/public:avm/res/operational-insights/workspace:0.3.0' = { /*...*/ }

module storage 'br/public:avm/res/storage/storage-account:0.9.0' = {
  params: {
    diagnosticSettings: [
      {
        workspaceResourceId: logAnalytics.outputs.resourceId
        logCategoriesAndGroups: [{ categoryGroup: 'allLogs' }]
      }
    ]
  }
}
```

---

## Related Documentation

- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
- [AVM Module Registry](https://aka.ms/avm)
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure Resource Naming](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
