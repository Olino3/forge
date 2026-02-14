---
name: project-planning
version: 1.0.0
description: Generate structured planning docs for web projects with context-safe phases, verification criteria, and exit conditions. Creates IMPLEMENTATION_PHASES.md plus conditional docs (TECH_STACK_DECISIONS.md, MIGRATION_PLAN.md, API_CONTRACT.md, DATA_MODEL.md). Like Hephaestus drafting blueprints before the first strike of the hammer, this skill ensures every project begins with a clear plan.
context:
  primary_domain: engineering
  supporting_domains:
    - documentation
  memory:
    skill_memory: project-planning
    scopes:
      - planning_patterns
      - project_history
tags:
  - planning
  - workflow
  - project
  - phases
  - implementation
triggers:
  - new project
  - start a project
  - create app
##   - build app

# Project Planning

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 8-step workflow outlined in this document MUST be followed in exact order for EVERY project planning session. Skipping steps or deviating from the procedure will result in incomplete or inaccurate planning documents. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Planning scenarios with sample outputs
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("project-planning", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Planning Focus Areas

Project planning evaluates requirements across 7 focus areas:

1. **Project Scope**: Define boundaries, deliverables, and what is explicitly out of scope
2. **Tech Stack Selection**: Identify languages, frameworks, libraries, and infrastructure requirements
3. **Phase Decomposition**: Break the project into sequential, verifiable implementation phases
4. **Dependency Mapping**: Identify inter-phase dependencies and critical path items
5. **Verification Criteria**: Define how to confirm each phase is complete (tests pass, endpoints respond, UI renders)
6. **Exit Conditions**: Define what must be true before moving to the next phase
7. **Conditional Documents**: Determine which additional planning documents are needed based on project type

**Note**: The skill produces planning documents with actionable phases. It does not implement any code unless explicitly requested.

---

## Purpose

Generate structured planning docs for web projects with context-safe phases, verification criteria, and exit conditions. Creates IMPLEMENTATION_PHASES.md plus conditional docs (TECH_STACK_DECISIONS.md, MIGRATION_PLAN.md, API_CONTRACT.md, DATA_MODEL.md). Like Hephaestus drafting blueprints before the first strike of the hammer, this skill ensures every project begins with a clear plan.


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Gather project requirements from the user prompt or conversation context
2. Identify the target tech stack:
   - Language(s) (TypeScript, Python, Go, etc.)
   - Framework(s) (Next.js, FastAPI, Express, Django, etc.)
   - Database(s) (PostgreSQL, MongoDB, Redis, etc.)
   - Infrastructure (Docker, Kubernetes, cloud provider, etc.)
3. Determine project scope and complexity:
   - Greenfield vs migration vs extension of existing system
   - Number of major features or modules
   - Integration points (APIs, third-party services, auth providers)
4. Classify project type for conditional document generation:
   - **Greenfield**: New project from scratch → triggers TECH_STACK_DECISIONS.md
   - **Migration**: Moving between technologies → triggers MIGRATION_PLAN.md
   - **API-heavy**: Primary deliverable is an API surface → triggers API_CONTRACT.md
   - **Database-heavy**: Significant data modeling required → triggers DATA_MODEL.md

**DO NOT PROCEED WITHOUT IDENTIFYING PROJECT TYPE, TECH STACK, AND SCOPE**

### ⚠️ STEP 2: Load Memory (REQUIRED)

**YOU MUST:**
1. Identify the project name from the user prompt or ask the user
2. Use `memoryStore.getSkillMemory("project-planning", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
3. If memory exists, review previous planning patterns:
   - Check for similar project types planned before
   - Review phase structures that worked well in past projects
   - Note any lessons learned from prior planning sessions
4. **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from other skill executions
5. If no memory exists, you will create it after generating the plan

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

**YOU MUST:**
1. Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
2. Load supporting context for documentation standards
3. If the project uses specific technologies, load relevant domain context:
   - Python projects: `contextProvider.getIndex("python")`
   - JavaScript/TypeScript projects: `contextProvider.getIndex("javascript")`
   - Infrastructure projects: `contextProvider.getIndex("devops")`
4. Apply cross-domain triggers as defined in the [Cross-Domain Matrix](../../context/cross_domain.md)

**DO NOT PROCEED WITHOUT LOADING RELEVANT CONTEXT**

### ⚠️ STEP 4: Define Project Phases (REQUIRED)

**YOU MUST break the project into sequential implementation phases. Each phase MUST include:**

1. **Phase Name**: Clear, descriptive name (e.g., "Phase 1: Project Scaffolding & Dev Environment")
2. **Description**: What this phase accomplishes and why it matters
3. **Deliverables**: Concrete outputs produced by completing this phase
4. **Verification Criteria**: How to confirm the phase is complete:
   - Specific tests that pass
   - Endpoints that respond correctly
   - UI components that render
   - Commands that execute successfully
5. **Exit Conditions**: What must be true before moving to the next phase:
   - All deliverables produced
   - All verification criteria met
   - No blocking issues remaining
   - Documentation updated for completed work
6. **Estimated Effort**: Relative effort (Small / Medium / Large / XL)
7. **Dependencies**: Which prior phases must be complete before this phase can begin

**Phase design principles:**
- Each phase should be independently verifiable
- Earlier phases should establish foundations that later phases build upon
- No phase should require undoing work from a previous phase
- Phases should be small enough to complete in a focused session

**DO NOT PROCEED WITHOUT DEFINING ALL PHASES WITH COMPLETE METADATA**

### ⚠️ STEP 5: Generate IMPLEMENTATION_PHASES.md (REQUIRED)

**YOU MUST produce the master planning document with the following structure:**

1. **Project Overview**: Name, description, tech stack summary, and project type classification
2. **Phase Summary Table**:
   | Phase | Name | Effort | Dependencies |
   |-------|------|--------|--------------|
   | 1 | Project Scaffolding | Small | None |
   | 2 | Core Data Model | Medium | Phase 1 |
   | ... | ... | ... | ... |
3. **Detailed Phase Definitions**: Full phase details with all metadata from Step 4
4. **Dependency Graph**: Visual or textual representation of phase dependencies
5. **Milestones**: Key project milestones mapped to phase completions
6. **Risk Factors**: Known risks and mitigation strategies

**DO NOT PROCEED WITHOUT GENERATING THE MASTER PLANNING DOCUMENT**

### ⚠️ STEP 6: Generate Conditional Documents (REQUIRED)

**Based on the project type classification from Step 1, generate the appropriate additional documents:**

#### TECH_STACK_DECISIONS.md (Greenfield projects)
- Technology choices with rationale for each decision
- Alternatives considered and reasons for rejection
- Version pinning strategy
- Compatibility matrix between chosen technologies

#### MIGRATION_PLAN.md (Migration projects)
- Current state architecture summary
- Target state architecture summary
- Migration strategy (big bang, strangler fig, parallel run, etc.)
- Rollback plan for each migration step
- Data migration approach and validation strategy

#### API_CONTRACT.md (API-heavy projects)
- Endpoint inventory with HTTP methods and paths
- Request/response schemas for each endpoint
- Authentication and authorization requirements
- Error response format and error code catalog
- Versioning strategy

#### DATA_MODEL.md (Database-heavy projects)
- Entity relationship overview
- Table/collection definitions with field types and constraints
- Index strategy for query performance
- Migration/seeding approach
- Data validation rules

**Note**: A project may trigger multiple conditional documents (e.g., a greenfield API project generates both TECH_STACK_DECISIONS.md and API_CONTRACT.md).

**IF NO CONDITIONAL DOCUMENTS APPLY, DOCUMENT WHY AND PROCEED**

### ⚠️ STEP 7: Generate Output (REQUIRED)

**YOU MUST:**
1. Save all planning documents to the `/claudedocs/` directory
2. Use the output naming conventions:
   - `IMPLEMENTATION_PHASES.md` — master planning document
   - `TECH_STACK_DECISIONS.md` — tech stack rationale (if applicable)
   - `MIGRATION_PLAN.md` — migration strategy (if applicable)
   - `API_CONTRACT.md` — API surface definition (if applicable)
   - `DATA_MODEL.md` — data model specification (if applicable)
3. Confirm all output files were written successfully
4. List all generated documents with a brief description of each

**DO NOT SKIP OUTPUT GENERATION**

### ⚠️ STEP 8: Update Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.update(layer="skill-specific", skill="project-planning", project="{project-name}", ...)` to store:
   - **planning_patterns.md**: Record the phase structure used, project type classification, and which conditional documents were generated
   - **project_history.md**: Log the project name, date, tech stack, number of phases, and conditional documents produced
2. If this is the first planning session, create both memory files with initial data
3. If previous memory exists, append to history and update patterns with new learnings

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY project planning session, verify:
- [ ] Step 1: Project requirements gathered, tech stack identified, project type classified
- [ ] Step 2: Project memory checked via `memoryStore.getSkillMemory()` and prior patterns reviewed
- [ ] Step 3: Engineering and supporting domain context loaded via `contextProvider.getIndex()`
- [ ] Step 4: All phases defined with name, description, deliverables, verification criteria, exit conditions, effort, and dependencies
- [ ] Step 5: IMPLEMENTATION_PHASES.md generated with phase summary table, detailed definitions, and dependency graph
- [ ] Step 6: Conditional documents generated based on project type (or documented why none apply)
- [ ] Step 7: All output saved to `/claudedocs/` with correct naming conventions
- [ ] Step 8: Memory updated with planning patterns and project history

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE PLANNING SESSION**

---

## Output File Naming Convention

**Primary output**: `IMPLEMENTATION_PHASES.md`

**Conditional outputs** (generated based on project type):
- `TECH_STACK_DECISIONS.md` — greenfield projects
- `MIGRATION_PLAN.md` — migration projects
- `API_CONTRACT.md` — API-heavy projects
- `DATA_MODEL.md` — database-heavy projects

All files are saved to the `/claudedocs/` directory.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-06-30 | Initial release — 8-step mandatory workflow for structured project planning with verification criteria, exit conditions, and conditional document generation |
