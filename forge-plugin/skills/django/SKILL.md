---
name: django
version: "1.0.0"
description: Expert-level Django development patterns and best practices for building secure, scalable web apps and APIs with Django and Django REST Framework. Guides architecture decisions, data modeling, API design, security, performance, and deployment.
context:
  primary_domain: "python"
  always_load_files: []
  detection_required: true
  file_budget: 5
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, architecture_notes.md, data_model_patterns.md, deployment_notes.md]
    - type: "shared-project"
      usage: "reference"
## tags: ["backend", "framework", "python", "django", "backend-frameworks"]

# Django Framework Expert

## Category
Backend & Frameworks

## ⚠️ MANDATORY COMPLIANCE ⚠️
**CRITICAL**: The 6-step workflow outlined in this document MUST be followed in exact order for EVERY Django engagement. Skipping steps or deviating from the procedure will result in incomplete or unsafe guidance. This is non-negotiable.

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
1. **Project Architecture**: settings layout, apps, middleware, environment configuration
2. **Data Modeling**: ORM usage, migrations, query optimization, constraints
3. **API Design**: Django REST Framework serializers, viewsets, pagination, filtering
4. **Security**: auth flows, permissions, CSRF, secrets management, input validation
5. **Performance**: caching, database indexing, async tasks, query reduction
6. **Testing**: pytest strategies, factories, fixtures, integration tests
7. **Deployment**: ASGI/WSGI, static/media, environment parity, observability

---

## Purpose

Expert-level Django development patterns and best practices for building secure, scalable web apps and APIs with Django and Django REST Framework. Guides architecture decisions, data modeling, API design, security, performance, and deployment.


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Scope the Django Engagement (REQUIRED)
**YOU MUST:**
1. Identify the Django version and whether Django REST Framework is in use
2. Determine the project type (monolith, API-only, hybrid) and deployment target
3. Clarify the goal (new feature, refactor, performance, security, debugging)
4. Ask clarifying questions if scope is ambiguous (apps involved, data models, endpoints)
5. **Think through your implementation plan in a `<thinking>` block before writing any files or recommending changes**

**DO NOT PROCEED WITHOUT A CLEAR SCOPE AND PLAN**

### ⚠️ STEP 2: Load Project Memory (REQUIRED)
**YOU MUST:**
1. Load project-specific memory with `memoryStore.getSkillMemory("django", "{project-name}")`
2. Review cross-skill memory with `memoryStore.getByProject("{project-name}")`
3. Note existing architectural decisions, conventions, and known issues

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)
**YOU MUST:**
1. Use `contextProvider.getDomainIndex("python")` to identify Django-related context files
2. Load Django-specific guidance with `contextProvider.getConditionalContext("python", "django")`
3. Pull security context as needed with `contextProvider.getCrossDomainContext("python", ["auth", "input", "database"])`
4. Stay within the declared file budget

**DO NOT PROCEED WITHOUT RELEVANT CONTEXT**

### ⚠️ STEP 4: Analyze Architecture & Code Paths (REQUIRED)
**YOU MUST:**
1. Review settings modules, app structure, and dependency configuration
2. Inspect models, migrations, and query patterns for correctness and performance
3. Assess API layers (views, serializers, routers) for consistency and security
4. Identify async/background task usage (Celery, RQ, async views)
5. Flag risks: N+1 queries, missing permissions, unsafe serializers

**DO NOT PROCEED WITHOUT A COMPLETE ANALYSIS**

### ⚠️ STEP 5: Provide Django Guidance (REQUIRED)
**YOU MUST:**
1. Recommend improvements using Django/DRF best practices
2. Provide actionable patterns for data modeling, views, and serializers
3. Include security controls (permissions, CSRF, secret storage, validation)
4. Suggest test strategies and observability where appropriate

**DO NOT PROVIDE GENERIC OR UNSUPPORTED RECOMMENDATIONS**

### ⚠️ STEP 6: Generate Output & Update Memory (REQUIRED)
**YOU MUST:**
1. Produce a structured report in `/claudedocs/django_{project}_{YYYY-MM-DD}.md`
2. Follow the naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Update memory with `memoryStore.update("django", "{project-name}", ...)`:
   - `project_overview.md`
   - `architecture_notes.md`
   - `data_model_patterns.md`
   - `deployment_notes.md`

**DO NOT FINISH WITHOUT SAVING OUTPUT AND UPDATING MEMORY**

---

## Compliance Checklist
Before completing ANY Django task, verify:
- [ ] Step 1: Scope defined and plan documented in `<thinking>`
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()`
- [ ] Step 3: Context loaded via `contextProvider`
- [ ] Step 4: Architecture and code paths analyzed
- [ ] Step 5: Django guidance provided with actionable recommendations
- [ ] Step 6: Output saved to `/claudedocs/` and memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE GUIDANCE**

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release for Django framework guidance |
