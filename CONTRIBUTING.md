# ⚒️ Contributing to The Forge

> *"Even the gods sought Hephaestus when they needed tools worthy of Olympus."*

Thank you for your interest in contributing to The Forge — an Agentic Software Factory powered by Claude Code. Whether you're forging a new skill, summoning a new agent, or sharpening existing tools, this guide will help you contribute effectively.

## Table of Contents

- [Getting Started](#getting-started)
- [Architecture Overview](#architecture-overview)
- [Adding New Skills](#adding-new-skills)
- [Adding New Agents](#adding-new-agents)
- [Adding New Commands](#adding-new-commands)
- [Adding Context Files](#adding-context-files)
- [Adding Hooks](#adding-hooks)
- [Coding Conventions](#coding-conventions)
- [Pull Request Process](#pull-request-process)
- [Code of Conduct](#code-of-conduct)

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** from `develop` for your changes
4. **Make your changes** following the conventions below
5. **Test** your changes with Claude Code
6. **Submit a Pull Request** against `develop`

### Prerequisites

- [Claude Code](https://claude.ai/code) installed and configured
- Git
- Bash (for hook scripts)
- No build tools, package managers, or compiled languages required — The Forge is convention-based

---

## Architecture Overview

The Forge uses an **interface-driven architecture** with four core abstractions:

| Interface | Purpose | Spec |
|-----------|---------|------|
| **ContextProvider** | Load context files by domain, tags, and sections | `interfaces/context_provider.md` |
| **MemoryStore** | Read/write project memory with automated lifecycle | `interfaces/memory_store.md` |
| **SkillInvoker** | Delegate to skills with structured I/O | `interfaces/skill_invoker.md` |
| **ExecutionContext** | Pass context between chained commands | `interfaces/execution_context.md` |

All skills, commands, and agents reference these interfaces instead of hardcoded filesystem paths. See `interfaces/README.md` for the full architecture overview.

---

## Adding New Skills

Skills are specialized capabilities invoked via `skill:{name}` syntax.

### Step-by-Step

1. **Create directory**: `forge-plugin/skills/{skill-name}/`
2. **Create `SKILL.md`** — start from `forge-plugin/skills/SKILL_TEMPLATE.md`
   - Include YAML frontmatter with `name`, `version`, `description`, `context`, `memory`, `tags`
   - Define mandatory workflow steps using interface references (`contextProvider`, `memoryStore`)
   - Include compliance checklist
   - Add version history
3. **Create `examples.md`** with 3+ usage scenarios
4. **Optional**: Add `scripts/` for shell utilities, `templates/` for output formatting
5. **Create memory index**: `forge-plugin/memory/skills/{skill-name}/index.md`
6. **Update ROADMAP.md** to list the new skill

### Skill Requirements

- Must follow the mandatory workflow pattern (see SKILL_TEMPLATE.md)
- Must use `contextProvider` for context loading (not hardcoded paths)
- Must use `memoryStore` for memory operations (not direct file I/O)
- Must include YAML frontmatter with required fields
- Output goes to `/claudedocs/` following `OUTPUT_CONVENTIONS.md`

---

## Adding New Agents

Agents are specialized AI personas with domain expertise.

### Step-by-Step

1. **Create agent file**: `forge-plugin/agents/{agent-name}.md`
   - Include YAML frontmatter: `name`, `description`, `tools`, `model`, `permissionMode`, `memory`, `skills`, `context`
   - Write the agent's mission, personality, workflow, and task patterns
2. **Create config file**: `forge-plugin/agents/{agent-name}.config.json`
   - Must conform to `interfaces/schemas/agent_config.schema.json`
   - Declare `contextDomains`, `skills`, `memory.storagePath`, `memory.fileTypes`
3. **Create memory directory**: `forge-plugin/memory/agents/{agent-name}/`
   - Add a `README.md` documenting the agent's memory structure
4. **Update ROADMAP.md** to list the new agent

### Agent Requirements

- Config.json must validate against `agent_config.schema.json`
- Memory path must use canonical location: `forge-plugin/memory/agents/{name}/`
- Frontmatter `memory:` field must match config.json `storagePath`
- No hardcoded filesystem paths in the agent.md prose

---

## Adding New Commands

Commands are structured workflows invoked via `/command-name` syntax.

### Step-by-Step

1. **Create directory**: `forge-plugin/commands/{command-name}/`
2. **Create `COMMAND.md`** with:
   - YAML frontmatter: `name`, `description`, `category`, `complexity`, `skills`, `context`
   - Structured workflow steps using `contextProvider` and `memoryStore`
   - Skill delegation patterns via `skillInvoker` (when applicable)
   - Output format specification
3. **Create `examples.md`** with usage scenarios
4. **Create context file** (optional): `forge-plugin/context/commands/{command}_patterns.md`
   - Include YAML frontmatter with `tags` and `sections`
5. **Update ROADMAP.md** to list the new command

---

## Adding Context Files

Context files are shared, static reference material organized by domain.

### Step-by-Step

1. **Place file** in appropriate domain: `forge-plugin/context/{domain}/{filename}.md`
2. **Add YAML frontmatter** (required):
   ```yaml
   ---
   id: "{domain}/{filename}"
   domain: {domain}
   title: "Human-Readable Title"
   type: framework  # always | framework | pattern | reference
   estimatedTokens: 200
   loadingStrategy: onDemand  # always | onDemand | lazy
   tags: [tag1, tag2, tag3]
   sections:
     - name: "Section Name"
       estimatedTokens: 50
       keywords: [keyword1, keyword2]
   ---
   ```
3. **Update domain index**: `forge-plugin/context/{domain}/index.md`
4. **Update main index**: `forge-plugin/context/index.md`

### Context Guidelines

- Use the **compact approach** — quick reference tables, link to official docs
- Only add knowledge that applies to **multiple projects** (project-specific → memory)
- All context files must have valid YAML frontmatter with `tags` and `sections`

---

## Adding Hooks

Hooks are bash scripts that execute in response to Claude Code events. The Forge uses **20 hooks across 9 events**, organized into 4 thematic layers.

### Hook Layers

| Layer | Purpose | Examples |
|-------|---------|----------|
| 🛡️ **Shield** | Security & initialization | `sandbox_boundary_guard`, `pii_redactor` |
| 📜 **Chronicle** | Memory & learning | `memory_quality_gate`, `memory_pruning_daemon` |
| 👷 **Foreman** | Workflow & quality | `skill_compliance_checker`, `agent_config_validator` |
| 📢 **Town Crier** | Telemetry & reporting | `system_health_emitter`, `forge_telemetry` |

### Step-by-Step

1. **Create script**: `forge-plugin/hooks/{hook_name}.sh`
2. **Source shared library**: `source "${SCRIPT_DIR}/lib/health_buffer.sh"`
3. **Follow design principles**:
   - Use `set -euo pipefail` for strict error handling
   - Complete in < 5 seconds
   - Idempotent — safe to run multiple times
   - Non-destructive — never modify source code
   - Graceful failure — warnings, not hard errors
   - Minimal dependencies — standard bash utilities only
   - Use safe grep patterns (`|| true` and `${var:-0}` for unset variables)
4. **Register in `hooks/hooks.json`** under the appropriate event and matcher:
   ```json
   {
     "event": "PostToolUse",
     "hooks": [
       {
         "type": "command",
         "command": "bash forge-plugin/hooks/your_hook.sh \"$TOOL_NAME\" \"$FILE_PATH\"",
         "matcher": "Write|Edit"
       }
     ]
   }
   ```
5. **Update `hooks/index.md`** with hook entry, event, and layer assignment
6. **Update `hooks/HOOKS_GUIDE.md`** with detailed documentation under the appropriate layer

---

## Coding Conventions

| File Type | Convention |
|-----------|-----------|
| **Markdown** (`.md`) | All documentation, skills, commands, context, agent definitions |
| **JSON** (`.json`) | Config files — 2-space indentation, consistent with existing files |
| **Bash** (`.sh`) | Hook scripts — `set -e`, quote variables, use `[[ ]]` for tests |
| **YAML frontmatter** | Required in all context files and skill/command definitions |

### General Rules

- No build tools, package managers, or compiled languages
- Use interface references (`contextProvider`, `memoryStore`, `skillInvoker`) — never hardcoded paths
- Follow existing naming patterns (kebab-case for directories, snake_case for scripts)
- Keep context files compact — link to official docs instead of duplicating content
- Memory paths use the canonical structure: `memory/{layer}/{name}/`

---

## Pull Request Process

1. **Branch from `develop`** — never push directly to `main`
2. **One concern per PR** — a single skill, agent, command, or focused improvement
3. **Include a clear description** of what changed and why
4. **Verify no hardcoded paths** — run the verification commands from the architectural roadmap
5. **Test with Claude Code** — ensure your skill/command/agent works end-to-end
6. **Update documentation** — ROADMAP.md, relevant index files, this guide if applicable

### PR Checklist

- [ ] New skills follow `SKILL_TEMPLATE.md` patterns
- [ ] New agents have both `.md` and `.config.json` files
- [ ] New context files have complete YAML frontmatter (tags + sections)
- [ ] New hooks registered in `hooks/hooks.json` and documented in `HOOKS_GUIDE.md`
- [ ] No hardcoded filesystem paths (use interface references)
- [ ] Memory directories use canonical paths (`memory/agents/`, `memory/skills/`, etc.)
- [ ] ROADMAP.md updated
- [ ] Tested with Claude Code

---

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Be respectful, inclusive, and constructive. The Forge is a collaborative workshop — every contribution makes the tools sharper.

---

## Questions?

Open an issue or start a discussion. The Forge's fires are always burning, and fellow smiths are always ready to help.

*"What we forge together, the gods themselves would envy."* — Hephaestus

---

*Last Updated: 2026-02-11*
