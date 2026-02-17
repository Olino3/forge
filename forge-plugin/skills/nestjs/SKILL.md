---
name: nestjs
version: "1.0.0"
description: Enterprise-grade NestJS development guidance for building modular, testable Node.js backends with TypeScript. Covers module design, dependency injection, validation, security, performance, and deployment.
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, module_map.md, integration_notes.md, testing_strategy.md]
    - type: "shared-project"
      usage: "reference"
tags: ["backend", "framework", "nestjs", "typescript", "backend-frameworks"]
---

# NestJS Framework Expert

## Category
Backend & Frameworks

## ⚠️ MANDATORY COMPLIANCE ⚠️
**CRITICAL**: The 6-step workflow outlined in this document MUST be followed in exact order for EVERY NestJS engagement. Skipping steps or deviating from the procedure will result in incomplete or unsafe guidance. This is non-negotiable.

## File Structure
- **SKILL.md** (this file): Main instructions and MANDATORY workflow

### Step 1: Initial Analysis

Gather inputs and determine scope and requirements.

### Step 2: Load Memory

Load project-specific memory via MemoryStore interface.

### Step 3: Load Context

Load relevant context files via ContextProvider interface.

### Step 4: Core Implementation

Execute the skill-specific core action.

### Step 5: Generate Output

Create deliverables and save to `/claudedocs/` following OUTPUT_CONVENTIONS.md.

### Step 6: Update Memory

Update project memory with new patterns and decisions.

## Interface References
- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)

## Focus Areas
1. **Module Architecture**: feature modules, shared modules, dependency boundaries
2. **Controllers & Providers**: DI scopes, service layering, lifecycle hooks
3. **Validation & DTOs**: class-validator, pipes, transformation
4. **Data Access**: TypeORM/Prisma patterns, transactions, migrations
5. **Security**: guards, auth strategies, rate limiting, secrets
6. **Messaging**: microservices, queues, event-driven patterns
7. **Testing**: unit + e2e setup, test modules, mocking

---

## Purpose

Enterprise-grade NestJS development guidance for building modular, testable Node.js backends with TypeScript. Covers module design, dependency injection, validation, security, performance, and deployment.


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Scope the NestJS Engagement (REQUIRED)
**YOU MUST:**
1. Identify NestJS version and runtime environment
2. Clarify the domain (API, microservice, hybrid) and deployment target
3. Determine ORM/transport stack (TypeORM, Prisma, Redis, RabbitMQ)
4. Ask clarifying questions about auth, messaging, and module boundaries
5. **Think through your implementation plan in a `<thinking>` block before writing any files or recommending changes**

**DO NOT PROCEED WITHOUT A CLEAR SCOPE AND PLAN**

### ⚠️ STEP 2: Load Project Memory (REQUIRED)
**YOU MUST:**
1. Load memory with `memoryStore.getSkillMemory("nestjs", "{project-name}")`
2. Review cross-skill memory with `memoryStore.getByProject("{project-name}")`
3. Note existing module conventions and integrations

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)
**YOU MUST:**
1. Use `contextProvider.getDomainIndex("engineering")` for general architecture patterns
2. Pull security context with `contextProvider.getCrossDomainContext("engineering", ["auth", "security"])`
3. Stay within the declared file budget

**DO NOT PROCEED WITHOUT RELEVANT CONTEXT**

### ⚠️ STEP 4: Analyze Architecture & Code Paths (REQUIRED)
**YOU MUST:**
1. Review module boundaries, controller routes, and provider scopes
2. Inspect DTO validation, pipes, and exception filters
3. Evaluate data access patterns and transaction handling
4. Check integration points (queues, caches, external services)

**DO NOT PROCEED WITHOUT A COMPLETE ANALYSIS**

### ⚠️ STEP 5: Provide NestJS Guidance (REQUIRED)
**YOU MUST:**
1. Recommend module restructuring or DI improvements
2. Provide validation, security, and testing guidance
3. Suggest performance or messaging enhancements

**DO NOT PROVIDE GENERIC OR UNSUPPORTED RECOMMENDATIONS**

### ⚠️ STEP 6: Generate Output & Update Memory (REQUIRED)
**YOU MUST:**
1. Produce a structured report in `/claudedocs/nestjs_{project}_{YYYY-MM-DD}.md`
2. Follow the naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Update memory with `memoryStore.update("nestjs", "{project-name}", ...)`:
   - `project_overview.md`
   - `module_map.md`
   - `integration_notes.md`
   - `testing_strategy.md`

**DO NOT FINISH WITHOUT SAVING OUTPUT AND UPDATING MEMORY**

---

## Compliance Checklist
Before completing ANY NestJS task, verify:
- [ ] Step 1: Scope defined and plan documented in `<thinking>`
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()`
- [ ] Step 3: Context loaded via `contextProvider`
- [ ] Step 4: Architecture and code paths analyzed
- [ ] Step 5: NestJS guidance provided with actionable recommendations
- [ ] Step 6: Output saved to `/claudedocs/` and memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE GUIDANCE**

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release for NestJS framework guidance |
