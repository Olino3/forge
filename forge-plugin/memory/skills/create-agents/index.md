# Memory Structure: create-agents

## Purpose

This directory stores **project-specific** agent creation patterns, naming conventions, and delegation strategies learned during custom agent design sessions. Each project gets its own subdirectory to maintain isolated, project-specific knowledge.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/engineering/`): **Shared, static** engineering standards and patterns
- **Memory** (this directory): **Project-specific, dynamic** agent creation patterns (naming conventions, common skill mappings, delegation strategies)

**Example**:
- Context says: "Agents require paired .md and .config.json files"
- Memory records: "In this project, specialist agents use sonnet model, always include Grep and Glob tools, and delegate to language-specific review skills"

## Directory Structure

```
create-agents/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── agent_patterns.md       # Common agent configuration patterns
    └── delegation_strategies.md # Delegation and sub-agent strategies
```

## Memory Files

### 1. `agent_patterns.md`

**What to store**:
- Agent naming conventions used in the project
- Common tool access patterns (which tools are typically needed)
- Preferred model tiers for different agent types
- Skill-to-domain mappings that work well
- Config.json template patterns
- Context domain assignments

**When to update**: After each agent creation when new patterns observed

### 2. `delegation_strategies.md`

**What to store**:
- How agents delegate to sub-agents in this project
- Which agents commonly work together
- Autonomy levels for different task types
- Escalation paths and decision criteria
- Cross-agent communication patterns

**When to update**: After creating agents with delegation rules

## Workflow

### When Creating Memory (First Time)

1. **During Step 2 (Load Memory)**: Check if `{project-name}/` exists, note first session
2. **During Step 7 (Update Memory)**: Create directory and initial files

### When Using Existing Memory (Subsequent Times)

1. **During Step 2 (Load Memory)**: Read patterns and strategies to guide design
2. **During Step 7 (Update Memory)**: Append new patterns discovered

## Related Files

- `../../index.md` — Overall memory system explanation
- `../../../skills/create-agents/SKILL.md` — Skill workflow documentation
- `../../../interfaces/schemas/agent_config.schema.json` — Agent config validation schema
