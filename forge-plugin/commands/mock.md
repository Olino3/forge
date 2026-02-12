---
name: mock
description: "Generate mock services and test doubles for API development and testing"
category: orchestration
complexity: basic
skills: [generate-mock-service]
context: [commands/mocking_patterns]
---

# /mock - Mock Service Generation

## Triggers
- Need to develop against external APIs that aren't available yet
- Testing components that depend on third-party services
- Creating realistic test scenarios with controlled responses
- Local development without real backend dependencies

## Usage
```
/mock [service-name] [--type express|flask|fastapi|wiremock|prism] [--scenarios success|error|edge|all]
```

**Parameters**:
- `service-name`: Name of the service to mock (required)
- `--type`: Mock server framework (default: auto-detect based on project)
  - `express`: Node.js/JavaScript projects
  - `flask`: Python projects (simple)
  - `fastapi`: Python projects (modern, with OpenAPI)
  - `wiremock`: Java projects or complex scenarios
  - `prism`: OpenAPI/Swagger-first approach
- `--scenarios`: Response scenarios to generate (default: all)
  - `success`: Happy path responses only
  - `error`: Error scenarios (4xx, 5xx)
  - `edge`: Edge cases and unusual inputs
  - `all`: Complete scenario coverage

## Workflow

### Step 1: Analyze Requirements

1. Identify the service to mock:
   - API specification (OpenAPI, Swagger, or description)
   - Endpoints to implement
   - Expected request/response formats
2. Detect project context:
   - Primary language and framework
   - Existing development environment (Docker, Tilt, etc.)
   - Testing framework in use

### Step 2: Load Context & Memory

**Context Loading** (via ContextProvider):
1. Load `contextProvider.getConditionalContext("commands", "mocking_patterns")` for best practices

**Memory Loading** (via MemoryStore):
1. Determine project name
2. Load `memoryStore.getCommandMemory("mock", project)` for existing mocks
3. Load `memoryStore.getSkillMemory("generate-mock-service", project)` for patterns

### Step 3: Gather API Specification

If API specification not provided, gather interactively:

**Questions**:
- What API are you mocking? (e.g., Stripe, internal user service)
- What endpoints are needed? (List URLs and methods)
- Do you have an OpenAPI/Swagger spec? (If yes, use it)
- What data format? (JSON, XML, etc.)
- Authentication required? (API key, OAuth, etc.)

### Step 4: Delegate to Skill

Invoke the generate-mock-service skill with gathered parameters:

```
skill:generate-mock-service --service-name {name} --type {type} --endpoints [{endpoints}] --scenarios {scenarios}
```

**Skill handles**:
- Mock server scaffolding
- Endpoint implementation with realistic data (using Faker)
- Scenario variants (success, error, edge cases)
- Request validation
- Docker containerization
- Integration with existing dev environment

### Step 5: Integration & Verification

After skill completes:

1. Review generated mock service structure
2. If Tilt environment exists: Add mock to Tiltfile
3. If Docker Compose exists: Add mock service
4. Test mock endpoints for functionality
5. Document available endpoints and scenarios

### Step 6: Generate Output & Update Memory

**Output**:
Save summary to `/claudedocs/mock_{service-name}_{date}.md`:

```markdown
# Mock Service - {Service Name}
**Date**: {date}
**Command**: /mock {full invocation}
**Type**: {framework}

## Endpoints
| Method | Path | Description | Scenarios |
|--------|------|-------------|-----------|
| GET | /api/users | List users | success, error, empty |
| POST | /api/users | Create user | success, validation_error |

## Setup Instructions
1. Navigate to mock service directory: `cd mocks/{service-name}`
2. Start mock server:
   - **Docker**: `docker-compose up mock-{service-name}`
   - **Tilt**: `tilt up` (auto-includes mock)
   - **Direct**: `npm start` or `python app.py`
3. Mock available at: `http://localhost:{port}`

## Scenarios
### Success Scenario
- All endpoints return valid responses
- Status codes: 200, 201

### Error Scenario
- Simulates server errors
- Status codes: 500, 503

### Validation Error Scenario
- Invalid request handling
- Status codes: 400, 422

## Environment Variables
- `MOCK_PORT`: {default port}
- `MOCK_DELAY`: Response delay in ms (default: 0)
- `MOCK_SCENARIO`: Active scenario (success|error|edge)

## Next Steps
- Use mock in your application by pointing to `http://localhost:{port}`
- Use `/test` to validate integration with mock
- Use `/implement` when ready to replace mock with real service
```

**Memory Updates**:
1. Use `memoryStore.append("commands", project, "command_history.md", entry)`
2. Use `memoryStore.update("commands", project, "mock_services.md", content)` with:
   - List of active mocks, endpoints, ports
3. Update skill memory with mock patterns

## Tool Coordination
- **Read**: API specifications, existing docker-compose files
- **Grep/Glob**: Find existing mock services and configurations
- **Write**: Mock service code, configuration files
- **Bash**: Docker/Tilt commands for testing
- **Skill**: generate-mock-service for actual implementation

## Key Patterns
- **Specification-Driven**: Use OpenAPI when available for accuracy
- **Realistic Data**: Faker library for believable test data
- **Scenario-Based**: Multiple response variants for thorough testing
- **Environment-Aware**: Integrates with existing dev setup

## Boundaries

**Will:**
- Generate complete mock services with multiple scenarios
- Integrate mocks into existing development environment
- Create realistic test data for endpoints
- Support multiple mock frameworks based on project needs
- Delegate to generate-mock-service skill for implementation

**Will Not:**
- Create production-ready services (use `/implement` for real APIs)
- Mock complex business logic beyond simple responses
- Generate mocks for every possible edge case automatically
- Replace proper integration testing with real services

**Output**: Mock service documentation saved to `/claudedocs/mock_{service-name}_{date}.md`

**Next Step**: Use `/test` to validate integration, or `/implement` when ready for real service.
