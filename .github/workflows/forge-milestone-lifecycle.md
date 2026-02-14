---
description: "Consolidated workflow for milestone planning, tracking, and progress review"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
engine:
  id: copilot
  model: gemini-3
on:
  milestone:
    types: [created]
  schedule: "daily"
  pull_request:
    types: [opened, synchronize]
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
    labels: ["forge-automation", "milestones", "planning"]
    max: 5
    expires: 30
---

# Forge Milestone Lifecycle

**Consolidated Workflow** — Replaces:
- `forge-milestone-planner.md` (planning and feature decomposition)
- `forge-project-milestone-tracker.md` (daily progress tracking)
- `forge-milestone-progress-reviewer.md` (PR contribution analysis)

This workflow manages the complete milestone lifecycle through three event-driven stages: Plan (on milestone creation), Track (daily progress), and Review (PR impact analysis). Each stage executes independently based on the triggering event.

---

## Event Routing

**Execute the appropriate stage based on the triggering event:**

| Trigger | Stage | Behavior |
|---------|-------|----------|
| `milestone.created` | **Planning Stage** | Decompose milestone into feature issues, associate existing issues |
| `schedule` (daily) | **Tracking Stage** | Progress report, blocked items, velocity, reprioritization |
| `pull_request` | **Review Stage** | PR contribution analysis, gap detection, remediation issues |
| `workflow_dispatch` | **Tracking Stage** | Manual check (default to tracking) |

**Determine which stage to execute FIRST before any detailed analysis.**

---

## Stage 1: Planning (on milestone.created)

**Objective**: Decompose newly created milestones into executable feature issues and associate relevant existing issues.

### Loop Prevention

If the triggering milestone meets any of these conditions, do nothing:
- Title contains `[automation]`
- Description contains `forge-automation`
- Created by a bot account

### Planning Steps

#### 1. Analyze Milestone Structure

Parse the milestone to extract:

**Basic Metadata**:
- Title
- Description (full text)
- Due date (if set)
- Labels or keywords in title

**Acceptance Criteria**:
- Look for checklist items: `- [ ]` or `- [x]` patterns
- Look for numbered lists of deliverables
- Look for "Acceptance Criteria" or "Done When" sections

**Requirements**:
- Technical specs
- Functional requirements
- "Must have" vs. "Nice to have" items

**Scope**:
- "In scope" items
- "Out of scope" items
- Dependencies on other milestones

**Priority and Effort**:
- Infer priority from title keywords: "critical", "urgent", "P0", "P1", etc.
- Estimate overall effort from description complexity

**Ambiguities**:
- Missing information
- Unclear acceptance criteria
- Undefined dependencies

#### 2. Decompose into Feature Issues

Create **3-5 focused feature issues** that:
- Break down milestone goals into distinct, deliverable features
- Map subset of acceptance criteria to each feature
- Map relevant requirements to each feature
- Assign priority (P0/P1/P2/P3) based on:
  - Milestone priority + feature criticality
  - Dependency order (blockers should be P0)
- Estimate effort level (small/medium/large) based on complexity
- Identify questions or clarifications needed

**Feature Issue Structure**:

**Title**: `[Feature] {brief feature description}`

**Body**:
```markdown
# Feature: {Name}

**Milestone**: #{milestone-number} {milestone-title}

## Description
{Clear description of what this feature accomplishes}

## Acceptance Criteria
{Subset of milestone acceptance criteria specific to this feature}
- [ ] {criterion 1}
- [ ] {criterion 2}
- [ ] {criterion 3}

## Requirements
{Technical/functional requirements from milestone}
- {requirement 1}
- {requirement 2}

## Priority
**{P0/P1/P2/P3}** — {Justification for priority}

## Effort
**{Small/Medium/Large}** — {Justification for effort estimate}

## Dependencies
- Depends on: #{issue-or-feature} (if applicable)
- Blocks: #{issue-or-feature} (if applicable)

## Questions
- [ ] {Clarification needed} (@maintainer please advise)

## Implementation Notes
{Any design considerations, approach suggestions, or constraints}
```

**Labels**: `milestone-feature`, `forge-automation`, priority labels (`P0`, `P1`, etc.)

#### 3. Associate Existing Issues

Search for open issues that match the milestone:

**Search Strategy**:
- Extract keywords from milestone title and description
- Search open issues using GitHub API (keywords + repository context)
- Filter results:
  - ✓ Must be open
  - ✓ Must NOT already have a milestone assigned
  - ✓ Must NOT be automation-generated (no `forge-automation` label)
  - ✓ Semantic relevance score >70% (use description similarity)

**Association Process**:
- Assign milestone to the issue
- Add comment explaining association:

```markdown
🤖 **Automated Milestone Association**

This issue has been associated with milestone #{milestone-number} {milestone-title}.

**Reason**: {explanation of semantic match — which keywords/requirements matched}

**Next Steps**:
- Review the milestone's acceptance criteria
- Determine if this issue should be broken into sub-issues
- Assign appropriate priority label (P0/P1/P2/P3)

If this association is incorrect, remove the milestone and add the `milestone-mismatch` label.
```

**Constraints**:
- Maximum 10 issues associated per milestone
- Prioritize issues with higher relevance scores
- Skip issues with "wontfix", "duplicate", or "invalid" labels

#### 4. Output Summary Issue

Create a planning summary issue:

**Title**: `[milestone] Planning Complete: {milestone-title}`

**Body**:
```markdown
# Milestone Planning Summary

**Milestone**: #{milestone-number} {milestone-title}

## Features Created
- [ ] #XXX — {Feature 1} (P0, Large)
- [ ] #YYY — {Feature 2} (P1, Medium)
- [ ] #ZZZ — {Feature 3} (P2, Small)

## Existing Issues Associated
- #AAA — {Issue title} (relevance: 85%)
- #BBB — {Issue title} (relevance: 72%)

## Milestone Metadata
- **Due Date**: {date or "Not set"}
- **Total Features**: {count}
- **Total Associated Issues**: {count}
- **Estimated Effort**: {sum of effort levels}
- **Priority Distribution**: {P0: n, P1: m, P2: k, P3: j}

## Ambiguities / Questions
- {question 1}
- {question 2}

## Next Steps
1. Review and refine feature issues
2. Assign features to team members
3. Begin work on P0 features
4. Monitor progress with daily tracking reports

---
*Generated by Forge Milestone Lifecycle (Planning Stage)*
```

**Labels**: `forge-automation`, `milestone-plan`

---

## Stage 2: Tracking (on schedule: daily)

**Objective**: Monitor all active milestones and produce a daily execution report.

### Analysis Scope

For each **open milestone** in the repository:

#### 1. Milestone Progress

Calculate:
- **Open vs. Closed**:
  - Open issues count
  - Closed issues count
  - Open PRs count
  - Merged PRs count
- **Completion Percentage**:
  - `(closed issues + merged PRs) / (total issues + total PRs) * 100`
- **Velocity**:
  - Items closed in last 7 days
  - Items closed in last 24 hours
  - Projected completion date based on current velocity
- **Due Date Status**:
  - Days until due date (if set)
  - On track / At risk / Overdue

#### 2. Blocked Items

Identify issues or PRs that are blocked:

**Blocked Criteria**:
- No activity (comments or commits) for 7+ days
- Has label `blocked` or `waiting-for-review`
- Has label `needs-info` or `needs-decision`
- PR with requested changes but no updates for 3+ days
- Issue with unanswered questions (question marks in last comment)

**Dependency Blockers**:
- Issue has "Depends on: #XXX" but #XXX is still open

**Review Bottlenecks**:
- PR with review requests but no reviews submitted for 2+ days

#### 3. Risk Signals

Flag milestones at risk:

**Critical Unresolved Items**:
- Any P0 issue still open within 7 days of due date
- Any P0 PR with requested changes

**Missing Implementation**:
- Milestone has acceptance criteria but no feature issues created
- Feature issue has no linked PRs or work items

**Velocity Risk**:
- Current velocity < 50% of required velocity to meet due date

### Output: Daily Status Issue

Create one issue per run (closes previous day's issue):

**Title**: `[milestone] Daily Milestone Status — {YYYY-MM-DD}`

**Body**:
```markdown
# Daily Milestone Status

**Report Date**: {date}

## Summary
- **Milestones Tracked**: {count}
- **On Track**: {count} ✅
- **At Risk**: {count} ⚠️
- **Overdue**: {count} 🚨
- **Blocked Items**: {count}

## Milestone Progress

| Milestone | Due Date | Completion | Open | Closed | Velocity | Status |
|-----------|----------|------------|------|--------|----------|--------|
| #{num} {title} | {date} | 75% | 5 | 15 | 2.1/day | ✅ On track |
| #{num} {title} | {date} | 45% | 11 | 9 | 0.8/day | ⚠️ At risk |
| #{num} {title} | {date} | 30% | 14 | 6 | 0.5/day | 🚨 Overdue |

## Blocked Work

### High Priority (P0/P1)
- #{issue}: {title} — **Blocker**: {reason} — **Age**: {days} days
- #{pr}: {title} — **Blocker**: Waiting for review from @{user} — **Age**: {days} days

### Medium/Low Priority (P2/P3)
- #{issue}: {title} — **Blocker**: {reason} — **Age**: {days} days

## Risk Analysis

### Milestone #{num}: {title}
**Status**: ⚠️ At Risk
**Reason**: Current velocity (0.8 items/day) is below required velocity (1.5 items/day) to meet due date in {n} days.
**Recommendation**: Prioritize P0 items, defer P2/P3 items, or extend due date by {n} days.

### Milestone #{num}: {title}
**Status**: 🚨 Critical
**Reason**: P0 issue #{num} still open with {n} days until due date.
**Recommendation**: Focus all effort on unblocking #{num}.

## Reprioritization Suggestions

1. **Milestone #{num}**: Move #{issue} from P1 to P0 (blocks multiple P0 items)
2. **Milestone #{num}**: Move #{issue} from P0 to P1 (no longer blocking, other P0 items more critical)
3. **Milestone #{num}**: Consider splitting #{large-feature} into smaller work items for faster progress

## Recommended Actions (next 24h)

- [ ] **#{issue}**: Ping @{assignee} for status update (blocked {n} days)
- [ ] **#{pr}**: Ping @{reviewer} for review (waiting {n} days)
- [ ] **Milestone #{num}**: Review and adjust due date (+{n} days based on velocity)
- [ ] **#{issue}**: Add `needs-decision` label and request maintainer input

---
*Generated by Forge Milestone Lifecycle (Tracking Stage)*
```

**Labels**: `forge-automation`, `milestone-tracking`

**Safe-Output Config**:
- `close-older-issues: true` (close previous day's status issue)
- `expires: 14` (keep for 2 weeks then auto-close)

---

## Stage 3: Review (on pull_request)

**Objective**: Evaluate PR contributions to milestones and identify delivery gaps.

### IMMEDIATE MILESTONE CHECK

**CRITICAL: Execute this check BEFORE any detailed analysis to avoid wasted runs.**

1. Check if PR title or body contains issue references (`#NNN` pattern or `Fixes #NNN`)
2. Check if PR has a milestone field assigned
3. If NEITHER condition is met:
   - Output "No milestone association detected. PR is not milestone-related. Exiting."
   - Stop immediately without further analysis
4. If EITHER condition is met, proceed to Loop Prevention checks

Do NOT perform detailed Association Detection Hierarchy analysis, issue fetching, or milestone metadata collection before completing this quick check.

### Loop Prevention

If the triggering PR meets any of these conditions, do nothing:
- Has label `forge-automation`
- Title starts with `[Work item]`, `[Feature]`, `[milestone]`, `[improve]`, `[docs]`, or `[forge-`
- Is from a bot account

### Association Detection Hierarchy

Determine the PR's relationship to milestones by checking in this order:

#### 1. Work Item Association
Check if PR references an issue with `work-item` label:
- Parse PR title for `#123` or `Fixes #123` patterns
- Parse PR body for issue references
- Parse PR branch name for issue numbers (e.g., `fix-123-bug`)
- If work item found:
  - Extract parent feature from work item's body (references `Parent Feature: #456`)
  - Extract milestone from parent feature or work item's milestone field
  - **Association**: work item #123 → feature #456 → milestone #789

#### 2. Milestone Feature Association
If no work item found, check if PR references an issue with `milestone-feature` label:
- Parse PR title/body/branch for issue references
- If milestone-feature found:
  - Extract milestone from feature's milestone field or body
  - **Association**: feature #456 → milestone #789

#### 3. Direct Milestone Association
If no feature found, check if PR has direct milestone:
- Check PR's milestone field
- Parse PR body for milestone references (e.g., "Part of milestone #789")
- **Association**: PR → milestone #789

#### 4. No Association
If none of the above found:
- **Skip processing** — PR is not milestone-related
- Do not create any issues
- Exit workflow

### Milestone Progress Analysis

Once milestone association is established:

#### 1. Collect Milestone Metadata

Use GitHub API to fetch:
- Milestone title, description, due date, state
- All issues associated with milestone
- All PRs associated with milestone
- Open vs. closed counts

Parse milestone description for:
- **Acceptance criteria**: Checklist items (`- [ ]` or `- [x]`)
- **Requirements**: Numbered or bulleted capability lists
- **Scope boundaries**: "In scope" and "Out of scope" sections

#### 2. Categorize Milestone Issues

Group milestone issues by type:

- **Feature issues**: Has `milestone-feature` label
- **Work items**: Has `work-item` label
- **Bugs**: Has `bug` label
- **Enhancements**: Has `enhancement` label
- **Research/Exploration**: Has `research` or `spike` label

Count by status:
- Open features
- Closed features
- Open work items per feature
- Closed work items per feature

#### 3. Analyze PR Contribution

Determine what the PR addresses:

**File Analysis**:
- Changed files count
- Primary domains touched (skills, agents, commands, context, tests, docs)
- Scope (narrow: 1-3 files, medium: 4-10 files, broad: 11+ files)

**Acceptance Criteria Coverage**:
- Does PR description reference any milestone acceptance criteria?
- Which criteria are addressed by the changed files?
- Which criteria remain unaddressed?

**Requirement Coverage**:
- Does PR implement any milestone requirements?
- Are implementations partial or complete?

**Feature Contribution**:
- If PR references a feature issue, which feature acceptance criteria does it address?
- Are there feature acceptance criteria still open?

#### 4. Gap Detection

Identify delivery gaps:

**Acceptance Criteria Gaps**:
- Milestone acceptance criteria with no matching feature issues
- Milestone acceptance criteria with no matching PRs or work items

**Requirement Gaps**:
- Milestone requirements with no implementation work

**Feature Gaps**:
- Features with no work items or PRs
- Features with incomplete acceptance criteria coverage

**Testing Gaps**:
- PRs without corresponding test file changes
- Features without test coverage

**Documentation Gaps**:
- Features without documentation updates (README, CONTRIBUTING, etc.)

### Output: Remediation Issues

For each identified gap, create a remediation issue (maximum 5 per PR):

**Gap Type: Missing Feature Work**

**Title**: `[Work item] {milestone-title}: {specific work needed}`

**Body**:
```markdown
# Work Item

**Milestone**: #{milestone-number} {milestone-title}  
**Parent Feature**: #{feature-number} {feature-title}

## Description
{What needs to be done to address the gap}

## Context
This work item was generated from PR #{pr-number} analysis. The PR addresses {what-it-addresses}, but the following milestone acceptance criteria remain unaddressed:
- [ ] {criterion 1}
- [ ] {criterion 2}

## Acceptance Criteria
{Specific criteria for this work item}
- [ ] {criterion 1}
- [ ] {criterion 2}

## Definition of Done
- [ ] Acceptance criteria met
- [ ] Tests added
- [ ] Documentation updated
- [ ] PR reviewed and merged

---
*Generated by Forge Milestone Lifecycle (Review Stage)*
```

**Labels**: `work-item`, `forge-automation`, milestone label

---

**Gap Type: Missing Tests**

**Title**: `[Work item] {milestone-title}: Add tests for {feature/component}`

**Body**:
```markdown
# Work Item: Test Coverage

**Milestone**: #{milestone-number} {milestone-title}  
**Related PR**: #{pr-number}

## Description
PR #{pr-number} implements {feature/change} but does not include corresponding tests.

## Files Requiring Tests
- `{file1}` — needs unit tests
- `{file2}` — needs integration tests

## Acceptance Criteria
- [ ] Unit tests cover all new functions/methods
- [ ] Integration tests verify feature behavior
- [ ] Test coverage >80% for changed files
- [ ] All tests pass in CI

---
*Generated by Forge Milestone Lifecycle (Review Stage)*
```

---

**Gap Type: Missing Documentation**

**Title**: `[Work item] {milestone-title}: Document {feature/capability}`

**Body**:
```markdown
# Work Item: Documentation

**Milestone**: #{milestone-number} {milestone-title}  
**Related PR**: #{pr-number}

## Description
PR #{pr-number} adds {feature/capability} but does not update relevant documentation.

## Documentation Needed
- [ ] Update README.md with new capability
- [ ] Add examples to COOKBOOK.md
- [ ] Update CONTRIBUTING.md if contributor-facing
- [ ] Update ROADMAP.md to mark feature complete

## Acceptance Criteria
- [ ] All listed documentation updated
- [ ] Examples are accurate and tested
- [ ] Cross-references are correct

---
*Generated by Forge Milestone Lifecycle (Review Stage)*
```

---

## Success Criteria

✅ **Planning Stage** correctly decomposes milestones into 3-5 focused features  
✅ **Planning Stage** associates relevant existing issues with semantic matching  
✅ **Tracking Stage** produces daily reports with accurate progress metrics  
✅ **Tracking Stage** identifies blocked items and risk signals  
✅ **Review Stage** only processes PRs with milestone associations  
✅ **Review Stage** accurately detects acceptance criteria, testing, and documentation gaps  
✅ All stages respect loop prevention rules  
✅ Remediation issues are actionable and well-structured  
