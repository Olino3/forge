# Project Session Management Examples

This file contains example scenarios demonstrating how to use the project-session-management skill to track progress across sessions, create git checkpoints, and prepare effective session handoffs.

---

## Example 1: Creating Initial SESSION.md from IMPLEMENTATION_PHASES.md

### Scenario
A developer has just completed project planning for a new FastAPI application and has an IMPLEMENTATION_PHASES.md with 6 phases. They want to start tracking progress with SESSION.md before beginning Phase 1.

### User Prompt
```
Create SESSION.md for my fastapi-inventory project. I have IMPLEMENTATION_PHASES.md already.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Operation Type: Create (no SESSION.md found)
IMPLEMENTATION_PHASES.md: Found at /claudedocs/IMPLEMENTATION_PHASES.md
Git State:
  Branch: main
  Last Commit: a1b2c3d — "Add IMPLEMENTATION_PHASES.md for fastapi-inventory"
  Uncommitted Changes: None
Phases Found: 6
  Phase 1: Project Scaffolding & Dev Environment (Small)
  Phase 2: Database Models & Migrations (Medium)
  Phase 3: Core CRUD API Endpoints (Large)
  Phase 4: Authentication & Authorization (Medium)
  Phase 5: Search & Filtering (Medium)
  Phase 6: Testing, Docs & Deployment (Large)
```

**Step 2 - Load Memory**:
- No previous memory found; first session for this project

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded Python domain context for FastAPI patterns

**Step 4 - Assess Session State**:
- IMPLEMENTATION_PHASES.md parsed successfully
- All 6 phases set to "not started"
- Initial next actions derived from Phase 1 deliverables
- No blockers identified

**Step 5 - Create Session Document**:

```markdown
# SESSION — fastapi-inventory

## Current Phase
**Phase 1: Project Scaffolding & Dev Environment**
Progress: 0% complete

## Completed Items
_(No items completed yet)_

## In Progress
- [ ] Initialize FastAPI project with Poetry — not started
- [ ] Configure Docker Compose with PostgreSQL — not started
- [ ] Set up pre-commit hooks (ruff, mypy) — not started
- [ ] Create CI pipeline stub with GitHub Actions — not started

## Blockers
| Blocker | Impact | Mitigation | Status |
|---------|--------|------------|--------|
| _(None identified)_ | — | — | — |

## Next Actions
1. Run `poetry init` and add fastapi, uvicorn, sqlalchemy, alembic dependencies
2. Create `docker-compose.yml` with PostgreSQL 16 and Redis services
3. Create `Dockerfile` for the FastAPI application with multi-stage build
4. Set up `.pre-commit-config.yaml` with ruff and mypy hooks
5. Verify `docker compose up` starts all services and API responds on localhost:8000

## Git Checkpoint
- **Branch**: main
- **Last Commit**: `a1b2c3d` — Add IMPLEMENTATION_PHASES.md for fastapi-inventory
- **Uncommitted Changes**: None
- **Timestamp**: 2025-06-30T14:00:00Z

## Session History
| Session | Date | Duration | Progress |
|---------|------|----------|----------|
| 1 | 2025-06-30 | — | Initial SESSION.md created from IMPLEMENTATION_PHASES.md |
```

**Step 6 - Git Checkpoint**:
- Branch: main
- HEAD: `a1b2c3d` — Add IMPLEMENTATION_PHASES.md for fastapi-inventory
- Uncommitted changes: None (SESSION.md will be a new file)
- Timestamp recorded

**Step 7 - Output**:
- `SESSION.md` saved to project root
- `/claudedocs/SESSION_SNAPSHOT_2025-06-30.md` saved as historical record

**Step 8 - Memory Update**:
- Created `session_history.md` with initial session entry
- Created `handoff_patterns.md` with initial creation pattern noted

---

## Example 2: Wrapping Up a Session (Recording Progress and Next Actions)

### Scenario
A developer has been working on Phase 2 of the fastapi-inventory project for 2 hours. They completed the database models and ran the first migration, but hit a blocker with Alembic autogenerate not detecting a relationship. They need to wrap up and hand off to the next session.

### User Prompt
```
Update SESSION.md — I'm wrapping up for today. I finished the SQLAlchemy models and ran the initial migration, but Alembic autogenerate isn't picking up the inventory-supplier relationship.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Operation Type: Update (SESSION.md exists)
Git State:
  Branch: feature/database-models
  Last Commit: f4e5d6c — "Add SQLAlchemy models for inventory, supplier, category"
  Uncommitted Changes:
    M alembic/versions/001_initial.py
    M src/models/inventory.py
```

**Step 2 - Load Memory**:
- Previous session found: Session 1 created initial SESSION.md
- No handoff patterns yet (first update)

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded Python domain context

**Step 4 - Assess Session State**:
- Current phase: Phase 2 (Database Models & Migrations)
- Completed since last session:
  - SQLAlchemy models for inventory, supplier, category (commit `f4e5d6c`)
  - Initial Alembic migration generated
- In progress: Alembic autogenerate configuration
- Blocker identified: Alembic not detecting many-to-many relationship

**Step 5 - Update Session Document**:

```markdown
# SESSION — fastapi-inventory

## Current Phase
**Phase 2: Database Models & Migrations**
Progress: 60% complete

## Completed Items
- [x] Initialize FastAPI project with Poetry — `b3c4d5e` (2025-06-30)
- [x] Configure Docker Compose with PostgreSQL — `b3c4d5e` (2025-06-30)
- [x] Set up pre-commit hooks (ruff, mypy) — `c4d5e6f` (2025-06-30)
- [x] Create CI pipeline stub — `d5e6f7g` (2025-06-30)
- [x] SQLAlchemy models: Inventory, Supplier, Category — `f4e5d6c` (2025-07-01)
- [x] Initial Alembic migration generated — `f4e5d6c` (2025-07-01)

## In Progress
- [ ] Fix Alembic autogenerate for inventory-supplier relationship — blocked (see Blockers)
- [ ] Seed data scripts for development — not started
- [ ] Index strategy for query patterns — not started

## Blockers
| Blocker | Impact | Mitigation | Status |
|---------|--------|------------|--------|
| Alembic autogenerate not detecting many-to-many relationship between Inventory and Supplier | Cannot generate complete migration; manual migration editing required | 1. Check `target_metadata` in `env.py` includes all models. 2. Verify `inventory_supplier` association table is imported. 3. Try `--autogenerate` with `--compare-type` flag. | Open |

## Next Actions
1. Fix Alembic: verify `env.py` imports `src.models.inventory` and the association table is registered in `Base.metadata`
2. Run `alembic revision --autogenerate -m "add inventory_supplier relationship"` and verify the migration includes the association table
3. Create `scripts/seed_data.py` with 100 sample inventory items, 20 suppliers, and 10 categories
4. Add database indexes on `inventory.sku` (unique) and `inventory.category_id` (foreign key lookup)
5. Run full migration suite: `alembic upgrade head` on a clean database and verify all tables created

## Git Checkpoint
- **Branch**: feature/database-models
- **Last Commit**: `f4e5d6c` — Add SQLAlchemy models for inventory, supplier, category
- **Uncommitted Changes**: M alembic/versions/001_initial.py, M src/models/inventory.py
- **Timestamp**: 2025-07-01T18:30:00Z

## Session History
| Session | Date | Duration | Progress |
|---------|------|----------|----------|
| 1 | 2025-06-30 | — | Initial SESSION.md created; Phase 1 completed |
| 2 | 2025-07-01 | ~2 hours | Phase 2 at 60% — models created, migration started, Alembic blocker identified |
```

**Step 6 - Git Checkpoint**:
- Branch: feature/database-models
- HEAD: `f4e5d6c`
- Uncommitted changes: 2 modified files noted
- Timestamp recorded

**Step 7 - Output**:
- `SESSION.md` updated at project root
- `/claudedocs/SESSION_SNAPSHOT_2025-07-01.md` saved

**Step 8 - Memory Update**:
- Updated `session_history.md` with Session 2 entry (duration, progress delta, blocker)
- Updated `handoff_patterns.md`: noted that including specific file paths and commands in Next Actions makes handoffs more effective

---

## Example 3: Resuming a Session (Reading SESSION.md and Continuing)

### Scenario
A new AI session is starting on the fastapi-inventory project. The previous session left a SESSION.md with a blocker and 5 next actions. The AI needs to read the session state, verify the git checkpoint, and continue from where the last session left off.

### User Prompt
```
Resume work on fastapi-inventory. Check SESSION.md and continue from where we left off.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Operation Type: Resume (SESSION.md exists)
SESSION.md parsed:
  Current Phase: Phase 2 (Database Models & Migrations) — 60% complete
  Open Blocker: Alembic autogenerate not detecting many-to-many relationship
  Next Actions: 5 items (Alembic fix, migration, seed data, indexes, verification)
Git State Verification:
  Expected Branch: feature/database-models ✓
  Expected Last Commit: f4e5d6c ✓
  Uncommitted Changes: M alembic/versions/001_initial.py, M src/models/inventory.py ✓
  Checkpoint Verified: Git state matches SESSION.md — safe to continue
```

**Step 2 - Load Memory**:
- Session history loaded: 2 previous sessions found
- Handoff pattern: specific file paths and commands in Next Actions are effective
- Cross-skill: project-planning memory confirms Phase 2 deliverables

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded Python domain context for SQLAlchemy and Alembic patterns

**Step 4 - Assess Session State**:
- Priority 1: Resolve Alembic blocker (Next Action #1 and #2)
- Priority 2: Complete remaining Phase 2 deliverables (Next Actions #3-5)
- Blocker mitigation steps are clearly documented — start with checking `env.py`
- Estimated remaining work: 3 items to complete Phase 2

**Step 5 - Session Document**:
- SESSION.md read and validated — no updates needed until work begins
- Session 3 will be logged when progress is made

**Step 6 - Git Checkpoint**:
- Checkpoint verified against actual git state — all values match
- Safe to continue from documented state

**Step 7 - Output**:
- No output generated yet — session is resuming, not wrapping up
- SESSION.md will be updated when progress is made during this session

**Step 8 - Memory Update**:
- No update yet — memory will be updated when session wraps up

### Resume Action Plan
Based on SESSION.md analysis, the session proceeds with:

1. **Immediate**: Open `alembic/env.py` and verify `target_metadata` imports all model modules
2. **Immediate**: Check that the `inventory_supplier` association table is defined and imported before Alembic runs
3. **After blocker resolved**: Generate the corrected migration and verify with `alembic upgrade head`
4. **Then**: Create seed data script and add indexes
5. **Finally**: Update SESSION.md with progress and prepare next handoff

---

## Summary of Session Management Scenarios

1. **Initial creation** — Parse IMPLEMENTATION_PHASES.md, set up SESSION.md with Phase 1 deliverables as next actions, record git baseline
2. **Session wrap-up** — Record completed items with commit hashes, document blockers with mitigations, define concrete next actions for handoff
3. **Session resume** — Verify git checkpoint matches actual state, prioritize blocker resolution, continue from documented next actions

## Best Practices

- Always verify the git checkpoint when resuming — if the state doesn't match, investigate before proceeding
- Next actions should be specific enough that someone unfamiliar with the project can execute them
- Record blockers with mitigation strategies, not just descriptions — the next session should know how to start resolving them
- Update SESSION.md at natural breakpoints during a session, not just at the end
- Use commit hashes in completed items so progress can be verified against the git log
- Keep session history entries concise — one line per session with the key outcome
