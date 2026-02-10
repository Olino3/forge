# Prometheus Agent Memory

This directory stores project-specific knowledge for the `@prometheus` agent.

## Structure

```
prometheus/
├── architectures/  # Track system designs and decisions
├── roadmaps/       # Store planning documents and milestones
├── refactorings/   # Record refactoring strategies and outcomes
└── decisions/      # Maintain architectural decision records (ADRs)
```

## Usage

The `@prometheus` agent automatically stores and retrieves:
- System architecture diagrams and rationale
- Technology selection decisions with pros/cons
- Refactoring roadmaps and progress
- Performance bottlenecks and solutions
- Scalability plans and implementations
- Team conventions and architectural patterns

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores architectural decisions and strategies
3. **Retrieval**: Agent loads relevant history before planning
4. **Updates**: Memory is updated as systems evolve
5. **Cleanup**: Superseded decisions can be archived with reference to current decisions

## Example Memory Files

- `architectures/microservices-migration.md` - Microservices architecture design
- `roadmaps/2026-q1-technical-roadmap.md` - Quarterly technical roadmap
- `refactorings/monolith-to-services.md` - Refactoring strategy and progress
- `decisions/ADR-001-database-selection.md` - Architectural Decision Record

## Best Practices

- Document the "why" behind architectural decisions
- Record alternatives considered and trade-offs
- Track outcomes of decisions for future reference
- Link related decisions together
- Keep ADRs immutable (create new ones for changes)
- Review and learn from past decisions
