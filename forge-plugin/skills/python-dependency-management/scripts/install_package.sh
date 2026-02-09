#!/usr/bin/env bash
# install_package.sh - Execute package operations using the appropriate package manager
# Part of the python-dependency-management skill

set -euo pipefail

# Execute a package installation operation
# Args: package_manager, operation (install|remove|update|list), packages..., [--dev]
execute_package_operation() {
    local package_manager="$1"
    local operation="$2"
    shift 2

    local packages=()
    local is_dev=0

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dev)
                is_dev=1
                shift
                ;;
            *)
                packages+=("$1")
                shift
                ;;
        esac
    done

    case "$package_manager" in
        uv)
            execute_uv_operation "$operation" "$is_dev" "${packages[@]}"
            ;;
        poetry)
            execute_poetry_operation "$operation" "$is_dev" "${packages[@]}"
            ;;
        conda)
            execute_conda_operation "$operation" "$is_dev" "${packages[@]}"
            ;;
        pipenv)
            execute_pipenv_operation "$operation" "$is_dev" "${packages[@]}"
            ;;
        pdm)
            execute_pdm_operation "$operation" "$is_dev" "${packages[@]}"
            ;;
        pip)
            execute_pip_operation "$operation" "$is_dev" "${packages[@]}"
            ;;
        *)
            echo "ERROR: Unknown package manager: $package_manager" >&2
            return 1
            ;;
    esac
}

# UV operations
execute_uv_operation() {
    local operation="$1"
    local is_dev="$2"
    shift 2
    local packages=("$@")

    case "$operation" in
        install)
            if [[ $is_dev -eq 1 ]]; then
                uv pip install --group dev "${packages[@]}"
            else
                uv pip install "${packages[@]}"
            fi
            ;;
        remove)
            uv pip uninstall "${packages[@]}"
            ;;
        update)
            if [[ ${#packages[@]} -eq 0 ]]; then
                # Update all packages
                uv pip install --upgrade $(uv pip list --format=freeze | cut -d'=' -f1)
            else
                uv pip install --upgrade "${packages[@]}"
            fi
            ;;
        list)
            if [[ ${#packages[@]} -eq 0 ]]; then
                uv pip list
            else
                uv pip show "${packages[@]}"
            fi
            ;;
        *)
            echo "ERROR: Unknown operation: $operation" >&2
            return 1
            ;;
    esac
}

# Poetry operations
execute_poetry_operation() {
    local operation="$1"
    local is_dev="$2"
    shift 2
    local packages=("$@")

    case "$operation" in
        install)
            if [[ $is_dev -eq 1 ]]; then
                poetry add --group dev "${packages[@]}"
            else
                poetry add "${packages[@]}"
            fi
            ;;
        remove)
            poetry remove "${packages[@]}"
            ;;
        update)
            if [[ ${#packages[@]} -eq 0 ]]; then
                poetry update
            else
                poetry update "${packages[@]}"
            fi
            ;;
        list)
            if [[ ${#packages[@]} -eq 0 ]]; then
                poetry show
            else
                poetry show "${packages[@]}"
            fi
            ;;
        *)
            echo "ERROR: Unknown operation: $operation" >&2
            return 1
            ;;
    esac
}

# Conda operations
execute_conda_operation() {
    local operation="$1"
    local is_dev="$2"  # Conda doesn't distinguish dev deps
    shift 2
    local packages=("$@")

    # Determine environment (use CONDA_DEFAULT_ENV if set, otherwise extract from environment.yml)
    local env_name="${CONDA_DEFAULT_ENV:-}"
    if [[ -z "$env_name" ]] && [[ -f "environment.yml" ]]; then
        env_name=$(grep -E "^name:" environment.yml 2>/dev/null | awk '{print $2}' || echo "")
    fi

    local env_arg=""
    if [[ -n "$env_name" ]]; then
        env_arg="-n $env_name"
    fi

    case "$operation" in
        install)
            conda install $env_arg "${packages[@]}"
            ;;
        remove)
            conda remove $env_arg "${packages[@]}"
            ;;
        update)
            if [[ ${#packages[@]} -eq 0 ]]; then
                conda update $env_arg --all
            else
                conda update $env_arg "${packages[@]}"
            fi
            ;;
        list)
            if [[ ${#packages[@]} -eq 0 ]]; then
                conda list $env_arg
            else
                # Show specific packages
                for pkg in "${packages[@]}"; do
                    conda list $env_arg "^${pkg}$"
                done
            fi
            ;;
        *)
            echo "ERROR: Unknown operation: $operation" >&2
            return 1
            ;;
    esac
}

# Pipenv operations
execute_pipenv_operation() {
    local operation="$1"
    local is_dev="$2"
    shift 2
    local packages=("$@")

    case "$operation" in
        install)
            if [[ $is_dev -eq 1 ]]; then
                pipenv install --dev "${packages[@]}"
            else
                pipenv install "${packages[@]}"
            fi
            ;;
        remove)
            pipenv uninstall "${packages[@]}"
            ;;
        update)
            if [[ ${#packages[@]} -eq 0 ]]; then
                pipenv update
            else
                pipenv update "${packages[@]}"
            fi
            ;;
        list)
            pipenv graph
            ;;
        *)
            echo "ERROR: Unknown operation: $operation" >&2
            return 1
            ;;
    esac
}

# PDM operations
execute_pdm_operation() {
    local operation="$1"
    local is_dev="$2"
    shift 2
    local packages=("$@")

    case "$operation" in
        install)
            if [[ $is_dev -eq 1 ]]; then
                pdm add --dev "${packages[@]}"
            else
                pdm add "${packages[@]}"
            fi
            ;;
        remove)
            pdm remove "${packages[@]}"
            ;;
        update)
            if [[ ${#packages[@]} -eq 0 ]]; then
                pdm update
            else
                pdm update "${packages[@]}"
            fi
            ;;
        list)
            if [[ ${#packages[@]} -eq 0 ]]; then
                pdm list
            else
                pdm show "${packages[@]}"
            fi
            ;;
        *)
            echo "ERROR: Unknown operation: $operation" >&2
            return 1
            ;;
    esac
}

# Pip operations
execute_pip_operation() {
    local operation="$1"
    local is_dev="$2"
    shift 2
    local packages=("$@")

    # Determine pip command (pip or pip3)
    local pip_cmd="pip"
    if ! command -v pip &>/dev/null && command -v pip3 &>/dev/null; then
        pip_cmd="pip3"
    fi

    case "$operation" in
        install)
            # Note: pip doesn't have native dev dependency handling
            # Claude should update requirements-dev.txt manually if needed
            $pip_cmd install "${packages[@]}"
            ;;
        remove)
            $pip_cmd uninstall -y "${packages[@]}"
            ;;
        update)
            if [[ ${#packages[@]} -eq 0 ]]; then
                # Update all packages (requires pip-review or manual list)
                $pip_cmd list --outdated --format=freeze | cut -d'=' -f1 | xargs -n1 $pip_cmd install -U
            else
                $pip_cmd install -U "${packages[@]}"
            fi
            ;;
        list)
            if [[ ${#packages[@]} -eq 0 ]]; then
                $pip_cmd list
            else
                $pip_cmd show "${packages[@]}"
            fi
            ;;
        *)
            echo "ERROR: Unknown operation: $operation" >&2
            return 1
            ;;
    esac
}

# Verify package installation
verify_installation() {
    local package_manager="$1"
    local package_name="$2"

    case "$package_manager" in
        uv)
            uv pip show "$package_name" &>/dev/null
            ;;
        poetry)
            poetry show "$package_name" &>/dev/null
            ;;
        conda)
            local env_arg=""
            if [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
                env_arg="-n $CONDA_DEFAULT_ENV"
            fi
            conda list $env_arg "^${package_name}$" | grep -q "^${package_name} "
            ;;
        pipenv)
            pipenv graph | grep -q "^${package_name}=="
            ;;
        pdm)
            pdm show "$package_name" &>/dev/null
            ;;
        pip)
            local pip_cmd="pip"
            if ! command -v pip &>/dev/null && command -v pip3 &>/dev/null; then
                pip_cmd="pip3"
            fi
            $pip_cmd show "$package_name" &>/dev/null
            ;;
        *)
            return 1
            ;;
    esac
}

# Get installed package version
get_package_version() {
    local package_manager="$1"
    local package_name="$2"

    case "$package_manager" in
        uv)
            uv pip show "$package_name" 2>/dev/null | grep "^Version:" | awk '{print $2}'
            ;;
        poetry)
            poetry show "$package_name" 2>/dev/null | grep "version" | awk '{print $3}'
            ;;
        conda)
            local env_arg=""
            if [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
                env_arg="-n $CONDA_DEFAULT_ENV"
            fi
            conda list $env_arg "^${package_name}$" 2>/dev/null | grep "^${package_name} " | awk '{print $2}'
            ;;
        pipenv)
            pipenv graph 2>/dev/null | grep "^${package_name}==" | cut -d'=' -f3
            ;;
        pdm)
            pdm show "$package_name" 2>/dev/null | grep "^Version:" | awk '{print $2}'
            ;;
        pip)
            local pip_cmd="pip"
            if ! command -v pip &>/dev/null && command -v pip3 &>/dev/null; then
                pip_cmd="pip3"
            fi
            $pip_cmd show "$package_name" 2>/dev/null | grep "^Version:" | awk '{print $2}'
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Main execution when run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <package_manager> <operation> [packages...] [--dev]"
        echo
        echo "Operations: install, remove, update, list"
        echo "Package managers: uv, poetry, conda, pipenv, pdm, pip"
        echo
        echo "Examples:"
        echo "  $0 poetry install requests httpx"
        echo "  $0 uv install pytest --dev"
        echo "  $0 pip remove numpy"
        echo "  $0 poetry update"
        echo "  $0 conda list"
        exit 1
    fi

    execute_package_operation "$@"
fi
