#!/usr/bin/env bash
#
# Git Utility Functions
#
# General utility functions for git operations and formatting.
#
# Author: Claude Code get-git-diff skill
# Version: 0.2.0-alpha

set -euo pipefail

#######################################
# Get current branch name
# Outputs:
#   Branch name, or "HEAD" if detached
#######################################
get_current_branch() {
    local branch

    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "HEAD")
    echo "${branch}"
}

#######################################
# Get default branch (main or master)
# Outputs:
#   Default branch name, or empty if not found
#######################################
get_default_branch() {
    if git rev-parse --verify main >/dev/null 2>&1; then
        echo "main"
    elif git rev-parse --verify master >/dev/null 2>&1; then
        echo "master"
    else
        echo ""
    fi
}

#######################################
# Format diff filename
# Arguments:
#   $1 - first commit short hash
#   $2 - second commit short hash
#   $3 - extension (optional, default: md)
# Outputs:
#   Formatted filename like "diff_abc123_def456.md"
#######################################
format_diff_filename() {
    local hash1="$1"
    local hash2="$2"
    local ext="${3:-md}"

    echo "diff_${hash1}_${hash2}.${ext}"
}

#######################################
# Get repository root directory
# Outputs:
#   Absolute path to repository root
#######################################
get_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null
}

#######################################
# Get repository name
# Outputs:
#   Name of the repository (directory name)
#######################################
get_repo_name() {
    local root

    root=$(get_repo_root)
    if [[ -n "${root}" ]]; then
        basename "${root}"
    fi
}

#######################################
# Get remote URL (if available)
# Arguments:
#   $1 - remote name (optional, default: origin)
# Outputs:
#   Remote URL or empty if not found
#######################################
get_remote_url() {
    local remote="${1:-origin}"

    git remote get-url "${remote}" 2>/dev/null || echo ""
}

#######################################
# Check if commit is reachable from another
# Arguments:
#   $1 - ancestor commit
#   $2 - descendant commit
# Returns:
#   0 if reachable, 1 if not
#######################################
is_ancestor() {
    local ancestor="$1"
    local descendant="$2"

    git merge-base --is-ancestor "${ancestor}" "${descendant}" 2>/dev/null
}

#######################################
# Get common ancestor of two commits
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Common ancestor commit hash
#######################################
get_common_ancestor() {
    local commit1="$1"
    local commit2="$2"

    git merge-base "${commit1}" "${commit2}" 2>/dev/null
}

#######################################
# Format timestamp
# Arguments:
#   $1 - format (optional, default: "%Y-%m-%d %H:%M:%S")
# Outputs:
#   Formatted current timestamp
#######################################
format_timestamp() {
    local format="${1:-%Y-%m-%d %H:%M:%S}"

    date "+${format}"
}

#######################################
# Create directory if it doesn't exist
# Arguments:
#   $1 - directory path
# Returns:
#   0 if successful or already exists
#######################################
ensure_directory() {
    local dir="$1"

    if [[ ! -d "${dir}" ]]; then
        mkdir -p "${dir}"
    fi
}

#######################################
# Get git config value
# Arguments:
#   $1 - config key (e.g., user.name)
# Outputs:
#   Config value or empty if not set
#######################################
get_git_config() {
    local key="$1"

    git config --get "${key}" 2>/dev/null || echo ""
}

#######################################
# Check if working directory is clean
# Returns:
#   0 if clean, 1 if dirty
#######################################
is_working_tree_clean() {
    git diff-index --quiet HEAD -- 2>/dev/null
}

#######################################
# Get list of all branches
# Arguments:
#   $1 - type: "local", "remote", or "all" (default: local)
# Outputs:
#   List of branches, one per line
#######################################
get_branches() {
    local type="${1:-local}"

    case "${type}" in
        local)
            git branch --format='%(refname:short)' 2>/dev/null
            ;;
        remote)
            git branch -r --format='%(refname:short)' 2>/dev/null
            ;;
        all)
            git branch -a --format='%(refname:short)' 2>/dev/null
            ;;
        *)
            echo "Error: Invalid branch type: ${type}" >&2
            return 1
            ;;
    esac
}

#######################################
# Check if ref exists
# Arguments:
#   $1 - ref name (branch, tag, commit)
# Returns:
#   0 if exists, 1 if not
#######################################
ref_exists() {
    local ref="$1"

    git rev-parse --verify "${ref}" >/dev/null 2>&1
}

# Allow script to be sourced or run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Example usage
    echo "=== Git Repository Utilities ==="
    echo ""

    echo "Current branch: $(get_current_branch)"
    echo "Default branch: $(get_default_branch)"
    echo "Repository root: $(get_repo_root)"
    echo "Repository name: $(get_repo_name)"

    remote_url=$(get_remote_url)
    if [[ -n "${remote_url}" ]]; then
        echo "Remote URL (origin): ${remote_url}"
    fi

    echo ""
    echo "Git user name: $(get_git_config user.name)"
    echo "Git user email: $(get_git_config user.email)"

    echo ""
    if is_working_tree_clean; then
        echo "Working tree: clean"
    else
        echo "Working tree: dirty (uncommitted changes)"
    fi

    echo ""
    echo "Example filename: $(format_diff_filename "abc123" "def456")"
    echo "Current timestamp: $(format_timestamp)"

    echo ""
    echo "=== Local Branches ==="
    get_branches local | head -5
    local_count=$(get_branches local | wc -l)
    if [[ ${local_count} -gt 5 ]]; then
        echo "  ... and $((local_count - 5)) more"
    fi
fi
