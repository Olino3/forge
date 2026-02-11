---
name: python-dependency-management
description: Intelligently manages Python dependencies and virtual environments by detecting the project's package manager (uv, poetry, conda, pip) and executing dependency operations using project-specific conventions.
version: 1.1.0
context:
  primary: [python]
  topics: [dependency_management, virtual_environments]
memory:
  scope: per-project
  files: [package_manager.md, virtual_environment.md, dependency_patterns.md, configuration_files.md]
---

# Python Dependency Management Skill

This skill provides intelligent Python dependency management by automatically detecting how a project manages its dependencies and virtual environments, then executing add/remove/update operations using the appropriate package manager and conventions.

## 🚨 MANDATORY COMPLIANCE WARNING

**CRITICAL**: This skill uses a **mandatory 6-step workflow** that MUST be followed exactly as documented. The workflow is non-negotiable and ensures:
- Correct package manager detection
- Safe virtual environment handling
- Consistent project-specific operations
- Accurate memory learning

**DO NOT skip steps, change their order, or omit any required actions.**

## File Structure

### Skill Files
```
forge-plugin/skills/python-dependency-management/
├── SKILL.md                           # This file - mandatory workflow
├── examples.md                        # 8 usage scenarios
├── scripts/
│   ├── README.md                      # Script documentation
│   ├── detect_package_manager.sh      # Detect uv, poetry, conda, pip
│   ├── detect_venv.sh                 # Find existing virtual environments
│   ├── install_package.sh             # Execute package operations
│   └── utils.sh                       # Helper functions
└── templates/
    ├── memory_template.md             # Project memory structure
    └── output_template.md             # Action report format
```

### Interface References
- [ContextProvider](../../interfaces/context_provider.md) — `getDomainIndex("python")`, `getConditionalContext("python", topic)`
- [MemoryStore](../../interfaces/memory_store.md) — `getSkillMemory("python-dependency-management", project)`, `update()`, `append()`

### Context (via ContextProvider)
- `contextProvider.getConditionalContext("python", "dependency_management")` — Package manager command reference
- `contextProvider.getConditionalContext("python", "virtual_environments")` — Virtual environment best practices

### Memory (via MemoryStore)
- `memoryStore.getSkillMemory("python-dependency-management", project)` returns per-project files:
  - `package_manager.md` — Which manager and version
  - `virtual_environment.md` — Venv location and activation
  - `dependency_patterns.md` — Installation patterns and preferences
  - `configuration_files.md` — Config files and their purposes

## Focus Areas

This skill evaluates and manages **7 critical dimensions** of Python dependency management:

1. **Package Manager Detection**: Correctly identifies uv, poetry, conda, pip, or pipenv
2. **Virtual Environment Discovery**: Finds existing venvs or creates new ones appropriately
3. **Configuration File Analysis**: Understands pyproject.toml, requirements.txt, environment.yml, etc.
4. **Dependency Resolution**: Handles version constraints and dependency conflicts
5. **Environment Activation**: Properly activates virtual environments before operations
6. **Error Handling**: Gracefully handles installation failures and provides actionable feedback
7. **Memory Learning**: Stores project-specific patterns for future efficiency

## MANDATORY WORKFLOW

### ⚠️ STEP 1: Detect Dependency Task and Gather Information

**YOU MUST:**
- Identify the user's intent: install, remove, update, or list dependencies
- Extract package names mentioned by the user
- Extract any version constraints (e.g., ">=1.2.0", "~=2.0")
- Determine the scope: production, development, or both
- Identify the target directory (current project or specified path)

**DO NOT PROCEED** to Step 2 until you have clearly identified:
1. The operation type (install/remove/update/list)
2. All package names involved
3. Any version requirements
4. The project directory path

---

### ⚠️ STEP 2: Load Indexes and Project Memory

**YOU MUST:**
1. Determine the project name from the git repository or directory name
2. Load project memory via `memoryStore.getSkillMemory("python-dependency-management", project)`
3. If memory exists, load ALL memory files:
   - `package_manager.md` - Remember which package manager this project uses
   - `virtual_environment.md` - Remember venv location and Python version
   - `dependency_patterns.md` - Remember project's dependency conventions
   - `configuration_files.md` - Remember which config files exist
4. Load domain index via `contextProvider.getDomainIndex("python")` to understand available context

**DO NOT PROCEED** to Step 3 until you have:
1. Loaded all existing project memory (or confirmed it doesn't exist yet)
2. Loaded the Python domain index via contextProvider
3. Identified the project name

---

### ⚠️ STEP 3: Detect Package Manager and Environment

**IF project memory exists and contains package_manager.md:**
- Use the remembered package manager
- Use the remembered virtual environment location
- Skip to Step 4

**IF project memory does NOT exist:**

**YOU MUST:**
1. Source and run `scripts/detect_package_manager.sh` to detect:
   - Check for `uv.lock` or `uv` in pyproject.toml
   - Check for `poetry.lock` or `[tool.poetry]` in pyproject.toml
   - Check for `conda` environment files (environment.yml)
   - Check for `Pipfile` (pipenv)
   - Default to `pip` if no other manager detected
2. Source and run `scripts/detect_venv.sh` to find virtual environments:
   - Check for `.venv`, `venv`, `.claude-venv`
   - Check for conda environments
   - Check for poetry-managed environments
3. **IF NO virtual environment exists:**
   - Use `AskUserQuestion` tool to ask user if they want to create `.claude-venv`
   - Provide context about which Python version will be used
   - If user approves, create the virtual environment using detected package manager
   - If user declines, ask where to install packages (system Python, user site-packages, or exit)
4. Record detection results for memory update in Step 6

**DO NOT PROCEED** to Step 4 until you have:
1. Confirmed which package manager to use
2. Confirmed which virtual environment to use (or created one with user approval)
3. Verified the virtual environment exists and is accessible

---

### ⚠️ STEP 4: Load Relevant Context

**YOU MUST:**
1. Load dependency management context via `contextProvider.getConditionalContext("python", "dependency_management")`:
   - Package manager command reference
   - Command equivalents across managers (uv/poetry/conda/pip)
   - Version constraint syntax for each manager
   - Configuration file formats
2. Load virtual environment context via `contextProvider.getConditionalContext("python", "virtual_environments")`:
   - Virtual environment activation methods
   - Best practices for venv management
   - Troubleshooting common venv issues

**DO NOT PROCEED** to Step 5 until you have:
1. Loaded both context topics via contextProvider
2. Understood the correct commands for the detected package manager

---

### ⚠️ STEP 5: Execute Dependency Operation

**YOU MUST:**
1. Construct the appropriate command for the operation:
   - **Install**: Use package manager's add/install command with correct flags
   - **Remove**: Use package manager's remove/uninstall command
   - **Update**: Use package manager's update/upgrade command
   - **List**: Use package manager's list/show command
2. Activate the virtual environment using the appropriate method:
   - For venv/virtualenv: `source {venv_path}/bin/activate`
   - For conda: `conda activate {env_name}`
   - For poetry: Poetry handles activation automatically
3. Execute the command using the Bash tool
4. Capture output and any errors
5. Verify the operation succeeded:
   - For install: Verify package is listed in installed packages
   - For remove: Verify package is no longer listed
   - For update: Compare versions before and after
6. If operation failed:
   - Analyze error message
   - Provide actionable feedback to user
   - Suggest fixes (update package manager, resolve conflicts, etc.)
   - Do NOT update memory with failed operations

**DO NOT PROCEED** to Step 6 until:
1. The operation has completed (successfully or with clear failure)
2. You have verified the result
3. You have provided clear feedback to the user

---

### ⚠️ STEP 6: Update Memory and Generate Report

**YOU MUST:**
1. **Update or create project memory files:**

   **If this is the first analysis (no memory existed):**
   - Use `memoryStore.update("python-dependency-management", project, "package_manager.md", content)` with detected package manager and version
   - Use `memoryStore.update(...)` for `virtual_environment.md` with venv location, Python version, activation method
   - Use `memoryStore.update(...)` for `dependency_patterns.md` with initial patterns observed
   - Use `memoryStore.update(...)` for `configuration_files.md` with detected config files

   **If memory existed:**
   - Update `dependency_patterns.md` via `memoryStore.update(...)` with new patterns:
     - Version constraint preferences
     - Dev vs prod dependency separation
     - Common package combinations
   - Update `configuration_files.md` via `memoryStore.update(...)` if new config files were created/modified
   - Update `package_manager.md` via `memoryStore.update(...)` if version changed

2. **Generate action report:**
   - Use `templates/output_template.md` as format
   - Include operation performed, packages affected, success/failure status
   - Include any warnings or recommendations
   - Save to `/claudedocs/dependency-{project-name}-{timestamp}.md` if significant changes

3. **Provide summary to user:**
   - Confirm what was done
   - List packages installed/removed/updated
   - Mention any important warnings or next steps

**DO NOT SKIP** memory updates - they are critical for improving future efficiency.

---

## Compliance Checklist

Before considering this skill execution complete, verify ALL items:

- [ ] **Step 1**: Identified operation type, package names, version constraints, and target directory
- [ ] **Step 2**: Loaded memory indexes, project memory (if exists), and context indexes
- [ ] **Step 3**: Detected or retrieved package manager and virtual environment
- [ ] **Step 3**: Asked user before creating new virtual environment (if needed)
- [ ] **Step 4**: Loaded dependency_management.md and virtual_environments.md context
- [ ] **Step 5**: Constructed correct command for detected package manager
- [ ] **Step 5**: Activated virtual environment properly
- [ ] **Step 5**: Executed operation and verified result
- [ ] **Step 6**: Updated or created all required memory files
- [ ] **Step 6**: Generated action report (if significant changes)
- [ ] **Step 6**: Provided clear summary to user

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DEPENDENCY OPERATION**

## Design Requirements

1. **Package Manager Support**:
   - Primary: uv, poetry, conda, pip
   - Secondary: pipenv, pdm
   - Always detect automatically, never assume

2. **Virtual Environment Handling**:
   - Never create without asking user
   - Always activate before operations
   - Support standard names: .venv, venv, .claude-venv
   - Support conda environments

3. **Configuration File Awareness**:
   - Respect existing config files
   - Update appropriate file for package manager
   - Preserve formatting and comments
   - Handle multiple config files (pyproject.toml + requirements.txt)

4. **Error Recovery**:
   - Graceful handling of network failures
   - Clear messages for dependency conflicts
   - Suggestions for resolution
   - Never leave environment in broken state

## Prompting Guidelines

**Automatic Activation Triggers:**
This skill automatically activates when Claude detects the user wants to:
- "install {package}"
- "add {package} to dependencies"
- "remove {package}"
- "update {package}"
- "upgrade dependencies"
- "list installed packages"

**Clear Communication:**
- Always tell user which package manager was detected
- Explain why creating .claude-venv (if asking)
- Provide progress updates for long operations
- Show full error messages when failures occur

**Memory Usage:**
- On first run: Explain that you're learning project conventions
- On subsequent runs: Mention using remembered package manager
- Update user when patterns change

## Best Practices

1. **Detection Priority Order**:
   - Check memory first (fastest, most accurate)
   - Check lock files (uv.lock, poetry.lock, Pipfile.lock)
   - Check pyproject.toml tool sections
   - Check for conda files
   - Default to pip as last resort

2. **Virtual Environment Creation**:
   - Always use `.claude-venv` name for Claude-created environments
   - Use project's Python version if detectable
   - Create in project root, not in subdirectories
   - Add to .gitignore if not already present

3. **Memory Updates**:
   - Update after every successful operation
   - Record failures in dependency_patterns.md to avoid repeating
   - Track version constraints actually used
   - Note any manual configuration changes

4. **Error Messages**:
   - Include package manager name in error context
   - Provide copy-pasteable fix commands when possible
   - Link to relevant documentation
   - Explain impact (can continue vs must fix)

## Additional Notes

### Package Manager Command Equivalents

| Operation | uv | poetry | conda | pip |
|-----------|----|---------||-----|
| Install | `uv pip install` | `poetry add` | `conda install` | `pip install` |
| Install dev | `uv pip install --dev` | `poetry add --group dev` | N/A | `pip install` (mark in requirements-dev.txt) |
| Remove | `uv pip uninstall` | `poetry remove` | `conda remove` | `pip uninstall` |
| Update | `uv pip install -U` | `poetry update` | `conda update` | `pip install -U` |
| List | `uv pip list` | `poetry show` | `conda list` | `pip list` |

### Configuration Files by Package Manager

- **uv**: `pyproject.toml` (project.dependencies), `uv.lock`
- **poetry**: `pyproject.toml` ([tool.poetry.dependencies]), `poetry.lock`
- **conda**: `environment.yml`
- **pip**: `requirements.txt`, `requirements-dev.txt`, or `pyproject.toml` (project.dependencies)
- **pipenv**: `Pipfile`, `Pipfile.lock`

### Virtual Environment Activation

**Bash/Zsh:**
```bash
source .claude-venv/bin/activate
```

**Fish:**
```fish
source .claude-venv/bin/activate.fish
```

**Windows CMD:**
```cmd
.claude-venv\Scripts\activate.bat
```

**Windows PowerShell:**
```powershell
.claude-venv\Scripts\Activate.ps1
```

### Detecting Active Virtual Environment

Check `$VIRTUAL_ENV` environment variable:
```bash
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual environment active: $VIRTUAL_ENV"
fi
```

## Further Reading

- [uv Documentation](https://github.com/astral-sh/uv)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Conda Documentation](https://docs.conda.io/)
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)
- [PEP 508 - Dependency Specification](https://peps.python.org/pep-0508/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)

## Version History

### v1.1.0 (2025-07-15)
- Phase 4 Migration: Replaced hardcoded `../../context/` and `../../memory/` paths with ContextProvider and MemoryStore interface calls
- Added Interface References section
- Updated workflow steps to use `contextProvider.getConditionalContext()` and `memoryStore.getSkillMemory()`/`memoryStore.update()`

### v1.0.0 (2025-11-14)
- Initial release
- Support for uv, poetry, conda, pip, pipenv
- Automatic package manager detection
- Virtual environment detection and creation (with user approval)
- Project-specific memory system (package manager, venv, patterns, config files)
- Centralized context system (dependency_management.md, virtual_environments.md)
- 6-step mandatory workflow
- Automatic activation when dependency tasks detected
- Helper scripts for detection and operations
- Comprehensive error handling and recovery
