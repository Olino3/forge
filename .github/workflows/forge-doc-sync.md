---
description: "Keep Forge top-level documentation in sync with codebase reality"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 7 * * 1-5"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "documentation", "sync"]
    title-prefix: "[docs] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# Forge Doc Sync

Keep high-signal Forge documentation aligned with repository reality.

## Scope

Validate and update these documents when needed:

- `README.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `COOKBOOK.md`
- `forge-plugin/context/index.md`
- Domain index files under `forge-plugin/context/*/index.md`

## Checks

1. **Count accuracy**
   - Ensure documented counts for skills, agents, commands, hooks, context files, external skills, and plugins match the repository.
2. **Path and structure accuracy**
   - Ensure documented file paths and structure examples still exist and match current layout.
3. **Reference integrity**
   - Ensure referenced commands, skills, agents, scripts, and workflow files actually exist.
4. **Capability claim accuracy**
   - Remove or correct stale capability claims that are no longer true.
5. **Index consistency**
   - Ensure context index listings match files present in each domain.

## Constraints

- Keep edits minimal, factual, and behavior-safe.
- Do not rewrite style or tone unless needed for correctness.
- Prefer focused updates over broad reformatting.
- If nothing is out of sync, make no changes.

## Output

Create one documentation-sync PR only when meaningful mismatches are found.
