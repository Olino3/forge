# divine Memory

Project-specific memory for toolkit discovery patterns, workflow compositions, and recommendation history.

## Purpose

This memory helps the `skill:divine` remember:
- Which tools were recommended for which types of tasks
- Successful workflow compositions and their outcomes
- User preferences for tool selection
- Common task-to-tool mapping patterns

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `recommendation_history.md`

**Purpose**: Track tool recommendations and their success

**Should contain**:
- Task descriptions and recommended tools
- User feedback on recommendations
- Confidence score accuracy over time
- Workflow compositions that worked well

**When to update**: After each recommendation and when feedback is received

#### `common_patterns.md`

**Purpose**: Track recurring task patterns specific to this project

**Should contain**:
- Frequently requested tool categories
- Preferred workflows for common tasks
- Tool combinations that work well together
- Project-specific tool preferences

**When to update**: After each discovery or workflow composition session

## Memory Lifecycle

### Creation (First Use)
1. Skill runs for the first time on a project
2. Generates initial catalog and recommendation
3. Creates project memory directory
4. Saves initial patterns

### Growth (Ongoing Use)
1. Each recommendation adds to history
2. Feedback improves future recommendations
3. Workflow patterns become more refined
4. Tool preference profiles develop

### Maintenance (Periodic Review)
1. Review recommendation accuracy
2. Remove outdated tool references
3. Update workflow patterns for new capabilities
4. Consolidate similar patterns

## Related Documentation

- **Skill Documentation**: `../../skills/divine/SKILL.md`
- **Main Memory Index**: `../index.md`
