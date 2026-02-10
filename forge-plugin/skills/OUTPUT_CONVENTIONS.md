# Output File Naming Conventions

Central reference for consistent output file naming across all Forge skills.

## Convention

**Pattern**: `{skill-name}_{project}_{YYYY-MM-DD}[_qualifier].md`

**Location**: `/claudedocs/` directory (created at project root if it doesn't exist)

## Naming by Skill Type

| Skill Type | Pattern | Example |
|---|---|---|
| Code review | `{lang}-code-review_{project}_{date}.md` | `python-code-review_myapi_2026-02-10.md` |
| Git diff | `get-git-diff_{project}_{short1}_{short2}.md` | `get-git-diff_myapi_abc1234_def5678.md` |
| Test generation | `generate-{lang}-unit-tests_{project}_{date}.md` | `generate-python-unit-tests_myapi_2026-02-10.md` |
| Azure Functions | `generate-azure-functions_{project}_{date}.md` | `generate-azure-functions_myapi_2026-02-10.md` |
| Azure Pipelines | `generate-azure-pipelines_{project}_{date}.md` | `generate-azure-pipelines_myapi_2026-02-10.md` |
| Azure Bicep | `generate-azure-bicep_{project}_{date}.md` | `generate-azure-bicep_myapi_2026-02-10.md` |
| Tilt environment | `generate-tilt-dev-environment_{project}_{date}.md` | `generate-tilt-dev-environment_myapi_2026-02-10.md` |
| Mock service | `generate-mock-service_{project}_{date}.md` | `generate-mock-service_myapi_2026-02-10.md` |
| Schema analysis | `{type}-schema-analysis_{project}_{date}.md` | `database-schema-analysis_myapi_2026-02-10.md` |
| CLI testing | `test-cli-tools_{project}_{date}.md` | `test-cli-tools_mycli_2026-02-10.md` |
| Dependency mgmt | `python-dependency-management_{project}_{date}.md` | `python-dependency-management_myapi_2026-02-10.md` |

## Qualifier Rules

Use a qualifier suffix when multiple outputs of the same type are generated on the same day:

- Sequential: `_1`, `_2`, `_3`
- Scope-based: `_auth`, `_api`, `_models`
- Focus-based: `_security`, `_performance`

Example: `python-code-review_myapi_2026-02-10_auth.md`

## Project Name Detection

Determine project name in this priority order:

1. Git remote repository name (from `git remote get-url origin`)
2. Root directory name of the repository
3. Current working directory name
4. User-provided name

Normalize: lowercase, hyphens for spaces, strip special characters.

---

*Last Updated: 2026-02-10*
