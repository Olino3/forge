#!/bin/bash
# ⚒️ The Forge — Master Test Runner
#
# Usage:
#   bash tests/run_all.sh            # Layer 1 only (CI default)
#   bash tests/run_all.sh --layer2   # Layer 1 + Layer 2 (integration)
#   bash tests/run_all.sh --e2e      # Layer 1 + Layer 2 + E2E (full)
#
# Exit codes:
#   0 — All tests passed
#   1 — One or more tests failed
#
# CI Notes (GitHub Actions):
#   - The workflow (forge-tests.yml) was validated locally; first CI run may reveal issues
#   - FORGE_DIR is exported for Layer 1 pytest compatibility
#   - shellcheck exclusion rules may differ between Ubuntu versions (use SC codes if needed)
#   - For Layer 2 tests, use this script with --layer2 rather than layer2/run_layer2.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
export FORGE_DIR

# --- Argument Parsing ---
RUN_LAYER2=false
RUN_E2E=false

for arg in "$@"; do
    case "$arg" in
        --layer2) RUN_LAYER2=true ;;
        --e2e)    RUN_LAYER2=true; RUN_E2E=true ;;
        --help|-h)
            echo "Usage: bash tests/run_all.sh [--layer2] [--e2e]"
            echo "  (no flags)  Run Layer 1 (static/CI) tests only"
            echo "  --layer2    Run Layer 1 + Layer 2 (integration) tests"
            echo "  --e2e       Run Layer 1 + Layer 2 + E2E tests"
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
NC='\033[0m' # No Color

pass() { echo -e "${GREEN}✓ $1${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; }
info() { echo -e "${BLUE}→ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

# --- Dependency Checks ---
FAILED=0

check_dep() {
    local name="$1"
    local required="$2"
    if command -v "$name" &>/dev/null; then
        pass "$name found: $(command -v "$name")"
        return 0
    elif [ "$required" = "true" ]; then
        fail "$name is required but not found"
        FAILED=1
        return 1
    else
        warn "$name not found (optional, skipping related tests)"
        return 1
    fi
}

echo ""
echo "⚒️  The Forge — Test Runner"
echo "═══════════════════════════════════════"
echo ""
info "Checking dependencies..."

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
    pass "python found: $PYTHON"
fi
check_dep "jq" "true"

HAVE_PYTEST=true
if [[ -n "$PYTHON" ]]; then
    "$PYTHON" -c "import pytest" 2>/dev/null || { fail "pytest not installed (pip install pytest)"; HAVE_PYTEST=false; FAILED=1; }
    "$PYTHON" -c "import yaml" 2>/dev/null || { fail "pyyaml not installed (pip install pyyaml)"; FAILED=1; }
    "$PYTHON" -c "import jsonschema" 2>/dev/null || { fail "jsonschema not installed (pip install jsonschema)"; FAILED=1; }
fi

if [ "$FAILED" -eq 1 ]; then
    echo ""
    fail "Missing required dependencies. Install with:"
    echo "  pip install pytest pyyaml jsonschema"
    exit 1
fi

pass "All required dependencies found"
echo ""

# --- Layer 1: Static/CI Tests ---
echo "═══════════════════════════════════════"
echo "  Layer 1: Static/CI Tests"
echo "═══════════════════════════════════════"
echo ""

LAYER1_FAILED=0

# Run pytest for Layer 1
info "Running Layer 1 pytest tests..."
if (cd "$SCRIPT_DIR" && "$PYTHON" -m pytest layer1/ -v --tb=short); then
    pass "Layer 1 pytest tests passed"
else
    fail "Layer 1 pytest tests failed"
    LAYER1_FAILED=1
fi
echo ""

# Run bash tests
info "Running hook syntax checks..."
if bash "${SCRIPT_DIR}/layer1/test_hook_syntax.sh"; then
    pass "Hook syntax checks passed"
else
    fail "Hook syntax checks failed"
    LAYER1_FAILED=1
fi
echo ""

# Shellcheck (optional)
if command -v shellcheck &>/dev/null; then
    info "Running shellcheck..."
    if bash "${SCRIPT_DIR}/layer1/test_shellcheck.sh" 2>/dev/null; then
        pass "Shellcheck passed"
    else
        fail "Shellcheck found issues"
        LAYER1_FAILED=1
    fi
else
    warn "shellcheck not installed, skipping bash linting"
fi
echo ""

if [ "$LAYER1_FAILED" -eq 0 ]; then
    pass "Layer 1: ALL TESTS PASSED"
else
    fail "Layer 1: SOME TESTS FAILED"
fi
echo ""

# --- Layer 2: Integration Tests ---
LAYER2_FAILED=0

if [ "$RUN_LAYER2" = true ]; then
    echo "═══════════════════════════════════════"
    echo "  Layer 2: Integration Tests"
    echo "═══════════════════════════════════════"
    echo ""

    if [ -d "${SCRIPT_DIR}/layer2" ]; then
        # Hook tests
        if [ -d "${SCRIPT_DIR}/layer2/hooks" ]; then
            info "Running hook integration tests..."
            if (cd "$SCRIPT_DIR" && "$PYTHON" -m pytest layer2/hooks/ -v --tb=short); then
                pass "Hook integration tests passed"
            else
                fail "Hook integration tests failed"
                LAYER2_FAILED=1
            fi
            echo ""
        fi

        # Memory tests
        if [ -d "${SCRIPT_DIR}/layer2/memory" ]; then
            info "Running memory lifecycle tests..."
            if (cd "$SCRIPT_DIR" && "$PYTHON" -m pytest layer2/memory/ -v --tb=short); then
                pass "Memory lifecycle tests passed"
            else
                fail "Memory lifecycle tests failed"
                LAYER2_FAILED=1
            fi
            echo ""
        fi

        # Context tests
        if [ -d "${SCRIPT_DIR}/layer2/context" ]; then
            info "Running context loading tests..."
            if (cd "$SCRIPT_DIR" && "$PYTHON" -m pytest layer2/context/ -v --tb=short); then
                pass "Context loading tests passed"
            else
                fail "Context loading tests failed"
                LAYER2_FAILED=1
            fi
            echo ""
        fi
    else
        warn "Layer 2 test directory not found, skipping"
    fi

    if [ "$LAYER2_FAILED" -eq 0 ]; then
        pass "Layer 2: ALL TESTS PASSED"
    else
        fail "Layer 2: SOME TESTS FAILED"
    fi
    echo ""
fi

# --- E2E Tests ---
E2E_FAILED=0

if [ "$RUN_E2E" = true ]; then
    echo "═══════════════════════════════════════"
    echo "  E2E Tests (requires claude CLI)"
    echo "═══════════════════════════════════════"
    echo ""

    if command -v claude &>/dev/null; then
        if [ -d "${SCRIPT_DIR}/layer2/e2e" ]; then
            for test_script in "${SCRIPT_DIR}"/layer2/e2e/test_*.sh; do
                if [ -f "$test_script" ]; then
                    test_name="$(basename "$test_script")"
                    info "Running ${test_name}..."
                    if bash "$test_script"; then
                        pass "${test_name} passed"
                    else
                        fail "${test_name} failed"
                        E2E_FAILED=1
                    fi
                fi
            done
        else
            warn "E2E test directory not found, skipping"
        fi
    else
        warn "claude CLI not found, skipping E2E tests"
    fi
    echo ""
fi

# --- Summary ---
echo "═══════════════════════════════════════"
echo "  Summary"
echo "═══════════════════════════════════════"
echo ""

TOTAL_FAILED=$((LAYER1_FAILED + LAYER2_FAILED + E2E_FAILED))

if [ "$LAYER1_FAILED" -eq 0 ]; then pass "Layer 1: PASSED"; else fail "Layer 1: FAILED"; fi

if [ "$RUN_LAYER2" = true ]; then
    if [ "$LAYER2_FAILED" -eq 0 ]; then pass "Layer 2: PASSED"; else fail "Layer 2: FAILED"; fi
fi

if [ "$RUN_E2E" = true ]; then
    if [ "$E2E_FAILED" -eq 0 ]; then pass "E2E: PASSED"; else fail "E2E: FAILED"; fi
fi

echo ""

if [ "$TOTAL_FAILED" -eq 0 ]; then
    pass "ALL TESTS PASSED ⚒️"
    exit 0
else
    fail "SOME TESTS FAILED"
    exit 1
fi
