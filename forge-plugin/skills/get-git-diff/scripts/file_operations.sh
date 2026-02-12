#!/usr/bin/env bash
#
# Git File Operations Functions
#
# Functions for analyzing file operations in diffs (add, modify, delete, rename).
#
# Author: Claude Code get-git-diff skill
# Version: 0.2.0-alpha

set -euo pipefail

#######################################
# Get file operations (add, modify, delete, rename)
# Arguments:
#   $1 - first commit
#   $2 - second commit
#   $3 - detect renames (optional, default: true)
# Outputs:
#   File operations, one per line (status TAB path)
#######################################
get_file_operations() {
    local commit1="$1"
    local commit2="$2"
    local detect_renames="${3:-true}"
    local cmd="git diff --name-status"

    if [[ "${detect_renames}" == "true" ]]; then
        cmd="${cmd} -M"
    fi

    ${cmd} "${commit1}...${commit2}" 2>/dev/null
}

#######################################
# Count file operations by type
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Tab-separated: added modified deleted renamed copied
#######################################
count_file_operations() {
    local commit1="$1"
    local commit2="$2"
    local operations

    operations=$(get_file_operations "${commit1}" "${commit2}")

    local added=0 modified=0 deleted=0 renamed=0 copied=0

    while IFS= read -r line; do
        [[ -z "${line}" ]] && continue

        local status="${line:0:1}"
        case "${status}" in
            A) ((added++)) ;;
            M) ((modified++)) ;;
            D) ((deleted++)) ;;
            R) ((renamed++)) ;;
            C) ((copied++)) ;;
        esac
    done <<< "${operations}"

    echo "${added}	${modified}	${deleted}	${renamed}	${copied}"
}

#######################################
# Get files by operation type
# Arguments:
#   $1 - first commit
#   $2 - second commit
#   $3 - operation type (A, M, D, R, C)
# Outputs:
#   List of files, one per line
#######################################
get_files_by_operation() {
    local commit1="$1"
    local commit2="$2"
    local operation_type="$3"
    local operations

    operations=$(get_file_operations "${commit1}" "${commit2}")

    echo "${operations}" | awk -v op="${operation_type}" '$1 ~ "^"op {print $2}'
}

#######################################
# Get renamed files with old and new paths
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Tab-separated: similarity old_path new_path (one per line)
#######################################
get_renamed_files() {
    local commit1="$1"
    local commit2="$2"
    local operations

    operations=$(get_file_operations "${commit1}" "${commit2}" true)

    echo "${operations}" | awk '
        /^R[0-9]+/ {
            similarity = substr($1, 2)
            old_path = $2
            new_path = $3
            print similarity "\t" old_path "\t" new_path
        }
    '
}

#######################################
# Get binary files in diff
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   List of binary file paths, one per line
#######################################
get_binary_files() {
    local commit1="$1"
    local commit2="$2"
    local numstat

    if numstat=$(git diff --numstat "${commit1}...${commit2}" 2>/dev/null); then
        echo "${numstat}" | awk '$1 == "-" && $2 == "-" {print $3}'
    fi
}

#######################################
# Count binary files
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Number of binary files
#######################################
count_binary_files() {
    local commit1="$1"
    local commit2="$2"

    get_binary_files "${commit1}" "${commit2}" | wc -l | tr -d ' '
}

#######################################
# Categorize files by type
# Arguments:
#   Reads file paths from stdin, one per line
# Outputs:
#   Tab-separated: source tests docs config database other
#######################################
categorize_files() {
    local source=0 tests=0 docs=0 config=0 database=0 other=0

    while IFS= read -r path; do
        [[ -z "${path}" ]] && continue

        # Categorize based on path and extension
        if [[ "${path}" =~ test|tests/ ]]; then
            ((tests++))
        elif [[ "${path}" =~ \.md$|doc ]]; then
            ((docs++))
        elif [[ "${path}" =~ config|settings|\.env|\.ya?ml$|\.json$|\.toml$|\.ini$ ]]; then
            ((config++))
        elif [[ "${path}" =~ migration|schema|models ]]; then
            ((database++))
        elif [[ "${path}" =~ \.(py|js|ts|java|go|rs|cpp|c|rb|php|swift|kt)$ ]]; then
            ((source++))
        else
            ((other++))
        fi
    done

    echo "${source}	${tests}	${docs}	${config}	${database}	${other}"
}

#######################################
# Get categorized file counts from diff
# Arguments:
#   $1 - first commit
#   $2 - second commit
# Outputs:
#   Tab-separated category counts
#######################################
get_categorized_counts() {
    local commit1="$1"
    local commit2="$2"

    get_file_operations "${commit1}" "${commit2}" | cut -f2 | categorize_files
}

# Allow script to be sourced or run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Example usage
    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <commit1> <commit2>"
        echo ""
        echo "Examples:"
        echo "  $0 HEAD^ HEAD"
        echo "  $0 main feature-branch"
        exit 1
    fi

    commit1="$1"
    commit2="$2"

    echo "=== File Operations: ${commit1} → ${commit2} ==="
    counts=$(count_file_operations "${commit1}" "${commit2}")
    IFS=$'\t' read -r added modified deleted renamed copied <<< "${counts}"

    echo "Added: ${added}"
    echo "Modified: ${modified}"
    echo "Deleted: ${deleted}"
    echo "Renamed: ${renamed}"
    echo "Copied: ${copied}"

    binary_count=$(count_binary_files "${commit1}" "${commit2}")
    echo "Binary: ${binary_count}"

    if [[ ${added} -gt 0 ]]; then
        echo ""
        echo "=== Added Files ==="
        get_files_by_operation "${commit1}" "${commit2}" "A" | head -10
        if [[ ${added} -gt 10 ]]; then
            echo "  ... and $((added - 10)) more"
        fi
    fi

    if [[ ${renamed} -gt 0 ]]; then
        echo ""
        echo "=== Renamed Files ==="
        get_renamed_files "${commit1}" "${commit2}" | head -10 | while IFS=$'\t' read -r sim old new; do
            echo "  ${old} → ${new} (${sim}%)"
        done
        if [[ ${renamed} -gt 10 ]]; then
            echo "  ... and $((renamed - 10)) more"
        fi
    fi

    echo ""
    echo "=== File Categorization ==="
    categories=$(get_categorized_counts "${commit1}" "${commit2}")
    IFS=$'\t' read -r source tests docs config database other <<< "${categories}"
    echo "Source code: ${source}"
    echo "Tests: ${tests}"
    echo "Documentation: ${docs}"
    echo "Configuration: ${config}"
    echo "Database: ${database}"
    echo "Other: ${other}"
fi
