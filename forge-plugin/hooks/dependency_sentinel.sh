#!/bin/bash
# dependency_sentinel.sh — The Shield: Supply Chain Security Guard
#
# Hook:    PreToolUse (matcher: Bash)
# Layer:   §6.1 The Shield
# Purpose: Block package install commands that reference known-bad
#          packages from the deny list. Prevents AI agents from
#          hallucinating typosquatted or malicious dependencies.
#
# Trigger: Bash commands matching: pip install, npm install, yarn add,
#          go get, dotnet add package
#
# Deny list: forge-plugin/security/deny_list.txt
#   - Supports ecosystem prefixes (pip:, npm:, go:)
#   - Unprefixed entries match all ecosystems
#   - Comments (#) and blank lines ignored
#
# Input:  JSON on stdin (Claude Code PreToolUse format)
# Output: JSON with hookSpecificOutput.permissionDecision (deny if match)

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

FORGE_DIR="$(dirname "$SCRIPT_DIR")"
DENY_LIST="${FORGE_DIR}/security/deny_list.txt"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Only process Bash commands
[[ "$TOOL_NAME" != "Bash" ]] && exit 0
[[ -z "$COMMAND" ]] && exit 0

# --- Detect package install commands -------------------------------------
# Returns the ecosystem and package names from the command
_detect_install() {
    local cmd="$1"
    local ecosystem=""
    local packages=""

    # pip install (including pip3, python -m pip)
    if echo "$cmd" | grep -qE '(^|\s|&&|\|)(pip3?|python3?\s+-m\s+pip)\s+install\s'; then
        ecosystem="pip"
        # Extract package names: everything after 'install' that isn't a flag
        packages=$(echo "$cmd" | sed -n 's/.*install\s\+//p' | tr ' ' '\n' | grep -vE '^-' | sed 's/[>=<\[].*//;s/\s*$//' | grep -v '^$')
    # npm install / npm i / npm add
    elif echo "$cmd" | grep -qE '(^|\s|&&|\|)npm\s+(install|i|add)\s'; then
        ecosystem="npm"
        packages=$(echo "$cmd" | sed -n 's/.*\(install\|add\|i\)\s\+//p' | tr ' ' '\n' | grep -vE '^-' | sed 's/@.*//;s/\s*$//' | grep -v '^$')
    # yarn add
    elif echo "$cmd" | grep -qE '(^|\s|&&|\|)yarn\s+add\s'; then
        ecosystem="npm"
        packages=$(echo "$cmd" | sed -n 's/.*add\s\+//p' | tr ' ' '\n' | grep -vE '^-' | sed 's/@.*//;s/\s*$//' | grep -v '^$')
    # go get
    elif echo "$cmd" | grep -qE '(^|\s|&&|\|)go\s+get\s'; then
        ecosystem="go"
        packages=$(echo "$cmd" | sed -n 's/.*get\s\+//p' | tr ' ' '\n' | grep -vE '^-' | sed 's/@.*//;s/\s*$//' | grep -v '^$')
    # dotnet add package
    elif echo "$cmd" | grep -qE '(^|\s|&&|\|)dotnet\s+add\s.*\s+package\s'; then
        ecosystem="nuget"
        packages=$(echo "$cmd" | sed -n 's/.*package\s\+//p' | tr ' ' '\n' | grep -vE '^-' | head -1 | sed 's/\s*$//')
    fi

    # No install command detected
    [[ -z "$ecosystem" ]] && return 1

    echo "$ecosystem"
    echo "$packages"
    return 0
}

# --- Load deny list ------------------------------------------------------
_load_deny_list() {
    local ecosystem="$1"

    [[ ! -f "$DENY_LIST" ]] && return 0

    # Read deny list, strip comments and blanks, filter by ecosystem
    while IFS= read -r line; do
        # Skip comments and blanks
        [[ -z "$line" ]] && continue
        [[ "$line" == \#* ]] && continue

        # Strip inline comments
        line="${line%%#*}"
        line="${line%% *}"
        [[ -z "$line" ]] && continue

        # Check ecosystem prefix
        if [[ "$line" == *:* ]]; then
            local prefix="${line%%:*}"
            local pkg="${line#*:}"
            # Only match if ecosystem matches
            [[ "$prefix" == "$ecosystem" ]] && echo "$pkg"
        else
            # Unprefixed = matches all ecosystems
            echo "$line"
        fi
    done < "$DENY_LIST"
}

# --- Main check ----------------------------------------------------------
INSTALL_OUTPUT=$(_detect_install "$COMMAND" 2>/dev/null) || exit 0

ECOSYSTEM=$(echo "$INSTALL_OUTPUT" | head -1)
PACKAGES=$(echo "$INSTALL_OUTPUT" | tail -n +2)

[[ -z "$PACKAGES" ]] && exit 0

# Load denied packages for this ecosystem
DENIED=$(_load_deny_list "$ECOSYSTEM" 2>/dev/null || true)
[[ -z "$DENIED" ]] && exit 0

# Check each package against the deny list
BLOCKED=""
while IFS= read -r pkg; do
    [[ -z "$pkg" ]] && continue
    # Case-insensitive match
    pkg_lower=$(echo "$pkg" | tr '[:upper:]' '[:lower:]')
    while IFS= read -r denied_pkg; do
        [[ -z "$denied_pkg" ]] && continue
        denied_lower=$(echo "$denied_pkg" | tr '[:upper:]' '[:lower:]')
        if [[ "$pkg_lower" == "$denied_lower" ]]; then
            BLOCKED="${BLOCKED}${pkg}, "
        fi
    done <<< "$DENIED"
done <<< "$PACKAGES"

# No matches = allow
[[ -z "$BLOCKED" ]] && exit 0

# Remove trailing comma
BLOCKED="${BLOCKED%, }"

health_buffer_append "🛡️ Dependency sentinel blocked: ${ECOSYSTEM} packages [${BLOCKED}] on deny list"

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🛡️ Dependency Sentinel: Blocked installation of [${BLOCKED}] — these packages are on the security deny list (forge-plugin/security/deny_list.txt). They may be typosquatted, malicious, or have critical unpatched vulnerabilities. Verify the correct package name and update the deny list if this is a false positive."
  }
}
EOF
exit 0
