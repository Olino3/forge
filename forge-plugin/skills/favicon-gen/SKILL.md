---
name: favicon-gen
description: "Generate custom favicons from logos, text, or brand colors — prevents launching with CMS defaults. Extract icons from logos, create monogram favicons from initials, or use branded shapes. Outputs all required formats (ICO, PNG, SVG, Apple Touch, web manifest)."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [brand_assets.md, favicon_history.md]
    - type: "shared-project"
      usage: "reference"
## tags: [favicon, icon, branding, svg, png, ico, apple-touch, web-manifest, monogram]

# skill:favicon-gen - Custom Favicon Generator

## Version: 1.0.0

## Purpose

Generate custom favicons from logos, text/initials, or brand colors. Prevents launching with CMS defaults by producing a complete favicon set covering all platforms and devices. Supports three approaches: extracting icons from existing logos, creating monogram favicons from brand initials, or generating geometric shape favicons from brand colors. Outputs all required formats — favicon.ico (16/32/48), favicon.svg, apple-touch-icon.png (180×180), android-chrome icons (192/512), PNG fallbacks, and the web manifest JSON.

## File Structure

```
skills/favicon-gen/
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

- Gather the favicon source from the user:
  - **Logo file**: SVG or high-res PNG to extract/simplify into an icon
  - **Text/initials**: Letters for a monogram favicon (e.g., "AB", "F")
  - **Brand colors**: Hex values for generating geometric shape icons
- Determine size requirements (standard set or custom sizes)
- Identify format preferences (all formats by default)
- Detect project type and existing favicon configuration

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="favicon-gen"` and `domain="engineering"`.

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Determine Favicon Strategy

Based on the source input, select the generation approach:

1. **Logo extraction** — Simplify an existing logo SVG for small sizes, remove fine details that break at 16×16, ensure the icon reads clearly at every target size
2. **Monogram generation** — Render initials using a bold, legible font on a branded background, ensure letterforms are crisp at 16×16 and 32×32
3. **Branded shape** — Create a geometric shape (circle, rounded square, shield) filled with the brand color, optionally with an embedded initial or symbol

For all approaches:
- Define the primary color and background color
- Choose a shape mask (square, rounded square, circle) for platform-specific variants
- Plan the SVG source that will serve as the master from which all raster sizes are derived

### Step 5: Generate Favicon Assets

Produce the complete favicon set from the master SVG:

| File | Size | Purpose |
|------|------|---------|
| `favicon.ico` | 16×16, 32×32, 48×48 | Legacy browser fallback (multi-size ICO) |
| `favicon.svg` | Scalable | Modern browsers, supports dark mode via `prefers-color-scheme` |
| `favicon-16x16.png` | 16×16 | PNG fallback for older browsers |
| `favicon-32x32.png` | 32×32 | Standard browser tab icon |
| `apple-touch-icon.png` | 180×180 | iOS home screen bookmark |
| `android-chrome-192x192.png` | 192×192 | Android home screen icon |
| `android-chrome-512x512.png` | 512×512 | Android splash screen / PWA install |

For the SVG favicon:
- Use `prefers-color-scheme` media query for automatic dark mode adaptation
- Keep the SVG minimal — no embedded fonts, no external references
- Ensure crisp rendering at small sizes with pixel-aligned paths

### Step 6: Generate HTML Meta Tags

Produce the complete `<head>` snippet for all icon references:

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

Generate the `site.webmanifest` file:

```json
{
  "name": "{Project Name}",
  "short_name": "{Short Name}",
  "icons": [
    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "{brand-hex}",
  "background_color": "{background-hex}",
  "display": "standalone"
}
```

### Step 7: Generate Output

- Save output to `/claudedocs/favicon-gen_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Output includes:
  - Master SVG source code
  - Instructions or scripts for generating raster formats from the SVG
  - Complete HTML `<head>` snippet
  - `site.webmanifest` contents
  - File placement guide (where each file goes in the project)

### Step 8: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="favicon-gen"`. Store brand assets, generation approach, and project preferences.

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Favicon strategy determined and documented (Step 4)
- [ ] All required favicon formats generated (Step 5)
- [ ] HTML meta tags and web manifest produced (Step 6)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 8)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — logo extraction, monogram generation, branded shapes, full format output |
