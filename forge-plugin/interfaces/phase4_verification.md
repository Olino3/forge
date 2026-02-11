# Phase 4 Verification Checklist

Version: 1.0.0
Last Updated: 2026-02-10

---

## Overview

This document provides the verification checklist for Phase 4 (Complete Migration) of the Forge interface refactor. Phase 4 completes the migration of all remaining skills (22), commands (9), and agents (8), and introduces the ExecutionContext interface and cross-skill memory discovery.

---

## File Inventory

### Modified Files — Skills (22 migrated)

| # | File | Status |
|---|------|--------|
| 1 | `forge-plugin/skills/documentation-generator/SKILL.md` | [ ] Verified |
| 2 | `forge-plugin/skills/email-writer/SKILL.md` | [ ] Verified |
| 3 | `forge-plugin/skills/excel-skills/SKILL.md` | [ ] Verified |
| 4 | `forge-plugin/skills/slack-message-composer/SKILL.md` | [ ] Verified |
| 5 | `forge-plugin/skills/jupyter-notebook-skills/SKILL.md` | [ ] Verified |
| 6 | `forge-plugin/skills/generate-more-skills-with-claude/SKILL.md` | [ ] Verified |
| 7 | `forge-plugin/skills/database-schema-analysis/SKILL.md` | [ ] Verified |
| 8 | `forge-plugin/skills/file-schema-analysis/SKILL.md` | [ ] Verified |
| 9 | `forge-plugin/skills/generate-mock-service/SKILL.md` | [ ] Verified |
| 10 | `forge-plugin/skills/generate-tilt-dev-environment/SKILL.md` | [ ] Verified |
| 11 | `forge-plugin/skills/python-dependency-management/SKILL.md` | [ ] Verified |
| 12 | `forge-plugin/skills/angular-code-review/SKILL.md` | [ ] Verified |
| 13 | `forge-plugin/skills/generate-azure-bicep/SKILL.md` | [ ] Verified |
| 14 | `forge-plugin/skills/generate-azure-functions/SKILL.md` | [ ] Verified |
| 15 | `forge-plugin/skills/generate-azure-pipelines/SKILL.md` | [ ] Verified |
| 16 | `forge-plugin/skills/generate-jest-unit-tests/SKILL.md` | [ ] Verified |
| 17 | `forge-plugin/skills/generate-python-unit-tests/SKILL.md` | [ ] Verified |
| 18 | `forge-plugin/skills/test-cli-tools/SKILL.md` | [ ] Verified |
| 19 | `forge-plugin/skills/python-code-review/SKILL.md` | [ ] Verified (cross-skill discovery added) |
| 20 | `forge-plugin/skills/angular-code-review/SKILL.md` | [ ] Verified (cross-skill discovery added) |
| 21 | `forge-plugin/skills/documentation-generator/SKILL.md` | [ ] Verified (cross-skill discovery added) |

### Modified Files — Commands (9 migrated)

| # | File | Status |
|---|------|--------|
| 22 | `forge-plugin/commands/document/COMMAND.md` | [ ] Verified |
| 23 | `forge-plugin/commands/mock/COMMAND.md` | [ ] Verified |
| 24 | `forge-plugin/commands/brainstorm/COMMAND.md` | [ ] Verified |
| 25 | `forge-plugin/commands/test/COMMAND.md` | [ ] Verified |
| 26 | `forge-plugin/commands/build/COMMAND.md` | [ ] Verified |
| 27 | `forge-plugin/commands/etl-pipeline/COMMAND.md` | [ ] Verified |
| 28 | `forge-plugin/commands/azure-pipeline/COMMAND.md` | [ ] Verified |
| 29 | `forge-plugin/commands/azure-function/COMMAND.md` | [ ] Verified |
| 30 | `forge-plugin/commands/improve/COMMAND.md` | [ ] Verified |

### Modified Files — Agents (8 migrated)

| # | File | Status |
|---|------|--------|
| 31 | `forge-plugin/agents/ares.md` | [ ] Verified |
| 32 | `forge-plugin/agents/data-scientist.md` | [ ] Verified |
| 33 | `forge-plugin/agents/developer-environment-engineer.md` | [ ] Verified |
| 34 | `forge-plugin/agents/frontend-engineer.md` | [ ] Verified |
| 35 | `forge-plugin/agents/full-stack-engineer.md` | [ ] Verified |
| 36 | `forge-plugin/agents/hephaestus.md` | [ ] Verified |
| 37 | `forge-plugin/agents/poseidon.md` | [ ] Verified |
| 38 | `forge-plugin/agents/prometheus.md` | [ ] Verified |

### New Files — Agent Configs (8 created)

| # | File | Status |
|---|------|--------|
| 39 | `forge-plugin/agents/ares.config.json` | [ ] Verified |
| 40 | `forge-plugin/agents/data-scientist.config.json` | [ ] Verified |
| 41 | `forge-plugin/agents/developer-environment-engineer.config.json` | [ ] Verified |
| 42 | `forge-plugin/agents/frontend-engineer.config.json` | [ ] Verified |
| 43 | `forge-plugin/agents/full-stack-engineer.config.json` | [ ] Verified |
| 44 | `forge-plugin/agents/hephaestus.config.json` | [ ] Verified |
| 45 | `forge-plugin/agents/poseidon.config.json` | [ ] Verified |
| 46 | `forge-plugin/agents/prometheus.config.json` | [ ] Verified |

### New Files — Interfaces & Documentation

| # | File | Status |
|---|------|--------|
| 47 | `forge-plugin/interfaces/execution_context.md` | [ ] Verified |
| 48 | `forge-plugin/interfaces/phase4_verification.md` | [ ] Verified (this file) |

### Modified Files — Migration Guide

| # | File | Status |
|---|------|--------|
| 49 | `forge-plugin/interfaces/migration_guide.md` | [ ] Verified (cross-skill discovery + getByProject docs) |

---

## Verification Checks

### 1. Zero Hardcoded Paths — Skills

Run:
```bash
cd forge-plugin/skills && grep -rn '../../context/\|../../memory/' */SKILL.md | grep -v '../../interfaces/'
```
**Expected**: No output (zero matches across all 22 skills)

### 2. Zero Hardcoded Paths — Commands

Run:
```bash
cd forge-plugin/commands && grep -rn '../../context/\|../../memory/' */COMMAND.md | grep -v '../../interfaces/'
```
**Expected**: No output (zero matches across all 12 commands)

### 3. Zero Hardcoded Paths — Agents

Run:
```bash
cd forge-plugin/agents && grep -rn '../../\|../context/\|../memory/' *.md | grep -v '../../interfaces/'
```
**Expected**: No output (zero matches across all 11 agents)

### 4. All Agent Config Files Valid

For each of the 8 new agent config files, verify:
- [ ] Valid JSON syntax: `python3 -c "import json; json.load(open('file.json'))"`
- [ ] Has required fields: `name`, `version`, `context`, `memory`, `skills`
- [ ] `$schema` references `../interfaces/schemas/agent_config.schema.json`
- [ ] `context` has `primaryDomains`, `secondaryDomains`, `alwaysLoadFiles`
- [ ] `memory` has `storagePath`, `categories`
- [ ] `name` matches filename (kebab-case)

Run batch validation:
```bash
cd forge-plugin/agents && for f in ares data-scientist developer-environment-engineer frontend-engineer full-stack-engineer hephaestus poseidon prometheus; do python3 -c "import json; d=json.load(open('${f}.config.json')); assert d['name']=='${f}', f'name mismatch'; assert '\$schema' in d, 'no schema'; print(f'✅ ${f}.config.json')" 2>&1; done
```

### 5. Agent .md Files Reference Config

For each migrated agent, verify the .md file references the config file:
```bash
cd forge-plugin/agents && for f in ares data-scientist developer-environment-engineer frontend-engineer full-stack-engineer hephaestus poseidon prometheus; do grep -l "${f}.config.json" "${f}.md" || echo "❌ ${f}.md missing config reference"; done
```
**Expected**: All 8 files listed (no ❌ output)

### 6. MemoryStore Interface References

All agents reference memoryStore.getAgentMemory():
```bash
cd forge-plugin/agents && for f in ares data-scientist developer-environment-engineer frontend-engineer full-stack-engineer hephaestus poseidon prometheus; do grep -l 'memoryStore.getAgentMemory' "${f}.md" || echo "❌ ${f}.md missing memoryStore ref"; done
```
**Expected**: All 8 files listed

### 7. ExecutionContext Interface Complete

- [ ] `forge-plugin/interfaces/execution_context.md` exists
- [ ] Has Types section with `ExecutionState` and `CommandExecution`
- [ ] Has Interface Methods section with: `create`, `getOrCreate`, `recordContextLoad`, `getCachedContext`, `recordMemoryLoad`, `getCachedMemory`, `setSharedData`, `getSharedData`, `startCommand`, `completeCommand`, `getPreviousCommand`
- [ ] Has Integration Pattern section with COMMAND.md example
- [ ] Has Common Command Chains table
- [ ] References ContextProvider, MemoryStore, and SkillInvoker interfaces

### 8. Cross-Skill Memory Discovery

- [ ] `migration_guide.md` has "Cross-Skill Memory Discovery" section
- [ ] `migration_guide.md` method table includes `getByProject()` and `search()`
- [ ] `python-code-review/SKILL.md` references `memoryStore.getByProject()`
- [ ] `angular-code-review/SKILL.md` references `memoryStore.getByProject()`
- [ ] `documentation-generator/SKILL.md` references `memoryStore.getByProject()`

### 9. Interface References Consistent

All migrated skills should link to interfaces using `../../interfaces/`:
```bash
cd forge-plugin/skills && grep -L '../../interfaces/' */SKILL.md
```
**Expected**: Only skills that legitimately don't need interface refs (commit-helper, get-git-diff, dotnet-code-review — already migrated in Phase 3)

All migrated agents should link to `../interfaces/`:
```bash
cd forge-plugin/agents && grep -L '../interfaces/' ares.md data-scientist.md developer-environment-engineer.md frontend-engineer.md full-stack-engineer.md hephaestus.md poseidon.md prometheus.md
```
**Expected**: No output (all 8 agents reference interfaces)

### 10. YAML Frontmatter Present on Skills

Skills migrated in Phase 4 should have YAML frontmatter:
```bash
cd forge-plugin/skills && for d in documentation-generator email-writer excel-skills slack-message-composer jupyter-notebook-skills generate-more-skills-with-claude database-schema-analysis file-schema-analysis generate-mock-service generate-tilt-dev-environment python-dependency-management angular-code-review generate-azure-bicep generate-azure-functions generate-azure-pipelines generate-jest-unit-tests generate-python-unit-tests test-cli-tools; do head -1 "$d/SKILL.md" | grep -q '^---' && echo "✅ $d" || echo "❌ $d missing frontmatter"; done
```

---

## Quantitative Summary

| Metric | Target | Actual | Pass |
|--------|--------|--------|------|
| Skills migrated | 22/22 | [ ] | [ ] |
| Commands migrated | 12/12 (3 Phase 3 + 9 Phase 4) | [ ] | [ ] |
| Agents migrated | 11/11 (3 Phase 3 + 8 Phase 4) | [ ] | [ ] |
| Agent config.json files | 11/11 (3 Phase 3 + 8 Phase 4) | [ ] | [ ] |
| Hardcoded `../../context/` paths remaining | 0 | [ ] | [ ] |
| Hardcoded `../../memory/` paths remaining | 0 | [ ] | [ ] |
| Hardcoded `../context/` paths remaining (agents) | 0 | [ ] | [ ] |
| New interfaces designed | 1 (ExecutionContext) | [ ] | [ ] |
| Cross-skill discovery consumers | ≥3 skills | [ ] | [ ] |

---

## Summary

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Skills paths | Zero hardcoded context/memory paths in 22 skills | [ ] |
| Commands paths | Zero hardcoded context/memory paths in 12 commands | [ ] |
| Agents paths | Zero hardcoded context/memory paths in 11 agents | [ ] |
| Agent configs | 8 new valid JSON configs conforming to schema | [ ] |
| Agent .md refs | All 8 agents reference their config file | [ ] |
| MemoryStore refs | All 8 agents use memoryStore.getAgentMemory() | [ ] |
| ExecutionContext | Interface designed with types, methods, and patterns | [ ] |
| Cross-skill discovery | getByProject() documented and adopted by 3+ skills | [ ] |
| Interface links | All migrated files reference interface docs correctly | [ ] |
| Frontmatter | All Phase 4 skills have YAML frontmatter | [ ] |

---

*Phase 4 is complete when all checks pass. After Phase 4, the entire Forge plugin should have zero hardcoded filesystem paths in any skill, command, or agent.*
