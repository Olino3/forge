# kubernetes-specialist Memory

Project-specific memory for Kubernetes orchestration, including cluster configurations, deployment strategies, autoscaling patterns, security policies, and operational learnings.

## Purpose

This memory helps the `skill:kubernetes-specialist` remember:
- Cluster architecture decisions and configurations
- Deployment patterns and strategies used
- Autoscaling configurations and effectiveness
- Networking and service mesh choices
- Security policies and RBAC configurations
- Performance metrics and resource utilization
- Troubleshooting history and incident learnings
- Custom operator implementations

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md` ⭐ CRITICAL

**Purpose**: High-level project understanding - ALWAYS CREATE THIS FIRST

**Must contain**:
- **Project name and purpose**: What does this application/platform do?
- **Cloud provider and service**: AKS (Azure), EKS (AWS), GKE (Google), self-hosted
- **Cluster name(s)**: Development, staging, production cluster names
- **Kubernetes version**: Current version and upgrade schedule
- **Workload type**: Microservices, monolith, batch jobs, ML training, databases
- **Scale profile**: Number of services, pods, nodes, requests/sec
- **Deployment targets**: Namespaces, environments
- **Team size and expertise**: Number of developers, Kubernetes experience level
- **High availability requirements**: Multi-zone, multi-region, SLA targets
- **Compliance requirements**: PCI-DSS, HIPAA, SOC2, CIS Kubernetes Benchmark

#### `cluster_patterns.md`

**Purpose**: Document reusable cluster and application patterns

**Must contain**:
- **Node pool strategy**: System nodes, user nodes, GPU nodes, spot instances
- **Networking**: CNI plugin, ingress controller, service mesh
- **Storage**: StorageClasses, persistent volume configurations
- **Compute patterns**: Deployment, StatefulSet, DaemonSet usage
- **Service exposure**: ClusterIP, LoadBalancer, Ingress patterns
- **Resource management**: Requests/limits strategy, LimitRanges, ResourceQuotas
- **Health checks**: Liveness, readiness, startup probe configurations

#### `deployment_strategies.md`

**Purpose**: Track deployment approaches and results

**Must contain**:
- **Strategy type**: Rolling updates, blue/green, canary, recreate
- **Rollout configuration**: maxSurge, maxUnavailable, progressDeadlineSeconds
- **Progressive delivery**: Flagger, Argo Rollouts configuration
- **Health validation**: Post-deployment checks and smoke tests
- **Rollback procedures**: How to revert deployments
- **Deployment frequency**: How often deployments occur per service
- **Incident history**: Failed deployments and lessons learned

### Optional Files

#### `autoscaling_configs.md`
- Horizontal Pod Autoscaler (HPA) configurations
- Vertical Pod Autoscaler (VPA) settings
- Cluster Autoscaler configuration
- KEDA event-driven autoscaling
- Custom metrics and scaling effectiveness
- Cost savings from autoscaling

#### `security_policies.md`
- RBAC roles and bindings
- Pod Security Standards implementation
- Network Policies and traffic rules
- Secrets management approach (External Secrets, Sealed Secrets)
- Image scanning and admission control
- Service mesh security (mTLS, authorization policies)
- Compliance configurations

#### `networking_notes.md`
- CNI plugin choice and rationale
- Ingress controller configuration
- Service mesh implementation (Istio, Linkerd)
- DNS configuration
- Network policy patterns
- Load balancer and CDN integration

#### `observability_setup.md`
- Prometheus and Grafana configuration
- Logging stack (ELK, Loki)
- Distributed tracing (Jaeger, Tempo)
- Alerting rules and notification channels
- Dashboards and visualizations
- SLO/SLI definitions

#### `operator_implementations.md`
- Custom operators developed
- CRD definitions
- Operator deployment and lifecycle
- Automation use cases
- Lessons learned from operator development

#### `troubleshooting_guide.md`
- Common issues and resolutions
- CrashLoopBackOff debugging steps
- Networking troubleshooting
- Performance optimization learnings
- Node and pod eviction patterns
- Emergency procedures and contacts

## Cross-Skill Integration

The `kubernetes-specialist` skill integrates with:
- **cloud-architect**: Cluster infrastructure design and cloud service integration
- **devops-engineer**: CI/CD pipeline integration and deployment automation
- **sre-engineer**: Observability, monitoring, and reliability engineering
- **terraform-engineer**: Infrastructure as Code for cluster provisioning
- **security-engineer**: Cluster hardening and compliance

Use `memoryStore.getByProject("{project-name}")` to discover insights from other skills.

## Memory Lifecycle

- **Fresh** (0-30 days): Active cluster, full detail
- **Active** (31-90 days): Stable cluster, maintain key configurations
- **Stale** (91-180 days): Legacy cluster, summarize learnings
- **Archived** (181+ days): Decommissioned cluster, keep lessons learned only

## Example Memory Entry

### Example: `ecommerce-platform/cluster_patterns.md`

```markdown
# Cluster Patterns - E-Commerce Platform

**Last Updated**: 2026-02-12
**Cluster Provider**: Azure Kubernetes Service (AKS)
**Kubernetes Version**: 1.28.3
**Cluster Name**: production-aks-eastus

## Node Pool Configuration

### System Node Pool
- **Name**: system
- **VM Size**: Standard_D2s_v3 (2 vCPU, 8 GB RAM)
- **Node Count**: 3 (autoscale 3-5)
- **Availability Zones**: 1, 2, 3
- **Taints**: CriticalAddonsOnly=true:NoSchedule
- **Purpose**: CoreDNS, metrics-server, cluster-autoscaler, ingress-nginx
- **Cost**: $260/month

### User Node Pool
- **Name**: user
- **VM Size**: Standard_D4s_v3 (4 vCPU, 16 GB RAM)
- **Node Count**: 5 (autoscale 3-20)
- **Availability Zones**: 1, 2, 3
- **Purpose**: Application workloads (15 microservices)
- **Cost**: $650/month (baseline), up to $2,600/month (peak)

### Spot Node Pool
- **Name**: spot
- **VM Size**: Standard_D4s_v3
- **Node Count**: 0 (autoscale 0-10)
- **Priority**: Spot (evictable)
- **Taints**: kubernetes.azure.com/scalesetpriority=spot:NoSchedule
- **Purpose**: Background jobs, batch processing, non-critical workloads
- **Cost**: $195/month (70% savings vs on-demand)
- **Note**: Applications must tolerate node evictions

## Networking

### CNI Plugin: Azure CNI
- **Rationale**: Direct VNET integration, better performance than kubenet
- **Pod CIDR**: 10.244.0.0/16 (65,536 IPs)
- **Service CIDR**: 10.0.0.0/16
- **DNS Service IP**: 10.0.0.10
- **Trade-off**: Higher IP consumption but better Azure integration

### Network Policy: Calico
- **Rationale**: Fine-grained network policies, eBPF support
- **Default Policy**: Deny all ingress, allow DNS
- **Pattern**: Namespace isolation + service-to-service whitelisting
- **Cost**: Free (open-source)

### Ingress Controller: NGINX Ingress
- **Version**: 4.8.0
- **Replicas**: 3 (spread across zones)
- **TLS**: cert-manager with Let's Encrypt
- **Rate Limiting**: 100 req/sec per IP
- **Cost**: $195/month (Azure Load Balancer)
- **Alternatives Considered**: Traefik (simpler), Kong (API gateway features)

## Deployment Patterns

### Pattern 1: Stateless Microservices
- **Resource**: Deployment
- **Replicas**: 3-5 (HPA managed)
- **Update Strategy**: RollingUpdate with maxSurge=1, maxUnavailable=0
- **Health Checks**: 
  - Liveness: HTTP GET /health/live, delay 30s, period 10s
  - Readiness: HTTP GET /health/ready, delay 10s, period 5s
- **Resources**: 
  - Requests: 100m CPU, 128Mi memory
  - Limits: 500m CPU, 512Mi memory
- **QoS Class**: Burstable
- **Example Services**: user-service, order-service, payment-service

### Pattern 2: Background Workers
- **Resource**: Deployment
- **Replicas**: 2-10 (KEDA managed based on queue depth)
- **Tolerations**: Spot instances (cost optimization)
- **Resources**: 
  - Requests: 200m CPU, 256Mi memory
  - Limits: 1000m CPU, 1Gi memory
- **Queue Integration**: Azure Service Bus
- **Autoscaling**: KEDA ScaledObject with queue length trigger
- **Example Services**: email-worker, invoice-generator, analytics-worker

### Pattern 3: Stateful Databases
- **Resource**: StatefulSet with CloudNativePG operator
- **Replicas**: 3 (1 primary + 2 replicas)
- **Storage**: Azure Premium Disks (managed-premium-retain)
- **Backup**: Daily to Azure Blob Storage with 30-day retention
- **Anti-Affinity**: Required, spread across zones
- **Example**: PostgreSQL cluster for transactional data

## Autoscaling Configuration

### HPA - Horizontal Pod Autoscaler
- **Metrics**: CPU (70%), Memory (80%), custom metrics (requests/sec)
- **Scale-down Stabilization**: 300 seconds (5 minutes)
- **Scale-up Policy**: Max 100% (double) or +4 pods per 15 seconds
- **Scale-down Policy**: Max 50% per minute
- **Effectiveness**: Handles 3x traffic spikes during sales events
- **Cost Savings**: $800/month during off-peak hours

### VPA - Vertical Pod Autoscaler
- **Mode**: Recommendations only (not auto-update)
- **Usage**: Right-size resource requests based on actual usage
- **Result**: Reduced memory requests by 30% average
- **Cost Savings**: $300/month from better node bin-packing

### Cluster Autoscaler
- **Scale-up**: When pods pending due to insufficient resources
- **Scale-down**: When node utilization < 50% for 10 minutes
- **Effectiveness**: Adds nodes in 2-3 minutes, removes in 10-15 minutes
- **Max Nodes**: 20 (user pool) + 10 (spot pool)
- **Cost Impact**: Dynamic scaling saves $1,200/month vs fixed capacity

## Security Policies

### RBAC Strategy
- **Developers**: Namespace-scoped roles (read-only production)
- **DevOps**: Cluster-wide admin (with audit logging)
- **Services**: Minimal ServiceAccount permissions (least privilege)
- **Example**: user-service can only read its own ConfigMaps/Secrets

### Pod Security Standards
- **Production Namespace**: Restricted (no privileged containers)
- **Development Namespace**: Baseline (some flexibility)
- **Policy Enforcement**: Admission controller (built-in)

### Network Policies
- **Default**: Deny all ingress
- **Allowed**: 
  - Ingress from ingress-nginx namespace
  - Service-to-service (explicit whitelist)
  - Egress to DNS, databases, external APIs
- **Result**: Zero lateral movement in case of pod compromise

### Secrets Management
- **Approach**: External Secrets Operator + Azure Key Vault
- **Rotation**: Automatic every 90 days
- **Access**: Pod ServiceAccount identity with Azure AD workload identity
- **Benefit**: Secrets never stored in Git or etcd (encrypted in transit only)

## Cost Optimization

### Total Monthly Cost: $4,200 (baseline) to $8,500 (peak)
- **Compute**: $3,500 (nodes)
- **Storage**: $400 (persistent volumes + backups)
- **Networking**: $200 (load balancer + ingress)
- **Monitoring**: $100 (Prometheus storage)

### Optimizations Applied
1. **Spot Instances**: 70% savings for non-critical workloads ($600/month saved)
2. **HPA Scale-Down**: Reduce replicas during off-peak ($800/month saved)
3. **VPA Recommendations**: Right-sized requests ($300/month saved)
4. **Reserved Instances**: 40% savings on baseline nodes ($500/month saved)
5. **Storage Tiering**: Cool tier for old backups ($50/month saved)

**Total Savings**: $2,250/month (35% reduction from unoptimized)

## Lessons Learned

### Lesson 1: PodDisruptionBudgets are Critical
- **Issue**: Cluster autoscaler scaled down node, taking all 3 replicas of payment-service offline
- **Solution**: Added PDB with minAvailable: 2
- **Result**: Zero unplanned downtime since implementation

### Lesson 2: Readiness Probes Save Deployments
- **Issue**: New deployment pushed to production, pods started serving traffic before database connection ready
- **Solution**: Added readiness probe with 10-second initial delay
- **Result**: Zero 5xx errors during deployments

### Lesson 3: Resource Limits Prevent Noisy Neighbors
- **Issue**: Analytics job consumed all node memory, causing OOM kills for other pods
- **Solution**: Enforced LimitRanges and set strict memory limits
- **Result**: Stable memory utilization, no more evictions

### Lesson 4: Spot Instances Need Toleration
- **Issue**: Critical service scheduled on spot node, evicted during high demand
- **Solution**: Added node anti-affinity to avoid spot instances for critical services
- **Result**: Only non-critical workloads use spot, 70% cost savings maintained
```

## Guidelines

1. **Always load memory first** before making cluster recommendations
2. **Document all architecture decisions** with rationale and trade-offs
3. **Track autoscaling effectiveness** with before/after metrics
4. **Record security policies** and compliance configurations
5. **Update troubleshooting guide** with every incident
6. **Cross-reference related skills** for holistic understanding
7. **Capture cost optimizations** with measurable savings
8. **Keep version information current** - track Kubernetes upgrades
9. **Document operator implementations** for knowledge sharing
10. **Measure everything** - resource utilization, scaling events, deployment frequency

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial memory structure for kubernetes-specialist skill |
