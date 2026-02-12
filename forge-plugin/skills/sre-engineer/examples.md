# SRE Engineer Examples

This file contains example scenarios demonstrating how the **sre-engineer** skill implements Site Reliability Engineering practices, SLO definitions, incident response, and observability.

## Example 1: SLO Definition and Error Budget Tracking for E-commerce API

### Scenario

An e-commerce platform has a critical product catalog API serving 50M requests/day. The team needs to define SLOs, implement error budget tracking, and create dashboards to monitor reliability.

### Requirements
- Define SLIs and SLOs aligned with user experience
- Calculate error budgets for each SLO
- Implement multi-burn-rate alerting
- Create reliability dashboard
- Establish error budget policy

### SLO Definitions

#### SLI 1: Availability (Success Rate)

**Definition**: Percentage of HTTP requests that return 2xx or 3xx status codes (excluding 429 rate limits)

**Measurement**:
```promql
# Success rate over 30 days
sum(rate(http_requests_total{status=~"2..|3..", job="product-api"}[30d]))
/
sum(rate(http_requests_total{job="product-api"}[30d]))
```

**SLO Target**: 99.9% of requests succeed over rolling 30 days

**Error Budget**:
- Total requests/month: 1.5 billion
- Allowed failures: 1.5 million requests (0.1%)
- Equivalent downtime: 43.2 minutes/month

**Multi-Burn-Rate Alerts**:

```yaml
# Fast burn - 2% budget consumed in 1 hour
- alert: HighErrorBudgetBurn_1h
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status=~"2..|3..", job="product-api"}[1h]))
        /
        sum(rate(http_requests_total{job="product-api"}[1h]))
      )
    ) > (14.4 * 0.001)  # 14.4x burn rate = 2% in 1 hour
  for: 5m
  labels:
    severity: critical
    team: product-api
  annotations:
    summary: "Product API burning error budget 14x faster than expected"
    description: "{{ $value | humanizePercentage }} error rate in last hour"
    runbook_url: "https://runbooks.example.com/product-api/high-error-rate"

# Slow burn - 5% budget consumed in 6 hours  
- alert: ModerateErrorBudgetBurn_6h
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status=~"2..|3..", job="product-api"}[6h]))
        /
        sum(rate(http_requests_total{job="product-api"}[6h]))
      )
    ) > (3 * 0.001)  # 3x burn rate = 5% in 6 hours
  for: 30m
  labels:
    severity: warning
    team: product-api
  annotations:
    summary: "Product API burning error budget faster than sustainable"
    description: "{{ $value | humanizePercentage }} error rate in last 6 hours"
    runbook_url: "https://runbooks.example.com/product-api/elevated-error-rate"
```

#### SLI 2: Latency (Response Time)

**Definition**: Time from request received to response sent, measured at the load balancer

**Measurement**:
```promql
# p95 latency over 30 days
histogram_quantile(0.95, 
  sum(rate(http_request_duration_seconds_bucket{job="product-api"}[30d])) by (le)
)
```

**SLO Target**: 95% of requests complete in < 500ms over rolling 30 days

**Error Budget**:
- Total requests/month: 1.5 billion
- Allowed slow requests: 75 million (5%)

**Alert**:
```yaml
- alert: HighLatency_p95
  expr: |
    histogram_quantile(0.95,
      sum(rate(http_request_duration_seconds_bucket{job="product-api"}[5m])) by (le)
    ) > 0.5
  for: 10m
  labels:
    severity: warning
    team: product-api
  annotations:
    summary: "Product API p95 latency above SLO threshold"
    description: "p95 latency is {{ $value }}s (threshold: 0.5s)"
    runbook_url: "https://runbooks.example.com/product-api/high-latency"
```

### Error Budget Dashboard (Grafana)

```json
{
  "dashboard": {
    "title": "Product API - SLO and Error Budget",
    "panels": [
      {
        "title": "Availability SLO (99.9%)",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"2..|3..\", job=\"product-api\"}[30d])) / sum(rate(http_requests_total{job=\"product-api\"}[30d]))",
            "legendFormat": "Current SLO"
          }
        ],
        "thresholds": [
          {"value": 0.999, "color": "green"},
          {"value": 0.995, "color": "yellow"},
          {"value": 0, "color": "red"}
        ]
      },
      {
        "title": "Error Budget Remaining (30 days)",
        "targets": [
          {
            "expr": "1 - (sum(increase(http_requests_total{status=~\"5..|4..\", job=\"product-api\"}[30d])) / (0.001 * sum(increase(http_requests_total{job=\"product-api\"}[30d]))))",
            "legendFormat": "Budget Remaining"
          }
        ],
        "thresholds": [
          {"value": 0.5, "color": "green"},
          {"value": 0.1, "color": "yellow"},
          {"value": 0, "color": "red"}
        ]
      },
      {
        "title": "Error Budget Burn Rate",
        "targets": [
          {
            "expr": "(1 - (sum(rate(http_requests_total{status=~\"2..|3..\", job=\"product-api\"}[1h])) / sum(rate(http_requests_total{job=\"product-api\"}[1h])))) / 0.001",
            "legendFormat": "1h burn rate (target: 1x)"
          }
        ]
      },
      {
        "title": "Latency SLO (p95 < 500ms)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job=\"product-api\"}[5m])) by (le))",
            "legendFormat": "p95 latency"
          }
        ],
        "thresholds": [
          {"value": 0.5, "color": "red"}
        ]
      }
    ]
  }
}
```

### Error Budget Policy

**Healthy Budget (> 50% remaining):**
- ✅ Approve all planned releases
- ✅ Allow experimental features and A/B tests
- ✅ Schedule chaos engineering experiments
- ✅ Optimize for velocity

**Low Budget (10-50% remaining):**
- ⚠️ Increase change review scrutiny
- ⚠️ Require load testing for major changes
- ⚠️ Defer low-priority features
- ⚠️ Balance velocity with reliability

**Exhausted Budget (< 10% remaining):**
- 🛑 **Feature freeze**: Only critical bug fixes
- 🛑 All hands on reliability improvements
- 🛑 Daily error budget review meetings
- 🛑 Conduct reliability retrospective
- 🛑 Create recovery plan with timeline

### Key Outcomes
- ✅ **Clear SLOs** based on user experience (not arbitrary thresholds)
- ✅ **Quantified risk** via error budgets (43.2 min downtime allowed)
- ✅ **Early detection** via multi-burn-rate alerts (catch issues in 5 min vs hours)
- ✅ **Informed decisions** via error budget policy (when to slow down vs speed up)
- ✅ **Visibility** via dashboards showing real-time reliability status

---

## Example 2: Incident Response Runbook - Database Connection Pool Exhaustion

### Scenario

The product API frequently experiences database connection pool exhaustion during traffic spikes. Need a detailed runbook for on-call engineers to diagnose and mitigate quickly.

### Runbook: Database Connection Pool Exhaustion

#### 🔴 Severity: SEV2 - High

**Symptoms:**
- Spike in API 500 errors with "connection pool exhausted" in logs
- Increased API latency (p95 > 2s, normally < 500ms)
- Database CPU normal but connection count at max
- Alert: `DatabaseConnectionPoolSaturated`

**Impact:**
- User-facing errors on product listing, search, checkout
- Estimated revenue impact: $1000/minute of full outage
- SLO impact: Burns ~2% of monthly error budget per hour

---

#### Step 1: Immediate Mitigation (5 minutes)

**Goal**: Stop the bleeding, restore service

**Actions:**

1. **Increase connection pool size** (temporary relief):
   ```bash
   # Connect to app servers via kubectl
   kubectl exec -it deployment/product-api -n production -- /bin/bash
   
   # Update connection pool config (requires app restart)
   # Edit config/database.yml
   # Change: pool: 10 → pool: 20
   
   # Rollout restart to apply
   kubectl rollout restart deployment/product-api -n production
   
   # Monitor restart progress
   kubectl rollout status deployment/product-api -n production
   ```

2. **Scale out application** (more connections distributed):
   ```bash
   # Increase replicas from 5 to 10
   kubectl scale deployment/product-api --replicas=10 -n production
   
   # Watch pods come online
   kubectl get pods -n production -l app=product-api -w
   ```

3. **Verify recovery**:
   ```bash
   # Check error rate dropping
   curl -s "http://prometheus/api/v1/query?query=rate(http_requests_total{status=~\"5..\",job=\"product-api\"}[5m])"
   
   # Check connection pool usage
   kubectl logs -n production -l app=product-api --tail=50 | grep "pool_usage"
   ```

**Expected outcome**: Error rate drops to < 0.1%, latency returns to < 500ms within 5 minutes

**If mitigation fails**: Escalate to database team, consider read-replica failover

---

#### Step 2: Investigation (15 minutes)

**Goal**: Understand root cause

**Check 1: Query Performance**
```bash
# Check for slow queries
kubectl exec -it postgres-primary -n production -- psql -U app -d productdb

SELECT pid, query_start, state, query 
FROM pg_stat_activity 
WHERE state != 'idle' AND query_start < now() - interval '5 seconds'
ORDER BY query_start;

# Check for lock contention
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query,
       blocking_activity.query AS blocking_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

**Check 2: Connection Leak**
```bash
# Application-side: Check for connection leaks
kubectl logs -n production -l app=product-api --tail=1000 | grep -i "connection" | grep -E "(timeout|leak|not returned)"

# Database-side: Check connection states
kubectl exec -it postgres-primary -n production -- psql -U app -d productdb -c "SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"
```

**Check 3: Traffic Spike**
```bash
# Check if traffic spike caused the issue
curl -s "http://prometheus/api/v1/query?query=rate(http_requests_total{job=\"product-api\"}[1h])"

# Compare to normal baseline (should be ~20k req/sec)
```

**Common Root Causes:**
- ✅ **Long-running queries**: Inventory sync query taking 30s+ (normally 2s)
- ✅ **Connection leak**: Code not closing connections in error paths
- ✅ **Traffic spike**: Black Friday traffic 10x normal load
- ✅ **Database slowdown**: Disk I/O saturation on primary

---

#### Step 3: Permanent Fix (varies by root cause)

**If root cause: Long-running query**
```sql
-- Add index to slow query
CREATE INDEX CONCURRENTLY idx_products_category_updated 
ON products(category_id, updated_at) 
WHERE deleted_at IS NULL;

-- Verify query plan improved
EXPLAIN ANALYZE SELECT * FROM products WHERE category_id = 123 ORDER BY updated_at DESC LIMIT 50;
```

**If root cause: Connection leak**
```python
# Code fix: Ensure connections always released
# BAD (leaks on exception)
def get_products():
    conn = db.get_connection()
    products = conn.execute("SELECT * FROM products")
    conn.close()  # Never reached if exception above
    return products

# GOOD (connection released even on exception)
def get_products():
    with db.get_connection() as conn:  # Context manager ensures cleanup
        products = conn.execute("SELECT * FROM products")
        return products
```

**If root cause: Traffic spike**
```bash
# Increase default connection pool permanently
# Edit Kubernetes ConfigMap
kubectl edit configmap product-api-config -n production

# Change:
# DB_POOL_SIZE: "10" → "25"
# DB_POOL_TIMEOUT: "5000" → "10000"

# Rollout to apply
kubectl rollout restart deployment/product-api -n production
```

---

#### Step 4: Postmortem and Prevention

**Schedule postmortem** (within 48 hours):
- Document timeline from detection to resolution
- Identify root cause with 5 Whys analysis
- List action items to prevent recurrence

**Immediate action items**:
1. Add alert for connection pool usage > 80% (proactive warning)
2. Add database query performance monitoring
3. Review all database access code for connection leaks
4. Implement automatic scaling based on traffic (HPA)
5. Add circuit breaker to fail fast when pool saturated

**Monitoring improvements**:
```yaml
# New proactive alert
- alert: DatabaseConnectionPoolHighUsage
  expr: |
    (db_connection_pool_active / db_connection_pool_max) > 0.8
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Connection pool usage above 80%"
    description: "Pool at {{ $value | humanizePercentage }} capacity"
    action: "Investigate slow queries or scale application"
```

---

#### Communication Template

**Initial notification** (Slack #incidents):
```
🔴 SEV2 Incident - Product API Database Connections Exhausted

IMPACT: 500 errors on product pages, ~30% of requests failing
STARTED: 2026-02-12 14:32 UTC
STATUS: Investigating
INCIDENT COMMANDER: @jane-smith
BRIDGE: https://zoom.us/incident-bridge

Updates every 15 minutes or on status change.
```

**Resolution notification**:
```
✅ SEV2 Incident RESOLVED - Product API Database Connections

RESOLUTION: Scaled app replicas 5→10, increased pool size 10→20
DURATION: 23 minutes (14:32 - 14:55 UTC)
SLO IMPACT: 0.8% of monthly error budget consumed
POSTMORTEM: To be completed by 2026-02-14

Root cause: Traffic spike (3x normal) + long-running inventory query
Next steps: Add connection pool alerting, optimize slow query
```

### Key Features
- ✅ **Time-bound steps**: Each section has time goal
- ✅ **Copy-paste commands**: Exact commands to run (no guessing)
- ✅ **Decision trees**: Clear escalation path if mitigation fails
- ✅ **Root cause checklist**: Common causes to investigate
- ✅ **Prevention focus**: Action items to prevent recurrence
- ✅ **Communication templates**: Consistent stakeholder updates

---

## Example 3: Blameless Postmortem - Payment Processing Outage

### Incident Overview

**Date**: 2026-02-05  
**Duration**: 47 minutes (13:14 - 14:01 UTC)  
**Severity**: SEV1 - Critical  
**Incident Commander**: Sarah Chen  
**Services Affected**: Payment processing, checkout  
**Impact**: $127,000 revenue loss, 12,450 failed transactions  

---

### Executive Summary

On February 5th, 2026, the payment processing service experienced a 47-minute outage affecting all customer checkouts. The root cause was a database schema migration that introduced a slow query, exhausting the connection pool and cascading to API failures. The incident was detected by automated alerts 2 minutes after onset. Mitigation involved rolling back the migration and scaling database resources. No customer data was compromised. We have identified 8 action items to prevent similar incidents.

---

### Timeline (All times UTC)

| Time | Event |
|------|-------|
| **13:14** | 🟢 Payment service v2.5.0 deployment begins (includes schema migration) |
| **13:16** | 🔴 Alert fires: `PaymentAPIErrorRateHigh` (error rate 45%) |
| **13:17** | 🟠 On-call engineer Jane Doe acknowledges alert, joins incident bridge |
| **13:18** | 🔴 Alert fires: `PaymentAPILatencyHigh` (p95 latency 12 seconds) |
| **13:20** | 🟠 Incident escalated to SEV1, Sarah Chen takes Incident Commander role |
| **13:21** | 🟠 Customer support reports flood of checkout failures (~200 tickets/min) |
| **13:22** | 🟠 Engineering investigates: Database connection pool at 100% usage |
| **13:25** | 🟠 Status page updated: "Payment processing degraded" |
| **13:28** | 🟠 Root cause identified: Migration added non-indexed column to query |
| **13:30** | 🟠 Decision: Rollback v2.5.0 deployment to v2.4.3 |
| **13:32** | 🟢 Rollback initiated via `kubectl rollout undo` |
| **13:35** | 🟢 Rollback complete, but database schema still migrated |
| **13:37** | 🔴 Error rate still high (40%) - schema migration cannot be auto-reverted |
| **13:40** | 🟠 Decision: Manual schema rollback by DBA team |
| **13:42** | 🟠 DBA connects to database, identifies problematic query |
| **13:45** | 🟢 Temporary fix: Add index on new column `payment_metadata` |
| **13:47** | ```sql
CREATE INDEX CONCURRENTLY idx_payments_metadata 
ON payments(payment_metadata);
``` |
| **13:50** | 🟢 Query performance improved: 12s → 150ms |
| **13:52** | 🟢 Connection pool usage drops to 40% |
| **13:55** | 🟢 Error rate drops below 1% |
| **14:01** | ✅ Incident resolved, all services nominal |
| **14:05** | 🟢 Status page updated: "All systems operational" |
| **14:30** | 🟢 Customer support backlog cleared |

---

### Root Cause Analysis (5 Whys)

**Problem Statement**: Payment API error rate spiked to 45% causing checkout failures.

1. **Why did payment API return errors?**  
   → Database connection pool was exhausted (100% utilization)

2. **Why was the connection pool exhausted?**  
   → Queries were taking 12 seconds instead of normal 150ms, holding connections

3. **Why were queries slow?**  
   → New column `payment_metadata` was queried without an index

4. **Why was the column unindexed?**  
   → Migration script created the column but forgot to add index

5. **Why did the migration not include the index?**  
   → No automated performance testing in staging caught the slow query

**Root Cause**: Schema migration added unindexed column to frequently queried table, causing 80x query slowdown.

**Contributing Factors**:
- No query performance testing in CI/CD pipeline
- Migration rollback procedure not documented
- Staging environment had 1/100th production data volume (query fast in staging)
- No alerting on database query performance degradation

---

### What Went Well ✅

1. **Fast detection**: Automated SLO alerts fired within 2 minutes
2. **Clear escalation**: SEV1 declared quickly, IC assigned immediately
3. **Good communication**: Status page updated within 11 minutes
4. **Effective debugging**: Root cause identified in 14 minutes
5. **Team collaboration**: DBA team responded within 10 minutes of page
6. **Documentation**: Incident timeline captured in real-time by scribe

---

### What Went Wrong ❌

1. **Schema migration risk**: No performance testing before production deployment
2. **Staging limitations**: Staging data volume too small to catch performance issues
3. **Missing index**: Developer oversight, no review checklist for migrations
4. **Difficult rollback**: Schema migrations cannot be auto-reverted with app rollback
5. **Alert gaps**: No proactive alert on query performance degradation
6. **Monitoring blind spot**: Connection pool saturation only detected via errors

---

### Impact Assessment

**Technical Impact**:
- 47 minutes of payment processing downtime
- 12,450 failed payment transactions
- 2.1% of monthly error budget consumed

**Business Impact**:
- $127,000 in lost revenue (transactions abandoned)
- 2,347 support tickets created
- Customer trust impact (difficult to quantify)

**SLO Impact**:
- Payment API availability SLO: 99.9% target
- Actual: 99.891% for the month (after incident)
- Error budget: 21% consumed by this single incident

---

### Action Items

| # | Action | Owner | Due Date | Priority |
|---|--------|-------|----------|----------|
| 1 | Add query performance testing to CI/CD (assert p95 < 500ms) | Jane Doe | 2026-02-15 | P0 |
| 2 | Create migration checklist (includes index planning) | Sarah Chen | 2026-02-12 | P0 |
| 3 | Document schema migration rollback procedure | DBA Team | 2026-02-18 | P0 |
| 4 | Scale staging database to 10% of prod size (catch perf issues) | DevOps | 2026-02-25 | P1 |
| 5 | Add alert: `DatabaseQueryLatencyHigh` (p95 > 1s) | SRE Team | 2026-02-15 | P0 |
| 6 | Add alert: `ConnectionPoolUsageHigh` (> 80%) | SRE Team | 2026-02-15 | P0 |
| 7 | Implement blue/green schema migrations (zero-downtime) | Engineering | 2026-03-15 | P1 |
| 8 | Create payment service runbook (connection pool exhaustion) | Jane Doe | 2026-02-20 | P1 |

**Follow-up**: Review action items in SRE weekly meeting every Friday until all complete.

---

### Lessons Learned

1. **Test migrations at scale**: Staging must represent production data volume
2. **Query performance = reliability**: Slow queries are availability incidents
3. **Automate testing**: Humans miss things, automated checks catch regressions
4. **Schema changes are risky**: Treat with same caution as code deployments
5. **Observability gaps**: We had no visibility into query performance before failure

---

### Communication Artifacts

**Internal Slack Update** (13:25 UTC):
```
🔴 SEV1 Incident - Payment Processing Down

IMPACT: All checkouts failing, ~200 support tickets/min
STARTED: 13:14 UTC (11 min ago)
STATUS: Root cause identified (database), working on fix
IC: @sarah-chen | BRIDGE: https://zoom.us/incident-123

ETA: 15-20 min to mitigation
Next update: 13:40 UTC or on status change
```

**Customer-Facing Status Page** (13:25 UTC):
```
⚠️ Payment Processing Degraded

We are currently experiencing issues with payment processing. 
Customers may see errors during checkout.

Our team is actively working on a fix. 

Started: 1:14 PM UTC
Updates: Every 15 minutes

We apologize for the inconvenience.
```

**Postmortem Distribution**:
- Engineering team: Full postmortem (this document)
- Executive team: Executive summary + impact + action items
- Customer support: Timeline + customer talking points
- Public blog: High-level summary (optional, for transparency)

### Key Features
- ✅ **Blameless tone**: No individual blame, focus on systems
- ✅ **Detailed timeline**: Minute-by-minute events
- ✅ **5 Whys analysis**: Digs deep to root cause
- ✅ **Balanced reflection**: What went well + what didn't
- ✅ **Actionable items**: Specific, assigned, time-bound
- ✅ **Lessons learned**: Generalizable insights for the future

---

## Example 4: Observability Stack Setup - Three Pillars for Microservices

### Scenario

A company is migrating from a monolith to microservices (15 services). They need a complete observability stack to monitor, debug, and ensure reliability across distributed services.

### Requirements
- **Metrics**: Service health, SLOs, resource usage
- **Logs**: Structured logging with trace correlation
- **Traces**: Distributed request tracing across services
- **Cost-effective**: Open-source preferred
- **Kubernetes-native**: Services run on AKS

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Observability Stack                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Metrics: Prometheus + Grafana                               │
│  Logs: Promtail → Loki                                       │
│  Traces: OpenTelemetry → Tempo                               │
│  Correlation: trace_id links metrics, logs, traces           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

### Component 1: Metrics with Prometheus + Grafana

**Install Prometheus Operator** (Kubernetes-native):

```bash
# Add Prometheus Operator Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install with sensible defaults
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=100Gi \
  --set grafana.adminPassword=<secure-password>
```

**Instrument Application** (Node.js example):

```javascript
// Install: npm install prom-client express-prom-bundle

const express = require('express');
const promBundle = require('express-prom-bundle');

const app = express();

// Automatic metrics collection
const metricsMiddleware = promBundle({
  includeMethod: true,
  includePath: true,
  includeStatusCode: true,
  includeUp: true,
  customLabels: {service: 'product-api'},
  promClient: {
    collectDefaultMetrics: {
      timeout: 5000
    }
  }
});

app.use(metricsMiddleware);

// Custom business metric
const orderCounter = new promClient.Counter({
  name: 'orders_total',
  help: 'Total number of orders processed',
  labelNames: ['status', 'payment_method']
});

app.post('/orders', async (req, res) => {
  try {
    const order = await processOrder(req.body);
    orderCounter.inc({status: 'success', payment_method: order.payment});
    res.json({orderId: order.id});
  } catch (err) {
    orderCounter.inc({status: 'failed', payment_method: 'unknown'});
    res.status(500).json({error: err.message});
  }
});

// Metrics exposed at /metrics (auto-discovered by Prometheus)
app.listen(3000);
```

**ServiceMonitor** (tells Prometheus to scrape service):

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: product-api
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: product-api
  endpoints:
  - port: http
    path: /metrics
    interval: 15s
```

**Grafana Dashboard** (RED method - Rate, Errors, Duration):

```json
{
  "dashboard": {
    "title": "Product API - RED Metrics",
    "panels": [
      {
        "title": "Request Rate (req/sec)",
        "targets": [{
          "expr": "sum(rate(http_request_duration_seconds_count{service='product-api'}[5m]))",
          "legendFormat": "Requests/sec"
        }]
      },
      {
        "title": "Error Rate (%)",
        "targets": [{
          "expr": "sum(rate(http_request_duration_seconds_count{service='product-api',status=~'5..'}[5m])) / sum(rate(http_request_duration_seconds_count{service='product-api'}[5m])) * 100",
          "legendFormat": "Error %"
        }],
        "thresholds": [
          {"value": 1, "color": "red"}
        ]
      },
      {
        "title": "Request Duration (p50, p95, p99)",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{service='product-api'}[5m])) by (le))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service='product-api'}[5m])) by (le))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service='product-api'}[5m])) by (le))",
            "legendFormat": "p99"
          }
        ]
      }
    ]
  }
}
```

---

### Component 2: Logs with Loki + Promtail

**Install Loki Stack**:

```bash
helm install loki grafana/loki-stack \
  --namespace monitoring \
  --set grafana.enabled=false \
  --set loki.persistence.enabled=true \
  --set loki.persistence.size=50Gi \
  --set promtail.enabled=true
```

**Application Structured Logging** (with trace correlation):

```javascript
// Install: npm install winston

const winston = require('winston');
const { v4: uuidv4 } = require('uuid');

// Structured JSON logging
const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

// Middleware to add trace_id to every request
app.use((req, res, next) => {
  req.trace_id = req.headers['x-trace-id'] || uuidv4();
  res.setHeader('x-trace-id', req.trace_id);
  next();
});

// Log with trace correlation
app.post('/orders', async (req, res) => {
  logger.info('Order received', {
    trace_id: req.trace_id,
    user_id: req.body.user_id,
    cart_value: req.body.total,
    service: 'product-api'
  });
  
  try {
    const order = await processOrder(req.body);
    logger.info('Order processed successfully', {
      trace_id: req.trace_id,
      order_id: order.id,
      processing_time_ms: order.duration
    });
    res.json({orderId: order.id});
  } catch (err) {
    logger.error('Order processing failed', {
      trace_id: req.trace_id,
      error: err.message,
      stack: err.stack
    });
    res.status(500).json({error: err.message});
  }
});
```

**Loki Query Examples** (in Grafana Explore):

```logql
# All errors in last hour
{service="product-api"} |= "ERROR"

# Specific trace across all services
{trace_id="abc-123-def"} 

# High-value failed orders
{service="product-api"} | json | cart_value > 1000 and level="error"

# Error rate by service
sum by (service) (rate({level="error"}[5m]))
```

---

### Component 3: Distributed Tracing with OpenTelemetry + Tempo

**Install Tempo**:

```bash
helm install tempo grafana/tempo \
  --namespace monitoring \
  --set tempo.persistence.enabled=true \
  --set tempo.persistence.size=50Gi
```

**Instrument Application with OpenTelemetry**:

```javascript
// Install: npm install @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-grpc

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://tempo.monitoring.svc.cluster.local:4317'
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {},
      '@opentelemetry/instrumentation-express': {},
      '@opentelemetry/instrumentation-pg': {}  // Auto-trace database queries
    })
  ],
  serviceName: 'product-api'
});

sdk.start();

// Traces automatically created for HTTP, DB, etc.
// Manual span creation for business logic:
const { trace } = require('@opentelemetry/api');

app.post('/orders', async (req, res) => {
  const tracer = trace.getTracer('product-api');
  const span = tracer.startSpan('process_order');
  
  span.setAttribute('user_id', req.body.user_id);
  span.setAttribute('order_total', req.body.total);
  
  try {
    const order = await processOrder(req.body);
    span.setAttribute('order_id', order.id);
    span.setStatus({ code: 1 }); // OK
    res.json({orderId: order.id});
  } catch (err) {
    span.setStatus({ code: 2, message: err.message }); // ERROR
    span.recordException(err);
    res.status(500).json({error: err.message});
  } finally {
    span.end();
  }
});
```

**Grafana Trace View** (query in Explore):
- Search by `trace_id`, `service.name`, `http.status_code`
- Visualize request flow: API Gateway → Product API → Database
- Identify slowest span in trace (e.g., database query took 800ms of 1s total)

---

### Correlation: Linking Metrics, Logs, Traces

**Grafana Dashboard with Correlations**:

```json
{
  "dashboard": {
    "title": "Product API - Correlated Observability",
    "panels": [
      {
        "title": "Error Rate (Metric)",
        "datasource": "Prometheus",
        "targets": [{
          "expr": "rate(http_requests_total{status=~'5..',service='product-api'}[5m])"
        }],
        "links": [
          {
            "title": "View Error Logs",
            "url": "/explore?datasource=Loki&queries=[{expr:\"{service=\\\"product-api\\\",level=\\\"error\\\"}\"}]"
          }
        ]
      },
      {
        "title": "Recent Error Logs (Logs)",
        "datasource": "Loki",
        "targets": [{
          "expr": "{service=\"product-api\",level=\"error\"}"
        }],
        "links": [
          {
            "title": "View Trace",
            "url": "/explore?datasource=Tempo&queries=[{query:\"${__data.fields.trace_id}\"}]"
          }
        ]
      },
      {
        "title": "Slow Traces (Traces)",
        "datasource": "Tempo",
        "targets": [{
          "query": "{service.name=\"product-api\" && duration>1s}"
        }]
      }
    ]
  }
}
```

**Workflow: Debug a slow request**
1. **See spike in p95 latency** (Metrics dashboard)
2. **Click "View Slow Traces"** → Opens Tempo
3. **Find slowest trace** → See database span took 2.5s
4. **Click trace_id** → Opens Loki with all logs for that request
5. **See ERROR log**: "Database connection timeout"
6. **Root cause**: Database connection pool exhausted

---

### Cost Optimization

**Open-Source Stack Cost** (self-hosted on Kubernetes):
- Prometheus: ~$50/month (storage)
- Loki: ~$30/month (storage)
- Tempo: ~$40/month (storage)
- **Total: ~$120/month** for 15 services

**Commercial APM Comparison**:
- Datadog: ~$3,000/month (15 hosts × $200/host)
- New Relic: ~$2,500/month (15 users × $99/user + data)
- **Savings: ~$2,800/month** (96% cheaper)

**Trade-offs**:
- ✅ Cost: 96% cheaper than commercial
- ✅ Flexibility: Full control and customization
- ❌ Ops burden: Team must maintain stack
- ❌ Features: Less polished UX than Datadog

---

### Key Outcomes
- ✅ **Complete observability**: Metrics, logs, traces in one stack
- ✅ **Correlated debugging**: Jump from metric → log → trace seamlessly
- ✅ **Cost-effective**: $120/month vs $3,000/month commercial
- ✅ **Kubernetes-native**: Auto-discovery, no manual config
- ✅ **Production-ready**: 30-day retention, persistent storage, HA

