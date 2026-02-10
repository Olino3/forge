# /mock Examples

## Example 1: Quick Mock for External API

```
/mock stripe-payment --type express --scenarios success
```

**What happens**:
1. Prompts for basic endpoints:
   - "What endpoints? (e.g., POST /v1/charges, GET /v1/customers)"
2. Delegates to `skill:generate-mock-service`
3. Generates Express.js mock with:
   - POST /v1/charges (returns successful charge object)
   - GET /v1/customers (returns customer list)
4. Creates Docker container configuration
5. Saves documentation to `/claudedocs/mock_stripe-payment_20260210.md`
6. Mock available at `http://localhost:3001`

## Example 2: Python Mock with All Scenarios

```
/mock user-api --type fastapi --scenarios all
```

**What happens**:
1. Asks for endpoint details
2. Generates FastAPI mock service with scenarios:
   - **Success**: 200 OK with valid user data
   - **Not Found**: 404 for invalid user IDs
   - **Validation Error**: 422 for malformed requests
   - **Server Error**: 500 for error testing
3. Includes OpenAPI documentation at `/docs`
4. Adds to existing docker-compose.yml if present
5. Environment variable `MOCK_SCENARIO` controls active scenario

## Example 3: Mock from OpenAPI Specification

```
/mock payment-gateway --type prism
```

**What happens**:
1. Asks: "Do you have an OpenAPI spec?"
   - User provides path to `openapi.yaml`
2. Delegates to skill with OpenAPI spec
3. Prism generates mock based on specification:
   - All endpoints from spec automatically mocked
   - Responses match schema exactly
   - Validation against spec
4. Mock validates requests against OpenAPI schema
5. Perfect for contract testing

## Example 4: WireMock for Complex Scenarios

```
/mock legacy-soap-service --type wiremock --scenarios all
```

**What happens**:
1. Gathers SOAP endpoint details
2. Generates WireMock configuration with:
   - Multiple response stubs (success, fault, delay)
   - Request matching rules (URL, headers, body)
   - Stateful scenarios (e.g., idempotency)
3. Creates JSON mapping files for each scenario
4. Includes admin UI at `http://localhost:8080/__admin`
5. Can record and playback real API calls

## Example 5: Integration with Tilt

```
/mock notification-service --type flask
```

**What happens** (with existing Tilt environment):
1. Generates Flask mock service
2. Detects existing `Tiltfile`
3. Adds mock service to Tilt:
   ```python
   docker_build('mock-notification', './mocks/notification-service')
   k8s_yaml('mocks/notification-service/k8s.yaml')
   k8s_resource('mock-notification', port_forwards='3002:5000')
   ```
4. Mock auto-starts with `tilt up`
5. Live reload on code changes

## Example 6: Error-Only Mock for Testing

```
/mock unreliable-api --type express --scenarios error
```

**What happens**:
1. Generates mock that simulates failures:
   - Random 500 errors
   - Timeout simulation (delayed responses)
   - Rate limiting (429 Too Many Requests)
   - Network errors
2. Useful for testing retry logic and error handling
3. Configurable failure rate via environment variable
4. Logs all requests for debugging

## Example 7: Updating Existing Mock

```
/mock user-api --scenarios edge
```

**What happens** (with existing mock):
1. Loads existing mock configuration from memory
2. Adds new edge case scenarios:
   - Empty responses
   - Large payloads
   - Special characters in data
   - Unusual but valid inputs
3. Updates mock service without recreating
4. Preserves existing success and error scenarios
5. Updates documentation

## Example 8: Multi-Service Mocking

```
/mock microservices --type fastapi
```

**What happens**:
1. Asks: "Which services to mock?" (e.g., auth, orders, inventory)
2. Generates separate mock for each service
3. Creates docker-compose.yml with all mocks:
   - mock-auth: port 3001
   - mock-orders: port 3002  
   - mock-inventory: port 3003
4. Inter-service communication mocked
5. Single command starts all mocks: `docker-compose up`
