#!/usr/bin/env bash
# Test hook quality from forge-hook-checker workflow
#
# Validates:
# 1. set -euo pipefail presence
# 2. shellcheck pass
# 3. hooks.json registration
# 4. HOOKS_GUIDE.md mention
# 5. No blocking patterns (long sleeps, interactive prompts, network calls without timeout)
#
# Migrated from .github/workflows/forge-hook-checker.md as part of Phase 2 optimization

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="${SCRIPT_DIR}/../.."
HOOKS_DIR="${FORGE_DIR}/hooks"
HOOKS_JSON="${HOOKS_DIR}/hooks.json"
HOOKS_GUIDE="${HOOKS_DIR}/HOOKS_GUIDE.md"

exit_code=0
failures=()

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Running Hook Quality Checks..."
echo

# ---------------------------------------------------------------------------
# Check 1-2: set -euo pipefail and shellcheck
# ---------------------------------------------------------------------------

echo "Check 1-2: Bash best practices (set -euo pipefail + shellcheck)..."
hook_count=0
for hook in "${HOOKS_DIR}"/*.sh; do
    [[ -f "$hook" ]] || continue
    hook_name="$(basename "$hook")"
    hook_count=$((hook_count + 1))
    
    # Check 1: set -euo pipefail
    if ! grep -q 'set -euo pipefail' "$hook" && ! grep -q 'set -e.*-u.*-o pipefail' "$hook"; then
        failures+=("❌ $hook_name: Missing 'set -euo pipefail'")
        exit_code=1
    fi
    
    # Check 2: shellcheck
    if command -v shellcheck &>/dev/null; then
        if ! shellcheck -x "$hook" 2>/dev/null; then
            failures+=("❌ $hook_name: shellcheck failed")
            exit_code=1
        fi
    else
        echo "${YELLOW}⚠️  shellcheck not found, skipping shellcheck validation${NC}"
    fi
done

if [[ $hook_count -eq 0 ]]; then
    echo "${RED}❌ No hook files found in ${HOOKS_DIR}${NC}"
    exit 1
fi

echo "  Checked $hook_count hook files"
echo

# ---------------------------------------------------------------------------
# Check 3: hooks.json registration
# ---------------------------------------------------------------------------

echo "Check 3: hooks.json registration..."
if [[ ! -f "$HOOKS_JSON" ]]; then
    echo "${RED}❌ hooks.json not found${NC}"
    exit 1
fi

# Validate JSON syntax
if ! jq empty "$HOOKS_JSON" 2>/dev/null; then
    echo "${RED}❌ hooks.json is not valid JSON${NC}"
    exit 1
fi

# Check that every .sh file is registered in hooks.json
for hook in "${HOOKS_DIR}"/*.sh; do
    [[ -f "$hook" ]] || continue
    hook_name="$(basename "$hook")"
    
    # Check if hook is mentioned in hooks.json (as command value)
    if ! jq -e --arg hook "$hook_name" '.events[] | select(.handlers[].command == $hook)' "$HOOKS_JSON" >/dev/null 2>&1; then
        failures+=("❌ $hook_name: Not registered in hooks.json")
        exit_code=1
    fi
done

# Check that every command in hooks.json exists as a file
registered_hooks=$(jq -r '.events[].handlers[].command' "$HOOKS_JSON" | sort -u)
for registered_hook in $registered_hooks; do
    hook_path="${HOOKS_DIR}/${registered_hook}"
    if [[ ! -f "$hook_path" ]]; then
        failures+=("❌ hooks.json references non-existent hook: $registered_hook")
        exit_code=1
    fi
done

echo "  hooks.json is valid and consistent"
echo

# ---------------------------------------------------------------------------
# Check 4: HOOKS_GUIDE.md mention
# ---------------------------------------------------------------------------

echo "Check 4: HOOKS_GUIDE.md documentation..."
if [[ ! -f "$HOOKS_GUIDE" ]]; then
    echo "${RED}❌ HOOKS_GUIDE.md not found${NC}"
    exit 1
fi

for hook in "${HOOKS_DIR}"/*.sh; do
    [[ -f "$hook" ]] || continue
    hook_name="$(basename "$hook" .sh)"
    
    # Check if hook is mentioned in HOOKS_GUIDE.md
    if ! grep -q "$hook_name" "$HOOKS_GUIDE"; then
        failures+=("⚠️  $hook_name: Not documented in HOOKS_GUIDE.md")
        # Don't fail on this, just warn
    fi
done

echo "  Documentation check complete"
echo

# ---------------------------------------------------------------------------
# Check 5: No blocking patterns
# ---------------------------------------------------------------------------

echo "Check 5: No blocking/unsafe patterns..."
blocking_patterns=(
    "sleep [0-9]{2,}"         # Sleep for 10+ seconds
    "read -p"                 # Interactive prompt
    "curl.*-m\s*[0-9]{3,}"    # Curl timeout >100s
    "wget.*--timeout=[0-9]{3,}" # Wget timeout >100s
)

for hook in "${HOOKS_DIR}"/*.sh; do
    [[ -f "$hook" ]] || continue
    hook_name="$(basename "$hook")"
    
    for pattern in "${blocking_patterns[@]}"; do
        if grep -E "$pattern" "$hook" >/dev/null 2>&1; then
            failures+=("⚠️  $hook_name: Contains potentially blocking pattern: $pattern")
            # Don't fail on this, just warn
        fi
    done
done

echo "  Blocking pattern check complete"
echo

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

if [[ ${#failures[@]} -gt 0 ]]; then
    echo "${RED}═══════════════════════════════════════${NC}"
    echo "${RED}  Hook Quality Issues Found${NC}"
    echo "${RED}═══════════════════════════════════════${NC}"
    for failure in "${failures[@]}"; do
        echo "  $failure"
    done
    echo "${RED}═══════════════════════════════════════${NC}"
    echo
fi

if [[ $exit_code -eq 0 ]]; then
    echo "${GREEN}✅ All hook quality checks passed!${NC}"
else
    echo "${RED}❌ Some hook quality checks failed${NC}"
fi

exit $exit_code
