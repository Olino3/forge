# Skill: generate-azure-bicep

**Version**: 1.0.0
**Purpose**: Generate Azure Bicep infrastructure modules using Azure Verified Modules (AVM) and bicepparams
**Author**: The Forge
**Last Updated**: 2025-11-18

---

## Title

**Generate Azure Bicep** - Create production-ready Bicep infrastructure modules using Azure Verified Modules with environment-specific parameters

---

## File Structure

```
forge-plugin/skills/generate-azure-bicep/
├── SKILL.md                  # This file - mandatory workflow
├── examples.md               # Usage scenarios and examples
├── scripts/
│   └── bicep_generator.py    # Helper script for Bicep generation
└── templates/
    ├── main-bicep-avm-template.bicep          # Main Bicep using AVM
    ├── bicepparams-template.bicep             # Parameters file template
    ├── wrapper-module-template.bicep          # Custom wrapper for AVM module
    └── README-template.md                     # Documentation template
```

---

## Required Reading

**Before executing this skill**, read these files in order:

1. **Context indexes**:
   - `../../context/azure/index.md` - Azure context navigation

2. **Memory index**:
   - `../../memory/skills/generate-azure-bicep/index.md` - Memory structure for this skill

3. **Context files**:
   - `../../context/azure/azure_verified_modules.md` - AVM concepts, usage patterns, best practices
   - `../../context/azure/azure_bicep_overview.md` - Bicep syntax and structure

4. **Project memory** (if exists):
   - `../../memory/skills/generate-azure-bicep/{project-name}/` - Previous Bicep configurations

---

## Design Requirements

### Core Functionality

This skill must:
1. **Use Azure Verified Modules** as the foundation for all resource deployments
2. **Generate main.bicep** that composes AVM modules
3. **Create bicepparams files** for each environment (development, staging, production)
4. **Generate custom wrapper modules** when needed for project-specific requirements
5. **Create `.azure/bicep/` directory structure** with modules subdirectory
6. **Apply consistent naming and tagging** across all resources
7. **Store Bicep configuration** in memory for future updates

### Output Requirements

Generate a **complete `.azure/bicep/` directory** with:
- main.bicep using AVM module references
- Environment-specific .bicepparams files
- Custom wrapper modules (if needed)
- Documentation explaining module usage
- Consistent resource naming strategy

### Quality Requirements

Generated Bicep must:
- **Use latest stable AVM versions** from public registry
- **Follow Azure Well-Architected Framework** principles
- **Pin module versions** for reproducibility
- **Include diagnostic settings** where applicable
- **Apply tags consistently** across all resources
- **Be well-documented** with parameter descriptions

---

## Prompting Guidelines

### User Questions Framework

Use **Socratic method** to gather requirements. Ask questions in this order:

#### 1. Infrastructure Scope

**Question**: "What Azure resources does your application need?"

**Options** (can select multiple):
- Storage Account (Blob, Queue, Table)
- Function App / App Service
- Key Vault (secrets management)
- Application Insights (monitoring)
- SQL Database / Cosmos DB
- Virtual Network (VNet, subnets, NSG)
- Container Registry
- Service Bus / Event Hub
- Other resources

**Follow-up**: "This determines which AVM modules to use."

#### 2. Environments

**Question**: "Which environments do you need?"

**Options**:
- Development only
- Development + Production
- Development + Staging + Production
- Custom environments

**Follow-up**: "This creates environment-specific bicepparams files."

#### 3. Resource Naming Convention

**Question**: "What naming convention should we use for resources?"

**Options**:
- Standard Azure naming (`{resource-abbr}-{environment}-{region}`)
- Custom prefix (e.g., `myapp-{resource}-{environment}`)
- Project-specific pattern
- Use Azure naming tool recommendations

**Follow-up**: "This ensures consistent resource names across environments."

#### 4. Azure Region

**Question**: "Which Azure region(s) for deployments?"

**Options**:
- Single region for all environments
- Different regions per environment
- Multi-region deployment

**Follow-up**: "This sets location parameters in bicepparams files."

#### 5. Deployment Scope

**Question**: "What deployment scope do you need?"

**Options**:
- Resource Group (most common)
- Subscription (for creating resource groups)
- Management Group
- Tenant

**Follow-up**: "This sets the targetScope in main.bicep."

#### 6. Custom Requirements

**Question**: "Do you have any custom requirements?"

**Options**:
- Private endpoints for resources
- Managed identities
- VNet integration
- Custom RBAC roles
- Bring your own keys (BYOK)
- Compliance requirements

**Follow-up**: "This determines which optional AVM parameters to configure."

---

## Instructions

### Mandatory Workflow

**IMPORTANT**: Follow these steps **in order**. Do not skip steps.

---

#### Step 1: Initial Analysis

**Objective**: Understand current project context

**Actions**:
1. Identify current working directory
2. Check if `.azure/bicep/` directory already exists
3. Check for existing Bicep files or AVM module usage
4. Identify project type and deployment target

**Verification**: Project context understood before proceeding

---

#### Step 2: Load Index Files

**Objective**: Understand available context and memory structure

**Actions**:
1. Read `../../context/azure/index.md` to understand Azure Bicep context
2. Read `../../memory/skills/generate-azure-bicep/index.md` to understand memory structure

**Verification**: Indexes loaded, know which context files to load next

---

#### Step 3: Load Project Memory

**Objective**: Check for existing project-specific Bicep configurations

**Actions**:
1. Determine project name from current directory or user input
2. Check if `../../memory/skills/generate-azure-bicep/{project-name}/` exists
3. If exists, read all memory files:
   - `bicep_config.md` - Previous infrastructure setup
   - `avm_modules.md` - AVM modules used and versions
   - `resource_naming.md` - Naming conventions
   - `customizations.md` - Custom wrapper modules

**Verification**: Memory loaded if exists; ready to use previous configurations

---

#### Step 4: Load Bicep Context

**Objective**: Load Azure Verified Modules and Bicep knowledge

**Actions**:
1. Read `../../context/azure/azure_verified_modules.md` - AVM usage, module references, best practices
2. Read `../../context/azure/azure_bicep_overview.md` - Bicep syntax and structure

**Verification**: Context loaded, understand AVM patterns and Bicep syntax

---

#### Step 5: Gather Requirements

**Objective**: Ask user Socratic questions to gather all requirements

**Actions**:
1. Ask about **infrastructure scope** (which Azure resources)
2. Ask about **environments** (dev, staging, prod)
3. Ask about **resource naming convention**
4. Ask about **Azure region(s)**
5. Ask about **deployment scope** (resource group, subscription, etc.)
6. Ask about **custom requirements** (private endpoints, managed identities, etc.)

**Verification**: All requirements gathered, user confirmed ready to proceed

---

#### Step 6: Design Module Structure

**Objective**: Plan which AVM modules to use and how to compose them

**Actions**:
1. **Map requirements to AVM modules**:
   - Storage Account → `avm/res/storage/storage-account`
   - Function App → `avm/res/web/site`
   - Key Vault → `avm/res/key-vault/vault`
   - (etc. for all required resources)

2. **Determine module dependencies**:
   - Identify which modules depend on others
   - Plan output sharing between modules
   - Design proper ordering

3. **Plan custom wrapper modules**:
   - Identify if any resources need custom wrappers
   - Design wrapper module parameters
   - Document wrapper purpose

**Verification**: Module structure designed, dependencies mapped

---

#### Step 7: Generate Bicep Structure

**Objective**: Create `.azure/bicep/` directory with all files

**Actions**:

1. **Create directory structure**:
   ```bash
   mkdir -p .azure/bicep/modules
   mkdir -p .azure/docs
   ```

2. **Generate main.bicep**:
   - Set targetScope (subscription, resourceGroup, etc.)
   - Define parameters for environment-agnostic values
   - Reference AVM modules with pinned versions
   - Pass parameters to modules
   - Define outputs for resource IDs and names

3. **Generate bicepparams files** for each environment:
   - `main.development.bicepparams`
   - `main.staging.bicepparams`
   - `main.production.bicepparams`
   - Set environment-specific SKUs, regions, names

4. **Generate custom wrapper modules** (if needed):
   - Create modules in `.azure/bicep/modules/`
   - Wrap AVM modules with project-specific defaults
   - Document wrapper purpose and parameters

5. **Generate documentation**:
   - `.azure/docs/infrastructure.md` - Explains infrastructure setup
   - Parameter descriptions
   - Deployment instructions

**Verification**: All files created, no errors during generation

---

#### Step 8: Customize Templates

**Objective**: Populate templates with project-specific values

**Actions**:
1. Replace placeholders in main.bicep:
   - `{{PROJECT_NAME}}` - Project name
   - `{{RESOURCE_PREFIX}}` - Resource naming prefix
   - `{{DEFAULT_LOCATION}}` - Default Azure region

2. Replace placeholders in bicepparams:
   - `{{ENVIRONMENT}}` - Environment name
   - `{{LOCATION}}` - Azure region
   - `{{SKU}}` - Resource SKU for environment

3. Configure AVM module versions:
   - Use latest stable versions from registry
   - Pin to specific versions for reproducibility
   - Document version choices

**Verification**: Templates customized with correct values

---

#### Step 9: Validate Bicep Files

**Objective**: Ensure generated Bicep is syntactically correct

**Actions**:
1. Validate Bicep syntax:
   ```bash
   az bicep build --file .azure/bicep/main.bicep
   ```

2. Validate deployment (if Azure CLI available):
   ```bash
   az deployment sub validate \
     --location <location> \
     --template-file .azure/bicep/main.bicep \
     --parameters .azure/bicep/main.development.bicepparams
   ```

3. Check AVM module versions exist:
   ```bash
   az bicep list-versions --module-path "br/public:avm/res/..."
   ```

**Verification**: No syntax errors, all modules accessible

---

#### Step 10: Present Results

**Objective**: Show user what was generated and next steps

**Actions**:
1. Display generated directory structure
2. List all created files with their purposes
3. Provide deployment instructions:
   ```bash
   # Deploy to subscription
   az deployment sub create \
     --location <location> \
     --template-file .azure/bicep/main.bicep \
     --parameters .azure/bicep/main.development.bicepparams

   # Or deploy to resource group
   az deployment group create \
     --resource-group <rg-name> \
     --template-file .azure/bicep/main.bicep \
     --parameters .azure/bicep/main.development.bicepparams
   ```

4. Explain how to update:
   - Change parameters in .bicepparams files
   - Update AVM module versions
   - Add new resources to main.bicep

**Verification**: User understands what was generated and how to deploy

---

#### Step 11: Update Project Memory

**Objective**: Store configuration for future reference

**Actions**:
1. Create/update `../../memory/skills/generate-azure-bicep/{project-name}/bicep_config.md`:
   - Deployment scope (subscription, resource group)
   - Resource naming convention
   - Environments configured
   - Azure regions used

2. Create/update `avm_modules.md`:
   - List all AVM modules used
   - Module versions and purposes
   - Module dependencies

3. Create/update `resource_naming.md`:
   - Naming patterns for each resource type
   - Examples of generated names

4. Create/update `customizations.md`:
   - Custom wrapper modules created
   - Deviations from standard AVM usage
   - Special configurations

**Verification**: Memory files created/updated with all relevant information

---

### Compliance Checklist

Before completing this skill, verify:

- [ ] User questions asked and answered (Step 5)
- [ ] AVM modules identified and mapped to requirements (Step 6)
- [ ] `.azure/bicep/` directory created with correct structure (Step 7)
- [ ] main.bicep generated using AVM module references (Step 7)
- [ ] bicepparams files created for all environments (Step 7)
- [ ] Custom wrapper modules created if needed (Step 7)
- [ ] Documentation generated (Step 7)
- [ ] Templates customized with project-specific values (Step 8)
- [ ] Bicep files validated (syntax and deployment) (Step 9)
- [ ] Results presented to user with deployment instructions (Step 10)
- [ ] Project memory updated (Step 11)

---

## Best Practices

### Azure Verified Modules

1. **Always use AVM modules** - Don't rewrite what Microsoft provides
2. **Pin module versions** - Use specific versions, not `latest`
3. **Use public registry** - `br/public:avm/...` for stable, tested modules
4. **Check module documentation** - Review parameters and examples before use
5. **Leverage module outputs** - Pass resource IDs between modules
6. **Apply consistent tags** - Use AVM's built-in tagging support

### Bicep Structure

1. **One main.bicep** - Single entry point for all environments
2. **Separate bicepparams** - Environment-specific configurations
3. **Use modules directory** - For custom wrapper modules only
4. **Document parameters** - Clear descriptions for all params
5. **Define outputs** - Make resource IDs available to callers
6. **Set deployment scope** - Explicit `targetScope` declaration

### Resource Naming

1. **Follow Azure conventions** - Use resource type abbreviations
2. **Include environment** - Clear distinction between dev/staging/prod
3. **Use unique suffixes** - `uniqueString()` for globally unique names
4. **Be consistent** - Same pattern across all resources
5. **Document convention** - Explain naming in README

### Security

1. **Use managed identities** - Avoid storing credentials
2. **Enable diagnostic logging** - Configure in AVM modules
3. **Apply least privilege** - RBAC via AVM parameters
4. **Use private endpoints** - Where applicable
5. **Enable encryption** - Use AVM's security defaults

---

## Additional Notes

### AVM Module Registry

Modules are referenced using:
```bicep
module resource 'br/public:avm/res/{provider}/{type}:{version}' = {
  // ...
}
```

### Finding Modules

- Browse: https://aka.ms/avm
- Search: Use resource type (e.g., "storage account")
- CLI: `az bicep list-versions --module-path "br/public:avm/..."`

### Updating Modules

1. Check new versions: `az bicep list-versions ...`
2. Review changelog for breaking changes
3. Update version in main.bicep
4. Test deployment in dev environment
5. Promote to staging/production

### Custom Wrappers

Create wrappers only when:
- Need project-specific defaults
- Combining multiple AVM modules
- Adding custom logic on top of AVM

Otherwise, use AVM modules directly.

---

## Version History

### v1.0.0 (2025-11-18)

**Initial Release**
- Complete Bicep generation using Azure Verified Modules
- Support for all common Azure resources
- Multi-environment support with bicepparams
- Custom wrapper module generation
- Resource naming convention support
- Memory system for configuration tracking
- Comprehensive context for AVM usage
