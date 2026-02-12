#!/bin/bash
# scripts/setup.sh
# Main setup script for The Forge - initializes submodules, verifies symlinks, validates plugins

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$FORGE_ROOT"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  ⚒️  The Forge - Setup Script                                        ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Initialize git submodules
echo "📦 Initializing external skill repositories..."
if [ -f ".gitmodules" ]; then
    git submodule update --init --recursive
    echo "  ✓ Submodules initialized"
else
    echo "  ⚠️  No .gitmodules file found - submodules not configured"
fi
echo ""

# Step 2: Verify symlinks
echo "🔗 Verifying symlink integrity..."
if [ -f "$SCRIPT_DIR/verify-symlinks.sh" ]; then
    if bash "$SCRIPT_DIR/verify-symlinks.sh"; then
        echo "  ✓ All symlinks healthy"
    else
        echo "  ⚠️  Broken symlinks detected, attempting repair..."
        bash "$SCRIPT_DIR/fix-symlinks.sh"
        echo "  ✓ Symlinks repaired"
    fi
else
    echo "  ⚠️  Verify script not found, skipping"
fi
echo ""

# Step 3: Validate plugins
echo "✅ Validating plugin manifests..."
if [ -f "$SCRIPT_DIR/validate-plugins.sh" ]; then
    bash "$SCRIPT_DIR/validate-plugins.sh"
else
    echo "  ⚠️  Validation script not found, skipping"
fi
echo ""

# Step 4: Install git hooks (optional)
echo "🪝 Installing git hooks..."
if [ -d "$SCRIPT_DIR/hooks" ]; then
    if [ -d ".git/hooks" ]; then
        cp "$SCRIPT_DIR/hooks/"* ".git/hooks/" 2>/dev/null && chmod +x .git/hooks/* 2>/dev/null
        echo "  ✓ Git hooks installed"
    else
        echo "  ⚠️  .git/hooks directory not found, skipping"
    fi
else
    echo "  ℹ️  Hook templates not found (will be added in future version)"
fi
echo ""

# Step 5: Display summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Setup complete! The Forge is ready."
echo ""
echo "📚 Available plugins in marketplace:"
echo "  • 1 Forge core plugin (22 native skills)"
echo "  • 10 external wrapper plugins (159 skills)"
echo "  • 27 Trail of Bits security plugins (53 skills)"
echo ""
echo "  Total: 38 plugins • 234 skills • 27 agents"
echo ""
echo "📖 Next steps:"
echo "  • Read README.md for usage instructions"
echo "  • Run: claude plugin list"
echo "  • Install plugins: /plugin install <name>@forge-marketplace"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
