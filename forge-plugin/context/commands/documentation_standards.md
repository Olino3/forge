---
id: "commands/documentation_standards"
domain: commands
title: "Documentation Standards"
type: pattern
estimatedTokens: 900
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Documentation Types"
    estimatedTokens: 53
    keywords: [documentation, types]
  - name: "Language-Specific Conventions"
    estimatedTokens: 134
    keywords: [language-specific, conventions]
  - name: "API Documentation"
    estimatedTokens: 74
    keywords: [api, documentation]
  - name: "Architecture Documentation"
    estimatedTokens: 20
    keywords: [architecture, documentation]
  - name: "Status"
    estimatedTokens: 20
    keywords: [status]
  - name: "Context"
    estimatedTokens: 20
    keywords: [context]
  - name: "Decision"
    estimatedTokens: 20
    keywords: [decision]
  - name: "Consequences"
    estimatedTokens: 33
    keywords: [consequences]
  - name: "README Standards"
    estimatedTokens: 11
    keywords: [readme, standards]
  - name: "Quick Start"
    estimatedTokens: 20
    keywords: [quick, start]
  - name: "Installation"
    estimatedTokens: 20
    keywords: [installation]
  - name: "Usage"
    estimatedTokens: 20
    keywords: [usage]
  - name: "Contributing"
    estimatedTokens: 20
    keywords: [contributing]
  - name: "License"
    estimatedTokens: 21
    keywords: [license]
  - name: "Comment Best Practices"
    estimatedTokens: 51
    keywords: [comment]
  - name: "Documentation Generation Strategy"
    estimatedTokens: 48
    keywords: [documentation, generation, strategy]
  - name: "Official References"
    estimatedTokens: 12
    keywords: [official, references]
tags: [commands, documentation, api-docs, comments, readme, adr, docstrings]
---

# Documentation Standards

Reference patterns for the `/document` command. Covers API documentation, inline comments, architecture documentation, and README standards.

## Documentation Types

### Inline Documentation
- **Docstrings/JSDoc**: Function-level documentation with parameters, returns, examples
- **Comments**: Explain *why*, not *what* - code should be self-documenting for the *what*
- **Type annotations**: Self-documenting types reduce need for parameter docs

### External Documentation
- **README**: Project overview, setup, usage
- **API Reference**: Endpoint/method documentation with examples
- **Architecture Docs**: System design, decisions, trade-offs
- **User Guides**: How-to tutorials for end users
- **ADRs**: Architecture Decision Records

## Language-Specific Conventions

### Python Docstrings
```python
def process_order(order_id: int, validate: bool = True) -> OrderResult:
    """Process an order through the fulfillment pipeline.

    Args:
        order_id: The unique identifier for the order.
        validate: Whether to validate inventory before processing.

    Returns:
        OrderResult with status and tracking information.

    Raises:
        OrderNotFoundError: If order_id doesn't exist.
        InsufficientInventoryError: If validation fails.
    """
```
- **Style**: Google style (Args/Returns/Raises) or NumPy style
- **Reference**: [PEP 257](https://peps.python.org/pep-0257/), [Google Python Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### C# XML Documentation
```csharp
/// <summary>
/// Processes an order through the fulfillment pipeline.
/// </summary>
/// <param name="orderId">The unique identifier for the order.</param>
/// <param name="validate">Whether to validate inventory before processing.</param>
/// <returns>An <see cref="OrderResult"/> with status and tracking information.</returns>
/// <exception cref="OrderNotFoundException">Thrown when the order doesn't exist.</exception>
```
- **Reference**: [XML Documentation Comments](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/)

### TypeScript/JavaScript JSDoc
```typescript
/**
 * Processes an order through the fulfillment pipeline.
 * @param orderId - The unique identifier for the order
 * @param validate - Whether to validate inventory before processing
 * @returns OrderResult with status and tracking information
 * @throws {OrderNotFoundError} If order doesn't exist
 */
```
- **Reference**: [JSDoc](https://jsdoc.app/), [TSDoc](https://tsdoc.org/)

## API Documentation

### REST API (OpenAPI/Swagger)
- Document all endpoints with method, path, description
- Define request/response schemas with examples
- Include authentication requirements
- Document error responses with status codes
- Provide usage examples with curl/HTTP

### Key Elements Per Endpoint
| Element | Description |
|---------|-------------|
| Method + Path | `POST /api/v1/orders` |
| Summary | One-line description |
| Description | Detailed explanation |
| Parameters | Path, query, header params |
| Request Body | Schema with example |
| Responses | All possible status codes with schemas |
| Authentication | Required auth method |

## Architecture Documentation

### Architecture Decision Records (ADRs)
```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a primary database that supports...

## Decision
We will use PostgreSQL 15 because...

## Consequences
- Positive: ACID compliance, JSON support...
- Negative: Operational complexity vs SQLite...
```
- **Reference**: [ADR GitHub](https://adr.github.io/)

### C4 Model Levels
1. **Context**: System boundaries and external actors
2. **Container**: Applications, databases, services
3. **Component**: Major components within containers
4. **Code**: Class/module level (usually auto-generated)

## README Standards

### Minimal README Structure
```markdown
# Project Name

Brief description of what this project does.

## Quick Start
[Fastest path to running the project]

## Installation
[Step-by-step setup instructions]

## Usage
[Basic usage examples]

## Contributing
[How to contribute]

## License
[License information]
```

### Enhanced README Additions
- Badges (CI status, coverage, version)
- Screenshots/demos for UI projects
- API overview table
- Configuration reference
- Troubleshooting section

## Comment Best Practices

### When to Comment
- **Why** decisions were made (not what the code does)
- **Workarounds** for known issues (with issue tracker link)
- **Warnings** about non-obvious behavior
- **TODO/FIXME** with ticket numbers
- **Public API** contracts

### When NOT to Comment
- Code that is self-explanatory
- Restating what the code does
- Commented-out code (delete it, use version control)
- Obvious getter/setter documentation
- Trivial operations

## Documentation Generation Strategy

### For Existing Code Without Docs
1. Analyze public interfaces first (most impact)
2. Document complex/non-obvious logic
3. Add missing type annotations
4. Generate API reference from annotations
5. Create README if missing

### For New Features
1. Write API documentation before implementation (design-first)
2. Add inline documentation during implementation
3. Update README and guides after implementation
4. Generate reference docs from code annotations

## Official References

- [Diátaxis Framework](https://diataxis.fr/) - Documentation system
- [Write the Docs](https://www.writethedocs.org/) - Documentation community
- [OpenAPI Specification](https://swagger.io/specification/)
