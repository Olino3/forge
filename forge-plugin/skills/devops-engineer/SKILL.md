---
name: "devops-engineer"
description: "CI/CD pipelines, infrastructure automation, and DevOps practices. Designs build, test, and deployment pipelines across platforms (GitHub Actions, GitLab CI, Azure Pipelines, Jenkins). Implements infrastructure automation, release strategies, and DevOps culture practices."
version: "1.0.0"
context:
  primary_domain: "azure"
  always_load_files: []
  detection_required: false
  file_budget: 6
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, pipeline_patterns.md, deployment_strategies.md]
    - type: "shared-project"
      usage: "reference"
## tags: [devops, cicd, pipelines, automation, github-actions, azure-pipelines, gitlab, jenkins]

# skill:devops-engineer - CI/CD Pipelines & Infrastructure Automation

## Version: 1.0.0

## Purpose

The **devops-engineer** skill designs and implements CI/CD pipelines, infrastructure automation, and DevOps practices. It creates efficient build, test, and deployment workflows, implements release strategies, and promotes DevOps culture.

**Use this skill when:**
- Setting up CI/CD pipelines for a new project
- Optimizing existing build and deployment workflows
- Implementing infrastructure automation
- Designing release strategies (blue/green, canary, rolling)
- Troubleshooting pipeline failures
- Migrating between CI/CD platforms

**Produces:**
- Pipeline configuration files (GitHub Actions, Azure Pipelines, GitLab CI, etc.)
- Infrastructure automation scripts
- Deployment strategies and runbooks
- Pipeline optimization recommendations
- DevOps best practices documentation

## File Structure

```
skills/devops-engineer/
├── SKILL.md (this file)
├── examples.md
└── templates/
    └── pipeline_template.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather project requirements:
  - Source control platform (GitHub, GitLab, Azure DevOps, Bitbucket)
  - Programming language(s) and build tools
  - Testing framework(s)
  - Deployment targets (cloud, on-premise, hybrid)
  - Release frequency and strategy
  - Team size and expertise
  - Security and compliance requirements
- Detect existing CI/CD configuration:
  - Analyze `.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`
  - Review build scripts and deployment configurations
  - Identify pain points and bottlenecks
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="devops-engineer"` and `domain="azure"` (or detected domain).

**Load project-specific memory:**
```
memoryStore.getSkillMemory("devops-engineer", "{project-name}")
```

**Check for cross-skill insights:**
```
memoryStore.getByProject("{project-name}")
```

**Review memory for:**
- Previous pipeline configurations and lessons learned
- Deployment strategies that worked/failed
- Build optimization techniques
- Security scanning integrations
- Performance benchmarks (build times, deployment times)

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `azure` domain and other relevant domains. Stay within the file budget declared in frontmatter.

**Use context indexes:**
```
contextProvider.getDomainIndex("azure")
contextProvider.getDomainIndex("git")
contextProvider.getDomainIndex("engineering")
contextProvider.getDomainIndex("security")
```

**Load relevant context files based on project needs:**
- Azure Pipelines patterns if using Azure DevOps
- Git workflow patterns
- Security scanning patterns
- Container and Kubernetes patterns if relevant

**Budget: 6 files maximum**

### Step 4: Pipeline Design

- Design CI/CD pipeline stages:
  - **Source**: Trigger conditions (push, PR, schedule, manual)
  - **Build**: Compilation, dependency resolution, artifact creation
  - **Test**: Unit tests, integration tests, security scans, code quality
  - **Package**: Container images, application packages, deployment artifacts
  - **Deploy**: Environment promotion (dev → staging → prod)
  - **Verify**: Smoke tests, health checks, rollback triggers
- Choose pipeline platform and justify:
  - GitHub Actions: Best for GitHub-hosted repos, extensive marketplace
  - GitLab CI: Best for GitLab, integrated security scanning
  - Azure Pipelines: Best for Microsoft stack, enterprise features
  - Jenkins: Best for self-hosted, maximum customization
- Define pipeline triggers and conditions
- Plan artifact management and caching strategies
- Design environment-specific configurations

### Step 5: Infrastructure Automation

- Implement Infrastructure as Code (IaC):
  - Terraform for multi-cloud provisioning
  - ARM/Bicep for Azure resources
  - CloudFormation for AWS resources
  - Pulumi for programming language-based IaC
- Automate environment provisioning:
  - Development, staging, production environments
  - Environment parity (minimize dev/prod differences)
  - Ephemeral environments for PRs/feature branches
- Implement configuration management:
  - Environment variables and secrets
  - Feature flags
  - Configuration drift detection

### Step 6: Release Strategy

- Design deployment strategy:
  - **Blue/Green**: Zero-downtime, instant rollback
  - **Canary**: Gradual rollout with monitoring
  - **Rolling**: Sequential updates with minimal downtime
  - **Feature Flags**: Progressive feature enablement
- Implement deployment gates:
  - Manual approval gates for production
  - Automated quality gates (test pass rate, code coverage)
  - Security gates (vulnerability scanning, compliance checks)
- Plan rollback and disaster recovery:
  - Automated rollback triggers
  - Database migration rollback
  - State recovery procedures

### Step 7: Testing & Quality Gates

- Implement comprehensive testing:
  - **Unit Tests**: Fast, isolated component tests
  - **Integration Tests**: API and service integration tests
  - **E2E Tests**: Full user journey tests
  - **Performance Tests**: Load and stress testing
  - **Security Tests**: SAST, DAST, dependency scanning
- Set quality gates:
  - Code coverage thresholds (e.g., 80% minimum)
  - Test pass rate requirements (e.g., 100% for production)
  - Security vulnerability limits (e.g., no critical CVEs)
  - Code quality scores (e.g., Sonar quality gate)
- Implement fail-fast mechanisms

### Step 8: Observability & Monitoring

- Implement pipeline observability:
  - Build and deployment metrics (success rate, duration)
  - Failure alerts and notifications
  - Pipeline analytics and trends
- Integrate application monitoring:
  - Health check endpoints
  - Deployment markers in monitoring tools
  - Error rate tracking post-deployment
- Set up feedback loops:
  - Failed build notifications (Slack, Teams, email)
  - Deployment summaries
  - Performance regression alerts

### Step 9: Security & Compliance

- Implement security scanning:
  - Static Application Security Testing (SAST)
  - Software Composition Analysis (SCA) for dependencies
  - Container image scanning
  - Infrastructure security scanning (IaC validation)
- Manage secrets securely:
  - Use platform secret stores (GitHub Secrets, Azure Key Vault)
  - Rotate secrets regularly
  - Never commit secrets to source control
- Implement compliance controls:
  - Audit logging
  - Access controls and approvals
  - Artifact signing and verification

### Step 10: Generate Output

- Save DevOps documentation to `/claudedocs/devops-engineer_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Use template from `templates/pipeline_template.md` if available
- Include:
  - Pipeline architecture diagram
  - Configuration files (complete and ready to use)
  - Deployment strategy and runbooks
  - Testing strategy and quality gates
  - Security and compliance measures
  - Monitoring and alerting setup
  - Troubleshooting guide
  - Next steps and improvement recommendations

### Step 11: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="devops-engineer"`.

**Store learned insights:**
```
memoryStore.updateSkillMemory("devops-engineer", "{project-name}", {
  pipeline_patterns: [...],
  deployment_strategies: [...],
  optimizations: [...],
  lessons_learned: [...]
})
```

**Update memory with:**
- Pipeline configurations and patterns
- Deployment strategies and results
- Build optimization techniques
- Security integration patterns
- Performance metrics and improvements
- Common issues and resolutions

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Pipeline design completed with all stages (Step 4)
- [ ] Infrastructure automation implemented (Step 5)
- [ ] Release strategy defined (Step 6)
- [ ] Testing and quality gates configured (Step 7)
- [ ] Observability and monitoring set up (Step 8)
- [ ] Security and compliance measures implemented (Step 9)
- [ ] Output saved with standard naming convention (Step 10)
- [ ] Standard Memory Update pattern followed (Step 11)

## DevOps Principles

### 1. Automation First
- Automate repetitive tasks
- Infrastructure as Code
- Automated testing at every stage
- Self-service environments

### 2. Continuous Integration
- Commit code frequently (daily minimum)
- Build and test on every commit
- Fail fast with rapid feedback
- Maintain a single source of truth

### 3. Continuous Delivery
- Every commit is a release candidate
- Automated deployment to staging
- Manual or automated production deployment
- Rollback capability always available

### 4. Shift Left Security
- Security scanning in development
- Automated vulnerability detection
- Secure secrets management
- Compliance as code

### 5. Observability
- Comprehensive logging
- Metrics and monitoring
- Distributed tracing
- Actionable alerts

## CI/CD Platform Comparison

| Feature | GitHub Actions | Azure Pipelines | GitLab CI | Jenkins |
|---------|---------------|-----------------|-----------|---------|
| Hosting | Cloud | Cloud + Self-hosted | Cloud + Self-hosted | Self-hosted |
| Pricing | Free (public), metered (private) | Free tier, then metered | Free tier, then metered | Free (DIY hosting) |
| Marketplace | Extensive (10K+ actions) | Moderate | Good | Extensive (plugins) |
| YAML Syntax | Straightforward | Comprehensive | Straightforward | Groovy/Declarative |
| Container Support | Excellent | Excellent | Excellent | Good |
| Kubernetes | Good (via actions) | Excellent (native) | Excellent | Good (plugins) |
| Security Scanning | Via actions | Built-in + extensions | Built-in | Via plugins |
| Best For | GitHub repos | Microsoft stack | GitLab repos | Custom workflows |

## Common Pipeline Patterns

### Pattern 1: Monorepo Multi-Service
- Detect changed services via path filters
- Run tests only for changed services
- Deploy only changed services
- Shared pipeline templates

### Pattern 2: Trunk-Based Development
- Frequent small commits to main
- Short-lived feature branches
- Feature flags for incomplete features
- Continuous deployment to staging

### Pattern 3: GitFlow
- Long-lived develop and main branches
- Feature branches for development
- Release branches for stabilization
- Hotfix branches for production fixes

### Pattern 4: Microservices Pipeline
- Service-specific pipelines
- Contract testing between services
- Independent deployment schedules
- Service mesh integration

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with comprehensive CI/CD and DevOps capabilities |
