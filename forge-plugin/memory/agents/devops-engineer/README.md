# DevOps Engineer Agent Memory

This directory stores project-specific knowledge for the `@devops-engineer` agent.

## Structure

```
devops-engineer/
├── projects/       # Track deployment configurations per project
├── infrastructure/ # Record infrastructure patterns and decisions
├── pipelines/      # Store CI/CD pipeline templates and customizations
└── environments/   # Maintain environment-specific configurations
```

## Usage

The `@devops-engineer` agent automatically stores and retrieves:
- Infrastructure as Code patterns
- Pipeline configurations and templates
- Environment-specific settings
- Deployment strategies and runbooks
- Team conventions and preferences

## Memory Lifecycle

1. **Initial Setup**: Agent creates project-specific subdirectories on first use
2. **During Work**: Agent stores decisions, patterns, and configurations
3. **Retrieval**: Agent loads relevant memory before starting new tasks
4. **Updates**: Memory is updated as infrastructure evolves
5. **Cleanup**: Old patterns can be archived or removed manually

## Example Memory Files

- `projects/my-app/deployment-config.md` - Deployment configuration for my-app
- `infrastructure/naming-conventions.md` - Azure resource naming standards
- `pipelines/ci-template.yml` - Reusable CI pipeline template
- `environments/production/variables.md` - Production environment variables (non-sensitive)

## Best Practices

- Store decisions and rationale, not just configurations
- Document deviations from standards
- Keep sensitive data out of memory (use Azure Key Vault, etc.)
- Update memory when patterns change
- Review and prune outdated memory periodically
