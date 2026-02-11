#!/bin/bash
# frontmatter_validator.sh — The Foreman: Context File Gate
#
# Hook:    PreToolUse (matcher: Write|Edit)
# Layer:   §6.3 The Foreman
# Purpose: Block writes to context/ files that lack required YAML
#          frontmatter fields, as defined by context_metadata.schema.json.
#
# Required fields: id, domain, title, type, estimatedTokens, loadingStrategy
#
# Domain enum:  engineering|angular|azure|commands|dotnet|git|python|schema|security
# Type enum:    always|framework|reference|pattern|index|detection
# Strategy enum: always|onDemand|lazy
#
# For Write: Validates the content that is about to be written.
# For Edit:  We cannot easily validate partial edits, so we validate the
#            existing file if the frontmatter fields are in the edit region.
#
# Input:  JSON on stdin (Claude Code PreToolUse format)
# Output: JSON with hookSpecificOutput.permissionDecision (deny if invalid)

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

FORGE_DIR="$(dirname "$SCRIPT_DIR")"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# Exit early if not a context file
[[ -z "$FILE_PATH" ]] && exit 0
[[ "$FILE_PATH" != *"context/"* ]] && exit 0
[[ "$FILE_PATH" != *.md ]] && exit 0

# Skip index files — they use a different structure
BASENAME=$(basename "$FILE_PATH")
[[ "$BASENAME" == "index.md" ]] && exit 0
[[ "$BASENAME" == "cross_domain.md" ]] && exit 0
[[ "$BASENAME" == "loading_protocol.md" ]] && exit 0

# --- Determine content to validate ---------------------------------------
CONTENT=""
if [[ "$TOOL_NAME" == "Write" ]]; then
    # For Write, the content is in tool_input.content
    CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // empty' 2>/dev/null)
elif [[ "$TOOL_NAME" == "Edit" ]]; then
    # For Edit, validate the existing file (the edit may touch frontmatter)
    if [[ -f "$FILE_PATH" ]]; then
        CONTENT=$(cat "$FILE_PATH")
    else
        exit 0  # New file via Edit is unusual; let it through
    fi
fi

[[ -z "$CONTENT" ]] && exit 0

# --- Check for YAML frontmatter delimiters --------------------------------
if ! echo "$CONTENT" | head -1 | grep -q '^---$'; then
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🚧 Frontmatter Validator: Context file '${FILE_PATH}' is missing YAML frontmatter. All context files must begin with '---' delimited frontmatter containing required fields: id, domain, title, type, estimatedTokens, loadingStrategy. See context_metadata.schema.json."
  }
}
EOF
    exit 0
fi

# Extract frontmatter (between first and second '---')
FRONTMATTER=$(echo "$CONTENT" | sed -n '/^---$/,/^---$/p' | sed '1d;$d')

if [[ -z "$FRONTMATTER" ]]; then
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🚧 Frontmatter Validator: Context file '${FILE_PATH}' has empty YAML frontmatter. Required fields: id, domain, title, type, estimatedTokens, loadingStrategy."
  }
}
EOF
    exit 0
fi

# --- Validate required fields --------------------------------------------
MISSING=""
INVALID=""

# Required fields check (simple grep — YAML is flat enough for this)
for field in id domain title type estimatedTokens loadingStrategy; do
    if ! echo "$FRONTMATTER" | grep -qE "^${field}:"; then
        MISSING="${MISSING} ${field}"
    fi
done

if [[ -n "$MISSING" ]]; then
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🚧 Frontmatter Validator: Context file '${FILE_PATH}' is missing required frontmatter fields:${MISSING}. See context_metadata.schema.json for the full schema."
  }
}
EOF
    exit 0
fi

# --- Validate enum values ------------------------------------------------
DOMAIN_VAL=$(echo "$FRONTMATTER" | grep -oP '^domain:\s*\K\S+' 2>/dev/null || echo "")
TYPE_VAL=$(echo "$FRONTMATTER" | grep -oP '^type:\s*\K\S+' 2>/dev/null || echo "")
STRATEGY_VAL=$(echo "$FRONTMATTER" | grep -oP '^loadingStrategy:\s*\K\S+' 2>/dev/null || echo "")

VALID_DOMAINS="engineering angular azure commands dotnet git python schema security"
VALID_TYPES="always framework reference pattern index detection"
VALID_STRATEGIES="always onDemand lazy"

if [[ -n "$DOMAIN_VAL" ]] && ! echo "$VALID_DOMAINS" | grep -qw "$DOMAIN_VAL"; then
    INVALID="${INVALID} domain='${DOMAIN_VAL}' (valid: ${VALID_DOMAINS})"
fi

if [[ -n "$TYPE_VAL" ]] && ! echo "$VALID_TYPES" | grep -qw "$TYPE_VAL"; then
    INVALID="${INVALID} type='${TYPE_VAL}' (valid: ${VALID_TYPES})"
fi

if [[ -n "$STRATEGY_VAL" ]] && ! echo "$VALID_STRATEGIES" | grep -qw "$STRATEGY_VAL"; then
    INVALID="${INVALID} loadingStrategy='${STRATEGY_VAL}' (valid: ${VALID_STRATEGIES})"
fi

if [[ -n "$INVALID" ]]; then
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "🚧 Frontmatter Validator: Context file '${FILE_PATH}' has invalid enum values:${INVALID}. See context_metadata.schema.json."
  }
}
EOF
    exit 0
fi

# --- All checks passed — allow (no output) --------------------------------
exit 0
