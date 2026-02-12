---
name: cli-developer
description: Designs and implements command-line tools with professional CLI UX patterns. Covers argument parsing, subcommand hierarchies, help text generation, output formatting (human-readable and machine-parseable), error handling, configuration management, shell completions, and interactive prompts. Supports any language or framework including Click, Commander.js, Cobra, argparse, Clap, and more.
---

# CLI Developer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY CLI development task. Skipping steps or deviating from the procedure will result in poorly designed CLI tools with inconsistent UX. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: CLI development scenarios with sample outputs
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("cli-developer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## CLI Development Focus Areas

Comprehensive CLI development evaluates 7 critical dimensions:

1. **Argument & Option Design**: Define intuitive positional arguments, flags, and options with sensible defaults, validation, and mutual exclusivity
2. **Subcommand Architecture**: Structure multi-level command hierarchies with consistent naming, grouped help text, and command aliases
3. **Help Text & Discoverability**: Generate clear, contextual help messages with usage examples, argument descriptions, and man page compatibility
4. **Output Formatting**: Support human-readable (tables, colors, progress bars) and machine-parseable (JSON, CSV, TSV) output modes
5. **Error Handling & Exit Codes**: Provide actionable error messages, meaningful exit codes, and graceful degradation on unexpected input
6. **Configuration Management**: Layer configuration from defaults, config files, environment variables, and CLI flags with clear precedence
7. **Shell Completions & Integration**: Generate completions for Bash, Zsh, Fish, and PowerShell; support piping, stdin/stdout, and signal handling

**Note**: A great CLI tool is invisible when it works and helpful when it doesn't. Every flag, every message, every exit code must be intentional.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Analyze CLI Requirements (REQUIRED)

**YOU MUST:**
1. Determine the **purpose** of the CLI tool:
   - Developer tooling (build, test, lint, deploy)
   - System administration (file management, networking, monitoring)
   - Data processing (ETL, transformation, reporting)
   - API interaction (REST client, cloud provider CLI)
   - Project scaffolding or code generation
2. Identify the **target users**:
   - Developers using it in daily workflows
   - DevOps/SRE engineers in automation pipelines
   - End users with limited technical knowledge
   - Scripts and CI/CD systems (machine consumers)
3. Determine **invocation patterns**:
   - Single command (e.g., `curl`, `cat`)
   - Subcommand-based (e.g., `git`, `docker`, `kubectl`)
   - Interactive/wizard mode (e.g., `npm init`)
   - Daemon/long-running mode (e.g., `watch`, `serve`)
4. Identify **input sources**: arguments, stdin, files, environment variables, config files
5. Identify **output targets**: stdout, stderr, files, network

**DO NOT PROCEED WITHOUT A CLEAR UNDERSTANDING OF THE CLI'S PURPOSE AND AUDIENCE**

### ⚠️ STEP 2: Evaluate Architecture & Patterns (REQUIRED)

**YOU MUST:**
1. Select the appropriate **framework** for the target language:
   - Python: Click, Typer, argparse, Fire
   - Node.js: Commander.js, yargs, oclif, meow
   - Go: Cobra, urfave/cli, Kong
   - Rust: Clap, structopt, argh
   - Ruby: Thor, OptionParser, GLI
   - Shell: getopts, getopt
2. Design the **command tree** (if subcommand-based):
   - Group related commands logically
   - Define shared flags (global vs. local)
   - Plan command aliases for common operations
3. Evaluate **CLI conventions** for the ecosystem:
   - POSIX flag conventions (`-v`, `--verbose`)
   - GNU long-option style (`--output=FILE`)
   - Platform-specific conventions (Windows `/flag` vs. Unix `-flag`)
4. Plan **output modes**:
   - Default: human-readable with colors and formatting
   - `--json` or `--output json`: machine-parseable JSON
   - `--quiet` / `--silent`: minimal output
   - `--verbose` / `-v`: increased detail (stackable: `-vvv`)
5. Design **error handling strategy**:
   - Exit code mapping (0 = success, 1 = general error, 2 = usage error)
   - Error message format (context, cause, suggestion)
   - Stderr for errors, stdout for data

**DO NOT PROCEED WITHOUT A CLEAR ARCHITECTURAL PLAN**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("cli-developer", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from all previous skill executions for comprehensive CLI design
   - If memory exists, review previously learned CLI conventions, argument patterns, and output styles
   - If no memory exists, you will create it later in this process
2. Check for existing CLI patterns in the repository:
   - Existing CLI entry points, argument parsers, and command definitions
   - Configuration file formats and locations
   - Output formatting conventions already in use
   - Testing patterns for CLI components (snapshot testing, subprocess testing)
3. Adopt the project's existing CLI conventions if one is established
4. Note any CLI usability issues that should be addressed

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY AND EXISTING CLI PATTERNS**

### ⚠️ STEP 4: Design & Implement CLI (REQUIRED)

**YOU MUST:**
1. **Argument Parsing**:
   - Define all positional arguments with clear names and descriptions
   - Define options with short (`-o`) and long (`--output`) forms
   - Add type validation, default values, and required/optional markers
   - Implement mutually exclusive option groups where needed
   - Support environment variable fallbacks for sensitive values (tokens, passwords)
2. **Subcommand Structure** (if applicable):
   - Create logical command groups with consistent naming (verb-noun or noun-verb)
   - Implement shared parent options that propagate to subcommands
   - Add command aliases for frequently used commands
   - Include a default command or helpful error when invoked without subcommand
3. **Help Text**:
   - Write concise, actionable descriptions for every command and option
   - Include usage examples in help text (`Examples:` section)
   - Add epilog/footer text with links to documentation or support
   - Support `--help` at every level of the command hierarchy
4. **Output Formatting**:
   - Implement table output for list data with aligned columns
   - Add color support with graceful degradation (`NO_COLOR`, `--no-color`)
   - Support progress indicators for long-running operations
   - Implement `--json` flag for machine-parseable output
   - Use stderr for progress/status, stdout for data
5. **Error Handling**:
   - Return meaningful exit codes (document the mapping)
   - Print errors to stderr with context and suggested fixes
   - Handle keyboard interrupts (Ctrl+C) gracefully
   - Validate input early and fail fast with clear messages
6. **Configuration**:
   - Define configuration precedence: CLI flags > env vars > config file > defaults
   - Support standard config locations (`~/.config/tool/`, `./tool.yaml`)
   - Implement `config init`, `config show`, or `config set` subcommands if needed
7. **Shell Completions**:
   - Generate completion scripts for Bash, Zsh, Fish
   - Include dynamic completions for file paths, resource names, etc.
   - Document installation of completions in help text or README

**DO NOT GENERATE SHALLOW OR HALF-IMPLEMENTED CLI TOOLS**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST:**
1. **Validate the CLI design**:
   - Every command and option has help text
   - Exit codes are consistent and documented
   - Error messages include context and suggestions
   - Output modes (human, JSON, quiet, verbose) work correctly
   - No ambiguous or conflicting flags
2. **Test considerations**:
   - Unit tests for argument parsing and validation logic
   - Integration tests for command execution and output
   - Snapshot tests for help text stability
   - Edge cases: empty input, invalid flags, missing required args
3. **Ask user for output destination**:
   - **Option A**: Write to file(s) in the repository
   - **Option B**: Write to `/claudedocs/` directory
   - **Option C (Default)**: Output inline in the conversation
4. Save the generated CLI code to the chosen destination
5. Confirm the output was written successfully

**DO NOT SKIP VALIDATION**

**After completing implementation, UPDATE PROJECT MEMORY**:

Use `memoryStore.update(layer="skill-specific", skill="cli-developer", project="{project-name}", ...)` to store:

1. **cli_patterns.md**: CLI framework, argument conventions, subcommand structure
2. **arg_conventions.md**: Flag naming, option styles, environment variable patterns
3. **output_formatting.md**: Output modes, color usage, table styles, JSON structure

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

This memory will be consulted in future CLI development tasks to maintain consistency.

---

## Compliance Checklist

Before completing ANY CLI development task, verify:
- [ ] Step 1: CLI purpose, target users, and invocation patterns identified
- [ ] Step 2: Framework selected, command tree designed, output modes and error strategy planned
- [ ] Step 3: Project memory checked via `memoryStore.getSkillMemory()` and existing CLI patterns reviewed
- [ ] Step 4: CLI implemented with argument parsing, help text, output formatting, error handling, configuration, and completions
- [ ] Step 5: Output validated for completeness and usability AND project memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE CLI IMPLEMENTATION**

---

## CLI Patterns Quick Reference

### Frameworks by Language

| Language | Framework      | Best For                        | Notable Feature                  |
|----------|----------------|---------------------------------|----------------------------------|
| Python   | Click          | Complex CLIs with subcommands   | Decorator-based, composable      |
| Python   | Typer          | Type-hint driven CLIs           | Auto-generates from type hints   |
| Python   | argparse       | Standard library, simple CLIs   | No dependencies required         |
| Python   | Fire           | Quick prototyping               | Auto-generates from functions    |
| Node.js  | Commander.js   | Subcommand-based CLIs           | Fluent API, widespread adoption  |
| Node.js  | yargs          | Complex argument parsing        | Middleware, validation, i18n     |
| Node.js  | oclif          | Enterprise CLIs                 | Plugin system, code generation   |
| Go       | Cobra          | Production CLIs (kubectl, hugo) | Subcommands, completions, docs   |
| Go       | urfave/cli     | Simple, fast CLIs               | Lightweight, intuitive API       |
| Rust     | Clap           | Type-safe, derive-based CLIs    | Derive macros, validation        |
| Ruby     | Thor           | Task-based CLIs                 | Rails generator foundation       |

### Universal Flag Conventions

| Flag                 | Purpose                          | Notes                          |
|----------------------|----------------------------------|--------------------------------|
| `-h`, `--help`       | Show help text                   | Framework-provided             |
| `-v`, `--verbose`    | Increase output verbosity        | Often stackable (-vvv)         |
| `-q`, `--quiet`      | Suppress non-essential output    | Opposite of verbose            |
| `--version`          | Print version and exit           | Semantic version string        |
| `-o`, `--output`     | Output file or format            | Context-dependent              |
| `--no-color`         | Disable colored output           | Respect `NO_COLOR` env var     |
| `--json`             | Machine-parseable JSON output    | Stdout only                    |
| `-n`, `--dry-run`    | Preview changes without applying | Essential for destructive ops  |
| `-f`, `--force`      | Skip confirmations               | Use with caution               |
| `--config`           | Specify config file path         | Override default locations     |

### Exit Code Conventions

| Code  | Meaning                 | Example                        |
|-------|-------------------------|--------------------------------|
| 0     | Success                 | Command completed normally     |
| 1     | General error           | Unspecified failure            |
| 2     | Usage error             | Invalid arguments or flags     |
| 126   | Cannot execute          | Permission denied              |
| 127   | Command not found       | Missing dependency             |
| 130   | Interrupted (SIGINT)    | User pressed Ctrl+C            |

---

## Further Reading

Refer to official documentation and standards:
- **CLI Guidelines**:
  - CLIG (Command Line Interface Guidelines): https://clig.dev/
  - 12 Factor CLI Apps: https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46
- **POSIX Standards**:
  - Utility Conventions: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html
- **Frameworks**:
  - Click: https://click.palletsprojects.com/
  - Commander.js: https://github.com/tj/commander.js
  - Cobra: https://cobra.dev/
  - Clap: https://docs.rs/clap/
- **UX Patterns**:
  - NO_COLOR standard: https://no-color.org/
  - Terminal colors: https://terminalcolors.com/

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow
  - CLI architecture and UX pattern guidance
  - Framework selection matrix for 6 languages
  - Universal flag conventions and exit code standards
  - Project memory system for CLI conventions
  - Example scenarios for Python, Node.js, and Go CLIs
