#!/bin/bash
# Post-skill hook: Validate and timestamp memory files
# Triggered after Write/Edit operations on memory/ directory
#
# Usage: bash memory_sync.sh [file_path]
#
# Behavior:
# 1. Find memory files modified in last 5 minutes
# 2. Ensure each has "Last Updated: YYYY-MM-DD" comment on first line
# 3. Warn if any file exceeds 500 lines
# 4. Log sync event to memory/sync_log.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$FORGE_DIR/memory"
SYNC_LOG="$MEMORY_DIR/sync_log.md"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +%Y-%m-%dT%H:%M:%S)
MAX_LINES=500

# Only run if the modified file is in the memory directory
if [[ -n "${1:-}" ]] && [[ "$1" != *"memory/"* ]]; then
    exit 0
fi

# Find memory .md files modified in the last 5 minutes
MODIFIED_FILES=$(find "$MEMORY_DIR" -name "*.md" -mmin -5 -not -name "sync_log.md" 2>/dev/null || true)

if [[ -z "$MODIFIED_FILES" ]]; then
    exit 0
fi

WARNINGS=""

while IFS= read -r file; do
    [[ -z "$file" ]] && continue

    # Check for freshness timestamp on first line
    FIRST_LINE=$(head -1 "$file" 2>/dev/null || echo "")
    if [[ "$FIRST_LINE" != *"Last Updated:"* ]]; then
        # Add timestamp as first line
        TEMP_FILE=$(mktemp)
        echo "<!-- Last Updated: $TODAY -->" > "$TEMP_FILE"
        cat "$file" >> "$TEMP_FILE"
        mv "$TEMP_FILE" "$file"
    fi

    # Check line count
    LINE_COUNT=$(wc -l < "$file" 2>/dev/null || echo "0")
    if [[ "$LINE_COUNT" -gt "$MAX_LINES" ]]; then
        WARNINGS="${WARNINGS}\n- WARNING: $file exceeds ${MAX_LINES} lines (${LINE_COUNT} lines). Consider splitting or archiving."
    fi

done <<< "$MODIFIED_FILES"

# Log sync event
FILE_COUNT=$(echo "$MODIFIED_FILES" | grep -c '.' || echo "0")
{
    echo "- [$NOW] Synced $FILE_COUNT memory file(s)${WARNINGS:+ | Issues: $WARNINGS}"
} >> "$SYNC_LOG" 2>/dev/null || true

# Output warnings to stderr (visible to user)
if [[ -n "$WARNINGS" ]]; then
    echo -e "Memory sync warnings:$WARNINGS" >&2
fi

exit 0
