# Implementation Strategies

Reference patterns for the `/implement` command. Covers development approaches, testing integration, and incremental development strategies.

## Development Approaches

### Test-Driven Development (TDD)
1. Write failing test for expected behavior
2. Write minimal code to pass test
3. Refactor while tests pass
- **Best for**: Well-defined interfaces, business logic, utility functions
- **Skill integration**: Use `skill:generate-python-unit-tests` or `skill:generate-jest-unit-tests`

### Behavior-Driven Development (BDD)
1. Define behavior in user story format ("Given/When/Then")
2. Write acceptance tests from stories
3. Implement to satisfy acceptance tests
- **Best for**: User-facing features, API endpoints, UI components

### Feature-First Development
1. Implement feature with basic functionality
2. Add error handling and edge cases
3. Write tests to cover implementation
4. Refactor for quality
- **Best for**: Prototyping, exploratory features, unclear requirements

## Implementation Workflow

### Step 1: Requirements Analysis
- Identify inputs, outputs, and side effects
- Define success criteria and edge cases
- Map dependencies and integration points
- Determine scope boundaries

### Step 2: Architecture Decision
- Choose appropriate design pattern
- Identify affected files and modules
- Plan database/API changes if needed
- Consider backward compatibility

### Step 3: Implementation
- Create feature branch (if using git)
- Implement core logic first
- Add error handling
- Add input validation
- Write/update tests

### Step 4: Integration
- Verify all tests pass
- Check for breaking changes
- Update documentation
- Review against requirements

## Testing Integration Patterns

### When to Generate Tests
- **Always**: Public API methods, business logic, data transformations
- **Usually**: UI components with logic, service methods, utility functions
- **Sometimes**: Configuration, simple getters/setters, framework boilerplate
- **Rarely**: Third-party integrations (mock instead), generated code

### Test Generation Strategy
1. Identify testable units in the implementation
2. Determine test framework from project config
3. Delegate to appropriate test generation skill:
   - Python: `skill:generate-python-unit-tests`
   - Angular/TypeScript: `skill:generate-jest-unit-tests`
4. Verify generated tests pass

## Incremental Development

### Feature Flags
- Use configuration-based toggles for gradual rollout
- Keep flag logic separate from business logic
- Clean up flags after full rollout

### Vertical Slicing
- Implement one complete flow end-to-end first
- Add breadth (more endpoints, more UI) incrementally
- Each slice should be independently testable

### Strangler Fig Pattern (for legacy)
- Build new feature alongside old
- Route traffic gradually to new implementation
- Remove old code after migration complete

## Common Implementation Patterns

### API Endpoint Implementation
1. Define route and method
2. Add request validation
3. Implement business logic (or delegate to service)
4. Define response format
5. Add error handling
6. Write integration test

### Service/Business Logic Implementation
1. Define interface/contract
2. Implement core logic
3. Add dependency injection
4. Handle edge cases and errors
5. Write unit tests

### UI Component Implementation
1. Define props/inputs and events/outputs
2. Create component structure
3. Implement rendering logic
4. Add interactivity and state management
5. Write component tests

### Database Integration
1. Define schema/model
2. Create migration
3. Implement repository/data access layer
4. Add validation and constraints
5. Write integration tests with test database

## Error Handling Strategy

### Input Validation
- Validate at system boundaries (API endpoints, UI forms)
- Use framework validation (Pydantic, FluentValidation, class-validator)
- Return descriptive error messages

### Exception Handling
- Catch specific exceptions, not generic `Exception`
- Log errors with context (request ID, user, operation)
- Return appropriate HTTP status codes for APIs
- Don't swallow exceptions silently

### Graceful Degradation
- Provide fallback behavior for non-critical features
- Use circuit breakers for external service calls
- Implement retry logic with exponential backoff

## Official References

- [12-Factor App](https://12factor.net/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
