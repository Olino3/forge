---
description: "Consolidated workflow to improve and simplify Forge components based on best practices"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
  - shared/model-codex-mini.md
engine:
  id: copilot
  model: gpt-5.1-codex-mini
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop]
    paths:
      - "forge-plugin/skills/**"
      - "forge-plugin/agents/**"
      - "forge-plugin/commands/**"
      - "forge-plugin/context/**"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default, pull_requests]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "improvement", "component-quality"]
    title-prefix: "[improve] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# Forge Component Improver

**Consolidated Workflow** — Replaces:
- `forge-best-practices-improver.md` (best practices compliance)
- `forge-skill-simplifier.md` (verbosity reduction)

This workflow analyzes changed Forge components (skills, agents, commands, context) in feature branch PRs and creates a single unified draft PR with improvements addressing both best practices compliance and simplification opportunities.

## Three-Stage Pipeline

This workflow executes in three sequential stages:

### Stage 1: Analyze Changes

**Objective**: Identify all changed Forge components and classify them by type.

**Steps**:

1. **Fetch changed files** from the triggering PR using GitHub API
2. **Filter and classify**:
   - Skills: `forge-plugin/skills/*/SKILL.md`
   - Agents: `forge-plugin/agents/*.md` and `forge-plugin/agents/*.config.json`
   - Commands: `forge-plugin/commands/*.md`
   - Context: `forge-plugin/context/**/*.md`
3. **Read each file** and extract current structure
4. **Output**: Structured analysis mapping each file to its component type and current state

**Exit Criteria**: If no relevant files are found, stop and output "No Forge components changed. Exiting."

---

### Stage 2: Improve + Simplify

**Objective**: For each identified component, perform both best practices checks and simplification analysis in one pass.

**Reference Documents**:
- `CONTRIBUTING.md` — contribution guidelines
- `CLAUDE.md` — Forge operating manual
- `forge-plugin/skills/SKILL_TEMPLATE.md` — canonical skill structure
- `forge-plugin/interfaces/schemas/*.schema.json` — JSON validation schemas
- Anthropic Claude Code Repository: https://github.com/anthropics/claude-code (for latest conventions)

**Component-Specific Analysis**:

#### For Skills (`SKILL.md` files):

**Best Practices Checks**:
- ✓ Does the skill follow the 6-step mandatory workflow?
  - 1. Initial Analysis
  - 2. Load Memory
  - 3. Load Context
  - 4. Perform Analysis
  - 5. Generate Output
  - 6. Update Memory
- ✓ Are interface references used instead of hardcoded paths?
  - Must use `contextProvider`, `memoryStore`, `skillInvoker`
  - No hardcoded filesystem paths allowed
- ✓ Are examples provided in `examples.md`?
- ✓ Does output follow `OUTPUT_CONVENTIONS.md`?
- ✓ Are all required sections from SKILL_TEMPLATE.md present?

**Simplification Checks**:
- ✗ Verbose instructions — can they be more concise?
- ✗ Redundant sections — duplicate information across Overview, Workflow Steps, etc.
- ✗ Over-engineered examples — examples demonstrating too many concepts at once
- ✗ Dead references — links to skills, agents, or context files that don't exist

#### For Agents (`.md` and `.config.json` files):

**Best Practices Checks**:
- ✓ Does `.config.json` validate against `agent_config.schema.json`?
- ✓ Are context domains declared and do they exist in `forge-plugin/context/`?
- ✓ Are skill references valid (skills actually exist)?
- ✓ Are MCP references valid (MCPs actually exist in `forge-plugin/mcps/`)?
- ✓ Is the model choice appropriate for the agent's role?
- ✓ Are tool declarations consistent with agent capabilities?

**Simplification Checks**:
- ✗ Verbose personality descriptions in `.md` file
- ✗ Redundant expertise listings
- ✗ Over-long workflow descriptions

#### For Commands (`.md` files):

**Best Practices Checks**:
- ✓ Does YAML frontmatter include all required fields?
  - `name`, `description`, `category`, `complexity`, `skills`, `context`
- ✓ Are workflow steps clearly defined?
- ✓ Does the command use `ExecutionContext` for chaining (if applicable)?
- ✓ Are skill delegations using `skillInvoker` interface?
- ✓ Are context domains properly declared and valid?

**Simplification Checks**:
- ✗ Verbose step descriptions
- ✗ Redundant examples
- ✗ Over-complicated workflow steps

#### For Context (`.md` files):

**Best Practices Checks**:
- ✓ Does YAML frontmatter validate against `context_metadata.schema.json`?
- ✓ Are required frontmatter fields present?
  - `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`, `version`, `lastUpdated`, `sections`, `tags`
- ✓ Is `estimatedTokens` reasonable and accurate (±20%)?
- ✓ Is `lastUpdated` current (within 90 days)?
- ✓ Are `tags` and `sections` arrays properly structured?
- ✓ Is the content domain-appropriate and not duplicating skill content?

**Simplification Checks**:
- ✗ Verbose explanations that could be condensed
- ✗ Duplicate information across sections
- ✗ Over-long code examples

**Output**: Unified improvement list with each improvement categorized as:
- **[BP]** Best Practice violation
- **[SIMP]** Simplification opportunity
- **[BP+SIMP]** Both

Format:
```json
{
  "changes": [
    {
      "file": "forge-plugin/skills/example/SKILL.md",
      "type": "skill",
      "improvements": [
        {
          "category": "BP",
          "issue": "Missing step 2 (Load Memory) in workflow",
          "fix": "Add Load Memory section with memoryStore.read() call",
          "line_range": "45-60"
        },
        {
          "category": "SIMP",
          "issue": "Verbose overview section (150 words, could be 50)",
          "fix": "Condense to 3 bullet points",
          "line_range": "10-25"
        }
      ]
    }
  ]
}
```

**Constraints**:
- Maximum 3 components improved per run (prioritize by impact)
- Preserve all meaningful content — only remove true redundancy
- Keep technical accuracy — don't simplify at the cost of correctness
- Each improvement must have clear before/after justification

---

### Stage 3: Generate Draft PR

**Objective**: Apply all approved improvements and create a single consolidated draft PR on the feature branch.

**Steps**:

1. **Apply changes** to each file identified in Stage 2
2. **Verify changes** — re-read each modified file to ensure correctness
3. **Generate PR body** with structured summary:

**PR Body Template**:

```markdown
# Component Improvements

This PR consolidates best practices improvements and simplification changes for Forge components modified in PR #{triggering-pr-number}.

## Summary

- **Components analyzed**: {count}
- **Best practice fixes**: {count}
- **Simplification improvements**: {count}
- **Total changes**: {count}

## Changes by Component

### Skills

#### `{skill-name}`
**Best Practices**:
- ✓ Fixed: {issue description}
- ✓ Fixed: {issue description}

**Simplification**:
- ✗ Reduced verbosity in {section}: {before word count} → {after word count} words

### Agents

#### `{agent-name}`
**Best Practices**:
- ✓ Fixed: {issue description}

### Commands

#### `{command-name}`
**Simplification**:
- ✗ Condensed workflow steps from {before} to {after} steps

### Context

#### `{context-file}`
**Best Practices**:
- ✓ Updated `lastUpdated` field (was {old-date}, now {new-date})
- ✓ Corrected `estimatedTokens` (was {old}, now {new} — measured at {actual})

## Review Guidance

This is an automated improvement PR. Please review:

1. ✅ Are best practice fixes accurate and necessary?
2. ✅ Do simplifications preserve technical meaning?
3. ✅ Are all file changes correct and complete?

If approved, merge to apply improvements to the feature branch.
If changes are needed, edit this PR or close and re-run the workflow with `workflow_dispatch`.
```

4. **Create PR** with:
   - Title: `[improve] {component-names}: best practices + simplification`
   - Labels: `forge-automation`, `improvement`, `component-quality`
   - Draft: true
   - Base branch: feature branch from triggering PR
   - Expires: 7 days

**Exit Criteria**: If no improvements are identified in Stage 2, output "All components meet current standards. No changes needed." and exit without creating a PR.

---

## Loop Prevention

If the triggering PR meets any of these conditions, do nothing:
- Has label `forge-automation`
- Title starts with `[improve]`, `[best-practices]`, `[simplify]`, or `[forge-`
- Is from a bot account

---

## Workflow Constraints

- Only analyze components changed in the triggering PR
- Focus on high-impact improvements (correctness > style)
- Keep edits minimal and reviewable
- One consolidated PR per run (not one per component)
- All schema validations must use the actual JSON schema files
- All path existence checks must verify against the repository

---

## Success Criteria

✅ Stage 1 correctly identifies and classifies all changed components  
✅ Stage 2 performs comprehensive analysis for both best practices and simplification  
✅ Stage 3 creates a single, well-structured draft PR  
✅ PR body clearly categorizes improvements by type and component  
✅ All changes preserve technical accuracy and meaning  
✅ No false positives (claimed violations that aren't actual violations)  
