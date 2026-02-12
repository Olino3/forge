---
name: fullstack-development
description: Full-stack development oversight and architecture spanning frontend, backend, database, and infrastructure layers. Evaluates technology choices, enforces architectural consistency across the entire application stack, designs API contracts, manages cross-layer data flow, and ensures cohesive integration between all system tiers. Like Hephaestus orchestrating the elements of a grand automaton, this skill ensures every layer of the stack works in harmony — from the user interface down to the database and infrastructure beneath.
---

# Full-Stack Development Oversight

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY full-stack development task. Skipping steps or deviating from the procedure will result in fragmented architectures, misaligned layers, and integration failures. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different full-stack architecture tasks
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("fullstack-development", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **ContextProvider**: Load domain-specific context via `contextProvider.getIndex("{domain}")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **MemoryStore**: Read/write project-specific memory via `memoryStore.getSkillMemory(...)` and `memoryStore.update(...)`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **Schemas**: Validate configurations against `agent_config.schema.json`, `context_metadata.schema.json`, and `memory_entry.schema.json`. See [Interface Schemas](../../interfaces/schemas/).

## Focus Areas

Full-stack development oversight evaluates 7 critical dimensions:

1. **Frontend Architecture**: Component design patterns, state management strategies, client-side routing, SSR/CSR rendering decisions, accessibility, and responsive design principles
2. **Backend Architecture**: API design and endpoint structure, business logic organization, middleware pipelines, authentication/authorization flows, and service layer patterns
3. **Data Layer**: Database schema design, ORM patterns and query optimization, migration strategies, caching layers, data validation, and persistence patterns
4. **API Contract Design**: REST and GraphQL schema definitions, API versioning strategies, request/response validation, error response standards, and documentation generation
5. **Infrastructure & DevOps**: Deployment strategies, CI/CD pipeline design, containerization and orchestration, monitoring and observability, environment management, and infrastructure as code
6. **Cross-Layer Integration**: End-to-end data flow tracing, error propagation across boundaries, shared type definitions between frontend and backend, consistent validation rules, and contract testing
7. **Performance & Scalability**: Load pattern analysis, caching strategies at every layer, database query optimization, CDN configuration, horizontal/vertical scaling decisions, and bottleneck identification

**Note**: This skill provides architectural oversight and design guidance. It coordinates across layers but delegates implementation details to layer-specific skills when available.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Analyze Project Stack (REQUIRED)

**YOU MUST:**
1. Identify all **frontend** technologies (framework, UI library, state management, build tools)
2. Identify all **backend** technologies (language, framework, runtime, ORM/database driver)
3. Identify the **database** layer (type, version, ORM, migration tool)
4. Identify **infrastructure** components (hosting, CI/CD, containers, CDN, monitoring)
5. Map dependencies between layers and identify integration points
6. Check for existing configuration files (`package.json`, `requirements.txt`, `docker-compose.yml`, etc.)

**DO NOT PROCEED WITHOUT A COMPLETE STACK INVENTORY**

### ⚠️ STEP 2: Evaluate Architecture (REQUIRED)

**YOU MUST:**
1. **Review architectural patterns**: Identify the current architecture style (monolith, microservices, serverless, modular monolith)
2. **Identify structural issues**: Look for layer violations, circular dependencies, tight coupling, and missing abstractions
3. **Assess scalability**: Evaluate whether the current architecture supports projected growth in users, data, and features
4. **Check consistency**: Verify naming conventions, error handling patterns, and coding standards are consistent across layers
5. **Evaluate security posture**: Review authentication flow, authorization boundaries, input validation, and data sanitization across the stack

**DO NOT PROCEED WITHOUT UNDERSTANDING THE ARCHITECTURAL LANDSCAPE**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. Load project memory using `memoryStore.getSkillMemory("fullstack-development", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.
2. Review previous stack assessments and architecture decisions
3. Check for known integration pain points and resolved issues
4. Load relevant context domains using `contextProvider.getIndex("{domain}")`:
   - Language/framework context for the identified stack
   - Infrastructure context for deployment patterns
   - Security context for auth/validation patterns
5. If no prior memory exists, note this is a first-time analysis

**DO NOT PROCEED WITHOUT CHECKING PROJECT HISTORY**

### ⚠️ STEP 4: Design & Implement (REQUIRED)

**YOU MUST:**
1. **Design cross-layer architecture**: Define clear boundaries, interfaces, and communication patterns between layers
2. **Define API contracts**: Specify request/response schemas, error formats, authentication headers, and versioning strategy
3. **Map data flow**: Trace data from user interaction through frontend, API, backend logic, database, and back
4. **Establish shared conventions**: Define shared types, validation rules, error codes, and naming patterns that span layers
5. **Address integration concerns**: Plan for authentication propagation, error handling across boundaries, logging correlation, and transaction management
6. **Document decisions**: Record architectural decisions with rationale, alternatives considered, and trade-offs accepted

**DO NOT PROCEED WITHOUT A COHERENT CROSS-LAYER DESIGN**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST:**
1. **Validate completeness**: Ensure all layers are addressed and no integration gaps exist
2. **Cross-reference requirements**: Verify the architecture satisfies functional and non-functional requirements
3. **Generate output**: Write analysis and recommendations to `/claudedocs/` following `OUTPUT_CONVENTIONS.md`
4. **Update project memory**: Use `memoryStore.update("fullstack-development", "{project-name}", ...)` to store:
   - Stack inventory and version information
   - Architecture decisions and rationale
   - Integration patterns and conventions
   - Known issues and improvement opportunities
5. **Present findings**: Summarize key recommendations, risks, and next steps to the user

See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

**DO NOT SKIP VALIDATION OR MEMORY UPDATES**

---

## Compliance Checklist

Before completing ANY full-stack development task, verify:
- [ ] Step 1: Project stack fully inventoried (frontend, backend, database, infrastructure)
- [ ] Step 2: Architecture evaluated for patterns, issues, scalability, and security
- [ ] Step 3: Project memory loaded and historical context reviewed
- [ ] Step 4: Cross-layer design completed with API contracts, data flow, and shared conventions
- [ ] Step 5: Output generated to /claudedocs/, memory updated, findings presented

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE ANALYSIS**

---

## Full-Stack Technology Matrix

Common full-stack combinations and their characteristics:

| Stack Name | Frontend | Backend | Database | Key Strengths |
|------------|----------|---------|----------|---------------|
| **MERN** | React | Node.js/Express | MongoDB | JavaScript everywhere, rapid prototyping |
| **MEAN** | Angular | Node.js/Express | MongoDB | TypeScript-first, enterprise patterns |
| **Django + React** | React | Python/Django | PostgreSQL | Robust ORM, admin panel, REST framework |
| **Rails + Vue** | Vue.js | Ruby on Rails | PostgreSQL | Convention over configuration, rapid development |
| **Next.js Full-Stack** | Next.js (React) | Next.js API Routes | PostgreSQL/Prisma | Unified framework, SSR/SSG, edge functions |
| **Laravel + Vue** | Vue.js | PHP/Laravel | MySQL | Elegant syntax, built-in auth, queue system |
| **Spring Boot + Angular** | Angular | Java/Spring Boot | PostgreSQL/MySQL | Enterprise-grade, strong typing, mature ecosystem |
| **FastAPI + React** | React | Python/FastAPI | PostgreSQL/MongoDB | Async-first, auto-docs, high performance |
| **Go + React** | React | Go (Gin/Echo) | PostgreSQL | High concurrency, low latency, compiled |
| **T3 Stack** | Next.js (React) | tRPC | PostgreSQL/Prisma | End-to-end type safety, modern DX |

---

## Further Reading

Refer to official documentation:
- **Architecture Patterns**:
  - 12-Factor App: https://12factor.net/
  - Patterns of Enterprise Application Architecture (Fowler)
  - Clean Architecture (Martin): https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **API Design**:
  - RESTful API Design: https://restfulapi.net/
  - GraphQL Best Practices: https://graphql.org/learn/best-practices/
  - OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- **Frontend Architecture**:
  - React Documentation: https://react.dev/
  - Vue.js Guide: https://vuejs.org/guide/
  - Next.js Documentation: https://nextjs.org/docs
- **Infrastructure**:
  - Docker Documentation: https://docs.docker.com/
  - Kubernetes Documentation: https://kubernetes.io/docs/
  - Terraform Documentation: https://developer.hashicorp.com/terraform/docs

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow for full-stack development oversight
  - 7 focus areas spanning all application layers
  - Full-stack technology matrix with common stack combinations
  - Cross-layer integration patterns and API contract design
  - Project memory integration for stack and architecture tracking
  - Interface-based context and memory access
