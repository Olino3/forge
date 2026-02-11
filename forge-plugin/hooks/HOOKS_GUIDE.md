# Forge Hooks Guide

Comprehensive guide for using, configuring, and creating Forge hooks.

## How Claude Code Plugin Hooks Work

The Forge registers hooks via `hooks/hooks.json` in the plugin root. Claude Code discovers this file automatically and wires up the handlers — no manual `settings.local.json` editing required.

### hooks.json Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolNameRegex",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/script.sh\""
          }
        ]
      }
    ]
  }
}
```

**Key points:**
- `matcher` is a regex tested against the tool name (e.g. `Bash`, `Read`, `Write|Edit`, `.*`)
- `${CLAUDE_PLUGIN_ROOT}` resolves to the plugin directory at runtime
- Multiple hooks in the same matcher group all execute
- Hooks for the same event run **in parallel**

### Supported Events

| Event | When It Fires | Input Fields |
|-------|--------------|-------------|
| `SessionStart` | Session begins | `source`, `model` + common fields |
| `SessionEnd` | Session ends | `reason` + common fields |
| `UserPromptSubmit` | User sends a message | `prompt` + common fields |
| `PreToolUse` | Before a tool runs | `tool_name`, `tool_input`, `tool_use_id` + common fields |
| `PostToolUse` | After a tool runs | `tool_name`, `tool_input`, `tool_response`, `tool_use_id` + common fields |
| `PostToolUseFailure` | Tool execution failed | `tool_name`, `tool_input`, `error` + common fields |
| `PermissionRequest` | Permission prompt | `tool_name`, `tool_input` + common fields |
| `Notification` | Claude sends notification | `message`, `notification_type` + common fields |
| `SubagentStart` | Subagent spawned | `agent_id`, `agent_type` + common fields |
| `SubagentStop` | Subagent finished | `agent_id`, `agent_type`, `agent_transcript_path` + common fields |
| `Stop` | Claude stops responding | `stop_hook_active` + common fields |
| `TeammateIdle` | Teammate becomes idle | `teammate_name`, `team_name` + common fields |
| `TaskCompleted` | Task finished | `task_id`, `task_subject` + common fields |
| `PreCompact` | Before context compaction | `trigger`, `custom_instructions` + common fields |

**Common input fields** (all events): `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success — stdout is parsed as JSON |
| `2` | **Blocking error** — stderr is fed to Claude |
| Other | Non-blocking error — logged but ignored |

### Decision Control (PreToolUse)

PreToolUse hooks can allow, deny, or escalate tool execution:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Explanation for Claude"
  }
}
```

| Decision | Effect |
|----------|--------|
| `allow` | Tool proceeds without prompting |
| `deny` | Tool is blocked; reason shown to Claude |
| `ask` | Escalates to user for manual approval |

### Feedback (PostToolUse)

PostToolUse hooks surface information to Claude:

```json
{
  "additionalContext": "This text is added to Claude's context"
}
```

### SessionStart Output

For SessionStart hooks, both stdout text and `additionalContext` JSON are added to Claude's initial context.

## Currently Active Hooks

### The Shield — Safety & Guardrails (§6.1)

#### pre_commit_quality.sh

**Event**: PreToolUse → `Bash`

Blocks `git commit` commands that would stage secrets or violate conventions.

**Checks:**
- Staged secret files (`.env`, `credentials.json`, `*.pem`, `*.key`)
- Staged `/claudedocs/` output files (warning)
- Modified `SKILL.md` files without Version History (warning)
- Absolute paths in memory files (warning)

**Behavior:** Denies the Bash tool if secrets are detected. Surfaces warnings as `additionalContext` for non-blocking issues.

#### memory_freshness_enforcer.sh

**Event**: PreToolUse → `Read`

Implements the **Ghost Archive** pattern: blocks reads of stale memory files.

| Age | Action |
|-----|--------|
| 0–30 days | Allow (fresh) |
| 31–90 days | Allow + health buffer warning |
| 90+ days | **Deny** — forces refresh or archival |
| No timestamp | **Deny** — must add timestamp first |

**Skips:** Non-memory files, operational files (`sync_log.md`, `index.md`, `lifecycle.md`, `quality_guidance.md`).

#### root_agent_validator.sh

**Event**: SessionStart

Validates plugin structural integrity at the start of every session:

- Required directories and files exist (per safety profile)
- `hooks.json` is valid JSON
- Agent configs have matching `.md` files
- Creates `.forge/` runtime directory if missing

**Output**: Plain text summary added to Claude's initial context, including component counts.

**Safety profile**: Uses `templates/root_safety_profile.json` by default. Override by placing `safety_profile.json` in `.forge/`.

#### sandbox_boundary_guard.sh

**Event**: PreToolUse → `Read|Write|Edit|Bash`

Restricts file operations to the project directory, blocking access to sensitive host paths.

**For Read/Write/Edit:**
- Resolves the file path to absolute form
- Checks if path is within the project directory (`cwd`)
- Allows exceptions: `/tmp`, `/var/tmp`, `/dev/null`, `/dev/std*`
- Denies everything else

**For Bash (best-effort):**
- Scans command text for known dangerous path patterns:
  - `~/.ssh`, `~/.gnupg`, `~/.aws`, `~/.kube`, `~/.docker`
  - `~/.config`, `~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, `~/.profile`
  - `/etc/passwd`, `/etc/shadow`, `/etc/hosts`, `/etc/sudoers`
  - `$HOME/.ssh`, `$HOME/.gnupg`, `$HOME/.config`, `$HOME/.aws`
- Detects `rm -rf /` (whole-filesystem destruction)

**Behavior:** Denies the tool call and surfaces a denial reason to Claude. Logs violations to the health buffer.

**Configuration**: Dangerous path patterns are documented in `templates/root_safety_profile.json` under `sandboxBoundary`.

#### dependency_sentinel.sh

**Event**: PreToolUse → `Bash`

Blocks installation of packages listed on the security deny list.

**Trigger**: Bash commands matching package install patterns:
- `pip install`, `pip3 install`, `python -m pip install`
- `npm install`, `npm i`, `npm add`
- `yarn add`
- `go get`
- `dotnet add package`

**Deny list**: `forge-plugin/security/deny_list.txt`
- One package per line
- Supports ecosystem prefixes (`pip:`, `npm:`, `go:`) for disambiguation
- Unprefixed entries match all ecosystems
- Comments (`#`) and blank lines ignored

**Detection**: Extracts package names from install commands, strips version specifiers, and compares case-insensitively against the deny list.

**Behavior**: Denies the Bash tool call and names the blocked packages. Logs to health buffer.

#### git_hygiene_enforcer.sh

**Event**: PreToolUse → `Bash`

Enforces safe git practices for push and commit commands.

**For `git push`:**
1. **Block force push**: `--force`, `-f`, `--force-with-lease` are denied
2. **Protect branches**: Direct push to `main`/`master` is blocked
3. **Bare push check**: `git push` without arguments checks current branch against protected list

**For `git commit`:**
1. **Conventional Commits**: Warns (non-blocking) if commit message doesn't match `type(scope): description`
   - Accepted types: `feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert`
2. **Secret scanning**: Scans staged diff for credential patterns:
   - API keys, access tokens, auth tokens
   - AWS access key IDs (`AKIA...`)
   - GitHub tokens (`ghp_...`, `ghs_...`, `github_pat_...`)
   - Private key material (`BEGIN PRIVATE KEY`)
   - Passwords in assignment patterns
   - Database connection strings (MongoDB, PostgreSQL, MySQL)
   - Azure storage keys (`AccountKey=...`, `SharedAccessKey=...`)

**Behavior**: Force push and secret leaks are **blocking** (deny). Conventional Commits violations are **non-blocking** (additionalContext warning).

#### pii_redactor.sh

**Event**: UserPromptSubmit (no matcher — fires on every prompt)

Scans user prompts for potential PII before text enters the model context.

**Detected patterns**:
- Email addresses
- Public IPv4 addresses (excludes private ranges: `10.x`, `192.168.x`, `172.16-31.x`, loopback)
- US phone numbers (various formats)
- Social Security Numbers (`XXX-XX-XXXX`)
- Credit card numbers (13-19 digits with optional separators)
- AWS access key IDs
- GitHub personal access tokens
- Private key material

**Behavior**: **Non-blocking** — outputs `additionalContext` warning to Claude. Does NOT erase or block the prompt, since the user may intentionally include PII for legitimate purposes (e.g., debugging). Logs detection count to the health buffer.

**Design note**: The roadmap spec called for sanitization (`<REDACTED>`), but UserPromptSubmit cannot modify the prompt text — it can only block or add context. Warning-only is the safer approach, avoiding false-positive prompt erasure.

### The Chronicle — Observability (§6.2)

#### system_health_emitter.sh

**Event**: PostToolUse → `.*` (all tools)

Flushes the shared health buffer and surfaces accumulated warnings to Claude via `additionalContext`.

**Design note**: Due to parallel execution, warnings from sibling PostToolUse hooks in the *same* event cycle may not yet be in the buffer. They appear on the next cycle (one-event lag — an acceptable trade-off).

#### memory_cross_pollinator.sh

**Event**: PostToolUse → `Write|Edit`

Automatically shares critical findings across skills via `memory/projects/{project}/cross_skill_insights.md`.

**Trigger**: Writes to `memory/skills/{skill}/{project}/{file}.md`

**Detection**: Scans written file for critical finding headers:
- `## Critical`
- `## Security`
- `## Breaking`
- `## Performance`

**Behavior**:
1. Extracts content blocks under each critical header
2. Creates/updates `memory/projects/{project}/cross_skill_insights.md`
3. Tags each entry with skill name and date
4. Deduplicates entries (same skill + date = replace)
5. Reports via `additionalContext` what was cross-pollinated

**Skips**: Operational files (`index.md`, `lifecycle.md`), paths with fewer than 3 components after `skills/`.

#### memory_pruning_daemon.sh

**Event**: SessionEnd (no matcher restriction — fires on all session ends)

Performs batch pruning of memory files after the session ends, enforcing the line-count limits from `lifecycle.md`.

**Line limits:**

| File | Limit |
|------|-------|
| `project_overview.md` | 200 lines |
| `review_history.md` | 300 lines |
| All other memory files | 500 lines |

**File detection:**
1. Scans session transcript for Write/Edit operations on `memory/` files
2. Also finds recently-modified files (last 2 hours) in `forge-plugin/memory/`
3. Skips operational files (`index.md`, `lifecycle.md`, `quality_guidance.md`, `cross_skill_insights.md`)
4. Skips files in `archive/` directories

**Pruning strategy**: When a file exceeds its limit:
1. Preserve the first 5 lines (header/metadata)
2. Insert a pruning marker with removal count and date
3. Keep the most recent content (tail) to fit the limit
4. Refresh the freshness timestamp

**Telemetry**: Logs pruning results to `.forge/telemetry.log` with session ID, files pruned, and total lines removed.

**Design note**: Runs at SessionEnd (after user interaction is complete) to avoid adding latency during active sessions. SessionEnd hooks cannot block termination — this is purely fire-and-forget cleanup.

### The Foreman — Quality Enforcement (§6.3)

#### memory_quality_gate.sh

**Event**: PostToolUse → `Write|Edit`

Validates memory files after they are written. **Supersedes `memory_sync.sh`**.

**Checks:**
1. **Timestamp**: Injects `<!-- Last Updated: YYYY-MM-DD -->` if missing, refreshes if stale
2. **Line limits**: Warns if file exceeds limits (500 general, 200 for `project_overview.md`, 300 for `review_history.md`)
3. **Specificity**: Flags vague language (heuristic check)
4. **Absolute paths**: Warns about `/home/`, `/Users/`, `C:\` paths

**Output**: `additionalContext` with quality feedback.

#### context_drift_detector.sh

**Event**: PostToolUse → `Write|Edit`

Detects when a project's actual dependencies conflict with the context domain tags loaded in the Forge.

**Trigger**: Writes to dependency files:
- `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`
- `go.mod`, `*.csproj`

**Detection**:
1. Extracts package names from the dependency file
2. Scans ALL context files' YAML frontmatter tags
3. Cross-references against `lib/framework_conflicts.json` conflict groups
4. Warns on two scenarios:
   - **Multi-framework conflict**: Project has two competing frameworks from the same group (e.g., both `flask` and `fastapi`)
   - **Stale context**: Context files are tagged for a framework the project doesn't use (e.g., `[django]` tags but project uses `fastapi`)

**Conflict groups** (from `lib/framework_conflicts.json`):
- Python web: `django` / `flask` / `fastapi`
- Python ML: `pytorch` / `tensorflow`
- JS frontend: `angular` / `react` / `vue`
- JS state: `ngrx` / `ngxs`
- JS testing: `jest` / `vitest` / `karma`
- .NET UI: `blazor` / `winforms` / `wpf`
- CSS: `tailwind` / `bootstrap`

**Output**: Health buffer warnings + `additionalContext`.

#### skill_compliance_checker.sh

**Event**: Stop (no matcher — fires on every stop)

Audits the session transcript for skill workflow compliance after Claude finishes responding.

**Detection**: Scans `transcript_path` (a common input field on all events) for:
- Skill invocations (reads of `skills/*/SKILL.md`)
- Step 2 compliance: memory loading from `memory/skills/{skill}/` or `memory/projects/`
- Step 3 compliance: context loading from `context/` domain files
- Step N-1 compliance: output to `/claudedocs/`
- Step N compliance: memory writes to `memory/skills/{skill}/`

**Behavior**: If violations are found, returns `decision: "block"` with `reason` listing which skills missed which steps. Claude is asked to complete missing steps before finishing.

**Safety**: Checks `stop_hook_active` to prevent infinite loops — skips when Claude is already continuing due to a Stop hook.

#### frontmatter_validator.sh

**Event**: PreToolUse → `Write|Edit`

Blocks writes to `context/` files that lack required YAML frontmatter.

**Required fields** (from `context_metadata.schema.json`):
- `id` — format: `{domain}/{filename}`
- `domain` — enum: `engineering|angular|azure|commands|dotnet|git|python|schema|security`
- `title` — human-readable name
- `type` — enum: `always|framework|reference|pattern|index|detection`
- `estimatedTokens` — integer
- `loadingStrategy` — enum: `always|onDemand|lazy`

**Skips**: `index.md`, `cross_domain.md`, `loading_protocol.md`.

#### command_chain_context.sh

**Event**: TaskCompleted (no matcher support — fires on every task completion)

Serializes the accumulated command execution context to `.forge/chain_state.json` when a task completes, enabling efficient command chaining.

**State captured:**
- Command name (detected from task subject against known forge commands)
- Context files loaded during the task (from transcript)
- Memory files read and written (from transcript)
- Skills invoked (from transcript)
- Output files generated (from transcript)
- Completion timestamp and task metadata

**Chain state structure** (`.forge/chain_state.json`):
```json
{
  "sessionId": "abc-123",
  "startedAt": "2026-02-11T10:00:00Z",
  "lastUpdated": "2026-02-11T10:15:00Z",
  "commandHistory": [
    {
      "command": "analyze",
      "completedAt": "...",
      "contextLoaded": ["context/python/patterns.md"],
      "memoryWritten": ["memory/skills/python-code-review/forge/insights.md"],
      "skillsInvoked": ["python-code-review"],
      "outputFiles": ["claudedocs/python-code-review_forge_2026-02-11.md"]
    }
  ]
}
```

**Session handling**: If the same session ID is already in `chain_state.json`, appends to the command history. Otherwise, starts a fresh chain.

**Design note**: Uses exit code 0 only — never blocks task completion. Chain state is advisory, enabling downstream commands to check for upstream results via the `ExecutionContext` interface.

#### agent_config_validator.sh

**Event**: SubagentStart (matcher: agent type name)

Validates a Forge agent's configuration against `agent_config.schema.json` when a subagent is spawned.

**Skips**: Built-in agent types (`Bash`, `Explore`, `Plan`) that don't have Forge configs.

**Validation checks (10 total):**
1. Config file is valid JSON
2. Required top-level fields present (`name`, `version`, `context`, `memory`, `skills`)
3. Config `name` matches filename
4. Version is valid semver (X.Y.Z)
5. Primary context domains are valid enum values
6. Secondary context domains are valid enum values
7. Always-load context files exist on disk
8. Memory storage path directory exists
9. Referenced skill directories and SKILL.md files exist
10. Agent personality `.md` file exists alongside config

**On success**: Injects a brief validation summary as `additionalContext` (skill count, domain count).

**On failure**: Injects all validation issues as `additionalContext`. SubagentStart cannot block subagent creation, so warnings are advisory.

**Model check**: If `model` is specified, validates it's one of: `opus`, `sonnet`, `haiku`.

### The Town Crier — Notifications (§6.4)

#### output_archival.sh

**Event**: PostToolUse → `Write|Edit`

Archives recent `/claudedocs/` output files:
- Copies to `/claudedocs/archive/{YYYY-MM}/`
- Maintains `manifest.md`
- Cleans archives older than 30 days

#### forge_telemetry.sh

**Event**: Stop (no matcher — fires on every stop)

Aggregates session-level metrics from the transcript and appends a structured entry to `.forge/telemetry.log`.

**Metrics collected:**
- Skills invoked (total + unique count)
- Memory reads and writes
- Context files loaded (total + unique)
- Tool calls by type (Bash, Write, Edit, Read, Glob, Grep, Task)
- Slash command invocations
- Output files generated
- Transcript size (lines and KB)

**Log format**: YAML entries separated by `---`, each timestamped with session ID.

**Maintenance**: Automatically caps `telemetry.log` at ~10,000 lines (~500 entries). Older entries are truncated.

**Behavior**: Purely observational — does NOT block the stop. Skips when `stop_hook_active=true` to prevent double-logging during stop-hook continuation. Logs a summary to the health buffer.

#### context_usage_tracker.sh

**Event**: PreCompact (matcher: `manual|auto` — fires on all compactions)

Analyzes the session transcript before context compaction to identify which context files were loaded but never referenced again ("unused"). Injects a usage report into the compacted context.

**Analysis heuristic:**
- A context file is "loaded" if `context/{file}.md` appears in the transcript
- A file is "active" if its basename appears more than once (loaded + subsequently referenced)
- A file is "unused" if it appears only once (loaded but never used)

**Report includes:**
- Total context files loaded
- Active vs. unused file breakdown with usage rate percentage
- Estimated wasted tokens (from frontmatter `estimatedTokens` metadata)
- List of unused files for loading-trigger refinement

**Output**: `additionalContext` injected into the compacted context. Also logs to `.forge/telemetry.log` and health buffer.

**Purpose**: Helps optimize `cross_domain.md` triggers by identifying false positives — context files that are loaded automatically but never actually used.

#### output_quality_scorer.sh

**Event**: PostToolUse → `Write|Edit`

Evaluates `/claudedocs/` output files against four quality criteria and appends a quality metadata block at the end of the file.

**Scoring criteria (100 points max):**

| Criterion | Points | Checks |
|-----------|--------|--------|
| Completeness | 30 | H1 title, H2 section structure (3+), summary/overview section, findings/results section |
| Actionability | 30 | Recommendations/next-steps section, actionable language density (should/must/consider/etc.) |
| Formatting | 25 | Code blocks, bullet/numbered lists, tables |
| Naming | 15 | Follows `OUTPUT_CONVENTIONS.md` pattern: `{skill}_{project}_{YYYY-MM-DD}.md` |

**Grades:** A (90%+), B (80%+), C (70%+), D (60%+), F (<60%)

**Output metadata** (appended to file):
```markdown
<!-- Quality Score (auto-generated by output_quality_scorer) -->
<!-- score: 85/100 (85%) grade: B -->
<!-- lines: 245 words: 1832 -->
<!-- scored: 2026-02-11 -->
```

**Behavior**: Non-blocking. Scores are informational for trend analysis. Logs grade to health buffer. Skips archive files and `manifest.md`.

## Utility Scripts

These are run on-demand and are located in `hooks/lib/` (not registered in `hooks.json`):

#### lib/context_freshness.sh

Audits context file health:
- Files without timestamps
- Files older than 6 months
- Orphaned files not referenced by any SKILL.md
- Tests first 20 HTTP links

**Usage**: `bash forge-plugin/hooks/lib/context_freshness.sh`

#### lib/session_context.sh

Displays project context at session start:
- Detects project from git remote or directory name
- Shows project profile if available
- Lists skill memory status

**Usage**: `bash forge-plugin/hooks/lib/session_context.sh [project-name]`

## Legacy Scripts

| Script | Replacement | Notes |
|--------|-------------|-------|
| `lib/memory_sync.sh` | `memory_quality_gate.sh` | All functionality absorbed (timestamping, line-count checks, logging). Additional quality checks added. Not recommended for use. |

## Creating Custom Hooks

### Template

```bash
#!/bin/bash
# hook_name.sh — Layer: Description
#
# Hook:    EventName (matcher: ToolPattern)
# Layer:   §6.X Layer Name
# Purpose: What this hook does
#
# Input:  JSON on stdin (Claude Code EventName format)
# Output: JSON with hookSpecificOutput or additionalContext

set -euo pipefail

# Source shared library if needed
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# Parse stdin
INPUT=$(cat)

# Extract relevant fields
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# Your logic here

# For PreToolUse deny:
# cat <<EOF
# {
#   "hookSpecificOutput": {
#     "hookEventName": "PreToolUse",
#     "permissionDecision": "deny",
#     "permissionDecisionReason": "Reason"
#   }
# }
# EOF

# For PostToolUse feedback:
# cat <<EOF
# {
#   "additionalContext": "Information for Claude"
# }
# EOF

exit 0
```

### Registration

Add your hook to `hooks.json`:

```json
{
  "matcher": "ToolNameRegex",
  "hooks": [
    {
      "type": "command",
      "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/your_hook.sh\""
    }
  ]
}
```

### Design Principles

1. **Fast** — Complete within 60 seconds (ideally < 5s)
2. **Idempotent** — Safe to run multiple times with same result
3. **Non-destructive** — Only touch memory, logs, reports — never source code
4. **Graceful failure** — Handle missing files, bad JSON, empty input
5. **Standard tools only** — bash, jq, grep, find, sed, wc, date, flock
6. **Use health buffer** — For warnings that should aggregate across hooks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook not running | Check `matcher` regex in `hooks.json` matches the tool name |
| Hook blocks unexpectedly | Check PreToolUse `permissionDecision` — only `deny` blocks |
| Hook output ignored | Ensure exit code is 0 and stdout is valid JSON |
| Permission denied | Run `chmod +x forge-plugin/hooks/*.sh` |
| Health buffer not flushing | Check `.forge/` directory exists and is writable |
| jq not found | Install jq — required dependency for all hooks |
| Hook killed (timeout) | Optimize or set `timeout_secs` in hooks.json handler |

---

*Last Updated: 2026-02-11*
