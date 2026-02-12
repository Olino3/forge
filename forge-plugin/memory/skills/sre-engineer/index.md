# sre-engineer Memory

Project-specific memory for Site Reliability Engineering, including SLO definitions, incident learnings, observability configurations, chaos experiments, and on-call practices.

## Purpose

This memory helps the `skill:sre-engineer` remember:
- SLO definitions, targets, and historical burn rates
- Incident patterns, root causes, and resolutions
- Effective alerting rules and false positive rates
- Chaos engineering experiments and findings
- Observability stack configurations
- Capacity planning trends and forecasts
- On-call rotation insights and improvements
- Postmortem action items and completion status

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md` ⭐ CRITICAL

**Purpose**: High-level service understanding - ALWAYS CREATE THIS FIRST

**Must contain**:
- **Service name and purpose**: What does this service do?
- **Service type**: Request-driven API, data pipeline, storage, batch processing, user-facing app
- **User base**: Internal users, external customers, B2B, B2C
- **Business criticality**: Revenue-critical, customer-facing, internal, best-effort
- **Current availability**: Baseline uptime and performance
- **SLA commitments**: What has been promised to customers?
- **Team size**: Number of engineers on-call
- **Infrastructure**: Cloud provider, Kubernetes, serverless, VMs
- **Dependencies**: Critical upstream/downstream services
- **Peak traffic**: Normal load vs peak load patterns

#### `slo_definitions.md`

**Purpose**: Document Service Level Objectives and error budgets

**Must contain**:
- **SLIs selected**: Availability, latency, throughput, freshness, etc.
- **SLO targets**: Specific percentages and thresholds (e.g., 99.9%)
- **Time windows**: Rolling 30 days, calendar month, custom
- **Measurement methods**: PromQL queries, log analysis, traces
- **Error budgets**: Calculated allowable failure (requests, downtime)
- **Burn rates**: Historical consumption rates
- **Budget policy**: Actions when budget healthy/low/exhausted
- **SLO tiers**: Different targets for different service levels

#### `incident_learnings.md`

**Purpose**: Track incidents, patterns, and prevention

**Must contain**:
- **Incident history**: Date, severity, duration, impact
- **Root causes**: Technical and process failures
- **Recurring patterns**: Common failure modes (DB exhaustion, traffic spikes)
- **MTTR trends**: Mean Time To Recovery over time
- **Postmortem action items**: Status and completion
- **Prevention measures**: What was done to prevent recurrence
- **Escalation patterns**: When and why incidents escalated

### Optional Files

#### `observability_config.md`
- Monitoring stack details (Prometheus, Datadog, etc.)
- Dashboard links and purposes
- Alerting rules and thresholds
- Log aggregation configuration
- Tracing setup and correlation
- Custom metrics and business KPIs

#### `chaos_experiments.md`
- Planned and executed chaos experiments
- Hypotheses tested
- Blast radius and abort conditions
- Findings and system weaknesses discovered
- Remediation actions taken
- Game day schedules and outcomes

#### `capacity_planning.md`
- Current resource utilization (CPU, memory, disk, network)
- Growth trends (weekly, monthly, yearly)
- Peak capacity events (Black Friday, product launches)
- Scaling decisions and outcomes
- Cost optimization opportunities
- Resource forecasts (3 months, 6 months, 1 year)

#### `on_call_notes.md`
- On-call rotation schedule
- Common issues and quick fixes
- Runbook effectiveness feedback
- Response time metrics
- Pages per shift trends
- Escalation frequency
- On-call engineer feedback and improvements

#### `alerting_tuning.md`
- Alert definitions and evolution
- False positive rates and tuning
- Alert fatigue metrics
- Notification routing changes
- Silence patterns and justified suppressions
- Alert effectiveness scores

## Cross-Skill Integration

The `sre-engineer` skill integrates with:
- **devops-engineer**: CI/CD pipeline reliability and deployment safety
- **cloud-architect**: Infrastructure design for reliability and resilience
- **kubernetes-specialist**: K8s reliability patterns and health checks
- **terraform-engineer**: Infrastructure as Code for consistent environments
- **security**: Security monitoring, compliance, and incident response

Use `memoryStore.getByProject("{project-name}")` to discover insights from other skills.

## Memory Lifecycle

- **Fresh** (0-30 days): Active SRE practice, full detail on incidents and experiments
- **Active** (31-90 days): Stable reliability, maintain SLOs and key learnings
- **Stale** (91-180 days): Legacy service, summarize patterns and final state
- **Archived** (181+ days): Deprecated service, keep major incidents and lessons only

## Example Memory Entry

### Example: `payment-api/slo_definitions.md`

```markdown
# SLO Definitions - Payment API

**Last Updated**: 2026-02-10
**Service Type**: Request-driven API (payment processing)
**Business Criticality**: Revenue-critical, customer-facing
**Current Availability**: 99.95% (last 90 days)
**Team Size**: 5 engineers on-call rotation

---

## SLI 1: Availability (Success Rate)

**Definition**: Percentage of payment requests that successfully process without errors

**Measurement**:
```promql
sum(rate(payment_requests_total{status="success"}[30d]))
/
sum(rate(payment_requests_total[30d]))
```

**SLO Target**: 99.9% of requests succeed over rolling 30 days

**Rationale**: 
- Users expect payments to work every time
- 99.9% balances reliability with innovation velocity
- Industry standard for payment processing (Stripe: 99.99%, Square: 99.95%)

**Error Budget**:
- Total requests/month: 10 million
- Allowed failures: 10,000 requests (0.1%)
- Equivalent downtime: 43.2 minutes/month

**Historical Performance**:
- Jan 2026: 99.94% (budget: 40% consumed) ✅
- Dec 2025: 99.87% (budget: 130% consumed - SEV1 incident) ❌
- Nov 2025: 99.92% (budget: 80% consumed) ✅

**Alerting**:
- Fast burn (2% budget in 1 hour): Page on-call immediately
- Slow burn (5% budget in 6 hours): Create ticket for next business day

---

## SLI 2: Latency (Response Time)

**Definition**: Time from request received to response sent, measured at API Gateway

**Measurement**:
```promql
histogram_quantile(0.95,
  sum(rate(payment_request_duration_seconds_bucket[30d])) by (le)
)
```

**SLO Target**: 95% of requests complete in < 2 seconds over rolling 30 days

**Rationale**:
- User research: 3 seconds feels "too slow" for payment
- 2 second target gives margin for network latency
- P95 (not P99) balances coverage with outlier tolerance

**Error Budget**:
- Total requests/month: 10 million
- Allowed slow requests: 500,000 (5%)

**Historical Performance**:
- Jan 2026: p95 = 1.2s ✅
- Dec 2025: p95 = 3.5s (database incident) ❌
- Nov 2025: p95 = 1.1s ✅

**Optimization History**:
- 2025-11: Reduced p95 from 2.8s → 1.1s by adding Redis cache
- 2025-09: Reduced p95 from 4.2s → 2.8s by optimizing database queries

---

## Error Budget Policy

### Healthy Budget (> 50% remaining)
- ✅ Approve all planned feature releases
- ✅ Allow A/B tests and experiments
- ✅ Schedule chaos engineering game days
- ✅ Optimize for velocity over reliability

### Low Budget (10-50% remaining)
- ⚠️ Increase change review scrutiny
- ⚠️ Require load testing for major features
- ⚠️ Defer low-priority features to next month
- ⚠️ Focus 20% engineering time on reliability

### Exhausted Budget (< 10% remaining)
- 🛑 **Feature freeze**: Only critical bug fixes and security patches
- 🛑 All hands on reliability improvements
- 🛑 Daily SRE standup to review progress
- 🛑 Conduct reliability retrospective
- 🛑 Create recovery plan with timeline

**Historical Invocations**:
- Dec 2025: Feature freeze for 1 week after SEV1 incident (budget exhausted)
- Result: Shipped 3 reliability improvements, budget recovered to 60% by Jan 15

---

## SLO Review Schedule

- **Weekly**: Check burn rates, trending toward budget exhaustion?
- **Monthly**: Review SLO targets, still aligned with user needs?
- **Quarterly**: Deep dive on SLO effectiveness, adjust targets if needed

**Last Review**: 2026-02-01
**Next Review**: 2026-05-01
**Adjustments Needed**: None, SLOs well-calibrated
```

---

### Example: `payment-api/incident_learnings.md`

```markdown
# Incident Learnings - Payment API

**Service**: Payment API
**On-Call Team**: 5 engineers, 1-week rotation
**Incident Count (Last 90 Days)**: 4 incidents (1 SEV1, 2 SEV2, 1 SEV3)
**MTTR Average**: 38 minutes

---

## Incident #2026-001: Database Connection Pool Exhaustion

**Date**: 2026-01-15  
**Duration**: 47 minutes (14:22 - 15:09 UTC)  
**Severity**: SEV2  
**Impact**: 35% of payment requests failed, $23,000 revenue loss  

### Root Cause
Database connection pool exhausted (100% utilization) due to long-running query introduced in v2.3.0. Query scanned entire `payments` table (12M rows) without index.

### Contributing Factors
- No query performance testing in CI/CD
- Staging database had only 10k rows (query fast in staging)
- No proactive alert on connection pool usage

### Mitigation
1. Rollback v2.3.0 → v2.2.5 (10 min)
2. Add missing index on `payments.user_id` (5 min)
3. Scale database read replicas 2 → 4 (10 min)

### Prevention
- ✅ Added query performance tests to CI (assert p95 < 1s) - COMPLETE
- ✅ Scaled staging DB to 1M rows (10% of prod) - COMPLETE
- ✅ Added alert: ConnectionPoolUsageHigh (> 80%) - COMPLETE
- ⏳ Implement query performance dashboard - IN PROGRESS (Due: 2026-02-28)

### Pattern
**Recurring**: Database connection pool exhaustion (3rd time in 6 months)  
**Action**: Need automated connection pool tuning based on traffic

---

## Incident #2025-012: Payment Gateway Timeout Cascade

**Date**: 2025-12-18  
**Duration**: 2 hours 14 minutes (SEV1)  
**Impact**: 100% payment failures, $127,000 revenue loss  

### Root Cause
Third-party payment gateway (Stripe) experienced 30-second API timeouts. Our service had 60-second timeout, held connections open, exhausted connection pool, cascaded to entire service failure.

### Prevention
- ✅ Reduced payment gateway timeout: 60s → 5s - COMPLETE
- ✅ Implemented circuit breaker (fail fast after 3 consecutive failures) - COMPLETE
- ✅ Added fallback to secondary payment processor - COMPLETE
- ✅ Chaos experiment: Test payment gateway timeout handling - COMPLETE

### Lessons Learned
- **Fail fast**: 60s timeout held resources too long
- **Circuit breakers**: Essential for external dependencies
- **Redundancy**: Secondary payment processor reduced impact by 80% in subsequent incident

---

## Recurring Patterns (Last 12 Months)

### Pattern 1: Database Connection Pool Exhaustion
- **Frequency**: 3 incidents in 6 months
- **Impact**: 35-100% request failures
- **Causes**: Slow queries, traffic spikes, connection leaks
- **Actions**: 
  - Implemented automated pool scaling (COMPLETE)
  - Added query performance gates in CI/CD (COMPLETE)
  - Scheduled quarterly load testing (ONGOING)

### Pattern 2: Third-Party API Failures
- **Frequency**: 2 incidents in 6 months
- **Impact**: 80-100% payment failures
- **Causes**: Stripe outage, AWS S3 outage
- **Actions**:
  - Implemented circuit breakers (COMPLETE)
  - Added fallback payment processor (COMPLETE)
  - Created runbook: "Third-Party Dependency Failure" (COMPLETE)

### Pattern 3: Deployment-Induced Incidents
- **Frequency**: 2 incidents in 12 months
- **Impact**: 20-50% error rate spike
- **Causes**: Bad config, untested code paths, missing index
- **Actions**:
  - Implemented canary deployments (10% → 50% → 100%) (COMPLETE)
  - Added automated rollback on error rate spike (COMPLETE)
  - Increased test coverage: 68% → 87% (IN PROGRESS)

---

## MTTR Trends

| Month | Incidents | Avg MTTR | Trend |
|-------|-----------|----------|-------|
| Jan 2026 | 1 | 47 min | 📈 (worse) |
| Dec 2025 | 2 | 134 min | 📈 (SEV1 incident) |
| Nov 2025 | 1 | 22 min | 📉 (improved) |
| Oct 2025 | 0 | - | 🎉 (no incidents) |
| Sep 2025 | 2 | 56 min | → (stable) |

**Goal**: MTTR < 30 minutes for SEV2+  
**Current**: 38 minutes (not meeting goal)  
**Actions**: Focus on faster rollback automation

---

## Postmortem Action Items Status

| Item | Owner | Due Date | Status |
|------|-------|----------|--------|
| Query performance CI tests | Alice | 2026-01-20 | ✅ DONE |
| Connection pool alerting | Bob | 2026-01-25 | ✅ DONE |
| Circuit breaker for Stripe | Carol | 2025-12-30 | ✅ DONE |
| Canary deployment | DevOps | 2026-01-10 | ✅ DONE |
| Query performance dashboard | David | 2026-02-28 | ⏳ IN PROGRESS |
| Automated pool scaling | Alice | 2026-03-15 | ⏳ IN PROGRESS |
| Quarterly load testing | Team | 2026-04-01 | 📅 SCHEDULED |

**Completion Rate**: 57% (4/7) - Target: 80%+  
**Overdue Items**: 0

---

## Prevention Improvements (Cumulative)

### 2025 → 2026 Comparison
- **Incident Count**: 12 (2025) → 4 (projected 2026) = 67% reduction 🎉
- **Avg MTTR**: 78 min (2025) → 38 min (2026) = 51% improvement 🎉
- **SLO Budget Exhaustion**: 3 times (2025) → 0 times (2026) = 100% improvement 🎉
- **Postmortem Action Completion**: 45% (2025) → 57% (2026) = +12% (needs improvement)
```

---

## Guidelines

1. **Always load memory first** before defining SLOs or responding to incidents
2. **Document incidents immediately** while details are fresh (within 48 hours)
3. **Track error budget trends** weekly to catch issues early
4. **Review action items** in SRE meetings, measure completion rate
5. **Update SLOs quarterly** to ensure alignment with user needs and business goals
6. **Cross-reference related skills** for infrastructure and deployment context
7. **Learn from patterns** - recurring incidents need systemic fixes, not one-off patches
8. **Measure everything** - MTTR, error budgets, alert effectiveness, on-call health

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial memory structure for sre-engineer skill |
