# graphql-design Memory

Project-specific memory for GraphQL schema design, resolver patterns, federation topology, and conventions.

## Purpose

This memory helps the `skill:graphql-design` remember:
- Schema conventions (naming, nullability, custom scalars)
- Entity types and their relationships
- Federation topology and entity ownership
- Pagination and error handling patterns
- Query complexity budgets and DataLoader strategies
- Past schema evolution decisions

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`

**Purpose**: High-level GraphQL API context

**Must contain**:
- **Schema scope**: Entities, relationships, federation topology
- **Consumers**: Web, mobile, server-to-server, public
- **Data sources**: Databases, REST APIs, microservices backing the resolvers
- **Real-time requirements**: Subscriptions, live queries
- **Performance targets**: Query complexity budget, max depth, response time

**When to update**: First invocation, new entity types, federation changes

#### `schema_conventions.md`

**Purpose**: Established GraphQL conventions for consistency

**Must contain**:
- **Naming rules**: Type, field, enum, mutation naming conventions
- **Pagination style**: Relay connections, offset-based, or hybrid
- **Error handling**: Mutation payload errors, error codes catalog
- **Custom scalars**: DateTime, URL, Money, etc.
- **Authorization patterns**: Directive-based, resolver middleware, or both
- **Complexity rules**: Field costs, max depth, max complexity

**When to update**: After each design session when new patterns are established

### Optional Files

#### `federation_map.md`

**Purpose**: Entity ownership across subgraphs and extension points

#### `schema_changelog.md`

**Purpose**: Track schema evolution — added types, deprecated fields, breaking changes

---

## Usage in skill:graphql-design

### Loading Memory (Step 2)

```markdown
project_name = detect_project_name()
memory = memoryStore.getSkillMemory("graphql-design", project_name)

if memory exists:
    # Adopt established naming and pagination conventions
    # Ensure new types follow existing patterns
    # Reference federation ownership map
```

### Updating Memory (Step 8)

```markdown
# First design session
if not exists(memory_path):
    create project_overview.md with schema scope and consumer types
    create schema_conventions.md with naming and error patterns

# Subsequent sessions
else:
    update schema_conventions.md with any new patterns
    update federation_map.md if subgraphs added
```

---

## Related Documentation

- **Skill Definition**: `../../skills/graphql-design/SKILL.md`
- **Context Files**: `../../context/engineering/`
- **Memory Index**: `../index.md`
