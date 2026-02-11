#!/usr/bin/env bash
#
# Git Validation Functions
#
# Functions for validating git repositories and commit references.
#
# Author: Claude Code get-git-diff skill
# Version: 0.1.0-alpha

set -euo pipefail

#######################################
# Check if in a git repository
# Returns:
#   0 if in git repo, 1 if not
#######################################
is_git_repo() {
    git rev-parse --is-inside-work-tree >/dev/null 2>&1
}

#######################################
# Validate that a commit reference exists
# Arguments:
#   $1 - commit reference (hash, branch, tag)
# Returns:
#   0 if valid, 1 if invalid
# Outputs:
#   Full commit hash if valid, error message to stderr if invalid
#######################################
validate_commit() {
    local commit_ref="$1"
    local full_hash

    if full_hash=$(git rev-parse --verify "${commit_ref}" 2>/dev/null); then
        echo "${full_hash}"
        return 0
    else
        echo "Error: Invalid commit reference: ${commit_ref}" >&2
        return 1
    fi
}

#######################################
# Validate two commit references
# Arguments:
#   $1 - first commit reference
#   $2 - second commit reference
# Returns:
#   0 if both valid, 1 if either invalid
# Outputs:
#   Tab-separated full hashes if valid
#######################################
validate_commit_pair() {
    local commit1="$1"
    local commit2="$2"
    local hash1 hash2

    if hash1=$(validate_commit "${commit1}") && hash2=$(validate_commit "${commit2}"); then
        echo "${hash1}	${hash2}"
        return 0
    else
        return 1
    fi
}

# Allow script to be sourced or run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Example usage
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 <commit-ref> [<commit-ref2>]"
        echo ""
        echo "Examples:"
        echo "  $0 HEAD"
        echo "  $0 abc123 def456"
        exit 1
    fi

    if is_git_repo; then
        if [[ $# -eq 1 ]]; then
            validate_commit "$1"
        else
            validate_commit_pair "$1" "$2"
        fi
    else
        echo "Error: Not in a git repository" >&2
        exit 1
    fi
fi
