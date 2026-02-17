---
name: "icon-design"
description: "Select semantically appropriate icons for websites using Lucide, Heroicons, or Phosphor icon libraries. Covers concept-to-icon mapping, React and HTML integration templates, consistent sizing and styling, and tree-shaking patterns for optimal bundle size."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [icon_mappings.md, library_preferences.md]
    - type: "shared-project"
      usage: "reference"
tags: [icons, lucide, heroicons, phosphor, react, svg, design, ui, tree-shaking]
---

# skill:icon-design - Semantically Appropriate Icon Selection

## Version: 1.0.0

## Purpose

Select semantically appropriate icons for websites and applications using Lucide, Heroicons, or Phosphor icon libraries. This skill maps UI concepts to the best-fitting icons, generates framework-specific integration code (React, Vue, HTML), enforces consistent sizing and styling, and applies tree-shaking patterns for optimal bundle size.

## File Structure

```
skills/icon-design/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather UI concepts and features that need icons
- Identify the target framework (React, Vue, HTML, React Native)
- Determine the preferred icon library (Lucide, Heroicons, Phosphor) or recommend one
- Note any existing icon conventions in the project (size, stroke width, color scheme)
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="icon-design"` and `domain="engineering"`.

- Load `icon_mappings.md` for previously mapped concept-to-icon associations
- Load `library_preferences.md` for project-specific library choices and styling conventions

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Map Concepts to Icons

- For each UI concept, find the semantically best icon from the chosen library
- Provide 2–3 alternative icons per concept for user selection
- Consider cultural and universal meaning (e.g., floppy disk for "save" may not resonate universally)
- Ensure visual consistency across the icon set (matching style weight, fill vs outline)
- Document the rationale for each primary recommendation

### Step 5: Generate Integration Code

- Produce framework-specific code for the selected icons:
  - **React**: Named imports from the library package, JSX component usage
  - **HTML**: SVG references, CDN links, or sprite sheet includes
  - **Vue**: Component imports and template usage
  - **React Native**: Library-specific native component imports
- Include sizing, color, and stroke-width props for consistency
- Generate a shared icon wrapper component if the project uses many icons

### Step 6: Optimize for Production

- Add tree-shaking patterns to ensure only used icons are bundled
- Recommend dynamic imports for large icon sets with code splitting
- For HTML projects, generate SVG sprite sheets to reduce HTTP requests
- Verify that import patterns support dead-code elimination
- Note bundle size impact estimates where possible

### Step 7: Generate Output

- Save output to `/claudedocs/icon-design_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include: icon mapping table, integration code snippets, optimization notes

### Step 8: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="icon-design"`. Store any newly learned patterns, conventions, or project insights.

- Update `icon_mappings.md` with new concept-to-icon associations
- Update `library_preferences.md` with confirmed library choice, sizing, and style settings

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Icon alternatives provided for each concept (Step 4)
- [ ] Framework-specific integration code generated (Step 5)
- [ ] Tree-shaking and optimization patterns included (Step 6)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 8)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-15 | Initial release |
