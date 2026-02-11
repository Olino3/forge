---
id: "python/virtual_environments"
domain: python
title: "Python Virtual Environments Reference"
type: reference
estimatedTokens: 1100
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "What is a Virtual Environment?"
    estimatedTokens: 14
    keywords: [virtual, environment]
  - name: "Virtual Environment Types"
    estimatedTokens: 69
    keywords: [virtual, environment, types]
  - name: "Quick Command Reference"
    estimatedTokens: 106
    keywords: [quick, command, reference]
  - name: "Common Virtual Environment Locations"
    estimatedTokens: 42
    keywords: [virtual, environment, locations]
  - name: "Best Practices"
    estimatedTokens: 63
    keywords: [best]
  - name: "Common Issues & Solutions"
    estimatedTokens: 85
    keywords: [issues, solutions]
  - name: "IDE Integration"
    estimatedTokens: 39
    keywords: [ide, integration]
  - name: "Management Commands"
    estimatedTokens: 53
    keywords: [management, commands]
  - name: "Environment Variables"
    estimatedTokens: 35
    keywords: [environment, variables]
  - name: "Detection Patterns"
    estimatedTokens: 40
    keywords: [detection, patterns]
  - name: "Official Documentation"
    estimatedTokens: 25
    keywords: [official, documentation]
tags: [python, venv, virtualenv, poetry, conda, environments]
---

# Python Virtual Environments Reference

Quick reference for creating, activating, and managing Python virtual environments. For detailed documentation, see official sources linked below.

---

## What is a Virtual Environment?

An isolated Python environment that allows project-specific package installations without affecting the system Python. See [Python venv documentation](https://docs.python.org/3/library/venv.html).

---

## Virtual Environment Types

| Type | Pros | Cons | Best For | Docs |
|------|------|------|----------|------|
| **venv** | Built-in, lightweight | Basic features | Simple projects | [venv docs](https://docs.python.org/3/library/venv.html) |
| **virtualenv** | Python 2+3, feature-rich | Requires install | Legacy projects | [virtualenv docs](https://virtualenv.pypa.io/) |
| **poetry** | Auto-managed, integrated | Opinionated | Modern projects | [Poetry envs](https://python-poetry.org/docs/managing-environments/) |
| **conda** | Non-Python packages, binaries | Large, slower | Data science | [Conda envs](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) |
| **pipenv** | Combines pip + venv | Less active | Transitioning teams | [Pipenv docs](https://pipenv.pypa.io/) |

---

## Quick Command Reference

### Creating Environments

```bash
# venv (built-in)
python -m venv .venv

# virtualenv
virtualenv .venv

# poetry
poetry install  # Auto-creates

# conda
conda create -n myenv python=3.11

# uv
uv venv .venv
```

### Activating Environments

| Platform | venv/virtualenv | Poetry | Conda |
|----------|----------------|---------|-------|
| **Linux/macOS** | `source .venv/bin/activate` | `poetry shell` | `conda activate myenv` |
| **Windows CMD** | `.venv\Scripts\activate.bat` | `poetry shell` | `conda activate myenv` |
| **Windows PS** | `.venv\Scripts\Activate.ps1` | `poetry shell` | `conda activate myenv` |

### Deactivating

```bash
deactivate          # venv/virtualenv
exit                # Poetry (exit shell)
conda deactivate    # Conda
```

### Verification

```bash
# Check if active
echo $VIRTUAL_ENV           # venv/virtualenv (Unix)
echo $CONDA_DEFAULT_ENV     # Conda

# Check Python location
which python                # Should point to venv

# Check pip location
which pip                   # Should point to venv
```

---

## Common Virtual Environment Locations

### Recommended Project-Local (in .gitignore)

```
project/
├── .venv/           # Standard (recommended)
├── venv/            # Alternative
├── .claude-venv/    # Claude Code-created
```

### Poetry Cache (Managed)

```
~/.cache/pypoetry/virtualenvs/  # Linux/macOS
%LOCALAPPDATA%\pypoetry\Cache\  # Windows
```

### Conda Environments

```
~/anaconda3/envs/myenv/     # Default location
```

**Configure poetry** to use project-local .venv:
```bash
poetry config virtualenvs.in-project true
```

---

## Best Practices

### 1. Always Use Virtual Environments

- Never install packages to system Python (except tools like pip, poetry, uv)
- One venv per project
- See [Python Packaging Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

### 2. Standard Naming

**Use**: `.venv`, `venv`, `.claude-venv`
**Avoid**: Non-descriptive names like `env`, `test`, `my_venv`

### 3. Add to .gitignore

```gitignore
.venv/
venv/
.claude-venv/
env/
*.egg-info/
__pycache__/
*.pyc
```

See [Python .gitignore template](https://github.com/github/gitignore/blob/main/Python.gitignore)

### 4. Document Python Version

**pyproject.toml**:
```toml
[tool.poetry.dependencies]
python = "^3.11"
```

**.python-version** (pyenv):
```
3.11.5
```

**README.md**: Mention required Python version

---

## Common Issues & Solutions

### Issue: "Command not found" after activation

**Cause**: Not using `source`

**Solution**:
```bash
source .venv/bin/activate  # Correct (Unix)
./.venv/bin/activate       # Wrong - runs in subprocess
```

### Issue: pip installs to wrong location

**Cause**: Venv not activated

**Solution**:
```bash
which pip    # Verify location
# Or use:
python -m pip install package  # Always uses active Python's pip
```

### Issue: Permission denied creating venv

**Solution**:
```bash
# Create without pip, install separately
python -m venv --without-pip .venv
source .venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
```

### Issue: Poetry venv in wrong location

**Solution**:
```bash
poetry config virtualenvs.in-project true
poetry env remove python  # Remove old
poetry install            # Recreate
```

See [virtualenv troubleshooting](https://virtualenv.pypa.io/en/latest/user_guide.html#troubleshooting)

---

## IDE Integration

### VS Code

**`.vscode/settings.json`**:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```

[VS Code Python environments](https://code.visualstudio.com/docs/python/environments)

### PyCharm

File → Settings → Project → Python Interpreter → Add → Existing → Select `.venv/bin/python`

[PyCharm virtual environments](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

### Jupyter

```bash
pip install ipykernel
python -m ipykernel install --user --name=myproject
```

[Jupyter kernels](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)

---

## Management Commands

### List Environments

```bash
# Poetry
poetry env list

# Conda
conda env list
```

### Remove Environments

```bash
# venv/virtualenv (manual)
rm -rf .venv/

# Poetry
poetry env remove python3.11

# Conda
conda env remove -n myenv
```

### Export/Clone

```bash
# pip
pip freeze > requirements.txt

# Poetry
poetry export -f requirements.txt > requirements.txt

# Conda
conda env export > environment.yml
conda create --name newenv --clone myenv
```

---

## Environment Variables

```bash
# Set when venv active
VIRTUAL_ENV="/path/to/venv"              # venv location
PATH="/path/to/venv/bin:$PATH"           # Modified PATH
PYTHONHOME=""                            # Unset

# Poetry-specific
POETRY_VIRTUALENVS_CREATE=true           # Auto-create
POETRY_VIRTUALENVS_IN_PROJECT=true       # Create in project

# Conda-specific
CONDA_DEFAULT_ENV="myenv"                # Active env name
CONDA_PREFIX="/path/to/env"              # Env location

# Pip-specific
PIP_REQUIRE_VIRTUALENV=true              # Prevent system installs
```

---

## Detection Patterns

Use these to identify virtual environment type:

| Pattern | Type |
|---------|------|
| `.venv/bin/activate` exists | venv/virtualenv |
| `$VIRTUAL_ENV` set | venv/virtualenv (active) |
| `poetry env info -p` returns path | poetry |
| `$CONDA_DEFAULT_ENV` set | conda (active) |
| `environment.yml` + conda installed | conda (not active) |

---

## Official Documentation

- **venv**: https://docs.python.org/3/library/venv.html
- **virtualenv**: https://virtualenv.pypa.io/
- **Poetry**: https://python-poetry.org/docs/managing-environments/
- **Conda**: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- **PEP 405** (venv specification): https://peps.python.org/pep-0405/
- **Python Packaging Guide**: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

---

**Version**: 0.1.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-dependency-management skill
