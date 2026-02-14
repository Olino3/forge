---
description: "DEPRECATED: Migrated to forge-milestone-lifecycle.md — see Phase 3 consolidation"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
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
  create-issue:
    labels: ["forge-automation", "milestones", "planning"]
    title-prefix: "[milestone] "
    max: 1
    close-older-issues: true
    expires: 14
---

# ⚠️ DEPRECATED: Forge Project Milestone Tracker

**This workflow has been DEPRECATED and replaced by `forge-milestone-lifecycle.md`.**

- **Replacement**: [forge-milestone-lifecycle.md](./forge-milestone-lifecycle.md) (Tracking Stage)
- **Migration Date**: 2026-02-13
- **Deprecation Phase**: Phase 3 — Pipeline Consolidation
- **Reason**: Consolidated with `forge-milestone-planner.md` and `forge-milestone-progress-reviewer.md` to create unified milestone lifecycle management

**This workflow is disabled for automatic runs.** It can only be triggered manually via `workflow_dispatch` as an escape hatch. It will be deleted after 2 weeks of successful consolidated workflow operation.

---

# Forge Project Milestone Tracker

Monitor roadmap milestones and produce a daily project execution report.

## Analysis Scope

1. Milestone progress:
   - open vs closed issues/PRs
   - completion percentage
   - expected vs actual throughput
2. Blocked items:
   - no activity for 7+ days
   - dependency blockers
   - awaiting review bottlenecks
3. Risk signals:
   - milestones with critical unresolved items
   - milestones missing linked implementation issues

## Output

Create one issue:

`[milestone] Daily Milestone Status — {YYYY-MM-DD}`

Body format:

```markdown
# Daily Milestone Status

## Summary
- Milestones tracked: {count}
- On track: {count}
- At risk: {count}
- Blocked items: {count}

## Milestone Progress
| Milestone | Completion | Open | Closed | Status |
|-----------|------------|------|--------|--------|

## Blocked Work
- #{issue-or-pr}: {blocker reason}

## Reprioritization Suggestions
1. {suggestion}
2. {suggestion}

## Recommended Actions (next 24h)
- [ ] {action}
```

## Constraints

- Focus on actionable status changes, not noise.
- Keep suggestions aligned with ROADMAP priorities.
