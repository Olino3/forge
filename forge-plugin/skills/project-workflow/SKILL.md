---
name: "project-workflow"
description: "Nine integrated slash commands for complete project lifecycle: /explore-idea, /plan-project, /plan-feature, /wrap-session, /continue-session, /workflow, /release, /brief, /reflect. Like Hephaestus orchestrating the full lifecycle of a divine artifact — from inspiration through forging to final polish — this skill unifies all project commands into a single cohesive workflow."
version: "1.0.0"
context:
  primary_domain: "engineering"
  supporting_domains:
    - "documentation"
  always_load_files: []
  detection_required: false
  file_budget: 5
memory:
  skill_memory: project-workflow
  scopes:
    - type: "skill-specific"
      files: [workflow_history.md, command_usage.md]
    - type: "shared-project"
      usage: "reference"
tags:
  - "planning"
  - "workflow"
  - "project"
  - "lifecycle"
  - "commands"
triggers:
  - "start new project"
##   - "/plan-project"

# skill:project-workflow - Project Lifecycle Workflow Manager

## Version: 1.0.0

## Purpose

The project-workflow skill manages the complete project lifecycle through nine integrated slash commands. It serves as the central dispatcher for all project-related operations — from initial idea exploration through planning, session management, release preparation, and retrospective analysis. Each command delegates to specialized skills where appropriate, ensuring consistent workflow patterns and memory continuity across the entire project lifecycle.

## File Structure

```
skills/project-workflow/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Command Overview

| Command | Purpose | Delegation |
|---------|---------|------------|
| `/explore-idea` | Brainstorm and validate a project concept with feasibility analysis | Self-contained |
| `/plan-project` | Generate full project plan with phases, tech stack, and milestones | Delegates to `skill:project-planning` |
| `/plan-feature` | Plan a single feature with tasks, acceptance criteria, and estimation | Self-contained |
| `/wrap-session` | Save current progress, create git checkpoint, document next actions | Delegates to `skill:project-session-management` |
| `/continue-session` | Load last session state, review progress, suggest next steps | Delegates to `skill:project-session-management` |
| `/workflow` | Display current project workflow status and available commands | Self-contained |
| `/release` | Prepare release notes, version bump, changelog update | Self-contained |
| `/brief` | Generate concise project status brief for stakeholders | Self-contained |
| `/reflect` | Retrospective analysis of recent work — what went well, what to improve | Self-contained |

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Identify which workflow command was invoked from the user prompt or conversation context
2. Gather project context:
   - Project name (from user prompt, `SESSION.md`, repository name, or ask the user)
   - Current project state (new, in-progress, nearing release, post-release)
   - Existing project artifacts (`IMPLEMENTATION_PHASES.md`, `SESSION.md`, `CHANGELOG.md`)
3. Detect current project state:
   - Check for `SESSION.md` at the project root
   - Check for `IMPLEMENTATION_PHASES.md` (in project root or `/claudedocs/`)
   - Check for `CHANGELOG.md` and version information
   - Identify current git state (branch, last commit, uncommitted changes)
4. Validate the command is appropriate for the current project state:
   - `/explore-idea` and `/plan-project`: Valid at any stage, but warn if planning docs already exist
   - `/plan-feature`: Requires an existing project context
   - `/wrap-session` and `/continue-session`: Require session tracking capability
   - `/release`: Requires existing codebase with changes to release
   - `/brief` and `/reflect`: Require project history to analyze

**DO NOT PROCEED WITHOUT IDENTIFYING THE COMMAND AND PROJECT STATE**

### ⚠️ STEP 2: Load Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("project-workflow", "{project-name}")` to load existing workflow memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
2. If memory exists, review previous workflow patterns:
   - Check command usage history for this project
   - Review workflow patterns that were effective
   - Note any command-specific preferences or conventions
3. **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from other skill executions (especially `project-planning` and `project-session-management`)
4. If no memory exists, you will create it after executing the command

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
5. Stay within the file budget declared in frontmatter

**DO NOT PROCEED WITHOUT LOADING RELEVANT CONTEXT**

### ⚠️ STEP 4: Route to Command Handler (REQUIRED)

**Based on the command identified in Step 1, dispatch to the appropriate handler:**

#### `/explore-idea` — Brainstorm and Validate a Project Concept
1. Capture the idea description from the user prompt
2. Analyze feasibility across dimensions: technical complexity, resource requirements, market fit, timeline
3. Identify risks, unknowns, and dependencies
4. Generate a structured idea brief with go/no-go recommendation
5. Suggest next steps if the idea is viable (typically `/plan-project`)

#### `/plan-project` — Generate Full Project Plan
1. **Delegate to `skill:project-planning`** via `skillInvoker.invoke("project-planning", { project, requirements })`
2. Pass gathered context and memory to the delegated skill
3. Receive structured planning documents (IMPLEMENTATION_PHASES.md + conditional docs)
4. Record the delegation in workflow history

#### `/plan-feature` — Plan a Single Feature
1. Capture the feature description and scope from the user prompt
2. Break the feature into discrete tasks with clear boundaries
3. Define acceptance criteria for each task
4. Estimate effort for each task (Small / Medium / Large)
5. Identify dependencies on other features or infrastructure
6. Generate a feature plan document

#### `/wrap-session` — Save Progress and Create Checkpoint
1. **Delegate to `skill:project-session-management`** via `skillInvoker.invoke("project-session-management", { operation: "update", project })`
2. Pass current git state and progress context to the delegated skill
3. Receive updated SESSION.md with git checkpoint and next actions
4. Record the session wrap in workflow history

#### `/continue-session` — Resume from Last Checkpoint
1. **Delegate to `skill:project-session-management`** via `skillInvoker.invoke("project-session-management", { operation: "resume", project })`
2. Receive session state with progress summary and next actions
3. Present the resumption context to the user with suggested next steps
4. Record the session continuation in workflow history

#### `/workflow` — Display Workflow Status
1. Scan for existing project artifacts (planning docs, session state, changelogs)
2. Determine current lifecycle stage (ideation, planning, development, release, maintenance)
3. List available commands relevant to the current stage
4. Display project timeline and recent activity summary

#### `/release` — Prepare Release
1. Scan git log for changes since the last tag or release
2. Categorize changes (features, fixes, breaking changes, docs)
3. Generate or update `CHANGELOG.md` with the new release entry
4. Suggest version bump based on change types (semver)
5. Prepare release notes suitable for publication

#### `/brief` — Generate Status Brief
1. Gather project status from `SESSION.md`, recent git activity, and planning docs
2. Summarize current progress against planned milestones
3. Highlight blockers, risks, and upcoming deadlines
4. Generate a concise stakeholder-friendly brief

#### `/reflect` — Retrospective Analysis
1. Review recent work history from `SESSION.md`, git log, and memory
2. Identify what went well — effective patterns, smooth phases, good decisions
3. Identify what to improve — blockers, slow phases, rework areas
4. Generate actionable improvement items for future work
5. Record insights in workflow memory for future reference

**DO NOT PROCEED WITHOUT COMPLETING THE COMMAND HANDLER**

### ⚠️ STEP 5: Execute Command Logic (REQUIRED)

**YOU MUST:**
1. Run the specific command's workflow as defined in Step 4
2. For delegated commands (`/plan-project`, `/wrap-session`, `/continue-session`):
   - Invoke the target skill with appropriate parameters
   - Wait for the delegated skill to complete
   - Integrate the results into the workflow response
3. For self-contained commands:
   - Execute the full command logic within this skill
   - Apply project-specific conventions from memory
   - Validate outputs against quality criteria
4. Handle edge cases gracefully:
   - Missing prerequisites (e.g., no `SESSION.md` for `/continue-session`) — guide the user to the appropriate setup command
   - Conflicting state (e.g., uncommitted changes during `/release`) — warn and suggest resolution

**DO NOT PROCEED WITHOUT EXECUTING THE COMMAND LOGIC**

### ⚠️ STEP 6: Generate Output (REQUIRED)

**YOU MUST:**
1. Save command output to `/claudedocs/` following naming conventions:
   - `/explore-idea`: `explore_idea_{project}_{YYYY-MM-DD}.md`
   - `/plan-project`: Output generated by delegated `skill:project-planning`
   - `/plan-feature`: `feature_plan_{feature-name}_{YYYY-MM-DD}.md`
   - `/wrap-session`: Output generated by delegated `skill:project-session-management`
   - `/continue-session`: Output generated by delegated `skill:project-session-management`
   - `/workflow`: `workflow_status_{project}_{YYYY-MM-DD}.md`
   - `/release`: `release_notes_{version}_{YYYY-MM-DD}.md`
   - `/brief`: `project_brief_{project}_{YYYY-MM-DD}.md`
   - `/reflect`: `retrospective_{project}_{YYYY-MM-DD}.md`
2. Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Confirm all output files were written successfully
4. List all generated documents with a brief description of each

**DO NOT SKIP OUTPUT GENERATION**

### ⚠️ STEP 7: Update Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.update(layer="skill-specific", skill="project-workflow", project="{project-name}", ...)` to store:
   - **workflow_history.md**: Record the command invoked, date, project state, delegation targets, and outcome summary
   - **command_usage.md**: Track command frequency, common sequences, and effective patterns per project
2. If this is the first workflow interaction, create both memory files with initial data
3. If previous memory exists, append to history and update usage patterns with new learnings
4. For delegated commands, note that the delegated skill handles its own memory update

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY project workflow command, verify:
- [ ] Step 1: Command identified, project context gathered, project state detected, command validity confirmed
- [ ] Step 2: Workflow memory checked via `memoryStore.getSkillMemory()` and prior patterns reviewed
- [ ] Step 3: Engineering and supporting domain context loaded via `contextProvider.getIndex()`
- [ ] Step 4: Correct command handler selected and dispatched
- [ ] Step 5: Command logic executed with delegations completed and edge cases handled
- [ ] Step 6: Output saved to `/claudedocs/` with correct naming conventions
- [ ] Step 7: Memory updated with workflow history and command usage patterns

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE WORKFLOW COMMAND**

---

## Output File Naming Convention

| Command | Format |
|---------|--------|
| `/explore-idea` | `explore_idea_{project}_{YYYY-MM-DD}.md` |
| `/plan-project` | Managed by `skill:project-planning` |
| `/plan-feature` | `feature_plan_{feature-name}_{YYYY-MM-DD}.md` |
| `/wrap-session` | Managed by `skill:project-session-management` |
| `/continue-session` | Managed by `skill:project-session-management` |
| `/workflow` | `workflow_status_{project}_{YYYY-MM-DD}.md` |
| `/release` | `release_notes_{version}_{YYYY-MM-DD}.md` |
| `/brief` | `project_brief_{project}_{YYYY-MM-DD}.md` |
| `/reflect` | `retrospective_{project}_{YYYY-MM-DD}.md` |

All files are saved to the `/claudedocs/` directory.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-06-30 | Initial release — 7-step mandatory workflow with nine integrated slash commands for complete project lifecycle management, skill delegation for planning and session management, and unified workflow memory |
