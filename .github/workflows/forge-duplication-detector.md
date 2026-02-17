---
description: "Detect meaningful content duplication across Forge skills, context, and hooks"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
  - shared/forge-quality-issue-template.md
  - shared/model-codex-mini.md
engine:
  id: copilot
  model: gpt-5.1-codex-mini
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
    paths:
      - "forge-plugin/skills/**"
      - "forge-plugin/context/**"
      - "forge-plugin/hooks/**"
      - "forge-plugin/commands/**"
  schedule:
    - cron: "0 6 * * 1"
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
    labels: ["forge-automation", "quality", "duplication"]
    title-prefix: "[duplication] "
    expires: 14
    close-older-issues: true
    max: 1
---

# Forge Duplication Detector

Detect meaningful content duplication across Forge components. This workflow replaces the static `test_duplication.py` test which relied on brittle fuzzy matching with a growing boilerplate allowlist.

## Goal

Identify **copy-paste duplication** that should be refactored — NOT intentional shared patterns from templates or conventions.

## Scope

Scan these component types for duplicated content blocks:

| Component | Files | Location |
|-----------|-------|----------|
| Skills | `SKILL.md` | `forge-plugin/skills/*/SKILL.md` |
| Context | `*.md` | `forge-plugin/context/**/*.md` (excluding `index.md`) |
| Hooks | `*.sh` | `forge-plugin/hooks/*.sh` |
| Commands | `*.md` | `forge-plugin/commands/*.md` (excluding `index.md`) |

## Analysis Steps

### Step 1: Collect Files

1. List all files matching the scope above using file system tools
2. If triggered by a PR, focus analysis on changed files but compare against all files
3. If triggered by schedule/dispatch, scan all files

### Step 2: Identify Duplicate Content

For each pair of files within the same component type, look for content blocks (paragraphs, sections, or multi-line sequences) that are substantially similar.

**What counts as meaningful duplication:**
- Entire sections copy-pasted between skills with only the skill name changed
- Identical workflow step descriptions that go beyond the standard 6-step template
- Duplicated domain-specific guidance (e.g., identical code examples, identical pattern catalogs)
- Copied analysis criteria, decision trees, or evaluation rubrics

**What is NOT duplication (ignore these):**
- Standard 6-step workflow headers (Initial Analysis, Load Memory, Load Context, Perform Analysis, Generate Output, Update Memory)
- Compliance checklist items following the template pattern (`- [ ] Step N ...`)
- Interface reference blocks (`contextProvider`, `memoryStore`, `skillInvoker`)
- File structure sections listing `SKILL.md` + `examples.md`
- Memory loading patterns referencing `shared_loading_patterns.md`
- Output convention references to `OUTPUT_CONVENTIONS.md`
- YAML frontmatter with standard fields
- Hook preambles (`set -euo pipefail`, `source` shared libraries, `jq` parsing)
- Version history entries

### Step 3: Assess Severity

For each duplication finding, classify severity:

- **critical**: Entire sections (>500 chars) duplicated verbatim or near-verbatim across files, indicating copy-paste without adaptation
- **warning**: Significant blocks (200-500 chars) that are >80% similar and contain domain-specific content that should be unique
- **info**: Moderate similarity (70-80%) in blocks that may warrant consolidation but aren't urgent

### Step 4: Generate Report

If meaningful duplication is found, create an issue following the [standard quality requirements](shared/forge-quality-issue-template.md#standard-issue-quality-requirements).

For this workflow, include:
- Exact file paths for both files in each duplicate pair
- The duplicated content block (first 200 chars) as evidence
- Whether the duplication is verbatim or near-verbatim
- Suggested remediation (extract to shared context, differentiate content, or accept as intentional)

## Output

Only create an issue if **critical** or **warning** level duplication is found. Do not create issues for **info** level findings alone.

If no meaningful duplication is found, output: "No actionable content duplication detected."

## Constraints

- Compare files only within the same component type (skills vs skills, context vs context)
- Skip files smaller than 500 characters
- Focus on content blocks, not headers or metadata
- Maximum 10 findings per issue (prioritize by severity)
- Do not flag duplication between a skill and its own `examples.md`
