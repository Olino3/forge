---
name: test-cli-tools
description: Iterative testing of command-line interface tools with automated failure detection, documentation, and fix suggestions.
version: "0.3.0-alpha"
context:
  primary: []
  topics: []
memory:
  scope: per-project
  files: [tested_commands.md, known_issues.md, command_reference.md, test_results_history.md]
---

# test-cli-tools

## Title

**CLI Tool Testing & Validation** - Iterative testing of command-line interface tools with automated failure detection, documentation, and fix suggestions.

## Version

**v1.0.0** - Initial release

## File Structure

### Skill Files
```
forge-plugin/skills/test-cli-tools/
├── SKILL.md                          # This file
├── examples.md                       # Usage examples
├── scripts/
│   └── test_runner.py                # Helper for running tests
└── templates/
    ├── test_report_template.md       # Test report format
    └── failure_report_template.md    # Failure documentation format
```

### Interface References
- [ContextProvider](../../interfaces/context_provider.md) — `detectProjectType()`, `getConditionalContext(domain, topic)` (if CLI context domain exists)
- [MemoryStore](../../interfaces/memory_store.md) — `getSkillMemory("test-cli-tools", project)`, `update()`

### Memory (via MemoryStore)
- `memoryStore.getSkillMemory("test-cli-tools", project)` returns per-project files:
  - `tested_commands.md` — Successfully tested commands
  - `known_issues.md` — Known failing commands
  - `command_reference.md` — Command syntax and usage
  - `test_results_history.md` — Historical test results

## Required Reading

### Context & Memory Loading (via Interfaces)

**Before starting any CLI testing, load resources in this order:**

1. **Project Memory** (via MemoryStore):
   - `memoryStore.getSkillMemory("test-cli-tools", project)` — loads all per-project files if they exist

2. **CLI Context** (via ContextProvider, if available):
   - Use `contextProvider.detectProjectType()` to identify available domains
   - Load CLI-specific context if the domain exists

### Loading Order

**CRITICAL**: Resources must be loaded in this exact order:

```
1. Project memory via memoryStore (load previously tested commands and issues)
2. Available context via contextProvider (CLI testing standards, if domain exists)
3. CLI documentation (README, --help output)
```

## Design Requirements

### Core Principles

1. **Iterative Testing**: Test commands one at a time, systematically
2. **Failure Documentation**: Document all failures to /claudedocs with details
3. **Source Code Analysis**: Analyze code to find root cause of failures
4. **Fix Suggestions**: Provide actionable fixes for failures
5. **Project Memory**: Remember tested commands and known issues
6. **Comprehensive Coverage**: Test all commands, subcommands, options, and flags
7. **Exit Code Validation**: Verify correct exit codes (0 for success, non-zero for errors)

### Test Quality Criteria

Testing must:

- ✅ Execute each command in isolation
- ✅ Verify expected output and exit codes
- ✅ Test with valid and invalid inputs
- ✅ Check error messages are helpful
- ✅ Document failures with reproduction steps
- ✅ Suggest fixes when failures occur
- ✅ Update project memory after testing

### What NOT to Do

- ❌ Run untested commands without verification
- ❌ Skip documenting failures
- ❌ Ignore exit codes
- ❌ Test destructive commands without confirmation
- ❌ Assume commands work without testing
- ❌ Forget to update memory

## Prompting Guidelines

### User Interaction

**Clarify scope**:
- Which CLI tool to test
- Which commands/subcommands to focus on
- Whether to test with sample data or real data
- Destructive commands handling

**Confirm before testing**:
- Destructive operations (delete, remove, etc.)
- Commands that modify system state
- Commands requiring authentication/credentials

## Instructions

### Mandatory Workflow (7 Steps)

This workflow is **MANDATORY** and **NON-NEGOTIABLE**. Every step must be completed in order.

---

#### Step 1: Initial Analysis

**Purpose**: Identify the CLI tool and understand its structure.

**Actions**:
1. Determine the CLI tool to test (executable name, path)
2. Identify the project name from repository or directory
3. Find CLI documentation:
   - README files
   - `--help` or `-h` output
   - `man` pages if available
   - Online documentation
4. List all available commands and subcommands
5. Categorize commands by risk:
   - **Safe**: read-only operations (list, show, get, describe)
   - **Moderate**: operations with side effects (create, update, configure)
   - **Destructive**: dangerous operations (delete, remove, destroy, drop)
6. Check if source code is available

**Validation**:
- [ ] CLI tool identified
- [ ] Project name determined
- [ ] Documentation located
- [ ] Commands categorized by risk
- [ ] Source code availability confirmed

---

#### Step 2: Load Index Files

**Purpose**: Understand what memory and context is available.

**Actions**:
1. Use `contextProvider.detectProjectType()` to identify available context domains
2. If CLI context domain exists, load it via `contextProvider.getDomainIndex("cli")`

**Validation**:
- [ ] Available context domains identified
- [ ] CLI context loaded if available

---

#### Step 3: Load Project Memory

**Purpose**: Load previously tested commands and known issues.

**Actions**:
1. Load project memory via `memoryStore.getSkillMemory("test-cli-tools", project)`
2. If memory exists, review all files:
   - `tested_commands.md` - Previously successful tests
   - `known_issues.md` - Known failing commands
   - `command_reference.md` - Command syntax reference
   - `test_results_history.md` - Historical results
3. If no memory exists, note that this is a new project (memory will be created later)
4. Determine which commands need testing (all, or only new/changed ones)

**Validation**:
- [ ] Project memory checked
- [ ] Previous test results loaded (if available)
- [ ] Test scope determined

---

#### Step 4: Discover Commands

**Purpose**: Build comprehensive list of commands to test.

**Actions**:
1. Execute `{cli-tool} --help` to discover commands
2. For each command, execute `{cli-tool} {command} --help` to discover:
   - Subcommands
   - Options and flags
   - Required vs optional arguments
   - Examples
3. Build command test matrix:
   - Command with valid inputs
   - Command with invalid inputs
   - Command with missing required arguments
   - Command with edge cases
4. Document command signatures and expected behavior

**Validation**:
- [ ] All commands discovered
- [ ] Subcommands enumerated
- [ ] Options and flags documented
- [ ] Test matrix created

---

#### Step 5: Execute Test Suite

**Purpose**: Systematically test each command.

**Actions**:
1. **For each command in test matrix**:

   a. **Before execution**:
      - Check if command is destructive
      - If destructive, confirm with user before proceeding
      - Prepare test environment if needed

   b. **Execute command**:
      - Run command using Bash tool
      - Capture stdout, stderr, and exit code
      - Measure execution time

   c. **Verify results**:
      - Exit code: 0 for success, non-zero for expected errors
      - Output format: matches expected format
      - Error messages: clear and helpful
      - Side effects: verify intended changes occurred

   d. **Document outcome**:
      - **If PASS**: Record in tested_commands.md
      - **If FAIL**:
        - Document failure in /claudedocs/{cli-tool}_test_failures.md
        - Include: command, expected behavior, actual behavior, error output
        - Add to known_issues.md
        - Proceed to Step 6 for analysis

2. **Test categories** (in order of safety):
   - Help/info commands (`--help`, `--version`, `list`, `describe`)
   - Read-only commands (`get`, `show`, `status`)
   - Safe write commands (`create`, `update` with test data)
   - Destructive commands (only with user confirmation)

3. **For each test**:
   - Log command being tested
   - Show command output
   - Report PASS/FAIL status
   - Continue to next test

**Validation**:
- [ ] All safe commands tested
- [ ] Read-only commands tested
- [ ] Write commands tested (with confirmation)
- [ ] Destructive commands tested (with explicit confirmation)
- [ ] All results documented

---

#### Step 6: Analyze Failures

**Purpose**: For failed commands, find root cause and suggest fixes.

**Actions**:
1. **For each failed command**:

   a. **Analyze error output**:
      - Parse error messages
      - Identify error type (syntax, runtime, logic)
      - Check exit code meaning

   b. **If source code available**:
      - Search for command implementation
      - Read command handler code
      - Identify where error occurs
      - Trace error path

   c. **Diagnose root cause**:
      - Missing validation
      - Incorrect logic
      - Missing dependency
      - Configuration issue
      - Documentation mismatch

   d. **Suggest fix**:
      - Code changes needed
      - Configuration changes
      - Documentation updates
      - Usage pattern corrections

   e. **Document in failure report**:
      - Command and arguments
      - Expected behavior
      - Actual behavior
      - Error output
      - Root cause analysis
      - Suggested fix
      - Code location (file:line)

2. **Create detailed failure report in /claudedocs**:
   - Use failure_report_template.md
   - Include reproduction steps
   - Add fix suggestions
   - Link to source code locations

**Validation**:
- [ ] Each failure analyzed
- [ ] Root cause identified
- [ ] Fix suggested
- [ ] Failure report created in /claudedocs

---

#### Step 7: Update Project Memory

**Purpose**: Store test results for future reference.

**Actions**:
1. Use `memoryStore.update("test-cli-tools", project, filename, content)` for each file

2. Create or update memory files:

   **tested_commands.md**:
   - List all successfully tested commands
   - Document command syntax
   - Note test date and result
   - Include example usage

   **known_issues.md**:
   - List failing commands
   - Document failure reason
   - Link to failure report in /claudedocs
   - Note if fix is pending

   **command_reference.md**:
   - Complete command reference
   - Syntax and options
   - Expected behavior
   - Examples

   **test_results_history.md**:
   - Append test session summary
   - Commands tested count
   - Pass/fail statistics
   - Date and time

3. Create test summary report in /claudedocs:
   - Total commands tested
   - Passed commands count and list
   - Failed commands count and list
   - Coverage percentage
   - Links to detailed failure reports

**Validation**:
- [ ] Project memory directory exists
- [ ] tested_commands.md updated
- [ ] known_issues.md updated
- [ ] command_reference.md updated
- [ ] test_results_history.md updated
- [ ] Test summary created in /claudedocs

---

## Compliance Checklist

Before completing the skill invocation, verify ALL items:

### Workflow Compliance
- [ ] Step 1: Initial Analysis completed
- [ ] Step 2: Index files loaded
- [ ] Step 3: Project memory loaded
- [ ] Step 4: Commands discovered
- [ ] Step 5: Test suite executed
- [ ] Step 6: Failures analyzed (if any)
- [ ] Step 7: Memory updated

### Testing Compliance
- [ ] All safe commands tested
- [ ] Destructive commands confirmed before testing
- [ ] Exit codes verified
- [ ] Output format verified
- [ ] Error messages checked

### Documentation Compliance
- [ ] Failures documented in /claudedocs
- [ ] Root cause analysis performed
- [ ] Fixes suggested
- [ ] Memory updated with results
- [ ] Test summary created

## Best Practices

### Testing Strategy

1. **Start with safe commands**:
   - `--help`, `--version` first
   - Read-only commands next
   - Write commands with test data
   - Destructive commands last (with confirmation)

2. **Test systematically**:
   - One command at a time
   - Document each result before moving on
   - Don't skip failures - analyze them

3. **Test edge cases**:
   - Empty inputs
   - Invalid inputs
   - Missing required arguments
   - Very large inputs
   - Special characters

### Failure Analysis

1. **Read error messages carefully**:
   - Look for file paths and line numbers
   - Identify error type
   - Note any stack traces

2. **Search source code**:
   - Use Grep to find command implementations
   - Read relevant code sections
   - Understand error paths

3. **Suggest practical fixes**:
   - Specific code changes
   - Alternative approaches
   - Workarounds if fix is complex

### Documentation

1. **Failure reports should include**:
   - Clear reproduction steps
   - Expected vs actual behavior
   - Complete error output
   - Root cause if identified
   - Suggested fix
   - Code references

2. **Test summaries should include**:
   - High-level statistics
   - Quick links to failures
   - Overall assessment

## Additional Notes

### /claudedocs Directory Structure

```
/claudedocs/
├── {cli-tool}_test_summary.md           # Overall test results
├── {cli-tool}_test_failures.md          # All failures in one file
└── {cli-tool}_failure_{command}.md      # Detailed per-command failures
```

### Exit Code Conventions

- `0`: Success
- `1`: General error
- `2`: Misuse of command (invalid arguments)
- `127`: Command not found
- `130`: Terminated by Ctrl+C

### Source Code Analysis Tips

**Finding command implementations**:
- Search for command name in source
- Look for CLI framework (click, argparse, cobra, clap)
- Check for command handlers or routers
- Read main/entry point files

**Common CLI patterns**:
- Python: click, argparse, typer
- Node.js: commander, yargs, oclif
- Go: cobra, urfave/cli
- Rust: clap, structopt

### Safety Guidelines

**NEVER run without confirmation**:
- Delete commands
- Remove commands
- Drop commands
- Destroy commands
- Format commands
- System modification commands

**Always confirm**:
- Commands that modify files
- Commands that change configuration
- Commands that connect to external services
- Commands with `--force` or `--yes` flags

## Version History

### v1.1.0 (2025-07-15)
- Phase 4 Migration: Replaced hardcoded `../../context/` and `../../memory/` paths with ContextProvider and MemoryStore interface calls
- Added YAML frontmatter with context/memory declarations
- Added Interface References section
- Resolved non-existent `../../context/cli/` reference with graceful contextProvider fallback

### v1.0.0 (2025-11-18)
- Initial release
- Mandatory 7-step workflow
- Iterative command testing
- Failure analysis and fix suggestions
- /claudedocs integration
- Project-specific memory system
- Source code analysis integration
