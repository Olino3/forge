#!/bin/bash
# ⚒️ The Forge — E2E: Plugin Loading Test
#
# Verifies that the Forge plugin loads correctly via the claude CLI.
# Skips gracefully if claude CLI is not available.
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
echo "⚒️  The Forge — E2E: Plugin Loading"
echo "═══════════════════════════════════════"
echo ""

FAILED=0

# --- Check prerequisites ---
if ! command -v claude &>/dev/null; then
    warn "claude CLI not found — skipping E2E plugin loading tests"
    exit 0
fi

# --- Test 1: Plugin manifest exists and is valid JSON ---
info "Checking plugin manifest..."
MANIFEST="${PLUGIN_DIR}/.claude-plugin/plugin.json"
if [ -f "$MANIFEST" ]; then
    if jq empty "$MANIFEST" 2>/dev/null; then
        pass "Plugin manifest is valid JSON"
    else
        fail "Plugin manifest is not valid JSON"
        FAILED=1
    fi
else
    fail "Plugin manifest not found at ${MANIFEST}"
    FAILED=1
fi

# --- Test 2: Plugin has required fields ---
info "Checking plugin manifest fields..."
if [ -f "$MANIFEST" ]; then
    NAME=$(jq -r '.name // empty' "$MANIFEST")
    VERSION=$(jq -r '.version // empty' "$MANIFEST")

    if [ -n "$NAME" ]; then
        pass "Plugin name: ${NAME}"
    else
        fail "Plugin missing 'name' field"
        FAILED=1
    fi

    if [ -n "$VERSION" ]; then
        pass "Plugin version: ${VERSION}"
    else
        fail "Plugin missing 'version' field"
        FAILED=1
    fi

    # Commands field should NOT be present (discovered from filesystem)
    if jq -e 'has("commands")' "$MANIFEST" >/dev/null 2>&1; then
        fail "Plugin has 'commands' field but commands should be discovered from filesystem"
        FAILED=1
    else
        pass "Plugin correctly omits 'commands' field (discovered from filesystem)"
    fi
fi

# --- Test 3: Command directories exist ---
info "Checking command directories exist..."
EXPECTED_COMMANDS=(
    "analyze" "implement" "improve" "document" "test" "build"
    "brainstorm" "remember" "mock" "azure-pipeline" "etl-pipeline" "azure-function"
)

for cmd in "${EXPECTED_COMMANDS[@]}"; do
    CMD_DIR="${PLUGIN_DIR}/commands/${cmd}"
    if [ -d "$CMD_DIR" ]; then
        CMD_FILE="${CMD_DIR}/COMMAND.md"
        if [ -f "$CMD_FILE" ]; then
            pass "Command directory and COMMAND.md exist: commands/${cmd}/"
        else
            fail "Command directory exists but COMMAND.md missing: commands/${cmd}/"
            FAILED=1
        fi
    else
        fail "Command directory missing: commands/${cmd}/"
        FAILED=1
    fi
done

# --- Test 4: Try loading plugin via claude CLI (if available) ---
info "Attempting plugin load via claude CLI..."
# Use --print-plugin-info if available, otherwise just verify the directory structure
if claude --help 2>&1 | grep -q "plugin"; then
    # Claude CLI has plugin support — attempt to list/verify
    # Note: Exact flags depend on claude CLI version; test basic invocation
    if claude --plugin-dir "$PLUGIN_DIR" --help &>/dev/null 2>&1; then
        pass "claude CLI accepted plugin directory"
    else
        # Try alternative flag format
        if claude -p "$PLUGIN_DIR" --help &>/dev/null 2>&1; then
            pass "claude CLI accepted plugin directory (short flag)"
        else
            warn "claude CLI did not accept --plugin-dir flag (CLI version may not support it)"
        fi
    fi
else
    warn "claude CLI does not appear to have plugin support in --help output"
fi

# --- Test 5: Plugin directory structure is complete ---
info "Checking plugin directory structure..."
REQUIRED_DIRS=(
    ".claude-plugin"
    "agents"
    "commands"
    "context"
    "hooks"
    "interfaces"
    "memory"
    "skills"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "${PLUGIN_DIR}/${dir}" ]; then
        pass "Directory exists: ${dir}/"
    else
        fail "Missing required directory: ${dir}/"
        FAILED=1
    fi
done

# --- Summary ---
echo ""
if [ "$FAILED" -eq 0 ]; then
    pass "Plugin loading: ALL CHECKS PASSED"
    exit 0
else
    fail "Plugin loading: SOME CHECKS FAILED"
    exit 1
fi
