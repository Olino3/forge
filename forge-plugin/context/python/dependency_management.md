# Python Dependency Management Reference

This context file provides comprehensive reference information for managing Python dependencies across different package managers. Use this as a command reference and best practices guide.

---

## Package Manager Overview

### Supported Package Managers

| Manager | Primary Use Case | Config File | Lock File | Strengths |
|---------|-----------------|-------------|-----------|-----------|
| **uv** | Modern, fast dependency management | pyproject.toml | uv.lock | Extremely fast, Rust-based, pip-compatible |
| **poetry** | Complete project management | pyproject.toml | poetry.lock | Dependency resolution, packaging, publishing |
| **conda** | Scientific computing, non-Python deps | environment.yml | conda.lock | Cross-language, binary packages, environments |
| **pip** | Standard Python package installer | requirements.txt | N/A | Universal, simple, built-in |
| **pipenv** | Development environments | Pipfile | Pipfile.lock | Automatic venv, deterministic builds |
| **pdm** | PEP 582 compliant, modern | pyproject.toml | pdm.lock | Standards-based, fast, centralized cache |

---

## Command Reference

### Installing Packages

#### Production Dependencies

```bash
# uv
uv pip install <package>
uv pip install "package>=1.0,<2.0"

# poetry
poetry add <package>
poetry add "package>=1.0,<2.0"

# conda
conda install <package>
conda install "package>=1.0,<2.0"

# pip
pip install <package>
pip install "package>=1.0,<2.0"

# pipenv
pipenv install <package>

# pdm
pdm add <package>
```

#### Development Dependencies

```bash
# uv
uv pip install --group dev <package>

# poetry
poetry add --group dev <package>

# conda (no dev distinction)
conda install <package>

# pip (manual organization)
pip install <package>  # Add to requirements-dev.txt manually

# pipenv
pipenv install --dev <package>

# pdm
pdm add --dev <package>
```

#### Installing from Requirements Files

```bash
# uv
uv pip install -r requirements.txt

# poetry (imports to pyproject.toml)
poetry add $(cat requirements.txt)

# conda
conda install --file requirements.txt

# pip
pip install -r requirements.txt

# pipenv (imports to Pipfile)
pipenv install -r requirements.txt

# pdm (imports to pyproject.toml)
pdm add $(cat requirements.txt)
```

### Removing Packages

```bash
# uv
uv pip uninstall <package>

# poetry
poetry remove <package>

# conda
conda remove <package>

# pip
pip uninstall <package>

# pipenv
pipenv uninstall <package>

# pdm
pdm remove <package>
```

### Updating Packages

#### Update Specific Package

```bash
# uv
uv pip install --upgrade <package>

# poetry
poetry update <package>

# conda
conda update <package>

# pip
pip install --upgrade <package>

# pipenv
pipenv update <package>

# pdm
pdm update <package>
```

#### Update All Packages

```bash
# uv
uv pip install --upgrade $(uv pip list --format=freeze | cut -d'=' -f1)

# poetry
poetry update

# conda
conda update --all

# pip
pip list --outdated --format=freeze | cut -d'=' -f1 | xargs pip install -U

# pipenv
pipenv update

# pdm
pdm update
```

### Listing Packages

#### List All Installed

```bash
# uv
uv pip list

# poetry
poetry show

# conda
conda list

# pip
pip list

# pipenv
pipenv graph

# pdm
pdm list
```

#### Show Package Details

```bash
# uv
uv pip show <package>

# poetry
poetry show <package>

# conda
conda list <package>

# pip
pip show <package>

# pipenv (via graph)
pipenv graph --reverse | grep <package>

# pdm
pdm show <package>
```

#### List Outdated Packages

```bash
# uv
uv pip list --outdated

# poetry
poetry show --outdated

# conda
conda search --outdated

# pip
pip list --outdated

# pipenv
pipenv update --outdated

# pdm
pdm update --outdated
```

---

## Version Constraint Syntax

### Constraint Types

| Constraint | Syntax | Example | Meaning |
|------------|--------|---------|---------|
| **Exact** | `==` | `django==4.2.7` | Exactly version 4.2.7 |
| **Minimum** | `>=` | `requests>=2.28.0` | Version 2.28.0 or higher |
| **Maximum** | `<` | `numpy<2.0` | Any version before 2.0 |
| **Compatible** | `~=` | `flask~=2.3.0` | 2.3.0 <= version < 2.4.0 |
| **Caret** (Poetry) | `^` | `fastapi^0.100.0` | 0.100.0 <= version < 1.0.0 |
| **Range** | `>=,<` | `pandas>=1.5,<2.0` | Between 1.5 and 2.0 |
| **Exclusion** | `!=` | `sphinx!=3.0.0` | Any version except 3.0.0 |
| **Wildcard** | `*` | `pytest==7.*` | Any 7.x version |

### Combining Constraints

```python
# Multiple constraints (AND logic)
"package>=1.0,<2.0,!=1.5.0"  # 1.0 <= version < 2.0, but not 1.5.0

# Extras (optional features)
"package[extra1,extra2]>=1.0"  # Install with extras

# Environment markers
"package>=1.0; python_version>='3.8'"  # Only on Python 3.8+
```

### Package Manager Preferences

**uv**: Supports all pip-style constraints
**poetry**: Prefers caret (`^`) for automatic compatibility
**conda**: Uses standard comparison operators
**pip**: Supports all PEP 440 constraints
**pipenv**: Uses Pipfile format with version strings
**pdm**: Supports all PEP 440 constraints

---

## Configuration Files

### pyproject.toml (uv, poetry, pdm)

#### Poetry Format

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31.0"
django = ">=4.2,<5.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.0.0"

[tool.poetry.group.docs.dependencies]
sphinx = "^7.0.0"
```

#### PEP 621 Format (uv, pdm)

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "django>=4.2,<5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
]
```

### requirements.txt (pip)

```txt
# Production dependencies
requests>=2.31.0
django>=4.2,<5.0
celery[redis]~=5.3.0

# Comments are allowed
numpy==1.26.0  # Pinned for compatibility

# Environment markers
dataclasses>=0.6; python_version<'3.7'

# URLs and VCS
git+https://github.com/user/repo.git@main#egg=package
```

### environment.yml (conda)

```yaml
name: my-env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy>=1.24
  - pandas>=2.0
  - pip:
    - requests>=2.31.0
```

### Pipfile (pipenv)

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = ">=2.31.0"
django = ">=4.2,<5.0"

[dev-packages]
pytest = "*"
black = "==23.11.0"

[requires]
python_version = "3.11"
```

---

## Best Practices

### 1. Version Pinning Strategy

**For Applications** (deployed code):
- Pin exact versions in production: `package==1.2.3`
- Use lock files: `poetry.lock`, `uv.lock`, `Pipfile.lock`
- Ensures reproducible deployments

**For Libraries** (published packages):
- Use minimum version constraints: `package>=1.0`
- Allow flexibility for downstream users
- Avoid overly restrictive pins

### 2. Virtual Environment Usage

**Always use virtual environments** to isolate project dependencies:

```bash
# Standard venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows

# Poetry (auto-manages)
poetry install  # Creates venv automatically

# Conda
conda create -n myenv python=3.11
conda activate myenv

# uv
uv venv .venv
source .venv/bin/activate
```

### 3. Dependency Organization

Separate dependencies by purpose:

- **Production**: Core runtime dependencies
- **Development**: Testing, linting, formatting tools
- **Documentation**: Sphinx, mkdocs, etc.
- **Optional**: Feature-specific extras

### 4. Lock File Management

**Commit lock files** to version control:
- `poetry.lock` - Yes, always
- `uv.lock` - Yes, always
- `Pipfile.lock` - Yes, always
- `conda.lock` - Yes, if using conda-lock
- `pdm.lock` - Yes, always

**Don't commit**:
- Virtual environment directories (`.venv`, `venv`, etc.)
- `__pycache__` directories
- `.pyc` files

### 5. Updating Dependencies

**Regular updates**:
```bash
# Check for outdated packages
[package_manager] list --outdated

# Update specific critical packages
[package_manager] update requests urllib3

# Full update (test thoroughly!)
[package_manager] update
```

**Security updates**:
```bash
# Use tools like safety or pip-audit
pip install safety
safety check

# Or pip-audit
pip install pip-audit
pip-audit
```

### 6. Handling Dependency Conflicts

**Resolution strategies**:

1. **Use constraint files** (pip):
   ```bash
   pip install -c constraints.txt package
   ```

2. **Override sub-dependencies** (poetry):
   ```toml
   [tool.poetry.dependencies.package.extras]
   override = "numpy<2.0"
   ```

3. **Create separate environments** for conflicting stacks

4. **Use dependency groups** to isolate conflicts

### 7. Performance Optimization

**Use faster package managers** when possible:
- **uv**: 10-100x faster than pip
- **poetry**: Built-in dependency resolution
- **pdm**: Parallel downloads and installs

**Cache packages**:
```bash
# pip cache
pip cache dir
pip cache list

# poetry cache
poetry cache list
poetry cache clear pypi --all
```

**Use binary wheels** instead of source distributions

---

## Common Issues and Solutions

### Issue 1: Dependency Resolution Conflicts

**Symptoms**: Can't install because of version conflicts

**Solutions**:
```bash
# Poetry: Use --dry-run to preview
poetry add package --dry-run

# pip: Use pip-compile for resolution
pip install pip-tools
pip-compile requirements.in

# Create constraints file
pip freeze > constraints.txt
```

### Issue 2: Slow Installations

**Solutions**:
```bash
# Use uv instead of pip
pip install uv
uv pip install -r requirements.txt

# Use pip with caching
pip install --cache-dir ~/.pip/cache package

# Poetry: Disable parallel installers if problems
poetry config installer.parallel false
```

### Issue 3: SSL Certificate Errors

**Solutions**:
```bash
# Temporary (NOT recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org package

# Better: Fix certificate store
pip install --upgrade certifi

# Or use conda which bundles certificates
conda install package
```

### Issue 4: Package Not Found

**Solutions**:
```bash
# Check package name (case-sensitive on some indexes)
pip search package

# Try alternative indexes
pip install --index-url https://pypi.org/simple package

# For conda, add channel
conda install -c conda-forge package
```

### Issue 5: ImportError After Installation

**Solutions**:
```bash
# Verify installation
pip show package

# Check virtual environment is activated
which python  # Should point to venv

# Reinstall package
pip uninstall package
pip install package

# Check for naming conflicts (package name vs import name)
# e.g., "pillow" package but "import PIL"
```

---

## Environment Variables

### Useful Variables

```bash
# Pip configuration
PIP_INDEX_URL="https://pypi.org/simple"
PIP_TRUSTED_HOST="pypi.org"
PIP_CACHE_DIR="~/.pip/cache"
PIP_DISABLE_PIP_VERSION_CHECK=1

# Virtual environment
VIRTUAL_ENV="/path/to/venv"  # Set when venv active
PIPENV_VENV_IN_PROJECT=1     # Create .venv in project root

# Conda
CONDA_DEFAULT_ENV="myenv"     # Active conda environment
CONDA_PREFIX="/path/to/env"   # Conda environment path

# Poetry
POETRY_VIRTUALENVS_IN_PROJECT=true  # Create .venv in project
POETRY_VIRTUALENVS_CREATE=true      # Auto-create venvs
```

---

## Integration with CI/CD

### GitHub Actions

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: '3.11'
      cache: 'pip'  # or 'poetry'

  - name: Install dependencies
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
```

### GitLab CI

```yaml
test:
  image: python:3.11
  cache:
    paths:
      - .cache/pip
  before_script:
    - pip install --cache-dir .cache/pip -r requirements.txt
  script:
    - pytest
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy application
COPY . .

CMD ["python", "app.py"]
```

---

## Quick Reference Tables

### Operation Cheat Sheet

| Task | uv | poetry | conda | pip |
|------|----|---------||-----|
| Create venv | `uv venv` | `poetry install` | `conda create -n` | `python -m venv` |
| Activate | `source .venv/bin/activate` | `poetry shell` | `conda activate` | `source .venv/bin/activate` |
| Install | `uv pip install` | `poetry add` | `conda install` | `pip install` |
| Remove | `uv pip uninstall` | `poetry remove` | `conda remove` | `pip uninstall` |
| Update | `uv pip install -U` | `poetry update` | `conda update` | `pip install -U` |
| List | `uv pip list` | `poetry show` | `conda list` | `pip list` |
| Lock | Auto (uv.lock) | Auto (poetry.lock) | `conda lock` | N/A |
| Export | `uv pip freeze` | `poetry export` | `conda env export` | `pip freeze` |

### Config File Locations

| Manager | Primary Config | Lock File | Location |
|---------|---------------|-----------|----------|
| uv | pyproject.toml | uv.lock | Project root |
| poetry | pyproject.toml | poetry.lock | Project root |
| conda | environment.yml | conda.lock | Project root |
| pip | requirements.txt | N/A | Project root or subdirs |
| pipenv | Pipfile | Pipfile.lock | Project root |
| pdm | pyproject.toml | pdm.lock | Project root |

---

## Further Reading

- [PEP 440 - Version Identification](https://peps.python.org/pep-0440/)
- [PEP 508 - Dependency Specification](https://peps.python.org/pep-0508/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Conda User Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [pipenv Documentation](https://pipenv.pypa.io/)
- [PDM Documentation](https://pdm.fming.dev/)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-14
**Maintained For**: python-dependency-management skill
