# Phase 2 Migration Guide

Version: 1.0.0
Last Updated: 2026-02-10

---

## Overview

This guide explains how to migrate Forge skills, commands, and agents from hardcoded filesystem paths to the interface-based pattern introduced in Phase 1. Migration updates the **instruction files** (SKILL.md, COMMAND.md, agent.md) — no runtime code changes are needed.

### What Changes
- `../../context/{domain}/` paths → `contextProvider.method()` calls
- `../../memory/skills/{skill}/{project}/` paths → `memoryStore.method()` calls
- Direct file reads/writes → Interface method calls with automatic features (timestamps, staleness, validation)

### What Does NOT Change
- Physical file structure (context/ and memory/ directories stay the same)
- Memory file format (markdown with `<!-- Last Updated -->` headers)
- Output conventions (/claudedocs naming)
- Compliance checklist structure

---

## Migrating Skills

### Step-by-Step Process

1. **Read the current SKILL.md** and identify all hardcoded paths
2. **Categorize each path** as context read, memory read, or memory write
3. **Replace context reads** with ContextProvider methods:
   - `../../context/{domain}/index.md` → `contextProvider.getDomainIndex("{domain}")`
   - `../../context/{domain}/{file}` → `contextProvider.getConditionalContext("{domain}", detection)` or `contextProvider.getAlwaysLoadFiles("{domain}")`
   - `../../context/loading_protocol.md` → `contextProvider.getLoadingProtocol()`
   - `../../context/cross_domain.md` → `contextProvider.getCrossDomainContext("{domain}", triggers)`
4. **Replace memory reads** with MemoryStore methods:
   - `../../memory/skills/{skill}/{project}/` → `memoryStore.getSkillMemory("{skill}", "{project}")`
   - `../../memory/projects/{project}/` → `memoryStore.getSharedProjectMemory("{project}")`
   - `../../memory/skills/{skill}/{project}/index.md` → included in `getSkillMemory()` result
5. **Replace memory writes** with MemoryStore methods:
   - `store insights in ../../memory/skills/{skill}/{project}/` → `memoryStore.update("{skill}", "{project}", ...)`
   - Manual timestamp management → handled automatically by MemoryStore
6. **Update File Structure section** to reference interfaces instead of relative paths
7. **Update Version History** with migration entry
8. **Verify** with grep: `grep -n '../../' SKILL.md` should return empty

### Before/After: commit-helper (Simple Skill — 2 paths)

**Before** (File Structure):
```
- **../../memory/skills/commit-helper/**: Project-specific memory storage
  - `{project-name}/`: Per-project commit conventions and patterns
```

**After**:
```
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("commit-helper", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
```

**Before** (Step 2 — memory read):
```
4. **Check project memory**: Look in `../../memory/skills/commit-helper/{project-name}/` for project-specific commit conventions
```

**After**:
```
4. **Check project memory**: Use `memoryStore.getSkillMemory("commit-helper", "{project-name}")` to load project-specific commit conventions. See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.
```

### Before/After: get-git-diff (Complex Skill — 6 paths)

**Before** (Step 2 — context + memory reads):
```
1. **READ** `../../context/git/index.md` to understand available git context files
2. **READ** `../../memory/skills/get-git-diff/index.md` to understand memory system
3. Check for project-specific memory in `../../memory/skills/get-git-diff/{project-name}/`
```

**After**:
```
1. **Load domain index**: Use `contextProvider.getDomainIndex("git")` to discover available git context files
2. **Load skill memory**: Use `memoryStore.getSkillMemory("get-git-diff", "{project-name}")` to load project-specific patterns
```

**Before** (Step 3 — context reads):
```
1. **READ** `../../context/git/git_diff_reference.md` for diff format understanding
2. **READ** `../../context/git/diff_patterns.md` for change pattern classification
```

**After**:
```
1. **Load context**: Use `contextProvider.getConditionalContext("git", detection)` to load relevant context files (git_diff_reference.md, diff_patterns.md)
```

---

## Migrating Commands

### Step-by-Step Process

1. **Read the current COMMAND.md** and identify all hardcoded paths
2. **Categorize each path** as context read, memory read, or memory write
3. **Replace context reads** following the same pattern as skills
4. **Replace memory reads** with appropriate MemoryStore methods:
   - `../../memory/commands/{project}/` → `memoryStore.getCommandMemory("{project}")`
   - `../../memory/skills/{skill}/{project}/` → `memoryStore.getSkillMemory("{skill}", "{project}")`
   - Shared project memory → `memoryStore.getSharedProjectMemory("{project}")`
5. **Replace memory writes** with `memoryStore.update(id, content)` or `memoryStore.append(id, content)`
6. **Add interface references** as markdown links
7. **Verify** with grep

### Before/After: /remember Command (11 paths)

**Before** (Step 2 — context + memory loading):
```
**Context Loading**:
1. Read `../../context/commands/index.md` for command guidance
2. Load `../../context/commands/memory_patterns.md` (if exists)

**Memory Loading**:
1. Determine project name
2. Check existing memory structure in `../../memory/`
3. Load relevant existing memory files:
   - Project memory: `../../memory/commands/{project}/`
   - Skill memory: `../../memory/skills/{skill}/{project}/`
```

**After**:
```
**Context Loading**:
1. Use `contextProvider.getDomainIndex("commands")` for command guidance
2. Use `contextProvider.getConditionalContext("commands", {"command": "remember"})` to load relevant patterns

**Memory Loading**:
1. Determine project name
2. Use `memoryStore.getCommandMemory("{project}")` for existing command memory
3. Use `memoryStore.getSharedProjectMemory("{project}")` for cross-skill project knowledge
```

---

## Migrating Agents

### Step-by-Step Process

1. **Read the agent's .md file** and identify hardcoded memory paths
2. **Replace memory paths** with MemoryStore interface calls
3. **Create agent.config.json** conforming to `agent_config.schema.json`:
   - Define context domains, memory categories, and skill integrations
   - Reference the schema: `"$schema": "../interfaces/schemas/agent_config.schema.json"`
4. **Update the agent.md** to reference the config file
5. **Verify** JSON validates against schema

### Before/After: technical-writer Agent

**Before** (memory access):
```
Access your memory at: `forge-plugin/agents/memory/technical-writer/`
```

**After**:
```
Access your memory via `memoryStore.getAgentMemory("technical-writer")`. See [MemoryStore Interface](../interfaces/memory_store.md) and your [agent configuration](technical-writer.config.json) for full context, memory, and skill configuration.
```

---

## Cross-Skill Memory Discovery

### Overview

Skills can use `memoryStore.getByProject(projectName)` to discover what other skills have learned about a project. This enables cross-pollination of insights without manual directory scanning.

### When to Use

- **Code review skills** checking if schema analysis or test generation already ran
- **Generation skills** checking if code review found patterns to follow
- **Documentation skills** gathering insights from all previous skill executions

### Integration Pattern

Add to the Memory Loading step of skills that benefit from cross-skill knowledge:

```markdown
**Memory Loading** (via MemoryStore):
1. Load skill-specific memory: `memoryStore.getSkillMemory("{skill}", project)`
2. **Cross-skill discovery**: `memoryStore.getByProject(project)` — check if other skills have relevant findings
   - Look for schema analysis results before generating code
   - Check code review findings before generating tests
   - Review test results before suggesting improvements
```

### Key Consumers

| Skill | Benefits From |
|-------|--------------|
| `python-code-review` | Schema analysis, test results |
| `angular-code-review` | Test results, component patterns |
| `dotnet-code-review` | Schema analysis, test results |
| `generate-python-unit-tests` | Code review findings |
| `generate-jest-unit-tests` | Code review findings, component patterns |
| `documentation-generator` | All skill findings for comprehensive docs |

---

## Adding YAML Frontmatter to Context Files

### Process

1. **Check the schema**: Read `interfaces/schemas/context_metadata.schema.json` for required fields
2. **Required fields**: `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`
3. **Prepend frontmatter** between `---` delimiters before existing content
4. **Do NOT modify body content** — only add the frontmatter block
5. **For index files**: Include `indexedFiles` array listing all files in the domain

### Template

```yaml
---
id: "{domain}/{filename_without_extension}"
domain: {domain}
title: "{Human-Readable Title}"
type: {always|framework|reference|pattern|index|detection}
estimatedTokens: {approximate_token_count}
loadingStrategy: {always|onDemand|lazy}
version: "1.0.0"
lastUpdated: "YYYY-MM-DD"
tags: [{relevant}, {searchable}, {tags}]
---
```

---

## Verification Checklist

After migrating any file:

- [ ] `grep -n '../../context/' {file}` returns empty
- [ ] `grep -n '../../memory/' {file}` returns empty
- [ ] All interface method calls reference correct interface names
- [ ] Interface documentation links are valid relative paths
- [ ] Version history updated with migration entry
- [ ] Body content (non-path sections) unchanged
- [ ] YAML frontmatter validates against schema (for context files)
- [ ] JSON config validates against schema (for agents)

---

## Interface Quick Reference

### ContextProvider Methods
| Method | Replaces |
|--------|----------|
| `getDomainIndex(domain)` | `Read ../../context/{domain}/index.md` |
| `getAlwaysLoadFiles(domain)` | `Read ../../context/{domain}/{always-file}.md` |
| `getConditionalContext(domain, detection)` | `Read ../../context/{domain}/{conditional-file}.md` |
| `getCrossDomainContext(domain, triggers)` | `Read ../../context/cross_domain.md` + manual resolution |
| `getLoadingProtocol()` | `Read ../../context/loading_protocol.md` |
| `getReference(domain, file)` | Metadata-only access (no previous equivalent) |
| `materialize(reference)` | Deferred full content load (no previous equivalent) |
| `search(query, domain?)` | Manual index scanning + cross-domain checks |

### MemoryStore Methods
| Method | Replaces |
|--------|----------|
| `getSkillMemory(skill, project)` | `Read ../../memory/skills/{skill}/{project}/` |
| `getSharedProjectMemory(project)` | `Read ../../memory/projects/{project}/` |
| `getCommandMemory(project)` | `Read ../../memory/commands/{project}/` |
| `getAgentMemory(agentName)` | `Read memory/agents/{agent}/` |
| `getByProject(projectName)` | Manual scanning of all memory directories for a project |
| `search(pattern, layer?, project?)` | Manual grep across memory files |
| `update(id, content)` | `Write ../../memory/.../{file}.md` + manual timestamp |
| `append(id, content)` | `Read + Write + manual pruning` |
| `create(entry)` | Manual directory creation + file write + timestamp |
| `validate(id)` | Manual quality checks (usually skipped) |

---

*See [ContextProvider Interface](context_provider.md) and [MemoryStore Interface](memory_store.md) for full method documentation.*
