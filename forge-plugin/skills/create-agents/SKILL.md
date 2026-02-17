---
name: create-agents
description: Design and build custom Claude Code agents with effective descriptions, tool access patterns, and delegation strategies. Guides users through agent architecture decisions, generates paired .md and .config.json files, and ensures compliance with The Forge agent conventions. Triggers: create agent, custom agent, build agent, agent description
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [agent_patterns.md, delegation_strategies.md]
    - type: "shared-project"
      usage: "reference"
tags:
  - agents
  - workflow
  - scaffolding
##   - configuration

# skill:create-agents - Custom Agent Builder

## Version: 1.0.0

## Purpose

Design and build custom Claude Code agents with effective descriptions, tool access patterns, and delegation strategies. This skill guides users through the full agent creation lifecycle — from defining the agent's persona and expertise to generating properly structured `.md` and `.config.json` files that comply with The Forge's agent conventions and JSON schema validation.

Use this skill when:
- Creating a new specialist or Olympian-tier agent
- Defining agent tool access and skill delegation
- Writing effective agent descriptions and system prompts
- Configuring context domains, memory paths, and always-load files
- Reviewing or refactoring existing agent configurations

## File Structure

```
skills/create-agents/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [agent_config.schema.json](../../interfaces/schemas/agent_config.schema.json)

## Agent Architecture Overview

Every Forge agent consists of two paired files:

1. **`{agent-name}.md`** — Personality, expertise, workflow instructions, and delegation rules
2. **`{agent-name}.config.json`** — Structured configuration: model, tools, skills, context domains, memory path

Both files must exist in `forge-plugin/agents/` and pass schema validation.

### Key Design Dimensions

1. **Persona & Expertise**: Define the agent's identity, domain knowledge, and communication style
2. **Tool Access**: Specify which tools the agent can use (Read, Write, Bash, Browser, etc.)
3. **Skill Delegation**: Map which skills the agent can invoke via `skillInvoker`
4. **Context Domains**: Configure primary and secondary knowledge domains
5. **Memory Configuration**: Set up the agent's memory storage path and scopes
6. **Model Selection**: Choose the appropriate model tier (sonnet, opus, haiku)
7. **Delegation Strategy**: Define when and how the agent delegates to sub-agents

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Requirements Gathering (REQUIRED)

**YOU MUST:**
1. Determine the agent's **purpose and role**:
   - What domain does this agent specialize in?
   - What problems does it solve?
   - Is it an Olympian (broad) or Specialist (narrow) agent?
2. Identify the agent's **target users**:
   - Who will invoke this agent?
   - What level of autonomy should it have?
3. Clarify **naming conventions**:
   - Agent name must be lowercase with hyphens (e.g., `security-engineer`)
   - Name should reflect the agent's primary function
4. Determine **tier and model**:
   - **Olympian**: Broad expertise, higher model (sonnet/opus)
   - **Specialist**: Deep narrow expertise, efficient model (sonnet/haiku)
5. Ask clarifying questions if the agent's scope is ambiguous

**DO NOT PROCEED WITHOUT A CLEAR AGENT DEFINITION**

### ⚠️ STEP 2: Load Memory (REQUIRED)

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="create-agents"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("create-agents", "{project-name}")` to load existing patterns
2. Review previously created agents and their configurations
3. Check for established naming conventions and delegation patterns
4. If no memory exists, note this is the first agent creation session

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

**YOU MUST:**
1. Load existing agent configurations from `forge-plugin/agents/` for reference
2. Load the agent config schema from `interfaces/schemas/agent_config.schema.json`
3. Review existing agents similar to the one being created
4. Identify available context domains, skills, and memory paths

**DO NOT PROCEED WITHOUT UNDERSTANDING EXISTING PATTERNS**

### ⚠️ STEP 4: Design Agent Architecture (REQUIRED)

**YOU MUST:**
1. **Define the agent's skill set**:
   - List skills the agent should be able to invoke
   - Verify each skill exists in `forge-plugin/skills/`
   - Map skill triggers to agent capabilities
2. **Configure context domains**:
   - Primary domains: Core knowledge areas (loaded always)
   - Secondary domains: Supplementary knowledge (loaded on demand)
   - Always-load files: Critical references loaded on every invocation
3. **Design tool access**:
   - Read: File reading capabilities
   - Write: File creation/modification
   - Bash: Command execution
   - Browser: Web access
   - MCP servers: External integrations
4. **Plan delegation strategy**:
   - When should this agent delegate to sub-agents?
   - Which sub-agents should it prefer?
   - What autonomy level should delegated tasks have?
5. **Define memory structure**:
   - Storage path: `forge-plugin/memory/agents/{agent-name}/`
   - Memory scopes and files

**DO NOT SKIP ARCHITECTURE DESIGN**

### ⚠️ STEP 5: Generate Agent Files (REQUIRED)

**YOU MUST:**
1. **Generate `{agent-name}.md`**:
   - Write a compelling agent description with personality
   - Define expertise areas and communication style
   - Document the agent's workflow and decision-making process
   - Include delegation rules and escalation criteria
   - Add compliance checklist and version history
2. **Generate `{agent-name}.config.json`**:
   - Populate all required schema fields
   - Set `contextDomains`, `skills`, `memoryPath`, `model`, `tools`
   - Ensure all referenced skills, domains, and paths exist
   - Validate against `agent_config.schema.json`
3. **Create memory directory**:
   - Create `forge-plugin/memory/agents/{agent-name}/`
   - Initialize with a reference.md if needed
4. **Validate the agent**:
   - Verify `.md` and `.config.json` are paired
   - Confirm all cross-references resolve (skills exist, domains exist, paths exist)
   - Check JSON schema compliance

**DO NOT GENERATE INCOMPLETE AGENT DEFINITIONS**

### ⚠️ STEP 6: Generate Output (REQUIRED)

- Save output to `/claudedocs/create-agents_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Summary of the agent created
  - Files generated with paths
  - Validation results
  - Recommendations for testing

### ⚠️ STEP 7: Update Memory (REQUIRED)

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="create-agents"`. Store any newly learned patterns, conventions, or project insights.

**YOU MUST:**
1. Store the agent creation pattern for future reference
2. Document any new delegation strategies discovered
3. Update naming conventions if new patterns emerged
4. Record the agent's skill-to-domain mapping

---

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order

### Step 1: Initial Analysis

Gather inputs and determine scope and requirements.

### Step 2: Load Memory

Load project-specific memory via MemoryStore interface.

### Step 3: Load Context

Load relevant context files via ContextProvider interface.

### Step 4: Core Implementation

Execute the skill-specific core action.

### Step 5: Generate Output

Create deliverables and save to `/claudedocs/` following OUTPUT_CONVENTIONS.md.

### Step 6: Update Memory

Update project memory with new patterns and decisions.

## Output File Naming Convention

**Format**: `create-agents_{project}_{YYYY-MM-DD}.md`

**Examples**:
- `create-agents_myapp_2026-02-12.md`
- `create-agents_forge_2026-02-12_security-engineer.md`

---

## Agent Config Schema Quick Reference

```json
{
  "name": "agent-name",
  "description": "What this agent does",
  "model": "sonnet",
  "tools": ["Read", "Write", "Bash"],
  "context": {
    "primaryDomains": ["engineering"],
    "secondaryDomains": [],
    "alwaysLoadFiles": []
  },
  "skills": [
    { "name": "skill-name", "trigger": "when to use" }
  ],
  "memory": {
    "storagePath": "forge-plugin/memory/agents/agent-name"
  }
}
```

---

## Further Reading

- **Agent Schema**: `interfaces/schemas/agent_config.schema.json`
- **Existing Agents**: `forge-plugin/agents/` for reference implementations
- **Contributing Guide**: `CONTRIBUTING.md` for agent creation conventions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — agent scaffolding with schema validation, delegation design, and memory integration |
