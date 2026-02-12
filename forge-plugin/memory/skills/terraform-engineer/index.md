# Terraform Engineer - Memory Index

**Skill:** terraform-engineer  
**Category:** Cloud & Infrastructure  
**Version:** 1.0.0  
**Last Updated:** {timestamp}

---

## Purpose

This memory store captures learnings, patterns, and decisions from terraform-engineer skill invocations. Each entry records infrastructure architectures, module designs, state management strategies, security implementations, and lessons learned to improve future Infrastructure as Code deployments.

---

## Memory Structure

### Entry Format
```yaml
timestamp: ISO8601
project: string
infrastructure:
  providers: [aws, azure, gcp, etc.]
  resource_count: number
  modules_created: [list]
  environments: [dev, staging, production]
state_management:
  backend: string
  encryption: string
  locking: string
state_backend:
  backend_type: s3|azurerm|gcs|terraform-cloud
  encryption_method: string
  locking_enabled: boolean
modules_developed:
  - name: string
    purpose: string
    reusable: boolean
    tested: boolean
security:
  scanning_tools: [list]
  issues_found: number
  issues_resolved: number
  secrets_management: string
testing:
  validation_passed: boolean
  security_scan_passed: boolean
  integration_tests: number
  cost_estimate: string
ci_cd:
  tool: string
  automation: [list]
multi_cloud:
  enabled: boolean
  providers_used: [list]
  cross_cloud_networking: boolean
lessons_learned: [list]
reusable_patterns: [list]
```

---

## Memory Categories

### 1. Infrastructure Architectures
Successful infrastructure patterns across cloud providers:
- Multi-tier application architectures
- Hub-spoke network topologies
- Microservices infrastructure
- Serverless architectures
- Container orchestration platforms
- Landing zones and account structures
- Disaster recovery setups
- Multi-cloud architectures

### 2. Module Designs
Reusable Terraform modules created:
- Networking modules (VPC, subnets, routing)
- Compute modules (VMs, auto-scaling, load balancers)
- Database modules (RDS, Azure SQL, Cloud SQL)
- Security modules (security groups, NSGs, firewall rules)
- Monitoring modules (CloudWatch, Azure Monitor, Stackdriver)
- Kubernetes cluster modules
- Multi-cloud abstraction modules

### 3. State Management
Backend configurations and strategies:
- S3 + DynamoDB (AWS)
- Azure Storage with blob lease locking
- GCS with native locking
- Terraform Cloud workspaces
- State file organization patterns
- Workspace vs. separate state files
- State migration experiences
- State backup and recovery procedures

### 4. Security Implementations
Security patterns and controls:
- Secrets management approaches (Vault, Secrets Manager, Key Vault)
- Encryption strategies (KMS, CMEK, Key Vault)
- Network security architectures
- IAM and RBAC patterns
- Security scanning results (tfsec, Checkov, Terrascan)
- Compliance requirements met
- Zero-trust network designs

### 5. Testing Strategies
Testing approaches and results:
- Terratest integration tests
- Security scanning configurations
- Cost estimation integrations
- Plan validation processes
- Drift detection setups
- Module testing patterns
- Pre-commit hooks and validations

### 6. CI/CD Integration
Automation and GitOps patterns:
- GitHub Actions workflows
- Azure DevOps pipelines
- GitLab CI configurations
- Atlantis setups
- Terraform Cloud automations
- Spacelift configurations
- Custom pipeline scripts

### 7. Multi-Cloud Patterns
Cross-cloud infrastructure:
- Provider configuration strategies
- Cross-cloud networking (VPN, ExpressRoute, Interconnect)
- Multi-cloud disaster recovery
- Cloud-agnostic abstractions
- Cost optimization across clouds
- Unified monitoring and observability

### 8. Performance Optimizations
Terraform execution optimizations:
- Parallelism configurations
- State file size management
- Targeted operations usage
- Workspace strategies
- Dependency optimization
- Resource import techniques

---

## Query Patterns

Memory can be queried by:
- **Cloud Provider**: `aws`, `azure`, `gcp`, `multi-cloud`
- **Module Type**: `networking`, `compute`, `database`, `security`
- **State Backend**: `s3`, `azurerm`, `gcs`, `terraform-cloud`
- **Environment**: `dev`, `staging`, `production`
- **Architecture Pattern**: `multi-tier`, `hub-spoke`, `microservices`, `serverless`
- **Security Tool**: `tfsec`, `checkov`, `terrascan`, `vault`
- **CI/CD Tool**: `github-actions`, `azure-devops`, `atlantis`, `terraform-cloud`
- **Testing Type**: `terratest`, `security-scan`, `cost-estimate`

---

## Example Queries

### Find AWS Multi-Tier Architectures
```
Filter entries where:
  infrastructure.providers contains "aws"
  AND "multi-tier" in reusable_patterns
```

### Find Modules with Terratest Coverage
```
Filter entries where:
  testing.integration_tests > 0
  AND modules_developed[].tested == true
```

### Find Multi-Cloud Setups
```
Filter entries where:
  multi_cloud.enabled == true
  AND length(multi_cloud.providers_used) > 1
```

### Find Specific Security Patterns
```
Filter entries where:
  security.secrets_management == "vault"
  AND security.issues_resolved == security.issues_found
```

---

## Maintenance

### Pruning Criteria
Memory entries are retained based on:
- **Reusability**: Entries with reusable patterns kept indefinitely
- **Recency**: Recent projects (< 6 months) always retained
- **Uniqueness**: Novel architectures or solutions retained
- **Reference Value**: Frequently referenced entries retained
- **Age**: Entries > 2 years old reviewed for relevance

### Quality Indicators
High-value entries should include:
- ✅ Detailed module inventory with purposes
- ✅ State management configuration specifics
- ✅ Security scanning results with remediation
- ✅ Testing coverage metrics
- ✅ Cost estimates and optimizations
- ✅ Lessons learned with actionable insights
- ✅ Reusable patterns applicable to future projects
- ✅ CI/CD automation details
- ✅ Performance optimization techniques

---

## Integration with Skill Workflow

Memory is accessed at two key points:

### Load Phase (Step 2)
Retrieve relevant patterns before infrastructure design:
```bash
memoryStore.load("terraform-engineer")
# Filter by project characteristics
# Apply relevant patterns to current design
```

### Update Phase (Step 12)
Append new learnings after implementation:
```bash
memoryStore.append("terraform-engineer", {
  # Complete entry with all metadata
  # Include lessons learned
  # Document reusable patterns
})
```

---

## Sample Memory Entries

### Entry 1: AWS Multi-Tier Web Application
```yaml
timestamp: 2024-01-15T10:30:00Z
project: ecommerce-platform
infrastructure:
  providers: [aws]
  resource_count: 87
  modules_created: [networking, compute, database, monitoring]
  environments: [dev, staging, production]
state_management:
  backend: s3
  encryption: aws-kms
  locking: dynamodb
modules_developed:
  - name: networking
    purpose: VPC with public/private/data subnets across 3 AZs
    reusable: true
    tested: true
  - name: compute
    purpose: ALB + Auto Scaling Groups with CloudWatch integration
    reusable: true
    tested: true
  - name: database
    purpose: RDS MySQL with read replica and automated backups
    reusable: true
    tested: false
security:
  scanning_tools: [tfsec, checkov]
  issues_found: 8
  issues_resolved: 8
  secrets_management: aws-secrets-manager
testing:
  validation_passed: true
  security_scan_passed: true
  integration_tests: 12
  cost_estimate: "$2,450/month"
ci_cd:
  tool: github-actions
  automation: [plan-on-pr, apply-on-merge, drift-detection, cost-comment]
lessons_learned:
  - "Use lifecycle policies on state bucket to prevent accidental deletion"
  - "Enable detailed CloudWatch logs for all Auto Scaling actions"
  - "Implement cost allocation tags at the provider level"
  - "Use data sources for AMI IDs instead of hardcoding"
reusable_patterns:
  - "3-tier network segmentation pattern works well for most applications"
  - "Separate state files per environment reduces blast radius"
  - "ALB health checks should match application readiness probes"
```

### Entry 2: Azure Landing Zone
```yaml
timestamp: 2024-02-20T14:45:00Z
project: enterprise-landing-zone
infrastructure:
  providers: [azure]
  resource_count: 156
  modules_created: [hub, spoke, governance, shared-services]
  environments: [production]
state_management:
  backend: azurerm
  encryption: azure-key-vault
  locking: blob-lease
modules_developed:
  - name: hub
    purpose: Central hub VNet with Firewall, Bastion, VPN Gateway
    reusable: true
    tested: true
  - name: spoke
    purpose: Spoke VNet with peering, routing, and NSGs
    reusable: true
    tested: true
  - name: governance
    purpose: Management groups, policies, budgets, Security Center
    reusable: true
    tested: false
security:
  scanning_tools: [checkov, terrascan]
  issues_found: 12
  issues_resolved: 11
  secrets_management: azure-key-vault
testing:
  validation_passed: true
  security_scan_passed: false
  integration_tests: 0
  cost_estimate: "$8,750/month"
ci_cd:
  tool: azure-devops
  automation: [plan-on-pr, manual-approval, apply-on-merge]
lessons_learned:
  - "Use azurerm_features block to prevent accidental deletions"
  - "Management group structure should be planned before implementation"
  - "Azure Policy assignments take 15-30 minutes to propagate"
  - "Use service endpoints instead of private endpoints for cost savings in dev"
  - "One unresolved security issue: NSG rule too permissive (accepted for Bastion)"
reusable_patterns:
  - "Hub-spoke topology scales well to 50+ spokes"
  - "Centralized Azure Firewall reduces costs vs. per-spoke firewalls"
  - "Use Bastion instead of jump boxes for better security"
  - "Policy-driven governance is more maintainable than manual controls"
```

### Entry 3: Multi-Cloud Kubernetes
```yaml
timestamp: 2024-03-10T09:15:00Z
project: multi-cloud-k8s-platform
infrastructure:
  providers: [aws, azure, gcp]
  resource_count: 243
  modules_created: [k8s-cluster, networking, monitoring]
  environments: [dev, staging, production]
state_management:
  backend: terraform-cloud
  encryption: terraform-cloud-native
  locking: terraform-cloud-native
multi_cloud:
  enabled: true
  providers_used: [aws, azure, gcp]
  cross_cloud_networking: false
modules_developed:
  - name: k8s-cluster
    purpose: Abstracted K8s cluster for AWS/Azure/GCP
    reusable: true
    tested: true
  - name: networking
    purpose: Cloud-agnostic network setup
    reusable: true
    tested: true
security:
  scanning_tools: [tfsec, checkov, infracost]
  issues_found: 15
  issues_resolved: 15
  secrets_management: vault
testing:
  validation_passed: true
  security_scan_passed: true
  integration_tests: 24
  cost_estimate: "$12,300/month (all clouds)"
ci_cd:
  tool: gitlab-ci
  automation: [plan-on-pr, atlantis-integration, sentinel-policies]
lessons_learned:
  - "Provider version constraints critical for multi-cloud modules"
  - "Use HashiCorp Vault for secrets across all clouds"
  - "Cloud-agnostic abstractions require careful planning"
  - "Terraform Cloud workspaces work better than local state for teams"
  - "Test each cloud provider independently before integration"
reusable_patterns:
  - "Abstract cloud differences behind consistent module interfaces"
  - "Use conditional logic for cloud-specific resources"
  - "Unified outputs enable consistent consumption patterns"
  - "Separate workspaces per cloud provider, not per environment"
```

---

## Notes

- Memory is append-only; entries are never modified, only added
- Use descriptive project names for easy identification
- Include specific version numbers for providers and modules when relevant
- Document both successes and failures for complete learning
- Tag entries with architecture patterns for easier discovery
- Cost estimates should include currency and time period
- Security issues should document both findings and resolutions (or accepted risks)
- Lessons learned should be actionable and specific
- Reusable patterns should be detailed enough to apply to new projects

---

## Related Memory Stores

- `azure-automation`: Azure-specific patterns and ARM integration
- `docker-specialist`: Container infrastructure on cloud platforms
- `security-architect`: Security patterns applicable to IaC
- `ci-cd-expert`: Pipeline patterns for Terraform automation
