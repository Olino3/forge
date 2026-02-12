# Monitoring Expert Examples

This file contains example scenarios demonstrating how to use the monitoring-expert skill to design and implement observability solutions for various system architectures.

---

## Example 1: Setting Up Observability for a Microservices Architecture

### Scenario
A team is launching a microservices platform with 6 services (API Gateway, User Service, Order Service, Payment Service, Inventory Service, Notification Service) on Kubernetes. They need full observability using OpenTelemetry, Prometheus, and Grafana.

### User Prompt
```
Set up comprehensive monitoring for our microservices platform on Kubernetes
```

### Skill Execution

**Step 1 — Assess Monitoring Needs**:
- **Services**: 6 microservices running as Kubernetes Deployments
- **Critical paths**: User → API Gateway → Order Service → Payment Service → Notification Service
- **SLOs**: 99.9% availability for API Gateway, p99 latency < 500ms for order creation
- **Current state**: No monitoring beyond basic Kubernetes health checks
- **Environment**: Kubernetes 1.28 on AWS EKS, services written in Go and Node.js

**Step 2 — Design Observability Stack**:
- **Metrics**: Prometheus with kube-prometheus-stack for cluster and application metrics
- **Tracing**: OpenTelemetry SDK with OTLP exporter → Jaeger backend
- **Logging**: Fluent Bit DaemonSet → Loki → Grafana
- **Dashboards**: Grafana with overview, per-service, and infrastructure dashboards
- **Alerting**: Prometheus Alertmanager → PagerDuty (critical) / Slack (warning)

Golden signals per service:
| Service | Latency Metric | Traffic Metric | Error Metric | Saturation Metric |
|---------|---------------|----------------|--------------|-------------------|
| API Gateway | `http_request_duration_seconds` | `http_requests_total` | `http_requests_total{status=~"5.."}` | `process_open_fds / process_max_fds` |
| Order Service | `order_creation_duration_seconds` | `orders_created_total` | `order_errors_total` | `db_connection_pool_used / pool_max` |
| Payment Service | `payment_processing_duration_seconds` | `payments_processed_total` | `payment_failures_total` | `payment_queue_length` |

**Step 3 — Load Project Memory**:
```
memory = memoryStore.getSkillMemory("monitoring-expert", "ecommerce-platform")
→ No existing memory found. First-time setup.
context = contextProvider.getIndex("devops")
→ Loaded Kubernetes and Prometheus context.
```

**Step 4 — Implement Monitoring**:

OpenTelemetry instrumentation for Go services:
```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/trace"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func initTracer() (*trace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(context.Background(),
        otlptracegrpc.WithEndpoint("jaeger-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("order-service"),
        )),
    )
    otel.SetTracerProvider(tp)
    return tp, nil
}
```

Prometheus alerting rules:
```yaml
groups:
  - name: golden-signals
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          / sum(rate(http_requests_total[5m])) by (service)
          > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 1%)"
          runbook_url: "https://wiki.internal/runbooks/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency on {{ $labels.service }}"
          description: "p99 latency is {{ $value }}s (threshold: 500ms)"
          runbook_url: "https://wiki.internal/runbooks/high-latency"

      - alert: HighSaturation
        expr: |
          sum(db_connection_pool_used) by (service)
          / sum(db_connection_pool_max) by (service)
          > 0.85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Connection pool nearing saturation on {{ $labels.service }}"
          runbook_url: "https://wiki.internal/runbooks/connection-pool-saturation"
```

Kubernetes health check endpoints:
```go
// Liveness probe - is the process healthy?
http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("ok"))
})

// Readiness probe - can it serve traffic?
http.HandleFunc("/readyz", func(w http.ResponseWriter, r *http.Request) {
    if err := db.PingContext(r.Context()); err != nil {
        w.WriteHeader(http.StatusServiceUnavailable)
        w.Write([]byte("database unavailable"))
        return
    }
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("ready"))
})
```

**Step 5 — Review & Output**:
- ✅ All 6 services have golden signal metrics defined
- ✅ Distributed tracing configured with OpenTelemetry → Jaeger
- ✅ Structured logging via Fluent Bit → Loki
- ✅ Health check endpoints on all services
- ✅ Alerting rules with severity levels and runbook links
- ✅ Grafana dashboards: cluster overview, per-service, infrastructure
- Output: `/claudedocs/monitoring_ecommerce_platform_2026-02-12.md`
- Memory updated with stack decisions and SLO definitions

---

## Example 2: Designing Alerting Rules for an E-Commerce Platform

### Scenario
An e-commerce platform experiences frequent alert fatigue — the on-call team receives 200+ alerts per day, most of which are non-actionable. They need SLO-based alerting with PagerDuty integration and clear escalation policies.

### User Prompt
```
Redesign our alerting strategy to reduce alert fatigue. We use Prometheus and want SLO-based alerts with PagerDuty integration.
```

### Skill Execution

**Step 1 — Assess Monitoring Needs**:
- **Current state**: 87 alert rules, ~200 alerts/day, 80% acknowledged without action
- **Services**: Checkout, Product Catalog, Search, Recommendations, Cart, Payments
- **SLAs**: 99.95% uptime for checkout flow, 99.9% for catalog/search
- **Pain points**: Flapping alerts, no severity differentiation, missing runbooks
- **On-call team**: 5 engineers in weekly rotation

**Step 2 — Design Observability Stack**:

SLO-based alert tiers:
| Tier | Severity | Error Budget Burn Rate | Response Time | Notification |
|------|----------|----------------------|---------------|-------------|
| SEV1 | Critical | 14.4x (exhausts 30-day budget in 2 days) | 5 minutes | PagerDuty page + Slack #incidents |
| SEV2 | Warning | 6x (exhausts 30-day budget in 5 days) | 30 minutes | PagerDuty low-urgency + Slack |
| SEV3 | Info | 3x (exhausts 30-day budget in 10 days) | Next business day | Slack #alerts only |
| SEV4 | Ticket | 1x (trending toward budget exhaustion) | Sprint planning | Jira ticket auto-created |

**Step 3 — Load Project Memory**:
```
memory = memoryStore.getSkillMemory("monitoring-expert", "ecommerce-platform")
→ Loaded: monitoring_stack.md (Prometheus + Grafana), existing alert rules
→ Reviewed: Previous SLO definitions for checkout (99.95%) and catalog (99.9%)
```

**Step 4 — Implement Monitoring**:

SLO definitions and multi-window burn rate alerts:
```yaml
groups:
  - name: slo-checkout-availability
    rules:
      # SLO: 99.95% availability for checkout flow
      # Error budget: 0.05% = 21.6 minutes/month

      # SEV1: Fast burn - 14.4x burn rate over 1h (checked against 5m window)
      - alert: CheckoutSLOCriticalBurn
        expr: |
          (
            sum(rate(checkout_requests_total{status=~"5.."}[1h]))
            / sum(rate(checkout_requests_total[1h]))
          ) > (14.4 * 0.0005)
          and
          (
            sum(rate(checkout_requests_total{status=~"5.."}[5m]))
            / sum(rate(checkout_requests_total[5m]))
          ) > (14.4 * 0.0005)
        for: 2m
        labels:
          severity: critical
          slo: checkout-availability
          team: checkout
        annotations:
          summary: "Checkout availability SLO critical burn rate"
          description: "Error budget burning 14.4x faster than normal. Will exhaust 30-day budget in ~2 days at this rate."
          runbook_url: "https://wiki.internal/runbooks/checkout-slo-critical"
          pagerduty_severity: critical

      # SEV2: Slow burn - 6x burn rate over 6h (checked against 30m window)
      - alert: CheckoutSLOWarningBurn
        expr: |
          (
            sum(rate(checkout_requests_total{status=~"5.."}[6h]))
            / sum(rate(checkout_requests_total[6h]))
          ) > (6 * 0.0005)
          and
          (
            sum(rate(checkout_requests_total{status=~"5.."}[30m]))
            / sum(rate(checkout_requests_total[30m]))
          ) > (6 * 0.0005)
        for: 5m
        labels:
          severity: warning
          slo: checkout-availability
          team: checkout
        annotations:
          summary: "Checkout availability SLO elevated burn rate"
          description: "Error budget burning 6x faster than normal. Will exhaust 30-day budget in ~5 days."
          runbook_url: "https://wiki.internal/runbooks/checkout-slo-warning"
          pagerduty_severity: warning
```

Alertmanager configuration with PagerDuty routing:
```yaml
global:
  pagerduty_url: "https://events.pagerduty.com/v2/enqueue"

route:
  receiver: default-slack
  group_by: [alertname, slo, team]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: pagerduty-critical
      repeat_interval: 1h
      continue: true
    - match:
        severity: critical
      receiver: slack-incidents
    - match:
        severity: warning
      receiver: pagerduty-warning
      repeat_interval: 4h
      continue: true
    - match:
        severity: warning
      receiver: slack-alerts

receivers:
  - name: pagerduty-critical
    pagerduty_configs:
      - service_key_file: /etc/alertmanager/secrets/pagerduty-critical-key
        severity: critical
        description: "{{ .CommonAnnotations.summary }}"
        details:
          runbook: "{{ .CommonAnnotations.runbook_url }}"
          firing: "{{ .Alerts.Firing | len }}"

  - name: pagerduty-warning
    pagerduty_configs:
      - service_key_file: /etc/alertmanager/secrets/pagerduty-warning-key
        severity: warning
        description: "{{ .CommonAnnotations.summary }}"

  - name: slack-incidents
    slack_configs:
      - channel: "#incidents"
        title: "🔴 {{ .CommonAnnotations.summary }}"
        text: "{{ .CommonAnnotations.description }}\nRunbook: {{ .CommonAnnotations.runbook_url }}"

  - name: slack-alerts
    slack_configs:
      - channel: "#alerts"
        title: "🟡 {{ .CommonAnnotations.summary }}"

  - name: default-slack
    slack_configs:
      - channel: "#monitoring"
```

**Step 5 — Review & Output**:
- ✅ Reduced from 87 to 24 alert rules (SLO-based consolidation)
- ✅ Every alert has severity, runbook link, and clear ownership
- ✅ Multi-window burn rate prevents flapping
- ✅ PagerDuty integration with critical/warning differentiation
- ✅ Escalation policy: SEV1 → page immediately, SEV2 → low-urgency page, SEV3 → Slack only
- ✅ Estimated alert reduction: 200/day → ~15/day (92% reduction)
- Output: `/claudedocs/monitoring_ecommerce_alerting_2026-02-12.md`
- Memory updated with new SLO burn rate thresholds and PagerDuty routing

---

## Example 3: Adding Distributed Tracing to a Polyglot System

### Scenario
A team runs a polyglot system with Node.js (API layer) and Python (ML inference and data processing) services. They need distributed tracing with Jaeger to debug cross-service latency issues. Requests must be traceable from the API gateway through to the ML inference pipeline using correlation IDs.

### User Prompt
```
Add distributed tracing to our Node.js + Python services. We want to use Jaeger and need correlation IDs across all services.
```

### Skill Execution

**Step 1 — Assess Monitoring Needs**:
- **Services**:
  - `api-gateway` (Node.js/Express) — receives client requests
  - `recommendation-api` (Node.js/Express) — serves recommendation results
  - `ml-inference` (Python/FastAPI) — runs ML model predictions
  - `data-pipeline` (Python/Celery) — async data processing
- **Problem**: Latency spikes in recommendations; unclear which service is the bottleneck
- **Requirements**: End-to-end trace from API call to ML inference response, correlation IDs in all logs
- **Environment**: Docker Compose (dev), Kubernetes (prod)

**Step 2 — Design Observability Stack**:
- **Instrumentation**: OpenTelemetry SDKs for both Node.js and Python
- **Propagation**: W3C Trace Context headers (`traceparent`, `tracestate`)
- **Backend**: Jaeger all-in-one (dev), Jaeger with Elasticsearch (prod)
- **Correlation**: Extract trace ID as correlation ID, inject into all structured logs
- **Sampling**: Head-based 10% in production, 100% in development

**Step 3 — Load Project Memory**:
```
memory = memoryStore.getSkillMemory("monitoring-expert", "recommendation-platform")
→ No existing memory found. First-time setup.
context = contextProvider.getIndex("devops")
→ Loaded OpenTelemetry and distributed tracing context.
```

**Step 4 — Implement Monitoring**:

Node.js OpenTelemetry setup (`api-gateway/tracing.js`):
```javascript
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-grpc");
const { Resource } = require("@opentelemetry/resources");
const { ATTR_SERVICE_NAME } = require("@opentelemetry/semantic-conventions");

const sdk = new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: "api-gateway",
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://jaeger:4317",
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      "@opentelemetry/instrumentation-http": {
        ignoreIncomingPaths: ["/healthz", "/readyz"],
      },
      "@opentelemetry/instrumentation-express": { enabled: true },
    }),
  ],
});

sdk.start();
process.on("SIGTERM", () => sdk.shutdown());
```

Node.js correlation ID middleware:
```javascript
const { trace, context } = require("@opentelemetry/api");

function correlationMiddleware(req, res, next) {
  const span = trace.getActiveSpan();
  if (span) {
    const traceId = span.spanContext().traceId;
    req.correlationId = traceId;
    res.setHeader("X-Correlation-ID", traceId);
    req.log = req.log.child({ correlationId: traceId });
  }
  next();
}
```

Python OpenTelemetry setup (`ml-inference/tracing.py`):
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import logging
import os

def init_tracing(app):
    resource = Resource.create({SERVICE_NAME: "ml-inference"})
    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317"),
        insecure=True,
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()

    return provider
```

Python correlation ID middleware for FastAPI:
```python
from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        span = trace.get_current_span()
        correlation_id = format(span.get_span_context().trace_id, "032x")

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response
```

Custom span for ML inference:
```python
tracer = trace.get_tracer("ml-inference")

async def predict(request: PredictionRequest):
    with tracer.start_as_current_span(
        "ml.predict",
        attributes={
            "ml.model_name": request.model_name,
            "ml.model_version": request.model_version,
            "ml.input_features_count": len(request.features),
        },
    ) as span:
        result = model.predict(request.features)
        span.set_attribute("ml.prediction_confidence", float(result.confidence))
        span.set_attribute("ml.prediction_latency_ms", result.latency_ms)
        return result
```

Jaeger Docker Compose configuration:
```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one:1.54
    environment:
      COLLECTOR_OTLP_ENABLED: "true"
    ports:
      - "16686:16686"   # Jaeger UI
      - "4317:4317"     # OTLP gRPC
      - "4318:4318"     # OTLP HTTP

  api-gateway:
    environment:
      OTEL_EXPORTER_OTLP_ENDPOINT: "http://jaeger:4317"
      OTEL_SERVICE_NAME: "api-gateway"
    depends_on:
      - jaeger

  ml-inference:
    environment:
      OTEL_EXPORTER_OTLP_ENDPOINT: "http://jaeger:4317"
      OTEL_SERVICE_NAME: "ml-inference"
    depends_on:
      - jaeger
```

**Step 5 — Review & Output**:
- ✅ OpenTelemetry SDKs configured for both Node.js and Python
- ✅ W3C Trace Context propagation across service boundaries
- ✅ Correlation IDs extracted from trace ID and injected into all logs
- ✅ Custom spans for ML inference with model-specific attributes
- ✅ Jaeger backend configured for both dev (all-in-one) and prod (Elasticsearch)
- ✅ Auto-instrumentation for HTTP, Express, FastAPI, and requests library
- ✅ Health check paths excluded from tracing to reduce noise
- Output: `/claudedocs/monitoring_recommendation_tracing_2026-02-12.md`
- Memory updated with tracing setup, SDK versions, and sampling decisions

---

## Summary of Examples

1. **Full Observability Stack** — End-to-end setup with metrics, tracing, logging, and dashboards for microservices
2. **SLO-Based Alerting** — Alert fatigue reduction through burn rate alerts, severity tiers, and PagerDuty escalation
3. **Polyglot Distributed Tracing** — Cross-language trace propagation with correlation IDs and custom spans

## Best Practices

- Always start with golden signals (latency, traffic, errors, saturation) before custom metrics
- Use SLO-based alerting with multi-window burn rates instead of static thresholds
- Propagate trace context using W3C standard headers for vendor neutrality
- Extract trace IDs as correlation IDs to unify logs, metrics, and traces
- Exclude health check endpoints from tracing and metrics to reduce noise
- Use auto-instrumentation first, then add custom spans for business-critical operations
- Design dashboards to answer on-call questions: "Is it broken? Where? Since when?"
- Every alert must be actionable — if it doesn't require action, it shouldn't page
