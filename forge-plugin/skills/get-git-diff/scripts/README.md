# Git Diff Helper Scripts

This directory contains bash utility scripts for git diff operations used by the get-git-diff skill.

## Scripts Overview

### validate.sh
Validation and verification functions.

**Functions:**
- `is_git_repo()` - Check if in a git repository
- `validate_commit <ref>` - Validate a commit reference
- `validate_commit_pair <ref1> <ref2>` - Validate two commits

**Usage:**
```bash
source validate.sh
if is_git_repo; then
    validate_commit "HEAD"
fi
```

### commit_info.sh
Commit information and metadata retrieval.

**Functions:**
- `get_commit_info <ref>` - Get full commit information
- `get_short_hash <ref>` - Get 7-character hash
- `is_merge_commit <ref>` - Check if merge commit
- `get_commits_between <ref1> <ref2>` - Count commits between refs
- `get_commit_message <ref>` - Get commit message
- `get_commit_author <ref>` - Get commit author
- `get_commit_date <ref>` - Get commit date

**Usage:**
```bash
source commit_info.sh
info=$(get_commit_info "HEAD")
IFS='|' read -r full short author email date message <<< "$info"
echo "Commit: $short - $message"
```

### diff_stats.sh
Diff statistics and analysis.

**Functions:**
- `get_diff_stats <ref1> <ref2>` - Get diff statistics
- `get_file_stats <ref1> <ref2>` - Get per-file statistics
- `is_large_diff <ref1> <ref2> [threshold]` - Check if diff is large
- `get_total_lines <ref1> <ref2>` - Get total lines changed
- `get_files_changed <ref1> <ref2>` - Get file count

**Usage:**
```bash
source diff_stats.sh
stats=$(get_diff_stats "HEAD^" "HEAD")
IFS=$'\t' read -r files ins del net <<< "$stats"
echo "Changed: $files files, +$ins -$del"
```

### file_operations.sh
File operation analysis (add, modify, delete, rename).

**Functions:**
- `get_file_operations <ref1> <ref2>` - Get file operations
- `count_file_operations <ref1> <ref2>` - Count operations by type
- `get_files_by_operation <ref1> <ref2> <type>` - Filter by operation (A/M/D/R)
- `get_renamed_files <ref1> <ref2>` - Get renames with similarity
- `get_binary_files <ref1> <ref2>` - Get binary files
- `count_binary_files <ref1> <ref2>` - Count binary files
- `categorize_files` - Categorize files by type (reads from stdin)
- `get_categorized_counts <ref1> <ref2>` - Get category counts

**Usage:**
```bash
source file_operations.sh
counts=$(count_file_operations "main" "feature-branch")
IFS=$'\t' read -r added modified deleted renamed copied <<< "$counts"
echo "Added: $added, Modified: $modified"
```

### utils.sh
General utility functions.

**Functions:**
- `get_current_branch()` - Get current branch name
- `get_default_branch()` - Get default branch (main/master)
- `format_diff_filename <hash1> <hash2>` - Format output filename
- `get_repo_root()` - Get repository root path
- `get_repo_name()` - Get repository name
- `get_remote_url [remote]` - Get remote URL
- `is_ancestor <ref1> <ref2>` - Check if ref1 is ancestor of ref2
- `get_common_ancestor <ref1> <ref2>` - Get merge base
- `format_timestamp [format]` - Format current timestamp
- `ensure_directory <path>` - Create directory if needed
- `get_git_config <key>` - Get git config value
- `is_working_tree_clean()` - Check for uncommitted changes
- `get_branches [type]` - List branches (local/remote/all)
- `ref_exists <ref>` - Check if ref exists

**Usage:**
```bash
source utils.sh
branch=$(get_current_branch)
filename=$(format_diff_filename "abc123" "def456")
```

## Running Scripts Directly

All scripts can be sourced for their functions or run directly for examples:

```bash
# Run directly for examples
./commit_info.sh HEAD
./diff_stats.sh HEAD^ HEAD
./file_operations.sh main feature-branch
./utils.sh

# Source for functions
source diff_stats.sh
if is_large_diff "HEAD^" "HEAD" 500; then
    echo "Large diff detected!"
fi
```

## Complete Example

```bash
#!/usr/bin/env bash

# Source all helper scripts
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
source "${SCRIPT_DIR}/validate.sh"
source "${SCRIPT_DIR}/commit_info.sh"
source "${SCRIPT_DIR}/diff_stats.sh"
source "${SCRIPT_DIR}/file_operations.sh"
source "${SCRIPT_DIR}/utils.sh"

# Validate we're in a git repo
if ! is_git_repo; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Get commits to compare
commit1="HEAD^"
commit2="HEAD"

# Validate commits
if ! validate_commit_pair "$commit1" "$commit2" >/dev/null; then
    echo "Error: Invalid commits"
    exit 1
fi

# Get commit info
info1=$(get_commit_info "$commit1")
info2=$(get_commit_info "$commit2")
IFS='|' read -r _ short1 _ _ _ msg1 <<< "$info1"
IFS='|' read -r _ short2 _ _ _ msg2 <<< "$info2"

echo "Comparing: $short1 → $short2"

# Get statistics
stats=$(get_diff_stats "$commit1" "$commit2")
IFS=$'\t' read -r files ins del net <<< "$stats"

echo "Files: $files"
echo "Changes: +$ins -$del (net: $net)"

# Check if large
if is_large_diff "$commit1" "$commit2"; then
    total=$(is_large_diff "$commit1" "$commit2")
    echo "⚠ Large diff: $total lines"
fi

# File operations
ops=$(count_file_operations "$commit1" "$commit2")
IFS=$'\t' read -r added modified deleted renamed _ <<< "$ops"

echo "Added: $added, Modified: $modified"
if [[ $renamed -gt 0 ]]; then
    echo "Renamed files:"
    get_renamed_files "$commit1" "$commit2" | while IFS=$'\t' read -r sim old new; do
        echo "  $old → $new ($sim%)"
    done
fi

# Generate filename
filename=$(format_diff_filename "$short1" "$short2")
echo "Output: $filename"
```

## Error Handling

All scripts use `set -euo pipefail` for strict error handling:
- `-e`: Exit on error
- `-u`: Exit on undefined variable
- `-o pipefail`: Fail on pipe errors

When sourcing, you may want to disable this:
```bash
set +euo pipefail
source diff_stats.sh
set -euo pipefail
```

## Dependencies

- bash 4.0+
- git 2.0+
- Standard Unix utilities (awk, sed, cut, wc)

## Testing

Each script includes a main section that runs when executed directly:

```bash
# Test all scripts
./validate.sh HEAD
./commit_info.sh HEAD HEAD^
./diff_stats.sh HEAD^ HEAD
./file_operations.sh HEAD^ HEAD
./utils.sh
```

## Integration with Skill

These scripts are designed to be used by Claude Code when executing the get-git-diff skill. They provide reliable, composable functions for git diff analysis.

Example integration:
```bash
# In skill execution
source scripts/validate.sh
source scripts/diff_stats.sh

if validate_commit "$user_commit"; then
    stats=$(get_diff_stats "$user_commit" "HEAD")
    # Process stats...
fi
```
