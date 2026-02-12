# cloud-architect Memory

Project-specific memory for cloud architecture design, including architectural decisions, cloud provider choices, patterns, and cost optimizations.

## Purpose

This memory helps the `skill:cloud-architect` remember:
- Project architecture decisions and rationale
- Cloud provider selections and constraints
- Cloud-native patterns and anti-patterns discovered
- Cost optimization strategies that worked
- Migration lessons learned
- Performance benchmarks and scale profiles

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md` ⭐ CRITICAL

**Purpose**: High-level project understanding - ALWAYS CREATE THIS FIRST

**Must contain**:
- **Project name and purpose**: What does this application do?
- **Cloud provider(s)**: AWS, Azure, GCP, or multi-cloud
- **Deployment regions**: Geographic distribution
- **Architecture pattern**: Microservices, serverless, monolith, etc.
- **Key services**: Compute, database, storage, networking services
- **Scale profile**: Expected users, transactions, data volume
- **Performance requirements**: Latency, throughput, availability SLAs
- **Compliance requirements**: SOC2, HIPAA, GDPR, PCI-DSS, etc.
- **Budget constraints**: Monthly infrastructure budget
- **Team expertise**: Cloud platform experience level

#### `architecture_patterns.md`

**Purpose**: Document reusable patterns and design decisions

**Must contain**:
- **Compute patterns**: Container orchestration, serverless, VMs
- **Data patterns**: Database choices, caching strategies, data partitioning
- **Networking patterns**: Load balancing, CDN, VPC design
- **Security patterns**: IAM, encryption, network isolation
- **Resilience patterns**: HA, DR, fault tolerance strategies
- **Scaling patterns**: Auto-scaling policies, load distribution

#### `cloud_decisions.md`

**Purpose**: Track major architectural decisions and trade-offs

**Must contain**:
- **Decision**: What was decided
- **Context**: Why the decision was needed
- **Alternatives considered**: What other options were evaluated
- **Rationale**: Why this option was chosen
- **Trade-offs**: What was gained and what was sacrificed
- **Date**: When the decision was made
- **Status**: Active, deprecated, superseded

### Optional Files

#### `cost_optimizations.md`
- Cost reduction strategies implemented
- Savings achieved (percentage or dollar amount)
- Reserved capacity and savings plans
- Right-sizing recommendations
- Monitoring and alerting for cost anomalies

#### `migration_notes.md`
- Migration strategy and phases
- Lessons learned during migration
- Rollback procedures
- Data migration approaches
- Downtime windows and impact

#### `performance_benchmarks.md`
- Load testing results
- Latency measurements
- Throughput capabilities
- Bottlenecks identified
- Optimization impact

## Cross-Skill Integration

The `cloud-architect` skill integrates with:
- **devops-engineer**: CI/CD pipeline design
- **kubernetes-specialist**: Container orchestration
- **sre-engineer**: Observability and reliability
- **terraform-engineer**: Infrastructure as Code
- **secure-code**: Security architecture

Use `memoryStore.getByProject("{project-name}")` to discover insights from other skills.

## Memory Lifecycle

- **Fresh** (0-30 days): Active project, full detail
- **Active** (31-90 days): Ongoing project, maintain key decisions
- **Stale** (91-180 days): Archived project, summarize learnings
- **Archived** (181+ days): Compress to key decisions only

## Example Memory Entry

### Example: `e-commerce-platform/architecture_patterns.md`

```markdown
# Architecture Patterns - E-Commerce Platform

**Last Updated**: 2026-02-10
**Cloud Provider**: AWS
**Regions**: us-east-1 (primary), eu-west-1 (secondary)

## Compute Patterns

### Pattern: Containerized Microservices
- **Technology**: ECS Fargate
- **Services**: Web frontend, API gateway, order service, inventory service, payment service
- **Auto-scaling**: CPU-based (target 70%) + custom metrics (order queue depth)
- **Rationale**: Simplified operations with Fargate, avoid Kubernetes overhead
- **Cost**: ~$18K/month

## Data Patterns

### Pattern: Polyglot Persistence
- **Transactional Data**: Aurora PostgreSQL (orders, users, products)
- **Session Data**: ElastiCache Redis (user sessions, shopping carts)
- **Search**: OpenSearch (product catalog search)
- **Files**: S3 (product images, user uploads)
- **Rationale**: Use the right database for the right use case

### Pattern: Database Sharding
- **Approach**: Horizontal sharding by customer_id
- **Shards**: 4 Aurora clusters (us-east-1a, 1b, 1c, 1d)
- **Routing**: Consistent hashing in application layer
- **Rationale**: Support 10M+ customers with consistent performance

## Security Patterns

### Pattern: Zero-Trust Network
- **VPC**: Private subnets for all services
- **Access**: VPC endpoints for AWS services (no internet gateway)
- **Authentication**: JWT tokens with 15-minute expiry
- **Encryption**: TLS 1.3 in transit, KMS encryption at rest
- **Secrets**: AWS Secrets Manager with automatic rotation

## Cost Optimizations

- **Savings Plans**: 3-year commitment for ECS (30% savings = $5.4K/month)
- **Reserved Instances**: Aurora reserved capacity (40% savings = $4.8K/month)
- **S3 Intelligent-Tiering**: Automatic storage class migration (15% savings = $750/month)
- **Total Savings**: $11K/month (20% reduction)
```

## Guidelines

1. **Always load memory first** before making architecture recommendations
2. **Document all major decisions** with rationale and trade-offs
3. **Track cost optimizations** with measurable savings
4. **Update memory after each engagement** to capture learnings
5. **Cross-reference related skills** for holistic project understanding
6. **Use templates** for consistency across projects
7. **Keep memory current** - prune outdated patterns quarterly

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial memory structure for cloud-architect skill |
