#!/usr/bin/env bash
# detect_venv.sh - Detect Python virtual environments in a project
# Part of the python-dependency-management skill

set -euo pipefail

# Detect virtual environment in a project directory
# Checks common venv locations and Poetry/Conda environments
# Returns: venv_type|venv_path|python_version
detect_venv() {
    local project_dir="${1:-.}"

    cd "$project_dir" || {
        echo "ERROR: Cannot access directory: $project_dir" >&2
        return 1
    }

    # Check for standard venv directories in project
    local venv_candidates=(".venv" "venv" ".claude-venv" "env" ".env")

    for venv_name in "${venv_candidates[@]}"; do
        if [[ -d "$venv_name" ]] && [[ -f "$venv_name/bin/activate" || -f "$venv_name/Scripts/activate" ]]; then
            local python_version
            if [[ -f "$venv_name/bin/python" ]]; then
                python_version=$("$venv_name/bin/python" --version 2>&1 | awk '{print $2}')
            elif [[ -f "$venv_name/Scripts/python.exe" ]]; then
                python_version=$("$venv_name/Scripts/python.exe" --version 2>&1 | awk '{print $2}')
            else
                python_version="unknown"
            fi
            echo "venv|$(realpath "$venv_name")|$python_version"
            return 0
        fi
    done

    # Check for Poetry-managed virtual environment
    if command -v poetry &>/dev/null && [[ -f "pyproject.toml" ]]; then
        local poetry_venv
        poetry_venv=$(poetry env info -p 2>/dev/null || echo "")
        if [[ -n "$poetry_venv" ]] && [[ -d "$poetry_venv" ]]; then
            local python_version
            python_version=$(poetry env info -p 2>/dev/null && poetry run python --version 2>&1 | awk '{print $2}' || echo "unknown")
            echo "poetry|$poetry_venv|$python_version"
            return 0
        fi
    fi

    # Check for active Conda environment
    if [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
        local conda_prefix="${CONDA_PREFIX:-unknown}"
        local python_version="unknown"
        if command -v python &>/dev/null; then
            python_version=$(python --version 2>&1 | awk '{print $2}')
        fi
        echo "conda|$conda_prefix|$python_version"
        return 0
    fi

    # Check for Conda environment files
    if command -v conda &>/dev/null; then
        for env_file in environment.yml environment.yaml conda.yml; do
            if [[ -f "$env_file" ]]; then
                # Try to extract environment name from file
                local env_name
                env_name=$(grep -E "^name:" "$env_file" 2>/dev/null | awk '{print $2}' || echo "")
                if [[ -n "$env_name" ]]; then
                    # Check if environment exists
                    if conda env list | grep -q "^$env_name "; then
                        local conda_prefix
                        conda_prefix=$(conda env list | grep "^$env_name " | awk '{print $2}')
                        echo "conda|$conda_prefix|unknown"
                        return 0
                    fi
                fi
            fi
        done
    fi

    # Check if we're currently in any virtual environment
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
        local python_version
        python_version=$(python --version 2>&1 | awk '{print $2}')
        echo "venv|$VIRTUAL_ENV|$python_version"
        return 0
    fi

    # No virtual environment detected
    echo "none||"
    return 0
}

# Check if a virtual environment is currently active
is_venv_active() {
    [[ -n "${VIRTUAL_ENV:-}" ]] || [[ -n "${CONDA_DEFAULT_ENV:-}" ]]
}

# Get the activation command for a virtual environment
get_activation_command() {
    local venv_type="$1"
    local venv_path="$2"

    case "$venv_type" in
        venv)
            # Detect OS and return appropriate activation command
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
                # Windows
                if [[ -f "$venv_path/Scripts/activate.bat" ]]; then
                    echo "$venv_path\\Scripts\\activate.bat"
                else
                    echo "$venv_path\\Scripts\\Activate.ps1"
                fi
            else
                # Unix-like (Linux, macOS)
                if [[ -n "${FISH_VERSION:-}" ]]; then
                    echo "source $venv_path/bin/activate.fish"
                else
                    echo "source $venv_path/bin/activate"
                fi
            fi
            ;;
        poetry)
            echo "poetry shell"
            ;;
        conda)
            local env_name
            env_name=$(basename "$venv_path")
            echo "conda activate $env_name"
            ;;
        *)
            echo "ERROR: Unknown venv type: $venv_type" >&2
            return 1
            ;;
    esac
}

# List all potential virtual environment locations in project
list_all_venvs() {
    local project_dir="${1:-.}"

    cd "$project_dir" || return 1

    echo "=== Scanning for virtual environments ==="
    echo

    # Check standard locations
    local venv_candidates=(".venv" "venv" ".claude-venv" "env" ".env")
    local found=0

    for venv_name in "${venv_candidates[@]}"; do
        if [[ -d "$venv_name" ]]; then
            if [[ -f "$venv_name/bin/activate" || -f "$venv_name/Scripts/activate" ]]; then
                echo "✓ Found: $venv_name (standard venv)"
                found=1
            else
                echo "? Found directory: $venv_name (not a valid venv)"
            fi
        fi
    done

    # Check Poetry
    if command -v poetry &>/dev/null && [[ -f "pyproject.toml" ]]; then
        local poetry_venv
        poetry_venv=$(poetry env info -p 2>/dev/null || echo "")
        if [[ -n "$poetry_venv" ]]; then
            echo "✓ Found: Poetry-managed venv at $poetry_venv"
            found=1
        fi
    fi

    # Check Conda
    if command -v conda &>/dev/null; then
        for env_file in environment.yml environment.yaml conda.yml; do
            if [[ -f "$env_file" ]]; then
                local env_name
                env_name=$(grep -E "^name:" "$env_file" 2>/dev/null | awk '{print $2}' || echo "")
                if [[ -n "$env_name" ]]; then
                    if conda env list | grep -q "^$env_name "; then
                        echo "✓ Found: Conda environment '$env_name'"
                        found=1
                    else
                        echo "? Conda environment file exists ($env_file) but environment '$env_name' not created"
                    fi
                fi
            fi
        done
    fi

    if [[ $found -eq 0 ]]; then
        echo "✗ No virtual environments found"
    fi

    echo
}

# Get Python version from a virtual environment
get_venv_python_version() {
    local venv_type="$1"
    local venv_path="$2"

    case "$venv_type" in
        venv)
            if [[ -f "$venv_path/bin/python" ]]; then
                "$venv_path/bin/python" --version 2>&1 | awk '{print $2}'
            elif [[ -f "$venv_path/Scripts/python.exe" ]]; then
                "$venv_path/Scripts/python.exe" --version 2>&1 | awk '{print $2}'
            else
                echo "unknown"
            fi
            ;;
        poetry)
            poetry run python --version 2>&1 | awk '{print $2}' || echo "unknown"
            ;;
        conda)
            conda run -p "$venv_path" python --version 2>&1 | awk '{print $2}' || echo "unknown"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Main execution when run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "=== Virtual Environment Detection ==="
    echo

    project_dir="${1:-.}"
    echo "Project directory: $project_dir"
    echo

    if [[ "${2:-}" == "--list" ]]; then
        list_all_venvs "$project_dir"
    else
        result=$(detect_venv "$project_dir")
        venv_type=$(echo "$result" | cut -d'|' -f1)
        venv_path=$(echo "$result" | cut -d'|' -f2)
        python_version=$(echo "$result" | cut -d'|' -f3)

        if [[ "$venv_type" == "none" ]]; then
            echo "✗ No virtual environment detected"
            echo
            echo "To create one, run:"
            echo "  python -m venv .claude-venv"
            echo "  # or"
            echo "  poetry env use python3"
            echo "  # or"
            echo "  conda create -n myenv python=3.11"
        else
            echo "✓ Detected virtual environment:"
            echo "  Type: $venv_type"
            echo "  Path: $venv_path"
            echo "  Python version: $python_version"
            echo
            echo "Activation command:"
            echo "  $(get_activation_command "$venv_type" "$venv_path")"
            echo
            if is_venv_active; then
                echo "✓ A virtual environment is currently active"
            else
                echo "⚠ Virtual environment is NOT currently active"
            fi
        fi
    fi
fi
