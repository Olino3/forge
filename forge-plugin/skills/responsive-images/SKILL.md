---
name: responsive-images
version: "1.0.0"
description: "Implement performant responsive images with srcset, sizes, lazy loading, and modern formats (WebP, AVIF). Covers aspect-ratio for CLS prevention, picture element for art direction, and fetchpriority."
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
      usage: "reference"
## tags: [images, responsive, srcset, sizes, lazy-loading, webp, avif, picture, fetchpriority, cls, performance]

# skill:responsive-images - Performant Responsive Images

## Version: 1.0.0

## Purpose

Implement performant responsive images that load the right size and format for every device. This skill covers `srcset`/`sizes` attributes, modern formats (WebP, AVIF), lazy loading, CLS prevention with `aspect-ratio`, the `<picture>` element for art direction, `fetchpriority` for LCP images, and framework-specific image components (Next.js `Image`, Astro `Image`). Use when adding images to any web project, optimizing existing images for performance, or fixing Core Web Vitals (CLS, LCP) issues related to images.

## File Structure

```
skills/responsive-images/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Image Optimization Focus Areas

1. **Resolution Switching**: `srcset` with width descriptors (`w`) and `sizes` attribute for viewport-based selection
2. **Format Selection**: `<picture>` with `<source>` for AVIF → WebP → JPEG/PNG fallback chain
3. **Art Direction**: `<picture>` with `media` queries for different crops at different breakpoints
4. **Lazy Loading**: `loading="lazy"` for below-fold images, `loading="eager"` for LCP images
5. **Fetch Priority**: `fetchpriority="high"` on LCP image, `fetchpriority="low"` on non-critical
6. **CLS Prevention**: Explicit `width`/`height` or `aspect-ratio` CSS to reserve space before load
7. **Decoding**: `decoding="async"` for non-critical images to avoid blocking main thread
8. **Framework Components**: `next/image`, Astro `<Image>`, Nuxt `<NuxtImg>` — automatic optimization

## Common Pitfalls Prevented

1. Missing `width` and `height` attributes causing CLS (Cumulative Layout Shift)
2. Using `loading="lazy"` on the LCP (Largest Contentful Paint) image — slows it down
3. `srcset` without `sizes` — browser defaults to `100vw`, downloading oversized images
4. `sizes="100vw"` on images that are never full-width (sidebar images, cards)
5. Missing AVIF/WebP sources — serving large JPEG/PNG to modern browsers
6. `fetchpriority="high"` on too many images — defeats the purpose
7. Lazy loading images that are in the initial viewport
8. Missing `alt` text on informational images (accessibility violation)
9. Using CSS `background-image` for content images (not accessible, not optimizable)
10. Serving retina images to non-retina screens (wasted bandwidth)

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### Step 1: Initial Analysis

**YOU MUST:**
1. Identify the image context:
   - Hero/banner images (LCP candidates)
   - Content images (articles, products)
   - Thumbnails/avatars
   - Decorative/background images
2. Detect the framework and any image optimization tooling
3. Identify the image source (local files, CMS, CDN, user uploads)
4. Determine target breakpoints from the project's responsive design
5. Ask clarifying questions:
   - What image formats are available?
   - Is there an image CDN (Cloudinary, imgix, Vercel Image Optimization)?
   - What are the Core Web Vitals targets?

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="responsive-images"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("responsive-images", "{project-name}")` to load project patterns
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill context (breakpoints, design system)
3. Review previously documented image patterns, CDN config, and format support

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Implement Responsive Images

**YOU MUST apply these patterns:**

**LCP Hero Image (above-fold, critical):**
```html
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w, hero-1600.jpg 1600w"
  sizes="100vw"
  alt="Descriptive alt text for the hero image"
  width="1600"
  height="900"
  fetchpriority="high"
  decoding="async"
/>
```

**Content Image (below-fold):**
```html
<img
  src="photo-800.jpg"
  srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1200.jpg 1200w"
  sizes="(min-width: 768px) 50vw, 100vw"
  alt="Description of the image content"
  width="1200"
  height="800"
  loading="lazy"
  decoding="async"
/>
```

**Modern Format Chain:**
```html
<picture>
  <source type="image/avif" srcset="photo.avif" />
  <source type="image/webp" srcset="photo.webp" />
  <img src="photo.jpg" alt="Description" width="800" height="600" loading="lazy" />
</picture>
```

**CLS Prevention:**
```css
.image-container {
  aspect-ratio: 16 / 9;
  width: 100%;
  overflow: hidden;
}
.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

**Rules:**
- LCP image: `fetchpriority="high"`, `loading="eager"` (or omit loading), no lazy loading
- Below-fold images: `loading="lazy"`, `decoding="async"`
- Always provide `width` and `height` OR CSS `aspect-ratio`
- `sizes` must reflect the actual rendered width at each breakpoint
- Every `<img>` with content meaning must have descriptive `alt` text
- Decorative images: `alt=""` and `role="presentation"`

**DO NOT use `loading="lazy"` on LCP images**

### Step 5: Generate Output

- Save to `/claudedocs/responsive-images_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include HTML/JSX code, CSS, and any configuration changes

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="responsive-images"`.

Store image conventions, breakpoints used, CDN configuration, format support, and component patterns.

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: Image context and optimization scope identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Responsive images implemented with correct srcset/sizes, lazy loading, and CLS prevention
- [ ] Step 5: Output saved with standard naming convention
- [ ] Step 6: Standard Memory Update pattern followed

## Further Reading

- **Responsive Images MDN**: https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images
- **web.dev Image Optimization**: https://web.dev/fast/#optimize-your-images
- **fetchpriority**: https://web.dev/articles/fetch-priority
- **CLS Debug**: https://web.dev/articles/optimize-cls

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with interface-based architecture |
