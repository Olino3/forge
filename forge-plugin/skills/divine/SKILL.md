---
name: "divine"
description: "Entry point to the divine toolkit — skills, agents, and commands that work with Claude Code's capabilities. Discovers available skills, agents, commands, and recommends the right tool for any task."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
      usage: "reference"
tags: ["planning", "workflow", "discovery", "toolkit", "meta"]
---

# skill:divine - Divine Toolkit Entry Point

## Version: 1.0.0

## Purpose

The divine skill is the master entry point for The Forge's entire toolkit. It discovers and catalogs all available skills, agents, and commands, then recommends the optimal tool or workflow for a given task. Use this skill when users need guidance on which Forge capabilities to employ, when exploring what's available, or when orchestrating multi-skill workflows.

## File Structure

```
skills/divine/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather user intent (what task or problem they want to solve)
- Determine the scope: skill discovery, agent recommendation, command lookup, or full workflow orchestration
- Identify whether the user needs a single tool or a multi-tool workflow

### Step 2: Load Memory

- Use `memoryStore.getSkillMemory("divine", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
- Load previously recommended workflows and their outcomes
- Retrieve user preference patterns for tool selection

### Step 3: Load Context

- Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- Load the skill registry (all available SKILL.md files)
- Load the agent registry (all agent .config.json files)
- Load the command registry (all command .md files)

### Step 4: Discover Available Tools

- Enumerate all skills, agents, and commands in The Forge
- Classify each by category, domain, and capability
- Build an indexed catalog with triggers, descriptions, and prerequisites

### Step 5: Match Task to Tools

- Analyze the user's task against the catalog
- Score each tool for relevance based on:
  - Domain alignment (language, framework, infrastructure)
  - Task type match (review, generate, plan, analyze, deploy)
  - Trigger keyword matches
  - Historical success from memory
- Rank recommendations by confidence

### Step 6: Compose Workflow

- For simple tasks: recommend a single skill, agent, or command
- For complex tasks: compose a multi-step workflow with:
  - Ordered skill invocations via `skillInvoker`
  - Agent delegation assignments
  - Command sequences
  - Data flow between steps
- Include estimated effort and prerequisites for each step

### Step 7: Generate Output

- Save output to `/claudedocs/divine_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Present recommendations with rationale and confidence scores

### Step 8: Update Memory

- Use `memoryStore.update(layer="skill-specific", skill="divine", project="{project-name}", ...)` to store insights. See [MemoryStore Interface](../../interfaces/memory_store.md).
- Record which tools were recommended and for what tasks
- Track user feedback on recommendation quality
- Update preference patterns for future recommendations

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Memory loaded via `memoryStore.getSkillMemory()` (Step 2)
- [ ] Context loaded via `contextProvider.getIndex()` (Step 3)
- [ ] Tool discovery completed with full catalog (Step 4)
- [ ] Task-to-tool matching performed with scoring (Step 5)
- [ ] Output saved with standard naming convention
- [ ] Memory updated via `memoryStore.update()` (Step 8)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — toolkit discovery, task matching, workflow composition |
