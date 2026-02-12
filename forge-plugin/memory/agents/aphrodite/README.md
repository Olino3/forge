# Aphrodite Agent Memory

This directory stores project-specific knowledge for the `@aphrodite` agent.

## Structure

```
aphrodite/
├── design_systems/ # Track design system components and patterns
├── user_research/  # Store user research findings and insights
├── interactions/   # Record interaction patterns and animations
└── accessibility/  # Maintain accessibility patterns and solutions
```

## Usage

The `@aphrodite` agent automatically stores and retrieves:
- Design system components and patterns
- User research findings and insights
- Interaction patterns and animations
- Accessibility patterns and solutions
- Visual design guidelines
- Usability test results

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores design patterns and research
3. **Retrieval**: Agent loads relevant patterns before design work
4. **Updates**: Memory is updated as designs evolve
5. **Cleanup**: Outdated patterns can be archived or removed manually

## Example Memory Files

- `design_systems/component-library.md` - Design system components
- `user_research/user-personas.md` - User personas and needs
- `interactions/animation-patterns.md` - Interaction patterns
- `accessibility/wcag-patterns.md` - Accessibility solutions

## Best Practices

- Store design decisions with rationale
- Document user insights from research
- Keep interaction patterns with examples
- Update memory with accessibility solutions
- Review and refine design guidelines periodically
