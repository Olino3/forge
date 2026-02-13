---
name: "{skill-name}"
description: "{description}"
version: "0.3.0-alpha"
context:
  primary_domain: "{domain}"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
      usage: "reference"
---

# skill:{skill-name} - [Short Description]

## Version: 0.3.0-alpha

## Purpose

[What this skill does, when to use it, and what it produces]

## File Structure

```
skills/{skill-name}/
├── SKILL.md (this file)
├── examples.md
├── scripts/ (optional)
│   └── [helper scripts]
└── templates/ (optional)
    └── [output templates]
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather inputs (user parameters, target files, scope)
- Detect project type (language, framework, architecture)
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="{this-skill}"` and `domain="{domain}"`.

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `{domain}` domain. Stay within the file budget declared in frontmatter.

### Step 4: [Skill-Specific Core Action]

[Describe the main action this skill performs]

### Step 5: [Additional Skill-Specific Steps as Needed]

[Add more steps as needed for the skill's workflow]

### Step N-1: Generate Output

- Save output to `/claudedocs/{skill-name}_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Use templates from `templates/` directory if available

### Step N: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="{this-skill}"`. Store any newly learned patterns, conventions, or project insights.

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step N)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-02-11 | Refactored to use shared loading patterns; reduced boilerplate |
| 1.0.0 | YYYY-MM-DD | Initial release |
