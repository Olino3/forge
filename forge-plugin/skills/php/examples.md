# PHP Skill Examples

This file provides sample usage scenarios for the `php` skill.

---

## Example 1: Laravel API Resource

### Scenario
A Laravel app needs standardized API responses for orders.

### User Prompt
"Create a Laravel API resource for orders with nested items."

### Skill Execution
- **Step 1**: Confirm Laravel version and response conventions.
- **Step 2**: Load memory for `orders-api`.
- **Step 3**: Load engineering and security context.
- **Step 4**: Inspect existing controllers and models.
- **Step 5**: Recommend Resource classes and transformer structure.
- **Step 6**: Output to `/claudedocs/php_orders-api_2026-02-12.md`.

### Generated Output
```markdown
# PHP Guidance - orders-api

## API Resource Plan
- Create `OrderResource` with `items` relationship
- Use `OrderCollection` for pagination metadata
- Add `OrderItemResource` for nested items
```

---

## Example 2: Symfony Command and Service Injection

### Scenario
A Symfony app needs a CLI command with injected services.

### User Prompt
"Build a Symfony console command that exports invoices nightly."

### Skill Execution
- **Step 1**: Confirm Symfony version and service container setup.
- **Step 2**: Load memory for CLI conventions.
- **Step 3**: Load engineering context.
- **Step 4**: Inspect existing services.
- **Step 5**: Recommend command structure and dependency injection.
- **Step 6**: Output to `/claudedocs/php_invoices_2026-02-12.md`.

### Generated Output
```markdown
# PHP Guidance - invoices

## Symfony Command
- Create `ExportInvoicesCommand` in `src/Command`
- Inject `InvoiceExporter` via constructor
- Schedule via cron or Symfony Scheduler
```

---

## Example 3: Composer Package Structure

### Scenario
A team wants to publish a reusable PHP library.

### User Prompt
"Structure a PHP package with Composer and PHPUnit tests."

### Skill Execution
- **Step 1**: Confirm package scope and PHP version.
- **Step 2**: Load memory for packaging conventions.
- **Step 3**: Load engineering context.
- **Step 4**: Review expected public API.
- **Step 5**: Recommend PSR-4 structure and testing setup.
- **Step 6**: Output to `/claudedocs/php_package_2026-02-12.md`.

### Generated Output
```markdown
# PHP Guidance - package

## Package Layout
- `src/` for production code
- `tests/` for PHPUnit
- `composer.json` with PSR-4 autoload

## Testing
- Use PHPUnit 10 with `tests/bootstrap.php`
- Add CI job for `composer test`
```
