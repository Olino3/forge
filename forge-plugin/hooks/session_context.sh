#!/bin/bash
# Summarize project context at session start
#
# Usage: bash session_context.sh [project_name]
#
# Behavior:
# 1. Detect current project from git remote or directory name
# 2. Read memory/projects/{project}/project_profile.md if exists
# 3. Count recent skill invocations from memory files
# 4. Output brief summary to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$FORGE_DIR/memory"

# Detect project name
if [[ -n "${1:-}" ]]; then
    PROJECT="$1"
else
    # Try git remote name
    PROJECT=$(git remote get-url origin 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//' || true)
    if [[ -z "$PROJECT" ]]; then
        # Fall back to directory name
        PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
    fi
fi

echo "=== Forge Session Context ==="
echo "Project: $PROJECT"
echo ""

# Check shared project memory
PROFILE="$MEMORY_DIR/projects/$PROJECT/project_profile.md"
if [[ -f "$PROFILE" ]]; then
    echo "--- Project Profile ---"
    # Show first 20 non-comment lines
    grep -v '^<!--' "$PROFILE" | head -20
    echo ""
else
    echo "No shared project memory found. First skill invocation will create it."
    echo ""
fi

# Count skill memories for this project
echo "--- Skill Memory Status ---"
SKILL_COUNT=0
while IFS= read -r skill_dir; do
    [[ -z "$skill_dir" ]] && continue
    SKILL_NAME=$(basename "$skill_dir")
    PROJECT_MEM="$skill_dir/$PROJECT"
    if [[ -d "$PROJECT_MEM" ]]; then
        FILE_COUNT=$(find "$PROJECT_MEM" -name "*.md" -type f 2>/dev/null | wc -l)
        LAST_MOD=$(find "$PROJECT_MEM" -name "*.md" -type f -printf '%T@\n' 2>/dev/null | sort -rn | head -1 || echo "")
        if [[ -n "$LAST_MOD" ]]; then
            LAST_DATE=$(date -d "@${LAST_MOD%.*}" +%Y-%m-%d 2>/dev/null || echo "unknown")
        else
            LAST_DATE="unknown"
        fi
        echo "  $SKILL_NAME: $FILE_COUNT files (last updated: $LAST_DATE)"
        SKILL_COUNT=$((SKILL_COUNT + 1))
    fi
done < <(find "$MEMORY_DIR/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)

if [[ "$SKILL_COUNT" -eq 0 ]]; then
    echo "  No skill memory for this project yet."
fi

echo ""
echo "==========================="
