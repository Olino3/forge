# Phase 3 Verification Checklist

Version: 1.0.0
Last Updated: 2026-02-10

---

## Overview

This document provides the verification checklist for Phase 3 (Full Migration) of the Forge interface refactor. All items must pass before Phase 3 is considered complete.

---

## File Inventory

### Modified Files (Consumer Migrations)

| # | File | Type | Status |
|---|------|------|--------|
| 1 | `forge-plugin/skills/python-code-review/SKILL.md` | Skill | [ ] Verified |
| 2 | `forge-plugin/skills/dotnet-code-review/SKILL.md` | Skill | [ ] Verified |
| 3 | `forge-plugin/commands/analyze/COMMAND.md` | Command | [ ] Verified |
| 4 | `forge-plugin/commands/implement/COMMAND.md` | Command | [ ] Verified |
| 5 | `forge-plugin/agents/python-engineer.md` | Agent | [ ] Verified |
| 6 | `forge-plugin/agents/devops-engineer.md` | Agent | [ ] Verified |

### Modified Files (Protocol/Index Updates)

| # | File | Type | Status |
|---|------|------|--------|
| 7 | `forge-plugin/context/loading_protocol.md` | Protocol | [ ] Verified |
| 8 | `forge-plugin/context/cross_domain.md` | Protocol | [ ] Verified |
| 9 | `forge-plugin/context/index.md` | Index | [ ] Verified |

### New Files

| # | File | Type | Status |
|---|------|------|--------|
| 10 | `forge-plugin/agents/python-engineer.config.json` | Agent config | [ ] Verified |
| 11 | `forge-plugin/agents/devops-engineer.config.json` | Agent config | [ ] Verified |
| 12 | `forge-plugin/interfaces/phase3_verification.md` | Verification | [ ] Verified (this file) |

---

## Verification Checks

### 1. Zero Hardcoded Paths in Migrated Consumers

Run:
```bash
grep -rn '../../context/' forge-plugin/skills/python-code-review/SKILL.md forge-plugin/skills/dotnet-code-review/SKILL.md forge-plugin/commands/analyze/COMMAND.md forge-plugin/commands/implement/COMMAND.md forge-plugin/agents/python-engineer.md forge-plugin/agents/devops-engineer.md
```
**Expected**: No output (zero matches)

Run:
```bash
grep -rn '../../memory/' forge-plugin/skills/python-code-review/SKILL.md forge-plugin/skills/dotnet-code-review/SKILL.md forge-plugin/commands/analyze/COMMAND.md forge-plugin/commands/implement/COMMAND.md forge-plugin/agents/python-engineer.md forge-plugin/agents/devops-engineer.md
```
**Expected**: No output (zero matches)

Run:
```bash
grep -rn '\.\./skills/' forge-plugin/agents/python-engineer.md forge-plugin/agents/devops-engineer.md
```
**Expected**: No output (zero matches -- skill references moved to config.json and `skill:` invocations)

### 2. YAML Frontmatter Validation

For each of the 3 files with new frontmatter:
- [ ] `forge-plugin/context/loading_protocol.md` has valid YAML between `---` delimiters
- [ ] `forge-plugin/context/cross_domain.md` has valid YAML between `---` delimiters
- [ ] `forge-plugin/context/index.md` has valid YAML between `---` delimiters

Required fields per `context_metadata.schema.json`:
- [ ] `id` (format: `{domain}/{filename}`)
- [ ] `domain` (valid enum value)
- [ ] `title` (non-empty string)
- [ ] `type` (valid enum: always, framework, reference, pattern, index, detection)
- [ ] `estimatedTokens` (positive integer)
- [ ] `loadingStrategy` (valid enum: always, onDemand, lazy)

Specific frontmatter values:
- [ ] `loading_protocol.md`: id=`engineering/loading_protocol`, type=`reference`, loadingStrategy=`always`
- [ ] `cross_domain.md`: id=`engineering/cross_domain`, type=`reference`, loadingStrategy=`onDemand`
- [ ] `index.md`: id=`engineering/index`, type=`index`, loadingStrategy=`always`, has `indexedFiles` with 9 domain indexes

### 3. Agent Config Validation

For each new agent config file:

**python-engineer.config.json**:
- [ ] Valid JSON syntax
- [ ] Has required fields: `name`, `version`, `context`, `memory`, `skills`
- [ ] `context.primaryDomains` = `["python"]`
- [ ] `context.secondaryDomains` = `["security", "engineering"]`
- [ ] `skills` array has 4 entries: python-code-review, generate-python-unit-tests, python-dependency-management, jupyter-notebook-skills
- [ ] `$schema` references `../interfaces/schemas/agent_config.schema.json`

**devops-engineer.config.json**:
- [ ] Valid JSON syntax
- [ ] Has required fields: `name`, `version`, `context`, `memory`, `skills`
- [ ] `context.primaryDomains` = `["azure"]`
- [ ] `context.secondaryDomains` = `["engineering"]`
- [ ] `skills` array has 5 entries: generate-azure-pipelines, generate-azure-bicep, generate-azure-functions, generate-tilt-dev-environment, generate-mock-service
- [ ] `$schema` references `../interfaces/schemas/agent_config.schema.json`

### 4. Loading Protocol Enhancements

- [ ] `loading_protocol.md` has "Loading Modes" section after Step 5
- [ ] Loading Modes section describes Traditional Mode (default) and Reference-First Mode (opt-in)
- [ ] Reference-First Mode references `contextProvider.getCatalog()`, `materialize()`, `materializeSections()`
- [ ] Links to ContextProvider interface

### 5. Cross-Domain Enhancements

- [ ] `cross_domain.md` trigger matrix has "Relevance Score" column (0.0-1.0 values)
- [ ] `cross_domain.md` trigger matrix has "Token Impact" column
- [ ] Scoring explanation section present (0.8-1.0=always, 0.5-0.7=budget-dependent, 0.1-0.4=reference only)
- [ ] Links to ContextProvider interface

### 6. Version History Updated

- [ ] `python-code-review/SKILL.md` has v2.2.0 entry for interface migration
- [ ] `dotnet-code-review/SKILL.md` has v1.1.0 entry for interface migration

### 7. Interface References Valid

All migrated files should reference interface documentation correctly:
- [ ] Links to `../../interfaces/context_provider.md` are valid (skills, commands)
- [ ] Links to `../../interfaces/memory_store.md` are valid (skills, commands)
- [ ] Links to `../interfaces/context_provider.md` are valid (agents)
- [ ] Links to `../interfaces/memory_store.md` are valid (agents)
- [ ] Agent config links (`python-engineer.config.json`, `devops-engineer.config.json`) are valid in agent .md files

### 8. Body Content Preserved

For context files with added frontmatter, verify body content (everything after the closing `---`) matches pre-migration intent:
- [ ] `loading_protocol.md` original 5-step content preserved, new "Loading Modes" section added
- [ ] `cross_domain.md` trigger matrix rows preserved, new columns added
- [ ] `index.md` full directory listing and guidance preserved

---

## Summary

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Hardcoded paths | Zero `../../context/`, `../../memory/`, `../skills/` in 6 migrated consumers | [ ] |
| YAML frontmatter | 3 files have valid frontmatter per schema | [ ] |
| Agent configs | 2 valid JSON files conforming to agent_config.schema.json | [ ] |
| Loading protocol | Loading Modes section added with Traditional and Reference-First modes | [ ] |
| Cross-domain | Relevance Score and Token Impact columns added with scoring guide | [ ] |
| Version history | Migration entries added to 2 skill files | [ ] |
| Interface links | All interface references resolve correctly | [ ] |
| Content preserved | Body content of 3 context files preserved or correctly extended | [ ] |

---

*Phase 3 is complete when all checks pass.*
