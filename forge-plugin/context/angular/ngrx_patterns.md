# NgRx State Management Patterns – Quick Reference

Best‑practice checklist for NgRx (and similar store libraries) in Angular.

**Load this file** when you see NgRx imports (`@ngrx/store`, `@ngrx/effects`, `@ngrx/entity`) or a custom store/facade layer.

---

## 1. Actions, Reducers, Selectors {#core}

| Area | Good Practice | Smell to Flag | References |
|------|--------------|---------------|------------|
| Action naming | `[Source] Event` format, use `createAction` with `props` | Vague action names like `LOAD`/`SUCCESS`, string literals all over | [Actions](https://ngrx.io/guide/store/actions) |
| Reducer purity | Use `createReducer`/`on`, always return new state, no side‑effects | `state.something.push(...)`, `new Date()`, service calls in reducer | [Reducers](https://ngrx.io/guide/store/reducers) |
| Selectors | Use `createSelector`/`createFeatureSelector`, memoize projections | Components calling `.pipe(map(...))` on `store.select` everywhere | [Selectors](https://ngrx.io/guide/store/selectors) |

---

## 2. Effects {#effects}

| Pattern | Good Practice | Smell to Flag | References |
|---------|--------------|---------------|------------|
| Side‑effects | Use `createEffect`, inject `Actions`, call services in effects only | HTTP calls directly in components or reducers | [Effects](https://ngrx.io/guide/effects) |
| Flattening | Use `switchMap` for request/cancel, `concatMap` for ordered, `mergeMap` for parallel | Nested subscriptions or wrong operator leading to duplicate calls | [Choosing an operator](https://ngrx.io/guide/effects#flattening-operators) |
| Error handling | Map errors to failure actions, keep effects small | Effects that `catchError` but only `console.log` or swallow errors | [Error handling](https://ngrx.io/guide/effects#handling-errors) |

---

## 3. Entity + Normalization {#entity}

| Area | Good Practice | Smell to Flag | References |
|------|--------------|---------------|------------|
| Collections | Use `@ngrx/entity` for large collections (add/update/remove helpers) | Big arrays with manual `map/filter/find` in reducers | [Entity](https://ngrx.io/guide/entity) |
| IDs and selectors | Use adapter selectors (`selectAll`, `selectEntities`, etc.) | Duplicated logic to pick items by id in many places | [Entity selectors](https://ngrx.io/guide/entity/adapter#selectors) |

---

## 4. Facade Pattern {#facade}

| Purpose | Good Practice | Smell to Flag | References |
|---------|--------------|---------------|------------|
| Component API | Expose `vm$`/observables and commands from a facade or feature store | Components directly dispatching many actions and doing `store.select` everywhere | [Facade discussions](https://ngrx.io/guide/store#component-store-and-facades) |
| Testability | Components stay mostly dumb; business logic lives in facade/effects | Hard‑to‑test components with complex store wiring | |

---

## 5. General State Management Smells

| Smell | What to Look For | Why It’s a Problem |
|-------|------------------|---------------------|
| Over‑using global store | Everything is in a single root store; no local/component state | Increases coupling, noisy action logs, performance impact |
| Async logic in components | HTTP calls and branching logic in components rather than effects/services | Harder to reuse/test and to reason about flows |
| Massive state shape | Huge state objects with many unrelated concerns | Refactoring becomes hard; performance/debugging issues |

---

## 6. Quick Checklist

- [ ] Actions have meaningful `[Source] Event` names.
- [ ] Reducers are pure, immutable, and side‑effect free.
- [ ] Selectors are centralized and memoized.
- [ ] Effects own async work and handle errors via actions.
- [ ] Collections use `@ngrx/entity` where appropriate.
- [ ] Components use facades or a thin store API, not store spaghetti.

---

**Version**: 2.0.0 (Compact Reference Format)
**Last Updated**: 2025-11-14
