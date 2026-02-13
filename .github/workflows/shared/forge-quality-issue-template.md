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

## Standard Issue Quality Requirements

All workflow-generated issues must include:

1. **Evidence:** File paths, line numbers, exact error messages, or failing validation rules
2. **Remediation:** Concrete, actionable steps to resolve the issue
3. **Severity:** Appropriate classification (critical/warning/info) when applicable
4. **Scope:** Specific components, files, or assets affected

### Anti-Patterns to Avoid

- Creating issues for style preferences without convention backing
- Vague findings without file paths or line numbers
- Multiple issues for the same root cause (consolidate when possible)
- Issues for experimental code or intentional divergence from conventions

## Usage in Workflows

Workflows should reference these requirements in their "Output" sections and add workflow-specific details:

```markdown
## Output

Create issues following the [standard quality requirements](shared/forge-quality-issue-template.md#standard-issue-quality-requirements).

For this workflow, include:
- {Workflow-specific requirement 1}
- {Workflow-specific requirement 2}
- {Workflow-specific requirement 3}
```
