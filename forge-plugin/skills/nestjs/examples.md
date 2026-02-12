# NestJS Skill Examples

This file provides sample usage scenarios for the `nestjs` skill.

---

## Example 1: Orders Module Buildout

### Scenario
A NestJS monolith needs a new Orders module with REST endpoints.

### User Prompt
"Design a NestJS Orders module with CRUD endpoints."

### Skill Execution
- **Step 1**: Confirm NestJS version, database choice, and module layout.
- **Step 2**: Load memory for `commerce-api`.
- **Step 3**: Load engineering context and security references.
- **Step 4**: Review existing modules and shared providers.
- **Step 5**: Recommend controllers, services, and DTO validation.
- **Step 6**: Output to `/claudedocs/nestjs_commerce-api_2026-02-12.md`.

### Generated Output
```markdown
# NestJS Guidance - commerce-api

## Orders Module
- `OrdersModule` imports `TypeOrmModule.forFeature([Order])`
- `OrdersController` for REST routes
- `OrdersService` for business logic

## DTO Validation
- Use `CreateOrderDto` with `@IsUUID()` for userId
- Enable `ValidationPipe` globally
```

---

## Example 2: Validation and Error Handling

### Scenario
The API lacks consistent validation and error handling.

### User Prompt
"Add validation and consistent error responses in our NestJS API."

### Skill Execution
- **Step 1**: Confirm existing pipes and filters.
- **Step 2**: Load memory for current conventions.
- **Step 3**: Load engineering context.
- **Step 4**: Inspect controller DTO usage.
- **Step 5**: Recommend global pipes and exception filters.
- **Step 6**: Output to `/claudedocs/nestjs_validation_2026-02-12.md`.

### Generated Output
```markdown
# NestJS Guidance - validation

## Validation
- Enable `ValidationPipe({ whitelist: true, transform: true })`
- Add DTO decorators for all request bodies

## Error Handling
- Implement `HttpExceptionFilter` for standardized errors
- Include `error_code` field in responses
```

---

## Example 3: Messaging Integration

### Scenario
The service needs to publish events to a queue.

### User Prompt
"Integrate RabbitMQ messaging for order-created events."

### Skill Execution
- **Step 1**: Confirm RabbitMQ infrastructure and event schema.
- **Step 2**: Load memory for integration notes.
- **Step 3**: Load engineering and security context.
- **Step 4**: Inspect module boundaries.
- **Step 5**: Recommend microservice client setup and retries.
- **Step 6**: Output to `/claudedocs/nestjs_messaging_2026-02-12.md`.

### Generated Output
```markdown
# NestJS Guidance - messaging

## RabbitMQ Client
- Configure `ClientsModule.register` with `transport: Transport.RMQ`
- Use durable queue `orders.events`

## Reliability
- Add retry policy for publish failures
- Log correlation IDs for tracing
```
