# test-cli-tools Examples

## Usage Scenarios

This document provides practical examples of using the `test-cli-tools` skill to test various command-line tools.

## Example 1: Testing a Simple CLI Tool (git-like tool)

### Scenario
Testing a custom git-like CLI tool called `mygit` with basic commands.

### User Request
```
Please use skill:test-cli-tools to test the mygit CLI tool in this repository
```

### Skill Workflow

**Step 1-3**: Initial analysis and memory loading
- Identifies `mygit` executable in project
- Loads project memory (first time, so empty)
- Discovers commands: `init`, `add`, `commit`, `status`, `log`

**Step 4**: Command discovery
```
$ mygit --help
Available commands:
  init      Initialize a new repository
  add       Add files to staging
  commit    Commit staged changes
  status    Show working tree status
  log       Show commit history

$ mygit add --help
Usage: mygit add <file>...
Add files to the staging area
```

**Step 5**: Execute test suite
```
Testing mygit commands...

[TEST 1/8] mygit --help
✓ PASS - Help displayed, exit code 0

[TEST 2/8] mygit --version
✓ PASS - Version 1.0.0, exit code 0

[TEST 3/8] mygit init
✓ PASS - Repository initialized, exit code 0

[TEST 4/8] mygit status
✓ PASS - Shows clean working tree, exit code 0

[TEST 5/8] mygit add file.txt
✗ FAIL - Error: "file.txt not found", exit code 1
Expected: Should check if file exists before erroring

[TEST 6/8] mygit commit
✗ FAIL - Error: "AttributeError: 'NoneType' object has no attribute 'author'", exit code 1
Expected: Should show helpful error message

[TEST 7/8] mygit log
✓ PASS - Shows empty log, exit code 0

[TEST 8/8] mygit invalid-command
✓ PASS - Shows error "Unknown command", exit code 1
```

**Step 6**: Analyze failures

For `mygit add file.txt` failure:
- Searched source code in `src/commands/add.py`
- Found issue at line 23: No file existence check
- Suggested fix:
```python
# Add before staging
if not os.path.exists(filename):
    print(f"Error: '{filename}' not found")
    sys.exit(1)
```

For `mygit commit` failure:
- Searched source code in `src/commands/commit.py`
- Found issue at line 45: Assumes git config exists
- Suggested fix:
```python
# Add validation
author = git_config.get('user.name')
if not author:
    print("Error: Please configure user.name (mygit config user.name 'Your Name')")
    sys.exit(1)
```

**Step 7**: Update memory

Created `/claudedocs/mygit_test_summary.md`:
```markdown
# mygit Test Summary

**Date**: 2025-11-18
**Total Commands Tested**: 8
**Passed**: 6 (75%)
**Failed**: 2 (25%)

## Passed Commands
- mygit --help
- mygit --version
- mygit init
- mygit status
- mygit log
- mygit invalid-command (error handling works)

## Failed Commands
1. **mygit add file.txt** - Missing file existence check
   - See: /claudedocs/mygit_failure_add.md
2. **mygit commit** - Missing config validation
   - See: /claudedocs/mygit_failure_commit.md

## Recommendations
- Add file validation in add command
- Add config validation in commit command
- Improve error messages to be more user-friendly
```

---

## Example 2: Testing REST API CLI Tool

### Scenario
Testing an API client CLI tool with authentication and CRUD operations.

### User Request
```
Test the api-client tool, but skip any destructive delete commands for now
```

### Skill Workflow

**Step 1-4**: Analysis and discovery
- Tool: `api-client`
- Commands: `auth login`, `auth logout`, `get`, `post`, `put`, `delete`
- User requested skip of delete commands
- API requires authentication token

**Step 5**: Execute test suite (with constraints)
```
Testing api-client commands...

[TEST 1/10] api-client --help
✓ PASS - Help displayed

[TEST 2/10] api-client auth login --help
✓ PASS - Login help displayed

[TEST 3/10] api-client auth login
⚠ SKIP - Requires credentials (interactive)

[TEST 4/10] api-client get /users
✗ FAIL - Error: "401 Unauthorized", exit code 1
Expected: Should indicate authentication required

[TEST 5/10] api-client get /invalid
✗ FAIL - Error: "500 Internal Server Error", exit code 1
Expected: Should be 404 Not Found

[TEST 6/10] api-client post /users --data '{}'
✗ FAIL - Error: "Validation failed", exit code 1
Expected: Should list which fields are required

[TEST 7/10] api-client delete /users/1
⚠ SKIP - Destructive command (per user request)
```

**Step 6**: Analyze failures

Found issues:
1. **Authentication**: Not checking token before making requests
2. **Error handling**: Not parsing API errors properly
3. **Validation messages**: Not showing detailed validation errors

Created detailed failure reports in /claudedocs with code references and fixes.

---

## Example 3: Testing Package Manager CLI

### Scenario
Testing a custom package manager with install, update, remove commands.

### User Request
```
Test the pkg CLI tool comprehensively, including install and remove with test packages
```

### Skill Workflow

**Step 1-4**: Analysis
- Tool: `pkg`
- Commands: `install`, `update`, `remove`, `list`, `search`, `info`
- Risk: Install/remove are moderate risk (modify system)
- Strategy: Use test packages for install/remove

**Step 5**: Execute comprehensive test suite
```
Testing pkg commands...

[SAFE COMMANDS]
[TEST 1/15] pkg --help
✓ PASS

[TEST 2/15] pkg list
✓ PASS - Shows 0 packages installed

[TEST 3/15] pkg search nonexistent
✓ PASS - Shows "No packages found"

[TEST 4/15] pkg info testpkg
✗ FAIL - Error: "Package not found", exit code 1
Note: Expected behavior, but error message could be clearer

[MODERATE RISK COMMANDS]
Confirming: Will test 'pkg install' with test package. Proceed? YES

[TEST 5/15] pkg install --help
✓ PASS

[TEST 6/15] pkg install testpkg
✗ FAIL - Error: "Failed to download: Connection refused", exit code 1
Analysis: Repository URL not configured

[TEST 7/15] pkg install invalid-package
✓ PASS - Shows helpful error

[TEST 8/15] pkg update
✓ PASS - No updates available

[TEST 9/15] pkg list
✓ PASS - Still shows 0 packages (install failed)

[DESTRUCTIVE COMMANDS]
Confirming: Will test 'pkg remove' (destructive). Proceed? YES

[TEST 10/15] pkg remove nonexistent
✓ PASS - Error: "Package not installed"
```

**Step 6**: Analyze key failure
- Install failed due to missing repository configuration
- Found in `src/installer.py:67`
- Fix: Check if config exists, provide setup instructions

**Step 7**: Comprehensive documentation
- Created test summary in /claudedocs
- Documented all 15 test results
- Noted that install requires configuration setup
- Updated memory with command reference

---

## Example 4: Testing CLI with Complex Subcommands

### Scenario
Testing a Docker-like tool with nested subcommands.

### User Request
```
Test the container CLI tool, focus on container management commands
```

### Skill Workflow

**Step 4**: Complex command discovery
```
$ container --help
Commands:
  container
    list
    run
    stop
    rm
  image
    list
    pull
    build
    rm
  network
    list
    create
    rm

$ container container run --help
Usage: container container run [OPTIONS] IMAGE [COMMAND]
Options:
  -d, --detach    Run in background
  -p, --port      Publish ports
  --name         Container name
```

**Step 5**: Test subcommand hierarchies
```
Testing container CLI...

[TEST] container --help
✓ PASS

[TEST] container container --help
✓ PASS

[TEST] container container list
✓ PASS - No containers

[TEST] container container run --help
✓ PASS

[TEST] container container run alpine echo hello
⚠ SKIP - Would create container (needs confirmation)

Confirming: Create test container? YES

[TEST] container container run alpine echo hello
✓ PASS - Output: "hello", exit code 0

[TEST] container container list
✓ PASS - Shows 1 container

[TEST] container container stop <container-id>
✓ PASS - Container stopped

[TEST] container container rm <container-id>
✓ PASS - Container removed

[TEST] container image list
✓ PASS - Shows alpine image

[TEST] container network list
✓ PASS - Shows default network
```

All tests passed! Tool is working well.

**Step 7**: Document comprehensive test results
- All major commands tested successfully
- No failures to analyze
- Memory updated with full command reference
- Summary shows 100% pass rate

---

## Example 5: Testing CLI with Interactive Commands

### Scenario
Testing a CLI that has interactive prompts.

### User Request
```
Test the setup CLI tool, it has interactive commands
```

### Skill Workflow

**Step 4**: Identify interactive vs non-interactive commands
```
Commands:
  setup init         (Interactive - prompts for config)
  setup config set   (Non-interactive - direct args)
  setup config get   (Non-interactive - read only)
  setup status       (Non-interactive - read only)
```

**Step 5**: Test with appropriate strategies
```
Testing setup CLI...

[TEST] setup --help
✓ PASS

[TEST] setup status
✓ PASS - Shows "Not configured"

[TEST] setup config get database.host
✗ FAIL - Error: "Config not initialized", exit code 1
Expected: Should suggest running 'setup init' first

[TEST] setup config set database.host localhost
✗ FAIL - Same error

[TEST] setup init
⚠ SKIP - Interactive command
Note: Would require answering prompts. Suggest non-interactive mode.

[TEST] setup init --non-interactive --defaults
✓ PASS - Initialized with defaults

[TEST] setup status
✓ PASS - Shows "Configured"

[TEST] setup config get database.host
✓ PASS - Shows "localhost"

[TEST] setup config set database.host 127.0.0.1
✓ PASS

[TEST] setup config get database.host
✓ PASS - Shows "127.0.0.1"
```

**Step 6**: Analyze early failures
- Commands failed before initialization
- Error messages didn't suggest solution
- Fix: Add helpful error suggesting `setup init --non-interactive --defaults`

**Step 7**: Document findings
- Noted need for `--non-interactive` flag for CI/CD
- Suggested improving error messages
- All commands work after initialization

---

## Key Patterns

### Common Themes

1. **Start safe**: Always test `--help` and read-only commands first
2. **Confirm destructive**: Get explicit confirmation for risky commands
3. **Analyze failures**: Look at source code to find root cause
4. **Suggest fixes**: Provide actionable code changes
5. **Document thoroughly**: Create comprehensive reports in /claudedocs
6. **Update memory**: Store results for next time

### When to Use This Skill

- ✅ Testing a new CLI tool
- ✅ Validating CLI after changes
- ✅ Documenting CLI behavior
- ✅ Finding and fixing CLI bugs
- ✅ Verifying error handling

### When NOT to Use This Skill

- ❌ Testing GUIs
- ❌ Testing web applications (use different tools)
- ❌ Running production commands on live systems
- ❌ Testing without source code access (limited analysis)

---

## Tips for Best Results

1. **Be specific about scope**:
   - Good: "Test all read-only commands"
   - Better: "Test get, list, and describe commands, skip delete"

2. **Provide context**:
   - Mention if tool requires setup
   - Note if credentials needed
   - Specify test data location

3. **Set boundaries**:
   - "Skip destructive commands"
   - "Only test with test-* files"
   - "Don't connect to production"

4. **Review results**:
   - Check /claudedocs for detailed reports
   - Review suggested fixes
   - Run fixed commands manually

5. **Build project memory**:
   - Use skill multiple times on same project
   - Memory will track tested vs untested commands
   - Known issues will be remembered
