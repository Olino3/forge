#!/bin/bash
# context_usage_tracker.sh — The Town Crier: Context Usage Analyzer
#
# Hook:    PreCompact (matcher: manual|auto — fires on all compactions)
# Layer:   §6.4 The Town Crier
# Purpose: Before context compaction, analyze the session transcript
#          to identify which context files were loaded (Read from
#          context/) but never referenced in subsequent tool actions.
#          Logs usage stats to help refine cross_domain.md triggers
#          and optimize token spending.
#
#          Reports:
#            - Total context files loaded
#            - Files loaded but never referenced again ("unused")
#            - Files loaded and subsequently referenced ("active")
#            - Estimated wasted tokens (from frontmatter estimatedTokens)
#
# Input:  JSON on stdin (Claude Code PreCompact format)
# Output: JSON with additionalContext (summary injected into compacted context)
#
# Design: PreCompact is ideal because compaction is when token budget
#         matters most — knowing what was wasted helps the compactor
#         prioritize. Cannot block compaction (exit 2 only shows stderr
#         to user). Non-blocking by design.

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

FORGE_DIR="$(dirname "$SCRIPT_DIR")"
CONTEXT_DIR="$FORGE_DIR/context"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)
TRIGGER=$(echo "$INPUT" | jq -r '.trigger // "unknown"' 2>/dev/null)

# No transcript = nothing to analyze
[[ -z "$TRANSCRIPT_PATH" ]] && exit 0
[[ ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# --- Find all context files loaded during session ------------------------
# Look for Read operations on context/ files in the transcript
LOADED_FILES=$(grep -oE 'context/[a-z0-9_/-]+\.md' "$TRANSCRIPT_PATH" 2>/dev/null | sort -u) || true

[[ -z "$LOADED_FILES" ]] && exit 0

TOTAL_LOADED=0
ACTIVE_COUNT=0
UNUSED_COUNT=0
UNUSED_FILES=""
ACTIVE_FILES=""
ESTIMATED_WASTED_TOKENS=0

while IFS= read -r ctx_file; do
    [[ -z "$ctx_file" ]] && continue
    TOTAL_LOADED=$((TOTAL_LOADED + 1))

    BASENAME=$(basename "$ctx_file" .md)

    # A context file is "active" if its content influenced subsequent actions.
    # Heuristic: after the file was loaded, was its basename (minus .md),
    # or any of its frontmatter tags, referenced in tool_input or tool_response?
    #
    # We check if the basename appears more than once in the transcript
    # (once = the initial Read, more = actually used).
    OCCURRENCE_COUNT=$(grep -c "$BASENAME" "$TRANSCRIPT_PATH" 2>/dev/null) || true
    OCCURRENCE_COUNT=${OCCURRENCE_COUNT:-0}

    if [[ "$OCCURRENCE_COUNT" -gt 1 ]]; then
        ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
        ACTIVE_FILES="${ACTIVE_FILES}  ✅ ${ctx_file}\n"
    else
        UNUSED_COUNT=$((UNUSED_COUNT + 1))
        UNUSED_FILES="${UNUSED_FILES}  ❌ ${ctx_file}\n"

        # Try to read estimatedTokens from frontmatter
        FULL_PATH="$FORGE_DIR/$ctx_file"
        if [[ -f "$FULL_PATH" ]]; then
            EST_TOKENS=$(grep -m1 'estimatedTokens:' "$FULL_PATH" 2>/dev/null \
                | sed 's/.*estimatedTokens:[[:space:]]*//' \
                | tr -d '[:space:]' || echo "0")
            if [[ "$EST_TOKENS" =~ ^[0-9]+$ ]]; then
                ESTIMATED_WASTED_TOKENS=$((ESTIMATED_WASTED_TOKENS + EST_TOKENS))
            fi
        fi
    fi
done <<< "$LOADED_FILES"

# --- Calculate usage rate ------------------------------------------------
if [[ "$TOTAL_LOADED" -gt 0 ]]; then
    USAGE_RATE=$(( (ACTIVE_COUNT * 100) / TOTAL_LOADED ))
else
    USAGE_RATE=0
fi

# --- Log to telemetry ----------------------------------------------------
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
TELEMETRY_DIR="${CWD:-.}/.forge"
TELEMETRY_LOG="$TELEMETRY_DIR/telemetry.log"
mkdir -p "$TELEMETRY_DIR" 2>/dev/null || true

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat >> "$TELEMETRY_LOG" <<EOF
---
timestamp: $TIMESTAMP
event: context_usage_report
trigger: $TRIGGER
context_files:
  total_loaded: $TOTAL_LOADED
  active: $ACTIVE_COUNT
  unused: $UNUSED_COUNT
  usage_rate: ${USAGE_RATE}%
  estimated_wasted_tokens: $ESTIMATED_WASTED_TOKENS
EOF

# --- Health buffer -------------------------------------------------------
if [[ "$UNUSED_COUNT" -gt 0 ]]; then
    health_buffer_append "📖 Context usage: ${ACTIVE_COUNT}/${TOTAL_LOADED} files active (${USAGE_RATE}%), ~${ESTIMATED_WASTED_TOKENS} tokens wasted on ${UNUSED_COUNT} unused file(s)"
fi

# --- Build response ------------------------------------------------------
# Inject a summary into the compacted context so Claude can learn from it
SUMMARY="📖 Context Usage Report (${TRIGGER} compaction):\\n"
SUMMARY="${SUMMARY}• ${TOTAL_LOADED} context file(s) loaded during session\\n"
SUMMARY="${SUMMARY}• ${ACTIVE_COUNT} actively used (${USAGE_RATE}% utilization)\\n"
SUMMARY="${SUMMARY}• ${UNUSED_COUNT} loaded but never referenced (~${ESTIMATED_WASTED_TOKENS} tokens wasted)\\n"

if [[ -n "$UNUSED_FILES" ]]; then
    SUMMARY="${SUMMARY}\\nUnused context files (consider removing from loading triggers):\\n"
    SUMMARY="${SUMMARY}$(echo -e "$UNUSED_FILES" | sed 's/"/\\"/g' | tr '\n' ' ')"
fi

cat <<EOF
{
  "additionalContext": "${SUMMARY}"
}
EOF

exit 0
