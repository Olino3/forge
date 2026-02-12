# /document Examples

## Example 1: Inline Code Documentation

```
/document src/services/auth_service.py --type inline
```

**What happens**:
1. Reads `auth_service.py` and identifies undocumented functions
2. Detects project's docstring style (Google-style)
3. Adds docstrings with Args, Returns, Raises sections
4. Adds type annotations where missing
5. Preserves existing documentation, only fills gaps

## Example 2: API Reference Generation

```
/document src/api --type api --style detailed
```

**What happens**:
1. Scans all API route files
2. Extracts endpoints: method, path, parameters, responses
3. Generates `docs/api_reference.md` with:
   - Endpoint table of contents
   - Detailed per-endpoint documentation
   - Request/response examples
   - Authentication requirements
4. Saves documentation report to `/claudedocs`

## Example 3: User Guide

```
/document payment-module --type guide --style brief
```

**What happens**:
1. Analyzes payment module structure and public APIs
2. Creates `docs/payment_guide.md` with:
   - Quick start for common payment operations
   - Configuration instructions
   - Example usage for each payment method
   - Error handling guidance
3. Focuses on practical usage over implementation details

## Example 4: Component Documentation

```
/document src/components/ --type external
```

**What happens**:
1. Scans all components in directory
2. For each component, generates markdown with:
   - Purpose and description
   - Props/Inputs and Events/Outputs
   - Usage examples
   - Integration notes
3. Creates `docs/components/` directory with per-component docs

## Example 5: Detailed Python Module Documentation

```
/document src/models --type inline --style detailed
```

**What happens**:
1. Reads all model files
2. Adds comprehensive docstrings:
   - Module-level docstrings with overview
   - Class docstrings with attributes and usage
   - Method docstrings with full parameter descriptions
   - Property docstrings
3. Adds type annotations where missing

## Example 6: .NET XML Documentation

```
/document Controllers/ --type inline
```

**What happens**:
1. Detects C# project
2. Identifies undocumented public classes and methods
3. Adds XML doc comments with `<summary>`, `<param>`, `<returns>`
4. Follows existing project documentation conventions
5. Reports documentation coverage improvement
