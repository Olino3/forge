# api-design Memory

Project-specific memory for API design, including conventions, resource models, versioning strategies, and design decisions.

## Purpose

This memory helps the `skill:api-design` remember:
- Project API conventions (naming, versioning, error formats)
- Resource models and URL structures
- Authentication and security patterns
- Pagination strategies
- Past design decisions and their rationale

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`

**Purpose**: High-level API scope and architecture

**Must contain**:
- **API name and purpose**: What does this API serve?
- **Base URL structure**: e.g., `https://api.example.com/v1/`
- **API style**: RESTful, RPC, hybrid
- **Consumer types**: Public, internal, partner, mobile
- **Authentication mechanism**: OAuth2, API key, JWT, mTLS
- **Rate limiting**: Limits and quotas per consumer type
- **Versioning strategy**: URL path, header, query parameter

**When to update**: First invocation, architecture changes, new consumer types

#### `api_conventions.md`

**Purpose**: Established conventions for consistency across endpoints

**Must contain**:
- **URL naming rules**: Plural nouns, kebab-case, nesting depth
- **Request/response format**: Envelope structure, date format, ID format
- **Pagination style**: Cursor-based or offset-based, parameter names
- **Error format**: RFC 7807 or custom, error code catalog
- **Status code mapping**: Which codes are used for which scenarios
- **Header conventions**: Custom headers, CORS, caching

**When to update**: After each design session when new conventions are established

### Optional Files

#### `design_decisions.md`

**Purpose**: Track significant API design decisions with rationale

#### `endpoint_inventory.md`

**Purpose**: Complete inventory of all designed endpoints across the project

---

## Usage in skill:api-design

### Loading Memory (Step 2)

```markdown
project_name = detect_project_name()
memory = memoryStore.getSkillMemory("api-design", project_name)

if memory exists:
    # Apply established conventions to new designs
    # Ensure consistency with previous endpoints
    # Reference past design decisions
```

### Updating Memory (Step 7)

```markdown
# First design session
if not exists(memory_path):
    create project_overview.md with API scope and architecture
    create api_conventions.md with established naming and format rules

# Subsequent sessions
else:
    update api_conventions.md with any new patterns
    append to design_decisions.md if significant choices were made
```

---

## Related Documentation

- **Skill Definition**: `../../skills/api-design/SKILL.md`
- **Context Files**: `../../context/engineering/`
- **Memory Index**: `../index.md`
