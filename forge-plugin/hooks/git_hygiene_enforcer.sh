#!/bin/bash
# git_hygiene_enforcer.sh — The Shield: Source Control Safety Guard
#
# Hook:    PreToolUse (matcher: Bash)
# Layer:   §6.1 The Shield
# Purpose: Enforce safe git practices — prevent direct pushes to
#          protected branches, enforce Conventional Commits, and
#          scan staged diffs for leaked secrets.
#
# Trigger: Bash commands matching: git push, git commit
#
# Checks:
#   1. Block direct push to main/master/develop (configurable)
#   2. Enforce Conventional Commits format on commit messages
#   3. Scan staged diff for secret patterns (API keys, tokens, passwords)
#   4. Block force-push (--force, -f) to any branch
#
# Input:  JSON on stdin (Claude Code PreToolUse format)
# Output: JSON with hookSpecificOutput.permissionDecision (deny if violation)

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)

# Only process Bash commands
[[ "$TOOL_NAME" != "Bash" ]] && exit 0
[[ -z "$COMMAND" ]] && exit 0

# Only process git commands
echo "$COMMAND" | grep -qE '(^|\s|&&|\|)git\s+(push|commit)' || exit 0

# --- Protected branches --------------------------------------------------
PROTECTED_BRANCHES=("main" "master")

# --- Helper: deny with message -------------------------------------------
_deny() {
    local msg="$1"
    health_buffer_append "🛡️ Git hygiene: ${msg}"

    # Escape for JSON
    local escaped
    escaped=$(echo "$msg" | sed 's/"/\\"/g' | tr '\n' ' ')

    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ Git Hygiene Enforcer: ${escaped}"
  }
}
EOF
    exit 0
}

# --- Helper: warn (non-blocking) -----------------------------------------
_warn() {
    local msg="$1"
    health_buffer_append "⚠️ Git hygiene: ${msg}"
}

ISSUES=""
WARNINGS=""

# === Check: git push =====================================================
if echo "$COMMAND" | grep -qE '(^|\s|&&|\|)git\s+push'; then

    # Check 1: Force push
    if echo "$COMMAND" | grep -qE '\s+(-f|--force|--force-with-lease)\b'; then
        _deny "Force push detected. Force-pushing rewrites history and can destroy team members' work. Use regular push or create a new branch instead."
    fi

    # Check 2: Push to protected branch
    # Try to detect the target branch from the command
    # Patterns: git push origin main, git push origin HEAD:main
    for branch in "${PROTECTED_BRANCHES[@]}"; do
        if echo "$COMMAND" | grep -qE "(push\s+\S+\s+${branch}\b|push\s+\S+\s+\S+:${branch}\b|push\s+${branch}\b)"; then
            _deny "Direct push to protected branch '${branch}' is blocked. Create a feature branch and use a pull request instead."
        fi
    done

    # Check 3: Bare 'git push' — check current branch
    if echo "$COMMAND" | grep -qE '(^|\s|&&|\|)git\s+push\s*$'; then
        if [[ -n "$CWD" ]] && [[ -d "${CWD}/.git" ]]; then
            CURRENT_BRANCH=$(cd "$CWD" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
            for branch in "${PROTECTED_BRANCHES[@]}"; do
                if [[ "$CURRENT_BRANCH" == "$branch" ]]; then
                    _deny "Bare 'git push' while on protected branch '${branch}'. Switch to a feature branch or specify the remote and branch explicitly."
                fi
            done
        fi
    fi
fi

# === Check: git commit ===================================================
if echo "$COMMAND" | grep -qE '(^|\s|&&|\|)git\s+(commit|.+commit)'; then

    # Check 4: Conventional Commits format
    # Extract commit message from -m "..." or -m '...'
    COMMIT_MSG=""
    if echo "$COMMAND" | grep -qE '\s+-m\s'; then
        # Try double quotes first, then single quotes
        COMMIT_MSG=$(echo "$COMMAND" | sed -n 's/.*-m\s*"\([^"]*\)".*/\1/p' 2>/dev/null)
        if [[ -z "$COMMIT_MSG" ]]; then
            COMMIT_MSG=$(echo "$COMMAND" | sed -n "s/.*-m\s*'\([^']*\)'.*/\1/p" 2>/dev/null)
        fi
    fi

    if [[ -n "$COMMIT_MSG" ]]; then
        # Conventional Commits pattern: type(scope): description  or  type: description
        if ! echo "$COMMIT_MSG" | grep -qE '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?\s*(!)?:\s+.+'; then
            WARNINGS="${WARNINGS}\n  ⚠️ Commit message does not follow Conventional Commits format."
            WARNINGS="${WARNINGS}\n     Expected: type(scope): description"
            WARNINGS="${WARNINGS}\n     Types: feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"
            WARNINGS="${WARNINGS}\n     Got: '${COMMIT_MSG}'"
            _warn "Non-conventional commit message: '${COMMIT_MSG}'"
        fi
    fi

    # Check 5: Scan staged diff for secrets (only if in a git repo)
    if [[ -n "$CWD" ]] && [[ -d "${CWD}/.git" ]]; then
        STAGED_DIFF=$(cd "$CWD" && git diff --cached --no-color 2>/dev/null || echo "")

        if [[ -n "$STAGED_DIFF" ]]; then
            # Secret patterns to scan for in diffs
            SECRET_PATTERNS=(
                # API keys and tokens (generic)
                'api[_-]?key\s*[:=]\s*["\x27][A-Za-z0-9_\-]{20,}'
                'api[_-]?secret\s*[:=]\s*["\x27][A-Za-z0-9_\-]{20,}'
                'access[_-]?token\s*[:=]\s*["\x27][A-Za-z0-9_\-]{20,}'
                'auth[_-]?token\s*[:=]\s*["\x27][A-Za-z0-9_\-]{20,}'
                # AWS keys
                'AKIA[0-9A-Z]{16}'
                # GitHub tokens
                'gh[ps]_[A-Za-z0-9_]{36,}'
                'github_pat_[A-Za-z0-9_]{22,}'
                # Private keys
                'BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY'
                # Generic password assignments
                'password\s*[:=]\s*["\x27][^"\x27]{8,}'
                'passwd\s*[:=]\s*["\x27][^"\x27]{8,}'
                # Connection strings
                'mongodb(\+srv)?://[^\s]+'
                'postgres(ql)?://[^\s]+'
                'mysql://[^\s]+'
                # Azure / cloud keys
                'AccountKey=[A-Za-z0-9+/=]{40,}'
                'SharedAccessKey=[A-Za-z0-9+/=]{40,}'
            )

            FOUND_SECRETS=""
            for pattern in "${SECRET_PATTERNS[@]}"; do
                MATCHES=$(echo "$STAGED_DIFF" | grep -nEi "$pattern" 2>/dev/null | head -3 || true)
                if [[ -n "$MATCHES" ]]; then
                    FOUND_SECRETS="${FOUND_SECRETS}\n  Pattern: ${pattern}\n  ${MATCHES}\n"
                fi
            done

            if [[ -n "$FOUND_SECRETS" ]]; then
                ISSUES="Secrets detected in staged diff:${FOUND_SECRETS}"
                ISSUES="${ISSUES}\nRemove secrets from staged files before committing. Use environment variables or a secrets manager instead."
            fi
        fi
    fi
fi

# --- Output results ------------------------------------------------------
if [[ -n "$ISSUES" ]]; then
    _deny "$ISSUES"
fi

if [[ -n "$WARNINGS" ]]; then
    # Non-blocking warnings
    ESCAPED_WARN=$(echo -e "Git hygiene warnings (non-blocking):${WARNINGS}" | sed 's/"/\\"/g' | tr '\n' ' ')
    cat <<EOF
{
  "additionalContext": "⚠️ ${ESCAPED_WARN}"
}
EOF
fi

exit 0
