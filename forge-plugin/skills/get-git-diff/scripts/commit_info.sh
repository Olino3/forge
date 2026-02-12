#!/usr/bin/env bash
#
# Git Commit Information Functions
#
# Functions for retrieving commit metadata and relationships.
#
# Author: Claude Code get-git-diff skill
# Version: 0.2.0-alpha

set -euo pipefail

#######################################
# Get detailed information about a commit
# Arguments:
#   $1 - commit reference
# Outputs:
#   Pipe-separated: full_hash|short_hash|author_name|author_email|date|message
#######################################
get_commit_info() {
    local commit_ref="$1"
    local format="%H|%h|%an|%ae|%ad|%s"

    git log -1 --format="${format}" "${commit_ref}" 2>/dev/null
}

#######################################
# Get short hash from commit reference
# Arguments:
#   $1 - commit reference
#   $2 - length (optional, default: 7)
# Outputs:
#   Short hash
#######################################
get_short_hash() {
    local commit_ref="$1"
    local length="${2:-7}"

    git rev-parse --short="${length}" "${commit_ref}" 2>/dev/null
}

#######################################
# Check if a commit is a merge commit
# Arguments:
#   $1 - commit reference
# Returns:
#   0 if merge commit, 1 if not
# Outputs:
#   Parent hashes separated by spaces
#######################################
is_merge_commit() {
    local commit_ref="$1"
    local parents

    if parents=$(git log -1 --format="%P" "${commit_ref}" 2>/dev/null); then
        local parent_count=$(echo "${parents}" | wc -w)
        if [[ ${parent_count} -gt 1 ]]; then
            echo "${parents}"
            return 0
        fi
    fi

    return 1
}

#######################################
# Get number of commits between two refs
# Arguments:
#   $1 - first commit (older)
#   $2 - second commit (newer)
# Outputs:
#   Number of commits between them
#######################################
get_commits_between() {
    local commit1="$1"
    local commit2="$2"

    git rev-list --count "${commit1}..${commit2}" 2>/dev/null || echo "0"
}

#######################################
# Get commit message (first line)
# Arguments:
#   $1 - commit reference
# Outputs:
#   Commit message subject line
#######################################
get_commit_message() {
    local commit_ref="$1"

    git log -1 --format="%s" "${commit_ref}" 2>/dev/null
}

#######################################
# Get commit author
# Arguments:
#   $1 - commit reference
# Outputs:
#   Author name and email
#######################################
get_commit_author() {
    local commit_ref="$1"

    git log -1 --format="%an <%ae>" "${commit_ref}" 2>/dev/null
}

#######################################
# Get commit date
# Arguments:
#   $1 - commit reference
# Outputs:
#   Commit date
#######################################
get_commit_date() {
    local commit_ref="$1"

    git log -1 --format="%ad" "${commit_ref}" 2>/dev/null
}

# Allow script to be sourced or run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Example usage
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 <commit-ref> [<commit-ref2>]"
        echo ""
        echo "Examples:"
        echo "  $0 HEAD"
        echo "  $0 HEAD HEAD^"
        exit 1
    fi

    commit1="$1"
    commit2="${2:-}"

    echo "=== Commit Info for ${commit1} ==="
    info=$(get_commit_info "${commit1}")
    IFS='|' read -r full short author email date message <<< "${info}"
    echo "Full hash: ${full}"
    echo "Short hash: ${short}"
    echo "Author: ${author} <${email}>"
    echo "Date: ${date}"
    echo "Message: ${message}"

    if is_merge_commit "${commit1}"; then
        parents=$(is_merge_commit "${commit1}")
        echo "Merge commit: yes"
        echo "Parents: ${parents}"
    else
        echo "Merge commit: no"
    fi

    if [[ -n "${commit2}" ]]; then
        echo ""
        echo "=== Comparison: ${commit1} to ${commit2} ==="
        count=$(get_commits_between "${commit1}" "${commit2}")
        echo "Commits between: ${count}"
    fi
fi
