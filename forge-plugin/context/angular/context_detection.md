# Angular Context Detection

This file provides patterns and techniques for detecting the Angular framework version, architecture patterns, state management solutions, and UI libraries used in a project. Use this information to guide which additional context files to load.

---

## Detection Workflow

1. **Check package.json dependencies** (primary detection method)
2. **Analyze file structure** (module system, standalone components)
3. **Examine import statements** in changed files
4. **Review angular.json configuration**
5. **Check tsconfig.json** for TypeScript settings

---

## Angular Version Detection

### Check package.json
```json
{
  "dependencies": {
    "@angular/core": "^17.0.0"  // Version 17
  }
}
```

### Version Indicators in Code

| Version | Key Indicators | Features |
|---------|---------------|----------|
| **2-8** | `@NgModule` everywhere, no `providedIn` | Legacy Angular, NgModules only |
| **9-12** | `providedIn: 'root'` common, Ivy renderer | Tree-shakable providers, better performance |
| **13-14** | Standalone components optional, modern imports | Simplified module system |
| **15** | Standalone components stable, directive composition | More standalone adoption |
| **16** | Signals introduced (`signal()`, `computed()`, `effect()`) | Reactive primitives |
| **17-18** | Signals mature, standalone default, control flow syntax | Modern Angular, `@if`, `@for` syntax |

### Detection Patterns

**Signals Usage (Angular 16+)**:
```typescript
import { signal, computed, effect } from '@angular/core';

export class Component {
  count = signal(0);
  doubled = computed(() => this.count() * 2);
}
```

**Control Flow Syntax (Angular 17+)**:
```html
@if (condition) {
  <div>New syntax</div>
}

@for (item of items; track item.id) {
  <div>{{ item.name }}</div>
}
```

**Standalone Components (Angular 14+)**:
```typescript
@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  selector: 'app-my-component',
  templateUrl: './my-component.component.html'
})
export class MyComponent {}
```

---

## Module System Detection

### NgModules (Traditional)
**Indicators**:
- `app.module.ts` file exists
- `@NgModule` decorators throughout codebase
- `imports`, `declarations`, `providers` arrays in modules

```typescript
@NgModule({
  declarations: [AppComponent, UserComponent],
  imports: [BrowserModule, HttpClientModule],
  providers: [UserService],
  bootstrap: [AppComponent]
})
export class AppModule {}
```

**Action**: Load context about module organization and lazy loading patterns.

### Standalone Components
**Indicators**:
- `standalone: true` in `@Component` decorators
- `imports` array directly in components
- No `app.module.ts` or minimal module usage

```typescript
@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  // ...
})
```

**Action**: Focus on component-level imports and dependency management.

---

## State Management Detection

### NgRx

**Detection in package.json**:
```json
{
  "dependencies": {
    "@ngrx/store": "^17.0.0",
    "@ngrx/effects": "^17.0.0",
    "@ngrx/entity": "^17.0.0",
    "@ngrx/store-devtools": "^17.0.0"
  }
}
```

**File Structure Indicators**:
```
src/app/state/
├── actions/
│   └── user.actions.ts
├── reducers/
│   └── user.reducer.ts
├── effects/
│   └── user.effects.ts
└── selectors/
    └── user.selectors.ts
```

**Code Indicators**:
```typescript
import { Store } from '@ngrx/store';
import { createAction, props } from '@ngrx/store';
import { createReducer, on } from '@ngrx/store';
import { createEffect, Actions } from '@ngrx/effects';
import { createSelector } from '@ngrx/store';
```

**Action**: Load `ngrx_patterns.md` for state management review.

### Akita

**Detection in package.json**:
```json
{
  "dependencies": {
    "@datorama/akita": "^7.0.0"
  }
}
```

**Code Indicators**:
```typescript
import { Store, StoreConfig } from '@datorama/akita';
import { Query } from '@datorama/akita';
import { EntityStore, EntityState } from '@datorama/akita';
```

**Action**: Load `ngrx_patterns.md` (similar patterns apply).

### Component State Only (No Global State Management)
**Indicators**:
- No NgRx or Akita dependencies
- State managed via services with BehaviorSubject
- Component-level state only

**Action**: Focus on service patterns and RxJS observable management.

---

## RxJS Version Detection

**Check package.json**:
```json
{
  "dependencies": {
    "rxjs": "^7.8.0"  // RxJS 7
  }
}
```

| Version | Key Changes | Migration Concerns |
|---------|-------------|-------------------|
| **6** | Pipeable operators, `pipe()` syntax | Legacy projects may use this |
| **7** | Smaller bundle, `toPromise()` deprecated | Modern projects |
| **8** (future) | Further optimizations | Cutting edge |

**Code Indicators**:
```typescript
// Modern RxJS (v6+)
import { map, filter, switchMap } from 'rxjs/operators';
observable$.pipe(
  map(x => x * 2),
  filter(x => x > 10)
);

// Legacy RxJS (v5)
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
observable.map(x => x * 2); // Deprecated
```

**Action**: Always load `rxjs_patterns.md` - RxJS is ubiquitous in Angular.

---

## UI Library Detection

### PrimeNG

**Detection in package.json**:
```json
{
  "dependencies": {
    "primeng": "^17.0.0",
    "primeicons": "^6.0.0"
  }
}
```

**Code Indicators**:
```typescript
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
```

**Template Indicators**:
```html
<p-table [value]="products">
  <ng-template pTemplate="header">
    <!-- ... -->
  </ng-template>
</p-table>

<p-button label="Click Me"></p-button>
<p-dialog [(visible)]="display"></p-dialog>
```

**Action**: Load `primeng_patterns.md` when PrimeNG components are used.

### Angular Material

**Detection in package.json**:
```json
{
  "dependencies": {
    "@angular/material": "^17.0.0",
    "@angular/cdk": "^17.0.0"
  }
}
```

**Code Indicators**:
```typescript
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
```

**Note**: Material-specific patterns not yet in context. Focus on general component patterns.

### Other UI Libraries
- **ng-bootstrap**: `@ng-bootstrap/ng-bootstrap`
- **Ant Design**: `ng-zorro-antd`
- **Clarity**: `@clr/angular`

**Action**: Focus on general component patterns unless library-specific context exists.

---

## CSS Framework Detection

### TailwindCSS

**Detection in package.json**:
```json
{
  "devDependencies": {
    "tailwindcss": "^3.3.0"
  }
}
```

**Config File Indicators**:
- `tailwind.config.js` exists
- `postcss.config.js` references tailwindcss

**Template Indicators**:
```html
<div class="flex items-center justify-between p-4 bg-blue-500 text-white">
  <h1 class="text-2xl font-bold">Title</h1>
</div>
```

**Action**: Load `tailwind_patterns.md` when Tailwind classes are detected.

### Bootstrap

**Detection**:
```json
{
  "dependencies": {
    "bootstrap": "^5.3.0"
  }
}
```

**Template Indicators**:
```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Content</div>
  </div>
</div>
```

### SCSS/SASS
**angular.json indicates**:
```json
{
  "schematics": {
    "@schematics/angular:component": {
      "style": "scss"
    }
  }
}
```

---

## TypeScript Configuration Detection

**Check tsconfig.json**:
```json
{
  "compilerOptions": {
    "strict": true,  // Strict mode enabled
    "strictNullChecks": true,
    "noImplicitAny": true,
    "strictPropertyInitialization": true,
    "target": "ES2022",
    "lib": ["ES2022", "dom"]
  }
}
```

| Setting | Implication | Review Focus |
|---------|-------------|--------------|
| `"strict": true` | All strict checks enabled | Enforce strict patterns, no `any` |
| `"strict": false` | Relaxed type checking | More likely to find type issues |
| `"strictNullChecks": true` | Null/undefined checked | Good - proper null handling |
| `"noImplicitAny": true` | No implicit any types | Good - explicit typing required |
| `"target": "ES2022"` | Modern JavaScript | Can use latest features |

**Action**: Always load `typescript_patterns.md` for TypeScript review.

---

## Testing Framework Detection

### Jasmine + Karma (Angular Default)
```json
{
  "devDependencies": {
    "karma": "^6.4.0",
    "jasmine-core": "^5.0.0"
  }
}
```

### Jest (Alternative)
```json
{
  "devDependencies": {
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }
}
```

---

## Build System Detection

### Angular CLI (Standard)
**Indicators**:
- `angular.json` exists
- Scripts in package.json: `ng build`, `ng serve`, `ng test`

### Nx Monorepo
**Indicators**:
- `nx.json` exists
- `workspace.json` or `project.json` files
- Multiple apps in `apps/` directory

**Detection**:
```json
{
  "devDependencies": {
    "@nrwl/angular": "^17.0.0",
    "nx": "^17.0.0"
  }
}
```

---

## HTTP Client Detection

### HttpClient (Standard)
```typescript
import { HttpClient } from '@angular/common/http';

constructor(private http: HttpClient) {}
```

### HttpClient with Interceptors
```typescript
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './auth.interceptor';

providers: [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
]
```

**Action**: Load `service_patterns.md` and `security_patterns.md` for API review.

---

## Routing Detection

### Standard Angular Router
```typescript
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'users', component: UserListComponent },
  { path: 'users/:id', component: UserDetailComponent }
];
```

### Lazy Loading
```typescript
const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule)
  }
];
```

**Action**: Check for proper guards, lazy loading configuration.

---

## Forms Detection

### Template-Driven Forms
```typescript
import { FormsModule } from '@angular/forms';
```
```html
<form #form="ngForm">
  <input [(ngModel)]="user.name" name="name">
</form>
```

### Reactive Forms (Recommended)
```typescript
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';

this.form = this.fb.group({
  name: ['', Validators.required],
  email: ['', [Validators.required, Validators.email]]
});
```

**Action**: Focus on validation, error handling, security (injection).

---

## Detection Summary Checklist

When starting a review, detect and document:

- [ ] **Angular Version**: [Version] (check package.json)
- [ ] **Module System**: NgModules / Standalone Components / Mixed
- [ ] **Signals**: Used / Not Used (Angular 16+)
- [ ] **State Management**: NgRx / Akita / Service-based / None
- [ ] **RxJS Version**: [Version]
- [ ] **UI Library**: PrimeNG / Material / Bootstrap / Other / None
- [ ] **CSS Framework**: TailwindCSS / Bootstrap / SCSS / Other
- [ ] **TypeScript Strict Mode**: Enabled / Disabled
- [ ] **Testing Framework**: Jasmine/Karma / Jest / Other
- [ ] **Build System**: Angular CLI / Nx / Other
- [ ] **Routing**: Standard / Lazy Loading
- [ ] **Forms**: Reactive / Template-Driven / Both

---

## Context Loading Decision

Based on detection results, load these context files:

| Detection Result | Load Context Files |
|------------------|-------------------|
| **Any Angular** | `common_issues.md`, `rxjs_patterns.md`, `typescript_patterns.md` |
| **Components** | `component_patterns.md`, `performance_patterns.md` |
| **Services** | `service_patterns.md` |
| **NgRx/Akita** | `ngrx_patterns.md` |
| **PrimeNG** | `primeng_patterns.md` |
| **TailwindCSS** | `tailwind_patterns.md` |
| **Auth/Guards/Interceptors** | `security_patterns.md`, `../../security/security_guidelines.md` |
| **Performance-Critical** | `performance_patterns.md` |

---

## Examples

### Example 1: Modern Standalone Angular 17 with NgRx and TailwindCSS
**Detection Results**:
- Angular 17
- Standalone components
- Signals used
- NgRx for state
- TailwindCSS
- TypeScript strict mode

**Load**:
- `common_issues.md`
- `component_patterns.md`
- `rxjs_patterns.md`
- `ngrx_patterns.md`
- `performance_patterns.md` (signals optimization)
- `typescript_patterns.md`
- `tailwind_patterns.md`

### Example 2: Legacy Angular 12 with NgModules
**Detection Results**:
- Angular 12
- NgModules everywhere
- No state management (service-based)
- Bootstrap CSS
- TypeScript non-strict

**Load**:
- `common_issues.md`
- `component_patterns.md`
- `service_patterns.md`
- `rxjs_patterns.md`
- `typescript_patterns.md` (focus on improving type safety)

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-01-14
**Covers**: Angular 2-18+
