#!/usr/bin/env bash

# bump-version.sh — Automated version bumping across The Forge
#
# Usage: ./scripts/bump-version.sh NEW_VERSION
# Example: ./scripts/bump-version.sh 0.3.0-alpha

set -euo pipefail

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check arguments
if [ $# -ne 1 ]; then
    echo -e "${RED}Error: Missing version argument${NC}"
    echo "Usage: $0 NEW_VERSION"
    echo "Example: $0 0.3.0-alpha"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format (x.y.z or x.y.z-suffix)
if ! echo "$NEW_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$'; then
    echo -e "${RED}Error: Invalid version format${NC}"
    echo "Version must be in format: x.y.z or x.y.z-suffix"
    echo "Example: 0.3.0-alpha"
    exit 1
fi

# Read current version
if [ -f "$REPO_ROOT/VERSION" ]; then
    CURRENT_VERSION=$(cat "$REPO_ROOT/VERSION")
else
    CURRENT_VERSION="unknown"
fi

echo -e "${BLUE}⚒️  Version Bump${NC}"
echo -e "${YELLOW}Current version:${NC} $CURRENT_VERSION"
echo -e "${YELLOW}New version:${NC} $NEW_VERSION"
echo ""

# Update VERSION file
echo -e "${BLUE}Updating VERSION file...${NC}"
echo "$NEW_VERSION" > "$REPO_ROOT/VERSION"
echo -e "${GREEN}✓ VERSION file updated${NC}"

# Update plugin.json (canonical source)
echo -e "${BLUE}Updating plugin.json...${NC}"
PLUGIN_JSON="$REPO_ROOT/forge-plugin/.claude-plugin/plugin.json"
if [ -f "$PLUGIN_JSON" ]; then
    # Use jq for safe JSON manipulation if available
    if command -v jq &> /dev/null; then
        jq --arg version "$NEW_VERSION" '.version = $version' "$PLUGIN_JSON" > "${PLUGIN_JSON}.tmp"
        mv "${PLUGIN_JSON}.tmp" "$PLUGIN_JSON"
    else
        # Fallback to sed
        sed -i.bak "s/\"version\": \"[^\"]*\"/\"version\": \"$NEW_VERSION\"/" "$PLUGIN_JSON"
        rm -f "${PLUGIN_JSON}.bak"
    fi
    echo -e "${GREEN}✓ plugin.json updated${NC}"
else
    echo -e "${RED}✗ plugin.json not found${NC}"
fi

# Find and update all files containing the old version
echo -e "${BLUE}Searching for version references...${NC}"

# Escape dots for regex
CURRENT_VERSION_ESCAPED=$(echo "$CURRENT_VERSION" | sed 's/\./\\./g')
NEW_VERSION_ESCAPED=$(echo "$NEW_VERSION" | sed 's/\./\\./g')

# Files to update (excluding certain directories)
EXCLUDE_DIRS=(
    ".git"
    "node_modules"
    ".forge"
    "__pycache__"
    ".pytest_cache"
)

# Build find exclude expression
EXCLUDE_EXPR=""
for dir in "${EXCLUDE_DIRS[@]}"; do
    EXCLUDE_EXPR="$EXCLUDE_EXPR -path '*/$dir/*' -prune -o"
done

# Find all text files containing the current version
echo -e "${YELLOW}Scanning files...${NC}"
FILES_TO_UPDATE=()

while IFS= read -r -d '' file; do
    # Skip binary files
    if file "$file" | grep -q text; then
        if grep -q "$CURRENT_VERSION" "$file" 2>/dev/null; then
            FILES_TO_UPDATE+=("$file")
        fi
    fi
done < <(find "$REPO_ROOT" $EXCLUDE_EXPR -type f -print0 2>/dev/null)

if [ ${#FILES_TO_UPDATE[@]} -eq 0 ]; then
    echo -e "${YELLOW}No additional files to update${NC}"
else
    echo -e "${YELLOW}Found ${#FILES_TO_UPDATE[@]} files to update${NC}"

    for file in "${FILES_TO_UPDATE[@]}"; do
        # Skip VERSION file (already updated) and plugin.json (already updated)
        if [ "$file" == "$REPO_ROOT/VERSION" ] || [ "$file" == "$PLUGIN_JSON" ]; then
            continue
        fi

        # Update the file
        if sed -i.bak "s/$CURRENT_VERSION_ESCAPED/$NEW_VERSION_ESCAPED/g" "$file" 2>/dev/null; then
            rm -f "${file}.bak"
            echo -e "  ${GREEN}✓${NC} $(realpath --relative-to="$REPO_ROOT" "$file")"
        else
            echo -e "  ${RED}✗${NC} $(realpath --relative-to="$REPO_ROOT" "$file")"
        fi
    done
fi

echo ""
echo -e "${GREEN}✓ Version bump complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review changes: git diff"
echo "  2. Run tests: make test"
echo "  3. Commit: git add -A && git commit -m 'chore: bump version to $NEW_VERSION'"
echo "  4. Tag: git tag v$NEW_VERSION"
echo "  5. Push: git push && git push --tags"
