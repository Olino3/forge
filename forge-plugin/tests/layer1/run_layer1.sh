#!/bin/bash
# ⚒️ The Forge — Layer 1 Test Runner
#
# Runs all static/CI tests that validate structure, schemas, syntax,
# and cross-references without any runtime dependencies.
#
# Usage:
#   bash tests/layer1/run_layer1.sh
#
# Exit codes:
#   0 — All tests passed
#   1 — One or more tests failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FORGE_DIR="$(cd "${TESTS_DIR}/.." && pwd)"
export FORGE_DIR

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓ $1${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; }
info() { echo -e "${BLUE}→ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

FAILED=0

echo ""
echo "⚒️  Layer 1: Static/CI Tests"
echo "═══════════════════════════════════════"
echo ""

# --- Pytest Tests ---
info "Running pytest Layer 1 tests..."

# Detect Python: prefer venv, fall back to system python3
REPO_ROOT="$(cd "${FORGE_DIR}/.." && pwd)"
if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    PYTHON="${REPO_ROOT}/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    fail "python3 not found"
    FAILED=1
    PYTHON=""
fi

if [[ -n "$PYTHON" ]]; then
    if (cd "$TESTS_DIR" && "$PYTHON" -m pytest layer1/ -v --tb=short); then
        pass "pytest tests passed"
    else
        fail "pytest tests failed"
        FAILED=1
    fi
fi
echo ""

# --- Hook Syntax Tests ---
info "Running hook syntax checks..."
if bash "${SCRIPT_DIR}/test_hook_syntax.sh"; then
    pass "Hook syntax checks passed"
else
    fail "Hook syntax checks failed"
    FAILED=1
fi
echo ""

# --- Shellcheck (optional) ---
if command -v shellcheck &>/dev/null; then
    info "Running shellcheck..."
    if [ -f "${SCRIPT_DIR}/test_shellcheck.sh" ]; then
        if bash "${SCRIPT_DIR}/test_shellcheck.sh"; then
            pass "Shellcheck passed"
        else
            fail "Shellcheck failed"
            FAILED=1
        fi
    else
        warn "test_shellcheck.sh not yet implemented"
    fi
else
    warn "shellcheck not installed, skipping"
fi
echo ""

# --- Summary ---
echo "═══════════════════════════════════════"
if [ "$FAILED" -eq 0 ]; then
    pass "Layer 1: ALL TESTS PASSED ⚒️"
    exit 0
else
    fail "Layer 1: SOME TESTS FAILED"
    exit 1
fi
