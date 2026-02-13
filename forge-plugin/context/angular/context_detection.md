---
id: "angular/context_detection"
domain: angular
title: "Angular Context Detection - Quick Reference"
type: detection
estimatedTokens: 550
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "What to Look At"
    estimatedTokens: 83
    keywords: [look]
  - name: "Version & Feature Signals"
    estimatedTokens: 57
    keywords: [version, feature, signals]
  - name: "State Management Snapshot"
    estimatedTokens: 47
    keywords: [state, management, snapshot]
  - name: "UI Library & Styling"
    estimatedTokens: 63
    keywords: [library, styling]
  - name: "TypeScript & Tooling"
    estimatedTokens: 12
    keywords: [typescript, tooling]
tags: [angular, detection, version, framework, state-management, ui-library]
---

# Angular Context Detection - Quick Reference

Minimal cues to detect an Angular project's stack so you know which other context files to load.

**Load this file**: First time reviewing a project, or when the stack is unclear.

---

## 1. What to Look At

| Area | Files to Inspect | What You’re Looking For | References |
|------|------------------|-------------------------|------------|
| Framework version | `package.json` | `@angular/core` version range | [Angular Releases](https://angular.io/guide/releases) |
| Build system | `angular.json`, `nx.json` | Angular CLI vs Nx monorepo | [Angular CLI](https://angular.io/cli), [Nx + Angular](https://nx.dev/getting-started/angular) |
| Module system | `app.module.ts`, `*.module.ts`, `standalone: true` | NgModules vs standalone components | [Standalone Components](https://angular.io/guide/standalone-components) |
| State management | `package.json`, `src/app/state/**` | NgRx, Akita, or service-based state | [State Management Overview](https://angular.io/guide/state-management) |
| UI library | `package.json`, templates | PrimeNG, Material, Tailwind, Bootstrap, etc. | [Angular Resources](https://angular.io/resources) |
| TypeScript strictness | `tsconfig*.json` | `strict`, `noImplicitAny`, `strictNullChecks` | [TSConfig Reference](https://www.typescriptlang.org/tsconfig) |

---

## 2. Version & Feature Signals

| Feature in Code | Likely Angular Version | Implication | Reference |
|-----------------|------------------------|------------|-----------|
| Heavy `@NgModule` usage, no `standalone: true` | 2–13 | Classic NgModule architecture | [Architecture](https://angular.io/guide/architecture) |
| `standalone: true` on components/directives | 14+ | Standalone components supported | [Standalone Components](https://angular.io/guide/standalone-components) |
| `signal()`, `computed()`, `effect()` from `@angular/core` | 16+ | Signals used | [Signals Guide](https://angular.io/guide/signals) |
| `@if`, `@for`, `@switch` in templates | 17+ | New control-flow syntax | [Control Flow](https://angular.dev/guide/templates/control-flow) |

---

## 3. State Management Snapshot

| Indicator | Interpretation | What to Load Next | References |
|----------|----------------|--------------------|------------|
| `@ngrx/store`, `@ngrx/effects` in `package.json` | NgRx in use | `ngrx_patterns.md`, `rxjs_patterns.md` | [NgRx Docs](https://ngrx.io/docs) |
| `@datorama/akita` in `package.json` | Akita in use | `ngrx_patterns.md` (conceptually similar patterns) | [Akita Docs](https://akita.dev/) |
| No state libs; services with `BehaviorSubject` | Service-based state | `service_patterns.md`, `rxjs_patterns.md` | [Services](https://angular.io/guide/architecture-services) |

---

## 4. UI Library & Styling

| Library / Framework | How to Spot It | What to Load Next | References |
|---------------------|---------------|--------------------|------------|
| **PrimeNG** | `primeng` dependency, `<p-table>`, `<p-dialog>`, `<p-button>` | `primeng_patterns.md` | [PrimeNG](https://primeng.org/) |
| **Angular Material** | `@angular/material` dependency, `mat-` prefixed components | Use general component patterns | [Material](https://material.angular.io/) |
| **TailwindCSS** | `tailwindcss` devDependency, `tailwind.config.*`, utility classes (`flex`, `items-center`, etc.) | `tailwind_patterns.md` | [Tailwind + Angular](https://tailwindcss.com/docs/guides/angular) |
| **Bootstrap** | `bootstrap` dependency, `container`, `row`, `col-*` classes | General template patterns apply | [Bootstrap](https://getbootstrap.com/docs/) |

---

## 5. TypeScript & Tooling

| Setting / Tool | Detection Clue | Review Focus | References |
|----------------|----------------|-------------|------------|
| `tsconfig.json` (`strict`) | `"strict": true` in `tsconfig.json` | Expect stricter typing, null checks, and more explicit types | [TypeScript Config](https://www.typescriptlang.org/tsconfig) |
