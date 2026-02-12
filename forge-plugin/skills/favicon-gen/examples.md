# Favicon Generation Examples

This file contains example scenarios demonstrating how to use the favicon-gen skill to generate complete favicon sets from logos, text initials, or brand colors.

---

## Example 1: Extracting a Favicon from a Company Logo SVG

### Scenario
A startup has an existing logo SVG (`logo.svg`) that is detailed and works well at large sizes but needs a simplified favicon version for browser tabs and bookmarks.

### User Prompt
```
Generate a complete favicon set from our company logo at ./assets/logo.svg
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Source: Existing SVG logo at `./assets/logo.svg`
- Approach: Logo extraction — simplify for small sizes
- Format: All standard formats (ICO, SVG, PNG, Apple Touch, Android Chrome)
- Logo inspection: Complex paths, thin strokes, text elements that won't render at 16×16

**Step 2 - Load Memory**:
No prior favicon history found for this project. Fresh generation.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Determine Favicon Strategy**:
Logo extraction approach selected:
- Remove the wordmark — keep only the logomark (icon portion)
- Simplify thin strokes into filled shapes for clarity at small sizes
- Remove gradients — use flat brand color for 16×16 legibility
- Add a transparent background for flexibility across light/dark browser themes

**Step 5 - Generate Favicon Assets**:
Master SVG created by simplifying the logomark:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <path d="M6 4h20a2 2 0 0 1 2 2v20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="#2563eb"/>
  <path d="M10 16l4 4 8-8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <style>
    @media (prefers-color-scheme: dark) {
      path:first-child { fill: #60a5fa; }
    }
  </style>
</svg>
```

Generated files:

| File | Size | Notes |
|------|------|-------|
| `favicon.ico` | 16×16, 32×32, 48×48 | Multi-size ICO from simplified logomark |
| `favicon.svg` | Scalable | Dark mode support via `prefers-color-scheme` |
| `favicon-16x16.png` | 16×16 | Pixel-aligned, no fine details |
| `favicon-32x32.png` | 32×32 | Slightly more detail than 16×16 |
| `apple-touch-icon.png` | 180×180 | Logomark centered with padding on brand-color background |
| `android-chrome-192x192.png` | 192×192 | Full logomark, solid background |
| `android-chrome-512x512.png` | 512×512 | High-res for PWA splash |

**Step 6 - Generate HTML Meta Tags**:
```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

`site.webmanifest`:
```json
{
  "name": "Acme Corp",
  "short_name": "Acme",
  "icons": [
    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#2563eb",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

**Step 7 - Generate Output**:
Saved to `/claudedocs/favicon-gen_acme-corp_2026-02-12.md`.
Includes master SVG source, raster generation instructions, HTML snippet, and file placement guide.

**Step 8 - Update Memory**:
- ✅ Logo source path stored in `brand_assets.md`
- ✅ Simplified logomark SVG recorded for future regeneration
- ✅ Brand color `#2563eb` noted in `brand_assets.md`
- ✅ Generation details recorded in `favicon_history.md`

---

## Example 2: Creating a Monogram Favicon from Brand Initials

### Scenario
A consulting firm "Anderson & Blake" needs a favicon using their initials "AB" with their brand colors — navy blue (`#1e3a5f`) background and white text.

### User Prompt
```
Create a monogram favicon with the initials "AB" using brand color #1e3a5f on a rounded square
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Source: Text initials "AB"
- Brand color: `#1e3a5f` (navy blue)
- Text color: White (`#ffffff`)
- Shape: Rounded square
- Approach: Monogram generation
- Format: All standard formats

**Step 2 - Load Memory**:
No prior favicon history found. Fresh generation.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Determine Favicon Strategy**:
Monogram generation approach selected:
- Use a bold sans-serif font weight for legibility at small sizes
- "AB" letterforms — "A" is wide, "B" has fine counters; both need careful sizing
- At 16×16, two letters risk illegibility — consider using just "A" for the smallest size or tightening letter spacing
- Rounded square background with 20% corner radius
- White text on navy background ensures strong contrast

**Step 5 - Generate Favicon Assets**:
Master SVG for the monogram:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="102" fill="#1e3a5f"/>
  <text x="256" y="340" font-family="system-ui, -apple-system, sans-serif"
        font-size="280" font-weight="700" fill="#ffffff"
        text-anchor="middle" letter-spacing="-15">AB</text>
  <style>
    @media (prefers-color-scheme: dark) {
      rect { fill: #2d5a8e; }
    }
  </style>
</svg>
```

Generated files:

| File | Size | Notes |
|------|------|-------|
| `favicon.ico` | 16×16, 32×32, 48×48 | "AB" monogram, bold weight |
| `favicon.svg` | Scalable | Dark mode adjusts background to lighter navy |
| `favicon-16x16.png` | 16×16 | Tight letter spacing, pixel-hinted |
| `favicon-32x32.png` | 32×32 | Full "AB" with clear counters |
| `apple-touch-icon.png` | 180×180 | Rounded square with padding |
| `android-chrome-192x192.png` | 192×192 | Full monogram on navy |
| `android-chrome-512x512.png` | 512×512 | Crisp at high density |

**Step 6 - Generate HTML Meta Tags**:
```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

`site.webmanifest`:
```json
{
  "name": "Anderson & Blake Consulting",
  "short_name": "A&B",
  "icons": [
    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#1e3a5f",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

**Step 7 - Generate Output**:
Saved to `/claudedocs/favicon-gen_anderson-blake_2026-02-12.md`.
Includes monogram SVG source, rendering notes for small sizes, and complete integration guide.

**Step 8 - Update Memory**:
- ✅ Brand initials "AB" and color `#1e3a5f` stored in `brand_assets.md`
- ✅ Monogram approach and font sizing recorded in `favicon_history.md`
- ✅ Rounded square shape preference noted

---

## Example 3: Generating a Complete Favicon Set from Brand Color with Geometric Shape

### Scenario
An early-stage startup has no logo yet but wants to launch with a professional-looking favicon using their brand color teal (`#0d9488`) and a circle shape containing their initial "F".

### User Prompt
```
Generate a favicon using a circle shape with my brand color #0d9488 and the letter "F" inside
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Source: Brand color `#0d9488` (teal) + letter "F"
- Shape: Circle
- Text color: White (`#ffffff`)
- Approach: Branded shape with embedded initial
- Format: All standard formats

**Step 2 - Load Memory**:
No prior favicon history found. Fresh generation.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Determine Favicon Strategy**:
Branded shape approach selected:
- Circle filled with teal `#0d9488`
- Single letter "F" centered — excellent legibility even at 16×16
- White text on teal gives a contrast ratio of ~4.6:1 (AA pass)
- Circle shape will be masked to rounded square for Android adaptive icons
- SVG master with `prefers-color-scheme` for dark mode (lighter teal variant)

**Step 5 - Generate Favicon Assets**:
Master SVG for the branded shape:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <circle cx="256" cy="256" r="256" fill="#0d9488"/>
  <text x="256" y="340" font-family="system-ui, -apple-system, sans-serif"
        font-size="320" font-weight="700" fill="#ffffff"
        text-anchor="middle">F</text>
  <style>
    @media (prefers-color-scheme: dark) {
      circle { fill: #14b8a6; }
    }
  </style>
</svg>
```

Generated files:

| File | Size | Notes |
|------|------|-------|
| `favicon.ico` | 16×16, 32×32, 48×48 | Circle with "F", pixel-hinted at small sizes |
| `favicon.svg` | Scalable | Dark mode shifts to lighter teal |
| `favicon-16x16.png` | 16×16 | Simplified "F" centered in circle |
| `favicon-32x32.png` | 32×32 | Clean circle edge, bold "F" |
| `apple-touch-icon.png` | 180×180 | Circle on white background with safe-area padding |
| `android-chrome-192x192.png` | 192×192 | Full circle, maskable-safe |
| `android-chrome-512x512.png` | 512×512 | High-res for PWA install |

**Step 6 - Generate HTML Meta Tags**:
```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

`site.webmanifest`:
```json
{
  "name": "Forge Startup",
  "short_name": "Forge",
  "icons": [
    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#0d9488",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

**Step 7 - Generate Output**:
Saved to `/claudedocs/favicon-gen_forge-startup_2026-02-12.md`.
Includes circle SVG source, guidance on Android adaptive icon masking, and full HTML integration.

**Step 8 - Update Memory**:
- ✅ Brand color `#0d9488` and letter "F" stored in `brand_assets.md`
- ✅ Circle shape preference recorded in `favicon_history.md`
- ✅ Contrast ratio (4.6:1 AA) documented for future reference
