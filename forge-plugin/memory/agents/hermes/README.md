# Hermes Agent Memory

This directory stores project-specific knowledge for the `@hermes` agent.

## Structure

```
hermes/
├── api_designs/       # Track API designs and specifications
├── integrations/      # Store integration patterns and architectures
├── message_schemas/   # Record message schemas and contracts
└── security_patterns/ # Maintain authentication and authorization patterns
```

## Usage

The `@hermes` agent automatically stores and retrieves:
- API designs and specifications
- Integration patterns and architectures
- Message schemas and contracts
- Error handling and retry strategies
- Authentication and authorization patterns
- Performance optimization techniques

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores API designs and integration patterns
3. **Retrieval**: Agent loads relevant patterns before integration work
4. **Updates**: Memory is updated as integrations evolve
5. **Cleanup**: Outdated patterns can be archived or removed manually

## Example Memory Files

- `api_designs/rest-api-specification.md` - REST API design
- `integrations/microservices-integration.md` - Integration patterns
- `message_schemas/event-catalog.md` - Event schemas
- `security_patterns/oauth-implementation.md` - Auth patterns

## Best Practices

- Store API designs with OpenAPI specs
- Document integration patterns with examples
- Keep message schemas versioned
- Update memory with security patterns
- Review and refine integration strategies periodically
