#!/bin/bash
# scripts/verify-symlinks.sh
# Verifies that all wrapper plugin symlinks are healthy

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$FORGE_ROOT"

BROKEN=0
TOTAL=0

echo "🔍 Verifying symlinks..."
echo ""

# Vercel wrapper
echo "→ Vercel wrapper..."
if [ -L "vercel/vercel-skills-plugin/skills" ]; then
    TOTAL=$((TOTAL + 1))
    if [ ! -e "vercel/vercel-skills-plugin/skills" ]; then
        echo "  ❌ vercel/vercel-skills-plugin/skills (BROKEN)"
        BROKEN=$((BROKEN + 1))
    else
        echo "  ✓ vercel/vercel-skills-plugin/skills"
    fi
fi

# Google Labs wrapper
echo "→ Google Labs wrapper..."
if [ -L "google-labs-code/stitch-skills-plugin/skills" ]; then
    TOTAL=$((TOTAL + 1))
    if [ ! -e "google-labs-code/stitch-skills-plugin/skills" ]; then
        echo "  ❌ google-labs-code/stitch-skills-plugin/skills (BROKEN)"
        BROKEN=$((BROKEN + 1))
    else
        echo "  ✓ google-labs-code/stitch-skills-plugin/skills"
    fi
fi

# Microsoft wrappers
echo "→ Microsoft wrappers..."
for plugin_dir in microsoft/ms-skills-*-plugin/skills microsoft/ms-agents-plugin; do
    if [ -d "$plugin_dir" ]; then
        plugin_name=$(basename "$(dirname "$plugin_dir")" 2>/dev/null || basename "$plugin_dir")
        broken_in_plugin=0
        total_in_plugin=0
        
        for link in "$plugin_dir"/*; do
            if [ -L "$link" ]; then
                TOTAL=$((TOTAL + 1))
                total_in_plugin=$((total_in_plugin + 1))
                if [ ! -e "$link" ]; then
                    BROKEN=$((BROKEN + 1))
                    broken_in_plugin=$((broken_in_plugin + 1))
                fi
            fi
        done
        
        if [ $broken_in_plugin -gt 0 ]; then
            echo "  ❌ $plugin_name: $broken_in_plugin/$total_in_plugin broken"
        elif [ $total_in_plugin -gt 0 ]; then
            echo "  ✓ $plugin_name: $total_in_plugin symlinks healthy"
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $BROKEN -eq 0 ]; then
    echo "✅ All $TOTAL symlinks are healthy!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo "⚠️  Found $BROKEN broken symlinks out of $TOTAL total"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "To fix broken symlinks, run:"
    echo "  ./scripts/fix-symlinks.sh"
    exit 1
fi
