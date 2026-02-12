# Terraform Engineer Skill

**Version:** 1.0.0  
**Category:** Cloud & Infrastructure  
**Primary Domain:** azure  
**Tags:** terraform, iac, infrastructure-as-code, aws, azure, gcp, multi-cloud, automation, hashicorp

---

## Overview

The Terraform Engineer skill provides comprehensive Infrastructure as Code (IaC) capabilities using HashiCorp Terraform. This skill enables declarative infrastructure provisioning, state management, module design, multi-cloud deployments, and enterprise-grade automation across AWS, Azure, GCP, and hybrid environments.

## Core Capabilities

### 1. Infrastructure Design & Architecture
- Multi-tier infrastructure patterns (web, app, data layers)
- Network topology design (VPCs, subnets, routing, security groups)
- High availability and disaster recovery architectures
- Landing zone and account/subscription scaffolding
- Microservices infrastructure patterns
- Serverless infrastructure components
- Container orchestration infrastructure (EKS, AKS, GKE)

### 2. Module Development
- Reusable, composable module design
- Module versioning and registry management
- Input validation and type constraints
- Output organization and documentation
- Module testing strategies
- Private module registries
- Module dependency management

### 3. State Management
- Remote state backends (S3, Azure Storage, GCS, Terraform Cloud)
- State locking and consistency
- State file encryption and security
- State migration and import strategies
- Workspace isolation patterns
- State backup and recovery
- Multi-environment state organization

### 4. Multi-Cloud & Hybrid
- Provider configuration and version management
- Cross-cloud resource dependencies
- Multi-cloud disaster recovery
- Cloud-agnostic abstractions
- Hybrid cloud connectivity (VPN, ExpressRoute, Interconnect)
- Provider aliasing and multiple regions
- Federated identity and access

### 5. Security & Compliance
- Secret management (Vault, parameter stores, key vaults)
- Resource tagging and governance
- Policy as Code (Sentinel, OPA)
- Encryption at rest and in transit
- Network security (NSGs, NACLs, firewall rules)
- IAM roles, policies, and service principals
- Compliance scanning (Checkov, tfsec, Terrascan)

### 6. Testing & Validation
- Unit testing with Terratest
- Integration testing strategies
- Static analysis and linting (tflint, terraform validate)
- Security scanning (tfsec, Checkov, Snyk)
- Plan validation and change review
- Cost estimation (Infracost)
- Drift detection and remediation

### 7. CI/CD Integration
- GitOps workflows (Atlantis, Terraform Cloud, Spacelift)
- Pull request automation and validation
- Automated plan and apply pipelines
- Environment promotion strategies
- Rollback procedures
- Blue-green infrastructure deployments
- Canary release patterns

### 8. Day-2 Operations
- Drift detection and correction
- Resource import and adoption
- Infrastructure refactoring and migrations
- Performance optimization
- Cost optimization and rightsizing
- Lifecycle management (create_before_destroy, prevent_destroy)
- Disaster recovery and backup automation

---

## Provider Coverage

| Provider | Capabilities | Common Resources |
|----------|-------------|------------------|
| **AWS** | VPC, EC2, S3, RDS, Lambda, EKS, CloudFront, Route53 | vpc, subnet, instance, s3_bucket, rds_instance, lambda_function |
| **Azure** | VNet, VMs, Storage, SQL, AKS, App Service, Front Door | resource_group, virtual_network, linux_virtual_machine, storage_account |
| **GCP** | VPC, Compute Engine, GCS, Cloud SQL, GKE, Cloud Run | compute_network, compute_instance, storage_bucket, sql_database_instance |
| **Kubernetes** | Namespaces, deployments, services, ingress, RBAC | namespace, deployment, service, ingress, config_map |
| **Cloudflare** | DNS, CDN, WAF, Workers | zone, record, page_rule, worker_script |
| **Datadog** | Monitors, dashboards, SLOs, integrations | monitor, dashboard, service_level_objective |

---

## Remote Backend Comparison

| Backend | Best For | Locking | Encryption | Cost |
|---------|----------|---------|------------|------|
| **S3 + DynamoDB** | AWS environments | ✅ DynamoDB | ✅ KMS | Low (storage + requests) |
| **Azure Storage** | Azure environments | ✅ Blob lease | ✅ Key Vault | Low (storage + transactions) |
| **GCS** | GCP environments | ✅ Native | ✅ CMEK | Low (storage + operations) |
| **Terraform Cloud** | Multi-cloud, teams | ✅ Native | ✅ Native | Free tier, paid plans |
| **Consul** | Service mesh integration | ✅ Native | ✅ Vault integration | Self-hosted |
| **etcd** | Kubernetes-centric | ✅ Native | ✅ TLS | Self-hosted |

---

## Testing Tools Comparison

| Tool | Type | Language | Strengths |
|------|------|----------|-----------|
| **Terratest** | Integration testing | Go | Full infrastructure validation, retry logic, parallel tests |
| **terraform validate** | Syntax validation | Native | Fast, catches configuration errors |
| **tflint** | Linting | Native | Provider-specific rules, best practices |
| **tfsec** | Security scanning | Go | Fast, comprehensive security checks, custom rules |
| **Checkov** | Policy scanning | Python | Multi-framework, graph-based analysis, CI/CD integration |
| **Terrascan** | Compliance scanning | Go | 500+ policies, multi-cloud, admission controller |
| **Infracost** | Cost estimation | Go | Pull request cost estimates, budget alerts |
| **Sentinel** | Policy as Code | HCL | Terraform Cloud/Enterprise, fine-grained policies |

---

## Mandatory Workflow

All terraform-engineer invocations MUST follow this workflow:

### 1. Initial Analysis
```markdown
**Project Context:**
- Infrastructure scope: [cloud providers, regions, resource types]
- Environment: [dev/staging/production]
- Existing infrastructure: [greenfield/brownfield/hybrid]
- Terraform version: [version or latest stable]
- Team size and expertise: [context for module complexity]

**Requirements Analysis:**
- Functional requirements: [what infrastructure is needed]
- Non-functional: [HA, DR, performance, compliance]
- Security requirements: [encryption, access control, networking]
- Cost constraints: [budget limits, cost optimization needs]
- Timeline: [deployment schedule, phasing]
```

### 2. Load Memory
```bash
# Via memoryStore interface
memoryStore.load("terraform-engineer")
```

**Retrieve:**
- Previous infrastructure patterns used
- Module design decisions and rationale
- State management configurations
- Provider version constraints
- Security scanning results
- Testing strategies employed
- Lessons learned from previous deployments
- Reusable module inventory

### 3. Load Context
```bash
# Via contextProvider interface
contextProvider.loadDomains(["azure", "aws", "gcp", "security", "devops"])
contextProvider.getByTags(["terraform", "infrastructure-as-code", "cloud-native"])
```

**Focus Areas:**
- Cloud provider best practices (azure, aws, gcp context files)
- Security patterns (security domain)
- CI/CD integration patterns (devops domain)
- Network architecture patterns
- Multi-cloud design considerations

### 4. Architecture Design
```markdown
**Infrastructure Architecture:**
- Resource organization: [modules, workspaces, state files]
- Network topology: [VPCs/VNets, subnets, connectivity]
- Compute resources: [VMs, containers, serverless]
- Data layer: [databases, storage, caching]
- Security perimeter: [firewalls, NSGs, NACLs, WAF]
- Identity and access: [IAM, RBAC, service principals]

**Module Structure:**
```
terraform/
├── modules/
│   ├── networking/
│   ├── compute/
│   ├── database/
│   └── security/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
└── shared/
    ├── backend.tf
    ├── providers.tf
    └── variables.tf
```

**State Management:**
- Backend: [S3/Azure Storage/GCS/Terraform Cloud]
- State file organization: [per environment, per component]
- Locking mechanism: [DynamoDB/blob lease/native]
- Encryption: [KMS/Key Vault/CMEK]
```

### 5. Module Development
```markdown
**Module Design Principles:**
- Single responsibility per module
- Composable and reusable
- Well-documented inputs and outputs
- Sensible defaults with override capability
- Version constraints for dependencies

**Module Template:**
```hcl
# modules/example/main.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Input validation
variable "environment" {
  type        = string
  description = "Environment name"
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

# Resource definitions with lifecycle rules
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location
  
  tags = merge(
    var.common_tags,
    {
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  )
  
  lifecycle {
    prevent_destroy = true
  }
}

# Outputs with descriptions
output "resource_group_id" {
  description = "The ID of the resource group"
  value       = azurerm_resource_group.main.id
}
```
```

### 6. State Backend Configuration
```hcl
# backend.tf (AWS example)
terraform {
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "infrastructure/production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:ACCOUNT:key/KEY_ID"
    dynamodb_table = "terraform-state-lock"
    
    # Workspace prefix for multi-environment
    workspace_key_prefix = "environments"
  }
}

# backend.tf (Azure example)
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatestorage"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"
    use_azuread_auth     = true
  }
}
```

### 7. Security Implementation
```markdown
**Security Checklist:**
- [ ] Secrets stored in Vault/Parameter Store/Key Vault (never in code)
- [ ] State files encrypted at rest
- [ ] Network segmentation implemented (public/private subnets)
- [ ] Least privilege IAM policies
- [ ] Resource tagging for governance
- [ ] Encryption in transit (TLS/SSL)
- [ ] Security scanning configured (tfsec, Checkov)
- [ ] Audit logging enabled
- [ ] Backup and recovery procedures

**Secret Management Example:**
```hcl
# Using Azure Key Vault
data "azurerm_key_vault_secret" "db_password" {
  name         = "database-password"
  key_vault_id = data.azurerm_key_vault.main.id
}

# Using AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/password"
}

# Never hardcode secrets
resource "azurerm_mysql_server" "main" {
  administrator_login_password = data.azurerm_key_vault_secret.db_password.value
  # ...
}
```
```

### 8. Testing Strategy
```markdown
**Multi-Layer Testing:**

**1. Validation (fast, pre-commit):**
```bash
terraform fmt -check -recursive
terraform validate
tflint --config .tflint.hcl
```

**2. Security Scanning:**
```bash
tfsec .
checkov -d . --framework terraform
terrascan scan -t terraform
```

**3. Plan Analysis:**
```bash
terraform plan -out=tfplan
terraform show -json tfplan | jq '.resource_changes[] | select(.change.actions != ["no-op"])'
```

**4. Cost Estimation:**
```bash
infracost breakdown --path .
```

**5. Integration Testing (Terratest):**
```go
func TestAzureWebApp(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/azure-webapp",
        Vars: map[string]interface{}{
            "environment": "test",
        },
    }
    
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)
    
    appURL := terraform.Output(t, terraformOptions, "app_url")
    http_helper.HttpGetWithRetry(t, appURL, nil, 200, "Hello", 30, 5*time.Second)
}
```
```

### 9. CI/CD Integration
```markdown
**GitOps Workflow (GitHub Actions example):**
```yaml
name: Terraform
on:
  pull_request:
    paths: ['terraform/**']
  push:
    branches: [main]
    paths: ['terraform/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Init
        run: terraform init
        
      - name: Terraform Validate
        run: terraform validate
        
      - name: Security Scan
        run: |
          docker run --rm -v $(pwd):/src aquasec/tfsec /src
          
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        
      - name: Cost Estimate
        uses: infracost/actions/comment@v1
        with:
          path: tfplan
          
  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Terraform Apply
        run: terraform apply -auto-approve tfplan
```

**Atlantis Configuration:**
```yaml
version: 3
projects:
  - name: production
    dir: environments/production
    workspace: production
    terraform_version: v1.5.0
    autoplan:
      when_modified: ["*.tf", "*.tfvars"]
      enabled: true
    apply_requirements: [approved, mergeable]
    workflow: custom
    
workflows:
  custom:
    plan:
      steps:
        - init
        - plan
        - run: tfsec .
        - run: checkov -d .
    apply:
      steps:
        - apply
```
```

### 10. Drift Detection & Remediation
```markdown
**Drift Detection Strategy:**

**1. Scheduled Drift Detection:**
```bash
#!/bin/bash
# Run daily drift detection
terraform plan -detailed-exitcode -out=drift.tfplan

if [ $? -eq 2 ]; then
    echo "Drift detected!"
    terraform show drift.tfplan > drift-report.txt
    # Send notification (Slack, email, etc.)
    # Create ticket for remediation
fi
```

**2. Continuous Drift Monitoring:**
```yaml
# Using Terraform Cloud
resource "tfe_workspace" "production" {
  name         = "production"
  organization = "myorg"
  
  assessments_enabled = true  # Enable health assessments
  
  # Run drift detection daily
  trigger_prefixes = []
  auto_apply       = false
}
```

**3. Import Existing Resources:**
```bash
# Import manually created resources
terraform import azurerm_resource_group.main /subscriptions/SUB_ID/resourceGroups/my-rg
terraform import aws_instance.web i-1234567890abcdef0
```
```

### 11. Generate Output
Output is saved to `/claudedocs/` following `OUTPUT_CONVENTIONS.md`:

**File Structure:**
```
/claudedocs/terraform-engineer-{project}-{timestamp}/
├── architecture/
│   ├── infrastructure-diagram.md
│   ├── network-topology.md
│   └── security-controls.md
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
├── docs/
│   ├── deployment-guide.md
│   ├── operational-runbook.md
│   └── disaster-recovery.md
├── tests/
│   ├── terratest/
│   └── security-scans/
└── IMPLEMENTATION_SUMMARY.md
```

**IMPLEMENTATION_SUMMARY.md Template:**
```markdown
# Infrastructure Implementation Summary

**Project:** {project_name}
**Date:** {timestamp}
**Terraform Version:** {version}
**Providers:** {provider_list}

## Architecture Overview
{high-level description}

## Infrastructure Components
| Component | Type | Count | Cloud Provider |
|-----------|------|-------|----------------|
| VPC/VNet | Network | X | AWS/Azure/GCP |
| Subnets | Network | X | AWS/Azure/GCP |
| VMs/Instances | Compute | X | AWS/Azure/GCP |
| Load Balancers | Network | X | AWS/Azure/GCP |
| Databases | Data | X | AWS/Azure/GCP |

## Module Inventory
- **networking**: VPC/VNet with public/private subnets
- **compute**: Auto-scaling VM/instance groups
- **database**: RDS/Azure SQL/Cloud SQL with backups
- **security**: Security groups, NSGs, firewall rules

## State Management
- **Backend**: {S3/Azure Storage/GCS/Terraform Cloud}
- **Encryption**: {KMS/Key Vault/CMEK}
- **Locking**: {DynamoDB/blob lease/native}
- **State Files**: {count and organization}

## Security Measures
- All secrets stored in {Vault/Secrets Manager/Key Vault}
- State encrypted with {KMS/Key Vault/CMEK}
- Network segmentation: {public/private/data tiers}
- IAM policies: {least privilege approach}
- Scanning: {tfsec, Checkov results}

## Testing Results
- **Validation**: ✅ All files valid
- **Security Scan**: ✅ {X} checks passed, {Y} issues resolved
- **Cost Estimate**: ${estimated_monthly_cost}
- **Integration Tests**: ✅ {X} tests passed

## Deployment Instructions
1. Initialize: `terraform init`
2. Validate: `terraform validate && tfsec .`
3. Plan: `terraform plan -out=tfplan`
4. Review: Review plan output and cost estimates
5. Apply: `terraform apply tfplan`

## Operational Notes
- Drift detection: {schedule and process}
- Backup procedures: {state backup process}
- Disaster recovery: {RTO and RPO targets}
- Cost optimization: {recommendations}

## Next Steps
- [ ] {action items}
```
```

### 12. Update Memory
```bash
# Via memoryStore interface
memoryStore.append("terraform-engineer", {
  project: "project_name",
  timestamp: "ISO8601",
  infrastructure: {
    providers: ["aws", "azure", "gcp"],
    resource_count: 150,
    modules_created: ["networking", "compute", "database"],
    environments: ["dev", "staging", "production"]
  },
  state_management: {
    backend: "s3",
    encryption: "aws-kms",
    locking: "dynamodb"
  },
  security: {
    scanning_tools: ["tfsec", "checkov"],
    issues_found: 5,
    issues_resolved: 5,
    secrets_management: "aws-secrets-manager"
  },
  testing: {
    validation_passed: true,
    security_scan_passed: true,
    integration_tests: 12,
    cost_estimate: "$2,450/month"
  },
  ci_cd: {
    tool: "github-actions",
    automation: ["plan-on-pr", "apply-on-merge", "drift-detection"]
  },
  lessons_learned: [
    "consideration or optimization made",
    "challenge overcome and solution"
  ],
  reusable_patterns: [
    "pattern that can be applied to future projects"
  ]
})
```

---

## Best Practices

### Module Design
- **Single Responsibility**: Each module should do one thing well
- **Composition**: Build complex infrastructure from simple modules
- **Versioning**: Use semantic versioning for modules (1.0.0, 1.1.0, 2.0.0)
- **Documentation**: README.md with usage examples, inputs, outputs
- **Defaults**: Provide sensible defaults, allow overrides
- **Validation**: Use variable validation blocks for constraints
- **Testing**: Test modules independently with multiple scenarios

### State Management
- **Remote Backend**: Always use remote backends for team collaboration
- **State Locking**: Enable locking to prevent concurrent modifications
- **Encryption**: Encrypt state files at rest and in transit
- **Separation**: Separate state files by environment and component
- **Backup**: Regular automated backups of state files
- **Access Control**: Restrict state file access via IAM/RBAC
- **Version Control**: Never commit state files to Git

### Security
- **Secret Management**: Use Vault, Secrets Manager, or Key Vault
- **Least Privilege**: Apply minimal IAM permissions
- **Network Segmentation**: Public, private, and data tiers
- **Encryption**: Enable encryption at rest and in transit
- **Scanning**: Run tfsec/Checkov in CI/CD pipelines
- **Tagging**: Consistent tagging for governance and cost allocation
- **Audit Logging**: Enable CloudTrail, Azure Monitor, Cloud Audit Logs

### Performance
- **Parallelism**: Use `-parallelism` flag for large deployments
- **Targeted Operations**: Use `-target` for specific resource updates
- **State Optimization**: Keep state files reasonably sized (<10MB)
- **Resource Timeouts**: Configure appropriate timeouts for resources
- **Workspaces**: Use workspaces for environment isolation
- **Dependency Management**: Minimize explicit dependencies

### Workflow
- **Plan Before Apply**: Always review plans before applying
- **Small Changes**: Make incremental changes, not big-bang deployments
- **Testing**: Test in dev before deploying to production
- **Automation**: Automate plan/apply through CI/CD
- **Drift Detection**: Regular scheduled drift detection
- **Documentation**: Keep documentation in sync with code

---

## Multi-Cloud Patterns

### Provider Configuration
```hcl
# Configure multiple providers
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Provider aliases for multiple regions
provider "aws" {
  region = "us-east-1"
  alias  = "primary"
}

provider "aws" {
  region = "us-west-2"
  alias  = "secondary"
}

# Cross-cloud resource dependencies
resource "aws_s3_bucket" "backup" {
  provider = aws.primary
  bucket   = "multi-cloud-backup"
}

resource "azurerm_storage_account" "primary" {
  name                = "primarystorage"
  resource_group_name = azurerm_resource_group.main.name
  location            = "East US"
  
  # Reference to AWS resource for disaster recovery
  tags = {
    BackupLocation = aws_s3_bucket.backup.bucket
  }
}
```

### Cross-Cloud Networking
```hcl
# AWS VPN Gateway
resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "AWS-Azure VPN Gateway"
  }
}

# Azure VPN Gateway
resource "azurerm_virtual_network_gateway" "main" {
  name                = "azure-vpn-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  type     = "Vpn"
  vpn_type = "RouteBased"
  
  ip_configuration {
    public_ip_address_id          = azurerm_public_ip.vpn.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}

# Cross-cloud connection configuration
resource "azurerm_virtual_network_gateway_connection" "aws" {
  name                = "azure-to-aws"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  type                       = "IPsec"
  virtual_network_gateway_id = azurerm_virtual_network_gateway.main.id
  local_network_gateway_id   = azurerm_local_network_gateway.aws.id
  
  shared_key = data.azurerm_key_vault_secret.vpn_key.value
}
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| State lock timeout | Concurrent terraform runs | Check for stuck locks, force-unlock if needed |
| Provider version conflict | Incompatible versions | Update `required_providers` constraints |
| Resource already exists | Resource created outside Terraform | Use `terraform import` to adopt resource |
| Drift detected | Manual changes in console | Reconcile changes or update Terraform code |
| Plan shows unexpected changes | State out of sync | Run `terraform refresh` to sync state |
| Module not found | Incorrect source path | Verify module source and run `terraform init` |
| Authentication failure | Expired credentials | Refresh credentials (aws sso login, az login, gcloud auth) |

### Debugging Techniques
```bash
# Enable detailed logging
export TF_LOG=DEBUG
export TF_LOG_PATH=terraform.log
terraform plan

# Validate configuration
terraform validate
terraform fmt -check -recursive

# Check state
terraform state list
terraform state show <resource>

# Graph dependencies
terraform graph | dot -Tpng > graph.png

# Force unlock state
terraform force-unlock <LOCK_ID>

# Refresh state without changes
terraform plan -refresh-only
```

---

## Integration Points

- **Azure DevOps**: Use Azure Pipelines for automated deployments
- **GitHub Actions**: Automate plan/apply on PR and merge
- **GitLab CI**: Use GitLab runners for Terraform execution
- **Jenkins**: Classic CI/CD integration with Terraform plugins
- **Atlantis**: Pull request automation for Terraform
- **Terraform Cloud**: HashiCorp's managed Terraform service
- **Spacelift**: Advanced Terraform automation platform
- **Vault**: Dynamic secret generation and management
- **Sentinel**: Policy as Code enforcement (Terraform Cloud/Enterprise)
- **Infracost**: Cost estimation in pull requests
- **Datadog**: Infrastructure monitoring integration
- **PagerDuty**: Alert routing for infrastructure issues

---

## Related Skills

- **azure-automation**: Azure-specific automation and ARM templates
- **docker-specialist**: Container infrastructure and orchestration
- **security-architect**: Infrastructure security patterns
- **ci-cd-expert**: Pipeline integration and GitOps workflows

---

## References

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Azure Terraform Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [AWS Terraform Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GCP Terraform Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Terratest Documentation](https://terratest.gruntwork.io/)
- [tfsec Documentation](https://aquasecurity.github.io/tfsec/)
- [Checkov Documentation](https://www.checkov.io/)
- [Infracost Documentation](https://www.infracost.io/docs/)
