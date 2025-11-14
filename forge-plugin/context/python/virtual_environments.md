# Python Virtual Environments Reference

This context file provides comprehensive guidance on Python virtual environments: creation, activation, management, and best practices.

---

## What is a Virtual Environment?

A **virtual environment** is an isolated Python environment that allows you to:
- Install packages without affecting the system Python
- Maintain different package versions for different projects
- Ensure reproducible development environments
- Avoid dependency conflicts between projects

---

## Types of Virtual Environments

### 1. venv (Built-in)

**Pros**:
- Built into Python 3.3+
- No additional installation needed
- Lightweight and fast
- Standard and well-supported

**Cons**:
- Basic feature set
- No dependency resolution
- Manual requirements.txt management

**Best for**: Simple projects, learning, quick scripts

### 2. virtualenv

**Pros**:
- Works with Python 2 and 3
- More features than venv
- Can create envs for different Python versions
- Faster than venv in some cases

**Cons**:
- Requires installation
- Mostly superseded by venv

**Best for**: Legacy Python 2 projects, cross-version testing

### 3. Poetry Environments

**Pros**:
- Automatic venv creation
- Integrated with dependency management
- Handles activation automatically
- Manages multiple environments per project

**Cons**:
- Requires Poetry installation
- Stored in cache directory by default
- Opinionated structure

**Best for**: Modern Python projects, library development

### 4. Conda Environments

**Pros**:
- Can install non-Python packages
- Multiple Python versions
- Cross-platform consistency
- Binary package support

**Cons**:
- Larger disk footprint
- Slower than pip-based tools
- Separate package ecosystem

**Best for**: Data science, scientific computing, cross-language projects

### 5. pipenv Environments

**Pros**:
- Combines pip and venv
- Automatic Pipfile management
- Built-in lock file
- Security scanning

**Cons**:
- Slower than alternatives
- Less active development
- Complex dependency resolution

**Best for**: Teams transitioning from requirements.txt

---

## Creating Virtual Environments

### venv (Standard Library)

```bash
# Create in .venv directory (recommended name)
python -m venv .venv

# Create with specific Python version
python3.11 -m venv .venv

# Create without pip (minimal)
python -m venv --without-pip .venv

# Create with system site-packages access
python -m venv --system-site-packages .venv

# Create with symlinks (Unix only, faster)
python -m venv --symlinks .venv
```

### virtualenv

```bash
# Install virtualenv
pip install virtualenv

# Create environment
virtualenv .venv

# Create with specific Python version
virtualenv -p python3.11 .venv

# Create with specific interpreter
virtualenv -p /usr/bin/python3.10 .venv
```

### Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create environment (automatic on install)
poetry install

# Create with specific Python version
poetry env use python3.11

# Create with system Python
poetry env use system
```

### Conda

```bash
# Create environment with Python version
conda create -n myenv python=3.11

# Create from environment.yml
conda env create -f environment.yml

# Create with specific packages
conda create -n myenv python=3.11 numpy pandas
```

### uv

```bash
# Install uv
pip install uv

# Create virtual environment
uv venv .venv

# Create with specific Python version
uv venv --python 3.11 .venv
```

---

## Activating Virtual Environments

### Unix/Linux/macOS

```bash
# Bash/Zsh (venv/virtualenv)
source .venv/bin/activate

# Fish shell
source .venv/bin/activate.fish

# Csh/Tcsh
source .venv/bin/activate.csh

# Conda
conda activate myenv

# Poetry (opens new shell)
poetry shell

# Or use poetry run for single commands
poetry run python script.py
```

### Windows

```cmd
# Command Prompt
.venv\Scripts\activate.bat

# PowerShell
.venv\Scripts\Activate.ps1

# Git Bash
source .venv/Scripts/activate

# Conda (same as Unix)
conda activate myenv
```

### Checking Activation

```bash
# Check if venv is active
echo $VIRTUAL_ENV  # Should show path to venv

# Check Python path
which python  # Should point to venv Python

# Check pip path
which pip  # Should point to venv pip

# For conda
echo $CONDA_DEFAULT_ENV  # Should show env name
```

---

## Deactivating Virtual Environments

```bash
# venv/virtualenv
deactivate

# Conda
conda deactivate

# Poetry (exit shell)
exit
```

---

## Common Virtual Environment Locations

### Project-Local (Recommended)

```
my-project/
├── .venv/           # Standard venv location
├── venv/            # Alternative common name
├── .claude-venv/    # Claude Code-created venvs
└── env/             # Another alternative
```

**Pros**: Easy to find, clear per-project isolation, simple cleanup
**Cons**: Takes up project disk space, must be in .gitignore

### Poetry Cache Directory

```
# Linux/macOS
~/.cache/pypoetry/virtualenvs/myproject-Xy3z1AbC-py3.11/

# Windows
%LOCALAPPDATA%\pypoetry\Cache\virtualenvs\myproject-Xy3z1AbC-py3.11\
```

**Pros**: Doesn't clutter project, managed automatically
**Cons**: Harder to find, opaque naming

### Conda Environments

```
# Default conda environments
~/anaconda3/envs/myenv/
~/miniconda3/envs/myenv/

# Custom location
conda create --prefix /path/to/env python=3.11
```

**Pros**: Centralized, named environments, cross-project reuse
**Cons**: Not project-local, manual cleanup needed

---

## Configuring Virtual Environment Behavior

### venv/virtualenv

No configuration needed, but you can set environment variables:

```bash
# Set custom prompt
export VIRTUAL_ENV_PROMPT="(my-env)"

# Disable prompt modification
export VIRTUAL_ENV_DISABLE_PROMPT=1
```

### Poetry

```bash
# Create .venv in project (recommended)
poetry config virtualenvs.in-project true

# Disable automatic venv creation
poetry config virtualenvs.create false

# Set custom path
poetry config virtualenvs.path /path/to/envs

# Use system Python (no venv)
poetry config virtualenvs.create false
```

### Conda

```bash
# Always activate base environment
conda config --set auto_activate_base true

# Never activate base
conda config --set auto_activate_base false

# Show full environment path in prompt
conda config --set env_prompt '({name})'
```

---

## Managing Virtual Environments

### Listing Environments

```bash
# venv/virtualenv - no built-in list, manually check directories

# Poetry
poetry env list
poetry env info  # Show current env

# Conda
conda env list
conda info --envs  # Same as above
```

### Removing Environments

```bash
# venv/virtualenv
rm -rf .venv/  # or del /s .venv\ on Windows

# Poetry
poetry env remove python3.11
poetry env remove --all  # Remove all envs for project

# Conda
conda env remove -n myenv
conda remove --all -n myenv  # Same as above
```

### Cloning Environments

```bash
# venv/virtualenv - use requirements.txt
pip freeze > requirements.txt
python -m venv new-venv
source new-venv/bin/activate
pip install -r requirements.txt

# Conda
conda create --name newenv --clone myenv
```

### Exporting Environments

```bash
# venv/virtualenv
pip freeze > requirements.txt

# Poetry
poetry export -f requirements.txt > requirements.txt

# Conda
conda env export > environment.yml
conda list --export > requirements.txt  # pip format
```

---

## Best Practices

### 1. Always Use Virtual Environments

**Never install packages to system Python** except for:
- Package managers themselves (pip, poetry, uv)
- System tools (virtualenv, pipx)

**Why**: Avoids breaking system tools, ensures reproducibility, prevents conflicts

### 2. Use Standard Names

**Recommended venv names**:
- `.venv` - Most common, hidden in Unix
- `venv` - Simple, explicit
- `.claude-venv` - For Claude Code-created envs

**Avoid**: Non-descriptive names like `env`, `test`, `my_venv`

### 3. Add to .gitignore

Always ignore virtual environment directories:

```gitignore
# Virtual environments
.venv/
venv/
.claude-venv/
env/
*.egg-info/

# Python cache
__pycache__/
*.pyc
*.pyo

# Poetry
poetry.lock  # Optional: commit for apps, ignore for libraries
```

### 4. Document Python Version

Specify required Python version:

**pyproject.toml** (Poetry/PDM):
```toml
[tool.poetry.dependencies]
python = "^3.11"  # 3.11 or higher
```

**runtime.txt** (Heroku):
```
python-3.11.5
```

**.python-version** (pyenv):
```
3.11.5
```

**README.md**:
```markdown
## Requirements

- Python 3.11 or higher
```

### 5. Create Venv at Project Root

**Do**:
```
my-project/
├── .venv/
├── src/
├── tests/
└── pyproject.toml
```

**Don't**:
```
my-project/
├── src/
│   └── .venv/  # Wrong location
└── tests/
```

### 6. Activate Before Installing

**Always activate** before running pip install:

```bash
# Wrong
pip install requests

# Right
source .venv/bin/activate
pip install requests
```

### 7. Use Lock Files

Generate lock files for reproducible installs:

```bash
# pip
pip freeze > requirements.txt

# Poetry
poetry lock  # Automatic

# Conda
conda lock  # Requires conda-lock
```

### 8. Separate Dev Dependencies

Keep development tools separate:

**requirements-dev.txt**:
```txt
pytest>=7.0
black>=23.0
mypy>=1.0
```

**pyproject.toml** (Poetry):
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
black = "^23.0"
```

---

## Troubleshooting

### Issue 1: "Command not found" after activation

**Cause**: Activation script not sourced properly

**Solution**:
```bash
# Make sure you use 'source' (or '.')
source .venv/bin/activate

# Not this (common mistake)
./.venv/bin/activate  # Wrong - executes in subprocess
```

### Issue 2: pip installs to wrong location

**Cause**: Venv not activated, or multiple Pythons

**Solution**:
```bash
# Check which pip
which pip  # Should be in venv

# If wrong, deactivate and reactivate
deactivate
source .venv/bin/activate

# Or use python -m pip (always uses active Python's pip)
python -m pip install requests
```

### Issue 3: Permission denied creating venv

**Cause**: Insufficient permissions or corrupted Python install

**Solution**:
```bash
# Use --without-pip and install pip separately
python -m venv --without-pip .venv
source .venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python

# Or use virtualenv instead
pip install --user virtualenv
virtualenv .venv
```

### Issue 4: Venv created with wrong Python version

**Cause**: Multiple Python installations, used wrong python command

**Solution**:
```bash
# Be explicit about Python version
python3.11 -m venv .venv

# Or use pyenv to manage Python versions
pyenv install 3.11.5
pyenv local 3.11.5
python -m venv .venv
```

### Issue 5: "ModuleNotFoundError" after activation

**Cause**: Package installed to wrong environment, or not installed

**Solution**:
```bash
# Verify venv is active
echo $VIRTUAL_ENV

# Check if package is installed
pip list | grep package-name

# Reinstall if needed
pip install package-name

# Check Python path in code
import sys
print(sys.executable)  # Should show venv Python
```

### Issue 6: Conda activate doesn't work

**Cause**: Conda not initialized for shell

**Solution**:
```bash
# Initialize conda for bash
conda init bash

# Or for zsh
conda init zsh

# Then restart shell or source bashrc
source ~/.bashrc

# Now activate should work
conda activate myenv
```

### Issue 7: Poetry venv in wrong location

**Cause**: Poetry default config stores in cache

**Solution**:
```bash
# Configure to create in project
poetry config virtualenvs.in-project true

# Remove old env
poetry env remove python

# Recreate
poetry install
```

---

## IDE Integration

### VS Code

```json
// .vscode/settings.json
{
  "python.venvPath": "${workspaceFolder}",
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Virtualenv Environment"
4. Choose "Existing environment" and browse to `.venv/bin/python`

### Jupyter

```bash
# Install ipykernel in venv
pip install ipykernel

# Add venv as Jupyter kernel
python -m ipykernel install --user --name=myproject

# Now available in Jupyter
jupyter notebook
# Select "myproject" kernel
```

---

## Automation Scripts

### Auto-create and activate (Bash)

```bash
#!/bin/bash
# setup-venv.sh

VENV_DIR=".venv"
PYTHON_VERSION="python3.11"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_VERSION -m venv $VENV_DIR
    echo "✓ Virtual environment created"
fi

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

echo "✓ Environment ready"
```

### Auto-activate on cd (Bash)

Add to `~/.bashrc`:

```bash
auto_activate_venv() {
    if [ -f ".venv/bin/activate" ]; then
        if [ -z "$VIRTUAL_ENV" ] || [ "$VIRTUAL_ENV" != "$(pwd)/.venv" ]; then
            source .venv/bin/activate
            echo "✓ Activated $(pwd)/.venv"
        fi
    fi
}

cd() {
    builtin cd "$@"
    auto_activate_venv
}
```

---

## Environment Variables Reference

```bash
# Set when venv is active
VIRTUAL_ENV="/path/to/venv"           # venv location
PATH="/path/to/venv/bin:$PATH"        # Modified PATH
PYTHONHOME=""                         # Unset to avoid conflicts

# Poetry-specific
POETRY_VIRTUALENVS_CREATE=true        # Auto-create venvs
POETRY_VIRTUALENVS_IN_PROJECT=true    # Create in project
POETRY_VIRTUALENVS_PATH="/path"       # Custom venv location

# Conda-specific
CONDA_DEFAULT_ENV="myenv"             # Active environment name
CONDA_PREFIX="/path/to/env"           # Environment location
CONDA_PYTHON_EXE="/path/to/python"    # Python executable

# Pip-specific
PIP_REQUIRE_VIRTUALENV=true           # Prevent system installs
PIP_RESPECT_VIRTUALENV=true           # Use active venv
```

---

## Quick Reference

### Venv Commands Cheatsheet

| Task | venv | Poetry | Conda |
|------|------|---------|-------|
| Create | `python -m venv .venv` | `poetry install` | `conda create -n env` |
| Activate (Unix) | `source .venv/bin/activate` | `poetry shell` | `conda activate env` |
| Activate (Win) | `.venv\Scripts\activate` | `poetry shell` | `conda activate env` |
| Deactivate | `deactivate` | `exit` | `conda deactivate` |
| List | - | `poetry env list` | `conda env list` |
| Remove | `rm -rf .venv` | `poetry env remove` | `conda env remove -n` |
| Export | `pip freeze >` | `poetry export >` | `conda env export >` |

---

## Further Reading

- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [virtualenv Documentation](https://virtualenv.pypa.io/)
- [Poetry Virtual Environments](https://python-poetry.org/docs/managing-environments/)
- [Conda Environments Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [PEP 405 - Python Virtual Environments](https://peps.python.org/pep-0405/)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-14
**Maintained For**: python-dependency-management skill
