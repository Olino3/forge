# Forge Hooks Architecture

Claude Code hooks are shell commands that execute in response to tool events. They are configured in `.claude/settings.local.json` under the `hooks` key. This document defines the Forge hook system.

## Available Hook Points

| Hook Point | Trigger | Use Case |
|-----------|---------|----------|
| `PreToolUse` | Before a tool executes | Block operations, validate inputs |
| `PostToolUse` | After a tool executes | Process results, sync data |
| `Notification` | When Claude sends a notification | Alert routing, logging |
| `Stop` | When Claude stops responding | Cleanup, final reports |

## Forge Hook Catalog

| Hook | Type | Trigger | Purpose |
|------|------|---------|---------|
| `memory_sync` | PostToolUse | After Write/Edit to `memory/` | Timestamp and validate memory files |
| `pre_commit_quality` | PreToolUse | Before `git commit` | Block commits with secrets or `/claudedocs` files |
| `context_freshness` | Manual | On demand | Audit context file health and broken links |
| `output_archival` | PostToolUse | After Write to `/claudedocs` | Archive skill output with manifest |
| `session_context` | Manual | Start of work session | Summarize project state from memory |

## Hook Design Principles

1. **Fast**: Hooks must complete in < 5 seconds
2. **Idempotent**: Safe to run multiple times with same result
3. **Non-destructive**: Must not modify source code (only memory, logs, reports)
4. **Graceful failure**: Warnings, not hard errors. Never block the user unnecessarily
5. **Minimal dependencies**: Use only standard bash utilities (grep, find, wc, date)

## Configuration

To enable Forge hooks, add to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "bash forge-plugin/hooks/memory_sync.sh \"$TOOL_INPUT\""
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

## File Reference

| File | Description |
|------|-------------|
| `index.md` | This architecture document |
| `HOOKS_GUIDE.md` | Comprehensive usage guide |
| `memory_sync.sh` | Memory file validation and timestamping |
| `pre_commit_quality.sh` | Pre-commit quality gate |
| `context_freshness.sh` | Context health audit |
| `output_archival.sh` | Output file archival |
| `session_context.sh` | Session start context summary |

---

*Last Updated: 2026-02-10*
