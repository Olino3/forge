# Code Reviewer Examples

This file contains example code review scenarios demonstrating the language-agnostic review framework across different languages, architectures, and codebases.

## Example 1: Cross-Language PR Review

A pull request contains changes to both Python backend and JavaScript frontend code.

### User Prompt

> "Review the changes in my PR that updates user authentication — there are changes in both the Python API and the React frontend."

### Skill Execution

**Step 1 — Identify Review Scope**: Invoke `get-git-diff` to get changed files. Detected: `auth_service.py`, `auth_middleware.py` (Python), `useAuth.js`, `LoginForm.jsx` (JavaScript/React). Two languages identified.

**Step 2 — Load Memory & Context**: Load `memoryStore.getSkillMemory("code-reviewer", "my-app")`. Cross-skill discovery finds prior `python-code-review` memory with known project patterns. Load `contextProvider.getDomainIndex("python")` and `contextProvider.getDomainIndex("javascript")`.

**Step 3 — Load Relevant Context**: Load Python common issues and FastAPI patterns via `contextProvider.getAlwaysLoadFiles("python")`. Load JavaScript/React patterns via `contextProvider.getConditionalContext("javascript", "react")`. Load security context via `contextProvider.getCrossDomainContext("python", ["auth"])`.

**Step 4 — Deep Review**: Systematic review of all changed files across all 8 dimensions.

**Step 5 — Generate Report & Update Memory**: Produce structured report and update project memory.

### Generated Review Output

#### Finding 1

**Severity**: Critical
**Category**: Error Handling
**File**: auth_service.py:47

The token validation catches a broad `Exception` and returns a generic error, silently swallowing authentication failures. An expired token and a malformed token produce the same response, making debugging impossible.

```python
# Before
def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception:
        return None
```

```python
# After
def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Invalid token: {e}")
```

#### Finding 2

**Severity**: Important
**Category**: DRY-KISS
**File**: useAuth.js:12, LoginForm.jsx:30

Token storage logic is duplicated in both `useAuth.js` and `LoginForm.jsx`. The same `localStorage.setItem`/`getItem` pattern with the same key appears in two places.

```javascript
// Before — useAuth.js:12
const token = localStorage.getItem('auth_token');

// Before — LoginForm.jsx:30
localStorage.setItem('auth_token', response.data.token);
```

```javascript
// After — tokenStorage.js (new shared module)
const TOKEN_KEY = 'auth_token';

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (token) => localStorage.setItem(TOKEN_KEY, token);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);
```

#### Finding 3

**Severity**: Minor
**Category**: Documentation
**File**: auth_service.py:1

The `auth_service.py` module has no docstring explaining its purpose, the authentication flow, or the expected token format. Public functions `validate_token` and `create_token` lack parameter and return type documentation.

---

## Example 2: Architecture & SOLID Principles Review

Reviewing Go code for a microservice that handles order processing.

### User Prompt

> "Review my order processing service for architecture and design issues."

### Skill Execution

**Step 1 — Identify Review Scope**: Invoke `get-git-diff`. Detected: `order_handler.go`, `order_service.go`, `email_sender.go` (Go). Single language identified.

**Step 2 — Load Memory & Context**: Load `memoryStore.getSkillMemory("code-reviewer", "order-service")`. No prior memory found — first review. Load `contextProvider.getDomainIndex("go")`.

**Step 3 — Load Relevant Context**: Load Go common issues via `contextProvider.getAlwaysLoadFiles("go")`. No framework-specific context needed for standard library HTTP service.

**Step 4 — Deep Review**: Systematic review with focus on SOLID principles and architecture.

**Step 5 — Generate Report & Update Memory**: Produce structured report and initialize project memory.

### Generated Review Output

#### Finding 1

**Severity**: Critical
**Category**: SOLID
**File**: order_service.go:15

The `OrderService` struct violates the Single Responsibility Principle. It handles order validation, persistence, payment processing, inventory updates, and email notifications — five distinct responsibilities in one type.

```go
// Before
type OrderService struct {
    db        *sql.DB
    smtp      *smtp.Client
    paymentGW *PaymentGateway
}

func (s *OrderService) ProcessOrder(order Order) error {
    if err := s.validateOrder(order); err != nil {
        return err
    }
    if err := s.chargePayment(order); err != nil {
        return err
    }
    if err := s.updateInventory(order); err != nil {
        return err
    }
    if err := s.saveOrder(order); err != nil {
        return err
    }
    return s.sendConfirmation(order)
}
```

```go
// After — separate responsibilities behind interfaces
type OrderValidator interface {
    Validate(order Order) error
}

type PaymentProcessor interface {
    Charge(order Order) error
}

type InventoryManager interface {
    Update(order Order) error
}

type OrderNotifier interface {
    SendConfirmation(order Order) error
}

type OrderService struct {
    validator  OrderValidator
    payment    PaymentProcessor
    inventory  InventoryManager
    notifier   OrderNotifier
    repo       OrderRepository
}

func (s *OrderService) ProcessOrder(order Order) error {
    if err := s.validator.Validate(order); err != nil {
        return fmt.Errorf("validation failed: %w", err)
    }
    if err := s.payment.Charge(order); err != nil {
        return fmt.Errorf("payment failed: %w", err)
    }
    if err := s.inventory.Update(order); err != nil {
        return fmt.Errorf("inventory update failed: %w", err)
    }
    if err := s.repo.Save(order); err != nil {
        return fmt.Errorf("save failed: %w", err)
    }
    return s.notifier.SendConfirmation(order)
}
```

#### Finding 2

**Severity**: Important
**Category**: Error Handling
**File**: order_handler.go:42

The HTTP handler ignores the error from `json.NewDecoder(r.Body).Decode(&order)`. A malformed request body will result in a zero-value `Order` struct being processed silently.

```go
// Before
func (h *Handler) CreateOrder(w http.ResponseWriter, r *http.Request) {
    var order Order
    json.NewDecoder(r.Body).Decode(&order)
    h.service.ProcessOrder(order)
    w.WriteHeader(http.StatusCreated)
}
```

```go
// After
func (h *Handler) CreateOrder(w http.ResponseWriter, r *http.Request) {
    var order Order
    if err := json.NewDecoder(r.Body).Decode(&order); err != nil {
        http.Error(w, "invalid request body", http.StatusBadRequest)
        return
    }
    if err := h.service.ProcessOrder(order); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    w.WriteHeader(http.StatusCreated)
}
```

#### Finding 3

**Severity**: Important
**Category**: SOLID
**File**: email_sender.go:8

`email_sender.go` depends directly on the concrete `*smtp.Client` type. This violates the Dependency Inversion Principle and makes the email sender untestable without a real SMTP connection.

```go
// Before
type EmailSender struct {
    client *smtp.Client
}
```

```go
// After — depend on an interface
type Mailer interface {
    Send(to, subject, body string) error
}

type EmailSender struct {
    mailer Mailer
}
```

---

## Example 3: Legacy Code Quality Assessment

Reviewing Java code for maintainability and technical debt in a legacy monolith.

### User Prompt

> "Assess the code quality of our payment module — it's legacy code and we want to understand the technical debt before refactoring."

### Skill Execution

**Step 1 — Identify Review Scope**: User specifies files directly: `PaymentProcessor.java`, `PaymentUtils.java`, `PaymentConstants.java`. Single language: Java.

**Step 2 — Load Memory & Context**: Load `memoryStore.getSkillMemory("code-reviewer", "legacy-erp")`. Prior memory shows known issues with god classes and missing tests. Load `contextProvider.getDomainIndex("java")`.

**Step 3 — Load Relevant Context**: Load Java common issues via `contextProvider.getAlwaysLoadFiles("java")`. Load Spring patterns via `contextProvider.getConditionalContext("java", "spring")`.

**Step 4 — Deep Review**: Systematic review with emphasis on maintainability, naming, and test coverage.

**Step 5 — Generate Report & Update Memory**: Produce structured report and update project memory with new findings.

### Generated Review Output

#### Finding 1

**Severity**: Critical
**Category**: Maintainability
**File**: PaymentProcessor.java:1-850

`PaymentProcessor.java` is 850 lines long with 23 public methods. The class handles credit card processing, refunds, invoicing, receipt generation, audit logging, and retry logic. This god class has a cyclomatic complexity exceeding 150, making it nearly impossible to test or modify safely.

```java
// Before — single class with mixed concerns
public class PaymentProcessor {
    // 850 lines, 23 methods, 15 dependencies
    public PaymentResult processCard(CardDetails card, Amount amount) { ... }
    public RefundResult processRefund(String transactionId) { ... }
    public Invoice generateInvoice(PaymentResult result) { ... }
    public void sendReceipt(String email, Invoice invoice) { ... }
    public void logAuditTrail(PaymentEvent event) { ... }
    // ... 18 more methods
}
```

```java
// After — decompose into focused classes
public class CardPaymentService {
    PaymentResult processCard(CardDetails card, Amount amount) { ... }
}

public class RefundService {
    RefundResult processRefund(String transactionId) { ... }
}

public class InvoiceGenerator {
    Invoice generate(PaymentResult result) { ... }
}

public class PaymentNotifier {
    void sendReceipt(String email, Invoice invoice) { ... }
}

public class PaymentAuditLogger {
    void log(PaymentEvent event) { ... }
}
```

#### Finding 2

**Severity**: Important
**Category**: Naming
**File**: PaymentUtils.java:15

Utility methods have vague, misleading names. `process()` returns a boolean but doesn't indicate what it processes or what true/false means. `handle()` takes an `Object` parameter with no type safety. `doWork()` provides no indication of its purpose.

```java
// Before
public class PaymentUtils {
    public static boolean process(String s) { ... }
    public static Object handle(Object o) { ... }
    public static void doWork(String a, String b, int c) { ... }
}
```

```java
// After
public class PaymentValidation {
    public static boolean isValidCardNumber(String cardNumber) { ... }
}

public class PaymentFormatter {
    public static FormattedAmount formatCurrency(Amount amount) { ... }
}

public class TransactionRetry {
    public static void retryWithBackoff(String txId, String endpoint, int maxAttempts) { ... }
}
```

#### Finding 3

**Severity**: Important
**Category**: Testing
**File**: PaymentProcessor.java (entire file)

There are zero unit tests for `PaymentProcessor.java`. The 23 public methods, including critical payment logic, have no automated test coverage. The tight coupling to concrete database and SMTP clients makes the class untestable without significant refactoring.

**Recommended approach**:
1. Extract interfaces for external dependencies (`PaymentGateway`, `AuditStore`, `NotificationService`)
2. Add constructor injection for dependencies
3. Write tests for each extracted class starting with the highest-risk methods (`processCard`, `processRefund`)
4. Use test doubles for external dependencies

```java
// Step 1: Make testable with dependency injection
public class CardPaymentService {
    private final PaymentGateway gateway;
    private final TransactionRepository repository;

    public CardPaymentService(PaymentGateway gateway, TransactionRepository repository) {
        this.gateway = gateway;
        this.repository = repository;
    }

    // Now testable with mock gateway and repository
}
```

---

## Summary

These examples demonstrate the code-reviewer skill's language-agnostic approach:

1. **Cross-Language PR Review**: Handling multiple languages in a single review, identifying cross-cutting concerns like DRY violations across language boundaries
2. **Architecture & SOLID Review**: Deep structural analysis using SOLID principles, applicable to any object-oriented or interface-based language
3. **Legacy Code Assessment**: Evaluating technical debt, maintainability, and test coverage to guide refactoring priorities

Use these examples as reference when conducting reviews. Adapt the feedback style and technical depth to the codebase context.
