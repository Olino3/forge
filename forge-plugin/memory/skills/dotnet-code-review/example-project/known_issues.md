# Known Issues: MyEcommerceApp

**Last Updated**: 2025-01-14

This file tracks recurring issues discovered in code reviews. Issues are organized by category and severity, with frequency tracking to identify persistent problems.

---

## 🔴 Critical Issues

### None Currently

---

## 🟠 High Severity Issues

### 1. Missing CancellationToken Propagation

**Issue**: Async methods don't accept or propagate CancellationToken

**Frequency**: Found in 8 out of 10 reviews

**Severity**: High (impacts request cancellation, potential resource leaks)

**Affected Areas**:
- `Application/Features/Orders/Commands/` - 5 command handlers
- `Application/Features/Products/Queries/` - 3 query handlers
- `Infrastructure/Services/EmailService.cs`

**Examples**:
```csharp
// ❌ Bad - missing CancellationToken
public async Task<Order> GetOrderAsync(int id)
{
    return await _repository.GetByIdAsync(id);
}

// ✅ Should be
public async Task<Order> GetOrderAsync(int id, CancellationToken cancellationToken = default)
{
    return await _repository.GetByIdAsync(id, cancellationToken);
}
```

**Status**: ⚠️ Ongoing - developers frequently forget this

**Action Items**:
- Add analyzer rule to detect missing CancellationToken
- Update code review checklist
- Team training on async best practices

**History**:
- 2024-12: Found in 3 PRs
- 2025-01: Found in 2 PRs (slight improvement)

---

### 2. N+1 Query in Order Processing

**Issue**: Loading orders with items causes N+1 query

**Frequency**: Reoccurred in 3 reviews after being fixed

**Severity**: High (performance issue, scales with data)

**Affected Areas**:
- `Application/Features/Orders/Queries/GetOrderDetailsQuery.cs`
- `Application/Features/Orders/Queries/GetCustomerOrdersQuery.cs`

**Example**:
```csharp
// ❌ Bad - N+1 query
var orders = await _context.Orders
    .Where(o => o.CustomerId == customerId)
    .ToListAsync(); // Query 1: Get all orders

foreach (var order in orders)
{
    var items = await _context.OrderItems
        .Where(i => i.OrderId == order.Id)
        .ToListAsync(); // Query 2, 3, 4... N+1 queries!
}

// ✅ Should be
var orders = await _context.Orders
    .Include(o => o.OrderItems)
    .Where(o => o.CustomerId == customerId)
    .ToListAsync(); // Single query with JOIN
```

**Status**: ⚠️ Recurring - fixed multiple times, keeps coming back

**Root Cause**: Developers not aware of eager loading patterns

**Action Items**:
- ✅ Added `EnsureCorrectEagerLoading` analyzer
- Document Include/ThenInclude patterns in team wiki
- Code review focus: Always check for Include when accessing navigation properties

**History**:
- 2024-10: First occurrence in PR #187
- 2024-11: Fixed in PR #198
- 2024-12: Reoccurred in PR #245 (different developer)
- 2025-01: Reoccurred in PR #283 (new team member)

---

### 3. Async Void Event Handlers

**Issue**: Event handlers using `async void` instead of `async Task`

**Frequency**: Found in 4 reviews

**Severity**: High (exceptions crash application)

**Affected Areas**:
- Custom event handlers in `WebApi/EventHandlers/`

**Example**:
```csharp
// ❌ CRITICAL - async void
private async void OnOrderPlaced(object sender, OrderPlacedEventArgs e)
{
    await _emailService.SendOrderConfirmationAsync(e.OrderId);
    // If exception thrown here, application crashes!
}

// ✅ Should be
private async Task OnOrderPlaced(object sender, OrderPlacedEventArgs e)
{
    try
    {
        await _emailService.SendOrderConfirmationAsync(e.OrderId);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Failed to send order confirmation for order {OrderId}", e.OrderId);
    }
}
```

**Status**: ✅ Mostly resolved - analyzer added, catches most cases

**Action Items**:
- ✅ Analyzer rule enabled (CA2012)
- Team trained on async void dangers

**History**:
- 2024-11: Found in 4 different files
- 2024-12: All fixed
- 2025-01: No new occurrences

---

## 🟡 Medium Severity Issues

### 4. Direct DbContext Usage in Controllers

**Issue**: Some controllers inject `DbContext` directly instead of using repositories

**Frequency**: Found in 6 reviews

**Severity**: Medium (architectural violation, hard to test)

**Affected Areas**:
- Legacy controllers in `WebApi/Controllers/LegacyOrdersController.cs`
- Some admin endpoints

**Example**:
```csharp
// ❌ Bad - direct DbContext in controller
public class OrdersController(ApplicationDbContext context) : ApiControllerBase
{
    [HttpGet("{id}")]
    public async Task<ActionResult<Order>> GetOrder(int id)
    {
        var order = await context.Orders.FindAsync(id);
        if (order == null) return NotFound();
        return Ok(order);
    }
}

// ✅ Should be
public class OrdersController(
    IMediator mediator,
    ILogger<OrdersController> logger
) : ApiControllerBase(mediator, logger)
{
    [HttpGet("{id}")]
    public async Task<ActionResult<OrderDto>> GetOrder(int id)
    {
        var result = await Mediator.Send(new GetOrderByIdQuery(id));
        return HandleResult(result);
    }
}
```

**Status**: 🔄 In Progress - migrating legacy controllers

**Action Items**:
- ✅ Created migration plan
- 🔄 Migrating 3 controllers per sprint
- Target completion: 2025-Q2

**History**:
- 2024-09: Identified 12 legacy controllers
- 2024-10-12: Migrated 4 controllers
- 2025-01: 6 remaining

---

### 5. Missing Null Checks on Navigation Properties

**Issue**: Accessing navigation properties without null checks

**Frequency**: Found in 5 reviews

**Severity**: Medium (potential NullReferenceException)

**Affected Areas**:
- DTO mapping in `Application/Mappings/`
- Query handlers

**Example**:
```csharp
// ❌ Bad - no null check
public class ProductDto
{
    public string CategoryName => Product.Category.Name; // NullReferenceException if Category is null!
}

// ✅ Should be
public class ProductDto
{
    public string? CategoryName => Product.Category?.Name;
}

// Or in mapping configuration
CreateMap<Product, ProductDto>()
    .ForMember(dest => dest.CategoryName,
        opt => opt.MapFrom(src => src.Category != null ? src.Category.Name : null));
```

**Status**: ⚠️ Ongoing

**Action Items**:
- Enable nullable reference types project-wide (currently partial)
- Review all navigation property mappings

**History**:
- Recurring issue since project start
- Improved with nullable reference types enabled in Application layer
- Still occurring in Infrastructure and WebApi layers

---

### 6. Sync-over-Async in Background Services

**Issue**: Blocking on async code with `.Result` or `.Wait()`

**Frequency**: Found in 3 reviews

**Severity**: Medium (potential deadlocks, but .NET Core 3.0+ mitigates)

**Affected Areas**:
- `Infrastructure/BackgroundServices/OrderProcessingService.cs`
- `Infrastructure/BackgroundServices/InventoryUpdateService.cs`

**Example**:
```csharp
// ❌ Bad - sync-over-async
protected override void ExecuteAsync(CancellationToken stoppingToken)
{
    while (!stoppingToken.IsCancellationRequested)
    {
        var orders = _orderService.GetPendingOrdersAsync().Result; // Blocks thread!
        ProcessOrders(orders);
        Thread.Sleep(5000);
    }
}

// ✅ Should be
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    while (!stoppingToken.IsCancellationRequested)
    {
        var orders = await _orderService.GetPendingOrdersAsync(stoppingToken);
        await ProcessOrdersAsync(orders, stoppingToken);
        await Task.Delay(5000, stoppingToken);
    }
}
```

**Status**: ✅ Mostly resolved

**History**:
- 2024-11: Found in 3 background services
- 2024-12: All fixed
- 2025-01: No new occurrences

---

## 🟢 Low Severity Issues

### 7. Inconsistent Logging Levels

**Issue**: Using incorrect log levels for events

**Frequency**: Found in 7 reviews

**Severity**: Low (operational, not functional)

**Pattern**:
```csharp
// ❌ Bad - logging normal operation as Warning
_logger.LogWarning("User {UserId} logged in", userId);

// ✅ Should be
_logger.LogInformation("User {UserId} logged in", userId);

// ❌ Bad - logging exception as Information
_logger.LogInformation("Failed to send email: {Error}", ex.Message);

// ✅ Should be
_logger.LogError(ex, "Failed to send email to {Email}", emailAddress);
```

**Status**: 🔄 Ongoing education

**Guidelines**:
- **Trace**: Very detailed, development only
- **Debug**: Detailed, for debugging specific issues
- **Information**: Normal application flow
- **Warning**: Unexpected but handled (e.g., retry logic kicked in)
- **Error**: Failed operation that needs attention
- **Critical**: Application crash or data loss

---

### 8. Missing XML Documentation Comments

**Issue**: Public APIs lack XML documentation

**Frequency**: Found in most reviews

**Severity**: Low (documentation, not functional)

**Affected**: All public APIs, DTOs, commands, queries

**Example**:
```csharp
// ❌ Bad - no documentation
public record CreateProductCommand(string Name, decimal Price);

// ✅ Should be
/// <summary>
/// Command to create a new product in the catalog.
/// </summary>
/// <param name="Name">The product name (max 100 characters).</param>
/// <param name="Price">The product price (must be positive).</param>
public record CreateProductCommand(string Name, decimal Price);
```

**Status**: 🔄 Gradual improvement

**Action Items**:
- Enable XML documentation generation
- Add to PR checklist
- Target: 80% coverage by 2025-Q2

---

## 📊 Issue Trends

### Improving
- ✅ Async void usage (down from 4 to 0)
- ✅ Sync-over-async (down from 5 to 0)
- ✅ Proper exception handling (improved with global handler)

### Persistent Issues
- ⚠️ Missing CancellationToken (8 occurrences in 10 reviews)
- ⚠️ N+1 queries (3 recurrences after fixes)
- ⚠️ Navigation property null checks (ongoing)

### New Issue Categories (Watch For)
- 🆕 ValueTask misuse (1 occurrence in 2025-01)
- 🆕 IAsyncEnumerable not used for streaming (2 occurrences)

---

## 🎯 Focus Areas for Next Reviews

Based on frequency and severity:

1. **High Priority**: CancellationToken propagation
2. **High Priority**: N+1 query detection
3. **Medium Priority**: Complete CQRS migration (legacy controllers)
4. **Medium Priority**: Enable nullable reference types everywhere
5. **Low Priority**: XML documentation coverage

---

## 📝 Notes for Reviewers

### Quick Wins
- Always check: CancellationToken in async methods
- Always check: Include() when accessing navigation properties
- Always check: Result<T> return type in handlers

### Red Flags
- 🚩 `.Result` or `.Wait()` on Task
- 🚩 `async void` outside event handlers
- 🚩 Direct DbContext injection in controllers
- 🚩 Returning domain entities from API (use DTOs)
- 🚩 `new HttpClient()` (use IHttpClientFactory)

---

**Update this file after every review**:
- Increment frequency for recurring issues
- Add new issues discovered
- Mark resolved issues with ✅
- Track trends (improving/worsening)

---

**Last Updated**: 2025-01-14 after Review #10
