# Example Project Memory Reference

This is an example of how memory files should be structured for an Angular project. Use this as a template when creating memory for new projects.

---

## Note

Actual project memory would have 4 separate files:
1. `project_overview.md`
2. `common_patterns.md`
3. `known_issues.md`
4. `review_history.md`

This single file shows examples of what each should contain.

---

## Example: project_overview.md

```markdown
# Project Overview: E-Commerce Dashboard

## Framework Stack
- **Angular**: 17.2.0
- **TypeScript**: 5.3.0 (strict mode enabled)
- **RxJS**: 7.8.1
- **Node**: 20.x

## UI & Styling
- **UI Library**: PrimeNG 17.3.0
- **CSS Framework**: TailwindCSS 3.4.0
- **Icons**: PrimeIcons + Custom SVGs

## State Management
- **Approach**: NgRx 17.0.0
- **Pattern**: Facade pattern for component access
- **Structure**: Feature-based state slices
- **DevTools**: Redux DevTools enabled in development

## Architecture
- **Type**: Standalone components (no NgModules)
- **Routing**: Lazy-loaded feature routes with preloading
- **Forms**: Reactive forms with custom validators
- **HTTP**: Interceptors for auth, error handling, caching
- **Build**: Angular CLI with custom webpack config

## Project Structure
```
src/app/
├── core/           # Singletons (guards, interceptors, services)
├── shared/         # Reusable components, pipes, directives
├── features/       # Feature modules (lazy-loaded)
│   ├── products/
│   ├── orders/
│   └── customers/
└── state/          # NgRx state (actions, reducers, effects, selectors)
```

## Testing
- **Framework**: Jasmine + Karma
- **Coverage**: 80% minimum enforced
- **E2E**: Cypress

## Code Style & Conventions
- **Linting**: ESLint with Angular rules
- **Formatting**: Prettier
- **Commits**: Conventional commits enforced
- **Pre-commit**: Husky runs lint + tests

## Development Environment
- **IDE**: VS Code (recommended extensions documented)
- **Package Manager**: npm (not yarn or pnpm)
- **Node Version**: Managed via .nvmrc

## Deployment
- **Environment**: Azure (dev, staging, prod)
- **CI/CD**: GitHub Actions
- **Monitoring**: Application Insights

## Team Conventions
- **Change Detection**: OnPush default for all components
- **Subscriptions**: takeUntil pattern required (no manual unsubscribe)
- **State Access**: Always via facades, never direct store access
- **Naming**: Feature-first (e.g., ProductListComponent, OrderService)
- **File Structure**: One component per file, tests co-located
```

---

## Example: common_patterns.md

```markdown
# Common Patterns: E-Commerce Dashboard

## Component Patterns

### Base Component Pattern
All feature components extend BaseComponent for common functionality:

\`\`\`typescript
export abstract class BaseComponent implements OnDestroy {
  protected destroy$ = new Subject<void>();

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
\`\`\`

Usage:
\`\`\`typescript
export class ProductListComponent extends BaseComponent implements OnInit {
  ngOnInit() {
    this.productService.getProducts()
      .pipe(takeUntil(this.destroy$))
      .subscribe(products => this.products = products);
  }
}
\`\`\`

### Loading State Pattern
Components display loading states using a shared pattern:

\`\`\`typescript
// Component
isLoading$ = this.productFacade.loading$;
error$ = this.productFacade.error$;
products$ = this.productFacade.products$;

// Template
<div *ngIf="isLoading$ | async">Loading...</div>
<div *ngIf="error$ | async as error" class="error">{{ error }}</div>
<div *ngIf="products$ | async as products">
  <app-product-card *ngFor="let product of products; trackBy: trackById" [product]="product">
  </app-product-card>
</div>
\`\`\`

### Smart vs Presentational Split
- **Smart (Container)**: Route components in features/ (e.g., ProductListComponent)
- **Presentational (Dumb)**: All in shared/ (e.g., ProductCardComponent)
- **Rule**: Presentational components never inject facades or services (except utils)

## Service Patterns

### API Services
All API services extend BaseApiService<T>:

\`\`\`typescript
@Injectable({ providedIn: 'root' })
export class ProductService extends BaseApiService<Product> {
  constructor(http: HttpClient) {
    super(http, '/api/products');
  }

  // BaseApiService provides: get(), getAll(), create(), update(), delete()
  // Custom methods added here
}
\`\`\`

### Error Handling
All HTTP calls use centralized error handling via ErrorInterceptor.
Components display errors via shared ErrorDisplayComponent.

### Caching Strategy
- GET requests cached for 5 minutes
- Cache invalidated on mutations (POST, PUT, DELETE)
- Implemented in CacheInterceptor

## State Management (NgRx)

### Action Naming
Format: `[Source] Action`
\`\`\`typescript
export const loadProducts = createAction('[Product List] Load Products');
export const loadProductsSuccess = createAction(
  '[Product API] Load Products Success',
  props<{ products: Product[] }>()
);
\`\`\`

### Facade Pattern
Components access state ONLY via facades:
\`\`\`typescript
@Injectable({ providedIn: 'root' })
export class ProductFacade {
  products$ = this.store.select(selectAllProducts);
  loading$ = this.store.select(selectProductsLoading);

  constructor(private store: Store) {}

  loadProducts() {
    this.store.dispatch(loadProducts());
  }
}
\`\`\`

### Entity Adapter
All feature state uses @ngrx/entity adapters for CRUD operations.

## Form Patterns

### Form Setup
\`\`\`typescript
form = this.fb.group({
  name: ['', [Validators.required, Validators.maxLength(100)]],
  email: ['', [Validators.required, Validators.email]],
  phone: ['', [CustomValidators.phone]]
});
\`\`\`

### Custom Validators
Located in `@shared/validators/`:
- `CustomValidators.phone`
- `CustomValidators.strongPassword`
- `CustomValidators.futureDate`

### Error Display
Use `<app-field-error>` component:
\`\`\`html
<input pInputText formControlName="email" />
<app-field-error [control]="form.get('email')"></app-field-error>
\`\`\`

## Routing Patterns

### Lazy Loading
\`\`\`typescript
{
  path: 'products',
  loadChildren: () => import('./features/products/products.routes').then(m => m.PRODUCT_ROUTES)
}
\`\`\`

### Guards
- AuthGuard: Checks authentication
- RoleGuard: Checks authorization
- UnsavedChangesGuard: Prevents navigation with unsaved data

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Component | `{Feature}{Type}Component` | `ProductListComponent` |
| Service | `{Feature}Service` | `ProductService` |
| Facade | `{Feature}Facade` | `ProductFacade` |
| Guard | `{Purpose}Guard` | `AuthGuard` |
| Pipe | `{Purpose}Pipe` | `CurrencyFormatPipe` |
| Directive | `{Purpose}Directive` | `HighlightDirective` |

## File Organization
\`\`\`
product-list/
├── product-list.component.ts
├── product-list.component.html
├── product-list.component.scss
└── product-list.component.spec.ts
\`\`\`

## Path Aliases
- `@app/*` → `src/app/*`
- `@core/*` → `src/app/core/*`
- `@shared/*` → `src/app/shared/*`
- `@features/*` → `src/app/features/*`
- `@state/*` → `src/app/state/*`
```

---

## Example: known_issues.md

```markdown
# Known Issues: E-Commerce Dashboard

## Technical Debt

### 1. Legacy Product Service (Documented - Q1 2025 Refactor)
**Location**: `src/app/core/services/legacy-product.service.ts`
**Issue**: Uses deprecated HttpClient patterns, no type safety
**Reason**: Original service from Angular 8 migration
**Impact**: Works but lacks modern error handling
**Planned**: Complete refactor in Q1 2025 sprint 3
**Ticket**: JIRA-456
**Workaround**: New endpoints use ProductService, legacy endpoints use LegacyProductService
**Review Note**: Do not flag as issue - this is acknowledged technical debt with timeline

### 2. Manual Change Detection in Order Dashboard
**Location**: `src/app/features/orders/order-dashboard/order-dashboard.component.ts:89`
**Issue**: Uses `ChangeDetectorRef.detectChanges()` manually in ngAfterViewInit
**Reason**: PrimeNG Chart component with dynamic data doesn't trigger CD properly
**Impact**: None - working as intended for this specific use case
**Attempted**: Tried OnPush + markForCheck, caused flickering
**Accepted**: This is the correct solution for PrimeNG Chart + dynamic data
**Review Note**: This is intentional and acceptable - do not flag

### 3. Any Types in Legacy Migration Code
**Location**: `src/app/legacy/**/*.ts` (entire legacy directory)
**Issue**: Multiple uses of `any` type, weak type safety
**Reason**: Migrated code from AngularJS, gradual TypeScript adoption
**Planned**: Gradual migration, 1 module per sprint
**Progress**: 60% complete (as of 2025-01-14)
**Review Note**: Flag new `any` usage outside legacy/, but not within legacy/

### 4. Subscription in ngAfterViewInit (Intentional)
**Location**: `src/app/features/products/product-detail/product-detail.component.ts:55`
**Issue**: Observable subscription in ngAfterViewInit instead of ngOnInit
**Reason**: Requires @ViewChild(ImageGallery) to be initialized first
**Impact**: None - correct lifecycle for this dependency
**Review Note**: This is correct and intentional - do not flag

### 5. Large Bundle Size (Optimization in Progress)
**Location**: Main bundle
**Issue**: Main bundle 800KB (target: 500KB)
**Reason**: Some dependencies not lazy-loaded, legacy code
**Plan**: Lazy load @angular/material (Q1 2025), refactor legacy (Q2 2025)
**Progress**: Identified 10 optimization opportunities
**Review Note**: Acknowledge but don't flag - team is aware and working on it

## Accepted Limitations

### PrimeNG Table Virtual Scrolling Disabled
**Location**: All p-table components
**Reason**: PrimeNG bug #5678 - virtual scroll breaks with dynamic columns
**Workaround**: Using pagination instead
**Trade-off**: Acceptable - pagination provides better UX for our use case
**Review Note**: Virtual scrolling intentionally not used - do not suggest

### RxJS Nested Subscription in Order Flow
**Location**: `src/app/features/orders/order-flow.service.ts:120`
**Issue**: Nested subscription pattern (usually anti-pattern)
**Reason**: Complex order flow requires sequential user confirmations
**Attempted**: Flattening operators caused race conditions
**Accepted**: This specific case requires nested pattern for correctness
**Review Note**: Looks like anti-pattern but is correct for this use case

### localStorage for User Preferences
**Location**: `src/app/core/services/preferences.service.ts`
**Issue**: Using localStorage (security concern if used for auth)
**Clarification**: ONLY for UI preferences (theme, language, table columns)
**Not Used For**: Auth tokens, sensitive data, PII
**Review Note**: Safe usage of localStorage - do not flag security concern

## Third-Party Library Issues

### PrimeNG 17.3.0 - Known Issue with Table Filter
**Issue**: PrimeNG table filter dropdown flickers on large datasets
**Workaround**: Custom debounce on filter input (300ms)
**Tracking**: PrimeNG GitHub issue #9876
**Expected Fix**: PrimeNG 17.4.0 (Feb 2025)

### TailwindCSS Conflict with PrimeNG Buttons
**Issue**: Tailwind CSS reset conflicts with PrimeNG button styles
**Workaround**: Custom CSS layer order in styles.scss
**Acceptable**: Styling works correctly after workaround

## False Positives to Avoid

### "Missing Error Handling" in Effects
**Note**: All effects use catchError, but it's in the ErrorInterceptor
**Pattern**: Effects assume interceptor handles errors globally
**Do Not Flag**: Missing catchError in individual effects

### "Unused Imports" in State Files
**Note**: Some imports used only by generated types
**Example**: Entity adapters import EntityState but only use in type definitions
**Do Not Flag**: These imports are necessary for type safety
```

---

## Example: review_history.md

```markdown
# Review History: E-Commerce Dashboard

## 2025-01-14 - Feature/Order-Tracking Implementation
**Scope**: New order tracking feature (23 files changed)
**Reviewer**: angular-code-review v1.0.0
**Duration**: Comprehensive review

### Summary
Major new feature adding real-time order tracking with WebSocket integration.

### Key Findings
- **Critical**: 2 issues
  - Memory leak in WebSocket subscription (fixed)
  - Missing error handling in connection retry (fixed)
- **Important**: 5 issues
  - Missing trackBy in 3 components (fixed)
  - OnPush not used in 2 new components (added)
- **Minor**: 8 suggestions
  - Type annotations could be more specific
  - Some complex functions could be extracted

### Positive Highlights
- Excellent use of NgRx for order state
- Good separation of concerns (smart/presentational)
- Comprehensive unit tests (95% coverage)
- Proper loading states throughout

### Actions Taken
- Fixed all critical and important issues
- Updated `known_issues.md` with WebSocket retry pattern (intentional design)
- Updated `common_patterns.md` with new WebSocket service pattern

### Trends vs Previous Review
- **Subscription Management**: ✅ Improved (no leaks found vs 3 in last review)
- **Type Safety**: ✅ Stable (strict mode compliance maintained)
- **Testing**: ✅ Improved (95% coverage vs 87% last review)
- **Performance**: ➡️ Stable (OnPush usage consistent)

---

## 2025-01-07 - Refactor/Authentication System
**Scope**: Complete auth system refactor (15 files)
**Reviewer**: angular-code-review v1.0.0

### Summary
Refactored authentication to use httpOnly cookies instead of localStorage.

### Key Findings
- **Critical**: 1 issue (original issue - JWT in localStorage)
  - Migrated to httpOnly cookies (resolved)
- **Important**: 2 issues
  - Missing token refresh logic (added)
  - Guard error handling (improved)

### Positive Highlights
- Excellent security improvement
- Clean facade implementation
- Good separation of concerns

### Actions Taken
- Updated `project_overview.md` with new auth approach
- Documented auth patterns in `common_patterns.md`
- Removed old localStorage issue from `known_issues.md`

---

## 2024-12-15 - Feature/Product-Catalog
**Scope**: Product catalog with filtering and search (18 files)
**Reviewer**: angular-code-review v1.0.0

### Summary
Initial implementation of product catalog with PrimeNG Table.

### Key Findings
- **Critical**: 3 issues (all subscription leaks - fixed)
- **Important**: 4 issues (missing trackBy, no OnPush)
- **Minor**: 6 suggestions

### Positive Highlights
- Good NgRx patterns
- Clean component structure

### Actions Taken
- Created initial memory files
- Documented project conventions
- Fixed all critical issues

### Notes
First review of this project - created comprehensive memory baseline.

---

## Overall Trends

### Quality Metrics Over Time
| Metric | Dec 2024 | Jan 2025 | Trend |
|--------|----------|----------|-------|
| Critical Issues | 3 | 2 | ⬇️ Improving |
| Important Issues | 4 | 5 | ➡️ Stable |
| Subscription Leaks | 3 | 0 | ✅ Resolved |
| Test Coverage | 75% | 95% | ⬆️ Great! |
| OnPush Adoption | 60% | 85% | ⬆️ Improving |

### Recurring Patterns
- **Strength**: Excellent NgRx patterns maintained consistently
- **Improvement**: Subscription management much better
- **Watch**: Bundle size growing (on team's radar)
- **Positive**: Test coverage increasing steadily

### Recommendations
- Continue current trajectory - quality improving
- Focus on bundle optimization next
- Consider updating PrimeNG when 17.4.0 released
```

---

## Usage Notes

This reference shows examples only. In actual project memory, create 4 separate files as shown above, update all files after each review, and keep files concise and focused.

---

**Created**: 2025-01-14
**Purpose**: Template for angular-code-review memory files
