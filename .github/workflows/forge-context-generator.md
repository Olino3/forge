---
description: "Generate context files when new skills are added to Forge"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
  - shared/model-codex-mini.md
engine:
  id: copilot
  model: claude-haiku-4.5
on:
  pull_request:
    types: [closed]
    paths:
      - "forge-plugin/skills/*/SKILL.md"
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default, pull_requests]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "context", "new-skill"]
    title-prefix: "[context] "
    expires: 14
    draft: true
    if-no-changes: "ignore"
---

# Forge Context Generator

When a new skill is added to `forge-plugin/skills/`, generate a matching context file.

## Prerequisites

This workflow only runs on **merged** pull requests. If the PR was closed without merging, exit immediately with no action.

## Step 1: Identify New Skills

Check the merged PR for **new** `SKILL.md` files added under `forge-plugin/skills/`.
If this PR does not add new skills (only modifies existing ones), exit with no action.

To determine if a file is new vs modified, check the PR's file status — only process files with status `added`.

## Step 2: Determine Context Domain

Map the skill to an existing context domain based on its category:

| Skill Category | Context Domain |
|---------------|----------------|
| Python-related (django, fastapi, pandas, etc.) | `python/` |
| .NET-related (dotnet-core, csharp) | `dotnet/` |
| Angular-related | `angular/` |
| Azure-related (azure-auth, generate-azure-*) | `azure/` |
| Security-related (secure-code, security-reviewer) | `security/` |
| Git-related (get-git-diff, commit-helper) | `git/` |
| General engineering | `engineering/` |

If no domain exists, place in `engineering/`.

## Step 3: Generate Context File

Create `forge-plugin/context/{domain}/{skill-name}.md` with this structure:

```yaml
---
id: "{domain}/{skill-name}"
domain: {domain}
title: "{Skill Display Name} Context"
type: reference
estimatedTokens: 400
loadingStrategy: conditional
version: "0.3.0-alpha"
lastUpdated: "{today's date in YYYY-MM-DD format}"
sections:
  - name: "Overview"
    estimatedTokens: 50
    keywords: [overview, {skill-name}]
  - name: "Common Issues"
    estimatedTokens: 150
    keywords: [common, issues, problems]
  - name: "Quick Reference"
    estimatedTokens: 100
    keywords: [quick, reference, patterns]
  - name: "Integration"
    estimatedTokens: 100
    keywords: [integration, workflow]
tags: [{domain}, {skill-name}, context, reference]
---
```

Populate sections by reading the skill's `SKILL.md` and extracting:
- **Overview**: Key purpose and when to use this skill
- **Common Issues**: Typical problems and pitfalls (from the skill's domain)
- **Quick Reference**: Essential patterns, commands, or configurations
- **Integration**: How this skill connects to other Forge skills and context

## Step 4: Update Domain Index

Add the new file to `forge-plugin/context/{domain}/index.md`.
Follow the existing format in the index file — each entry should include:
- File path
- Brief description
- Estimated tokens

## Step 5: Update Top-Level Index

Update `forge-plugin/context/index.md` with the new file count for the affected domain.

## Step 6: Create PR

Create a single PR with all generated context files for human review.
Include in the PR body:
- Which skills triggered the generation
- Which domains were targeted
- What sections were generated
- Token estimates for each file
- A checklist for the reviewer:
  - [ ] Context accurately reflects the skill's purpose
  - [ ] Token estimates are reasonable
  - [ ] Domain assignment is correct
  - [ ] Index entries are properly formatted
