#!/usr/bin/env bash
# detect_package_manager.sh - Detect which Python package manager a project uses
# Part of the python-dependency-management skill

set -euo pipefail

# Detect the package manager used by a Python project
# Priority: uv > poetry > conda > pipenv > pip
# Returns: Package manager name and version
detect_package_manager() {
    local project_dir="${1:-.}"

    cd "$project_dir" || {
        echo "ERROR: Cannot access directory: $project_dir" >&2
        return 1
    }

    # Check for uv
    if [[ -f "uv.lock" ]] || ( [[ -f "pyproject.toml" ]] && grep -q "tool.uv" pyproject.toml 2>/dev/null ); then
        if command -v uv &>/dev/null; then
            local uv_version
            uv_version=$(uv --version 2>/dev/null | awk '{print $2}')
            echo "uv|${uv_version:-unknown}"
            return 0
        else
            echo "WARNING: uv project detected but uv not installed" >&2
            # Fall through to check other managers
        fi
    fi

    # Check for Poetry
    if [[ -f "poetry.lock" ]] || ( [[ -f "pyproject.toml" ]] && grep -q "\[tool.poetry\]" pyproject.toml 2>/dev/null ); then
        if command -v poetry &>/dev/null; then
            local poetry_version
            poetry_version=$(poetry --version 2>/dev/null | awk '{print $3}' | tr -d '()')
            echo "poetry|${poetry_version:-unknown}"
            return 0
        else
            echo "WARNING: Poetry project detected but poetry not installed" >&2
            # Fall through to check other managers
        fi
    fi

    # Check for Conda
    if [[ -f "environment.yml" ]] || [[ -f "environment.yaml" ]] || [[ -f "conda.yml" ]]; then
        if command -v conda &>/dev/null; then
            local conda_version
            conda_version=$(conda --version 2>/dev/null | awk '{print $2}')
            echo "conda|${conda_version:-unknown}"
            return 0
        else
            echo "WARNING: Conda environment file detected but conda not installed" >&2
            # Fall through to check other managers
        fi
    fi

    # Check for Pipenv
    if [[ -f "Pipfile" ]] || [[ -f "Pipfile.lock" ]]; then
        if command -v pipenv &>/dev/null; then
            local pipenv_version
            pipenv_version=$(pipenv --version 2>/dev/null | awk '{print $3}')
            echo "pipenv|${pipenv_version:-unknown}"
            return 0
        else
            echo "WARNING: Pipenv project detected but pipenv not installed" >&2
            # Fall through to pip
        fi
    fi

    # Check for PDM
    if [[ -f "pdm.lock" ]] || ( [[ -f "pyproject.toml" ]] && grep -q "\[tool.pdm\]" pyproject.toml 2>/dev/null ); then
        if command -v pdm &>/dev/null; then
            local pdm_version
            pdm_version=$(pdm --version 2>/dev/null | awk '{print $3}')
            echo "pdm|${pdm_version:-unknown}"
            return 0
        else
            echo "WARNING: PDM project detected but pdm not installed" >&2
            # Fall through to pip
        fi
    fi

    # Default to pip (always available in Python installations)
    if command -v pip &>/dev/null; then
        local pip_version
        pip_version=$(pip --version 2>/dev/null | awk '{print $2}')
        echo "pip|${pip_version:-unknown}"
        return 0
    elif command -v pip3 &>/dev/null; then
        local pip_version
        pip_version=$(pip3 --version 2>/dev/null | awk '{print $2}')
        echo "pip|${pip_version:-unknown}"
        return 0
    else
        echo "ERROR: No Python package manager found (not even pip)" >&2
        return 1
    fi
}

# Get the configuration file(s) used by the detected package manager
get_config_files() {
    local package_manager="$1"
    local project_dir="${2:-.}"

    cd "$project_dir" || return 1

    case "$package_manager" in
        uv)
            [[ -f "pyproject.toml" ]] && echo "pyproject.toml"
            [[ -f "uv.lock" ]] && echo "uv.lock"
            [[ -f "requirements.txt" ]] && echo "requirements.txt"
            ;;
        poetry)
            [[ -f "pyproject.toml" ]] && echo "pyproject.toml"
            [[ -f "poetry.lock" ]] && echo "poetry.lock"
            ;;
        conda)
            [[ -f "environment.yml" ]] && echo "environment.yml"
            [[ -f "environment.yaml" ]] && echo "environment.yaml"
            [[ -f "conda.yml" ]] && echo "conda.yml"
            ;;
        pipenv)
            [[ -f "Pipfile" ]] && echo "Pipfile"
            [[ -f "Pipfile.lock" ]] && echo "Pipfile.lock"
            ;;
        pdm)
            [[ -f "pyproject.toml" ]] && echo "pyproject.toml"
            [[ -f "pdm.lock" ]] && echo "pdm.lock"
            ;;
        pip)
            [[ -f "requirements.txt" ]] && echo "requirements.txt"
            [[ -f "requirements-dev.txt" ]] && echo "requirements-dev.txt"
            [[ -f "pyproject.toml" ]] && echo "pyproject.toml"
            [[ -f "setup.py" ]] && echo "setup.py"
            ;;
        *)
            echo "ERROR: Unknown package manager: $package_manager" >&2
            return 1
            ;;
    esac
}

# Check if a package manager is installed
is_package_manager_installed() {
    local package_manager="$1"

    case "$package_manager" in
        uv|poetry|conda|pipenv|pdm)
            command -v "$package_manager" &>/dev/null
            ;;
        pip)
            command -v pip &>/dev/null || command -v pip3 &>/dev/null
            ;;
        *)
            return 1
            ;;
    esac
}

# Main execution when run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "=== Package Manager Detection ==="
    echo

    project_dir="${1:-.}"
    echo "Project directory: $project_dir"
    echo

    result=$(detect_package_manager "$project_dir")
    manager=$(echo "$result" | cut -d'|' -f1)
    version=$(echo "$result" | cut -d'|' -f2)

    echo "Detected package manager: $manager"
    echo "Version: $version"
    echo

    echo "Configuration files:"
    get_config_files "$manager" "$project_dir"
    echo

    echo "Installation status:"
    if is_package_manager_installed "$manager"; then
        echo "✓ $manager is installed and available"
    else
        echo "✗ $manager is NOT installed"
    fi
fi
