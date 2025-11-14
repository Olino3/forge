#!/usr/bin/env bash
# utils.sh - Utility functions for python-dependency-management skill
# Part of the python-dependency-management skill

set -euo pipefail

# Get the project name from git repository or directory name
get_project_name() {
    local project_dir="${1:-.}"

    cd "$project_dir" || {
        echo "ERROR: Cannot access directory: $project_dir" >&2
        return 1
    }

    # Try to get from git repository name
    if git rev-parse --git-dir &>/dev/null; then
        basename "$(git rev-parse --show-toplevel)" 2>/dev/null && return 0
    fi

    # Fallback to directory name
    basename "$(pwd)"
}

# Get Python version from system or virtual environment
get_python_version() {
    local venv_path="${1:-}"

    if [[ -n "$venv_path" ]] && [[ -f "$venv_path/bin/python" ]]; then
        "$venv_path/bin/python" --version 2>&1 | awk '{print $2}'
    elif [[ -n "$venv_path" ]] && [[ -f "$venv_path/Scripts/python.exe" ]]; then
        "$venv_path/Scripts/python.exe" --version 2>&1 | awk '{print $2}'
    elif command -v python &>/dev/null; then
        python --version 2>&1 | awk '{print $2}'
    elif command -v python3 &>/dev/null; then
        python3 --version 2>&1 | awk '{print $2}'
    else
        echo "unknown"
    fi
}

# Create a virtual environment
create_venv() {
    local venv_path="$1"
    local python_version="${2:-python3}"

    if [[ -d "$venv_path" ]]; then
        echo "ERROR: Virtual environment already exists at $venv_path" >&2
        return 1
    fi

    echo "Creating virtual environment at $venv_path..."

    if ! command -v "$python_version" &>/dev/null; then
        echo "ERROR: Python version '$python_version' not found" >&2
        return 1
    fi

    "$python_version" -m venv "$venv_path"

    if [[ $? -eq 0 ]]; then
        echo "✓ Virtual environment created successfully"
        return 0
    else
        echo "ERROR: Failed to create virtual environment" >&2
        return 1
    fi
}

# Create .gitignore entry for venv if needed
add_venv_to_gitignore() {
    local venv_name="$1"
    local project_dir="${2:-.}"

    cd "$project_dir" || return 1

    # Only add if in a git repository
    if ! git rev-parse --git-dir &>/dev/null; then
        return 0
    fi

    local gitignore=".gitignore"

    # Check if .gitignore exists
    if [[ ! -f "$gitignore" ]]; then
        echo "# Python virtual environment" > "$gitignore"
        echo "$venv_name/" >> "$gitignore"
        echo "✓ Created .gitignore with $venv_name"
        return 0
    fi

    # Check if venv already in .gitignore
    if grep -q "^${venv_name}/\?$" "$gitignore" 2>/dev/null; then
        return 0  # Already present
    fi

    # Add to .gitignore
    echo "" >> "$gitignore"
    echo "# Python virtual environment (added by Claude Code)" >> "$gitignore"
    echo "$venv_name/" >> "$gitignore"
    echo "✓ Added $venv_name to .gitignore"
}

# Parse package specification (name==version, name>=version, etc.)
parse_package_spec() {
    local package_spec="$1"

    # Extract package name (everything before version constraint)
    local package_name
    package_name=$(echo "$package_spec" | sed -E 's/([<>=!~]+).*//' | sed -E 's/\[.*\]$//')

    # Extract version constraint (everything after package name)
    local version_constraint
    version_constraint=$(echo "$package_spec" | sed -E 's/^[a-zA-Z0-9_-]+(\[.*\])?//')

    echo "$package_name|$version_constraint"
}

# Format package list for display
format_package_list() {
    local packages=("$@")

    if [[ ${#packages[@]} -eq 0 ]]; then
        echo "  (none)"
        return
    fi

    for pkg in "${packages[@]}"; do
        echo "  - $pkg"
    done
}

# Check if we're in a git repository
is_git_repo() {
    git rev-parse --git-dir &>/dev/null
}

# Get timestamp for file naming
get_timestamp() {
    date +%Y%m%d-%H%M%S
}

# Sanitize project name for use in file names
sanitize_project_name() {
    local project_name="$1"
    echo "$project_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]/-/g'
}

# Detect OS type
get_os_type() {
    case "$OSTYPE" in
        linux*)   echo "linux" ;;
        darwin*)  echo "macos" ;;
        msys*)    echo "windows" ;;
        win32*)   echo "windows" ;;
        cygwin*)  echo "windows" ;;
        *)        echo "unknown" ;;
    esac
}

# Check if running in CI/CD environment
is_ci_environment() {
    [[ -n "${CI:-}" ]] || \
    [[ -n "${GITHUB_ACTIONS:-}" ]] || \
    [[ -n "${GITLAB_CI:-}" ]] || \
    [[ -n "${JENKINS_HOME:-}" ]] || \
    [[ -n "${CIRCLECI:-}" ]]
}

# Create memory directory structure for a project
create_memory_structure() {
    local project_name="$1"
    local skill_dir="$2"

    local memory_dir="$skill_dir/../../memory/skills/python-dependency-management/$project_name"

    if [[ -d "$memory_dir" ]]; then
        echo "Memory directory already exists: $memory_dir"
        return 0
    fi

    mkdir -p "$memory_dir"
    echo "✓ Created memory directory: $memory_dir"
}

# Generate output filename for reports
generate_output_filename() {
    local project_name="$1"
    local operation="$2"

    local sanitized_name
    sanitized_name=$(sanitize_project_name "$project_name")

    local timestamp
    timestamp=$(get_timestamp)

    echo "dependency-${operation}-${sanitized_name}-${timestamp}.md"
}

# Check if a package name is valid
is_valid_package_name() {
    local package_name="$1"

    # Python package names: lowercase letters, digits, hyphens, underscores
    # Must start with a letter
    if [[ "$package_name" =~ ^[a-zA-Z][a-zA-Z0-9_-]*$ ]]; then
        return 0
    else
        return 1
    fi
}

# Extract package names from a requirements.txt file
extract_packages_from_requirements() {
    local requirements_file="$1"

    if [[ ! -f "$requirements_file" ]]; then
        echo "ERROR: Requirements file not found: $requirements_file" >&2
        return 1
    fi

    # Extract package names (ignore comments, blank lines, and options)
    grep -v '^#' "$requirements_file" | \
        grep -v '^[[:space:]]*$' | \
        grep -v '^-' | \
        sed -E 's/([<>=!~]+).*//' | \
        sed -E 's/\[.*\]$//' | \
        tr -d '[:space:]'
}

# Count installed packages
count_installed_packages() {
    local package_manager="$1"

    case "$package_manager" in
        uv)
            uv pip list 2>/dev/null | tail -n +3 | wc -l
            ;;
        poetry)
            poetry show 2>/dev/null | wc -l
            ;;
        conda)
            local env_arg=""
            if [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
                env_arg="-n $CONDA_DEFAULT_ENV"
            fi
            conda list $env_arg 2>/dev/null | tail -n +4 | wc -l
            ;;
        pip)
            local pip_cmd="pip"
            if ! command -v pip &>/dev/null && command -v pip3 &>/dev/null; then
                pip_cmd="pip3"
            fi
            $pip_cmd list 2>/dev/null | tail -n +3 | wc -l
            ;;
        *)
            echo "0"
            ;;
    esac
}

# Check for common issues in the environment
check_environment_health() {
    echo "=== Environment Health Check ==="
    echo

    # Check Python installation
    if command -v python &>/dev/null; then
        echo "✓ Python: $(python --version 2>&1)"
    elif command -v python3 &>/dev/null; then
        echo "✓ Python3: $(python3 --version 2>&1)"
    else
        echo "✗ Python not found"
    fi

    # Check pip
    if command -v pip &>/dev/null; then
        echo "✓ pip: $(pip --version 2>&1 | awk '{print $2}')"
    elif command -v pip3 &>/dev/null; then
        echo "✓ pip3: $(pip3 --version 2>&1 | awk '{print $2}')"
    else
        echo "✗ pip not found"
    fi

    # Check virtual environment status
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
        echo "✓ Virtual environment active: $VIRTUAL_ENV"
    elif [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
        echo "✓ Conda environment active: $CONDA_DEFAULT_ENV"
    else
        echo "⚠ No virtual environment active"
    fi

    # Check for package managers
    local managers=("uv" "poetry" "conda" "pipenv" "pdm")
    local found_managers=()

    for mgr in "${managers[@]}"; do
        if command -v "$mgr" &>/dev/null; then
            found_managers+=("$mgr")
        fi
    done

    if [[ ${#found_managers[@]} -gt 0 ]]; then
        echo "✓ Package managers available: ${found_managers[*]}"
    fi

    echo
}

# Main execution when run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "=== Python Dependency Management Utilities ==="
    echo

    project_dir="${1:-.}"

    echo "Project name: $(get_project_name "$project_dir")"
    echo "Python version: $(get_python_version)"
    echo "OS type: $(get_os_type)"
    echo "CI environment: $(is_ci_environment && echo "yes" || echo "no")"
    echo "Git repository: $(is_git_repo && echo "yes" || echo "no")"
    echo

    check_environment_health
fi
