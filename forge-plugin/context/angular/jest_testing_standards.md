---
id: "angular/jest_testing_standards"
domain: angular
title: "Angular/Jest Testing Standards"
type: pattern
estimatedTokens: 400
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Core Principles"
    estimatedTokens: 65
    keywords: [core, principles]
  - name: "Quick Reference"
    estimatedTokens: 87
    keywords: [quick, reference]
  - name: "Framework Detection"
    estimatedTokens: 23
    keywords: [framework, detection]
  - name: "Official Documentation"
    estimatedTokens: 13
    keywords: [official, documentation]
  - name: "Related Context Files"
    estimatedTokens: 16
    keywords: [related, context, files]
tags: [angular, testing, jest, jasmine, karma, naming-conventions]
---

# Angular/Jest Testing Standards

## Core Principles

### Test Quality Fundamentals

1. **Test Behavior, Not Implementation**
   - Focus on what the component/service does
   - Tests should survive refactoring
   - Reference: [Testing Angular Guide](https://angular.io/guide/testing)

2. **AAA Pattern** (Arrange-Act-Assert)
   - Arrange: Set up TestBed, mocks, test data
   - Act: Trigger action (detectChanges, method call)
   - Assert: Verify expected outcome

3. **Test Independence**
   - Each test runs in isolation
   - Use beforeEach for TestBed setup
   - Use afterEach for cleanup (fixture.destroy())

### Naming Conventions

**Angular test naming**:
```
should_{expected_behavior}_when_{condition}
```

**Examples**:
- `should_display_user_name_when_user_provided`
- `should_emit_event_when_button_clicked`
- `should_call_service_when_component_initialized`

## Quick Reference

### Jest vs Jasmine

| Feature | Jest | Jasmine/Karma |
|---------|------|---------------|
| Mocking | `jest.fn()`, `jest.mock()` | `jasmine.createSpyObj()`, `spyOn()` |
| Return Value | `.mockReturnValue()` | `.and.returnValue()` |
| Assertions | `expect().toBe()` | `expect().toBe()` (same) |
| Async | `done`, promises, async/await | `done`, `fakeAsync`, `async` |
| HTTP Mocking | `jest.mock()` or manual | `HttpTestingController` |
| Snapshot | Built-in | Requires plugin |

### Angular Testing Utilities

```typescript
import { TestBed, ComponentFixture, fakeAsync, tick, flush } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
```

- `TestBed`: Configure and create test module
- `ComponentFixture`: Component test harness
- `fakeAsync/tick`: Synchronous async testing
- `async/whenStable`: Asynchronous async testing
- `By.css()`: Query elements by CSS selector

## Framework Detection

**Detect Jest**:
- `jest.config.js` or `jest.config.ts` exists
- `package.json` has `@types/jest`
- Tests use `jest.fn()`, `mockReturnValue`

**Detect Jasmine/Karma**:
- `karma.conf.js` exists
- `package.json` has `jasmine-core`, `karma`
- Tests use `jasmine.createSpyObj`, `.and.returnValue()`

## Official Documentation

- [Angular Testing Guide](https://angular.io/guide/testing)
- [Angular Testing Components](https://angular.io/guide/testing-components-basics)
- [Angular Testing Services](https://angular.io/guide/testing-services)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Jasmine Documentation](https://jasmine.github.io/)

## Related Context Files

- `component_testing_patterns.md` - Component-specific patterns
- `service_testing_patterns.md` - Service testing strategies
- `testing_utilities.md` - TestBed, mocks, spies
- `test_antipatterns.md` - Common mistakes
