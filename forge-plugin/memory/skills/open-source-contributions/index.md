# Open Source Contributions - Memory System

This file documents the memory structure for the `open-source-contributions` skill. Memory is project-specific knowledge that accumulates over time through repeated contributions to open-source projects.

---

## Purpose

The memory system enables the skill to:
- **Remember project conventions** — Avoid re-reading CONTRIBUTING.md, linter configs, and CI pipelines on every contribution
- **Track contribution history** — Know what was submitted, merged, or rejected and why
- **Learn from reviewer feedback** — Apply past review comments to future contributions
- **Maintain relationships** — Remember maintainer preferences and communication style
- **Improve efficiency** — Faster contributions with known conventions pre-loaded

---

## Memory Structure

```
memory/skills/open-source-contributions/
├── index.md (this file)
└── {project-name}/
    ├── project_conventions.md     # Project-specific contribution conventions
    └── contribution_history.md    # Past contributions and reviewer feedback
```

---

## Per-Project Memory Files

### 1. project_conventions.md

**Purpose**: Store discovered conventions for a specific open-source project so they don't need to be re-analyzed on every contribution.

**What to Document**:
- Commit message format (Conventional Commits, Angular-style, custom)
- Branch naming conventions
- Code style rules (linter, formatter, indentation, naming)
- Test framework and coverage requirements
- CI/CD pipeline checks and their typical run times
- PR description template requirements
- CLA or DCO requirements
- Preferred communication style (formal, casual)
- Maintainer response patterns (typical review time, who reviews what)
- Merge strategy (squash, rebase, merge commit)

**Example Structure**:
```markdown
# Project Conventions: react-awesome-ui

## Contribution Workflow
- **Model**: Fork and PR
- **Branch naming**: `fix/issue-{number}` or `feature/{description}`
- **Merge strategy**: Squash merge

## Commit Format
- Conventional Commits required
- Scope matches component name (e.g., `fix(datepicker): ...`)
- commitlint enforced in CI

## Code Style
- ESLint + Prettier
- 2-space indent, single quotes, semicolons
- TypeScript strict mode

## Testing
- Jest + React Testing Library
- Tests colocated in `__tests__/` directories
- No coverage threshold, but reviewers expect tests for all changes

## CI Pipeline
- GitHub Actions: lint, typecheck, unit tests, visual regression
- Typical CI run: ~8 minutes
- Visual regression tests sometimes flaky — re-run if unrelated

## Review Process
- Core maintainers review within 48 hours
- @alice-maintainer handles component PRs
- @bob-maintainer handles infrastructure PRs
- CLA bot checks on first PR

## Documentation
- Storybook stories required for new components
- CHANGELOG.md updated by maintainers at release time
```

### 2. contribution_history.md

**Purpose**: Track past contributions to a project, including outcomes and lessons learned.

**What to Document**:
- Date and issue/PR reference for each contribution
- Type of contribution (bug fix, feature, docs, performance)
- Outcome (merged, closed, pending)
- Reviewer feedback and lessons learned
- Time from submission to merge

**Example Structure**:
```markdown
# Contribution History: react-awesome-ui

## 2025-07-14 - Fix DatePicker Locale Crash
- **Issue**: #4821
- **PR**: #4830
- **Type**: Bug fix
- **Status**: Merged
- **Review time**: 2 days
- **Feedback**: Reviewer requested moving the `useEffect` above the
  early return. Applied feedback, merged on second review.
- **Lesson**: This project prefers hooks at the top of the function
  body, even if they could be placed lower for readability.

## 2025-08-02 - Add Tooltip Delay Prop
- **Issue**: #4905
- **PR**: #4912
- **Type**: Feature
- **Status**: Merged
- **Review time**: 5 days
- **Feedback**: Initial implementation used `setTimeout`. Reviewer
  preferred `requestAnimationFrame` for smoother UX. Also needed
  Storybook story (missed this requirement).
- **Lesson**: Always add Storybook stories for component changes.
  Check existing components for animation patterns before using
  setTimeout.

## Trends
- Reviews typically take 2-5 business days
- Code quality feedback is constructive and specific
- Missing docs/stories is the most common revision request
```

---

## Why This Skill Needs Memory

### Without Memory
Each contribution starts from scratch:
1. Re-read CONTRIBUTING.md
2. Re-discover commit format by reading git log
3. Re-examine linter and CI configuration
4. Risk repeating mistakes from past reviewer feedback
5. No awareness of maintainer preferences

### With Memory
Contributions are faster and higher quality:
1. Conventions pre-loaded — start coding immediately
2. Commit format known — no guessing
3. Reviewer preferences remembered — fewer revision rounds
4. Past mistakes not repeated — lessons applied automatically
5. Relationship context maintained — appropriate communication style

---

## Memory Growth Pattern

### First Contribution to a Project
1. **project_conventions.md**: Created with comprehensive analysis of CONTRIBUTING.md, linter configs, CI pipeline, and PR templates
2. **contribution_history.md**: Created with first contribution entry

### Subsequent Contributions
1. **project_conventions.md**: Updated with newly discovered conventions, corrected misunderstandings, noted changes in project tooling
2. **contribution_history.md**: New entry appended with outcome and lessons learned

### Memory Maintenance
- **Keep concise**: Summarize conventions, don't copy entire config files
- **Update on change**: If a project updates its contribution guidelines, refresh conventions
- **Archive old history**: If contribution_history.md exceeds ~500 lines, summarize older entries
- **Remove stale projects**: If no contribution in 12+ months, conventions may be outdated — flag for re-analysis

---

## Related Documentation

- **Skill Workflow**: `../../skills/open-source-contributions/SKILL.md`
- **Memory Lifecycle**: `../lifecycle.md`
- **Memory Quality Guidance**: `../quality_guidance.md`
- **MemoryStore Interface**: `../../interfaces/memory_store.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-07-14
