---
name: "sre-engineer"
description: "Site reliability engineering, observability, and incident response. Implements SLIs/SLOs/SLAs, error budgets, monitoring, alerting, incident management, postmortems, chaos engineering, and capacity planning for reliable production systems."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 6
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, slo_definitions.md, incident_learnings.md]
    - type: "shared-project"
      usage: "reference"
tags: [sre, reliability, observability, monitoring, alerting, incidents, slo, sla, chaos-engineering, error-budget, postmortem, on-call]
---

# skill:sre-engineer - Site Reliability Engineering & Observability

## Version: 1.0.0

## Purpose

The **sre-engineer** skill implements Site Reliability Engineering practices for production systems. It defines and tracks Service Level Objectives (SLOs), implements comprehensive observability, designs incident response processes, conducts postmortems, performs chaos engineering, and manages on-call practices.

**Use this skill when:**
- Defining SLIs, SLOs, and error budgets for services
- Implementing monitoring and observability stacks
- Designing alerting strategies and on-call processes
- Creating incident response runbooks and playbooks
- Conducting postmortems and blameless retrospectives
- Planning capacity and performance testing
- Implementing chaos engineering experiments
- Establishing reliability culture and SRE practices

**Produces:**
- SLO definitions and error budget tracking
- Observability stack configurations (metrics, logs, traces)
- Alerting rules and on-call schedules
- Incident response runbooks and playbooks
- Postmortem reports with action items
- Chaos engineering experiment plans
- Capacity planning analysis
- Reliability dashboards and reports

## File Structure

```
skills/sre-engineer/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather system requirements:
  - Service architecture (microservices, monolith, serverless)
  - User-facing vs internal services
  - Business impact and criticality
  - Current availability and performance baseline
  - Existing monitoring and alerting (if any)
  - Team size and on-call capability
  - Budget constraints for tooling
- Understand reliability expectations:
  - Customer SLA requirements
  - Business tolerance for downtime
  - Performance expectations (latency, throughput)
  - Data consistency requirements
  - Geographic distribution and traffic patterns
- Detect existing SRE practices:
  - Review existing SLOs, dashboards, runbooks
  - Analyze incident history and patterns
  - Assess current observability coverage
  - Evaluate on-call process maturity
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="sre-engineer"` and `domain="engineering"`.

**Load project-specific memory:**
```
memoryStore.getSkillMemory("sre-engineer", "{project-name}")
```

**Check for cross-skill insights:**
```
memoryStore.getByProject("{project-name}")
```

**Review memory for:**
- Previously defined SLOs and their burn rates
- Historical incident patterns and root causes
- Effective alerting rules and false positive rates
- Successful chaos experiments and findings
- Capacity planning trends and forecasts
- On-call rotation learnings
- Postmortem action items and completion status

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain and other relevant domains. Stay within the file budget declared in frontmatter.

**Use context indexes:**
```
contextProvider.getDomainIndex("engineering")
contextProvider.getDomainIndex("azure")
contextProvider.getDomainIndex("kubernetes")
contextProvider.getDomainIndex("git")
```

**Load relevant context files based on infrastructure:**
- Monitoring and observability patterns
- Cloud platform reliability features (Azure, AWS, GCP)
- Kubernetes reliability patterns if using K8s
- Security monitoring and compliance
- Performance optimization techniques

**Budget: 6 files maximum**

### Step 4: Define Service Level Indicators (SLIs)

- Select appropriate SLIs for service type:
  - **Request-driven services**: Availability, latency, error rate
  - **Data processing**: Freshness, correctness, coverage
  - **Storage systems**: Durability, availability, latency
  - **User-facing apps**: Page load time, interaction responsiveness, error rate
- Implement SLI measurement:
  - Define precise measurement methodology
  - Identify data sources (metrics, logs, traces)
  - Configure instrumentation and collection
  - Validate measurement accuracy and coverage
- Document SLI specifications:
  - What you're measuring and why
  - How it's calculated (formulas, aggregations)
  - Measurement frequency and windows
  - Data source and query examples

### Step 5: Establish Service Level Objectives (SLOs)

- Set SLO targets based on:
  - **User expectations**: What do users need to be successful?
  - **Business requirements**: What does the business promise customers?
  - **Current performance**: Where are you today? (can't go backward)
  - **Error budget**: How much failure can you tolerate?
  - **Cost of reliability**: Cost to improve 99% → 99.9% → 99.99%
- Define SLO structure:
  - **Target**: e.g., "99.9% of requests return success in < 500ms"
  - **Time window**: Rolling 30 days, calendar month, or custom
  - **Measurement method**: Request-based or time-based
  - **Valid events**: What requests count toward SLO?
- Calculate error budgets:
  - Error budget = (100% - SLO target) × total events
  - Example: 99.9% SLO = 0.1% error budget = 43 min downtime/month
- Create SLO tiers for different service levels:
  - **Critical**: User-facing, revenue-impacting (99.95% - 99.99%)
  - **High**: Important, customer-visible (99.5% - 99.9%)
  - **Medium**: Internal, business operations (99% - 99.5%)
  - **Low**: Non-critical, best-effort (95% - 99%)

### Step 6: Implement Observability Stack

- Design three pillars of observability:
  
  **1. Metrics** (aggregated numeric data)
  - System metrics: CPU, memory, disk, network
  - Application metrics: Request rate, error rate, latency (RED method)
  - Business metrics: Orders/sec, signups, revenue
  - Use case: Alerting, dashboards, capacity planning
  
  **2. Logs** (discrete event records)
  - Structured logging (JSON format)
  - Contextual fields (trace_id, user_id, request_id)
  - Log levels (ERROR, WARN, INFO, DEBUG)
  - Use case: Debugging, audit trails, security analysis
  
  **3. Traces** (request flow across services)
  - Distributed tracing (OpenTelemetry, Jaeger, Zipkin)
  - Span attributes and relationships
  - Service dependency mapping
  - Use case: Performance optimization, root cause analysis

- Choose observability tools:
  - **Cloud-native**: Azure Monitor, AWS CloudWatch, GCP Stackdriver
  - **Open-source**: Prometheus + Grafana, ELK Stack, Jaeger
  - **Commercial**: Datadog, New Relic, Dynatrace, Splunk
  - **Hybrid**: Mix of cloud and OSS for cost optimization

- Implement collection and storage:
  - Metrics: Prometheus, InfluxDB, CloudWatch
  - Logs: Elasticsearch, Loki, Azure Log Analytics
  - Traces: Jaeger, Tempo, AWS X-Ray
  - Correlation: Link metrics, logs, traces via trace IDs

### Step 7: Design Alerting Strategy

- Define alerting principles:
  - **Alert on symptoms, not causes**: Alert on user pain (SLO violations), not disk space
  - **Actionable only**: Every alert must require human action
  - **Context-rich**: Include runbook link, dashboard, severity
  - **Avoid alert fatigue**: Max 1-2 pages per on-call shift
  
- Implement multi-burn-rate alerting:
  - **Fast burn**: 2% budget consumed in 1 hour → Page immediately
  - **Slow burn**: 5% budget consumed in 6 hours → Ticket for next business day
  - Reduces false positives while catching real issues early

- Set up alert routing:
  - **Page**: Immediate attention required (PagerDuty, Opsgenie)
  - **Ticket**: Work item for next day (Jira, GitHub Issues)
  - **Info**: Awareness only (Slack, email)

- Define severity levels:
  - **SEV1/Critical**: Customer-impacting outage, all hands on deck
  - **SEV2/High**: Degraded service, significant impact
  - **SEV3/Medium**: Minor impact, workaround available
  - **SEV4/Low**: Informational, no immediate action

### Step 8: Create Incident Response Process

- Design incident response workflow:
  1. **Detection**: Alert fires or user report received
  2. **Triage**: Assess severity and impact, page on-call
  3. **Investigation**: Gather data, form hypotheses, test
  4. **Mitigation**: Stop the bleeding (rollback, scale, disable feature)
  5. **Resolution**: Fix root cause or plan permanent fix
  6. **Recovery**: Restore service, verify SLOs recovering
  7. **Postmortem**: Document timeline, root cause, action items

- Create incident roles:
  - **Incident Commander**: Coordinates response, makes decisions
  - **Communications Lead**: Updates stakeholders, customers
  - **Technical Lead**: Drives technical investigation and mitigation
  - **Scribe**: Documents timeline and actions in real-time

- Build runbooks and playbooks:
  - **Runbook**: Step-by-step diagnostic and remediation procedures
  - **Playbook**: High-level response strategy for incident types
  - Include: Symptoms, investigation steps, mitigation actions, escalation path
  - Example runbooks: "High API latency", "Database connection pool exhausted"

- Implement incident tracking:
  - Incident management tool (PagerDuty, Opsgenie, custom)
  - Document: Start time, severity, impacted services, timeline
  - Status page: Communicate to customers (statuspage.io, custom)

### Step 9: Establish Postmortem Culture

- Conduct blameless postmortems:
  - **Blameless**: Focus on systems and processes, not individuals
  - **Timely**: Within 48 hours while memory is fresh
  - **Inclusive**: Include all responders and affected teams
  - **Actionable**: Every postmortem produces improvement items

- Postmortem structure:
  1. **Summary**: One-paragraph overview (what, when, impact)
  2. **Timeline**: Chronological events from detection to resolution
  3. **Root Cause**: Technical and process failures (5 Whys analysis)
  4. **Impact**: Users affected, revenue lost, SLO burn
  5. **Resolution**: How was it fixed?
  6. **Lessons Learned**: What went well, what didn't
  7. **Action Items**: Concrete, assigned, time-bound improvements

- Track action items:
  - Assign owner and due date
  - Review in weekly SRE meetings
  - Measure completion rate (target: 80%+ within 30 days)
  - Identify recurring themes across postmortems

### Step 10: Implement Chaos Engineering

- Design chaos experiments:
  - **Hypothesis**: "If we kill a database node, the system will failover in < 5 seconds"
  - **Blast radius**: Start small (dev), gradually expand (staging → prod)
  - **Abort conditions**: Define when to stop experiment (SLO violation, error spike)
  - **Rollback plan**: How to restore normal operation

- Common chaos experiments:
  - **Resource exhaustion**: CPU, memory, disk, network
  - **Dependency failure**: Database down, API timeout, DNS failure
  - **Network issues**: Latency injection, packet loss, partition
  - **State corruption**: Malformed data, disk corruption
  - **Time travel**: Clock skew, leap seconds

- Use chaos engineering tools:
  - **Chaos Monkey**: Random instance termination (Netflix OSS)
  - **Gremlin**: Full-featured chaos engineering platform
  - **Litmus Chaos**: Kubernetes-native chaos experiments
  - **Azure Chaos Studio**: Managed chaos service for Azure
  - **Chaos Toolkit**: Open-source automation framework

- Schedule and execute:
  - **Game Days**: Scheduled chaos exercises (quarterly)
  - **Continuous chaos**: Automated low-impact experiments in prod
  - **Document findings**: What broke, how to improve

### Step 11: Plan Capacity and Performance

- Implement capacity planning:
  - **Current utilization**: Measure baseline resource consumption
  - **Growth trends**: Analyze historical growth (weekly, monthly, yearly)
  - **Peak handling**: Plan for traffic spikes (Black Friday, product launch)
  - **Lead time**: Account for provisioning time (cloud: minutes, hardware: weeks)

- Set resource utilization targets:
  - **CPU**: 50-70% average (headroom for spikes)
  - **Memory**: 60-80% average (avoid OOM kills)
  - **Disk**: 70-80% full (time to provision more)
  - **Network**: 50-70% of bandwidth (burst capacity)

- Perform load testing:
  - **Baseline**: Current capacity and breaking points
  - **Stress testing**: Gradual load increase until failure
  - **Spike testing**: Sudden traffic surge handling
  - **Soak testing**: Sustained load for memory leaks, degradation
  - Tools: k6, Gatling, JMeter, Locust, Azure Load Testing

- Establish performance budgets:
  - Page load time: < 2 seconds (Google research: 53% abandon after 3s)
  - API latency: p50 < 100ms, p95 < 500ms, p99 < 1s
  - Time to interactive: < 3 seconds
  - Largest contentful paint: < 2.5 seconds

### Step 12: Design On-Call Practices

- Structure on-call rotation:
  - **Primary**: First responder for all alerts
  - **Secondary**: Backup if primary unresponsive
  - **Rotation length**: 1 week (balance context vs burden)
  - **Team size**: Minimum 4 people for sustainable rotation

- Set on-call expectations:
  - **Response time**: Acknowledge page in 5 minutes, engage in 15 minutes
  - **Availability**: Must be sober, near computer, reliable internet
  - **Handoff**: 15-minute overlap with next on-call engineer
  - **Documentation**: Update runbooks during shift

- Implement on-call support:
  - **Compensation**: Time off in lieu, on-call pay, bonuses
  - **Tools**: PagerDuty, Opsgenie, VictorOps for alerting
  - **Training**: Shadow on-call shifts before primary rotation
  - **Health**: Limit consecutive on-call weeks, monitor burnout

- Measure on-call health:
  - **Pages per shift**: Target < 5 actionable pages per week
  - **Time to acknowledge**: Should be < 5 minutes for 95% of pages
  - **Escalations**: Measure how often secondary is needed
  - **Toil**: Track time spent on repetitive manual work (automate if > 50%)

### Step 13: Generate Output

- Save SRE documentation to `/claudedocs/sre-engineer_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - **SLO definitions**: SLIs, targets, error budgets, measurement methods
  - **Observability setup**: Metrics, logs, traces configuration and dashboards
  - **Alerting rules**: Alert definitions, thresholds, routing, runbooks
  - **Incident response**: Roles, workflow, communication templates
  - **Postmortem template**: Structure and guidelines
  - **Chaos experiments**: Planned experiments and schedule
  - **Capacity plan**: Growth forecasts and scaling timeline
  - **On-call guide**: Rotation schedule, runbooks, escalation paths
  - **Reliability metrics**: Current SLO performance, error budget status
  - **Improvement roadmap**: Action items prioritized by impact

### Step 14: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="sre-engineer"`.

**Store learned insights:**
```
memoryStore.updateSkillMemory("sre-engineer", "{project-name}", {
  slo_definitions: [...],
  incident_patterns: [...],
  effective_alerts: [...],
  chaos_findings: [...],
  capacity_trends: [...],
  on_call_learnings: [...]
})
```

**Update memory with:**
- SLO definitions and historical burn rates
- Incident patterns, root causes, and resolutions
- Effective alerting rules and false positive rates
- Chaos engineering findings and system weaknesses
- Capacity trends and scaling decisions
- On-call rotation insights and improvements
- Postmortem action items and completion status

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] SLIs defined with measurement methodology (Step 4)
- [ ] SLOs established with error budgets (Step 5)
- [ ] Observability stack implemented (metrics, logs, traces) (Step 6)
- [ ] Alerting strategy designed with multi-burn-rate alerts (Step 7)
- [ ] Incident response process created with roles and runbooks (Step 8)
- [ ] Postmortem culture established with blameless principles (Step 9)
- [ ] Chaos engineering experiments planned (Step 10)
- [ ] Capacity and performance planning completed (Step 11)
- [ ] On-call practices designed (Step 12)
- [ ] Output saved with standard naming convention (Step 13)
- [ ] Standard Memory Update pattern followed (Step 14)

## SRE Principles

### 1. Embrace Risk
- 100% reliability is wrong target (costs too much, slows innovation)
- Define acceptable risk via error budgets
- Spend error budget on innovation and velocity
- When budget exhausted, focus on reliability

### 2. Service Level Objectives
- SLOs are the foundation of SRE practice
- Must be based on user experience, not internal metrics
- Defend SLOs with error budgets, not heroics
- Review and adjust SLOs quarterly

### 3. Eliminate Toil
- Toil: Manual, repetitive, automatable work with no enduring value
- Target: < 50% of SRE time on toil
- Automate: Provisioning, deployments, incident response
- Measure toil and set reduction goals

### 4. Monitoring and Observability
- Monitor for symptoms (user pain), not causes (disk full)
- Use SLIs to drive alerts, not arbitrary thresholds
- Dashboards should answer questions, not just display data
- Invest in observability infrastructure

### 5. Automation
- Automate everything: deployments, scaling, incident response
- Reliability through automation, not manual intervention
- Write runbooks, then automate them
- Continuous improvement of automation

### 6. Release Engineering
- Small, frequent releases reduce risk
- Automated testing and progressive rollouts
- Fast rollback capability (< 5 minutes)
- Canary deployments and feature flags

### 7. Simplicity
- Complexity is the enemy of reliability
- Minimize components, dependencies, configurations
- Delete unused code and features
- Document architectural decisions

## SLI Examples by Service Type

| Service Type | SLI Examples |
|--------------|--------------|
| **Request-driven API** | Availability (% successful requests), Latency (p50, p95, p99), Throughput (req/sec) |
| **Data pipeline** | Freshness (time since last update), Correctness (% records processed without error), Coverage (% expected data present) |
| **Storage system** | Durability (% data not lost), Availability (% successful reads/writes), Latency (p95 read/write time) |
| **Web application** | Page load time (p95), Time to interactive, Error rate (% pages with errors) |
| **Batch processing** | Throughput (records/hour), Success rate (% jobs completed), Latency (job completion time) |
| **Message queue** | Availability (% time accepting messages), Latency (end-to-end message delay), Backlog (unprocessed messages) |

## Monitoring Tool Comparison

| Tool | Type | Strengths | Best For | Cost |
|------|------|-----------|----------|------|
| **Prometheus + Grafana** | OSS Metrics | Powerful query language (PromQL), widely adopted, Kubernetes-native | Metrics collection and dashboards | Free (self-hosted) |
| **Datadog** | Commercial APM | All-in-one observability, beautiful UX, extensive integrations | Teams wanting managed solution | $$$ (per host) |
| **New Relic** | Commercial APM | Deep application insights, AI-powered anomaly detection | Application performance monitoring | $$$ (per user) |
| **Azure Monitor** | Cloud-native | Native Azure integration, Application Insights, Log Analytics | Azure workloads | $$ (per GB ingested) |
| **ELK Stack** | OSS Logs | Powerful log search, visualization, alerting | Log aggregation and analysis | Free (self-hosted) |
| **Jaeger** | OSS Tracing | Distributed tracing, service dependency graphs | Microservices debugging | Free (self-hosted) |
| **Splunk** | Commercial SIEM | Enterprise-grade search, security analytics, compliance | Security and compliance | $$$$ (per GB) |
| **Grafana Cloud** | Managed OSS | Hosted Prometheus, Loki, Tempo, Grafana | Teams wanting OSS without ops burden | $$ (per metrics/logs) |

## On-Call Platform Comparison

| Platform | Strengths | Best For | Cost |
|----------|-----------|----------|------|
| **PagerDuty** | Industry standard, rich integrations, incident response workflows | Enterprise teams, complex escalations | $$$ (per user/month) |
| **Opsgenie** | Atlassian integration, flexible routing, on-call scheduling | Teams using Jira/Confluence | $$ (per user/month) |
| **VictorOps (Splunk)** | Real-time collaboration, timeline view, post-incident analysis | Teams needing chat-based incident management | $$ (per user/month) |
| **AlertManager** | Open-source, Prometheus-native, flexible routing rules | Teams using Prometheus, DIY setup | Free (self-hosted) |
| **Azure Monitor Alerts** | Native Azure integration, action groups, metric alerts | Azure-only environments | $ (per alert rule) |

## Error Budget Policies

### Policy Template

**When error budget is healthy (> 10% remaining):**
- Approve risky changes and experiments
- Fast-track feature releases
- Schedule chaos engineering tests
- Optimize for velocity over reliability

**When error budget is low (1-10% remaining):**
- Increase change review scrutiny
- Slow down release cadence
- Defer risky experiments to next period
- Focus on reliability improvements

**When error budget is exhausted (0% remaining):**
- Freeze all feature launches
- Only critical bug fixes and security patches
- All hands on reliability improvements
- Conduct reliability-focused postmortem
- Set recovery plan and timeline

### Example Error Budget Calculation

```
Service: API Gateway
SLO: 99.9% of requests succeed in < 500ms over rolling 30 days

Error budget:
- Allowed failure: 0.1% of requests
- Total requests (30 days): 100M
- Allowed failures: 100,000 requests
- OR: 43.2 minutes of downtime per month

Current status:
- Failed requests: 25,000 (25% of budget consumed)
- Budget remaining: 75,000 requests (75%)
- Days into month: 10
- Burn rate: 2.5% per day
- Projected: 75% consumed by end of month → HEALTHY

Alert thresholds:
- Fast burn: 2% budget in 1 hour → Page
- Slow burn: 5% budget in 6 hours → Ticket
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with comprehensive SRE capabilities |
