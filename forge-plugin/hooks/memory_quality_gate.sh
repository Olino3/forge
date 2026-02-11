#!/bin/bash
# memory_quality_gate.sh — The Foreman: Memory Write Validator
#
# Hook:    PostToolUse (matcher: Write|Edit)
# Layer:   §6.3 The Foreman
# Purpose: Validate memory files after Write/Edit operations.
#          Supersedes the legacy memory_sync.sh with:
#            1. Timestamp injection/refresh (from memory_sync.sh)
#            2. Line-count limit enforcement (from lifecycle.md)
#            3. Quality checks (from quality_guidance.md)
#            4. Health buffer integration (new)
#
# Input:  JSON on stdin (Claude Code PostToolUse format)
# Output: JSON with additionalContext for Claude (quality feedback)

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

FORGE_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$FORGE_DIR/memory"
TODAY=$(date +%Y-%m-%d)

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

# Extract the file path from tool_input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# Exit early if not a memory file
[[ -z "$FILE_PATH" ]] && exit 0
[[ "$FILE_PATH" != *"memory/"* ]] && exit 0
[[ "$FILE_PATH" != *.md ]] && exit 0

# Skip operational files
BASENAME=$(basename "$FILE_PATH")
case "$BASENAME" in
    sync_log.md|index.md|lifecycle.md|quality_guidance.md)
        exit 0
        ;;
esac

# File must exist (it was just written/edited)
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

WARNINGS=""
CONTEXT_LINES=""

# --- Check 1: Freshness timestamp ----------------------------------------
FIRST_LINE=$(head -1 "$FILE_PATH" 2>/dev/null || echo "")
if [[ "$FIRST_LINE" != *"Last Updated:"* ]]; then
    # Inject timestamp as first line
    TEMP_FILE=$(mktemp)
    echo "<!-- Last Updated: $TODAY -->" > "$TEMP_FILE"
    cat "$FILE_PATH" >> "$TEMP_FILE"
    mv "$TEMP_FILE" "$FILE_PATH"
    CONTEXT_LINES="${CONTEXT_LINES}• Injected freshness timestamp into ${BASENAME}\n"
elif [[ "$FIRST_LINE" != *"$TODAY"* ]]; then
    # Update existing timestamp to today
    sed -i "1s/Last Updated: [0-9-]*/Last Updated: $TODAY/" "$FILE_PATH"
    CONTEXT_LINES="${CONTEXT_LINES}• Refreshed timestamp in ${BASENAME} to ${TODAY}\n"
fi

# --- Check 2: Line-count limits (from lifecycle.md) ----------------------
LINE_COUNT=$(wc -l < "$FILE_PATH" 2>/dev/null || echo "0")

# Determine limit based on filename
MAX_LINES=500  # default
case "$BASENAME" in
    project_overview.md) MAX_LINES=200 ;;
    review_history.md)   MAX_LINES=300 ;;
esac

if [[ "$LINE_COUNT" -gt "$MAX_LINES" ]]; then
    WARN="⚠️ Memory file ${FILE_PATH} exceeds ${MAX_LINES}-line limit (${LINE_COUNT} lines). Consider splitting or archiving per lifecycle.md."
    WARNINGS="${WARNINGS}${WARN}\n"
    health_buffer_append "$WARN"
fi

# --- Check 3: Specificity — no vague entries (heuristic) -----------------
# Count lines with vague phrasing (quick heuristic, not exhaustive)
VAGUE_COUNT=$(grep -ciE '(uses custom|has some|there are|various|multiple|several|certain)' "$FILE_PATH" 2>/dev/null || echo "0")
if [[ "$VAGUE_COUNT" -gt 3 ]]; then
    WARN="⚠️ Memory file ${BASENAME} has ${VAGUE_COUNT} potentially vague entries. Memory should reference specific files and paths (see quality_guidance.md)."
    WARNINGS="${WARNINGS}${WARN}\n"
    health_buffer_append "$WARN"
fi

# --- Check 4: Absolute paths (should be relative) -----------------------
ABS_PATH_COUNT=$(grep -cE '/home/|/Users/|C:\\' "$FILE_PATH" 2>/dev/null || echo "0")
if [[ "$ABS_PATH_COUNT" -gt 0 ]]; then
    WARN="⚠️ Memory file ${BASENAME} contains ${ABS_PATH_COUNT} absolute path(s). Use relative paths for portability."
    WARNINGS="${WARNINGS}${WARN}\n"
    health_buffer_append "$WARN"
fi

# --- Build response ------------------------------------------------------
if [[ -n "$WARNINGS" ]] || [[ -n "$CONTEXT_LINES" ]]; then
    FULL_CONTEXT="${CONTEXT_LINES}${WARNINGS}"
    # Escape for JSON
    ESCAPED=$(echo -e "$FULL_CONTEXT" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/ $//')
    cat <<EOF
{
  "additionalContext": "📋 Memory Quality Gate — ${BASENAME}: ${ESCAPED}"
}
EOF
fi

exit 0
