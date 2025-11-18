# RxJS Patterns for Angular - Quick Reference

Detection patterns and solution references for common RxJS usage in Angular.

**Load this file**: Whenever code uses `Observable`, `Subject`, or RxJS operators.

---

## 1. Subscription Management {#subscription-management}

| Issue / Pattern | Detection Clue in Code | Recommended Approach | References |
|-----------------|------------------------|----------------------|------------|
| **Manual `.subscribe()` in components** | Many `.subscribe()` calls assigning to fields | Prefer `async` pipe in templates for UI-facing streams | [AsyncPipe](https://angular.io/api/common/AsyncPipe), [RxJS in Angular](https://angular.io/guide/rx-library) |
| **No teardown for subscriptions** | `.subscribe()` in `ngOnInit` with no `ngOnDestroy` | Use `takeUntil` pattern with `Subject`, or `DestroyRef` in v16+ | [Unsubscribing to Observables](https://angular.io/guide/rx-library#unsubscribing-to-observables), [DestroyRef](https://angular.io/api/core/DestroyRef) |
| **Subscriptions inside services** | Long‑lived services calling `.subscribe()` | Prefer returning `Observable` from services and letting components subscribe/async pipe | [HttpClient Best Practices](https://angular.io/guide/http) |
| **Event streams without completion** | `Subject`/`BehaviorSubject` never completed | Complete streams when appropriate (esp. in services with finite lifetime) | [Subjects](https://rxjs.dev/guide/subject) |

**Review focus**
- Minimize manual `.subscribe()` in components.
- Ensure teardown via `async` pipe, `takeUntil`, or `DestroyRef`.

---

## 2. Flattening Operators {#flattening-operators}

| Operator | When to Use | Smell if Misused | References |
|----------|------------|------------------|------------|
| **switchMap** | User-driven events (search box, typeahead, route changes) where you only care about latest | Using `mergeMap` for searches → outdated responses racing in | [switchMap](https://rxjs.dev/api/operators/switchMap), [Operator Decision Tree](https://rxjs.dev/operator-decision-tree) |
| **mergeMap** | Fire-and-forget concurrent tasks (logging, non‑dependent side effects) | Using `mergeMap` where order matters or where cancellation is needed | [mergeMap](https://rxjs.dev/api/operators/mergeMap) |
| **concatMap** | Sequential processing where order matters (queue of HTTP calls) | Using `switchMap` when every request result must be processed | [concatMap](https://rxjs.dev/api/operators/concatMap) |
| **exhaustMap** | Ignore new triggers while work in progress (form submit button) | Using `mergeMap` on click handler → double submit bugs | [exhaustMap](https://rxjs.dev/api/operators/exhaustMap) |

**Review focus**
- Match operator to use case (latest only vs all vs sequential vs ignore‑while‑busy).

---

## 3. Error Handling & Recovery {#error-handling}

| Pattern | Detection Clue | Recommended Approach | References |
|---------|----------------|----------------------|------------|
| **No error handling** | Pipe chain with no `catchError` | Add `catchError` close to source and return safe fallback values | [Error Handling](https://angular.io/guide/observables#error-handling), [catchError](https://rxjs.dev/api/operators/catchError) |
| **Side effects in `catchError` only** | `catchError(err => { log; throw err; })` | Separate logging from error mapping, avoid swallowing errors silently | [RxJS Error Handling Patterns](https://rxjs.dev/guide/operators#error-handling-operators) |
| **Blind `retry`** | `retry()` without limit or backoff | Use bounded retries (`retry(2)` or `retryWhen` with delay/backoff) | [retry](https://rxjs.dev/api/operators/retry), [retryWhen](https://rxjs.dev/api/operators/retryWhen) |
| **UI error states** | Stream errors not mapped to UI model | Map errors to typed result (e.g. `{ data, error }`) instead of throwing | [Angular HttpClient Guide](https://angular.io/guide/http#getting-error-details) |

---

## 4. Subject Choices {#subjects}

| Type | Use Case | Smells / Anti‑patterns | References |
|------|----------|------------------------|------------|
| **Subject** | Fire-and-forget events (button clicks, internal events) | Overused for state; prefer `BehaviorSubject`/store for stateful data | [Subject](https://rxjs.dev/guide/subject) |
| **BehaviorSubject** | State with current value (form state, user settings) | Exposed as `BehaviorSubject` instead of `Observable` (prefer `asObservable()`) | [BehaviorSubject](https://rxjs.dev/api/index/class/BehaviorSubject) |
| **ReplaySubject** | Cache/replay limited history | Large buffer sizes leading to memory usage | [ReplaySubject](https://rxjs.dev/api/index/class/ReplaySubject) |
| **AsyncSubject** | Emit last value on completion (rare) | Used for regular UI streams (usually not appropriate) | [AsyncSubject](https://rxjs.dev/api/index/class/AsyncSubject) |

**Review focus**
- Expose streams as `Observable` from services, keep subjects private.

---

## 5. Common Operator Patterns {#operator-patterns}

| Scenario | Recommended Pattern | References |
|----------|--------------------|------------|
| **Live search / typeahead** | `valueChanges` → `debounceTime` → `distinctUntilChanged` → `switchMap` | [Reactive Forms](https://angular.io/guide/reactive-forms), [debounceTime](https://rxjs.dev/api/operators/debounceTime) |
| **Combining HTTP results** | `combineLatest` / `forkJoin` → `map` to view model | [Combination Operators](https://rxjs.dev/guide/operators#combination-operators) |
| **Filtering / mapping lists** | `map`, `filter`, `tap` for side effects | [Transformation Operators](https://rxjs.dev/guide/operators#transformation-operators) |
| **Throttling events** | `throttleTime` for scroll/resize events to reduce change detection pressure | [throttleTime](https://rxjs.dev/api/operators/throttleTime) |

---

## 6. RxJS Anti‑patterns to Flag {#anti-patterns}

| Anti‑pattern | What It Looks Like | Risk | References |
|--------------|--------------------|------|------------|
| **Nested subscriptions** | `observable$.subscribe(v => other$.subscribe(...))` | Memory leaks, unreadable control flow | [Flattening Operators](https://rxjs.dev/guide/operators#joining-creation-operators-with-flattening-operators) |
| **`subscribe` in services for business logic** | Service method both subscribes and mutates component | Hard to test, hidden side effects | [Angular Service Patterns](https://angular.io/guide/architecture-services) |
| **Non‑typed streams (`Observable<any>`)** | Widespread `any` usage in RxJS types | Loss of type safety | [TypeScript + RxJS](https://rxjs.dev/guide/typescript) |
| **Long chains in components** | Very complex `pipe(...)` chains in components | Move composition to services or helper functions | [Composing Operators](https://rxjs.dev/guide/operators) |

---

## 7. Quick Checklist for Reviews

- [ ] Components use `async` pipe instead of manual `.subscribe()` where possible.
- [ ] All manual subscriptions have a clear teardown strategy (`takeUntil`, `DestroyRef`, or `Subscription` cleanup).
- [ ] No nested subscriptions; appropriate flattening operator (`switchMap` / `mergeMap` / `concatMap` / `exhaustMap`) is used.
- [ ] Streams have explicit error handling and map errors to safe UI states.
- [ ] Subjects are encapsulated in services; components consume `Observable` only.
- [ ] Operator chains are readable and, if complex, moved into reusable helpers/services.

---

## External Resources

- [RxJS Documentation](https://rxjs.dev/)
- [RxJS Operator Decision Tree](https://rxjs.dev/operator-decision-tree)
- [Angular: Observables and RxJS](https://angular.io/guide/rx-library)
- [Angular HttpClient Guide](https://angular.io/guide/http)

---

**Version**: 2.0.0 (Compact Reference Format)
**Last Updated**: 2025-11-14
**Angular Versions**: 2-18+
