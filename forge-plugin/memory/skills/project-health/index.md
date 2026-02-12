# project-health Memory

Project-specific memory for health audit scores, improvement tracking, and trend analysis.

## Purpose

This memory helps the `skill:project-health` remember:
- Historical health scores across Documentation, Workflow, and AI-Readiness categories
- Recommendations made and their completion status over time
- Score trends for identifying improvement or degradation patterns
- Project-specific audit context and baselines

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `health_history.md`

**Purpose**: Track historical health scores for trend analysis

**Should contain**:
- Date of each audit with per-category scores (Documentation, Workflow, AI-Readiness)
- Overall weighted score and letter grade
- Summary of key changes since previous audit
- Score deltas showing improvement or regression

**Example structure**:
```markdown
# Health History - payments-api

## Audit: 2025-04-15
- **Documentation**: 92/100 (A) — +14 from previous
- **Workflow**: 90/100 (A) — +10 from previous
- **AI-Readiness**: 88/100 (B) — +16 from previous
- **Overall**: 90/100 (A) — +13 from previous
- **Key changes**: Added API error code docs, completed CLAUDE.md updates

## Audit: 2025-01-15
- **Documentation**: 78/100 (B)
- **Workflow**: 80/100 (B)
- **AI-Readiness**: 72/100 (C)
- **Overall**: 77/100 (B)
- **Key changes**: Initial audit, baseline established
```

**When to update**: After every health audit execution

#### `improvement_tracking.md`

**Purpose**: Track recommendations and their completion status

**Should contain**:
- All recommendations from each audit with priority level
- Current status: pending, in-progress, completed, or dismissed
- Date recommended and date resolved (if applicable)
- Estimated and actual score impact

**Example structure**:
```markdown
# Improvement Tracking - payments-api

## Active Recommendations

### 🟡 Add security scanning to CI pipeline
- **Status**: Pending
- **Date recommended**: 2025-04-15
- **Estimated impact**: Workflow +2
- **Category**: Workflow

### 🟡 Document test fixture conventions in CLAUDE.md
- **Status**: Pending
- **Date recommended**: 2025-04-15
- **Estimated impact**: AI-Readiness +3
- **Category**: AI-Readiness

## Completed Recommendations

### ✅ Add API error code documentation
- **Status**: Completed
- **Date recommended**: 2025-01-15
- **Date completed**: 2025-03-20
- **Estimated impact**: Documentation +5
- **Actual impact**: Documentation +7 (also improved Swagger completeness)

### ✅ Create CLAUDE.md with build/test commands
- **Status**: Completed
- **Date recommended**: 2025-01-15
- **Date completed**: 2025-02-10
- **Estimated impact**: AI-Readiness +20
- **Actual impact**: AI-Readiness +16
```

**When to update**: After every health audit — add new recommendations, update status of existing ones

## Memory Lifecycle

### Creation (First Audit)
1. Skill runs for the first time on a project
2. Completes full audit across all three categories
3. Creates project memory directory
4. Saves initial scores to `health_history.md`
5. Saves initial recommendations to `improvement_tracking.md`

### Growth (Ongoing Audits)
1. Each audit appends to `health_history.md` with new scores
2. Previous recommendations are checked for completion
3. New recommendations added to `improvement_tracking.md`
4. Trend data accumulates for meaningful analysis

### Maintenance (Periodic Review)
1. Review improvement tracking for stale recommendations
2. Archive completed recommendations older than 6 months
3. Update baselines when project undergoes major restructuring
4. Consolidate historical data if audit count exceeds 20 entries

## Related Documentation

- **Skill Documentation**: `../../skills/project-health/SKILL.md`
- **Main Memory Index**: `../index.md`
