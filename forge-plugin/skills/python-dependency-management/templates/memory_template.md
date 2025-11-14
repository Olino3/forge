# Project Memory Template

This template defines the structure for project-specific memory files in the `python-dependency-management` skill.

Memory files are stored in: `../../memory/skills/python-dependency-management/{project-name}/`

---

## File 1: package_manager.md

```markdown
# Package Manager Configuration

## Detected Manager

- **Manager**: [uv|poetry|conda|pipenv|pdm|pip]
- **Version**: [version number]
- **Detection Method**: [e.g., "Found poetry.lock", "Found uv.lock", "Default pip"]
- **Installation Path**: [path to package manager executable]

## Configuration Files

- **Primary Config**: [e.g., pyproject.toml, environment.yml, requirements.txt]
- **Lock File**: [e.g., poetry.lock, uv.lock, Pipfile.lock, conda.lock]
- **Additional Files**: [e.g., requirements-dev.txt, setup.py]

## Manager-Specific Notes

[Any special configuration or settings for this project]

## Detection History

- **First Detected**: [YYYY-MM-DD]
- **Last Verified**: [YYYY-MM-DD]
- **Changes**: [Note any changes to package manager over time]
```

---

## File 2: virtual_environment.md

```markdown
# Virtual Environment Configuration

## Environment Details

- **Type**: [venv|poetry|conda]
- **Location**: [absolute path to virtual environment]
- **Created By**: [Claude|User|Package Manager]
- **Creation Date**: [YYYY-MM-DD]

## Python Version

- **Version**: [e.g., 3.11.5]
- **Executable Path**: [path to python executable in venv]

## Activation

- **Activation Command**: [OS-specific command]
- **Shell**: [bash|zsh|fish|cmd|powershell]
- **Auto-activation**: [yes|no - e.g., Poetry auto-activates]

## Environment Variables

- **VIRTUAL_ENV**: [path if applicable]
- **CONDA_DEFAULT_ENV**: [name if applicable]
- **Other Variables**: [any project-specific environment variables]

## Size and Package Count

- **Total Packages**: [number]
- **Disk Usage**: [size in MB/GB]
- **Last Updated**: [YYYY-MM-DD]

## Notes

[Any special notes about this environment]
```

---

## File 3: dependency_patterns.md

```markdown
# Dependency Patterns and Preferences

## Version Constraint Style

- **Preferred Style**: [exact|caret|tilde|compatible|range]
- **Examples**:
  - Production: [e.g., "django==4.2.7" or "django^4.2"]
  - Development: [e.g., "pytest>=7.0,<8.0"]

## Dependency Organization

- **Production Dependencies**: [How they're organized]
- **Development Dependencies**: [How they're organized]
- **Optional Dependencies**: [If applicable]
- **Extras**: [If using extras syntax: package[extra]]

## Common Patterns

### Installation Patterns

- [Pattern 1: e.g., "Always installs test dependencies together"]
- [Pattern 2: e.g., "Uses specific constraints for Django packages"]
- [Pattern 3: e.g., "Pins numpy to avoid ML library conflicts"]

### Update Patterns

- [How updates are typically handled]
- [Which packages are updated regularly vs pinned]

### Removal Patterns

- [Any patterns in removing packages]

## Package Groups

### Core Dependencies
[List core packages that are always needed]

### Testing Dependencies
[List testing packages]

### Development Tools
[List dev tools like linters, formatters]

### Optional/Conditional Dependencies
[List optional dependencies and when they're used]

## Known Issues and Workarounds

### Issue 1: [Description]
- **Problem**: [What breaks]
- **Workaround**: [How to fix]
- **Affected Packages**: [Which packages]

## Dependency Update History

- **[YYYY-MM-DD]**: [What was updated and why]
- **[YYYY-MM-DD]**: [What was updated and why]

## Notes

[Any additional patterns or preferences learned]
```

---

## File 4: configuration_files.md

```markdown
# Configuration Files

## Detected Configuration Files

### Primary Configuration

- **File**: [e.g., pyproject.toml]
- **Purpose**: [e.g., "Poetry dependencies and project metadata"]
- **Format**: [TOML|YAML|INI|plain text]
- **Sections Used**:
  - [e.g., "[tool.poetry.dependencies]"]
  - [e.g., "[tool.poetry.group.dev.dependencies]"]

### Lock Files

- **File**: [e.g., poetry.lock]
- **Purpose**: [e.g., "Locked versions for reproducible installs"]
- **Auto-generated**: [yes|no]
- **Committed to Git**: [yes|no]

### Additional Configuration

- **File**: [e.g., requirements.txt]
- **Purpose**: [e.g., "Fallback for pip compatibility"]
- **Maintained By**: [Auto|Manual|Both]

### Package Manager Configuration

- **File**: [e.g., pyproject.toml [tool.uv]]
- **Settings**: [List important settings]

## File Relationships

[Explain how different config files relate]
- [e.g., "pyproject.toml is source of truth, requirements.txt generated from it"]

## Update Strategy

- **Which files to update manually**: [List]
- **Which files are auto-updated**: [List]
- **Update Order**: [If order matters]

## Git Tracking

- **Tracked Files**:
  - [File 1]
  - [File 2]
- **Ignored Files**:
  - [File 1]
  - [File 2]

## Configuration History

- **[YYYY-MM-DD]**: [Change made and why]
- **[YYYY-MM-DD]**: [Change made and why]

## Notes

[Any special notes about configuration]
```

---

## Usage Instructions

When creating memory for a new project:

1. **Create the directory**: `../../memory/skills/python-dependency-management/{project-name}/`

2. **Create all four files** using this template structure

3. **Fill in detected information** from Steps 2-5 of the workflow

4. **Leave placeholders** for information not yet available (will be filled in later)

5. **Update existing files** when new information is learned

## Update Guidelines

- **Always update** memory files after successful operations
- **Add to history sections** when significant changes occur
- **Preserve patterns** that emerge over multiple operations
- **Document failures** in "Known Issues" to avoid repeating mistakes
- **Update timestamps** (Last Updated, Last Verified) when files change

## Benefits of This Structure

- **Faster future operations**: Skip detection by using remembered information
- **Consistent operations**: Apply learned patterns automatically
- **Avoid known issues**: Reference documented problems and workarounds
- **Project continuity**: Maintain context across sessions
- **Better error recovery**: Understand project history when debugging

---

<!--
This template is used by the python-dependency-management skill.
Do not modify the structure without updating SKILL.md workflow documentation.
-->
