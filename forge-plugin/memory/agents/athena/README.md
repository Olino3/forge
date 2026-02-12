# Athena Agent Memory

This directory stores project-specific knowledge for the `@athena` agent.

## Structure

```
athena/
├── architectures/ # Track system architecture designs
├── decisions/     # Store architectural decision records (ADRs)
├── patterns/      # Maintain design patterns and their applications
└── evaluations/   # Record technology evaluations and selections
```

## Usage

The `@athena` agent automatically stores and retrieves:
- System architecture designs and rationale
- Technical decision records (ADRs)
- Design patterns and their applications
- Technology evaluations and selections
- Architectural trade-offs and compromises
- Lessons learned from past designs

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores architectural designs and decisions
3. **Retrieval**: Agent loads relevant patterns before design work
4. **Updates**: Memory is updated as architectures evolve
5. **Cleanup**: Outdated designs can be archived or removed manually

## Example Memory Files

- `architectures/microservices-design.md` - Microservices architecture
- `decisions/adr-001-database-selection.md` - Database choice ADR
- `patterns/cqrs-pattern-application.md` - CQRS pattern usage
- `evaluations/frontend-framework-comparison.md` - Framework evaluation

## Best Practices

- Store architectural decisions with full context
- Document design patterns with examples
- Keep ADRs structured and consistent
- Update memory when designs evolve
- Review and refine patterns periodically
