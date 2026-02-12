---
id: "dotnet/blazor_patterns"
domain: dotnet
title: "Blazor Component Patterns - Quick Reference"
type: framework
estimatedTokens: 1150
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Authoritative References"
    estimatedTokens: 33
    keywords: [authoritative, references]
  - name: "Common Blazor Patterns"
    estimatedTokens: 288
    keywords: [blazor, patterns]
  - name: "Blazor Anti-Patterns"
    estimatedTokens: 87
    keywords: [blazor, anti-patterns]
  - name: "Quick Review Checklist"
    estimatedTokens: 169
    keywords: [quick, review, checklist]
  - name: "When to Read External Docs"
    estimatedTokens: 52
    keywords: [read, external, docs]
tags: [dotnet, blazor, components, lifecycle, state, js-interop, forms, rendering]
---

# Blazor Component Patterns – Quick Reference

Compact Blazor patterns for component design, state management, rendering, and JS interop.

**Load this file when reviewing** `.razor` components, Blazor lifecycle/state code, or JS interop.

---

## Authoritative References

- ASP.NET Core Blazor docs (current):  
  https://learn.microsoft.com/aspnet/core/blazor
- Blazor components and lifecycle:  
  https://learn.microsoft.com/aspnet/core/blazor/components
- Blazor forms and validation:  
  https://learn.microsoft.com/aspnet/core/blazor/forms-validation
- Blazor JavaScript interop:  
  https://learn.microsoft.com/aspnet/core/blazor/js-interop
- Blazor performance best practices:  
  https://learn.microsoft.com/aspnet/core/blazor/performance

Use this file for cues; use the links above for detailed APIs and examples.

---

## Common Blazor Patterns

| Area | Good Pattern | Detection Cues | Risk if Ignored |
|------|--------------|----------------|------------------|
| Lifecycle | Use `OnInitializedAsync` / `OnParametersSet[Async]` for data loading; use `OnAfterRender[Async]` only for JS/DOM work and check `firstRender` | Data loads in `OnInitializedAsync`, parameter-dependent loads in `OnParametersSet[Async]`, minimal logic in `OnAfterRender` | Double renders, hard-to-debug side effects, JS interop failures during prerendering |
| Async | Avoid `async void` lifecycle/event handlers; return `Task` and use `InvokeAsync(StateHasChanged)` only for non-Blazor threads | `async Task` overrides with awaits; `async void` only for event handlers that must be void | Swallowed exceptions, race conditions, UI not updating correctly |
| Parameters | Validate `[Parameter]` and `[CascadingParameter]` in `OnParametersSet`; use `[EditorRequired]` where appropriate | Guard clauses for required parameters; clear exception messages on invalid values | Components silently misconfigured, null reference crashes |
| Events | Use `EventCallback`/`EventCallback<T>` for parent notifications instead of `Action`/delegates | Parameters typed as `EventCallback<T>`; children `InvokeAsync` callbacks | Parent not re-rendering, subtle state desync |
| State | Keep view state in components; put app-wide state in DI services (scoped for Server, singleton for WASM) with change notifications | `@inject` state services; components subscribe/unsubscribe to events | Memory leaks, duplicated state, unpredictable UI updates |
| Rendering | Only call `StateHasChanged` when Blazor can’t detect changes itself; override `ShouldRender` for expensive components; use `<Virtualize>` for large lists | `ShouldRender` override with simple change detection; `<Virtualize>` on large collections | Excessive re-rendering, slow UI, unnecessary network traffic (Server) |
| JS Interop | Use `IJSRuntime` and JS modules (`IJSObjectReference`) in `OnAfterRenderAsync(firstRender)`; dispose modules and `DotNetObjectReference` | `OnAfterRenderAsync` guarded by `firstRender`; `IAsyncDisposable` for cleanup | Leaked JS objects, errors during prerender, memory bloat |
| Forms | Use `EditForm` + validation components; bind to a model with data annotations; handle valid/invalid submit separately | `EditForm` with `Model`, `<DataAnnotationsValidator />`, `ValidationMessage` | Weak validation, inconsistent UX, business rules scattered in UI |
| Disposal | Implement `IDisposable`/`IAsyncDisposable` when subscribing to events or owning JS modules/timers | `Dispose`/`DisposeAsync` unsubscribes and disposes external resources | Memory leaks, callbacks to disposed components |
| Hosting Model | Use scoped services for Blazor Server per-circuit state; singleton for WASM; avoid JS interop during prerender (`!OperatingSystem.IsBrowser()`) | Registration patterns and environment checks in startup | State bleeding between users (Server), runtime errors during prerender |

---

## Blazor Anti-Patterns

- Loading initial data in `OnAfterRender[Async]` instead of `OnInitialized[Async]` / `OnParametersSet[Async]`.
- Using `async void` in lifecycle methods or complex event handlers (except where required by the framework).
- Failing to validate parameters or cascading parameters, leading to null/invalid state.
- Using `Action`/delegates instead of `EventCallback` for parent notifications.
- Calling `StateHasChanged` unnecessarily after awaited operations that already trigger renders.
- Not using `<Virtualize>` or other techniques for large lists or expensive UIs.
- Subscribing to events (timers, state services) without unsubscribing in `Dispose`.
- Creating services inside components instead of injecting them via DI.
- Attempting JS interop before first render or during prerender without guards.
- Forgetting `[JSInvokable]` on methods called from JavaScript.

---

## Quick Review Checklist

- **Lifecycle & Async**
  - [ ] Data-loading code is in `OnInitialized[Async]` / `OnParametersSet[Async]`, not `OnAfterRender[Async]`.
  - [ ] No `async void` lifecycle overrides; exceptions are observable.
  - [ ] `OnAfterRender[Async]` is only used when rendering has occurred and guarded by `firstRender` when appropriate.

- **Parameters & Events**
  - [ ] Required parameters are marked (`[EditorRequired]`) and validated in `OnParametersSet`.
  - [ ] Child-to-parent communication uses `EventCallback`/`EventCallback<T>`.
  - [ ] Cascading parameters are used deliberately for cross-cutting/shared context.

- **State & Rendering**
  - [ ] Component-specific state lives inside the component; app-wide state lives in DI services.
  - [ ] Long lists or heavy UIs use `<Virtualize>` or alternative paging/lazy-loading.
  - [ ] `ShouldRender` is overridden only where necessary and remains simple and correct.

- **JS Interop**
  - [ ] JS calls are made via `IJSRuntime`/JS modules in `OnAfterRenderAsync(firstRender)`.
  - [ ] `DotNetObjectReference` and JS modules are disposed via `IDisposable`/`IAsyncDisposable`.
  - [ ] Components avoid JS interop during prerender (Server) by checking the environment.

- **Forms & Validation**
  - [ ] Forms use `EditForm` with `Model` binding and validation components.
  - [ ] Data annotations or other validation rules reflect actual business rules.

- **Hosting Model**
  - [ ] Blazor Server: per-user/circuit state is scoped; reconnection scenarios are considered.
  - [ ] Blazor WASM: app state services are singleton where appropriate; payload size/perf are considered.

---

## When to Read External Docs

- You see an unfamiliar lifecycle pattern → read **Blazor components and lifecycle** docs.
- You need detailed examples of forms, validation, or input components → read **Blazor forms and validation** docs.
- You’re debugging JS interop or memory leaks → read **Blazor JavaScript interop** docs.
- You’re concerned about rendering performance, flicker, or latency → read **Blazor performance best practices**.

---

**Version**: 0.2.0-alpha (Compact Reference Format)
**Last Updated**: 2025-11-15
