---
description: "Monitor dependency and action updates, propose safe upgrade pull requests"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "daily"
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
    labels: ["forge-automation", "dependencies", "maintenance"]
    title-prefix: "[deps] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# Forge Dependency Update Sentinel

Monitor dependency surfaces and prepare low-risk upgrade pull requests with compatibility analysis.

## Dependency Surfaces

Prioritize these sources:

1. GitHub Actions versions in `.github/workflows/*.yml` and `.github/workflows/*.lock.yml`
2. Marketplace plugin references in `.claude-plugin/marketplace.json`
3. Submodule references in `.gitmodules`
4. Tooling/version pins in repository docs and scripts where explicitly versioned

## Analysis Steps

1. Identify outdated or vulnerable dependency references.
2. Propose upgrades that remain compatible with Forge conventions.
3. For each upgrade, include:
   - current version/reference
   - proposed version/reference
   - compatibility notes
   - rollback strategy
4. Apply only safe, bounded changes in one PR.

## PR Output

Create a single draft PR:

`[deps] update dependency references ({date})`

PR description should include:

- Risk summary (low/medium/high)
- Change table (before/after)
- Compatibility notes
- Validation checklist

## Constraints

- Do not modify unrelated files.
- Do not introduce breaking major version updates without explicit migration notes.
- If no safe updates are available, create no PR.
