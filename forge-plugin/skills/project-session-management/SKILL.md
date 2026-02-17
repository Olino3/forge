---
name: project-session-management
version: 1.0.0
description: Track progress across sessions using SESSION.md with git checkpoints and concrete next actions. Converts IMPLEMENTATION_PHASES.md into trackable session state. Like Hephaestus marking his progress on each divine artifact, this skill ensures no work is lost between forging sessions.
context:
  primary_domain: engineering
  supporting_domains:
    - documentation
  memory:
    skill_memory: project-session-management
    scopes:
      - session_history
      - handoff_patterns
tags:
  - planning
  - workflow
  - session
  - tracking
  - progress
triggers:
  - create SESSION.md
  - set up session tracking
  - manage session state
##   - session handoff

# Project Session Management

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 8-step workflow outlined in this document MUST be followed in exact order for EVERY session management operation. Skipping steps or deviating from the procedure will result in lost progress or incomplete handoffs. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Session management scenarios with sample outputs
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("project-session-management", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Session Management Focus Areas

Session management evaluates and tracks progress across 5 focus areas:

1. **Phase Tracking**: Map current progress against IMPLEMENTATION_PHASES.md phases and deliverables
2. **Git State Capture**: Record branch, commit hash, and uncommitted changes as verifiable checkpoints
3. **Blocker Identification**: Surface blockers with mitigation strategies so the next session starts unblocked
4. **Next Actions**: Define 3-5 concrete, actionable items for the next session — never vague or open-ended
5. **Session Handoff**: Package session state so any contributor (human or AI) can resume without context loss

**Note**: This skill produces and maintains SESSION.md as a living tracking document. It does not implement project features unless explicitly requested.

---

## Purpose

Track progress across sessions using SESSION.md with git checkpoints and concrete next actions. Converts IMPLEMENTATION_PHASES.md into trackable session state. Like Hephaestus marking his progress on each divine artifact, this skill ensures no work is lost between forging sessions.


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Check for an existing `SESSION.md` at the project root
2. Check for `IMPLEMENTATION_PHASES.md` (in project root or `/claudedocs/`)
3. Identify current git state:
   - Current branch name
   - Last commit hash and message
   - Uncommitted changes summary (`git status --short`)
4. Determine the operation type:
   - **Create**: No SESSION.md exists — initialize session tracking
   - **Update**: SESSION.md exists — record progress and prepare handoff
   - **Resume**: SESSION.md exists — read state and continue from checkpoint

**DO NOT PROCEED WITHOUT IDENTIFYING OPERATION TYPE AND GIT STATE**

### ⚠️ STEP 2: Load Memory (REQUIRED)

**YOU MUST:**
1. Identify the project name from the user prompt, SESSION.md, or repository name
2. Use `memoryStore.getSkillMemory("project-session-management", "{project-name}")` to load existing session memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
3. If memory exists, review previous session patterns:
   - Check session history for duration trends and progress velocity
   - Review handoff formats that worked well in past sessions
   - Note any recurring blockers from prior sessions
4. **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from other skill executions (especially `project-planning`)
5. If no memory exists, you will create it after generating the session document

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

**YOU MUST:**
1. Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
2. Load supporting context for documentation standards
3. If the project uses specific technologies, load relevant domain context:
   - Python projects: `contextProvider.getIndex("python")`
   - JavaScript/TypeScript projects: `contextProvider.getIndex("javascript")`
   - Infrastructure projects: `contextProvider.getIndex("devops")`
4. Apply cross-domain triggers as defined in the [Cross-Domain Matrix](../../context/cross_domain.md)

**DO NOT PROCEED WITHOUT LOADING RELEVANT CONTEXT**

### ⚠️ STEP 4: Assess Session State (REQUIRED)

**IF SESSION.md EXISTS:**
1. Parse current phase and progress percentage
2. Identify completed items with their git commit references
3. List in-progress items with current status
4. Review existing blockers — check if any have been resolved
5. Read previous next actions — determine which have been addressed

**IF SESSION.md DOES NOT EXIST:**
1. If IMPLEMENTATION_PHASES.md exists:
   - Parse all phases, deliverables, and verification criteria
   - Set initial progress to Phase 1, 0% complete
   - Pre-populate next actions from Phase 1 deliverables
2. If IMPLEMENTATION_PHASES.md does not exist:
   - Create SESSION.md from scratch based on project analysis
   - Define initial phase structure from repository state and user input
   - Set all items to "not started"

**DO NOT PROCEED WITHOUT COMPLETING SESSION STATE ASSESSMENT**

### ⚠️ STEP 5: Create/Update Session Document (REQUIRED)

**YOU MUST produce SESSION.md with the following structure:**

```markdown
# SESSION — {project-name}

## Current Phase
**Phase {N}: {Phase Name}**
Progress: {X}% complete

## Completed Items
- [x] {Item description} — `{commit-hash}` ({date})
- [x] {Item description} — `{commit-hash}` ({date})

## In Progress
- [ ] {Item description} — {status notes}
- [ ] {Item description} — {status notes}

## Blockers
| Blocker | Impact | Mitigation | Status |
|---------|--------|------------|--------|
| {Description} | {What it blocks} | {How to resolve} | {Open/Resolved} |

## Next Actions
1. {Concrete actionable item with specific deliverable}
2. {Concrete actionable item with specific deliverable}
3. {Concrete actionable item with specific deliverable}

## Git Checkpoint
- **Branch**: {branch-name}
- **Last Commit**: `{commit-hash}` — {commit-message}
- **Uncommitted Changes**: {summary or "None"}
- **Timestamp**: {ISO 8601 timestamp}

## Session History
| Session | Date | Duration | Progress |
|---------|------|----------|----------|
| {N} | {date} | {duration} | {summary of what was accomplished} |
```

**SESSION.md principles:**
- Completed items MUST reference git commit hashes for traceability
- Next actions MUST be concrete — include specific files, functions, or commands
- Blockers MUST include mitigation strategies, not just descriptions
- Progress percentage should reflect deliverables completed, not time spent
- The document must be self-contained — a new contributor should be able to resume from it alone

**DO NOT PROCEED WITHOUT GENERATING THE SESSION DOCUMENT**

### ⚠️ STEP 6: Git Checkpoint (REQUIRED)

**YOU MUST record the current git state:**
1. Capture current branch name via `git branch --show-current`
2. Capture HEAD commit hash and message via `git log -1 --format="%H — %s"`
3. Capture uncommitted changes summary via `git status --short`
4. Record timestamp in ISO 8601 format
5. Update the Git Checkpoint section of SESSION.md with this information

This checkpoint enables session handoff between human and AI sessions. Any contributor can read the checkpoint, verify they are on the correct branch and commit, and resume work from the documented state.

**DO NOT PROCEED WITHOUT RECORDING GIT CHECKPOINT**

### ⚠️ STEP 7: Generate Output (REQUIRED)

**YOU MUST:**
1. Save `SESSION.md` at the project root (this is the living tracking document)
2. Save a timestamped session snapshot to `/claudedocs/`:
   - Format: `SESSION_SNAPSHOT_{YYYY-MM-DD}.md`
   - This preserves session history even if SESSION.md is overwritten
3. Confirm all output files were written successfully
4. List all generated/updated documents with a brief description of each

**DO NOT SKIP OUTPUT GENERATION**

### ⚠️ STEP 8: Update Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.update(layer="skill-specific", skill="project-session-management", project="{project-name}", ...)` to store:
   - **session_history.md**: Record session date, duration, items completed, progress delta, and git checkpoint
   - **handoff_patterns.md**: Record which handoff formats were effective — what information the resuming session actually used
2. If this is the first session, create both memory files with initial data
3. If previous memory exists, append to history and update patterns with new learnings

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY session management operation, verify:
- [ ] Step 1: Existing SESSION.md checked, IMPLEMENTATION_PHASES.md checked, git state captured, operation type determined
- [ ] Step 2: Session memory checked via `memoryStore.getSkillMemory()` and prior patterns reviewed
- [ ] Step 3: Engineering and supporting domain context loaded via `contextProvider.getIndex()`
- [ ] Step 4: Session state fully assessed — completed items, in-progress items, blockers, and next actions identified
- [ ] Step 5: SESSION.md created/updated with all required sections (phase, completed, in-progress, blockers, next actions, git checkpoint, history)
- [ ] Step 6: Git checkpoint recorded with branch, commit hash, uncommitted changes, and timestamp
- [ ] Step 7: SESSION.md saved to project root and snapshot saved to `/claudedocs/`
- [ ] Step 8: Memory updated with session history and handoff patterns

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE SESSION MANAGEMENT OPERATION**

---

## Output File Naming Convention

**Primary output**: `SESSION.md` (project root — living document)

**Session snapshots**: `SESSION_SNAPSHOT_{YYYY-MM-DD}.md` (in `/claudedocs/` — historical record)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-06-30 | Initial release — 8-step mandatory workflow for session tracking with git checkpoints, progress mapping from IMPLEMENTATION_PHASES.md, and concrete next-action generation |
