---
name: typescript
version: "1.0.0"
description: TypeScript advanced types, generics, and strict configuration
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, tsconfig_profile.md, type_patterns.md, migration_notes.md]
    - type: "shared-project"
      usage: "reference"
tags: [programming-languages, typescript, typing, engineering]
---

# Skill: typescript - Advanced TypeScript Architecture

## Purpose

Deliver expert TypeScript guidance focused on expressive types, strict compiler configuration, and safe API design.

## File Structure

```
forge-plugin/skills/typescript/
├── SKILL.md
└── examples.md
```

## Interface References

- **Context**: Load guidance via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Store project knowledge via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Output**: Save reports to `/claudedocs/` using [OUTPUT_CONVENTIONS.md](../OUTPUT_CONVENTIONS.md)

## Mandatory Workflow

### Step 1: Initial Analysis

- Identify TypeScript version, build pipeline, and project scope
- Review `tsconfig` strictness, module resolution, and emit targets
- Capture API surface areas and typing pain points

### Step 2: Load Memory

- Use `memoryStore.getSkillMemory("typescript", "{project-name}")` to load conventions
- Review cross-skill notes via `memoryStore.getByProject("{project-name}")`

### Step 3: Load Context

- Use `contextProvider.getDomainIndex("engineering")` to select relevant guidance
- Load only the context files required for the task

### Step 4: Perform Analysis

- Evaluate advanced type usage (conditional, mapped, template literal types)
- Assess API boundaries, generics, and inference ergonomics
- Identify unsafe `any`, type assertion hotspots, and strictness gaps
- Provide migration guidance for incremental typing improvements

### Step 5: Generate Output

- Deliver type strategy recommendations and code examples
- Save the report to `/claudedocs/typescript_{project}_{YYYY-MM-DD}.md` following OUTPUT_CONVENTIONS

### Step 6: Update Memory

- Record tsconfig decisions, type patterns, and migration status
- Update memory with `memoryStore.update("typescript", "{project-name}", ...)`

## Compliance Checklist

- [ ] Step 1 captured TypeScript version and tsconfig scope
- [ ] Step 2 loaded project memory via MemoryStore
- [ ] Step 3 loaded relevant context via ContextProvider
- [ ] Step 4 analysis covered typing, APIs, and strictness
- [ ] Step 5 output saved to `/claudedocs/` with correct naming
- [ ] Step 6 memory updated with new insights

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release |
