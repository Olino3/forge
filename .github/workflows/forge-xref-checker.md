---
description: "Detect broken cross-references between Forge components"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-quality-issue-template.md
  - shared/forge-conventions.md
on:
  schedule: "weekly on tuesday"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "cross-reference", "integrity"]
    title-prefix: "[xref] "
    max: 1
    close-older-issues: true
    expires: 14
---

# Forge Cross-Reference Checker

Detect broken cross-references between Forge components to maintain system integrity.

## Cross-Reference Matrix

Validate all bidirectional relationships:

### 1. Skills ↔ Context Files (Domain Mapping)

**Check**: Do skills reference context domains that exist?

For each `SKILL.md`:
- Extract domain references from "Load Context" section
- Verify each domain exists in `forge-plugin/context/{domain}/`
- Verify domain has files (not just empty directory)

**Example violations**:
- Skill references `python` domain but `forge-plugin/context/python/` is empty
- Skill references `react` domain but only `angular` exists

### 2. Skills ↔ Agent Configs (Skills Array)

**Check**: Do agent configs reference skills that exist?

For each `forge-plugin/agents/*.config.json`:
- Extract `skills` array from config
- Verify each skill directory exists in `forge-plugin/skills/{skill-name}/`
- Verify skill has both `SKILL.md` and `examples.md`

**Example violations**:
- Agent config lists `"python-testing"` but `forge-plugin/skills/python-testing/` doesn't exist
- Agent config lists `"react-forms"` but only `SKILL.md` exists (missing `examples.md`)

### 3. Skills ↔ Commands (Frontmatter Skills)

**Check**: Do commands reference skills that exist?

For each command in `forge-plugin/commands/*/`:
- Parse YAML frontmatter
- Extract `skills` array
- Verify each skill exists in `forge-plugin/skills/`

**Example violations**:
- Command frontmatter lists `"azure-deployment"` but skill doesn't exist
- Command delegates to skill that was renamed or removed

### 4. Agents ↔ MCP Configs (AllowedMcps)

**Check**: Do agent configs reference valid MCP servers?

For each `forge-plugin/agents/*.config.json`:
- Extract `allowedMcps` array (if present)
- Verify each MCP has documentation in `forge-plugin/mcps/servers/{mcp-name}.md`
- Verify MCP is listed in `forge-plugin/mcps/index.md`

**Example violations**:
- Agent references `"tavily"` but no `forge-plugin/mcps/servers/tavily.md`
- Agent references outdated MCP that was removed

### 5. Context ↔ Domain Indexes (File Listings)

**Check**: Are all context files listed in their domain index?

For each domain in `forge-plugin/context/`:
- List all `.md` files (excluding `index.md`)
- Parse domain's `index.md` for file references
- Detect orphaned files (exist but not in index)
- Detect ghost entries (in index but file doesn't exist)

**Example violations**:
- `forge-plugin/context/python/pandas-guide.md` exists but not listed in `python/index.md`
- `python/index.md` references `django-auth.md` but file doesn't exist

### 6. Hooks ↔ hooks.json (Registration)

**Check**: Are all hook scripts registered in hooks.json?

For each `.sh` file in `forge-plugin/hooks/`:
- Check if script basename appears in `hooks.json` as a handler
- Verify hook has corresponding entry in `hooks.json` with event mapping

**Example violations**:
- `memory_pruning_daemon.sh` exists but not registered in `hooks.json`
- `hooks.json` references `old_hook.sh` that was deleted

### 7. Hooks ↔ HOOKS_GUIDE.md (Documentation)

**Check**: Are all hooks documented in the guide?

For each hook in `hooks.json`:
- Verify hook is mentioned in `forge-plugin/hooks/HOOKS_GUIDE.md`
- Check if documentation includes purpose, event, and layer assignment

**Example violations**:
- Hook `sandbox_boundary_guard` registered but not documented in guide
- Documentation mentions deleted hook `legacy_checker`

### 8. Commands ↔ Context Domains (Context Array)

**Check**: Do commands reference valid context domains?

For each command frontmatter:
- Extract `context` array (if present)
- Verify each domain exists in `forge-plugin/context/{domain}/`

**Example violations**:
- Command references `kubernetes` context but domain doesn't exist
- Command references outdated domain name

## Output Format

Create a single issue with broken references organized by severity:

```markdown
# Cross-Reference Integrity Report — {YYYY-MM-DD}

## Summary

- 🔴 Critical: {count} broken references
- 🟡 Warning: {count} missing documentation
- 🟢 Info: {count} suggestions
- Total references checked: {count}

---

## 🔴 Critical Issues (Broken References)

### Skills → Context Domains

- [ ] `{skill-name}` references domain `{domain}` which doesn't exist
  - **Location**: `forge-plugin/skills/{skill-name}/SKILL.md`
  - **Fix**: Create context domain or update skill to reference valid domain

### Agents → Skills

- [ ] `{agent-name}.config.json` references skill `{skill}` which doesn't exist
  - **Location**: `forge-plugin/agents/{agent-name}.config.json`
  - **Fix**: Remove reference or create missing skill

### Commands → Skills

- [ ] `{command-name}` references skill `{skill}` which doesn't exist
  - **Location**: `forge-plugin/commands/{command-name}/COMMAND.md`
  - **Fix**: Update command frontmatter or restore skill

### Agents → MCPs

- [ ] `{agent-name}.config.json` references MCP `{mcp}` which doesn't exist
  - **Location**: `forge-plugin/agents/{agent-name}.config.json`
  - **Fix**: Remove MCP reference or add MCP documentation

---

## 🟡 Warnings (Missing Index/Documentation)

### Context Files → Domain Indexes

- [ ] `{file-path}` exists but not listed in domain index
  - **Location**: `{file-path}`
  - **Fix**: Add entry to `{domain}/index.md`

### Domain Indexes → Context Files

- [ ] `{domain}/index.md` references `{file}` which doesn't exist
  - **Location**: `forge-plugin/context/{domain}/index.md`
  - **Fix**: Remove entry or create missing file

### Hooks → hooks.json

- [ ] `{hook-name}.sh` exists but not registered in hooks.json
  - **Location**: `forge-plugin/hooks/{hook-name}.sh`
  - **Fix**: Add registration entry to `hooks.json`

### Hooks → HOOKS_GUIDE.md

- [ ] `{hook-name}` registered but not documented in guide
  - **Location**: `forge-plugin/hooks/hooks.json`
  - **Fix**: Add documentation to `HOOKS_GUIDE.md`

---

## 🟢 Suggestions

- Consider adding context domain for frequently referenced technologies
- Document rationale for agent-skill assignments
- Add examples for newly referenced skills

---

## Health Score

**Cross-Reference Integrity**: {percentage}%

- Skills → Context: {valid}/{total} ({%})
- Agents → Skills: {valid}/{total} ({%})
- Commands → Skills: {valid}/{total} ({%})
- Agents → MCPs: {valid}/{total} ({%})
- Context → Indexes: {valid}/{total} ({%})
- Hooks → Registry: {valid}/{total} ({%})
- Hooks → Docs: {valid}/{total} ({%})
```

## Analysis Approach

1. **Parse Configuration Files**: Use `jq` to extract arrays from JSON configs
2. **Directory Listing**: Use `find` to enumerate actual files
3. **Text Parsing**: Use `grep` to find references in Markdown frontmatter
4. **Set Operations**: Compare "expected" vs "actual" to find missing/extra items
5. **Report Generation**: Group by severity and component type

## Constraints

- Only report actual broken references, not potential improvements
- Include file paths and line numbers where possible
- Provide actionable fix suggestions for each issue
- Maximum 1 issue per run (consolidate all findings)
- Close previous week's issue automatically

## Example Commands

```bash
# Extract skills from agent config
jq -r '.skills[]' forge-plugin/agents/zeus.config.json

# List all skill directories
find forge-plugin/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \;

# Find context domain references in skills
grep -r "contextProvider.getIndex" forge-plugin/skills/ | cut -d'"' -f2 | sort -u

# List hooks in hooks.json
jq -r '.hooks[].handler' forge-plugin/hooks/hooks.json | sort

# List actual hook files
find forge-plugin/hooks -name "*.sh" -type f -exec basename {} \; | sort
```
