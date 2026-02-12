# Code Documenter Examples

This file contains example scenarios demonstrating how to use the code-documenter skill for various documentation tasks.

---

## Example 1: Documenting a Python REST API

### Scenario
Developer needs docstrings and inline comments added to Flask/FastAPI endpoints for a payment processing service.

### User Prompt
```
Add documentation to the payment API endpoints in src/api/payments.py
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: REST API endpoints in `src/api/payments.py`
- Target audience: Backend developers and API consumers
- Documentation type: Inline docstrings + API reference

**Step 2 - Load Project Memory**:
- No existing memory found; will create after generation
- Existing docstrings use Google style; adopting same convention
- Project uses FastAPI with Pydantic models

**Step 3 - Load Context**:
- Loaded Python domain context via `contextProvider.getDomainIndex("python")`
- Loaded FastAPI patterns via `contextProvider.getConditionalContext("python", {"framework": "fastapi"})`
- Loaded security context for payment handling via `contextProvider.getCrossDomainContext("python", {"security": true})`

**Step 4 - Generate Documentation**:
Inline docstrings and comments added to source file.

**Step 5 - Output**:
Documentation added inline to `src/api/payments.py`. Memory updated with project conventions.

### Generated Documentation

**Before**:
```python
@router.post("/payments")
async def create_payment(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    existing = await db.execute(
        select(Payment).where(
            Payment.idempotency_key == payment.idempotency_key,
            Payment.user_id == user.id,
        )
    )
    if existing.scalar_one_or_none():
        return existing.scalar_one()

    new_payment = Payment(
        user_id=user.id,
        amount=payment.amount,
        currency=payment.currency,
        idempotency_key=payment.idempotency_key,
        status=PaymentStatus.PENDING,
    )
    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)

    await payment_queue.enqueue(new_payment.id)

    return new_payment
```

**After**:
```python
@router.post("/payments", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new payment intent for the authenticated user.

    Initiates a payment by validating the request, checking for duplicate
    submissions via idempotency key, persisting the payment record, and
    enqueuing it for asynchronous processing by the payment gateway.

    Args:
        payment: Payment creation request containing amount, currency,
            and idempotency key.
        db: Async database session injected via dependency.
        user: Authenticated user extracted from the Bearer token.

    Returns:
        PaymentResponse: The created payment record with status PENDING.

    Raises:
        HTTPException(400): If the payment amount is zero or negative.
        HTTPException(401): If the user is not authenticated (via dependency).

    Example:
        POST /payments
        {
            "amount": 29.99,
            "currency": "USD",
            "idempotency_key": "order-abc-123"
        }
    """
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    # Idempotency check: return existing payment if the same user already
    # submitted a request with this key, preventing duplicate charges.
    existing = await db.execute(
        select(Payment).where(
            Payment.idempotency_key == payment.idempotency_key,
            Payment.user_id == user.id,
        )
    )
    if existing.scalar_one_or_none():
        return existing.scalar_one()

    new_payment = Payment(
        user_id=user.id,
        amount=payment.amount,
        currency=payment.currency,
        idempotency_key=payment.idempotency_key,
        status=PaymentStatus.PENDING,
    )
    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)

    # Enqueue for async processing — the payment gateway worker picks this
    # up and transitions the status to COMPLETED or FAILED.
    await payment_queue.enqueue(new_payment.id)

    return new_payment
```

---

## Example 2: TypeScript Library Documentation

### Scenario
Developer needs JSDoc comments added to a utility library for event handling.

### User Prompt
```
Add JSDoc documentation to the EventEmitter class in src/utils/event-emitter.ts
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: `EventEmitter` class in `src/utils/event-emitter.ts`
- Target audience: Internal developers consuming the utility library
- Documentation type: JSDoc inline comments + module overview

**Step 2 - Load Project Memory**:
- Found existing memory: project uses strict TypeScript with `@param` and `@returns` JSDoc tags
- Cross-skill discovery: test skill memory indicates 92% coverage on this module

**Step 3 - Load Context**:
- Loaded TypeScript domain context via `contextProvider.getDomainIndex("typescript")`
- No framework-specific context needed (pure utility library)

**Step 4 - Generate Documentation**:
JSDoc comments added to all public interfaces.

**Step 5 - Output**:
Documentation added inline to `src/utils/event-emitter.ts`. Memory updated.

### Generated Documentation

**Before**:
```typescript
type EventHandler<T = unknown> = (data: T) => void;

export class EventEmitter {
  private handlers: Map<string, Set<EventHandler>> = new Map();

  on<T>(event: string, handler: EventHandler<T>): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler as EventHandler);

    return () => this.off(event, handler);
  }

  off<T>(event: string, handler: EventHandler<T>): void {
    this.handlers.get(event)?.delete(handler as EventHandler);
  }

  emit<T>(event: string, data: T): void {
    this.handlers.get(event)?.forEach((handler) => handler(data));
  }

  once<T>(event: string, handler: EventHandler<T>): () => void {
    const wrapper: EventHandler<T> = (data) => {
      this.off(event, wrapper);
      handler(data);
    };
    return this.on(event, wrapper);
  }
}
```

**After**:
```typescript
/**
 * Callback function invoked when an event is emitted.
 * @typeParam T - The type of data passed to the handler.
 */
type EventHandler<T = unknown> = (data: T) => void;

/**
 * A lightweight, type-safe event emitter for pub/sub communication.
 *
 * Supports registering multiple handlers per event, one-time listeners,
 * and returns unsubscribe functions for easy cleanup.
 *
 * @example
 * ```ts
 * const emitter = new EventEmitter();
 *
 * const unsub = emitter.on<string>("message", (msg) => {
 *   console.log(`Received: ${msg}`);
 * });
 *
 * emitter.emit("message", "hello"); // logs "Received: hello"
 * unsub(); // removes the listener
 * ```
 */
export class EventEmitter {
  private handlers: Map<string, Set<EventHandler>> = new Map();

  /**
   * Register an event handler that fires every time the event is emitted.
   *
   * @typeParam T - The expected event payload type.
   * @param event - The event name to listen for.
   * @param handler - The callback to invoke when the event fires.
   * @returns An unsubscribe function that removes this handler when called.
   *
   * @example
   * ```ts
   * const unsub = emitter.on("click", (pos: Point) => draw(pos));
   * // later: unsub() to stop listening
   * ```
   */
  on<T>(event: string, handler: EventHandler<T>): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler as EventHandler);

    return () => this.off(event, handler);
  }

  /**
   * Remove a previously registered event handler.
   *
   * @typeParam T - The event payload type.
   * @param event - The event name to unsubscribe from.
   * @param handler - The exact handler reference to remove.
   */
  off<T>(event: string, handler: EventHandler<T>): void {
    this.handlers.get(event)?.delete(handler as EventHandler);
  }

  /**
   * Emit an event, invoking all registered handlers with the provided data.
   *
   * Handlers are called synchronously in registration order.
   *
   * @typeParam T - The event payload type.
   * @param event - The event name to emit.
   * @param data - The payload passed to each handler.
   */
  emit<T>(event: string, data: T): void {
    this.handlers.get(event)?.forEach((handler) => handler(data));
  }

  /**
   * Register an event handler that fires only once, then auto-removes itself.
   *
   * @typeParam T - The expected event payload type.
   * @param event - The event name to listen for.
   * @param handler - The callback to invoke on the first emission.
   * @returns An unsubscribe function that can cancel the listener before it fires.
   *
   * @example
   * ```ts
   * emitter.once("ready", () => initialize());
   * ```
   */
  once<T>(event: string, handler: EventHandler<T>): () => void {
    // Wrap the handler to auto-unsubscribe after first invocation
    const wrapper: EventHandler<T> = (data) => {
      this.off(event, wrapper);
      handler(data);
    };
    return this.on(event, wrapper);
  }
}
```

---

## Example 3: Architecture Decision Record

### Scenario
Team needs high-level architecture documentation generated from codebase analysis of a microservices system.

### User Prompt
```
Create architecture documentation for the order processing system in src/services/
```

### Skill Execution

**Step 1 - Identify Documentation Scope**:
- Scope: Architecture overview of the order processing subsystem
- Target audience: New team members and senior engineers evaluating the design
- Documentation type: Architecture documentation

**Step 2 - Load Project Memory**:
- Found cross-skill memory from `python-code-review`: identified event-driven architecture with RabbitMQ
- Found `database-schema-analysis` results: 12 tables in the orders schema
- No existing architecture docs in `docs/`

**Step 3 - Load Context**:
- Loaded architecture domain context via `contextProvider.getDomainIndex("architecture")`
- Loaded Python patterns via `contextProvider.getDomainIndex("python")`
- Loaded security context for payment data handling

**Step 4 - Generate Documentation**:
Architecture document produced from source analysis.

**Step 5 - Output**:
File: `/claudedocs/architecture_order_processing.md`. Memory updated with discovered architecture patterns.

### Generated Documentation

```markdown
# Order Processing System — Architecture Overview

## Purpose

The order processing system manages the lifecycle of customer orders from
placement through fulfillment. It coordinates payment authorization, inventory
reservation, shipment scheduling, and notification delivery.

## System Components

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  API Gateway  │───▶│ Order Service │───▶│Payment Service│
│  (FastAPI)    │    │              │    │  (Stripe)     │
└──────────────┘    └──────┬───────┘    └──────────────┘
                          │
                    ┌─────▼──────┐
                    │  RabbitMQ   │
                    │  Event Bus  │
                    └─────┬──────┘
              ┌───────────┼───────────┐
              ▼           ▼           ▼
     ┌──────────────┐ ┌────────┐ ┌────────────┐
     │  Inventory    │ │Shipping│ │Notification│
     │  Service      │ │Service │ │  Service   │
     └──────────────┘ └────────┘ └────────────┘
```

## Data Flow

1. **Order Placement**: API Gateway validates the request and forwards to
   Order Service. Order record created with status `PENDING`.

2. **Payment Authorization**: Order Service publishes `order.created` event.
   Payment Service subscribes, authorizes the charge via Stripe, and
   publishes `payment.authorized` or `payment.failed`.

3. **Inventory Reservation**: On `payment.authorized`, Inventory Service
   reserves stock. Publishes `inventory.reserved` or `inventory.insufficient`.

4. **Shipment Scheduling**: On `inventory.reserved`, Shipping Service
   creates a shipment label and publishes `shipment.scheduled`.

5. **Notification**: Notification Service subscribes to all terminal events
   and sends email/SMS updates to the customer.

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Event-driven (RabbitMQ) | Decouples services; enables retry and dead-letter handling |
| Idempotency keys on all writes | Prevents duplicate orders during retries |
| Saga pattern for transactions | No distributed transactions; compensating actions on failure |
| Separate read/write models | CQRS for order queries vs. command processing |

## Database Schema (Orders)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| orders | Order records | id, user_id, status, total, created_at |
| order_items | Line items | id, order_id, product_id, quantity, price |
| order_events | Audit log | id, order_id, event_type, payload, timestamp |
| payments | Payment records | id, order_id, stripe_id, status, amount |

## Error Handling

- **Payment failure**: Order status set to `PAYMENT_FAILED`; user notified.
  No inventory reservation occurs.
- **Inventory shortage**: Compensating action releases payment hold.
  Order status set to `OUT_OF_STOCK`.
- **Service unavailable**: Messages remain in RabbitMQ with exponential
  backoff retry. Dead-letter queue after 5 attempts triggers alerting.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| API Gateway | FastAPI 0.104+ |
| Message Broker | RabbitMQ 3.12 |
| Database | PostgreSQL 16 |
| Payment Provider | Stripe API v2023-10 |
| Containerization | Docker + Kubernetes |
```

---

## Summary of Use Cases

1. **Python REST API documentation** — Docstrings and inline comments for Flask/FastAPI endpoints with parameter, return, and exception documentation
2. **TypeScript library documentation** — JSDoc comments for classes and methods with type parameters and usage examples
3. **Architecture documentation** — System overview with component diagrams, data flow, design decisions, and technology stack

## Best Practices

- Explain *why*, not *what* — the code shows what happens, documentation explains the reasoning
- Follow the project's existing docstring convention; do not introduce a conflicting style
- Include at least one usage example per public function, method, or endpoint
- Document error cases and edge conditions, not just the happy path
- Keep inline comments concise — one line for simple clarifications, a short block for complex logic
- Update project memory after every task to maintain consistency across future documentation sessions
