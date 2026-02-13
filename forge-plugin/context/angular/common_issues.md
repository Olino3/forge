---
id: "angular/common_issues"
domain: angular
title: "Angular Common Issues - Quick Reference"
type: always
estimatedTokens: 1250
loadingStrategy: always
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Memory Leaks"
    estimatedTokens: 53
    keywords: [memory, leaks, memory-leaks]
  - name: "Change Detection Errors"
    estimatedTokens: 54
    keywords: [change, detection, errors, change-detection-errors]
  - name: "Lifecycle Hook Misuse"
    estimatedTokens: 53
    keywords: [lifecycle, hook, misuse, lifecycle-hook-misuse]
  - name: "Observable Subscription Problems"
    estimatedTokens: 64
    keywords: [observable, subscription, problems, observable-subscription-problems]
  - name: "Template Syntax Mistakes"
    estimatedTokens: 70
    keywords: [template, syntax, mistakes, template-syntax-mistakes]
  - name: "Zone.js Issues"
    estimatedTokens: 48
    keywords: [zonejs, issues, zonejs-issues]
  - name: "Dependency Injection Problems"
    estimatedTokens: 71
    keywords: [dependency, injection, problems, dependency-injection-problems]
  - name: "Router Navigation Issues"
    estimatedTokens: 66
    keywords: [router, navigation, issues, router-navigation-issues]
  - name: "Quick Checklist for Reviews"
    estimatedTokens: 150
    keywords: [quick, checklist, reviews]
  - name: "External Resources"
    estimatedTokens: 38
    keywords: [external, resources]
tags: [angular, common-issues, memory-leaks, change-detection, lifecycle, observables]
---

# Angular Common Issues - Quick Reference

Detection patterns and solution references for frequently encountered Angular problems.

**Load this file**: ALWAYS (for every Angular code review)

---

## 1. Memory Leaks {#memory-leaks}

| Issue | Detection Pattern | Solution Reference |
|-------|------------------|-------------------|
| **Unmanaged Subscriptions** | `.subscribe()` without cleanup | [Async Pipe](https://angular.io/api/common/AsyncPipe), [takeUntil Pattern](https://angular.io/guide/rx-library#unsubscribing-to-observables), [DestroyRef](https://angular.io/api/core/DestroyRef) |
| **Event Listeners** | `addEventListener()` without `removeEventListener()` | [Lifecycle Hooks Guide](https://angular.io/guide/lifecycle-hooks), [@HostListener](https://angular.io/api/core/HostListener) |
| **Intervals/Timeouts** | `setInterval()`/`setTimeout()` without `clear*()` | Store IDs, clear in `ngOnDestroy()` |
| **Component References** | `ViewChild`/`ContentChild` accessed after destroy | Check `ngOnDestroy()` implementation |

**Key Pattern**: Always implement `ngOnDestroy()` for cleanup

---

## 2. Change Detection Errors {#change-detection-errors}

| Issue | Detection Pattern | Solution Reference |
|-------|------------------|-------------------|
| **ExpressionChangedAfterItHasBeenCheckedError** | State change after view checked (in `ngAfterViewInit`, etc.) | [Change Detection Guide](https://angular.io/guide/change-detection), use `setTimeout()` or `ChangeDetectorRef.detectChanges()` |
| **OnPush Not Triggering** | `@Input()` object mutated instead of replaced | [OnPush Strategy](https://angular.io/api/core/ChangeDetectionStrategy#onpush), use immutable updates |
| **Infinite Change Detection** | Impure pipes, getters in templates | [Pure Pipes](https://angular.io/guide/pipes-overview#pure-and-impure-pipes) |

**References**:
- [Change Detection in Depth](https://angular.io/guide/change-detection)
- [ChangeDetectorRef API](https://angular.io/api/core/ChangeDetectorRef)

---

## 3. Lifecycle Hook Misuse {#lifecycle-hook-misuse}

| Anti-Pattern | Correct Approach | Reference |
|-------------|------------------|-----------|
| Data loading in constructor | Use `ngOnInit()` | [Lifecycle Hooks Guide](https://angular.io/guide/lifecycle-hooks) |
| Data loading in `ngAfterViewInit()` | Use `ngOnInit()` (unless view-dependent) | [View Lifecycle](https://angular.io/guide/lifecycle-hooks#responding-to-view-changes) |
| Missing `ngOnDestroy()` | Always implement for cleanup | [OnDestroy Interface](https://angular.io/api/core/OnDestroy) |
| Modifying state in `ngAfterViewChecked()` | Use `ngAfterContentChecked()` or defer with `setTimeout()` | [Lifecycle Sequence](https://angular.io/guide/lifecycle-hooks#lifecycle-event-sequence) |

**Quick Reference**: [Lifecycle Hooks Sequence Diagram](https://angular.io/guide/lifecycle-hooks#lifecycle-event-sequence)

---

## 4. Observable Subscription Problems {#observable-subscription-problems}

| Anti-Pattern | Detection | Solution |
|-------------|-----------|----------|
| **Nested Subscriptions** | Multiple nested `.subscribe()` calls | Use RxJS operators: `switchMap`, `mergeMap`, `concatMap` - [RxJS Operators](https://rxjs.dev/guide/operators) |
| **No Error Handling** | `.subscribe()` without error callback | Add `catchError` operator - [Error Handling](https://angular.io/guide/observables#error-handling) |
| **Manual Subscription** | Assignment in `.subscribe()` callback | Use `async` pipe in template - [Async Pipe](https://angular.io/api/common/AsyncPipe) |
| **Subject Memory Leaks** | Subject not completed | Call `.complete()` in `ngOnDestroy()` |

**References**:
- [RxJS in Angular](https://angular.io/guide/rx-library)
- [Operator Decision Tree](https://rxjs.dev/operator-decision-tree)

---

## 5. Template Syntax Mistakes {#template-syntax-mistakes}

| Issue | Detection | Solution Reference |
|-------|-----------|-------------------|
| **Two-way Binding Misuse** | `[(ngModel)]` without FormsModule | [Forms Guide](https://angular.io/guide/forms-overview) |
| **Unsafe Property Access** | `user.address.city` when address might be null | Use optional chaining `user.address?.city` or `*ngIf` |
| **Function Calls in Templates** | `{{ calculateTotal() }}` | Use pipes or computed properties - [Performance Guide](https://angular.io/guide/change-detection-best-practices) |
| **Missing TrackBy** | `*ngFor` without `trackBy` on large lists | [TrackBy Function](https://angular.io/api/common/NgForOf#change-propagation) |
| **Incorrect Event Syntax** | `(click)="method"` (missing parentheses) | Should be `(click)="method()"` |

**References**:
- [Template Syntax](https://angular.io/guide/template-syntax)
- [Built-in Directives](https://angular.io/guide/built-in-directives)

---

## 6. Zone.js Issues {#zonejs-issues}

| Issue | Detection | Solution Reference |
|-------|-----------|-------------------|
| **External Libraries Not Triggering CD** | Third-party callbacks don't update view | Use `NgZone.run()` - [NgZone API](https://angular.io/api/core/NgZone) |
| **Performance with High-Frequency Events** | Events like `mousemove`, `scroll` | Use `NgZone.runOutsideAngular()` - [Zone Optimization](https://angular.io/guide/zone) |
| **Testing Zone Issues** | `fakeAsync` errors | [Testing with Zones](https://angular.io/guide/testing-components-scenarios#waiting-for-asynchronous-data) |

**References**:
- [Zone.js Documentation](https://angular.io/guide/zone)
- [NgZone API](https://angular.io/api/core/NgZone)

---

## 7. Dependency Injection Problems {#dependency-injection-problems}

| Issue | Detection | Solution Reference |
|-------|-----------|-------------------|
| **Missing providedIn** | Service not registered anywhere | Add `providedIn: 'root'` - [Injectable Decorator](https://angular.io/api/core/Injectable) |
| **Wrong Injection Scope** | Service should be singleton but provided in component | Use `providedIn: 'root'` for singletons - [Hierarchical DI](https://angular.io/guide/hierarchical-dependency-injection) |
| **Circular Dependencies** | Services depend on each other | Use `forwardRef()` or refactor - [Forward Reference](https://angular.io/api/core/forwardRef) |
| **Optional Dependencies Not Handled** | `@Optional()` injection without null checks | Always check for null - [Optional Decorator](https://angular.io/api/core/Optional) |

**References**:
- [Dependency Injection Guide](https://angular.io/guide/dependency-injection)
- [Dependency Providers](https://angular.io/guide/dependency-injection-providers)

---

## 8. Router Navigation Issues {#router-navigation-issues}

| Issue | Detection | Solution Reference |
|-------|-----------|-------------------|
| **Memory Leaks from Route Subscriptions** | `this.route.params.subscribe()` without cleanup | Use `async` pipe or snapshot - [Router Guide](https://angular.io/guide/router) |
| **Incorrect Route Guards** | Guard doesn't return boolean/Observable/Promise | [Route Guards](https://angular.io/guide/router-tutorial-toh#canactivate-requiring-authentication) |
| **NavigationEnd Not Filtered** | Listening to all router events | Filter with `filter(event => event instanceof NavigationEnd)` - [Router Events](https://angular.io/guide/router-reference#router-events) |
| **Fragment/QueryParams Lost** | Navigation without preserving params | Use `queryParamsHandling: 'merge'` - [Navigation Extras](https://angular.io/api/router/NavigationExtras) |

**References**:
- [Router Tutorial](https://angular.io/guide/router-tutorial)
- [Router API](https://angular.io/api/router/Router)

---

## Quick Checklist for Reviews

Use this checklist when reviewing Angular code:

### Memory Management
- [ ] All `.subscribe()` calls have cleanup (async pipe, takeUntil, or manual)
- [ ] Event listeners removed in `ngOnDestroy()`
- [ ] Intervals/timeouts cleared
- [ ] Subjects completed in `ngOnDestroy()`

### Change Detection
- [ ] No state changes after view checked
- [ ] OnPush components use immutable updates
- [ ] No function calls in templates (use pipes or properties)
- [ ] TrackBy functions used with large `*ngFor` lists

### Lifecycle
- [ ] Data loading in `ngOnInit()`, not constructor
- [ ] `ngOnDestroy()` implemented when needed
- [ ] Correct lifecycle hook for the operation

### Observables
- [ ] No nested subscriptions (use operators)
- [ ] Error handling with `catchError`
- [ ] Prefer `async` pipe over manual subscription

### Templates
- [ ] Safe navigation (`?.`) or `*ngIf` for nullable properties
- [ ] Correct event binding syntax with `()`
- [ ] Two-way binding with proper imports

### DI & Routing
- [ ] Services use `providedIn: 'root'` when appropriate
- [ ] Route param subscriptions cleaned up or use snapshot
- [ ] Guards return correct types

---

## External Resources

### Official Documentation
- [Angular.io Documentation](https://angular.io/docs)
- [Angular Style Guide](https://angular.io/guide/styleguide)
- [Angular API Reference](https://angular.io/api)

### Best Practices
- [Angular Performance Guide](https://angular.io/guide/change-detection-best-practices)
- [Security Guide](https://angular.io/guide/security)
- [Testing Guide](https://angular.io/guide/testing)

### Community Resources
- [Angular Blog](https://blog.angular.io/)
- [RxJS Documentation](https://rxjs.dev/)
- [Angular ESLint](https://github.com/angular-eslint/angular-eslint)

---

**Version**: 0.3.0-alpha (Compact Reference Format)
**Last Updated**: 2025-11-14
**Angular Versions**: 2-18+
