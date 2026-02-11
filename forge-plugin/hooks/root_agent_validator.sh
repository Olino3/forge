#!/bin/bash
# root_agent_validator.sh — The Shield: Startup Integrity Check
#
# Hook:    SessionStart
# Layer:   §6.1 The Shield
# Purpose: Validate plugin structural integrity at session start.
#          Checks that required directories, files, and configurations
#          exist. Surfaces a summary to Claude via stdout (which Claude
#          Code adds to its context for SessionStart hooks).
#
# Uses:    forge-plugin/templates/root_safety_profile.json as the
#          default manifest of required structure. Projects can override
#          by placing a custom safety_profile.json in .forge/.
#
# Input:  JSON on stdin (Claude Code SessionStart format)
# Output: stdout text → added to Claude's context

set -euo pipefail

# --- Resolve paths -------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT=$(cd "$FORGE_DIR/.." && pwd)

# --- Load safety profile -------------------------------------------------
CUSTOM_PROFILE="${REPO_ROOT}/.forge/safety_profile.json"
DEFAULT_PROFILE="${FORGE_DIR}/templates/root_safety_profile.json"

if [[ -f "$CUSTOM_PROFILE" ]]; then
    PROFILE="$CUSTOM_PROFILE"
else
    PROFILE="$DEFAULT_PROFILE"
fi

if [[ ! -f "$PROFILE" ]]; then
    echo "⚠️ Forge: No safety profile found. Skipping startup validation."
    exit 0
fi

# --- Validate required directories ---------------------------------------
MISSING_DIRS=""
MISSING_FILES=""
WARNINGS=""

# Read required directories from profile
while IFS= read -r dir; do
    [[ -z "$dir" ]] && continue
    if [[ ! -d "${REPO_ROOT}/${dir}" ]]; then
        MISSING_DIRS="${MISSING_DIRS}\n  ✗ ${dir}"
    fi
done < <(jq -r '.requiredStructure.directories[]?' "$PROFILE" 2>/dev/null)

# Read required files from profile
while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    if [[ ! -f "${REPO_ROOT}/${file}" ]]; then
        MISSING_FILES="${MISSING_FILES}\n  ✗ ${file}"
    fi
done < <(jq -r '.requiredStructure.files[]?' "$PROFILE" 2>/dev/null)

# --- Check hooks.json exists and is valid JSON ---------------------------
HOOKS_JSON="${FORGE_DIR}/hooks/hooks.json"
if [[ -f "$HOOKS_JSON" ]]; then
    if ! jq empty "$HOOKS_JSON" 2>/dev/null; then
        WARNINGS="${WARNINGS}\n  ⚠️ hooks/hooks.json is not valid JSON"
    fi
else
    MISSING_FILES="${MISSING_FILES}\n  ✗ forge-plugin/hooks/hooks.json"
fi

# --- Check agent configs have matching .md files -------------------------
AGENT_ISSUES=""
for config in "${FORGE_DIR}"/agents/*.config.json; do
    [[ ! -f "$config" ]] && continue
    AGENT_NAME=$(jq -r '.name // empty' "$config" 2>/dev/null)
    [[ -z "$AGENT_NAME" ]] && continue
    MD_FILE="${FORGE_DIR}/agents/${AGENT_NAME}.md"
    if [[ ! -f "$MD_FILE" ]]; then
        AGENT_ISSUES="${AGENT_ISSUES}\n  ⚠️ Agent config '${AGENT_NAME}.config.json' has no matching '${AGENT_NAME}.md'"
    fi
done

# --- Ensure .forge runtime directory exists ------------------------------
RUNTIME_DIR="${REPO_ROOT}/.forge"
if [[ ! -d "$RUNTIME_DIR" ]]; then
    mkdir -p "$RUNTIME_DIR"
    WARNINGS="${WARNINGS}\n  ℹ️ Created .forge/ runtime directory"
fi

# --- Build session context output ----------------------------------------
PROFILE_VERSION=$(jq -r '.version // "unknown"' "$PROFILE" 2>/dev/null)

echo "⚒️ Forge Session Start — Safety Profile v${PROFILE_VERSION}"
echo ""

HAS_ISSUES=false

if [[ -n "$MISSING_DIRS" ]]; then
    HAS_ISSUES=true
    echo -e "Missing directories:${MISSING_DIRS}"
    echo ""
fi

if [[ -n "$MISSING_FILES" ]]; then
    HAS_ISSUES=true
    echo -e "Missing files:${MISSING_FILES}"
    echo ""
fi

if [[ -n "$AGENT_ISSUES" ]]; then
    HAS_ISSUES=true
    echo -e "Agent integrity issues:${AGENT_ISSUES}"
    echo ""
fi

if [[ -n "$WARNINGS" ]]; then
    echo -e "Warnings:${WARNINGS}"
    echo ""
fi

if [[ "$HAS_ISSUES" == "false" ]]; then
    echo "✅ All structural checks passed."
fi

# Count components for context
AGENT_COUNT=$(find "${FORGE_DIR}/agents" -name "*.md" -type f 2>/dev/null | wc -l)
SKILL_COUNT=$(find "${FORGE_DIR}/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
COMMAND_COUNT=$(find "${FORGE_DIR}/commands" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
HOOK_COUNT=$(find "${FORGE_DIR}/hooks" -name "*.sh" -type f 2>/dev/null | wc -l)

echo "Components: ${AGENT_COUNT} agents, ${SKILL_COUNT} skills, ${COMMAND_COUNT} commands, ${HOOK_COUNT} hooks"

exit 0
