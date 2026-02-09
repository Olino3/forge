# Copilot Instructions for The Forge

## Project Overview

The Forge is a curated, versioned registry of Claude Code plugins. It serves as a marketplace where plugins can be discovered and installed directly from Claude Code. The project is shell-based and does not use a build system, package manager, or compiled language.

## Repository Structure

```
forge/
├── .claude-plugin/          # Marketplace registry
│   └── marketplace.json     # Catalog of available plugins
├── .github/                 # GitHub configuration
│   └── copilot-instructions.md
├── forge-plugin/            # Main plugin package
│   ├── .claude-plugin/      # Plugin manifest (plugin.json)
│   ├── agents/              # Specialized sub-agents
│   │   └── devops-engineer.md  # DevOps automation expert
│   ├── context/             # Shared contextual knowledge (read-only reference)
│   │   ├── angular/         # Angular/TypeScript patterns
│   │   ├── azure/           # Azure Functions, Pipelines, Bicep patterns
│   │   ├── dotnet/          # .NET/C# standards
│   │   ├── git/             # Git diff references
│   │   ├── python/          # Python best practices
│   │   ├── schema/          # Schema analysis patterns
│   │   └── security/        # Security guidelines
│   ├── memory/              # Project-specific learning (dynamic)
│   │   ├── agents/          # Per-agent memory
│   │   └── skills/          # Per-skill, per-project memory
│   └── skills/              # Plugin skills (tools)
├── README.md
└── ROADMAP.md
```

## Key Concepts

- **Marketplace**: Defined by `.claude-plugin/marketplace.json` at the repo root. Lists all available plugins.
- **Plugin**: Defined by `forge-plugin/.claude-plugin/plugin.json`. Contains metadata (name, version, author).
- **Agents**: Located in `forge-plugin/agents/`. Specialized sub-agents with YAML frontmatter configuration for focused tasks. Each agent has access to specific skills, context, memory, hooks, and MCP servers.
- **Skills**: Located in `forge-plugin/skills/`. Each skill has its own directory with `SKILL.md`, `examples.md`, optional `scripts/` and `templates/` subdirectories.
- **Context files**: Located in `forge-plugin/context/`. Shared, read-only reference material organized by domain (angular, azure, dotnet, git, python, schema, security). Each domain has an `index.md` for navigation.
- **Memory files**: Located in `forge-plugin/memory/`. Dynamic, project-specific learning stored per skill and per agent in separate subdirectories.

## Coding Conventions

- **Markdown**: All documentation, skill definitions, context files, and templates use Markdown.
- **JSON**: Configuration files (`marketplace.json`, `plugin.json`) use JSON with 2-space or 4-space indentation consistent with the existing file.
- **Shell scripts**: Scripts in `skills/*/scripts/` are written in Bash.
- **Context file style**: Use the compact approach — keep quick reference tables and detection patterns, link to official docs instead of duplicating content. See `forge-plugin/context/index.md` for detailed guidelines.
- **Skill structure**: Each skill directory must contain at minimum a `SKILL.md` (documentation) and `examples.md` (usage examples).

## Adding New Skills

When adding a new skill:
1. Create a directory under `forge-plugin/skills/<skill-name>/`
2. Include `SKILL.md` with skill documentation
3. Include `examples.md` with usage examples
4. Add optional `scripts/` for shell utilities and `templates/` for output templates
5. Update `ROADMAP.md` to reflect the new skill's status

## Adding New Agents

When adding a new agent:
1. Create a markdown file under `forge-plugin/agents/<agent-name>.md`
2. Include YAML frontmatter with:
   - `name`: Agent identifier
   - `description`: What the agent does (used by Claude router)
   - `tools`: Array of allowed tools (Read, Write, Bash, Grep, Glob, etc.)
   - `model`: Model to use (haiku, sonnet, opus)
   - `permissionMode`: Permission handling (auto, restricted, etc.)
   - `hooks`: Array of lifecycle hooks
   - `mcpServers`: Array of MCP server integrations
   - `memory`: Memory configuration with storage path and structure
3. Include clear mission, workflow, and task patterns in the markdown body
4. Create memory directory structure at `forge-plugin/memory/agents/<agent-name>/`
5. Update `ROADMAP.md` to reflect the new agent's status

## Adding New Context Files

When adding context files:
- Place them in the appropriate domain directory under `forge-plugin/context/`
- Update the domain's `index.md` and the top-level `forge-plugin/context/index.md`
- Only add knowledge that applies to multiple projects (project-specific info goes in `memory/`)
- Use the compact approach: brief summaries with links to official docs

## Contributing

1. Fork the repository
2. Add or modify plugins, skills, or context files
3. Open a pull request with a clear description of the changes
