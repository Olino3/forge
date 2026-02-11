#!/bin/bash
# ⚒️ The Forge — Layer 2 Test Runner
#
# Runs all Layer 2 integration tests: hooks, memory, context, and E2E.
#
# Usage:
#   bash tests/layer2/run_layer2.sh             # Integration tests only
#   bash tests/layer2/run_layer2.sh --e2e       # Include E2E tests
#
# Exit codes:
#   0 — All tests passed
#   1 — One or more tests failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FORGE_DIR="$(cd "${TESTS_DIR}/.." && pwd)"
export FORGE_DIR

# --- Argument Parsing ---
RUN_E2E=false

for arg in "$@"; do
    case "$arg" in
        --e2e) RUN_E2E=true ;;
        --help|-h)
            echo "Usage: bash tests/layer2/run_layer2.sh [--e2e]"
            echo "  (no flags)  Run integration tests (hooks, memory, context)"
            echo "  --e2e       Also run E2E tests (requires claude CLI)"
            exit 0
            ;;
        *)
            echo "Unknown argument: $arg"
            exit 1
            ;;
    esac
done

# --- Color Output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓ $1${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; }
info() { echo -e "${BLUE}→ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

echo ""
echo "⚒️  The Forge — Layer 2: Integration Tests"
echo "═══════════════════════════════════════"
echo ""

# --- Detect Python ---
REPO_ROOT="$(cd "${FORGE_DIR}/.." && pwd)"
if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    PYTHON="${REPO_ROOT}/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    fail "python3 not found"
    exit 1
fi

# --- Dependency Checks ---
"$PYTHON" -c "import pytest" 2>/dev/null || { fail "pytest not installed"; exit 1; }
"$PYTHON" -c "import yaml" 2>/dev/null || { fail "pyyaml not installed"; exit 1; }
"$PYTHON" -c "import jsonschema" 2>/dev/null || { fail "jsonschema not installed"; exit 1; }
command -v jq &>/dev/null || { fail "jq not found"; exit 1; }

pass "All dependencies found"
echo ""

FAILED=0

# --- Hook Integration Tests ---
if [ -d "${SCRIPT_DIR}/hooks" ]; then
    info "Running hook integration tests..."
    if (cd "$TESTS_DIR" && "$PYTHON" -m pytest layer2/hooks/ -v --tb=short); then
        pass "Hook integration tests passed"
    else
        fail "Hook integration tests failed"
        FAILED=1
    fi
    echo ""
fi

# --- Memory Lifecycle Tests ---
if [ -d "${SCRIPT_DIR}/memory" ]; then
    info "Running memory lifecycle tests..."
    if (cd "$TESTS_DIR" && "$PYTHON" -m pytest layer2/memory/ -v --tb=short); then
        pass "Memory lifecycle tests passed"
    else
        fail "Memory lifecycle tests failed"
        FAILED=1
    fi
    echo ""
fi

# --- Context Loading Tests ---
if [ -d "${SCRIPT_DIR}/context" ]; then
    info "Running context loading tests..."
    if (cd "$TESTS_DIR" && "$PYTHON" -m pytest layer2/context/ -v --tb=short); then
        pass "Context loading tests passed"
    else
        fail "Context loading tests failed"
        FAILED=1
    fi
    echo ""
fi

# --- E2E Tests ---
if [ "$RUN_E2E" = true ]; then
    echo "═══════════════════════════════════════"
    echo "  E2E Tests"
    echo "═══════════════════════════════════════"
    echo ""

    if [ -d "${SCRIPT_DIR}/e2e" ]; then
        for test_script in "${SCRIPT_DIR}"/e2e/test_*.sh; do
            if [ -f "$test_script" ]; then
                test_name="$(basename "$test_script")"
                info "Running ${test_name}..."
                if bash "$test_script"; then
                    pass "${test_name} passed"
                else
                    fail "${test_name} failed"
                    FAILED=1
                fi
                echo ""
            fi
        done
    else
        warn "E2E test directory not found"
    fi
fi

# --- Summary ---
echo "═══════════════════════════════════════"
echo "  Summary"
echo "═══════════════════════════════════════"
echo ""

if [ "$FAILED" -eq 0 ]; then
    pass "Layer 2: ALL TESTS PASSED ⚒️"
    exit 0
else
    fail "Layer 2: SOME TESTS FAILED"
    exit 1
fi
