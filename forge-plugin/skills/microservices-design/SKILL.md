---
name: microservices-design
description: "Design microservice architectures with proper service boundaries, communication patterns, data management, and operational concerns. Covers service decomposition, API gateways, saga patterns, service mesh, event choreography vs orchestration, and observability. Prevents distributed monoliths, data coupling, and cascade failures."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, service_catalog.md]
    - type: "shared-project"
      usage: "reference"
tags: [microservices, distributed-systems, service-mesh, saga, cqrs, api-gateway, event-driven, observability]
---

# skill:microservices-design — Microservices Patterns, Orchestration, and Service Mesh

## Version: 1.0.0

## Purpose

Design resilient microservice architectures with well-defined service boundaries, communication patterns, and operational strategies. This skill guides decisions from monolith decomposition to distributed system concerns — producing service catalogs, interaction diagrams, data ownership maps, and operational runbooks.

Use when:
- Decomposing a monolith into microservices
- Designing a new distributed system from scratch
- Establishing inter-service communication patterns
- Implementing distributed transactions (saga patterns)
- Designing observability and resilience strategies
- Evaluating whether microservices are the right choice

## File Structure

```
skills/microservices-design/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Assess Microservices Readiness

**YOU MUST:**
1. **Evaluate whether microservices are warranted**:
   - Team size ≥ 15 developers? (smaller teams rarely benefit)
   - Independent deployment requirement? (features on different release cycles)
   - Diverse scaling needs? (one component needs 10x the capacity)
   - Organizational boundaries? (separate teams owning separate domains)
   - Technology diversity requirement? (some components need different stacks)
2. **If the answer to most is "no"** — recommend a modular monolith instead and document the decision as an ADR
3. **Identify the system scope**:
   - Greenfield distributed system
   - Monolith decomposition
   - Existing microservices optimization
   - Service boundary redesign
4. **Determine constraints**:
   - Team structure and expertise
   - Infrastructure maturity (Kubernetes, service mesh, CI/CD)
   - Latency and throughput requirements
   - Consistency requirements (strong, eventual, causal)
   - Regulatory and compliance constraints

**DO NOT PROCEED WITHOUT VALIDATING MICROSERVICES READINESS**

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="microservices-design"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("microservices-design", "{project-name}")` to load existing service catalog
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill insights
3. If memory exists, honor existing service boundaries and data ownership
4. If no memory exists, proceed and create it in Step 9

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Define Service Boundaries

**YOU MUST:**
1. **Use Domain-Driven Design** to identify bounded contexts:
   - Map the domain model — entities, aggregates, domain events
   - Identify bounded contexts — areas with distinct ubiquitous language
   - One service per bounded context (not per entity)
2. **Validate boundaries with the litmus tests**:
   - Can this service be deployed independently?
   - Does this service own its data without sharing a database?
   - Can the team owning this service make changes without coordinating with other teams?
   - Does this service have a clear, cohesive purpose?
3. **Produce a service catalog**:

| Service | Domain | Owner | Data Store | Key Entities |
|---------|--------|-------|------------|-------------|
| user-service | Identity | Team Auth | PostgreSQL | User, Role, Session |
| order-service | Commerce | Team Commerce | PostgreSQL | Order, OrderItem |
| inventory-service | Warehouse | Team Supply | PostgreSQL + Redis | Product, Stock |
| notification-service | Communication | Team Platform | MongoDB | Template, Delivery |

### Step 5: Design Communication Patterns

**YOU MUST define:**
1. **Synchronous communication** (request-response):
   - REST over HTTP/2 — simple, widely supported
   - gRPC — high performance, strong typing, bidirectional streaming
   - Use for: Queries, real-time user-facing requests
   - Always implement: Timeouts, retries with exponential backoff, circuit breakers
2. **Asynchronous communication** (event-driven):
   - Message broker (Kafka, RabbitMQ, NATS) for domain events
   - Use for: Cross-service data propagation, workflows, notifications
   - Event types:
     - **Domain events**: `OrderPlaced`, `PaymentProcessed`, `UserRegistered`
     - **Integration events**: Published for other services to consume
     - **Command events**: Directed to a specific service for action
3. **Choose choreography vs orchestration**:
   - **Choreography**: Services react to events independently (no central coordinator)
     - Better for: Simple workflows, loosely coupled services
     - Risk: Hard to understand the full workflow; debugging is difficult
   - **Orchestration**: A coordinator service manages the workflow
     - Better for: Complex multi-step workflows, visibility into process state
     - Risk: Central coordinator becomes a bottleneck or single point of failure

### Step 6: Design Data Management

**YOU MUST address:**
1. **Database per service** — each service owns its data exclusively:
   - No shared databases between services
   - No direct database access from other services
   - Data accessed only through the owning service's API
2. **Data consistency patterns**:
   - **Saga pattern** for distributed transactions:
     - Choreography-based: Each service publishes events and listens for failures
     - Orchestration-based: A saga coordinator manages the workflow
   - **Eventual consistency**: Accept that data across services will be temporarily inconsistent
   - **CQRS**: Separate read models updated via events for cross-service queries
3. **Data duplication strategy**:
   - Services may store local copies of data they need frequently
   - Local copies updated via domain events
   - Source-of-truth is always the owning service
4. **Example Saga — Order Placement**:

```
    Order Service          Payment Service        Inventory Service
         │                       │                       │
    ┌────▼────┐                  │                       │
    │ Create  │ ──OrderCreated──►│                       │
    │ Order   │                  │                       │
    └─────────┘            ┌─────▼─────┐                 │
                           │ Process   │ ──PaymentOK────►│
                           │ Payment   │                 │
                           └───────────┘           ┌─────▼─────┐
                                                   │ Reserve   │
                                                   │ Stock     │
                                                   └─────┬─────┘
                                                         │
                           ◄──StockReserved──────────────┘
         │
    ┌────▼────┐
    │ Confirm │
    │ Order   │
    └─────────┘

    Compensating actions on failure:
    - StockFailed → Payment.Refund → Order.Cancel
    - PaymentFailed → Order.Cancel
```

### Step 7: Design Operational Concerns

**YOU MUST address:**
1. **API Gateway**:
   - Single entry point for all external traffic
   - Handles: Authentication, rate limiting, request routing, TLS termination
   - Options: Kong, Envoy, AWS API Gateway, Azure API Management
2. **Service mesh** (for internal traffic):
   - Handles: mTLS, load balancing, retries, circuit breaking, observability
   - Options: Istio, Linkerd, Consul Connect
   - Implement when: ≥ 10 services or strict security requirements
3. **Observability** — the three pillars:
   - **Logs**: Structured JSON logs with correlation IDs
   - **Metrics**: RED method (Rate, Errors, Duration) per service
   - **Traces**: Distributed tracing (OpenTelemetry) across service calls
4. **Resilience patterns**:
   - **Circuit breaker**: Stop calling a failing service (fail fast)
   - **Bulkhead**: Isolate failures to prevent cascade
   - **Retry with backoff**: Retry transient failures with exponential delay
   - **Timeout**: Every inter-service call must have a timeout
   - **Fallback**: Gracefully degrade when a dependency is unavailable
5. **Deployment strategy**:
   - Independent deployment per service (no coordinated releases)
   - Blue-green or canary deployments
   - Feature flags for gradual rollout
   - Contract testing between services (Pact, schema registry)

### Step 8: Generate Output

- Save output to `/claudedocs/microservices-design_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Service catalog with ownership and data stores
  - Interaction diagram (ASCII or Mermaid)
  - Communication pattern decisions (sync/async per interaction)
  - Data ownership map
  - Saga definitions for distributed workflows
  - Operational concerns (gateway, mesh, observability, resilience)
  - ADRs for key decisions

### Step 9: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="microservices-design"`.

Store:
1. **service_catalog.md**: Service inventory, boundaries, data ownership, communication patterns
2. **project_overview.md**: System scope, team structure, infrastructure, key constraints

---

## Microservices Design Principles

| Principle | Guideline |
|-----------|-----------|
| **Single responsibility** | Each service does one thing well |
| **Autonomy** | Services can be developed, deployed, and scaled independently |
| **Data sovereignty** | Each service owns its data; no shared databases |
| **Resilience** | Design for failure; every dependency will fail eventually |
| **Evolutionary** | Start with fewer, larger services; split when complexity warrants |
| **Smart endpoints, dumb pipes** | Business logic in services, not in message brokers |
| **Decentralized governance** | Teams choose their own tech stack within guardrails |

## Common Anti-Patterns to Prevent

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Distributed monolith | Services must be independently deployable |
| Shared database | Database per service; sync via events |
| Synchronous chains (A→B→C→D) | Use async events or aggregate at gateway |
| Entity-based services (UserService, OrderService for simple CRUD) | Bounded-context-based services with cohesive domain logic |
| No circuit breakers | Every sync call needs timeout + circuit breaker |
| Chatty services (many small calls) | Batch or aggregate calls; use async where possible |
| Ignoring Conway's Law | Align service boundaries with team boundaries |
| Testing in production only | Contract tests + integration tests in CI |

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: Microservices readiness validated (or modular monolith recommended)
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Service boundaries defined with DDD bounded contexts
- [ ] Step 5: Communication patterns (sync/async, choreography/orchestration) defined
- [ ] Step 6: Data management — ownership, sagas, consistency patterns addressed
- [ ] Step 7: Operational concerns — gateway, mesh, observability, resilience addressed
- [ ] Step 8: Output saved with standard naming convention
- [ ] Step 9: Standard Memory Update pattern followed

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DESIGN**

---

## Further Reading

- **Building Microservices** by Sam Newman
- **Microservices Patterns** by Chris Richardson
- **Domain-Driven Design** by Eric Evans
- **Release It!** by Michael T. Nygard
- **Microservices.io Patterns**: https://microservices.io/patterns/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — service decomposition, communication, sagas, data ownership, operational concerns |
