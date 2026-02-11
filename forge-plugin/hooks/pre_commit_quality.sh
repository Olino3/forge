#!/bin/bash
# pre_commit_quality.sh — The Shield: Pre-commit Quality Gate
#
# Hook:    PreToolUse (matcher: Bash)
# Layer:   §6.1 The Shield
# Purpose: Block git commit commands that would stage secrets or
#          violate quality conventions.
#
# Checks:
#   1. No .env, credentials.json, or secret files staged
#   2. No /claudedocs/ output files accidentally staged
#   3. Modified SKILL.md files have updated "Version History" section
#   4. Memory files don't contain absolute paths (should be relative)
#
# Input:  JSON on stdin (Claude Code PreToolUse format)
# Output: JSON with hookSpecificOutput.permissionDecision (deny if secrets found)

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

# Extract the command from tool_input
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Only run for git commit commands
if [[ -z "$COMMAND" ]] || { [[ "$COMMAND" != *"git commit"* ]] && [[ "$COMMAND" != *"git -c"*"commit"* ]]; }; then
    exit 0
fi

ISSUES=""
WARNINGS=""

# Check 1: No secret files staged
# Note: SECRET_PATTERNS uses grep -E regex matching. Patterns like "*.pem" are
# matched as regex suffix patterns (e.g., cert.pem, server.key) via the regex
# "(^|/)${pattern}$". The * is not a literal glob in this grep context.
SECRET_PATTERNS=(".env" "credentials.json" "secrets.json" ".env.local" "*.pem" "*.key" "id_rsa")
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")

for pattern in "${SECRET_PATTERNS[@]}"; do
    MATCHES=$(echo "$STAGED_FILES" | grep -E "(^|/)${pattern}$" 2>/dev/null || true)
    if [[ -n "$MATCHES" ]]; then
        ISSUES="${ISSUES}\n  BLOCKED: Secret file staged: $MATCHES"
        health_buffer_append "🛡️ Pre-commit quality: secret file staged: ${MATCHES}"
    fi
done

# Check 2: No /claudedocs/ output files staged
CLAUDEDOCS_FILES=$(echo "$STAGED_FILES" | grep -E "(^|/)claudedocs/" 2>/dev/null || true)
if [[ -n "$CLAUDEDOCS_FILES" ]]; then
    WARNINGS="${WARNINGS}\n  WARNING: /claudedocs/ files staged (usually should not be committed): $CLAUDEDOCS_FILES"
fi

# Check 3: Modified SKILL.md files should have Version History
SKILL_FILES=$(echo "$STAGED_FILES" | grep "SKILL.md" 2>/dev/null || true)
for skill_file in $SKILL_FILES; do
    [[ -z "$skill_file" ]] && continue
    if ! grep -q "Version History" "$skill_file" 2>/dev/null; then
        WARNINGS="${WARNINGS}\n  WARNING: $skill_file modified but has no Version History section"
    fi
done

# Check 4: Memory files should not contain absolute paths
MEMORY_FILES=$(echo "$STAGED_FILES" | grep "memory/" 2>/dev/null || true)
for mem_file in $MEMORY_FILES; do
    [[ -z "$mem_file" ]] && continue
    [[ ! -f "$mem_file" ]] && continue
    if grep -qE '/home/|/Users/|C:\\' "$mem_file" 2>/dev/null; then
        WARNINGS="${WARNINGS}\n  WARNING: $mem_file contains absolute paths (should be relative)"
    fi
done

# Output results
if [[ -n "$ISSUES" ]]; then
    FULL_MSG="Pre-commit quality gate BLOCKED:${ISSUES}"
    if [[ -n "$WARNINGS" ]]; then
        FULL_MSG="${FULL_MSG}\nAdditional warnings:${WARNINGS}"
    fi
    # Escape for JSON
    ESCAPED_MSG=$(echo -e "$FULL_MSG" | sed 's/"/\\"/g' | tr '\n' ' ')
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ ${ESCAPED_MSG}"
  }
}
EOF
    exit 0
fi

if [[ -n "$WARNINGS" ]]; then
    # Non-blocking warnings — surface as additionalContext
    ESCAPED_WARN=$(echo -e "Pre-commit warnings (non-blocking):${WARNINGS}" | sed 's/"/\\"/g' | tr '\n' ' ')
    cat <<EOF
{
  "additionalContext": "⚠️ ${ESCAPED_WARN}"
}
EOF
fi

exit 0
