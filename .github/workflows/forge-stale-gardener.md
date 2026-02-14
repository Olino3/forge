---
description: "Identify stale issues and PRs, propose ping/close actions with grace-period handling"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
  - shared/model-gpt4.md
engine:
  id: copilot
  model: gpt-4.1
on:
  schedule: "weekly on saturday"
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
    labels: ["forge-automation", "stale", "maintenance"]
    title-prefix: "[stale] "
    max: 1
    close-older-issues: true
    expires: 14
---

# Forge Stale Issue/PR Gardener

Produce a weekly stale-work maintenance report with ping and closure recommendations.

## Staleness Policy

- Issues stale threshold: 30 days without meaningful activity
- PR stale threshold: 14 days without meaningful activity
- Grace period before closure recommendation: 7 days after ping

## Scope Rules

- Exclude items labeled `security` or `do-not-close`.
- Exclude automation-generated housekeeping issues unless explicitly requested.
- Prioritize stale work that blocks active milestones.

## Output

Create one issue:

`[stale] Weekly Stale Review — {YYYY-MM-DD}`

Body format:

```markdown
# Weekly Stale Review

## Summary
- Stale issues: {count}
- Stale PRs: {count}
- Blocking stale items: {count}

## Ping Now
- #{id}: @{assignee-or-author} — {reason stale} — Suggested comment: "{ping text}"

## Candidate Closures After Grace
- #{id}: {reason} — Earliest close date: {date}

## Keep Open (Explicitly Justified)
- #{id}: {justification}

## Maintainer Checklist
- [ ] Post pings
- [ ] Apply stale labels
- [ ] Close grace-expired items with summary comments
```

## Constraints

- Keep recommendations conservative and reversible.
- Include rationale for every closure recommendation.
