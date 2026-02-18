---
# REQUIRED FRONTMATTER FIELDS
# Replace all placeholders in curly braces with actual values

name: {skill-name}  # Lowercase, hyphen-separated (e.g., generate-python-unit-tests)
description: {Brief one-line description of what this skill does}
version: "1.0.0"  # Semantic versioning

# CONTEXT CONFIGURATION (REQUIRED)
context:
  primary_domain: "{domain-name}"  # REQUIRED: python, dotnet, angular, security, git, azure, schema, engineering
  file_budget: 4  # REQUIRED: Maximum number of context files to load (typically 4-6)
  # Optional: specific topics to load from domain
  topics: ["{topic1}", "{topic2}"]  # e.g., [unit_testing_standards, mocking_patterns]

# MEMORY CONFIGURATION (REQUIRED)
memory:
  scopes:  # REQUIRED: Define what memory gets persisted
    - type: "skill-specific"  # Skill-specific memory files
      files: ["{file1}.md", "{file2}.md"]  # e.g., [project_overview.md, common_patterns.md]
    - type: "shared-project"  # Can reference cross-skill insights
      usage: "reference"

# OPTIONAL: Tags for categorization
tags: ["{tag1}", "{tag2}", "{tag3}"]
---

# {skill-name}

<!-- Brief description of what this skill does and when to use it -->

## Version

**v{X.Y.Z}** - {Release note or description}

## File Structure

### Skill Files
```
forge-plugin/skills/{skill-name}/
├── SKILL.md                    # This file - main skill definition
├── examples.md                 # Usage examples and sample outputs
├── scripts/                    # (Optional) Helper scripts
│   └── {helper_script}.py
└── templates/                  # (Optional) Output templates
    └── {template_file}.txt
```

### Interface References

<!-- ALWAYS use interface references, NEVER hardcoded paths -->

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Loading Protocol**: [Context Loading Protocol](../../context/loading_protocol.md)

### Context (via ContextProvider)

<!-- List the context files this skill needs, accessed through contextProvider methods -->

- `contextProvider.getDomainIndex("{domain}")` — Domain context navigation
- `contextProvider.getConditionalContext("{domain}", "{topic}")` — Topic-specific context
- Additional domain-specific context as needed

### Memory (via MemoryStore)

<!-- List the memory files this skill creates/maintains, accessed through memoryStore methods -->

- `memoryStore.getSkillMemory("{skill-name}", project)` returns per-project files:
  - `{memory_file1}.md` — Description of what this file contains
  - `{memory_file2}.md` — Description of what this file contains
  - `{memory_file3}.md` — Description of what this file contains

## Purpose

<!-- Detailed description of the skill's purpose and capabilities -->

{Explain what this skill does, what problems it solves, and when it should be used}

## Inputs

<!-- Define what inputs this skill requires -->

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| {input1} | {type} | Yes/No | {What this input is for} |
| {input2} | {type} | Yes/No | {What this input is for} |

## Outputs

<!-- Define what this skill produces -->

**Output Location**: `/claudedocs/`

**Naming Convention**: Follow [OUTPUT_CONVENTIONS.md](./OUTPUT_CONVENTIONS.md)
- Pattern: `{skill-name}_{project}_{YYYY-MM-DD}[_qualifier].md`
- Example: `{skill-name}_myproject_2026-02-18.md`

**Output Contents**: {Describe what the output file contains}

## Mandatory Workflow

<!-- THE 6 MANDATORY STEPS - These MUST be H2 headings for programmatic extraction -->
<!-- Each step should use interface references, NOT hardcoded paths -->

> **CRITICAL**: Execute ALL 6 steps in order. Skipping any step invalidates the skill execution.

### Step 1: Initial Analysis

**Purpose**: Gather inputs and understand the task scope.

**Actions**:
1. Validate required inputs are provided
2. Determine project name (from git remote, repo name, or user input)
3. Detect relevant project characteristics (language, framework, etc.)
4. Identify what needs to be analyzed or generated

**Validation**:
- [ ] All required inputs validated
- [ ] Project name determined
- [ ] Project characteristics identified
- [ ] Task scope clear

---

### Step 2: Load Memory

**Purpose**: Load project-specific patterns and history.

**Actions**:
1. Load skill memory via `memoryStore.getSkillMemory("{skill-name}", project)`
2. Review existing memory files:
   - `{memory_file1}.md` — {What to look for in this file}
   - `{memory_file2}.md` — {What to look for in this file}
   - `{memory_file3}.md` — {What to look for in this file}
3. If no memory exists, note this is a new project (memory will be created in Step 6)
4. (Optional) Check shared project memory via `memoryStore.getByProject(project)` for cross-skill insights

**Validation**:
- [ ] Project memory checked via memoryStore
- [ ] Existing patterns loaded (if available)
- [ ] Cross-skill insights reviewed (if relevant)
- [ ] Ready to create new memory (if needed)

---

### Step 3: Load Context

**Purpose**: Load domain knowledge and best practices.

**Actions**:
1. Load domain index via `contextProvider.getDomainIndex("{domain}")`
2. Follow [Context Loading Protocol](../../context/loading_protocol.md):
   - Read domain index
   - Load "always-load" files
   - Detect project type (if detection file exists)
   - Load conditional context based on detection
   - Check cross-domain context needs
3. **Always load** (core context files):
   - `contextProvider.getConditionalContext("{domain}", "{topic1}")` — {Why this is needed}
   - `contextProvider.getConditionalContext("{domain}", "{topic2}")` — {Why this is needed}
4. **Conditionally load** (based on analysis from Step 1):
   - Load additional context via contextProvider based on detected characteristics
   - Stay within file_budget limit (typically 4-6 files)
5. (Optional) Load cross-domain context if needed (e.g., security guidelines)

**Validation**:
- [ ] Domain index loaded via contextProvider
- [ ] Core context files loaded
- [ ] Conditional context loaded based on detection
- [ ] File budget not exceeded
- [ ] Cross-domain context loaded (if needed)

---

### Step 4: {Core Action Name}

**Purpose**: {Describe the main action this skill performs}

**Actions**:
1. {First main action using loaded context and memory}
2. {Second main action}
3. {Third main action}
4. Apply patterns from memory
5. Apply best practices from context

**Validation**:
- [ ] {Validation criterion 1}
- [ ] {Validation criterion 2}
- [ ] {Validation criterion 3}
- [ ] Memory patterns applied
- [ ] Context best practices followed

---

### Step 5: Generate Output

**Purpose**: Create the output artifact following conventions.

**Actions**:
1. Create output file in `/claudedocs/` directory
2. Use naming convention from [OUTPUT_CONVENTIONS.md](./OUTPUT_CONVENTIONS.md):
   - Pattern: `{skill-name}_{project}_{YYYY-MM-DD}.md`
   - Determine project name in priority order: git remote → repo name → working directory
3. Include these sections in output:
   - **Summary**: {What to include}
   - **Details**: {What to include}
   - **Recommendations**: {What to include}
4. Ensure output is actionable and clear

**Validation**:
- [ ] Output file created in `/claudedocs/`
- [ ] Naming convention followed
- [ ] All required sections included
- [ ] Output is clear and actionable

---

### Step 6: Update Memory

**Purpose**: Store learned patterns for future skill invocations.

**Actions**:
1. Update memory files via `memoryStore.update("{skill-name}", project, filename, content)`:
   - **{memory_file1}.md**: Document {what patterns/insights to store}
   - **{memory_file2}.md**: Document {what patterns/insights to store}
   - **{memory_file3}.md**: Document {what patterns/insights to store}
2. Include specifics: file paths, line numbers, patterns discovered
3. Add timestamp (memoryStore handles this automatically)
4. Follow [Memory Quality Guidance](../../memory/quality_guidance.md):
   - Use specific file paths and line numbers
   - Avoid vague descriptions
   - Store project-specific insights (not general knowledge)
5. Follow [Memory Lifecycle](../../memory/lifecycle.md) rules:
   - Stay within size limits (500 lines max per file)
   - Include freshness indicators
   - Prune stale entries

**Validation**:
- [ ] Memory files updated via memoryStore
- [ ] New patterns documented with specifics
- [ ] Quality guidance followed
- [ ] Lifecycle rules followed

---

## Compliance Checklist

<!-- Verify ALL items before completing skill invocation -->

**⚠️ FAILURE TO COMPLETE ALL MANDATORY STEPS INVALIDATES THE SKILL EXECUTION**

### Workflow Compliance
- [ ] Step 1: Initial Analysis completed
- [ ] Step 2: Load Memory completed (used memoryStore interface)
- [ ] Step 3: Load Context completed (used contextProvider interface)
- [ ] Step 4: {Core Action Name} completed
- [ ] Step 5: Generate Output completed
- [ ] Step 6: Update Memory completed (used memoryStore interface)

### Interface Usage
- [ ] Used `contextProvider.*` methods (NOT hardcoded paths)
- [ ] Used `memoryStore.*` methods (NOT hardcoded paths)
- [ ] Followed [Context Loading Protocol](../../context/loading_protocol.md)
- [ ] Followed [Memory Lifecycle](../../memory/lifecycle.md)

### Output Quality
- [ ] Output saved to `/claudedocs/`
- [ ] Naming convention followed
- [ ] Output is clear and actionable
- [ ] {Skill-specific quality criterion 1}
- [ ] {Skill-specific quality criterion 2}

### Memory Quality
- [ ] Memory updated with specific patterns
- [ ] File paths and line numbers included
- [ ] Quality guidance followed

## Examples

See [examples.md](./examples.md) for:
- Sample invocations
- Expected outputs
- Common use cases
- Edge case handling

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | {YYYY-MM-DD} | Initial release |

---

*Template Version: 1.0.0*
*Last Updated: 2026-02-18*
