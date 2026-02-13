---
id: "angular/performance_patterns"
domain: angular
title: "Angular Performance Patterns - Quick Reference"
type: pattern
estimatedTokens: 550
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Change Detection"
    estimatedTokens: 53
    keywords: [change, detection, change-detection]
  - name: "Lists & `*ngFor`"
    estimatedTokens: 43
    keywords: [lists, ngfor, trackby]
  - name: "Lazy Loading & Defer"
    estimatedTokens: 30
    keywords: [lazy, loading, defer, lazy-loading]
  - name: "Bundle Size"
    estimatedTokens: 48
    keywords: [bundle, size, bundle]
  - name: "Memory & Leaks"
    estimatedTokens: 39
    keywords: [memory, leaks, memory]
  - name: "Quick Checklist"
    estimatedTokens: 47
    keywords: [quick, checklist]
tags: [angular, performance, change-detection, lazy-loading, bundle-size, trackby]
---

# Angular Performance Patterns - Quick Reference

High-impact performance checks for Angular apps with minimal examples and links.

**Load this file**: When reviewing performance‑sensitive components, large lists, or app startup.

---

## 1. Change Detection {#change-detection}

| Area | Good Practice | Smell to Flag | References |
|------|--------------|---------------|------------|
| Strategy choice | Use `OnPush` for presentational/perf‑critical components | Many complex components using Default CD | [Change Detection](https://angular.io/guide/change-detection) |
| Immutable inputs | Replace arrays/objects instead of mutating | `this.list.push(...)` in OnPush components | [Best Practices](https://angular.io/guide/change-detection-best-practices) |
| Manual CD | Use `ChangeDetectorRef` only when needed | Frequent `detectChanges()` in normal code paths | [ChangeDetectorRef](https://angular.io/api/core/ChangeDetectorRef) |

---

## 2. Lists & `*ngFor` {#trackby}

| Pattern | Good Practice | Smell to Flag | References |
|---------|--------------|---------------|------------|
| `trackBy` | Always use for large or identity‑based lists | `*ngFor` over big collections without `trackBy` | [NgForOf#change-propagation](https://angular.io/api/common/NgForOf#change-propagation) |
| Virtual scrolling | Use CDK Virtual Scroll for very large lists | Rendering thousands of items directly in DOM | [Virtual Scrolling](https://material.angular.io/cdk/scrolling/overview) |

---

## 3. Lazy Loading & Defer {#lazy-loading}

| Technique | What to Check | References |
|-----------|---------------|------------|
| Route‑based lazy loading | Feature modules loaded via `loadChildren` | [Lazy Loading](https://angular.io/guide/lazy-loading-ngmodules) |
| Deferred views (v17+) | Heavy components wrapped in `@defer` syntax | [Defer Loading](https://angular.dev/guide/defer) |

---

## 4. Bundle Size {#bundle}

| Area | Good Practice | Smell to Flag | References |
|------|--------------|---------------|------------|
| Imports | Import from feature modules (e.g. `import { map } from 'rxjs/operators'`) | Wildcard imports (`import * as operators`) | [Optimizing Builds](https://angular.io/guide/optimizing-performance) |
| Analysis | Use stats and bundle analyzers for large apps | No awareness of bundle size / vendor chunk growth | [CLI Build Options](https://angular.io/cli/build) |

---

## 5. Memory & Leaks {#memory}

| Pattern | Good Practice | Smell to Flag | References |
|---------|--------------|---------------|------------|
| Subscriptions | Use `async` pipe or `takeUntil`/`DestroyRef` | Components with many `.subscribe()` and no `ngOnDestroy` | [RxJS in Angular](https://angular.io/guide/rx-library) |
| DOM listeners | Remove listeners in `ngOnDestroy` | `addEventListener` with no corresponding removal | [Lifecycle Hooks](https://angular.io/guide/lifecycle-hooks) |

---

## 6. Quick Checklist

- [ ] OnPush or signals are used where appropriate.
- [ ] Large lists use `trackBy` and virtual scroll when needed.
- [ ] Feature modules/routes are lazy‑loaded when appropriate.
- [ ] No unnecessary wildcard imports that bloat bundles.
- [ ] Subscriptions and event listeners have clear cleanup.

---

**Version**: 0.3.0-alpha (Compact Reference Format)
**Last Updated**: 2025-11-14
**Angular Versions**: 2-18+
