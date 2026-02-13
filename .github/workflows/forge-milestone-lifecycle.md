---
description: "Unified milestone lifecycle: planning, daily tracking, and PR progress review"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  milestone:
    types: [created, edited]
  schedule: "daily"
  workflow_dispatch:
engine:
  id: copilot
  model: claude-opus-4.6
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default, pull_requests]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "milestone", "planning"]
    title-prefix: "[milestone] "
    max: 5
    expires: 30
    close-older-issues: true
---

# Forge Milestone Lifecycle Manager

Comprehensive milestone management: planning, daily tracking, and progress analysis. This workflow consolidates the former `milestone-planner`, `project-milestone-tracker`, and `milestone-progress-reviewer` workflows.

## Trigger-Specific Behavior

### On Milestone Created/Edited

Run **Planning** mode:

1. **Analyze milestone structure**:
   - Parse title and description
   - Extract acceptance criteria (checklist or numbered items)
   - Identify requirements (technical/functional specs)
   - Determine overall priority and effort level

2. **Decompose into feature issues** (3-5 focused items):
   - Break down milestone goals into distinct features
   - Map acceptance criteria to each feature
   - Assign priority (P0-P3) based on milestone priority + criticality
   - Estimate effort level (small/medium/large)

3. **Associate existing issues**:
   - Search for open issues matching milestone keywords/domain
   - Filter out issues already assigned to other milestones
   - Filter out automation-generated issues

Each feature issue uses this title format: `[milestone] Feature: {brief description}`

Feature issue body:
```markdown
# Feature: {Name}

**Milestone**: #{milestone-number} {milestone-title}

## Description
{What this feature accomplishes}

## Acceptance Criteria
- [ ] {criterion from milestone}

## Priority
{P0|P1|P2|P3} — {rationale}

## Effort Estimate
{small|medium|large} — {reasoning}
```

Labels: `forge-automation`, `milestone`, `milestone-feature`, `priority:p{0-3}`, `effort:{small|medium|large}`

### On Daily Schedule

Run **Tracking** mode:

1. **Milestone progress**: Open vs closed issues/PRs, completion percentage
2. **Blocked items**: No activity for 7+ days, dependency blockers
3. **Risk signals**: Milestones with critical unresolved items

Create one tracking issue:

`[milestone] Daily Status — {YYYY-MM-DD}`

```markdown
# Daily Milestone Status

## Summary
- Milestones tracked: {count}
- On track: {count}
- At risk: {count}

## Milestone Progress
| Milestone | Completion | Open | Closed | Status |
|-----------|------------|------|--------|--------|

## Blocked Work
- #{issue}: {blocker reason}

## Recommended Actions (next 24h)
- [ ] {action}
```

## Loop Prevention

- If milestone title contains `[automation]` or description contains `forge-automation`, skip planning.
- For daily tracking, close-older-issues prevents stale status reports.

## Constraints

- Maximum 5 total issues per run (via safe-outputs max)
- Prioritize quality over quantity (3 well-defined features > 5 vague ones)
- Keep suggestions aligned with ROADMAP priorities
- Focus on actionable status changes, not noise
- Do not auto-close milestones (requires human review)

## Integration Points

- **forge-feature-decomposer**: Decomposes features into work items
- **forge-project-manager-agent**: Weekly roadmap alignment includes milestones
- **forge-stale-gardener**: Closes stale milestone issues after 30 days
