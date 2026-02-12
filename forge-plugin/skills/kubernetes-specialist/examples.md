# Kubernetes Specialist Examples

This file contains example scenarios demonstrating how the **kubernetes-specialist** skill designs production-ready Kubernetes clusters and implements deployment strategies.

## Example 1: Production AKS Cluster for Microservices

### Scenario

A SaaS company is deploying 15 microservices to Azure Kubernetes Service (AKS). They need a production-ready cluster with high availability, autoscaling, observability, and strong security.

### Requirements
- **Workload**: 15 Node.js microservices + 3 background workers
- **Scale**: Start with 50K requests/day, grow to 5M requests/day
- **Availability**: 99.9% SLA, multi-zone deployment
- **Security**: RBAC, network policies, private cluster
- **Observability**: Prometheus, Grafana, distributed tracing
- **Cost**: Optimize with autoscaling and spot instances

### Cluster Architecture

**AKS Configuration**:
```yaml
cluster_name: production-aks
region: eastus
kubernetes_version: 1.28.3
network_plugin: azure  # Azure CNI for VNET integration
network_policy: calico  # Network policies for pod isolation
dns_service_ip: 10.0.0.10
service_cidr: 10.0.0.0/16
```

**Node Pools**:
```yaml
node_pools:
  # System node pool (for system pods like CoreDNS, metrics-server)
  - name: system
    vm_size: Standard_D2s_v3
    node_count: 3
    min_count: 3
    max_count: 5
    enable_auto_scaling: true
    mode: System
    availability_zones: [1, 2, 3]
    node_taints: ["CriticalAddonsOnly=true:NoSchedule"]
    
  # User node pool (for application workloads)
  - name: user
    vm_size: Standard_D4s_v3
    node_count: 3
    min_count: 3
    max_count: 20
    enable_auto_scaling: true
    mode: User
    availability_zones: [1, 2, 3]
    
  # Spot node pool (for cost optimization)
  - name: spot
    vm_size: Standard_D4s_v3
    node_count: 0
    min_count: 0
    max_count: 10
    enable_auto_scaling: true
    priority: Spot
    eviction_policy: Delete
    spot_max_price: -1  # Pay up to on-demand price
    node_taints: ["kubernetes.azure.com/scalesetpriority=spot:NoSchedule"]
```

### Microservice Deployment Example

**Deployment Manifest** (`user-service.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: production
  labels:
    app: user-service
    version: v1.2.3
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero downtime
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        version: v1.2.3
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: user-service
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: user-service
        image: myacr.azurecr.io/user-service:v1.2.3
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_HOST
          valueFrom:
            configMapKeyRef:
              name: user-service-config
              key: database_host
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: user-service-secrets
              key: database_password
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - user-service
              topologyKey: topology.kubernetes.io/zone
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: production
  labels:
    app: user-service
spec:
  type: ClusterIP
  selector:
    app: user-service
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  sessionAffinity: None
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Percent
        value: 50  # Scale down max 50% at a time
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0  # Scale up immediately
      policies:
      - type: Percent
        value: 100  # Double pods if needed
        periodSeconds: 15
      - type: Pods
        value: 4  # Or add 4 pods, whichever is less
        periodSeconds: 15
      selectPolicy: Max
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: user-service
  namespace: production
spec:
  minAvailable: 2  # Always keep at least 2 pods running
  selector:
    matchLabels:
      app: user-service
```

### Ingress Configuration

**NGINX Ingress with TLS**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls-cert
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: user-service
            port:
              number: 80
      - path: /orders
        pathType: Prefix
        backend:
          service:
            name: order-service
            port:
              number: 80
      - path: /payments
        pathType: Prefix
        backend:
          service:
            name: payment-service
            port:
              number: 80
```

### Security Configuration

**RBAC**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: user-service
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: user-service
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: user-service
  namespace: production
subjects:
- kind: ServiceAccount
  name: user-service
  namespace: production
roleRef:
  kind: Role
  name: user-service
  apiGroup: rbac.authorization.k8s.io
```

**Network Policy**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: user-service-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: user-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow traffic from ingress controller
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  # Allow traffic from other microservices
  - from:
    - podSelector:
        matchLabels:
          tier: backend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  # Allow DNS resolution
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
  # Allow PostgreSQL database access
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  # Allow external HTTPS
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

### Observability Stack

**Prometheus ServiceMonitor**:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: user-service
  namespace: production
  labels:
    app: user-service
spec:
  selector:
    matchLabels:
      app: user-service
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Key Features
- ✅ **High Availability**: 3 nodes across 3 availability zones
- ✅ **Autoscaling**: HPA with CPU, memory, and custom metrics
- ✅ **Zero Downtime**: Rolling updates with `maxUnavailable: 0`
- ✅ **Security**: RBAC, network policies, pod security context
- ✅ **Cost Optimization**: Spot instances for non-critical workloads
- ✅ **Observability**: Prometheus metrics, health checks

---

## Example 2: Stateful Application with Operators

### Scenario

Deploy a production PostgreSQL database on Kubernetes using the CloudNativePG operator. Requires automated backups, point-in-time recovery, connection pooling, and high availability.

### Requirements
- **Database**: PostgreSQL 15 with replication
- **Availability**: Multi-replica with automatic failover
- **Backups**: Daily backups to Azure Blob Storage
- **PITR**: Point-in-time recovery capability
- **Connection Pooling**: PgBouncer for efficient connections
- **Monitoring**: Prometheus metrics for database health

### Operator Installation

**Install CloudNativePG Operator**:
```bash
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.21/releases/cnpg-1.21.0.yaml
```

### PostgreSQL Cluster Configuration

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: postgres-cluster
  namespace: databases
spec:
  instances: 3  # 1 primary + 2 replicas
  
  # PostgreSQL configuration
  postgresql:
    parameters:
      max_connections: "200"
      shared_buffers: "256MB"
      effective_cache_size: "1GB"
      maintenance_work_mem: "64MB"
      checkpoint_completion_target: "0.9"
      wal_buffers: "16MB"
      default_statistics_target: "100"
      random_page_cost: "1.1"
      effective_io_concurrency: "200"
      work_mem: "2621kB"
      min_wal_size: "1GB"
      max_wal_size: "4GB"
  
  # Bootstrap from backup or empty database
  bootstrap:
    initdb:
      database: app_db
      owner: app_user
      secret:
        name: postgres-app-user
  
  # Storage configuration
  storage:
    storageClass: managed-premium-retain
    size: 100Gi
  
  # Backup configuration
  backup:
    barmanObjectStore:
      destinationPath: https://mystorageaccount.blob.core.windows.net/postgres-backups
      azureCredentials:
        storageAccount:
          name: azure-storage-account
          key: accountName
        storageKey:
          name: azure-storage-account
          key: accountKey
      wal:
        compression: gzip
        encryption: AES256
      data:
        compression: gzip
        encryption: AES256
        immediateCheckpoint: true
        jobs: 2
    retentionPolicy: "30d"
  
  # Resource limits
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "2000m"
  
  # High availability configuration
  primaryUpdateStrategy: unsupervised
  primaryUpdateMethod: switchover
  
  # Monitoring
  monitoring:
    enablePodMonitor: true
  
  # Affinity rules - spread replicas across zones
  affinity:
    podAntiAffinityType: required
    topologyKey: topology.kubernetes.io/zone
---
# Scheduled backup
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: postgres-cluster-backup
  namespace: databases
spec:
  schedule: "0 0 2 * * *"  # Daily at 2 AM
  backupOwnerReference: self
  cluster:
    name: postgres-cluster
---
# PgBouncer connection pooler
apiVersion: postgresql.cnpg.io/v1
kind: Pooler
metadata:
  name: postgres-pooler
  namespace: databases
spec:
  cluster:
    name: postgres-cluster
  instances: 3
  type: rw  # Read-write connections
  pgbouncer:
    poolMode: transaction
    parameters:
      max_client_conn: "1000"
      default_pool_size: "25"
      max_db_connections: "100"
      max_user_connections: "100"
  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
    limits:
      cpu: "500m"
      memory: "512Mi"
```

### Application Connection

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  # Connect via PgBouncer pooler
  database_host: postgres-pooler-rw.databases.svc.cluster.local
  database_port: "5432"
  database_name: app_db
---
apiVersion: v1
kind: Secret
metadata:
  name: app-database-credentials
  namespace: production
type: Opaque
stringData:
  username: app_user
  password: <generated-password>
```

### Disaster Recovery Procedure

**Point-in-Time Recovery**:
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: postgres-cluster-restored
  namespace: databases
spec:
  instances: 3
  
  # Restore from backup
  bootstrap:
    recovery:
      source: postgres-cluster
      recoveryTarget:
        targetTime: "2024-02-12 14:30:00.000000+00"
  
  externalClusters:
  - name: postgres-cluster
    barmanObjectStore:
      destinationPath: https://mystorageaccount.blob.core.windows.net/postgres-backups
      azureCredentials:
        storageAccount:
          name: azure-storage-account
          key: accountName
        storageKey:
          name: azure-storage-account
          key: accountKey
```

### Key Features
- ✅ **Automated Backups**: Daily backups to Azure Blob Storage
- ✅ **High Availability**: 3 replicas with automatic failover
- ✅ **Connection Pooling**: PgBouncer for efficient connections
- ✅ **Point-in-Time Recovery**: Restore to any point in time
- ✅ **Monitoring**: Prometheus metrics via ServiceMonitor
- ✅ **Anti-Affinity**: Replicas spread across availability zones

---

## Example 3: Canary Deployment with Flagger

### Scenario

Implement progressive canary deployment for a high-traffic API using Flagger and Istio. Automatically promote or rollback based on metrics (error rate, latency).

### Requirements
- **Progressive Rollout**: 5% → 10% → 25% → 50% → 100%
- **Metrics-Based**: Promote if error rate < 1% and p95 latency < 500ms
- **Automatic Rollback**: Rollback if metrics exceed thresholds
- **Load Testing**: Automated load testing during canary

### Istio Installation

```bash
# Install Istio with default profile
istioctl install --set profile=default -y

# Enable Istio injection for namespace
kubectl label namespace production istio-injection=enabled
```

### Flagger Installation

```bash
# Install Flagger
kubectl apply -k github.com/fluxcd/flagger//kustomize/istio

# Install Prometheus (metrics provider)
kubectl apply -f https://raw.githubusercontent.com/fluxcd/flagger/main/artifacts/prometheus/deployment.yaml
```

### Application Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
        version: stable
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      containers:
      - name: api-service
        image: myacr.azurecr.io/api-service:v1.0.0
        ports:
        - name: http
          containerPort: 8080
        - name: metrics
          containerPort: 9090
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: api-service
  ports:
  - name: http
    port: 80
    targetPort: http
```

### Canary Configuration

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api-service
  namespace: production
spec:
  # Deployment reference
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  
  # Service configuration
  service:
    port: 80
    targetPort: 8080
    portDiscovery: true
  
  # Canary analysis configuration
  analysis:
    # Progressive traffic routing
    interval: 1m
    threshold: 5  # Number of failed checks before rollback
    maxWeight: 50
    stepWeight: 5
    
    # Metrics for promotion decision
    metrics:
    # HTTP request success rate
    - name: request-success-rate
      thresholdRange:
        min: 99  # At least 99% success rate
      interval: 1m
    
    # HTTP request duration P95
    - name: request-duration
      thresholdRange:
        max: 500  # P95 latency must be < 500ms
      interval: 1m
    
    # Custom metric from Prometheus
    - name: error-rate
      templateRef:
        name: error-rate
        namespace: istio-system
      thresholdRange:
        max: 1  # Error rate must be < 1%
      interval: 1m
    
    # Webhooks for additional checks
    webhooks:
    # Load testing during canary
    - name: load-test
      type: pre-rollout
      url: http://flagger-loadtester.production/
      timeout: 15s
      metadata:
        type: bash
        cmd: "hey -z 1m -q 10 -c 2 http://api-service-canary.production/"
    
    # Integration tests
    - name: integration-tests
      type: pre-rollout
      url: http://flagger-loadtester.production/
      timeout: 30s
      metadata:
        type: bash
        cmd: "curl -sf http://api-service-canary.production/health || exit 1"
    
    # Slack notification
    - name: slack-notification
      type: post-rollout
      url: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
      metadata:
        message: "API Service canary deployment"
  
  # Istio traffic routing
  provider: istio
  
  # Istio virtual service
  ingressRef:
    apiVersion: networking.istio.io/v1beta1
    kind: VirtualService
    name: api-service
---
# Prometheus metric template
apiVersion: flagger.app/v1beta1
kind: MetricTemplate
metadata:
  name: error-rate
  namespace: istio-system
spec:
  provider:
    type: prometheus
    address: http://prometheus.istio-system:9090
  query: |
    sum(
      rate(
        istio_requests_total{
          reporter="destination",
          destination_workload_namespace="{{ namespace }}",
          destination_workload=~"{{ target }}",
          response_code=~"5.*"
        }[{{ interval }}]
      )
    )
    /
    sum(
      rate(
        istio_requests_total{
          reporter="destination",
          destination_workload_namespace="{{ namespace }}",
          destination_workload=~"{{ target }}"
        }[{{ interval }}]
      )
    )
    * 100
```

### Canary Deployment Flow

1. **Deploy new version** by updating image tag:
   ```bash
   kubectl -n production set image deployment/api-service \
     api-service=myacr.azurecr.io/api-service:v2.0.0
   ```

2. **Flagger detects change** and creates canary deployment

3. **Progressive traffic shift**:
   - 0% → 5% (1 minute)
   - Check metrics, run load tests
   - 5% → 10% (1 minute)
   - Check metrics
   - 10% → 25% → 50% (incrementally)

4. **Automatic decision**:
   - **Promote**: If all metrics pass → 100% traffic to new version
   - **Rollback**: If any metric fails → revert to stable version

5. **Notification**: Slack alert with deployment result

### Canary Promotion Example

```
# Canary deployment detected
api-service.production - New revision detected! Scaling up api-service.production
api-service.production - Starting canary analysis for api-service.production
api-service.production - Advance api-service.production canary weight 5
api-service.production - Advance api-service.production canary weight 10
api-service.production - Advance api-service.production canary weight 25
api-service.production - Advance api-service.production canary weight 50
api-service.production - Copying api-service.production template spec to api-service-primary.production
api-service.production - Promotion completed! Scaling down api-service.production
```

### Key Features
- ✅ **Progressive Rollout**: 5% → 10% → 25% → 50% → 100% traffic shift
- ✅ **Metrics-Based**: Automated decision based on success rate and latency
- ✅ **Automatic Rollback**: Revert on metric threshold breach
- ✅ **Load Testing**: Automated testing during canary
- ✅ **Integration Tests**: Pre-rollout validation
- ✅ **Notifications**: Slack alerts for deployment status

---

## Example 4: Multi-Cluster GitOps with Argo CD

### Scenario

Manage 3 Kubernetes clusters (dev, staging, production) with GitOps using Argo CD. Applications are deployed from Git, with automatic sync and drift detection.

### Requirements
- **3 Clusters**: dev, staging, production
- **Git as Source of Truth**: All manifests in Git repository
- **Automatic Sync**: Git commit triggers deployment
- **Environment Promotion**: dev → staging → production
- **Drift Detection**: Alert on manual cluster changes

### Repository Structure

```
gitops-repo/
├── apps/
│   ├── user-service/
│   │   ├── base/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       │   ├── kustomization.yaml
│   │       │   └── config.yaml
│   │       ├── staging/
│   │       │   ├── kustomization.yaml
│   │       │   └── config.yaml
│   │       └── production/
│   │           ├── kustomization.yaml
│   │           ├── config.yaml
│   │           └── hpa.yaml
│   └── order-service/
│       └── ...
└── clusters/
    ├── dev/
    │   └── apps/
    │       └── user-service.yaml (Application manifest)
    ├── staging/
    │   └── apps/
    │       └── user-service.yaml
    └── production/
        └── apps/
            └── user-service.yaml
```

### Argo CD Installation

```bash
# Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access Argo CD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Application Configuration

**Dev Cluster Application**:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service-dev
  namespace: argocd
spec:
  project: default
  
  # Source repository
  source:
    repoURL: https://github.com/myorg/gitops-repo.git
    targetRevision: HEAD
    path: apps/user-service/overlays/dev
  
  # Destination cluster
  destination:
    server: https://kubernetes.default.svc
    namespace: development
  
  # Sync policy
  syncPolicy:
    automated:
      prune: true     # Delete resources not in Git
      selfHeal: true  # Revert manual changes
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  # Health assessment
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas  # Ignore HPA-managed replicas
```

**Production Cluster Application** (with manual sync):
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service-production
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/myorg/gitops-repo.git
    targetRevision: v1.2.3  # Pin to specific version/tag
    path: apps/user-service/overlays/production
  
  destination:
    server: https://production-cluster-api.example.com
    namespace: production
  
  syncPolicy:
    # Manual sync for production (no automated)
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    retry:
      limit: 3
```

### Kustomize Overlay Example

**Base Deployment** (`apps/user-service/base/deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 1  # Override per environment
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: myacr.azurecr.io/user-service:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

**Production Overlay** (`apps/user-service/overlays/production/kustomization.yaml`):
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

bases:
- ../../base

# Override image tag for production
images:
- name: myacr.azurecr.io/user-service
  newTag: v1.2.3

# Patch replicas for production
patches:
- target:
    kind: Deployment
    name: user-service
  patch: |-
    - op: replace
      path: /spec/replicas
      value: 5

# Add production-specific resources
resources:
- hpa.yaml
- pdb.yaml

# Production config
configMapGenerator:
- name: user-service-config
  literals:
  - ENV=production
  - LOG_LEVEL=info
  - DATABASE_HOST=postgres-prod.example.com
```

### Multi-Cluster Management

**ApplicationSet for Multi-Cluster**:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: user-service
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - cluster: dev
        url: https://kubernetes.default.svc
        targetRevision: HEAD
        replicas: "2"
      - cluster: staging
        url: https://staging-cluster-api.example.com
        targetRevision: release-branch
        replicas: "3"
      - cluster: production
        url: https://production-cluster-api.example.com
        targetRevision: v1.2.3
        replicas: "5"
  
  template:
    metadata:
      name: 'user-service-{{cluster}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/gitops-repo.git
        targetRevision: '{{targetRevision}}'
        path: 'apps/user-service/overlays/{{cluster}}'
      destination:
        server: '{{url}}'
        namespace: '{{cluster}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### Notifications Configuration

**Slack Notifications**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  
  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded']
      send: [app-deployed]
  
  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      send: [app-health-degraded]
  
  trigger.on-sync-failed: |
    - when: app.status.operationState.phase in ['Error', 'Failed']
      send: [app-sync-failed]
  
  template.app-deployed: |
    message: |
      Application {{.app.metadata.name}} has been deployed to {{.app.spec.destination.namespace}}
    slack:
      attachments: |
        [{
          "title": "{{ .app.metadata.name}}",
          "title_link":"{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
          "color": "#18be52",
          "fields": [
          {
            "title": "Sync Status",
            "value": "{{.app.status.sync.status}}",
            "short": true
          },
          {
            "title": "Repository",
            "value": "{{.app.spec.source.repoURL}}",
            "short": true
          }
          ]
        }]
```

### Deployment Workflow

1. **Developer commits** to `main` branch
2. **Argo CD detects** Git change in dev cluster
3. **Auto-sync** deploys to dev cluster
4. **Automated tests** run in dev
5. **Manual approval** to merge to `release-branch`
6. **Auto-sync** deploys to staging cluster
7. **QA validation** in staging
8. **Tag release** as `v1.2.3`
9. **Manual sync** to production cluster (requires approval)
10. **Slack notification** confirms deployment

### Key Features
- ✅ **GitOps**: Git as single source of truth
- ✅ **Multi-Cluster**: Manage dev, staging, production
- ✅ **Automatic Sync**: Git commit triggers deployment
- ✅ **Drift Detection**: Auto-heal manual changes
- ✅ **Environment Promotion**: Progressive deployment pipeline
- ✅ **Notifications**: Slack alerts for deployment events

---

## Common Kubernetes Troubleshooting

### Issue 1: Pods in CrashLoopBackOff
```bash
# Check pod logs
kubectl logs <pod-name> --previous

# Describe pod for events
kubectl describe pod <pod-name>

# Common causes:
# - Application crashes on startup
# - Missing environment variables
# - Failed liveness/readiness probes
# - Insufficient resources
```

### Issue 2: Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints <service-name>

# Check pod labels match service selector
kubectl get pods --show-labels

# Test service DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup <service-name>

# Common causes:
# - Pod labels don't match service selector
# - Pods not ready (failing readiness probes)
# - NetworkPolicy blocking traffic
```

### Issue 3: High Pod Evictions
```bash
# Check node pressure
kubectl describe node <node-name>

# Check pod resource usage
kubectl top pods

# Common causes:
# - Insufficient memory (OOMKilled)
# - Disk pressure
# - Node out of ephemeral storage
# - No resource limits set
```

### Issue 4: Slow Cluster Autoscaler
```bash
# Check cluster autoscaler logs
kubectl logs -n kube-system deployment/cluster-autoscaler

# Check pending pods
kubectl get pods --all-namespaces --field-selector=status.phase=Pending

# Common causes:
# - Node pool at max capacity
# - No node pool matches pod requirements
# - PodDisruptionBudget preventing scale down
# - Insufficient cloud quota
```
