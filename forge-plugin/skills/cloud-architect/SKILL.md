---
name: "cloud-architect"
description: "Multi-cloud architecture and cloud-native design patterns. Analyzes infrastructure requirements, designs scalable cloud solutions across AWS, Azure, GCP, and recommends cloud-native patterns. Evaluates architectural trade-offs, cost optimization, and migration strategies."
version: "1.0.0"
context:
  primary_domain: "azure"
  always_load_files: []
  detection_required: false
  file_budget: 6
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, architecture_patterns.md, cloud_decisions.md]
    - type: "shared-project"
      usage: "reference"
## tags: [cloud, architecture, aws, azure, gcp, multi-cloud, cloud-native, infrastructure]

# skill:cloud-architect - Multi-Cloud Architecture & Cloud-Native Design

## Version: 1.0.0

## Purpose

The **cloud-architect** skill analyzes infrastructure requirements and designs scalable, resilient cloud solutions across multiple cloud providers (AWS, Azure, GCP). It evaluates architectural patterns, recommends cloud-native approaches, performs cost-benefit analysis, and provides migration strategies.

**Use this skill when:**
- Designing a new cloud-native application architecture
- Evaluating migration from on-premise to cloud
- Reviewing existing cloud architecture for optimization
- Making cloud provider selection decisions
- Designing multi-cloud or hybrid cloud solutions
- Optimizing cloud costs and resource utilization

**Produces:**
- Architecture diagrams and design documents
- Cloud provider recommendations with trade-off analysis
- Migration roadmaps and strategies
- Cost optimization recommendations
- Disaster recovery and business continuity plans

## File Structure

```
skills/cloud-architect/
├── SKILL.md (this file)
├── examples.md
└── templates/
    └── architecture_report_template.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather project requirements and constraints:
  - Business objectives and user requirements
  - Expected scale (users, transactions, data volume)
  - Performance requirements (latency, throughput)
  - Compliance and regulatory requirements
  - Budget constraints
  - Existing infrastructure and dependencies
- Detect current cloud environment (if any):
  - Analyze infrastructure files (Terraform, CloudFormation, ARM templates)
  - Review deployment configurations
  - Identify existing cloud services in use
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="cloud-architect"` and `domain="azure"` (or detected domain).

**Load project-specific memory:**
```
memoryStore.getSkillMemory("cloud-architect", "{project-name}")
```

**Check for cross-skill insights:**
```
memoryStore.getByProject("{project-name}")
```

**Review memory for:**
- Previous architecture decisions and rationale
- Cloud provider preferences and constraints
- Existing patterns and conventions
- Performance benchmarks and load profiles
- Cost optimization learnings

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `azure` domain and other relevant cloud domains. Stay within the file budget declared in frontmatter.

**Use context indexes:**
```
contextProvider.getDomainIndex("azure")
contextProvider.getDomainIndex("engineering")
contextProvider.getDomainIndex("security")
```

**Load relevant context files based on project needs:**
- Azure patterns if targeting Azure
- Docker/Kubernetes patterns for containerization
- CI/CD patterns for deployment pipelines
- Security guidelines for compliance

**Budget: 6 files maximum**

### Step 4: Requirements Analysis

- Analyze functional and non-functional requirements
- Identify architectural drivers:
  - Performance requirements
  - Scalability needs
  - Availability and reliability targets
  - Security and compliance constraints
  - Cost constraints
- Map requirements to cloud service capabilities
- Identify potential architectural challenges

### Step 5: Cloud Provider Evaluation

- Evaluate cloud providers based on:
  - **Service Capabilities**: Required services availability and maturity
  - **Cost**: Pricing models, total cost of ownership
  - **Geographic Coverage**: Data center locations for compliance/latency
  - **Ecosystem**: Integration with existing tools and services
  - **Expertise**: Team familiarity and available talent
  - **Lock-in Risk**: Portability and multi-cloud strategies
- Perform comparative analysis (AWS vs Azure vs GCP)
- Consider hybrid and multi-cloud scenarios
- Document trade-offs and recommendations

### Step 6: Architecture Design

- Design cloud-native architecture:
  - **Compute Layer**: Containers, serverless, VMs, managed services
  - **Data Layer**: Databases, caching, data warehouses, object storage
  - **Networking**: VPC design, load balancing, CDN, API gateway
  - **Security**: IAM, encryption, network security, compliance
  - **Observability**: Logging, monitoring, tracing, alerting
  - **Resilience**: High availability, disaster recovery, fault tolerance
- Apply architectural patterns:
  - Microservices vs monolith
  - Event-driven architecture
  - CQRS and Event Sourcing
  - Strangler Fig for migrations
  - Circuit breaker and retry patterns
- Create architecture diagrams
- Document design decisions and alternatives considered

### Step 7: Cost Optimization

- Estimate infrastructure costs:
  - Compute costs (VMs, containers, serverless)
  - Storage costs (block, object, database)
  - Network costs (bandwidth, data transfer)
  - Service costs (managed services, API calls)
- Identify cost optimization opportunities:
  - Right-sizing instances
  - Reserved capacity and savings plans
  - Spot/preemptible instances
  - Auto-scaling strategies
  - Storage tiering
  - Network optimization
- Calculate TCO and ROI

### Step 8: Migration Strategy (if applicable)

- Assess current state (on-premise or existing cloud)
- Define target state architecture
- Develop migration strategy:
  - **Rehost** (lift-and-shift)
  - **Replatform** (lift-tinker-shift)
  - **Refactor** (re-architect for cloud-native)
  - **Rebuild** (rewrite from scratch)
  - **Replace** (adopt SaaS)
- Create phased migration roadmap
- Identify risks and mitigation strategies
- Plan for rollback and contingency

### Step 9: Generate Output

- Save architecture report to `/claudedocs/cloud-architect_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Use template from `templates/architecture_report_template.md` if available
- Include:
  - Executive summary
  - Requirements analysis
  - Cloud provider recommendation with justification
  - Architecture design with diagrams
  - Cost estimates and optimization recommendations
  - Migration roadmap (if applicable)
  - Risk assessment and mitigation
  - Next steps and implementation plan

### Step 10: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="cloud-architect"`.

**Store learned insights:**
```
memoryStore.updateSkillMemory("cloud-architect", "{project-name}", {
  architecture_patterns: [...],
  cloud_decisions: [...],
  cost_optimizations: [...],
  lessons_learned: [...]
})
```

**Update memory with:**
- Architecture decisions and rationale
- Cloud provider selection and constraints
- Patterns and anti-patterns discovered
- Cost optimization strategies that worked
- Migration lessons learned
- Performance benchmarks

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Requirements thoroughly analyzed (Step 4)
- [ ] Cloud provider evaluation completed (Step 5)
- [ ] Architecture design documented with diagrams (Step 6)
- [ ] Cost analysis performed (Step 7)
- [ ] Migration strategy defined if applicable (Step 8)
- [ ] Output saved with standard naming convention (Step 9)
- [ ] Standard Memory Update pattern followed (Step 10)

## Architecture Focus Areas

### 1. Scalability Patterns
- Horizontal vs vertical scaling
- Auto-scaling strategies
- Load balancing and distribution
- Database scaling (read replicas, sharding)
- Caching strategies

### 2. Resilience Patterns
- High availability design
- Fault tolerance and self-healing
- Disaster recovery planning
- Backup and restore strategies
- Chaos engineering principles

### 3. Security Patterns
- Zero-trust architecture
- Defense in depth
- Identity and access management
- Data encryption (at rest and in transit)
- Network segmentation
- Compliance frameworks (SOC2, HIPAA, GDPR, PCI-DSS)

### 4. Cloud-Native Patterns
- Twelve-factor app methodology
- Microservices architecture
- Event-driven architecture
- Serverless computing
- Container orchestration
- Service mesh

### 5. Cost Optimization Patterns
- Resource right-sizing
- Reserved capacity utilization
- Spot instance strategies
- Storage tiering
- Network optimization
- Idle resource elimination

## Cloud Provider Comparison Matrix

| Criteria | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Market Leader | Yes | Enterprise Focus | Innovation Focus |
| Service Breadth | Most comprehensive | Enterprise integration | Best-in-class ML/Data |
| Pricing Model | Complex, granular | Enterprise licensing | Simple, sustained use |
| Kubernetes | EKS | AKS | GKE (best-in-class) |
| Serverless | Lambda | Functions, Container Apps | Cloud Functions, Cloud Run |
| ML/AI Services | SageMaker | Azure ML | Vertex AI (strongest) |
| Enterprise Integration | Good | Excellent (Microsoft stack) | Good |
| Global Reach | Largest | Large | Growing |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with comprehensive multi-cloud architecture capabilities |
