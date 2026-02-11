# Python Dependency Management - Memory Structure

This file documents the memory structure for the `python-dependency-management` skill. Memory files store project-specific knowledge that improves efficiency and accuracy over time.

---

## Purpose

The memory system for `python-dependency-management` stores:
- **Package manager detection results** - Avoids re-detection on every invocation
- **Virtual environment configuration** - Remembers location and activation method
- **Dependency patterns** - Learns project-specific conventions and preferences
- **Configuration files** - Tracks which files exist and their purposes

This allows the skill to:
- **Skip detection steps** when information is already known
- **Apply learned patterns** automatically (e.g., preferred version constraints)
- **Avoid known issues** by referencing documented problems
- **Provide consistent operations** across multiple invocations

---

## Memory Directory Structure

For each project, memory is stored in:
```
../../memory/skills/python-dependency-management/{project-name}/
├── package_manager.md         # Package manager type and version
├── virtual_environment.md     # Venv location and configuration
├── dependency_patterns.md     # Installation patterns and preferences
└── configuration_files.md     # Config files and their relationships
```

Where `{project-name}` is derived from:
1. Git repository name (if project is in a git repo)
2. Directory name (if not a git repo)

---

## Memory Files

### 1. package_manager.md

**Contains**:
- Package manager name (uv, poetry, conda, pip, pipenv, pdm)
- Package manager version
- How it was detected
- Configuration file locations
- Manager-specific settings

**When created**: First time the skill runs on a project
**When updated**: When package manager version changes, or new config files are added

**Example content**:
```markdown
# Package Manager Configuration

- **Manager**: Poetry
- **Version**: 1.7.1
- **Detection**: Found poetry.lock
- **Config File**: pyproject.toml
- **Lock File**: poetry.lock
```

### 2. virtual_environment.md

**Contains**:
- Virtual environment type (venv, poetry, conda)
- Absolute path to venv
- Python version in venv
- Activation command
- Who created it (Claude, user, package manager)

**When created**: First time venv is detected or created
**When updated**: When venv is recreated, Python version changes, or location changes

**Example content**:
```markdown
# Virtual Environment Configuration

- **Type**: venv
- **Location**: /home/user/projects/myapp/.venv
- **Python Version**: 3.11.5
- **Activation**: source .venv/bin/activate
- **Created By**: Claude (.claude-venv)
```

### 3. dependency_patterns.md

**Contains**:
- Preferred version constraint style (exact, caret, range)
- Production vs development dependency organization
- Common package groups (testing, linting, docs)
- Update frequency patterns
- Known dependency conflicts and workarounds

**When created**: After first package installation
**When updated**: After every successful dependency operation (to learn patterns)

**Example content**:
```markdown
# Dependency Patterns

## Version Constraints
- Production: Uses caret constraints (^)
- Development: Uses >= constraints

## Common Patterns
- Always installs pytest, pytest-cov, black together
- Pins numpy<2.0 to avoid ML library conflicts

## Known Issues
- tensorflow 2.10 conflicts with pandas 2.1 (numpy versions)
  Workaround: Use tensorflow>=2.13 or pandas<2.0
```

### 4. configuration_files.md

**Contains**:
- List of all dependency-related config files
- Purpose of each file
- Which files are auto-generated vs manual
- Git tracking status (.gitignore)
- Relationships between files

**When created**: First time the skill runs
**When updated**: When new config files are created or relationships change

**Example content**:
```markdown
# Configuration Files

- **pyproject.toml**: Poetry dependencies, source of truth
- **poetry.lock**: Auto-generated lock file, committed to git
- **requirements.txt**: Exported for pip compatibility (optional)

## Relationships
- poetry.lock generated from pyproject.toml
- requirements.txt generated via `poetry export`
```

---

## Workflow Integration

### Step 2: Load Project Memory

The skill MUST check for existing memory:

```python
# Pseudocode for memory loading
project_name = get_project_name()
memory_dir = f"../../memory/skills/python-dependency-management/{project_name}/"

if memory_exists(memory_dir):
    load_file(f"{memory_dir}/package_manager.md")
    load_file(f"{memory_dir}/virtual_environment.md")
    load_file(f"{memory_dir}/dependency_patterns.md")
    load_file(f"{memory_dir}/configuration_files.md")

    # Use remembered information in Step 3
    skip_detection = True
else:
    # No memory exists, must detect in Step 3
    skip_detection = False
```

### Step 3: Use Memory or Detect

**If memory exists**:
- Skip package manager detection
- Skip virtual environment detection
- Use remembered information directly

**If memory doesn't exist**:
- Perform full detection
- Prepare information for memory creation in Step 6

### Step 6: Update Memory

**First time (no memory)**:
- Create memory directory
- Create all four memory files
- Populate with detected information

**Subsequent times (memory exists)**:
- Update `dependency_patterns.md` with new patterns learned
- Update `configuration_files.md` if new files created
- Update `package_manager.md` if version changed
- Update `virtual_environment.md` if venv changed

---

## Memory Benefits

### 1. Speed

**Without memory** (first run):
```
Step 3: Detect package manager (2-3 seconds)
Step 3: Detect virtual environment (1-2 seconds)
Step 3: Scan for config files (1 second)
Total: 4-6 seconds
```

**With memory** (subsequent runs):
```
Step 2: Load memory files (0.5 seconds)
Step 3: Use remembered information (instant)
Total: 0.5 seconds
```

**Speedup**: 8-12x faster for detection phase

### 2. Accuracy

Memory prevents issues like:
- Installing to wrong package manager
- Using wrong virtual environment
- Forgetting known dependency conflicts
- Repeating failed installation attempts

### 3. Consistency

Memory ensures:
- Same package manager used every time
- Same version constraint style applied
- Same dev dependency organization
- Predictable behavior across sessions

### 4. Learning

Memory improves over time by:
- Recording successful patterns
- Documenting failed approaches (in patterns file)
- Building project-specific knowledge
- Adapting to project conventions

---

## Memory Management

### When to Create Memory

Create memory directory and files when:
- First time the skill runs on a project
- No existing memory directory found
- Project name is successfully identified

### When to Update Memory

Update existing memory files when:
- After every successful dependency operation
- When package manager version changes
- When virtual environment is recreated
- When new configuration files are added
- When new patterns or issues are discovered

### When to Delete Memory

Delete or ignore memory when:
- Project is moved to a different location (path changes)
- Package manager is intentionally switched
- Starting fresh configuration
- Memory contains outdated or wrong information

**How to delete**:
```bash
rm -rf ../../memory/skills/python-dependency-management/{project-name}/
```

### When to Migrate Memory

Migrate memory when:
- Project is renamed
- Moving from old memory structure to new version

**How to migrate**:
```bash
# Rename directory
mv old-project-name/ new-project-name/

# Update paths inside files if needed
sed -i 's|/old/path|/new/path|g' new-project-name/*.md
```

---

## Memory Anti-Patterns

### ❌ Don't:

1. **Store absolute paths** that might change
   - ❌ `/home/user/projects/myapp/.venv`
   - ✅ `{project-root}/.venv` or relative paths

2. **Store temporary state** that should be detected fresh
   - ❌ "Currently installing package X"
   - ✅ "Typically installs packages X, Y, Z together"

3. **Store credentials or secrets**
   - ❌ PyPI tokens, private repo URLs with credentials
   - ✅ Public index URLs only

4. **Override user preferences** silently
   - ❌ Always use remembered manager even if user specifies different
   - ✅ Suggest remembered manager but allow override

5. **Keep stale information**
   - ❌ Package manager version from 6 months ago
   - ✅ Update version on every invocation

### ✅ Do:

1. **Store patterns and preferences**
   - ✅ "Prefers exact version pins in production"
   - ✅ "Uses pytest-cov with pytest"

2. **Document known issues**
   - ✅ "Package X conflicts with Y, use version constraint Z"
   - ✅ "SSL certificate error on install, use --trusted-host"

3. **Track configuration relationships**
   - ✅ "requirements.txt exported from pyproject.toml"
   - ✅ "Lock file auto-generated, don't edit manually"

4. **Record timestamps**
   - ✅ "Last detected: 2025-11-14"
   - ✅ "Last updated: 2025-11-14"

5. **Preserve user intent**
   - ✅ "User prefers development dependencies in separate file"
   - ✅ "User manually pins numpy<2.0 for compatibility"

---

## Example Memory Evolution

### First Run (Memory Created)

```markdown
# package_manager.md
- Manager: poetry
- Version: 1.7.1
- Detection: Found poetry.lock
```

### After Several Operations (Memory Enriched)

```markdown
# dependency_patterns.md (updated)
- Prefers caret constraints (^) in production
- Always installs pytest, pytest-cov, black together (dev)
- Typically updates minor versions weekly
- Pins Django to specific version for stability

## Known Issues
- numpy 2.0 breaks sklearn (use numpy<2.0)
- Tried tensorflow 2.10 but conflicts with pandas 2.1
```

Memory has grown to include learned patterns, making future operations more efficient and avoiding known issues.

---

## Template

See `templates/memory_template.md` for the complete structure to use when creating memory files.

---

## Related Files

- **Skill workflow**: `../../../skills/python-dependency-management/SKILL.md`
- **Memory template**: `../../../skills/python-dependency-management/templates/memory_template.md`
- **Context files**:
  - `../../../context/python/dependency_management.md`
  - `../../../context/python/virtual_environments.md`

---

**Version**: 0.1.0-alpha
**Last Updated**: 2025-11-14
**Maintained By**: python-dependency-management skill
