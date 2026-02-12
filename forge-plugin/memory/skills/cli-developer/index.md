# cli-developer Memory

Project-specific memory for CLI development patterns, argument conventions, and output formatting preferences.

## Purpose

This memory helps the `skill:cli-developer` remember:
- Which CLI framework and argument style each project uses
- Project-specific flag naming conventions and option patterns
- Output formatting preferences (table styles, color usage, JSON structure)
- Configuration management strategy and file locations
- Common subcommand patterns and command tree structure

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `cli_patterns.md`

**Purpose**: Track CLI framework, architecture, and design patterns for this project

**Should contain**:
- **Framework**: Which CLI framework is used (Click, Cobra, Commander.js, etc.)
- **Command structure**: Flat commands vs. subcommand hierarchy
- **Global flags**: Flags available on all commands (--verbose, --env, --output)
- **Plugin system**: Whether the CLI supports plugins or extensions
- **Entry points**: How the CLI is invoked and installed

**Example structure**:
```markdown
# CLI Patterns - MyProject

## Framework
- Language: Python 3.11+
- Framework: Click 8.x with click-plugins
- Entry point: `src/cli/main.py` → `mycli` console_script

## Command Structure
Subcommand-based with two levels:
- `mycli auth login|logout|status`
- `mycli resources list|create|delete`
- `mycli config show|set|init`

## Global Flags
- `--env` / `-e`: Target environment (dev, staging, prod)
- `--verbose` / `-v`: Increase output detail (stackable)
- `--quiet` / `-q`: Suppress non-essential output
- `--output` / `-o`: Output format (table, json, csv)
- `--no-color`: Disable colored output

## Plugin System
Uses click-plugins for third-party command registration.
Plugin commands registered under `mycli plugins` namespace.

## Installation
- pip install: `pip install mycli`
- Completions: `mycli completion install`
```

**When to update**: After each CLI development or modification task

---

#### `arg_conventions.md`

**Purpose**: Document argument naming, flag styles, and validation patterns

**Should contain**:
- **Naming conventions**: How flags and options are named (kebab-case, camelCase)
- **Short flag assignments**: Which single-letter flags are used and available
- **Required vs. optional**: How required arguments are indicated
- **Environment variable mapping**: How flags map to env vars
- **Validation rules**: Common validation patterns for arguments

**Example structure**:
```markdown
# Argument Conventions - MyProject

## Naming
- Long flags: kebab-case (--output-format, --dry-run)
- Short flags: single letter, lowercase (-o, -n, -v)
- Positional args: lowercase, descriptive (resource-name, file-path)

## Short Flag Registry
| Short | Long            | Command   | Description         |
|-------|-----------------|-----------|---------------------|
| -e    | --env           | global    | Target environment  |
| -o    | --output        | global    | Output format       |
| -v    | --verbose       | global    | Verbosity level     |
| -q    | --quiet         | global    | Suppress output     |
| -f    | --force         | delete    | Skip confirmation   |
| -n    | --dry-run       | deploy    | Preview only        |
| -t    | --tag           | create    | Resource tags       |

## Environment Variable Mapping
Pattern: `MYCLI_{FLAG_NAME}` (uppercase, underscores)
- `MYCLI_ENV` → --env
- `MYCLI_OUTPUT` → --output
- `MYCLI_API_KEY` → --api-key (sensitive, never in config file)

## Validation Patterns
- Environments: choice validation (dev|staging|prod)
- File paths: existence check with clear error on missing
- Resource names: regex ^[a-z0-9-]{3,63}$ with explanation on failure
```

**When to update**: When new flags or arguments are added or conventions change

---

#### `output_formatting.md`

**Purpose**: Track output formatting conventions, color usage, and structured output patterns

**Should contain**:
- **Table format**: Column alignment, header style, separator characters
- **Color scheme**: Which colors map to which semantic meanings
- **JSON structure**: Standard fields, envelope format, error format
- **Progress indicators**: Spinner vs. progress bar, when to use each
- **Error format**: How errors are presented to users

**Example structure**:
```markdown
# Output Formatting - MyProject

## Table Format
- Headers: bold, uppercase
- Separator: ─ (box drawing character)
- Alignment: left-aligned text, right-aligned numbers
- Truncation: long values truncated at 40 chars with …
- Empty state: "No resources found." (not empty table)

## Color Scheme
| Color   | Meaning                   | Example              |
|---------|---------------------------|----------------------|
| Green   | Success, running, healthy | ✓ Deployed           |
| Red     | Error, stopped, failed    | ✗ Connection refused |
| Yellow  | Warning, pending, partial | ⚠ Degraded           |
| Blue    | Info, links, highlights   | → See docs           |
| Gray    | Disabled, archived, meta  | (deprecated)         |

## JSON Output Envelope
Standard structure for --json output:
{
  "data": [...],
  "meta": { "total": 42, "page": 1 },
  "errors": []
}

## Error Format
Pattern: "Error: {what happened}\n  → {suggestion}"
Example:
  Error: Instance i-abc123 not found in staging.
    → Run 'mycli instances list --env staging' to see available instances.

## Progress
- Short operations (<5s): spinner with status text
- Long operations (>5s): progress bar with ETA
- Batch operations: counter (3/10 processed...)
```

**When to update**: When output formatting conventions change or new patterns emerge

---

## Usage in skill:cli-developer

### Loading Memory

```markdown
# In skill workflow Step 3

project_name = detect_project_name()
memory = memoryStore.getSkillMemory("cli-developer", "{project-name}")

if memory exists:
    cli_patterns = read(memory, "cli_patterns.md")
    arg_conventions = read(memory, "arg_conventions.md")
    output_formatting = read(memory, "output_formatting.md")

    # Use for design decisions
    - Follow established framework and command patterns
    - Reuse flag naming conventions and short flag assignments
    - Match existing output formatting and color scheme
```

### Updating Memory

```markdown
# In skill workflow Step 5

After generating CLI implementation:

1. Check if new patterns emerged:
   - New commands added to the command tree?
   - New flags or argument conventions?
   - Changes to output formatting?

2. If yes, update relevant memory file:
   memoryStore.update(layer="skill-specific", skill="cli-developer",
                      project="{project-name}", ...)

3. If first time developing CLI for project:
   - Create directory and all memory files
   - Populate with observations from this implementation
```

---

## Memory Evolution Over Time

### After 1st CLI Task
```markdown
# cli_patterns.md

## Framework
- Language: Go
- Framework: Cobra + Viper
- Entry point: cmd/root.go

## Command Structure
- `mytool serve`
- `mytool migrate`
```

### After 5 CLI Tasks
```markdown
# cli_patterns.md

## Framework
- Language: Go 1.21+
- Framework: Cobra 1.8 + Viper 1.18
- Entry point: cmd/root.go → main.go
- Build: goreleaser for cross-platform binaries

## Command Structure (17 commands)
- `mytool serve` (start, stop, status)
- `mytool migrate` (up, down, status, create)
- `mytool config` (show, set, init)
- `mytool auth` (login, logout, whoami)
- `mytool completion` (bash, zsh, fish)

## Conventions Learned
- All destructive commands require --force or confirmation
- Progress output always goes to stderr
- JSON output uses { "data": ..., "meta": ... } envelope
```

### After 20 CLI Tasks
```markdown
# Comprehensive patterns, battle-tested conventions, full flag registry
# Memory now provides high-value project-specific CLI design guidance
```

---

## Related Documentation

- **Main Memory Index**: `../index.md` for memory system overview
- **Skill Documentation**: `../../skills/cli-developer/SKILL.md` for skill workflow
- **Context Files**: `../../context/` for general development knowledge
- **Memory Lifecycle**: `../lifecycle.md` for memory freshness and pruning
- **Memory Quality**: `../quality_guidance.md` for memory validation
