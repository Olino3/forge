# Color Palette Examples

This file contains example scenarios demonstrating how to use the color-palette skill to generate accessible color palettes, design tokens, and WCAG compliance reports from brand hex values.

---

## Example 1: Tailwind CSS Palette from Brand Blue

### Scenario
A developer is building a SaaS dashboard with Tailwind CSS and needs a complete blue color scale derived from their brand color `#2563eb`.

### User Prompt
```
Generate a Tailwind CSS color palette from my brand blue #2563eb
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Brand hex: `#2563eb`
- Output format: Tailwind CSS config
- Framework: Tailwind CSS v3
- HSL breakdown: `hsl(217, 83%, 53%)`

**Step 2 - Load Memory**:
No prior palette history found for this project. Fresh generation.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Generate Shade Scale**:
Parse `#2563eb` → HSL(217°, 83%, 53%). Generate 11 shades:

```
brand: {
  50:  '#eff4ff',  // hsl(217, 100%, 97%)
  100: '#dbe6fe',  // hsl(217, 95%, 93%)
  200: '#bfd3fe',  // hsl(217, 93%, 87%)
  300: '#93b4fd',  // hsl(217, 90%, 78%)
  400: '#6090fa',  // hsl(217, 88%, 68%)
  500: '#2563eb',  // hsl(217, 83%, 53%) ← base
  600: '#1d4ed8',  // hsl(217, 78%, 48%)
  700: '#1e40af',  // hsl(217, 72%, 40%)
  800: '#1e3a8a',  // hsl(217, 65%, 33%)
  900: '#1a2f6b',  // hsl(217, 60%, 26%)
  950: '#111d45',  // hsl(217, 58%, 17%)
}
```

**Step 5 - Generate Semantic Tokens**:
Mapped to Tailwind theme extension with primary, secondary, and accent roles.

**Step 6 - WCAG Contrast Checking**:

| Pair | Foreground | Background | Ratio | Level |
|------|-----------|------------|-------|-------|
| Primary on white | #2563eb | #ffffff | 4.56:1 | ✅ AA |
| 50 on 950 | #eff4ff | #111d45 | 14.2:1 | ✅ AAA |
| 900 on 50 | #1a2f6b | #eff4ff | 11.8:1 | ✅ AAA |
| White on 500 | #ffffff | #2563eb | 4.56:1 | ✅ AA |
| 300 on 800 | #93b4fd | #1e3a8a | 5.1:1 | ✅ AA |

All pairs meet AA or higher.

**Step 7 - Generate Dark Mode Variants**:
Dark mode inverts the lightness mapping. 950 becomes the background, 50 becomes foreground.

**Step 8 - Generate Output**:
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#eff4ff',
          100: '#dbe6fe',
          200: '#bfd3fe',
          300: '#93b4fd',
          400: '#6090fa',
          500: '#2563eb',
          600: '#1d4ed8',
          700: '#1e40af',
          800: '#1e3a8a',
          900: '#1a2f6b',
          950: '#111d45',
        },
      },
    },
  },
};
```

Saved to `/claudedocs/color-palette_saas-dashboard_2026-02-12.md`.

**Step 9 - Update Memory**:
- ✅ Brand color `#2563eb` stored in `brand_colors.md`
- ✅ Palette generation recorded in `palette_history.md`
- ✅ Tailwind format preference noted

---

## Example 2: shadcn/ui Design Tokens from Brand Green

### Scenario
A developer using Next.js with shadcn/ui needs semantic design tokens derived from their brand green `#16a34a`. They need both light and dark mode CSS custom properties in the shadcn/ui `globals.css` format.

### User Prompt
```
Create shadcn/ui design tokens from #16a34a for my Next.js app, include dark mode
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Brand hex: `#16a34a`
- Output format: shadcn/ui globals.css (CSS custom properties in HSL)
- Framework: shadcn/ui + Next.js
- HSL breakdown: `hsl(142, 76%, 36%)`

**Step 2 - Load Memory**:
No prior palette history found. Fresh generation.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Generate Shade Scale**:
Parse `#16a34a` → HSL(142°, 76%, 36%). Generate 11 shades:

```
green: {
  50:  '#f0fdf4',  // hsl(142, 76%, 97%)
  100: '#dcfce7',  // hsl(142, 71%, 93%)
  200: '#bbf7d0',  // hsl(142, 69%, 85%)
  300: '#86efac',  // hsl(142, 68%, 73%)
  400: '#4ade80',  // hsl(142, 69%, 58%)
  500: '#16a34a',  // hsl(142, 76%, 36%) ← base
  600: '#15803d',  // hsl(142, 72%, 30%)
  700: '#166534',  // hsl(142, 64%, 24%)
  800: '#14532d',  // hsl(142, 61%, 20%)
  900: '#0f3d21',  // hsl(142, 61%, 15%)
  950: '#082614',  // hsl(142, 55%, 9%)
}
```

**Step 5 - Generate Semantic Tokens**:
Map to shadcn/ui token structure using HSL values:

```css
@layer base {
  :root {
    --background: 142 76% 97%;
    --foreground: 142 55% 9%;
    --card: 142 71% 93%;
    --card-foreground: 142 61% 15%;
    --popover: 142 76% 97%;
    --popover-foreground: 142 55% 9%;
    --primary: 142 76% 36%;
    --primary-foreground: 0 0% 100%;
    --secondary: 142 69% 85%;
    --secondary-foreground: 142 64% 24%;
    --muted: 142 71% 93%;
    --muted-foreground: 142 69% 58%;
    --accent: 142 69% 85%;
    --accent-foreground: 142 64% 24%;
    --destructive: 0 84% 60%;
    --destructive-foreground: 0 0% 100%;
    --border: 142 69% 85%;
    --input: 142 69% 85%;
    --ring: 142 76% 36%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 142 55% 9%;
    --foreground: 142 76% 97%;
    --card: 142 61% 15%;
    --card-foreground: 142 71% 93%;
    --popover: 142 61% 15%;
    --popover-foreground: 142 76% 97%;
    --primary: 142 69% 58%;
    --primary-foreground: 142 55% 9%;
    --secondary: 142 64% 24%;
    --secondary-foreground: 142 71% 93%;
    --muted: 142 61% 20%;
    --muted-foreground: 142 69% 73%;
    --accent: 142 61% 20%;
    --accent-foreground: 142 71% 93%;
    --destructive: 0 62% 50%;
    --destructive-foreground: 0 0% 100%;
    --border: 142 64% 24%;
    --input: 142 64% 24%;
    --ring: 142 69% 58%;
  }
}
```

**Step 6 - WCAG Contrast Checking**:

| Pair | Foreground | Background | Ratio | Level |
|------|-----------|------------|-------|-------|
| foreground on background (light) | #082614 | #f0fdf4 | 15.8:1 | ✅ AAA |
| primary on primary-foreground | #16a34a | #ffffff | 4.58:1 | ✅ AA |
| card-foreground on card | #0f3d21 | #dcfce7 | 11.4:1 | ✅ AAA |
| muted-foreground on muted | #4ade80 | #dcfce7 | 1.8:1 | ❌ FAIL |
| foreground on background (dark) | #f0fdf4 | #082614 | 15.8:1 | ✅ AAA |

⚠️ **Issue detected**: `muted-foreground` on `muted` in light mode fails contrast. Recommend darkening muted-foreground to shade 600 (`#15803d`, ratio 5.2:1, AA pass).

**Step 7 - Generate Dark Mode Variants**:
Dark mode tokens generated and included in the CSS output above. Lightness values are inverted. Saturation reduced slightly in dark mode to prevent neon glow effect.

**Step 8 - Generate Output**:
Saved to `/claudedocs/color-palette_nextjs-app_2026-02-12.md`.
Output includes the full `globals.css` snippet ready to paste into the project.

**Step 9 - Update Memory**:
- ✅ Brand color `#16a34a` stored in `brand_colors.md`
- ✅ shadcn/ui format preference recorded
- ✅ Contrast issue and fix documented in `palette_history.md`

---

## Example 3: Full WCAG Audit for Brand Purple

### Scenario
A design system team needs a comprehensive accessibility audit for their brand purple `#7c3aed`. They want every shade tested against every other shade with full WCAG 2.1 compliance reporting.

### User Prompt
```
Run a full WCAG contrast audit on #7c3aed — I need to know every safe text/background combination
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Brand hex: `#7c3aed`
- Output format: WCAG accessibility report (comprehensive)
- Focus: Contrast ratio matrix, safe pair identification
- HSL breakdown: `hsl(263, 83%, 58%)`

**Step 2 - Load Memory**:
No prior palette history found. Fresh generation.

**Step 3 - Load Context**:
Loaded engineering domain context. File budget: 4 files.

**Step 4 - Generate Shade Scale**:
Parse `#7c3aed` → HSL(263°, 83%, 58%). Generate 11 shades:

```
purple: {
  50:  '#faf5ff',  // hsl(263, 100%, 98%)
  100: '#f3e8ff',  // hsl(263, 95%, 95%)
  200: '#e9d5ff',  // hsl(263, 90%, 92%)
  300: '#d8b4fe',  // hsl(263, 90%, 85%)
  400: '#c084fc',  // hsl(263, 90%, 75%)
  500: '#7c3aed',  // hsl(263, 83%, 58%) ← base
  600: '#6d28d9',  // hsl(263, 70%, 50%)
  700: '#5b21b6',  // hsl(263, 70%, 42%)
  800: '#4c1d95',  // hsl(263, 68%, 35%)
  900: '#3b1578',  // hsl(263, 68%, 28%)
  950: '#240d4a',  // hsl(263, 68%, 17%)
}
```

**Step 5 - Generate Semantic Tokens**:
Tokens generated for both light and dark modes using the purple scale.

**Step 6 - WCAG Contrast Checking**:

Full contrast matrix (selected pairs):

| Text Color | Background | Ratio | AA Normal | AA Large | AAA |
|-----------|------------|-------|-----------|----------|-----|
| 950 on 50 | #240d4a / #faf5ff | 16.4:1 | ✅ | ✅ | ✅ |
| 900 on 50 | #3b1578 / #faf5ff | 13.7:1 | ✅ | ✅ | ✅ |
| 900 on 100 | #3b1578 / #f3e8ff | 12.1:1 | ✅ | ✅ | ✅ |
| 800 on 50 | #4c1d95 / #faf5ff | 10.5:1 | ✅ | ✅ | ✅ |
| 800 on 100 | #4c1d95 / #f3e8ff | 9.3:1 | ✅ | ✅ | ✅ |
| 800 on 200 | #4c1d95 / #e9d5ff | 7.2:1 | ✅ | ✅ | ✅ |
| 700 on 50 | #5b21b6 / #faf5ff | 8.1:1 | ✅ | ✅ | ✅ |
| 700 on 100 | #5b21b6 / #f3e8ff | 7.1:1 | ✅ | ✅ | ✅ |
| 700 on 200 | #5b21b6 / #e9d5ff | 5.5:1 | ✅ | ✅ | ❌ |
| 600 on 50 | #6d28d9 / #faf5ff | 6.3:1 | ✅ | ✅ | ❌ |
| 600 on 100 | #6d28d9 / #f3e8ff | 5.5:1 | ✅ | ✅ | ❌ |
| 500 on 50 | #7c3aed / #faf5ff | 4.6:1 | ✅ | ✅ | ❌ |
| 500 on 100 | #7c3aed / #f3e8ff | 4.1:1 | ❌ | ✅ | ❌ |
| 500 on white | #7c3aed / #ffffff | 4.8:1 | ✅ | ✅ | ❌ |
| 400 on 50 | #c084fc / #faf5ff | 2.1:1 | ❌ | ❌ | ❌ |
| 400 on 900 | #c084fc / #3b1578 | 5.8:1 | ✅ | ✅ | ❌ |
| 50 on 700 | #faf5ff / #5b21b6 | 8.1:1 | ✅ | ✅ | ✅ |
| 50 on 800 | #faf5ff / #4c1d95 | 10.5:1 | ✅ | ✅ | ✅ |
| 50 on 950 | #faf5ff / #240d4a | 16.4:1 | ✅ | ✅ | ✅ |
| 100 on 800 | #f3e8ff / #4c1d95 | 9.3:1 | ✅ | ✅ | ✅ |
| 200 on 900 | #e9d5ff / #3b1578 | 8.3:1 | ✅ | ✅ | ✅ |
| 300 on 900 | #d8b4fe / #3b1578 | 5.9:1 | ✅ | ✅ | ❌ |

### Safe Pair Summary

**For normal body text (AA ≥ 4.5:1)**:
- ✅ Shades 700–950 on backgrounds 50–200
- ✅ Shades 50–200 on backgrounds 700–950
- ✅ Shade 500 on white or shade 50
- ✅ Shade 600 on shades 50–100

**For large text only (AA Large ≥ 3:1)**:
- ⚠️ Shade 500 on shade 100
- ⚠️ Shade 400 on shades 800–900

**Avoid entirely (FAIL < 3:1)**:
- ❌ Shade 400 on shades 50–300 (insufficient contrast)
- ❌ Adjacent shades (e.g., 300 on 400, 500 on 600)
- ❌ Mid-range shades on mid-range backgrounds

**Step 7 - Generate Dark Mode Variants**:
Dark mode variants generated with inverted lightness. All dark mode pairs re-validated against WCAG thresholds.

**Step 8 - Generate Output**:
Saved to `/claudedocs/color-palette_design-system_2026-02-12.md`.
Report includes:
- Full 11-shade scale with hex and HSL values
- Complete contrast ratio matrix
- Safe pair quick-reference card
- Failing pair warnings with recommended alternatives
- Dark mode token set with independent contrast validation

**Step 9 - Update Memory**:
- ✅ Brand color `#7c3aed` stored in `brand_colors.md`
- ✅ Accessibility audit results recorded in `palette_history.md`
- ✅ Safe/unsafe pair data stored for future reference
