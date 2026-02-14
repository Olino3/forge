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
    labels: ["forge-automation", "documentation", "unbloat"]
    title-prefix: "[docs-unbloat] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# ⚠️ DEPRECATED: Forge Doc Unbloat

**This workflow has been DEPRECATED and replaced by `forge-doc-maintainer.md`.**

- **Replacement**: [forge-doc-maintainer.md](./forge-doc-maintainer.md)
- **Migration Date**: 2026-02-13
- **Deprecation Phase**: Phase 3 — Pipeline Consolidation
- **Reason**: Consolidated with `forge-doc-sync.md` to reduce duplication and create unified documentation maintenance pipeline

**This workflow is disabled for automatic runs.** It can only be triggered manually via `workflow_dispatch` as an escape hatch. It will be deleted after 2 weeks of successful consolidated workflow operation.

---

# Forge Doc Unbloat

Improve documentation scannability by removing avoidable redundancy and verbosity.

## Scope

Review documentation in:

- `README.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `COOKBOOK.md`
- `TROUBLESHOOTING.md`
- `forge-plugin/hooks/HOOKS_GUIDE.md`

## Unbloat Rules

1. Remove duplicate paragraphs or repeated guidance that appears in the same file.
2. Replace overly long prose with concise bullet points when meaning is unchanged.
3. Keep canonical details in one place and convert duplicates to short references.
4. Preserve all critical technical constraints, safety rules, and workflow requirements.
5. Do not change factual meaning, policy intent, or required checklists.

## Constraints

- Make small, reviewable edits.
- Preserve existing structure unless simplification clearly improves readability.
- Avoid touching generated files or lock files.
- If no meaningful bloat is found, make no changes.

## Output

Create one documentation-unbloat PR with a concise summary of what was simplified and why.
