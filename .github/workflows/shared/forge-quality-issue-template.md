---
description: "Shared quality issue template contract for Forge issue-generating workflows"
---

When this workflow creates an issue, structure the body to align with `.github/ISSUE_TEMPLATE/quality_issue.yml`.

## Required Body Structure

Use this structure in order:

1. `## Summary`
2. `## Quality Issue Type`
3. `## Severity`
4. `## Affected Components`
5. `## Evidence`
6. `## Impact`
7. `## Proposed Remediation`
8. `## Validation Steps`
9. `## Additional Context`

## Required Metadata Block

Include this block at the top of every workflow-generated quality issue:

- `Template: quality_issue`
- `Source Workflow: {workflow-name}`
- `Run Trigger: {schedule|pull_request|manual}`
- `Detected On: {YYYY-MM-DD}`
- `Severity: {critical|warning|info}`

## Guardrails

- Create an issue only when there is a concrete, actionable finding.
- Include explicit file paths and evidence for every finding.
- Prefer one consolidated issue per run unless separate issues are clearly necessary.

