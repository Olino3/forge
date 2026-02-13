---
description: "Validate Forge skill structure compliance against SKILL_TEMPLATE.md"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-quality-issue-template.md
  - shared/forge-conventions.md
on:
  schedule: "0 9 * * 2,4"
  pull_request:
    types: [opened, synchronize]
    paths:
      - "forge-plugin/skills/*/SKILL.md"
      - "forge-plugin/skills/*/examples.md"
      - "forge-plugin/skills/SKILL_TEMPLATE.md"
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
    labels: ["forge-automation", "refactoring", "skills"]
    title-prefix: "[skill-structure] "
    max: 5
    close-older-issues: true
    expires: 14
---

# Forge Skill Structure Validator

Validate Forge skills against `forge-plugin/skills/SKILL_TEMPLATE.md` and report structural gaps.

## Checks

For each relevant skill directory in `forge-plugin/skills/`:

1. **Template compliance**: `SKILL.md` contains required template sections.
2. **6-step workflow compliance**: The skill explicitly follows:
   1. Initial Analysis
   2. Load Memory
   3. Load Context
   4. Perform Analysis
   5. Generate Output
   6. Update Memory
3. **Examples presence**: Directory includes `examples.md`.
4. **Skill isolation**: No hardcoded references to other skills or filesystem paths.
5. **Output conventions**: References `OUTPUT_CONVENTIONS.md` where output format is defined.

## Scope

- On pull requests, prioritize changed skills.
- On schedule/manual runs, scan all skill directories.

## Output

Create issues for meaningful violations only, with:
- Exact files and missing/invalid elements
- Concrete remediation steps
- Severity (critical/warning/info)
