---
description: "Forge project conventions for agentic workflows"
---

## Forge Project Structure

- **Skills**: `forge-plugin/skills/{name}/SKILL.md` + `examples.md`
- **Agents**: `forge-plugin/agents/{name}.md` + `{name}.config.json`
- **Context**: `forge-plugin/context/{domain}/` with YAML frontmatter
- **Hooks**: `forge-plugin/hooks/{name}.sh` (bash, `set -euo pipefail`)
- **Commands**: `forge-plugin/commands/{name}.md` with YAML frontmatter

## Key Conventions

- All documentation is Markdown
- All config is JSON (2-space or 4-space indent)
- All scripts are Bash with `set -e`
- Skills follow the 6-step mandatory workflow
- Context files have YAML frontmatter with tags, sections, estimated tokens
- Hooks must complete in < 5 seconds
- No hardcoded filesystem paths — use interface references

## Asset Counts (as of v0.3.0-alpha)

| Asset Type | Count | Location |
|-----------|-------|----------|
| Skills | 102 | `forge-plugin/skills/` |
| Agents | 19 | `forge-plugin/agents/` |
| Context Files | 81 | `forge-plugin/context/` |
| Hooks | 20 | `forge-plugin/hooks/` |
| Commands | 12 | `forge-plugin/commands/` |

## Quality Dimensions

| Asset | Key Quality Checks |
|-------|--------------------|
| **Skills** (`SKILL.md`) | Template adherence, required sections, examples presence, 6-step workflow |
| **Agent Configs** (`.config.json`) | Schema compliance, valid skill/MCP references, memory dir exists |
| **Context Files** (`.md`) | Frontmatter validity, token estimates, staleness (<90 days) |
| **Hooks** (`.sh`) | Idempotency, 5s budget, `set -euo pipefail`, error handling |
| **Commands** (`.md`) | Frontmatter structure, workflow steps, skill references |

## File Naming Conventions

| Asset | Pattern | Example |
|-------|---------|---------|
| Skill directories | kebab-case | `react-forms/` |
| Agent files | kebab-case + extension | `apollo.md`, `apollo.config.json` |
| Hook scripts | snake_case | `agent_config_validator.sh` |
| Context files | kebab-case in domain dirs | `context/python/django.md` |
| Commands | kebab-case | `azure-function.md` |

## Interface References

Always use interface references instead of hardcoded paths:

```
✅ contextProvider.getIndex("python")
❌ context/python/index.md

✅ memoryStore.read("projects/current")
❌ memory/projects/current.md

✅ skillInvoker.invoke("code-review", params)
❌ skills/code-review/SKILL.md
```
