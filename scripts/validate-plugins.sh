#!/bin/bash
# scripts/validate-plugins.sh
# Validates that all Forge marketplace plugins load correctly

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$FORGE_ROOT"

echo "✅ Validating Forge marketplace plugins..."
echo ""

# Validate marketplace
if command -v claude &> /dev/null; then
    echo "→ Validating marketplace.json..."
    if claude plugin validate . 2>&1 | grep -q "Validation passed"; then
        echo "  ✓ Marketplace validation passed"
    else
        echo "  ❌ Marketplace validation failed"
        claude plugin validate .
        exit 1
    fi
else
    echo "⚠️  Claude Code CLI not found - skipping validation"
    echo "   Install Claude Code to validate plugins"
fi

echo ""
echo "✅ Plugin validation complete!"
