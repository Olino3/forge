# skill-creator Memory

Skill-specific memory for tracking created skills, design patterns, and lessons learned during skill creation sessions.

## Purpose

This memory helps the `skill:skill-creator` remember:
- Skills created in past sessions, their type classifications, and design decisions
- Effective design patterns for different skill types (Code Analysis, Code Generation, Planning & Workflow, etc.)
- Common mistakes encountered during skill creation and how they were avoided
- Reusable structures and templates that produced high-quality skills

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `created_skills.md`

**Purpose**: Log of all skills created, including design decisions and patterns used

**Should contain**:
- Skill name and date of creation
- Type classification (Code Analysis, Code Generation, Planning & Workflow, Documentation, DevOps & Infrastructure)
- Design decisions: freedom level, token budget, number of workflow steps
- Triggers defined and interface usage
- Notes on any issues encountered during creation

**Example structure**:
```markdown
# Created Skills

## go-code-review — 2025-06-30
- **Type**: Code Analysis
- **Freedom Level**: Strict Procedural
- **Token Budget**: Compact
- **Workflow Steps**: 6
- **Interfaces**: ContextProvider, MemoryStore
- **Notes**: Strict procedural works well for review checklists. Compact budget appropriate for experienced Go developers.

## deploy-automation — 2025-07-05
- **Type**: DevOps & Infrastructure
- **Freedom Level**: Flexible Guidance
- **Token Budget**: Detailed
- **Workflow Steps**: 8
- **Interfaces**: ContextProvider, MemoryStore
- **Notes**: Flexible guidance necessary due to wide variation in deployment targets. Detailed budget justified by high cost of deployment mistakes.
```

**When to update**: After every skill creation session — record the skill and its design decisions

#### `design_patterns.md`

**Purpose**: Effective skill design patterns and common mistakes to avoid

**Should contain**:
- Patterns that produce high-quality skills for each skill type
- Anti-patterns and common mistakes encountered
- Reusable structures (frontmatter templates, workflow step patterns, checklist formats)
- Token efficiency techniques that worked well

**Example structure**:
```markdown
# Design Patterns

## Pattern: Code Analysis Skills
- **Freedom Level**: Strict Procedural — review checklists must be exhaustive
- **Token Budget**: Compact — target users are domain experts
- **Key Pattern**: Define review categories upfront, then iterate through each with findings and severity
- **Common Mistake**: Forgetting to validate file types before analysis — always add a file detection step

## Pattern: Planning & Workflow Skills
- **Freedom Level**: Flexible Guidance — planning varies by project context
- **Token Budget**: Detailed — planning decisions have long-term impact
- **Key Pattern**: Use conditional outputs based on project classification (greenfield, migration, etc.)
- **Common Mistake**: Making framework recommendations without validating ecosystem compatibility

## Anti-Pattern: Overly Strict Freedom Level
- Skills with highly variable inputs (documentation, creative tasks) should not use strict procedural
- Strict procedural works best when correctness is critical and inputs are well-defined
```

**When to update**: After every skill creation session — record new patterns and anti-patterns discovered

## Memory Lifecycle

### Creation (First Skill Creation Session)
1. Skill-creator runs for the first time
2. Completes full skill creation workflow
3. Creates memory directory
4. Saves skill entry to `created_skills.md`
5. Saves design patterns to `design_patterns.md`

### Growth (Ongoing Sessions)
1. Each skill creation session appends to `created_skills.md`
2. New design patterns added to `design_patterns.md`
3. Anti-patterns recorded when mistakes are caught during quality validation
4. Pattern refinements recorded based on feedback from skill usage

### Maintenance (Periodic Review)
1. Review patterns for accuracy — remove outdated recommendations
2. Archive created skills entries older than 12 months
3. Consolidate similar patterns into generalized templates
4. Update design recommendations based on skill usage outcomes

## Related Documentation

- **Skill Documentation**: `../../skills/skill-creator/SKILL.md`
- **Main Memory Index**: `../index.md`
