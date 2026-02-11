# Phase 2 Verification Checklist

Version: 1.0.0
Last Updated: 2026-02-10

---

## Overview

This document provides the verification checklist for Phase 2 (Pilot Migration) of the Forge interface refactor. All items must pass before Phase 2 is considered complete.

---

## File Inventory

### Modified Files (9)

| # | File | Status |
|---|------|--------|
| 1 | `forge-plugin/skills/commit-helper/SKILL.md` | [ ] Verified |
| 2 | `forge-plugin/skills/get-git-diff/SKILL.md` | [ ] Verified |
| 3 | `forge-plugin/commands/remember/COMMAND.md` | [ ] Verified |
| 4 | `forge-plugin/agents/technical-writer.md` | [ ] Verified |
| 5 | `forge-plugin/skills/SKILL_TEMPLATE.md` | [ ] Verified |
| 6 | `forge-plugin/context/git/index.md` | [ ] Verified |
| 7 | `forge-plugin/context/git/diff_patterns.md` | [ ] Verified |
| 8 | `forge-plugin/context/git/git_diff_reference.md` | [ ] Verified |
| 9 | `forge-plugin/context/commands/index.md` | [ ] Verified |

### New Files (3)

| # | File | Status |
|---|------|--------|
| 10 | `forge-plugin/agents/technical-writer.config.json` | [ ] Verified |
| 11 | `forge-plugin/interfaces/migration_guide.md` | [ ] Verified |
| 12 | `forge-plugin/interfaces/phase2_verification.md` | [ ] Verified (this file) |

---

## Verification Checks

### 1. Zero Hardcoded Paths in Migrated Consumers

Run:
```bash
grep -n '../../context/' forge-plugin/skills/commit-helper/SKILL.md forge-plugin/skills/get-git-diff/SKILL.md forge-plugin/commands/remember/COMMAND.md forge-plugin/agents/technical-writer.md
```
**Expected**: No output (zero matches)

Run:
```bash
grep -n '../../memory/' forge-plugin/skills/commit-helper/SKILL.md forge-plugin/skills/get-git-diff/SKILL.md forge-plugin/commands/remember/COMMAND.md forge-plugin/agents/technical-writer.md
```
**Expected**: No output (zero matches)

### 2. YAML Frontmatter Validation

For each of the 4 context files with new frontmatter:
- [ ] `forge-plugin/context/git/index.md` has valid YAML between `---` delimiters
- [ ] `forge-plugin/context/git/diff_patterns.md` has valid YAML between `---` delimiters
- [ ] `forge-plugin/context/git/git_diff_reference.md` has valid YAML between `---` delimiters
- [ ] `forge-plugin/context/commands/index.md` has valid YAML between `---` delimiters

Required fields per `context_metadata.schema.json`:
- [ ] `id` (format: `{domain}/{filename}`)
- [ ] `domain` (valid enum value)
- [ ] `title` (non-empty string)
- [ ] `type` (valid enum: always, framework, reference, pattern, index, detection)
- [ ] `estimatedTokens` (positive integer)
- [ ] `loadingStrategy` (valid enum: always, onDemand, lazy)

### 3. Agent Config Validation

File: `forge-plugin/agents/technical-writer.config.json`
- [ ] Valid JSON syntax
- [ ] Has required fields: `name`, `version`, `context`, `memory`, `skills`
- [ ] `context` has required fields: `primaryDomains`, `secondaryDomains`, `alwaysLoadFiles`
- [ ] `memory` has required fields: `storagePath`, `categories`
- [ ] `skills` is an array with required `name` field per entry
- [ ] `$schema` references `../interfaces/schemas/agent_config.schema.json`

### 4. SKILL_TEMPLATE.md Clean

Run:
```bash
grep -n '../../' forge-plugin/skills/SKILL_TEMPLATE.md
```
**Expected**: Only valid interface references (e.g., `../../interfaces/`), zero `../../context/` or `../../memory/` paths

### 5. Body Content Preserved

For each context file with added frontmatter, verify the body content (everything after the closing `---`) is identical to the pre-migration version:
- [ ] `forge-plugin/context/git/index.md` body unchanged
- [ ] `forge-plugin/context/git/diff_patterns.md` body unchanged
- [ ] `forge-plugin/context/git/git_diff_reference.md` body unchanged
- [ ] `forge-plugin/context/commands/index.md` body unchanged

### 6. Interface References Valid

All migrated files should reference interface documentation correctly:
- [ ] Links to `../../interfaces/context_provider.md` are valid
- [ ] Links to `../../interfaces/memory_store.md` are valid
- [ ] Links to `../../interfaces/schemas/context_metadata.schema.json` are valid (in SKILL_TEMPLATE.md)
- [ ] Links to `../../interfaces/schemas/memory_entry.schema.json` are valid (in SKILL_TEMPLATE.md)

### 7. Zero Collateral Changes

No files outside the 12 deliverables should be modified:
```bash
git diff --name-only
```
**Expected**: Only the 9 modified files listed above appear (plus any new untracked files)

### 8. Version History Updated

- [ ] `commit-helper/SKILL.md` has v1.1.0 entry for interface migration
- [ ] `get-git-diff/SKILL.md` has v1.2.0 entry for interface migration

---

## Summary

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Hardcoded paths | Zero `../../context/` or `../../memory/` in 4 migrated consumers | [ ] |
| YAML frontmatter | 4 context files have valid frontmatter per schema | [ ] |
| Agent config | Valid JSON conforming to agent_config.schema.json | [ ] |
| Template clean | SKILL_TEMPLATE.md has zero `../../context/` or `../../memory/` paths | [ ] |
| Content preserved | Body content of 4 context files unchanged | [ ] |
| Interface links | All interface references resolve correctly | [ ] |
| No collateral | Only 12 specified files created/modified | [ ] |
| Version history | Migration entries added to 2 skill files | [ ] |

---

*Phase 2 is complete when all checks pass.*
