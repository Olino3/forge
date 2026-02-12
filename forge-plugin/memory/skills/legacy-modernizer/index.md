# legacy-modernizer Memory

Project-specific memory for legacy code modernization progress, technical debt inventories, and migration patterns.

## Purpose

This memory helps the `skill:legacy-modernizer` remember:
- The current technical debt inventory and what has been addressed for each project
- Migration progress across phases and milestones
- Which modernization patterns worked well or poorly for each codebase
- Lessons learned during previous modernization sessions
- Baseline metrics (coverage, complexity, performance) to measure improvement over time

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `debt_inventory.md`

**Purpose**: Track all identified technical debt items, their classification, priority scores, and resolution status

**Should contain**:
- **Debt items**: Each item with type, description, location, and current status
- **Risk/Effort/Value scores**: Priority scoring on the 1-5 scale for each axis
- **Resolution status**: Open, in-progress, resolved, or deferred with rationale
- **Quick wins**: Low-effort, high-value items flagged for immediate action
- **Baseline metrics**: Complexity scores, coverage percentages, dependency ages at time of assessment

**Example structure**:
```markdown
# Debt Inventory - MyProject

## Assessment Date: 2026-02-12

## Summary
- Total items: 47
- Critical: 4
- High: 12
- Medium: 18
- Low: 13
- Resolved: 6

## Critical Items
| ID | Type | Description | Risk | Effort | Value | Status |
|----|------|-------------|------|--------|-------|--------|
| D-001 | Infrastructure | Python 2.7 EOL runtime | 5 | 5 | 5 | In Progress |
| D-002 | Dependency | requests 2.18 — CVE-2023-32681 | 5 | 1 | 5 | Resolved |

## Baseline Metrics
- Cyclomatic complexity (avg): 28
- Test coverage: 0%
- Dependencies behind major version: 12/34
- Build time: 4m 32s
```

**When to update**: After each assessment session or when debt items are resolved

---

#### `migration_progress.md`

**Purpose**: Track migration plan phases, milestones, and current status for ongoing modernization efforts

**Should contain**:
- **Migration plan**: Phases with descriptions, timelines, and success criteria
- **Current phase**: Which phase is active and what work remains
- **Completed milestones**: What has been accomplished with dates
- **Blockers**: Any issues preventing progress
- **Metrics delta**: How key metrics have changed since the last assessment

**Example structure**:
```markdown
# Migration Progress - MyProject

## Strategy: Strangler Fig + Parallel Run
## Started: 2026-02-12
## Current Phase: Phase 2 — API Extraction

## Phases
| Phase | Description | Status | Completion |
|-------|-------------|--------|------------|
| 1 | Safety nets & characterization tests | ✅ Complete | 2026-02-28 |
| 2 | API extraction & parallel run | 🔄 In Progress | — |
| 3 | Frontend migration (jQuery → React) | ⏳ Pending | — |
| 4 | Backend cutover (PHP → Node.js) | ⏳ Pending | — |

## Phase 2 Progress
- [x] Product catalog API endpoint
- [x] User authentication API endpoint
- [ ] Shopping cart API endpoint
- [ ] Payment processing API endpoint
- [ ] Order management API endpoint

## Metrics Delta
| Metric | Baseline | Current | Target |
|--------|----------|---------|--------|
| Test coverage | 0% | 34% | 80% |
| Avg complexity | 28 | 22 | <10 |
| Critical CVEs | 8 | 2 | 0 |
```

**When to update**: After each modernization session or phase completion

---

#### `modernization_patterns.md`

**Purpose**: Record which modernization patterns were applied, their outcomes, and lessons learned for this specific project

**Should contain**:
- **Patterns applied**: Which patterns were used and where
- **Outcomes**: Whether each pattern application succeeded, with evidence
- **Lessons learned**: What worked, what didn't, and what to do differently
- **Project-specific conventions**: Naming, structure, or approach decisions made during modernization
- **Gotchas**: Unexpected issues encountered and how they were resolved

**Example structure**:
```markdown
# Modernization Patterns - MyProject

## Patterns Applied

### Strangler Fig (API Layer)
- **Applied to**: PHP backend → Node.js API migration
- **Outcome**: Success — 5 endpoints migrated, zero downtime
- **Mechanism**: Nginx reverse proxy routes /api/v2/* to Node.js, everything else to PHP
- **Lesson**: Start with read-only endpoints to build confidence before migrating writes

### Characterization Tests
- **Applied to**: Checkout flow, payment processing
- **Outcome**: Caught 3 undocumented discount rules during migration
- **Mechanism**: Recorded production I/O pairs as test fixtures
- **Lesson**: Always capture edge cases from production logs, not just happy paths

## Gotchas
1. Session handling differed between PHP and Node.js — needed shared Redis session store
2. Date formatting in legacy PHP used server timezone, new code uses UTC — added conversion layer
3. Legacy database had implicit charset Latin-1, new ORM assumed UTF-8 — bulk conversion needed

## Project Conventions
- API versioning: /api/v2/ for new endpoints, /api/v1/ (legacy) maintained until Phase 4
- Feature toggles: LaunchDarkly flags prefixed with `modernize-*`
- Commit convention: `modernize(scope): description` for all migration-related changes
```

**When to update**: After each modernization session, especially when new patterns are tried or lessons are learned

---

## Usage in skill:legacy-modernizer

### Loading Memory

```markdown
# In skill workflow Step 3

project_name = detect_project_name()
memory = memoryStore.getSkillMemory("legacy-modernizer", "{project-name}")

if memory exists:
    debt_inventory = read(memory, "debt_inventory.md")
    migration_progress = read(memory, "migration_progress.md")
    patterns = read(memory, "modernization_patterns.md")

    # Use for planning decisions
    - Skip already-resolved debt items
    - Continue from current migration phase
    - Reuse patterns that worked, avoid those that failed
    - Apply lessons learned to current session
```

### Updating Memory

```markdown
# In skill workflow Step 5

After completing modernization work:

1. Update debt inventory:
   - Mark resolved items, add newly discovered items
   - Update metrics delta

2. Update migration progress:
   - Check off completed milestones
   - Advance phase status if applicable
   - Record any new blockers

3. Update patterns:
   - Document any new patterns applied
   - Record outcomes and lessons learned

4. Persist:
   memoryStore.update(layer="skill-specific", skill="legacy-modernizer",
                      project="{project-name}", ...)
```

---

## Memory Evolution Over Time

### After 1st Assessment
```markdown
# debt_inventory.md — Initial assessment with 47 items scored and prioritized
# migration_progress.md — Plan drafted with 4 phases, Phase 1 starting
# modernization_patterns.md — Empty, no patterns applied yet
```

### After 5 Sessions
```markdown
# debt_inventory.md — 12 items resolved, 3 new items discovered, metrics improving
# migration_progress.md — Phase 2 in progress, Phase 1 lessons applied
# modernization_patterns.md — 3 patterns documented with outcomes and 5 gotchas
```

### After 20 Sessions
```markdown
# Comprehensive modernization history — serves as institutional knowledge
# Debt inventory is a living document with full resolution history
# Pattern library is project-specific best practices guide
# Memory provides high-value guidance for remaining modernization work
```

---

## Related Documentation

- **Main Memory Index**: `../index.md` for memory system overview
- **Skill Documentation**: `../../skills/legacy-modernizer/SKILL.md` for skill workflow
- **Context Files**: `../../context/` for general development knowledge
- **Memory Lifecycle**: `../lifecycle.md` for memory freshness and pruning
- **Memory Quality**: `../quality_guidance.md` for memory validation
