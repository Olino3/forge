# generate-mock-service Memory

## Purpose

Remember project-specific mock service configurations, endpoint definitions, and test scenarios for efficient mock updates and consistency across services.

## Directory Structure

```
generate-mock-service/{project-name}/
├── mock_config.md       # Core mock configuration
├── endpoints.md         # Endpoint definitions and responses
├── scenarios.md         # Test scenarios and data patterns
└── customizations.md    # User-specific deviations
```

## Required Memory Files

### `mock_config.md` (ALWAYS CREATE)

- Mock server framework (Express, Flask, FastAPI, WireMock, Prism)
- Port assignments per mock service
- Authentication middleware configuration
- Request validation settings
- Docker containerization details
- Generation timestamp and skill version

**Example snippet**:
```markdown
<!-- Last Updated: 2026-02-10 -->
# Mock Configuration - my-app

## Mock Services
1. **payment-mock** (Express, Port 9001): Stripe API simulation
2. **notification-mock** (Flask, Port 9002): Email/SMS service simulation
3. **auth-mock** (WireMock, Port 9003): OAuth2 provider simulation

## Shared Configuration
- Response delay: 50-200ms (realistic latency)
- Authentication: API key validation on all endpoints
- Data generation: Faker for realistic test data
```

### `endpoints.md` (COMPREHENSIVE)

- All mocked endpoints with HTTP methods
- Request/response schemas
- Default response data
- Error response configurations
- Rate limiting simulation settings

### `scenarios.md` (TEST SCENARIOS)

- Success scenarios with expected data
- Error scenarios (400, 401, 403, 404, 500)
- Edge cases (timeout, partial response, malformed data)
- Stateful scenarios (order flow, auth flow)

### `customizations.md` (USER-SPECIFIC)

- Non-standard mock behaviors and reasons
- Custom middleware additions
- Special data patterns or constraints
- Integration-specific configurations

## Why This Skill Needs Memory

- **Endpoint consistency**: Same mock endpoints across regenerations
- **Scenario reuse**: Test scenarios accumulated over time
- **Configuration tracking**: Remember framework choices and port assignments
- **Data patterns**: Maintain consistent test data across mock services

## Memory Growth Pattern

**First generation**: Framework choice, initial endpoints, basic scenarios
**Subsequent operations**: New endpoints, refined scenarios, custom behaviors added

---

*Last Updated: 2026-02-10*
