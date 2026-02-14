---
description: "Prune stale context files and validate context integrity in Forge"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-quality-issue-template.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
    paths:
      - "forge-plugin/context/**"
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
    labels: ["forge-automation", "context", "maintenance"]
    title-prefix: "[context-maintenance] "
    max: 1
    close-older-issues: true
    expires: 14
---

# Forge Context Pruner & Maintainer

Validate and maintain the integrity of Forge's context file system.

## Validation Checks

### 1. Staleness Detection

For each context file in `forge-plugin/context/`:
- Check if referenced skills still exist in `forge-plugin/skills/`
- Check if referenced agents still exist in `forge-plugin/agents/`
- Flag files with `lastUpdated` older than 90 days

### 2. Frontmatter Validation

Every context file must have these required YAML frontmatter fields:
- `id` (string, format: "{domain}/{filename}")
- `domain` (string, must match parent directory name)
- `title` (string)
- `type` (string: reference | guide | checklist)
- `estimatedTokens` (number, > 0, < 5000)
- `loadingStrategy` (string: always | conditional | on-demand)
- `version` (string, semver format)
- `lastUpdated` (string, ISO date format YYYY-MM-DD)
- `sections` (array of objects, each with `name`, `estimatedTokens`, `keywords`)
- `tags` (array of strings)

### 3. Drift Detection

Compare context file content against its source skill's `SKILL.md`:
- Are the context's "Common Issues" still relevant to the skill's current state?
- Has the skill added capabilities not reflected in the context file?
- Are framework versions mentioned in the context still current?

### 4. Index Integrity

- Every `.md` file in `forge-plugin/context/{domain}/` (except `index.md`) must have an entry in `{domain}/index.md`
- Every entry in `{domain}/index.md` must point to an existing file
- `forge-plugin/context/index.md` file counts must match actual file counts per domain

## Severity Classification

- 🔴 **Critical**: Broken skill/agent references, missing required frontmatter fields, orphaned index entries pointing to non-existent files
- 🟡 **Warning**: Stale content (>90 days), significant drift from source skill, file count mismatches in indexes
- 🟢 **Info**: Minor drift, version updates available, token estimate adjustments suggested

## Output

Create a single issue titled `[context-maintenance] Context Health Report — {today's date}`
with a table of findings organized by severity level.

Include summary statistics:
- Total context files scanned
- Files passing all checks
- Critical / Warning / Info counts
- Domains with the most issues
