#!/bin/bash
# =============================================================================
# test_shellcheck.sh — Lint all hook scripts with shellcheck
#
# Runs shellcheck at warning level on all hooks/*.sh and hooks/lib/*.sh.
# Gracefully skips if shellcheck is not installed.
#
# Exit codes:
#   0 — All checks passed (or shellcheck not installed)
#   1 — One or more scripts have shellcheck warnings
#
# Phase 2 of the Forge Testing Architecture.
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve paths
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Walk up to find forge-plugin/hooks
FORGE_DIR="$SCRIPT_DIR"
while [[ ! -d "$FORGE_DIR/hooks" ]] && [[ "$FORGE_DIR" != "/" ]]; do
    FORGE_DIR="$(dirname "$FORGE_DIR")"
done

HOOKS_DIR="$FORGE_DIR/hooks"

if [[ ! -d "$HOOKS_DIR" ]]; then
    echo "FATAL: Cannot find hooks/ directory" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Check shellcheck availability
# ---------------------------------------------------------------------------

if ! command -v shellcheck &>/dev/null; then
    echo "=== ShellCheck Linting ==="
    echo "  ○ shellcheck not installed — skipping all checks"
    echo ""
    echo "  To install:"
    echo "    Ubuntu/Debian: sudo apt install shellcheck"
    echo "    macOS:         brew install shellcheck"
    echo "    Arch:          sudo pacman -S shellcheck"
    echo ""
    echo "RESULT: SKIP (shellcheck not available)"
    exit 0
fi

SHELLCHECK_VERSION=$(shellcheck --version 2>/dev/null | grep '^version:' | awk '{print $2}')
echo "=== ShellCheck Linting (v${SHELLCHECK_VERSION:-unknown}) ==="

# ---------------------------------------------------------------------------
# Collect scripts
# ---------------------------------------------------------------------------

mapfile -t HOOK_SCRIPTS < <(find "$HOOKS_DIR" -name '*.sh' -type f | sort)

if [[ ${#HOOK_SCRIPTS[@]} -eq 0 ]]; then
    echo "FATAL: No .sh files found in $HOOKS_DIR" >&2
    exit 1
fi

echo "Found ${#HOOK_SCRIPTS[@]} shell scripts to lint"
echo ""

# ---------------------------------------------------------------------------
# Run shellcheck
# ---------------------------------------------------------------------------

PASS=0
FAIL=0
TOTAL=0

for script in "${HOOK_SCRIPTS[@]}"; do
    name="${script#$HOOKS_DIR/}"
    ((TOTAL++)) || true

    # Run shellcheck at warning severity (-S warning)
    # Exclude specific rules that are intentional patterns:
    #   SC2034 - Variable appears unused (hooks set vars for sourcing)
    #   SC1091 - Can't follow sourced file (dynamic CLAUDE_PLUGIN_ROOT)
    #   SC2154 - Variable referenced but not assigned (set by environment)
    if shellcheck -S warning -e SC2034,SC1091,SC2154 "$script" 2>/dev/null; then
        echo "  ✓ $name"
        ((PASS++)) || true
    else
        echo "  ✗ $name"
        echo "    Details:"
        shellcheck -S warning -e SC2034,SC1091,SC2154 -f gcc "$script" 2>/dev/null | \
            sed 's/^/      /' || true
        ((FAIL++)) || true
    fi
done

echo ""

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo "=== ShellCheck Summary ==="
echo "  Passed:  $PASS"
echo "  Failed:  $FAIL"
echo "  Total:   $TOTAL"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo "RESULT: FAIL ($FAIL scripts with warnings)"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
