#!/bin/bash
# forge_telemetry.sh — The Town Crier: Session Telemetry Logger
#
# Hook:    Stop (no matcher — fires on every stop)
# Layer:   §6.4 The Town Crier
# Purpose: When Claude finishes responding, scan the session transcript
#          and aggregate key metrics:
#            - Total skills invoked
#            - Memory reads/writes performed
#            - Context files loaded
#            - Commands run (slash commands)
#            - Tool calls by type (Bash, Write, Edit, Read, etc.)
#            - Session duration (approximate)
#          Appends a structured log entry to .forge/telemetry.log
#
# Input:  JSON on stdin (Claude Code Stop format)
# Output: None (telemetry is logged, not surfaced to Claude)
#
# Design: Runs at Stop, not SessionEnd, because Stop fires within
#         the agentic loop and has transcript access. Does NOT block
#         the stop (purely observational). Skips when stop_hook_active=true.

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

FORGE_DIR="$(dirname "$SCRIPT_DIR")"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

# Guard: prevent double-logging during stop-hook continuation
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
    exit 0
fi

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)

# No transcript = nothing to measure
[[ -z "$TRANSCRIPT_PATH" ]] && exit 0
[[ ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# --- Resolve telemetry log path ------------------------------------------
TELEMETRY_DIR="${CWD:-.}/.forge"
TELEMETRY_LOG="$TELEMETRY_DIR/telemetry.log"
mkdir -p "$TELEMETRY_DIR" 2>/dev/null || true

# --- Gather metrics from transcript --------------------------------------
# Helper: safe grep count (grep exits 1 on no match, which kills set -e)
_grep_count() {
    local count
    count=$(grep -cE "$@" 2>/dev/null) || true
    echo "${count:-0}"
}

_grep_count_o() {
    local count
    count=$(grep -oE "$@" 2>/dev/null | sort -u | wc -l) || true
    echo "${count:-0}"
}

# Skills invoked (reads of SKILL.md files)
SKILLS_INVOKED=$(_grep_count 'skills/[a-z0-9_-]+/SKILL\.md' "$TRANSCRIPT_PATH")
UNIQUE_SKILLS=$(_grep_count_o 'skills/[a-z0-9_-]+/SKILL\.md' "$TRANSCRIPT_PATH")

# Memory operations
MEMORY_READS=$(_grep_count '(Read|read).*memory/' "$TRANSCRIPT_PATH")
MEMORY_WRITES=$(_grep_count '(Write|Edit|write|edit).*memory/' "$TRANSCRIPT_PATH")

# Context files loaded
CONTEXT_LOADS=$(_grep_count '(Read|read).*context/' "$TRANSCRIPT_PATH")
UNIQUE_CONTEXT=$(_grep_count_o 'context/[a-z0-9_/-]+\.md' "$TRANSCRIPT_PATH")

# Tool calls by type (count tool_name occurrences)
# Use a safe pattern: grep returns exit 1 on no match, so capture and default
_count_tool() {
    local tool="$1"
    local count
    count=$(grep -c "\"tool_name\".*\"${tool}\"" "$TRANSCRIPT_PATH" 2>/dev/null) || true
    echo "${count:-0}"
}

BASH_CALLS=$(_count_tool "Bash")
WRITE_CALLS=$(_count_tool "Write")
EDIT_CALLS=$(_count_tool "Edit")
READ_CALLS=$(_count_tool "Read")
GLOB_CALLS=$(_count_tool "Glob")
GREP_CALLS=$(_count_tool "Grep")
TASK_CALLS=$(_count_tool "Task")

TOTAL_TOOL_CALLS=$((BASH_CALLS + WRITE_CALLS + EDIT_CALLS + READ_CALLS + GLOB_CALLS + GREP_CALLS + TASK_CALLS))

# Slash commands (look for common forge commands)
COMMAND_INVOCATIONS=$(_grep_count '/(analyze|implement|test|improve|build|document|mock|brainstorm|remember|etl-pipeline|azure-function|azure-pipeline)' "$TRANSCRIPT_PATH")

# Output files generated
OUTPUT_FILES=$(_grep_count 'claudedocs/[a-zA-Z0-9_-]+\.md' "$TRANSCRIPT_PATH")

# Transcript size (rough proxy for session length)
TRANSCRIPT_LINES=$(wc -l < "$TRANSCRIPT_PATH" 2>/dev/null || echo "0")
TRANSCRIPT_BYTES=$(wc -c < "$TRANSCRIPT_PATH" 2>/dev/null || echo "0")
TRANSCRIPT_SIZE_KB=$((TRANSCRIPT_BYTES / 1024))

# --- Build telemetry entry -----------------------------------------------
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat >> "$TELEMETRY_LOG" <<EOF
---
timestamp: $TIMESTAMP
session_id: $SESSION_ID
transcript_lines: $TRANSCRIPT_LINES
transcript_size_kb: ${TRANSCRIPT_SIZE_KB}KB
skills:
  invocations: $SKILLS_INVOKED
  unique: $UNIQUE_SKILLS
memory:
  reads: $MEMORY_READS
  writes: $MEMORY_WRITES
context:
  loads: $CONTEXT_LOADS
  unique_files: $UNIQUE_CONTEXT
tools:
  total: $TOTAL_TOOL_CALLS
  bash: $BASH_CALLS
  write: $WRITE_CALLS
  edit: $EDIT_CALLS
  read: $READ_CALLS
  glob: $GLOB_CALLS
  grep: $GREP_CALLS
  task: $TASK_CALLS
commands: $COMMAND_INVOCATIONS
output_files: $OUTPUT_FILES
EOF

# --- Cap telemetry log size (keep last 500 entries) ----------------------
if [[ -f "$TELEMETRY_LOG" ]]; then
    LOG_LINES=$(wc -l < "$TELEMETRY_LOG" 2>/dev/null || echo "0")
    # Each entry is ~20 lines; 500 entries ≈ 10,000 lines
    if [[ "$LOG_LINES" -gt 10000 ]]; then
        TEMP_FILE=$(mktemp)
        tail -n 5000 "$TELEMETRY_LOG" > "$TEMP_FILE"
        mv "$TEMP_FILE" "$TELEMETRY_LOG"
    fi
fi

# --- Health buffer notification ------------------------------------------
health_buffer_append "📊 Telemetry: ${TOTAL_TOOL_CALLS} tool calls, ${UNIQUE_SKILLS} skill(s), ${MEMORY_WRITES} memory write(s), ${UNIQUE_CONTEXT} context file(s)"

exit 0
