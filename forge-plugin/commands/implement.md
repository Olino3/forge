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
1. Use `contextProvider.getDomainIndex("commands")` for command guidance
2. Use `contextProvider.getConditionalContext("commands", {"command": "implement"})` to load implementation strategies
3. Based on detected framework, load domain-specific context:
   - **Python**: Use `contextProvider.getDomainIndex("python")`, then `contextProvider.getConditionalContext("python", detection)` for framework patterns
   - **.NET**: Use `contextProvider.getDomainIndex("dotnet")`, then `contextProvider.getConditionalContext("dotnet", detection)` for ASP.NET, EF, DI patterns
   - **Angular**: Use `contextProvider.getDomainIndex("angular")`, then `contextProvider.getConditionalContext("angular", detection)` for component, service, state patterns
   - **Azure**: Use `contextProvider.getDomainIndex("azure")` if serverless/cloud components involved
4. If implementing auth, user input, or data handling: Use `contextProvider.getCrossDomainContext("{domain}", ["auth_code", "user_input"])` to load security guidelines

**Memory Loading**:
1. Determine project name
2. Use `memoryStore.getCommandMemory("{project}")` for related past implementations and patterns
3. Use `memoryStore.getSharedProjectMemory("{project}")` for cross-skill project conventions

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

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
1. Use `memoryStore.append("command/{project}/command_history", ...)` to record execution
2. Use `memoryStore.update("command/{project}/implement_patterns", ...)` to record:
   - Patterns used, conventions followed, design decisions

See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

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
