#!/bin/bash
# sandbox_boundary_guard.sh — The Shield: Host Isolation Guard
#
# Hook:    PreToolUse (matcher: Read|Write|Edit|Bash)
# Layer:   §6.1 The Shield
# Purpose: Block file operations targeting paths outside the project
#          directory. Prevents agents from reading or modifying system
#          configuration, SSH keys, or personal data.
#
# For Read/Write/Edit: checks file_path against project scope.
# For Bash: best-effort detection of known dangerous path patterns.
#
# Allowed exceptions:
#   - /tmp, /var/tmp (temporary operations)
#   - /dev/null, /dev/stdin, /dev/stdout, /dev/stderr
#   - Paths within the project directory (from cwd)
#
# Input:  JSON on stdin (Claude Code PreToolUse format)
# Output: JSON with hookSpecificOutput.permissionDecision (deny if violation)

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

FORGE_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT=$(cd "$FORGE_DIR/.." && pwd)

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)

# Use CWD from hook input, fall back to REPO_ROOT
PROJECT_ROOT="${CWD:-$REPO_ROOT}"

# --- Path allowlist check ------------------------------------------------
_is_path_allowed() {
    local path="$1"

    # Allow: anything within the project directory
    [[ "$path" == "${PROJECT_ROOT}"* ]] && return 0

    # Allow: /tmp (temporary operations)
    [[ "$path" == /tmp* ]] && return 0
    [[ "$path" == /var/tmp* ]] && return 0

    # Allow: /dev/null, /dev/stdin, /dev/stdout, /dev/stderr
    [[ "$path" == /dev/null ]] && return 0
    [[ "$path" == /dev/stdin ]] && return 0
    [[ "$path" == /dev/stdout ]] && return 0
    [[ "$path" == /dev/stderr ]] && return 0

    # Deny everything else
    return 1
}

# --- Sensitive filename patterns (secrets) --------------------------------
# These are blocked everywhere — even inside the project directory.
# Operations on these files risk leaking credentials into AI context.
SENSITIVE_FILE_PATTERNS=(
    '.env'
    '.env.*'          # .env.local, .env.production, etc.
    '*.pem'
    '*.key'
    '*.p12'
    '*.pfx'
    '*.jks'
    '*.keystore'
    '.npmrc'          # may contain auth tokens
    '.pypirc'         # PyPI credentials
    '.netrc'          # machine credentials
    '.htpasswd'
    'credentials'
    'credentials.json'
    'credentials.yaml'
    'credentials.yml'
    'service-account*.json'
    '*secret*'
    '.git-credentials'
)

_is_sensitive_file() {
    local filename
    filename=$(basename "$1")

    for pattern in "${SENSITIVE_FILE_PATTERNS[@]}"; do
        # Use bash pattern matching (case) for glob-style comparison
        # shellcheck disable=SC2254
        case "$filename" in
            $pattern) return 0 ;;
        esac
    done
    return 1
}

# --- File path checking (Read/Write/Edit) --------------------------------
_sandbox_check_file_path() {
    local FILE_PATH
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

    # No path = nothing to check
    [[ -z "$FILE_PATH" ]] && return 0

    # Resolve to absolute path for comparison
    if [[ "$FILE_PATH" != /* ]]; then
        FILE_PATH="${PROJECT_ROOT}/${FILE_PATH}"
    fi

    # Resolve symlinks and normalize (remove .., .)
    local RESOLVED_PATH
    RESOLVED_PATH=$(realpath -m "$FILE_PATH" 2>/dev/null || echo "$FILE_PATH")

    # Check: secrets/sensitive files (blocked even inside the project)
    if _is_sensitive_file "$RESOLVED_PATH"; then
        health_buffer_append "🛡️ Sandbox violation blocked: ${TOOL_NAME} → sensitive file '${RESOLVED_PATH}'"

        cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ Sandbox Boundary Guard: ${TOOL_NAME} operation targets '${RESOLVED_PATH}' which appears to contain secrets or credentials. Reading/writing secrets files is blocked to prevent credential leakage into AI context."
  }
}
EOF
        exit 0
    fi

    # Check: is the path within allowed scope?
    if _is_path_allowed "$RESOLVED_PATH"; then
        return 0
    fi

    # Blocked
    health_buffer_append "🛡️ Sandbox violation blocked: ${TOOL_NAME} → ${RESOLVED_PATH}"

    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ Sandbox Boundary Guard: ${TOOL_NAME} operation targets '${RESOLVED_PATH}' which is outside the project directory '${PROJECT_ROOT}'. File operations are restricted to the project scope for host isolation."
  }
}
EOF
    exit 0
}

# --- Bash command checking (best-effort dangerous pattern matching) ------
_sandbox_check_bash_command() {
    local COMMAND
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

    [[ -z "$COMMAND" ]] && return 0

    # Known dangerous path patterns (best-effort detection)
    local DANGEROUS_PATTERNS=(
        '~/.ssh'
        '~/.gnupg'
        '~/.config'
        '~/.bashrc'
        '~/.bash_profile'
        '~/.zshrc'
        '~/.profile'
        '~/.aws'
        '~/.kube'
        '~/.docker'
        '/etc/passwd'
        '/etc/shadow'
        '/etc/hosts'
        '/etc/sudoers'
        '$HOME/.ssh'
        '$HOME/.gnupg'
        '$HOME/.config'
        '$HOME/.aws'
    )

    # Sensitive file patterns in Bash commands (secrets leakage)
    local SENSITIVE_CMD_PATTERNS=(
        '.env'
        '.pem'
        '.key'
        '.p12'
        '.pfx'
        '.npmrc'
        '.pypirc'
        '.netrc'
        '.htpasswd'
        '.git-credentials'
        'credentials.json'
        'credentials.yaml'
        'service-account'
    )

    for pattern in "${SENSITIVE_CMD_PATTERNS[@]}"; do
        if [[ "$COMMAND" == *"$pattern"* ]]; then
            health_buffer_append "🛡️ Sandbox violation blocked (Bash): secrets file pattern '${pattern}' in command"

            cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ Sandbox Boundary Guard: Bash command references secrets file pattern '${pattern}'. Commands must not read or expose credentials, keys, or secrets files."
  }
}
EOF
            exit 0
        fi
    done

    for pattern in "${DANGEROUS_PATTERNS[@]}"; do
        if [[ "$COMMAND" == *"$pattern"* ]]; then
            health_buffer_append "🛡️ Sandbox violation blocked (Bash): dangerous path '${pattern}' in command"

            cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ Sandbox Boundary Guard: Bash command references sensitive path '${pattern}'. Commands must not access system configuration, SSH keys, or personal data outside the project scope."
  }
}
EOF
            exit 0
        fi
    done

    # Check for broad destructive commands
    if echo "$COMMAND" | grep -qE '^\s*rm\s+(-rf?|--recursive)\s+/\s*$'; then
        health_buffer_append "🛡️ Sandbox violation blocked (Bash): destructive 'rm -rf /' detected"

        cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ Sandbox Boundary Guard: Destructive command 'rm -rf /' detected. This would remove the entire filesystem."
  }
}
EOF
        exit 0
    fi

    # No dangerous patterns detected — allow
    return 0
}

# --- Main dispatch -------------------------------------------------------
case "$TOOL_NAME" in
    Read|Write|Edit)
        _sandbox_check_file_path
        ;;
    Bash)
        _sandbox_check_bash_command
        ;;
esac

exit 0
