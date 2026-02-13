---
description: "Improve Forge components for best practices alignment and documentation clarity"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "weekly on wednesday"
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
    paths:
      - 'forge-plugin/skills/**'
      - 'forge-plugin/agents/**'
      - 'forge-plugin/commands/**'
      - 'forge-plugin/context/**'
  workflow_dispatch:
engine:
  id: copilot
  model: gemini-3-pro
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default, pull_requests]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "improvement", "best-practices"]
    title-prefix: "[improve] "
    expires: 14
    draft: true
    if-no-changes: "ignore"
---

# Forge Component Improver

Automatically improve Forge components (skills, agents, commands, context) for best practices alignment and documentation clarity. This workflow consolidates the former `best-practices-improver` and `skill-simplifier` workflows into a single multi-stage pipeline.

## Trigger-Specific Behavior

### On Pull Request (path-filtered)
Analyze only the **files changed in the triggering PR**. Focus improvements on those specific components.

### On Weekly Schedule
Scan the full `forge-plugin/` directory for improvement opportunities across all components.

## Stage 1: Analyze Best Practices Alignment

For each component in scope, check against current conventions:

**Skills** (`forge-plugin/skills/*/SKILL.md`):
- Does the skill follow the 6-step mandatory workflow? (Initial Analysis → Load Memory → Load Context → Perform Analysis → Generate Output → Update Memory)
- Are interface references used instead of hardcoded paths? (`contextProvider.getByTags()` not `../../context/`)
- Does the skill properly invoke `memoryStore` and `contextProvider`?
- Are examples provided in `examples.md`?

**Agents** (`forge-plugin/agents/*.md` + `*.config.json`):
- Does the `.config.json` validate against `agent_config.schema.json`?
- Are context domains, skills, and MCP references valid?
- Is the model choice appropriate for the agent's role?

**Commands** (`forge-plugin/commands/*.md`):
- Does YAML frontmatter include all required fields?
- Does the command properly use `ExecutionContext` for chaining?
- Are skill delegations using `skillInvoker` interface?

**Context** (`forge-plugin/context/**/*.md`):
- Does YAML frontmatter validate against `context_metadata.schema.json`?
- Are `tags` and `sections` arrays properly structured?
- Is `lastUpdated` current (within 90 days)?

## Stage 2: Simplify Documentation

For each component with verbose documentation:

1. Remove redundant explanations that repeat information from templates or conventions
2. Consolidate repetitive sections (e.g., merged constraint blocks)
3. Replace overly long prose with concise bullet points where meaning is preserved
4. Ensure examples remain comprehensive but not over-engineered
5. Remove dead references to non-existent files

## Stage 3: Generate Improvement PR

If improvements found, create a **single PR** with all changes:

- Categorize changes with inline comments: `[best-practices]` or `[simplify]`
- Include before/after metrics (word count, complexity) in PR body
- Only modify files that were in scope (changed in PR or entire repo for schedule)
- Preserve all meaningful content — only remove true redundancy
- Keep technical accuracy — don't simplify at cost of correctness

## Constraints

- ✅ **DO**: Cite specific conventions (CLAUDE.md, SKILL_TEMPLATE.md, schema files)
- ✅ **DO**: Provide before/after comparisons for each change
- ✅ **DO**: Preserve author's technical intent and domain expertise
- ❌ **DON'T**: Rewrite entire files (surgical improvements only)
- ❌ **DON'T**: Change behavior without citing convention source
- ❌ **DON'T**: Create PRs for trivial style issues
- If nothing needs improvement, make no changes (safe-outputs `if-no-changes: "ignore"` handles this)
