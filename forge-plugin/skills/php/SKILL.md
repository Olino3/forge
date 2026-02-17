---
name: php
version: "1.0.0"
description: Professional PHP development guidance for modern backend services and web applications. Covers PHP 8+ best practices, framework conventions (Laravel/Symfony), security, performance, testing, and deployment.
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, framework_conventions.md, dependency_map.md, deployment_notes.md]
    - type: "shared-project"
      usage: "reference"
tags: ["backend", "framework", "php", "backend-frameworks"]
---

# PHP Framework Expert

## Category
Backend & Frameworks

## ⚠️ MANDATORY COMPLIANCE ⚠️
**CRITICAL**: The 6-step workflow outlined in this document MUST be followed in exact order for EVERY PHP engagement. Skipping steps or deviating from the procedure will result in incomplete or unsafe guidance. This is non-negotiable.

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
1. **Modern PHP Practices**: PHP 8+ features, strict typing, PSR standards
2. **Framework Conventions**: Laravel/Symfony architecture, routing, service containers
3. **Dependency Management**: Composer, autoloading, package boundaries
4. **Security**: input validation, auth, session management, secrets
5. **Performance**: caching, opcache, query optimization
6. **Testing**: PHPUnit/Pest, integration tests, mocking
7. **Deployment**: environment config, containerization, observability

---

## Purpose

Professional PHP development guidance for modern backend services and web applications. Covers PHP 8+ best practices, framework conventions (Laravel/Symfony), security, performance, testing, and deployment.


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Scope the PHP Engagement (REQUIRED)
**YOU MUST:**
1. Identify PHP version and framework (Laravel, Symfony, custom)
2. Clarify application type (API, web app, CLI) and deployment target
3. Determine database and cache layers
4. Ask clarifying questions on auth, routing, and packaging
5. **Think through your implementation plan in a `<thinking>` block before writing any files or recommending changes**

**DO NOT PROCEED WITHOUT A CLEAR SCOPE AND PLAN**

### ⚠️ STEP 2: Load Project Memory (REQUIRED)
**YOU MUST:**
1. Load memory with `memoryStore.getSkillMemory("php", "{project-name}")`
2. Review cross-skill memory with `memoryStore.getByProject("{project-name}")`
3. Note framework conventions and dependency rules

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)
**YOU MUST:**
1. Use `contextProvider.getDomainIndex("engineering")` for architecture patterns
2. Pull security context with `contextProvider.getCrossDomainContext("engineering", ["auth", "security"])`
3. Stay within the declared file budget

**DO NOT PROCEED WITHOUT RELEVANT CONTEXT**

### ⚠️ STEP 4: Analyze Architecture & Code Paths (REQUIRED)
**YOU MUST:**
1. Review routing and controller structure
2. Inspect service container usage and dependency configuration
3. Evaluate ORM or query patterns (Eloquent, Doctrine, PDO)
4. Check error handling, logging, and performance tooling

**DO NOT PROCEED WITHOUT A COMPLETE ANALYSIS**

### ⚠️ STEP 5: Provide PHP Guidance (REQUIRED)
**YOU MUST:**
1. Recommend framework-specific patterns (Laravel/Symfony)
2. Provide security and performance guidance
3. Suggest testing strategies and deployment improvements

**DO NOT PROVIDE GENERIC OR UNSUPPORTED RECOMMENDATIONS**

### ⚠️ STEP 6: Generate Output & Update Memory (REQUIRED)
**YOU MUST:**
1. Produce a structured report in `/claudedocs/php_{project}_{YYYY-MM-DD}.md`
2. Follow the naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Update memory with `memoryStore.update("php", "{project-name}", ...)`:
   - `project_overview.md`
   - `framework_conventions.md`
   - `dependency_map.md`
   - `deployment_notes.md`

**DO NOT FINISH WITHOUT SAVING OUTPUT AND UPDATING MEMORY**

---

## Compliance Checklist
Before completing ANY PHP task, verify:
- [ ] Step 1: Scope defined and plan documented in `<thinking>`
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()`
- [ ] Step 3: Context loaded via `contextProvider`
- [ ] Step 4: Architecture and code paths analyzed
- [ ] Step 5: PHP guidance provided with actionable recommendations
- [ ] Step 6: Output saved to `/claudedocs/` and memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE GUIDANCE**

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release for PHP framework guidance |
