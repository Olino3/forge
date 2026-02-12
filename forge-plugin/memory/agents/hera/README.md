# Hera Agent Memory

This directory stores project-specific knowledge for the `@hera` agent.

## Structure

```
hera/
├── standards/      # Track coding standards and conventions
├── quality_gates/  # Record quality gate configurations
├── compliance/     # Store compliance requirements and audits
└── governance/     # Maintain governance decisions and policies
```

## Usage

The `@hera` agent automatically stores and retrieves:
- Project standards and conventions
- Quality gate configurations
- Compliance requirements and audits
- Team alignment strategies
- Documentation templates and guidelines
- Governance decisions and rationale

## Memory Lifecycle

1. **Initial Setup**: Agent creates subdirectories on first use
2. **During Work**: Agent stores standards and governance patterns
3. **Retrieval**: Agent loads relevant standards before reviews
4. **Updates**: Memory is updated as governance evolves
5. **Cleanup**: Outdated standards can be archived or removed manually

## Example Memory Files

- `standards/python-style-guide.md` - Python coding standards
- `quality_gates/pr-checklist.md` - Pull request quality gates
- `compliance/security-requirements.md` - Security compliance needs
- `governance/architectural-decisions.md` - Key governance decisions

## Best Practices

- Store governance decisions and rationale
- Document standards with examples
- Keep quality gates practical and achievable
- Update memory when standards evolve
- Review and refine governance periodically
