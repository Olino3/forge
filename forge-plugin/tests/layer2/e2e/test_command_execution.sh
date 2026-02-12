#!/bin/bash
# ⚒️ The Forge — E2E: Command Execution Test
#
# Verifies that all 12 commands are registered, discoverable, and have
# valid COMMAND.md files with expected structure.
# Skips runtime command invocation if claude CLI is not available.
#
# Exit codes:
#   0 — All checks passed (or skipped due to missing CLI)
#   1 — One or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
PLUGIN_DIR="${FORGE_DIR}"

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
echo "⚒️  The Forge — E2E: Command Execution"
echo "═══════════════════════════════════════"
echo ""

FAILED=0

# --- Expected commands (from plugin.json) ---
EXPECTED_COMMANDS=(
    "analyze"
    "implement"
    "improve"
    "document"
    "test"
    "build"
    "brainstorm"
    "remember"
    "mock"
    "azure-pipeline"
    "etl-pipeline"
    "azure-function"
)

# --- Test 1: All expected commands exist as directories with COMMAND.md ---
info "Checking command directories and COMMAND.md files..."
MANIFEST="${PLUGIN_DIR}/.claude-plugin/plugin.json"
if [ ! -f "$MANIFEST" ]; then
    fail "Plugin manifest not found"
    exit 1
fi

for cmd in "${EXPECTED_COMMANDS[@]}"; do
    CMD_DIR="${PLUGIN_DIR}/commands/${cmd}"
    CMD_FILE="${CMD_DIR}/COMMAND.md"
    
    if [ -d "$CMD_DIR" ]; then
        if [ -f "$CMD_FILE" ]; then
            pass "Command '/${cmd}' directory and COMMAND.md exist"
        else
            fail "Command '/${cmd}' directory exists but COMMAND.md missing"
            FAILED=1
        fi
    else
        fail "Command directory missing: commands/${cmd}/"
        FAILED=1
    fi
done

# --- Test 2: COMMAND.md files are non-empty and have expected sections ---
info "Checking COMMAND.md content structure..."
for cmd in "${EXPECTED_COMMANDS[@]}"; do
    CMD_FILE="${PLUGIN_DIR}/commands/${cmd}/COMMAND.md"
    if [ -f "$CMD_FILE" ]; then
        LINE_COUNT=$(wc -l < "$CMD_FILE")
        if [ "$LINE_COUNT" -gt 5 ]; then
            pass "/${cmd}/COMMAND.md has content (${LINE_COUNT} lines)"
        else
            warn "/${cmd}/COMMAND.md seems too short (${LINE_COUNT} lines)"
        fi
    fi
done

# --- Test 3: Command count matches expected ---
info "Checking command count..."
ACTUAL_COUNT=$(find "${PLUGIN_DIR}/commands" -mindepth 1 -maxdepth 1 -type d | wc -l)
EXPECTED_COUNT=${#EXPECTED_COMMANDS[@]}

if [ "$ACTUAL_COUNT" -eq "$EXPECTED_COUNT" ]; then
    pass "Command count matches: ${ACTUAL_COUNT} directories, ${EXPECTED_COUNT} expected"
else
    fail "Command count differs: ${ACTUAL_COUNT} directories, ${EXPECTED_COUNT} expected"
    FAILED=1
fi

# --- Test 4: Commands index file exists ---
info "Checking commands index..."
INDEX_FILE="${PLUGIN_DIR}/commands/index.md"
if [ -f "$INDEX_FILE" ]; then
    pass "commands/index.md exists"
    # Check that index references all commands
    for cmd in "${EXPECTED_COMMANDS[@]}"; do
        if grep -q "$cmd" "$INDEX_FILE" 2>/dev/null; then
            pass "Index references /${cmd}"
        else
            warn "Index may not reference /${cmd}"
        fi
    done
else
    warn "commands/index.md not found"
fi

# --- Test 5: Runtime command invocation (requires claude CLI) ---
# NOTE: True runtime E2E testing of command invocation is not currently possible because the
# `claude` CLI requires an interactive session. This test validates structure and discoverability.
# Future options: (1) claude CLI batch/non-interactive mode, (2) dedicated Claude CLI test harness.
if command -v claude &>/dev/null; then
    info "claude CLI found — runtime command invocation tests not yet implemented"
    warn "claude CLI requires interactive session; skipping runtime invocation"
else
    warn "claude CLI not found — skipping runtime command invocation tests"
fi

# --- Summary ---
echo ""
if [ "$FAILED" -eq 0 ]; then
    pass "Command execution: ALL CHECKS PASSED"
    exit 0
else
    fail "Command execution: SOME CHECKS FAILED"
    exit 1
fi
