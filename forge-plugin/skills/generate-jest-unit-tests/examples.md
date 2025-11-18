# generate-jest-unit-tests Examples

## Usage Scenarios

This document provides practical examples of using the `generate-jest-unit-tests` skill for Angular components, services, and other Angular artifacts.

## Example 1: Basic Component Testing

### Scenario
You have a display component that shows user information and needs comprehensive tests.

### User Request
```
Please use skill:generate-jest-unit-tests to create tests for src/app/components/user-card/user-card.component.ts
```

### Skill Workflow

**Step 1-5**: Initial analysis and context loading
- Identifies `UserCardComponent` with inputs: `user: User`, outputs: `cardClicked: EventEmitter<User>`
- Loads project memory (first time, so empty)
- Loads testing context (jest_testing_standards.md, component_testing_patterns.md)
- Analyzes the component code

**Step 6**: Socratic Planning
```
I analyzed UserCardComponent and found the following to test:

Component Structure:
- @Input() user: User
- @Output() cardClicked = new EventEmitter<User>()
- Displays user avatar, name, email
- Click handler emits cardClicked event
- Uses OnPush change detection

Before generating tests, I need to understand the expected behavior:

1. **For user input**:
   - How should the component handle when user is null/undefined?
   - Are there default values to display?
   - Should it validate user data?

2. **For display logic**:
   - What should show when user.avatar is missing (default avatar)?
   - How should long names be handled (truncation)?
   - Any conditional rendering based on user properties?

3. **For cardClicked event**:
   - Should clicking anywhere on the card emit the event?
   - Should it emit when user is null?
   - Any debouncing or throttling?

4. **Testing approach**:
   - Should I test the template (shallow rendering)?
   - Mock any child components?
```

**User Response**:
```
1. user null/undefined should show placeholder text "No user selected"
2. Missing avatar should show default avatar from assets
   Long names should be truncated with ellipsis (CSS)
3. Click anywhere emits the event, but not if user is null
4. Yes, test template. No child components to mock
```

**Step 7**: Generate tests based on clarified behavior
- Creates `user-card.component.spec.ts`
- Tests input handling (valid user, null user)
- Tests template rendering (name, email, avatar display)
- Tests click event emission
- Tests OnPush change detection

**Step 8**: Update memory
- Creates project memory documenting:
  - Test file location: co-located with component
  - Use Jest as testing framework
  - Components use OnPush change detection
  - Stores the clarified behaviors (null handling, default avatar, click event rules)

---

## Example 2: Service with HTTP Dependencies

### Scenario
Testing a service that makes HTTP calls to a REST API.

### User Request
```
I need tests for UserService in src/app/services/user.service.ts. Use skill:generate-jest-unit-tests
```

### Skill Workflow

**Step 1-5**: Analysis
- Identifies `UserService` with methods: `getUser(id)`, `updateUser(user)`, `deleteUser(id)`
- Detects HttpClient dependency
- Loads existing project memory (second time using skill)
- Loads service_testing_patterns.md context

**Step 6**: Socratic Planning
```
I analyzed UserService and found HTTP-dependent methods. Clarifications needed:

1. **HTTP testing approach**:
   - Should I use HttpTestingController (Jasmine) or jest.mock (Jest)?
   - Based on project memory, you're using Jest - confirm?

2. **For getUser(id)**:
   - What should happen when user not found (404)?
   - Should it retry on network errors?
   - Return type: Observable<User> or Promise<User>?

3. **For updateUser(user)**:
   - What validations happen before HTTP call?
   - How should 400/500 errors be handled?
   - Should it update local cache after success?

4. **For deleteUser(id)**:
   - Confirmation dialog or direct delete?
   - What happens if delete fails?
   - Should it clear related data?

5. **Error handling**:
   - Custom error types or standard HttpErrorResponse?
   - Should errors be transformed/mapped?
```

**User Response**:
```
1. Use jest.mock for HttpClient
2. getUser returns Observable<User>, 404 should return null,
   no retry logic, errors propagate as-is
3. updateUser validates user.id exists, throws error if not
   400/500 errors propagate, no local cache
4. Direct delete (no dialog in service), errors propagate,
   no cleanup in service (handled by caller)
5. Standard HttpErrorResponse, errors propagate without transformation
```

**Step 7**: Generate tests
- Creates `user.service.spec.ts`
- Mocks HttpClient using jest.mock
- Tests each method with happy path
- Tests 404 handling for getUser
- Tests validation error for updateUser
- Tests HTTP errors for all methods
- Uses RxJS testing patterns (subscribe, firstValueFrom)

**Step 8**: Update memory
- Documents HTTP mocking pattern with jest.mock
- Records service error handling rules
- Stores that services don't handle UI concerns (dialogs, cache)
- Updates expected_behaviors.md with API response patterns

---

## Example 3: Component with NgRx Store

### Scenario
Testing a component that uses NgRx for state management.

### User Request
```
Generate tests for the ProductListComponent that uses NgRx. Use skill:generate-jest-unit-tests
```

### Skill Workflow

**Step 1-5**: Analysis
- Identifies `ProductListComponent` with Store dependency
- Detects NgRx actions dispatched: `loadProducts`, `selectProduct`
- Detects selectors used: `selectAllProducts`, `selectLoading`
- Loads ngrx_patterns.md context

**Step 6**: Socratic Planning
```
I found ProductListComponent using NgRx Store. Need clarification:

Component Structure:
- Injects Store<AppState>
- Dispatches loadProducts on init
- Subscribes to selectAllProducts selector
- Dispatches selectProduct(id) on product click
- Shows loading spinner based on selectLoading

Questions:

1. **Store testing approach**:
   - Should I use provideMockStore from @ngrx/store/testing?
   - Mock selectors with specific values?

2. **For loadProducts action**:
   - Should it dispatch immediately in ngOnInit?
   - Any conditions for dispatching (auth check)?

3. **For product selection**:
   - What happens when product is clicked (dispatch selectProduct)?
   - Should it navigate to product detail?
   - Any validation before dispatching?

4. **For loading state**:
   - How should loading spinner be tested?
   - Should products list be hidden while loading?
   - Test loading → loaded → error states?

5. **Observable subscriptions**:
   - Should I test that subscriptions are cleaned up on destroy?
   - Using async pipe or manual subscribe?
```

**User Response**:
```
1. Yes, use provideMockStore with initial state
2. Dispatch loadProducts immediately in ngOnInit, no conditions
3. Click dispatches selectProduct and navigates to /product/:id
   No validation needed
4. Yes test all three states (loading, loaded, error)
   Products hidden while loading
5. Using async pipe, so no manual cleanup needed
```

**Step 7**: Generate tests
- Creates `product-list.component.spec.ts`
- Uses provideMockStore from @ngrx/store/testing
- Mocks selectors (selectAllProducts, selectLoading, selectError)
- Tests action dispatching (loadProducts in ngOnInit)
- Tests template rendering based on selector values
- Tests navigation on product click
- Tests loading/error state display

**Step 8**: Update memory
- Documents NgRx testing pattern with provideMockStore
- Records that components use async pipe (no manual unsubscribe)
- Stores navigation pattern for entity selection
- Notes loading/error state display conventions

---

## Example 4: Reactive Form Testing

### Scenario
Testing a component with complex reactive form validation.

### User Request
```
Create tests for src/app/forms/registration-form/registration-form.component.ts using skill:generate-jest-unit-tests
```

### Skill Workflow

**Step 1-5**: Analysis
- Identifies `RegistrationFormComponent` with FormBuilder dependency
- Form has fields: username, email, password, confirmPassword
- Custom validators: passwordMatch, usernameAvailability (async)
- Form submission emits registrationData

**Step 6**: Socratic Planning
```
I found RegistrationFormComponent with reactive forms. Questions:

Form Structure:
- Fields: username, email, password, confirmPassword
- Validators: required, email format, password strength, password match
- Async validator: username availability check
- Submit button disabled when form invalid

Clarifications needed:

1. **For username field**:
   - Min/max length requirements?
   - Allowed characters (alphanumeric only)?
   - Async validation: debounce time?
   - What to show during async validation check?

2. **For password field**:
   - Password strength rules (min length, complexity)?
   - Show strength indicator?
   - Any forbidden passwords (common passwords list)?

3. **For confirmPassword**:
   - When should password match validation trigger?
   - Clear error when passwords start matching?

4. **For form submission**:
   - What data is emitted (all fields or subset)?
   - Should form reset after successful submission?
   - Disable form during submission?

5. **Testing approach**:
   - Test validators individually or through form controls?
   - Mock async username check service?
   - Test template (error messages, disabled states)?
```

**User Response**:
```
1. Username: 3-20 chars, alphanumeric + underscore only
   Async check: 500ms debounce, show spinner during check
2. Password: min 8 chars, requires uppercase, lowercase, number
   No strength indicator, no forbidden list
3. Password match: validate on confirmPassword value change
   Clear error when match
4. Emit {username, email, password} (exclude confirmPassword)
   Reset form after emit, disable during submission
5. Test validators through form, mock username service,
   yes test template for errors and disabled states
```

**Step 7**: Generate tests
- Creates `registration-form.component.spec.ts`
- Tests form initialization
- Tests each validator (required, email, password strength, match)
- Tests async username validator with fakeAsync/tick
- Tests form submission with valid/invalid data
- Tests template (error messages, disabled submit button)
- Tests form reset after submission

**Step 8**: Update memory
- Documents reactive form testing patterns
- Records validation rules for registration
- Stores async validator pattern with debounce
- Notes form reset behavior after submission

---

## Example 5: Pipe Testing

### Scenario
Testing a custom pipe that formats currency.

### User Request
```
Generate tests for shared/pipes/currency-format.pipe.ts using skill:generate-jest-unit-tests
```

### Skill Workflow

**Step 1-5**: Analysis
- Identifies `CurrencyFormatPipe` implementing PipeTransform
- Method: `transform(value: number, currencyCode?: string)`
- Returns formatted currency string

**Step 6**: Socratic Planning
```
I found CurrencyFormatPipe for currency formatting. Questions:

Pipe Signature:
- transform(value: number, currencyCode = 'USD'): string

Clarifications:

1. **For currency formatting**:
   - Which currency codes should be supported (USD, EUR, GBP, etc.)?
   - Decimal places (always 2 for USD)?
   - Thousand separators (comma for US)?

2. **For edge cases**:
   - How to handle null/undefined value?
   - How to handle negative numbers?
   - How to handle very large numbers?
   - Invalid currency codes?

3. **Locale handling**:
   - Use browser locale or fixed locale (en-US)?
   - Different format for different currencies?

4. **Testing approach**:
   - Test pipe in isolation or through component?
   - Need to mock Intl.NumberFormat?
```

**User Response**:
```
1. Support USD, EUR, GBP
   2 decimal places for all
   Use standard thousand separators per currency
2. null/undefined returns empty string
   Negative numbers show with minus sign: -$10.00
   Large numbers format normally
   Invalid currency defaults to USD
3. Use 'en-US' locale for consistency
   Currency symbol position varies by code ($ before, € after)
4. Test pipe in isolation (no component needed)
   No mocking needed, use real Intl.NumberFormat
```

**Step 7**: Generate tests
- Creates `currency-format.pipe.spec.ts`
- Tests basic formatting for different currencies
- Tests edge cases (null, undefined, negative, large numbers)
- Tests invalid currency code fallback
- Tests decimal places and thousand separators

**Step 8**: Update memory
- Documents pipe testing pattern (simple instantiation)
- Records currency formatting rules
- Stores edge case handling for pipes
- Notes that pipes are tested in isolation

---

## Key Patterns

### Common Themes Across Examples

1. **Always ask before generating**: Socratic planning prevents assumptions
2. **Load project memory**: Maintain consistency with existing tests
3. **Context guides quality**: Testing standards ensure best practices
4. **Update memory after**: Each invocation improves future generations
5. **User collaboration**: Tests reflect actual expected behavior

### When to Use This Skill

- ✅ Creating new tests for untested Angular code
- ✅ Expanding test coverage for components/services
- ✅ Refactoring tests to be more maintainable
- ✅ Standardizing test structure across project
- ✅ Learning project-specific testing patterns

### When NOT to Use This Skill

- ❌ Just running existing tests (use ng test directly)
- ❌ Debugging failing tests (use regular Claude Code interaction)
- ❌ Generating E2E tests (different skill needed)
- ❌ Simple one-line pipes that don't need tests

---

## Tips for Best Results

1. **Be specific in your request**:
   - Good: "Generate tests for UserProfileComponent"
   - Better: "Generate tests for UserProfileComponent including form validation and HTTP error handling"

2. **Provide context**:
   - Mention testing framework if not Jest (e.g., "using Jasmine/Karma")
   - Note any special requirements (NgRx, reactive forms, async operations)
   - Share relevant documentation or specs

3. **Engage in Socratic planning**:
   - Answer questions thoroughly
   - Provide examples of expected behavior
   - Clarify edge cases and error scenarios

4. **Review generated tests**:
   - Ensure they match your understanding
   - Request adjustments if needed
   - Run tests and provide feedback

5. **Build project memory**:
   - Use the skill multiple times on the same project
   - Patterns will be learned and applied automatically
   - Tests will become more consistent over time

---

## Angular-Specific Examples

### Testing @ViewChild

```typescript
it('should_access_child_element_after_view_init', () => {
  fixture.detectChanges();

  expect(component.childElement).toBeDefined();
  expect(component.childElement.nativeElement.textContent).toContain('Expected');
});
```

### Testing Router Navigation

```typescript
it('should_navigate_to_detail_when_item_clicked', () => {
  const router = TestBed.inject(Router);
  const navigateSpy = spyOn(router, 'navigate');

  component.onItemClick('123');

  expect(navigateSpy).toHaveBeenCalledWith(['/detail', '123']);
});
```

### Testing Observable with async Pipe

```typescript
it('should_display_data_from_observable', fakeAsync(() => {
  component.data$ = of({ value: 'test' });
  fixture.detectChanges();
  tick();

  const element = fixture.nativeElement.querySelector('.data-display');
  expect(element.textContent).toContain('test');
}));
```

### Testing Component Inputs/Outputs

```typescript
it('should_emit_event_when_button_clicked', () => {
  let emittedValue: string;
  component.itemSelected.subscribe((value: string) => {
    emittedValue = value;
  });

  component.selectItem('test-id');

  expect(emittedValue).toBe('test-id');
});
```

### Testing Lifecycle Hooks

```typescript
it('should_load_data_on_init', () => {
  const service = TestBed.inject(DataService);
  spyOn(service, 'loadData').and.returnValue(of([]));

  fixture.detectChanges(); // Triggers ngOnInit

  expect(service.loadData).toHaveBeenCalled();
});
```
