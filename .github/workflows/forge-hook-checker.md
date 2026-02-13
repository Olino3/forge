---
description: "Validate Forge hook scripts for quality, safety, and performance"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  schedule: "weekly on friday"
  pull_request:
    types: [opened, synchronize]
    paths:
      - "forge-plugin/hooks/*.sh"
      - "forge-plugin/hooks/hooks.json"
      - "forge-plugin/hooks/HOOKS_GUIDE.md"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "hooks", "quality"]
    title-prefix: "[hook-quality] "
    max: 1
    close-older-issues: true
    expires: 14
---

# Forge Hook Quality Checker

Validate Forge hook scripts for reliability, safety, and adherence to the 5-second budget.

## Checks

For hooks under `forge-plugin/hooks/`:

1. `set -euo pipefail` is present in each `.sh`.
2. Optional grep-like checks fail safely when no matches are found.
3. Hooks using health reporting should source `forge-plugin/hooks/lib/health_buffer.sh`.
4. No long-running or blocking patterns that violate the <5s design target.
5. Hook scripts are registered in `forge-plugin/hooks/hooks.json`.
6. Hook behavior is documented in `forge-plugin/hooks/HOOKS_GUIDE.md`.
7. Scripts remain idempotent and non-destructive.

## Scope

- On pull requests, focus on changed hook assets.
- On schedule/manual runs, scan all hook scripts and manifests.

## Output

Open a single actionable issue only when meaningful violations are found, including:
- Failing hook name
- Rule violations with file/line evidence
- Suggested fix for each violation
