#!/bin/bash
# command_chain_context.sh — The Foreman: Command Chain State Persistence
#
# Hook:    TaskCompleted (no matcher support — fires on every task completion)
# Layer:   §6.3 The Foreman
# Purpose: When a task (forge command) completes, serialize the accumulated
#          ExecutionContext state to .forge/chain_state.json so that
#          subsequent commands in the chain can inherit context, findings,
#          and decisions without redundant re-analysis.
#
#          Captures:
#            - Command name and completion status
#            - Loaded context files (detected from transcript)
#            - Memory files read/written (detected from transcript)
#            - Skills invoked (detected from transcript)
#            - Shared data keys (output files, findings)
#            - Timestamp for freshness
#
#          Subsequent commands check .forge/chain_state.json before
#          loading context or memory, enabling efficient chaining:
#            /analyze → /improve → /test
#
# Input:  JSON on stdin (Claude Code TaskCompleted format)
#           - task_id, task_subject, task_description (optional)
#           - teammate_name, team_name (optional)
# Output: Exit 0 silently on success. Does NOT block task completion.
#
# Design: Uses exit code 0 only — never exit 2 (which would block
#         task completion). Chain state is advisory, not mandatory.

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

TASK_ID=$(echo "$INPUT" | jq -r '.task_id // "unknown"' 2>/dev/null)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject // ""' 2>/dev/null)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)

# Need a working directory
[[ -z "$CWD" ]] && exit 0

# --- Detect forge command from task_subject ------------------------------
# Forge commands appear as /analyze, /implement, /test, etc. in task subjects
FORGE_COMMANDS="analyze|implement|test|improve|build|document|mock|brainstorm|remember|etl-pipeline|azure-function|azure-pipeline"

COMMAND_NAME=""
if echo "$TASK_SUBJECT" | grep -qEi "(${FORGE_COMMANDS})" 2>/dev/null; then
    COMMAND_NAME=$(echo "$TASK_SUBJECT" | grep -oEi "(${FORGE_COMMANDS})" 2>/dev/null | head -1 | tr '[:upper:]' '[:lower:]')
fi

# If we can't identify a forge command, still persist state but mark as generic
[[ -z "$COMMAND_NAME" ]] && COMMAND_NAME="task"

# --- Resolve chain state path --------------------------------------------
CHAIN_DIR="${CWD}/.forge"
CHAIN_STATE="$CHAIN_DIR/chain_state.json"
mkdir -p "$CHAIN_DIR" 2>/dev/null || true

# --- Helper: safe grep count under set -e --------------------------------
_gcount() {
    local count
    count=$(grep -cE "$@" 2>/dev/null) || true
    echo "${count:-0}"
}

# --- Gather context from transcript (if available) -----------------------
CONTEXT_FILES="[]"
MEMORY_READS="[]"
MEMORY_WRITES="[]"
SKILLS_INVOKED="[]"
OUTPUT_FILES="[]"

if [[ -n "$TRANSCRIPT_PATH" ]] && [[ -f "$TRANSCRIPT_PATH" ]]; then
    # Context files loaded (reads of context/*.md)
    CONTEXT_FILES_RAW=$(grep -oE 'context/[a-z0-9_/-]+\.md' "$TRANSCRIPT_PATH" 2>/dev/null | sort -u) || true
    if [[ -n "$CONTEXT_FILES_RAW" ]]; then
        CONTEXT_FILES=$(echo "$CONTEXT_FILES_RAW" | jq -R '.' | jq -s '.')
    fi

    # Memory files read
    MEMORY_READS_RAW=$(grep -oE 'memory/[a-z0-9_/-]+\.md' "$TRANSCRIPT_PATH" 2>/dev/null | sort -u) || true
    if [[ -n "$MEMORY_READS_RAW" ]]; then
        MEMORY_READS=$(echo "$MEMORY_READS_RAW" | jq -R '.' | jq -s '.')
    fi

    # Memory files written (Write/Edit operations on memory/)
    MEMORY_WRITES_RAW=$(grep -E '(Write|Edit).*memory/' "$TRANSCRIPT_PATH" 2>/dev/null | grep -oE 'memory/[a-z0-9_/-]+\.md' 2>/dev/null | sort -u) || true
    if [[ -n "$MEMORY_WRITES_RAW" ]]; then
        MEMORY_WRITES=$(echo "$MEMORY_WRITES_RAW" | jq -R '.' | jq -s '.')
    fi

    # Skills invoked
    SKILLS_RAW=$(grep -oE 'skills/[a-z0-9_-]+/SKILL\.md' "$TRANSCRIPT_PATH" 2>/dev/null | sed 's|skills/||;s|/SKILL\.md||' | sort -u) || true
    if [[ -n "$SKILLS_RAW" ]]; then
        SKILLS_INVOKED=$(echo "$SKILLS_RAW" | jq -R '.' | jq -s '.')
    fi

    # Output files generated
    OUTPUT_RAW=$(grep -oE 'claudedocs/[a-zA-Z0-9_.-]+\.md' "$TRANSCRIPT_PATH" 2>/dev/null | sort -u) || true
    if [[ -n "$OUTPUT_RAW" ]]; then
        OUTPUT_FILES=$(echo "$OUTPUT_RAW" | jq -R '.' | jq -s '.')
    fi
fi

# --- Build or update chain state -----------------------------------------
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# New command execution entry
NEW_ENTRY=$(jq -n \
    --arg cmd "$COMMAND_NAME" \
    --arg ts "$TIMESTAMP" \
    --arg status "success" \
    --arg task_id "$TASK_ID" \
    --arg task_subject "$TASK_SUBJECT" \
    --argjson context "$CONTEXT_FILES" \
    --argjson memory_reads "$MEMORY_READS" \
    --argjson memory_writes "$MEMORY_WRITES" \
    --argjson skills "$SKILLS_INVOKED" \
    --argjson outputs "$OUTPUT_FILES" \
    '{
        command: $cmd,
        completedAt: $ts,
        status: $status,
        taskId: $task_id,
        taskSubject: $task_subject,
        contextLoaded: $context,
        memoryRead: $memory_reads,
        memoryWritten: $memory_writes,
        skillsInvoked: $skills,
        outputFiles: $outputs
    }')

# Load existing chain state or create new one
if [[ -f "$CHAIN_STATE" ]] && jq empty "$CHAIN_STATE" 2>/dev/null; then
    # Existing chain — check if same session
    EXISTING_SESSION=$(jq -r '.sessionId // ""' "$CHAIN_STATE" 2>/dev/null)
    if [[ "$EXISTING_SESSION" == "$SESSION_ID" ]]; then
        # Same session — append to command history
        UPDATED=$(jq --argjson entry "$NEW_ENTRY" --arg ts "$TIMESTAMP" \
            '.lastUpdated = $ts | .commandHistory += [$entry]' "$CHAIN_STATE")
        echo "$UPDATED" > "$CHAIN_STATE"
    else
        # New session — start fresh
        jq -n \
            --arg sid "$SESSION_ID" \
            --arg ts "$TIMESTAMP" \
            --argjson entry "$NEW_ENTRY" \
            '{
                sessionId: $sid,
                startedAt: $ts,
                lastUpdated: $ts,
                commandHistory: [$entry]
            }' > "$CHAIN_STATE"
    fi
else
    # No existing chain state — create new
    jq -n \
        --arg sid "$SESSION_ID" \
        --arg ts "$TIMESTAMP" \
        --argjson entry "$NEW_ENTRY" \
        '{
            sessionId: $sid,
            startedAt: $ts,
            lastUpdated: $ts,
            commandHistory: [$entry]
        }' > "$CHAIN_STATE"
fi

# --- Log to health buffer ------------------------------------------------
CHAIN_LENGTH=$(jq '.commandHistory | length' "$CHAIN_STATE" 2>/dev/null || echo "1")
health_buffer_append "🔗 Command chain updated: '${COMMAND_NAME}' completed (${CHAIN_LENGTH} command(s) in chain)"

exit 0
