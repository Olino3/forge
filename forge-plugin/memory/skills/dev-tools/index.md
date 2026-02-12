# Memory Structure: dev-tools

## Purpose

This directory stores **project-specific** workflow patterns, tool preferences, and pipeline configurations learned during developer workflow orchestration. Each project gets its own subdirectory to maintain isolated, project-specific knowledge.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/engineering/`): **Shared, static** engineering standards and best practices
- **Memory** (this directory): **Project-specific, dynamic** workflow preferences (preferred pipelines, tool configurations, step customizations)

**Example**:
- Context says: "Use code review before committing"
- Memory records: "In this project, the review pipeline uses `python-code-review` with FastAPI focus, always checks rate limiting, and prefers `black` formatting"

## Directory Structure

```
dev-tools/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── workflow_patterns.md    # Preferred pipelines and step configurations
    └── tool_preferences.md     # Project-specific tool and framework preferences
```

## Memory Files

### 1. `workflow_patterns.md`

**What to store**:
- Which pipelines are most frequently used for this project
- Custom pipeline configurations and step overrides
- Step success/failure history for optimization
- Common step sequences that work well together
- Pipeline timing data for performance optimization

**When to update**: After each pipeline execution

### 2. `tool_preferences.md`

**What to store**:
- Test runner and framework (pytest, jest, etc.)
- Linter and formatter (black, eslint, prettier, etc.)
- Build tool (webpack, vite, etc.)
- Code review focus areas for this project
- Documentation tooling preferences
- Git workflow conventions (branch naming, merge strategy)

**When to update**: When new tool preferences are discovered

## Workflow

### When Creating Memory (First Time)

1. **During Step 2 (Load Memory)**: Check if `{project-name}/` exists, note first session
2. **During Step 6 (Update Memory)**: Create directory and initial files

### When Using Existing Memory (Subsequent Times)

1. **During Step 2 (Load Memory)**: Load preferences to pre-configure pipeline
2. **During Step 6 (Update Memory)**: Update with new patterns and preferences

## Related Files

- `../../index.md` — Overall memory system explanation
- `../../../skills/dev-tools/SKILL.md` — Skill workflow documentation
- `../../../interfaces/skill_invoker.md` — Skill delegation patterns
- `../../../interfaces/execution_context.md` — Pipeline context passing
