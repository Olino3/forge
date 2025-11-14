# Common Patterns: MyEcommerceApp

**Last Updated**: 2025-01-14

This file documents project-specific coding patterns, conventions, and architectural decisions that reviewers should recognize and validate against.

---

## Base Classes

### 1. ApiControllerBase

**Purpose**: Base class for all API controllers

**Location**: `WebApi/Controllers/ApiControllerBase.cs`

**Pattern**:
```csharp
public abstract class ApiControllerBase : ControllerBase
{
    protected readonly IMediator Mediator;
    protected readonly ILogger Logger;
    
    public ApiControllerBase(IMediator mediator, ILogger logger)
    {
        Mediator = mediator;
        Logger = logger;
    }
    
    protected ActionResult HandleResult<T>(Result<T> result)
    {
        if (result.IsSuccess)
            return Ok(result.Value);
        
        if (result.Error.Code == ErrorCode.NotFound)
            return NotFound(result.Error);
        
        if (result.Error.Code == ErrorCode.ValidationFailed)
            return BadRequest(result.Error);
        
        return StatusCode(500, result.Error);
    }
}
```

**Usage**: All controllers inherit from this, don't inject IMediator directly in controllers.

**Review Point**: 
- ✅ Controllers should inherit from `ApiControllerBase`
- ❌ Don't inject `IMediator` directly in controller constructors (it's in base class)

---

### 2. Result<T> Pattern

**Purpose**: Standardized return type for commands/queries

**Location**: `Application/Common/Result.cs`

**Pattern**:
```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public T Value { get; }
    public Error Error { get; }
    
    public static Result<T> Success(T value) => new(true, value, default);
    public static Result<T> Failure(Error error) => new(false, default, error);
}
```

**Usage**: All command/query handlers return `Result<T>` instead of throwing exceptions.

**Review Point**:
- ✅ Handlers should return `Result<T>`
- ❌ Don't throw exceptions in handlers (return `Result.Failure` instead)

---

## CQRS Pattern

### Command Structure

**Location**: `Application/Features/{Feature}/Commands/`

**Pattern**:
```csharp
// Command
public record CreateProductCommand(
    string Name,
    decimal Price,
    int CategoryId
) : IRequest<Result<ProductDto>>;

// Validator
public class CreateProductCommandValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(100);
        RuleFor(x => x.Price).GreaterThan(0);
        RuleFor(x => x.CategoryId).GreaterThan(0);
    }
}

// Handler
public class CreateProductCommandHandler(
    IProductRepository repository,
    IMapper mapper,
    ILogger<CreateProductCommandHandler> logger
) : IRequestHandler<CreateProductCommand, Result<ProductDto>>
{
    public async Task<Result<ProductDto>> Handle(
        CreateProductCommand request,
        CancellationToken cancellationToken)
    {
        // Implementation
    }
}
```

**Review Points**:
- ✅ Command is a `record` with `IRequest<Result<T>>`
- ✅ Validator exists for each command
- ✅ Handler uses primary constructor (C# 12)
- ✅ `CancellationToken` parameter present
- ✅ Returns `Result<T>`, not throwing exceptions

---

### Query Structure

**Location**: `Application/Features/{Feature}/Queries/`

**Pattern**:
```csharp
// Query
public record GetProductByIdQuery(int Id) : IRequest<Result<ProductDto>>;

// Handler
public class GetProductByIdQueryHandler(
    IProductRepository repository,
    IMapper mapper
) : IRequestHandler<GetProductByIdQuery, Result<ProductDto>>
{
    public async Task<Result<ProductDto>> Handle(
        GetProductByIdQuery request,
        CancellationToken cancellationToken)
    {
        var product = await repository.GetByIdAsync(request.Id, cancellationToken);
        
        if (product == null)
            return Result<ProductDto>.Failure(Error.NotFound("Product not found"));
        
        return Result<ProductDto>.Success(mapper.Map<ProductDto>(product));
    }
}
```

**Review Points**:
- ✅ Query is a `record` with `IRequest<Result<T>>`
- ✅ Queries have no side effects (read-only)
- ✅ Handler uses `IMapper` for DTO mapping
- ✅ Returns `Result.Failure` for not found, not throwing exception

---

## Validation Pipeline

### FluentValidation Registration

**Location**: `Application/DependencyInjection.cs`

**Pattern**:
```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        var assembly = Assembly.GetExecutingAssembly();
        
        services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(assembly));
        services.AddValidatorsFromAssembly(assembly);
        services.AddAutoMapper(assembly);
        
        // Validation pipeline behavior
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        
        return services;
    }
}
```

**ValidationBehavior**:
```csharp
public class ValidationBehavior<TRequest, TResponse>(
    IEnumerable<IValidator<TRequest>> validators
) : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!validators.Any())
            return await next();
        
        var context = new ValidationContext<TRequest>(request);
        var validationResults = await Task.WhenAll(
            validators.Select(v => v.ValidateAsync(context, cancellationToken)));
        
        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();
        
        if (failures.Any())
            throw new ValidationException(failures);
        
        return await next();
    }
}
```

**Review Points**:
- ✅ All commands have corresponding validators
- ✅ Validators registered automatically via assembly scanning
- ✅ Validation runs before handler via pipeline behavior

---

## Repository Pattern

### Interface

**Location**: `Application/Interfaces/IRepository.cs`

**Pattern**:
```csharp
public interface IRepository<T> where T : Entity
{
    Task<T?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<List<T>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<T> AddAsync(T entity, CancellationToken cancellationToken = default);
    Task UpdateAsync(T entity, CancellationToken cancellationToken = default);
    Task DeleteAsync(int id, CancellationToken cancellationToken = default);
}

public interface IProductRepository : IRepository<Product>
{
    Task<List<Product>> GetByCategoryAsync(int categoryId, CancellationToken cancellationToken = default);
    Task<List<Product>> GetExpensiveProductsAsync(decimal minPrice, CancellationToken cancellationToken = default);
}
```

**Implementation**:
```csharp
public class ProductRepository(ApplicationDbContext context) : IProductRepository
{
    public async Task<Product?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {
        return await context.Products.FindAsync(new object[] { id }, cancellationToken);
    }
    
    public async Task<List<Product>> GetByCategoryAsync(
        int categoryId,
        CancellationToken cancellationToken = default)
    {
        return await context.Products
            .Where(p => p.CategoryId == categoryId)
            .AsNoTracking()
            .ToListAsync(cancellationToken);
    }
}
```

**Review Points**:
- ✅ All data access goes through repositories
- ✅ Repositories use primary constructors
- ✅ All methods accept `CancellationToken`
- ✅ Query methods use `AsNoTracking()` for read-only data
- ❌ Don't inject `DbContext` directly into handlers (use repository)

---

## Domain Events

### Event Definition

**Location**: `Domain/Events/`

**Pattern**:
```csharp
public record OrderPlacedEvent(
    int OrderId,
    int CustomerId,
    decimal Total,
    DateTime PlacedAt
) : DomainEvent;

public abstract record DomainEvent
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public DateTime OccurredAt { get; init; } = DateTime.UtcNow;
}
```

### Event Handler

**Location**: `Application/Features/{Feature}/EventHandlers/`

**Pattern**:
```csharp
public class OrderPlacedEventHandler(
    IEmailService emailService,
    ILogger<OrderPlacedEventHandler> logger
) : INotificationHandler<OrderPlacedEvent>
{
    public async Task Handle(OrderPlacedEvent notification, CancellationToken cancellationToken)
    {
        logger.LogInformation("Order {OrderId} placed by customer {CustomerId}",
            notification.OrderId, notification.CustomerId);
        
        await emailService.SendOrderConfirmationAsync(
            notification.OrderId,
            cancellationToken);
    }
}
```

**Review Points**:
- ✅ Events are immutable `record` types
- ✅ Events inherit from `DomainEvent`
- ✅ Event handlers implement `INotificationHandler<T>`
- ✅ Multiple handlers can handle same event

---

## DTOs and Mapping

### DTO Naming Convention

**Pattern**:
```csharp
// Response DTOs (read)
public class ProductDto { }
public class ProductDetailDto { }
public class ProductSummaryDto { }

// Request DTOs (write)
public class CreateProductRequest { }
public class UpdateProductRequest { }
```

### AutoMapper Configuration

**Location**: `Application/Mappings/MappingProfile.cs`

**Pattern**:
```csharp
public class MappingProfile : Profile
{
    public MappingProfile()
    {
        CreateMap<Product, ProductDto>();
        CreateMap<Product, ProductDetailDto>()
            .ForMember(dest => dest.CategoryName,
                opt => opt.MapFrom(src => src.Category.Name));
        
        CreateMap<CreateProductRequest, Product>()
            .ForMember(dest => dest.Id, opt => opt.Ignore())
            .ForMember(dest => dest.CreatedAt, opt => opt.Ignore());
    }
}
```

**Review Points**:
- ✅ DTOs are separate from domain entities
- ✅ DTOs have `Dto`, `Request`, or `Response` suffix
- ✅ Mapping configured in `MappingProfile`
- ❌ Don't return domain entities from API (use DTOs)

---

## Error Handling

### Global Exception Handler

**Location**: `WebApi/Middleware/GlobalExceptionHandler.cs`

**Pattern**:
```csharp
public class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger) : IExceptionHandler
{
    public async ValueTask<bool> Handle WebApi/Controllers/ApiControllerBase.cs(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        logger.LogError(exception, "Unhandled exception occurred");
        
        var problemDetails = exception switch
        {
            ValidationException validationException => new ValidationProblemDetails
            {
                Status = StatusCodes.Status400BadRequest,
                Detail = "Validation failed",
                Errors = validationException.Errors
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Detail = "An error occurred processing your request"
            }
        };
        
        httpContext.Response.StatusCode = problemDetails.Status ?? 500;
        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);
        
        return true;
    }
}
```

**Review Points**:
- ✅ Exceptions handled globally, not in controllers
- ✅ ProblemDetails (RFC 7807) used for errors
- ✅ Validation exceptions return 400, not 500

---

## Dependency Injection Patterns

### Service Registration

**Location**: `WebApi/Program.cs`

**Pattern**:
```csharp
// Application layer
builder.Services.AddApplication();

// Infrastructure layer
builder.Services.AddInfrastructure(builder.Configuration);

// Repositories (Scoped)
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddScoped<IOrderRepository, OrderRepository>();

// Services (Scoped for stateful, Transient for stateless)
builder.Services.AddScoped<IEmailService, SendGridEmailService>();
builder.Services.AddTransient<IPdfGenerator, PdfGenerator>();

// HttpClients (named or typed)
builder.Services.AddHttpClient<IPaymentService, StripePaymentService>();
```

**Review Points**:
- ✅ Repositories are `Scoped` (DbContext lifetime)
- ✅ Services are `Scoped` or `Transient`
- ✅ Never register DbContext as `Singleton`
- ✅ HttpClient via `AddHttpClient`, never `new HttpClient()`

---

## Summary

When reviewing code for MyEcommerceApp, expect:

1. **Controllers** inherit from `ApiControllerBase`
2. **Commands/Queries** follow CQRS pattern with `Result<T>`
3. **Validation** via FluentValidation, automatic via pipeline
4. **Data Access** through repositories, not direct DbContext
5. **DTOs** for all API responses, never domain entities
6. **Primary Constructors** (C# 12) for services
7. **CancellationToken** in all async methods
8. **Domain Events** for cross-aggregate communication
9. **Global Exception Handling** via middleware
10. **Result Pattern** instead of exceptions in business logic

---

**Update this file when**:
- New patterns established
- Architecture decisions change
- New conventions adopted
- Common abstractions created

---

**Last Updated**: 2025-01-14 by Alice (Lead Developer)
