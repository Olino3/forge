# Favicon Generation - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during favicon generation sessions. Each project gets its own subdirectory containing brand asset references, generation history, format preferences, and platform-specific findings discovered during favicon creation.

## Directory Structure

```
memory/skills/favicon-gen/
├── index.md (this file)
└── {project-name}/
    ├── brand_assets.md
    └── favicon_history.md
```

## Project Memory Contents

### brand_assets.md
- Source logo file paths and descriptions
- Brand hex values used in favicon generation
- Monogram initials and font preferences
- Shape choices (circle, rounded square, shield)
- Dark mode color variants
- Contrast ratios between text and background colors
- Related color palette references (if color-palette skill was used)

### favicon_history.md
- Generated favicon sets with timestamps
- Generation approach used (logo extraction, monogram, branded shape)
- Sizes and formats produced per session
- HTML meta tag snippets generated
- Web manifest configurations
- Platform-specific adjustments (iOS safe areas, Android adaptive icon masking)
- User feedback or manual refinements applied
- File placement locations within the project

## Why This Skill Needs Memory

Favicon generation benefits from persistent memory because:

1. **Brand asset continuity** — Projects reuse the same logos, initials, and brand colors across sessions. Memory prevents re-specifying source assets and ensures visual consistency when regenerating favicons.
2. **Format and placement preferences** — A project's favicon file structure (e.g., `/public/` vs `/static/` vs root) is consistent. Memory remembers where files were placed.
3. **Platform-specific learnings** — Adjustments made for iOS safe areas, Android adaptive icons, or dark mode variants are project-specific and should persist across sessions.
4. **Iterative refinement** — Favicons evolve with the brand. Memory tracks which approach was used, what simplifications were made to logos, and why — preserving design decisions across sessions.

## Memory Lifecycle

### Creation
Memory is created the FIRST time a favicon is generated for a project. The project name is either:
1. Extracted from the repository root directory name
2. Specified by the user
3. Derived from the framework config (e.g., `package.json` name field)

### Updates
Memory is UPDATED every time the skill generates or modifies favicons:
- New brand assets are added to the inventory
- Favicon generation details are appended to history
- Format preferences are confirmed or updated
- Platform-specific adjustments are recorded

### Usage
Memory is READ at the START of every favicon generation:
- Recalls established brand colors, logos, and initials
- Applies preferred generation approach automatically
- References past platform adjustments
- Ensures consistency with previously generated favicon sets

## Memory Growth Pattern

```
Session 1: brand_assets.md created with logo path and brand color
           favicon_history.md created with first favicon set + HTML snippet

Session 2: brand_assets.md updated with dark mode color variant
           favicon_history.md appended with regenerated set for new brand color

Session 3: brand_assets.md unchanged
           favicon_history.md appended with monogram variant for sub-brand

Session N: Both files grow incrementally — prune old entries
           per memory/lifecycle.md freshness rules
```

## Best Practices

### DO:
- ✅ Update memory after every favicon generation
- ✅ Record source asset paths and brand colors
- ✅ Document generation approach and simplification decisions
- ✅ Track file placement locations within the project
- ✅ Note platform-specific adjustments and reasoning

### DON'T:
- ❌ Store binary image data (reference file paths instead)
- ❌ Duplicate SVG/HTML/manifest specifications (link to output)
- ❌ Include user-specific preferences unrelated to the project
- ❌ Store temporary conversion intermediates
- ❌ Leave memory stale (always update after generation)

## Memory vs Context

### Context (`../../context/engineering/`)
- **Universal knowledge**: Applies to ALL projects
- **Format standards**: ICO structure, SVG favicon best practices, web manifest spec
- **Best practices**: Platform icon requirements, dark mode techniques
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project
- **Learned preferences**: Discovered during favicon generation
- **Evolving**: Changes with each session
- **Dynamic**: Updated by the skill automatically

## Privacy and Security

### DO Store:
- Brand color hex values
- Source asset file paths (relative to project root)
- Generation approach and parameters
- File placement preferences
- Platform adjustment history

### DON'T Store:
- Client credentials or API keys
- User PII
- Full binary image files
- Proprietary logo specifications beyond what's needed for regeneration
- Complete generated output files

---

**Memory System Version**: 1.0.0
**Last Updated**: 2026-02-12
**Maintained by**: favicon-gen skill
