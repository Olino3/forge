---
id: "angular/tailwind_patterns"
domain: angular
title: "TailwindCSS with Angular"
type: framework
estimatedTokens: 250
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Configuration"
    estimatedTokens: 30
    keywords: [configuration]
  - name: "Dynamic Classes"
    estimatedTokens: 43
    keywords: [dynamic, classes, dynamic-classes]
  - name: "Responsive Design"
    estimatedTokens: 11
    keywords: [responsive, design]
  - name: "Component Integration"
    estimatedTokens: 18
    keywords: [component, integration, components]
  - name: "PrimeNG Conflicts"
    estimatedTokens: 18
    keywords: [primeng, conflicts, primeng-conflicts]
tags: [angular, tailwindcss, css, responsive, dynamic-classes, primeng-conflicts]
---

# TailwindCSS with Angular

Best practices for integrating TailwindCSS with Angular applications.

---

## Configuration {#configuration}

### tailwind.config.js

```javascript
module.exports = {
  content: [
    './src/**/*.{html,ts}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### PurgeCSS Setup

Ensure unused classes are removed in production:
```javascript
module.exports = {
  content: [
    './src/**/*.{html,ts}',
    './src/**/*.component.html',
  ],
}
```

---

## Dynamic Classes {#dynamic-classes}

### Using [class] Binding

**Bad**:
```html
<div class="text-{{ color }}">Text</div>
<!-- Purged by TailwindCSS! -->
```

**Good**:
```html
<div [class]="'text-' + color">Text</div>

<!-- Or safelist in config -->
<!-- tailwind.config.js -->
module.exports = {
  safelist: ['text-red-500', 'text-blue-500']
}
```

### Using [ngClass]

```html
<div [ngClass]="{
  'bg-blue-500': isActive,
  'bg-gray-300': !isActive,
  'text-white': isActive,
  'text-gray-700': !isActive
}">
  Content
</div>
```

---

## Responsive Design {#responsive}

```html
<div class="
  w-full
  md:w-1/2
  lg:w-1/3
  px-4
  py-2
  sm:py-4
">
  Responsive content
</div>
```

---

## Component Integration {#components}

### Host Classes

```typescript
@Component({
  selector: 'app-card',
  host: {
    'class': 'block p-4 bg-white rounded-lg shadow'
  },
  template: `<ng-content></ng-content>`
})
export class CardComponent {}
```

---

## PrimeNG Conflicts {#primeng-conflicts}

When using both TailwindCSS and PrimeNG:

```scss
// Override PrimeNG with Tailwind
.p-button {
  @apply px-4 py-2 bg-blue-500 text-white rounded;
}
```

---

**Version**: 0.1.0-alpha
