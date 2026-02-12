# Documentation Workflow Examples

This file contains example scenarios demonstrating how to use the docs-workflow skill to create, maintain, and audit project documentation.

---

## Example 1: Initializing Documentation for a New Project

### Scenario
Developer just created a new Python FastAPI project and wants to set up proper documentation from scratch.

### User Prompt
```
/docs-init
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Command: `/docs-init` — full documentation initialization
- Project type detected: Python (FastAPI) via `pyproject.toml` and `main.py`
- Current state: No `CLAUDE.md`, basic auto-generated `README.md`, no `docs/` directory
- Framework: FastAPI with SQLAlchemy, Alembic migrations

**Step 2 - Load Memory**:
- Check `memoryStore.getSkillMemory("docs-workflow", "my-fastapi-app")` for prior conventions
- No prior memory found (first use on this project)

**Step 3 - Load Context**:
- Load engineering domain context via `contextProvider`
- Load Python project documentation templates
- Load output naming conventions

**Step 4 - Assess Documentation State**:
- `CLAUDE.md`: ❌ Does not exist
- `README.md`: ⚠️ Exists but contains only auto-generated placeholder content
- `docs/`: ❌ Does not exist
- Documentation health score: **15/100** (critical — nearly no documentation)

**Step 5 - Execute `/docs-init`**:

Created `CLAUDE.md`:
```markdown
# CLAUDE.md — my-fastapi-app

## Build & Run
- Install: `pip install -e ".[dev]"`
- Run: `uvicorn app.main:app --reload`
- Test: `pytest`
- Lint: `ruff check .`

## Architecture
- FastAPI application in `app/`
- SQLAlchemy models in `app/models/`
- Alembic migrations in `migrations/`
- API routes in `app/routes/`

## Conventions
- Use type hints on all function signatures
- Async endpoints preferred
- Pydantic models for request/response schemas
```

Created `README.md` with sections:
- Project description, prerequisites, installation, usage, API documentation, testing, contributing, license

Created `docs/` structure:
```
docs/
├── architecture.md
├── api-reference.md
├── deployment.md
└── development-guide.md
```

**Step 6 - Generate Output**:
Saved report to `/claudedocs/docs_workflow_my-fastapi-app_2026-03-15.md`

**Step 7 - Update Memory**:
- Stored: Python/FastAPI project conventions
- Stored: Documentation structure template used
- Stored: Initial health score baseline (15 → 85 after init)

### Result
```
🔱 Documentation Initialized — my-fastapi-app

Created:
  ✅ CLAUDE.md — Build commands, architecture, conventions
  ✅ README.md — Full project documentation (7 sections)
  ✅ docs/ — 4 documentation files

Health: 15/100 → 85/100
Remaining: API reference needs endpoint details, deployment guide needs environment config
```

---

## Example 2: Updating Documentation After Major Changes

### Scenario
Developer completed a major refactor adding authentication, new API endpoints, and database migrations. Documentation is now out of date.

### User Prompt
```
/docs-update
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Command: `/docs-update` — refresh existing documentation
- Project type: Python (FastAPI) — previously initialized
- Current state: `CLAUDE.md`, `README.md`, and `docs/` all exist but are outdated
- Recent changes detected: new `app/auth/` module, 3 new route files, 2 new migrations

**Step 2 - Load Memory**:
- Check `memoryStore.getSkillMemory("docs-workflow", "my-fastapi-app")`
- Found: Previous documentation conventions, structure template, last update date
- Last documentation update: 2026-02-01 (6 weeks ago)

**Step 3 - Load Context**:
- Load engineering domain context
- Load project-specific documentation patterns from memory

**Step 4 - Assess Documentation State**:
- `CLAUDE.md`: ⚠️ Missing auth module in architecture, missing new test commands
- `README.md`: ⚠️ Setup instructions don't mention `AUTH_SECRET` env var, API section incomplete
- `docs/api-reference.md`: ⚠️ Missing 3 new endpoints (`/auth/login`, `/auth/register`, `/auth/refresh`)
- `docs/architecture.md`: ⚠️ No mention of authentication layer
- Documentation health score: **52/100** (degraded — significant gaps after refactor)

**Step 5 - Execute `/docs-update`**:

Updated `CLAUDE.md`:
```diff
## Architecture
  - FastAPI application in `app/`
  - SQLAlchemy models in `app/models/`
  - Alembic migrations in `migrations/`
  - API routes in `app/routes/`
+ - Authentication in `app/auth/` (JWT-based)
+
+ ## Environment Variables
+ - `AUTH_SECRET` — JWT signing secret (required)
+ - `AUTH_TOKEN_EXPIRY` — Token expiry in minutes (default: 30)
```

Updated `README.md`:
- Added `AUTH_SECRET` to prerequisites and setup sections
- Added authentication endpoints to API overview
- Updated installation steps with new dependency

Updated `docs/api-reference.md`:
- Added `/auth/login`, `/auth/register`, `/auth/refresh` endpoint documentation
- Added authentication headers section

Updated `docs/architecture.md`:
- Added authentication layer diagram and description

**Step 6 - Generate Output**:
Saved report to `/claudedocs/docs_workflow_my-fastapi-app_2026-03-15.md`

**Step 7 - Update Memory**:
- Updated: Documentation health trend (85 → 52 → 88)
- Stored: Auth module documentation patterns
- Stored: Environment variable documentation convention

### Result
```
🔱 Documentation Updated — my-fastapi-app

Modified:
  ✏️ CLAUDE.md — Added auth module, environment variables
  ✏️ README.md — Updated setup, prerequisites, API overview
  ✏️ docs/api-reference.md — Added 3 auth endpoints
  ✏️ docs/architecture.md — Added authentication layer

Health: 52/100 → 88/100
⚠️ Manual review suggested: docs/deployment.md may need auth config for production
```

---

## Example 3: Auditing Documentation Health

### Scenario
Tech lead wants to check the overall documentation health of the project before a release.

### User Prompt
```
/docs
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Command: `/docs` — documentation status and health audit
- Project type: Python (FastAPI) — well-established project
- Mode: Read-only audit, no modifications

**Step 2 - Load Memory**:
- Check `memoryStore.getSkillMemory("docs-workflow", "my-fastapi-app")`
- Found: Documentation history with 3 prior updates, health trend data
- Last update: 2026-03-15

**Step 3 - Load Context**:
- Load engineering domain context for documentation standards
- Load documentation completeness criteria

**Step 4 - Assess Documentation State**:

Comprehensive audit performed:

| File | Status | Completeness | Freshness |
|------|--------|-------------|-----------|
| `CLAUDE.md` | ✅ Exists | 90% | Current |
| `README.md` | ✅ Exists | 85% | Current |
| `docs/architecture.md` | ✅ Exists | 80% | Current |
| `docs/api-reference.md` | ⚠️ Exists | 70% | Stale (new endpoints since last update) |
| `docs/deployment.md` | ⚠️ Exists | 40% | Stale (missing container config) |
| `docs/development-guide.md` | ✅ Exists | 75% | Current |
| `CONTRIBUTING.md` | ❌ Missing | — | — |
| `CHANGELOG.md` | ❌ Missing | — | — |

**Step 5 - Execute `/docs`**:

Generated health summary (no files modified):
```
🔱 Documentation Health — my-fastapi-app

Overall Score: 72/100

📊 Coverage:
  ✅ CLAUDE.md ................. 90%  (current)
  ✅ README.md ................. 85%  (current)
  ✅ docs/architecture.md ...... 80%  (current)
  ⚠️ docs/api-reference.md .... 70%  (stale — 2 new endpoints undocumented)
  ⚠️ docs/deployment.md ....... 40%  (stale — missing container/k8s config)
  ✅ docs/development-guide.md . 75%  (current)
  ❌ CONTRIBUTING.md ........... missing
  ❌ CHANGELOG.md .............. missing

📈 Health Trend: 15 → 85 → 52 → 88 → 72

🔧 Recommendations:
  1. [HIGH] Update docs/api-reference.md — 2 new endpoints need documentation
  2. [HIGH] Update docs/deployment.md — Add container and Kubernetes configuration
  3. [MEDIUM] Create CONTRIBUTING.md — Important for open-source readiness
  4. [LOW] Create CHANGELOG.md — Track release history for users
  5. [LOW] Add code examples to docs/development-guide.md

💡 Run /docs-update to automatically address items 1 and 2
```

**Step 6 - Generate Output**:
Saved report to `/claudedocs/docs_workflow_my-fastapi-app_2026-03-15.md`

**Step 7 - Update Memory**:
- Updated: Health score history with current audit
- Stored: Documentation gaps identified for future reference

### Result
Documentation health dashboard displayed with actionable recommendations prioritized by impact. No files were modified — audit is read-only.

---

## Summary

The docs-workflow skill supports three primary documentation workflows:

1. **Initialize** (`/docs-init`) — Create documentation structure from scratch with smart templates
2. **Update** (`/docs-update`) — Refresh existing documentation to match current project state
3. **Audit** (`/docs`) — Read-only health check with coverage metrics and recommendations

Additionally, `/docs-claude` focuses specifically on generating or refreshing `CLAUDE.md` with project conventions, build commands, and architecture notes.
