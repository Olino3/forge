# project-session-management Memory

Project-specific memory for session history, progress tracking, and handoff patterns.

## Purpose

This memory helps the `skill:project-session-management` remember:
- Past sessions including dates, durations, and progress deltas
- Which handoff formats were most effective for resuming work
- Recurring blockers and how they were resolved across sessions
- Progress velocity trends to improve effort estimation

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `session_history.md`

**Purpose**: Track past sessions with durations, progress deltas, and key outcomes for trend analysis

**Should contain**:
- Session number, date, and approximate duration
- Phase at start and end of session
- Progress delta (percentage or items completed)
- Git checkpoint (branch and commit hash)
- Blockers encountered and whether they were resolved
- Key decisions made during the session

**Example structure**:
```markdown
# Session History

## Session 1 — 2025-06-30
- **Duration**: —
- **Phase**: 1 → 1 (0% → 0%)
- **Progress**: Initial SESSION.md created from IMPLEMENTATION_PHASES.md
- **Git**: main @ `a1b2c3d`
- **Blockers**: None
- **Notes**: Set up session tracking. 6 phases identified from planning docs.

## Session 2 — 2025-07-01
- **Duration**: ~2 hours
- **Phase**: 1 → 2 (100% → 60%)
- **Progress**: Phase 1 completed. Phase 2 models created, migration started.
- **Git**: feature/database-models @ `f4e5d6c`
- **Blockers**: Alembic autogenerate not detecting many-to-many relationship (Open)
- **Notes**: Good velocity on Phase 1. Phase 2 blocker needs env.py investigation.

## Session 3 — 2025-07-02
- **Duration**: ~1.5 hours
- **Phase**: 2 → 2 (60% → 100%)
- **Progress**: Alembic blocker resolved. Seed data and indexes added. Phase 2 complete.
- **Git**: feature/database-models @ `g5h6i7j`
- **Blockers**: None (previous blocker resolved — missing import in env.py)
- **Notes**: Handoff next actions were immediately actionable. Pattern: include specific file paths in blocker mitigations.
```

**When to update**: After every session wrap-up — record duration, progress, and key outcomes

#### `handoff_patterns.md`

**Purpose**: Track which handoff formats and information lead to effective session resumption

**Should contain**:
- Handoff format observations (what information was useful when resuming)
- Next action specificity levels that worked well
- Blocker documentation styles that led to faster resolution
- Anti-patterns — handoff formats that caused confusion or wasted time

**Example structure**:
```markdown
# Handoff Patterns

## Effective Patterns
- **Specific file paths in next actions**: "Fix `alembic/env.py` line 23" is immediately actionable vs "Fix Alembic config"
- **Commands in next actions**: Including the exact command to run (e.g., `alembic revision --autogenerate -m "..."`) eliminates guesswork
- **Blocker mitigations as numbered steps**: Ordered steps for resolving blockers lead to faster resolution than prose descriptions
- **Commit hash references**: Linking completed items to commit hashes lets the resuming session verify progress against git log

## Anti-Patterns
- **Vague next actions**: "Continue working on the API" provides no direction — always specify which endpoints or functions
- **Blockers without mitigations**: "Alembic doesn't work" is useless without investigation steps
- **Missing git checkpoint**: Without branch and commit info, the resuming session may start from wrong state
```

**When to update**: After every session that includes a resume operation — note what information was actually used and what was missing

## Memory Lifecycle

### Creation (First Session)
1. Skill runs for the first time on a project
2. Creates initial SESSION.md (from IMPLEMENTATION_PHASES.md or from scratch)
3. Creates project memory directory
4. Saves initial entry to `session_history.md`
5. Saves baseline patterns to `handoff_patterns.md`

### Growth (Ongoing Sessions)
1. Each session wrap-up appends to `session_history.md`
2. Each session resume evaluates and updates `handoff_patterns.md`
3. Progress velocity trends emerge from session history
4. Effective handoff formats are reinforced, anti-patterns documented

### Maintenance (Periodic Review)
1. Review session history for stale entries — archive sessions older than 6 months
2. Consolidate handoff patterns — remove redundant observations
3. Update velocity baselines based on accumulated data
4. Prune resolved blockers that are no longer relevant

## Related Documentation

- **Skill Documentation**: `../../skills/project-session-management/SKILL.md`
- **Main Memory Index**: `../index.md`
