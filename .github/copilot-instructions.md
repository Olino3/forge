# ⚒️ The Forge — Contributor's Codex

> *"Those who would forge alongside Hephaestus must know the ways of the workshop."*

## What Is The Forge?

The Forge is an **Agentic Software Factory** — a Claude Code plugin that extends AI-assisted development with specialized agents, skills, commands, context, memory, hooks, and MCP integrations. It is convention-based: no build tools, no package managers, no compiled code.

## Architecture at a Glance

```
forge-plugin/
├── interfaces/    # 4 core contracts (ContextProvider, MemoryStore, SkillInvoker, ExecutionContext)
│   ├── adapters/  # Default implementations (MarkdownFileContextProvider, MarkdownFileMemoryAdapter)
│   └── schemas/   # JSON validation schemas (agent_config, context_metadata, memory_entry)
├── agents/        # 11 agents (4 Olympian + 7 specialist) with .md + .config.json each
├── skills/        # 28 skills — each directory has SKILL.md + examples.md
├── commands/      # 12 slash commands — flat .md files + _docs/ directory for examples
├── context/       # 81 files across 9 domains — shared, static knowledge with YAML frontmatter
├── memory/        # 4-layer dynamic learning (projects/, skills/, commands/, agents/)
├── hooks/         # 20 hook handlers across 9 events, 4 thematic layers
│                  # hooks.json — registration manifest
│                  # lib/ — shared utilities (health_buffer.sh)
└── mcps/          # 8 MCP server integrations
```

## Core Interfaces

All components communicate through **convention-based interfaces** — never hardcoded paths.

| Interface | Purpose |
|-----------|---------|
| **ContextProvider** | Load context by domain, tags, or sections |
| **MemoryStore** | Read/write project-specific memory with lifecycle automation |
| **SkillInvoker** | Delegate to skills with structured I/O |
| **ExecutionContext** | Pass context between chained commands |

**Rule**: Always use interface references (e.g., `contextProvider.getIndex("python")`), never filesystem paths.

## Adding Skills

1. Create `forge-plugin/skills/{skill-name}/`
2. Add `SKILL.md` (use `SKILL_TEMPLATE.md` as base)
3. Add `examples.md` with usage examples
4. Optional: `scripts/` for bash utilities, `templates/` for output templates
5. Skills must follow the 6-step mandatory workflow: Initial Analysis → Load Memory → Load Context → Perform Analysis → Generate Output → Update Memory
6. All output goes to `/claudedocs/` following `OUTPUT_CONVENTIONS.md`

## Adding Agents

1. Create `forge-plugin/agents/{name}.md` (personality, expertise, workflow)
2. Create `forge-plugin/agents/{name}.config.json` following `agent_config.schema.json`
3. Create `forge-plugin/memory/agents/{name}/` for agent memory
4. Config must declare: `contextDomains`, `skills`, `memoryPath`, `model`, `tools`

## Adding Commands

1. Create `forge-plugin/commands/{command-name}.md` (flat file structure)
2. Add YAML frontmatter with: `name`, `description`, `category`, `complexity`, `skills`, `context`
3. Add workflow steps using `contextProvider` and `memoryStore`
4. Add usage examples in `forge-plugin/commands/_docs/{command-name}-examples.md`
5. Commands can delegate to skills via `skillInvoker` and chain via `ExecutionContext`

## Adding Context

1. Place files in the appropriate domain under `forge-plugin/context/{domain}/`
2. Include YAML frontmatter with `tags` and `sections` metadata
3. Update the domain's `index.md` and the top-level `context/index.md`
4. Context is **static** and shared — project-specific info goes in memory

## Adding Hooks

1. Create bash script in `forge-plugin/hooks/`
2. Source shared library: `source "${SCRIPT_DIR}/lib/health_buffer.sh"`
3. Register in `hooks/hooks.json` under the appropriate event and matcher
4. Update `hooks/index.md` with event, layer assignment, and purpose
5. Update `hooks/HOOKS_GUIDE.md` with detailed documentation under the appropriate layer
6. Hooks must be: fast (<5s), idempotent, non-destructive, graceful on failure
7. Use `set -euo pipefail` and safe grep patterns (`|| true` + `${var:-0}`)

### Hook Layers

| Layer | Purpose | Example Hooks |
|-------|---------|---------------|
| 🛡️ Shield | Security & initialization | `sandbox_boundary_guard`, `pii_redactor` |
| 📜 Chronicle | Memory & learning | `memory_quality_gate`, `memory_pruning_daemon` |
| 👷 Foreman | Workflow & quality | `skill_compliance_checker`, `agent_config_validator` |
| 📢 Town Crier | Telemetry & reporting | `system_health_emitter`, `forge_telemetry` |

## Coding Conventions

| Item | Convention |
|------|-----------|
| Docs | Markdown everywhere |
| Config | JSON (2-space or 4-space indent, match existing files) |
| Scripts | Bash with `set -e` |
| Context style | Compact — quick refs + links to official docs |
| Skill structure | `SKILL.md` + `examples.md` minimum |
| Command structure | `COMMAND.md` + `examples.md` minimum |
| Agent structure | `.md` + `.config.json` + memory directory |
| Output naming | Follow `OUTPUT_CONVENTIONS.md` |

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | The Forge Operating Manual — definitive guide for Claude Code |
| `CONTRIBUTING.md` | Full contribution guide |
| `ROADMAP.md` | Vision, capabilities, and changelog |
| `ARCHITECTURAL_ROADMAP.md` | Technical architecture and migration phases |
| `forge-plugin/hooks/hooks.json` | Hook registration manifest (20 handlers, 9 events) |
| `forge-plugin/hooks/HOOKS_GUIDE.md` | Hook architecture guide — 4 thematic layers |
| `forge-plugin/context/loading_protocol.md` | 5-step context loading protocol |
| `forge-plugin/context/cross_domain.md` | Cross-domain trigger matrix |
| `forge-plugin/memory/lifecycle.md` | Memory freshness, pruning, archival |
| `forge-plugin/memory/quality_guidance.md` | Memory quality validation |

## Pull Request Checklist

- [ ] New skills follow `SKILL_TEMPLATE.md` structure
- [ ] New agents have both `.md` and `.config.json`
- [ ] Context files include YAML frontmatter (tags + sections)
- [ ] Domain indexes updated if context files added/removed
- [ ] Memory directories created for new agents
- [ ] No hardcoded filesystem paths — use interface references
- [ ] `ROADMAP.md` updated if adding new capabilities

---

*Forged by Hephaestus. Tempered by experience. Worthy of Olympus.*
