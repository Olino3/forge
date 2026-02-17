---
name: java-architect
version: "1.0.0"
description: Enterprise Java architecture and design patterns
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, architecture_decisions.md, framework_stack.md, performance_notes.md]
    - type: "shared-project"
      usage: "reference"
tags: [programming-languages, java, architecture, enterprise]
---

# Skill: java-architect - Enterprise Java Architecture

## Purpose

Provide architectural guidance for Java systems, emphasizing scalable design patterns, domain boundaries, and JVM performance considerations for enterprise services.

## File Structure

```
forge-plugin/skills/java-architect/
├── SKILL.md
└── examples.md
```

## Interface References

- **Context**: Load guidance via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Store project knowledge via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Output**: Save reports to `/claudedocs/` using [OUTPUT_CONVENTIONS.md](../OUTPUT_CONVENTIONS.md)

## Mandatory Workflow

### Step 1: Initial Analysis

- Identify Java version, build tool (Maven/Gradle), and deployment model
- Capture framework stack (Spring, Jakarta EE, Quarkus, Micronaut)
- Clarify primary goals: scalability, migration, or architecture review

### Step 2: Load Memory

- Use `memoryStore.getSkillMemory("java-architect", "{project-name}")` for project history
- Review cross-skill context via `memoryStore.getByProject("{project-name}")`

### Step 3: Load Context

- Use `contextProvider.getDomainIndex("engineering")` to pull architecture guidance
- Load only the necessary context files for the requested scope

### Step 4: Perform Analysis

- Evaluate bounded contexts, layering, and dependency direction
- Review persistence strategies, transaction boundaries, and caching
- Assess JVM performance (GC strategy, thread pools, connection pools)
- Recommend resilience patterns (retry, circuit breaker, bulkheads)

### Step 5: Generate Output

- Deliver architecture recommendations, diagrams, and phased plans
- Save the report to `/claudedocs/java-architect_{project}_{YYYY-MM-DD}.md` following OUTPUT_CONVENTIONS

### Step 6: Update Memory

- Capture architecture decisions, framework constraints, and scaling limits
- Update memory with `memoryStore.update("java-architect", "{project-name}", ...)`

## Compliance Checklist

- [ ] Step 1 documented platform, framework, and goals
- [ ] Step 2 loaded project memory via MemoryStore
- [ ] Step 3 loaded relevant context via ContextProvider
- [ ] Step 4 analysis covered architecture, data, and runtime concerns
- [ ] Step 5 output saved to `/claudedocs/` with correct naming
- [ ] Step 6 memory updated with new insights

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release |
