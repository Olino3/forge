#!/usr/bin/env bash
#
# Git Diff Statistics Functions
#
# Functions for calculating and analyzing diff statistics.
#
# Author: Claude Code get-git-diff skill
# Version: 0.1.0-alpha

set -euo pipefail

#######################################
# Get diff statistics between two commits
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Tab-separated: files_changed insertions deletions net_change
#######################################
get_diff_stats() {
    local commit1="$1"
    local commit2="$2"
    local shortstat

    if shortstat=$(git diff --shortstat "${commit1}...${commit2}" 2>/dev/null); then
        local files=0 insertions=0 deletions=0

        # Parse: "3 files changed, 165 insertions(+), 20 deletions(-)"
        if [[ ${shortstat} =~ ([0-9]+)\ files?\ changed ]]; then
            files="${BASH_REMATCH[1]}"
        fi
        if [[ ${shortstat} =~ ([0-9]+)\ insertions? ]]; then
            insertions="${BASH_REMATCH[1]}"
        fi
        if [[ ${shortstat} =~ ([0-9]+)\ deletions? ]]; then
            deletions="${BASH_REMATCH[1]}"
        fi

        local net_change=$((insertions - deletions))
        echo "${files}	${insertions}	${deletions}	${net_change}"
    else
        echo "0	0	0	0"
    fi
}

#######################################
# Get detailed per-file statistics
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Tab-separated: insertions deletions filename (one per line)
#######################################
get_file_stats() {
    local commit1="$1"
    local commit2="$2"

    git diff --numstat "${commit1}...${commit2}" 2>/dev/null
}

#######################################
# Check if diff is large (exceeds threshold)
# Arguments:
#   $1 - first commit
#   $2 - second commit
#   $3 - threshold (optional, default: 1000)
# Returns:
#   0 if large, 1 if not
# Outputs:
#   Total line count if large
#######################################
is_large_diff() {
    local commit1="$1"
    local commit2="$2"
    local threshold="${3:-1000}"
    local stats

    if stats=$(get_diff_stats "${commit1}" "${commit2}"); then
        local insertions deletions total_lines
        insertions=$(echo "${stats}" | cut -f2)
        deletions=$(echo "${stats}" | cut -f3)
        total_lines=$((insertions + deletions))

        if [[ ${total_lines} -gt ${threshold} ]]; then
            echo "${total_lines}"
            return 0
        fi
    fi

    return 1
}

#######################################
# Get total line count in diff
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Total lines changed (insertions + deletions)
#######################################
get_total_lines() {
    local commit1="$1"
    local commit2="$2"
    local stats

    if stats=$(get_diff_stats "${commit1}" "${commit2}"); then
        local insertions deletions
        insertions=$(echo "${stats}" | cut -f2)
        deletions=$(echo "${stats}" | cut -f3)
        echo $((insertions + deletions))
    else
        echo "0"
    fi
}

#######################################
# Get files changed count
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Number of files changed
#######################################
get_files_changed() {
    local commit1="$1"
    local commit2="$2"
    local stats

    if stats=$(get_diff_stats "${commit1}" "${commit2}"); then
        echo "${stats}" | cut -f1
    else
        echo "0"
    fi
}

# Allow script to be sourced or run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Example usage
    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <commit1> <commit2> [threshold]"
        echo ""
        echo "Examples:"
        echo "  $0 HEAD^ HEAD"
        echo "  $0 main feature-branch 500"
        exit 1
    fi

    commit1="$1"
    commit2="$2"
    threshold="${3:-1000}"

    echo "=== Diff Statistics: ${commit1} → ${commit2} ==="
    stats=$(get_diff_stats "${commit1}" "${commit2}")
    IFS=$'\t' read -r files ins del net <<< "${stats}"

    echo "Files changed: ${files}"
    echo "Insertions: +${ins}"
    echo "Deletions: -${del}"
    echo "Net change: ${net}"
    echo "Total lines: $((ins + del))"

    if is_large_diff "${commit1}" "${commit2}" "${threshold}"; then
        total=$(is_large_diff "${commit1}" "${commit2}" "${threshold}")
        echo "⚠ Large diff detected (${total} lines, threshold: ${threshold})"
    else
        echo "✓ Normal size diff (threshold: ${threshold})"
    fi

    echo ""
    echo "=== Top 10 Changed Files ==="
    get_file_stats "${commit1}" "${commit2}" | head -10 | while IFS=$'\t' read -r ins del file; do
        if [[ "${ins}" == "-" && "${del}" == "-" ]]; then
            echo "  ${file} (binary)"
        else
            echo "  ${file} (+${ins}, -${del})"
        fi
    done
fi
