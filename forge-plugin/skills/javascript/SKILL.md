---
name: javascript
version: "1.0.0"
description: Advanced JavaScript patterns, ES2024+, and runtime optimization
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, runtime_profile.md, module_strategy.md, performance_notes.md]
    - type: "shared-project"
      usage: "reference"
## tags: [programming-languages, javascript, es2024, runtime]

# Skill: javascript - Advanced JavaScript Engineering

## Purpose

Provide advanced JavaScript guidance across runtimes, focusing on modern language features, performance optimization, and robust async patterns.

## File Structure

```
forge-plugin/skills/javascript/
├── SKILL.md
└── examples.md
```

## Interface References

- **Context**: Load guidance via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Store project knowledge via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Output**: Save reports to `/claudedocs/` using [OUTPUT_CONVENTIONS.md](../OUTPUT_CONVENTIONS.md)

## Mandatory Workflow

### Step 1: Initial Analysis

- Identify runtime (Node.js, browser, edge) and deployment constraints
- Confirm module system (ESM/CJS) and bundler/tooling
- Capture performance goals and latency budgets

### Step 2: Load Memory

- Use `memoryStore.getSkillMemory("javascript", "{project-name}")` to load prior decisions
- Review cross-skill notes via `memoryStore.getByProject("{project-name}")`

### Step 3: Load Context

- Use `contextProvider.getDomainIndex("engineering")` to select relevant guidance
- Load only the context files required for the task

### Step 4: Perform Analysis

- Review async patterns (promise chains, async/await, streaming)
- Evaluate module boundaries, dependency graphs, and bundling strategy
- Identify performance optimizations (event loop, caching, memory usage)
- Address runtime-specific security and stability concerns

### Step 5: Generate Output

- Provide code samples, optimization plans, and rollout steps
- Save the report to `/claudedocs/javascript_{project}_{YYYY-MM-DD}.md` following OUTPUT_CONVENTIONS

### Step 6: Update Memory

- Record runtime constraints, module strategies, and performance baselines
- Update memory with `memoryStore.update("javascript", "{project-name}", ...)`

## Compliance Checklist

- [ ] Step 1 captured runtime and tooling constraints
- [ ] Step 2 loaded project memory via MemoryStore
- [ ] Step 3 loaded relevant context via ContextProvider
- [ ] Step 4 analysis covered async patterns and performance
- [ ] Step 5 output saved to `/claudedocs/` with correct naming
- [ ] Step 6 memory updated with new insights

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release |
