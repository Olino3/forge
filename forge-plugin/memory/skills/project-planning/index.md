# project-planning Memory

Project-specific memory for planning patterns, phase structures, and project history.

## Purpose

This memory helps the `skill:project-planning` remember:
- Common phase structures that work well for specific project types (greenfield, migration, API-heavy, database-heavy)
- Past projects planned, their tech stacks, and outcomes
- Lessons learned about phase sizing, dependency ordering, and verification criteria
- Which conditional documents were generated and their effectiveness

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `planning_patterns.md`

**Purpose**: Track common phase structures by project type for reuse in future planning sessions

**Should contain**:
- Project type classification and the phase structure used
- Number of phases and their names
- Which conditional documents were generated
- Notes on what worked well or needed adjustment

**Example structure**:
```markdown
# Planning Patterns

## Pattern: Greenfield E-Commerce (Next.js)
- **Phases**: 8 (Scaffolding → Schema → Auth → Catalog → Cart → Checkout → Orders → Deploy)
- **Conditional docs**: TECH_STACK_DECISIONS.md
- **Notes**: Auth and Catalog can run in parallel after Schema phase. Checkout phase took longer than estimated — consider sizing as XL for payment integrations.

## Pattern: API Migration (Express → FastAPI)
- **Phases**: 7 (Setup → Infrastructure → Read Endpoints → Write Endpoints → Testing → Cutover → Decommission)
- **Conditional docs**: MIGRATION_PLAN.md
- **Notes**: Strangler fig pattern worked well. Splitting endpoints into read vs write batches reduced risk. Allow extra time for parity testing.
```

**When to update**: After every planning session — record the phase structure and any observations

#### `project_history.md`

**Purpose**: Log past projects planned and their outcomes for trend analysis

**Should contain**:
- Project name and date of planning session
- Tech stack summary
- Project type classification
- Number of phases defined
- Conditional documents generated
- Outcome notes (if available from follow-up sessions)

**Example structure**:
```markdown
# Project History

## next-ecommerce — 2025-06-30
- **Type**: Greenfield
- **Stack**: Next.js 14, TypeScript, PostgreSQL, Prisma, Stripe
- **Phases**: 8
- **Conditional docs**: TECH_STACK_DECISIONS.md
- **Outcome**: Phases 1-3 completed on schedule. Phase 6 (Stripe) required an additional sub-phase for webhook handling.

## api-migration — 2025-07-10
- **Type**: Migration (Express → FastAPI)
- **Stack**: FastAPI, Python 3.12, MongoDB/Motor
- **Phases**: 7
- **Conditional docs**: MIGRATION_PLAN.md
- **Outcome**: Cutover completed with zero downtime. Parity testing caught 3 edge cases in date serialization.
```

**When to update**: After every planning session — add new entry. Update outcome notes when follow-up information is available.

## Memory Lifecycle

### Creation (First Planning Session)
1. Skill runs for the first time on a project
2. Completes full planning workflow
3. Creates project memory directory
4. Saves phase structure to `planning_patterns.md`
5. Saves project entry to `project_history.md`

### Growth (Ongoing Sessions)
1. Each planning session appends to `project_history.md`
2. New project type patterns added to `planning_patterns.md`
3. Outcome notes updated when follow-up data is available
4. Pattern refinements recorded based on real-world results

### Maintenance (Periodic Review)
1. Review patterns for accuracy — remove outdated structures
2. Archive project history entries older than 12 months
3. Consolidate similar patterns into generalized templates
4. Update effort estimates based on actual outcomes

## Related Documentation

- **Skill Documentation**: `../../skills/project-planning/SKILL.md`
- **Main Memory Index**: `../index.md`
