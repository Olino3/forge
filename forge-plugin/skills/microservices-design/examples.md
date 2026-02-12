# Microservices Design Examples

This file contains example scenarios demonstrating how to use the microservices-design skill for various distributed system design tasks.

---

## Example 1: E-Commerce Platform Decomposition

### Scenario
A growing e-commerce company (25 developers, 3 teams) needs to decompose their monolith into microservices. The monolith handles products, orders, payments, shipping, and notifications.

### User Prompt
```
Design a microservices architecture for our e-commerce platform. We have 25 developers in 3 teams and need independent deployment.
```

### Skill Execution

**Step 1 — Readiness Assessment**:
- Team size: 25 (sufficient)
- Independent deployment: Yes — shipping team blocked by payment team releases
- Scaling diversity: Yes — catalog reads 50x more than order writes
- Organizational boundaries: 3 teams with distinct domains
- **Verdict: Microservices warranted**

**Step 4 — Service Boundaries**:

| Service | Bounded Context | Team | Data Store | Scaling Profile |
|---------|----------------|------|------------|----------------|
| catalog-service | Product Catalog | Team Catalog | PostgreSQL + Elasticsearch | High read, low write |
| order-service | Order Management | Team Commerce | PostgreSQL | Medium read/write |
| payment-service | Payment Processing | Team Commerce | PostgreSQL (encrypted) | Low volume, high security |
| shipping-service | Fulfillment | Team Logistics | PostgreSQL | Batch-oriented |
| notification-service | Communication | Team Platform | MongoDB | High write, fire-and-forget |
| user-service | Identity & Access | Team Platform | PostgreSQL + Redis | High read (auth checks) |

**Step 5 — Communication Patterns**:

```markdown
## Service Interactions

### Synchronous (REST/gRPC)
- Web → API Gateway → catalog-service (product search, browsing)
- Web → API Gateway → order-service (place order, order history)
- order-service → payment-service (process payment — gRPC)
- order-service → user-service (validate user — gRPC)

### Asynchronous (Kafka Events)
- order-service → OrderPlaced → payment-service, notification-service
- payment-service → PaymentProcessed → order-service, shipping-service
- payment-service → PaymentFailed → order-service (saga compensation)
- shipping-service → ShipmentDispatched → notification-service, order-service
- catalog-service → ProductUpdated → order-service (price validation cache)

## Interaction Diagram

    ┌──────────┐
    │   Web    │
    │   App    │
    └────┬─────┘
         │ HTTPS
    ┌────▼─────────┐
    │  API Gateway  │ (Kong)
    │  Auth + Rate  │
    └──┬───┬───┬───┘
       │   │   │  REST/gRPC
    ┌──▼┐ ┌▼──┐ ┌▼──────┐
    │Cat│ │Ord│ │User   │
    │log│ │er │ │Service│
    └───┘ └┬──┘ └───────┘
           │ gRPC
       ┌───▼────┐
       │Payment │
       └───┬────┘
           │ Kafka: PaymentProcessed
    ┌──────▼───────┐
    │  Shipping    │
    └──────┬───────┘
           │ Kafka: ShipmentDispatched
    ┌──────▼───────┐
    │ Notification │
    └──────────────┘
```

**Step 6 — Saga: Order Placement**:

```markdown
## Order Placement Saga (Orchestration)

Coordinator: order-service

1. order-service: Create order (status: PENDING)
2. order-service → payment-service: ProcessPayment
   - Success → continue
   - Failure → Cancel order (compensate)
3. order-service → catalog-service: ReserveInventory
   - Success → continue
   - Failure → Refund payment → Cancel order (compensate)
4. order-service: Confirm order (status: CONFIRMED)
5. order-service → notification-service: SendOrderConfirmation
6. order-service → shipping-service: CreateShipment

## Compensating Actions

| Step Failed | Compensations (in order) |
|------------|--------------------------|
| Payment | Cancel order |
| Inventory | Refund payment → Cancel order |
| Shipping | Release inventory → Refund payment → Cancel order |
```

**Step 7 — Operational Concerns**:

```markdown
## Observability Stack

| Pillar | Tool | Implementation |
|--------|------|---------------|
| Logs | ELK Stack | Structured JSON, correlation ID in all logs |
| Metrics | Prometheus + Grafana | RED metrics per service, SLO dashboards |
| Traces | Jaeger (OpenTelemetry) | Auto-instrumented with OTel SDK |

## Resilience Configuration

| Pattern | Configuration |
|---------|--------------|
| Timeout | 3s for service-to-service, 10s for external APIs |
| Retry | 3 retries, exponential backoff (100ms, 500ms, 2s) |
| Circuit breaker | Open after 5 failures in 30s, half-open after 60s |
| Bulkhead | 10 concurrent connections per downstream service |
```

**Step 8 — Output**:
File: `/claudedocs/microservices-design_ecommerce_2025-01-15.md`

---

## Example 2: Event-Driven Financial System

### Scenario
A fintech company needs a distributed system for processing real-time transactions with strict audit trail and regulatory compliance requirements.

### User Prompt
```
Design a microservices architecture for real-time transaction processing with full audit trail and compliance requirements
```

### Skill Execution

**Step 1 — Readiness Assessment**:
- Team: 30 developers across 5 teams
- Independent deployment: Critical — compliance changes must ship instantly
- Scaling: Transaction processing 100K TPS peak, audit trail is write-heavy
- **Verdict: Microservices warranted** (strong regulatory and scaling reasons)

**Step 4 — Service Boundaries**:

| Service | Domain | Consistency | Key Requirement |
|---------|--------|-------------|-----------------|
| transaction-processor | Core Processing | Strong | Sub-100ms latency |
| fraud-detector | Risk Assessment | Eventual | ML model scoring |
| ledger-service | Accounting | Strong | Double-entry bookkeeping |
| audit-service | Compliance | Append-only | Immutable audit log |
| notification-service | Communication | Eventual | Multi-channel delivery |
| account-service | Account Mgmt | Strong | Balance accuracy |

**Step 5 — Communication: Event Sourcing**:

```markdown
## Architecture: Event Sourcing + CQRS

Every state change is captured as an immutable event.
The event log IS the source of truth, not the database.

### Event Flow

    Transaction         Event           Consumers
    Request             Store
                        (Kafka)
    ┌───────────┐  ┌────────────┐  ┌──────────────┐
    │ Process   ├──► TxnCreated ├──► Fraud Check   │
    │ Payment   │  │ TxnScored  │  │ (async)       │
    └───────────┘  │ TxnApproved│  ├──────────────┤
                   │ TxnSettled │  │ Ledger Update │
                   │ TxnFailed  │  │ (async)       │
                   └─────┬──────┘  ├──────────────┤
                         │         │ Audit Log    │
                         │         │ (append-only)│
                         │         ├──────────────┤
                         │         │ Notification │
                         │         │ (async)      │
                         │         ├──────────────┤
                         │         │ Read Model   │
                         │         │ Projector    │
                         └─────────┴──────────────┘

### Event Schema

    {
      "eventId": "evt_a1b2c3",
      "eventType": "TransactionApproved",
      "aggregateId": "txn_x1y2z3",
      "timestamp": "2025-01-15T10:30:00.123Z",
      "version": 3,
      "payload": {
        "amount": { "value": 15000, "currency": "USD" },
        "fromAccount": "acc_sender",
        "toAccount": "acc_receiver"
      },
      "metadata": {
        "correlationId": "req_m1n2o3",
        "causationId": "evt_prev",
        "userId": "user_officer1"
      }
    }

### Compliance Requirements

| Requirement | Implementation |
|------------|---------------|
| Immutable audit trail | Event store is append-only; no updates or deletes |
| Data retention (7 years) | Cold storage tier for events > 1 year old |
| PII protection | Events encrypted at rest; PII in separate encrypted store |
| Regulatory reporting | Materialized views rebuilt from event stream on demand |
```

**Step 8 — Output**:
File: `/claudedocs/microservices-design_fintech_2025-01-15.md`

---

## Example 3: Recommending Against Microservices

### Scenario
A 4-person startup team wants to build their MVP with microservices because they expect to scale to millions of users someday.

### User Prompt
```
We're a startup with 4 engineers building an MVP. Design a microservices architecture for our todo app.
```

### Skill Execution

**Step 1 — Readiness Assessment**:
- Team size: 4 (too small for microservices)
- Independent deployment: Not needed yet (single team, single release)
- Scaling diversity: No (todo app has uniform scaling needs)
- Organizational boundaries: One team
- **Verdict: Microservices NOT warranted**

```markdown
## Recommendation: Modular Monolith

### Why Not Microservices

| Factor | Your Situation | Microservices Threshold |
|--------|---------------|------------------------|
| Team size | 4 developers | 15+ developers |
| Deployment needs | Single release cycle | Multiple independent cycles |
| Scale diversity | Uniform load | 10x difference between components |
| Domain complexity | Simple CRUD | Multiple bounded contexts |
| Infrastructure maturity | Basic CI/CD | Kubernetes, service mesh, observability |

### The Cost of Premature Microservices

For a 4-person team, microservices would add:
- **Operational overhead**: Service mesh, distributed tracing, log aggregation
- **Development overhead**: API contracts, schema registry, contract testing
- **Debugging complexity**: Distributed tracing instead of stack traces
- **Infrastructure cost**: 6+ deployments instead of 1

### Recommended Architecture

    ┌─────────────────────────────────────┐
    │         Modular Monolith             │
    │                                     │
    │  ┌──────────┐  ┌──────────┐        │
    │  │  Users   │  │  Todos   │        │
    │  │  Module  │  │  Module  │        │
    │  └──────────┘  └──────────┘        │
    │  ┌──────────┐  ┌──────────┐        │
    │  │  Teams   │  │  Notifs  │        │
    │  │  Module  │  │  Module  │        │
    │  └──────────┘  └──────────┘        │
    │                                     │
    │  ── Module Event Bus (in-process) ──│
    │                                     │
    │          PostgreSQL                  │
    │     (schema-per-module)             │
    └─────────────────────────────────────┘

### When to Revisit

Reconsider microservices when:
- Team grows to 10+ developers
- Modules develop different scaling needs
- Release coordination becomes a bottleneck
- Module boundaries are stable and well-tested

The modular monolith with enforced boundaries makes future extraction
straightforward because the module interfaces are already defined.
```

**ADR**:

```markdown
# ADR-001: Modular Monolith Over Microservices for MVP

**Status**: Accepted
**Date**: 2025-01-15

## Decision
Use a modular monolith architecture for the MVP phase.
Module boundaries are enforced through schema-per-module
database isolation and an in-process event bus.

## Rationale
A 4-person team building an MVP does not have the organizational
or technical need for distributed services. The operational overhead
of microservices would consume 30-40% of engineering capacity that
should be spent on product development.
```

**Step 8 — Output**:
File: `/claudedocs/microservices-design_startup-todo_2025-01-15.md`

---

## Summary of Use Cases

1. **E-Commerce decomposition** — Full service catalog, saga orchestration, and operational stack
2. **Event-sourced financial system** — CQRS, immutable audit trails, compliance patterns
3. **Recommending against microservices** — When a modular monolith is the better choice

## Best Practices

- Always validate microservices readiness before designing — the biggest mistake is choosing microservices when they're not needed
- Define service boundaries using DDD bounded contexts, not entity types
- Every synchronous call is a potential cascade failure — use circuit breakers universally
- Embrace eventual consistency — strong consistency across services is extremely expensive
- Design sagas for every multi-service workflow — identify compensating actions upfront
- Instrument everything from day one — you cannot debug distributed systems without observability
- Contract test all service boundaries — integration tests alone are insufficient
