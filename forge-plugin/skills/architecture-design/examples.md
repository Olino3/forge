# Architecture Design Examples

This file contains example scenarios demonstrating how to use the architecture-design skill for various system design tasks.

---

## Example 1: SaaS Platform — Modular Monolith

### Scenario
A startup (team of 6) is building a B2B SaaS project management tool. They need an architecture that supports rapid feature development now with a clear path to scale later.

### User Prompt
```
Design the architecture for our SaaS project management platform. We have 6 developers, expect 10K users in year one, and need to ship fast.
```

### Skill Execution

**Step 1 — Requirements**:
- System type: Web application (SPA + API backend)
- Quality attributes: Maintainability (top), Deployability, Testability
- Team: 6 developers, mixed experience
- Scale: 10K users year one, 100K year three
- Constraints: Ship MVP in 3 months, PostgreSQL required (existing expertise)

**Step 4 — Pattern Selection**:

**Selected: Modular Monolith**

| Considered | Verdict | Reason |
|-----------|---------|--------|
| Layered | Rejected | Insufficient module isolation for 6 devs |
| Modular Monolith | **Selected** | Right balance of simplicity and structure |
| Microservices | Rejected | Premature for team size and scale |
| Hexagonal | Partial adoption | Used within each module |

**Step 5 — Component Structure**:

```
┌─────────────────────────────────────────────────┐
│                   API Gateway                     │
│              (Auth, Rate Limiting)                 │
└──────────┬──────────┬──────────┬─────────────────┘
           │          │          │
    ┌──────▼──┐ ┌─────▼────┐ ┌──▼─────────┐
    │ Projects │ │  Users   │ │ Billing    │
    │ Module   │ │  Module  │ │ Module     │
    │          │ │          │ │            │
    │ - Tasks  │ │ - Auth   │ │ - Plans    │
    │ - Boards │ │ - Teams  │ │ - Invoices │
    │ - Files  │ │ - Roles  │ │ - Payments │
    └──────────┘ └──────────┘ └────────────┘
           │          │          │
    ┌──────▼──────────▼──────────▼─────────┐
    │         Shared Kernel                  │
    │   (Events, Base Models, Utils)         │
    └──────────────────┬───────────────────┘
                       │
    ┌──────────────────▼───────────────────┐
    │           PostgreSQL                   │
    │   (Schema-per-module isolation)        │
    └──────────────────────────────────────┘
```

**Dependency Rules**:
- Modules communicate only through the Shared Kernel event bus
- No direct imports between module internals
- Each module owns its database schema (no cross-module joins)
- Shared Kernel contains only domain events, base types, and utilities

**Step 6 — ADR**:

```markdown
# ADR-001: Modular Monolith Over Microservices

**Status**: Accepted
**Date**: 2025-01-15
**Deciders**: Engineering Lead, CTO

## Context
Building a SaaS product management tool with a 6-person team targeting
10K users in year one. Need to ship MVP in 3 months.

## Decision
Adopt a modular monolith with strict module boundaries enforced through
schema-per-module database isolation and an internal event bus. Each module
follows hexagonal architecture internally.

## Consequences
### Positive
- Single deployment unit — simple CI/CD for small team
- Module boundaries provide clear ownership per team pair
- Can extract modules to services later if needed
### Negative
- Must enforce boundaries through code review (no physical separation)
- Shared database instance (though schemas are isolated)
### Risks
- Module coupling creep — mitigated by CI lint rules checking imports
```

**Step 7 — Output**:
File: `/claudedocs/architecture-design_saas-pm_2025-01-15.md`

---

## Example 2: Real-Time Collaboration — Event-Driven Architecture

### Scenario
A team needs to design a real-time document collaboration system (like Google Docs) supporting concurrent editing, presence indicators, and version history.

### User Prompt
```
Design the architecture for a real-time collaborative document editor supporting 500 concurrent editors per document
```

### Skill Execution

**Step 1 — Requirements**:
- System type: Real-time collaboration platform
- Quality attributes: Performance (top), Reliability, Scalability
- Scale: 500 concurrent editors per document, 50K total concurrent users
- Constraints: Sub-100ms latency for edits, eventual consistency acceptable

**Step 4 — Pattern Selection**:

**Selected: Event-Driven + CQRS**

Rationale: Read/write asymmetry (many reads, fewer writes), real-time requirements demand event streaming, conflict resolution needs event sourcing.

**Step 5 — Component Structure**:

```
┌─────────────────────────────────────────────────────┐
│                    Clients (SPA)                      │
│    WebSocket ──── REST API ──── SSE (presence)        │
└────────┬──────────────┬───────────────┬──────────────┘
         │              │               │
┌────────▼────────┐ ┌───▼──────────┐ ┌──▼────────────┐
│  Collaboration  │ │  Document    │ │  Presence      │
│  Gateway        │ │  Service     │ │  Service       │
│  (WebSocket)    │ │  (REST/CRUD) │ │  (Redis PubSub)│
└────────┬────────┘ └───┬──────────┘ └───────────────┘
         │              │
    ┌────▼──────────────▼────┐
    │     Event Bus          │
    │     (Kafka/NATS)       │
    └────┬──────────┬────────┘
         │          │
┌────────▼────┐ ┌───▼──────────────┐
│  Event      │ │  Read Model      │
│  Store      │ │  Projector       │
│  (Write)    │ │  (Materialized   │
│             │ │   views)         │
└─────────────┘ └──────────────────┘
```

**Key Decisions**:
- **CRDT** (Conflict-free Replicated Data Types) for concurrent edit resolution
- **Event sourcing** for full document version history (every edit is an event)
- **CQRS** separates write path (event store) from read path (materialized views)
- **WebSocket** for real-time edit broadcasting
- **Redis PubSub** for lightweight presence tracking

**Step 7 — Output**:
File: `/claudedocs/architecture-design_collab-editor_2025-01-15.md`

---

## Example 3: Legacy Monolith Modernization

### Scenario
A 10-year-old monolithic application (PHP, 500K lines) is becoming unmaintainable. The team needs a modernization strategy that doesn't require a rewrite.

### User Prompt
```
Design a modernization strategy for our legacy PHP monolith. We can't do a big-bang rewrite — it needs to be incremental.
```

### Skill Execution

**Step 1 — Requirements**:
- System type: Legacy monolith modernization
- Quality attributes: Maintainability (top), Deployability, Testability
- Team: 12 developers, some with only PHP experience
- Constraints: Zero downtime during migration, incremental approach mandatory

**Step 4 — Pattern: Strangler Fig**:

```markdown
## Modernization Strategy: Strangler Fig Pattern

### Phase 1: Establish Facade (Month 1-2)
- Deploy API gateway in front of the monolith
- Route all traffic through the gateway
- No behavior changes — pure passthrough

### Phase 2: Extract Authentication (Month 3-4)
- First module extracted: User auth → new Node.js service
- Gateway routes /auth/* to new service
- Monolith delegates auth checks to new service via API
- Shared session store (Redis) during transition

### Phase 3: Strangle High-Value Modules (Month 5-12)
- Extract in order of business value and coupling:
  1. Payments (high value, low coupling)
  2. Notifications (medium value, low coupling)
  3. Product catalog (high value, medium coupling)
  4. Order management (high value, high coupling — last)

### Phase 4: Decommission Monolith (Month 12-18)
- Remaining low-value features rewritten or retired
- Monolith database migrated to per-service databases
- Legacy codebase archived

## Anti-Corruption Layer

    ┌──────────────────────────────┐
    │         API Gateway          │
    └─────┬──────────┬─────────────┘
          │          │
    ┌─────▼───┐ ┌───▼───────────┐
    │ New     │ │ Anti-Corruption│
    │ Service │ │ Layer (ACL)    │
    └─────────┘ └───┬───────────┘
                    │
              ┌─────▼──────────┐
              │ Legacy Monolith│
              └────────────────┘

The ACL translates between new service contracts and legacy
monolith interfaces, preventing legacy concepts from leaking
into new services.
```

**Step 6 — ADR**:

```markdown
# ADR-001: Strangler Fig Over Big-Bang Rewrite

**Status**: Accepted

## Context
500K-line PHP monolith, 12 developers, zero-downtime requirement.

## Decision
Use Strangler Fig pattern with API gateway as the routing layer.
Extract modules incrementally based on business value and coupling.

## Consequences
### Positive
- Zero downtime — old and new systems coexist
- Incremental delivery — each extraction provides immediate value
- Risk reduction — rollback to monolith always possible
### Negative
- Dual maintenance during transition (12-18 months)
- Increased infrastructure complexity (gateway + services + monolith)
### Risks
- Team fatigue from maintaining two systems — mitigated by extracting
  highest-value modules first for early wins
```

**Step 7 — Output**:
File: `/claudedocs/architecture-design_legacy-modernization_2025-01-15.md`

---

## Example 4: Hexagonal Architecture for Domain-Heavy Application

### Scenario
An insurance company needs a claims processing system with complex business rules that frequently change based on regulations.

### User Prompt
```
Design an architecture for our insurance claims system where business rules change quarterly based on regulations
```

### Skill Execution

**Step 4 — Pattern: Hexagonal Architecture**:

```markdown
## Hexagonal Architecture (Ports & Adapters)

### Core Principle
Business logic has ZERO dependencies on infrastructure. External
concerns (databases, APIs, UI) connect through defined ports.

### Structure

             ┌──────────────────────────────┐
    Driving   │                              │  Driven
    Adapters  │      Domain Core             │  Adapters
              │                              │
    ┌─────┐   │  ┌────────────────────┐      │   ┌──────────┐
    │ REST├───►──►  Claims            │      ├───► PostgreSQL│
    │ API │   │  │  Processing        │      │   └──────────┘
    └─────┘   │  │  Rules Engine      │      │   ┌──────────┐
    ┌─────┐   │  │  Policy Validation │      ├───► Email     │
    │ CLI ├───►──►                    │      │   │ Service   │
    └─────┘   │  └────────────────────┘      │   └──────────┘
    ┌─────┐   │                              │   ┌──────────┐
    │Event├───►──►  Ports (interfaces)       ├───► Regulatory│
    │ Bus │   │                              │   │ API       │
    └─────┘   │                              │   └──────────┘
              └──────────────────────────────┘

### Ports (Interfaces)

**Driving Ports** (input):
- `ClaimSubmissionPort` — Submit a new claim
- `ClaimReviewPort` — Review and adjudicate a claim
- `PolicyQueryPort` — Query policy coverage

**Driven Ports** (output):
- `ClaimRepository` — Persist and retrieve claims
- `NotificationPort` — Send notifications to claimants
- `RegulatoryCompliancePort` — Validate against current regulations
- `PaymentPort` — Issue claim payments

### Why Hexagonal for This System
1. **Regulatory changes**: Business rules in the domain core change quarterly;
   infrastructure adapters remain stable
2. **Testability**: Domain core tested without any infrastructure (pure unit tests)
3. **Adapter swapability**: Switch from email to SMS notifications without
   touching business logic
4. **Multiple entry points**: REST API, CLI batch processing, and event-driven
   triggers all use the same domain logic
```

**Step 7 — Output**:
File: `/claudedocs/architecture-design_claims-system_2025-01-15.md`

---

## Summary of Use Cases

1. **Greenfield SaaS platform** — Modular monolith with clear module boundaries and scaling path
2. **Real-time collaboration** — Event-driven + CQRS with event sourcing and WebSocket streaming
3. **Legacy modernization** — Strangler Fig pattern for incremental migration without downtime
4. **Domain-heavy regulation system** — Hexagonal architecture isolating volatile business rules

## Best Practices

- Always start with the simplest architecture that meets requirements
- Consider Conway's Law — align architecture with team structure
- Document decisions in ADRs, not just the outcome but the reasoning
- Design for evolutionary architecture — make it easy to change later
- Validate architecture against quality attribute scenarios, not just functional requirements
- A diagram without dependency rules is incomplete — always specify what can and cannot depend on what
