---
name: monitoring-expert
## description: Architects comprehensive observability solutions by designing metrics collection pipelines, alerting rules, distributed tracing instrumentation, log aggregation strategies, and observability platform integrations. Evaluates application health through golden signals, defines SLIs/SLOs, builds operational dashboards, and establishes incident response workflows. Like Hephaestus monitoring the eternal flames of his forge, this skill ensures every service is observed, every anomaly detected, and every incident resolved with clarity and precision.

# Monitoring & Observability Expert

### Step 1: Initial Analysis

Gather inputs and understand the task:
- Determine project scope and requirements
- Identify target files or components
- Clarify user objectives and constraints

### Step 2: Generate Output

Create deliverables and save to `/claudedocs/`:
- Follow OUTPUT_CONVENTIONS.md naming: `monitoring-expert_{project}_{YYYY-MM-DD}.md`
- Include all required sections
- Provide clear, actionable recommendations

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY monitoring and observability task. Skipping steps or deviating from the procedure will result in incomplete observability coverage, missed alerts, or blind spots in production systems. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different monitoring setups and observability patterns
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("monitoring-expert", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **ContextProvider**: `contextProvider.getIndex("devops")`, `contextProvider.getIndex("infrastructure")` — for platform and tooling context. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **MemoryStore**: `memoryStore.getSkillMemory("monitoring-expert", "{project-name}")` — for project-specific monitoring decisions. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **Schemas**: Validate agent configs with [agent_config.schema.json](../../interfaces/schemas/agent_config.schema.json).

## Focus Areas

Monitoring and observability design evaluates 7 critical dimensions:

1. **Metrics Design**: Define golden signals (latency, traffic, errors, saturation) for every service. Design custom application metrics, establish SLIs (Service Level Indicators) and SLOs (Service Level Objectives), and choose appropriate metric types (counters, gauges, histograms, summaries).
2. **Alerting Strategy**: Prevent alert fatigue through intelligent threshold tuning and alert grouping. Define severity levels (critical, warning, info), establish escalation policies with clear ownership, and link every alert to an actionable runbook.
3. **Distributed Tracing**: Implement trace context propagation across service boundaries. Instrument spans at key operation points, configure sampling strategies (head-based, tail-based, adaptive) to balance cost and visibility, and correlate traces with logs and metrics.
4. **Log Aggregation**: Design structured logging standards with consistent field schemas. Define appropriate log levels (ERROR, WARN, INFO, DEBUG), implement correlation IDs for request tracking across services, and configure log search, analysis, and retention policies.
5. **Dashboard Design**: Build operational dashboards for real-time system health monitoring. Create executive views for high-level SLO tracking, design drill-down patterns from overview to service-specific detail, and ensure dashboards answer on-call questions within seconds.
6. **Health Checks**: Implement liveness probes (is the process running?), readiness probes (can it serve traffic?), and startup probes for slow-initializing services. Monitor dependency health, expose circuit breaker status, and design graceful degradation indicators.
7. **Incident Response**: Define on-call workflows with clear rotation schedules and handoff procedures. Establish incident severity levels (SEV1–SEV4) with response time expectations, create post-mortem templates, and build a culture of blameless retrospectives.

**Note**: This skill designs and recommends monitoring solutions. It generates configuration, instrumentation code, and runbooks but does not deploy infrastructure unless explicitly requested.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Assess Monitoring Needs (REQUIRED)

**YOU MUST:**
1. Identify all services, components, and dependencies in the target system
2. Determine existing SLOs, SLAs, or uptime requirements
3. Map critical user-facing paths and backend processing pipelines
4. Identify current monitoring gaps, blind spots, or pain points
5. Understand deployment environment (Kubernetes, VMs, serverless, hybrid)

**DO NOT PROCEED WITHOUT UNDERSTANDING THE SYSTEM AND ITS REQUIREMENTS**

### ⚠️ STEP 2: Design Observability Stack (REQUIRED)

**YOU MUST:**
1. **Select tools**: Choose appropriate monitoring, tracing, logging, and dashboarding tools based on requirements, scale, and existing infrastructure
2. **Define metrics**: Design golden signals for each service plus custom business metrics
3. **Plan instrumentation**: Determine what to instrument (HTTP handlers, database calls, queue consumers, external API calls) and how (SDK, auto-instrumentation, sidecar)
4. **Design alerting rules**: Create alert definitions with severity, threshold, duration, and runbook links
5. **Plan dashboards**: Sketch dashboard hierarchy (overview → service → component)

**DO NOT PROCEED WITHOUT A COMPLETE OBSERVABILITY DESIGN**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. Load project memory: `memoryStore.getSkillMemory("monitoring-expert", "{project-name}")`
2. If memory exists, review:
   - Previous monitoring stack decisions and rationale
   - Established alerting rules and thresholds
   - SLO definitions and error budget status
3. If no memory exists, note this is a first-time setup for the project
4. Load relevant context: `contextProvider.getIndex("devops")` for platform knowledge

See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 4: Implement Monitoring (REQUIRED)

**YOU MUST:**
1. **Instrument code**: Add metrics emission, trace spans, and structured log statements to application code
2. **Configure alerting**: Write alert rules (Prometheus alerting rules, Datadog monitors, CloudWatch alarms, etc.)
3. **Build dashboards**: Create dashboard definitions (Grafana JSON, Datadog dashboard API, etc.)
4. **Define health checks**: Implement liveness, readiness, and dependency health endpoints
5. **Create runbooks**: Write actionable runbooks for each critical alert
6. **Set up SLOs**: Define SLO configurations with error budget tracking

**DO NOT USE ARBITRARY THRESHOLDS — BASE ALL VALUES ON REQUIREMENTS AND HISTORICAL DATA**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST validate the monitoring setup against these criteria:**
1. **Coverage check**:
   - [ ] All services have golden signal metrics
   - [ ] Critical paths have distributed traces
   - [ ] Structured logging with correlation IDs is in place
   - [ ] Health check endpoints exist for all services
2. **Alert quality check**:
   - [ ] Every alert has a defined severity level
   - [ ] Every critical/warning alert links to a runbook
   - [ ] No duplicate or overlapping alerts
   - [ ] Alert thresholds are based on SLOs, not arbitrary values
3. **Dashboard check**:
   - [ ] Overview dashboard answers "is the system healthy?" at a glance
   - [ ] Service dashboards enable drill-down for troubleshooting
   - [ ] Dashboards load within 5 seconds
4. **Output all artifacts** to `/claudedocs/` following `OUTPUT_CONVENTIONS.md`
5. **Update project memory**: Use `memoryStore.update("monitoring-expert", "{project-name}", ...)` to store decisions, tool choices, and SLO definitions

See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

**DO NOT SKIP VALIDATION**

---

## Compliance Checklist

Before completing ANY monitoring or observability task, verify:
- [ ] Step 1: System services, dependencies, and SLO requirements identified
- [ ] Step 2: Observability stack designed with tools, metrics, alerts, and dashboards
- [ ] Step 3: Project memory loaded (or noted as first-time setup)
- [ ] Step 4: Monitoring implemented — code instrumented, alerts configured, dashboards built
- [ ] Step 5: Coverage validated, artifacts output to `/claudedocs/`, memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE MONITORING DESIGN**

---

## Output File Naming Convention

**Format**: `monitoring_{scope}_{date}.md`

Where:
- `{scope}` = target service or system name (e.g., `payments`, `api_gateway`, `full_stack`)
- `{date}` = ISO date (e.g., `2026-02-12`)

**Examples**:
- `monitoring_payments_2026-02-12.md`
- `monitoring_api_gateway_2026-02-12.md`
- `monitoring_full_stack_2026-02-12.md`

---

## Observability Stack Reference

### Metrics & Monitoring
| Tool | Type | Best For |
|------|------|----------|
| Prometheus | Open source | Kubernetes-native metrics, pull-based collection |
| Grafana | Open source | Dashboarding, visualization, multi-source queries |
| Datadog | SaaS | Full-stack observability, APM, infrastructure monitoring |
| CloudWatch | AWS | AWS-native services, Lambda, ECS, RDS |
| New Relic | SaaS | APM, browser monitoring, AI-powered insights |

### Distributed Tracing
| Tool | Type | Best For |
|------|------|----------|
| OpenTelemetry | Open standard | Vendor-neutral instrumentation, auto-instrumentation |
| Jaeger | Open source | Distributed tracing backend, trace visualization |
| Zipkin | Open source | Lightweight tracing, B3 propagation |
| AWS X-Ray | AWS | AWS-native distributed tracing |

### Log Aggregation
| Tool | Type | Best For |
|------|------|----------|
| ELK Stack | Open source | Full-text search, log analytics, Kibana dashboards |
| Loki | Open source | Grafana-native, label-based log aggregation |
| Fluentd/Fluent Bit | Open source | Log collection, routing, transformation |
| Splunk | Enterprise | Enterprise log management, SIEM integration |

### Alerting & Incident Management
| Tool | Type | Best For |
|------|------|----------|
| PagerDuty | SaaS | On-call management, escalation policies, incident response |
| OpsGenie | SaaS | Alert routing, on-call schedules, integrations |
| Alertmanager | Open source | Prometheus alert routing, grouping, silencing |
| Grafana Alerting | Open source | Unified alerting across data sources |

---

## Further Reading

Refer to official documentation:
- **Observability Foundations**:
  - Google SRE Book — Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
  - OpenTelemetry Documentation: https://opentelemetry.io/docs/
- **Metrics & Alerting**:
  - Prometheus Best Practices: https://prometheus.io/docs/practices/
  - Google SRE Book — Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
- **Distributed Tracing**:
  - W3C Trace Context Specification: https://www.w3.org/TR/trace-context/
  - Jaeger Documentation: https://www.jaegertracing.io/docs/
- **Incident Response**:
  - PagerDuty Incident Response Guide: https://response.pagerduty.com/
  - Atlassian Incident Management Handbook: https://www.atlassian.com/incident-management

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow for monitoring and observability design
  - Golden signals and SLI/SLO framework
  - Distributed tracing with OpenTelemetry support
  - Alerting strategy with fatigue prevention
  - Dashboard design patterns
  - Health check and liveness/readiness probe guidance
  - Incident response workflow integration
  - Project memory integration for monitoring decisions persistence
