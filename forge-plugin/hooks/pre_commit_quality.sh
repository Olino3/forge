#!/bin/bash
# Pre-commit hook: Quality gate before git commits
#
# Usage: bash pre_commit_quality.sh [command_string]
#
# Checks:
# 1. No .env, credentials.json, or secret files staged
# 2. No /claudedocs/ output files accidentally staged
# 3. Modified SKILL.md files have updated "Version History" section
# 4. Memory files don't contain absolute paths (should be relative)
#
# Returns exit code 1 to block commit if critical issues found

set -euo pipefail

# Only run for git commit commands
COMMAND="${1:-}"
if [[ "$COMMAND" != *"git commit"* ]] && [[ "$COMMAND" != *"git -c"*"commit"* ]]; then
    exit 0
fi

ISSUES=""
WARNINGS=""

# Check 1: No secret files staged
SECRET_PATTERNS=(".env" "credentials.json" "secrets.json" ".env.local" "*.pem" "*.key" "id_rsa")
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")

for pattern in "${SECRET_PATTERNS[@]}"; do
    MATCHES=$(echo "$STAGED_FILES" | grep -E "(^|/)${pattern}$" 2>/dev/null || true)
    if [[ -n "$MATCHES" ]]; then
        ISSUES="${ISSUES}\n  BLOCKED: Secret file staged: $MATCHES"
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
    echo -e "Pre-commit quality gate FAILED:$ISSUES" >&2
    if [[ -n "$WARNINGS" ]]; then
        echo -e "\nAdditional warnings:$WARNINGS" >&2
    fi
    exit 1
fi

if [[ -n "$WARNINGS" ]]; then
    echo -e "Pre-commit warnings (non-blocking):$WARNINGS" >&2
fi

exit 0
