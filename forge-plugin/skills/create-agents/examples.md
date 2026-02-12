# Create Agents Examples

This file contains example scenarios demonstrating how to use the create-agents skill to design and build custom Claude Code agents.

---

## Example 1: Creating a Security Engineer Specialist Agent

### Scenario
A team needs a dedicated security-focused agent that can perform code audits, identify vulnerabilities, and recommend security best practices.

### User Prompt
```
Create a security engineer agent that specializes in code security audits and vulnerability detection
```

### Skill Execution

**Step 1 - Requirements Gathering**:
- **Purpose**: Security-focused code review and vulnerability detection
- **Role**: Specialist agent (narrow, deep expertise)
- **Name**: `security-engineer`
- **Model**: `sonnet` (needs strong reasoning for vulnerability analysis)
- **Users**: Developers requesting security reviews, CI/CD pipelines

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("create-agents", "forge")` → No previous agent creation patterns found
- First agent creation session

**Step 3 - Load Context**:
- Reviewed existing agents: `@ares`, `@athena` for security-adjacent patterns
- Loaded `agent_config.schema.json` for validation requirements
- Identified relevant skills: `python-code-review`, `dotnet-code-review`
- Available domains: `security`, `engineering`, `python`

**Step 4 - Design Architecture**:
- **Skills**: `python-code-review`, `dotnet-code-review`, `angular-code-review`
- **Primary domains**: `security`, `engineering`
- **Secondary domains**: `python`, `dotnet`
- **Tools**: `Read`, `Bash`, `Grep`, `Glob` (no Write — reports only)
- **Delegation**: Delegates to language-specific review skills
- **Memory path**: `forge-plugin/memory/agents/security-engineer/`

**Step 5 - Generate Files**:

`forge-plugin/agents/security-engineer.md`:
```markdown
# Security Engineer

You are a security-focused engineering specialist...
(Agent personality, expertise, workflow)
```

`forge-plugin/agents/security-engineer.config.json`:
```json
{
  "name": "security-engineer",
  "description": "Security-focused code auditing and vulnerability detection",
  "model": "sonnet",
  "tools": ["Read", "Bash", "Grep", "Glob"],
  "context": {
    "primaryDomains": ["security", "engineering"],
    "secondaryDomains": ["python", "dotnet"],
    "alwaysLoadFiles": ["context/security/owasp_top_10.md"]
  },
  "skills": [
    { "name": "python-code-review", "trigger": "python security audit" },
    { "name": "dotnet-code-review", "trigger": "dotnet security audit" }
  ],
  "memory": {
    "storagePath": "forge-plugin/memory/agents/security-engineer"
  }
}
```

**Step 6 - Output**:
- Saved to `/claudedocs/create-agents_forge_2026-02-12_security-engineer.md`
- Validation: ✅ Schema valid, ✅ All skills exist, ✅ All domains exist

**Step 7 - Update Memory**:
- Stored specialist agent creation pattern
- Documented security domain mapping

---

## Example 2: Creating a Documentation Specialist Agent

### Scenario
A project needs an agent dedicated to maintaining and generating documentation across the entire codebase.

### User Prompt
```
Build an agent that handles all documentation tasks — README files, API docs, architecture docs, and changelogs
```

### Skill Execution

**Step 1 - Requirements Gathering**:
- **Purpose**: Documentation lifecycle management
- **Role**: Specialist agent
- **Name**: `documentation-specialist`
- **Model**: `sonnet` (needs strong writing and comprehension)
- **Users**: Developers needing docs generated or updated

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("create-agents", "forge")` → Found previous creation patterns
- Applied naming conventions from earlier sessions

**Step 3 - Load Context**:
- Reviewed `@technical-writer` agent for overlap assessment
- Loaded `documentation-generator` skill for capability mapping
- Confirmed `engineering` domain availability

**Step 4 - Design Architecture**:
- **Skills**: `documentation-generator`, `commit-helper`
- **Primary domains**: `engineering`
- **Secondary domains**: `git`
- **Tools**: `Read`, `Write`, `Bash`, `Grep`, `Glob`
- **Delegation**: Uses `documentation-generator` skill for heavy lifting
- **Memory path**: `forge-plugin/memory/agents/documentation-specialist/`

**Step 5 - Generate Files**:

`forge-plugin/agents/documentation-specialist.config.json`:
```json
{
  "name": "documentation-specialist",
  "description": "Documentation lifecycle management for codebases",
  "model": "sonnet",
  "tools": ["Read", "Write", "Bash", "Grep", "Glob"],
  "context": {
    "primaryDomains": ["engineering"],
    "secondaryDomains": ["git"],
    "alwaysLoadFiles": []
  },
  "skills": [
    { "name": "documentation-generator", "trigger": "generate docs" },
    { "name": "commit-helper", "trigger": "commit documentation changes" }
  ],
  "memory": {
    "storagePath": "forge-plugin/memory/agents/documentation-specialist"
  }
}
```

**Step 6 - Output**:
- Saved to `/claudedocs/create-agents_forge_2026-02-12_documentation-specialist.md`
- Validation: ✅ All checks passed

**Step 7 - Update Memory**:
- Updated agent patterns with documentation-specialist template
- Noted overlap considerations with existing `@technical-writer`

---

## Example 3: Creating a Data Pipeline Agent

### Scenario
A data engineering team wants an agent that can design, review, and troubleshoot ETL/ELT pipelines.

### User Prompt
```
Create a custom agent for data pipeline development — ETL design, schema validation, and pipeline debugging
```

### Skill Execution

**Step 1 - Requirements Gathering**:
- **Purpose**: Data pipeline design, review, and debugging
- **Role**: Specialist agent
- **Name**: `data-pipeline-engineer`
- **Model**: `sonnet`
- **Users**: Data engineers building and maintaining pipelines

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("create-agents", "forge")` → Loaded patterns
- Applied established conventions

**Step 3 - Load Context**:
- Reviewed `@demeter` and `@poseidon` for data-adjacent patterns
- Confirmed `database-schema-analysis` and `file-schema-analysis` skills available
- Identified `schema` and `engineering` domains

**Step 4 - Design Architecture**:
- **Skills**: `database-schema-analysis`, `file-schema-analysis`, `python-code-review`
- **Primary domains**: `schema`, `engineering`
- **Secondary domains**: `python`
- **Tools**: `Read`, `Write`, `Bash`, `Grep`, `Glob`
- **Delegation**: Delegates schema validation to analysis skills
- **Memory path**: `forge-plugin/memory/agents/data-pipeline-engineer/`

**Step 5 - Generate Files**:

`forge-plugin/agents/data-pipeline-engineer.config.json`:
```json
{
  "name": "data-pipeline-engineer",
  "description": "Data pipeline design, schema validation, and debugging",
  "model": "sonnet",
  "tools": ["Read", "Write", "Bash", "Grep", "Glob"],
  "context": {
    "primaryDomains": ["schema", "engineering"],
    "secondaryDomains": ["python"],
    "alwaysLoadFiles": []
  },
  "skills": [
    { "name": "database-schema-analysis", "trigger": "analyze database schema" },
    { "name": "file-schema-analysis", "trigger": "validate file schemas" },
    { "name": "python-code-review", "trigger": "review pipeline code" }
  ],
  "memory": {
    "storagePath": "forge-plugin/memory/agents/data-pipeline-engineer"
  }
}
```

**Step 6 - Output**:
- Saved to `/claudedocs/create-agents_forge_2026-02-12_data-pipeline-engineer.md`
- Validation: ✅ Schema valid, ✅ Skills exist, ✅ Domains exist, ✅ Memory path ready

**Step 7 - Update Memory**:
- Stored data-domain agent pattern
- Documented multi-skill delegation strategy for pipeline agents

---

## Summary of Agent Types

| Type | Example | Model | Focus |
|------|---------|-------|-------|
| Olympian | `@athena` | opus/sonnet | Broad domain expertise |
| Specialist | `security-engineer` | sonnet | Deep narrow expertise |
| Task Runner | `data-pipeline-engineer` | sonnet/haiku | Specific workflow automation |

## Best Practices

- Always pair `.md` and `.config.json` files — both are required
- Validate against `agent_config.schema.json` before finalizing
- Verify all referenced skills exist in `forge-plugin/skills/`
- Verify all referenced domains exist in `forge-plugin/context/`
- Create the memory directory even if initially empty
- Consider overlap with existing agents before creating new ones
- Use descriptive, hyphenated names that reflect the agent's function
- Keep agent descriptions concise but specific about capabilities
- Define clear delegation boundaries to avoid agent confusion
