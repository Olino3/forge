---
id: "engineering/architecture_patterns"
domain: engineering
title: "Architecture Patterns"
type: reference
estimatedTokens: 400
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Pattern Decision Matrix"
    estimatedTokens: 78
    keywords: [pattern, decision, matrix]
  - name: "When to Use Each"
    estimatedTokens: 85
    keywords: [each]
  - name: "Tradeoffs Summary"
    estimatedTokens: 48
    keywords: [tradeoffs, summary]
  - name: "References"
    estimatedTokens: 14
    keywords: [references]
tags: [engineering, architecture, microservices, clean-architecture, cqrs, event-driven]
---

# Architecture Patterns

Decision matrix for selecting architecture patterns. Use during `/brainstorm`, `/implement`, or architectural code reviews.

## Pattern Decision Matrix

| Pattern | Best For | Team Size | Complexity | Scalability |
|---------|----------|-----------|------------|-------------|
| **Monolith** | MVPs, small apps, rapid prototyping | 1-5 | Low | Vertical |
| **Clean Architecture** | Domain-heavy apps, long-lived projects | 3-10 | Medium | Vertical |
| **Hexagonal (Ports & Adapters)** | Integration-heavy apps, testability focus | 3-10 | Medium | Vertical |
| **CQRS** | Read/write asymmetry, event sourcing | 5-15 | High | Horizontal |
| **Event-Driven** | Async workflows, decoupled systems | 5-20 | High | Horizontal |
| **Microservices** | Large teams, independent deployment | 10+ | Very High | Horizontal |

## When to Use Each

### Monolith
- Starting a new project with unclear requirements
- Small team that deploys together
- Simple domain with mostly CRUD operations

### Clean / Hexagonal Architecture
- Complex business logic that needs isolation
- Multiple external integrations (APIs, databases, queues)
- Long-term project with evolving requirements

### CQRS + Event Sourcing
- Read-heavy systems with different read/write models
- Audit trail requirements (financial, compliance)
- Complex domain events that trigger workflows

### Event-Driven
- Multiple services need to react to the same events
- Asynchronous processing requirements
- Loose coupling between bounded contexts

### Microservices
- Large organization with multiple teams
- Services with different scaling requirements
- Independent deployment cycles needed

## Tradeoffs Summary

| Tradeoff | Simple (Monolith) | Complex (Microservices) |
|----------|-------------------|------------------------|
| Initial velocity | Fast | Slow |
| Long-term velocity | Decreasing | Stable |
| Deployment | Simple | Complex (CI/CD required) |
| Debugging | Easy (single process) | Hard (distributed tracing) |
| Data consistency | ACID transactions | Eventual consistency |
| Team autonomy | Low | High |

## References

- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [Martin Fowler - Microservices](https://martinfowler.com/articles/microservices.html)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

*Last Updated: 2026-02-10*
