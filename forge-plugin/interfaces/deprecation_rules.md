# Deprecation Rules

Version: 1.0.0
Status: Phase 5 - Optimization
Last Updated: 2026-02-11

---

## Overview

Deprecated patterns from pre-interface Forge code. These rules enable automated detection and migration guidance for any remaining or newly introduced legacy patterns. All rules map to interface-based replacements documented in the [Migration Guide](migration_guide.md).

---

## Deprecated Patterns

### D1: Hardcoded Context Path (Skills — `../../context/`)

**Severity**: Error
**Detection**: `grep -rn '../../context/' forge-plugin/skills/*/SKILL.md`
**Regex**: `\.\./\.\./context/`
**Replacement**: Use `contextProvider.getDomainIndex()`, `contextProvider.getAlwaysLoadFiles()`, etc.
**Example**:
```
BEFORE: Read ../../context/python/common_issues.md
AFTER:  contextProvider.getAlwaysLoadFiles("python")
```

### D2: Hardcoded Memory Path (Skills — `../../memory/`)

**Severity**: Error
**Detection**: `grep -rn '../../memory/' forge-plugin/skills/*/SKILL.md`
**Regex**: `\.\./\.\./memory/`
**Replacement**: Use `memoryStore.getSkillMemory()`, `memoryStore.getSharedProjectMemory()`, etc.
**Example**:
```
BEFORE: Read ../../memory/skills/python-code-review/{project}/project_overview.md
AFTER:  memoryStore.getSkillMemory("python-code-review", project)
```

### D3: Hardcoded Context Path (Commands — `../../context/`)

**Severity**: Error
**Detection**: `grep -rn '../../context/' forge-plugin/commands/*/COMMAND.md`
**Regex**: `\.\./\.\./context/`
**Replacement**: Use ContextProvider interface methods.

### D4: Hardcoded Memory Path (Commands — `../../memory/`)

**Severity**: Error
**Detection**: `grep -rn '../../memory/' forge-plugin/commands/*/COMMAND.md`
**Regex**: `\.\./\.\./memory/`
**Replacement**: Use MemoryStore interface methods.

### D5: Hardcoded Context Path (Agents — `../context/`)

**Severity**: Error
**Detection**: `grep -rn '../context/' forge-plugin/agents/*.md`
**Regex**: `\.\./context/`
**Replacement**: Use agent config.json `context.primaryDomains` + ContextProvider.

### D6: Hardcoded Memory Path (Agents — `../memory/`)

**Severity**: Error
**Detection**: `grep -rn '../memory/' forge-plugin/agents/*.md`
**Regex**: `\.\./memory/`
**Replacement**: Use agent config.json `memory.storagePath` + MemoryStore.

### D7: Hardcoded Context Path (Agents — `../../context/`)

**Severity**: Error
**Detection**: `grep -rn '../../context/' forge-plugin/agents/*.md`
**Regex**: `\.\./\.\./context/`
**Replacement**: Use ContextProvider via agent config.json.

### D8: Manual Timestamp Management

**Severity**: Warning
**Detection**: `grep -rn 'Last Updated:' forge-plugin/skills/*/SKILL.md forge-plugin/commands/*/COMMAND.md | grep -v '^---' | grep -v frontmatter`
**Regex**: `<!-- Last Updated:.*-->` (in skill/command workflow instructions telling users to manually manage timestamps)
**Replacement**: MemoryStore auto-manages timestamps on `create()`, `update()`, and `append()`.
**Example**:
```
BEFORE: Add <!-- Last Updated: YYYY-MM-DD --> to the memory file
AFTER:  memoryStore.update(id, content)  // timestamp auto-managed
```

### D9: Missing YAML Frontmatter on Context Files

**Severity**: Warning
**Detection**: `find forge-plugin/context -name "*.md" -exec sh -c 'head -1 "$1" | grep -qv "^---" && echo "$1"' _ {} \;`
**Regex**: (file-level check, not content regex)
**Replacement**: Add YAML frontmatter with required fields per `schemas/context_metadata.schema.json`.

### D10: Missing Agent config.json

**Severity**: Warning
**Detection**: `for f in forge-plugin/agents/*.md; do name=$(basename "$f" .md); [ ! -f "forge-plugin/agents/${name}.config.json" ] && echo "Missing: ${name}.config.json"; done`
**Regex**: (file existence check)
**Replacement**: Create `{agent-name}.config.json` per `schemas/agent_config.schema.json`.

### D11: Missing Interface References in Skills

**Severity**: Warning
**Detection**: `grep -L 'contextProvider\|ContextProvider\|memoryStore\|MemoryStore' forge-plugin/skills/*/SKILL.md`
**Regex**: (absence check)
**Replacement**: Reference ContextProvider and MemoryStore interfaces in workflow steps.

### D12: Missing Interface References in Commands

**Severity**: Warning
**Detection**: `grep -L 'contextProvider\|ContextProvider\|memoryStore\|MemoryStore' forge-plugin/commands/*/COMMAND.md`
**Regex**: (absence check)
**Replacement**: Reference ContextProvider and MemoryStore interfaces in workflow steps.

---

## Lint Script Design

### Individual Checks

Each pattern can be checked with a one-liner:

```bash
# D1: Skills with hardcoded context paths
grep -rn '../../context/' forge-plugin/skills/*/SKILL.md | grep -v '../../interfaces/' | wc -l

# D2: Skills with hardcoded memory paths
grep -rn '../../memory/' forge-plugin/skills/*/SKILL.md | grep -v '../../interfaces/' | wc -l

# D3-D4: Commands with hardcoded paths
grep -rn '../../context/\|../../memory/' forge-plugin/commands/*/COMMAND.md | grep -v '../../interfaces/' | wc -l

# D5-D7: Agents with hardcoded paths
grep -rn '\.\./context/\|\.\./memory/\|../../context/' forge-plugin/agents/*.md | grep -v '../../interfaces/' | wc -l

# D8: Manual timestamp instructions
grep -rn 'manually.*timestamp\|add.*Last Updated\|update.*Last Updated' forge-plugin/skills/*/SKILL.md forge-plugin/commands/*/COMMAND.md | wc -l

# D9: Context files without frontmatter
find forge-plugin/context -name "*.md" -exec sh -c 'head -1 "$1" | grep -qv "^---" && echo "$1"' _ {} \; | wc -l

# D10: Agents without config.json
for f in forge-plugin/agents/*.md; do name=$(basename "$f" .md); [ ! -f "forge-plugin/agents/${name}.config.json" ] && echo "$name"; done | wc -l

# D11-D12: Files without interface references
grep -rL 'contextProvider\|ContextProvider\|memoryStore\|MemoryStore' forge-plugin/skills/*/SKILL.md | wc -l
grep -rL 'contextProvider\|ContextProvider\|memoryStore\|MemoryStore' forge-plugin/commands/*/COMMAND.md | wc -l
```

### Full Lint Script: `deprecation_linter.sh`

```bash
#!/bin/bash
# Forge Deprecation Linter
# Checks for deprecated patterns across skills, commands, and agents
# Usage: bash forge-plugin/interfaces/deprecation_linter.sh

set -euo pipefail
FORGE_ROOT="${1:-.}/forge-plugin"
ERRORS=0
WARNINGS=0

echo "=== Forge Deprecation Linter ==="
echo ""

# D1-D2: Skills hardcoded paths (Error)
count=$(grep -rn '../../context/\|../../memory/' "$FORGE_ROOT/skills/"*/SKILL.md 2>/dev/null | grep -v '../../interfaces/' | wc -l)
if [ "$count" -gt 0 ]; then
  echo "D1-D2: $count hardcoded paths in skills (ERROR)"
  ERRORS=$((ERRORS + count))
else
  echo "D1-D2: No hardcoded paths in skills"
fi

# D3-D4: Commands hardcoded paths (Error)
count=$(grep -rn '../../context/\|../../memory/' "$FORGE_ROOT/commands/"*/COMMAND.md 2>/dev/null | grep -v '../../interfaces/' | wc -l)
if [ "$count" -gt 0 ]; then
  echo "D3-D4: $count hardcoded paths in commands (ERROR)"
  ERRORS=$((ERRORS + count))
else
  echo "D3-D4: No hardcoded paths in commands"
fi

# D5-D7: Agents hardcoded paths (Error)
count=$(grep -rn '\.\./context/\|\.\./memory/\|../../context/' "$FORGE_ROOT/agents/"*.md 2>/dev/null | grep -v '../../interfaces/' | wc -l)
if [ "$count" -gt 0 ]; then
  echo "D5-D7: $count hardcoded paths in agents (ERROR)"
  ERRORS=$((ERRORS + count))
else
  echo "D5-D7: No hardcoded paths in agents"
fi

# D9: Context files without frontmatter (Warning)
count=$(find "$FORGE_ROOT/context" -name "*.md" -exec sh -c 'head -1 "$1" | grep -qv "^---" && echo "$1"' _ {} \; 2>/dev/null | wc -l)
if [ "$count" -gt 0 ]; then
  echo "D9: $count context files without YAML frontmatter (WARNING)"
  WARNINGS=$((WARNINGS + count))
else
  echo "D9: All context files have YAML frontmatter"
fi

# D10: Agents without config.json (Warning)
count=0
for f in "$FORGE_ROOT/agents/"*.md; do
  name=$(basename "$f" .md)
  [ ! -f "$FORGE_ROOT/agents/${name}.config.json" ] && count=$((count + 1))
done
if [ "$count" -gt 0 ]; then
  echo "D10: $count agents without config.json (WARNING)"
  WARNINGS=$((WARNINGS + count))
else
  echo "D10: All agents have config.json"
fi

echo ""
echo "=== Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
[ "$ERRORS" -gt 0 ] && exit 1 || exit 0
```

---

## Migration Guidance

For each deprecated pattern, see the [Migration Guide](migration_guide.md) for detailed before/after examples and step-by-step migration instructions.

| Pattern | Migration Guide Section |
|---------|------------------------|
| D1-D2 | Skills Migration |
| D3-D4 | Commands Migration |
| D5-D7 | Agents Migration |
| D8 | MemoryStore Auto-Timestamps |
| D9 | Context File Frontmatter |
| D10 | Agent Configuration |
| D11-D12 | Interface Reference Adoption |

---

*Last Updated: 2026-02-11*
