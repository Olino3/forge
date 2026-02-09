# Python Dependency Management - Usage Examples

This document provides 8 comprehensive examples demonstrating the `python-dependency-management` skill in action across various scenarios.

---

## Example 1: First-Time Package Installation (New Project)

### Scenario
User starts working on a new project that uses Poetry but has never run the skill before. No memory exists for this project.

### User Prompt
"Install requests and httpx packages"

### Skill Execution

**Step 1: Detect Dependency Task**
- Operation: Install
- Packages: requests, httpx
- Version constraints: None specified
- Scope: Production dependencies
- Directory: /home/user/projects/my-api

**Step 2: Load Indexes and Memory**
- Read memory indexes
- Project name: "my-api" (from git repo)
- No memory exists for "my-api" yet
- Read context indexes

**Step 3: Detect Package Manager and Environment**
- Run `detect_package_manager.sh`:
  - Found `poetry.lock` → Detected: **Poetry**
  - Poetry version: 1.7.1
- Run `detect_venv.sh`:
  - No virtual environment found
- Use `AskUserQuestion` to ask about creating `.claude-venv`:
  - "No virtual environment detected. Would you like me to create `.claude-venv` using Poetry with Python 3.11?"
  - User approves
- Create virtual environment: `poetry env use python3.11`
- Poetry creates venv at `/home/user/.cache/pypoetry/virtualenvs/my-api-Xy3z1AbC-py3.11`

**Step 4: Load Context**
- Load `context/python/dependency_management.md`
- Load `context/python/virtual_environments.md`
- Learn Poetry commands: `poetry add {package}`

**Step 5: Execute Operation**
- Activate Poetry environment (handled by Poetry)
- Execute: `poetry add requests httpx`
- Output:
  ```
  Using version ^2.31.0 for requests
  Using version ^0.25.0 for httpx

  Updating dependencies
  Resolving dependencies... (3.2s)

  Writing lock file

  Package operations: 10 installs, 0 updates, 0 removals
  - Installing certifi (2023.7.22)
  - Installing charset-normalizer (3.3.0)
  ...
  - Installing requests (2.31.0)
  - Installing httpx (0.25.0)
  ```
- Verify: `poetry show requests httpx` → Both packages listed
- Success ✓

**Step 6: Update Memory**
- Create `memory/skills/python-dependency-management/my-api/` directory
- Create `package_manager.md`:
  ```markdown
  # Package Manager: Poetry

  - **Manager**: Poetry
  - **Version**: 1.7.1
  - **Detection**: Found poetry.lock
  - **Config File**: pyproject.toml
  ```
- Create `virtual_environment.md`:
  ```markdown
  # Virtual Environment

  - **Location**: /home/user/.cache/pypoetry/virtualenvs/my-api-Xy3z1AbC-py3.11
  - **Python Version**: 3.11.5
  - **Created By**: Poetry
  - **Activation**: Handled automatically by Poetry commands
  ```
- Create `dependency_patterns.md`:
  ```markdown
  # Dependency Patterns

  - Uses Poetry's automatic version constraint (^)
  - Production dependencies added to [tool.poetry.dependencies]
  - Lock file always updated after operations
  ```
- Create `configuration_files.md`:
  ```markdown
  # Configuration Files

  - **pyproject.toml**: Main project config, Poetry dependencies
  - **poetry.lock**: Locked dependency versions
  ```
- Provide summary: "Successfully installed requests (2.31.0) and httpx (0.25.0) using Poetry. Created project memory for future operations."

### Sample Output
```
✓ Detected Poetry 1.7.1 as package manager
✓ Created virtual environment with Python 3.11
✓ Installed requests (2.31.0)
✓ Installed httpx (0.25.0)
✓ Updated poetry.lock with 10 new packages

Memory saved for project 'my-api' - future operations will be faster.
```

---

## Example 2: Installing Package with Version Constraint (Existing Memory)

### Scenario
User previously used the skill on this project. Memory exists showing it uses `uv`.

### User Prompt
"Add django>=4.2,<5.0 to the project"

### Skill Execution

**Step 1: Detect Dependency Task**
- Operation: Install
- Package: django
- Version constraint: >=4.2,<5.0
- Scope: Production

**Step 2: Load Memory**
- Project: "my-django-app"
- Load `package_manager.md` → **uv** detected previously
- Load `virtual_environment.md` → `.venv` at project root
- Load `dependency_patterns.md` → Prefers specific version constraints
- Load `configuration_files.md` → Uses pyproject.toml

**Step 3: Use Remembered Package Manager**
- Memory says: uv
- Memory says: .venv exists
- Skip detection (already know from memory)

**Step 4: Load Context**
- Load context files
- Learn uv commands: `uv pip install`

**Step 5: Execute Operation**
- Activate venv: `source .venv/bin/activate`
- Execute: `uv pip install "django>=4.2,<5.0"`
- Verify: `uv pip list | grep Django` → django 4.2.7
- Success ✓

**Step 6: Update Memory**
- Update `dependency_patterns.md` to note: User prefers explicit version ranges
- Provide summary

### Sample Output
```
✓ Using remembered package manager: uv
✓ Activated .venv
✓ Installed django (4.2.7) matching constraint >=4.2,<5.0

Updated 3 dependencies in pyproject.toml
```

---

## Example 3: Removing a Package

### Scenario
User wants to remove an unused package from a conda-managed project.

### User Prompt
"Remove the pandas package, we're not using it anymore"

### Skill Execution

**Step 1: Detect Task**
- Operation: Remove
- Package: pandas

**Step 2: Load Memory**
- Project: "data-analysis"
- Load memory → Conda environment named "data-env"

**Step 3: Use Remembered Info**
- Package manager: conda
- Environment: data-env

**Step 4: Load Context**
- Learn conda remove command

**Step 5: Execute**
- Execute: `conda remove -n data-env pandas`
- Verify: `conda list -n data-env | grep pandas` → Not found
- Success ✓

**Step 6: Update Memory**
- Update `dependency_patterns.md`: Note that pandas was removed
- This prevents future confusion if code references are found

### Sample Output
```
✓ Removed pandas from conda environment 'data-env'
✓ Freed 120 MB of disk space
```

---

## Example 4: First Install with No Virtual Environment (User Declines Creation)

### Scenario
User has a simple script project with pip, no venv, and doesn't want .claude-venv created.

### User Prompt
"Install click"

### Skill Execution

**Step 1: Detect Task**
- Operation: Install
- Package: click

**Step 2: Load Memory**
- No memory exists

**Step 3: Detect Environment**
- Detect pip (no other managers found)
- No venv detected
- Ask user: "No virtual environment found. Create .claude-venv?"
- User: "No, install to my user site-packages"

**Step 4: Load Context**
- Learn pip user install: `pip install --user`

**Step 5: Execute**
- Execute: `pip install --user click`
- Success ✓

**Step 6: Update Memory**
- Create memory noting: "No venv, user prefers --user installs"

### Sample Output
```
✓ Installed click (8.1.7) to user site-packages
⚠ Consider creating a virtual environment for better isolation
```

---

## Example 5: Updating Multiple Packages

### Scenario
User wants to update all outdated packages in a Poetry project.

### User Prompt
"Update all outdated dependencies"

### Skill Execution

**Step 1: Detect Task**
- Operation: Update
- Packages: all

**Step 2: Load Memory**
- Package manager: Poetry
- Venv: Poetry-managed

**Step 3: Use Memory**
- Skip detection

**Step 4: Load Context**
- Learn Poetry update command

**Step 5: Execute**
- Check outdated: `poetry show --outdated`
- Execute: `poetry update`
- List updates applied

**Step 6: Update Memory**
- Record which packages were updated
- Note version jumps

### Sample Output
```
✓ Updated 8 packages:
  - requests: 2.31.0 → 2.32.0
  - httpx: 0.25.0 → 0.25.2
  - pytest: 7.4.0 → 7.4.3
  (+ 5 more)

All dependencies are now up to date.
```

---

## Example 6: Handling Installation Failure

### Scenario
User tries to install a package that has dependency conflicts.

### User Prompt
"Install tensorflow==2.10.0"

### Skill Execution

**Step 1-4**: Standard detection and loading

**Step 5: Execute**
- Execute: `pip install tensorflow==2.10.0`
- Error:
  ```
  ERROR: Cannot install tensorflow==2.10.0 because these package versions have conflicting dependencies:
  - numpy>=1.24.0 (required by pandas==2.1.0)
  - numpy<1.24,>=1.22 (required by tensorflow==2.10.0)
  ```
- Analyze error: Version conflict with numpy

**Step 6: Report Failure**
- Do NOT update memory with failed operation
- Provide clear explanation and suggestions:

### Sample Output
```
✗ Failed to install tensorflow==2.10.0

Reason: Dependency conflict with numpy
  - pandas 2.1.0 requires numpy>=1.24.0
  - tensorflow 2.10.0 requires numpy<1.24

Suggestions:
1. Update tensorflow: `pip install tensorflow>=2.13.0` (supports numpy 1.24+)
2. Downgrade pandas: `pip install pandas<2.0` (if you need tensorflow 2.10)
3. Create isolated environment for tensorflow

Would you like me to try one of these solutions?
```

---

## Example 7: Installing Development Dependencies

### Scenario
User wants to install testing tools as dev dependencies in a uv project.

### User Prompt
"Install pytest, pytest-cov, and black as development dependencies"

### Skill Execution

**Step 1: Detect Task**
- Operation: Install
- Packages: pytest, pytest-cov, black
- Scope: Development

**Step 2-3: Load Memory/Detect**
- Package manager: uv
- Venv: .venv

**Step 4: Load Context**
- Learn uv dev install (add to dev group in pyproject.toml)

**Step 5: Execute**
- Execute: `uv pip install --group dev pytest pytest-cov black`
- Verify installation

**Step 6: Update Memory**
- Update `dependency_patterns.md`: Project separates dev dependencies
- Update `configuration_files.md`: Dev deps in [project.optional-dependencies.dev]

### Sample Output
```
✓ Installed development dependencies:
  - pytest (7.4.3)
  - pytest-cov (4.1.0)
  - black (23.11.0)

Added to [project.optional-dependencies.dev] in pyproject.toml
```

---

## Example 8: Listing Installed Packages

### Scenario
User wants to see what's currently installed.

### User Prompt
"What packages are installed in this project?"

### Skill Execution

**Step 1: Detect Task**
- Operation: List

**Step 2: Load Memory**
- Package manager: poetry
- Venv: Poetry-managed

**Step 3-4**: Use memory, load context

**Step 5: Execute**
- Execute: `poetry show`
- Parse output

**Step 6: Report**
- Format package list
- Separate by dependency type

### Sample Output
```
Installed packages in 'my-api':

Production (12 packages):
  - requests 2.31.0
  - httpx 0.25.0
  - pydantic 2.5.0
  - fastapi 0.104.1
  ...

Development (8 packages):
  - pytest 7.4.3
  - black 23.11.0
  - mypy 1.7.0
  ...

Total: 20 packages
Package manager: Poetry 1.7.1
Virtual environment: Active (.venv)
```

---

## Common Patterns Across Examples

All examples follow the mandatory 6-step workflow:
1. Detect operation and extract details
2. Load memory (if exists) and indexes
3. Detect or use remembered package manager and venv
4. Load relevant context
5. Execute operation with proper activation
6. Update memory and report results

The skill learns from each interaction, making future operations faster and more accurate.
