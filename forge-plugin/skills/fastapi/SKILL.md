---
name: fastapi
version: "1.0.0"
description: Modern FastAPI development guidance for building high-performance APIs with async Python, Pydantic validation, dependency injection, and OpenAPI-first design. Covers architecture, security, performance, and deployment.
context:
  primary_domain: "python"
  always_load_files: []
  detection_required: true
  file_budget: 5
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, api_contracts.md, dependency_patterns.md, performance_notes.md]
    - type: "shared-project"
      usage: "reference"
tags: ["backend", "framework", "python", "fastapi", "backend-frameworks"]
---

# FastAPI Framework Expert

## Category
Backend & Frameworks

## ⚠️ MANDATORY COMPLIANCE ⚠️
**CRITICAL**: The 6-step workflow outlined in this document MUST be followed in exact order for EVERY FastAPI engagement. Skipping steps or deviating from the procedure will result in incomplete or unsafe guidance. This is non-negotiable.

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
1. **API Contracts**: OpenAPI-first design, route structure, response models
2. **Pydantic Models**: Validation, serialization, schema reuse
3. **Dependency Injection**: Lifespan events, shared dependencies, overrides
4. **Async Execution**: Concurrency, background tasks, streaming responses
5. **Data Access**: SQLAlchemy async, migrations, repository patterns
6. **Security**: OAuth2/JWT, CORS, rate limiting, input validation
7. **Observability**: logging, tracing, metrics, error handling

---

## Purpose

Modern FastAPI development guidance for building high-performance APIs with async Python, Pydantic validation, dependency injection, and OpenAPI-first design. Covers architecture, security, performance, and deployment.


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Scope the FastAPI Engagement (REQUIRED)
**YOU MUST:**
1. Identify FastAPI version and deployment target (ASGI server, container, serverless)
2. Clarify the API scope, expected traffic, and performance constraints
3. Determine database and dependency stack (SQLAlchemy, Redis, message queues)
4. Ask clarifying questions on auth, OpenAPI expectations, and testing needs
5. **Think through your implementation plan in a `<thinking>` block before writing any files or recommending changes**

**DO NOT PROCEED WITHOUT A CLEAR SCOPE AND PLAN**

### ⚠️ STEP 2: Load Project Memory (REQUIRED)
**YOU MUST:**
1. Load memory with `memoryStore.getSkillMemory("fastapi", "{project-name}")`
2. Review cross-skill memory with `memoryStore.getByProject("{project-name}")`
3. Note existing conventions for dependencies, routers, and testing

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)
**YOU MUST:**
1. Use `contextProvider.getDomainIndex("python")` to identify FastAPI context
2. Load FastAPI-specific guidance via `contextProvider.getConditionalContext("python", "fastapi")`
3. Pull security context with `contextProvider.getCrossDomainContext("python", ["auth", "input", "rate"])`
4. Stay within the declared file budget

**DO NOT PROCEED WITHOUT RELEVANT CONTEXT**

### ⚠️ STEP 4: Analyze Architecture & Code Paths (REQUIRED)
**YOU MUST:**
1. Review router structure, dependencies, and response models
2. Inspect data access patterns and async database usage
3. Evaluate background tasks, queue usage, and concurrency boundaries
4. Check error handling and observability hooks

**DO NOT PROCEED WITHOUT A COMPLETE ANALYSIS**

### ⚠️ STEP 5: Provide FastAPI Guidance (REQUIRED)
**YOU MUST:**
1. Recommend API structure, dependency injection, and validation improvements
2. Provide security guidance for auth, CORS, and rate limiting
3. Suggest performance tuning and testing strategies

**DO NOT PROVIDE GENERIC OR UNSUPPORTED RECOMMENDATIONS**

### ⚠️ STEP 6: Generate Output & Update Memory (REQUIRED)
**YOU MUST:**
1. Produce a structured report in `/claudedocs/fastapi_{project}_{YYYY-MM-DD}.md`
2. Follow the naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Update memory with `memoryStore.update("fastapi", "{project-name}", ...)`:
   - `project_overview.md`
   - `api_contracts.md`
   - `dependency_patterns.md`
   - `performance_notes.md`

**DO NOT FINISH WITHOUT SAVING OUTPUT AND UPDATING MEMORY**

---

## Compliance Checklist
Before completing ANY FastAPI task, verify:
- [ ] Step 1: Scope defined and plan documented in `<thinking>`
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()`
- [ ] Step 3: Context loaded via `contextProvider`
- [ ] Step 4: Architecture and code paths analyzed
- [ ] Step 5: FastAPI guidance provided with actionable recommendations
- [ ] Step 6: Output saved to `/claudedocs/` and memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE GUIDANCE**

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release for FastAPI framework guidance |
