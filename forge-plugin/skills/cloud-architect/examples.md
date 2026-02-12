# Cloud Architect Examples

This file contains example scenarios demonstrating how the **cloud-architect** skill designs cloud solutions across different use cases.

## Example 1: E-Commerce Platform Migration to Cloud

### Scenario

A mid-sized e-commerce company is migrating from on-premise infrastructure to the cloud. They need to support 1M daily users, process 50K orders/day, and handle seasonal traffic spikes (3x during holidays).

### Requirements
- **Performance**: < 200ms API response time, < 2s page load
- **Availability**: 99.9% uptime SLA
- **Compliance**: PCI-DSS for payment processing
- **Scale**: Handle 3x traffic during peak seasons
- **Budget**: $50K/month infrastructure budget

### Architecture Recommendation

**Cloud Provider**: AWS (chosen for mature e-commerce ecosystem and PCI-DSS compliance)

**Architecture Components**:

1. **Compute Layer**:
   - ECS Fargate for containerized microservices (web, API, order processing)
   - Lambda for background jobs (order confirmation emails, inventory updates)
   - Auto-scaling based on CPU/memory and custom metrics (order queue depth)

2. **Data Layer**:
   - Aurora PostgreSQL (Multi-AZ) for transactional data
   - ElastiCache Redis for session management and product catalog cache
   - S3 for product images and static assets
   - DynamoDB for shopping cart (low latency, high availability)

3. **Networking**:
   - CloudFront CDN for static assets and API acceleration
   - Application Load Balancer with WAF for security
   - VPC with public/private subnets across 3 AZs

4. **Security**:
   - AWS Secrets Manager for credentials
   - KMS for encryption at rest
   - VPC endpoints for private service access
   - Security groups and NACLs for network isolation
   - PCI-DSS compliant architecture (isolated payment processing)

5. **Observability**:
   - CloudWatch for metrics and logs
   - X-Ray for distributed tracing
   - SNS for alerting

**Migration Strategy**: Phased approach over 6 months
- Phase 1: Migrate static assets to S3/CloudFront (month 1)
- Phase 2: Migrate read-only APIs (product catalog) (month 2)
- Phase 3: Migrate transactional APIs with database replication (month 3-4)
- Phase 4: Migrate order processing with parallel running (month 5)
- Phase 5: Decommission on-premise (month 6)

**Cost Estimate**: $42K/month (baseline), $85K/month (peak season)
- Compute: $18K/month (ECS + Lambda)
- Database: $12K/month (Aurora + ElastiCache + DynamoDB)
- Storage & CDN: $5K/month (S3 + CloudFront)
- Networking: $4K/month (Load Balancer + Data Transfer)
- Other Services: $3K/month (CloudWatch, Secrets Manager, etc.)

**Cost Optimizations**:
- Use Savings Plans for predictable ECS workload (30% savings)
- S3 Intelligent-Tiering for product images (15% storage savings)
- Reserved capacity for Aurora (40% savings)
- Spot instances for batch processing (70% savings)

---

## Example 2: Greenfield SaaS Application (Multi-Tenant)

### Scenario

A startup is building a multi-tenant SaaS application for project management. They need a cloud-native architecture that supports rapid growth from 100 to 100K users.

### Requirements
- **Time to Market**: Launch MVP in 3 months
- **Scale**: Support 10-1000 tenants, 100-100K users
- **Data Isolation**: Strong tenant isolation for enterprise customers
- **Global**: Serve users in North America, Europe, and Asia
- **Developer Experience**: Fast iteration, CI/CD, feature flags
- **Budget**: Start with $2K/month, scale to $50K/month

### Architecture Recommendation

**Cloud Provider**: GCP (chosen for best Kubernetes support and developer experience)

**Architecture Components**:

1. **Compute Layer**:
   - GKE Autopilot for zero-ops Kubernetes
   - Cloud Run for API gateway and serverless workloads
   - Cloud Build for CI/CD

2. **Data Layer**:
   - Cloud SQL PostgreSQL with connection pooling
   - Firestore for real-time collaboration features
   - Cloud Storage for file attachments
   - Memorystore Redis for caching and rate limiting

3. **Multi-Tenancy Strategy**:
   - **Pool Model** for small tenants (shared DB with tenant_id)
   - **Silo Model** for enterprise tenants (dedicated DB instances)
   - Namespace-based isolation in Kubernetes

4. **Global Architecture**:
   - Multi-region GKE clusters (us-central1, europe-west1, asia-southeast1)
   - Cloud CDN + Load Balancer for global distribution
   - Cloud DNS with geo-routing

5. **Developer Experience**:
   - GitOps with Cloud Build + Artifact Registry
   - Separate dev/staging/production environments
   - Feature flags with LaunchDarkly (third-party)
   - Infrastructure as Code with Terraform

6. **Observability**:
   - Cloud Logging for centralized logs
   - Cloud Monitoring for metrics and alerts
   - Cloud Trace for distributed tracing
   - Error Reporting for exception tracking

**Migration Strategy**: N/A (greenfield)

**Development Phases**:
- Phase 1: MVP with single region (month 1-3)
- Phase 2: Multi-region expansion (month 4-6)
- Phase 3: Enterprise features and silo tenancy (month 7-12)

**Cost Estimate**:
- **MVP (Month 1-3)**: $2K/month
  - GKE Autopilot: $800/month (3 nodes)
  - Cloud SQL: $600/month (db-n1-standard-2)
  - Other: $600/month (storage, networking, monitoring)

- **Growth (100 tenants, 5K users)**: $12K/month
  - GKE Autopilot: $4K/month (auto-scaling)
  - Cloud SQL: $3K/month (larger instance + read replicas)
  - Multi-region: $2K/month additional
  - Other: $3K/month

- **Scale (1000 tenants, 100K users)**: $50K/month
  - GKE Autopilot: $20K/month (multi-region)
  - Cloud SQL: $15K/month (multiple instances for silo tenants)
  - Networking & CDN: $8K/month
  - Other: $7K/month

**Cost Optimizations**:
- Committed use discounts for predictable workloads (37% savings)
- Sustained use discounts automatically applied
- Cloud SQL automated backups to nearline storage
- Optimize container resource requests/limits

---

## Example 3: Hybrid Cloud Architecture for Financial Services

### Scenario

A financial services company needs to modernize their trading platform while keeping sensitive data on-premise for regulatory compliance. They need a hybrid cloud architecture.

### Requirements
- **Compliance**: SOX, FINRA - trading data must remain on-premise
- **Performance**: < 10ms latency for trade execution
- **Availability**: 99.99% uptime (52 minutes downtime/year)
- **Security**: End-to-end encryption, zero-trust network
- **Analytics**: Process historical trade data in cloud for ML models
- **Disaster Recovery**: RPO < 1 hour, RTO < 4 hours

### Architecture Recommendation

**Cloud Provider**: Azure (chosen for best hybrid cloud capabilities with Azure Arc and ExpressRoute)

**Architecture Components**:

1. **On-Premise (Core Trading)**:
   - High-performance bare metal servers for trading engine
   - PostgreSQL cluster for trade database
   - Redis for market data caching
   - HSM (Hardware Security Module) for key management

2. **Azure Cloud (Analytics & Backup)**:
   - Azure Synapse Analytics for data warehouse
   - Azure Machine Learning for predictive models
   - Azure Data Lake for historical trade data
   - Azure Site Recovery for DR

3. **Hybrid Connectivity**:
   - Azure ExpressRoute (10 Gbps) for private connectivity
   - VPN Gateway for backup connectivity
   - Azure Arc for unified management of on-premise Kubernetes

4. **Data Synchronization**:
   - Azure Data Factory for ETL pipelines
   - CDC (Change Data Capture) for near-real-time replication
   - End-of-day batch export to Data Lake
   - Encrypted data transfer with TLS 1.3

5. **Security Architecture**:
   - Zero-trust network with Azure AD + on-premise AD
   - Always-encrypted data in transit (ExpressRoute + TLS)
   - Azure Key Vault integrated with on-premise HSM
   - Azure Sentinel for SIEM
   - Private endpoints for all Azure services

6. **Disaster Recovery**:
   - On-premise active-passive cluster
   - Azure Site Recovery replication
   - Automated failover testing monthly
   - Backup retention: 7 years (compliance)

**Architecture Diagram (Conceptual)**:
```
On-Premise Data Center                     Azure Cloud
┌─────────────────────────┐               ┌─────────────────────────┐
│                         │               │                         │
│  Trading Engine         │               │  Synapse Analytics      │
│  (Bare Metal)           │               │  (Data Warehouse)       │
│         │               │               │         │               │
│         ▼               │               │         ▼               │
│  PostgreSQL Cluster ────┼──ExpressRoute─┼───▶ Data Factory        │
│  (Primary Database)     │    (10Gbps)   │    (ETL Pipeline)       │
│         │               │               │         │               │
│         │               │               │         ▼               │
│  Redis (Market Data) ───┼───────────────┼───▶ Data Lake           │
│                         │               │    (Historical Data)    │
│  HSM (Key Management) ──┼───────────────┼───▶ Key Vault           │
│                         │               │    (Cloud Secrets)      │
└─────────────────────────┘               └─────────────────────────┘
```

**Migration Strategy**: Hybrid-first (no migration)
- Deploy analytics workload to Azure (month 1-2)
- Implement CDC for near-real-time data sync (month 3)
- Set up DR with Azure Site Recovery (month 4-5)
- Implement ML models for trade prediction (month 6+)

**Cost Estimate**: $85K/month
- ExpressRoute 10Gbps: $15K/month
- Synapse Analytics: $35K/month (enterprise tier)
- Data Lake Storage: $5K/month (petabyte scale)
- Azure Machine Learning: $10K/month (GPU compute)
- Site Recovery & Backup: $8K/month
- Networking & Other: $12K/month

**Compliance Considerations**:
- SOX: Audit logging with Azure Monitor + Sentinel
- FINRA: Trade data retention policies (7 years)
- Encryption: FIPS 140-2 Level 3 (HSM)
- Access controls: RBAC with Just-In-Time access
- Network isolation: Private endpoints, no public internet

---

## Example 4: IoT Platform on Multi-Cloud

### Scenario

A manufacturing company needs to build an IoT platform to collect telemetry from 100K devices across 50 factories worldwide. They want to avoid cloud vendor lock-in.

### Requirements
- **Scale**: 100K devices, 1M messages/second
- **Global**: 50 factories in 20 countries
- **Latency**: < 100ms for command & control
- **Multi-Cloud**: Avoid vendor lock-in, use best-of-breed services
- **Analytics**: Real-time anomaly detection, predictive maintenance
- **Cost**: Optimize for massive data ingestion

### Architecture Recommendation

**Cloud Providers**: Multi-cloud (AWS + GCP)
- **AWS**: Global edge locations for IoT ingestion (AWS IoT Core)
- **GCP**: Best-in-class analytics and ML (BigQuery, Vertex AI)

**Architecture Components**:

1. **Ingestion Layer (AWS)**:
   - AWS IoT Core for device connectivity (MQTT/HTTPS)
   - IoT Device Defender for security
   - Kinesis Data Streams for real-time data buffering
   - Lambda for data transformation

2. **Analytics Layer (GCP)**:
   - Pub/Sub for cross-cloud messaging
   - Dataflow for stream processing
   - BigQuery for data warehouse
   - Vertex AI for ML models (anomaly detection)

3. **Edge Computing**:
   - AWS IoT Greengrass on factory edge devices
   - Local processing for low-latency control
   - Offline operation capability

4. **Cross-Cloud Integration**:
   - VPN connections between AWS and GCP
   - Kinesis → Pub/Sub bridge
   - Shared authentication with OIDC

5. **Data Flow**:
   ```
   Devices → AWS IoT Core → Kinesis → Lambda → Pub/Sub (GCP)
                                ↓
                          S3 (raw data archive)
                                               ↓
                                          Dataflow → BigQuery
                                                         ↓
                                                    Vertex AI
   ```

**Cost Estimate**: $65K/month
- AWS IoT Core: $15K/month (100K devices, 1M messages/sec)
- AWS Kinesis: $10K/month (data streams)
- GCP Pub/Sub: $8K/month (message delivery)
- GCP BigQuery: $20K/month (queries + storage)
- GCP Vertex AI: $8K/month (ML training + inference)
- Cross-cloud networking: $4K/month

**Multi-Cloud Benefits**:
- **Best-of-breed**: AWS for IoT, GCP for analytics
- **Reduced lock-in**: Can migrate analytics layer if needed
- **Negotiating power**: Competitive pricing discussions
- **Regulatory**: Use region-specific clouds for data sovereignty

**Multi-Cloud Challenges & Mitigations**:
- **Data transfer costs**: Batch transfers during off-peak, use compression
- **Operational complexity**: Terraform for IaC, unified monitoring with Datadog
- **Security**: Shared identity with OIDC, encrypted tunnels
- **Skills gap**: Cross-train team on both platforms

---

## Common Patterns Across Examples

### Architectural Principles Applied
1. **Cloud-Native Design**: Leverage managed services over self-managed
2. **Auto-Scaling**: Design for elastic scale
3. **High Availability**: Multi-AZ/region deployments
4. **Security**: Defense in depth, encryption everywhere, zero-trust
5. **Cost Optimization**: Right-sizing, reserved capacity, spot instances
6. **Observability**: Centralized logging, metrics, tracing

### Decision Frameworks
1. **Cost vs Performance**: Balance based on business SLAs
2. **Build vs Buy**: Prefer managed services for non-differentiating work
3. **Monolith vs Microservices**: Based on team size and complexity
4. **Stateful vs Stateless**: Prefer stateless for scalability
5. **Synchronous vs Asynchronous**: Use async for decoupling

### Migration Strategies
1. **Strangler Fig**: Gradually replace legacy with new
2. **Parallel Running**: Run old and new side-by-side
3. **Database Replication**: CDC for zero-downtime migration
4. **Phased Rollout**: Reduce risk with gradual cutover
5. **Rollback Plan**: Always have a path back
