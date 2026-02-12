# Project Workflow Examples

This file contains example scenarios demonstrating how to use the project-workflow skill's slash commands to manage the complete project lifecycle.

---

## Example 1: Exploring a New Project Idea with `/explore-idea`

### Scenario
A developer has an idea for a CLI tool that generates mock API data from OpenAPI specs. They want to explore feasibility before committing to a full project plan.

### User Prompt
```
/explore-idea — I want to build a CLI tool that reads OpenAPI specs and generates realistic mock data for every endpoint. It should support JSON and YAML specs, generate data that matches schema constraints, and optionally spin up a mock server.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Command: /explore-idea
Project: mock-data-cli (derived from idea)
Project State: New — no existing artifacts
Existing Artifacts: None
Git State: N/A (no repository yet)
Validation: ✅ /explore-idea is valid at any stage
```

**Step 2 - Load Memory**:
- No previous memory found; first workflow interaction for this project

**Step 3 - Load Context**:
- Loaded engineering domain context
- No technology-specific context needed yet (tech stack not decided)

**Step 4 - Route to Command Handler** (`/explore-idea`):
- Captured idea description and key requirements
- Analyzing feasibility across dimensions

**Step 5 - Execute Command Logic**:

Feasibility analysis:
```
Technical Complexity: Medium
- OpenAPI parsing: Well-supported libraries exist (swagger-parser, openapi3-parser)
- Schema-aware data generation: Faker libraries exist but need constraint mapping
- Mock server: Express/Fastify stub server is straightforward
- CLI framework: Commander.js, yargs, or oclif are mature options

Resource Requirements: Low-Medium
- Single developer can build MVP in 2-3 weeks
- No infrastructure requirements for CLI tool
- Mock server feature adds ~1 week

Market Fit: Strong
- Existing tools (Prism, MockServer) are heavy — opportunity for lightweight alternative
- Common pain point in API-first development workflows
- Good fit for CI/CD pipeline integration

Risks & Unknowns:
- Complex schema compositions ($ref, allOf, oneOf) may be hard to generate data for
- Circular references in schemas need detection and handling
- Performance on large specs (500+ endpoints) needs benchmarking

Dependencies:
- OpenAPI parser library (critical — evaluate swagger-parser vs openapi3-parser)
- Faker library for realistic data generation
- CLI framework selection impacts developer experience
```

**Step 6 - Generate Output**:

```markdown
# Idea Exploration: mock-data-cli

## Concept
CLI tool that reads OpenAPI specifications and generates realistic mock data for every endpoint, with optional mock server capability.

## Feasibility Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Technical Complexity | Medium | Libraries exist for parsing and data generation; schema composition is the main challenge |
| Resource Requirements | Low-Medium | Solo developer, 2-3 week MVP, no infrastructure |
| Market Fit | Strong | Lightweight alternative to heavy tools like Prism |
| Timeline Risk | Low | Core functionality is well-understood; mock server adds scope |

## Key Requirements
1. Parse OpenAPI 3.x specs in JSON and YAML formats
2. Generate mock data matching schema types, formats, and constraints
3. Handle schema compositions ($ref, allOf, oneOf, anyOf)
4. Optional: Spin up a mock HTTP server serving generated responses
5. CLI interface with intuitive commands and flags

## Risks
- **Schema composition complexity**: Nested $ref and allOf/oneOf may produce invalid combinations
- **Circular references**: Specs with circular $ref chains need detection to avoid infinite loops
- **Large spec performance**: Specs with 500+ endpoints may have slow generation times

## Recommendation
**GO** — Viable project with clear scope and strong market fit. Recommend proceeding to `/plan-project` with TypeScript as the implementation language for strong OpenAPI typing support.

## Suggested Next Steps
1. Run `/plan-project` to generate implementation phases
2. Evaluate `@apidevtools/swagger-parser` vs `openapi3-parser` in a spike
3. Create a test fixture set of OpenAPI specs covering edge cases
```

File: `/claudedocs/explore_idea_mock-data-cli_2025-06-30.md`

**Step 7 - Memory Update**:
- Created `workflow_history.md` with initial `/explore-idea` entry
- Created `command_usage.md` with command frequency tracking

---

## Example 2: Planning a Feature with `/plan-feature`

### Scenario
A developer working on an existing e-commerce project needs to plan a "wishlist" feature. The project already has `IMPLEMENTATION_PHASES.md` and `SESSION.md` from previous workflow commands.

### User Prompt
```
/plan-feature — Add a wishlist feature where users can save products for later. They should be able to add/remove items, view their wishlist, and get notified when wishlist items go on sale.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Command: /plan-feature
Project: next-ecommerce
Project State: In-progress (Phase 4 of 8)
Existing Artifacts:
  - IMPLEMENTATION_PHASES.md ✅ (8 phases defined)
  - SESSION.md ✅ (Phase 4: Product Catalog, 60% complete)
  - CHANGELOG.md ❌ (not yet created)
Git State: feature/product-catalog @ abc1234
Validation: ✅ /plan-feature is valid — project context exists
```

**Step 2 - Load Memory**:
- Previous workflow memory found: 3 prior commands (`/explore-idea`, `/plan-project`, `/wrap-session`)
- Cross-skill memory: `project-planning` has phase structure and tech stack details

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded JavaScript/TypeScript domain context for Next.js patterns

**Step 4 - Route to Command Handler** (`/plan-feature`):
- Captured feature description and scope
- Breaking feature into discrete tasks

**Step 5 - Execute Command Logic**:

```markdown
# Feature Plan: Wishlist

## Feature Overview
Allow authenticated users to save products to a personal wishlist, manage wishlist items, and receive notifications when wishlist items go on sale.

## Tasks

### Task 1: Wishlist Data Model
- **Description**: Add Wishlist and WishlistItem models to the Prisma schema with user and product relationships
- **Acceptance Criteria**:
  - [ ] `Wishlist` model with `id`, `userId`, `createdAt`, `updatedAt` fields
  - [ ] `WishlistItem` model with `id`, `wishlistId`, `productId`, `addedAt` fields
  - [ ] Unique constraint on `(wishlistId, productId)` to prevent duplicates
  - [ ] Migration runs cleanly on existing database
- **Effort**: Small
- **Dependencies**: Phase 2 (Database Schema) must be complete ✅

### Task 2: Wishlist API Endpoints
- **Description**: Create API routes for wishlist CRUD operations
- **Acceptance Criteria**:
  - [ ] `GET /api/wishlist` — returns current user's wishlist with product details
  - [ ] `POST /api/wishlist/items` — adds a product to the wishlist (idempotent)
  - [ ] `DELETE /api/wishlist/items/{productId}` — removes a product from the wishlist
  - [ ] All endpoints require authentication (return 401 if unauthenticated)
  - [ ] Proper error responses for invalid product IDs (404)
- **Effort**: Medium
- **Dependencies**: Task 1, Phase 3 (Authentication) must be complete ✅

### Task 3: Wishlist UI Components
- **Description**: Build wishlist UI — heart icon on product cards, wishlist page, empty state
- **Acceptance Criteria**:
  - [ ] Heart icon toggle on product cards (filled = in wishlist, outline = not in wishlist)
  - [ ] Optimistic UI update on toggle (instant visual feedback)
  - [ ] `/wishlist` page displaying all saved products in a grid
  - [ ] Empty state with call-to-action when wishlist is empty
  - [ ] Loading skeleton while wishlist data is fetched
- **Effort**: Medium
- **Dependencies**: Task 2, Phase 4 (Product Catalog) must be complete

### Task 4: Sale Notification System
- **Description**: Notify users when wishlist items have a price reduction
- **Acceptance Criteria**:
  - [ ] Price change detection when products are updated
  - [ ] In-app notification for price drops on wishlist items
  - [ ] Optional email notification (user preference toggle)
  - [ ] Notification includes old price, new price, and percentage savings
- **Effort**: Large
- **Dependencies**: Task 1, Task 2

## Summary

| Task | Name | Effort | Dependencies |
|------|------|--------|--------------|
| 1 | Wishlist Data Model | Small | Phase 2 ✅ |
| 2 | Wishlist API Endpoints | Medium | Task 1, Phase 3 ✅ |
| 3 | Wishlist UI Components | Medium | Task 2, Phase 4 |
| 4 | Sale Notification System | Large | Task 1, Task 2 |

**Total Estimated Effort**: Large (sum of all tasks)
**Recommended Insertion Point**: After Phase 5 (Shopping Cart) — wishlist is a parallel concern to cart functionality
```

**Step 6 - Generate Output**:
File: `/claudedocs/feature_plan_wishlist_2025-06-30.md`

**Step 7 - Memory Update**:
- Appended `/plan-feature` entry to `workflow_history.md`
- Updated `command_usage.md` with feature planning patterns

---

## Example 3: Reflecting on a Sprint with `/reflect`

### Scenario
A developer has just completed a two-week sprint on a data pipeline project. They've wrapped several sessions and want to analyze what went well and what needs improvement before starting the next sprint.

### User Prompt
```
/reflect — We just finished a two-week sprint on the data pipeline. I want to understand what worked, what didn't, and what we should change for the next sprint.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Command: /reflect
Project: data-pipeline
Project State: In-progress (Phase 3 of 6 complete)
Existing Artifacts:
  - IMPLEMENTATION_PHASES.md ✅ (6 phases defined)
  - SESSION.md ✅ (Phase 4: API Layer, 20% complete)
  - CHANGELOG.md ✅ (v0.2.0 released during sprint)
Git State: main @ def5678
Validation: ✅ /reflect is valid — project history exists
```

**Step 2 - Load Memory**:
- Previous workflow memory found: 8 prior commands over 2 weeks
- Cross-skill memory: `project-session-management` has 6 session records with durations and progress deltas

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded Python domain context (project uses FastAPI)

**Step 4 - Route to Command Handler** (`/reflect`):
- Reviewing recent work history from SESSION.md, git log, and memory
- Analyzing patterns across sessions

**Step 5 - Execute Command Logic**:

Analysis of the sprint:
```
Sprint Duration: 2 weeks (6 sessions)
Phases Completed: Phase 2 (Data Model) and Phase 3 (Ingestion Pipeline)
Phase Started: Phase 4 (API Layer) — 20% complete
Commits: 34 commits across 4 branches
Release: v0.2.0 (data model + ingestion pipeline)

Session Velocity:
- Session 1: Phase 2, 0% → 40% (data model design, schema creation)
- Session 2: Phase 2, 40% → 100% (indexes, seed data, migration scripts)
- Session 3: Phase 3, 0% → 30% (Redis Streams setup, basic consumer)
- Session 4: Phase 3, 30% → 50% (blocked on message serialization format)
- Session 5: Phase 3, 50% → 100% (serialization resolved, error handling, DLQ)
- Session 6: Phase 4, 0% → 20% (FastAPI scaffolding, first 2 endpoints)
```

**Step 6 - Generate Output**:

```markdown
# Sprint Retrospective: data-pipeline

**Sprint**: 2025-06-16 to 2025-06-30
**Sessions**: 6
**Phases Completed**: 2 (Phase 2: Data Model, Phase 3: Ingestion Pipeline)

## What Went Well ✅

### 1. Phase 2 Completed Ahead of Pace
- Data model design and implementation finished in 2 sessions
- TimescaleDB hypertable configuration worked on first attempt
- Seed data scripts are reusable for future testing

### 2. Effective Session Handoffs
- Next actions in SESSION.md were consistently specific and actionable
- Git checkpoints enabled clean session resumption every time
- Zero rework due to lost context between sessions

### 3. Strong Verification Criteria
- EXPLAIN ANALYZE validation caught a missing index before it reached production
- Seed data performance benchmark (1M rows in 28s) exceeded the 30s target
- Clear exit conditions made phase completion decisions objective

## What Needs Improvement 🔶

### 1. Session 4 Blocker (Message Serialization)
- **Impact**: Entire session spent investigating serialization format mismatch
- **Root Cause**: Redis Streams and the consumer used different serialization defaults (msgpack vs JSON)
- **Lesson**: Add a "data format contract" step when integrating two systems — validate serialization compatibility before building the pipeline

### 2. Phase 3 Estimation Was Optimistic
- **Planned**: Medium effort — estimated 2 sessions
- **Actual**: 3 sessions (50% over estimate)
- **Root Cause**: Error handling and dead letter queue were underestimated — treated as "cleanup" but required significant design
- **Lesson**: Error handling in pipeline systems should be sized as its own task, not bundled into "polish"

### 3. Limited Test Coverage on Ingestion Pipeline
- **Current**: 62% coverage on pipeline module
- **Gap**: Edge cases for malformed events and Redis connection failures not tested
- **Risk**: These gaps may surface as production issues
- **Lesson**: Add integration test tasks explicitly in phase planning — don't rely on "testing is implicit"

## Action Items for Next Sprint 📋

1. **Add data format contract validation** to Phase 4 planning — verify serialization format between API layer and pipeline before building endpoints
2. **Size error handling explicitly** in remaining phases — create dedicated tasks for error handling and edge case coverage in Phases 4-6
3. **Schedule a testing catch-up session** — bring pipeline test coverage from 62% to 80% before proceeding deeper into Phase 4
4. **Update IMPLEMENTATION_PHASES.md** — adjust effort estimates for remaining phases based on actual velocity data (1 phase per 2.5 sessions average)

## Sprint Metrics

| Metric | Value |
|--------|-------|
| Sessions | 6 |
| Commits | 34 |
| Phases completed | 2 (Phase 2, Phase 3) |
| Average session velocity | 0.33 phases/session |
| Blocker sessions | 1 (Session 4) |
| Release | v0.2.0 |
```

File: `/claudedocs/retrospective_data-pipeline_2025-06-30.md`

**Step 7 - Memory Update**:
- Appended `/reflect` entry to `workflow_history.md` with sprint analysis summary
- Updated `command_usage.md` with retrospective patterns and improvement items

---

## Summary of Workflow Scenarios

1. **Exploring a new idea** — `/explore-idea` provides structured feasibility analysis before committing to a project, with a clear go/no-go recommendation
2. **Planning a feature** — `/plan-feature` breaks a feature into discrete tasks with acceptance criteria and effort estimates, fitting into the existing project lifecycle
3. **Sprint retrospective** — `/reflect` analyzes recent work across sessions, identifying effective patterns and improvement areas with actionable items

## Best Practices

- Use commands in natural lifecycle order: `/explore-idea` → `/plan-project` → `/plan-feature` → `/wrap-session` / `/continue-session` → `/release` → `/reflect`
- Always check workflow status with `/workflow` when unsure which command to use next
- Use `/brief` before stakeholder meetings to generate a concise status summary
- Run `/reflect` at the end of each sprint or milestone to capture learnings while they are fresh
- Memory continuity across commands enables pattern recognition — the more you use the workflow, the better the recommendations become
