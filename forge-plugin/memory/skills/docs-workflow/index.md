# docs-workflow Memory

Project-specific memory for documentation conventions, generation history, and health tracking.

## Purpose

This memory helps the `skill:docs-workflow` remember:
- Documentation structure and conventions established for each project
- Which templates and sections were used during initialization
- Documentation health scores over time for trend analysis
- Custom preferences and manual overrides for documentation style

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `doc_conventions.md`

**Purpose**: Track project-specific documentation conventions and preferences

**Should contain**:
- Documentation structure decisions (which files, which sections)
- Project type and framework-specific template choices
- Preferred documentation style (terse vs verbose, section ordering)
- Custom sections added by the user beyond standard templates
- Environment variables and configuration that must be documented

**When to update**: After each `/docs-init` or when the user overrides default conventions

#### `doc_history.md`

**Purpose**: Track documentation generation and update history

**Should contain**:
- Timeline of documentation actions (`/docs-init`, `/docs-update`, `/docs-claude`, `/docs`)
- Health scores over time for trend tracking
- Gaps identified and whether they were resolved
- Files created, modified, or flagged for manual review
- Recommendations made and their outcomes

**When to update**: After each documentation workflow execution

## Memory Lifecycle

### Creation (First Use)
1. Skill runs for the first time on a project (typically via `/docs-init`)
2. Detects project type, framework, and structure
3. Creates project memory directory
4. Saves initial conventions and template choices

### Growth (Ongoing Use)
1. Each `/docs-update` adds to the history with health scores
2. Each `/docs` audit records coverage metrics
3. Convention preferences become more refined with user feedback
4. Health trends accumulate to show documentation trajectory

### Maintenance (Periodic Review)
1. Review health score trends for degradation patterns
2. Archive resolved gap entries from history
3. Update conventions when project structure changes significantly
4. Consolidate repeated patterns into stable conventions

## Related Documentation

- **Skill Documentation**: `../../skills/docs-workflow/SKILL.md`
- **Main Memory Index**: `../index.md`
