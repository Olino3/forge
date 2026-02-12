# Color Palette - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during color palette generation sessions. Each project gets its own subdirectory containing brand colors, palette history, format preferences, and accessibility findings discovered during palette generation.

## Directory Structure

```
memory/skills/color-palette/
├── index.md (this file)
└── {project-name}/
    ├── brand_colors.md
    └── palette_history.md
```

## Project Memory Contents

### brand_colors.md
- Brand hex values provided by the user
- HSL breakdowns of each brand color
- Named roles (primary, secondary, accent)
- Color relationships (complementary, analogous, triadic)
- Client or stakeholder color requirements

### palette_history.md
- Generated palettes with timestamps
- Output format used (Tailwind, CSS variables, shadcn/ui, SCSS, JSON)
- Target framework and version
- WCAG contrast audit results and flagged issues
- Adjustments made to fix failing contrast pairs
- User feedback or manual overrides applied

## Why This Skill Needs Memory

Color palette generation benefits from persistent memory because:

1. **Brand consistency** — Projects reuse the same brand colors across sessions. Memory prevents re-entering hex values and ensures the same base colors produce consistent scales.
2. **Format preferences** — A project that uses shadcn/ui today will use shadcn/ui next month. Memory remembers the preferred output format.
3. **Accessibility history** — WCAG contrast issues discovered in one session inform future palette adjustments, avoiding repeated failures.
4. **Iterative refinement** — Palettes evolve. Memory tracks which shades were manually adjusted and why, preserving design intent across sessions.

## Memory Lifecycle

### Creation
Memory is created the FIRST time a palette is generated for a project. The project name is either:
1. Extracted from the repository root directory name
2. Specified by the user
3. Derived from the framework config (e.g., `package.json` name field)

### Updates
Memory is UPDATED every time the skill generates or audits a palette:
- New brand colors are added to the inventory
- Palette variations are appended to history
- Contrast audit results are recorded
- Format preferences are confirmed or updated

### Usage
Memory is READ at the START of every palette generation:
- Recalls established brand colors
- Applies preferred output format automatically
- References past accessibility findings
- Ensures consistency with previously generated palettes

## Memory Growth Pattern

```
Session 1: brand_colors.md created with initial hex values
           palette_history.md created with first palette + WCAG results

Session 2: brand_colors.md updated with secondary color
           palette_history.md appended with new palette variation

Session 3: brand_colors.md unchanged
           palette_history.md appended with dark mode refinements

Session N: Both files grow incrementally — prune old entries
           per memory/lifecycle.md freshness rules
```

## Best Practices

### DO:
- ✅ Update memory after every palette generation
- ✅ Record brand hex values with their named roles
- ✅ Document WCAG contrast failures and fixes
- ✅ Track output format preferences
- ✅ Note manual shade adjustments and reasoning

### DON'T:
- ❌ Store entire generated CSS/config files (link to output instead)
- ❌ Duplicate Tailwind or framework documentation
- ❌ Include user-specific preferences unrelated to the project
- ❌ Store temporary calculation intermediates
- ❌ Leave memory stale (always update after generation)

## Memory vs Context

### Context (`../../context/engineering/`)
- **Universal knowledge**: Applies to ALL projects
- **Framework patterns**: Tailwind config structure, CSS variable conventions
- **Best practices**: WCAG standards, color theory principles
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project
- **Learned preferences**: Discovered during palette generation
- **Evolving**: Changes with each session
- **Dynamic**: Updated by the skill automatically

## Privacy and Security

### DO Store:
- Brand color hex values
- Palette generation parameters
- WCAG audit results
- Format and framework preferences
- Shade adjustment history

### DON'T Store:
- Client credentials or API keys
- User PII
- Proprietary design system specifications (unless essential to palette generation)
- Full generated output files

---

**Memory System Version**: 1.0.0
**Last Updated**: 2026-02-12
**Maintained by**: color-palette skill
