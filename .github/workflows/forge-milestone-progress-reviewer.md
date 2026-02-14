---
description: "DEPRECATED: Migrated to forge-milestone-lifecycle.md — see Phase 3 consolidation"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default, pull_requests]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "progress-gap", "planning"]
    max: 5
    expires: 30
---

# ⚠️ DEPRECATED: Forge Milestone Progress Reviewer

**This workflow has been DEPRECATED and replaced by `forge-milestone-lifecycle.md`.**

- **Replacement**: [forge-milestone-lifecycle.md](./forge-milestone-lifecycle.md) (Review Stage)
- **Migration Date**: 2026-02-13
- **Deprecation Phase**: Phase 3 — Pipeline Consolidation
- **Reason**: Consolidated with `forge-milestone-planner.md` and `forge-project-milestone-tracker.md` to create unified milestone lifecycle management

**This workflow is disabled for automatic runs.** It can only be triggered manually via `workflow_dispatch` as an escape hatch. It will be deleted after 2 weeks of successful consolidated workflow operation.

---

# Original: Forge Milestone Progress Reviewer

Evaluate milestone and feature delivery progress on each PR. Identify gaps in work coverage and create remediation issues (work items or features) to maintain milestone trajectory.

## IMMEDIATE MILESTONE CHECK

**CRITICAL: Execute this check BEFORE any detailed analysis to avoid wasted runs.**

1. Check if PR title or body contains issue references (#NNN pattern or "Fixes #NNN")
2. Check if PR has a milestone field assigned
3. If NEITHER condition is met:
   - Output "No milestone association detected. PR is not milestone-related. Exiting."
   - Stop immediately without further analysis
4. If EITHER condition is met, proceed to Loop Prevention checks

Do NOT perform detailed Association Detection Hierarchy analysis, issue fetching, or milestone metadata collection before completing this quick check.

## Loop Prevention

If the triggering PR meets any of these conditions, do nothing:
- Has label `forge-automation`
- Title starts with `[Work item]`, `[Feature]`, `[milestone]`, `[best-practices]`, `[triage]`
- Is from a bot account
- Has no milestone association (see Association Detection below)

## Association Detection Hierarchy

Determine the PR's relationship to milestones by checking in this order:

### 1. Work Item Association
Check if PR references an issue with `work-item` label:
- Parse PR title for `#123` or `Fixes #123` patterns
- Parse PR body for issue references
- Parse PR branch name for issue numbers (e.g., `fix-123-bug`)
- If work item found:
  - Extract parent feature from work item's body (references `Parent Feature: #456`)
  - Extract milestone from parent feature or work item's milestone field
  - **Association**: work item #123 → feature #456 → milestone #789

### 2. Milestone Feature Association
If no work item found, check if PR references an issue with `milestone-feature` label:
- Parse PR title/body/branch for issue references
- If milestone-feature found:
  - Extract milestone from feature's milestone field or body
  - **Association**: feature #456 → milestone #789

### 3. Direct Milestone Association
If no feature found, check if PR has direct milestone:
- Check PR's milestone field
- Parse PR body for milestone references (e.g., "Part of milestone #789")
- **Association**: PR → milestone #789

### 4. No Association
If none of the above found:
- **Skip processing** — PR is not milestone-related
- Do not create any issues
- Exit workflow

## Milestone Progress Analysis

Once milestone association is established, analyze progress:

### 1. Collect Milestone Metadata
Use GitHub API to fetch:
- Milestone title, description, due date, state
- All issues associated with milestone
- All PRs associated with milestone
- Open vs closed counts

Parse milestone description for:
- **Acceptance criteria**: Look for checklist items (`- [ ]` or `- [x]`)
- **Requirements**: Numbered or bulleted lists of capabilities
- **Scope boundaries**: "In scope" and "Out of scope" sections

### 2. Categorize Milestone Issues
Group issues by label:
- **Work items**: Issues with `work-item` label
  - Count: Open vs Closed
  - Group by parent feature (parse `Parent Feature: #123` from body)
  - Calculate completion: Closed / Total
- **Features**: Issues with `milestone-feature` label
  - Count: Open vs Closed
  - Check decomposition status (has child work items?)
  - Calculate completion per feature
- **Other issues**: Issues without work-item or milestone-feature labels
  - Flag as potential missing categorization

### 3. Map Acceptance Criteria Coverage
For each acceptance criterion in milestone description:
- Search for work items or features that reference the criterion text
- Check if criterion is marked complete (`[x]`)
- Classify coverage:
  - **Covered**: Has work item(s) or feature addressing it
  - **Partial**: Has feature but insufficient work items
  - **Uncovered**: No work item or feature addresses it
  - **Complete**: Criterion is checked off AND all work items closed

### 4. Calculate Progress Metrics
```
Milestone Completion % = (Closed Work Items + Closed Features) / (Total Work Items + Total Features) × 100

Feature Completion % = (Closed Work Items for Feature) / (Total Work Items for Feature) × 100

Acceptance Coverage % = (Covered Criteria) / (Total Criteria) × 100

Velocity = (Work Items Closed Last 7 Days) / 7
```

### 5. Assess Current PR Contribution
Determine what this PR contributes:
- If associated with work item: "Implements work item #123"
- If associated with feature: "Contributes to feature #456"
- If direct milestone: "Directly addresses milestone #789"

Estimate PR's impact:
- Files changed count
- Lines added/removed
- Expected acceptance criteria addressed (parse from PR body)

## Gap Identification

Identify gaps that could prevent milestone completion:

### Gap Type 1: Missing Work Items
**Criteria**: Acceptance criterion has no work items
**Detection**:
- Criterion in milestone description is uncovered
- No open or closed work items reference the criterion text
- No feature issue addresses the criterion

**Example**:
- Milestone criterion: "Add input validation for all API endpoints"
- Search finds: No work items with "input validation" or "API endpoints"
- **Gap**: Missing work items for input validation

### Gap Type 2: Incomplete Feature Decomposition
**Criteria**: Feature has <50% work items compared to expected
**Detection**:
- Feature issue exists with acceptance criteria
- Feature has <3 work items OR <50% of feature's acceptance criteria have work items
- Feature is not closed

**Example**:
- Feature #456: "Implement OAuth authentication" with 6 acceptance criteria
- Work items found: 2 (both closed)
- **Gap**: Feature needs more work items (only 2/6 criteria covered)

### Gap Type 3: Missing Features
**Criteria**: Milestone goal has no feature issue
**Detection**:
- Milestone description lists major capability
- No feature issue with title matching the capability
- Capability scope > 300 LOC or spans multiple components

**Example**:
- Milestone description: "Add webhook support for external integrations"
- Search finds: No feature issue with "webhook" in title
- Estimated scope: >500 LOC, multiple components
- **Gap**: Missing feature for webhook support

### Gap Type 4: Scope Creep (Warning Only)
**Criteria**: PR modifies files outside expected scope
**Detection**:
- PR modifies files not mentioned in work item or feature
- PR adds functionality not in milestone acceptance criteria
- PR size significantly exceeds work item estimate

**Action**: Add comment to PR (no issue created)

### Gap Type 5: Blocked Progress
**Criteria**: Work items awaiting dependencies
**Detection**:
- Work item body lists "Depends on: #123"
- Dependency issue is still open
- No recent activity on dependency

**Action**: Add comment highlighting blocker (no issue created)

## Issue Generation Strategy

Based on gap type and size, create appropriate issues:

### Small Gap (<300 LOC) → Create Work Item

**Title Format**: `[Work item] {specific gap description}`

**Body Template**:
```markdown
# Work Item: {Name}

**Created by**: Milestone Progress Reviewer (analyzing PR #{pr-number})
**Parent Feature**: #{feature-number} {feature-title} _(if applicable)_
**Milestone**: #{milestone-number} {milestone-title}
**Gap Type**: {missing-work | coverage | decomposition}

## Description
This work item addresses a gap identified during milestone progress review.

**Gap Details**:
{Specific description of what's missing}

**Acceptance Criterion** (from milestone):
- [ ] {criterion text from milestone description}

## Scope
{Estimated files/components to modify based on gap analysis}

## Success Criteria
- [ ] {Specific verification steps}
- [ ] {Tests to add or update}
- [ ] {Documentation to update}

## Effort Estimate
{small|medium} — {reasoning based on scope}
- Estimated LOC: {< 100 | 100-300}
- Files modified: {1-3}
- Complexity: {low|medium}

## Context
This gap was identified because:
{Explanation of why this work is needed for milestone completion}

**Related PR**: #{pr-number}
**Detection Date**: {current-date}

## Priority
{Inherit from milestone or feature, or assign based on criticality}
```

**Labels**:
- `forge-automation`
- `work-item`
- `progress-gap`
- `gap-type:{missing-work|coverage|decomposition}`
- `priority:p{0-3}` (inherited from milestone/feature)
- `effort:{small|medium}`

### Large Gap (>300 LOC) → Create Feature

**Title Format**: `[Feature] {feature description}`

**Body Template**:
```markdown
# Feature: {Name}

**Created by**: Milestone Progress Reviewer (analyzing PR #{pr-number})
**Milestone**: #{milestone-number} {milestone-title}
**Gap Type**: missing-feature

## Description
This feature addresses a major capability gap identified during milestone progress review.

**Gap Details**:
{Specific description of missing feature}

## Acceptance Criteria
{Extract from milestone description or infer from gap}
- [ ] {criterion 1}
- [ ] {criterion 2}
- [ ] {criterion 3}

## Requirements
{Technical or functional requirements for this feature}

## Scope Estimate
- Estimated LOC: {300-500 | 500+ | unknown}
- Components affected: {list components}
- Complexity: {medium|high}

## Priority
{Assign based on milestone criticality and due date}

## Context
This feature is required because:
{Explanation of why feature is critical for milestone}

**Milestone Goal** (from description):
> {Quote relevant section from milestone description}

**Related PR**: #{pr-number}
**Detection Date**: {current-date}

## Recommended Next Steps
1. Review and refine acceptance criteria
2. Decompose into work items using Feature Decomposer workflow
3. Assign to appropriate team member or Copilot
```

**Labels**:
- `forge-automation`
- `milestone-feature`
- `progress-gap`
- `gap-type:missing-feature`
- `priority:p{0-3}`
- `effort:{medium|large}`
- `needs-decomposition`

## Progress Report (PR Comment)

After analysis, add a comment to the triggering PR:

```markdown
## 🎯 Milestone Progress Report

**Milestone**: #{milestone-number} {milestone-title}
**Due Date**: {due-date} ({days-remaining} days remaining)

### Current PR Contribution
This PR {implements work item #123 | contributes to feature #456 | directly addresses milestone #789}

**Estimated Impact**:
- Files changed: {count}
- LOC changed: {+additions, -deletions}
- Acceptance criteria addressed: {list criteria}

---

### 📊 Milestone Progress

| Metric | Status |
|--------|--------|
| **Overall Completion** | {X}% ({closed}/{total} issues) |
| **Work Items** | {X}% ({closed}/{total}) |
| **Features** | {X}% ({closed}/{total}) |
| **Acceptance Coverage** | {X}% ({covered}/{total} criteria) |

### 🎯 Feature Progress _(if PR is work-item or feature-related)_
**Feature**: #{feature-number} {feature-title}
- Completion: {X}% ({closed}/{total} work items)
- Remaining work items: {list open work items}

---

### ⚠️ Gaps Identified

{If gaps found}:

#### Work Items Needed ({count})
{For each small gap}:
- Created #{work-item-number}: {title}
  - Addresses: {acceptance criterion}
  - Effort: {small|medium}

#### Features Needed ({count})
{For each large gap}:
- Created #{feature-number}: {title}
  - Scope: {major capability missing}
  - Effort: {medium|large}

{If no gaps}:
✅ No gaps identified. Milestone is on track!

---

### 📈 Velocity Analysis

**Recent Activity**:
- Work items closed (last 7 days): {count}
- Current velocity: {count/7} work items per day
- Projected completion: {date based on velocity}

**Status**:
- {If ahead of schedule}: ✅ Ahead of schedule
- {If on track}: ✅ On track for {due-date}
- {If at risk}: ⚠️ At risk — velocity needs to increase to {target} per day
- {If behind}: 🚨 Behind schedule — {days} delay projected

---

### 🎬 Recommended Next Steps

1. {Most critical action based on analysis}
2. {Second priority action}
3. {Third priority action}

---

_Generated by Milestone Progress Reviewer workflow_
_Analysis date: {current-datetime}_
```

## Constraints

### Issue Creation Limits
- **Maximum 5 total issues** per PR analysis (work items + features combined, via safe-outputs max)
- **Recommended split**: Up to 3 work items + up to 2 features, but flexible based on gaps
- **Only create issues for validated gaps** with concrete evidence

### Gap Validation Requirements
Before creating an issue for a gap:
1. ✅ **Evidence exists**: Acceptance criterion or milestone goal explicitly lists the missing work
2. ✅ **Not in progress**: No open issues or PRs address the gap
3. ✅ **Scope is clear**: Can estimate LOC and files affected
4. ✅ **Within milestone**: Gap is truly part of milestone scope, not future work

### Deduplication
Before creating an issue:
- Search existing open issues in milestone for similar titles
- Check if acceptance criterion already has associated work item/feature
- If duplicate found, add comment to existing issue instead of creating new one

### Scope Creep Handling
If PR appears to add work outside milestone scope:
- **Don't create gap issue** (scope is intentionally excluded)
- **Do add comment** explaining the scope creep detection
- **Suggest** creating a separate issue for the out-of-scope work

## Integration Points

- **forge-milestone-planner**: Created original milestone and initial features
- **forge-feature-decomposer**: Decomposes features into work items (may be triggered by gap detection)
- **forge-project-milestone-tracker**: Daily status tracking (complements per-PR analysis)
- **forge-issue-triage-agent**: May triage created gap issues
- **forge-stale-gardener**: Closes stale gap issues after 30 days

## Coordination

### With Milestone Planner
- Avoid creating features that duplicate milestone planner's initial decomposition
- Reference milestone planner's features when creating gap work items

### With Feature Decomposer
- If gap is "feature needs more work items", suggest re-running Feature Decomposer
- Link gap work items to parent features created by Feature Decomposer

### With Milestone Tracker
- Progress metrics should align with daily tracker's calculations
- Velocity data should match tracker's burn-down analysis

## Success Criteria

A successful progress review:
1. ✅ Correctly identifies PR's milestone association (work item → feature → milestone)
2. ✅ Calculates accurate progress metrics (completion %, coverage %)
3. ✅ Identifies real gaps with concrete evidence
4. ✅ Creates appropriate issue types (work items for small, features for large)
5. ✅ Provides actionable progress report on PR
6. ✅ Avoids duplicate gap issues
7. ✅ Helps milestone stay on track for due date
