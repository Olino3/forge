#!/bin/bash
# scripts/fix-symlinks.sh
# Recreates all wrapper plugin symlinks for external skill repositories

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$FORGE_ROOT"

echo "🔧 Fixing wrapper plugin symlinks..."
echo ""

# Vercel wrapper
echo "→ Vercel wrapper..."
mkdir -p vercel/vercel-skills-plugin
cd vercel/vercel-skills-plugin
rm -f skills
ln -sf ../agent-skills/skills skills
cd ../..
echo "  ✓ vercel/vercel-skills-plugin/skills"

# Google Labs wrapper
echo "→ Google Labs wrapper..."
mkdir -p google-labs-code/stitch-skills-plugin
cd google-labs-code/stitch-skills-plugin
rm -f skills
ln -sf ../stitch-skills/skills skills
cd ../..
echo "  ✓ google-labs-code/stitch-skills-plugin/skills"

# Microsoft Core plugin
echo "→ Microsoft Core plugin..."
mkdir -p microsoft/ms-skills-core-plugin/skills
cd microsoft/ms-skills-core-plugin/skills
for skill in ../../skills/.github/skills/{azd-deployment,copilot-sdk-guide,github-copilot-skills-plugin,mcp-builder,copilot-skills-prompt-guidelines,microsoft-foundry-skills-dev}; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        rm -f "$skill_name"
        ln -sf "$skill" "$skill_name"
    fi
done
cd ../../..
echo "  ✓ microsoft/ms-skills-core-plugin/skills (6 symlinks)"

# Microsoft Python plugin
echo "→ Microsoft Python plugin..."
mkdir -p microsoft/ms-skills-python-plugin/skills
cd microsoft/ms-skills-python-plugin/skills
count=0
for skill in ../../skills/.github/skills/*-py; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        rm -f "$skill_name"
        ln -sf "$skill" "$skill_name"
        count=$((count + 1))
    fi
done
cd ../../..
echo "  ✓ microsoft/ms-skills-python-plugin/skills ($count symlinks)"

# Microsoft .NET plugin
echo "→ Microsoft .NET plugin..."
mkdir -p microsoft/ms-skills-dotnet-plugin/skills
cd microsoft/ms-skills-dotnet-plugin/skills
count=0
for skill in ../../skills/.github/skills/*-dotnet; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        rm -f "$skill_name"
        ln -sf "$skill" "$skill_name"
        count=$((count + 1))
    fi
done
cd ../../..
echo "  ✓ microsoft/ms-skills-dotnet-plugin/skills ($count symlinks)"

# Microsoft TypeScript plugin
echo "→ Microsoft TypeScript plugin..."
mkdir -p microsoft/ms-skills-typescript-plugin/skills
cd microsoft/ms-skills-typescript-plugin/skills
count=0
for skill in ../../skills/.github/skills/*-ts; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        rm -f "$skill_name"
        ln -sf "$skill" "$skill_name"
        count=$((count + 1))
    fi
done
cd ../../..
echo "  ✓ microsoft/ms-skills-typescript-plugin/skills ($count symlinks)"

# Microsoft Java plugin
echo "→ Microsoft Java plugin..."
mkdir -p microsoft/ms-skills-java-plugin/skills
cd microsoft/ms-skills-java-plugin/skills
count=0
for skill in ../../skills/.github/skills/*-java; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        rm -f "$skill_name"
        ln -sf "$skill" "$skill_name"
        count=$((count + 1))
    fi
done
cd ../../..
echo "  ✓ microsoft/ms-skills-java-plugin/skills ($count symlinks)"

# Microsoft Rust plugin
echo "→ Microsoft Rust plugin..."
mkdir -p microsoft/ms-skills-rust-plugin/skills
cd microsoft/ms-skills-rust-plugin/skills
count=0
for skill in ../../skills/.github/skills/*-rust; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        rm -f "$skill_name"
        ln -sf "$skill" "$skill_name"
        count=$((count + 1))
    fi
done
cd ../../..
echo "  ✓ microsoft/ms-skills-rust-plugin/skills ($count symlinks)"

# Microsoft Agents plugin
echo "→ Microsoft Agents plugin..."
mkdir -p microsoft/ms-agents-plugin
cd microsoft/ms-agents-plugin
count=0
# Agent directories
for dir in ../skills/.github/agents/*; do
    if [ -d "$dir" ]; then
        dir_name=$(basename "$dir")
        rm -f "$dir_name"
        ln -sf "$dir" "$dir_name"
        count=$((count + 1))
    fi
done
# Deep-wiki plugin
if [ -d ../skills/.github/plugins/deep-wiki ]; then
    rm -f deep-wiki
    ln -sf ../skills/.github/plugins/deep-wiki deep-wiki
    count=$((count + 1))
fi
cd ../..
echo "  ✓ microsoft/ms-agents-plugin ($count symlinks)"

echo ""
echo "✅ All symlinks recreated successfully!"
