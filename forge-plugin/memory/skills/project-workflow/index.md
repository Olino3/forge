# project-workflow Memory

Project-specific memory for workflow command history, usage patterns, and lifecycle insights.

## Purpose

This memory helps the `skill:project-workflow` remember:
- Which workflow commands were invoked, in what order, and their outcomes
- Command usage frequency and common command sequences per project
- Effective workflow patterns for different project types and lifecycle stages
- Lessons learned from retrospectives and workflow optimizations

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `workflow_history.md`

**Purpose**: Track every workflow command invocation with context, delegation targets, and outcome summaries for audit and pattern analysis

**Should contain**:
- Command name, date, and project state at time of invocation
- Delegation target (if applicable — e.g., `skill:project-planning` for `/plan-project`)
- Outcome summary (what was produced, files generated)
- Project lifecycle stage at invocation (ideation, planning, development, release, maintenance)
- Any issues encountered or edge cases handled

**Example structure**:
```markdown
# Workflow History

## /explore-idea — 2025-06-15
- **Project State**: New (no existing artifacts)
- **Delegation**: None (self-contained)
- **Outcome**: Feasibility analysis generated — GO recommendation
- **Output**: `/claudedocs/explore_idea_mock-data-cli_2025-06-15.md`
- **Lifecycle Stage**: Ideation

## /plan-project — 2025-06-16
- **Project State**: Post-exploration (idea validated)
- **Delegation**: `skill:project-planning`
- **Outcome**: 6-phase implementation plan generated with TECH_STACK_DECISIONS.md
- **Output**: `/claudedocs/IMPLEMENTATION_PHASES.md`, `/claudedocs/TECH_STACK_DECISIONS.md`
- **Lifecycle Stage**: Planning

## /wrap-session — 2025-06-17
- **Project State**: In-progress (Phase 1, 80% complete)
- **Delegation**: `skill:project-session-management`
- **Outcome**: SESSION.md updated with git checkpoint and 3 next actions
- **Output**: `SESSION.md`, `/claudedocs/SESSION_SNAPSHOT_2025-06-17.md`
- **Lifecycle Stage**: Development
```

**When to update**: After every workflow command invocation — record the command, context, and outcome

#### `command_usage.md`

**Purpose**: Track command frequency, common sequences, and effective patterns to improve future workflow recommendations

**Should contain**:
- Command frequency counts per project
- Common command sequences (e.g., `/explore-idea` → `/plan-project` → `/plan-feature`)
- Effective patterns by project type (what commands worked well for which situations)
- Anti-patterns (command sequences that led to rework or confusion)

**Example structure**:
```markdown
# Command Usage

## Frequency (mock-data-cli)
| Command | Count | Last Used |
|---------|-------|-----------|
| /explore-idea | 1 | 2025-06-15 |
| /plan-project | 1 | 2025-06-16 |
| /plan-feature | 3 | 2025-06-25 |
| /wrap-session | 5 | 2025-06-28 |
| /continue-session | 4 | 2025-06-28 |
| /workflow | 2 | 2025-06-20 |
| /brief | 1 | 2025-06-27 |
| /reflect | 1 | 2025-06-30 |
| /release | 0 | — |

## Effective Sequences
- **New project startup**: `/explore-idea` → `/plan-project` → `/plan-feature` (for first feature) → `/wrap-session`
- **Daily development**: `/continue-session` → (work) → `/wrap-session`
- **Sprint boundary**: `/reflect` → `/brief` → `/plan-feature` (next sprint features)

## Patterns
- Running `/workflow` after `/continue-session` helps orient when returning to a project after a gap
- `/brief` before `/reflect` provides data for the retrospective analysis
- `/plan-feature` is most effective when run after `/continue-session` so current context is loaded
```

**When to update**: After every workflow command invocation — increment frequency, record sequences, and note effective patterns

## Memory Lifecycle

### Creation (First Workflow Command)
1. Skill runs for the first time on a project
2. Completes the requested command workflow
3. Creates project memory directory
4. Saves initial entry to `workflow_history.md`
5. Saves initial frequency data to `command_usage.md`

### Growth (Ongoing Usage)
1. Each command invocation appends to `workflow_history.md`
2. Each command invocation updates frequency counts in `command_usage.md`
3. Command sequences emerge from history analysis
4. Effective patterns are documented as they are discovered

### Maintenance (Periodic Review)
1. Review workflow history for stale entries — archive entries older than 6 months
2. Consolidate command usage patterns — remove outdated sequences
3. Update effective patterns based on accumulated project experience
4. Prune anti-patterns that have been resolved

## Related Documentation

- **Skill Documentation**: `../../skills/project-workflow/SKILL.md`
- **Main Memory Index**: `../index.md`
