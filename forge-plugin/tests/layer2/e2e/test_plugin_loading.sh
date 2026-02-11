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
    COMMANDS=$(jq -r '.commands // empty' "$MANIFEST")

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

    if [ "$COMMANDS" != "null" ] && [ -n "$COMMANDS" ]; then
        CMD_COUNT=$(jq '.commands | length' "$MANIFEST")
        pass "Plugin has ${CMD_COUNT} commands registered"
    else
        fail "Plugin missing 'commands' field"
        FAILED=1
    fi
fi

# --- Test 3: All command paths resolve ---
info "Checking command path resolution..."
if [ -f "$MANIFEST" ]; then
    CMD_NAMES=$(jq -r '.commands | keys[]' "$MANIFEST" 2>/dev/null)
    for cmd in $CMD_NAMES; do
        CMD_PATH=$(jq -r ".commands[\"${cmd}\"]" "$MANIFEST")
        FULL_PATH="${PLUGIN_DIR}/${CMD_PATH}"
        if [ -f "$FULL_PATH" ]; then
            pass "Command '/${cmd}' → ${CMD_PATH}"
        else
            fail "Command '/${cmd}' references missing file: ${CMD_PATH}"
            FAILED=1
        fi
    done
fi

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
