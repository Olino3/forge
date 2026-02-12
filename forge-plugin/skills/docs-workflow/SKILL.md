---
name: "docs-workflow"
description: "Four slash commands for documentation lifecycle: /docs, /docs-init, /docs-update, /docs-claude. Create, maintain, and audit CLAUDE.md, README.md, and docs/ structure with smart templates."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [doc_conventions.md, doc_history.md]
    - type: "shared-project"
      usage: "reference"
tags: ["planning", "workflow", "documentation", "lifecycle", "templates"]
---

# skill:docs-workflow - Documentation Lifecycle Manager

## Version: 1.0.0

## Purpose

The docs-workflow skill manages the complete documentation lifecycle for any project. It provides four slash commands — `/docs`, `/docs-init`, `/docs-update`, and `/docs-claude` — that create, maintain, and audit CLAUDE.md, README.md, and docs/ structures with smart templates. Like Hephaestus inscribing the purpose of each forged artifact, this skill ensures every project has clear, current, and comprehensive documentation.

## File Structure

```
skills/docs-workflow/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Triggers

- `create CLAUDE.md`
- `initialize documentation`
- `docs init`
- `update documentation`

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Detect documentation scope from user request and project state
- Identify project type (language, framework, monorepo vs single-repo)
- Determine which docs exist vs need creation:
  - Check for `CLAUDE.md`, `README.md`, `docs/` directory
  - Identify the slash command being invoked (`/docs`, `/docs-init`, `/docs-update`, `/docs-claude`)
- Assess project structure to inform template selection

### Step 2: Load Memory

- Use `memoryStore.getSkillMemory("docs-workflow", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
- Load project-specific documentation conventions and preferences
- Retrieve prior documentation generation history and patterns
- Check for established doc structure decisions from previous runs

### Step 3: Load Context

- Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- Load documentation standards and best practices
- Load project-type-specific templates and conventions
- Load output naming conventions from `../OUTPUT_CONVENTIONS.md`

### Step 4: Assess Documentation State

- Audit existing documentation files:
  - **CLAUDE.md**: Check for project conventions, build/test commands, architecture notes, coding standards
  - **README.md**: Check for project description, setup instructions, usage examples, contribution guidelines
  - **docs/ directory**: Check for structure, completeness, and organization
- Identify gaps: missing sections, outdated content, incomplete instructions
- Compare current project state against documentation accuracy
- Generate a documentation health score

### Step 5: Execute Documentation Action

Based on the command invoked, perform the appropriate action:

#### `/docs-init` — Initialize Documentation Structure
1. Create `CLAUDE.md` with project conventions, build commands, and architecture overview
2. Create or update `README.md` with project description, setup, usage, and contribution sections
3. Create `docs/` directory with appropriate structure for the project type
4. Populate templates with detected project information (language, framework, dependencies)

#### `/docs-update` — Update Existing Documentation
1. Scan project for changes since last documentation update (new files, changed APIs, updated dependencies)
2. Update `CLAUDE.md` with current build/test commands and conventions
3. Update `README.md` with current project state and any new sections needed
4. Update `docs/` files to reflect current architecture and APIs
5. Flag sections that may need manual review

#### `/docs-claude` — Generate or Refresh CLAUDE.md
1. Analyze project structure, build system, and conventions
2. Generate or refresh `CLAUDE.md` with:
   - Build and test commands
   - Code style and conventions
   - Architecture overview
   - Key file locations
   - Development workflow notes
3. Preserve any manually-added sections from existing `CLAUDE.md`

#### `/docs` — Documentation Status and Health Summary
1. Scan all documentation files for completeness and freshness
2. Report documentation health: what exists, what's missing, what's outdated
3. Provide actionable recommendations for improvement
4. Display a summary dashboard with coverage metrics

### Step 6: Generate Output

- Save output to `/claudedocs/docs_workflow_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include summary of actions taken, files created/modified, and recommendations

### Step 7: Update Memory

- Use `memoryStore.update(layer="skill-specific", skill="docs-workflow", project="{project-name}", ...)` to store insights. See [MemoryStore Interface](../../interfaces/memory_store.md).
- Record documentation conventions discovered for this project
- Track which templates and structures were used
- Store documentation health history for trend tracking
- Note any manual overrides or custom preferences

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Memory loaded via `memoryStore.getSkillMemory()` (Step 2)
- [ ] Context loaded via `contextProvider.getIndex()` (Step 3)
- [ ] Documentation state assessed with gap analysis (Step 4)
- [ ] Correct command action executed (Step 5)
- [ ] Output saved with standard naming convention
- [ ] Memory updated via `memoryStore.update()` (Step 7)

## Output File Naming Convention

**Format**: `docs_workflow_{project}_{YYYY-MM-DD}.md`

Where:
- `{project}` = Project name (lowercase, hyphens for spaces)
- `{YYYY-MM-DD}` = Date of execution

**Examples**:
- `docs_workflow_my-api_2026-03-15.md`
- `docs_workflow_forge-plugin_2026-03-15.md`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — four-command documentation lifecycle with smart templates, gap analysis, and health scoring |
