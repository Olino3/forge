---
name: generate-more-skills-with-claude
description: Generates new Claude Code skills following the Forge plugin architecture and conventions. Analyzes skill requirements, crafts MANDATORY workflows with compliance checklists, produces comprehensive examples, creates templates for output formatting, and ensures adherence to the skill pattern established in the repository. Like Hephaestus forging new divine tools, this meta-skill enables the AI to craft purpose-built skills that expand The Forge's capabilities.
---

# Generate More Skills with Claude

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 6-step workflow outlined in this document MUST be followed in exact order for EVERY skill generation. Skipping steps or deviating from the procedure will result in skills that don't follow the established pattern and won't integrate properly with The Forge. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Skill generation scenarios with complete outputs
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("generate-more-skills-with-claude", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **templates/**:
  - `skill_template.md`: Template for generating SKILL.md files
  - `examples_template.md`: Template for generating examples.md files

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Focus Areas

Skill generation evaluates 8 critical dimensions:

1. **Requirement Analysis**: Understand the problem domain, target audience, and desired outcomes
2. **Workflow Design**: Structure the skill as a mandatory, step-by-step workflow with clear decision points
3. **Compliance Integration**: Build non-negotiable checklists and validation gates into the workflow
4. **Pattern Adherence**: Follow the established skill structure (SKILL.md, examples.md, templates/, scripts/)
5. **Example Diversity**: Create 6+ comprehensive usage scenarios covering the full capability spectrum
6. **Template Creation**: Design reusable output templates that enforce consistency
7. **Memory Integration**: Enable project-specific learning and pattern persistence
8. **Context Awareness**: Leverage existing context files and create new ones when needed

**Note**: Generated skills should be autonomous yet guided — structured workflows ensure consistent, high-quality outputs while maintaining flexibility for different use cases.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Gather Skill Requirements (REQUIRED)

**YOU MUST:**
1. Determine the **skill purpose**: What problem does this skill solve? What value does it provide?
2. Identify the **target users**: Who will use this skill (developers, DevOps, data scientists, managers)?
3. Establish **scope boundaries**: What is explicitly in-scope vs. out-of-scope?
4. Map the **problem domain**:
   - What existing skills are similar or complementary?
   - What tools, frameworks, or technologies does this skill interact with?
   - What expertise is required from the AI to execute this skill?
5. Ask clarifying questions if requirements are incomplete:
   - What inputs will the user provide?
   - What outputs should the skill produce?
   - Are there specific quality standards or compliance requirements?
   - Should this skill integrate with project memory?
   - Should this skill reference existing context files or create new ones?

**DO NOT PROCEED WITHOUT UNDERSTANDING THE SKILL REQUIREMENTS**

### ⚠️ STEP 2: Design the Workflow (REQUIRED)

**YOU MUST:**
1. **Break down the skill into 4-7 sequential steps**:
   - Each step should be atomic and have a clear completion criterion
   - Steps should flow logically: gather context → analyze → process → generate → validate → polish
   - Each step must be marked as REQUIRED with ⚠️ emoji
2. **Identify decision points and branches**:
   - Where does the workflow need user input or clarification?
   - What alternative paths exist (e.g., different output formats, error conditions)?
3. **Define validation gates**:
   - What checks must pass before proceeding to the next step?
   - What quality criteria must the final output meet?
4. **Map dependencies**:
   - Which steps depend on prior step completion?
   - Which steps can reference context files or memory?
5. **Design the compliance checklist**:
   - List the non-negotiable requirements that every execution must satisfy
   - Each checklist item should be verifiable (yes/no answer)

**DO NOT PROCEED WITHOUT A COMPLETE WORKFLOW DESIGN**

### ⚠️ STEP 3: Load Context & Memory (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("generate-more-skills-with-claude", "{project-name}")` to load existing memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - If memory exists, review previously generated skills and patterns
   - If no memory exists, you will create it later in this process
2. **REVIEW EXISTING SKILLS**:
   - Scan `forge-plugin/skills/` to identify similar or related skills
   - Study 2-3 exemplar skills that match the target complexity level
   - Identify reusable patterns from existing skills
3. **IDENTIFY CONTEXT FILE NEEDS**:
   - Use `contextProvider.getDomainIndex("commands")` for overview of available context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
   - Determine which existing context domains are relevant (angular, azure, dotnet, git, python, schema, security)
   - Identify if new context files should be created for this skill's domain
4. **UNDERSTAND THE SKILL PATTERN**:
   - Review the directory structure: SKILL.md, examples.md, templates/, scripts/
   - Note the frontmatter format (name, description in YAML)
   - Understand the mandatory workflow structure and compliance checklist format

**DO NOT PROCEED WITHOUT LOADING CONTEXT AND UNDERSTANDING PATTERNS**

### ⚠️ STEP 4: Generate SKILL.md (REQUIRED)

**YOU MUST:**
1. **Use the template** from `templates/skill_template.md` as the foundation
2. **Write the frontmatter**:
   - `name`: Skill identifier (kebab-case, lowercase, descriptive)
   - `description`: 2-3 sentence description with poetic flair matching The Forge theme
3. **Write the header section**:
   - Skill title (properly formatted)
   - Mandatory compliance warning with critical emphasis
   - File structure section documenting all files in the skill directory
   - Focus Areas: 6-8 dimensions the skill evaluates
4. **Write the mandatory workflow** (4-7 steps):
   - Each step titled with ⚠️ STEP N: Action Name (REQUIRED)
   - Each step includes YOU MUST with numbered sub-tasks
   - Each step ends with a DO NOT PROCEED gate
   - Final step includes project memory update (optional)
5. **Write the compliance checklist**:
   - List all steps with checkbox format: `- [ ] Step N: Description`
   - Add a failure statement: "FAILURE TO COMPLETE ALL STEPS INVALIDATES THE OUTPUT"
6. **Add special case handling** (if applicable):
   - Edge cases, error conditions, alternative paths
   - Each case with clear handling instructions
7. **Add further reading section**:
   - Link to official documentation, best practices, tools
   - 3-5 authoritative external references
8. **Add version history**:
   - v1.0.0 with initial release date
   - List key features and capabilities

**DO NOT PROCEED WITHOUT A COMPLETE SKILL.MD**

### ⚠️ STEP 5: Generate examples.md (REQUIRED)

**YOU MUST:**
1. **Use the template** from `templates/examples_template.md` as the foundation
2. **Create 6+ comprehensive examples** covering:
   - **Example 1**: Simple, straightforward usage (baseline case)
   - **Example 2**: Moderate complexity with some edge cases
   - **Example 3**: Advanced usage with multiple features
   - **Example 4**: Error handling or constraint validation
   - **Example 5**: Integration with memory or context files
   - **Example 6**: Alternative output format or variation
   - *Additional examples as needed for full coverage*
3. **Structure each example** with:
   - **Scenario**: Brief context about the use case
   - **User Prompt**: Exactly what the user would say to invoke the skill
   - **Skill Execution**: Step-by-step walkthrough of the workflow
     - Show how each step of the mandatory workflow is applied
     - Include decision points and choices made
   - **Generated Output**: Complete, realistic output in proper format
     - Use code blocks with appropriate syntax highlighting
     - Show actual file content, not placeholders
4. **Ensure diversity**:
   - Cover different user personas (junior dev, senior architect, manager)
   - Show different output formats and variations
   - Demonstrate integration with other skills or tools
5. **Add a summary section** at the end:
   - List the example types covered
   - Highlight best practices demonstrated across examples

**DO NOT PROCEED WITHOUT COMPREHENSIVE EXAMPLES**

### ⚠️ STEP 6: Generate Templates & Scripts (REQUIRED)

**YOU MUST:**
1. **Create output templates** in `templates/` directory:
   - Identify what outputs the skill produces (documents, code, configs)
   - Create a `.md` template file for each output type
   - Use placeholders wrapped in `{{variable_name}}` or similar convention
   - Include instructions or comments explaining each section
   - Ensure templates enforce the desired output structure
2. **Create helper scripts** (if needed) in `scripts/` directory:
   - Determine if the skill requires automation (file processing, API calls, code generation)
   - Write shell scripts (`.sh`) for Bash-based automation
   - Include clear comments and error handling
   - Make scripts executable: `chmod +x scripts/*.sh`
   - Test scripts work in isolation
3. **Document script usage** in SKILL.md:
   - Add a Scripts section explaining what each script does
   - Include usage examples: `./scripts/script_name.sh <args>`
   - Document dependencies (tools, environment variables)
4. **Validate template structure**:
   - Templates should be complete but generic
   - Placeholders should be clearly marked and documented
   - Templates should match the examples shown in examples.md

**DO NOT SKIP TEMPLATE AND SCRIPT CREATION**

---

## Compliance Checklist

Before completing ANY skill generation, verify:
- [ ] Step 1: Requirements gathered — purpose, users, scope, and domain mapped
- [ ] Step 2: Workflow designed — 4-7 steps, decision points, validation gates, compliance checklist
- [ ] Step 3: Context loaded — memory checked, existing skills reviewed, pattern understood
- [ ] Step 4: SKILL.md generated — frontmatter, workflow, checklist, special cases, references, version
- [ ] Step 5: examples.md generated — 6+ examples with scenarios, prompts, execution, output
- [ ] Step 6: Templates & scripts created — output templates, helper scripts, documentation

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE SKILL**

---

## Special Case Handling

### Generating Skills with External Dependencies

When creating skills that interact with external tools, APIs, or services:
1. Document all dependencies clearly in the SKILL.md file structure section
2. Include setup instructions in a dedicated section
3. Handle authentication and credentials securely (environment variables, config files)
4. Provide fallback behavior when external services are unavailable
5. Include error handling examples showing how to diagnose and recover from failures

### Generating Skills that Modify Code

When creating skills that generate or modify code:
1. Always include a review and validation step before any changes are applied
2. Show the generated code to the user for approval
3. Include linting and testing steps in the workflow
4. Provide rollback or undo instructions
5. Document any assumptions about the target codebase structure

### Generating Skills with Memory Integration

When creating skills that should learn from usage:
1. Document the memory directory structure clearly
2. Explain what gets stored (patterns, configurations, preferences)
3. Include a memory loading step early in the workflow
4. Include an optional memory update step at the end
5. Provide examples showing how memory affects behavior over time

### Generating Skills for Multiple Languages/Frameworks

When creating polyglot skills:
1. Organize the workflow to handle language detection
2. Create separate template files for each supported language
3. Document language-specific behaviors and limitations
4. Provide examples for each major language variant
5. Consider referencing existing context files (angular, dotnet, python)

---

## Further Reading

Refer to official documentation and resources:
- **The Forge Documentation**:
  - `README.md`: Overview of The Forge plugin architecture
  - `ROADMAP.md`: Existing skills and planned capabilities
  - `.github/copilot-instructions.md`: Coding conventions and structure
- **Skill Design Patterns**:
  - Study existing skills: `forge-plugin/skills/*/SKILL.md`
  - Review context files: `forge-plugin/context/index.md`
  - Examine memory structure: `forge-plugin/memory/skills/index.md`
- **Claude Code Resources**:
  - Claude Artifact Creation: https://docs.anthropic.com/claude/artifacts
  - Prompt Engineering Guide: https://docs.anthropic.com/claude/prompt-engineering
  - Best Practices for AI Tools: https://www.anthropic.com/index/best-practices

---

## Version History

- v1.1.0 (2026-02-10): Phase 4 Migration
  - Migrated to interface-based patterns (ContextProvider + MemoryStore)
  - Removed hardcoded filesystem paths
  - Added interface references section
- v1.0.0 (2026-02-09): Initial release
  - Mandatory 6-step workflow for skill generation
  - Template-based SKILL.md and examples.md generation
  - Support for scripts and output templates
  - Memory integration for pattern learning
  - Context file awareness and integration
  - Special case handling for common scenarios
