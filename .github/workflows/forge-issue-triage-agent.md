---
description: "DECOMMISSIONED — Triage new issues with labels, priority, and assignment recommendations (manual dispatch only)"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  workflow_dispatch:
# DECOMMISSIONED: 96% no-op rate, low value in single-maintainer project
# issues:
#   types: [opened, reopened]
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "triage", "planning"]
    title-prefix: "[triage] "
    max: 1
    expires: 14
---

# Forge Issue Triage Agent

Analyze newly opened issues and generate structured triage decisions.

## Loop Prevention

If the triggering issue is automation-generated (title starts with `[triage]` or contains `forge-automation` label), do nothing.

## Triage Objectives

For each eligible issue:

1. Detect issue type from template/body:
   - bug report
   - feature request
   - documentation improvement
   - security concern
   - quality issue
2. Recommend labels:
   - type label
   - priority (`priority:p0`..`priority:p3`)
   - area (`area:workflows`, `area:docs`, `area:hooks`, etc.)
3. Suggest likely owner/assignee role.
4. Determine next action:
   - needs reproduction
   - needs design review
   - ready for implementation
   - needs security-private follow-up

## Output

Create one triage issue:

`[triage] #{issue-number} {original-title}`

Issue body format:

```markdown
# Triage Recommendation for #{issue-number}

## Intake Summary
- Source issue: #{issue-number}
- Detected type: {bug|feature|docs|security|quality}
- Confidence: {high|medium|low}

## Recommended Labels
- type:{...}
- priority:{...}
- area:{...}

## Priority Rationale
{reasoning}

## Assignment Suggestion
- Suggested owner: @{user-or-team}
- Why: {domain match}

## Next Action
- {specific next step}

## Notes
- If security-related, route to SECURITY.md private process.
```

## Constraints

- One triage issue per source issue.
- Keep recommendations actionable and evidence-based.
- Do not expose sensitive details from security-related reports.

