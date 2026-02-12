---
name: color-palette
description: "Generates complete, accessible color palettes from a single brand hex. Creates 11-shade scale (50-950), semantic tokens (background, foreground, card, muted), and dark mode variants. Includes WCAG contrast checking."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [brand_colors.md, palette_history.md]
    - type: "shared-project"
      usage: "reference"
tags: [color, palette, accessibility, wcag, tailwind, css, hsl, design-tokens, dark-mode]
---

# skill:color-palette - Accessible Color Palette Generator

## Version: 1.0.0

## Purpose

Generate complete, accessible color palettes from a single brand hex value. Produces an 11-shade scale (50-950) following Tailwind CSS conventions, semantic design tokens (background, foreground, card, muted, accent, destructive), dark mode variants, and WCAG contrast compliance reports. Use when building design systems, Tailwind configurations, or CSS custom property sheets.

## File Structure

```
skills/color-palette/
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

- Gather the brand hex value(s) from the user
- Determine output format preferences (Tailwind config, CSS variables, SCSS, JSON tokens)
- Identify target frameworks (Tailwind CSS, shadcn/ui, Radix, custom)
- Detect project type and existing color configuration

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="color-palette"` and `domain="engineering"`.

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Generate Shade Scale

1. Parse the input hex to HSL components (hue, saturation, lightness)
2. Generate 11 shades (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950):
   - 50: Very light tint (lightness ~97%)
   - 500: Base color (input hex)
   - 950: Very dark shade (lightness ~5-10%)
   - Interpolate intermediate shades with perceptually uniform spacing
3. Preserve hue consistency — adjust saturation subtly across the scale
4. Validate that each shade is visually distinct from adjacent shades

### Step 5: Generate Semantic Tokens

Map shades to semantic design tokens:
- `--background`: Lightest shade (50 light / 950 dark)
- `--foreground`: Darkest shade (950 light / 50 dark)
- `--card`: Slightly off-white (100 light / 900 dark)
- `--card-foreground`: High contrast text (900 light / 100 dark)
- `--primary`: Brand color (500/600)
- `--primary-foreground`: White or lightest shade for contrast
- `--muted`: Subtle background (200 light / 800 dark)
- `--muted-foreground`: Subdued text (500 light / 400 dark)
- `--accent`: Complementary or analogous color
- `--destructive`: Red-based destructive action color
- `--border`: Subtle border (300 light / 700 dark)
- `--ring`: Focus ring color (primary with opacity)

### Step 6: WCAG Contrast Checking

For every foreground/background token pair:
1. Calculate relative luminance for both colors
2. Compute contrast ratio using WCAG 2.1 formula
3. Report compliance level:
   - **AAA** (≥7:1): Large and normal text pass
   - **AA** (≥4.5:1): Normal text passes
   - **AA Large** (≥3:1): Only large text passes
   - **FAIL** (<3:1): Does not meet accessibility standards
4. Flag any failing pairs and suggest alternatives

### Step 7: Generate Dark Mode Variants

1. Invert the lightness mapping for dark mode
2. Adjust saturation to prevent washed-out colors in dark contexts
3. Ensure dark mode tokens maintain equivalent contrast ratios
4. Generate both light and dark token sets

### Step 8: Generate Output

- Save output to `/claudedocs/color-palette_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Output format options:
  - **Tailwind CSS config** (`tailwind.config.js` / `tailwind.config.ts`)
  - **CSS custom properties** (`:root` and `[data-theme="dark"]`)
  - **SCSS variables and maps**
  - **JSON design tokens** (Style Dictionary format)
  - **shadcn/ui globals.css** format

### Step 9: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="color-palette"`. Store brand colors, generated palettes, and project preferences.

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] 11-shade scale generated with perceptually uniform spacing
- [ ] Semantic tokens mapped for both light and dark modes
- [ ] WCAG contrast ratios calculated for all foreground/background pairs
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 9)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — 11-shade scale, semantic tokens, WCAG checking, dark mode |
