---
description: "Track milestone progress daily and surface blockers with reprioritization guidance"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
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
  create-issue:
    labels: ["forge-automation", "milestones", "planning"]
    title-prefix: "[milestone] "
    max: 1
    close-older-issues: true
    expires: 14
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
