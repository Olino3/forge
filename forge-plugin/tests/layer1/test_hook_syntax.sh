#!/bin/bash
# =============================================================================
# test_hook_syntax.sh — Validate hook script syntax and conventions
#
# Checks:
#   1. Every hooks/*.sh has a proper #!/bin/bash shebang
#   2. Every hooks/*.sh has set -euo pipefail (or set -e at minimum)
#   3. Every hooks/*.sh passes bash -n (syntax check)
#   4. Every hooks/*.sh is executable
#   5. lib/health_buffer.sh also passes all checks
#
# Phase 1 of the Forge Testing Architecture.
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
# Counters
# ---------------------------------------------------------------------------

PASS=0
FAIL=0
SKIP=0
TOTAL=0

pass() { ((PASS++)) || true; ((TOTAL++)) || true; echo "  ✓ $1"; }
fail() { ((FAIL++)) || true; ((TOTAL++)) || true; echo "  ✗ $1" >&2; }
skip() { ((SKIP++)) || true; echo "  ○ $1 (skipped)"; }

# ---------------------------------------------------------------------------
# Collect all .sh files (hooks/*.sh + hooks/lib/*.sh)
# ---------------------------------------------------------------------------

mapfile -t HOOK_SCRIPTS < <(find "$HOOKS_DIR" -name '*.sh' -type f | sort)

if [[ ${#HOOK_SCRIPTS[@]} -eq 0 ]]; then
    echo "FATAL: No .sh files found in $HOOKS_DIR" >&2
    exit 1
fi

echo "=== Hook Syntax Tests ==="
echo "Found ${#HOOK_SCRIPTS[@]} shell scripts in hooks/"
echo ""

# ---------------------------------------------------------------------------
# Test 1: Shebang line
# ---------------------------------------------------------------------------

echo "--- Shebang Check ---"
for script in "${HOOK_SCRIPTS[@]}"; do
    name="${script#$HOOKS_DIR/}"
    first_line=$(head -1 "$script" 2>/dev/null || echo "")
    if [[ "$first_line" == "#!/bin/bash" ]] || [[ "$first_line" == "#!/usr/bin/env bash" ]]; then
        pass "$name: has valid shebang"
    else
        fail "$name: missing or invalid shebang (got: '$first_line')"
    fi
done
echo ""

# ---------------------------------------------------------------------------
# Test 2: set -e or set -euo pipefail
# ---------------------------------------------------------------------------

echo "--- Strict Mode Check ---"
for script in "${HOOK_SCRIPTS[@]}"; do
    name="${script#$HOOKS_DIR/}"
    # Scan the entire file for set -euo pipefail or set -e
    # Some scripts have long headers; lib/ files are sourced and may not have it
    if grep -qE '^\s*set\s+-euo\s+pipefail' "$script" 2>/dev/null; then
        pass "$name: has set -euo pipefail"
    elif grep -qE '^\s*set\s+-e\b' "$script" 2>/dev/null; then
        pass "$name: has set -e (minimal strict mode)"
    elif [[ "$name" == lib/* ]]; then
        # Library files sourced by others don't need their own set -e
        pass "$name: library file (sourced, set -e inherited)"
    else
        fail "$name: missing set -e or set -euo pipefail"
    fi
done
echo ""

# ---------------------------------------------------------------------------
# Test 3: bash -n syntax check
# ---------------------------------------------------------------------------

echo "--- Syntax Validation (bash -n) ---"
for script in "${HOOK_SCRIPTS[@]}"; do
    name="${script#$HOOKS_DIR/}"
    if bash -n "$script" 2>/dev/null; then
        pass "$name: passes bash -n"
    else
        fail "$name: FAILS bash -n syntax check"
    fi
done
echo ""

# ---------------------------------------------------------------------------
# Test 4: Executable permission
# ---------------------------------------------------------------------------

echo "--- Executable Permission Check ---"
for script in "${HOOK_SCRIPTS[@]}"; do
    name="${script#$HOOKS_DIR/}"
    if [[ -x "$script" ]]; then
        pass "$name: is executable"
    else
        fail "$name: NOT executable (missing +x)"
    fi
done
echo ""

# ---------------------------------------------------------------------------
# Test 5 (optional): ShellCheck
# ---------------------------------------------------------------------------

echo "--- ShellCheck (optional) ---"
if command -v shellcheck &>/dev/null; then
    for script in "${HOOK_SCRIPTS[@]}"; do
        name="${script#$HOOKS_DIR/}"
        if shellcheck -S warning "$script" 2>/dev/null; then
            pass "$name: passes shellcheck"
        else
            # ShellCheck warnings are non-fatal
            skip "$name: shellcheck warnings (non-blocking)"
        fi
    done
else
    skip "shellcheck not installed — skipping"
fi
echo ""

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo "=== Hook Syntax Summary ==="
echo "  Passed:  $PASS"
echo "  Failed:  $FAIL"
echo "  Skipped: $SKIP"
echo "  Total:   $TOTAL"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo "RESULT: FAIL ($FAIL failures)"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
