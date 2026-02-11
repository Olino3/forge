#!/bin/bash
# memory_pruning_daemon.sh — The Chronicle: Session-End Memory Pruning
#
# Hook:    SessionEnd (no matcher restriction — fires on all session ends)
# Layer:   §6.2 The Chronicle
# Purpose: After the session ends, identify memory files modified during
#          the session and enforce the line-count limits defined in
#          lifecycle.md. This is a zero-latency cleanup — it runs
#          *after* user interaction is complete, so it never slows
#          down the active session.
#
#          Line limits (from lifecycle.md):
#            - project_overview.md: 200 lines
#            - review_history.md:   300 lines
#            - All other memory:    500 lines
#
#          Pruning strategy: Keep the most recent content. When a file
#          exceeds its limit, preserve the first 5 lines (header/metadata)
#          and keep the last N lines to fit within the limit. Insert a
#          pruning marker indicating how many lines were removed.
#
# Input:  JSON on stdin (Claude Code SessionEnd format)
#           - reason: clear|logout|prompt_input_exit|bypass_permissions_disabled|other
# Output: None (cleanup runs silently — session is already over)
#
# Design: SessionEnd hooks cannot block session termination and have
#         no decision control. This hook is purely fire-and-forget.

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# Allow FORGE_DIR override for testing in temporary directories
FORGE_DIR="${FORGE_DIR:-$(dirname "$SCRIPT_DIR")}"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
REASON=$(echo "$INPUT" | jq -r '.reason // "other"' 2>/dev/null)

# --- Identify memory files modified during the session -------------------
# Strategy 1: Scan the transcript for Write/Edit operations on memory/ files
MODIFIED_FILES=""

if [[ -n "$TRANSCRIPT_PATH" ]] && [[ -f "$TRANSCRIPT_PATH" ]]; then
    MODIFIED_FILES=$(grep -oE 'memory/[a-z0-9_/-]+\.md' "$TRANSCRIPT_PATH" 2>/dev/null | sort -u) || true
fi

# Strategy 2: Also check recently-modified files in the memory directory
# (catches files modified by hooks themselves, e.g., memory_quality_gate)
MEMORY_DIR="$FORGE_DIR/memory"
if [[ -d "$MEMORY_DIR" ]]; then
    # Find .md files modified in the last 2 hours (generous session window)
    RECENT_FILES=$(find "$MEMORY_DIR" -name '*.md' -mmin -120 -type f 2>/dev/null) || true
    if [[ -n "$RECENT_FILES" ]]; then
        # Convert to relative paths and merge with transcript-detected files
        while IFS= read -r fullpath; do
            [[ -z "$fullpath" ]] && continue
            REL=$(echo "$fullpath" | sed "s|${FORGE_DIR}/||")
            MODIFIED_FILES="${MODIFIED_FILES}"$'\n'"${REL}"
        done <<< "$RECENT_FILES"
        MODIFIED_FILES=$(echo "$MODIFIED_FILES" | sort -u | grep -v '^$') || true
    fi
fi

# Nothing modified — nothing to prune
[[ -z "$MODIFIED_FILES" ]] && exit 0

# --- Skip operational files that shouldn't be pruned ---------------------
_should_skip() {
    local basename
    basename=$(basename "$1")
    case "$basename" in
        index.md|lifecycle.md|quality_guidance.md|sync_log.md|cross_skill_insights.md)
            return 0
            ;;
    esac
    # Skip archive files
    if echo "$1" | grep -q 'archive/' 2>/dev/null; then
        return 0
    fi
    return 1
}

# --- Determine line limit for a file ------------------------------------
_line_limit() {
    local basename
    basename=$(basename "$1")
    case "$basename" in
        project_overview.md) echo 200 ;;
        review_history.md)   echo 300 ;;
        *)                   echo 500 ;;
    esac
}

# --- Prune a single file ------------------------------------------------
_prune_file() {
    local filepath="$1"
    local max_lines="$2"

    [[ ! -f "$filepath" ]] && return 0

    local current_lines
    current_lines=$(wc -l < "$filepath" 2>/dev/null || echo "0")

    # No pruning needed
    [[ "$current_lines" -le "$max_lines" ]] && return 0

    local excess=$((current_lines - max_lines))
    local header_lines=5  # preserve first 5 lines (metadata/headers)
    local keep_tail=$((max_lines - header_lines - 3))  # 3 lines for pruning marker

    # Safety: if keep_tail is too small, just keep what we can
    [[ "$keep_tail" -lt 10 ]] && keep_tail=$((max_lines - 3))

    local temp_file
    temp_file=$(mktemp)
    local today
    today=$(date +%Y-%m-%d)

    # Write header
    head -n "$header_lines" "$filepath" > "$temp_file"

    # Insert pruning marker
    cat >> "$temp_file" <<MARKER

<!-- Pruned: ${excess} lines removed on ${today} by memory_pruning_daemon (limit: ${max_lines}) -->

MARKER

    # Write tail (most recent content)
    tail -n "$keep_tail" "$filepath" >> "$temp_file"

    mv "$temp_file" "$filepath"

    # Update the freshness timestamp if present
    if head -1 "$filepath" | grep -q 'Last Updated:' 2>/dev/null; then
        sed -i "1s/Last Updated: [0-9-]*/Last Updated: ${today}/" "$filepath"
    fi

    echo "$excess"
}

# --- Process each modified file ------------------------------------------
TOTAL_PRUNED=0
FILES_PRUNED=0
PRUNE_LOG=""

while IFS= read -r memfile; do
    [[ -z "$memfile" ]] && continue

    # Resolve full path
    FULL_PATH="${FORGE_DIR}/${memfile}"
    [[ ! -f "$FULL_PATH" ]] && continue

    # Skip operational files
    if _should_skip "$memfile"; then
        continue
    fi

    # Get limit and check
    LIMIT=$(_line_limit "$memfile")
    CURRENT=$(wc -l < "$FULL_PATH" 2>/dev/null || echo "0")

    if [[ "$CURRENT" -gt "$LIMIT" ]]; then
        LINES_REMOVED=$(_prune_file "$FULL_PATH" "$LIMIT")
        if [[ -n "$LINES_REMOVED" ]] && [[ "$LINES_REMOVED" -gt 0 ]]; then
            TOTAL_PRUNED=$((TOTAL_PRUNED + LINES_REMOVED))
            FILES_PRUNED=$((FILES_PRUNED + 1))
            PRUNE_LOG="${PRUNE_LOG}  - ${memfile}: ${LINES_REMOVED} lines pruned (limit: ${LIMIT})\n"
        fi
    fi
done <<< "$MODIFIED_FILES"

# --- Log results ---------------------------------------------------------
if [[ "$FILES_PRUNED" -gt 0 ]]; then
    health_buffer_append "🧹 Memory pruning: ${FILES_PRUNED} file(s) pruned, ${TOTAL_PRUNED} total lines removed"

    # Also log to telemetry
    TELEMETRY_DIR="${CWD:-.}/.forge"
    TELEMETRY_LOG="$TELEMETRY_DIR/telemetry.log"
    if [[ -d "$TELEMETRY_DIR" ]]; then
        TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        cat >> "$TELEMETRY_LOG" <<EOF
---
timestamp: $TIMESTAMP
session_id: $SESSION_ID
event: memory_pruning
reason: $REASON
files_pruned: $FILES_PRUNED
total_lines_removed: $TOTAL_PRUNED
$(echo -e "$PRUNE_LOG")
EOF
    fi
fi

exit 0
