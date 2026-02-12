# Skill Review Auditor Examples

This file contains example scenarios demonstrating how to use the skill-review skill to audit claude-skills for standards compliance, accuracy, and quality.

---

## Example 1: Reviewing a Well-Structured Skill (Mostly Passing)

### Scenario
Auditing the `commit-helper` skill — a mature, well-maintained skill with proper structure, accurate examples, and current references.

### User Prompt
```
Review the commit-helper skill
```

### Skill Execution

**Step 1 — Initial Analysis**:
```
Target skill: commit-helper
Skill path: skills/commit-helper/
Files found:
- SKILL.md ✅
- examples.md ✅
Memory index: memory/skills/commit-helper/ ✅
SKILL_TEMPLATE.md loaded for comparison ✅
```

**Step 2 — Load Memory**:
- No previous skill-review memory found; first review session

**Step 3 — Load Context**:
- Loaded engineering domain context
- Loaded documentation standards context

**Step 4 — Phase 1: Standards Compliance** (Pass):
- YAML frontmatter: All required fields present ✅
  - `name: commit-helper` matches directory name ✅
  - `version: 1.0.0` valid semver ✅
  - `description` present and meaningful ✅
  - `context.primary_domain: engineering` ✅
  - `context.memory.skill_memory: commit-helper` ✅
  - `context.memory.scopes` present with scopes ✅
  - `tags` present ✅
  - `triggers` present ✅
- Mandatory workflow steps: All present in correct order ✅
  - Initial Analysis → Load Memory → Load Context → Core Steps → Output → Memory Update
- Compliance checklist: Present with one item per step ✅
- Version history: Present with initial entry ✅
- Interface references: All four interfaces linked, no hardcoded paths ✅

**Step 5 — Phase 2: Official Documentation Verification** (Pass):
- Conventional Commits specification reference: valid, current (v1.0.0) ✅
- Git diff command flags: correct and current ✅
- No deprecated APIs or patterns detected ✅

**Step 6 — Phase 3: Code Accuracy** (Pass):
- Git command examples syntactically correct ✅
- Commit message format examples follow Conventional Commits spec ✅
- Example outputs match described behavior ✅

**Step 7 — Phase 4: Cross-File Consistency** (Warn):
- SKILL.md description matches frontmatter ✅
- examples.md demonstrates all workflow steps ✅
- Memory index references correct skill name ✅
- Minor finding: One example in examples.md references a "Step 5" but SKILL.md only defines 4 steps ⚠️

**Step 8 — Phase 5: Version Drift Detection** (Pass):
- Conventional Commits v1.0.0: current ✅
- Git commands: stable, no drift ✅
- No framework-specific version dependencies ✅

**Step 9 — Phases 6–9: Quality Assessment**:
- Phase 6 — Description Clarity (Pass): Purpose immediately clear, steps unambiguous ✅
- Phase 7 — Example Quality (Pass): 8 examples covering common scenarios ✅
- Phase 8 — Token Efficiency (Warn): Some workflow descriptions could be more concise; repetitive phrasing in steps 2 and 3 ⚠️
- Phase 9 — Error Prevention (Pass): Gate conditions present at critical steps ✅

**Step 10 — Audit Report**:

### Generated Report

```markdown
<!-- SKILL_REVIEW: skill=commit-helper grade=B pass=7 warn=2 fail=0 date=2025-07-15 -->

# Skill Review Report: commit-helper

## Executive Summary

The commit-helper skill is well-structured and functionally accurate. It follows
Forge conventions closely with proper frontmatter, interface references, and a
clear workflow. Two minor warnings identified: a step numbering inconsistency in
examples.md and opportunities for improved token efficiency in the SKILL.md body.

## Phase Score Card

| Phase | Area | Result |
|-------|------|--------|
| 1 | Standards Compliance | ✅ Pass |
| 2 | Official Docs Verification | ✅ Pass |
| 3 | Code Accuracy | ✅ Pass |
| 4 | Cross-File Consistency | ⚠️ Warn |
| 5 | Version Drift Detection | ✅ Pass |
| 6 | Description Clarity | ✅ Pass |
| 7 | Example Quality | ✅ Pass |
| 8 | Token Efficiency | ⚠️ Warn |
| 9 | Error Prevention | ✅ Pass |

## Overall Skill Health Score: B

0 Fail, 2 Warn — Good, minor improvements recommended.

## Prioritized Recommendations

🟡 **Fix step reference mismatch in examples.md** (Cross-File Consistency)
   Example 4 references "Step 5" but SKILL.md defines only 4 workflow steps.
   Update the example to use correct step numbering.

🟢 **Reduce repetitive phrasing in SKILL.md** (Token Efficiency)
   Steps 2 and 3 contain near-identical boilerplate. Consider using a shared
   reference to the standard loading patterns.
```

**Step 11 — Output**:
File: `/claudedocs/skill_review_commit-helper_2025-07-15.md`

**Step 12 — Memory Update**:
- Created `review_history.md` with initial entry for commit-helper (Grade: B)
- Created `common_issues.md` with step-numbering mismatch pattern noted

---

## Example 2: Reviewing a Skill with Outdated References (Version Drift Detected)

### Scenario
Auditing a Python code review skill that references outdated library versions and deprecated linting patterns.

### User Prompt
```
Audit python-code-review — check if it needs updates
```

### Skill Execution

**Step 1 — Initial Analysis**:
```
Target skill: python-code-review
Skill path: skills/python-code-review/
Files found:
- SKILL.md ✅
- examples.md ✅
Memory index: memory/skills/python-code-review/ ✅
SKILL_TEMPLATE.md loaded for comparison ✅
```

**Step 2 — Load Memory**:
- Previous review found: python-code-review was last reviewed 6 months ago (Grade: A)
- Common issues log: no prior drift issues for this skill

**Step 3 — Load Context**:
- Loaded engineering domain context
- Loaded Python domain context for framework-specific checks

**Step 4 — Phase 1: Standards Compliance** (Pass):
- All required frontmatter fields present ✅
- Mandatory workflow steps in correct order ✅
- Compliance checklist present ✅
- Version history present ✅
- Interface references present, no hardcoded paths ✅

**Step 5 — Phase 2: Official Documentation Verification** (Fail):
- References `pylint` as primary linter but `ruff` has superseded it for most use cases ❌
- References `flake8` configuration patterns; `flake8` is now commonly replaced by `ruff` ❌
- `mypy` references are current and valid ✅
- PEP 8 reference URL is valid ✅

**Step 6 — Phase 3: Code Accuracy** (Warn):
- Most code examples syntactically correct ✅
- One example uses `pylint --rcfile=.pylintrc` which is valid but outdated pattern ⚠️
- Type hint examples use Python 3.9 syntax (`List[str]`) instead of modern 3.10+ (`list[str]`) ⚠️

**Step 7 — Phase 4: Cross-File Consistency** (Pass):
- SKILL.md and examples.md are consistent ✅
- Memory index references correct skill name ✅
- All internal references resolve ✅

**Step 8 — Phase 5: Version Drift Detection** (Fail):
- Skill references Python 3.9 patterns; Python 3.12 is current stable ❌
- `pylint` is referenced as primary tool; `ruff` (v0.5+) is now the community standard ❌
- `black` formatter referenced; `ruff format` has largely replaced standalone `black` ❌
- `isort` import sorting referenced; `ruff` handles this natively now ❌
- `mypy` version reference is current ✅

**Step 9 — Phases 6–9: Quality Assessment**:
- Phase 6 — Description Clarity (Pass): Clear purpose and workflow ✅
- Phase 7 — Example Quality (Pass): Good coverage of review scenarios ✅
- Phase 8 — Token Efficiency (Pass): Concise and well-structured ✅
- Phase 9 — Error Prevention (Pass): Proper gate conditions ✅

**Step 10 — Audit Report**:

### Generated Report

```markdown
<!-- SKILL_REVIEW: skill=python-code-review grade=D pass=7 warn=1 fail=2 date=2025-07-15 -->

# Skill Review Report: python-code-review

## Executive Summary

The python-code-review skill has solid structure and clear documentation but
suffers from significant version drift. The skill references pylint, flake8,
black, and isort as primary tools, but the Python ecosystem has largely converged
on ruff as a unified replacement. Code examples use Python 3.9 type hint syntax
instead of modern 3.10+ patterns. Immediate updates recommended.

## Phase Score Card

| Phase | Area | Result |
|-------|------|--------|
| 1 | Standards Compliance | ✅ Pass |
| 2 | Official Docs Verification | ❌ Fail |
| 3 | Code Accuracy | ⚠️ Warn |
| 4 | Cross-File Consistency | ✅ Pass |
| 5 | Version Drift Detection | ❌ Fail |
| 6 | Description Clarity | ✅ Pass |
| 7 | Example Quality | ✅ Pass |
| 8 | Token Efficiency | ✅ Pass |
| 9 | Error Prevention | ✅ Pass |

## Overall Skill Health Score: D

2 Fail — Below standard, significant rework needed.

## Prioritized Recommendations

🔴 **Migrate primary linting references from pylint/flake8 to ruff** (Docs Verification, Version Drift)
   Replace all `pylint` and `flake8` references with `ruff check`. Update
   configuration examples from `.pylintrc`/`.flake8` to `ruff.toml` or
   `pyproject.toml [tool.ruff]` sections.

🔴 **Replace black/isort references with ruff format** (Version Drift)
   `ruff format` replaces `black` and `ruff check --select I` replaces `isort`.
   Update all formatter and import sorting examples.

🔴 **Update type hint syntax to Python 3.10+ patterns** (Code Accuracy)
   Replace `List[str]`, `Dict[str, int]`, `Optional[str]` with `list[str]`,
   `dict[str, int]`, `str | None` throughout SKILL.md and examples.md.

🟡 **Update minimum Python version reference to 3.10+** (Version Drift)
   The skill should target Python 3.10+ as the minimum for modern features.

🟢 **Add ruff migration example to examples.md** (Example Quality)
   Add an example showing how to review code that uses the modern ruff-based
   toolchain.
```

**Step 11 — Output**:
File: `/claudedocs/skill_review_python-code-review_2025-07-15.md`

**Step 12 — Memory Update**:
- Appended python-code-review review to `review_history.md` (Grade: D, down from A)
- Updated `common_issues.md`: added "Python tooling drift — pylint/flake8/black → ruff migration" as recurring pattern

---

## Example 3: Reviewing a Skill with Cross-File Inconsistencies

### Scenario
Auditing a skill where the SKILL.md workflow doesn't match the examples.md scenarios, and the memory index references an incorrect skill name.

### User Prompt
```
Check the generate-mock-service skill for consistency issues
```

### Skill Execution

**Step 1 — Initial Analysis**:
```
Target skill: generate-mock-service
Skill path: skills/generate-mock-service/
Files found:
- SKILL.md ✅
- examples.md ✅
Memory index: memory/skills/generate-mock-service/ ✅
SKILL_TEMPLATE.md loaded for comparison ✅
```

**Step 2 — Load Memory**:
- No previous review found for this skill

**Step 3 — Load Context**:
- Loaded engineering domain context
- Loaded JavaScript/TypeScript domain context (skill targets Node.js mock services)

**Step 4 — Phase 1: Standards Compliance** (Warn):
- YAML frontmatter: Most fields present ✅
  - `name: generate-mock-service` ✅
  - `version: 1.0.0` ✅
  - `description` present ✅
  - `context.primary_domain` present ✅
  - `context.memory.skill_memory` present ✅
  - `context.memory.scopes` present ✅
  - `tags` present ✅
  - `triggers` missing ⚠️ — no triggers defined in frontmatter
- Mandatory workflow steps: Present but Step 6 (Generate Output) missing `/claudedocs/` reference ⚠️
- Compliance checklist: Present ✅
- Version history: Present ✅
- Interface references: Present, no hardcoded paths ✅

**Step 5 — Phase 2: Official Documentation Verification** (Pass):
- Express.js references current ✅
- MSW (Mock Service Worker) reference valid ✅
- No deprecated APIs detected ✅

**Step 6 — Phase 3: Code Accuracy** (Pass):
- Code examples syntactically correct ✅
- Mock service generation examples produce valid Node.js code ✅
- No logical errors detected ✅

**Step 7 — Phase 4: Cross-File Consistency** (Fail):
- SKILL.md defines a 7-step workflow, but examples.md only demonstrates steps 1–5 ❌
  - Missing: Step 6 (Generate Output) and Step 7 (Update Memory) not shown in any example
- Memory index file references `skill_memory: mock-service-generator` but frontmatter says `generate-mock-service` ❌
  - `memory/skills/generate-mock-service/index.md` line 8: `skill:mock-service-generator`
  - `skills/generate-mock-service/SKILL.md` frontmatter: `skill_memory: generate-mock-service`
- Example 2 in examples.md describes generating a GraphQL mock but SKILL.md workflow makes no mention of GraphQL support ⚠️
- SKILL.md File Structure section lists a `templates/` directory but no templates directory exists ⚠️

**Step 8 — Phase 5: Version Drift Detection** (Pass):
- Express.js v4.x reference: current stable ✅
- MSW v2.x reference: current ✅
- Node.js version references appropriate ✅

**Step 9 — Phases 6–9: Quality Assessment**:
- Phase 6 — Description Clarity (Pass): Purpose is clear ✅
- Phase 7 — Example Quality (Warn): Examples don't cover full workflow; GraphQL example undocumented in SKILL.md ⚠️
- Phase 8 — Token Efficiency (Pass): Concise structure ✅
- Phase 9 — Error Prevention (Pass): Gate conditions present ✅

**Step 10 — Audit Report**:

### Generated Report

```markdown
<!-- SKILL_REVIEW: skill=generate-mock-service grade=D pass=5 warn=3 fail=2 date=2025-07-15 -->

# Skill Review Report: generate-mock-service

## Executive Summary

The generate-mock-service skill has accurate code and current external references
but suffers from significant cross-file inconsistencies. The examples.md omits
the final workflow steps, the memory index references an incorrect skill name,
and an undocumented GraphQL capability appears in examples without corresponding
SKILL.md support. These inconsistencies could confuse both users and AI agents.

## Phase Score Card

| Phase | Area | Result |
|-------|------|--------|
| 1 | Standards Compliance | ⚠️ Warn |
| 2 | Official Docs Verification | ✅ Pass |
| 3 | Code Accuracy | ✅ Pass |
| 4 | Cross-File Consistency | ❌ Fail |
| 5 | Version Drift Detection | ✅ Pass |
| 6 | Description Clarity | ✅ Pass |
| 7 | Example Quality | ⚠️ Warn |
| 8 | Token Efficiency | ✅ Pass |
| 9 | Error Prevention | ✅ Pass |

## Overall Skill Health Score: D

2 Fail, 3 Warn — Below standard, significant rework needed.

## Prioritized Recommendations

🔴 **Fix memory index skill name mismatch** (Cross-File Consistency)
   `memory/skills/generate-mock-service/index.md` line 8 references
   `mock-service-generator`. Update to `generate-mock-service` to match
   the SKILL.md frontmatter `skill_memory` field.

🔴 **Add Steps 6–7 to examples.md** (Cross-File Consistency)
   All examples stop after Step 5. Add Generate Output and Update Memory
   steps to at least one example to demonstrate the complete workflow.

🟡 **Add triggers to YAML frontmatter** (Standards Compliance)
   The `triggers` field is missing. Add entries like:
   `["generate mock service", "create mock API", "mock service"]`

🟡 **Document GraphQL support in SKILL.md or remove from examples** (Cross-File Consistency)
   Example 2 demonstrates GraphQL mock generation, but SKILL.md workflow
   does not mention GraphQL. Either add GraphQL support to the workflow
   or remove the example.

🟡 **Add /claudedocs/ reference to Step 6** (Standards Compliance)
   The Generate Output step should reference the `/claudedocs/` output
   directory per Forge conventions.

🟢 **Remove templates/ from File Structure or create the directory** (Cross-File Consistency)
   SKILL.md lists a `templates/` directory that doesn't exist. Either
   create it with the referenced templates or remove it from the listing.
```

**Step 11 — Output**:
File: `/claudedocs/skill_review_generate-mock-service_2025-07-15.md`

**Step 12 — Memory Update**:
- Created `review_history.md` with generate-mock-service review (Grade: D)
- Created `common_issues.md` with two patterns: "memory index skill name mismatch" and "examples.md incomplete workflow coverage"

---

## Summary of Review Scenarios

1. **Well-structured skill** — Mostly passing with minor warnings; recommendations are refinements
2. **Outdated references** — Version drift causes failures; ecosystem migration needed
3. **Cross-file inconsistencies** — Mismatches between SKILL.md, examples.md, and memory index

## Best Practices

- Always load SKILL_TEMPLATE.md as the baseline for structural comparison
- Check cross-file consistency before code accuracy — structural issues often cause content issues
- Use specific file:line references in findings so issues are immediately actionable
- When version drift is detected, recommend specific migration paths, not just "update"
- Track common issues across reviews to identify systemic patterns in the skill library
- Run full 9-phase reviews even when the user asks about only one concern
