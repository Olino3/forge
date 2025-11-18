# Memory Structure: test-cli-tools

## Purpose

This directory stores **project-specific** CLI testing history, known issues, and command references learned during CLI tool testing. Each project gets its own subdirectory to track testing progress over time.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/cli/`): **Shared, static** CLI testing standards (how to test CLIs, common patterns)
- **Memory** (this directory): **Project-specific, dynamic** testing history (which commands tested, known failures, fixes applied)

**Example**:
- Context says: "Test --help first, then read-only commands, then write commands"
- Memory records: "In this project's CLI, 'list' and 'status' commands tested and pass, 'create' command fails with error X, fix applied on 2025-11-18"

## Directory Structure

```
test-cli-tools/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── tested_commands.md      # Successfully tested commands
    ├── known_issues.md         # Known failing commands and status
    ├── command_reference.md    # Complete command syntax reference
    └── test_results_history.md # Historical test results
```

## Memory Files

### 1. `tested_commands.md`

**What to store**:
- List of all successfully tested commands
- Command syntax and options
- Expected behavior documented
- Test date and result
- Example usage

**Example content**:
```markdown
# Tested Commands for mygit

## Successfully Tested Commands

### `mygit --help`
**Status**: ✅ PASS
**Last Tested**: 2025-11-18
**Exit Code**: 0
**Description**: Displays help information for all commands
**Example**:
```bash
$ mygit --help
Usage: mygit <command> [options]
...
```

### `mygit init`
**Status**: ✅ PASS
**Last Tested**: 2025-11-18
**Exit Code**: 0
**Description**: Initializes a new mygit repository
**Side Effects**: Creates `.mygit/` directory
**Example**:
```bash
$ mygit init
Initialized empty mygit repository in .mygit/
```

### `mygit status`
**Status**: ✅ PASS
**Last Tested**: 2025-11-18
**Exit Code**: 0
**Description**: Shows working tree status
**Example**:
```bash
$ mygit status
On branch main
nothing to commit, working tree clean
```

## Untested Commands

- `mygit push` - Requires remote setup
- `mygit pull` - Requires remote setup
- `mygit merge` - Requires multiple branches
```

### 2. `known_issues.md`

**What to store**:
- List of failing commands
- Failure reason and error output
- Root cause if identified
- Suggested fix
- Fix status (pending, applied, verified)
- Links to failure reports in /claudedocs

**Example content**:
```markdown
# Known Issues for mygit

## Active Issues

### Issue #1: commit command crashes without config
**Command**: `mygit commit`
**Status**: 🔴 FAIL
**Severity**: High
**First Detected**: 2025-11-18
**Last Tested**: 2025-11-18

**Error**:
```
AttributeError: 'NoneType' object has no attribute 'name'
```

**Root Cause**: Missing validation for user configuration before accessing config.user.name

**Location**: `src/commands/commit.py:45`

**Suggested Fix**:
```python
# Add validation
if not config.user or not config.user.name or not config.user.email:
    print("Error: Please configure your identity first")
    sys.exit(1)
```

**Fix Status**: Pending
**Detailed Report**: `/claudedocs/mygit_failure_commit.md`

---

### Issue #2: add command unclear error message
**Command**: `mygit add nonexistent.txt`
**Status**: 🟡 MINOR
**Severity**: Low
**First Detected**: 2025-11-18
**Last Tested**: 2025-11-18

**Error**:
```
file.txt not found
```

**Root Cause**: Generic error message doesn't suggest next steps

**Location**: `src/commands/add.py:23`

**Suggested Fix**:
```python
# Improve error message
if not os.path.exists(filename):
    print(f"Error: '{filename}' not found")
    print(f"Hint: Check the file path and try again")
    sys.exit(1)
```

**Fix Status**: Pending
**Detailed Report**: `/claudedocs/mygit_failure_add.md`

---

## Resolved Issues

### Issue #X: Example resolved issue
**Command**: `mygit example`
**Status**: ✅ FIXED
**Resolved**: 2025-11-15
**Fix Applied**: commit abc123
**Verified**: 2025-11-16
```

### 3. `command_reference.md`

**What to store**:
- Complete CLI command reference
- All commands, subcommands, options, flags
- Argument descriptions
- Usage examples
- Discovered through testing

**Example content**:
```markdown
# Command Reference for mygit

## Global Options

- `--help`, `-h`: Show help message
- `--version`, `-v`: Show version
- `--verbose`: Enable verbose output

## Commands

### `init`
**Description**: Initialize a new mygit repository

**Syntax**:
```bash
mygit init [directory]
```

**Arguments**:
- `directory` (optional): Directory to initialize (default: current directory)

**Options**: None

**Exit Codes**:
- 0: Success
- 1: Directory already initialized

**Example**:
```bash
$ mygit init
$ mygit init ~/my-project
```

---

### `add`
**Description**: Add files to the staging area

**Syntax**:
```bash
mygit add <file>...
```

**Arguments**:
- `file` (required): One or more files to add

**Options**:
- `-A`, `--all`: Add all changes
- `-u`, `--update`: Add only tracked files

**Exit Codes**:
- 0: Success
- 1: File not found or error

**Example**:
```bash
$ mygit add file.txt
$ mygit add file1.txt file2.txt
$ mygit add --all
```

---

### `commit`
**Description**: Commit staged changes

**Syntax**:
```bash
mygit commit [-m <message>]
```

**Arguments**: None

**Options**:
- `-m <message>`: Commit message (required if not using editor)
- `--amend`: Amend previous commit

**Exit Codes**:
- 0: Success
- 1: No changes staged or error

**Requirements**:
- User name and email must be configured
- At least one file must be staged

**Example**:
```bash
$ mygit commit -m "Add feature"
$ mygit commit --amend -m "Updated message"
```
```

### 4. `test_results_history.md`

**What to store**:
- Historical log of test sessions
- Date and time of testing
- Commands tested count
- Pass/fail statistics
- Links to test reports
- Trends over time

**Example content**:
```markdown
# Test Results History for mygit

## Test Session #3 - 2025-11-18 14:30

**Tester**: Claude Code skill:test-cli-tools
**Duration**: 3 minutes
**Commands Tested**: 10
**Results**:
- ✅ Passed: 8 (80%)
- ❌ Failed: 2 (20%)
- ⚠️ Skipped: 0 (0%)

**New Issues Found**: 2
**Issues Resolved**: 0

**Report**: `/claudedocs/mygit_test_summary_2025-11-18.md`

### Commands Tested
- mygit --help ✅
- mygit --version ✅
- mygit init ✅
- mygit add file.txt ❌
- mygit commit ❌
- mygit status ✅
- mygit log ✅
- mygit config --list ✅
- mygit branch ✅
- mygit invalid-cmd ✅

### Notable Changes
- First comprehensive test of mygit CLI
- Discovered 2 new issues (#1, #2)
- All read-only commands working correctly

---

## Test Session #2 - 2025-11-15 10:00

**Tester**: Claude Code skill:test-cli-tools
**Duration**: 2 minutes
**Commands Tested**: 5
**Results**:
- ✅ Passed: 4 (80%)
- ❌ Failed: 1 (20%)
- ⚠️ Skipped: 0 (0%)

**New Issues Found**: 1
**Issues Resolved**: 1

**Report**: `/claudedocs/mygit_test_summary_2025-11-15.md`

### Commands Tested
- mygit --help ✅
- mygit init ✅
- mygit status ✅
- mygit log ✅
- mygit commit ❌

### Notable Changes
- Resolved issue with init command
- commit command still failing

---

## Test Session #1 - 2025-11-10 09:00

**Tester**: Claude Code skill:test-cli-tools
**Duration**: 1 minute
**Commands Tested**: 3
**Results**:
- ✅ Passed: 2 (67%)
- ❌ Failed: 1 (33%)
- ⚠️ Skipped: 0 (0%)

**New Issues Found**: 1
**Issues Resolved**: 0

**Report**: `/claudedocs/mygit_test_summary_2025-11-10.md`

### Commands Tested
- mygit --help ✅
- mygit --version ✅
- mygit init ❌

### Notable Changes
- Initial test of mygit CLI
- init command failing

---

## Trends

| Session | Date | Commands | Pass Rate | New Issues | Resolved |
|---------|------|----------|-----------|------------|----------|
| #1 | 2025-11-10 | 3 | 67% | 1 | 0 |
| #2 | 2025-11-15 | 5 | 80% | 1 | 1 |
| #3 | 2025-11-18 | 10 | 80% | 2 | 0 |

**Overall Progress**: Pass rate stable at 80%, expanding test coverage
```

## Workflow

### When Creating Memory (First Time)

1. **During Step 1 (Initial Analysis)**:
   - Identify project name from repository or CLI tool name
   - Check if `{project-name}/` directory exists
   - If not exists, note that memory will be created in Step 7

2. **During Step 3 (Load Project Memory)**:
   - If directory doesn't exist: Note this is first-time testing
   - Continue with empty memory

3. **During Step 7 (Update Memory)**:
   - Create `{project-name}/` directory
   - Create all four memory files with initial content
   - Document all test results
   - Record any issues found

### When Using Existing Memory (Subsequent Times)

1. **During Step 3 (Load Project Memory)**:
   - Read all existing memory files
   - Know which commands already tested
   - Know existing issues
   - Determine what needs retesting

2. **During Step 7 (Update Memory)**:
   - **Append** new test results to history
   - **Update** known_issues.md with status changes
   - **Add** newly tested commands to tested_commands.md
   - **Refine** command_reference.md with more details

## Memory Evolution

Memory should grow and improve over time:

### First Testing Session
- Establish baseline: which commands work
- Document first set of issues
- Create command reference skeleton

### Subsequent Sessions
- Mark issues as resolved
- Add newly tested commands
- Refine command documentation
- Track trends in pass/fail rates

### Maintenance
- Remove resolved issues from active list
- Archive old test history
- Keep command reference up-to-date
- Update when CLI changes

## Best Practices

1. **Be Specific**: Document exact commands tested, not just categories
2. **Include Dates**: Always timestamp test results
3. **Link Reports**: Reference /claudedocs failure reports
4. **Track Status**: Update issue status (pending/applied/verified)
5. **Show Trends**: Maintain historical view of testing progress
6. **Keep Current**: Update when fixes applied
7. **Document Changes**: Note when CLI version changes

## Related Files

- `../../../context/cli/cli_testing_standards.md` - CLI testing best practices (if exists)
- `/claudedocs/{cli-tool}_test_summary.md` - Detailed test reports
- `/claudedocs/{cli-tool}_failure_*.md` - Individual failure reports
- `../../index.md` - Overall memory system explanation
