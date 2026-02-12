---
name: project-health
version: 1.0.0
description: AI-agent readiness auditing for project documentation and workflows. Evaluates documentation completeness, workflow maturity, and AI-agent onboarding readiness. Produces scored health reports with actionable recommendations. Like Hephaestus inspecting the readiness of each artifact before it leaves the forge, this skill ensures every project meets the standards required for effective AI-assisted development.
context:
  primary_domain: engineering
  supporting_domains:
    - documentation
    - testing
  memory:
    skill_memory: project-health
    scopes:
      - health_history
      - improvement_tracking
tags:
  - planning
  - workflow
  - auditing
  - readiness
  - health
triggers:
  - AI readability
  - agent readiness
  - context auditor
  - workflow validator
---

# Project Health Auditor

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 9-step workflow outlined in this document MUST be followed in exact order for EVERY project health audit. Skipping steps or deviating from the procedure will result in incomplete or inaccurate health assessments. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Audit scenarios with sample health reports
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("project-health", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Audit Focus Areas

Project health auditing evaluates 3 critical dimensions across 7 focus areas:

1. **Documentation Completeness**: Assess README, CONTRIBUTING, API docs, architecture docs, and inline documentation coverage
2. **Workflow Maturity**: Evaluate CI/CD pipelines, test infrastructure, dependency management, and deployment practices
3. **AI-Agent Readiness**: Score the project's preparedness for AI-assisted development — CLAUDE.md quality, structure discoverability, context file accuracy
4. **Configuration Hygiene**: Check for consistent config file patterns, environment documentation, and secret management
5. **Test Infrastructure**: Evaluate test coverage, test framework configuration, and testing conventions
6. **Dependency Health**: Assess lock file presence, dependency freshness, and security audit configuration
7. **Onboarding Quality**: Score how quickly a new developer or AI agent can become productive

**Note**: The skill produces a scored report with specific, actionable recommendations. It does not modify project files unless explicitly requested.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Identify the project root directory from the current working directory or user input
2. Detect the project type and primary framework:
   - Language(s) used (check `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.)
   - Framework(s) in use (React, Django, Spring, etc.)
   - Build system (npm, poetry, gradle, make, etc.)
3. Gather a comprehensive list of documentation and configuration files:
   - `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `LICENSE`
   - `docs/` directory contents
   - CI/CD configurations (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, etc.)
   - Test configuration files (`jest.config.*`, `pytest.ini`, `vitest.config.*`, etc.)
   - Dependency files (`package-lock.json`, `poetry.lock`, `go.sum`, etc.)
   - Git hooks (`.husky/`, `.pre-commit-config.yaml`)
4. Note the overall project structure and module organization

**DO NOT PROCEED WITHOUT IDENTIFYING PROJECT TYPE AND FILE INVENTORY**

### ⚠️ STEP 2: Load Memory (REQUIRED)

**YOU MUST:**
1. Identify the project name from the repository root or ask the user
2. Use `memoryStore.getSkillMemory("project-health", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
3. If memory exists, review previous health scores and improvement tracking:
   - Compare current state against historical baselines
   - Check which previous recommendations were addressed
   - Note score trends (improving, declining, stable)
4. **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from other skill executions
5. If no memory exists, you will create it after generating the report

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

**YOU MUST:**
1. Load engineering domain context via `contextProvider.getIndex("engineering")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
2. Load supporting context for documentation standards
3. If the project uses specific technologies, load relevant domain context:
   - Python projects: `contextProvider.getIndex("python")`
   - JavaScript/TypeScript projects: `contextProvider.getIndex("javascript")`
   - Infrastructure projects: `contextProvider.getIndex("devops")`
4. Apply cross-domain triggers as defined in the [Cross-Domain Matrix](../../context/cross_domain.md)

**DO NOT PROCEED WITHOUT LOADING RELEVANT CONTEXT**

### ⚠️ STEP 4: Audit Documentation Health (REQUIRED)

**YOU MUST evaluate each documentation area and assign a score (0-100):**

1. **README.md Quality** (0-25 points):
   - Present and non-empty (5 pts)
   - Contains project description and purpose (5 pts)
   - Includes installation/setup instructions (5 pts)
   - Has usage examples or quick start guide (5 pts)
   - Includes contributing, license, and badge information (5 pts)

2. **CLAUDE.md Presence and Accuracy** (0-25 points):
   - File exists (10 pts)
   - Contains accurate build/test/lint commands (5 pts)
   - Documents project structure and conventions (5 pts)
   - Includes relevant context for AI agent consumption (5 pts)

3. **CONTRIBUTING.md** (0-15 points):
   - File exists with development setup instructions (5 pts)
   - Documents coding standards and conventions (5 pts)
   - Describes PR process and review expectations (5 pts)

4. **API Documentation** (0-15 points):
   - Public APIs documented (endpoints, functions, interfaces) (5 pts)
   - Includes request/response examples (5 pts)
   - Error codes and edge cases documented (5 pts)

5. **Architecture Documentation** (0-10 points):
   - High-level architecture described (5 pts)
   - Module boundaries and dependencies documented (5 pts)

6. **Inline Documentation Coverage** (0-10 points):
   - Public functions/methods have docstrings or JSDoc (5 pts)
   - Complex logic has explanatory comments (5 pts)

**Total Documentation Score: 0-100**

**DO NOT PROCEED WITHOUT SCORING ALL DOCUMENTATION AREAS**

### ⚠️ STEP 5: Audit Workflow Health (REQUIRED)

**YOU MUST evaluate each workflow area and assign a score (0-100):**

1. **CI/CD Configuration** (0-30 points):
   - CI pipeline configuration present (10 pts)
   - Pipeline runs tests automatically (5 pts)
   - Pipeline includes linting/formatting checks (5 pts)
   - Pipeline includes security scanning (5 pts)
   - Pipeline is well-documented or self-explanatory (5 pts)

2. **Test Coverage and Infrastructure** (0-30 points):
   - Test framework configured and functional (10 pts)
   - Tests exist for core functionality (10 pts)
   - Test coverage measurement configured (5 pts)
   - Test conventions documented or discoverable (5 pts)

3. **Dependency Management** (0-20 points):
   - Lock file present and committed (10 pts)
   - Dependencies are reasonably up-to-date (5 pts)
   - Security audit tool configured (e.g., `npm audit`, `safety`, `dependabot`) (5 pts)

4. **Git Hooks and Pre-commit** (0-10 points):
   - Pre-commit hooks configured (5 pts)
   - Hooks enforce linting, formatting, or commit conventions (5 pts)

5. **Deployment Documentation** (0-10 points):
   - Deployment process documented (5 pts)
   - Environment configuration documented (5 pts)

**Total Workflow Score: 0-100**

**DO NOT PROCEED WITHOUT SCORING ALL WORKFLOW AREAS**

### ⚠️ STEP 6: Audit AI-Agent Readiness (REQUIRED)

**YOU MUST evaluate each AI-readiness area and assign a score (0-100):**

1. **CLAUDE.md Quality for Agent Context** (0-30 points):
   - File exists with meaningful content (10 pts)
   - Build, test, and lint commands are accurate and runnable (10 pts)
   - Project-specific conventions and gotchas documented (5 pts)
   - File is concise and well-structured for quick parsing (5 pts)

2. **Project Structure Clarity** (0-20 points):
   - Directory structure is logical and discoverable (10 pts)
   - Clear separation of concerns (source, tests, config, docs) (5 pts)
   - Naming conventions are consistent and intuitive (5 pts)

3. **Command and Skill Discoverability** (0-20 points):
   - Available scripts/commands documented (e.g., `scripts` in `package.json`) (10 pts)
   - Development workflow is clear (how to build, test, run) (5 pts)
   - Common tasks are scriptable or documented (5 pts)

4. **Context File Quality** (0-15 points):
   - Configuration files are well-commented or self-documenting (5 pts)
   - Environment variables documented with descriptions (5 pts)
   - Example configurations provided (`.env.example`, etc.) (5 pts)

5. **Agent Onboarding Readiness** (0-15 points):
   - An AI agent can become productive within minutes of reading docs (5 pts)
   - No tribal knowledge required — everything needed is written down (5 pts)
   - Error messages and logs are descriptive enough for agent debugging (5 pts)

**Total AI-Readiness Score: 0-100**

**DO NOT PROCEED WITHOUT SCORING ALL AI-READINESS AREAS**

### ⚠️ STEP 7: Generate Health Report (REQUIRED)

**YOU MUST produce a scored report with the following structure:**

1. **Executive Summary**: One-paragraph overview of project health
2. **Score Card**:
   | Category | Score | Grade |
   |----------|-------|-------|
   | Documentation | X/100 | A/B/C/D/F |
   | Workflow | X/100 | A/B/C/D/F |
   | AI-Readiness | X/100 | A/B/C/D/F |
   | **Overall** | **X/100** | **A/B/C/D/F** |

   **Grading scale**: A (90-100), B (75-89), C (60-74), D (40-59), F (0-39)
   **Overall score**: Weighted average — Documentation (35%), Workflow (35%), AI-Readiness (30%)

3. **Detailed Breakdown**: Per-category scoring with justification for each sub-score
4. **Recommendations**: Prioritized list of specific, actionable improvements:
   - 🔴 **Critical** (Score impact: +10 or more)
   - 🟡 **Important** (Score impact: +5 to +9)
   - 🟢 **Nice to have** (Score impact: +1 to +4)
5. **Trend Analysis** (if historical data available): Score comparison with previous audits

**DO NOT GENERATE VAGUE OR GENERIC RECOMMENDATIONS**

### ⚠️ STEP 8: Generate Output (REQUIRED)

**YOU MUST:**
1. Save the health report to `/claudedocs/` directory
2. Use the output naming convention: `project_health_{project-name}.md`
3. Include a machine-readable summary block at the top of the report for future parsing:
   ```
   <!-- HEALTH_SCORES: doc=XX workflow=XX ai=XX overall=XX date=YYYY-MM-DD -->
   ```
4. Confirm the output was written successfully

**DO NOT SKIP OUTPUT GENERATION**

### ⚠️ STEP 9: Update Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.update(layer="skill-specific", skill="project-health", project="{project-name}", ...)` to store:
   - **health_history.md**: Append current scores with date, per-category breakdown, and overall grade
   - **improvement_tracking.md**: Log new recommendations and update status of previously tracked recommendations
2. If this is the first audit, create both memory files with initial data
3. If previous memory exists, append to history and reconcile improvement tracking

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY project health audit, verify:
- [ ] Step 1: Project root identified, project type detected, file inventory gathered
- [ ] Step 2: Project memory checked via `memoryStore.getSkillMemory()` and historical data reviewed
- [ ] Step 3: Engineering and supporting domain context loaded via `contextProvider.getIndex()`
- [ ] Step 4: Documentation health audited with per-area scoring (0-100)
- [ ] Step 5: Workflow health audited with per-area scoring (0-100)
- [ ] Step 6: AI-agent readiness audited with per-area scoring (0-100)
- [ ] Step 7: Health report generated with score card, breakdown, and prioritized recommendations
- [ ] Step 8: Output saved to `/claudedocs/` with machine-readable summary block
- [ ] Step 9: Memory updated with health history and improvement tracking

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE HEALTH AUDIT**

---

## Output File Naming Convention

**Format**: `project_health_{project-name}.md`

Where:
- `{project-name}` = Name derived from repository root or user input, lowercased and hyphenated

**Examples**:
- `project_health_my-api.md`
- `project_health_forge.md`
- `project_health_e-commerce-platform.md`

---

## Further Reading

Refer to official documentation and standards:
- **Documentation Standards**:
  - Diátaxis Framework: https://diataxis.fr/
  - Write the Docs: https://www.writethedocs.org/guide/
- **CI/CD Best Practices**:
  - GitHub Actions Documentation: https://docs.github.com/en/actions
  - Continuous Delivery: https://continuousdelivery.com/
- **AI-Agent Readiness**:
  - CLAUDE.md Best Practices: See `context/documentation/` domain
  - Anthropic Claude Documentation: https://docs.anthropic.com/

---

## Version History

- v1.0.0 (2025-01-XX): Initial release
  - Mandatory 9-step workflow for project health auditing
  - Three-category scoring: Documentation, Workflow, AI-Readiness
  - Weighted overall score with letter grades
  - Prioritized recommendations with score impact estimates
  - Memory integration for historical tracking and trend analysis
  - Interface-based patterns (ContextProvider + MemoryStore)
