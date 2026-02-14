---
description: "DEPRECATED: Migrated to forge-component-improver.md — see Phase 3 consolidation"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "simplicity", "skills"]
    title-prefix: "[simplify] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# ⚠️ DEPRECATED: Forge Skill Simplifier

**This workflow has been DEPRECATED and replaced by `forge-component-improver.md`.**

- **Replacement**: [forge-component-improver.md](./forge-component-improver.md)
- **Migration Date**: 2026-02-13
- **Deprecation Phase**: Phase 3 — Pipeline Consolidation
- **Reason**: Consolidated with `forge-best-practices-improver.md` to reduce duplication and create unified component improvement pipeline

**This workflow is disabled for automatic runs.** It can only be triggered manually via `workflow_dispatch` as an escape hatch. It will be deleted after 2 weeks of successful consolidated workflow operation.

---

# Original: Forge Skill Simplifier

Analyze skill files in `forge-plugin/skills/` for simplification opportunities.

## Analysis Targets

For each `SKILL.md` file changed in this PR, check for:

1. **Verbose instructions** — can they be expressed more concisely?
2. **Redundant sections** — duplicate information across Overview, Workflow Steps, etc.
3. **Inconsistent structure** — deviations from `SKILL_TEMPLATE.md` pattern
4. **Over-engineered examples** — examples that demonstrate too many concepts at once
5. **Dead references** — links to skills, agents, or context files that don't exist

## Reference

Read `forge-plugin/skills/SKILL_TEMPLATE.md` to understand the canonical skill structure.
Each skill directory should contain at minimum `SKILL.md` and `examples.md`.
Skills must follow the 6-step mandatory workflow:
1. Initial Analysis
2. Load Memory
3. Load Context
4. Perform Analysis
5. Generate Output
6. Update Memory

## Constraints

- Preserve all meaningful content — only remove true redundancy
- Keep technical accuracy — don't simplify at the cost of correctness
- Follow the 6-step mandatory workflow pattern
- Maximum 3 PRs per run
- Each PR should address one skill file
- Only analyze skills that were changed in the triggering PR

## Output

For each simplification, create a PR with:
- Clear title: `[simplify] {skill-name}: {what was simplified}`
- Description explaining what was simplified and why
- Before/after comparison in PR body
