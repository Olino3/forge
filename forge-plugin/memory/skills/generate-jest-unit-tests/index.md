# Memory Structure: generate-jest-unit-tests

## Purpose

This directory stores **project-specific** testing patterns, expected behaviors, and conventions learned during Angular Jest/Jasmine unit test generation. Each project gets its own subdirectory to maintain isolated, project-specific knowledge.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/angular/`): **Shared, static** testing standards (Jest vs Jasmine, TestBed patterns, component testing)
- **Memory** (this directory): **Project-specific, dynamic** testing patterns (this project's test location, mocks, expected behaviors)

**Example**:
- Context says: "Use TestBed.configureTestingModule for component tests"
- Memory records: "In this project, tests use Jest with co-located spec files, all HTTP mocks use jest.fn(), components use OnPush so always call markForCheck()"

## Directory Structure

```
generate-jest-unit-tests/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── testing_patterns.md     # Test file conventions and framework setup
    ├── expected_behaviors.md   # User-clarified behaviors and business logic
    ├── common_mocks.md         # Reusable mocks and test data
    └── framework_config.md     # Jest/Jasmine configuration details
```

## Memory Files

### 1. `testing_patterns.md`

**What to store**:
- Test file location pattern (co-located, separate test directory)
- Test file naming convention (*.spec.ts vs *.test.ts)
- Testing framework (Jest vs Jasmine/Karma, versions)
- TestBed configuration patterns
- Mock creation patterns (jest.fn vs jasmine.createSpyObj)
- Change detection strategy (OnPush vs Default)
- Common test structure (describe blocks organization)

**Example content**:
```markdown
# Testing Patterns for MyAngularApp

## Test File Structure
- Location: Co-located with source files
- Naming: `{filename}.spec.ts` (Angular standard)
- Example: `user.component.ts` → `user.component.spec.ts`

## Framework
- Jest 29.0
- @angular/core/testing
- No Karma/Jasmine

## TestBed Patterns
- Always use `async()` in beforeEach
- Compile components with `.compileComponents()`
- Destroy fixtures in afterEach

## Mocking Conventions
- Services: `jest.fn().mockReturnValue(of(data))`
- HTTP: Manual jest mocks (no HttpTestingController)
- Child components: MockComponent pattern
- NgRx Store: provideMockStore from @ngrx/store/testing

## Change Detection
- All components use OnPush strategy
- Always call `component.changeDetectorRef.markForCheck()` before `fixture.detectChanges()`
```

### 2. `expected_behaviors.md`

**What to store**:
- User-clarified expected behaviors from Socratic planning
- Component interaction patterns
- Service response formats
- Error scenarios and expected exceptions
- Input validation rules
- Output emission triggers
- Domain-specific behaviors

**Example content**:
```markdown
# Expected Behaviors for MyAngularApp

## UserProfileComponent

### Inputs
- **@Input() userId**: string
  - When null/undefined: Display "No user selected" message
  - When changed: Trigger loadUser() automatically

### Outputs
- **@Output() profileUpdated**: EventEmitter<Profile>
  - Emits after successful profile save
  - Emits the complete updated profile object
  - Does NOT emit on validation errors

### Display Logic
- **Avatar**: Show default avatar from assets/default-avatar.png if user.avatar is empty
- **Loading state**: Show skeleton loader while loading
- **Error state**: Show error message with retry button

### Form Behavior
- **Email validation**: Standard email regex
- **Phone validation**: Optional, format (XXX) XXX-XXXX
- **Save button**: Disabled while saving or form invalid
- **Cancel**: Resets form to original values, does not emit

## UserService

### getUser(id: string)
- Returns: Observable<User | null>
- 404 response: Returns null (not error)
- 500 response: Throws error
- No caching

### updateUser(user: User)
- Validates: user.id must exist
- Returns: Observable<User>
- Success: Returns updated user from server
- Validation errors (400): Propagate as-is
```

### 3. `common_mocks.md`

**What to store**:
- Reusable mock components
- Mock services and spy objects
- Test data factories
- Common fixture configurations
- Shared TestBed setups

**Example content**:
```markdown
# Common Mocks for MyAngularApp

## Mock Components

### MockUserAvatarComponent
```typescript
@Component({
  selector: 'app-user-avatar',
  template: '<div class="mock-avatar"></div>'
})
export class MockUserAvatarComponent {
  @Input() user: User;
  @Input() size: 'sm' | 'md' | 'lg' = 'md';
}
```

## Mock Services

### MockUserService
```typescript
const mockUserService = {
  getUser: jest.fn().mockReturnValue(of(null)),
  updateUser: jest.fn().mockReturnValue(of(mockUser)),
  deleteUser: jest.fn().mockReturnValue(of(void 0))
};
```

### MockAuthService
```typescript
const mockAuthService = {
  currentUser$: new BehaviorSubject<User | null>(null),
  isAuthenticated$: new BehaviorSubject<boolean>(false),
  login: jest.fn(),
  logout: jest.fn()
};
```

## Test Data

### Mock User
```typescript
const mockUser: User = {
  id: '123',
  name: 'Test User',
  email: 'test@example.com',
  avatar: 'avatar.jpg',
  role: 'user'
};
```

### Mock Users List
```typescript
const mockUsers: User[] = [
  { id: '1', name: 'User 1', email: 'user1@example.com' },
  { id: '2', name: 'User 2', email: 'user2@example.com' }
];
```

## Common TestBed Configurations

### Component with Router
```typescript
await TestBed.configureTestingModule({
  declarations: [MyComponent],
  imports: [RouterTestingModule.withRoutes([])],
  providers: []
}).compileComponents();
```

### Component with NgRx
```typescript
await TestBed.configureTestingModule({
  declarations: [MyComponent],
  providers: [
    provideMockStore({ initialState: { feature: { data: [] } } })
  ]
}).compileComponents();
```
```

### 4. `framework_config.md`

**What to store**:
- jest.config.js / jest.config.ts configuration
- Test setup files (setupJest.ts)
- Global mocks and polyfills
- Test coverage settings
- Custom matchers or utilities

**Example content**:
```markdown
# Framework Configuration for MyAngularApp

## jest.config.js
```javascript
module.exports = {
  preset: 'jest-preset-angular',
  setupFilesAfterEnv: ['<rootDir>/setup-jest.ts'],
  testPathIgnorePatterns: ['/node_modules/', '/dist/'],
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/app/**/*.ts',
    '!src/app/**/*.spec.ts',
    '!src/app/**/*.module.ts'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

## setup-jest.ts
```typescript
import 'jest-preset-angular/setup-jest';

// Global mocks
Object.defineProperty(window, 'CSS', {value: null});
Object.defineProperty(window, 'getComputedStyle', {
  value: () => ({
    display: 'none',
    appearance: ['-webkit-appearance']
  })
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});
```

## Custom Test Utilities

### test-utils.ts
```typescript
export function createMockStore<T>(initialState: T): MockStore<T> {
  return provideMockStore({ initialState }).providers[0].useFactory();
}

export function triggerClick(fixture: ComponentFixture<any>, selector: string): void {
  const element = fixture.debugElement.query(By.css(selector));
  element.nativeElement.click();
  fixture.detectChanges();
}
```
```

## Workflow

### When Creating Memory (First Time)

1. **During Step 1 (Initial Analysis)**:
   - Identify project name from Angular workspace or directory
   - Check if `{project-name}/` directory exists
   - If not exists, note that memory will be created in Step 8

2. **During Step 3 (Load Project Memory)**:
   - If directory doesn't exist: Note this is the first time
   - Continue with empty memory

3. **During Step 8 (Update Memory)**:
   - Create `{project-name}/` directory
   - Create all four memory files with initial content
   - Document patterns observed during generation
   - Store user-clarified behaviors from Socratic phase

### When Using Existing Memory (Subsequent Times)

1. **During Step 3 (Load Project Memory)**:
   - Read all existing memory files
   - Use patterns to guide test generation
   - Apply known expected behaviors

2. **During Step 8 (Update Memory)**:
   - **Append** new patterns discovered
   - **Update** existing patterns if they've evolved
   - **Add** new expected behaviors learned
   - **Expand** mock library with new reusable mocks

## Memory Evolution

Memory should grow and improve over time:

### First Invocation
- Establish basic patterns (Jest vs Jasmine, file location)
- Document initial expected behaviors from user
- Create first mocks and test data

### Subsequent Invocations
- Refine TestBed configuration patterns
- Add new expected behaviors for new features
- Expand mock component/service library
- Update framework config as project evolves

### Maintenance
- Keep memory files concise and relevant
- Remove outdated mocks
- Update when testing framework changes
- Ensure consistency across all files

## Best Practices

1. **Be Specific**: "Tests in src/app/**/*.spec.ts" not "Tests in app folder"
2. **Include Examples**: Show actual mock code, not just descriptions
3. **Date Decisions**: Note when behaviors were clarified
4. **Link to Components**: Reference specific components where patterns apply
5. **Keep Current**: Update when Angular version or testing tools change
6. **Avoid Duplication**: Don't duplicate what's in context files
7. **Focus on Differences**: Store what makes THIS Angular project unique

## Related Files

- `../../../context/angular/jest_testing_standards.md` - Universal testing principles
- `../../../context/angular/component_testing_patterns.md` - Component test patterns
- `../../../context/angular/service_testing_patterns.md` - Service test patterns
- `../../../context/angular/testing_utilities.md` - TestBed, mocks, spies
- `../../../context/angular/test_antipatterns.md` - What to avoid
- `../../index.md` - Overall memory system explanation
