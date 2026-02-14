---
name: architecture-design
description: "Design software architectures with appropriate patterns for scale, maintainability, and team structure. Covers layered, hexagonal, event-driven, CQRS, and modular monolith architectures. Produces architecture decision records, component diagrams, and dependency maps. Prevents over-engineering, premature distribution, and architectural drift."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, architecture_decisions.md]
    - type: "shared-project"
      usage: "reference"
## tags: [architecture, design, patterns, system-design, hexagonal, cqrs, event-driven, layers]

# skill:architecture-design — Software Architecture Patterns and System Design

## Version: 1.0.0

## Purpose

Design scalable, maintainable software architectures by selecting appropriate patterns for the problem domain, team size, and scale requirements. This skill guides architectural decisions from high-level system decomposition to component-level design, producing Architecture Decision Records (ADRs), component diagrams, and dependency maps.

Use when:
- Starting a new project and choosing an architecture
- Evaluating whether to refactor a monolith
- Designing component boundaries and module structure
- Creating Architecture Decision Records (ADRs)
- Reviewing an existing architecture for drift or technical debt
- Scaling an application beyond its current architecture

## File Structure

```
skills/architecture-design/
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

### Step 1: Understand System Requirements

**YOU MUST:**
1. Identify the **system type**:
   - Web application (SPA, SSR, hybrid)
   - API/backend service
   - Data pipeline / ETL
   - Real-time system (chat, collaboration, gaming)
   - CLI tool or desktop application
   - Distributed system / platform
2. Determine **quality attribute priorities** (pick top 3):
   - **Scalability** — Handle growing load
   - **Maintainability** — Easy to modify and extend
   - **Performance** — Low latency, high throughput
   - **Reliability** — Fault tolerance, disaster recovery
   - **Security** — Data protection, access control
   - **Testability** — Easy to verify correctness
   - **Deployability** — CI/CD, independent releases
   - **Observability** — Monitoring, tracing, debugging
3. Assess **constraints**:
   - Team size and experience
   - Timeline and budget
   - Existing technology stack
   - Regulatory and compliance requirements
   - Infrastructure limitations
4. Define **scale parameters**:
   - Expected users (concurrent and total)
   - Data volume (storage and throughput)
   - Request rate (peak and average)
   - Geographic distribution

**DO NOT PROCEED WITHOUT UNDERSTANDING REQUIREMENTS AND CONSTRAINTS**

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="architecture-design"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("architecture-design", "{project-name}")` to load existing architecture context
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill insights
3. If memory exists, honor existing architectural decisions and constraints
4. If no memory exists, proceed and create it in Step 8

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Select Architecture Pattern

**YOU MUST evaluate and recommend from:**

#### Pattern Catalog

| Pattern | Best For | Team Size | Complexity |
|---------|----------|-----------|------------|
| **Layered** | CRUD apps, admin panels | 1–5 | Low |
| **Modular Monolith** | Most applications, growing teams | 3–15 | Medium |
| **Hexagonal (Ports & Adapters)** | Domain-heavy apps, high testability | 3–10 | Medium |
| **Clean Architecture** | Complex business logic, long-lived systems | 5–15 | Medium–High |
| **Event-Driven** | Async workflows, decoupled systems | 5–20 | High |

### Step 1: Initial Analysis

Gather inputs and determine scope and requirements.
| **CQRS** | Read/write asymmetry, complex queries | 5–15 | High |
| **Microservices** | Large orgs, independent deployment needs | 15+ | Very High |
| **Serverless** | Event-triggered workloads, variable traffic | 1–10 | Medium |

**Selection criteria**:
1. Start simple — choose the least complex pattern that satisfies requirements
2. Consider team experience — an unfamiliar pattern adds risk
3. Monolith first — unless there's a clear reason for distribution
4. Pattern combinations — e.g., Hexagonal + CQRS, Modular Monolith + Event-Driven

### Step 5: Design Component Structure

**YOU MUST define:**
1. **Component boundaries**:
   - Identify bounded contexts (DDD) or functional modules
   - Define public interfaces between components
   - Establish dependency rules (what depends on what)
2. **Layer definitions** (if layered):
   - Presentation / API layer
   - Application / orchestration layer
   - Domain / business logic layer
   - Infrastructure / persistence layer
3. **Communication patterns**:
   - Synchronous: Direct calls, REST, gRPC
   - Asynchronous: Events, message queues, pub/sub
   - Data sharing: Shared database, API calls, event sourcing
4. **Cross-cutting concerns**:
   - Authentication and authorization
   - Logging and observability
   - Error handling and resilience
   - Configuration management
   - Caching strategy

### Step 6: Define Architecture Decisions (ADRs)

**YOU MUST produce at least one ADR for each significant decision:**

```markdown
# ADR-{NNN}: {Title}

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Deciders**: {who}

## Context
{What is the issue and why does it matter?}

## Decision
{What was decided and why this option?}

## Consequences
### Positive
- {benefit 1}
### Negative
- {tradeoff 1}
### Risks
- {risk 1 with mitigation}

## Alternatives Considered
1. {alternative with reason for rejection}
```

### Step 7: Generate Output

- Save output to `/claudedocs/architecture-design_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Architecture overview with pattern selection rationale
  - Component diagram (ASCII or Mermaid)
  - Dependency map showing allowed and forbidden dependencies
  - ADRs for each significant decision
  - Technology recommendations
  - Migration path (if evolving from existing architecture)

### Step 8: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="architecture-design"`.

Store:
1. **architecture_decisions.md**: ADRs, pattern selection rationale, key constraints
2. **project_overview.md**: System type, quality attributes, components, dependencies, technology stack

---

## Architecture Principles

| Principle | Guideline |
|-----------|-----------|
| **Simplicity first** | The right architecture is the simplest one that satisfies requirements |
| **Dependency inversion** | High-level modules must not depend on low-level modules; both depend on abstractions |
| **Single responsibility** | Each component has one reason to change |
| **Explicit boundaries** | Component interfaces are deliberate, not accidental |
| **Evolutionary design** | Architecture should support incremental change, not require big-bang rewrites |
| **Conway's Law awareness** | Architecture will mirror team structure — design both together |

## Common Anti-Patterns to Prevent

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Distributed monolith | Use modular monolith first; split only when needed |
| Big ball of mud | Define explicit module boundaries with enforced dependency rules |
| Golden hammer | Choose patterns based on requirements, not familiarity |
| Premature optimization | Design for current scale with clear scaling strategy |
| Shared mutable state | Use events or explicit data ownership |
| Circular dependencies | Enforce acyclic dependency graph; use dependency inversion |
| Resume-driven development | Choose boring technology unless novel tech solves a real problem |

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: System type, quality attributes, constraints, and scale parameters identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Architecture pattern selected with rationale
- [ ] Step 5: Component boundaries, layers, communication patterns, and cross-cutting concerns defined
- [ ] Step 6: ADRs produced for each significant decision
- [ ] Step 7: Output saved with standard naming convention
- [ ] Step 8: Standard Memory Update pattern followed

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DESIGN**

---

## Further Reading

- **Clean Architecture** by Robert C. Martin
- **Fundamentals of Software Architecture** by Mark Richards & Neal Ford
- **Domain-Driven Design** by Eric Evans
- **Building Evolutionary Architectures** by Neal Ford, Rebecca Parsons, Patrick Kua
- **C4 Model**: https://c4model.com/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — pattern catalog, ADR framework, component design, anti-patterns |
