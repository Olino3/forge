# Responsive Images Skill — Examples

Usage scenarios demonstrating how `skill:responsive-images` implements performant image loading.

---

## Example 1: Hero Image Optimized for LCP

### Problem

A full-width hero image is the LCP element but loads slowly because it serves a single 3000px image to all devices.

### Before (Unoptimized)

```html
<img src="hero-3000.jpg" alt="Welcome to our store" />
```

### After (Optimized)

```html
<picture>
  <!-- AVIF: 30-50% smaller than WebP -->
  <source
    type="image/avif"
    srcset="
      hero-640.avif   640w,
      hero-960.avif   960w,
      hero-1280.avif 1280w,
      hero-1920.avif 1920w,
      hero-2560.avif 2560w
    "
    sizes="100vw"
  />
  <!-- WebP: 25-35% smaller than JPEG -->
  <source
    type="image/webp"
    srcset="
      hero-640.webp   640w,
      hero-960.webp   960w,
      hero-1280.webp 1280w,
      hero-1920.webp 1920w,
      hero-2560.webp 2560w
    "
    sizes="100vw"
  />
  <!-- JPEG fallback -->
  <img
    src="hero-1280.jpg"
    srcset="
      hero-640.jpg   640w,
      hero-960.jpg   960w,
      hero-1280.jpg 1280w,
      hero-1920.jpg 1920w,
      hero-2560.jpg 2560w
    "
    sizes="100vw"
    alt="Welcome to our store — browse our latest collection"
    width="2560"
    height="1440"
    fetchpriority="high"
    decoding="async"
  />
</picture>
```

```css
.hero {
  aspect-ratio: 16 / 9;
  width: 100%;
}
.hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

**Key points:**
- `fetchpriority="high"` tells the browser this is the most important image
- No `loading="lazy"` — LCP images must load eagerly
- `width`/`height` + `aspect-ratio` prevent CLS
- Format fallback: AVIF → WebP → JPEG
- 5 breakpoints cover mobile through 2x retina desktop

---

## Example 2: Product Card Images in a Grid

### Problem

Product images in a 3-column grid always download the full-size image, wasting bandwidth on mobile where the grid is 1-column.

### Before (Unoptimized)

```html
<div class="product-grid">
  <img src="product-large.jpg" alt="Blue running shoes" />
</div>
```

### After (Optimized)

```html
<div class="product-grid">
  <img
    src="product-400.jpg"
    srcset="
      product-200.jpg  200w,
      product-400.jpg  400w,
      product-600.jpg  600w,
      product-800.jpg  800w
    "
    sizes="
      (min-width: 1024px) 33vw,
      (min-width: 768px) 50vw,
      100vw
    "
    alt="Blue running shoes — lightweight mesh upper, cushioned sole"
    width="800"
    height="800"
    loading="lazy"
    decoding="async"
  />
</div>
```

```css
.product-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
@media (min-width: 768px) {
  .product-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .product-grid { grid-template-columns: repeat(3, 1fr); }
}
.product-grid img {
  aspect-ratio: 1 / 1;
  width: 100%;
  object-fit: cover;
  border-radius: 0.5rem;
}
```

**Key points:**
- `sizes` matches the CSS grid layout: 100vw on mobile, 50vw on tablet, 33vw on desktop
- `loading="lazy"` for below-fold product cards
- `aspect-ratio: 1/1` prevents CLS for square product images
- Browser selects the right image: ~400px on mobile, ~600px on desktop, ~800px on retina

---

## Example 3: Next.js Image Component

### Problem

A Next.js app needs responsive images with automatic optimization, but the developer is using plain `<img>` tags.

### Implementation

```tsx
// components/product-image.tsx
import Image from "next/image"

interface ProductImageProps {
  src: string
  alt: string
  priority?: boolean
}

export function ProductImage({ src, alt, priority = false }: ProductImageProps) {
  return (
    <div className="relative aspect-square overflow-hidden rounded-lg">
      <Image
        src={src}
        alt={alt}
        fill
        sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
        className="object-cover"
        priority={priority}  // Sets fetchpriority="high" and disables lazy loading
      />
    </div>
  )
}
```

```typescript
// next.config.ts — Required for external images
import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "cdn.example.com",
        pathname: "/products/**",
      },
    ],
    formats: ["image/avif", "image/webp"],
  },
}

export default nextConfig
```

**Key points:**
- `next/image` automatically generates srcset and serves AVIF/WebP
- `fill` + parent with `position: relative` for responsive sizing
- `sizes` must still be specified — tells Next.js what widths to generate
- `priority` on LCP images (hero, above-fold product)
- `remotePatterns` required for external image domains

---

## Example 4: Art Direction with Picture Element

### Problem

A marketing banner needs a wide landscape crop on desktop but a square crop focused on the product on mobile.

### Implementation

```html
<picture>
  <!-- Mobile: square crop, product-focused -->
  <source
    media="(max-width: 767px)"
    srcset="banner-mobile-400.avif 400w, banner-mobile-800.avif 800w"
    sizes="100vw"
    type="image/avif"
  />
  <source
    media="(max-width: 767px)"
    srcset="banner-mobile-400.webp 400w, banner-mobile-800.webp 800w"
    sizes="100vw"
    type="image/webp"
  />
  <source
    media="(max-width: 767px)"
    srcset="banner-mobile-400.jpg 400w, banner-mobile-800.jpg 800w"
    sizes="100vw"
  />

  <!-- Desktop: wide landscape -->
  <source
    srcset="banner-desktop-1200.avif 1200w, banner-desktop-1920.avif 1920w"
    sizes="100vw"
    type="image/avif"
  />
  <source
    srcset="banner-desktop-1200.webp 1200w, banner-desktop-1920.webp 1920w"
    sizes="100vw"
    type="image/webp"
  />

  <img
    src="banner-desktop-1200.jpg"
    srcset="banner-desktop-1200.jpg 1200w, banner-desktop-1920.jpg 1920w"
    sizes="100vw"
    alt="Summer sale — up to 50% off running shoes"
    width="1920"
    height="600"
    fetchpriority="high"
  />
</picture>
```

```css
.banner-container {
  width: 100%;
}
/* Mobile: square aspect ratio */
@media (max-width: 767px) {
  .banner-container { aspect-ratio: 1 / 1; }
}
/* Desktop: wide banner */
@media (min-width: 768px) {
  .banner-container { aspect-ratio: 16 / 5; }
}
.banner-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

**Key points:**
- Art direction uses `media` attribute on `<source>` — different crops per breakpoint
- Format negotiation (AVIF → WebP → JPEG) within each breakpoint
- `aspect-ratio` changes per breakpoint to match the crop
- This is the one case where `<picture>` is necessary vs. just `srcset`/`sizes`
