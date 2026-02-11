#!/bin/bash
# memory_cross_pollinator.sh — The Chronicle: Cross-Skill Insight Sharing
#
# Hook:    PostToolUse (matcher: Write|Edit)
# Layer:   §6.2 The Chronicle
# Purpose: When a skill writes critical findings to its own memory,
#          automatically copy those findings to the shared project
#          memory (memory/projects/{project}/cross_skill_insights.md)
#          so other skills can see them.
#
# Trigger: Writes to memory/skills/{skill}/{project}/{file}.md
# Detection: Scans for critical finding headers:
#            ## Critical, ## Security, ## Breaking, ## Performance
#
# Input:  JSON on stdin (Claude Code PostToolUse format)
# Output: JSON with additionalContext when cross-pollination occurs

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# Allow FORGE_DIR override for testing in temporary directories
FORGE_DIR="${FORGE_DIR:-$(dirname "$SCRIPT_DIR")}"
MEMORY_DIR="$FORGE_DIR/memory"
TODAY=$(date +%Y-%m-%d)

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# Exit early: must be a skill memory file
[[ -z "$FILE_PATH" ]] && exit 0
[[ "$FILE_PATH" != *"memory/skills/"* ]] && exit 0
[[ "$FILE_PATH" != *.md ]] && exit 0
[[ ! -f "$FILE_PATH" ]] && exit 0

# --- Extract path components ---------------------------------------------
# Expected path: .../memory/skills/{skill_name}/{project_name}/{file}.md
# We need: skill_name (component after skills/) and project_name (component after skill/)

# Get relative path from memory dir
REL_PATH="${FILE_PATH#*memory/skills/}"

# Split into components
IFS='/' read -ra PARTS <<< "$REL_PATH"

# Need at least 3 parts: skill/project/file.md
if [[ ${#PARTS[@]} -lt 3 ]]; then
    exit 0
fi

SKILL_NAME="${PARTS[0]}"
PROJECT_NAME="${PARTS[1]}"
FILE_NAME="${PARTS[2]}"

# Skip index files and operational files
case "$FILE_NAME" in
    index.md|lifecycle.md)
        exit 0
        ;;
esac

# --- Scan for critical finding headers -----------------------------------
CRITICAL_HEADERS=("## Critical" "## Security" "## Breaking" "## Performance")
FOUND_SECTIONS=()

for header in "${CRITICAL_HEADERS[@]}"; do
    if grep -q "^${header}" "$FILE_PATH" 2>/dev/null; then
        FOUND_SECTIONS+=("$header")
    fi
done

# No critical findings — nothing to cross-pollinate
if [[ ${#FOUND_SECTIONS[@]} -eq 0 ]]; then
    exit 0
fi

# --- Extract critical content blocks -------------------------------------
# For each found header, extract from header to next ## heading or EOF
EXTRACTED=""
for header in "${FOUND_SECTIONS[@]}"; do
    # Extract the section content (header line through next ## or EOF)
    SECTION=$(awk -v h="^${header}" '
        $0 ~ h { found=1; print; next }
        found && /^## / { found=0; next }
        found { print }
    ' "$FILE_PATH" 2>/dev/null)

    if [[ -n "$SECTION" ]]; then
        EXTRACTED="${EXTRACTED}${SECTION}"$'\n'
    fi
done

[[ -z "$EXTRACTED" ]] && exit 0

# --- Write to cross_skill_insights.md -----------------------------------
PROJECT_MEMORY_DIR="${MEMORY_DIR}/projects/${PROJECT_NAME}"
INSIGHTS_FILE="${PROJECT_MEMORY_DIR}/cross_skill_insights.md"

# Ensure project memory directory exists
mkdir -p "$PROJECT_MEMORY_DIR"

# Build the entry
ENTRY="### From \`${SKILL_NAME}\` — ${TODAY}
> Source: \`memory/skills/${SKILL_NAME}/${PROJECT_NAME}/${FILE_NAME}\`

${EXTRACTED}"

if [[ -f "$INSIGHTS_FILE" ]]; then
    # Update timestamp on first line
    sed -i "1s/Last Updated: [0-9-]*/Last Updated: $TODAY/" "$INSIGHTS_FILE" 2>/dev/null || true

    # Append new entry (avoid duplicates — check if same skill+date entry exists)
    if ! grep -q "From \`${SKILL_NAME}\` — ${TODAY}" "$INSIGHTS_FILE" 2>/dev/null; then
        echo "" >> "$INSIGHTS_FILE"
        echo "$ENTRY" >> "$INSIGHTS_FILE"
    else
        # Replace existing entry for this skill+date (remove old, append new)
        TEMP_FILE=$(mktemp)
        awk -v marker="From \`${SKILL_NAME}\` — ${TODAY}" '
            $0 ~ marker { skip=1; next }
            skip && /^### From/ { skip=0 }
            !skip { print }
        ' "$INSIGHTS_FILE" > "$TEMP_FILE"
        mv "$TEMP_FILE" "$INSIGHTS_FILE"
        echo "" >> "$INSIGHTS_FILE"
        echo "$ENTRY" >> "$INSIGHTS_FILE"
    fi
else
    # Create new insights file
    cat > "$INSIGHTS_FILE" <<HEADER
<!-- Last Updated: $TODAY -->
# Cross-Skill Insights — ${PROJECT_NAME}

> Auto-populated by memory_cross_pollinator.sh.
> Contains critical findings from individual skill memories.

${ENTRY}
HEADER
fi

SECTION_LIST=$(printf '%s, ' "${FOUND_SECTIONS[@]}")
SECTION_LIST="${SECTION_LIST%, }"

health_buffer_append "📡 Cross-pollinated ${#FOUND_SECTIONS[@]} critical section(s) from ${SKILL_NAME} → projects/${PROJECT_NAME}/cross_skill_insights.md"

cat <<EOF
{
  "additionalContext": "📡 Memory Cross-Pollinator: Detected critical findings (${SECTION_LIST}) in ${SKILL_NAME} memory for project '${PROJECT_NAME}'. Automatically copied to cross_skill_insights.md for visibility across all skills."
}
EOF

exit 0
