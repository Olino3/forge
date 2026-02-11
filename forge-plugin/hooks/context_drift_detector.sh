#!/bin/bash
# context_drift_detector.sh — The Foreman: Context Drift Detector
#
# Hook:    PostToolUse (matcher: Write|Edit)
# Layer:   §6.3 The Foreman
# Purpose: When dependency files are written/edited (package.json,
#          requirements.txt, pyproject.toml, go.mod, *.csproj), scan
#          ALL context files' tags and warn if the project's actual
#          dependencies conflict with the loaded context domain.
#
#          Example: If pyproject.toml adds "fastapi" but context files
#          tagged [flask] are present, warn that flask-specific guidance
#          may not apply.
#
# Input:  JSON on stdin (Claude Code PostToolUse format)
# Output: JSON with additionalContext warning on drift detection

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# Allow FORGE_DIR override for testing in temporary directories
FORGE_DIR="${FORGE_DIR:-$(dirname "$SCRIPT_DIR")}"
CONTEXT_DIR="$FORGE_DIR/context"
CONFLICTS_FILE="$SCRIPT_DIR/lib/framework_conflicts.json"

# --- Parse stdin ---------------------------------------------------------
INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)
[[ -z "$FILE_PATH" ]] && exit 0

# --- Guard: only trigger on dependency files -----------------------------
BASENAME=$(basename "$FILE_PATH")
DEP_TYPE=""
case "$BASENAME" in
    package.json)       DEP_TYPE="npm" ;;
    requirements.txt)   DEP_TYPE="pip" ;;
    pyproject.toml)     DEP_TYPE="pyproject" ;;
    Pipfile)            DEP_TYPE="pipfile" ;;
    go.mod)             DEP_TYPE="gomod" ;;
    *.csproj)           DEP_TYPE="dotnet" ;;
    *)                  exit 0 ;;
esac

[[ ! -f "$FILE_PATH" ]] && exit 0
[[ ! -f "$CONFLICTS_FILE" ]] && exit 0

# --- Extract installed packages from the dependency file -----------------
_extract_packages() {
    local file="$1"
    local type="$2"

    case "$type" in
        npm)
            # Extract from dependencies + devDependencies keys
            jq -r '(.dependencies // {} | keys[]), (.devDependencies // {} | keys[])' "$file" 2>/dev/null || true
            ;;
        pip)
            # requirements.txt: one package per line, strip version specifiers
            grep -vE '^\s*#|^\s*$' "$file" 2>/dev/null | sed 's/[><=!~;].*//' | sed 's/\[.*//' | tr -d ' ' || true
            ;;
        pyproject)
            # Extract from pyproject.toml (best-effort TOML parsing)
            # Poetry table format: key = value lines under [tool.poetry.dependencies]
            (awk '/^\[tool\.poetry\.dependencies\]/,/^\[/' "$file" 2>/dev/null \
                | grep -oE '^[a-zA-Z0-9_-]+' | grep -vE '^\[|^python$') 2>/dev/null || true
            # PEP 621 array format: lines containing "package..." within dependencies = [ ... ]
            # Use sed to extract all quoted package names from the dependencies array
            (sed -n '/^dependencies[[:space:]]*=[[:space:]]*\[/,/\]/p' "$file" 2>/dev/null \
                | grep -oE '"[a-zA-Z0-9_-]+' | tr -d '"') 2>/dev/null || true
            ;;
        pipfile)
            (awk '/^\[packages\]|^\[dev-packages\]/,/^\[/' "$file" 2>/dev/null \
                | grep -oE '^[a-zA-Z0-9_-]+' | grep -v '^\[') 2>/dev/null || true
            ;;
        gomod)
            (grep -E '^\s+[a-z]' "$file" 2>/dev/null | awk '{print $1}' | xargs -I{} basename {}) 2>/dev/null || true
            ;;
        dotnet)
            grep -oP 'PackageReference Include="\K[^"]+' "$file" 2>/dev/null || true
            ;;
    esac
}

PACKAGES=$(_extract_packages "$FILE_PATH" "$DEP_TYPE" | sort -u)
[[ -z "$PACKAGES" ]] && exit 0

# --- Scan context files for ALL tags -------------------------------------
ALL_CONTEXT_TAGS=$(
    find "$CONTEXT_DIR" -name '*.md' -exec grep -h '^tags:' {} \; 2>/dev/null \
    | sed 's/^tags:\s*//' \
    | tr -d '[]' \
    | tr ',' '\n' \
    | sed 's/^[[:space:]]*//' \
    | sed 's/[[:space:]]*$//' \
    | sort -u
)

# --- Check each conflict group -------------------------------------------
WARNINGS=""
CONFLICT_GROUPS=$(jq -r 'keys[] | select(. != "_comment")' "$CONFLICTS_FILE" 2>/dev/null)

for group in $CONFLICT_GROUPS; do
    MEMBERS=$(jq -r ".\"$group\".members | keys[]" "$CONFLICTS_FILE" 2>/dev/null)
    GROUP_DESC=$(jq -r ".\"$group\".description" "$CONFLICTS_FILE" 2>/dev/null)

    # Find which members are present in the project's dependencies
    DETECTED_IN_DEPS=()
    for member in $MEMBERS; do
        MEMBER_PACKAGES=$(jq -r ".\"$group\".members.\"$member\".packages[]" "$CONFLICTS_FILE" 2>/dev/null)
        for pkg in $MEMBER_PACKAGES; do
            if echo "$PACKAGES" | grep -qi "^${pkg}$"; then
                # Avoid duplicates
                if [[ ! " ${DETECTED_IN_DEPS[*]:-} " =~ " ${member} " ]]; then
                    DETECTED_IN_DEPS+=("$member")
                fi
                break
            fi
        done
    done

    # Skip if 0 or 1 member detected — no conflict
    [[ ${#DETECTED_IN_DEPS[@]} -lt 2 ]] && continue

    # Multiple frameworks from the same group detected in deps
    DEPS_LIST=$(printf '%s, ' "${DETECTED_IN_DEPS[@]}")
    DEPS_LIST="${DEPS_LIST%, }"
    WARN="⚠️ Context drift: ${GROUP_DESC} — detected multiple: [${DEPS_LIST}] in ${BASENAME}."
    WARNINGS="${WARNINGS}${WARN}\n"
    health_buffer_append "$WARN"

    # Also check: does the context domain have tags for a framework
    # the project does NOT use?
    for member in $MEMBERS; do
        MEMBER_TAGS=$(jq -r ".\"$group\".members.\"$member\".context_tags[]" "$CONFLICTS_FILE" 2>/dev/null)
        for tag in $MEMBER_TAGS; do
            if echo "$ALL_CONTEXT_TAGS" | grep -qi "^${tag}$"; then
                # Context has this tag — is this member in the project?
                if [[ ! " ${DETECTED_IN_DEPS[*]:-} " =~ " ${member} " ]]; then
                    WARN="⚠️ Stale context: context files tagged [${tag}] exist but '${member}' is not in ${BASENAME}."
                    WARNINGS="${WARNINGS}${WARN}\n"
                    health_buffer_append "$WARN"
                fi
            fi
        done
    done
done

# --- Also detect single-framework drift (context ≠ deps) ----------------
# For each conflict group, if exactly 1 member is in deps, check
# whether context tags for a DIFFERENT member also exist
for group in $CONFLICT_GROUPS; do
    MEMBERS=$(jq -r ".\"$group\".members | keys[]" "$CONFLICTS_FILE" 2>/dev/null)

    DETECTED_IN_DEPS=()
    for member in $MEMBERS; do
        MEMBER_PACKAGES=$(jq -r ".\"$group\".members.\"$member\".packages[]" "$CONFLICTS_FILE" 2>/dev/null)
        for pkg in $MEMBER_PACKAGES; do
            if echo "$PACKAGES" | grep -qi "^${pkg}$"; then
                if [[ ! " ${DETECTED_IN_DEPS[*]:-} " =~ " ${member} " ]]; then
                    DETECTED_IN_DEPS+=("$member")
                fi
                break
            fi
        done
    done

    # Only 1 framework detected — check for stale context of others
    [[ ${#DETECTED_IN_DEPS[@]} -ne 1 ]] && continue
    ACTIVE_MEMBER="${DETECTED_IN_DEPS[0]}"

    for member in $MEMBERS; do
        [[ "$member" == "$ACTIVE_MEMBER" ]] && continue
        MEMBER_TAGS=$(jq -r ".\"$group\".members.\"$member\".context_tags[]" "$CONFLICTS_FILE" 2>/dev/null)
        for tag in $MEMBER_TAGS; do
            if echo "$ALL_CONTEXT_TAGS" | grep -qi "^${tag}$"; then
                WARN="⚠️ Context drift: project uses '${ACTIVE_MEMBER}' but context files tagged [${tag}] (for '${member}') are loaded. Consider unloading irrelevant context."
                WARNINGS="${WARNINGS}${WARN}\n"
                health_buffer_append "$WARN"
            fi
        done
    done
done

# --- Build response ------------------------------------------------------
if [[ -n "$WARNINGS" ]]; then
    ESCAPED=$(echo -e "$WARNINGS" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/ $//')
    cat <<EOF
{
  "additionalContext": "🔍 Context Drift Detector — ${BASENAME}: ${ESCAPED}"
}
EOF
fi

exit 0
