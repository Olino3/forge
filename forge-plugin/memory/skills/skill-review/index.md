# skill-review Memory

Skill-specific memory for tracking skill audit history, scores, findings, and recurring issues across the skill library.

## Purpose

This memory helps the `skill:skill-review` remember:
- Past skill reviews with per-phase scores and overall grades
- Common issues found across multiple skills (structural patterns, version drift areas)
- Trends in skill quality over time
- Recurring non-compliance patterns to watch for in future reviews

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `review_history.md`

**Purpose**: Track all past skill reviews with scores and key findings

**Should contain**:
- Skill name and date of each review
- Per-phase results (Pass/Warn/Fail for each of the 9 phases)
- Overall grade (A/B/C/D/F)
- Key findings summary
- Comparison with previous review of the same skill (if applicable)

**Example structure**:
```markdown
# Review History

## python-code-review — 2025-07-15
- **Grade**: D (down from A on 2025-01-15)
- **Pass**: 7 | **Warn**: 1 | **Fail**: 2
- **Key findings**: Significant version drift — pylint/flake8/black ecosystem replaced by ruff; Python 3.9 type hints outdated
- **Phases failed**: Official Docs Verification, Version Drift Detection

## commit-helper — 2025-07-15
- **Grade**: B
- **Pass**: 7 | **Warn**: 2 | **Fail**: 0
- **Key findings**: Minor step-numbering mismatch in examples.md; some token efficiency improvements possible
- **Phases warned**: Cross-File Consistency, Token Efficiency
```

**When to update**: After every skill review — append the review entry with scores and findings

#### `common_issues.md`

**Purpose**: Track recurring problems found across multiple skills to identify systemic patterns

**Should contain**:
- Issue pattern name and description
- Skills affected by this issue
- Frequency (how many skills exhibit this pattern)
- Recommended systemic fix (if applicable)

**Example structure**:
```markdown
# Common Issues Across Skills

## Python Tooling Drift
- **Description**: Skills reference pylint, flake8, black, isort instead of modern ruff-based toolchain
- **Skills affected**: python-code-review, python-dependency-management
- **Frequency**: 2 skills
- **Systemic fix**: Update Python context domain to recommend ruff as default; update all Python skills

## Memory Index Skill Name Mismatch
- **Description**: Memory index references a different skill name than the SKILL.md frontmatter
- **Skills affected**: generate-mock-service
- **Frequency**: 1 skill
- **Systemic fix**: Add a cross-file name validation step to the skill-creator workflow

## Incomplete Workflow Coverage in Examples
- **Description**: examples.md demonstrates only core steps, omitting Generate Output and Update Memory steps
- **Skills affected**: generate-mock-service
- **Frequency**: 1 skill
- **Systemic fix**: Update SKILL_TEMPLATE.md to emphasize that examples must demonstrate all workflow steps
```

**When to update**: After every skill review — add new patterns and update frequency counts for existing patterns

## Memory Lifecycle

### Creation (First Review Session)
1. Skill-review runs for the first time
2. Completes full 9-phase audit of the target skill
3. Creates memory directory
4. Saves review entry to `review_history.md`
5. Saves any discovered patterns to `common_issues.md`

### Growth (Ongoing Reviews)
1. Each review session appends to `review_history.md`
2. New recurring patterns added to `common_issues.md`
3. Frequency counts updated when known patterns appear in new skills
4. Trend data accumulates for identifying systemic quality issues

### Maintenance (Periodic Review)
1. Review common issues for accuracy — remove resolved patterns
2. Archive review history entries older than 12 months
3. Consolidate similar issue patterns into generalized categories
4. Update systemic fix recommendations based on resolution outcomes

## Related Documentation

- **Skill Documentation**: `../../skills/skill-review/SKILL.md`
- **Main Memory Index**: `../index.md`
