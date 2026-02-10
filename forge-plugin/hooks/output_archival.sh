#!/bin/bash
# Archive skill output files from /claudedocs
#
# Usage: bash output_archival.sh [claudedocs_dir]
#
# Behavior:
# 1. Copy new output files to /claudedocs/archive/{YYYY-MM}/
# 2. Append entry to /claudedocs/archive/manifest.md
# 3. Clean archives older than 30 days

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORGE_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT=$(git -C "$FORGE_DIR" rev-parse --show-toplevel 2>/dev/null || dirname "$FORGE_DIR")
CLAUDEDOCS="${1:-$REPO_ROOT/claudedocs}"
TODAY=$(date +%Y-%m-%d)
YEAR_MONTH=$(date +%Y-%m)
ARCHIVE_DIR="$CLAUDEDOCS/archive/$YEAR_MONTH"
MANIFEST="$CLAUDEDOCS/archive/manifest.md"

# Exit if no claudedocs directory
if [[ ! -d "$CLAUDEDOCS" ]]; then
    exit 0
fi

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Initialize manifest if it doesn't exist
if [[ ! -f "$MANIFEST" ]]; then
    {
        echo "# Output Archive Manifest"
        echo ""
        echo "Automated archive of skill output files from /claudedocs."
        echo ""
        echo "---"
        echo ""
    } > "$MANIFEST"
fi

# Find output files modified in last 10 minutes (not in archive/)
ARCHIVED_COUNT=0
while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    BASENAME=$(basename "$file")

    # Skip manifest and non-output files
    [[ "$BASENAME" == "manifest.md" ]] && continue

    # Copy to archive
    cp "$file" "$ARCHIVE_DIR/$BASENAME"
    ARCHIVED_COUNT=$((ARCHIVED_COUNT + 1))

    # Append to manifest
    {
        echo "- **$TODAY** | \`$YEAR_MONTH/$BASENAME\` | Archived from \`$BASENAME\`"
    } >> "$MANIFEST"

done < <(find "$CLAUDEDOCS" -maxdepth 1 -name "*.md" -mmin -10 -type f 2>/dev/null)

# Clean old archives (older than 30 days)
if [[ -d "$CLAUDEDOCS/archive" ]]; then
    find "$CLAUDEDOCS/archive" -type f -mtime +30 -delete 2>/dev/null || true
    # Remove empty month directories
    find "$CLAUDEDOCS/archive" -type d -empty -delete 2>/dev/null || true
fi

if [[ "$ARCHIVED_COUNT" -gt 0 ]]; then
    echo "Archived $ARCHIVED_COUNT output file(s) to $ARCHIVE_DIR"
fi

exit 0
