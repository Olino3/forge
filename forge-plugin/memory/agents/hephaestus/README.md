# Hephaestus Agent Memory

This directory stores project-specific knowledge for the `@hephaestus` agent.

## Structure

```
hephaestus/
├── skills_created/  # Track skills forged and their evolution
├── tool_patterns/   # Record successful tool design patterns
├── templates/       # Store reusable skill templates and structures
└── innovations/     # Document new capabilities and techniques
```

## Usage

The `@hephaestus` agent automatically stores and retrieves:
- Successful skill designs and architectures
- Reusable templates and patterns
- Common pitfalls and how to avoid them
- Integration patterns with existing tools
- User feedback and iterations

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores skill patterns, templates, and learnings
3. **Retrieval**: Agent loads relevant patterns before creating new skills
4. **Updates**: Memory is updated as new skills are forged
5. **Cleanup**: Outdated patterns can be archived or removed manually

## Example Memory Files

- `skills_created/file-schema-analysis.md` - Lessons from creating schema analysis skill
- `tool_patterns/script-based-skill.md` - Pattern for skills with helper scripts
- `templates/basic-skill-template.md` - Reusable skill structure
- `innovations/meta-skill-pattern.md` - Meta-skill creation insights

## Best Practices

- Store design decisions and rationale, not just code
- Document what worked well and what didn't
- Keep templates generic and reusable
- Update memory when patterns evolve
- Review and refine patterns periodically
