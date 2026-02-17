---
name: sub-agent-patterns
version: 1.0.0
description: Comprehensive guide to sub-agents in Claude Code — built-in agents (Explore, Task, General-Purpose), custom agent creation, configuration, and delegation patterns.
context:
  primary_domain: engineering
  supporting_domains:
    - documentation
  memory:
    skill_memory: sub-agent-patterns
    scopes:
      - agent_catalog
      - delegation_patterns
tags:
  - planning
  - workflow
  - agents
  - delegation
  - patterns
triggers:
  - sub-agent
  - sub-agents
##   - subagent

# Sub-Agent Patterns

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 8-step workflow outlined in this document MUST be followed in exact order for EVERY sub-agent patterns session. Skipping steps or deviating from the procedure will result in incorrect agent selection, misconfigured custom agents, or broken delegation chains. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Sub-agent selection, creation, and delegation scenarios with sample outputs
- **Memory**: Skill-specific memory accessed via `memoryStore.getSkillMemory("sub-agent-patterns", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Sub-Agent Focus Areas

Sub-agent patterns evaluation covers 5 focus areas:

1. **Agent Selection**: Choosing the right built-in or custom agent for the task at hand
2. **Capability Matching**: Mapping task requirements to agent tools, models, and context domains
3. **Delegation Design**: Structuring single, chained, or parallel agent invocations
4. **Context Passing**: Ensuring agents receive the right input and produce usable output
5. **Error Handling**: Designing fallback strategies when agent execution fails or produces unexpected results

**Note**: The skill produces agent recommendations, custom agent configurations, and delegation chain designs. It does not execute agents directly — it designs the patterns for invoking them.

---

## Purpose

Comprehensive guide to sub-agents in Claude Code — built-in agents (Explore, Task, General-Purpose), custom agent creation, configuration, and delegation patterns.


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Determine the sub-agent task from the user prompt or conversation context:
   - **Creating a new agent**: Designing a custom Forge agent with personality, expertise, and configuration
   - **Choosing an existing agent**: Selecting the best built-in or custom agent for a specific task
   - **Designing delegation patterns**: Structuring multi-agent workflows with chaining or parallelism
   - **Understanding agent capabilities**: Documenting what agents can do and when to use them
2. Identify the target task that requires agent assistance:
   - What is the end goal? (code exploration, refactoring, testing, documentation, etc.)
   - What tools are needed? (file access, shell commands, web search, etc.)
   - What quality of reasoning is required? (fast/simple vs. deep/complex)
3. Determine scope:
   - Single agent selection vs. multi-agent delegation chain
   - One-off invocation vs. reusable pattern

**DO NOT PROCEED WITHOUT IDENTIFYING THE SUB-AGENT TASK TYPE AND TARGET GOAL**

### ⚠️ STEP 2: Load Memory (REQUIRED)

**YOU MUST:**
1. Identify the project name from the user prompt or ask the user
2. Use `memoryStore.getSkillMemory("sub-agent-patterns", "{project-name}")` to load existing memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
3. If memory exists, review previous sub-agent patterns:
   - Check for agent selections that worked well for similar tasks
   - Review delegation patterns that succeeded or failed
   - Note any agent capability insights from prior sessions
4. **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from other skill executions
5. If no memory exists, you will create it after generating the output

**DO NOT PROCEED WITHOUT CHECKING SUB-AGENT-PATTERNS MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

**YOU MUST:**
1. Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
2. Load supporting context for documentation standards
3. Load the Forge agent registry: review existing agents under `agents/` for capabilities and configurations
4. If the task targets a specific technology domain, load relevant context:
   - Python tasks: `contextProvider.getIndex("python")`
   - JavaScript/TypeScript tasks: `contextProvider.getIndex("javascript")`
   - DevOps tasks: `contextProvider.getIndex("devops")`
5. Apply cross-domain triggers as defined in the [Cross-Domain Matrix](../../context/cross_domain.md)

**DO NOT PROCEED WITHOUT LOADING CONTEXT AND REVIEWING AVAILABLE AGENTS**

### ⚠️ STEP 4: Catalog Available Agents (REQUIRED)

**YOU MUST enumerate all available agents and their capabilities:**

1. **Built-in Agents** (provided by Claude Code):

   | Agent | Model | Purpose | Tools | Best For |
   |-------|-------|---------|-------|----------|
   | **Explore** | Haiku | Fast codebase search and question answering | grep, glob, view | Finding files, searching code, answering codebase questions — safe to call in parallel |
   | **Task** | Haiku | Command execution with verbose output | All CLI tools | Tests, builds, lints, dependency installs — returns brief summary on success, full output on failure |
   | **General-Purpose** | Sonnet | Full-capability agent in subprocess | All CLI tools | Complex multi-step tasks requiring complete toolset and high-quality reasoning |

2. **Custom Forge Agents** — Olympian Tier (managed under `agents/`):
   - Enumerate each agent's `.config.json` for: `contextDomains`, `skills`, `memoryPath`, `model`, `tools`
   - Document each agent's `.md` file for: personality, expertise areas, workflow patterns

3. **Custom Forge Agents** — Specialist Legion (managed under `agents/`):
   - Enumerate each specialist agent and their domain focus
   - Document unique capabilities not covered by Olympian agents

4. For each agent, document:
   - **Strengths**: What the agent excels at
   - **Limitations**: What the agent cannot do or does poorly
   - **Cost profile**: Model tier (Haiku = fast/cheap, Sonnet = slower/expensive)
   - **Parallelism**: Whether the agent can be safely run in parallel

**DO NOT PROCEED WITHOUT A COMPLETE AGENT CATALOG**

### ⚠️ STEP 5: Design Delegation Strategy (REQUIRED)

**YOU MUST analyze the task and design the delegation approach:**

1. **Task Requirements Analysis**:
   - Break the task into discrete sub-tasks
   - For each sub-task, identify: required tools, reasoning depth, context needs, expected output
   - Determine dependencies between sub-tasks

2. **Agent-Task Matching**:
   - Map each sub-task to the best-fit agent based on the catalog from Step 4
   - Consider trade-offs: speed vs. quality, cost vs. capability
   - Prefer built-in agents for simple tasks — reserve custom agents for domain-specific work

3. **Delegation Architecture**:
   - **Agent type**: Built-in (Explore, Task, General-Purpose) vs. custom Forge agent
   - **Delegation depth**: Single agent invocation vs. chained multi-agent workflow
   - **Context passing**: What input each agent needs and how to provide it
   - **Output expectations**: What each agent returns and how results are composed
   - **Execution mode**: Parallel (independent sub-tasks) vs. sequential (dependent sub-tasks)

4. **Error Handling Design**:
   - Define fallback agents if the primary choice fails
   - Specify retry strategies for transient failures
   - Design output validation to catch incorrect or incomplete results

**DO NOT PROCEED WITHOUT A DOCUMENTED DELEGATION STRATEGY**

### ⚠️ STEP 6: Generate Agent Configuration (REQUIRED)

**YOU MUST produce the appropriate artifacts based on the task type:**

1. **For new custom agents**, generate:
   - **Agent `.md` file**: Personality, expertise areas, workflow patterns, and interaction style following existing agent `.md` conventions
   - **Agent `.config.json`**: Configuration following [agent_config.schema.json](../../interfaces/schemas/agent_config.schema.json) with:
     - `contextDomains`: Which context domains the agent loads
     - `skills`: Which skills the agent can invoke
     - `memoryPath`: Where the agent stores its memory
     - `model`: Model tier (haiku for fast tasks, sonnet for complex reasoning)
     - `tools`: Which tools the agent has access to
   - **Memory directory**: Create `memory/agents/{agent-name}/` for agent-specific memory

2. **For delegation patterns**, generate:
   - **Invocation chain**: Ordered list of agent calls with input/output contracts
   - **Context bridging**: How output from one agent becomes input for the next
   - **Error handling**: Fallback strategies and retry logic at each step
   - **Composition rules**: How final results are assembled from individual agent outputs

3. **For agent selection recommendations**, generate:
   - **Decision matrix**: Criteria-weighted comparison of candidate agents
   - **Rationale**: Why the recommended agent is the best fit
   - **Usage template**: Example invocation with parameters

**DO NOT PROCEED WITHOUT GENERATING THE REQUIRED ARTIFACTS**

### ⚠️ STEP 7: Generate Output (REQUIRED)

**YOU MUST:**
1. Save all generated artifacts to `/claudedocs/` following naming conventions:
   - Agent configurations: `sub-agent-config_{agent-name}_{date}.md`
   - Delegation patterns: `sub-agent-delegation_{task-name}_{date}.md`
   - Agent selection: `sub-agent-selection_{task-name}_{date}.md`
2. Include in the output:
   - Agent catalog summary with capabilities and recommendations
   - Delegation chain diagram (if multi-agent)
   - Configuration files for any new agents
3. Confirm all output files were written successfully

**DO NOT SKIP OUTPUT GENERATION**

### ⚠️ STEP 8: Update Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.update(layer="skill-specific", skill="sub-agent-patterns", project="{project-name}", ...)` to store:
   - **agent_catalog.md**: Update the catalog of available agents, their strengths, and any new capability insights discovered during this session
   - **delegation_patterns.md**: Record successful delegation strategies, agent-task matches that worked well, and any failed approaches with lessons learned
2. If this is the first session, create both memory files with initial data
3. If previous memory exists, append to history and update patterns with new learnings

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY sub-agent patterns session, verify:
- [ ] Step 1: Sub-agent task identified — task type (create, choose, delegate, understand) and target goal determined
- [ ] Step 2: Sub-agent-patterns memory checked via `memoryStore.getSkillMemory()` and prior patterns reviewed
- [ ] Step 3: Engineering and supporting domain context loaded via `contextProvider.getIndex()`; available agents reviewed
- [ ] Step 4: Complete agent catalog produced — built-in agents (Explore, Task, General-Purpose) and custom Forge agents enumerated with capabilities
- [ ] Step 5: Delegation strategy designed — agent-task matching, execution mode, context passing, and error handling documented
- [ ] Step 6: Required artifacts generated — agent configs, delegation patterns, or selection recommendations produced
- [ ] Step 7: All output files saved to `/claudedocs/` following naming conventions
- [ ] Step 8: Memory updated with agent catalog insights and delegation patterns learned

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE SUB-AGENT PATTERNS SESSION**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-16 | Initial release — 8-step mandatory workflow for sub-agent selection, custom agent creation, and delegation pattern design covering built-in agents (Explore, Task, General-Purpose) and custom Forge agents |
