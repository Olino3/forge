---
name: dotnet-core
version: "1.0.0"
description: .NET Core and ASP.NET Core architecture guidance for building secure, scalable backend services. Covers solution structure, dependency injection, middleware, data access, security, performance, and deployment.
context:
  primary_domain: "dotnet"
  always_load_files: []
  detection_required: true
  file_budget: 5
memory:
  scopes:
    - type: "skill-specific"
      files: [solution_overview.md, api_patterns.md, data_access.md, deployment_notes.md]
    - type: "shared-project"
      usage: "reference"
tags: ["backend", "framework", "dotnet", "aspnet-core", "backend-frameworks"]
---

# .NET Core Framework Expert

## Category
Backend & Frameworks

## ⚠️ MANDATORY COMPLIANCE ⚠️
**CRITICAL**: The 6-step workflow outlined in this document MUST be followed in exact order for EVERY .NET Core engagement. Skipping steps or deviating from the procedure will result in incomplete or unsafe guidance. This is non-negotiable.

## File Structure
- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: .NET Core guidance scenarios with sample outputs

## Interface References
- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)

## Focus Areas
1. **Solution Architecture**: project layout, layered patterns, clean architecture
2. **ASP.NET Core Pipeline**: middleware ordering, filters, minimal APIs vs controllers
3. **Dependency Injection**: service lifetimes, configuration, options pattern
4. **Data Access**: EF Core patterns, migrations, query optimization
5. **Security**: auth, authorization policies, secrets, input validation
6. **Performance**: caching, async IO, health checks, resilience policies
7. **Testing**: xUnit, integration testing, test containers

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Scope the .NET Core Engagement (REQUIRED)
**YOU MUST:**
1. Identify .NET runtime version and hosting target (IIS, Kestrel, containers)
2. Clarify service type (API, worker, background service)
3. Determine data access stack (EF Core, Dapper, Cosmos SDK)
4. Ask clarifying questions on auth, performance requirements, and deployment
5. **Think through your implementation plan in a `<thinking>` block before writing any files or recommending changes**

**DO NOT PROCEED WITHOUT A CLEAR SCOPE AND PLAN**

### ⚠️ STEP 2: Load Project Memory (REQUIRED)
**YOU MUST:**
1. Load memory with `memoryStore.getSkillMemory("dotnet-core", "{project-name}")`
2. Review cross-skill memory with `memoryStore.getByProject("{project-name}")`
3. Note existing solution conventions and architectural decisions

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)
**YOU MUST:**
1. Use `contextProvider.getDomainIndex("dotnet")` to identify ASP.NET Core context
2. Load .NET patterns via `contextProvider.getConditionalContext("dotnet", "aspnet")`
3. Pull security context with `contextProvider.getCrossDomainContext("dotnet", ["auth", "security"])`
4. Stay within the declared file budget

**DO NOT PROCEED WITHOUT RELEVANT CONTEXT**

### ⚠️ STEP 4: Analyze Architecture & Code Paths (REQUIRED)
**YOU MUST:**
1. Review solution layout, project dependencies, and API boundaries
2. Inspect middleware pipeline and authentication configuration
3. Evaluate data access patterns, migrations, and transaction handling
4. Check resilience patterns (retry, circuit breaker, timeouts)

**DO NOT PROCEED WITHOUT A COMPLETE ANALYSIS**

### ⚠️ STEP 5: Provide .NET Core Guidance (REQUIRED)
**YOU MUST:**
1. Recommend architecture and DI improvements
2. Provide security guidance for auth and policy enforcement
3. Suggest performance optimizations and testing strategies

**DO NOT PROVIDE GENERIC OR UNSUPPORTED RECOMMENDATIONS**

### ⚠️ STEP 6: Generate Output & Update Memory (REQUIRED)
**YOU MUST:**
1. Produce a structured report in `/claudedocs/dotnet-core_{project}_{YYYY-MM-DD}.md`
2. Follow the naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Update memory with `memoryStore.update("dotnet-core", "{project-name}", ...)`:
   - `solution_overview.md`
   - `api_patterns.md`
   - `data_access.md`
   - `deployment_notes.md`

**DO NOT FINISH WITHOUT SAVING OUTPUT AND UPDATING MEMORY**

---

## Compliance Checklist
Before completing ANY .NET Core task, verify:
- [ ] Step 1: Scope defined and plan documented in `<thinking>`
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()`
- [ ] Step 3: Context loaded via `contextProvider`
- [ ] Step 4: Architecture and code paths analyzed
- [ ] Step 5: .NET Core guidance provided with actionable recommendations
- [ ] Step 6: Output saved to `/claudedocs/` and memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE GUIDANCE**

---

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release for .NET Core framework guidance |
