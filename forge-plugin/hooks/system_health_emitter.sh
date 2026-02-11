#!/bin/bash
# system_health_emitter.sh — The Chronicle: Health Buffer Aggregator
#
# Hook:    PostToolUse (matcher: .*)
# Layer:   §6.2 The Chronicle
# Purpose: Flush the shared health buffer after every tool execution and
#          surface accumulated warnings to Claude via additionalContext.
#
# Design notes:
#   - Because Claude Code runs hooks for the same event in parallel,
#     warnings appended by *this* PostToolUse cycle's sibling hooks
#     (e.g. memory_quality_gate) may not yet be in the buffer.
#     They will be picked up on the *next* tool cycle — an acceptable
#     one-event lag confirmed during planning.
#   - The hook is intentionally cheap: if the buffer is empty it exits
#     immediately with no output.

set -euo pipefail

# --- Source shared library -----------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/health_buffer.sh
source "${SCRIPT_DIR}/lib/health_buffer.sh"

# --- Flush and emit ------------------------------------------------------
BUFFERED=$(health_buffer_flush 2>/dev/null) || exit 0

# Nothing to report
[[ -z "$BUFFERED" ]] && exit 0

# Count entries
ENTRY_COUNT=$(echo "$BUFFERED" | wc -l)

# Build JSON response with additionalContext for Claude
cat <<EOF
{
  "additionalContext": "🔥 Forge Health Report (${ENTRY_COUNT} event(s)):\n${BUFFERED//$'\n'/\\n}"
}
EOF

exit 0
