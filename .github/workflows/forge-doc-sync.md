---
description: "DEPRECATED: Migrated to forge-doc-maintainer.md — see Phase 3 consolidation"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
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

# ⚠️ DEPRECATED: Forge Doc Sync

**This workflow has been DEPRECATED and replaced by `forge-doc-maintainer.md`.**

- **Replacement**: [forge-doc-maintainer.md](./forge-doc-maintainer.md)
- **Migration Date**: 2026-02-13
- **Deprecation Phase**: Phase 3 — Pipeline Consolidation
- **Reason**: Consolidated with `forge-doc-unbloat.md` to reduce duplication and create unified documentation maintenance pipeline

**This workflow is disabled for automatic runs.** It can only be triggered manually via `workflow_dispatch` as an escape hatch. It will be deleted after 2 weeks of successful consolidated workflow operation.

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
