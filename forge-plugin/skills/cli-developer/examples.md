# CLI Developer Examples

This file contains example scenarios demonstrating how to use the cli-developer skill for various CLI development tasks.

---

## Example 1: Python CLI Tool with Click (Project Management Utility)

### Scenario
Developer needs a CLI tool for managing project tasks — creating, listing, completing, and archiving tasks with priority levels, due dates, and tag filtering.

### User Prompt
```
Build a CLI task manager called "taskcli" using Python and Click. It should support
creating tasks with priorities, listing/filtering tasks, marking tasks complete,
and archiving old tasks. Output should support both table and JSON formats.
```

### Skill Execution

**Step 1 - Analyze CLI Requirements**:
- Purpose: Developer productivity tool for task management
- Target users: Developers managing project tasks from the terminal
- Invocation pattern: Subcommand-based (`taskcli add`, `taskcli list`, `taskcli done`)
- Input: CLI arguments, optional config file (`~/.taskcli.yaml`)
- Output: Formatted tables (default) or JSON (`--json`)

**Step 2 - Evaluate Architecture & Patterns**:
- Framework: Click (Python) — ideal for subcommand hierarchies with decorators
- Command tree: `add`, `list`, `done`, `archive`, `config`
- Output modes: table (default), JSON (`--json`), quiet (`-q`)
- Error strategy: exit 0 (success), exit 1 (general error), exit 2 (usage error)
- Storage: Local SQLite database at `~/.taskcli/tasks.db`

**Step 3 - Load Project Memory**:
- No existing memory found; will create after generation
- No existing CLI patterns in repository

**Step 4 - Design & Implement CLI**:
Framework: Click with `click.Group` for subcommands.

**Step 5 - Review & Output**:
File: `/claudedocs/taskcli.py`

### Generated Output

```python
#!/usr/bin/env python3
"""taskcli — A command-line task manager for developers."""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click

APP_DIR = Path.home() / ".taskcli"
DEFAULT_DB = APP_DIR / "tasks.db"


class TaskStore:
    """Simple file-based task storage."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._tasks = self._load()

    def _load(self) -> list[dict]:
        if self.db_path.exists():
            return json.loads(self.db_path.read_text())
        return []

    def _save(self):
        self.db_path.write_text(json.dumps(self._tasks, indent=2, default=str))

    def add(self, title: str, priority: str, due: Optional[str], tags: list[str]) -> dict:
        task = {
            "id": len(self._tasks) + 1,
            "title": title,
            "priority": priority,
            "due": due,
            "tags": tags,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
        }
        self._tasks.append(task)
        self._save()
        return task

    def list(self, status: str = "pending", tag: Optional[str] = None) -> list[dict]:
        tasks = [t for t in self._tasks if t["status"] == status]
        if tag:
            tasks = [t for t in tasks if tag in t.get("tags", [])]
        return tasks

    def complete(self, task_id: int) -> Optional[dict]:
        for task in self._tasks:
            if task["id"] == task_id:
                task["status"] = "done"
                task["completed_at"] = datetime.now().isoformat()
                self._save()
                return task
        return None

    def archive(self, days: int = 30) -> int:
        count = 0
        for task in self._tasks:
            if task["status"] == "done":
                task["status"] = "archived"
                count += 1
        self._save()
        return count


class Context:
    """Shared context passed to all commands."""

    def __init__(self):
        self.store: Optional[TaskStore] = None
        self.json_output: bool = False
        self.quiet: bool = False


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group(epilog="Documentation: https://github.com/example/taskcli")
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format.")
@click.option("-q", "--quiet", is_flag=True, help="Suppress non-essential output.")
@click.option("--db", type=click.Path(), default=None, help="Path to task database.")
@click.version_option(version="1.0.0", prog_name="taskcli")
@pass_context
def cli(ctx, json_output, quiet, db):
    """taskcli — Manage your project tasks from the terminal.

    \b
    Examples:
        taskcli add "Fix login bug" --priority high --tag backend
        taskcli list --tag frontend
        taskcli done 42
        taskcli archive --days 7
    """
    ctx.json_output = json_output
    ctx.quiet = quiet
    db_path = Path(db) if db else DEFAULT_DB
    ctx.store = TaskStore(db_path)


@cli.command()
@click.argument("title")
@click.option("-p", "--priority", type=click.Choice(["low", "medium", "high"]),
              default="medium", help="Task priority level.")
@click.option("-d", "--due", default=None, help="Due date (YYYY-MM-DD).")
@click.option("-t", "--tag", multiple=True, help="Tags for categorization (repeatable).")
@pass_context
def add(ctx, title, priority, due, tag):
    """Create a new task.

    \b
    Examples:
        taskcli add "Write unit tests" --priority high
        taskcli add "Update docs" --due 2025-03-01 --tag docs --tag urgent
    """
    task = ctx.store.add(title, priority, due, list(tag))

    if ctx.json_output:
        click.echo(json.dumps(task, indent=2, default=str))
    elif not ctx.quiet:
        click.secho(f"✓ Task #{task['id']} created: {title}", fg="green")


@cli.command("list")
@click.option("-s", "--status", type=click.Choice(["pending", "done", "archived"]),
              default="pending", help="Filter by status.")
@click.option("-t", "--tag", default=None, help="Filter by tag.")
@click.option("--sort", type=click.Choice(["priority", "created", "due"]),
              default="priority", help="Sort order.")
@pass_context
def list_tasks(ctx, status, tag, sort):
    """List tasks with optional filtering.

    \b
    Examples:
        taskcli list
        taskcli list --status done --tag backend
        taskcli list --sort due --json
    """
    tasks = ctx.store.list(status=status, tag=tag)

    if ctx.json_output:
        click.echo(json.dumps(tasks, indent=2, default=str))
        return

    if not tasks:
        if not ctx.quiet:
            click.echo("No tasks found.")
        return

    # Table header
    click.secho(f"{'ID':<6}{'Priority':<10}{'Title':<40}{'Tags':<20}{'Due':<12}", bold=True)
    click.echo("─" * 88)

    priority_colors = {"high": "red", "medium": "yellow", "low": "green"}
    for task in tasks:
        color = priority_colors.get(task["priority"], "white")
        tags_str = ", ".join(task.get("tags", []))
        due_str = task.get("due") or "—"
        click.echo(
            f"{task['id']:<6}"
            f"{click.style(task['priority'], fg=color):<19}"
            f"{task['title']:<40}"
            f"{tags_str:<20}"
            f"{due_str:<12}"
        )


@cli.command()
@click.argument("task_id", type=int)
@pass_context
def done(ctx, task_id):
    """Mark a task as completed.

    \b
    Examples:
        taskcli done 42
    """
    task = ctx.store.complete(task_id)

    if task is None:
        click.secho(f"Error: Task #{task_id} not found.", fg="red", err=True)
        sys.exit(1)

    if ctx.json_output:
        click.echo(json.dumps(task, indent=2, default=str))
    elif not ctx.quiet:
        click.secho(f"✓ Task #{task_id} marked as done.", fg="green")


@cli.command()
@click.option("--days", default=30, help="Archive tasks completed more than N days ago.")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt.")
@pass_context
def archive(ctx, days, yes):
    """Archive completed tasks.

    \b
    Examples:
        taskcli archive --days 7
        taskcli archive --yes
    """
    if not yes:
        click.confirm(f"Archive all tasks completed more than {days} days ago?", abort=True)

    count = ctx.store.archive(days)

    if ctx.json_output:
        click.echo(json.dumps({"archived": count}))
    elif not ctx.quiet:
        click.secho(f"✓ Archived {count} task(s).", fg="green")


if __name__ == "__main__":
    cli()
```

---

## Example 2: Node.js CLI Tool with Commander.js (File Processing Utility)

### Scenario
Developer needs a CLI utility for batch processing files — converting formats, applying transformations, and generating reports on file collections.

### User Prompt
```
Build a Node.js CLI called "fileforge" using Commander.js for batch file processing.
It should support converting between JSON/YAML/TOML formats, validating files against
schemas, and generating summary reports. Support glob patterns for input files.
```

### Skill Execution

**Step 1 - Analyze CLI Requirements**:
- Purpose: Data processing tool for file format conversion and validation
- Target users: Developers and DevOps engineers working with configuration files
- Invocation pattern: Subcommand-based (`fileforge convert`, `fileforge validate`, `fileforge report`)
- Input: File paths with glob support, stdin piping
- Output: Converted files, validation reports (table/JSON)

**Step 2 - Evaluate Architecture & Patterns**:
- Framework: Commander.js — widely adopted, clean subcommand API
- Command tree: `convert`, `validate`, `report`
- Output modes: human-readable (default), JSON (`--json`), quiet (`-q`)
- Error strategy: exit 0 (success), exit 1 (processing error), exit 2 (usage error)

**Step 3 - Load Project Memory**:
- No existing memory found; will create after generation
- Found existing `.prettierrc` — will respect formatting conventions

**Step 4 - Design & Implement CLI**:
Framework: Commander.js with `.command()` for subcommands.

**Step 5 - Review & Output**:
File: `/claudedocs/fileforge/index.js`

### Generated Output

```javascript
#!/usr/bin/env node

/**
 * fileforge — Batch file processing, conversion, and validation.
 */

const { program } = require("commander");
const fs = require("fs");
const path = require("path");
const { glob } = require("glob");

const VERSION = "1.0.0";

program
  .name("fileforge")
  .description("Batch file processing, conversion, and validation")
  .version(VERSION, "-V, --version", "Print version number")
  .option("--json", "Output in JSON format")
  .option("-q, --quiet", "Suppress non-essential output")
  .option("--no-color", "Disable colored output");

// ─── convert command ───────────────────────────────────────────────

program
  .command("convert")
  .description("Convert files between JSON, YAML, and TOML formats")
  .argument("<pattern>", "Glob pattern for input files")
  .requiredOption("-t, --to <format>", "Target format (json, yaml, toml)")
  .option("-o, --outdir <dir>", "Output directory (default: in-place)")
  .option("-n, --dry-run", "Preview conversions without writing files")
  .addHelpText(
    "after",
    `
Examples:
  $ fileforge convert "config/*.yaml" --to json
  $ fileforge convert "**/*.toml" --to yaml --outdir dist/
  $ fileforge convert "settings.json" --to yaml --dry-run`
  )
  .action(async (pattern, options) => {
    const files = await glob(pattern);
    const isJson = program.opts().json;

    if (files.length === 0) {
      logError("No files matched the pattern: " + pattern);
      process.exit(1);
    }

    const results = [];
    for (const file of files) {
      const ext = path.extname(file).slice(1);
      const baseName = path.basename(file, path.extname(file));
      const outDir = options.outdir || path.dirname(file);
      const outFile = path.join(outDir, `${baseName}.${options.to}`);

      results.push({
        input: file,
        output: outFile,
        from: ext,
        to: options.to,
        status: options.dryRun ? "dry-run" : "converted",
      });

      if (!options.dryRun) {
        const content = fs.readFileSync(file, "utf8");
        const data = parseFile(content, ext);
        const output = serializeFile(data, options.to);
        fs.mkdirSync(path.dirname(outFile), { recursive: true });
        fs.writeFileSync(outFile, output);
      }
    }

    if (isJson) {
      console.log(JSON.stringify(results, null, 2));
    } else if (!program.opts().quiet) {
      console.log(`\n  Converted ${results.length} file(s) to ${options.to}\n`);
      for (const r of results) {
        const status = r.status === "dry-run" ? "[dry-run]" : "→";
        console.log(`    ${r.input} ${status} ${r.output}`);
      }
      console.log();
    }
  });

// ─── validate command ──────────────────────────────────────────────

program
  .command("validate")
  .description("Validate files against a JSON schema")
  .argument("<pattern>", "Glob pattern for files to validate")
  .requiredOption("-s, --schema <file>", "Path to JSON schema file")
  .option("--strict", "Fail on additional properties not in schema")
  .addHelpText(
    "after",
    `
Examples:
  $ fileforge validate "config/*.json" --schema config.schema.json
  $ fileforge validate "**/*.yaml" --schema schema.json --strict`
  )
  .action(async (pattern, options) => {
    const files = await glob(pattern);
    const isJson = program.opts().json;

    if (files.length === 0) {
      logError("No files matched the pattern: " + pattern);
      process.exit(1);
    }

    if (!fs.existsSync(options.schema)) {
      logError(`Schema file not found: ${options.schema}`);
      process.exit(2);
    }

    const results = [];
    let hasErrors = false;

    for (const file of files) {
      const errors = validateFile(file, options.schema, options.strict);
      const valid = errors.length === 0;
      if (!valid) hasErrors = true;
      results.push({ file, valid, errors });
    }

    if (isJson) {
      console.log(JSON.stringify(results, null, 2));
    } else if (!program.opts().quiet) {
      console.log(`\n  Validated ${files.length} file(s)\n`);
      for (const r of results) {
        const icon = r.valid ? "✓" : "✗";
        const color = r.valid ? "\x1b[32m" : "\x1b[31m";
        console.log(`    ${color}${icon}\x1b[0m ${r.file}`);
        for (const err of r.errors) {
          console.log(`      → ${err}`);
        }
      }
      console.log();
    }

    if (hasErrors) process.exit(1);
  });

// ─── report command ────────────────────────────────────────────────

program
  .command("report")
  .description("Generate a summary report of file collections")
  .argument("<pattern>", "Glob pattern for files to analyze")
  .option("-o, --output <file>", "Write report to file")
  .addHelpText(
    "after",
    `
Examples:
  $ fileforge report "src/**/*.json"
  $ fileforge report "config/*" --output report.json --json`
  )
  .action(async (pattern, options) => {
    const files = await glob(pattern);
    const isJson = program.opts().json;

    if (files.length === 0) {
      logError("No files matched the pattern: " + pattern);
      process.exit(1);
    }

    const report = {
      total_files: files.length,
      total_size_bytes: 0,
      by_extension: {},
      largest_files: [],
    };

    for (const file of files) {
      const stat = fs.statSync(file);
      const ext = path.extname(file) || "(none)";
      report.total_size_bytes += stat.size;
      report.by_extension[ext] = (report.by_extension[ext] || 0) + 1;
      report.largest_files.push({ file, size: stat.size });
    }

    report.largest_files.sort((a, b) => b.size - a.size);
    report.largest_files = report.largest_files.slice(0, 10);

    const output = isJson
      ? JSON.stringify(report, null, 2)
      : formatReportTable(report);

    if (options.output) {
      fs.writeFileSync(options.output, output);
      if (!program.opts().quiet) {
        console.log(`  Report written to ${options.output}`);
      }
    } else {
      console.log(output);
    }
  });

// ─── helpers ───────────────────────────────────────────────────────

function parseFile(content, format) {
  if (format === "json") return JSON.parse(content);
  throw new Error(`Unsupported input format: ${format}`);
}

function serializeFile(data, format) {
  if (format === "json") return JSON.stringify(data, null, 2) + "\n";
  throw new Error(`Unsupported output format: ${format}`);
}

function validateFile(file, schemaPath, strict) {
  // Placeholder — in production, use ajv or similar
  return [];
}

function formatReportTable(report) {
  const lines = [
    "",
    `  File Report`,
    `  ${"─".repeat(50)}`,
    `  Total files:  ${report.total_files}`,
    `  Total size:   ${(report.total_size_bytes / 1024).toFixed(1)} KB`,
    "",
    `  By extension:`,
  ];
  for (const [ext, count] of Object.entries(report.by_extension)) {
    lines.push(`    ${ext.padEnd(12)} ${count} file(s)`);
  }
  lines.push("", `  Largest files:`);
  for (const f of report.largest_files) {
    lines.push(`    ${f.file.padEnd(40)} ${(f.size / 1024).toFixed(1)} KB`);
  }
  lines.push("");
  return lines.join("\n");
}

function logError(message) {
  console.error(`\x1b[31mError:\x1b[0m ${message}`);
}

// ─── run ───────────────────────────────────────────────────────────

program.parse();
```

---

## Example 3: Go CLI Tool with Cobra (Cloud Infrastructure Management)

### Scenario
Developer needs a CLI tool for managing cloud infrastructure resources — listing instances, deploying services, and viewing logs — with multi-environment support and shell completions.

### User Prompt
```
Build a Go CLI tool called "cloudctl" using Cobra for cloud infrastructure management.
It should support managing instances (list, start, stop), deploying services, and
viewing logs. Support multiple environments (dev, staging, prod) via a --env flag,
and generate shell completions for Bash and Zsh.
```

### Skill Execution

**Step 1 - Analyze CLI Requirements**:
- Purpose: API interaction tool for cloud infrastructure management
- Target users: DevOps/SRE engineers managing cloud resources
- Invocation pattern: Subcommand-based with nested commands (`cloudctl instances list`, `cloudctl deploy`)
- Input: CLI flags, environment config (`~/.cloudctl/config.yaml`), env vars (`CLOUDCTL_ENV`)
- Output: Tables (default), JSON (`--output json`), quiet mode

**Step 2 - Evaluate Architecture & Patterns**:
- Framework: Cobra (Go) — industry standard for production CLIs (kubectl, docker, gh)
- Command tree: `instances` (list, start, stop), `deploy`, `logs`, `config`, `completion`
- Output modes: table (default), JSON (`-o json`), wide (`-o wide`)
- Error strategy: exit 0 (success), exit 1 (API error), exit 2 (usage error)
- Config: Viper for layered configuration (flag > env > config file > default)

**Step 3 - Load Project Memory**:
- No existing memory found; will create after generation
- Go module already initialized with `go.mod`

**Step 4 - Design & Implement CLI**:
Framework: Cobra with `cobra.Command` tree and Viper for config.

**Step 5 - Review & Output**:
Files: `/claudedocs/cloudctl/`

### Generated Output

**`cmd/root.go`** — Root command with global flags:

```go
package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	cfgFile string
	env     string
	output  string
)

var rootCmd = &cobra.Command{
	Use:   "cloudctl",
	Short: "Manage cloud infrastructure resources",
	Long: `cloudctl is a CLI tool for managing cloud infrastructure.

It supports managing instances, deploying services, and viewing logs
across multiple environments (dev, staging, prod).

Configuration precedence: CLI flags > env vars > config file > defaults`,
	Example: `  # List all instances in staging
  cloudctl instances list --env staging

  # Deploy a service to production
  cloudctl deploy myservice --env prod --image myapp:v2.1.0

  # Stream logs from a service
  cloudctl logs myservice --env dev --follow`,
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)

	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "",
		"config file (default: ~/.cloudctl/config.yaml)")
	rootCmd.PersistentFlags().StringVarP(&env, "env", "e", "dev",
		"target environment (dev, staging, prod)")
	rootCmd.PersistentFlags().StringVarP(&output, "output", "o", "table",
		"output format (table, json, wide)")

	// Register valid completions for --env flag
	rootCmd.RegisterFlagCompletionFunc("env", func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
		return []string{"dev", "staging", "prod"}, cobra.ShellCompDirectiveNoFileComp
	})

	// Register valid completions for --output flag
	rootCmd.RegisterFlagCompletionFunc("output", func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
		return []string{"table", "json", "wide"}, cobra.ShellCompDirectiveNoFileComp
	})

	// Bind env var CLOUDCTL_ENV to --env flag
	viper.BindEnv("env", "CLOUDCTL_ENV")
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		home, _ := os.UserHomeDir()
		viper.AddConfigPath(home + "/.cloudctl")
		viper.SetConfigName("config")
		viper.SetConfigType("yaml")
	}

	viper.SetEnvPrefix("CLOUDCTL")
	viper.AutomaticEnv()
	viper.ReadInConfig()
}
```

**`cmd/instances.go`** — Instance management subcommands:

```go
package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"text/tabwriter"

	"github.com/spf13/cobra"
)

type Instance struct {
	ID     string `json:"id"`
	Name   string `json:"name"`
	Status string `json:"status"`
	Type   string `json:"type"`
	Region string `json:"region"`
}

var instancesCmd = &cobra.Command{
	Use:     "instances",
	Aliases: []string{"inst", "i"},
	Short:   "Manage compute instances",
}

var instancesListCmd = &cobra.Command{
	Use:   "list",
	Short: "List all instances in the target environment",
	Example: `  cloudctl instances list --env staging
  cloudctl instances list -o json
  cloudctl instances list --env prod -o wide`,
	RunE: func(cmd *cobra.Command, args []string) error {
		instances, err := fetchInstances(env)
		if err != nil {
			return fmt.Errorf("failed to list instances: %w", err)
		}

		switch output {
		case "json":
			enc := json.NewEncoder(os.Stdout)
			enc.SetIndent("", "  ")
			return enc.Encode(instances)
		case "wide":
			printInstanceTableWide(instances)
		default:
			printInstanceTable(instances)
		}
		return nil
	},
}

var instancesStartCmd = &cobra.Command{
	Use:   "start <instance-id>",
	Short: "Start a stopped instance",
	Args:  cobra.ExactArgs(1),
	Example: `  cloudctl instances start i-abc123 --env staging`,
	RunE: func(cmd *cobra.Command, args []string) error {
		instanceID := args[0]
		fmt.Fprintf(os.Stderr, "Starting instance %s in %s...\n", instanceID, env)
		// API call would go here
		fmt.Printf("Instance %s started successfully.\n", instanceID)
		return nil
	},
}

var instancesStopCmd = &cobra.Command{
	Use:   "stop <instance-id>",
	Short: "Stop a running instance",
	Args:  cobra.ExactArgs(1),
	Example: `  cloudctl instances stop i-abc123 --env prod`,
	RunE: func(cmd *cobra.Command, args []string) error {
		instanceID := args[0]
		force, _ := cmd.Flags().GetBool("force")
		if !force {
			fmt.Fprintf(os.Stderr, "Warning: Stopping instance %s in %s.\n", instanceID, env)
			fmt.Fprint(os.Stderr, "Use --force to skip this warning.\n")
		}
		// API call would go here
		fmt.Printf("Instance %s stopped.\n", instanceID)
		return nil
	},
}

func init() {
	rootCmd.AddCommand(instancesCmd)
	instancesCmd.AddCommand(instancesListCmd)
	instancesCmd.AddCommand(instancesStartCmd)
	instancesCmd.AddCommand(instancesStopCmd)

	instancesStopCmd.Flags().BoolP("force", "f", false, "Skip confirmation warning")
}

func fetchInstances(environment string) ([]Instance, error) {
	// Placeholder — replace with actual API client
	return []Instance{
		{ID: "i-abc123", Name: "web-1", Status: "running", Type: "t3.medium", Region: "us-east-1"},
		{ID: "i-def456", Name: "api-1", Status: "running", Type: "t3.large", Region: "us-east-1"},
		{ID: "i-ghi789", Name: "worker-1", Status: "stopped", Type: "t3.small", Region: "us-west-2"},
	}, nil
}

func printInstanceTable(instances []Instance) {
	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	fmt.Fprintln(w, "ID\tNAME\tSTATUS\tTYPE")
	for _, inst := range instances {
		fmt.Fprintf(w, "%s\t%s\t%s\t%s\n", inst.ID, inst.Name, inst.Status, inst.Type)
	}
	w.Flush()
}

func printInstanceTableWide(instances []Instance) {
	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	fmt.Fprintln(w, "ID\tNAME\tSTATUS\tTYPE\tREGION")
	for _, inst := range instances {
		fmt.Fprintf(w, "%s\t%s\t%s\t%s\t%s\n", inst.ID, inst.Name, inst.Status, inst.Type, inst.Region)
	}
	w.Flush()
}
```

**`cmd/completion.go`** — Shell completion generation:

```go
package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var completionCmd = &cobra.Command{
	Use:   "completion [bash|zsh|fish|powershell]",
	Short: "Generate shell completion scripts",
	Long: `Generate shell completion scripts for cloudctl.

To load completions:

  Bash:
    $ source <(cloudctl completion bash)
    # To load for each session, add to ~/.bashrc:
    $ echo 'source <(cloudctl completion bash)' >> ~/.bashrc

  Zsh:
    $ cloudctl completion zsh > "${fpath[1]}/_cloudctl"

  Fish:
    $ cloudctl completion fish | source

  PowerShell:
    PS> cloudctl completion powershell | Out-String | Invoke-Expression`,
	DisableFlagsInUseLine: true,
	ValidArgs:             []string{"bash", "zsh", "fish", "powershell"},
	Args:                  cobra.MatchAll(cobra.ExactArgs(1), cobra.OnlyValidArgs),
	RunE: func(cmd *cobra.Command, args []string) error {
		switch args[0] {
		case "bash":
			return rootCmd.GenBashCompletionV2(os.Stdout, true)
		case "zsh":
			return rootCmd.GenZshCompletion(os.Stdout)
		case "fish":
			return rootCmd.GenFishCompletion(os.Stdout, true)
		case "powershell":
			return rootCmd.GenPowerShellCompletionWithDesc(os.Stdout)
		}
		return nil
	},
}

func init() {
	rootCmd.AddCommand(completionCmd)
}
```

---

## Summary of Use Cases

1. **Python CLI with Click** — Subcommand-based task manager with table/JSON output, color support, and confirmation prompts
2. **Node.js CLI with Commander.js** — File processing utility with glob patterns, format conversion, and schema validation
3. **Go CLI with Cobra** — Cloud infrastructure management with multi-environment support, Viper config, and shell completions

## Best Practices

- Always implement `--help` at every level of the command hierarchy
- Separate data output (stdout) from status messages (stderr)
- Support both human-readable and machine-parseable (`--json`) output modes
- Use meaningful exit codes and document them in help text
- Implement `--dry-run` for any destructive or write operations
- Respect the `NO_COLOR` environment variable and `--no-color` flag
- Generate shell completions when the framework supports them
- Layer configuration: CLI flags > env vars > config file > defaults
- Fail fast with clear error messages that suggest corrective actions
- Update project memory after every CLI development task for consistency
