# Project Planning Examples

This file contains example scenarios demonstrating how to use the project-planning skill to generate structured planning documents for web projects.

---

## Example 1: New Next.js E-Commerce Application (Greenfield)

### Scenario
Planning a new e-commerce application built with Next.js, Stripe for payments, and PostgreSQL for data storage. This is a greenfield project, so it generates IMPLEMENTATION_PHASES.md + TECH_STACK_DECISIONS.md.

### User Prompt
```
I want to build a new e-commerce app with Next.js. It needs product listings, a shopping cart, user accounts, and Stripe checkout. Use PostgreSQL for the database.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Project: next-ecommerce
Type: Greenfield
Tech Stack:
  - Language: TypeScript
  - Framework: Next.js 14 (App Router)
  - Database: PostgreSQL with Prisma ORM
  - Payments: Stripe
  - Auth: NextAuth.js
  - Styling: Tailwind CSS
Scope: Medium-Large (4 major modules: products, cart, auth, checkout)
Classification: Greenfield → triggers TECH_STACK_DECISIONS.md
```

**Step 2 - Load Memory**:
- No previous memory found; first planning session for this project

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded JavaScript/TypeScript domain context for Next.js patterns

**Step 4 - Define Project Phases**:

| Phase | Name | Effort | Dependencies |
|-------|------|--------|--------------|
| 1 | Project Scaffolding & Dev Environment | Small | None |
| 2 | Database Schema & Prisma Setup | Medium | Phase 1 |
| 3 | Authentication & User Accounts | Medium | Phase 2 |
| 4 | Product Catalog & Listings | Medium | Phase 2 |
| 5 | Shopping Cart | Medium | Phase 3, Phase 4 |
| 6 | Stripe Checkout Integration | Large | Phase 5 |
| 7 | Order Management & History | Medium | Phase 6 |
| 8 | Polish, Testing & Deployment | Large | Phase 7 |

**Phase 1 detail**:
- **Deliverables**: Next.js project initialized, Tailwind configured, ESLint/Prettier set up, Docker Compose for local PostgreSQL, CI pipeline stub
- **Verification Criteria**: `npm run dev` starts without errors, `npm run lint` passes, PostgreSQL container accessible on localhost:5432
- **Exit Conditions**: Dev environment fully functional, all team members can clone and run locally

**Step 5 - Generate IMPLEMENTATION_PHASES.md**:

```markdown
# Implementation Phases — next-ecommerce

## Project Overview
- **Name**: next-ecommerce
- **Description**: Full-featured e-commerce application with product listings, shopping cart, user accounts, and Stripe checkout
- **Tech Stack**: Next.js 14, TypeScript, PostgreSQL, Prisma, Stripe, NextAuth.js, Tailwind CSS
- **Type**: Greenfield

## Phase Summary

| Phase | Name | Effort | Dependencies |
|-------|------|--------|--------------|
| 1 | Project Scaffolding & Dev Environment | Small | None |
| 2 | Database Schema & Prisma Setup | Medium | Phase 1 |
| 3 | Authentication & User Accounts | Medium | Phase 2 |
| 4 | Product Catalog & Listings | Medium | Phase 2 |
| 5 | Shopping Cart | Medium | Phase 3, Phase 4 |
| 6 | Stripe Checkout Integration | Large | Phase 5 |
| 7 | Order Management & History | Medium | Phase 6 |
| 8 | Polish, Testing & Deployment | Large | Phase 7 |

## Phase 1: Project Scaffolding & Dev Environment

### Description
Initialize the Next.js project with all tooling, establish the development environment, and ensure every contributor can run the project locally.

### Deliverables
- Next.js 14 project with App Router and TypeScript
- Tailwind CSS configured with base theme
- ESLint + Prettier configured
- Docker Compose with PostgreSQL service
- GitHub Actions CI pipeline stub

### Verification Criteria
- [ ] `npm run dev` starts the dev server on localhost:3000
- [ ] `npm run lint` passes with zero errors
- [ ] `npm run build` completes successfully
- [ ] PostgreSQL container starts via `docker compose up -d`
- [ ] Database connection verified via Prisma

### Exit Conditions
- All verification criteria pass
- Project runs on a clean clone with only `npm install && docker compose up -d`
- No hardcoded secrets — all config via environment variables

### Estimated Effort
Small

### Dependencies
None — this is the foundation phase

...
(remaining phases follow the same structure)

## Milestones
1. **Dev Environment Ready** — Phase 1 complete
2. **Core Data Layer** — Phases 2-3 complete (users can sign up and sign in)
3. **Shopping Experience** — Phases 4-5 complete (users can browse and add to cart)
4. **Revenue Ready** — Phase 6 complete (users can purchase)
5. **Launch Ready** — Phase 8 complete (tested, deployed, monitored)
```

**Step 6 - Generate Conditional Documents**:
- TECH_STACK_DECISIONS.md generated with rationale for Next.js over Remix, PostgreSQL over MongoDB, Prisma over Drizzle, and Stripe over alternatives

**Step 7 - Output**:
- `/claudedocs/IMPLEMENTATION_PHASES.md`
- `/claudedocs/TECH_STACK_DECISIONS.md`

**Step 8 - Memory Update**:
- Created `planning_patterns.md` with greenfield e-commerce phase structure
- Created `project_history.md` with initial entry for next-ecommerce

---

## Example 2: REST API Migration from Express to FastAPI

### Scenario
Planning the migration of an existing Express.js REST API to FastAPI (Python). The API serves a mobile app and has 25 endpoints. This generates IMPLEMENTATION_PHASES.md + MIGRATION_PLAN.md.

### User Prompt
```
We need to migrate our Express.js API to FastAPI. It has 25 endpoints, uses MongoDB, and serves our mobile app. We can't have downtime.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Project: api-migration
Type: Migration (Express.js → FastAPI)
Current Stack:
  - Language: JavaScript (Node.js)
  - Framework: Express.js
  - Database: MongoDB with Mongoose
Target Stack:
  - Language: Python 3.12
  - Framework: FastAPI
  - Database: MongoDB with Motor (async driver)
Scope: Large (25 endpoints, zero-downtime requirement)
Classification: Migration → triggers MIGRATION_PLAN.md
```

**Step 2 - Load Memory**:
- No previous memory found; first planning session

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded Python domain context for FastAPI patterns

**Step 4 - Define Project Phases**:

| Phase | Name | Effort | Dependencies |
|-------|------|--------|--------------|
| 1 | FastAPI Project Setup & Tooling | Small | None |
| 2 | Shared Infrastructure (Auth, Middleware, Error Handling) | Medium | Phase 1 |
| 3 | Endpoint Migration — Read-Only Endpoints (12 endpoints) | Large | Phase 2 |
| 4 | Endpoint Migration — Write Endpoints (13 endpoints) | Large | Phase 2 |
| 5 | Integration Testing & Parity Validation | Large | Phase 3, Phase 4 |
| 6 | Traffic Cutover (Strangler Fig Pattern) | Medium | Phase 5 |
| 7 | Decommission Express Service | Small | Phase 6 |

**Phase 6 detail**:
- **Deliverables**: Load balancer routing rules, traffic split configuration, monitoring dashboards
- **Verification Criteria**: 10% traffic routed to FastAPI with error rate below 0.1%, response time parity within 20ms, all monitoring alerts configured
- **Exit Conditions**: 100% traffic on FastAPI for 72 hours with no incidents, Express service receiving zero requests, rollback procedure tested and documented

**Step 5 - Generate IMPLEMENTATION_PHASES.md**:

```markdown
# Implementation Phases — api-migration

## Project Overview
- **Name**: api-migration
- **Description**: Zero-downtime migration of 25-endpoint REST API from Express.js to FastAPI
- **Current Stack**: Express.js, JavaScript, MongoDB/Mongoose
- **Target Stack**: FastAPI, Python 3.12, MongoDB/Motor
- **Type**: Migration (Strangler Fig pattern)

## Phase Summary

| Phase | Name | Effort | Dependencies |
|-------|------|--------|--------------|
| 1 | FastAPI Project Setup & Tooling | Small | None |
| 2 | Shared Infrastructure | Medium | Phase 1 |
| 3 | Read-Only Endpoint Migration | Large | Phase 2 |
| 4 | Write Endpoint Migration | Large | Phase 2 |
| 5 | Integration Testing & Parity | Large | Phase 3, Phase 4 |
| 6 | Traffic Cutover | Medium | Phase 5 |
| 7 | Decommission Express | Small | Phase 6 |

## Phase 6: Traffic Cutover (Strangler Fig Pattern)

### Description
Gradually shift production traffic from Express to FastAPI using the strangler fig pattern. Start with 10% and increase to 100% over several days while monitoring error rates and latency.

### Deliverables
- Load balancer routing configuration for traffic splitting
- Monitoring dashboards comparing Express vs FastAPI metrics
- Automated rollback trigger configuration
- Runbook for manual rollback procedure

### Verification Criteria
- [ ] 10% traffic on FastAPI with error rate < 0.1%
- [ ] Response time parity within 20ms of Express baseline
- [ ] All monitoring alerts firing correctly on test scenarios
- [ ] Rollback procedure executes in under 2 minutes

### Exit Conditions
- 100% traffic on FastAPI for minimum 72 hours
- Zero critical incidents during cutover period
- Express service confirmed receiving zero requests
- Rollback procedure tested and documented

### Estimated Effort
Medium

### Dependencies
Phase 5 (all endpoints tested and validated for parity)

...

## Risk Factors
- **Data format differences**: Mongoose vs Motor may serialize ObjectIDs differently
- **Middleware behavior parity**: Express middleware ordering vs FastAPI dependency injection
- **Performance regression**: Python GIL could affect concurrent request handling — mitigated by FastAPI async support
```

**Step 6 - Generate Conditional Documents**:
- MIGRATION_PLAN.md generated with strangler fig strategy, per-endpoint migration checklist, rollback procedures, and data compatibility validation approach

**Step 7 - Output**:
- `/claudedocs/IMPLEMENTATION_PHASES.md`
- `/claudedocs/MIGRATION_PLAN.md`

**Step 8 - Memory Update**:
- Created `planning_patterns.md` with migration phase structure and strangler fig pattern
- Created `project_history.md` with initial entry for api-migration

---

## Example 3: Data-Intensive Dashboard Project

### Scenario
Planning a real-time analytics dashboard that ingests event data, processes it through a pipeline, and displays interactive charts. Heavy on data modeling and database design. This generates IMPLEMENTATION_PHASES.md + DATA_MODEL.md.

### User Prompt
```
Build a real-time analytics dashboard. We need to ingest clickstream events, aggregate them in near real-time, and show interactive charts. Use React for the frontend and PostgreSQL with TimescaleDB for time-series data.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Project: analytics-dashboard
Type: Greenfield, Database-heavy
Tech Stack:
  - Frontend: React 18, Recharts, TanStack Query
  - Backend: Node.js, Express, WebSocket (Socket.io)
  - Database: PostgreSQL + TimescaleDB extension
  - Queue: Redis Streams for event ingestion
  - Infrastructure: Docker Compose (local), planned for Kubernetes
Scope: Large (event ingestion, aggregation pipeline, real-time UI)
Classification: Database-heavy → triggers DATA_MODEL.md
```

**Step 2 - Load Memory**:
- No previous memory found; first planning session

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded JavaScript/TypeScript domain context

**Step 4 - Define Project Phases**:

| Phase | Name | Effort | Dependencies |
|-------|------|--------|--------------|
| 1 | Project Setup & Infrastructure | Small | None |
| 2 | Data Model & TimescaleDB Schema | Large | Phase 1 |
| 3 | Event Ingestion Pipeline | Large | Phase 2 |
| 4 | Aggregation Layer & Materialized Views | Large | Phase 3 |
| 5 | REST API for Dashboard Data | Medium | Phase 4 |
| 6 | React Dashboard UI & Charts | Large | Phase 5 |
| 7 | Real-Time Updates via WebSocket | Medium | Phase 5, Phase 6 |
| 8 | Performance Tuning & Load Testing | Large | Phase 7 |

**Phase 2 detail**:
- **Deliverables**: Complete database schema with hypertables, index strategy document, seed data scripts, Prisma schema or raw SQL migrations
- **Verification Criteria**: All migrations run without errors, seed data loads successfully, sample queries return expected results within performance thresholds (< 100ms for dashboard queries on 1M rows)
- **Exit Conditions**: Schema reviewed and approved, indexes validated with EXPLAIN ANALYZE, seed data represents realistic production patterns, TimescaleDB compression policies configured

**Step 5 - Generate IMPLEMENTATION_PHASES.md**:

```markdown
# Implementation Phases — analytics-dashboard

## Project Overview
- **Name**: analytics-dashboard
- **Description**: Real-time analytics dashboard with clickstream event ingestion, near-real-time aggregation, and interactive chart visualization
- **Tech Stack**: React 18, Node.js/Express, PostgreSQL + TimescaleDB, Redis Streams, Socket.io
- **Type**: Greenfield, Database-heavy

## Phase Summary

| Phase | Name | Effort | Dependencies |
|-------|------|--------|--------------|
| 1 | Project Setup & Infrastructure | Small | None |
| 2 | Data Model & TimescaleDB Schema | Large | Phase 1 |
| 3 | Event Ingestion Pipeline | Large | Phase 2 |
| 4 | Aggregation Layer & Materialized Views | Large | Phase 3 |
| 5 | REST API for Dashboard Data | Medium | Phase 4 |
| 6 | React Dashboard UI & Charts | Large | Phase 5 |
| 7 | Real-Time Updates via WebSocket | Medium | Phase 5, Phase 6 |
| 8 | Performance Tuning & Load Testing | Large | Phase 7 |

## Phase 2: Data Model & TimescaleDB Schema

### Description
Design and implement the complete data model for event storage and aggregation. Establish hypertables for time-series data, define indexes for dashboard query patterns, and create seed data for development.

### Deliverables
- PostgreSQL schema with TimescaleDB hypertables for raw events
- Dimension tables for users, sessions, pages, and event types
- Index strategy optimized for dashboard query patterns
- Database migration scripts (up and down)
- Seed data generator producing realistic clickstream patterns

### Verification Criteria
- [ ] All migrations execute cleanly on a fresh database
- [ ] `SELECT` queries for dashboard aggregations complete in < 100ms on 1M rows
- [ ] `EXPLAIN ANALYZE` confirms index usage on all dashboard queries
- [ ] Seed data loads 1M events in under 30 seconds
- [ ] TimescaleDB compression policies configured and tested

### Exit Conditions
- Schema reviewed and matches all known query patterns
- All indexes validated with query plan analysis
- Seed data represents realistic production data distribution
- Down migrations tested — can roll back to empty state
- Schema documentation added to project docs

### Estimated Effort
Large

### Dependencies
Phase 1 (Docker Compose with PostgreSQL + TimescaleDB running)

...

## Milestones
1. **Data Foundation** — Phase 2 complete (schema finalized, queryable)
2. **Pipeline Active** — Phase 4 complete (events flowing and aggregating)
3. **Dashboard Viewable** — Phase 6 complete (charts rendering real data)
4. **Real-Time Ready** — Phase 7 complete (live updates working)
5. **Production Ready** — Phase 8 complete (performance validated under load)
```

**Step 6 - Generate Conditional Documents**:
- DATA_MODEL.md generated with entity relationship diagram, hypertable definitions, dimension table schemas, index strategy, materialized view definitions, compression policies, and data retention rules

**Step 7 - Output**:
- `/claudedocs/IMPLEMENTATION_PHASES.md`
- `/claudedocs/DATA_MODEL.md`

**Step 8 - Memory Update**:
- Created `planning_patterns.md` with data-intensive dashboard phase structure
- Created `project_history.md` with initial entry for analytics-dashboard

---

## Summary of Planning Scenarios

1. **Greenfield e-commerce** — Standard web app phases from scaffolding to deployment; generates TECH_STACK_DECISIONS.md to document technology choices
2. **API migration** — Strangler fig pattern with parity validation and traffic cutover; generates MIGRATION_PLAN.md with rollback strategy
3. **Data-intensive dashboard** — Database-first approach with schema design before application logic; generates DATA_MODEL.md with hypertable and index strategy

## Best Practices

- Always define verification criteria that are concrete and testable — not vague statements
- Exit conditions should be binary (met or not met) — avoid subjective assessments
- Earlier phases should never need to be revisited due to later phase requirements
- Include risk factors for any phase with external dependencies or unfamiliar technology
- Use memory to track which phase structures work well for specific project types
- When a project triggers multiple conditional documents, generate all of them
