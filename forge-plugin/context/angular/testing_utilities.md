---
id: "angular/testing_utilities"
domain: angular
title: "Angular Testing Utilities"
type: reference
estimatedTokens: 550
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "TestBed Configuration"
    estimatedTokens: 49
    keywords: [testbed, configuration]
  - name: "Mocking Patterns"
    estimatedTokens: 45
    keywords: [mocking, patterns]
  - name: "Async Testing"
    estimatedTokens: 57
    keywords: [async, testing]
  - name: "Change Detection"
    estimatedTokens: 18
    keywords: [change, detection]
  - name: "Querying Elements"
    estimatedTokens: 37
    keywords: [querying, elements]
  - name: "NgRx Testing"
    estimatedTokens: 33
    keywords: [ngrx, testing]
  - name: "Router Testing"
    estimatedTokens: 27
    keywords: [router, testing]
  - name: "Official Documentation"
    estimatedTokens: 20
    keywords: [official, documentation]
  - name: "Related Context Files"
    estimatedTokens: 11
    keywords: [related, context, files]
tags: [angular, testing, testbed, mocking, async, ngrx-testing, router-testing]
---

# Angular Testing Utilities

## TestBed Configuration

### Basic Setup

```typescript
await TestBed.configureTestingModule({
  declarations: [ComponentToTest, MockComponents],
  imports: [CommonModule, ReactiveFormsModule],
  providers: [{ provide: Service, useValue: mockService }],
  schemas: [NO_ERRORS_SCHEMA] // Optional
}).compileComponents();
```

### Configuration Options

| Option | Purpose |
|--------|---------|
| `declarations` | Components, directives, pipes to declare |
| `imports` | Modules to import |
| `providers` | Services and dependency injection |
| `schemas` | NO_ERRORS_SCHEMA (ignore unknown elements) |

## Mocking Patterns

### Jest Mocks

```typescript
// Mock function
const mockFn = jest.fn();
mockFn.mockReturnValue('value');
mockFn.mockReturnValueOnce('first').mockReturnValue('rest');

// Mock object
const mockService = {
  method: jest.fn().mockReturnValue(of(data))
} as any;

// Spy on method
jest.spyOn(service, 'method').mockReturnValue(of(data));
```

### Jasmine Spies

```typescript
// Create spy object
const mockService = jasmine.createSpyObj('Service', ['method1', 'method2']);
mockService.method1.and.returnValue(of(data));

// Spy on existing object
spyOn(service, 'method').and.returnValue(of(data));

// Spy property
spyOnProperty(service, 'property', 'get').and.returnValue('value');
```

## Async Testing

### fakeAsync / tick

```typescript
import { fakeAsync, tick, flush } from '@angular/core/testing';

it('test', fakeAsync(() => {
  component.delayedAction();
  tick(1000); // Advance time by 1000ms
  expect(component.value).toBe('done');
}));

// flush() - advance time until all async tasks complete
flush();
```

### async / whenStable

```typescript
import { async } from '@angular/core/testing';

it('test', async(() => {
  fixture.detectChanges();
  fixture.whenStable().then(() => {
    expect(component.loaded).toBe(true);
  });
}));
```

### done Callback

```typescript
it('test', (done) => {
  service.getData().subscribe(data => {
    expect(data).toBeDefined();
    done();
  });
});
```

## Change Detection

```typescript
// Trigger change detection
fixture.detectChanges();

// OnPush components
component.changeDetectorRef.markForCheck();
fixture.detectChanges();

// Wait for stability
await fixture.whenStable();

// Auto change detection (deprecated)
fixture.autoDetectChanges();
```

## Querying Elements

```typescript
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

// By CSS
const element = fixture.debugElement.query(By.css('.class'));
const elements = fixture.debugElement.queryAll(By.css('.class'));

// By Directive
const directive = fixture.debugElement.query(By.directive(MyDirective));

// Native element
const nativeElement = element.nativeElement as HTMLElement;

// Compiled HTML
const compiled = fixture.nativeElement as HTMLElement;
```

## NgRx Testing

```typescript
import { provideMockStore, MockStore } from '@ngrx/store/testing';

beforeEach(() => {
  const initialState = { feature: { data: [] } };

  TestBed.configureTestingModule({
    providers: [provideMockStore({ initialState })]
  });

  store = TestBed.inject(MockStore);
});

// Override selectors
store.overrideSelector(selectData, mockData);

// Spy on dispatch
spyOn(store, 'dispatch');
expect(store.dispatch).toHaveBeenCalledWith(action());
```

## Router Testing

```typescript
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';

beforeEach(() => {
  TestBed.configureTestingModule({
    imports: [RouterTestingModule.withRoutes([])],
  });

  router = TestBed.inject(Router);
});

// Spy on navigation
const navigateSpy = spyOn(router, 'navigate');
component.goToDetail('123');
expect(navigateSpy).toHaveBeenCalledWith(['/detail', '123']);
```

## Official Documentation

- [TestBed API](https://angular.io/api/core/testing/TestBed)
- [Async Utilities](https://angular.io/api/core/testing/async)
- [NgRx Testing](https://ngrx.io/guide/store/testing)
- [Router Testing](https://angular.io/guide/testing-components-scenarios#routing-component)

## Related Context Files

- `jest_testing_standards.md` - Testing fundamentals
- `component_testing_patterns.md` - Component testing
- `service_testing_patterns.md` - Service testing
