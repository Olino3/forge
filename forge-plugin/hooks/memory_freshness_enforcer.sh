#!/bin/bash
# memory_freshness_enforcer.sh — The Shield: Ghost Archive Guard
#
# Hook:    PreToolUse (matcher: Read)
# Layer:   §6.1 The Shield
# Purpose: Block reads of memory files that are stale (90+ days) by
#          denying the Read tool invocation with a reason explaining
#          the staleness. This forces Claude to refresh or archive the
#          memory before relying on it.
#
# Staleness thresholds (from lifecycle.md):
#   0-30 days  → Fresh    → allow
#   31-90 days → Aging    → allow (with health buffer warning)
#   90+ days   → Stale    → DENY the read
#
# Input:  JSON on stdin (Claude Code PreToolUse format)
# Output: JSON with hookSpecificOutput.permissionDecision

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

# Extract the file path from the tool input
# PreToolUse input has: tool_name, tool_input (with file_path)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# Exit early if we can't determine the path or it's not a memory file
[[ -z "$FILE_PATH" ]] && exit 0
[[ "$FILE_PATH" != *"memory/"* ]] && exit 0

# Skip non-markdown files (e.g. sync_log.md is operational, not content)
[[ "$FILE_PATH" != *.md ]] && exit 0

# Skip operational files that shouldn't be freshness-gated
BASENAME=$(basename "$FILE_PATH")
case "$BASENAME" in
    sync_log.md|index.md|lifecycle.md|quality_guidance.md)
        exit 0
        ;;
esac

# --- Check freshness -----------------------------------------------------
# File must exist
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Read the first line, expecting: <!-- Last Updated: YYYY-MM-DD -->
FIRST_LINE=$(head -1 "$FILE_PATH" 2>/dev/null || echo "")

# Extract the date
TIMESTAMP=$(echo "$FIRST_LINE" | grep -oP '(?<=Last Updated: )\d{4}-\d{2}-\d{2}' 2>/dev/null || echo "")

if [[ -z "$TIMESTAMP" ]]; then
    # No timestamp at all — treat as stale (deny)
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🏚️ Ghost Archive: Memory file '${FILE_PATH}' has no freshness timestamp. It may contain outdated information. Please add a '<!-- Last Updated: YYYY-MM-DD -->' header or archive this file to memory/archive/ before reading."
  }
}
EOF
    exit 0
fi

# Calculate age in days
TIMESTAMP_EPOCH=$(date -d "$TIMESTAMP" +%s 2>/dev/null || echo "0")
NOW_EPOCH=$(date +%s)
AGE_DAYS=$(( (NOW_EPOCH - TIMESTAMP_EPOCH) / 86400 ))

if [[ "$AGE_DAYS" -ge 90 ]]; then
    # Stale — deny the read
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🏚️ Ghost Archive: Memory file '${FILE_PATH}' is ${AGE_DAYS} days old (last updated: ${TIMESTAMP}). It exceeds the 90-day staleness threshold and may contain outdated information. Please verify its contents and update the timestamp, or archive it to memory/archive/ before relying on it."
  }
}
EOF
    exit 0
fi

if [[ "$AGE_DAYS" -ge 31 ]]; then
    # Aging — allow but record a warning in the health buffer
    health_buffer_append "⚠️ Aging memory (${AGE_DAYS}d old): ${FILE_PATH} — verify critical claims"
fi

# Fresh or aging — allow the read (no output = allow)
exit 0
