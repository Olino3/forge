---
id: "angular/test_antipatterns"
domain: angular
title: "Angular Test Anti-Patterns"
type: pattern
estimatedTokens: 800
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "What to Avoid"
    estimatedTokens: 354
    keywords: [avoid]
  - name: "Quick Checklist"
    estimatedTokens: 66
    keywords: [quick, checklist]
  - name: "Official Documentation"
    estimatedTokens: 20
    keywords: [official, documentation]
  - name: "Related Context Files"
    estimatedTokens: 18
    keywords: [related, context, files]
tags: [angular, testing, anti-patterns, change-detection, mocking, async]
---

# Angular Test Anti-Patterns

## What to Avoid

### 1. Testing Implementation Details

❌ **Bad**:
```typescript
it('test', () => {
  expect(component.privateMethod).toHaveBeenCalled();
  expect(component.internalState).toBe('value');
});
```

✅ **Good**:
```typescript
it('should_display_message_when_button_clicked', () => {
  component.showMessage();
  fixture.detectChanges();

  const message = fixture.debugElement.query(By.css('.message'));
  expect(message.nativeElement.textContent).toContain('Hello');
});
```

### 2. Forgetting Change Detection

❌ **Bad**:
```typescript
it('test', () => {
  component.value = 'new';
  // Missing fixture.detectChanges()

  const element = fixture.debugElement.query(By.css('.value'));
  expect(element.nativeElement.textContent).toBe('new'); // Fails!
});
```

✅ **Good**:
```typescript
it('test', () => {
  component.value = 'new';
  fixture.detectChanges(); // Trigger change detection

  const element = fixture.debugElement.query(By.css('.value'));
  expect(element.nativeElement.textContent).toBe('new');
});
```

### 3. Not Cleaning Up Subscriptions in Tests

❌ **Bad**:
```typescript
it('test', () => {
  service.data$.subscribe(data => {
    expect(data).toBeDefined();
  });
  // Subscription never completes
});
```

✅ **Good**:
```typescript
it('test', (done) => {
  service.data$.subscribe({
    next: data => {
      expect(data).toBeDefined();
      done(); // Completes test
    }
  });
});
```

### 4. Over-Mocking

❌ **Bad** - Mocking everything:
```typescript
const mockComponent = {
  ngOnInit: jest.fn(),
  doSomething: jest.fn(),
  // ... mocking component under test
};
```

✅ **Good** - Mock dependencies only:
```typescript
const mockService = { getData: jest.fn().mockReturnValue(of([])) };
// Test real component behavior
```

### 5. Testing Framework Code

❌ **Bad**:
```typescript
it('should_bind_input', () => {
  component.user = { name: 'John' };
  expect(component.user.name).toBe('John'); // Testing TypeScript
});
```

✅ **Good**:
```typescript
it('should_display_user_name', () => {
  component.user = { name: 'John' };
  fixture.detectChanges();

  const element = fixture.debugElement.query(By.css('.name'));
  expect(element.nativeElement.textContent).toContain('John');
});
```

### 6. Shared Test State

❌ **Bad**:
```typescript
describe('MyComponent', () => {
  let sharedData = []; // Shared between tests

  it('test1', () => {
    sharedData.push('item');
    expect(sharedData.length).toBe(1);
  });

  it('test2', () => {
    // Depends on test1 running first!
    expect(sharedData.length).toBe(1); // Brittle
  });
});
```

✅ **Good**:
```typescript
describe('MyComponent', () => {
  let component: MyComponent;

  beforeEach(() => {
    // Fresh setup for each test
    component.data = [];
  });
});
```

### 7. Not Destroying Fixtures

❌ **Bad**:
```typescript
describe('MyComponent', () => {
  let fixture: ComponentFixture<MyComponent>;

  beforeEach(() => {
    fixture = TestBed.createComponent(MyComponent);
  });

  // No cleanup - memory leak
});
```

✅ **Good**:
```typescript
describe('MyComponent', () => {
  let fixture: ComponentFixture<MyComponent>;

  beforeEach(() => {
    fixture = TestBed.createComponent(MyComponent);
  });

  afterEach(() => {
    fixture.destroy(); // Clean up
  });
});
```

### 8. Ignoring Async Operations

❌ **Bad**:
```typescript
it('test', () => {
  component.loadData(); // Async operation

  expect(component.data).toBeDefined(); // Fails - data not loaded yet
});
```

✅ **Good**:
```typescript
it('test', fakeAsync(() => {
  component.loadData();
  tick(); // Wait for async

  expect(component.data).toBeDefined();
}));
```

### 9. Generic Test Names

❌ **Bad**:
```typescript
it('works', () => { ... });
it('test1', () => { ... });
it('should work correctly', () => { ... });
```

✅ **Good**:
```typescript
it('should_display_error_message_when_form_invalid', () => { ... });
it('should_emit_selected_item_when_row_clicked', () => { ... });
```

### 10. Not Using TestBed for Angular Features

❌ **Bad**:
```typescript
it('test', () => {
  const component = new MyComponent(mockService); // Manual instantiation
});
```

✅ **Good**:
```typescript
it('test', () => {
  const fixture = TestBed.createComponent(MyComponent);
  const component = fixture.componentInstance;
});
```

## Quick Checklist

Before committing tests:

- [ ] Tests are independent (no shared state)
- [ ] Test names describe behavior and conditions
- [ ] Change detection triggered when testing templates
- [ ] Fixtures destroyed in afterEach
- [ ] Async operations handled (fakeAsync/async/done)
- [ ] Mocking only dependencies, not code under test
- [ ] Testing behavior, not implementation
- [ ] No hard-coded assumptions about DOM structure
- [ ] Subscriptions cleaned up or using done callback
- [ ] TestBed used for Angular dependency injection

## Official Documentation

- [Angular Testing Best Practices](https://angular.io/guide/testing)
- [Common Testing Mistakes](https://angular.io/guide/testing-components-scenarios)

## Related Context Files

- `jest_testing_standards.md` - What TO do
- `component_testing_patterns.md` - Proper component testing
- `service_testing_patterns.md` - Proper service testing
- `testing_utilities.md` - Correct tool usage
