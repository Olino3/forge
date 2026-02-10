---
name: implement
description: "Feature implementation with intelligent context loading and test generation integration"
category: workflow
complexity: standard
skills: [generate-python-unit-tests, generate-jest-unit-tests, test-cli-tools]
context: [python, dotnet, angular, azure, commands/implementation_strategies]
---

# /implement - Feature Implementation

## Triggers
- Feature development requests for components, APIs, or complete functionality
- Code implementation needs with framework-specific requirements
- Multi-component development requiring coordinated implementation
- Implementation projects requiring testing and validation integration

## Usage
```
/implement [feature-description] [--type component|api|service|feature] [--with-tests] [--safe]
```

**Parameters**:
- `feature-description`: What to implement (required)
- `--type`: Implementation category for targeted guidance
- `--with-tests`: Generate tests after implementation using test generation skills
- `--safe`: Extra validation and confirmation before applying changes

## Workflow

### Step 1: Requirements Analysis

1. Parse the feature description and `--type` flag
2. Detect the project's technology stack:
   - Language and framework (Python/Django, .NET/ASP.NET, Angular, etc.)
   - Project structure and conventions
   - Existing patterns to follow
3. Identify implementation scope:
   - Files to create or modify
   - Dependencies to add
   - Integration points with existing code
4. Define success criteria and edge cases

### Step 2: Load Context & Memory

**Context Loading** (index-first approach):
1. Read `../../context/index.md` for overview
2. Read `../../context/commands/index.md` for command guidance
3. Load `../../context/commands/implementation_strategies.md` for development approach
4. Based on detected framework, load domain-specific context:
   - **Python**: `../../context/python/index.md` → framework patterns (Django, FastAPI, Flask)
   - **.NET**: `../../context/dotnet/index.md` → ASP.NET, EF, DI patterns
   - **Angular**: `../../context/angular/index.md` → component, service, state patterns
   - **Azure**: `../../context/azure/index.md` → if serverless/cloud components involved
5. Load `../../context/security/security_guidelines.md` if implementing auth, user input, or data handling

**Memory Loading**:
1. Determine project name
2. Check `../../memory/commands/{project}/command_history.md` for related past implementations
3. Load `../../memory/commands/{project}/implement_patterns.md` if exists
4. Check relevant skill memory for project conventions

### Step 3: Plan Implementation

1. Choose development approach (TDD, feature-first, etc.) based on context
2. Identify files to create or modify
3. Plan implementation order:
   - Data models / schemas first
   - Business logic / services
   - API endpoints / controllers
   - UI components (if applicable)
4. If `--safe`: Present plan to user for approval before proceeding

### Step 4: Execute Implementation

1. Create/modify files following project conventions
2. Apply framework-specific best practices from loaded context:
   - Use dependency injection patterns appropriate for the framework
   - Follow naming conventions from project memory
   - Apply error handling patterns
   - Add input validation at system boundaries
3. Ensure integration with existing code
4. Add necessary imports and registrations

### Step 5: Test Generation (if --with-tests)

Delegate to appropriate test generation skill:

**Python projects**:
```
skill:generate-python-unit-tests --target [implemented files]
```
- Socratic planning for expected behaviors
- Generates pytest/unittest tests following project conventions

**Angular projects**:
```
skill:generate-jest-unit-tests --target [implemented components/services]
```
- Generates Jest/Jasmine tests with TestBed configuration
- Tests components, services, pipes as appropriate

**CLI tools**:
```
skill:test-cli-tools --target [implemented commands]
```
- Tests CLI commands systematically

### Step 6: Generate Output & Update Memory

**Output**:
- Implementation code saved to project files
- If significant, document in `/claudedocs/implement_{feature}_{date}.md`:

```markdown
# Implementation - {Feature Name}
**Date**: {date}
**Command**: /implement {full invocation}
**Project**: {name}

## Summary
{What was implemented and why}

## Files Changed
- `path/to/file.py` - {description of changes}
- `path/to/new_file.py` - {new file purpose}

## Design Decisions
- {Decision 1}: {Rationale}
- {Decision 2}: {Rationale}

## Tests Generated
{If --with-tests was used, list generated test files}

## Next Steps
- Run `/test` to validate implementation
- Run `/analyze` to check quality
```

**Memory Updates**:
1. Append to `../../memory/commands/{project}/command_history.md`
2. Update `../../memory/commands/{project}/implement_patterns.md`:
   - Patterns used, conventions followed, design decisions

## Tool Coordination
- **Read/Grep/Glob**: Project analysis and pattern detection
- **Write/Edit**: Code generation and modification
- **Bash**: Dependency installation, build validation
- **Task**: Delegation for large-scale multi-file implementations

## Key Patterns
- **Context Detection**: Framework/stack → appropriate patterns and conventions
- **Implementation Flow**: Requirements → code generation → validation → integration
- **Skill Delegation**: Test needs → specialized test generation skills
- **Convention Following**: Project memory → consistent style and patterns

## Completion Criteria

**Implementation is DONE when**:
- Feature code is written and follows project conventions
- All imports and registrations are complete
- Basic functionality is verifiable
- Tests generated (if `--with-tests`)
- Files saved and ready for review

## Boundaries

**Will:**
- Implement features following project conventions and best practices
- Apply framework-specific patterns from loaded context
- Generate tests via skill delegation when requested
- Learn and apply project-specific patterns from memory

**Will Not:**
- Make architectural decisions without user consultation
- Override project conventions with "better" patterns
- Skip input validation on user-facing interfaces
- Implement features that conflict with existing architecture

**Output**: Implementation code in project files; documentation in `/claudedocs/implement_{feature}_{date}.md`

**Next Step**: Use `/test` to run tests, then `/analyze` to check quality.
