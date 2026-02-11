#!/bin/bash
# skill_compliance_checker.sh — The Foreman: Skill Workflow Compliance Audit
#
# Hook:    Stop (no matcher — fires on every stop)
# Layer:   §6.3 The Foreman
# Purpose: When Claude finishes responding, scan the session transcript
#          for skill invocations and verify they followed the mandatory
#          6-step workflow from SKILL_TEMPLATE.md:
#            Step 1: Initial Analysis
#            Step 2: Load Memory (Standard Memory Loading)
#            Step 3: Load Context (Standard Context Loading)
#            Step 4-5: Core Action
#            Step N-1: Generate Output (standard naming convention)
#            Step N: Update Memory (Standard Memory Update)
#
#          Reports violations as context feedback. Does NOT block the
#          stop (informational only). Skips when stop_hook_active=true
#          to avoid infinite loops.
#
# Input:  JSON on stdin (Claude Code Stop format — includes transcript_path)
# Output: JSON with decision/reason on violations, empty on success

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

# Guard: prevent infinite loops
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
    exit 0
fi

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)

# No transcript = nothing to audit
[[ -z "$TRANSCRIPT_PATH" ]] && exit 0
[[ ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# --- Detect skill invocations in transcript ------------------------------
# Skills are invoked via file reads of SKILL.md files.
# Look for patterns like: "skills/*/SKILL.md" being read
SKILLS_USED=$(grep -oE 'skills/[a-z0-9_-]+/SKILL\.md' "$TRANSCRIPT_PATH" 2>/dev/null | sort -u)

# No skills used = nothing to audit
[[ -z "$SKILLS_USED" ]] && exit 0

# Also try to detect skill invocations from tool use patterns
# The skill names appear in various forms in the transcript
SKILL_NAMES=()
while IFS= read -r skill_path; do
    SKILL_NAME=$(echo "$skill_path" | sed 's|skills/||;s|/SKILL\.md||')
    SKILL_NAMES+=("$SKILL_NAME")
done <<< "$SKILLS_USED"

[[ ${#SKILL_NAMES[@]} -eq 0 ]] && exit 0

# --- Audit each skill invocation ----------------------------------------
VIOLATIONS=""
VIOLATION_COUNT=0

for skill in "${SKILL_NAMES[@]}"; do
    SKILL_VIOLATIONS=""

    # Check Step 2: Memory Loading
    # Look for reads of memory/skills/{skill}/ or memory/projects/
    if ! grep -qE "memory/(skills/${skill}|projects/)" "$TRANSCRIPT_PATH" 2>/dev/null; then
        SKILL_VIOLATIONS="${SKILL_VIOLATIONS}  - Missing Step 2: No memory loading detected (expected reads from memory/skills/${skill}/ or memory/projects/)\n"
    fi

    # Check Step 3: Context Loading
    # Look for reads of context/ files
    if ! grep -qE "context/[a-z]" "$TRANSCRIPT_PATH" 2>/dev/null; then
        SKILL_VIOLATIONS="${SKILL_VIOLATIONS}  - Missing Step 3: No context loading detected (expected reads from context/ domain files)\n"
    fi

    # Check Step N: Memory Update
    # Look for writes to memory/skills/{skill}/
    if ! grep -qE "(Write|Edit).*memory/skills/${skill}" "$TRANSCRIPT_PATH" 2>/dev/null; then
        SKILL_VIOLATIONS="${SKILL_VIOLATIONS}  - Missing Step N: No memory update detected (expected writes to memory/skills/${skill}/)\n"
    fi

    # Check output generation (writes to /claudedocs/)
    if ! grep -q "claudedocs" "$TRANSCRIPT_PATH" 2>/dev/null; then
        SKILL_VIOLATIONS="${SKILL_VIOLATIONS}  - Missing Step N-1: No output generation to /claudedocs/ detected\n"
    fi

    if [[ -n "$SKILL_VIOLATIONS" ]]; then
        VIOLATIONS="${VIOLATIONS}🔧 Skill '${skill}' compliance issues:\n${SKILL_VIOLATIONS}\n"
        VIOLATION_COUNT=$((VIOLATION_COUNT + 1))
    fi
done

# --- Build response ------------------------------------------------------
if [[ -n "$VIOLATIONS" ]]; then
    health_buffer_append "📋 Skill compliance: ${VIOLATION_COUNT} skill(s) had workflow violations"

    ESCAPED=$(echo -e "$VIOLATIONS" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/ $//')

    cat <<EOF
{
  "decision": "block",
  "reason": "📋 Skill Compliance Checker: ${VIOLATION_COUNT} skill(s) did not follow the mandatory 6-step workflow (SKILL_TEMPLATE.md). ${ESCAPED} Please complete any missing steps before finishing."
}
EOF
fi

exit 0
