---
name: rails
version: "1.0.0"
description: Ruby on Rails development guidance for building reliable, secure web applications. Covers Rails conventions, MVC architecture, ActiveRecord patterns, background jobs, performance, testing, and deployment.
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, domain_models.md, job_queue_notes.md, performance_notes.md]
    - type: "shared-project"
      usage: "reference"
tags: ["backend", "framework", "rails", "ruby", "backend-frameworks"]
---

# Ruby on Rails Framework Expert

## Category
Backend & Frameworks

## ⚠️ MANDATORY COMPLIANCE ⚠️
**CRITICAL**: The 6-step workflow outlined in this document MUST be followed in exact order for EVERY Rails engagement. Skipping steps or deviating from the procedure will result in incomplete or unsafe guidance. This is non-negotiable.

## File Structure
- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Rails guidance scenarios with sample outputs

## Interface References
- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)

## Focus Areas
1. **Rails Conventions**: MVC structure, routes, concerns, service objects
2. **ActiveRecord**: associations, validations, callbacks, query tuning
3. **Background Jobs**: ActiveJob adapters, Sidekiq patterns, retries
4. **Security**: strong params, auth, CSRF, secrets management
5. **Performance**: caching layers, N+1 elimination, instrumentation
6. **Testing**: RSpec/Minitest, factories, system tests
7. **Deployment**: assets, environment configs, CI/CD

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Scope the Rails Engagement (REQUIRED)
**YOU MUST:**
1. Identify Rails version and deployment target
2. Clarify the domain (web app, API-only) and primary pain points
3. Determine background job stack and database choice
4. Ask clarifying questions on routes, models, and auth
5. **Think through your implementation plan in a `<thinking>` block before writing any files or recommending changes**

**DO NOT PROCEED WITHOUT A CLEAR SCOPE AND PLAN**

### ⚠️ STEP 2: Load Project Memory (REQUIRED)
**YOU MUST:**
1. Load memory with `memoryStore.getSkillMemory("rails", "{project-name}")`
2. Review cross-skill memory with `memoryStore.getByProject("{project-name}")`
3. Note existing conventions and known issues

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)
**YOU MUST:**
1. Use `contextProvider.getDomainIndex("engineering")` for architecture patterns
2. Pull security context with `contextProvider.getCrossDomainContext("engineering", ["auth", "security"])`
3. Stay within the declared file budget

**DO NOT PROCEED WITHOUT RELEVANT CONTEXT**

### ⚠️ STEP 4: Analyze Architecture & Code Paths (REQUIRED)
**YOU MUST:**
1. Review routes, controllers, and service objects
2. Inspect ActiveRecord models, scopes, and callbacks
3. Evaluate background job flows and retry strategies
4. Check caching and instrumentation setup

**DO NOT PROCEED WITHOUT A COMPLETE ANALYSIS**

### ⚠️ STEP 5: Provide Rails Guidance (REQUIRED)
**YOU MUST:**
1. Recommend improvements to models, services, and jobs
2. Provide security and performance guidance
3. Suggest testing strategies for critical paths

**DO NOT PROVIDE GENERIC OR UNSUPPORTED RECOMMENDATIONS**

### ⚠️ STEP 6: Generate Output & Update Memory (REQUIRED)
**YOU MUST:**
1. Produce a structured report in `/claudedocs/rails_{project}_{YYYY-MM-DD}.md`
2. Follow the naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Update memory with `memoryStore.update("rails", "{project-name}", ...)`:
   - `project_overview.md`
   - `domain_models.md`
   - `job_queue_notes.md`
   - `performance_notes.md`

**DO NOT FINISH WITHOUT SAVING OUTPUT AND UPDATING MEMORY**

---

## Compliance Checklist
Before completing ANY Rails task, verify:
- [ ] Step 1: Scope defined and plan documented in `<thinking>`
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()`
- [ ] Step 3: Context loaded via `contextProvider`
- [ ] Step 4: Architecture and code paths analyzed
- [ ] Step 5: Rails guidance provided with actionable recommendations
- [ ] Step 6: Output saved to `/claudedocs/` and memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE GUIDANCE**

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release for Rails framework guidance |
