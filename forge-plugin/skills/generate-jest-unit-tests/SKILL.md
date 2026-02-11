---
name: generate-jest-unit-tests
description: Intelligent Jest unit test generation for Angular components, services, and more with Socratic planning and project-specific memory.
version: "0.1.0-alpha"
context:
  primary: [angular]
  topics: [jest_testing_standards, component_testing_patterns, service_testing_patterns, testing_utilities, test_antipatterns, ngrx_patterns, rxjs_patterns]
memory:
  scope: per-project
  files: [testing_patterns.md, expected_behaviors.md, common_mocks.md, framework_config.md]
---

# generate-jest-unit-tests

## Title

**Angular/Jest Unit Test Generator** - Intelligent Jest unit test generation for Angular components, services, and more with Socratic planning and project-specific memory.

## Version

**v1.0.0** - Initial release

## File Structure

### Skill Files
```
forge-plugin/skills/generate-jest-unit-tests/
├── SKILL.md                          # This file
├── examples.md                       # Usage examples
├── scripts/
│   └── test_analyzer.ts              # Helper for analyzing existing tests
└── templates/
    ├── component_test_template.txt   # Component test structure
    ├── service_test_template.txt     # Service test structure
    └── test_case_template.txt        # Individual test case template
```

### Interface References
- [ContextProvider](../../interfaces/context_provider.md) — `getDomainIndex("angular")`, `getConditionalContext("angular", topic)`
- [MemoryStore](../../interfaces/memory_store.md) — `getSkillMemory("generate-jest-unit-tests", project)`, `update()`

### Context (via ContextProvider)
- `contextProvider.getDomainIndex("angular")` — Angular context navigation
- `contextProvider.getConditionalContext("angular", "jest_testing_standards")` — Jest/Angular testing best practices
- `contextProvider.getConditionalContext("angular", "component_testing_patterns")` — Component testing strategies
- `contextProvider.getConditionalContext("angular", "service_testing_patterns")` — Service testing patterns
- `contextProvider.getConditionalContext("angular", "testing_utilities")` — TestBed, mocking, spies, utilities
- `contextProvider.getConditionalContext("angular", "test_antipatterns")` — What to avoid

### Memory (via MemoryStore)
- `memoryStore.getSkillMemory("generate-jest-unit-tests", project)` returns per-project files:
  - `testing_patterns.md` — Project's testing conventions
  - `expected_behaviors.md` — Known expected behaviors
  - `common_mocks.md` — Reusable mocks and test data
  - `framework_config.md` — Jest/TestBed configuration

## Required Reading

### Context & Memory Loading (via Interfaces)

**Before starting any test generation, load resources in this order:**

1. **Project Memory** (via MemoryStore):
   - `memoryStore.getSkillMemory("generate-jest-unit-tests", project)` — loads all per-project files if they exist

2. **Domain Index** (via ContextProvider):
   - `contextProvider.getDomainIndex("angular")` — Angular context navigation

3. **Core Testing Context** (always load via ContextProvider):
   - `contextProvider.getConditionalContext("angular", "jest_testing_standards")` — Core testing principles
   - `contextProvider.getConditionalContext("angular", "testing_utilities")` — TestBed, mocking, spies
   - `contextProvider.getConditionalContext("angular", "test_antipatterns")` — What to avoid

4. **Conditional Context** (load based on code analysis):
   - If component: `contextProvider.getConditionalContext("angular", "component_testing_patterns")`
   - If service: `contextProvider.getConditionalContext("angular", "service_testing_patterns")`
   - If NgRx: `contextProvider.getConditionalContext("angular", "ngrx_patterns")`
   - If RxJS: `contextProvider.getConditionalContext("angular", "rxjs_patterns")`

### Loading Order

**CRITICAL**: Resources must be loaded in this exact order:

```
1. Project memory via memoryStore (load project-specific patterns)
2. Domain index via contextProvider (understand available context)
3. Core context via contextProvider (testing standards, patterns)
4. Conditional context via contextProvider (based on code being tested)
```

## Design Requirements

### Core Principles

1. **Practical Tests**: Generate tests that validate real behavior, not implementation details
2. **Maintainability**: Tests should be easy to understand and update
3. **Non-Brittleness**: Tests should not break on refactoring unless behavior changes
4. **Socratic Planning**: Collaborate with user to understand expected behavior
5. **Project Memory**: Learn and apply project-specific testing patterns
6. **Framework Awareness**: Support Jest, Jasmine/Karma migration, Angular TestBed
7. **Angular-Specific**: Handle components, services, pipes, directives, guards, resolvers

### Test Quality Criteria

Generated tests must:

- ✅ Test component/service behavior, not implementation
- ✅ Have clear, descriptive names (should_X_when_Y)
- ✅ Follow AAA pattern (Arrange, Act, Assert)
- ✅ Be independent and isolated
- ✅ Use appropriate mocking (TestBed, jasmine spies, jest.mock)
- ✅ Handle Angular change detection properly
- ✅ Test observable streams correctly
- ✅ Include meaningful assertions
- ✅ Follow project conventions from memory

### What NOT to Do

- ❌ Test private methods directly
- ❌ Create brittle tests tied to implementation
- ❌ Generate tests without understanding expected behavior
- ❌ Ignore existing project testing patterns
- ❌ Over-mock or under-mock
- ❌ Skip error/edge case scenarios
- ❌ Use generic test names
- ❌ Ignore change detection in component tests
- ❌ Not unsubscribe from observables in tests

## Prompting Guidelines

### User Interaction Phases

**Phase 1: Initial Analysis**
- Identify files to test (components, services, etc.)
- Analyze existing test structure
- Detect testing framework (Jest vs Jasmine/Karma)
- Identify Angular version and patterns

**Phase 2: Socratic Planning** (MANDATORY)
- Ask targeted questions about expected behavior
- Clarify edge cases and error scenarios
- Understand business logic and constraints
- Confirm testing approach

**Phase 3: Test Generation**
- Generate tests based on planning
- Apply project memory patterns
- Follow testing standards

### Socratic Questions Framework

Ask questions in these categories:

1. **Component Behavior** (for components):
   - "What should be displayed when [input changes]?"
   - "How should the component react to [user interaction]?"
   - "What should be emitted when [event occurs]?"
   - "What lifecycle hooks are critical to test?"

2. **Service Behavior** (for services):
   - "What should the service return when [method called]?"
   - "How should errors be handled?"
   - "Should HTTP calls be mocked?"
   - "What observables need testing?"

3. **Dependencies & Integration**:
   - "Should I create mock components for child components?"
   - "Which services should be mocked vs real?"
   - "Are there Router/ActivatedRoute dependencies?"
   - "Does this use NgRx/state management?"

4. **Angular-Specific**:
   - "Should I test with OnPush change detection?"
   - "Are there template-driven or reactive forms?"
   - "Does this component use @ViewChild/@ContentChild?"
   - "Are there async operations to handle?"

5. **Test Approach**:
   - "Shallow vs deep rendering for this component?"
   - "Should I use TestBed or standalone component testing?"
   - "Are there specific edge cases you're concerned about?"

## Instructions

### Mandatory Workflow (8 Steps)

This workflow is **MANDATORY** and **NON-NEGOTIABLE**. Every step must be completed in order.

---

#### Step 1: Initial Analysis

**Purpose**: Gather information about what needs to be tested.

**Actions**:
1. Identify the Angular file(s) to test (component, service, pipe, directive, guard)
2. Determine the project name from git repository or directory structure
3. Check if tests already exist for the target files
4. Identify the testing framework (Jest vs Jasmine/Karma)
5. Detect Angular version (standalone components vs NgModule)
6. List the classes/functions/methods that need test coverage
7. Identify dependencies (services, router, HTTP, state management)

**Validation**:
- [ ] Target files identified and type determined (component/service/etc.)
- [ ] Project name determined
- [ ] Testing framework detected (Jest or Jasmine)
- [ ] Angular version and patterns identified
- [ ] Dependencies listed

---

#### Step 2: Load Index Files

**Purpose**: Understand what memory and context is available.

**Actions**:
1. Load Angular domain index via `contextProvider.getDomainIndex("angular")`
2. Identify which context topics will be needed based on file types

**Validation**:
- [ ] Domain index loaded
- [ ] Angular context map understood
- [ ] Relevant topics identified

---

#### Step 3: Load Project Memory

**Purpose**: Load project-specific testing patterns and conventions.

**Actions**:
1. Load project memory via `memoryStore.getSkillMemory("generate-jest-unit-tests", project)`
2. If memory exists, review all files:
   - `testing_patterns.md` - Project's testing conventions
   - `expected_behaviors.md` - Known expected behaviors
   - `common_mocks.md` - Reusable mocks and test data
   - `framework_config.md` - Jest/TestBed configuration
3. If no memory exists, note that this is a new project (memory will be created later)

**Validation**:
- [ ] Project memory checked
- [ ] Existing patterns loaded (if available)
- [ ] Ready to create new memory (if needed)

---

#### Step 4: Load Context

**Purpose**: Load testing standards and best practices.

**Actions**:
1. **Always load**:
   - `contextProvider.getConditionalContext("angular", "jest_testing_standards")`
   - `contextProvider.getConditionalContext("angular", "testing_utilities")`
   - `contextProvider.getConditionalContext("angular", "test_antipatterns")`

2. **Conditionally load** (based on file type):
   - If component: `contextProvider.getConditionalContext("angular", "component_testing_patterns")`
   - If service: `contextProvider.getConditionalContext("angular", "service_testing_patterns")`
   - If using NgRx: `contextProvider.getConditionalContext("angular", "ngrx_patterns")`
   - If using RxJS heavily: `contextProvider.getConditionalContext("angular", "rxjs_patterns")`
   - Use domain index from Step 2 as guide

**Validation**:
- [ ] Core testing context loaded
- [ ] Type-specific context loaded (component/service)
- [ ] Framework-specific context loaded (if needed)
- [ ] Ready to apply testing standards

---

#### Step 5: Analyze Files to Test

**Purpose**: Understand the code structure and dependencies.

**Actions**:
1. Read the target TypeScript file(s) completely
2. Identify:
   - Public methods/properties (primary test targets)
   - Input/Output properties (for components)
   - Component template interactions (for components)
   - Service dependencies (injected via constructor)
   - Observable streams and subscriptions
   - Lifecycle hooks (ngOnInit, ngOnDestroy, etc.)
   - Error handling patterns
   - Complexity and edge cases
3. Read existing tests (if any) to understand coverage gaps
4. Analyze project structure to determine test file location
5. Identify change detection strategy (OnPush vs Default)

**Validation**:
- [ ] Target code thoroughly understood
- [ ] Dependencies identified
- [ ] Observable patterns noted
- [ ] Edge cases identified
- [ ] Test file location determined

---

#### Step 6: Socratic Planning Phase

**Purpose**: Collaborate with the user to understand expected behavior.

**CRITICAL**: This step is MANDATORY. You MUST ask the user questions before generating tests.

**Actions**:
1. Present a summary of what you analyzed
2. Ask targeted questions using the Socratic Questions Framework:
   - **Component questions**: Inputs, outputs, user interactions, display logic
   - **Service questions**: Return values, error handling, HTTP mocking
   - **Dependency questions**: What to mock, router usage, state management
   - **Angular-specific questions**: Change detection, forms, ViewChild
   - **Testing approach questions**: Shallow vs deep, TestBed setup
3. Wait for user responses
4. Use AskUserQuestion tool for structured multi-choice questions when appropriate
5. Clarify ambiguities and confirm understanding

**Example Questions**:
```
I analyzed `UserProfileComponent` and found the following to test:

Component:
- @Input() userId: string
- @Output() profileUpdated = new EventEmitter<Profile>()
- Displays user profile data from UserService
- Has edit form with validation
- Uses OnPush change detection

Before generating tests, I need to understand the expected behavior:

1. **For profile loading**:
   - Should I mock UserService.getProfile()?
   - What should display while loading (spinner, placeholder)?
   - How should it handle when userId is null/undefined?

2. **For profile editing**:
   - What validations should I test (email format, required fields)?
   - Should the form be disabled during save?
   - What happens on save success vs error?

3. **For profileUpdated output**:
   - When exactly should this emit (on save success)?
   - What data should be emitted?

4. **Dependencies**:
   - Mock UserService completely or use real service?
   - Any router navigation to test?

5. **Testing approach**:
   - Should I test with shallow rendering (mock child components)?
   - Test template-driven or reactive form validation?
```

**Validation**:
- [ ] Summary presented to user
- [ ] At least 3-5 meaningful questions asked
- [ ] User responses received
- [ ] Expected behaviors clarified
- [ ] Testing approach confirmed

---

#### Step 7: Generate Unit Tests

**Purpose**: Create comprehensive, maintainable unit tests.

**Actions**:
1. Create test file following project conventions:
   - File naming: `{filename}.spec.ts` (standard Angular convention)
   - Location: Co-located with source file or in separate test directory
2. Apply templates from `./templates/`
3. For each component/service/class:
   - Generate setup code (describe block, TestBed configuration)
   - Generate happy path tests
   - Generate edge case tests
   - Generate error scenario tests
   - Use AAA pattern (Arrange, Act, Assert)
4. Include:
   - Descriptive test names (should_X_when_Y)
   - Appropriate mocks (jasmine.createSpyObj, jest.mock)
   - Proper TestBed configuration
   - Change detection triggers (for components)
   - Observable testing (async/fakeAsync/done)
   - Cleanup (unsubscribe, destroy)
5. Apply project memory patterns and user's clarified behaviors
6. Follow Jest vs Jasmine conventions based on detected framework

**Component-Specific**:
- Mock dependencies via TestBed providers
- Test template interactions (query selectors, click events)
- Test Input/Output properties
- Handle change detection (detectChanges, tick, flush)
- Mock child components if shallow rendering

**Service-Specific**:
- Mock HTTP calls (HttpTestingController for Jasmine, jest.mock for Jest)
- Test observable streams (subscribe, toPromise, firstValueFrom)
- Test error handling
- Test caching/state management

**Validation**:
- [ ] Test file created in correct location
- [ ] TestBed properly configured
- [ ] All public methods have test coverage
- [ ] Happy paths tested
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] Change detection handled (components)
- [ ] Observables tested properly
- [ ] Mocks configured correctly
- [ ] Project conventions followed
- [ ] User's expected behaviors implemented

---

#### Step 8: Update Project Memory

**Purpose**: Store learned patterns for future test generation.

**Actions**:
1. Use `memoryStore.update("generate-jest-unit-tests", project, filename, content)` for each file
2. Create or update memory files:
   - **testing_patterns.md**: Document testing conventions observed/established
     - Test file location pattern
     - Naming conventions
     - Testing framework (Jest vs Jasmine) and version
     - TestBed configuration patterns
     - Mock creation patterns
     - Common test structure
   - **expected_behaviors.md**: Document clarified behaviors from Socratic phase
     - Component behaviors confirmed with user
     - Service response patterns
     - Error handling rules
     - Edge case handling
   - **common_mocks.md**: Document reusable mocks created
     - Mock components
     - Mock services
     - Mock data/fixtures
     - Spy configurations
   - **framework_config.md**: Document testing framework configuration
     - jest.config.js patterns
     - TestBed common configurations
     - Custom test utilities
     - Test setup files

**Validation**:
- [ ] Project memory directory exists
- [ ] testing_patterns.md created/updated
- [ ] expected_behaviors.md created/updated
- [ ] common_mocks.md created/updated
- [ ] framework_config.md created/updated

---

## Compliance Checklist

Before completing the skill invocation, verify ALL items:

### Workflow Compliance
- [ ] Step 1: Initial Analysis completed
- [ ] Step 2: Index files loaded
- [ ] Step 3: Project memory loaded
- [ ] Step 4: Context loaded
- [ ] Step 5: Files analyzed
- [ ] Step 6: Socratic planning completed (questions asked and answered)
- [ ] Step 7: Tests generated
- [ ] Step 8: Memory updated

### Test Quality
- [ ] Tests follow AAA pattern
- [ ] Test names are descriptive
- [ ] Appropriate mocking used (TestBed, spies)
- [ ] Change detection handled (components)
- [ ] Observables tested properly
- [ ] Edge cases covered
- [ ] Error scenarios covered
- [ ] Tests are independent
- [ ] Project conventions followed

### Angular-Specific
- [ ] TestBed configured correctly
- [ ] Dependencies mocked appropriately
- [ ] Component fixtures created and managed
- [ ] Change detection triggered when needed
- [ ] Async operations handled (async/fakeAsync)
- [ ] Subscriptions cleaned up

### Memory & Context
- [ ] Project memory checked and loaded
- [ ] New patterns documented in memory
- [ ] User-clarified behaviors stored
- [ ] Testing context applied

### User Collaboration
- [ ] Socratic questions asked (minimum 3-5)
- [ ] User responses incorporated
- [ ] Expected behaviors confirmed

## Best Practices

### Test Organization

1. **File Structure**:
   - Co-locate tests with source: `user.service.ts` → `user.service.spec.ts`
   - Or separate directory: `src/app/services/` → `src/app/services/tests/`
   - Group related tests in describe blocks

2. **Test Naming**:
   - `should_{expected_behavior}_when_{condition}`
   - Be specific and descriptive
   - Use clear describe block structure

3. **Test Independence**:
   - Each test should run independently
   - Use beforeEach for setup
   - Use afterEach for cleanup
   - Don't share state between tests

### Angular Testing Patterns

**Components**:
```typescript
describe('UserProfileComponent', () => {
  let component: UserProfileComponent;
  let fixture: ComponentFixture<UserProfileComponent>;
  let mockUserService: jasmine.SpyObj<UserService>;

  beforeEach(async () => {
    mockUserService = jasmine.createSpyObj('UserService', ['getProfile', 'updateProfile']);

    await TestBed.configureTestingModule({
      declarations: [UserProfileComponent],
      providers: [
        { provide: UserService, useValue: mockUserService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(UserProfileComponent);
    component = fixture.componentInstance;
  });

  it('should_load_user_profile_when_userId_provided', () => {
    // Arrange
    const mockProfile = { id: '123', name: 'Test User' };
    mockUserService.getProfile.and.returnValue(of(mockProfile));
    component.userId = '123';

    // Act
    fixture.detectChanges(); // Trigger ngOnInit

    // Assert
    expect(component.profile).toEqual(mockProfile);
    expect(mockUserService.getProfile).toHaveBeenCalledWith('123');
  });
});
```

**Services**:
```typescript
describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });
    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should_return_user_when_getProfile_called', () => {
    const mockUser = { id: '123', name: 'Test' };

    service.getProfile('123').subscribe(user => {
      expect(user).toEqual(mockUser);
    });

    const req = httpMock.expectOne('/api/users/123');
    expect(req.request.method).toBe('GET');
    req.flush(mockUser);
  });
});
```

### Mocking Strategy

1. **What to Mock**:
   - External HTTP services (use HttpTestingController)
   - Child components (use MockComponent or NO_ERRORS_SCHEMA)
   - Router (use jasmine.createSpyObj)
   - Services (use jasmine.createSpyObj or jest.mock)
   - NgRx Store (use provideMockStore)

2. **What NOT to Mock**:
   - Component/service under test
   - Simple TypeScript classes
   - Pure functions
   - Angular built-ins (unless necessary)

### Observable Testing

```typescript
// Using async
it('should_emit_value_when_observable_completes', async(() => {
  service.getData().subscribe(data => {
    expect(data).toBe('test');
  });
}));

// Using fakeAsync and tick
it('should_emit_after_delay', fakeAsync(() => {
  let result: string;
  service.getDelayedData().subscribe(data => result = data);

  tick(1000);

  expect(result).toBe('delayed');
}));

// Using done callback
it('should_complete_successfully', (done) => {
  service.getData().subscribe({
    next: data => expect(data).toBe('test'),
    complete: done
  });
});
```

### Change Detection

```typescript
// Trigger change detection
fixture.detectChanges();

// For OnPush components
component.changeDetectorRef.markForCheck();
fixture.detectChanges();

// Wait for async operations
await fixture.whenStable();

// In fakeAsync
tick();
fixture.detectChanges();
```

## Additional Notes

### Testing Frameworks

**Jest** (preferred for new projects):
- Fast execution
- Built-in mocking
- Snapshot testing
- Better TypeScript support
- Less boilerplate

**Jasmine/Karma** (Angular default):
- Traditional Angular testing
- Runs in real browser
- Good for E2E-like tests
- More verbose

### Migration Considerations

When migrating from Jasmine to Jest:
- Replace `jasmine.createSpyObj` with `jest.fn()`
- Replace `spyOn().and.returnValue()` with `jest.spyOn().mockReturnValue()`
- Replace `HttpTestingController` with `jest.mock()`
- Update test configuration

### Integration with Other Skills

- **Before testing**: Use `skill:angular-code-review` to understand code quality
- **After testing**: Review generated tests with `skill:angular-code-review`
- **For changes**: Use `skill:get-git-diff` to see what changed and needs new tests

### Common Patterns

**Mock Component**:
```typescript
@Component({
  selector: 'app-child',
  template: ''
})
class MockChildComponent {
  @Input() data: any;
  @Output() action = new EventEmitter();
}
```

**Spy Object**:
```typescript
const mockService = jasmine.createSpyObj('MyService', ['method1', 'method2'], {
  property: 'value'
});
```

**Test Async Pipe**:
```typescript
it('should_display_async_data', fakeAsync(() => {
  component.data$ = of('test data');
  fixture.detectChanges();
  tick();

  const element = fixture.nativeElement.querySelector('.data');
  expect(element.textContent).toContain('test data');
}));
```

## Version History

### v1.1.0 (2025-07-15)
- Phase 4 Migration: Replaced hardcoded `../../context/` and `../../memory/` paths with ContextProvider and MemoryStore interface calls
- Added YAML frontmatter with context/memory declarations
- Added Interface References section
- Updated workflow steps to use contextProvider/memoryStore

### v1.0.0 (2025-11-18)
- Initial release
- Mandatory 8-step workflow
- Socratic planning phase
- Project-specific memory system
- Centralized context integration
- Support for Jest and Jasmine/Karma
- Component and service test generation
- Template-based test generation
