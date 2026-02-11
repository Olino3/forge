---
name: generate-mock-service
description: Generate simulated service doppelgangers for testing and development. Creates mock servers (Express, Flask, FastAPI, WireMock, Prism) matching real API contracts with realistic responses, error scenarios, and Docker containerization.
version: "0.1.0-alpha"
context:
  primary_domain: ""
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [mock_config.md, generated_mocks.md, scenarios.md, integration_notes.md]
    - type: "shared-project"
      usage: "reference"
---

# Skill: generate-mock-service

**Version**: 0.1.0-alpha
**Purpose**: Generate simulated service doppelgangers for testing and development
**Author**: The Forge
**Last Updated**: 2026-02-06

---

## Title

**Generate Mock Service** - Forge simulated service doppelgangers for testing and local development

---

## File Structure

```
forge-plugin/skills/generate-mock-service/
├── SKILL.md                  # This file - mandatory workflow
├── examples.md               # Usage scenarios and examples
├── scripts/
│   └── mock_generator.py     # Helper script for mock generation
└── templates/
    ├── express_mock_template.js        # Express.js mock server template
    ├── flask_mock_template.py          # Flask mock server template
    ├── fastapi_mock_template.py        # FastAPI mock server template
    ├── wiremock_template.json          # WireMock mapping template
    ├── prism_config_template.yml       # Prism mock server template
    └── dockerfile_mock_template.txt    # Dockerfile for mock services
```

---

## Required Reading

**Before executing this skill**, load context and memory via interfaces:

1. **Context**: Use `contextProvider.getDomainIndex()` for relevant domain context. See [ContextProvider Interface](../../interfaces/context_provider.md).

2. **Skill memory**: Use `memoryStore.getSkillMemory("generate-mock-service", "{project-name}")` for previous mock configurations. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## Design Requirements

### Core Functionality

This skill must:
1. **Understand the external service to mock** (API contract, endpoints, responses)
2. **Ask user about mock requirements** (service type, endpoints, response patterns)
3. **Choose appropriate mocking strategy** (code-based, WireMock, Prism, etc.)
4. **Generate mock service implementation** (server code or configuration)
5. **Create realistic response data** (sample JSON, XML, or other formats)
6. **Support different scenarios** (success, error, edge cases)
7. **Provide containerization** (Dockerfile, docker-compose integration)
8. **Store mock configuration** in memory for future reference

### Output Requirements

Generate a **complete, working mock service** with:
- Mock server implementation (Express, Flask, FastAPI, WireMock, or Prism)
- Endpoint definitions matching the real service API
- Realistic sample responses for all endpoints
- Support for different HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Configurable delays to simulate network latency
- Error scenario support (4xx, 5xx responses)
- Request validation (optional)
- Dockerfile for containerization
- docker-compose configuration for integration
- README with usage instructions

### Quality Requirements

Generated mocks must:
- **Match the real API contract** (OpenAPI/Swagger spec if available)
- **Provide realistic responses** (proper data types, structures)
- **Support multiple scenarios** (success, validation errors, server errors)
- **Be easily configurable** (environment variables, config files)
- **Include logging** (request/response logging for debugging)
- **Be containerized** (ready to run in Docker)
- **Be well-documented** (clear setup and usage instructions)

---

## Prompting Guidelines

### User Questions Framework

After understanding the mock requirements, ask user about:

#### 1. Service to Mock
- **Question**: "What service do you need to mock?"
  - External REST API
  - SOAP service
  - GraphQL API
  - gRPC service
  - WebSocket service
  - Third-party integration (Stripe, SendGrid, etc.)
- **Why ask**: Determines mock server type and configuration
- **Follow-up**: "Do you have an API specification (OpenAPI, Swagger, WSDL)?"

#### 2. Mock Implementation Type
- **Question**: "What type of mock implementation do you prefer?"
  - **Code-based**: Express.js (Node.js), Flask (Python), FastAPI (Python)
  - **Configuration-based**: WireMock (JSON), Prism (OpenAPI), MockServer
  - **Simple**: JSON Server (for REST APIs)
- **Why ask**: Determines which templates to use
- **Recommendation**: 
  - Use Prism if you have OpenAPI spec
  - Use WireMock for complex scenarios
  - Use code-based for custom logic

#### 3. Endpoints and Methods
- **Question**: "What endpoints need to be mocked?"
  - List all endpoints (e.g., /users, /orders, /payments)
  - HTTP methods for each (GET, POST, PUT, DELETE, PATCH)
  - Request/response formats (JSON, XML, form data)
- **Why ask**: Determines mock routes and handlers
- **Follow-up**: "Do you have example request/response payloads?"

#### 4. Response Scenarios
- **Question**: "What response scenarios do you need?"
  - Success responses (200, 201, 204)
  - Client errors (400, 401, 403, 404, 422)
  - Server errors (500, 502, 503)
  - Edge cases (timeouts, rate limits)
- **Why ask**: Determines scenario configuration
- **Follow-up**: "Should scenarios be triggered by specific request parameters?"

#### 5. Data Requirements
- **Question**: "What kind of data should the mock return?"
  - Static data (same response every time)
  - Dynamic data (randomized, time-based)
  - Stateful (track state across requests)
  - Realistic fake data (using Faker library)
- **Why ask**: Determines data generation approach

#### 6. Behavior Configuration
- **Question**: "What behavior should the mock have?"
  - Response delays (simulate network latency)
  - Random failures (simulate unreliable service)
  - Request validation (validate required fields)
  - State management (CRUD operations)
  - Callback/webhook simulation
- **Why ask**: Determines mock server logic

#### 7. Port and Networking
- **Question**: "What port should the mock service run on?"
  - Default ports: 8080, 8081, 3001, etc.
  - Custom port
- **Why ask**: Prevents port conflicts
- **Follow-up**: "Should this integrate with your docker-compose setup?"

#### 8. Authentication/Authorization
- **Question**: "Does the service require authentication?"
  - No authentication
  - API key validation
  - OAuth2/JWT token validation
  - Basic authentication
- **Why ask**: Determines authentication middleware

---

## Instructions

### MANDATORY STEPS (Must Execute in Order)

---

#### **Step 1: Initial Analysis**

**Purpose**: Understand the service to be mocked

**Actions**:
1. Identify the external service to mock
2. Check if API specification exists (OpenAPI/Swagger, Postman collection, WSDL)
3. Review any existing documentation or examples
4. Determine integration points in the codebase
5. Note any existing mock implementations

**Output**: Clear understanding of service to mock and requirements

---

#### **Step 2: Load Index Files**

**Purpose**: Understand available context and memory

**Actions**:
1. Use `contextProvider.getDomainIndex()` for relevant context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
2. Use `memoryStore.getSkillMemory("generate-mock-service", "{project-name}")` to check for existing memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
3. Identify which context domains are relevant to the mock target

**Output**: Knowledge of available guidance and memory structure

---

#### **Step 3: Load Project Memory (if exists)**

**Purpose**: Understand previous mock configurations for this project

**Actions**:
1. Use `memoryStore.getSkillMemory("generate-mock-service", "{project-name}")` to load project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
2. If memory exists, review:
   - `mock_config.md` - Previous mock configurations
   - `generated_mocks.md` - What mocks were generated before
   - `scenarios.md` - Documented scenarios
   - `integration_notes.md` - Integration information
3. If not exists, note this is first-time generation

**Output**: Understanding of project mock history or recognition of new project

---

#### **Step 4: Load Context**

**Purpose**: Load relevant API mocking knowledge

**Actions**:
1. Read relevant context files based on service type:
   - REST API patterns
   - Testing best practices
   - Mock service patterns
2. Note any best practices for mocking

**Output**: Comprehensive understanding of mocking patterns

---

#### **Step 5: Gather Requirements**

**Purpose**: Understand user's needs through conversation

**Actions**:
1. Ask user about **service to mock**
2. Ask about **mock implementation type**
3. Ask about **endpoints and methods**
4. Ask about **response scenarios**
5. Ask about **data requirements**
6. Ask about **behavior configuration**
7. Ask about **port and networking**
8. Ask about **authentication/authorization**
9. Confirm all requirements with user before proceeding

**Output**: Complete specification of mock service to generate

---

#### **Step 6: Generate Mock Service**

**Purpose**: Create mock service implementation

**Actions**:

**A. For Code-Based Mocks (Express/Flask/FastAPI):**

1. **Generate main server file**:
   - Use appropriate template (express_mock_template.js, flask_mock_template.py, fastapi_mock_template.py)
   - Add endpoint handlers for each route
   - Implement request validation if needed
   - Add authentication middleware if required
   - Configure CORS for browser access
   - Add logging middleware

2. **Generate response data files**:
   - Create `data/` directory
   - Generate JSON files for each endpoint response
   - Include multiple scenarios (success, error)
   - Use realistic fake data if requested

3. **Generate utility functions**:
   - Response delay simulator
   - Random error generator
   - Fake data generator (using Faker or similar)
   - Request validator

4. **Generate configuration file**:
   - `config.json` or `.env` file
   - Port configuration
   - Delay settings
   - Error rate settings
   - Feature flags

**B. For Configuration-Based Mocks (WireMock/Prism):**

1. **Generate WireMock mappings** (if using WireMock):
   - Create `mappings/` directory
   - Generate JSON mapping files for each endpoint
   - Include request matchers
   - Define response templates
   - Add scenario state transitions if needed

2. **Generate Prism configuration** (if using Prism):
   - Use existing OpenAPI specification
   - Create `prism-config.yml`
   - Configure dynamic response behavior
   - Set up validation rules

**C. Common Files:**

1. **Generate Dockerfile**:
   - Use `templates/dockerfile_mock_template.txt`
   - Install dependencies
   - Copy server files and data
   - Expose port
   - Set startup command

2. **Generate docker-compose integration**:
   - Add service definition
   - Configure networking
   - Set environment variables
   - Add health check
   - Link to other services if needed

3. **Generate package/dependency files**:
   - `package.json` for Node.js
   - `requirements.txt` for Python
   - Include necessary libraries (express, flask, fastapi, faker, etc.)

4. **Generate README.md**:
   - Service description
   - Available endpoints
   - Request/response examples
   - How to run locally
   - How to run in Docker
   - Configuration options
   - Testing tips

5. **Generate test examples**:
   - `examples/` directory
   - curl commands for each endpoint
   - Example request payloads
   - Expected responses

**Output**: Complete mock service implementation

---

#### **Step 7: Validate Generated Mock**

**Purpose**: Ensure mock service is correctly configured

**Actions**:
1. Verify all required files exist
2. Check server code syntax
3. Validate JSON response files
4. Ensure Dockerfile is properly structured
5. Check that all endpoints are defined
6. Verify configuration is complete

**Do NOT start the server** - just validate file structure and syntax

**Output**: Confidence that generated mock is correct

---

#### **Step 8: Present Results to User**

**Purpose**: Show user what was generated and how to use it

**Actions**:
1. List all generated files with brief description
2. Show example endpoints and responses
3. Provide usage instructions:
   ```bash
   # Run locally (Node.js example)
   cd mock-{service-name}
   npm install
   npm start
   
   # Run with Docker
   docker build -t mock-{service-name} .
   docker run -p {port}:{port} mock-{service-name}
   
   # Or with docker-compose
   docker-compose up mock-{service-name}
   ```
4. Show how to test endpoints:
   ```bash
   # Example API call
   curl http://localhost:{port}/api/users
   ```
5. Point to README.md for detailed documentation
6. Explain how to modify responses or add scenarios

**Output**: User understands how to use the mock service

---

#### **Step 9: Update Project Memory**

**Purpose**: Store configuration for future reference

**Actions**:
1. Use `memoryStore.update(layer="skill-specific", skill="generate-mock-service", project="{project-name}", ...)` to store:
2. **mock_config.md**:
   - Service being mocked
   - Mock type (Express, Flask, WireMock, etc.)
   - Port configuration
   - Endpoints implemented
   - Authentication approach
3. Create `generated_mocks.md`:
   - List of all generated files
   - Timestamp of generation
   - Skill version used
4. Create `scenarios.md`:
   - Documented response scenarios
   - How to trigger different scenarios
   - Test cases covered
5. Create `integration_notes.md`:
   - How mock integrates with main application
   - Docker compose configuration
   - Environment variables used
   - Known limitations

**Output**: Memory stored for future skill invocations

---

## Best Practices

### Mock Design

1. **Match the real API**: Use same endpoints, methods, request/response formats
2. **Provide realistic data**: Don't just return `{"success": true}`
3. **Support error scenarios**: Test your error handling code
4. **Add delays**: Simulate real network conditions
5. **Version your mocks**: Track changes to mock behavior

### Response Design

1. **Use proper status codes**: 200, 201, 400, 404, 500, etc.
2. **Include all response fields**: Match the real API structure
3. **Vary responses**: Support different scenarios
4. **Add realistic timestamps**: Use current dates/times
5. **Include pagination**: If the real API paginates

### Configuration

1. **Make it configurable**: Use environment variables
2. **Easy scenario switching**: Change behavior without code changes
3. **Toggle features**: Enable/disable authentication, validation
4. **Adjust timing**: Configure delays, timeouts
5. **Control data**: Switch between datasets

### Integration

1. **Use same port in dev**: Match production configuration
2. **Document differences**: Note what's mocked vs real
3. **Easy switching**: Toggle between mock and real service
4. **Container-ready**: Always provide Docker setup
5. **Version control**: Commit mocks to repository

---

## Error Handling

### Common Issues

1. **Port conflicts**: Check for existing services on the port
2. **CORS errors**: Configure CORS headers properly
3. **Invalid JSON**: Validate all response files
4. **Missing dependencies**: Ensure all packages are installed
5. **Authentication failures**: Mock auth tokens correctly

### Debugging

1. **Enable verbose logging**: See all requests/responses
2. **Test endpoints manually**: Use curl or Postman
3. **Check Docker logs**: `docker logs <container>`
4. **Validate responses**: Ensure they match expected format
5. **Compare with real API**: Verify mock behavior matches

---

## Mock Implementation Options

### Express.js (Node.js)
- **Best for**: JavaScript/TypeScript projects
- **Pros**: Easy to customize, familiar for frontend devs
- **Cons**: Requires Node.js installation

### Flask (Python)
- **Best for**: Python projects
- **Pros**: Simple, minimal code
- **Cons**: May need additional libraries for complex scenarios

### FastAPI (Python)
- **Best for**: Modern Python projects, API-first
- **Pros**: Automatic validation, great documentation
- **Cons**: Slightly more complex setup

### WireMock
- **Best for**: Complex scenarios, stateful mocks
- **Pros**: Very powerful, no coding required
- **Cons**: JSON configuration can be verbose

### Prism
- **Best for**: OpenAPI/Swagger specs available
- **Pros**: Validates requests, generates examples automatically
- **Cons**: Requires OpenAPI specification

### JSON Server
- **Best for**: Simple REST APIs, prototyping
- **Pros**: Zero configuration, very fast setup
- **Cons**: Limited customization

---

## Version History

- **1.1.0** (2026-02-10): Phase 4 Migration
  - Migrated to interface-based patterns (ContextProvider + MemoryStore)
  - Added YAML frontmatter with declarative context/memory configuration
  - Removed hardcoded filesystem paths
  - Added interface references section
- **1.0.0** (2026-02-06): Initial implementation
  - Multiple mock server types (Express, Flask, FastAPI, WireMock, Prism)
  - Realistic response generation
  - Multiple scenario support
  - Docker containerization
  - Authentication middleware
  - Request validation
  - Memory system for configuration tracking

---

## Related Skills

- **generate-tilt-dev-environment**: For integrating mocks into development environment
- **generate-azure-functions**: May need mocks for Azure services
- **test-cli-tools**: For testing CLI tools that call mocked services

---

## References

- [WireMock Documentation](http://wiremock.org/docs/)
- [Prism Documentation](https://stoplight.io/open-source/prism)
- [JSON Server](https://github.com/typicode/json-server)
- [Express.js](https://expressjs.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Faker.js](https://fakerjs.dev/) / [Faker (Python)](https://faker.readthedocs.io/)
