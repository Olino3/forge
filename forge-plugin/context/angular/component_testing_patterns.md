---
id: "angular/component_testing_patterns"
domain: angular
title: "Angular Component Testing Patterns"
type: pattern
estimatedTokens: 500
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Quick Reference"
    estimatedTokens: 32
    keywords: [quick, reference]
  - name: "Testing Patterns"
    estimatedTokens: 108
    keywords: [testing, patterns]
  - name: "Mocking Strategies"
    estimatedTokens: 64
    keywords: [mocking, strategies]
  - name: "Form Testing"
    estimatedTokens: 32
    keywords: [form, testing]
  - name: "Official Documentation"
    estimatedTokens: 10
    keywords: [official, documentation]
  - name: "Related Context Files"
    estimatedTokens: 18
    keywords: [related, context, files]
tags: [angular, testing, components, testbed, fixtures, mocking]
---

# Angular Component Testing Patterns

## Quick Reference

### Basic Component Test Setup

```typescript
describe('MyComponent', () => {
  let component: MyComponent;
  let fixture: ComponentFixture<MyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MyComponent],
      imports: [...],
      providers: [...]
    }).compileComponents();

    fixture = TestBed.createComponent(MyComponent);
    component = fixture.componentInstance;
  });

  afterEach(() => {
    fixture.destroy();
  });
});
```

## Testing Patterns

### 1. Input Properties

```typescript
it('should_update_display_when_input_changes', () => {
  component.user = { name: 'John' };
  fixture.detectChanges();

  const element = fixture.debugElement.query(By.css('.name'));
  expect(element.nativeElement.textContent).toContain('John');
});
```

### 2. Output Properties

```typescript
it('should_emit_event_when_button_clicked', () => {
  let emittedValue: any;
  component.itemSelected.subscribe(value => emittedValue = value);

  component.selectItem('test');

  expect(emittedValue).toBe('test');
});
```

### 3. Template Rendering

```typescript
it('should_display_correct_elements', () => {
  fixture.detectChanges();

  const title = fixture.debugElement.query(By.css('h1'));
  expect(title.nativeElement.textContent).toContain('Expected Title');
});
```

### 4. User Interactions

```typescript
it('should_handle_click_event', () => {
  fixture.detectChanges();
  const button = fixture.debugElement.query(By.css('button'));

  button.nativeElement.click();
  fixture.detectChanges();

  expect(component.clicked).toBe(true);
});
```

### 5. Lifecycle Hooks

```typescript
it('should_initialize_on_init', () => {
  spyOn(component, 'loadData');

  fixture.detectChanges(); // Triggers ngOnInit

  expect(component.loadData).toHaveBeenCalled();
});
```

### 6. Change Detection

```typescript
// Default change detection
fixture.detectChanges();

// OnPush change detection
component.changeDetectorRef.markForCheck();
fixture.detectChanges();

// Wait for async operations
await fixture.whenStable();
```

### 7. Async Operations

```typescript
import { fakeAsync, tick } from '@angular/core/testing';

it('should_update_after_delay', fakeAsync(() => {
  component.delayedUpdate();
  tick(1000);

  expect(component.value).toBe('updated');
}));
```

## Mocking Strategies

### Mock Child Components

```typescript
@Component({ selector: 'app-child', template: '' })
class MockChildComponent {
  @Input() data: any;
  @Output() action = new EventEmitter();
}

// In TestBed
declarations: [ParentComponent, MockChildComponent]
```

### Use NO_ERRORS_SCHEMA

```typescript
import { NO_ERRORS_SCHEMA } from '@angular/core';

await TestBed.configureTestingModule({
  declarations: [MyComponent],
  schemas: [NO_ERRORS_SCHEMA] // Ignores unknown elements
}).compileComponents();
```

### Mock Services

```typescript
// Jest
const mockService = {
  getData: jest.fn().mockReturnValue(of([]))
} as any;

// Jasmine
const mockService = jasmine.createSpyObj('MyService', ['getData']);
mockService.getData.and.returnValue(of([]));

// In providers
providers: [{ provide: MyService, useValue: mockService }]
```

## Form Testing

### Reactive Forms

```typescript
it('should_validate_required_field', () => {
  const control = component.form.get('email');

  control?.setValue('');
  expect(control?.hasError('required')).toBe(true);

  control?.setValue('test@example.com');
  expect(control?.valid).toBe(true);
});
```

### Template-Driven Forms

```typescript
it('should_show_validation_error', () => {
  const input = fixture.debugElement.query(By.css('input'));
  input.nativeElement.value = '';
  input.nativeElement.dispatchEvent(new Event('blur'));
  fixture.detectChanges();

  const error = fixture.debugElement.query(By.css('.error'));
  expect(error).toBeTruthy();
});
```

## Official Documentation

- [Angular Component Testing](https://angular.io/guide/testing-components-basics)
- [Angular Component Scenarios](https://angular.io/guide/testing-components-scenarios)
- [TestBed API](https://angular.io/api/core/testing/TestBed)
- [ComponentFixture API](https://angular.io/api/core/testing/ComponentFixture)

## Related Context Files

- `jest_testing_standards.md` - Core testing principles
- `service_testing_patterns.md` - Service mocking
- `testing_utilities.md` - TestBed, spies, async utilities
- `test_antipatterns.md` - What to avoid
