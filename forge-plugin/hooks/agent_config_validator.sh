#!/bin/bash
# agent_config_validator.sh — The Foreman: Agent Configuration Integrity
#
# Hook:    SubagentStart (matcher: agent type name)
# Layer:   §6.3 The Foreman
# Purpose: When a subagent is spawned, validate its configuration
#          against the agent_config.schema.json. Checks:
#            1. Config file exists for the agent
#            2. Config has required fields (name, version, context, memory, skills)
#            3. Context domains are valid enum values
#            4. Memory storage path exists
#            5. Referenced skill directories exist
#            6. Agent .md file exists alongside config
#
#          If validation fails, injects warnings as additionalContext
#          (SubagentStart cannot block subagent creation).
#
# Input:  JSON on stdin (Claude Code SubagentStart format)
#           - agent_id, agent_type
# Output: JSON with additionalContext on validation failures

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

FORGE_DIR="$(dirname "$SCRIPT_DIR")"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // empty' 2>/dev/null)
AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id // empty' 2>/dev/null)

# Exit early if no agent type
[[ -z "$AGENT_TYPE" ]] && exit 0

# --- Check if this is a Forge agent (has a config.json) ------------------
# Built-in agent types: Bash, Explore, Plan — skip those
case "$AGENT_TYPE" in
    Bash|Explore|Plan|bash|explore|plan)
        exit 0
        ;;
esac

# Convert agent type to kebab-case for file lookup
# Agent types may come as "python-engineer", "PythonEngineer", etc.
AGENT_NAME=$(echo "$AGENT_TYPE" | sed 's/\([A-Z]\)/-\L\1/g' | sed 's/^-//' | tr '[:upper:]' '[:lower:]')

CONFIG_FILE="${FORGE_DIR}/agents/${AGENT_NAME}.config.json"
MD_FILE="${FORGE_DIR}/agents/${AGENT_NAME}.md"

# If no config file exists, this might not be a Forge agent — skip silently
[[ ! -f "$CONFIG_FILE" ]] && exit 0

# --- Validate the config -------------------------------------------------
ISSUES=""
ISSUE_COUNT=0

# Check 1: Valid JSON
if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
    ISSUES="${ISSUES}  ✗ Config file is not valid JSON\n"
    ISSUE_COUNT=$((ISSUE_COUNT + 1))
    # Can't continue validation if JSON is broken
    health_buffer_append "⚠️ Agent '${AGENT_NAME}' config is invalid JSON"
    ESCAPED=$(echo -e "$ISSUES" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/ $//')
    cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "SubagentStart",
        "additionalContext": "⚠️ Agent Config Validator — '${AGENT_NAME}': ${ESCAPED}"
    }
}
EOF
    exit 0
fi

# Check 2: Required top-level fields
for field in name version context memory skills; do
    VALUE=$(jq -r ".${field} // empty" "$CONFIG_FILE" 2>/dev/null)
    if [[ -z "$VALUE" ]] || [[ "$VALUE" == "null" ]]; then
        ISSUES="${ISSUES}  ✗ Missing required field: '${field}'\n"
        ISSUE_COUNT=$((ISSUE_COUNT + 1))
    fi
done

# Check 3: Name matches filename
CONFIG_NAME=$(jq -r '.name // empty' "$CONFIG_FILE" 2>/dev/null)
if [[ -n "$CONFIG_NAME" ]] && [[ "$CONFIG_NAME" != "$AGENT_NAME" ]]; then
    ISSUES="${ISSUES}  ✗ Config name '${CONFIG_NAME}' does not match filename '${AGENT_NAME}'\n"
    ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 4: Version is valid semver
VERSION=$(jq -r '.version // empty' "$CONFIG_FILE" 2>/dev/null)
if [[ -n "$VERSION" ]] && ! echo "$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
    ISSUES="${ISSUES}  ✗ Version '${VERSION}' is not valid semver (expected X.Y.Z)\n"
    ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 5: Context domains are valid
VALID_DOMAINS="engineering angular azure commands dotnet git python schema security"
if jq -e '.context.primaryDomains' "$CONFIG_FILE" > /dev/null 2>&1; then
    while IFS= read -r domain; do
        [[ -z "$domain" ]] && continue
        if ! echo "$VALID_DOMAINS" | grep -qw "$domain"; then
            ISSUES="${ISSUES}  ✗ Invalid primary context domain: '${domain}'\n"
            ISSUE_COUNT=$((ISSUE_COUNT + 1))
        fi
    done < <(jq -r '.context.primaryDomains[]?' "$CONFIG_FILE" 2>/dev/null)
fi

if jq -e '.context.secondaryDomains' "$CONFIG_FILE" > /dev/null 2>&1; then
    while IFS= read -r domain; do
        [[ -z "$domain" ]] && continue
        if ! echo "$VALID_DOMAINS" | grep -qw "$domain"; then
            ISSUES="${ISSUES}  ✗ Invalid secondary context domain: '${domain}'\n"
            ISSUE_COUNT=$((ISSUE_COUNT + 1))
        fi
    done < <(jq -r '.context.secondaryDomains[]?' "$CONFIG_FILE" 2>/dev/null)
fi

# Check 6: Always-load context files exist
if jq -e '.context.alwaysLoadFiles' "$CONFIG_FILE" > /dev/null 2>&1; then
    while IFS= read -r ctxfile; do
        [[ -z "$ctxfile" ]] && continue
        FULL_PATH="${FORGE_DIR}/context/${ctxfile}"
        if [[ ! -f "$FULL_PATH" ]]; then
            ISSUES="${ISSUES}  ✗ Always-load context file not found: '${ctxfile}'\n"
            ISSUE_COUNT=$((ISSUE_COUNT + 1))
        fi
    done < <(jq -r '.context.alwaysLoadFiles[]?' "$CONFIG_FILE" 2>/dev/null)
fi

# Check 7: Memory storage path exists
# storagePath in configs is relative to the repo root (e.g., "forge-plugin/memory/agents/...")
MEMORY_PATH=$(jq -r '.memory.storagePath // empty' "$CONFIG_FILE" 2>/dev/null)
REPO_ROOT="$(dirname "$FORGE_DIR")"
if [[ -n "$MEMORY_PATH" ]]; then
    FULL_MEMORY="${REPO_ROOT}/${MEMORY_PATH}"
    if [[ ! -d "$FULL_MEMORY" ]]; then
        ISSUES="${ISSUES}  ✗ Memory storage path does not exist: '${MEMORY_PATH}'\n"
        ISSUE_COUNT=$((ISSUE_COUNT + 1))
    fi
fi

# Check 8: Referenced skills exist
if jq -e '.skills' "$CONFIG_FILE" > /dev/null 2>&1; then
    while IFS= read -r skill; do
        [[ -z "$skill" ]] && continue
        SKILL_DIR="${FORGE_DIR}/skills/${skill}"
        SKILL_MD="${SKILL_DIR}/SKILL.md"
        if [[ ! -d "$SKILL_DIR" ]]; then
            ISSUES="${ISSUES}  ✗ Skill directory not found: 'skills/${skill}/'\n"
            ISSUE_COUNT=$((ISSUE_COUNT + 1))
        elif [[ ! -f "$SKILL_MD" ]]; then
            ISSUES="${ISSUES}  ✗ Skill missing SKILL.md: 'skills/${skill}/SKILL.md'\n"
            ISSUE_COUNT=$((ISSUE_COUNT + 1))
        fi
    done < <(jq -r '.skills[].name // empty' "$CONFIG_FILE" 2>/dev/null)
fi

# Check 9: Agent .md file exists
if [[ ! -f "$MD_FILE" ]]; then
    ISSUES="${ISSUES}  ✗ Agent personality file not found: 'agents/${AGENT_NAME}.md'\n"
    ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 10: Model is valid (if specified)
MODEL=$(jq -r '.model // empty' "$CONFIG_FILE" 2>/dev/null)
if [[ -n "$MODEL" ]] && ! echo "opus sonnet haiku" | grep -qw "$MODEL"; then
    ISSUES="${ISSUES}  ✗ Invalid model: '${MODEL}' (expected: opus, sonnet, or haiku)\n"
    ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# --- Build response ------------------------------------------------------
if [[ "$ISSUE_COUNT" -gt 0 ]]; then
    health_buffer_append "⚠️ Agent '${AGENT_NAME}' config has ${ISSUE_COUNT} validation issue(s)"

    ESCAPED=$(echo -e "$ISSUES" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/ $//')

    cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "SubagentStart",
        "additionalContext": "⚠️ Agent Config Validator — '${AGENT_NAME}' has ${ISSUE_COUNT} issue(s): ${ESCAPED}Refer to agent_config.schema.json for the required structure."
    }
}
EOF
else
    # Validation passed — optionally inject config summary
    SKILL_COUNT=$(jq '.skills | length' "$CONFIG_FILE" 2>/dev/null || echo "0")
    DOMAIN_COUNT=$(jq '(.context.primaryDomains // []) | length' "$CONFIG_FILE" 2>/dev/null || echo "0")

    cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "SubagentStart",
        "additionalContext": "✅ Agent '${AGENT_NAME}' config validated: v${VERSION:-0.0.0}, ${SKILL_COUNT} skills, ${DOMAIN_COUNT} primary domains."
    }
}
EOF
fi

exit 0
