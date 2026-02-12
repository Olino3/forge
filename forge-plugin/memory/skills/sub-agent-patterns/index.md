# sub-agent-patterns Memory

Skill-specific memory for tracking agent catalogs, delegation patterns, and lessons learned during sub-agent pattern sessions.

## Purpose

This memory helps the `skill:sub-agent-patterns` remember:
- Available agents and their strengths, limitations, and cost profiles
- Successful delegation strategies for different task types
- Agent-task matches that worked well and those that failed
- Custom agents created and their domain specializations
- Reusable delegation chain patterns for common workflows

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `agent_catalog.md`

**Purpose**: Catalog of available agents and their strengths, updated as new agents are created or new capabilities are discovered

**Should contain**:
- Built-in agent profiles (Explore, Task, General-Purpose) with observed strengths
- Custom Forge agent profiles with domain specializations
- Agent-task fitness observations from past sessions
- Cost and performance notes per agent type

**Example structure**:
```markdown
# Agent Catalog

## Built-in Agents

### Explore
- **Best for**: Read-only codebase search, file discovery, answering codebase questions
- **Observed strengths**: Fast pattern matching across large codebases; parallel-safe
- **Limitations**: Cannot run commands; answers limited to ~300 words
- **Cost**: Low (Haiku model)

### Task
- **Best for**: Running tests, builds, lints; any CLI command where pass/fail status matters
- **Observed strengths**: Clean output — brief on success, verbose on failure
- **Limitations**: Haiku model may struggle with complex multi-step tasks
- **Cost**: Low (Haiku model)

### General-Purpose
- **Best for**: Complex multi-step tasks requiring deep reasoning and full toolset
- **Observed strengths**: Can handle nuanced planning, code generation, and refactoring
- **Limitations**: Slower and more expensive; runs in separate context window
- **Cost**: High (Sonnet model)

## Custom Agents

### db-optimizer — 2025-07-16
- **Domain**: PostgreSQL optimization
- **Model**: Sonnet
- **Skills**: database-schema-analysis
- **Notes**: Created for query plan analysis and index recommendations
```

**When to update**: After every session — record new agent discoveries, capability insights, and performance observations

#### `delegation_patterns.md`

**Purpose**: Successful delegation strategies and lessons learned from agent coordination

**Should contain**:
- Delegation chain patterns that worked well (with agent assignments and context flow)
- Single-agent selection rationale for common task types
- Failed delegation approaches and why they failed
- Context passing techniques between agents
- Error handling strategies that proved effective

**Example structure**:
```markdown
# Delegation Patterns

## Pattern: Read-Only Codebase Exploration
- **Agent**: Explore (single call or parallel)
- **When**: Understanding code structure, finding files, answering "how does X work?"
- **Tip**: Use parallel Explore calls for independent search queries
- **Fallback**: Escalate to General-Purpose if Explore results are insufficient

## Pattern: Multi-Phase Refactoring
- **Phase 1**: Explore (parallel) — discover codebase structure
- **Phase 2**: General-Purpose — plan changes
- **Phase 3**: General-Purpose — execute changes
- **Phase 4**: Task — verify with tests/lint/build
- **Context passing**: Concatenate Phase 1 outputs as structured input to Phase 2
- **Error handling**: Git rollback on Phase 3 failure; retry Phase 3 on Phase 4 failure

## Anti-Pattern: Using General-Purpose for Simple Search
- General-Purpose is overkill for file search tasks
- Explore is faster, cheaper, and purpose-built for search
- Only escalate to General-Purpose when synthesis or reasoning depth is needed
```

**When to update**: After every session — record successful patterns, failed approaches, and new delegation insights

## Memory Lifecycle

### Creation (First Sub-Agent Patterns Session)
1. Sub-agent-patterns skill runs for the first time
2. Completes full workflow including agent catalog and delegation design
3. Creates memory directory
4. Saves agent profiles to `agent_catalog.md`
5. Saves delegation patterns to `delegation_patterns.md`

### Growth (Ongoing Sessions)
1. Each session updates `agent_catalog.md` with new agent insights
2. New delegation patterns added to `delegation_patterns.md`
3. Failed approaches recorded as anti-patterns with lessons learned
4. Custom agent profiles added as new agents are created

### Maintenance (Periodic Review)
1. Review agent catalog for accuracy — remove deprecated agents
2. Archive delegation patterns older than 12 months
3. Consolidate similar patterns into generalized templates
4. Update agent capability notes based on model upgrades or tool changes

## Related Documentation

- **Skill Documentation**: `../../skills/sub-agent-patterns/SKILL.md`
- **Main Memory Index**: `../index.md`
