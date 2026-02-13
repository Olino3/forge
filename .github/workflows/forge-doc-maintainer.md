---
description: "Keep Forge documentation synchronized and concise"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "weekly on thursday"
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
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "documentation"]
    title-prefix: "[docs] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# Forge Doc Maintainer

Keep Forge documentation accurate and scannable. This workflow consolidates the former `doc-sync` and `doc-unbloat` workflows into a single two-stage pipeline.

## Stage 1: Synchronize Documentation

Validate and update these documents when they drift from codebase reality:

- `README.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `COOKBOOK.md`
- `forge-plugin/context/index.md`
- Domain index files under `forge-plugin/context/*/index.md`

### Sync Checks

1. **Count accuracy** — Documented counts for skills, agents, commands, hooks, context files, external skills, and plugins must match the repository.
2. **Path and structure accuracy** — Documented file paths and structure examples must still exist and match current layout.
3. **Reference integrity** — Referenced commands, skills, agents, scripts, and workflow files must actually exist.
4. **Capability claim accuracy** — Remove or correct stale capability claims no longer true.
5. **Index consistency** — Context index listings must match files present in each domain.

## Stage 2: Unbloat Documentation

Review documentation in:

- `README.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `COOKBOOK.md`
- `TROUBLESHOOTING.md`
- `forge-plugin/hooks/HOOKS_GUIDE.md`

### Unbloat Rules

1. Remove duplicate paragraphs or repeated guidance within the same file.
2. Replace overly long prose with concise bullet points when meaning is unchanged.
3. Keep canonical details in one place; convert duplicates to short references.
4. Preserve all critical technical constraints, safety rules, and workflow requirements.
5. Do not change factual meaning, policy intent, or required checklists.

## Stage 3: Generate PR

Create **one PR** combining sync corrections and unbloat improvements.

## Constraints

- Keep edits minimal, factual, and behavior-safe.
- Do not rewrite style or tone unless needed for correctness.
- Prefer focused updates over broad reformatting.
- Avoid touching generated files or lock files.
- If nothing is out of sync and no bloat found, make no changes.
