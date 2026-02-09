# Python Dependency Management Scripts

This directory contains helper scripts for the `python-dependency-management` skill. These scripts provide detection, operation execution, and utility functions for managing Python dependencies across different package managers.

## Scripts Overview

### 1. detect_package_manager.sh

**Purpose**: Automatically detect which Python package manager a project uses.

**Detection Priority**: uv → poetry → conda → pipenv → pdm → pip (default)

**Functions**:
- `detect_package_manager [project_dir]` - Detect package manager and version
- `get_config_files <manager> [project_dir]` - List configuration files for a package manager
- `is_package_manager_installed <manager>` - Check if a package manager is installed

**Usage**:
```bash
# Source for functions
source detect_package_manager.sh
result=$(detect_package_manager /path/to/project)
manager=$(echo "$result" | cut -d'|' -f1)
version=$(echo "$result" | cut -d'|' -f2)

# Or run directly for demo
./detect_package_manager.sh /path/to/project
```

**Output Format**: `manager|version`

**Examples**:
```
uv|0.1.6
poetry|1.7.1
conda|23.7.4
pip|23.3.1
```

**Detection Logic**:
- **uv**: Checks for `uv.lock` or `[tool.uv]` in `pyproject.toml`
- **poetry**: Checks for `poetry.lock` or `[tool.poetry]` in `pyproject.toml`
- **conda**: Checks for `environment.yml`, `environment.yaml`, or `conda.yml`
- **pipenv**: Checks for `Pipfile` or `Pipfile.lock`
- **pdm**: Checks for `pdm.lock` or `[tool.pdm]` in `pyproject.toml`
- **pip**: Default fallback if no other manager detected

---

### 2. detect_venv.sh

**Purpose**: Find Python virtual environments in a project.

**Functions**:
- `detect_venv [project_dir]` - Detect virtual environment type, path, and Python version
- `is_venv_active` - Check if a virtual environment is currently active
- `get_activation_command <venv_type> <venv_path>` - Get OS-specific activation command
- `list_all_venvs [project_dir]` - Scan and list all potential venvs in project
- `get_venv_python_version <venv_type> <venv_path>` - Get Python version from a venv

**Usage**:
```bash
# Source for functions
source detect_venv.sh
result=$(detect_venv /path/to/project)
venv_type=$(echo "$result" | cut -d'|' -f1)
venv_path=$(echo "$result" | cut -d'|' -f2)
python_version=$(echo "$result" | cut -d'|' -f3)

# Or run directly
./detect_venv.sh /path/to/project

# List all potential venvs
./detect_venv.sh /path/to/project --list
```

**Output Format**: `venv_type|venv_path|python_version`

**Venv Types**:
- `venv` - Standard Python venv (checks `.venv`, `venv`, `.claude-venv`, `env`, `.env`)
- `poetry` - Poetry-managed virtual environment
- `conda` - Conda environment
- `none` - No virtual environment detected

**Examples**:
```
venv|/path/to/project/.venv|3.11.5
poetry|/home/user/.cache/pypoetry/virtualenvs/myproject-Xy3z-py3.11|3.11.5
conda|/home/user/anaconda3/envs/myenv|3.10.12
none||
```

**Activation Commands**:
The script generates OS-specific activation commands:
- **Linux/macOS (bash/zsh)**: `source .venv/bin/activate`
- **Linux/macOS (fish)**: `source .venv/bin/activate.fish`
- **Windows CMD**: `.venv\Scripts\activate.bat`
- **Windows PowerShell**: `.venv\Scripts\Activate.ps1`
- **Poetry**: `poetry shell`
- **Conda**: `conda activate <env_name>`

---

### 3. install_package.sh

**Purpose**: Execute package operations (install, remove, update, list) using the appropriate package manager.

**Functions**:
- `execute_package_operation <manager> <operation> [packages...] [--dev]` - Main operation dispatcher
- `execute_uv_operation` - UV-specific operations
- `execute_poetry_operation` - Poetry-specific operations
- `execute_conda_operation` - Conda-specific operations
- `execute_pipenv_operation` - Pipenv-specific operations
- `execute_pdm_operation` - PDM-specific operations
- `execute_pip_operation` - Pip-specific operations
- `verify_installation <manager> <package>` - Verify package was installed
- `get_package_version <manager> <package>` - Get installed package version

**Usage**:
```bash
# Source for functions
source install_package.sh
execute_package_operation poetry install requests httpx
execute_package_operation uv install pytest --dev
execute_package_operation pip remove numpy

# Or run directly
./install_package.sh poetry install requests httpx
./install_package.sh uv install pytest --dev
./install_package.sh pip update
./install_package.sh conda list
```

**Operations**:
- `install` - Install one or more packages
- `remove` - Remove/uninstall packages
- `update` - Update packages (or all if none specified)
- `list` - List installed packages

**Flags**:
- `--dev` - Install as development dependency (where supported)

**Command Translation Table**:

| Operation | uv | poetry | conda | pip |
|-----------|----|---------||-----|
| Install | `uv pip install` | `poetry add` | `conda install` | `pip install` |
| Install dev | `uv pip install --group dev` | `poetry add --group dev` | N/A | `pip install` |
| Remove | `uv pip uninstall` | `poetry remove` | `conda remove` | `pip uninstall` |
| Update | `uv pip install -U` | `poetry update` | `conda update` | `pip install -U` |
| List | `uv pip list` | `poetry show` | `conda list` | `pip list` |

**Examples**:
```bash
# Install production dependency
./install_package.sh poetry install requests

# Install dev dependency
./install_package.sh uv install pytest pytest-cov --dev

# Install with version constraint
./install_package.sh pip install "django>=4.2,<5.0"

# Remove package
./install_package.sh poetry remove pandas

# Update all packages
./install_package.sh poetry update

# Update specific package
./install_package.sh pip update numpy

# List packages
./install_package.sh conda list
```

---

### 4. utils.sh

**Purpose**: General utility functions for project analysis, environment management, and file operations.

**Functions**:

**Project Information**:
- `get_project_name [project_dir]` - Extract project name from git repo or directory
- `get_python_version [venv_path]` - Get Python version (from venv or system)
- `is_git_repo` - Check if current directory is a git repository

**Virtual Environment Management**:
- `create_venv <venv_path> [python_version]` - Create a new virtual environment
- `add_venv_to_gitignore <venv_name> [project_dir]` - Add venv to .gitignore

**Package Handling**:
- `parse_package_spec <package_spec>` - Parse package name and version constraint
- `format_package_list [packages...]` - Format package list for display
- `is_valid_package_name <package_name>` - Validate package name format
- `extract_packages_from_requirements <requirements_file>` - Parse requirements.txt
- `count_installed_packages <package_manager>` - Count installed packages

**File and Path Utilities**:
- `sanitize_project_name <project_name>` - Clean project name for filenames
- `get_timestamp` - Get current timestamp for file naming
- `generate_output_filename <project_name> <operation>` - Create output filename
- `create_memory_structure <project_name> <skill_dir>` - Create memory directories

**Environment Detection**:
- `get_os_type` - Detect operating system (linux, macos, windows)
- `is_ci_environment` - Check if running in CI/CD
- `check_environment_health` - Comprehensive environment health check

**Usage**:
```bash
# Source for functions
source utils.sh

project_name=$(get_project_name)
python_version=$(get_python_version)
os_type=$(get_os_type)

# Create virtual environment
create_venv .claude-venv python3.11
add_venv_to_gitignore .claude-venv

# Parse package specification
result=$(parse_package_spec "django>=4.2,<5.0")
package_name=$(echo "$result" | cut -d'|' -f1)      # "django"
version_constraint=$(echo "$result" | cut -d'|' -f2) # ">=4.2,<5.0"

# Generate output filename
filename=$(generate_output_filename "my-project" "install")
# Output: dependency-install-my-project-20251114-123456.md

# Or run directly for environment info
./utils.sh /path/to/project
```

**Package Name Validation**:
```bash
is_valid_package_name "requests"      # Returns 0 (valid)
is_valid_package_name "my-package"    # Returns 0 (valid)
is_valid_package_name "123invalid"    # Returns 1 (invalid - starts with number)
is_valid_package_name "bad@package"   # Returns 1 (invalid - contains @)
```

**Environment Health Check Output**:
```
=== Environment Health Check ===

✓ Python: Python 3.11.5
✓ pip: 23.3.1
✓ Virtual environment active: /path/to/.venv
✓ Package managers available: uv poetry
```

---

## Integration with SKILL.md Workflow

These scripts support the mandatory 6-step workflow:

### Step 2: Load Memory
- Uses `utils.sh::get_project_name()` to identify project

### Step 3: Detect Package Manager and Environment
- Uses `detect_package_manager.sh::detect_package_manager()` to find package manager
- Uses `detect_venv.sh::detect_venv()` to find virtual environments
- Uses `detect_venv.sh::list_all_venvs()` if no venv found
- Uses `utils.sh::create_venv()` if user approves new venv creation
- Uses `utils.sh::add_venv_to_gitignore()` to update .gitignore

### Step 5: Execute Operations
- Uses `detect_venv.sh::get_activation_command()` to activate venv
- Uses `install_package.sh::execute_package_operation()` to run operations
- Uses `install_package.sh::verify_installation()` to confirm success
- Uses `install_package.sh::get_package_version()` for version reporting

### Step 6: Update Memory and Report
- Uses `utils.sh::generate_output_filename()` for report naming
- Uses `utils.sh::create_memory_structure()` for first-time memory setup
- Uses `utils.sh::format_package_list()` for output formatting

---

## Common Usage Patterns

### Pattern 1: Complete Detection Flow
```bash
source detect_package_manager.sh
source detect_venv.sh
source utils.sh

# Detect everything
project=$(get_project_name)
manager_info=$(detect_package_manager)
manager=$(echo "$manager_info" | cut -d'|' -f1)
venv_info=$(detect_venv)
venv_type=$(echo "$venv_info" | cut -d'|' -f1)

echo "Project: $project"
echo "Package Manager: $manager"
echo "Venv Type: $venv_type"
```

### Pattern 2: Install with Verification
```bash
source install_package.sh

# Install package
execute_package_operation poetry install requests

# Verify
if verify_installation poetry requests; then
    version=$(get_package_version poetry requests)
    echo "✓ requests $version installed successfully"
else
    echo "✗ Installation failed"
fi
```

### Pattern 3: Setup New Environment
```bash
source utils.sh
source detect_venv.sh

# Check if venv exists
venv_info=$(detect_venv)
if [[ "$(echo "$venv_info" | cut -d'|' -f1)" == "none" ]]; then
    # Create new venv
    create_venv .claude-venv python3.11
    add_venv_to_gitignore .claude-venv
    echo "✓ Environment ready"
fi
```

---

## Error Handling

All scripts use `set -euo pipefail` for strict error handling:
- `-e`: Exit on error
- `-u`: Exit on undefined variable
- `-o pipefail`: Catch errors in pipes

Functions return appropriate exit codes:
- `0`: Success
- `1`: Error

Error messages are sent to stderr for proper stream handling.

---

## Testing Scripts

Each script can be run directly for testing:

```bash
# Test package manager detection
./detect_package_manager.sh

# Test venv detection
./detect_venv.sh

# List all venvs
./detect_venv.sh . --list

# Test package operations (requires packages as arguments)
./install_package.sh pip list

# Test utilities
./utils.sh
```

---

## Dependencies

**Required**:
- bash 4.0+
- Python 3.7+
- At least one package manager (pip, poetry, uv, conda, pipenv, or pdm)

**Optional**:
- git (for project name detection and .gitignore management)
- Specific package managers as needed

---

## File Permissions

All scripts should be executable:
```bash
chmod +x detect_package_manager.sh
chmod +x detect_venv.sh
chmod +x install_package.sh
chmod +x utils.sh
```

---

## Notes

1. **Sourcing vs Direct Execution**:
   - Source scripts to use functions: `source detect_package_manager.sh`
   - Run directly for demos/testing: `./detect_package_manager.sh`

2. **Cross-Platform Compatibility**:
   - Scripts detect OS and adjust commands accordingly
   - Windows paths use backslashes where appropriate
   - Activation commands are OS-specific

3. **Claude Code Integration**:
   - Scripts are designed to be called from SKILL.md workflow
   - Output format is machine-parsable (pipe-delimited)
   - Error messages go to stderr for clean parsing

4. **Memory Integration**:
   - `utils.sh` provides memory directory creation
   - Project names are sanitized for filesystem safety
   - Timestamps ensure unique filenames
