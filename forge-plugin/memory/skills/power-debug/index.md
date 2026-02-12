# Memory Structure: power-debug

## Purpose

This directory stores **project-specific** debugging patterns, resolved bug histories, and known fragile areas discovered during multi-agent investigation sessions. Each project gets its own subdirectory to maintain isolated, project-specific knowledge.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/engineering/`): **Shared, static** engineering standards and debugging best practices
- **Memory** (this directory): **Project-specific, dynamic** debugging history (resolved bugs, fragile areas, effective strategies)

**Example**:
- Context says: "Use binary search isolation to narrow down root causes"
- Memory records: "In this project, the sync job at `tasks/sync.py` uses module-level state that causes data corruption — always check for shared mutable state in Celery tasks"

## Directory Structure

```
power-debug/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── debug_patterns.md       # Effective debugging strategies for this project
    └── resolved_bugs.md        # History of bugs investigated and resolved
```

## Memory Files

### 1. `debug_patterns.md`

**What to store**:
- Debugging strategies that were most effective for this project
- Common root cause categories observed
- Known fragile areas of the codebase
- Cross-system interaction failure patterns
- Environmental factors that frequently cause issues

**When to update**: After each debugging session when new patterns are discovered

### 2. `resolved_bugs.md`

**What to store**:
- Bug symptoms and root causes (for future pattern matching)
- Investigation trails that led to resolution
- Fix strategies applied (quick, proper, preventive)
- Time from symptom to root cause (to measure investigation efficiency)
- Related areas that were ruled out (to avoid re-investigating)

**When to update**: After each successful bug resolution

## Workflow

### When Creating Memory (First Time)

1. **During Step 2 (Load Memory)**: Check if `{project-name}/` exists, note first session
2. **During Step 8 (Update Memory)**: Create directory and initial files

### When Using Existing Memory (Subsequent Times)

1. **During Step 2 (Load Memory)**: Check for similar symptoms in `resolved_bugs.md`
2. **During Step 8 (Update Memory)**: Append new bug resolution and patterns

## Related Files

- `../../index.md` — Overall memory system explanation
- `../../../skills/power-debug/SKILL.md` — Skill workflow documentation
- `../../../context/engineering/` — Engineering standards and practices
