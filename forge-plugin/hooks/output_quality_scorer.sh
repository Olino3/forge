#!/bin/bash
# output_quality_scorer.sh — The Town Crier: Output Quality Scorer
#
# Hook:    PostToolUse (matcher: Write|Edit)
# Layer:   §6.4 The Town Crier
# Purpose: When a skill writes output to /claudedocs/, evaluate the
#          file against quality criteria:
#            1. Completeness — required sections present
#            2. Actionability — has recommendations/next-steps
#            3. Formatting — proper headings, code blocks, no raw URLs
#            4. Naming — follows OUTPUT_CONVENTIONS.md pattern
#
#          Appends a YAML quality metadata block at the end of the file
#          for trend analysis and skill improvement tracking.
#
# Input:  JSON on stdin (Claude Code PostToolUse format)
# Output: JSON with additionalContext (quality feedback for Claude)
#
# Design: Non-blocking. Scores are informational — they help track
#         output quality trends over time but never block writes.

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# Exit early if not a claudedocs output file
[[ -z "$FILE_PATH" ]] && exit 0
[[ "$FILE_PATH" != *"claudedocs"* ]] && exit 0
[[ "$FILE_PATH" != *.md ]] && exit 0

# Skip archive and manifest files
BASENAME=$(basename "$FILE_PATH")
case "$BASENAME" in
    manifest.md) exit 0 ;;
esac
[[ "$FILE_PATH" == *"/archive/"* ]] && exit 0

# File must exist
[[ ! -f "$FILE_PATH" ]] && exit 0

# --- Quality scoring -----------------------------------------------------
TOTAL_SCORE=0
MAX_SCORE=0
FEEDBACK=""
TODAY=$(date +%Y-%m-%d)

# Helper: safe grep count (grep exits 1 on no match, which kills set -e)
_gcount() {
    local count
    count=$(grep -c "$@" 2>/dev/null) || true
    echo "${count:-0}"
}

_gcounti() {
    local count
    count=$(grep -ciE "$@" 2>/dev/null) || true
    echo "${count:-0}"
}

# Helper: add score
_score() {
    local points="$1"
    local max="$2"
    local label="$3"
    TOTAL_SCORE=$((TOTAL_SCORE + points))
    MAX_SCORE=$((MAX_SCORE + max))
    if [[ "$points" -lt "$max" ]]; then
        FEEDBACK="${FEEDBACK}  - ${label}: ${points}/${max}\n"
    fi
}

# --- Criterion 1: Completeness (30 points) --------------------------------
# Check for common required sections in skill output

# Title (H1 heading)
H1_COUNT=$(_gcount '^# ' "$FILE_PATH")
if [[ "$H1_COUNT" -ge 1 ]]; then
    _score 5 5 "Title heading"
else
    _score 0 5 "Missing H1 title heading"
fi

# H2 sections (structure)
H2_COUNT=$(_gcount '^## ' "$FILE_PATH")
if [[ "$H2_COUNT" -ge 3 ]]; then
    _score 10 10 "Section structure"
elif [[ "$H2_COUNT" -ge 1 ]]; then
    _score 5 10 "Minimal section structure (only ${H2_COUNT} H2 sections)"
else
    _score 0 10 "No H2 section structure"
fi

# Summary/overview section
if grep -qiE '^## (Summary|Overview|Executive Summary|Introduction)' "$FILE_PATH" 2>/dev/null; then
    _score 5 5 "Summary section"
else
    _score 0 5 "Missing summary/overview section"
fi

# Findings/results section
if grep -qiE '^## (Findings|Results|Analysis|Issues|Review|Details)' "$FILE_PATH" 2>/dev/null; then
    _score 10 10 "Findings section"
else
    _score 0 10 "Missing findings/results section"
fi

# --- Criterion 2: Actionability (30 points) --------------------------------

# Recommendations or next-steps section
if grep -qiE '^## (Recommendations|Next Steps|Action Items|Remediation|Suggestions|Improvements)' "$FILE_PATH" 2>/dev/null; then
    _score 15 15 "Recommendations section"
else
    _score 0 15 "Missing recommendations/next-steps section"
fi

# Actionable language (should/must/consider/recommend/implement)
ACTION_WORDS=$(_gcounti '\b(should|must|recommend|consider|implement|migrate|refactor|fix|add|remove|update|replace)\b' "$FILE_PATH")
if [[ "$ACTION_WORDS" -ge 5 ]]; then
    _score 15 15 "Actionable language"
elif [[ "$ACTION_WORDS" -ge 2 ]]; then
    _score 8 15 "Limited actionable language (${ACTION_WORDS} instances)"
else
    _score 0 15 "No actionable language found"
fi

# --- Criterion 3: Formatting (25 points) -----------------------------------

# Code blocks present (for technical output)
CODE_BLOCKS=$(_gcount '\`\`\`' "$FILE_PATH")
CODE_BLOCK_PAIRS=$((CODE_BLOCKS / 2))
if [[ "$CODE_BLOCK_PAIRS" -ge 1 ]]; then
    _score 10 10 "Code examples"
else
    # Not all outputs need code — partial credit
    _score 5 10 "No code blocks (may not be needed)"
fi

# Bullet or numbered lists
LIST_ITEMS=$(grep -cE '^[[:space:]]*[-*•]|^[[:space:]]*[0-9]+\.' "$FILE_PATH" 2>/dev/null || true)
LIST_ITEMS=${LIST_ITEMS:-0}
if [[ "$LIST_ITEMS" -ge 3 ]]; then
    _score 10 10 "Well-structured lists"
elif [[ "$LIST_ITEMS" -ge 1 ]]; then
    _score 5 10 "Minimal list usage (${LIST_ITEMS} items)"
else
    _score 0 10 "No lists — wall-of-text risk"
fi

# Tables (bonus for structured data)
TABLE_ROWS=$(_gcount '|.*|.*|' "$FILE_PATH")
if [[ "$TABLE_ROWS" -ge 2 ]]; then
    _score 5 5 "Tables for structured data"
else
    _score 2 5 "No tables (optional)"
fi

# --- Criterion 4: Naming Convention (15 points) ----------------------------

# Check filename follows OUTPUT_CONVENTIONS pattern:
# {skill-name}_{project}_{YYYY-MM-DD}[_qualifier].md
if [[ "$BASENAME" =~ ^[a-z][a-z0-9-]+_[a-z][a-z0-9-]+_[0-9]{4}-[0-9]{2}-[0-9]{2}.*\.md$ ]]; then
    _score 15 15 "Naming convention"
elif [[ "$BASENAME" =~ ^[a-z][a-z0-9-]+_.*\.md$ ]]; then
    _score 8 15 "Partial naming convention match (missing date or project)"
else
    _score 0 15 "Filename does not follow OUTPUT_CONVENTIONS.md pattern"
fi

# --- Calculate percentage ------------------------------------------------
if [[ "$MAX_SCORE" -gt 0 ]]; then
    PERCENTAGE=$(( (TOTAL_SCORE * 100) / MAX_SCORE ))
else
    PERCENTAGE=0
fi

# Grade
GRADE="F"
if [[ "$PERCENTAGE" -ge 90 ]]; then GRADE="A"
elif [[ "$PERCENTAGE" -ge 80 ]]; then GRADE="B"
elif [[ "$PERCENTAGE" -ge 70 ]]; then GRADE="C"
elif [[ "$PERCENTAGE" -ge 60 ]]; then GRADE="D"
fi

# --- Determine file size -------------------------------------------------
LINE_COUNT=$(wc -l < "$FILE_PATH" 2>/dev/null || echo "0")
WORD_COUNT=$(wc -w < "$FILE_PATH" 2>/dev/null || echo "0")

# --- Append quality metadata to file -------------------------------------
cat >> "$FILE_PATH" <<EOF

---
<!-- Quality Score (auto-generated by output_quality_scorer) -->
<!-- score: ${TOTAL_SCORE}/${MAX_SCORE} (${PERCENTAGE}%) grade: ${GRADE} -->
<!-- lines: ${LINE_COUNT} words: ${WORD_COUNT} -->
<!-- scored: ${TODAY} -->
EOF

# --- Health buffer -------------------------------------------------------
health_buffer_append "📝 Output quality: ${BASENAME} scored ${TOTAL_SCORE}/${MAX_SCORE} (${PERCENTAGE}%, grade ${GRADE})"

# --- Build response ------------------------------------------------------
ESCAPED_FEEDBACK=""
if [[ -n "$FEEDBACK" ]]; then
    ESCAPED_FEEDBACK=$(echo -e "$FEEDBACK" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/ $//')
fi

cat <<EOF
{
  "additionalContext": "📝 Output Quality Score — ${BASENAME}: ${TOTAL_SCORE}/${MAX_SCORE} (${PERCENTAGE}%, grade ${GRADE}). ${ESCAPED_FEEDBACK}"
}
EOF

exit 0
