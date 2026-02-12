---
name: skill-creator
version: 1.0.0
description: Design effective Claude Code skills with optimal descriptions, progressive disclosure, and error prevention patterns. Covers freedom levels, token efficiency, and quality standards.
context:
  primary_domain: engineering
  supporting_domains:
    - documentation
  memory:
    skill_memory: skill-creator
    scopes:
      - created_skills
      - design_patterns
tags:
  - planning
  - workflow
  - meta
  - skill-design
  - quality
triggers:
  - create a skill
  - new skill
  - design skill
  - build skill
---

# Skill Creator

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 10-step workflow outlined in this document MUST be followed in exact order for EVERY skill creation session. Skipping steps or deviating from the procedure will result in incomplete or poorly designed skills. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Skill creation scenarios with sample outputs
- **Memory**: Skill-specific memory accessed via `memoryStore.getSkillMemory("skill-creator", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Skill Design Focus Areas

Skill creation evaluates requirements across 5 focus areas:

1. **Freedom Level**: Determine whether the skill needs strict procedural steps or flexible guidance
2. **Token Efficiency**: Balance between compact quick-reference and detailed instructions
3. **Error Prevention**: Identify common mistakes and build guards against them
4. **Progressive Disclosure**: Present essential information first, details on demand
5. **Interface Usage**: Determine which interfaces the new skill needs (ContextProvider, MemoryStore, SkillInvoker)

**Note**: The skill produces complete skill directories with SKILL.md, examples.md, and memory structure. It does not register skills in any manifest unless explicitly requested.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Gather skill requirements from the user prompt or conversation context:
   - **Name**: The skill identifier (kebab-case, e.g., `code-review`, `deploy-automation`)
   - **Domain**: Primary context domain (engineering, python, javascript, devops, etc.)
   - **Purpose**: What the skill does and what output it produces
   - **Target Users**: Who will invoke this skill and in what scenarios
   - **Triggers**: Natural language phrases that should activate the skill
2. Classify the skill type:
   - **Code Analysis**: Reviews, audits, inspections of existing code
   - **Code Generation**: Creates new code, tests, configurations
   - **Planning & Workflow**: Designs plans, phases, strategies
   - **Documentation**: Generates docs, READMEs, guides
   - **DevOps & Infrastructure**: Deployment, CI/CD, environment setup
3. Determine scope and complexity:
   - Number of workflow steps needed
   - Which conditional outputs may be generated
   - Integration points with other skills or commands

**DO NOT PROCEED WITHOUT IDENTIFYING SKILL NAME, DOMAIN, PURPOSE, AND TYPE**

### ⚠️ STEP 2: Load Memory (REQUIRED)

**YOU MUST:**
1. Identify the project name from the user prompt or ask the user
2. Use `memoryStore.getSkillMemory("skill-creator", "{project-name}")` to load existing memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
3. If memory exists, review previous skill creation patterns:
   - Check for similar skill types created before
   - Review design patterns that worked well in past skills
   - Note any lessons learned from prior skill creation sessions
4. **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from other skill executions
5. If no memory exists, you will create it after generating the skill

**DO NOT PROCEED WITHOUT CHECKING SKILL-CREATOR MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

**YOU MUST:**
1. Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
2. Load supporting context for documentation standards
3. Load the skill template: `skills/SKILL_TEMPLATE.md` for the canonical skill structure
4. If the new skill targets a specific technology domain, load relevant context:
   - Python skills: `contextProvider.getIndex("python")`
   - JavaScript/TypeScript skills: `contextProvider.getIndex("javascript")`
   - DevOps skills: `contextProvider.getIndex("devops")`
5. Apply cross-domain triggers as defined in the [Cross-Domain Matrix](../../context/cross_domain.md)

**DO NOT PROCEED WITHOUT LOADING CONTEXT AND SKILL_TEMPLATE.md**

### ⚠️ STEP 4: Design Skill Architecture (REQUIRED)

**YOU MUST determine the following design decisions:**

1. **Freedom Level**:
   - **Strict Procedural**: Every step is mandatory and must be followed in exact order (e.g., code review checklists, compliance workflows)
   - **Flexible Guidance**: Steps provide guidance but allow adaptation based on context (e.g., documentation generation, creative tasks)
   - Choose based on: how critical correctness is, how variable the inputs are, how experienced the target users are

2. **Token Budget**:
   - **Compact**: Quick-reference style, minimal explanation, maximum density (best for experienced users, frequently used skills)
   - **Detailed**: Full explanations, rationale for each step, extensive examples (best for complex or rarely used skills)
   - Choose based on: skill complexity, frequency of use, target audience familiarity

3. **Error Prevention Patterns**:
   - Identify the 3-5 most common mistakes users will make with this skill
   - Design guardrails: validation checks, required preconditions, explicit warnings
   - Add "DO NOT PROCEED WITHOUT..." gates at critical decision points

4. **Progressive Disclosure Strategy**:
   - **Essential first**: Core workflow and minimum viable output
   - **Details on demand**: Advanced options, edge cases, customization
   - **Reference appendix**: Schemas, full examples, troubleshooting

5. **Interface Usage**:
   - Determine which interfaces the new skill needs:
     - `ContextProvider` — for loading domain knowledge (nearly always needed)
     - `MemoryStore` — for learning from past executions (recommended for all skills)
     - `SkillInvoker` — for delegating to other skills (only if composing skills)
     - `ExecutionContext` — for chaining with commands (only if command integration needed)

**DO NOT PROCEED WITHOUT DOCUMENTING ALL FIVE DESIGN DECISIONS**

### ⚠️ STEP 5: Generate SKILL.md (REQUIRED)

**YOU MUST produce the skill definition following SKILL_TEMPLATE.md structure:**

1. **YAML Frontmatter** with all required fields:
   - `name`, `version`, `description`
   - `context.primary_domain`, `context.supporting_domains`
   - `context.memory.skill_memory`, `context.memory.scopes`
   - `tags`, `triggers`
2. **Mandatory Compliance Warning**: Clear statement that the workflow must be followed
3. **File Structure**: Directory layout for the skill
4. **Interface References**: Links to all four interface documents
5. **Focus Areas**: Domain-specific evaluation criteria for the skill
6. **Mandatory Workflow Steps**: Each step with:
   - Clear step number and name
   - "YOU MUST" instructions with specific actions
   - "DO NOT PROCEED WITHOUT" gate at critical steps
   - Interface method calls where applicable
7. **Compliance Checklist**: One checkbox per workflow step
8. **Version History**: Initial entry with date and description

**DO NOT PROCEED WITHOUT A COMPLETE SKILL.md**

### ⚠️ STEP 6: Generate examples.md (REQUIRED)

**YOU MUST produce at least 3 usage examples demonstrating the skill in action:**

1. Each example must include:
   - **Scenario**: Description of the use case
   - **User Prompt**: The natural language input that triggers the skill
   - **Skill Execution**: Step-by-step walkthrough showing how the skill processes the request
   - **Generated Output**: Sample output documents or artifacts
2. Examples should cover different scenarios:
   - A straightforward, common use case
   - A complex or edge-case scenario
   - A scenario that demonstrates conditional outputs or advanced features
3. Examples should demonstrate real-world usage, not toy examples

**DO NOT PROCEED WITHOUT AT LEAST 3 COMPLETE EXAMPLES**

### ⚠️ STEP 7: Generate Memory Structure (REQUIRED)

**YOU MUST create the memory directory and index:**

1. Create `memory/skills/{skill-name}/index.md` with:
   - **Purpose**: What this skill's memory tracks
   - **Memory Files**: Description of each memory file with purpose, contents, and example structure
   - **Memory Lifecycle**: Creation → Growth → Maintenance phases
   - **Related Documentation**: Links back to the skill and main memory index
2. Define appropriate memory files based on the skill type:
   - Pattern tracking (what approaches worked well)
   - History logging (past executions and outcomes)
   - Domain-specific learnings (technology-specific insights)

**DO NOT PROCEED WITHOUT INITIALIZING MEMORY STRUCTURE**

### ⚠️ STEP 8: Quality Validation (REQUIRED)

**YOU MUST validate the generated skill against quality standards:**

1. **YAML Frontmatter Completeness**: All required fields present and correctly formatted
2. **Interface References Present**: All four interface links included (no hardcoded paths)
3. **Mandatory Workflow Steps Defined**: Each step has clear instructions and gate conditions
4. **Compliance Checklist Present**: One checkbox per workflow step
5. **Examples Demonstrate Real-World Usage**: At least 3 examples with complete step-by-step execution
6. **Memory Structure Initialized**: index.md created with appropriate memory files defined

**If any validation fails, return to the relevant step and fix the issue before proceeding.**

**DO NOT PROCEED WITHOUT PASSING ALL VALIDATION CHECKS**

### ⚠️ STEP 9: Generate Output (REQUIRED)

**YOU MUST:**
1. Save all generated files to the skill directory:
   - `skills/{skill-name}/SKILL.md` — skill definition
   - `skills/{skill-name}/examples.md` — usage examples
   - `memory/skills/{skill-name}/index.md` — memory structure
2. Confirm all output files were written successfully
3. List all generated files with a brief description of each

**DO NOT SKIP OUTPUT GENERATION**

### ⚠️ STEP 10: Update Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.update(layer="skill-specific", skill="skill-creator", project="{project-name}", ...)` to store:
   - **created_skills.md**: Log the skill name, date, type classification, design decisions (freedom level, token budget), and number of workflow steps
   - **design_patterns.md**: Record effective patterns discovered during this creation session — what worked well, common mistakes avoided, and reusable structures
2. If this is the first skill creation session, create both memory files with initial data
3. If previous memory exists, append to history and update patterns with new learnings

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY skill creation session, verify:
- [ ] Step 1: Skill requirements gathered — name, domain, purpose, type, and triggers identified
- [ ] Step 2: Skill-creator memory checked via `memoryStore.getSkillMemory()` and prior patterns reviewed
- [ ] Step 3: Engineering and supporting domain context loaded via `contextProvider.getIndex()`; SKILL_TEMPLATE.md loaded
- [ ] Step 4: All five design decisions documented — freedom level, token budget, error prevention, progressive disclosure, interface usage
- [ ] Step 5: SKILL.md generated with YAML frontmatter, interface references, mandatory workflow, and compliance checklist
- [ ] Step 6: examples.md generated with at least 3 complete usage examples
- [ ] Step 7: Memory structure initialized with index.md and memory file definitions
- [ ] Step 8: Quality validation passed — all six quality checks confirmed
- [ ] Step 9: All output files saved to the skill directory
- [ ] Step 10: Memory updated with skill creation log and design patterns

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE SKILL CREATION SESSION**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-06-30 | Initial release — 10-step mandatory workflow for designing effective skills with freedom levels, token efficiency, error prevention, and progressive disclosure |
