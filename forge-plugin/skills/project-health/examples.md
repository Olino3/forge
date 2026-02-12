# Project Health Auditor Examples

This file contains example scenarios demonstrating how to use the project-health skill to audit project documentation, workflows, and AI-agent readiness.

---

## Example 1: Well-Maintained Project (High Scores)

### Scenario
A mature Python API project with comprehensive documentation, robust CI/CD, and full AI-agent readiness.

### User Prompt
```
Audit the health of this project
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Project root: /workspace/payments-api
Type: Python (FastAPI)
Framework: FastAPI 0.109+
Build system: Poetry

Files detected:
- README.md ✅
- CONTRIBUTING.md ✅
- CLAUDE.md ✅
- LICENSE ✅
- docs/architecture.md ✅
- docs/api-reference.md ✅
- .github/workflows/ci.yml ✅
- .github/workflows/deploy.yml ✅
- .pre-commit-config.yaml ✅
- pyproject.toml + poetry.lock ✅
- pytest.ini ✅
- .env.example ✅
```

**Step 2 - Load Memory**:
- Previous audit found: Overall score was 82/100 (3 months ago)
- Two recommendations were pending: add API error code docs, add deployment runbook

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded Python domain context for framework-specific checks

**Step 4 - Documentation Health** (Score: 92/100):
- README.md: 25/25 — Comprehensive with badges, installation, usage examples, and contributing link
- CLAUDE.md: 22/25 — Present with accurate commands; minor gap in documenting test fixtures convention
- CONTRIBUTING.md: 15/15 — Full development setup, coding standards, and PR process
- API Documentation: 15/15 — OpenAPI spec auto-generated, error codes now documented (previously missing)
- Architecture: 10/10 — Clear architecture doc with diagrams
- Inline docs: 5/10 — Most public functions documented, some utility modules lack docstrings

**Step 5 - Workflow Health** (Score: 90/100):
- CI/CD: 28/30 — CI runs tests, linting, and type checking; missing security scanning step
- Tests: 27/30 — pytest configured with 85% coverage, good conventions; no integration test docs
- Dependencies: 20/20 — poetry.lock committed, dependencies current, dependabot configured
- Git hooks: 10/10 — pre-commit with ruff, mypy, and commit message validation
- Deployment: 5/10 — Deployment workflow exists but runbook still not created

**Step 6 - AI-Agent Readiness** (Score: 88/100):
- CLAUDE.md quality: 27/30 — Accurate build/test commands, conventions documented; missing test fixture guidance
- Structure clarity: 18/20 — Clean separation, logical naming, clear module boundaries
- Discoverability: 18/20 — Scripts documented in pyproject.toml, Makefile provides common tasks
- Context files: 13/15 — .env.example present, well-commented config; one undocumented env var
- Onboarding: 12/15 — Agent can be productive quickly; some tribal knowledge around migration scripts

**Step 7 - Health Report**:

### Generated Report

```markdown
<!-- HEALTH_SCORES: doc=92 workflow=90 ai=88 overall=90 date=2025-04-15 -->

# Project Health Report: payments-api

## Executive Summary

The payments-api project demonstrates excellent overall health with strong
documentation, mature workflows, and solid AI-agent readiness. Score improved
from 82 to 90 since last audit. Two of two previous recommendations addressed.

## Score Card

| Category | Score | Grade |
|----------|-------|-------|
| Documentation | 92/100 | A |
| Workflow | 90/100 | A |
| AI-Readiness | 88/100 | B |
| **Overall** | **90/100** | **A** |

## Recommendations

🟡 **Add security scanning to CI pipeline** (Workflow +2)
   Add a `safety check` or `pip-audit` step to the CI workflow.

🟡 **Document test fixture conventions in CLAUDE.md** (AI-Readiness +3)
   Add a section explaining shared fixtures and factory patterns.

🟢 **Add docstrings to utility modules** (Documentation +3)
   Files in `src/utils/` lack docstrings on public functions.

🟢 **Create deployment runbook** (Workflow +5)
   Document step-by-step deployment process for manual fallback.

## Trend Analysis

| Date | Doc | Workflow | AI-Ready | Overall |
|------|-----|----------|----------|---------|
| 2025-01-15 | 78 | 80 | 72 | 77 |
| 2025-04-15 | 92 | 90 | 88 | 90 |
| **Change** | **+14** | **+10** | **+16** | **+13** |
```

**Step 8 - Output**:
File: `/claudedocs/project_health_payments-api.md`

**Step 9 - Memory Update**:
- Appended scores to `health_history.md`
- Updated `improvement_tracking.md`: marked 2 previous items complete, added 4 new recommendations

---

## Example 2: Project Lacking AI-Readiness

### Scenario
A Node.js project with decent documentation and CI but no CLAUDE.md, poor structure descriptions, and undocumented conventions.

### User Prompt
```
Check how ready this project is for AI-assisted development
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Project root: /workspace/invoice-service
Type: TypeScript (Node.js)
Framework: Express.js
Build system: npm

Files detected:
- README.md ✅
- CONTRIBUTING.md ❌ (missing)
- CLAUDE.md ❌ (missing)
- LICENSE ✅
- .github/workflows/test.yml ✅
- package.json + package-lock.json ✅
- jest.config.ts ✅
- .env.example ❌ (missing)
```

**Step 2 - Load Memory**:
- No previous memory found; first audit for this project

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded JavaScript/TypeScript domain context

**Step 4 - Documentation Health** (Score: 28/100):
- README.md: 15/25 — Has description and install steps but no usage examples or badges
- CLAUDE.md: 0/25 — File does not exist
- CONTRIBUTING.md: 0/15 — File does not exist
- API Documentation: 8/15 — Partial Swagger setup, missing error codes and many endpoints undocumented
- Architecture: 5/10 — Brief mention in README, no dedicated architecture doc
- Inline docs: 0/10 — Some JSDoc on controllers, none on services or utilities

**Step 5 - Workflow Health** (Score: 62/100):
- CI/CD: 20/30 — GitHub Actions runs tests; no linting or security steps
- Tests: 22/30 — Jest configured, moderate coverage (~60%), but no test conventions doc
- Dependencies: 15/20 — Lock file committed, some outdated deps, no audit configured
- Git hooks: 0/10 — No pre-commit or husky configuration
- Deployment: 5/10 — Docker compose file exists but no deployment documentation

**Step 6 - AI-Agent Readiness** (Score: 25/100):
- CLAUDE.md quality: 0/30 — File does not exist; agent has no project-specific context
- Structure clarity: 10/20 — Flat `src/` directory with inconsistent naming; no clear module boundaries
- Discoverability: 5/20 — npm scripts exist but are minimal (`start`, `test` only); no `build`, `lint`, or `dev` scripts
- Context files: 5/15 — No `.env.example`, config is hardcoded or undocumented environment vars
- Onboarding: 5/15 — Agent would struggle significantly; many implicit conventions, no written standards

**Step 7 - Health Report**:

### Generated Report

```markdown
<!-- HEALTH_SCORES: doc=28 workflow=62 ai=25 overall=39 date=2025-04-15 -->

# Project Health Report: invoice-service

## Executive Summary

The invoice-service has foundational CI/CD and testing but significant gaps in
documentation and AI-agent readiness. The absence of CLAUDE.md, CONTRIBUTING.md,
and structured project documentation means AI agents cannot effectively assist
with this project. Immediate action on documentation and AI-readiness is recommended.

## Score Card

| Category | Score | Grade |
|----------|-------|-------|
| Documentation | 28/100 | F |
| Workflow | 62/100 | C |
| AI-Readiness | 25/100 | F |
| **Overall** | **39/100** | **F** |

## Recommendations

🔴 **Create CLAUDE.md with build/test/lint commands** (AI-Readiness +20, Documentation +10)
   Include project purpose, tech stack, directory structure, and all
   runnable commands. This is the single highest-impact improvement.

🔴 **Create .env.example with all environment variables** (AI-Readiness +5)
   Document every required environment variable with descriptions
   and example values.

🔴 **Add CONTRIBUTING.md** (Documentation +15)
   Document development setup, coding standards, and PR process.

🟡 **Add linting to CI and npm scripts** (Workflow +5, AI-Readiness +5)
   Configure ESLint, add `lint` script, and add CI step.

🟡 **Restructure src/ with clear module boundaries** (AI-Readiness +5)
   Organize into `controllers/`, `services/`, `models/`, `middleware/`.

🟡 **Configure pre-commit hooks with husky** (Workflow +5)
   Add lint-staged for automated formatting and linting on commit.

🟢 **Add usage examples to README** (Documentation +5)
   Include curl examples for key API endpoints.

🟢 **Document API error codes in Swagger** (Documentation +5)
   Complete the OpenAPI spec with error responses.
```

**Step 8 - Output**:
File: `/claudedocs/project_health_invoice-service.md`

**Step 9 - Memory Update**:
- Created `health_history.md` with initial scores
- Created `improvement_tracking.md` with 8 recommendations and pending status

---

## Example 3: Project with Workflow Gaps

### Scenario
A Go project with good documentation and a solid CLAUDE.md but no CI/CD, missing tests, and no dependency security auditing.

### User Prompt
```
Run a project health audit — I want to know where our workflow gaps are
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Project root: /workspace/data-pipeline
Type: Go 1.22
Framework: Standard library + Chi router
Build system: go mod

Files detected:
- README.md ✅
- CONTRIBUTING.md ✅
- CLAUDE.md ✅
- LICENSE ✅
- docs/architecture.md ✅
- docs/api.md ✅
- .github/workflows/ ❌ (directory missing)
- go.mod + go.sum ✅
- Makefile ✅
- .pre-commit-config.yaml ❌ (missing)
- .env.example ✅
```

**Step 2 - Load Memory**:
- No previous memory found; first audit for this project

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded Go-specific context patterns

**Step 4 - Documentation Health** (Score: 85/100):
- README.md: 23/25 — Thorough README with build instructions and examples; missing badges
- CLAUDE.md: 23/25 — Accurate `go build`, `go test`, `make lint` commands; documents conventions well
- CONTRIBUTING.md: 12/15 — Good setup guide and coding standards; missing PR review expectations
- API Documentation: 12/15 — Endpoints documented with examples; some newer endpoints missing
- Architecture: 10/10 — Dedicated architecture doc with data flow diagrams
- Inline docs: 5/10 — Exported functions have godoc comments; internal packages sparse

**Step 5 - Workflow Health** (Score: 28/100):
- CI/CD: 0/30 — No CI/CD configuration exists; all testing is manual
- Tests: 10/30 — Go test files exist for 2 of 8 packages; no coverage measurement; no test conventions
- Dependencies: 13/20 — go.sum committed; dependencies moderately current; no `govulncheck` or security audit
- Git hooks: 0/10 — No pre-commit configuration
- Deployment: 5/10 — Makefile has `deploy` target but no documentation of what it does or requires

**Step 6 - AI-Agent Readiness** (Score: 78/100):
- CLAUDE.md quality: 25/30 — Strong CLAUDE.md with build and test commands; could add more about test patterns
- Structure clarity: 18/20 — Clean Go project layout following standard conventions
- Discoverability: 15/20 — Makefile documents available commands; some targets undocumented
- Context files: 10/15 — .env.example present; some config options only in code comments
- Onboarding: 10/15 — Good docs but lack of tests makes agent validation difficult

**Step 7 - Health Report**:

### Generated Report

```markdown
<!-- HEALTH_SCORES: doc=85 workflow=28 ai=78 overall=63 date=2025-04-15 -->

# Project Health Report: data-pipeline

## Executive Summary

The data-pipeline project has strong documentation and good AI-agent readiness
but critically lacks workflow infrastructure. No CI/CD pipeline exists, test
coverage is minimal, and there are no automated quality gates. The documentation
investment is undermined by the inability to validate changes automatically.

## Score Card

| Category | Score | Grade |
|----------|-------|-------|
| Documentation | 85/100 | B |
| Workflow | 28/100 | F |
| AI-Readiness | 78/100 | B |
| **Overall** | **63/100** | **C** |

## Recommendations

🔴 **Create GitHub Actions CI pipeline** (Workflow +20)
   Add `.github/workflows/ci.yml` with `go build`, `go test ./...`,
   `golangci-lint run`, and `go vet` steps. This is the single most
   impactful improvement for the project.

🔴 **Add tests for untested packages** (Workflow +10)
   Six of eight packages have zero test files. Prioritize the core
   pipeline and handler packages.

🔴 **Configure govulncheck for dependency security** (Workflow +5)
   Add `govulncheck ./...` to Makefile and future CI pipeline.

🟡 **Add test coverage measurement** (Workflow +5)
   Configure `go test -coverprofile` and set a minimum coverage target.

🟡 **Configure pre-commit hooks** (Workflow +5)
   Add `.pre-commit-config.yaml` with `golangci-lint`, `gofmt`, and
   `go vet` hooks to catch issues before commit.

🟡 **Document the deploy Makefile target** (Workflow +3, Documentation +2)
   Add a deployment runbook explaining prerequisites, environment
   requirements, and rollback procedures.

🟢 **Add godoc comments to internal packages** (Documentation +3)
   Internal packages lack documentation; add package-level and
   function-level comments.

🟢 **Add CI badges to README** (Documentation +2)
   Once CI is configured, add build status badges.
```

**Step 8 - Output**:
File: `/claudedocs/project_health_data-pipeline.md`

**Step 9 - Memory Update**:
- Created `health_history.md` with initial scores
- Created `improvement_tracking.md` with 8 recommendations and pending status

---

## Summary of Audit Scenarios

1. **Well-maintained project** — High scores across all categories; recommendations are refinements, not fundamentals
2. **Missing AI-readiness** — Decent foundation but AI agents cannot work effectively without CLAUDE.md and structured context
3. **Workflow gaps** — Strong documentation undermined by lack of CI/CD, testing, and automated quality gates

## Best Practices

- Always run a full audit across all three categories, even if the user asks about only one area
- Provide specific, actionable recommendations with estimated score impact
- Use memory to track improvement over time — trends matter more than single scores
- Prioritize recommendations by impact: critical items first, nice-to-haves last
- Include the machine-readable summary block for automated trend tracking
- When previous audit data exists, always include a trend comparison table
