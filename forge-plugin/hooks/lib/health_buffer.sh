#!/bin/bash
# Shared health buffer library for Forge hooks
#
# Provides append/flush helpers for the .forge/health_buffer file.
# Uses flock(1) for safe concurrent writes since Claude Code runs
# hooks on the same event in parallel.
#
# Usage:
#   source "${CLAUDE_PLUGIN_ROOT}/hooks/lib/health_buffer.sh"
#   health_buffer_append "⚠️ Memory file exceeds 500 lines: skills/foo/bar.md"
#   health_buffer_flush   # returns buffered lines and truncates the file

# --- Configuration -------------------------------------------------------

# Resolve the .forge runtime directory relative to the repo root.
# Priority:
#   1. FORGE_RUNTIME_DIR env var (allows test injection)
#   2. git rev-parse --show-toplevel (robust, works from any cwd)
#   3. CLAUDE_PLUGIN_ROOT-based derivation (legacy fallback)
#   4. Script location-based fallback
if [[ -n "${FORGE_RUNTIME_DIR:-}" ]] && [[ -d "${FORGE_RUNTIME_DIR}" ]]; then
    _FORGE_RUNTIME_DIR="$FORGE_RUNTIME_DIR"
elif _GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then
    _FORGE_RUNTIME_DIR="${_GIT_ROOT}/.forge"
elif [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
    # Legacy: CLAUDE_PLUGIN_ROOT is forge-plugin/, so ../../.forge
    _FORGE_RUNTIME_DIR="${CLAUDE_PLUGIN_ROOT}/../../.forge"
else
    # Fallback: derive from the script's own location (lib/ → hooks/ → forge-plugin/ → repo/)
    _LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    _FORGE_RUNTIME_DIR="$(cd "$_LIB_DIR/../../.." && pwd)/.forge"
fi

HEALTH_BUFFER_DIR="$_FORGE_RUNTIME_DIR"
HEALTH_BUFFER_FILE="$HEALTH_BUFFER_DIR/health_buffer"
HEALTH_BUFFER_LOCK="$HEALTH_BUFFER_DIR/health_buffer.lock"
HEALTH_BUFFER_MAX_LINES=200  # safety cap — prevent unbounded growth

# --- Helpers --------------------------------------------------------------

# Ensure the runtime directory and buffer file exist.
_health_buffer_init() {
    mkdir -p "$HEALTH_BUFFER_DIR"
    touch "$HEALTH_BUFFER_FILE"
    touch "$HEALTH_BUFFER_LOCK"
}

# Append a single warning/info line to the health buffer.
# Usage: health_buffer_append "message"
health_buffer_append() {
    local msg="${1:-}"
    [[ -z "$msg" ]] && return 0

    _health_buffer_init

    # Timestamp each entry for traceability
    local ts
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

    (
        flock -w 2 200 || return 0  # give up silently if lock unavailable
        local current_lines
        current_lines=$(wc -l < "$HEALTH_BUFFER_FILE" 2>/dev/null || echo "0")
        if [[ "$current_lines" -lt "$HEALTH_BUFFER_MAX_LINES" ]]; then
            echo "[$ts] $msg" >> "$HEALTH_BUFFER_FILE"
        fi
    ) 200>"$HEALTH_BUFFER_LOCK"
}

# Read and flush the health buffer. Prints all buffered lines to stdout
# and truncates the file. Returns 1 if the buffer was empty.
health_buffer_flush() {
    _health_buffer_init

    local content=""
    (
        flock -w 2 200 || return 1
        if [[ -s "$HEALTH_BUFFER_FILE" ]]; then
            cat "$HEALTH_BUFFER_FILE"
            : > "$HEALTH_BUFFER_FILE"   # truncate
        else
            return 1
        fi
    ) 200>"$HEALTH_BUFFER_LOCK"
}
