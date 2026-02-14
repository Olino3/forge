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
    labels: ["forge-automation", "milestone-feature", "planning"]
    title-prefix: "[Feature] "
    max: 5
    expires: 30
---

# ⚠️ DEPRECATED: Forge Milestone Planner

**This workflow has been DEPRECATED and replaced by `forge-milestone-lifecycle.md`.**

- **Replacement**: [forge-milestone-lifecycle.md](./forge-milestone-lifecycle.md) (Planning Stage)
- **Migration Date**: 2026-02-13
- **Deprecation Phase**: Phase 3 — Pipeline Consolidation
- **Reason**: Consolidated with `forge-project-milestone-tracker.md` and `forge-milestone-progress-reviewer.md` to create unified milestone lifecycle management

**This workflow is disabled for automatic runs.** It can only be triggered manually via `workflow_dispatch` as an escape hatch. It will be deleted after 2 weeks of successful consolidated workflow operation.

---

# Forge Milestone Planner

Automatically plan and decompose newly created milestones into executable feature issues and associate relevant existing issues.

## Loop Prevention

If the triggering milestone is automation-generated (title contains `[automation]` or description contains `forge-automation`), do nothing.

## Planning Objectives

When a new milestone is created:

1. **Analyze milestone structure**:
   - Parse title and description
   - Extract acceptance criteria (checklist or numbered items)
   - Identify requirements (technical/functional specs)
   - Determine overall priority and effort level
   - Identify ambiguities or missing information

2. **Decompose into feature issues** (3-5 focused items):
   - Break down milestone goals into distinct features
   - Map subset of acceptance criteria to each feature
   - Map relevant requirements to each feature
   - Assign priority (P0/P1/P2/P3) based on milestone priority + feature criticality
   - Estimate effort level (small/medium/large) based on complexity
   - Identify questions or clarifications needed

3. **Associate existing issues**:
   - Search for open issues matching milestone keywords/domain
   - Analyze semantic relevance to milestone goals
   - Filter out issues already assigned to other milestones
   - Filter out automation-generated issues
   - Add comment explaining association rationale

4. **Track completion criteria**:
   - Monitor when all acceptance criteria are satisfied
   - Monitor when all requirements are met
   - Add status comment when milestone appears ready for review

## Feature Issue Structure

Each created feature issue should have:

**Title**: `[Feature] {brief feature description}`

**Body**:
```markdown
# Feature: {Name}

**Milestone**: #{milestone-number} {milestone-title}

## Description
{Clear description of what this feature accomplishes}

## Acceptance Criteria
- [ ] {criterion from milestone}
- [ ] {criterion from milestone}

## Requirements
- {requirement from milestone}
- {requirement from milestone}

## Priority
{P0|P1|P2|P3} — {brief rationale}

## Effort Estimate
{small|medium|large} — {brief reasoning}

## Implementation Notes
{Any technical considerations or dependencies}

## Questions for Maintainers
{If clarification needed, tag appropriate maintainers}
- [ ] @{maintainer}: {question}
```

**Labels**:
- `forge-automation`
- `milestone-feature`
- `priority:p0` (or p1/p2/p3)
- `effort:small` (or medium/large)
- `needs-clarification` (if questions exist)

## Existing Issue Association

For each relevant existing issue found:

1. Post a comment:
   ```markdown
   ## Associated with Milestone: {milestone-title}
   
   This issue has been associated with milestone #{milestone-number} because:
   - {reason 1: keyword match, domain relevance, etc.}
   - {reason 2}
   
   **Milestone Acceptance Criteria**:
   - [ ] {relevant criterion}
   
   cc: @{milestone-creator}
   ```

2. Request milestone assignment via safe-outputs (in comment, instruct to assign issue to milestone)

## Milestone Completion Detection

When analyzing milestone status:

- If all acceptance criteria appear met → add comment: "✅ All acceptance criteria satisfied. Ready for milestone review."
- If all requirements are satisfied → add label: `milestone:ready-for-review`
- If blockers exist → identify and list them
- Do NOT auto-close milestones (requires human review)

## Clarification Handling

When ambiguities or missing information is detected:

1. Add "Questions for Maintainers" section to feature issue
2. Tag milestone creator or default maintainers (@{milestone-creator})
3. Add label: `needs-clarification`
4. Provide specific, actionable questions

## Output Constraints

- Create maximum 5 feature issues per milestone
- Prioritize quality over quantity (3 well-defined features > 5 vague ones)
- Keep feature scope atomic (each should be independently completable)
- Associate only highly relevant existing issues (avoid noise)
- Questions should be specific and actionable
- Maintain alignment with ROADMAP priorities

## Integration Points

- **forge-project-milestone-tracker**: Daily tracker will monitor created feature issues
- **forge-project-manager-agent**: Weekly roadmap alignment includes new milestones
- **forge-issue-triage-agent**: Will triage created feature issues (coordinate to prevent double-triage)

## Coordination

- Avoid creating feature issues that duplicate existing open issues
- Check for similar milestones before decomposing
- Preserve milestone intent; do not invent out-of-scope features
- Keep decomposition aligned with milestone acceptance criteria
