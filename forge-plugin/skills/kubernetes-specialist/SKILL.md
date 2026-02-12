---
name: "kubernetes-specialist"
description: "Kubernetes cluster management, deployments, and operators. Designs production-ready Kubernetes infrastructure, implements deployment strategies, creates custom operators, configures autoscaling, networking, security, and observability for containerized workloads."
version: "1.0.0"
context:
  primary_domain: "azure"
  always_load_files: []
  detection_required: false
  file_budget: 6
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, cluster_patterns.md, deployment_strategies.md]
    - type: "shared-project"
      usage: "reference"
tags: [kubernetes, k8s, containers, orchestration, helm, operators, aks, eks, gke, kubectl, deployments, services, ingress, autoscaling]
---

# skill:kubernetes-specialist - Kubernetes Cluster Management & Orchestration

## Version: 1.0.0

## Purpose

The **kubernetes-specialist** skill designs and manages production-ready Kubernetes clusters, implements deployment strategies, creates custom operators, and configures autoscaling, networking, security, and observability for containerized workloads.

**Use this skill when:**
- Setting up production Kubernetes clusters (AKS, EKS, GKE, self-hosted)
- Designing microservices deployment strategies
- Creating custom Kubernetes operators
- Implementing autoscaling (HPA, VPA, Cluster Autoscaler)
- Configuring Kubernetes networking (CNI, Ingress, Service Mesh)
- Securing Kubernetes workloads (RBAC, Network Policies, Pod Security)
- Troubleshooting cluster and application issues
- Migrating workloads to Kubernetes

**Produces:**
- Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- Helm charts for application packaging
- Custom Resource Definitions (CRDs) and operators
- Cluster configuration and setup scripts
- Autoscaling and resource optimization recommendations
- Security policies and RBAC configurations
- Troubleshooting guides and runbooks

## File Structure

```
skills/kubernetes-specialist/
├── SKILL.md (this file)
├── examples.md
└── templates/
    └── k8s_architecture_template.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather cluster requirements:
  - **Workload type**: Stateless web apps, stateful databases, batch jobs, ML training
  - **Scale expectations**: Number of services, pods, nodes, requests/sec
  - **Cloud provider**: AKS (Azure), EKS (AWS), GKE (Google), or self-hosted
  - **High availability**: Multi-zone, multi-region requirements
  - **Compliance**: Security standards (CIS Kubernetes Benchmark, PCI-DSS)
  - **Budget constraints**: Node costs, storage costs, network egress
  - **Team expertise**: Kubernetes experience level
- Detect existing Kubernetes configuration:
  - Analyze `k8s/`, `kubernetes/`, `manifests/`, `.yaml` files
  - Review `helm/` charts and `kustomize/` overlays
  - Check for existing operators and CRDs
  - Identify current deployment patterns
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="kubernetes-specialist"` and `domain="azure"` (or detected domain).

**Load project-specific memory:**
```
memoryStore.getSkillMemory("kubernetes-specialist", "{project-name}")
```

**Check for cross-skill insights:**
```
memoryStore.getByProject("{project-name}")
```

**Review memory for:**
- Previous cluster configurations and architecture decisions
- Deployment patterns and strategies used
- Autoscaling configurations and effectiveness
- Security policies and RBAC configurations
- Performance benchmarks and resource utilization
- Troubleshooting history and incident learnings

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `azure` domain and other relevant domains. Stay within the file budget declared in frontmatter.

**Use context indexes:**
```
contextProvider.getDomainIndex("azure")
contextProvider.getDomainIndex("docker")
contextProvider.getDomainIndex("engineering")
contextProvider.getDomainIndex("security")
```

**Load relevant context files based on project needs:**
- Azure AKS patterns if using Azure Kubernetes Service
- Docker/container patterns for image management
- CI/CD patterns for deployment automation
- Security guidelines for cluster hardening

**Budget: 6 files maximum**

### Step 4: Cluster Architecture Design

- Design Kubernetes cluster architecture:
  - **Control Plane**: Managed (AKS/EKS/GKE) vs self-hosted
  - **Node Pools**: System nodes, user workload nodes, GPU nodes
  - **Node Sizing**: VM sizes based on workload requirements
  - **Availability Zones**: Multi-AZ for high availability
  - **Networking**: CNI plugin (Azure CNI, AWS VPC CNI, Calico, Cilium)
  - **Storage**: StorageClasses for persistent volumes (Azure Disk/Files, EBS, GCE PD)
  - **Ingress**: Ingress controller selection (NGINX, Traefik, Kong, Istio Gateway)
  - **DNS**: CoreDNS configuration and external DNS integration
- Choose Kubernetes distribution and justify:
  - **AKS**: Best for Azure workloads, managed control plane, AAD integration
  - **EKS**: Best for AWS workloads, managed control plane, IAM integration
  - **GKE**: Best for GCP workloads, best-in-class Kubernetes experience
  - **Self-hosted**: Best for on-premise, maximum control, air-gapped environments
- Define cluster sizing and scaling strategy
- Plan for disaster recovery and backup (Velero)

### Step 5: Application Deployment Strategy

- Design deployment patterns:
  - **Deployment vs StatefulSet vs DaemonSet**: Choose based on workload type
  - **ReplicaSet sizing**: Initial replicas and scaling bounds
  - **Update strategy**: RollingUpdate vs Recreate
  - **PodDisruptionBudgets**: Ensure availability during updates
  - **Resource requests/limits**: CPU and memory allocation
- Implement deployment strategies:
  - **Rolling Updates**: Zero-downtime gradual rollout
  - **Blue/Green**: Complete environment switch
  - **Canary**: Progressive traffic shifting (Flagger, Argo Rollouts)
  - **A/B Testing**: Feature-based traffic routing
- Design service exposure:
  - **ClusterIP**: Internal-only services
  - **LoadBalancer**: External cloud load balancer
  - **NodePort**: Direct node access (dev/testing)
  - **Ingress**: HTTP/S routing with path/host rules
- Configure health checks:
  - **Liveness probes**: Restart unhealthy pods
  - **Readiness probes**: Remove unhealthy pods from load balancing
  - **Startup probes**: Handle slow-starting containers

### Step 6: Autoscaling Configuration

- Implement horizontal autoscaling:
  - **Horizontal Pod Autoscaler (HPA)**:
    - Metrics: CPU, memory, custom metrics (queue depth, requests/sec)
    - Target utilization thresholds
    - Min/max replica counts
    - Scale-up/down behavior and stabilization windows
  - **KEDA (Event-driven autoscaling)**:
    - Scale based on external metrics (Azure Queue, AWS SQS, Kafka)
    - Scale to zero for cost optimization
- Implement vertical autoscaling:
  - **Vertical Pod Autoscaler (VPA)**:
    - Automatic resource request/limit optimization
    - Update mode: Auto vs Recreate vs Initial vs Off
    - Resource policies for critical workloads
- Implement cluster autoscaling:
  - **Cluster Autoscaler**: Add/remove nodes based on pending pods
  - **Node pool configuration**: Min/max node counts per pool
  - **Scale-down policies**: Graceful node draining
  - **Cost optimization**: Mix of spot/preemptible and on-demand nodes

### Step 7: Networking & Service Mesh

- Configure networking:
  - **CNI Plugin**: Choose and configure network plugin
    - Azure CNI: Azure VNET integration
    - AWS VPC CNI: AWS VPC integration
    - Calico: Network policies and performance
    - Cilium: eBPF-based networking and security
  - **Network Policies**: Pod-to-pod traffic rules
  - **Service mesh evaluation**: Istio, Linkerd, Consul
- Implement ingress strategy:
  - **Ingress Controller**: NGINX, Traefik, Kong, Contour
  - **TLS termination**: Cert-manager for automatic certificate management
  - **Rate limiting**: Protect backend services
  - **Path-based routing**: Multiple services behind single domain
  - **Sticky sessions**: Session affinity when needed
- Service mesh implementation (if needed):
  - **Traffic management**: Canary deployments, A/B testing, circuit breaking
  - **Observability**: Distributed tracing, metrics, service graph
  - **Security**: mTLS between services, authorization policies
  - **Resilience**: Retries, timeouts, fault injection

### Step 8: Security Hardening

- Implement RBAC (Role-Based Access Control):
  - **Roles and ClusterRoles**: Define permissions
  - **RoleBindings and ClusterRoleBindings**: Assign to users/groups
  - **ServiceAccounts**: Pod identity and permissions
  - **Principle of least privilege**: Minimal permissions required
- Configure pod security:
  - **Pod Security Standards**: Privileged, Baseline, Restricted
  - **SecurityContext**: runAsNonRoot, readOnlyRootFilesystem, capabilities
  - **AppArmor/SELinux**: Mandatory access control
  - **Seccomp profiles**: Syscall filtering
- Implement network security:
  - **Network Policies**: Default deny, allow specific traffic
  - **Private cluster**: No public API endpoint
  - **Authorized networks**: IP whitelisting for API access
- Secrets management:
  - **Kubernetes Secrets**: Base64 encoded (not encrypted by default)
  - **External Secrets Operator**: Sync from Azure Key Vault, AWS Secrets Manager
  - **Sealed Secrets**: Encrypted secrets in Git
  - **Secret rotation**: Automated credential updates
- Image security:
  - **Private container registry**: ACR, ECR, GCR, Harbor
  - **Image scanning**: Trivy, Anchore, Snyk for vulnerabilities
  - **Image signing**: Cosign, Notary for supply chain security
  - **Admission controllers**: OPA Gatekeeper, Kyverno for policy enforcement

### Step 9: Observability & Monitoring

- Implement logging:
  - **Container logs**: stdout/stderr collection
  - **Log aggregation**: Fluentd, Fluent Bit, Promtail
  - **Log storage**: Elasticsearch, Loki, Azure Log Analytics, CloudWatch
  - **Structured logging**: JSON format for parsing
- Implement metrics:
  - **Prometheus**: Metrics collection and storage
  - **Metrics-server**: Resource metrics for HPA
  - **Custom metrics**: Application-specific metrics via Prometheus exporter
  - **Grafana**: Visualization dashboards
  - **Pre-built dashboards**: Cluster health, node utilization, pod metrics
- Implement distributed tracing:
  - **Jaeger or Tempo**: Trace collection and storage
  - **OpenTelemetry**: Instrumentation standard
  - **Service dependency graph**: Visualize service interactions
- Implement alerting:
  - **Prometheus Alertmanager**: Alert routing and deduplication
  - **Alert rules**: CPU/memory threshold, pod restarts, deployment failures
  - **Notification channels**: Slack, PagerDuty, email, webhook
  - **Runbook automation**: Link alerts to troubleshooting docs

### Step 10: Custom Operators (if needed)

- Evaluate operator need:
  - **Stateful applications**: Databases, message queues, caches
  - **Complex lifecycle**: Backup, restore, upgrade automation
  - **Multi-resource coordination**: Related Kubernetes resources
- Operator implementation:
  - **Operator Framework**: Operator SDK, Kubebuilder
  - **Custom Resource Definitions (CRDs)**: Define custom resources
  - **Controller logic**: Reconciliation loop
  - **Idempotency**: Safe to run multiple times
  - **Finalizers**: Cleanup on resource deletion
- Operator deployment:
  - **Operator Lifecycle Manager (OLM)**: Operator installation and updates
  - **OperatorHub**: Discover pre-built operators
  - **Helm chart**: Package operator for deployment
  - **RBAC**: Operator service account permissions

### Step 11: Package Management & GitOps

- Implement Helm charts:
  - **Chart structure**: templates/, values.yaml, Chart.yaml
  - **Templating**: Parameterize configurations
  - **Dependencies**: Manage chart dependencies
  - **Versioning**: Semantic versioning for charts
  - **Repository**: Helm chart repository (ChartMuseum, Artifact Hub)
- Implement Kustomize overlays:
  - **Base manifests**: Common configuration
  - **Overlays**: Environment-specific customization (dev, staging, prod)
  - **Patches**: JSON/YAML patches for modifications
  - **ConfigMap/Secret generators**: Generate from files
- Implement GitOps:
  - **Git as source of truth**: All manifests in version control
  - **Argo CD or Flux**: Continuous deployment to cluster
  - **Automated sync**: Git commit triggers deployment
  - **Drift detection**: Alert on manual cluster changes
  - **Rollback**: Git revert for deployment rollback

### Step 12: Generate Output

- Save Kubernetes documentation to `/claudedocs/kubernetes-specialist_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Use template from `templates/k8s_architecture_template.md` if available
- Include:
  - Cluster architecture diagram
  - Complete Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets, Ingress)
  - Helm charts or Kustomize overlays
  - Autoscaling configurations (HPA, VPA, Cluster Autoscaler)
  - RBAC policies and security configurations
  - Monitoring and alerting setup
  - Custom operators (if applicable)
  - Troubleshooting guide and runbooks
  - Disaster recovery and backup procedures
  - Next steps and optimization recommendations

### Step 13: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="kubernetes-specialist"`.

**Store learned insights:**
```
memoryStore.updateSkillMemory("kubernetes-specialist", "{project-name}", {
  cluster_patterns: [...],
  deployment_strategies: [...],
  autoscaling_configs: [...],
  security_policies: [...],
  lessons_learned: [...]
})
```

**Update memory with:**
- Cluster architecture decisions and rationale
- Deployment patterns and strategies
- Autoscaling configurations and effectiveness
- Networking and service mesh choices
- Security policies and RBAC configurations
- Performance metrics and resource utilization
- Incident history and troubleshooting learnings
- Operator implementations and learnings

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Cluster architecture designed with HA and scaling (Step 4)
- [ ] Deployment strategy defined with health checks (Step 5)
- [ ] Autoscaling configured (HPA, VPA, Cluster Autoscaler) (Step 6)
- [ ] Networking and ingress configured (Step 7)
- [ ] Security hardening implemented (RBAC, Pod Security, Network Policies) (Step 8)
- [ ] Observability stack configured (Logging, Metrics, Tracing, Alerting) (Step 9)
- [ ] Custom operators implemented if needed (Step 10)
- [ ] GitOps and package management configured (Step 11)
- [ ] Output saved with standard naming convention (Step 12)
- [ ] Standard Memory Update pattern followed (Step 13)

## Kubernetes Expertise Areas

### 1. Cluster Management
- Multi-tenant clusters with namespace isolation
- Cluster upgrades and maintenance windows
- Node pool management (system, user, GPU)
- Cluster backup and disaster recovery (Velero)
- Multi-cluster management (Rancher, Anthos, Azure Arc)

### 2. Workload Deployment
- Deployment strategies (rolling, blue/green, canary)
- StatefulSets for stateful applications
- DaemonSets for node-level services
- Jobs and CronJobs for batch processing
- Init containers and sidecar patterns

### 3. Networking
- Service types (ClusterIP, NodePort, LoadBalancer, ExternalName)
- Ingress controllers and routing rules
- Network policies for pod-to-pod communication
- Service mesh (Istio, Linkerd, Consul)
- DNS and service discovery

### 4. Storage
- Persistent Volumes and Persistent Volume Claims
- StorageClasses for dynamic provisioning
- Volume snapshots and cloning
- CSI drivers for cloud storage
- StatefulSet volume management

### 5. Autoscaling
- Horizontal Pod Autoscaler (HPA) - pod count
- Vertical Pod Autoscaler (VPA) - resource requests
- Cluster Autoscaler - node count
- KEDA - event-driven autoscaling
- Predictive autoscaling with custom metrics

### 6. Security
- RBAC for access control
- Pod Security Standards (Privileged, Baseline, Restricted)
- Network Policies for traffic control
- Secrets management (External Secrets, Sealed Secrets)
- Image scanning and admission control (OPA, Kyverno)

### 7. Observability
- Prometheus and Grafana for metrics
- ELK/Loki stack for logging
- Jaeger/Tempo for distributed tracing
- Alertmanager for alerting
- Service Level Objectives (SLOs) and SLIs

## Deployment Strategy Comparison

| Strategy | Downtime | Rollback Speed | Resource Overhead | Complexity | Best For |
|----------|----------|----------------|-------------------|------------|----------|
| **Rolling Update** | Zero | Fast (revert) | Low (gradual) | Low | Most applications |
| **Blue/Green** | Zero | Instant (switch) | High (2x resources) | Medium | Critical apps |
| **Canary** | Zero | Fast (instant) | Medium (extra pods) | High | Risk mitigation |
| **Recreate** | Yes | Fast (redeploy) | None | Very Low | Dev/test only |

## Ingress Controller Comparison

| Controller | Features | Performance | TLS | Complexity | Best For |
|------------|----------|-------------|-----|------------|----------|
| **NGINX** | Mature, feature-rich | Excellent | cert-manager | Medium | General purpose |
| **Traefik** | Dynamic config, middleware | Very Good | Built-in LE | Low | Modern apps |
| **Kong** | API gateway, plugins | Excellent | Advanced | High | API-heavy |
| **Istio Gateway** | Service mesh integration | Good | Advanced | Very High | Service mesh |
| **Contour** | Envoy-based, simple | Excellent | cert-manager | Low | Simplicity |

## Service Mesh Comparison

| Feature | Istio | Linkerd | Consul | Best Choice |
|---------|-------|---------|--------|-------------|
| **Complexity** | High | Low | Medium | Linkerd (simplicity) |
| **Performance** | Good | Excellent | Good | Linkerd (lowest overhead) |
| **Features** | Most complete | Essential only | Good | Istio (feature-rich) |
| **Observability** | Excellent | Excellent | Good | Istio/Linkerd (tie) |
| **Multi-cluster** | Excellent | Good | Excellent | Istio/Consul |
| **Learning Curve** | Steep | Gentle | Moderate | Linkerd (easiest) |
| **Resource Usage** | High | Low | Medium | Linkerd (lightest) |

## Managed Kubernetes Service Comparison

| Feature | AKS (Azure) | EKS (AWS) | GKE (Google) |
|---------|-------------|-----------|--------------|
| **Kubernetes Version** | Latest-1 | Latest-2 | Latest (fastest) |
| **Control Plane Cost** | Free | $0.10/hour | Free |
| **Upgrade Experience** | Good | Manual | Excellent (auto) |
| **Integration** | Azure services | AWS services | GCP services |
| **Networking** | Azure CNI | VPC CNI | GKE CNI |
| **RBAC Integration** | Azure AD | IAM | Google IAM |
| **Monitoring** | Azure Monitor | CloudWatch | Cloud Monitoring |
| **Best For** | Azure workloads | AWS workloads | Best K8s experience |

## Common Kubernetes Patterns

### Pattern 1: Sidecar Container
- **Purpose**: Extend/enhance main container functionality
- **Use Cases**: Log shipping, service mesh proxy, config reload
- **Example**: Envoy proxy alongside application container

### Pattern 2: Init Container
- **Purpose**: Setup tasks before main container starts
- **Use Cases**: Database migrations, config download, wait for dependencies
- **Example**: Wait for database to be ready before starting app

### Pattern 3: Ambassador Container
- **Purpose**: Proxy connections to external services
- **Use Cases**: Database connection pooling, protocol translation
- **Example**: Cloud SQL proxy for secure database access

### Pattern 4: Adapter Container
- **Purpose**: Standardize output from main container
- **Use Cases**: Log format conversion, metrics normalization
- **Example**: Convert app logs to structured JSON for Fluentd

### Pattern 5: Multi-Container Pod
- **Purpose**: Tightly coupled containers sharing resources
- **Use Cases**: Web server + log shipper, app + monitoring agent
- **Example**: NGINX + Fluentd log collector

## Resource Management Best Practices

### 1. Set Resource Requests and Limits
```yaml
resources:
  requests:
    cpu: 100m      # Minimum guaranteed
    memory: 128Mi
  limits:
    cpu: 500m      # Maximum allowed
    memory: 512Mi
```

### 2. Use Quality of Service (QoS) Classes
- **Guaranteed**: requests = limits (highest priority)
- **Burstable**: requests < limits (medium priority)
- **BestEffort**: no requests/limits (lowest priority, evicted first)

### 3. Configure LimitRanges
- Set default requests/limits for namespaces
- Prevent resource hogging
- Enforce organizational standards

### 4. Use ResourceQuotas
- Limit total resources per namespace
- Prevent single team from consuming all resources
- Track usage and billing

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with comprehensive Kubernetes orchestration capabilities |
