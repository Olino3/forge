# Testing Skill Examples

This file contains example testing scenarios demonstrating comprehensive test strategy design, test generation, and coverage improvement.

## Example 1: Test Strategy for a New Microservice

### User Prompt

> "I have a new Node.js API service for order management. It uses Express, PostgreSQL with Knex, and Redis for caching. I need a full test strategy — unit, integration, and E2E."

### Skill Execution

1. **Assess Testing Scope**: Identified Node.js/Express API with Knex ORM and Redis. No existing tests. Critical paths: order creation, payment validation, inventory checks, order status transitions.
2. **Load Memory & Context**: No prior memory for this project. Loaded testing context via `contextProvider.getDomainIndex("testing")`. Cross-skill discovery found schema analysis results for the orders database.
3. **Design Test Strategy**: Defined testing pyramid — 70% unit, 20% integration, 10% E2E. Selected Jest as test runner, Supertest for HTTP integration, and Playwright for E2E.
4. **Generate Tests**: Created unit tests for business logic, integration tests for API endpoints with test database, E2E tests for critical order flows.
5. **Validate & Update Memory**: All tests passing. Stored testing conventions and coverage baseline in project memory.

### Test Strategy Output

**Testing Pyramid**:
- **Unit (70%)**: Order validation, price calculation, discount logic, status transitions
- **Integration (20%)**: API endpoints with test database, Redis cache behavior, error responses
- **E2E (10%)**: Complete order flow (create → pay → fulfill), authentication flows

**Unit Test — Order Validation**:

```javascript
// tests/unit/orders/orderValidation.test.js
const { validateOrder } = require('../../../src/services/orderService');

describe('Order Validation', () => {
  describe('validateOrder', () => {
    it('should accept a valid order with required fields', () => {
      const order = {
        customerId: 'cust-123',
        items: [{ productId: 'prod-1', quantity: 2, price: 29.99 }],
        shippingAddress: { street: '123 Main St', city: 'Seattle', zip: '98101' }
      };

      const result = validateOrder(order);

      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject an order with no items', () => {
      const order = {
        customerId: 'cust-123',
        items: [],
        shippingAddress: { street: '123 Main St', city: 'Seattle', zip: '98101' }
      };

      const result = validateOrder(order);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Order must contain at least one item');
    });

    it('should reject an order with negative quantity', () => {
      const order = {
        customerId: 'cust-123',
        items: [{ productId: 'prod-1', quantity: -1, price: 29.99 }],
        shippingAddress: { street: '123 Main St', city: 'Seattle', zip: '98101' }
      };

      const result = validateOrder(order);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Item quantity must be positive');
    });

    it('should reject an order without a shipping address', () => {
      const order = {
        customerId: 'cust-123',
        items: [{ productId: 'prod-1', quantity: 1, price: 10.00 }]
      };

      const result = validateOrder(order);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Shipping address is required');
    });
  });
});
```

**Integration Test — Create Order API**:

```javascript
// tests/integration/orders/createOrder.test.js
const request = require('supertest');
const app = require('../../../src/app');
const { setupTestDb, teardownTestDb, seedTestData } = require('../../helpers/db');

describe('POST /api/orders', () => {
  beforeAll(async () => {
    await setupTestDb();
  });

  afterAll(async () => {
    await teardownTestDb();
  });

  beforeEach(async () => {
    await seedTestData();
  });

  it('should create an order and return 201 with order details', async () => {
    const newOrder = {
      customerId: 'cust-123',
      items: [{ productId: 'prod-1', quantity: 2 }],
      shippingAddress: { street: '123 Main St', city: 'Seattle', zip: '98101' }
    };

    const response = await request(app)
      .post('/api/orders')
      .send(newOrder)
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      status: 'pending',
      customerId: 'cust-123',
      totalItems: 2
    });
  });

  it('should return 400 when required fields are missing', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({ customerId: 'cust-123' })
      .expect(400);

    expect(response.body.errors).toBeDefined();
  });

  it('should return 404 when product does not exist', async () => {
    const newOrder = {
      customerId: 'cust-123',
      items: [{ productId: 'nonexistent-prod', quantity: 1 }],
      shippingAddress: { street: '123 Main St', city: 'Seattle', zip: '98101' }
    };

    const response = await request(app)
      .post('/api/orders')
      .send(newOrder)
      .expect(404);

    expect(response.body.error).toContain('Product not found');
  });

  it('should return 409 when inventory is insufficient', async () => {
    const newOrder = {
      customerId: 'cust-123',
      items: [{ productId: 'prod-1', quantity: 999999 }],
      shippingAddress: { street: '123 Main St', city: 'Seattle', zip: '98101' }
    };

    const response = await request(app)
      .post('/api/orders')
      .send(newOrder)
      .expect(409);

    expect(response.body.error).toContain('Insufficient inventory');
  });
});
```

**E2E Test — Complete Order Flow**:

```javascript
// tests/e2e/orderFlow.test.js
const { test, expect } = require('@playwright/test');

test.describe('Order Management Flow', () => {
  test('should complete a full order lifecycle: browse → add to cart → checkout → confirm', async ({ page }) => {
    await page.goto('/products');

    await page.click('[data-testid="product-card-1"] >> text=Add to Cart');
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');

    await page.click('[data-testid="cart-icon"]');
    await expect(page.locator('[data-testid="cart-item"]')).toHaveCount(1);

    await page.click('text=Proceed to Checkout');
    await page.fill('[data-testid="shipping-street"]', '123 Main St');
    await page.fill('[data-testid="shipping-city"]', 'Seattle');
    await page.fill('[data-testid="shipping-zip"]', '98101');
    await page.click('text=Place Order');

    await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible();
    await expect(page.locator('[data-testid="order-status"]')).toHaveText('Pending');
  });
});
```

---

## Example 2: Increasing Coverage for Legacy Python Code

### User Prompt

> "We have a legacy Python billing module with 15% test coverage. The business logic is complex with lots of dependencies on external services. Help me get coverage above 80%."

### Skill Execution

1. **Assess Testing Scope**: Identified Python billing module using no test framework (only a few ad-hoc scripts). Critical paths: invoice generation, tax calculation, payment processing, refund logic. Heavy dependencies on Stripe API and an internal user service.
2. **Load Memory & Context**: No prior memory. Loaded testing and Python context. Cross-skill discovery found a prior code review flagging untested error handling in payment processing.
3. **Design Test Strategy**: Pyramid — 80% unit (isolate business logic from dependencies), 15% integration (verify Stripe and DB interactions), 5% E2E. Selected pytest with fixtures and unittest.mock for dependency isolation.
4. **Generate Tests**: Created focused unit tests for tax calculation and invoice generation with mocked external dependencies. Added integration tests for payment processing using Stripe test mode.
5. **Validate & Update Memory**: Coverage increased from 15% to 83%. Stored coverage baseline and mocking patterns in memory.

### Generated Tests Output

**Unit Test — Tax Calculation with Mocked Dependencies**:

```python
# tests/unit/test_tax_calculation.py
import pytest
from unittest.mock import patch, MagicMock
from billing.tax_calculator import TaxCalculator

class TestTaxCalculator:
    @pytest.fixture
    def calculator(self):
        return TaxCalculator()

    @pytest.fixture
    def sample_line_items(self):
        return [
            {"description": "Widget A", "amount": 100.00, "taxable": True},
            {"description": "Widget B", "amount": 50.00, "taxable": True},
            {"description": "Shipping", "amount": 10.00, "taxable": False},
        ]

    def test_calculates_tax_for_taxable_items_only(self, calculator, sample_line_items):
        result = calculator.calculate(sample_line_items, tax_rate=0.10)

        assert result.tax_amount == 15.00  # 10% of (100 + 50)
        assert result.subtotal == 160.00
        assert result.total == 175.00

    def test_handles_zero_tax_rate(self, calculator, sample_line_items):
        result = calculator.calculate(sample_line_items, tax_rate=0.0)

        assert result.tax_amount == 0.0
        assert result.total == 160.00

    def test_handles_empty_line_items(self, calculator):
        result = calculator.calculate([], tax_rate=0.10)

        assert result.tax_amount == 0.0
        assert result.subtotal == 0.0
        assert result.total == 0.0

    def test_raises_error_for_negative_amounts(self, calculator):
        items = [{"description": "Refund", "amount": -50.00, "taxable": True}]

        with pytest.raises(ValueError, match="Line item amount cannot be negative"):
            calculator.calculate(items, tax_rate=0.10)

    @patch("billing.tax_calculator.TaxRateService")
    def test_fetches_regional_tax_rate_when_not_provided(self, mock_service, calculator):
        mock_service.return_value.get_rate.return_value = 0.0875
        items = [{"description": "Widget", "amount": 100.00, "taxable": True}]

        result = calculator.calculate(items, region="WA")

        mock_service.return_value.get_rate.assert_called_once_with("WA")
        assert result.tax_amount == 8.75
```

**Unit Test — Invoice Generation with Mocked External Service**:

```python
# tests/unit/test_invoice_generator.py
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from billing.invoice_generator import InvoiceGenerator

class TestInvoiceGenerator:
    @pytest.fixture
    def mock_user_service(self):
        with patch("billing.invoice_generator.UserService") as mock:
            service = mock.return_value
            service.get_user.return_value = {
                "id": "user-123",
                "name": "Jane Doe",
                "email": "jane@example.com",
                "billing_address": "456 Oak Ave, Portland, OR 97201"
            }
            yield service

    @pytest.fixture
    def generator(self, mock_user_service):
        return InvoiceGenerator()

    def test_generates_invoice_with_correct_totals(self, generator):
        line_items = [
            {"description": "Service A", "amount": 200.00},
            {"description": "Service B", "amount": 150.00},
        ]

        invoice = generator.create_invoice("user-123", line_items)

        assert invoice.subtotal == 350.00
        assert invoice.invoice_number is not None
        assert invoice.date == date.today()

    def test_generates_unique_invoice_numbers(self, generator):
        items = [{"description": "Service", "amount": 100.00}]

        invoice1 = generator.create_invoice("user-123", items)
        invoice2 = generator.create_invoice("user-123", items)

        assert invoice1.invoice_number != invoice2.invoice_number

    def test_raises_error_for_unknown_user(self, mock_user_service):
        mock_user_service.get_user.side_effect = ValueError("User not found")
        generator = InvoiceGenerator()
        items = [{"description": "Service", "amount": 100.00}]

        with pytest.raises(ValueError, match="User not found"):
            generator.create_invoice("unknown-user", items)
```

**Integration Test — Payment Processing with Stripe Test Mode**:

```python
# tests/integration/test_payment_processing.py
import pytest
from billing.payment_processor import PaymentProcessor

@pytest.fixture
def processor():
    return PaymentProcessor(api_key="sk_test_fake_key")

@pytest.mark.integration
class TestPaymentProcessing:
    def test_successful_charge(self, processor, mocker):
        mock_stripe = mocker.patch("billing.payment_processor.stripe.Charge.create")
        mock_stripe.return_value = {"id": "ch_123", "status": "succeeded", "amount": 5000}

        result = processor.charge("cust-123", amount=50.00, currency="usd")

        assert result["status"] == "succeeded"
        mock_stripe.assert_called_once_with(
            amount=5000, currency="usd", customer="cust-123"
        )

    def test_handles_declined_card(self, processor, mocker):
        import stripe
        mocker.patch(
            "billing.payment_processor.stripe.Charge.create",
            side_effect=stripe.error.CardError("Card declined", param=None, code="card_declined")
        )

        with pytest.raises(Exception, match="Card declined"):
            processor.charge("cust-123", amount=50.00, currency="usd")

    def test_handles_network_timeout(self, processor, mocker):
        import stripe
        mocker.patch(
            "billing.payment_processor.stripe.Charge.create",
            side_effect=stripe.error.APIConnectionError("Network error")
        )

        with pytest.raises(Exception, match="Network error"):
            processor.charge("cust-123", amount=50.00, currency="usd")
```

---

## Example 3: E2E Testing with Playwright

### User Prompt

> "We have a React web application for a project management tool. I need E2E tests for the critical user journeys — login, creating a project, adding tasks, and inviting team members."

### Skill Execution

1. **Assess Testing Scope**: Identified React SPA with REST API backend. Existing unit tests with Jest/React Testing Library (60% coverage) but zero E2E tests. Critical user journeys: authentication, project CRUD, task management, team collaboration.
2. **Load Memory & Context**: Found prior memory from `generate-jest-unit-tests` skill with component test patterns. Loaded testing context for E2E strategies.
3. **Design Test Strategy**: E2E tests only (unit tests already exist). Selected Playwright for cross-browser support. Designed tests around 4 critical user journeys. Created Page Object Model for maintainability.
4. **Generate Tests**: Created Playwright tests with page objects, proper selectors, and assertions for all critical journeys.
5. **Validate & Update Memory**: All E2E tests passing across Chromium, Firefox, and WebKit. Stored Playwright configuration and page object patterns in memory.

### Generated Tests Output

**Playwright Configuration**:

```javascript
// playwright.config.js
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
```

**Page Object — Login Page**:

```javascript
// tests/e2e/pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

module.exports = { LoginPage };
```

**Page Object — Dashboard Page**:

```javascript
// tests/e2e/pages/DashboardPage.js
class DashboardPage {
  constructor(page) {
    this.page = page;
    this.createProjectButton = page.locator('[data-testid="create-project-btn"]');
    this.projectCards = page.locator('[data-testid="project-card"]');
    this.welcomeMessage = page.locator('[data-testid="welcome-message"]');
  }

  async createProject(name, description) {
    await this.createProjectButton.click();
    await this.page.fill('[data-testid="project-name-input"]', name);
    await this.page.fill('[data-testid="project-description-input"]', description);
    await this.page.click('[data-testid="submit-project-btn"]');
  }
}

module.exports = { DashboardPage };
```

**E2E Test — Authentication Flow**:

```javascript
// tests/e2e/auth.spec.js
const { test, expect } = require('@playwright/test');
const { LoginPage } = require('./pages/LoginPage');
const { DashboardPage } = require('./pages/DashboardPage');

test.describe('Authentication', () => {
  test('should log in successfully with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'ValidPass123!');

    const dashboard = new DashboardPage(page);
    await expect(dashboard.welcomeMessage).toBeVisible();
    await expect(dashboard.welcomeMessage).toContainText('Welcome');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'WrongPassword');

    await expect(loginPage.errorMessage).toBeVisible();
    await expect(loginPage.errorMessage).toContainText('Invalid email or password');
  });

  test('should redirect unauthenticated users to login', async ({ page }) => {
    await page.goto('/dashboard');

    await expect(page).toHaveURL(/\/login/);
  });
});
```

**E2E Test — Project and Task Management**:

```javascript
// tests/e2e/projectManagement.spec.js
const { test, expect } = require('@playwright/test');
const { LoginPage } = require('./pages/LoginPage');
const { DashboardPage } = require('./pages/DashboardPage');

test.describe('Project Management', () => {
  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'ValidPass123!');
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
  });

  test('should create a new project and verify it appears on dashboard', async ({ page }) => {
    const dashboard = new DashboardPage(page);
    const projectName = `Test Project ${Date.now()}`;

    await dashboard.createProject(projectName, 'A test project for E2E validation');

    await expect(page.locator(`text=${projectName}`)).toBeVisible();
  });

  test('should add a task to a project', async ({ page }) => {
    await page.click('[data-testid="project-card"] >> nth=0');
    await page.click('[data-testid="add-task-btn"]');
    await page.fill('[data-testid="task-title-input"]', 'Implement user authentication');
    await page.selectOption('[data-testid="task-priority-select"]', 'high');
    await page.click('[data-testid="save-task-btn"]');

    await expect(page.locator('text=Implement user authentication')).toBeVisible();
    await expect(page.locator('[data-testid="task-item"] >> nth=0')).toContainText('High');
  });

  test('should invite a team member to a project', async ({ page }) => {
    await page.click('[data-testid="project-card"] >> nth=0');
    await page.click('[data-testid="settings-tab"]');
    await page.click('[data-testid="invite-member-btn"]');
    await page.fill('[data-testid="invite-email-input"]', 'teammate@example.com');
    await page.selectOption('[data-testid="invite-role-select"]', 'editor');
    await page.click('[data-testid="send-invite-btn"]');

    await expect(page.locator('text=Invitation sent')).toBeVisible();
    await expect(page.locator('[data-testid="team-member-list"]')).toContainText('teammate@example.com');
  });
});
```

---

## Summary of Testing Patterns

1. **Test Strategy**: Always define the testing pyramid balance based on architecture and risk
2. **Unit Tests**: Isolate business logic, mock external dependencies, cover edge cases
3. **Integration Tests**: Verify component interactions with real (or test) infrastructure
4. **E2E Tests**: Validate critical user journeys end-to-end across the full stack
5. **Test Data**: Use factories and fixtures for repeatable, isolated test data
6. **Mocking**: Mock at the boundary — prefer real implementations where feasible
7. **Page Objects**: Use the Page Object Model for maintainable E2E tests

Use these examples as reference when designing test strategies. Adapt the patterns and depth to the project's specific framework, architecture, and testing maturity.
