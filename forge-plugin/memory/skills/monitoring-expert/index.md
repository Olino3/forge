# monitoring-expert Memory

Project-specific memory for monitoring stack decisions, alerting rules, SLO definitions, and observability patterns.

## Purpose

This memory helps the `skill:monitoring-expert` remember:
- Which monitoring tools and platforms each project uses
- Established SLO/SLI definitions and error budget status
- Alerting rules, severity thresholds, and escalation policies
- Distributed tracing configuration and sampling strategies
- Dashboard structures and naming conventions
- Incident response patterns and runbook locations

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `monitoring_stack.md`

**Purpose**: Track the observability tools, platforms, and architecture decisions for this project

**Should contain**:
- **Metrics platform**: Which metrics backend is used (Prometheus, Datadog, CloudWatch, etc.)
- **Tracing backend**: Distributed tracing tool and propagation format (Jaeger, Zipkin, X-Ray)
- **Log aggregation**: Logging pipeline and storage (ELK, Loki, Splunk)
- **Dashboarding**: Visualization platform and dashboard hierarchy
- **Instrumentation**: SDK versions, auto-instrumentation setup, custom span conventions
- **Infrastructure**: Deployment environment (Kubernetes, ECS, Lambda) and collection agents

**Example structure**:
```markdown
# Monitoring Stack - MyProject

## Metrics
- Platform: Prometheus 2.48 + Grafana 10.x
- Collection: kube-prometheus-stack Helm chart
- Retention: 15 days local, 1 year in Thanos long-term storage
- Custom metrics prefix: `myapp_`

## Tracing
- SDK: OpenTelemetry (Node.js 1.20, Python 1.22)
- Backend: Jaeger 1.54 with Elasticsearch
- Propagation: W3C Trace Context
- Sampling: 10% head-based (prod), 100% (dev/staging)

## Logging
- Collection: Fluent Bit DaemonSet
- Storage: Loki 2.9 with S3 backend
- Format: JSON structured logging
- Retention: 30 days hot, 90 days cold

## Dashboards
- Platform: Grafana
- Hierarchy: Cluster Overview → Service → Component
- Naming: `{team}-{service}-{view}` (e.g., payments-checkout-overview)
```

**When to update**: After any monitoring infrastructure change or tool migration

---

#### `alerting_rules.md`

**Purpose**: Document active alerting rules, severity definitions, and escalation policies

**Should contain**:
- **Severity levels**: Definition of each severity tier and expected response time
- **Alert inventory**: List of active alerts with ownership and runbook links
- **Escalation policies**: How alerts route through on-call, team leads, and management
- **Silencing patterns**: Known maintenance windows and recurring silence rules
- **Alert quality metrics**: False positive rate, MTTA, MTTR trends

**Example structure**:
```markdown
# Alerting Rules - MyProject

## Severity Definitions
| Severity | Response Time | Notification      | Example                    |
|----------|--------------|-------------------|----------------------------|
| SEV1     | 5 min        | PagerDuty page    | Checkout completely down    |
| SEV2     | 30 min       | PagerDuty low-urg | Elevated error rate (>1%)  |
| SEV3     | Next biz day | Slack #alerts     | Disk usage trending high   |
| SEV4     | Sprint plan  | Jira ticket       | Certificate expiry in 30d  |

## Active Alerts (24 rules)
### Checkout Service (8 rules)
- CheckoutSLOCriticalBurn — SEV1 — runbook: /runbooks/checkout-slo
- CheckoutSLOWarningBurn — SEV2 — runbook: /runbooks/checkout-slo
- CheckoutHighLatency — SEV2 — runbook: /runbooks/checkout-latency
...

## Escalation Policy
1. On-call engineer (0-15 min)
2. Secondary on-call (15-30 min)
3. Engineering manager (30-60 min)
4. VP Engineering (60+ min, SEV1 only)
```

**When to update**: When alerting rules are added, modified, or removed

---

#### `slo_definitions.md`

**Purpose**: Track SLI/SLO definitions, error budgets, and compliance status

**Should contain**:
- **SLO inventory**: All defined SLOs with target, measurement window, and owner
- **SLI definitions**: How each SLO is measured (query, metric, calculation)
- **Error budget tracking**: Current burn rate and remaining budget
- **SLO review history**: Quarterly review notes and threshold adjustments

**Example structure**:
```markdown
# SLO Definitions - MyProject

## SLO Inventory
| SLO Name              | Target  | Window | SLI Metric                         | Owner    |
|-----------------------|---------|--------|-------------------------------------|----------|
| Checkout Availability | 99.95%  | 30-day | successful_checkouts / total_checkouts | Payments |
| Search Latency p99    | < 200ms | 30-day | histogram_quantile(0.99, search_dur) | Search   |
| API Availability      | 99.9%   | 30-day | successful_requests / total_requests  | Platform |

## Error Budget Status (as of 2026-02-12)
| SLO                   | Budget (30d) | Consumed | Remaining | Status    |
|-----------------------|-------------|----------|-----------|-----------|
| Checkout Availability | 21.6 min    | 4.2 min  | 17.4 min  | ✅ Healthy |
| Search Latency p99    | 43.2 min    | 38.1 min | 5.1 min   | ⚠️ At Risk |
| API Availability      | 43.2 min    | 12.0 min | 31.2 min  | ✅ Healthy |

## Review History
- 2026-01-15: Tightened checkout SLO from 99.9% to 99.95% after Q4 stability improvements
- 2025-10-01: Added search latency SLO after customer complaints about slow search
```

**When to update**: After SLO reviews, error budget incidents, or threshold adjustments

---

## Usage in skill:monitoring-expert

### Loading Memory

```markdown
# In skill workflow Step 3

project_name = detect_project_name()
memory = memoryStore.getSkillMemory("monitoring-expert", "{project-name}")

if memory exists:
    monitoring_stack = read(memory, "monitoring_stack.md")
    alerting_rules = read(memory, "alerting_rules.md")
    slo_definitions = read(memory, "slo_definitions.md")

    # Use for design decisions
    - Follow established tool choices and conventions
    - Reuse alerting severity definitions and escalation policies
    - Reference existing SLO targets when designing new alerts
```

### Updating Memory

```markdown
# In skill workflow Step 5

After generating monitoring artifacts:

1. Check if new decisions were made:
   - New tools or platforms introduced?
   - New alerting rules or severity thresholds?
   - New or modified SLO definitions?

2. If yes, update relevant memory file:
   memoryStore.update(layer="skill-specific", skill="monitoring-expert",
                      project="{project-name}", ...)

3. If first time setting up monitoring for project:
   - Create directory and all memory files
   - Populate with observations from this implementation
```

---

## Memory Evolution Over Time

### After 1st Monitoring Task
```markdown
# monitoring_stack.md

## Metrics
- Platform: Prometheus + Grafana
- Custom metrics prefix: `myapp_`

## Tracing
- SDK: OpenTelemetry
- Backend: Jaeger (all-in-one)
```

### After 5 Monitoring Tasks
```markdown
# monitoring_stack.md

## Metrics
- Platform: Prometheus 2.48 + Grafana 10.2
- Collection: kube-prometheus-stack 55.x
- Retention: 15 days local, Thanos for long-term
- Custom metrics: 42 application metrics defined
- Naming convention: `myapp_{domain}_{metric}_{unit}`

## Alerting
- 24 active alert rules across 6 services
- SEV1 MTTA: 3.2 min, MTTR: 18 min
- False positive rate: 4% (down from 82%)

## SLOs
- 5 SLOs defined, all meeting targets
- Error budget reviews: monthly
```

### After 20 Monitoring Tasks
```markdown
# Comprehensive observability knowledge — full stack documented,
# alert tuning history preserved, SLO evolution tracked.
# Memory now provides high-value project-specific monitoring guidance.
```

---

## Related Documentation

- **Main Memory Index**: `../index.md` for memory system overview
- **Skill Documentation**: `../../skills/monitoring-expert/SKILL.md` for skill workflow
- **Context Files**: `../../context/` for general development knowledge
- **Memory Lifecycle**: `../lifecycle.md` for memory freshness and pruning
- **Memory Quality**: `../quality_guidance.md` for memory validation
