# File Schema Analysis - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during schema analysis sessions. Each project gets its own subdirectory containing patterns, conventions, and context discovered during analysis.

## Directory Structure

```
memory/skills/file-schema-analysis/
├── index.md (this file)
└── {project-name}/
    ├── analysis_summary.md
    ├── schema_conventions.md
    ├── discovered_patterns.md
    └── validation_rules.md
```

## Project Memory Contents

### analysis_summary.md
- List of analyzed schema files
- Formats used in the project
- Version history
- Overall schema architecture

### schema_conventions.md
- Naming conventions (camelCase, snake_case, PascalCase)
- Field naming patterns
- Type preferences
- Documentation style

### discovered_patterns.md
- Common data structures
- Reused types/definitions
- Design patterns observed
- Anti-patterns to avoid

### validation_rules.md
- Project-specific validation requirements
- Business rules encoded in schemas
- Custom formats and constraints
- Validation tooling used

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's schemas are analyzed. The project name is either:
1. Extracted from the repository root directory name
2. Specified by the user
3. Derived from schema package/namespace

### Updates
Memory is UPDATED every time the skill analyzes schemas in the project:
- New files are added to the inventory
- Patterns are refined based on new observations
- Conventions are confirmed or updated
- Evolution history is tracked

### Usage
Memory is READ at the START of every analysis:
- Provides context about project structure
- Informs about established patterns
- Guides analysis focus areas
- Ensures consistency with previous analyses

## Best Practices

### DO:
- ✅ Update memory after every analysis
- ✅ Document discovered patterns clearly
- ✅ Track schema evolution over time
- ✅ Note project-specific conventions
- ✅ Record validation tooling and processes

### DON'T:
- ❌ Copy entire schema files (link to them instead)
- ❌ Store temporary analysis reports
- ❌ Include user-specific preferences
- ❌ Duplicate information from context files
- ❌ Leave memory stale (always update)

## Memory vs Context

### Context (`../../context/schema/`)
- **Universal knowledge**: Applies to ALL projects
- **Format-specific patterns**: JSON Schema, Protobuf, etc.
- **Best practices**: Industry standards
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project
- **Learned patterns**: Discovered during analysis
- **Evolving**: Changes with each analysis
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
forge/
├── analysis_summary.md
│   - Analyzed 15 .proto files
│   - Using proto3 syntax
│   - gRPC service definitions
│   - Last analyzed: 2025-02-06
│
├── schema_conventions.md
│   - Package naming: com.olino3.forge.v1
│   - Message names: PascalCase
│   - Field names: snake_case
│   - Using go_package option
│
├── discovered_patterns.md
│   - Common base messages (BaseRequest, BaseResponse)
│   - Timestamp fields always using google.protobuf.Timestamp
│   - Pagination pattern with page_token
│   - Error response structure
│
└── validation_rules.md
    - All string IDs must be non-empty
    - Timestamps required for audit fields
    - Using buf for linting and breaking change detection
    - Enforcing PascalCase for message names
```

## Migration Notes

When a project undergoes major schema changes:
1. Document the migration in `analysis_summary.md`
2. Note breaking changes
3. Update patterns that changed
4. Keep historical context for reference

## Privacy and Security

### DO Store:
- Schema structure patterns
- Naming conventions
- Design patterns
- Validation rules
- Tool configurations

### DON'T Store:
- Actual production data
- Secrets or credentials
- User PII
- Proprietary business logic (unless essential to schema understanding)

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-02-06
**Maintained by**: file-schema-analysis skill
