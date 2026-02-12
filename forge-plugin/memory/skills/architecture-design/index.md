# architecture-design Memory

Project-specific memory for software architecture decisions, patterns, component structures, and evolution strategies.

## Purpose

This memory helps the `skill:architecture-design` remember:
- Selected architecture patterns and rationale
- Component boundaries and dependency rules
- Architecture Decision Records (ADRs)
- Quality attribute priorities and trade-offs
- Technology stack decisions
- Migration and evolution strategies

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`

**Purpose**: High-level system architecture context

**Must contain**:
- **System type**: Web app, API, pipeline, real-time, etc.
- **Architecture pattern**: Layered, modular monolith, hexagonal, event-driven, etc.
- **Quality attributes**: Top 3 priorities with rationale
- **Component inventory**: Major components and their responsibilities
- **Technology stack**: Languages, frameworks, databases, infrastructure
- **Scale parameters**: Users, data volume, request rates
- **Team structure**: Size, skill distribution, ownership boundaries

**When to update**: First invocation, major architecture changes, team restructuring

#### `architecture_decisions.md`

**Purpose**: Track all ADRs and significant design choices

**Must contain**:
- Numbered ADRs following the standard template
- Decision status (Proposed, Accepted, Deprecated, Superseded)
- Cross-references between related decisions

**When to update**: After each architecture review or design session

### Optional Files

#### `component_map.md`

**Purpose**: Detailed component boundaries, interfaces, and dependency rules

#### `evolution_roadmap.md`

**Purpose**: Planned architectural changes and migration strategies

---

## Usage in skill:architecture-design

### Loading Memory (Step 2)

```markdown
project_name = detect_project_name()
memory = memoryStore.getSkillMemory("architecture-design", project_name)

if memory exists:
    # Honor existing architectural decisions
    # Ensure new designs are consistent with established patterns
    # Reference previous ADRs
```

### Updating Memory (Step 8)

```markdown
# First design session
if not exists(memory_path):
    create project_overview.md with system context and pattern selection
    create architecture_decisions.md with initial ADRs

# Subsequent sessions
else:
    append new ADRs to architecture_decisions.md
    update project_overview.md if architecture evolved
```

---

## Related Documentation

- **Skill Definition**: `../../skills/architecture-design/SKILL.md`
- **Context Files**: `../../context/engineering/`
- **Memory Index**: `../index.md`
