# Blazor Component Patterns

This file documents Blazor-specific patterns for component development, state management, and rendering optimization for both Blazor Server and Blazor WebAssembly.

## Purpose

Load this file when reviewing:
- `.razor` files (Blazor components)
- Component lifecycle code
- State management
- JavaScript interop
- Blazor-specific patterns

---

## 1. Component Lifecycle

### 1.1 Lifecycle Method Order

```csharp
// Lifecycle execution order:
// 1. Constructor
// 2. SetParametersAsync
// 3. OnInitialized / OnInitializedAsync
// 4. OnParametersSet / OnParametersSetAsync
// 5. OnAfterRender / OnAfterRenderAsync (firstRender = true)
// 6. OnParametersSet / OnParametersSetAsync (when parameters change)
// 7. OnAfterRender / OnAfterRenderAsync (firstRender = false)

// ✅ Good - proper lifecycle usage
@code {
    [Parameter] public int ProductId { get; set; }
    
    private Product? _product;
    private bool _isLoading = true;
    
    protected override async Task OnInitializedAsync()
    {
        // One-time initialization
        await LoadProductAsync();
    }
    
    protected override async Task OnParametersSetAsync()
    {
        // Reload when ProductId changes
        if (ProductId != _product?.Id)
        {
            await LoadProductAsync();
        }
    }
    
    protected override void OnAfterRender(bool firstRender)
    {
        if (firstRender)
        {
            // Initialize JavaScript components
        }
    }
    
    private async Task LoadProductAsync()
    {
        _isLoading = true;
        _product = await ProductService.GetByIdAsync(ProductId);
        _isLoading = false;
    }
}

// ❌ Bad - loading data in OnAfterRender
protected override async Task OnAfterRenderAsync(bool firstRender)
{
    if (firstRender)
    {
        _product = await ProductService.GetByIdAsync(ProductId);
        StateHasChanged(); // Causes double render
    }
}
```

### 1.2 Async Initialization

**Best Practice**: Use `OnInitializedAsync`, not `OnInitialized` for async work.

```csharp
// ✅ Good - OnInitializedAsync
protected override async Task OnInitializedAsync()
{
    _products = await ProductService.GetAllAsync();
}

// ❌ Bad - async void in OnInitialized
protected override void OnInitialized()
{
    _ = LoadDataAsync(); // Fire-and-forget, errors swallowed
}

private async Task LoadDataAsync()
{
    _products = await ProductService.GetAllAsync();
    StateHasChanged();
}
```

---

## 2. Component Parameters

### 2.1 Parameter Validation

**Best Practice**: Validate parameters in `OnParametersSet`.

```csharp
// ✅ Good - parameter validation
@code {
    [Parameter, EditorRequired]
    public int ProductId { get; set; }
    
    [Parameter]
    public EventCallback<Product> OnSave { get; set; }
    
    protected override void OnParametersSet()
    {
        if (ProductId <= 0)
        {
            throw new ArgumentException("ProductId must be positive", nameof(ProductId));
        }
    }
}

// ❌ Bad - no validation
[Parameter]
public int ProductId { get; set; } // Could be 0, negative
```

### 2.2 EventCallback vs Action

**Best Practice**: Use `EventCallback` for parent notifications.

```csharp
// ✅ Good - EventCallback (triggers parent re-render)
@code {
    [Parameter]
    public EventCallback<Product> OnProductSelected { get; set; }
    
    private async Task SelectProduct(Product product)
    {
        await OnProductSelected.InvokeAsync(product);
    }
}

// ❌ Bad - Action (doesn't trigger parent re-render)
@code {
    [Parameter]
    public Action<Product>? OnProductSelected { get; set; }
    
    private void SelectProduct(Product product)
    {
        OnProductSelected?.Invoke(product); // Parent may not re-render
    }
}
```

### 2.3 Cascading Parameters

**Best Practice**: Use cascading parameters for deeply nested shared state.

```csharp
// Parent component
<CascadingValue Value="@_currentUser">
    <ChildComponent />
</CascadingValue>

@code {
    private User? _currentUser;
}

// Child component (any level deep)
@code {
    [CascadingParameter]
    public User? CurrentUser { get; set; }
    
    protected override void OnParametersSet()
    {
        if (CurrentUser == null)
        {
            throw new InvalidOperationException("CurrentUser required");
        }
    }
}
```

---

## 3. State Management

### 3.1 Component State

**Best Practice**: Keep component-specific state in the component.

```csharp
// ✅ Good - component state
@page "/products"
@inject IProductService ProductService

<h3>Products</h3>

@if (_isLoading)
{
    <p>Loading...</p>
}
else if (_error != null)
{
    <p class="error">@_error</p>
}
else
{
    <ul>
        @foreach (var product in _products)
        {
            <li>@product.Name - @product.Price.ToString("C")</li>
        }
    </ul>
}

@code {
    private List<Product> _products = new();
    private bool _isLoading = true;
    private string? _error;
    
    protected override async Task OnInitializedAsync()
    {
        try
        {
            _products = await ProductService.GetAllAsync();
        }
        catch (Exception ex)
        {
            _error = ex.Message;
        }
        finally
        {
            _isLoading = false;
        }
    }
}
```

### 3.2 Application State

**Best Practice**: Use services for app-wide state.

```csharp
// ✅ Good - app state service
public class AppState
{
    private User? _currentUser;
    
    public event Action? OnChange;
    
    public User? CurrentUser
    {
        get => _currentUser;
        set
        {
            _currentUser = value;
            NotifyStateChanged();
        }
    }
    
    private void NotifyStateChanged() => OnChange?.Invoke();
}

// Register as scoped (Blazor Server) or singleton (Blazor WASM)
builder.Services.AddScoped<AppState>();

// Component usage
@implements IDisposable
@inject AppState AppState

<p>Current user: @AppState.CurrentUser?.Name</p>

@code {
    protected override void OnInitialized()
    {
        AppState.OnChange += StateHasChanged;
    }
    
    public void Dispose()
    {
        AppState.OnChange -= StateHasChanged; // Prevent memory leak
    }
}
```

---

## 4. Rendering Optimization

### 4.1 StateHasChanged

**Best Practice**: Call `StateHasChanged` only when needed.

```csharp
// ✅ Good - StateHasChanged after async callback
private Timer? _timer;

protected override void OnInitialized()
{
    _timer = new Timer(async _ =>
    {
        _currentTime = DateTime.Now;
        await InvokeAsync(StateHasChanged); // Required for timer callback
    }, null, TimeSpan.Zero, TimeSpan.FromSeconds(1));
}

// ❌ Bad - unnecessary StateHasChanged
private async Task LoadDataAsync()
{
    _products = await ProductService.GetAllAsync();
    StateHasChanged(); // Not needed, automatic re-render after await
}
```

### 4.2 ShouldRender Override

**Best Practice**: Override `ShouldRender` for expensive components.

```csharp
// ✅ Good - prevent unnecessary re-renders
@code {
    [Parameter] public Product Product { get; set; } = default!;
    
    private Product? _previousProduct;
    
    protected override bool ShouldRender()
    {
        if (_previousProduct == null || _previousProduct.Id != Product.Id)
        {
            _previousProduct = Product;
            return true;
        }
        return false;
    }
}
```

### 4.3 Virtualization

**Best Practice**: Use `<Virtualize>` for large lists.

```csharp
// ✅ Good - virtualized list
<Virtualize Items="@_products" Context="product">
    <div class="product-card">
        <h4>@product.Name</h4>
        <p>@product.Price.ToString("C")</p>
    </div>
</Virtualize>

// ❌ Bad - rendering all items
<div>
    @foreach (var product in _products) // Renders all 10,000 items
    {
        <div class="product-card">
            <h4>@product.Name</h4>
            <p>@product.Price.ToString("C")</p>
        </div>
    }
</div>
```

---

## 5. JavaScript Interop

### 5.1 IJSRuntime Usage

**Best Practice**: Use IJSRuntime for JavaScript calls.

```csharp
// ✅ Good - JavaScript interop
@inject IJSRuntime JS

@code {
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await JS.InvokeVoidAsync("initializeMap", _elementReference);
        }
    }
    
    private async Task<string> ShowPromptAsync(string message)
    {
        return await JS.InvokeAsync<string>("prompt", message);
    }
}
```

### 5.2 JavaScript Module Loading

**Best Practice**: Use module imports for scoped JavaScript.

```javascript
// wwwroot/js/myModule.js
export function initialize(element) {
    console.log('Initialized', element);
}

export function cleanup() {
    console.log('Cleaned up');
}
```

```csharp
// ✅ Good - JavaScript module
@implements IAsyncDisposable
@inject IJSRuntime JS

@code {
    private IJSObjectReference? _module;
    
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            _module = await JS.InvokeAsync<IJSObjectReference>(
                "import", "./js/myModule.js");
            await _module.InvokeVoidAsync("initialize", _elementReference);
        }
    }
    
    public async ValueTask DisposeAsync()
    {
        if (_module != null)
        {
            await _module.InvokeVoidAsync("cleanup");
            await _module.DisposeAsync();
        }
    }
}
```

### 5.3 DotNetObjectReference

**Best Practice**: Use `DotNetObjectReference` for JavaScript callbacks.

```csharp
// ✅ Good - .NET callbacks from JavaScript
@implements IDisposable
@inject IJSRuntime JS

@code {
    private DotNetObjectReference<MyComponent>? _dotNetRef;
    
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            _dotNetRef = DotNetObjectReference.Create(this);
            await JS.InvokeVoidAsync("registerCallback", _dotNetRef);
        }
    }
    
    [JSInvokable]
    public void OnJavaScriptCallback(string data)
    {
        _receivedData = data;
        StateHasChanged();
    }
    
    public void Dispose()
    {
        _dotNetRef?.Dispose();
    }
}
```

---

## 6. Forms and Validation

### 6.1 EditForm

**Best Practice**: Use `EditForm` with validation.

```csharp
// ✅ Good - EditForm with validation
<EditForm Model="@_model" OnValidSubmit="@HandleValidSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary />
    
    <div class="form-group">
        <label for="name">Name:</label>
        <InputText id="name" @bind-Value="_model.Name" class="form-control" />
        <ValidationMessage For="@(() => _model.Name)" />
    </div>
    
    <div class="form-group">
        <label for="price">Price:</label>
        <InputNumber id="price" @bind-Value="_model.Price" class="form-control" />
        <ValidationMessage For="@(() => _model.Price)" />
    </div>
    
    <button type="submit" class="btn btn-primary">Save</button>
</EditForm>

@code {
    private ProductModel _model = new();
    
    private async Task HandleValidSubmit()
    {
        await ProductService.SaveAsync(_model);
        NavigationManager.NavigateTo("/products");
    }
}

public class ProductModel
{
    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; } = string.Empty;
    
    [Range(0.01, double.MaxValue)]
    public decimal Price { get; set; }
}
```

---

## 7. Disposal and Cleanup

### 7.1 IDisposable

**Best Practice**: Dispose event handlers and unmanaged resources.

```csharp
// ✅ Good - proper disposal
@implements IDisposable
@inject AppState AppState

@code {
    protected override void OnInitialized()
    {
        AppState.OnChange += StateHasChanged;
    }
    
    public void Dispose()
    {
        AppState.OnChange -= StateHasChanged; // Prevent memory leak
    }
}
```

### 7.2 IAsyncDisposable

**Best Practice**: Use `IAsyncDisposable` for async cleanup.

```csharp
// ✅ Good - async disposal
@implements IAsyncDisposable
@inject IJSRuntime JS

@code {
    private IJSObjectReference? _module;
    
    public async ValueTask DisposeAsync()
    {
        if (_module != null)
        {
            await _module.InvokeVoidAsync("cleanup");
            await _module.DisposeAsync();
        }
    }
}
```

---

## 8. Blazor Server vs WebAssembly

### 8.1 Server Considerations

```csharp
// ✅ Good - Blazor Server patterns
// 1. Circuit lifetime awareness
builder.Services.AddScoped<AppState>(); // Per-circuit state

// 2. SignalR reconnection handling
<div id="reconnect-modal" style="display: none;">
    Reconnecting...
</div>

// 3. Pre-rendering considerations
@code {
    protected override async Task OnInitializedAsync()
    {
        if (!OperatingSystem.IsBrowser())
        {
            // Pre-rendering on server, skip JS interop
            return;
        }
        
        await JS.InvokeVoidAsync("initialize");
    }
}
```

### 8.2 WebAssembly Considerations

```csharp
// ✅ Good - Blazor WASM patterns
// 1. Singleton services (no circuits)
builder.Services.AddSingleton<AppState>();

// 2. Authentication with JWT
builder.Services.AddAuthorizationCore();
builder.Services.AddScoped<AuthenticationStateProvider, JwtAuthStateProvider>();

// 3. Lazy loading assemblies
<Router AppAssembly="@typeof(App).Assembly"
        AdditionalAssemblies="@_lazyLoadedAssemblies">
</Router>

@code {
    private List<Assembly> _lazyLoadedAssemblies = new();
}
```

---

## Blazor Anti-Patterns

1. **Loading data in `OnAfterRender`** - Use `OnInitialized` or `OnParametersSet`
2. **Async void lifecycle methods** - Use `OnInitializedAsync`, not `OnInitialized` + async void
3. **Not disposing event handlers** - Causes memory leaks
4. **Using Action instead of EventCallback** - Parent won't re-render
5. **Calling StateHasChanged after await** - Automatic re-render already happens
6. **Not validating parameters** - Check required parameters in `OnParametersSet`
7. **JavaScript interop before firstRender** - Will throw in pre-rendering
8. **Not using Virtualize for large lists** - Performance issues
9. **Creating services in components** - Inject them instead
10. **Forgetting [JSInvokable] on callback methods** - JavaScript can't call them

---

**Last Updated**: 2025-01-14
**Maintained By**: The Forge - dotnet-code-review skill
