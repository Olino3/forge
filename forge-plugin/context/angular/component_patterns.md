# Angular Component Patterns - Quick Reference

Best-practice patterns for Angular components with minimal detection cues and links to official docs.

**Load this file**: When reviewing `.component.ts` or template files.

---

## 1. Smart vs Presentational Components {#smart-vs-presentational}

| Type | Characteristics to Look For | Detection Clues in Code | References |
|------|----------------------------|--------------------------|------------|
| **Presentational (Dumb)** | Displays data, emits events, no domain logic, highly reusable, OnPush | Uses only `@Input()` / `@Output()`, no injected services except UI helpers | [Component Interaction](https://angular.io/guide/component-interaction), [Architecture](https://angular.io/guide/architecture-components) |
| **Smart (Container)** | Coordinates data flow, injects services, handles routing/side effects | Injects `Store`, services, `Router`; passes data down via inputs | [Component Overview](https://angular.io/guide/component-overview) |

Review focus:

- Presentational components should be simple, stateless, and OnPush.
- Smart components should delegate display logic to children.

---

## 2. Input/Output Best Practices {#input-output}

| Pattern | Good Practice | Smell to Flag | References |
|---------|--------------|---------------|------------|
| **Required Inputs** | Mark required inputs (`!`) or validate in setter | Optional inputs that are always assumed non‑null | [@Input](https://angular.io/api/core/Input) |
| **Input Validation** | Use setters or form validation, not template logic | Complex validation logic in templates | [Inputs & Outputs Guide](https://angular.io/guide/inputs-outputs) |
| **Output Naming** | Past tense (`saved`, `changed`, `closed`) | Vague names like `onClick`, `event` | [Style Guide – Events](https://angular.io/guide/styleguide#delegate-complex-component-logic-to-services) |
| **EventEmitter Typing** | `EventEmitter<T>` with clear type | `EventEmitter<any>` | [@Output](https://angular.io/api/core/Output) |

---

## 3. ViewChild & ContentChild {#viewchild-contentchild}

| API | Used For | Lifecycle Hook to Access | References |
|-----|---------|-------------------------|------------|
| `@ViewChild` / `@ViewChildren` | Query template elements and child components | `ngAfterViewInit` / `ngAfterViewChecked` | [View Queries](https://angular.io/guide/view-queries) |
| `@ContentChild` / `@ContentChildren` | Query projected content (`<ng-content>`) | `ngAfterContentInit` / `ngAfterContentChecked` | [Content Projection](https://angular.io/guide/content-projection) |

Review focus:

- Ensure null checks before using queried references.
- Avoid DOM manipulation outside proper hooks.

---

## 4. Component Lifecycle {#lifecycle}

| Hook | Primary Purpose | Anti‑pattern to Flag | References |
|------|-----------------|----------------------|------------|
| `ngOnChanges` | React to input changes | Using for initial data fetch only | [OnChanges](https://angular.io/api/core/OnChanges) |
| `ngOnInit` | Initialization, data loading | Heavy logic in constructor instead | [OnInit](https://angular.io/api/core/OnInit) |
| `ngAfterContentInit` / `ngAfterViewInit` | Access content/view children | Mutating bound state causing `ExpressionChangedAfterItHasBeenCheckedError` | [Lifecycle Hooks](https://angular.io/guide/lifecycle-hooks) |
| `ngOnDestroy` | Cleanup (subscriptions, listeners) | Missing despite manual subscriptions or listeners | [OnDestroy](https://angular.io/api/core/OnDestroy) |

---

## 5. Change Detection Strategies {#change-detection}

| Strategy | When to Use | Review Checklist | References |
|----------|------------|------------------|------------|
| **Default** | Simple components, mutable patterns | Check for heavy templates and frequent bindings | [Change Detection](https://angular.io/guide/change-detection) |
| **OnPush** | Presentational components, performance‑sensitive views | Inputs treated immutably, `async` pipe for observables | [OnPush](https://angular.io/api/core/ChangeDetectionStrategy#onpush), [Best Practices](https://angular.io/guide/change-detection-best-practices) |
| **Signals (v16+)** | Signal‑based components | Components using `signal`, `computed`, `effect` consistently | [Signals Guide](https://angular.io/guide/signals) |

Review focus:

- For OnPush components, ensure no in‑place mutation (`array.push` etc.).

---

## 6. Component Communication {#communication}

| Method | Scope | When to Prefer | References |
|--------|-------|----------------|------------|
| `@Input` / `@Output` | Parent ↔ child | Simple, local communication | [Component Interaction](https://angular.io/guide/component-interaction) |
| View queries | Parent → child | When parent needs to call child APIs | [View Queries](https://angular.io/guide/view-queries) |
| Shared service with Observables | Sibling / distant components | Cross‑component communication | [Services](https://angular.io/guide/architecture-services) |
| State management (NgRx, etc.) | App‑wide state | Complex, global state | [State Management](https://angular.io/guide/state-management) |

Review focus:

- Prefer top‑down data flow; avoid deep chains of `@Output` events.

---

## 7. Template Best Practices {#templates}

| Pattern | Good Practice | Smell to Flag | References |
|---------|--------------|---------------|------------|
| **Logic in templates** | Use pipes or computed properties | Method calls or complex expressions in templates | [Template Syntax](https://angular.io/guide/template-syntax), [Style Guide](https://angular.io/guide/styleguide#put-presentation-logic-in-the-component-class) |
| **Safe navigation** | Use `?.` or `*ngIf` for nullable data | Direct deep property access on possibly null objects | [Safe Navigation](https://angular.io/guide/template-expression-operators#the-safe-navigation-operator-and-null-property-paths) |
| **TrackBy in `*ngFor`** | Always for large/identity lists | Large lists with no `trackBy` | [NgForOf#change-propagation](https://angular.io/api/common/NgForOf#change-propagation) |
| **Structural directives (v17+)** | `@if`, `@for` used consistently | Mixing old and new syntax inconsistently | [Control Flow](https://angular.dev/guide/templates/control-flow) |

---

## 8. Content Projection {#content-projection}

| Pattern | Use Case | References |
|---------|----------|------------|
| Single slot | Simple reusable shells/layouts | [Content Projection](https://angular.io/guide/content-projection) |
| Multi‑slot | Headers/footers/cells in complex components | [Multi-slot Projection](https://angular.io/guide/content-projection#multi-slot-content-projection) |
| Conditional projection | Optional sections | [Conditional Projection](https://angular.io/guide/content-projection#conditional-content-projection) |

---

## 9. Standalone Components (Angular 14+) {#standalone}

| Signal | Meaning | Review Focus | References |
|--------|---------|-------------|------------|
| `standalone: true` in `@Component` | Component is standalone | Imports are declared directly on the component; modules minimal | [Standalone Components](https://angular.io/guide/standalone-components) |
| Use of `bootstrapApplication` | Standalone bootstrap | Check app configuration and providers | [Standalone Bootstrap](https://angular.io/guide/standalone-components#bootstrap-with-standalone-components) |

---

## 10. Component Testing {#testing}

| Area | What to Look For | References |
|------|------------------|------------|
| Test structure | Use of `TestBed`, `ComponentFixture`, clear arrange/act/assert | [Testing Components Basics](https://angular.io/guide/testing-components-basics) |
| DOM queries | Use of `By.css` or testing-library patterns | [Component Testing Scenarios](https://angular.io/guide/testing-components-scenarios) |

---

## 11. Quick Checklist for Component Reviews

- [ ] Smart vs presentational roles are clear and reasonable.
- [ ] Inputs/outputs are typed, named clearly, and validated as needed.
- [ ] ViewChild/ContentChild used with correct lifecycle hooks and null checks.
- [ ] Lifecycle hooks are used appropriately; `ngOnDestroy` exists where needed.
- [ ] Change detection strategy (Default/OnPush/Signals) matches usage.
- [ ] Templates avoid heavy logic, use safe navigation, and use `trackBy` for lists.
- [ ] Communication patterns (inputs/outputs/services/state) are appropriate.

---

## External Resources

- [Angular Component Overview](https://angular.io/guide/component-overview)
- [Angular Style Guide](https://angular.io/guide/styleguide)
- [Change Detection Best Practices](https://angular.io/guide/change-detection-best-practices)
- [Signals in Components](https://angular.io/guide/signals-components)

---

**Version**: 2.0.0 (Compact Reference Format)
**Last Updated**: 2025-11-14
**Angular Versions**: 2-18+
