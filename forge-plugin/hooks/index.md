# Forge Hooks Architecture

Claude Code hooks are bash scripts that execute automatically in response to tool events. In the Forge plugin, hooks are registered in `hooks/hooks.json` and scripts live alongside it in `forge-plugin/hooks/`.

## Hook System Overview

### How Plugin Hooks Work

The Forge is a Claude Code plugin. Hooks are declared in `hooks/hooks.json` using a three-level structure:

```
event → matcher group (regex on tool name) → handler array
```

Claude Code reads `hooks.json` from the plugin root and executes matching handlers automatically. Scripts reference their own location via `${CLAUDE_PLUGIN_ROOT}`.

### Event Types

Claude Code supports 14 hook events. The Forge currently uses these:

| Event | When It Fires | Forge Hooks |
|-------|--------------|-------------|
| `SessionStart` | Session begins | `root_agent_validator` |
| `UserPromptSubmit` | User sends a prompt | `pii_redactor` |
| `PreToolUse` | Before a tool executes | `pre_commit_quality`, `memory_freshness_enforcer`, `frontmatter_validator`, `sandbox_boundary_guard`, `dependency_sentinel`, `git_hygiene_enforcer` |
| `PostToolUse` | After a tool executes | `memory_quality_gate`, `output_archival`, `system_health_emitter`, `memory_cross_pollinator`, `context_drift_detector`, `output_quality_scorer` |
| `Stop` | Claude stops responding | `skill_compliance_checker`, `forge_telemetry` |
| `PreCompact` | Before context compaction | `context_usage_tracker` |
| `TaskCompleted` | Task marked as completed | `command_chain_context` |
| `SubagentStart` | Subagent spawned | `agent_config_validator` |
| `SessionEnd` | Session terminates | `memory_pruning_daemon` |

Other available events (not yet used): `PermissionRequest`, `PostToolUseFailure`, `Notification`, `SubagentStop`, `TeammateIdle`.

### Input / Output Contract

| Aspect | Details |
|--------|---------|
| **Input** | JSON on stdin with `session_id`, `cwd`, `hook_event_name`, plus event-specific fields |
| **Output** | JSON on stdout (parsed by Claude Code) or plain text (for SessionStart) |
| **Exit 0** | Success — stdout JSON is parsed for decisions/context |
| **Exit 2** | Blocking error — stderr is fed to Claude as context |
| **Other exit** | Non-blocking error — logged but ignored |
| **Timeout** | Hooks must complete within 60 seconds (default) |

### PreToolUse Decision Control

PreToolUse hooks can control tool execution via JSON output:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow | deny | ask",
    "permissionDecisionReason": "Explanation shown to Claude"
  }
}
```

### PostToolUse Feedback

PostToolUse hooks surface context to Claude:

```json
{
  "additionalContext": "Information added to Claude's context"
}
```

### Parallel Execution

All matching hooks for the same event run **in parallel**. This means:
- Hooks cannot depend on the execution order of sibling hooks
- The health buffer aggregator (`system_health_emitter`) reports warnings from *prior* events, not the current one (one-event lag)

## Forge Hook Layers

Hooks are organized into four thematic layers from the Architectural Roadmap §6:

### §6.1 The Shield — Safety & Guardrails

| Hook | Event | Matcher | Purpose |
|------|-------|---------|---------|
| `pre_commit_quality` | PreToolUse | `Bash` | Block commits with secrets or staged `/claudedocs` files |
| `memory_freshness_enforcer` | PreToolUse | `Read` | Deny reads of stale memory (90+ days) — Ghost Archive |
| `root_agent_validator` | SessionStart | — | Validate plugin structure at startup |
| `sandbox_boundary_guard` | PreToolUse | `Read\|Write\|Edit\|Bash` | Block file ops outside project scope; detect dangerous Bash paths |
| `dependency_sentinel` | PreToolUse | `Bash` | Block install of denied/typosquatted packages |
| `git_hygiene_enforcer` | PreToolUse | `Bash` | Enforce safe git push/commit practices, scan for secrets |
| `pii_redactor` | UserPromptSubmit | — | Warn on PII patterns in user prompts |

### §6.2 The Chronicle — Observability

| Hook | Event | Matcher | Purpose |
|------|-------|---------|---------|
| `system_health_emitter` | PostToolUse | `.*` | Flush the health buffer and surface warnings to Claude |
| `memory_cross_pollinator` | PostToolUse | `Write\|Edit` | Share critical skill findings to `cross_skill_insights.md` |
| `memory_pruning_daemon` | SessionEnd | — | Batch-prune memory files exceeding line limits after session ends |

### §6.3 The Foreman — Quality Enforcement

| Hook | Event | Matcher | Purpose |
|------|-------|---------|---------|
| `memory_quality_gate` | PostToolUse | `Write\|Edit` | Validate memory files (timestamp, limits, specificity) |
| `frontmatter_validator` | PreToolUse | `Write\|Edit` | Block context file writes missing required frontmatter |
| `context_drift_detector` | PostToolUse | `Write\|Edit` | Warn when dep files conflict with context domain tags |
| `skill_compliance_checker` | Stop | — | Audit transcript for skill workflow compliance |
| `command_chain_context` | TaskCompleted | — | Persist ExecutionContext to `.forge/chain_state.json` for command chaining |
| `agent_config_validator` | SubagentStart | agent type | Validate agent config against `agent_config.schema.json` |

### §6.4 The Town Crier — Notifications

| Hook | Event | Matcher | Purpose |
|------|-------|---------|---------|
| `output_archival` | PostToolUse | `Write\|Edit` | Archive `/claudedocs` output files |
| `forge_telemetry` | Stop | — | Log session metrics to `.forge/telemetry.log` |
| `context_usage_tracker` | PreCompact | — | Identify unused context files for token optimization |
| `output_quality_scorer` | PostToolUse | `Write\|Edit` | Score `/claudedocs` output quality (completeness, actionability, formatting) |

## Manual Hooks (Not Registered)

These hooks are run manually and are **not** in `hooks.json`:

| Hook | Purpose | Usage |
|------|---------|-------|
| `context_freshness` | Audit context file health and broken links | `bash forge-plugin/hooks/context_freshness.sh` |
| `session_context` | Display project context summary | `bash forge-plugin/hooks/session_context.sh [project]` |

## Deprecated Hooks

| Hook | Status | Replacement |
|------|--------|-------------|
| `memory_sync` | Absorbed | `memory_quality_gate` — provides all of memory_sync's functionality plus additional quality checks |

## Shared Infrastructure

### Health Buffer (`lib/health_buffer.sh`)

A shared library for concurrent-safe warning aggregation:

```bash
source "${CLAUDE_PLUGIN_ROOT}/hooks/lib/health_buffer.sh"
health_buffer_append "⚠️ Warning message"     # append a warning
health_buffer_flush                             # read and clear all warnings
```

- Uses `flock(1)` for safe concurrent writes (hooks run in parallel)
- Buffer lives at `.forge/health_buffer` (gitignored)
- Capped at 200 lines to prevent unbounded growth

### Runtime Directory (`.forge/`)

Ephemeral runtime state directory (gitignored):

| File | Purpose |
|------|---------|
| `health_buffer` | Accumulated warnings between flush cycles |
| `health_buffer.lock` | flock lock file for concurrent access |
| `chain_state.json` | Command chain execution context (persisted by `command_chain_context`) |

### Safety Profile (`templates/root_safety_profile.json`)

Default structural manifest validated by `root_agent_validator` at session start. Projects can override by placing `safety_profile.json` in `.forge/`.

## File Reference

| File | Type | Description |
|------|------|-------------|
| `hooks.json` | Registry | Plugin hook registration (read by Claude Code) |
| `lib/health_buffer.sh` | Library | Shared health buffer helpers |
| `lib/framework_conflicts.json` | Data | Framework conflict groups for context drift detection |
| `system_health_emitter.sh` | PostToolUse | Health buffer aggregator |
| `memory_freshness_enforcer.sh` | PreToolUse | Ghost Archive — stale memory blocker |
| `memory_quality_gate.sh` | PostToolUse | Memory write validator |
| `frontmatter_validator.sh` | PreToolUse | Context frontmatter gate |
| `root_agent_validator.sh` | SessionStart | Startup integrity check |
| `pre_commit_quality.sh` | PreToolUse | Pre-commit quality gate |
| `output_archival.sh` | PostToolUse | Output file archival |
| `sandbox_boundary_guard.sh` | PreToolUse | Host isolation — project-scope enforcement |
| `memory_cross_pollinator.sh` | PostToolUse | Cross-skill critical insight sharing |
| `context_drift_detector.sh` | PostToolUse | Dependency-vs-context tag conflict detector |
| `skill_compliance_checker.sh` | Stop | Skill workflow compliance audit |
| `dependency_sentinel.sh` | PreToolUse | Supply chain security — deny list enforcement |
| `git_hygiene_enforcer.sh` | PreToolUse | Source control safety — branch protection, secret scanning |
| `pii_redactor.sh` | UserPromptSubmit | Data privacy — PII pattern detection in prompts |
| `forge_telemetry.sh` | Stop | Session metrics aggregation and telemetry logging |
| `context_usage_tracker.sh` | PreCompact | Context file usage analysis before compaction |
| `output_quality_scorer.sh` | PostToolUse | Output quality scoring for `/claudedocs/` files |
| `command_chain_context.sh` | TaskCompleted | Command chain state persistence for ExecutionContext |
| `agent_config_validator.sh` | SubagentStart | Agent configuration validation against schema |
| `memory_pruning_daemon.sh` | SessionEnd | Post-session memory file line-count pruning |
| `security/deny_list.txt` | Data | Package deny list for dependency_sentinel |
| `context_freshness.sh` | Manual | Context health audit |
| `session_context.sh` | Manual | Session context summary |
| `memory_sync.sh` | Deprecated | Superseded by memory_quality_gate |

---

*Last Updated: 2026-02-11*
