# Forge Hooks Guide

Comprehensive guide for using, configuring, and creating Forge hooks.

## How Claude Code Hooks Work

Claude Code hooks are shell commands that execute automatically in response to tool events. They are configured in `.claude/settings.local.json` under the `hooks` key.

### Hook Points

| Hook Point | When It Runs | Receives |
|-----------|-------------|----------|
| `PreToolUse` | Before a tool executes | Tool name and input |
| `PostToolUse` | After a tool executes | Tool name, input, and output |
| `Notification` | When Claude sends a notification | Notification content |
| `Stop` | When Claude stops responding | Stop reason |

### Hook Behavior

- **PreToolUse**: Return exit code 1 to **block** the tool from executing. Return 0 to allow.
- **PostToolUse**: Exit code is informational only (does not block).
- Hooks receive tool context via environment variables or arguments.
- Hooks must complete within 5 seconds or they are killed.

## Enabling Forge Hooks

Add to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "bash forge-plugin/hooks/memory_sync.sh \"$TOOL_INPUT\""
      },
      {
        "matcher": "Write",
        "command": "bash forge-plugin/hooks/output_archival.sh"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "bash forge-plugin/hooks/pre_commit_quality.sh \"$TOOL_INPUT\""
      }
    ]
  }
}
```

## Available Hooks

### memory_sync.sh (PostToolUse)

**Purpose**: Validate and timestamp memory files after they are written.

**What it does**:
- Finds memory files modified in the last 5 minutes
- Adds `<!-- Last Updated: YYYY-MM-DD -->` timestamp if missing
- Warns if any file exceeds 500 lines
- Logs sync events to `memory/sync_log.md`

**Trigger**: After Write/Edit operations on files in `memory/`

### pre_commit_quality.sh (PreToolUse)

**Purpose**: Quality gate before git commits.

**What it does**:
- Blocks commits with staged secret files (.env, credentials.json, *.pem, *.key)
- Warns about staged `/claudedocs/` output files
- Checks that modified SKILL.md files have Version History sections
- Warns about absolute paths in memory files

**Trigger**: Before `git commit` commands. Returns exit code 1 to block if secrets detected.

### context_freshness.sh (Manual)

**Purpose**: Audit context file health.

**What it does**:
- Finds context files without "Last Updated" timestamps
- Flags files older than 6 months
- Identifies orphaned files not referenced by any SKILL.md
- Tests HTTP links for accessibility (first 20)
- Generates report to `/claudedocs/context_health_{date}.md`

**Usage**: `bash forge-plugin/hooks/context_freshness.sh`

### output_archival.sh (PostToolUse)

**Purpose**: Archive skill output files.

**What it does**:
- Copies recent output files to `/claudedocs/archive/{YYYY-MM}/`
- Maintains a manifest of archived files
- Cleans archives older than 30 days

**Trigger**: After Write operations to `/claudedocs/`

### session_context.sh (Manual)

**Purpose**: Display project context at session start.

**What it does**:
- Detects current project from git remote or directory name
- Displays shared project profile if available
- Lists all skill memories for the project with last-updated dates

**Usage**: `bash forge-plugin/hooks/session_context.sh [project-name]`

## Disabling Individual Hooks

Remove or comment out the specific hook entry in `.claude/settings.local.json`. The other hooks continue to operate independently.

## Creating Custom Hooks

### Template

```bash
#!/bin/bash
# [Description of what this hook does]
# Type: PreToolUse | PostToolUse | Manual
# Trigger: [What triggers this hook]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(dirname "$SCRIPT_DIR")"

# Your hook logic here

# For PreToolUse: exit 1 to block, exit 0 to allow
# For PostToolUse: exit code is informational only
exit 0
```

### Requirements

1. **Complete in < 5 seconds** - hooks that take too long are killed
2. **Use `set -euo pipefail`** - fail fast on errors
3. **Exit 0 by default** - only use exit 1 for PreToolUse blocking
4. **Don't modify source code** - only touch memory, logs, and reports
5. **Handle missing files gracefully** - not all projects have all directories
6. **Use standard tools only** - bash, grep, find, wc, date, curl

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook not running | Check `matcher` pattern in settings.local.json matches the tool name |
| Hook blocks unexpectedly | Check exit codes; only PreToolUse exit 1 blocks |
| Hook too slow | Profile with `time bash hook.sh`; optimize or increase timeout |
| Permission denied | Run `chmod +x forge-plugin/hooks/*.sh` |
| Hook errors in output | Check stderr; hooks should write errors to stderr |

---

*Last Updated: 2026-02-10*
