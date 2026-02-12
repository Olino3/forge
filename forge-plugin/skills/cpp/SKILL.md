---
name: cpp
version: "1.0.0"
description: Modern C++ (C++17/20/23) development and best practices
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, toolchain_profile.md, performance_notes.md, known_issues.md]
    - type: "shared-project"
      usage: "reference"
tags: [programming-languages, cpp, modern-cpp, engineering]
---

# Skill: cpp - Modern C++ Development

## Purpose

Provide modern C++ guidance for new implementations, refactors, and performance tuning. Emphasize C++17/20/23 language features, safe resource management, and scalable architecture.

## File Structure

```
forge-plugin/skills/cpp/
├── SKILL.md
└── examples.md
```

## Interface References

- **Context**: Load guidance via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Store project knowledge via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Output**: Save reports to `/claudedocs/` using [OUTPUT_CONVENTIONS.md](../OUTPUT_CONVENTIONS.md)

## Mandatory Workflow

### Step 1: Initial Analysis

- Confirm target C++ standard (C++17/20/23) and compiler toolchain
- Identify build system (CMake, Bazel, Meson) and deployment targets
- Clarify goals: modernization, performance, safety, or API design

### Step 2: Load Memory

- Use `memoryStore.getSkillMemory("cpp", "{project-name}")` to load project-specific conventions
- Review cross-skill notes via `memoryStore.getByProject("{project-name}")`

### Step 3: Load Context

- Use `contextProvider.getDomainIndex("engineering")` to select relevant engineering guidance
- Load only the context files required for the current task and stay within the file budget

### Step 4: Perform Analysis

- Assess ownership and lifetime design (RAII, smart pointers, move semantics)
- Evaluate concurrency, synchronization, and lock-free patterns where applicable
- Review API boundaries, error handling, and ABI compatibility concerns
- Identify performance opportunities (allocation patterns, cache locality, algorithmic complexity)

### Step 5: Generate Output

- Deliver actionable guidance, code samples, and decision trade-offs
- Save the report to `/claudedocs/cpp_{project}_{YYYY-MM-DD}.md` following OUTPUT_CONVENTIONS

### Step 6: Update Memory

- Capture toolchain details, architectural decisions, and recurring pitfalls
- Update memory with `memoryStore.update("cpp", "{project-name}", ...)`

## Compliance Checklist

- [ ] Step 1 completed with project scope and C++ standard
- [ ] Step 2 loaded project memory via MemoryStore
- [ ] Step 3 loaded relevant context via ContextProvider
- [ ] Step 4 analysis covered safety, architecture, and performance
- [ ] Step 5 output saved to `/claudedocs/` with correct naming
- [ ] Step 6 memory updated with new insights

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release |
