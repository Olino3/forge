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
├── agents/        # 19 agents (12 Olympian + 7 specialist) with .md + .config.json each
├── skills/        # 102 skills — each directory has SKILL.md + examples.md
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

## Forge Marketplace & External Skills

The Forge includes **212 external skills** from 5 enterprise/community sources, loaded via the **Forge Marketplace** (`.claude-plugin/marketplace.json`). There are **38 plugins** total.

### Integration Patterns

| Pattern | Example | Description |
|---------|---------|-------------|
| **Multi-Plugin Wrapper** | Microsoft | 1 submodule → 7 wrapper plugins with symlinks, per-language separation |
| **Single Plugin Wrapper** | Vercel, Google Labs | 1 submodule → 1 wrapper plugin, single symlink |
| **Native Plugin** | Trail of Bits, Sentry | Direct source path references into submodule, no wrappers |

### Adding External Plugins

1. Fork the upstream repository under `Olino3/`
2. Add as git submodule: `git submodule add <fork-url> <path>`
3. Create Plugin Wrapper directory with `.claude-plugin/plugin.json` and `skills/` symlinks (or use Native Plugin pattern)
4. Register in `.claude-plugin/marketplace.json`
5. Update `scripts/fix-symlinks.sh` and `scripts/verify-symlinks.sh`
6. Run `./scripts/validate-plugins.sh` to verify

See `CONTRIBUTING.md` for detailed instructions and the Microsoft/Vercel/Trail of Bits patterns as templates.

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

## Agentic Workflows (gh-aw)

The Forge runs **12 agentic workflows** via [GitHub Agentic Workflows (gh-aw)](https://github.github.com/gh-aw/) — autonomous AI agents as GitHub Actions that continuously monitor, validate, and improve the codebase.

### What Contributors Should Know

- **On PRs**: Up to 3 workflows analyze your changes (component improvement, duplication detection, milestone tracking)
- **On schedules**: Workflows run for health monitoring, documentation sync, dependency updates, and planning
- **On events**: Workflows respond to milestones, releases, and labeled issues
- **All outputs** carry the `forge-automation` label — issues are findings, draft PRs are proposed changes
- **Nothing merges without human approval**

See [AGENTIC_FORGE.md](AGENTIC_FORGE.md) for the full contributor guide with lifecycle diagrams and developer scenarios.

### Quick Reference

```bash
gh extension install github/gh-aw   # Install CLI
gh aw compile                        # Compile .md → .lock.yml
gh aw status                         # Check workflow status
gh aw fix --write                    # Fix deprecated fields
```

### Workflow Structure

```
.github/workflows/
├── shared/                          # Shared imports (5 files)
│   ├── forge-base.md                # Engine (copilot) + base permissions
│   ├── forge-pr-creator.md          # PR-creating workflow defaults
│   ├── forge-issue-creator.md       # Issue-creating workflow defaults
│   ├── forge-conventions.md         # Forge project conventions
│   └── forge-quality-issue-template.md  # Issue body contract
├── forge-*.md                       # 19 workflow source files
└── forge-*.lock.yml                 # Compiled (DO NOT EDIT)
```

### Critical Rules for Writing Workflows

1. **Strict mode is repo-level** — set by `gh aw init`, not a frontmatter field
2. **Only read permissions allowed** — `contents: read`, `issues: read`, `pull-requests: read`
3. **Never add write permissions** — safe-outputs automatically handle writes
4. **Property names matter:**
   - `expires` (NOT `expire`) — integer days
   - `close-older-issues` (NOT `close-older`) — boolean, issue-only
   - `max` — valid on `create-issue` only, NOT on `create-pull-request`
5. **`default` toolset requires** `issues: read` + `pull-requests: read`
6. **Never edit `.lock.yml` files** — always edit `.md` source and recompile
7. **Import shared files** via `imports:` in frontmatter

### Required Repository Secrets

| Secret | Purpose |
|--------|---------|
| `GH_AW_GITHUB_TOKEN` | PAT for gh-aw agent operations |
| `COPILOT_GITHUB_TOKEN` | PAT for Copilot execution |
| `GH_AW_AGENT_TOKEN` | PAT for agent delegation |

All are repository secrets (Settings → Secrets → Actions). Account must have active Copilot license.

See `CLAUDE.md` Section XVI for the full authoring reference.

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | The Forge Operating Manual — definitive guide for Claude Code |
| `CONTRIBUTING.md` | Full contribution guide |
| `COOKBOOK.md` | Strategies, workflows, and persona-based plugin selection |
| `ROADMAP.md` | Vision, capabilities, and changelog |
| `AGENTIC_FORGE.md` | Agentic workflows contributor guide |
| `AGENTIC_WORKFLOWS_ROADMAP.md` | Agentic workflows technical roadmap |
| `SECURITY.md` | Private vulnerability reporting policy |
| `ARCHITECTURAL_ROADMAP.md` | Technical architecture and migration phases |
| `.claude-plugin/marketplace.json` | Forge Marketplace — 38 plugins for external skills |
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
- [ ] `marketplace.json` updated if plugins added/removed
- [ ] Symlinks verified with `./scripts/verify-symlinks.sh` if external plugins changed
- [ ] Agentic workflows compile cleanly: `gh aw compile` shows 0 errors
- [ ] No write permissions in agentic workflow frontmatter (safe-outputs handles writes)
- [ ] `.lock.yml` files regenerated after any workflow `.md` changes

---

*Forged by Hephaestus. Tempered by experience. Worthy of Olympus.*
