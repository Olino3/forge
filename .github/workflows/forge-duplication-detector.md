---
description: "Detect duplicated content across Forge skills, context, and hooks"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-quality-issue-template.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
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
    labels: ["forge-automation", "simplicity", "duplication"]
    title-prefix: "[duplication] "
    max: 3
    close-older-issues: true
    expires: 14
---

# Forge Duplication Detector

Detect duplicated content patterns across Forge's skills, context files, hooks, and agent configs.

## Scan Scope

Focus on files changed in this PR, but also compare against the broader codebase for duplication:

### 1. Skill Duplication
- Duplicate instructions across similar skills (e.g., all auth skills sharing boilerplate)
- Repeated workflow step patterns that could be extracted to shared templates
- Identical constraint sections across multiple skills

### 2. Context Duplication
- Copy-pasted context sections that should be cross-referenced instead
- Duplicate domain knowledge spread across multiple context files
- Repeated frontmatter patterns that could become shared templates

### 3. Hook Duplication
- Identical hook logic that should be extracted to `forge-plugin/hooks/lib/`
- Repeated grep/jq patterns across multiple hook scripts
- Duplicate error handling patterns

### 4. Agent Config Duplication
- Identical `contextDomains` or `skills` arrays across multiple agents
- Repeated tool configurations that could be factored out

## Analysis Method

1. Read all files in the changed directories
2. Identify content blocks that appear in 2+ files with >70% similarity
3. For each duplication found, suggest a consolidation strategy:
   - **Extract to shared file** — for boilerplate that belongs in a template
   - **Cross-reference** — for context that should link rather than copy
   - **Extract to lib/** — for hook logic that should be a shared utility

## Output

Create an issue for each significant duplication cluster found, with:
- Title: `[duplication] {description of what's duplicated}`
- Body listing all files involved
- Suggested consolidation approach
- Estimated lines that could be removed
