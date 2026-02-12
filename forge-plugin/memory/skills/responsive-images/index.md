# responsive-images Memory

Project-specific memory for image optimization patterns and performance configurations.

## Purpose

This memory helps `skill:responsive-images` remember:
- Image CDN and optimization pipeline
- Breakpoint definitions and sizes attribute values
- Format support decisions (AVIF, WebP, JPEG, PNG)
- Framework image component configuration
- Core Web Vitals image-related metrics

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`
- Framework and image component (next/image, Astro Image, native HTML)
- Image CDN or optimization service (Cloudinary, imgix, Vercel Image Optimization)
- Supported formats and fallback chain
- Responsive breakpoints from the design system
- LCP image identification and fetchpriority strategy

#### `common_patterns.md`
- Standard srcset breakpoints used across the project
- sizes attribute templates for common layouts (full-width, grid, sidebar)
- Art direction patterns for different content types
- Lazy loading boundary (which images are above/below fold)
- CLS prevention approach (aspect-ratio, width/height, placeholder)

## Related Documentation

- **Skill**: `../../skills/responsive-images/SKILL.md`
- **Memory System**: `../index.md`
