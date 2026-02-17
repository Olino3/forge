---
name: dev-tools
description: Essential development workflow agents for code review, debugging, testing, documentation, and git operations. Orchestrates multi-step developer workflows by composing existing skills into streamlined pipelines. Triggers: step
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [workflow_patterns.md, tool_preferences.md]
    - type: "shared-project"
      usage: "reference"
tags:
  - workflow
  - orchestration
  - developer-experience
##   - productivity

# skill:dev-tools - Developer Workflow Orchestrator

## Version: 1.0.0

## Purpose

Orchestrate essential development workflows by composing existing Forge skills into streamlined, multi-step pipelines. This skill acts as the developer's command center — coordinating code review, debugging, testing, documentation, and git operations into cohesive workflows.

Use this skill when:
- Need to perform a multi-step development workflow (e.g., review → test → commit)
- Want to compose multiple skills into a single pipeline
- Performing routine development tasks that span multiple tools
- Need guided step-by-step development workflows
- Trigger: `step` — invokes a guided workflow step

## File Structure

```
skills/dev-tools/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Skills**: Delegated via [SkillInvoker Interface](../../interfaces/skill_invoker.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Available Workflow Pipelines

### 1. Review Pipeline
Compose: `get-git-diff` → language-specific code review → `commit-helper`

### 2. Test Pipeline
Compose: `contextProvider.detectProjectType()` → test generation skill → `test-cli-tools`

### 3. Document Pipeline
Compose: code analysis → `documentation-generator` → `commit-helper`

### 4. Debug Pipeline
Compose: `power-debug` → fix implementation → test validation

### 5. Ship Pipeline
Compose: code review → test generation → `commit-helper` → documentation update

### 6. Custom Pipeline
User-defined composition of any available skills

---

### Step 1: Initial Analysis

Gather inputs and understand the task:
- Determine project scope and requirements
- Identify target files or components
- Clarify user objectives and constraints

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Workflow (REQUIRED)

**YOU MUST:**
1. **Determine the requested workflow**:
   - Parse the user's intent to identify which pipeline to execute
   - If user says `step`, ask which workflow they want
   - If ambiguous, present the available pipelines and ask for selection
2. **Identify the workflow steps**:
   - Map the pipeline to specific skills
   - Determine the execution order
   - Identify data dependencies between steps
3. **Detect the project context**:
   - Use `contextProvider.detectProjectType()` to identify language, framework, and tools
   - Select the appropriate language-specific skills (e.g., `python-code-review` for Python)
4. **Confirm the plan with the user**:
   - Present the steps that will be executed
   - Allow the user to modify, skip, or add steps
   - Confirm before proceeding

**DO NOT PROCEED WITHOUT A CLEAR WORKFLOW PLAN**

### ⚠️ STEP 2: Load Memory (REQUIRED)

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="dev-tools"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("dev-tools", "{project-name}")` to load workflow preferences
2. Check for previously used pipelines and their configurations
3. Load project-specific tool preferences (test runner, linter, formatter)
4. Cross-reference with `memoryStore.getByProject("{project-name}")` for broader context

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

**YOU MUST:**
1. Load engineering domain context for workflow patterns
2. Detect project type to select appropriate skills
3. Verify all skills in the pipeline exist and are available

**DO NOT PROCEED WITHOUT LOADING CONTEXT**

### ⚠️ STEP 4: Execute Pipeline (REQUIRED)

**YOU MUST:**
1. **Execute each step in order**:
   - Invoke skills via `skillInvoker.invoke("{skill-name}", params)` or execute directly
   - Pass output from each step as input to the next
   - Report progress after each step completes
2. **Handle step failures gracefully**:
   - If a step fails, report the error and ask the user how to proceed:
     - **Retry**: Run the step again
     - **Skip**: Move to the next step
     - **Abort**: Stop the pipeline
     - **Debug**: Invoke `power-debug` to investigate the failure
3. **Maintain execution context**:
   - Track which steps have completed
   - Preserve intermediate outputs for reference
   - Log timing for each step
4. **Report step results**:
   - After each step, summarize what was done and what was produced
   - Highlight any issues or warnings
   - Show progress through the pipeline (e.g., "Step 2/4 complete")

**DO NOT SKIP ERROR HANDLING**

### ⚠️ STEP 5: Generate Output (REQUIRED)

- Save output to `/claudedocs/dev-tools_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Pipeline executed (name and steps)
  - Results from each step
  - Overall summary and recommendations
  - Time taken per step

### ⚠️ STEP 6: Update Memory (REQUIRED)

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="dev-tools"`. Store any newly learned patterns, conventions, or project insights.

**YOU MUST:**
1. Record the workflow pipeline used and its success/failure
2. Store project-specific tool preferences discovered
3. Document any custom pipeline configurations
4. Update preferred skill compositions for this project

---

## Pipeline Definitions

### Review Pipeline

**Trigger**: "review my changes", "code review", "check my code"

**Steps**:
1. `get-git-diff` — Capture current changes (staged or unstaged)
2. Detect language → Select review skill (`python-code-review`, `dotnet-code-review`, `angular-code-review`)
3. Execute code review with project context
4. Present findings and recommendations
5. Optionally invoke `commit-helper` to craft commit message

### Test Pipeline

**Trigger**: "generate tests", "test my code", "add tests"

**Steps**:
1. `contextProvider.detectProjectType()` — Identify language and test framework
2. Select test generation skill (`generate-python-unit-tests`, `generate-jest-unit-tests`)
3. Generate tests for specified files or modules
4. Run generated tests to verify they pass
5. Optionally invoke `commit-helper` for test commit

### Document Pipeline

**Trigger**: "document this", "generate docs", "update docs"

**Steps**:
1. Analyze target code (files, modules, or project)
2. `documentation-generator` — Generate documentation
3. Review generated docs for completeness
4. Optionally invoke `commit-helper` for docs commit

### Debug Pipeline

**Trigger**: "debug this", "investigate bug", "help me debug"

**Steps**:
1. `power-debug` — Multi-agent investigation
2. Present diagnosis and fix recommendations
3. Implement the chosen fix
4. Run tests to verify the fix
5. Optionally invoke `commit-helper` for fix commit

### Ship Pipeline

**Trigger**: "ship it", "prepare for merge", "ready to merge"

**Steps**:
1. `get-git-diff` — Review all changes
2. Language-specific code review
3. Generate missing tests
4. Run full test suite
5. `documentation-generator` — Update docs if needed
6. `commit-helper` — Craft final commit message
7. Present merge readiness summary

---

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Pipeline steps executed with proper error handling
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Output File Naming Convention

**Format**: `dev-tools_{project}_{YYYY-MM-DD}.md`

**Examples**:
- `dev-tools_myapi_2026-02-12.md`
- `dev-tools_myapi_2026-02-12_review-pipeline.md`

---

## Skill Composition Reference

| Pipeline | Skills Used |
|----------|------------|
| Review | `get-git-diff`, `python-code-review` / `dotnet-code-review` / `angular-code-review`, `commit-helper` |
| Test | `generate-python-unit-tests` / `generate-jest-unit-tests`, `test-cli-tools` |
| Document | `documentation-generator`, `commit-helper` |
| Debug | `power-debug`, test skill, `commit-helper` |
| Ship | `get-git-diff`, review skill, test skill, `documentation-generator`, `commit-helper` |

---

## Further Reading

- **SkillInvoker**: `../../interfaces/skill_invoker.md` for skill delegation patterns
- **ExecutionContext**: `../../interfaces/execution_context.md` for pipeline context passing
- **Available Skills**: `../../skills/` for all available skill definitions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — five predefined pipelines with skill composition, step-by-step execution, and error recovery |
