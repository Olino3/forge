---
name: skill-review
version: 1.0.0
description: Audit claude-skills with systematic 9-phase review — standards compliance, official docs verification, code accuracy, cross-file consistency, and version drift detection. Produces scored audit reports with per-phase findings and prioritized recommendations.
context:
  primary_domain: engineering
  supporting_domains:
    - documentation
  memory:
    skill_memory: skill-review
    scopes:
      - review_history
      - common_issues
tags:
  - planning
  - workflow
  - audit
  - review
  - quality
triggers:
  - review this skill
  - audit skill
  - check if skill needs updates
  - skill quality check
---

# Skill Review Auditor

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 12-step workflow outlined in this document MUST be followed in exact order for EVERY skill review session. Skipping steps or deviating from the procedure will result in incomplete or inaccurate audit results. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Skill review scenarios with sample audit reports
- **Memory**: Skill-specific memory accessed via `memoryStore.getSkillMemory("skill-review", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Audit Focus Areas

Skill review evaluates quality across 9 phases grouped into 4 dimensions:

1. **Structural Compliance**: YAML frontmatter, mandatory workflow steps, compliance checklist, version history, interface references
2. **External Accuracy**: Official documentation verification, URL validity, deprecated API detection
3. **Internal Correctness**: Code example accuracy, output consistency, logical error detection
4. **Cross-File Integrity**: SKILL.md ↔ examples.md ↔ memory index consistency, internal reference resolution
5. **Version Currency**: Technology version drift, outdated framework references, update recommendations

**Note**: The skill produces a scored audit report with per-phase findings and prioritized recommendations. It does not modify the reviewed skill unless explicitly requested.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Identify the target skill to review from the user prompt or conversation context:
   - **Skill name**: The skill identifier (e.g., `commit-helper`, `project-health`)
   - **Skill path**: Resolve to `skills/{skill-name}/`
2. Verify the skill directory exists and contains expected files:
   - `SKILL.md` — skill definition (required)
   - `examples.md` — usage examples (required)
   - `scripts/` — helper scripts (optional)
   - `templates/` — output templates (optional)
3. Load the target skill's files:
   - Read `SKILL.md` completely
   - Read `examples.md` completely
   - Check for memory structure at `memory/skills/{skill-name}/index.md`
4. Load the skill template for comparison: `skills/SKILL_TEMPLATE.md`

**DO NOT PROCEED WITHOUT LOADING THE TARGET SKILL AND SKILL_TEMPLATE.md**

### ⚠️ STEP 2: Load Memory (REQUIRED)

**YOU MUST:**
1. Identify the project name from the user prompt or ask the user
2. Use `memoryStore.getSkillMemory("skill-review", "{project-name}")` to load existing memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
3. If memory exists, review previous review findings:
   - Check for prior reviews of the same target skill
   - Review common issues found across all skill reviews
   - Note patterns from past review sessions
4. **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from other skill executions
5. If no memory exists, you will create it after generating the audit report

**DO NOT PROCEED WITHOUT CHECKING SKILL-REVIEW MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

**YOU MUST:**
1. Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
2. Load supporting context for documentation standards
3. If the target skill references specific technology domains, load relevant context:
   - Python skills: `contextProvider.getIndex("python")`
   - JavaScript/TypeScript skills: `contextProvider.getIndex("javascript")`
   - DevOps skills: `contextProvider.getIndex("devops")`
4. Apply cross-domain triggers as defined in the [Cross-Domain Matrix](../../context/cross_domain.md)

**DO NOT PROCEED WITHOUT LOADING RELEVANT CONTEXT**

### ⚠️ STEP 4: Phase 1 — Standards Compliance (REQUIRED)

**YOU MUST verify structural compliance against SKILL_TEMPLATE.md:**

1. **YAML Frontmatter Completeness**:
   - `name` field present and matches directory name
   - `version` field present with valid semver format
   - `description` field present and meaningful
   - `context.primary_domain` field present
   - `context.memory.skill_memory` field present
   - `context.memory.scopes` field present with at least one scope
   - `tags` field present with relevant tags
   - `triggers` field present with at least one trigger
2. **Mandatory Workflow Steps**:
   - Initial Analysis step present with clear instructions
   - Load Memory step present with `memoryStore` calls
   - Load Context step present with `contextProvider` calls
   - Core skill-specific steps present
   - Generate Output step present with `/claudedocs/` reference
   - Update Memory step present with `memoryStore.update()` call
3. **Compliance Checklist**: Checkbox list present with one item per workflow step
4. **Version History**: Table or list present with at least one entry
5. **Interface References**: All four interface links present (no hardcoded filesystem paths)

**Score**: Pass / Warn / Fail per sub-check

**DO NOT PROCEED WITHOUT COMPLETING STANDARDS COMPLIANCE CHECK**

### ⚠️ STEP 5: Phase 2 — Official Documentation Verification (REQUIRED)

**YOU MUST verify external references:**

1. Check that referenced libraries and frameworks match current stable versions
2. Verify URLs and external references point to valid resources
3. Flag deprecated APIs, patterns, or tools mentioned in the skill
4. Check that recommended practices align with current official documentation
5. Note any references to tools or libraries that have been superseded

**Score**: Pass / Warn / Fail per sub-check

**DO NOT PROCEED WITHOUT COMPLETING DOCUMENTATION VERIFICATION**

### ⚠️ STEP 6: Phase 3 — Code Accuracy (REQUIRED)

**YOU MUST verify code correctness:**

1. Check all code examples in SKILL.md for syntactic correctness
2. Check all code examples in examples.md for syntactic correctness
3. Verify example outputs match described behavior
4. Check for logical errors in workflow descriptions
5. Verify command-line examples use correct flags and syntax

**Score**: Pass / Warn / Fail per sub-check

**DO NOT PROCEED WITHOUT COMPLETING CODE ACCURACY CHECK**

### ⚠️ STEP 7: Phase 4 — Cross-File Consistency (REQUIRED)

**YOU MUST verify internal consistency across all skill files:**

1. **SKILL.md ↔ Frontmatter**: Description in body matches frontmatter description
2. **SKILL.md ↔ examples.md**: Examples demonstrate the workflow steps defined in SKILL.md
3. **SKILL.md ↔ Memory Index**: Memory index references correct skill name and scopes
4. **Internal References**: All file references within the skill resolve correctly
5. **Naming Consistency**: Skill name used consistently across all files (frontmatter, headers, memory paths, interface calls)

**Score**: Pass / Warn / Fail per sub-check

**DO NOT PROCEED WITHOUT COMPLETING CROSS-FILE CONSISTENCY CHECK**

### ⚠️ STEP 8: Phase 5 — Version Drift Detection (REQUIRED)

**YOU MUST check for outdated technology references:**

1. Compare skill's stated versions for referenced technologies against latest stable releases
2. Flag framework or library versions that are more than one major version behind
3. Identify patterns or APIs that have been deprecated since the skill was last updated
4. Check if newer approaches or tools have superseded those recommended by the skill
5. Recommend specific version updates with migration notes where applicable

**Score**: Pass / Warn / Fail per sub-check

**DO NOT PROCEED WITHOUT COMPLETING VERSION DRIFT CHECK**

### ⚠️ STEP 9: Phases 6–9 — Quality Assessment (REQUIRED)

**YOU MUST evaluate overall skill quality across four dimensions:**

1. **Phase 6 — Description Clarity**:
   - Is the skill's purpose immediately clear?
   - Are workflow steps unambiguous and actionable?
   - Are error prevention patterns ("DO NOT PROCEED WITHOUT...") meaningful?

2. **Phase 7 — Example Quality**:
   - Do examples cover common, edge, and error scenarios?
   - Are examples realistic and representative of actual usage?
   - Do examples show complete step-by-step execution?

3. **Phase 8 — Token Efficiency**:
   - Is the skill concise without sacrificing clarity?
   - Are there redundant sections that could be eliminated?
   - Is progressive disclosure used effectively?

4. **Phase 9 — Error Prevention**:
   - Are common mistakes addressed with explicit guards?
   - Do gate conditions prevent skipping critical steps?
   - Are failure modes documented or handled?

**Score**: Pass / Warn / Fail per sub-check

**DO NOT PROCEED WITHOUT COMPLETING QUALITY ASSESSMENT**

### ⚠️ STEP 10: Generate Audit Report (REQUIRED)

**YOU MUST produce a structured audit report with:**

1. **Executive Summary**: One-paragraph overview of the skill's health
2. **Phase Score Card**:

   | Phase | Area | Result |
   |-------|------|--------|
   | 1 | Standards Compliance | Pass/Warn/Fail |
   | 2 | Official Docs Verification | Pass/Warn/Fail |
   | 3 | Code Accuracy | Pass/Warn/Fail |
   | 4 | Cross-File Consistency | Pass/Warn/Fail |
   | 5 | Version Drift Detection | Pass/Warn/Fail |
   | 6 | Description Clarity | Pass/Warn/Fail |
   | 7 | Example Quality | Pass/Warn/Fail |
   | 8 | Token Efficiency | Pass/Warn/Fail |
   | 9 | Error Prevention | Pass/Warn/Fail |

3. **Overall Skill Health Score**: A / B / C / D / F

   **Grading scale**:
   - **A**: 0 Fail, 0–1 Warn — Excellent, no action needed
   - **B**: 0 Fail, 2–3 Warn — Good, minor improvements recommended
   - **C**: 0–1 Fail, any Warn — Acceptable, targeted fixes needed
   - **D**: 2–3 Fail — Below standard, significant rework needed
   - **F**: 4+ Fail — Critical, skill should not be used until fixed

4. **Detailed Findings**: Per-phase findings with specific file:line references where applicable
5. **Prioritized Recommendations**:
   - 🔴 **Critical**: Failures that prevent correct skill operation
   - 🟡 **Important**: Warnings that reduce skill quality or accuracy
   - 🟢 **Nice to have**: Improvements for polish and completeness

**DO NOT GENERATE VAGUE OR GENERIC FINDINGS**

### ⚠️ STEP 11: Generate Output (REQUIRED)

**YOU MUST:**
1. Save the audit report to `/claudedocs/` directory
2. Use the output naming convention: `skill_review_{skill-name}_{YYYY-MM-DD}.md`
3. Include a machine-readable summary block at the top of the report:
   ```
   <!-- SKILL_REVIEW: skill={skill-name} grade=X pass=N warn=N fail=N date=YYYY-MM-DD -->
   ```
4. Confirm the output was written successfully

**DO NOT SKIP OUTPUT GENERATION**

### ⚠️ STEP 12: Update Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.update(layer="skill-specific", skill="skill-review", project="{project-name}", ...)` to store:
   - **review_history.md**: Append the reviewed skill name, date, per-phase scores, overall grade, and key findings
   - **common_issues.md**: Record any new recurring issues found across skills — patterns of non-compliance, common structural gaps, or frequent version drift areas
2. If this is the first review session, create both memory files with initial data
3. If previous memory exists, append to history and update common issues with new observations

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY skill review session, verify:
- [ ] Step 1: Target skill identified, SKILL.md and examples.md loaded, SKILL_TEMPLATE.md loaded
- [ ] Step 2: Skill-review memory checked via `memoryStore.getSkillMemory()` and prior reviews examined
- [ ] Step 3: Engineering and supporting domain context loaded via `contextProvider.getIndex()`
- [ ] Step 4: Phase 1 — Standards compliance checked (frontmatter, workflow, checklist, version history, interfaces)
- [ ] Step 5: Phase 2 — Official documentation references verified for accuracy and currency
- [ ] Step 6: Phase 3 — Code examples verified for syntactic correctness and logical accuracy
- [ ] Step 7: Phase 4 — Cross-file consistency verified across SKILL.md, examples.md, and memory index
- [ ] Step 8: Phase 5 — Version drift checked for all referenced technologies
- [ ] Step 9: Phases 6–9 — Quality assessment completed (clarity, examples, tokens, error prevention)
- [ ] Step 10: Audit report generated with phase scores, findings, and prioritized recommendations
- [ ] Step 11: Output saved to `/claudedocs/` with machine-readable summary block
- [ ] Step 12: Memory updated with review history and common issues

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE SKILL REVIEW SESSION**

---

## Output File Naming Convention

**Format**: `skill_review_{skill-name}_{YYYY-MM-DD}.md`

Where:
- `{skill-name}` = Name of the reviewed skill (kebab-case)
- `{YYYY-MM-DD}` = Date of the review

**Examples**:
- `skill_review_commit-helper_2025-07-15.md`
- `skill_review_project-health_2025-07-15.md`
- `skill_review_python-code-review_2025-07-15.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-15 | Initial release — 12-step mandatory workflow with 9-phase systematic review covering standards compliance, official docs verification, code accuracy, cross-file consistency, version drift detection, and quality assessment |
