---
name: csharp
version: "1.0.0"
description: C# language features and .NET ecosystem development
context:
  primary_domain: "dotnet"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, runtime_stack.md, csharp_conventions.md, known_issues.md]
    - type: "shared-project"
      usage: "reference"
## tags: [programming-languages, csharp, dotnet, engineering]

# Skill: csharp - .NET Language Expertise

## Purpose

Guide C# feature usage and .NET ecosystem decisions, including async workflows, LINQ, dependency injection, and performance tuning for modern runtimes.

## File Structure

```
forge-plugin/skills/csharp/
├── SKILL.md
└── examples.md
```

## Interface References

- **Context**: Load guidance via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Store project knowledge via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Output**: Save reports to `/claudedocs/` using [OUTPUT_CONVENTIONS.md](../OUTPUT_CONVENTIONS.md)

## Mandatory Workflow

### Step 1: Initial Analysis

- Identify .NET runtime and target framework (NET 6/7/8+)
- Confirm project type (ASP.NET Core, worker service, library, CLI)
- Capture style guidelines (nullable reference types, analyzers, formatting)

### Step 2: Load Memory

- Use `memoryStore.getSkillMemory("csharp", "{project-name}")` for existing conventions
- Review cross-skill insights via `memoryStore.getByProject("{project-name}")`

### Step 3: Load Context

- Use `contextProvider.getDomainIndex("dotnet")` to select relevant .NET guidance
- Load only the context files required for the task

### Step 4: Perform Analysis

- Evaluate async/await usage, cancellation tokens, and exception flow
- Review LINQ usage, allocation hotspots, and data access patterns
- Validate DI lifetimes, configuration bindings, and logging strategy
- Check nullability annotations, generics, and API surface consistency

### Step 5: Generate Output

- Provide implementation guidance with concise code samples
- Save the report to `/claudedocs/csharp_{project}_{YYYY-MM-DD}.md` following OUTPUT_CONVENTIONS

### Step 6: Update Memory

- Record framework versions, architectural decisions, and recurring issues
- Update memory with `memoryStore.update("csharp", "{project-name}", ...)`

## Compliance Checklist

- [ ] Step 1 captured runtime, project type, and standards
- [ ] Step 2 loaded project memory via MemoryStore
- [ ] Step 3 loaded relevant context via ContextProvider
- [ ] Step 4 analysis covered language, runtime, and architecture concerns
- [ ] Step 5 output saved to `/claudedocs/` with correct naming
- [ ] Step 6 memory updated with new insights

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release |
