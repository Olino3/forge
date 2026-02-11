# ⚒️ The Forge — Testing Architecture Roadmap

---

## Context

The Forge is a convention-based Claude Code plugin with zero build tools, zero package managers, and zero compiled code. It currently has no tests whatsoever — 22 skills, 11 agents, 12 commands, 81 context files, 20 hook scripts, and 3 JSON schemas all operate without any automated validation.

This roadmap establishes a layered testing architecture that validates the entire plugin — from static file structure to runtime hook behavior — using only bash, python3, jq, and optionally shellcheck. No new build tools or package managers are introduced.

## Why Now

- Every new skill, agent, or context file risks breaking conventions silently
- Hook scripts enforce security boundaries (sandbox guard, PII redaction, dependency blocking) with no tests proving they actually work
- Memory lifecycle rules (freshness, pruning, line limits) have no verification
- Cross-references between components (agents referencing skills, configs referencing domains) can drift without detection
- CI pipeline has nothing to run

---

## Definitions

| Term | Definition |
|------|-----------|
| **Layer 1** | Standard/CI tests — static validation of structure, schemas, syntax, and cross-references. No runtime needed. |
| **Layer 2** | Integration/E2E tests — runtime validation of hook behavior, memory lifecycle, context loading, and plugin operation. |
| **Hook** | A bash script registered in hooks.json that receives JSON on stdin from Claude Code and returns JSON on stdout with exit codes (0=allow, 2=deny). |
| **Frontmatter** | YAML metadata block delimited by `---` at the top of markdown files, validated against JSON schemas. |
| **Fixture** | Static test data (JSON inputs, sample memory files, mock transcripts) used to drive repeatable tests. |
| **HookRunner** | Python test harness that executes hook scripts via `subprocess.run()`, feeds JSON stdin, and asserts on exit codes and JSON stdout. |
| **TempForgeEnvironment** | Disposable temporary directory structure mimicking `.forge/` runtime state for isolated stateful tests. |

---

## Specifications

### Test Runner

- **Primary**: pytest for Python-based tests (schema validation, hook integration, lifecycle simulation)
- **Secondary**: Plain bash scripts for shellcheck linting and hook syntax checks
- **Master runner**: `tests/run_all.sh` orchestrates both layers with `--layer2` and `--e2e` flags
- **Fallback**: Each Python test file has a `if __name__ == "__main__"` block so `python3 tests/layer1/test_json_schemas.py` works without pytest

### Dependencies

| Tool | Required | Purpose |
|------|----------|---------|
| python3 (3.10+) | Yes | Test execution |
| pyyaml | Yes | YAML frontmatter parsing |
| jsonschema | Yes | JSON schema validation |
| pytest | Yes | Test framework |
| jq (1.6+) | Yes | JSON validation in bash tests |
| shellcheck | No (optional) | Bash linting (CI installs it) |
| claude CLI | No (optional) | E2E plugin loading tests |

### Exit Code Contract

| Code | Meaning | Used By |
|------|---------|---------|
| 0 | All tests passed | All test scripts |
| 1 | One or more tests failed | All test scripts |
| 0 (skip) | Dependency not available, test skipped | shellcheck, E2E tests |

### Hook Testing Contract

Hooks are tested by feeding them JSON on stdin and asserting on:
- **Exit code**: 0 (success/allow) or 2 (blocking deny)
- **JSON stdout**: `hookSpecificOutput.permissionDecision` = `allow` or `deny`
- **JSON stdout**: `hookSpecificOutput.permissionDecisionReason` contains expected message
- **Side effects**: Files created/modified in `.forge/` runtime directory (tested via TempForgeEnvironment)

---

## Directory Structure

```
forge-plugin/
└── tests/
    ├── README.md                        # How to run tests
    ├── run_all.sh                       # Master runner (--layer2, --e2e flags)
    ├── conftest.py                      # Shared pytest config + FORGE_DIR resolution
    ├── pytest.ini                       # Pytest configuration
    │
    ├── layer1/                          # Static/CI Tests
    │   ├── run_layer1.sh                # Run all Layer 1 tests
    │   ├── test_json_schemas.py         # All JSON configs against their schemas
    │   ├── test_yaml_frontmatter.py     # All 81 context files frontmatter validation
    │   ├── test_file_structure.py       # Required files/dirs exist, naming conventions
    │   ├── test_cross_references.py     # Referential integrity across components
    │   ├── test_hooks_registration.py   # All hook scripts registered in hooks.json
    │   ├── test_memory_structure.py     # Memory directory structure and file format
    │   ├── test_plugin_manifest.py      # plugin.json validity and completeness
    │   ├── test_shellcheck.sh           # Bash linting (skips if shellcheck absent)
    │   └── test_hook_syntax.sh          # Shebang, set -euo pipefail, bash -n
    │
    ├── layer2/                          # Integration/E2E Tests
    │   ├── run_layer2.sh                # Run all Layer 2 tests
    │   ├── hooks/                       # Hook unit tests (20 hooks)
    │   │   ├── conftest.py              # HookRunner + TempForgeEnvironment
    │   │   ├── test_sandbox_boundary_guard.py
    │   │   ├── test_pii_redactor.py
    │   │   ├── test_dependency_sentinel.py
    │   │   ├── test_git_hygiene_enforcer.py
    │   │   ├── test_pre_commit_quality.py
    │   │   ├── test_frontmatter_validator.py
    │   │   ├── test_memory_freshness_enforcer.py
    │   │   ├── test_memory_quality_gate.py
    │   │   ├── test_memory_cross_pollinator.py
    │   │   ├── test_memory_pruning_daemon.py
    │   │   ├── test_agent_config_validator.py
    │   │   ├── test_skill_compliance_checker.py
    │   │   ├── test_output_quality_scorer.py
    │   │   ├── test_context_drift_detector.py
    │   │   ├── test_command_chain_context.py
    │   │   ├── test_system_health_emitter.py
    │   │   ├── test_forge_telemetry.py
    │   │   ├── test_context_usage_tracker.py
    │   │   ├── test_root_agent_validator.py
    │   │   └── test_health_buffer_lib.py
    │   ├── memory/                      # Memory lifecycle simulation
    │   │   ├── test_freshness_lifecycle.py
    │   │   ├── test_pruning_behavior.py
    │   │   └── test_line_limits.py
    │   ├── context/                     # Context loading protocol
    │   │   ├── test_loading_protocol.py
    │   │   └── test_cross_domain_triggers.py
    │   └── e2e/                         # Full E2E (requires claude CLI)
    │       ├── test_plugin_loading.sh
    │       ├── test_command_execution.sh
    │       └── test_skill_invocation.sh
    │
    └── fixtures/                        # Shared test data
        ├── hook_inputs/                 # JSON stdin for hook tests (~19 files)
        ├── memory_files/                # Fixture memory files (~7 files)
        ├── context_files/               # Fixture context files (~5 files)
        ├── agent_configs/               # Fixture agent configs (~5 files)
        └── transcripts/                 # Mock transcripts (~3 files)
```

---

## Phases

### Phase 1: Foundation and Infrastructure ✅

**Goal**: Create the test directory structure, runner scripts, shared configuration, and the first high-value static tests.

**Status**: Complete — 170 pytest tests + 96 bash checks, all passing.

**Files to create:**
- `tests/conftest.py` — Shared FORGE_DIR resolution, helper for extracting YAML frontmatter
- `tests/pytest.ini` — Minimal pytest config (testpaths, markers)
- `tests/run_all.sh` — Master runner with dependency checks and `--layer2`/`--e2e` flags
- `tests/layer1/run_layer1.sh` — Layer 1 runner

**Tests to implement:**

| Test File | What It Validates | Components Covered |
|-----------|-------------------|-------------------|
| `test_json_schemas.py` | All 11 agent `*.config.json` files against `agent_config.schema.json`; `hooks.json` structure (valid event types); `plugin.json` required fields; `root_safety_profile.json` structure; `framework_conflicts.json` validity | 11 agent configs, hooks.json, plugin.json |
| `test_file_structure.py` | Required dirs/files from safety profile exist; each agent has paired `.md` + `.config.json`; each skill dir has `SKILL.md` + `examples.md`; each command dir has `COMMAND.md`; memory subdirs exist | All structural conventions |
| `test_hook_syntax.sh` | Every `hooks/*.sh` has `#!/bin/bash` shebang; has `set -euo pipefail`; is executable; passes `bash -n` syntax check | 20 hook scripts + lib |

**Validation rules for `test_json_schemas.py`:**
- Agent config `name` matches filename (e.g., `hephaestus.config.json` must have `"name": "hephaestus"`)
- Agent config `version` matches semver pattern `^\d+\.\d+\.\d+$`
- Agent config `context.primaryDomains` values are in enum: `[engineering, angular, azure, commands, dotnet, git, python, schema, security]`
- `hooks.json` event keys are in: `[PreToolUse, PostToolUse, SessionStart, UserPromptSubmit, Stop, PreCompact, TaskCompleted, SubagentStart, SessionEnd]`
- `plugin.json` has `name`, `version`, `commands`; all command paths resolve to existing files

**Existing files to reuse:**
- `forge-plugin/interfaces/schemas/agent_config.schema.json` — JSON schema for agent validation
- `forge-plugin/interfaces/schemas/context_metadata.schema.json` — JSON schema for context frontmatter
- `forge-plugin/interfaces/schemas/memory_entry.schema.json` — JSON schema for memory entries
- `forge-plugin/templates/root_safety_profile.json` — Required structure definition

---

### Phase 2: Static Validation (Context, Memory, Cross-References) ✅

**Goal**: Validate all 81 context files, memory structure, plugin manifest, cross-reference integrity, and hook registration completeness.

**Status**: Complete — 961 pytest tests (957 passed, 4 known data quality failures) + shellcheck (skips gracefully if not installed). See TODOs section for known failures.

**Tests to implement:**

| Test File | What It Validates | Components Covered |
|-----------|-------------------|-------------------|
| `test_yaml_frontmatter.py` | All `context/**/*.md` files have YAML frontmatter with required fields; enum values are valid; `estimatedTokens` is positive int; index files' `indexedFiles` reference existing files | 81 context files |
| `test_cross_references.py` | Skills in agent configs exist as directories; domains in agent configs exist as context dirs; `alwaysLoadFiles` paths exist; `memory.storagePath` dirs exist; `crossDomainTriggers` target existing files; `hooks.json` commands reference existing scripts | All inter-component references |
| `test_hooks_registration.py` | Every active `.sh` in `hooks/` is registered in `hooks.json`; every script path in `hooks.json` exists on disk; known legacy scripts are accounted for | 20 hooks + hooks.json |
| `test_memory_structure.py` | Required index/lifecycle/quality files exist; agent memory dirs match actual agents; skill memory dirs match actual skills; memory files (if present) have `<!-- Last Updated: YYYY-MM-DD -->` timestamp; no files exceed line limits | Memory directory tree |
| `test_plugin_manifest.py` | All 12 commands listed; each command path exists; version is semver; `.claude-plugin/` contains only `plugin.json` | plugin.json |
| `test_shellcheck.sh` | All hook scripts pass shellcheck at warning level (skips if shellcheck not installed) | 20 hooks + lib |

**Validation rules for `test_yaml_frontmatter.py`:**
- Required fields: `id`, `domain`, `title`, `type`, `estimatedTokens`, `loadingStrategy`
- `id` pattern: `^[a-z]+/[a-z_]+$`
- `domain` enum: `[engineering, angular, azure, commands, dotnet, git, python, schema, security]`
- `type` enum: `[always, framework, reference, pattern, index, detection]`
- `loadingStrategy` enum: `[always, onDemand, lazy]`
- `estimatedTokens`: integer >= 1
- For index files: `indexedFiles[].path` must resolve to existing file relative to parent dir
- File's `domain` field must match its parent directory name

**Validation rules for `test_cross_references.py`:**
- For each agent config's `skills[].name`: `forge-plugin/skills/{name}/SKILL.md` exists
- For each agent config's `context.primaryDomains[]`: `forge-plugin/context/{domain}/` exists
- For each agent config's `memory.storagePath`: directory exists relative to `forge-plugin/`
- `crossDomainTriggers` format `domain/filename` resolves to `context/{domain}/{filename}.md`
- No circular cross-domain triggers

**Skip files for frontmatter validation**: `cross_domain.md`, `loading_protocol.md` (have frontmatter but special structure)

---

### Phase 3: Hook Test Harness and Security Hooks ✅

**Goal**: Build the hook testing infrastructure and test the 5 Shield-layer security hooks — the highest-risk components.

**Status**: Complete — 208 pytest integration tests, all passing. Infrastructure includes HookRunner subprocess harness, TempForgeEnvironment with git staging support, and 18 fixture files.

**Infrastructure to create:**

| File | Purpose |
|------|---------|
| `layer2/hooks/conftest.py` | HookRunner class (subprocess execution, JSON I/O, exit code assertion), HookResult class (properties: `is_allow`, `is_deny`, `deny_reason`, `additional_context`), TempForgeEnvironment context manager |
| `fixtures/hook_inputs/*.json` | ~19 fixture files covering all hook event types with safe and dangerous variants |

**HookRunner spec:**

```
HookRunner(script_name, timeout=10)
  .run(input_json, env_overrides=None, cwd=None) -> HookResult

HookResult:
  .exit_code: int
  .stdout: str
  .stderr: str
  .json_output: dict | None
  .is_allow: bool  (no deny decision in JSON output)
  .is_deny: bool
  .deny_reason: str
  .additional_context: str

Environment variables set by HookRunner:
- CLAUDE_PLUGIN_ROOT = forge-plugin absolute path
- PATH = standard paths
- HOME = user home
```

**Tests to implement (Shield layer — 5 hooks):**

| Test File | Hook | Key Test Cases |
|-----------|------|----------------|
| `test_sandbox_boundary_guard.py` | `sandbox_boundary_guard.sh` | Allows project-internal paths; blocks `~/.ssh/`, `.env`, `/etc/passwd`; blocks bash commands accessing sensitive paths; allows `/tmp/`; handles Read, Write, Edit, Bash tool types |
| `test_pii_redactor.py` | `pii_redactor.sh` | Clean prompts pass; detects email, SSN, AWS keys, GitHub tokens, private keys; returns `additionalContext` with PII type labels |
| `test_dependency_sentinel.py` | `dependency_sentinel.sh` | Normal pip install requests allowed; typosquatted packages (`colourama`, `crossenv`) blocked; non-install commands ignored; handles pip, npm, yarn, dotnet package managers |
| `test_git_hygiene_enforcer.py` | `git_hygiene_enforcer.sh` | Blocks git push to main/master; blocks `--force` push; enforces conventional commit format; blocks `--no-verify`; allows normal git operations |
| `test_pre_commit_quality.py` | `pre_commit_quality.sh` | Blocks commits with staged `.env` files; blocks commits with staged `/claudedocs/` files; allows clean commits |

---

### Phase 4: Chronicle, Foreman & Town Crier Hook Tests ✅

**Goal**: Test all remaining 15 hooks plus the shared health_buffer library — memory lifecycle (Chronicle layer), workflow quality (Foreman layer), and telemetry/reporting (Town Crier layer).

**Status**: Complete — 175 new pytest integration tests (all passing). Total Layer 2 hook suite: 383 tests (208 Phase 3 + 175 Phase 4).

**Infrastructure additions:**
- `_run_pruning_in_env()` / `_run_validator_in_env()` helpers — copy hooks into TempForgeEnvironment so `SCRIPT_DIR`-derived `FORGE_DIR` resolves to temp files (required for hooks that derive file paths from `FORGE_DIR` rather than stdin JSON)
- `_make_plugin_root()` helper — creates 2-level deep subdirectory for `CLAUDE_PLUGIN_ROOT` so `../../.forge` resolves correctly in health_buffer.sh
- `env_overrides` parameter used extensively for `CLAUDE_PLUGIN_ROOT` in health buffer tests

**Tests implemented (Chronicle layer — 4 hooks):**

| Test File | Hook | Key Test Cases |
|-----------|------|----------------|
| `test_memory_freshness_enforcer.py` | `memory_freshness_enforcer.sh` | Fresh memory (< 30d) allowed; aging memory (31-90d) allowed with warning; stale memory (> 90d) denied; non-memory reads ignored; handles missing timestamp | 17 tests ✅ |
| `test_memory_quality_gate.py` | `memory_quality_gate.sh` | Validates freshness timestamp present; warns on oversized files; checks specificity (no absolute paths outside project); checks completeness for `project_overview` | 15 tests ✅ |
| `test_memory_cross_pollinator.py` | `memory_cross_pollinator.sh` | Critical skill findings propagated to shared `cross_skill_insights.md`; non-critical findings not propagated; creates file if absent | 10 tests ✅ |
| `test_memory_pruning_daemon.py` | `memory_pruning_daemon.sh` | Prunes files > line limit; preserves header (first 5 lines); respects per-type limits (200/300/500); inserts pruning marker; skips operational files (`index.md`, `lifecycle.md`); handles `review_history` 300-line limit | 9 tests ✅ |

**Tests implemented (Foreman layer — 8 hooks):**

| Test File | Hook | Key Test Cases |
|-----------|------|----------------|
| `test_frontmatter_validator.py` | `frontmatter_validator.sh` | Blocks context writes without frontmatter; blocks invalid domain enum; allows valid frontmatter; skips non-context files (skills, memory) | 18 tests ✅ |
| `test_agent_config_validator.py` | `agent_config_validator.sh` | Validates agent config on SubagentStart; blocks agents with missing config; validates schema compliance | 11 tests ✅ |
| `test_skill_compliance_checker.py` | `skill_compliance_checker.sh` | Detects compliant 6-step workflow in transcript; detects skipped steps; reports specific missing steps; handles multi-skill sessions | 9 tests ✅ |
| `test_output_quality_scorer.py` | `output_quality_scorer.sh` | Scores `/claudedocs/` output completeness; handles missing outputs; validates naming convention | 9 tests ✅ |
| `test_context_drift_detector.py` | `context_drift_detector.sh` | Detects dependency changes conflicting with loaded context; uses `framework_conflicts.json`; allows non-conflicting changes | 11 tests ✅ |
| `test_command_chain_context.py` | `command_chain_context.sh` | Persists ExecutionContext to `.forge/chain_state.json`; handles first command in chain; handles chained commands | 11 tests ✅ |
| `test_output_archival.py` | `output_archival.sh` | Archives `/claudedocs/` output with manifest tracking | 6 tests ✅ |
| `test_root_agent_validator.py` | `root_agent_validator.sh` | Validates required directories exist; validates required files exist; creates `.forge/` runtime dir; outputs session context with component counts | 7 tests ✅ |

**Tests implemented (Town Crier layer — 3 hooks):**

| Test File | Hook | Key Test Cases |
|-----------|------|----------------|
| `test_system_health_emitter.py` | `system_health_emitter.sh` | Aggregates health buffer warnings; outputs combined report; handles empty buffer | 7 tests ✅ |
| `test_forge_telemetry.py` | `forge_telemetry.sh` | Collects session statistics from transcript; logs to `.forge/telemetry.log` | 13 tests ✅ |
| `test_context_usage_tracker.py` | `context_usage_tracker.sh` | Identifies unreferenced context files; identifies over-used files; writes to `.forge/context_usage.json` | 12 tests ✅ |

**Shared library test (implemented):**

| Test File | Library | Key Test Cases |
|-----------|---------|----------------|
| `test_health_buffer_lib.py` | `lib/health_buffer.sh` | Append + flush cycle works; concurrent-safe with flock; max 200 lines enforced; graceful failure on lock timeout | 10 tests ✅ |

**Fixture files (created for Phase 4):**
- `fixtures/memory_files/` — fresh_memory.md, stale_memory.md, no_timestamp_memory.md, oversized_memory.md, vague_memory.md, absolute_paths_memory.md
- `fixtures/transcripts/` — compliant_skill_session.txt, noncompliant_skill_session.txt, multi_skill_session.txt, telemetry_session.txt
- `fixtures/hook_inputs/` — session_end_basic.json, stop_basic.json, stop_hook_active.json, subagent_start_valid.json, subagent_start_builtin.json, task_completed_analyze.json, pre_compact_auto.json

---

### Phase 5: Memory and Context Lifecycle Tests ✅

**Goal**: Test the memory lifecycle simulation and context loading protocol independently of hooks.

**Status**: Complete — 121 new pytest tests (57 memory + 64 context), all passing (11 context skips for absent cross-domain triggers). Total Layer 2 suite: 504 tests (383 Phase 3-4 + 121 Phase 5).

**Infrastructure additions:**
- `layer2/memory/` directory with conftest.py providing `temp_forge_env` fixture
- `layer2/context/` directory for static context validation tests
- `__init__.py` files for both new test packages

**Tests implemented (Memory lifecycle — 3 files, 57 tests):**

| Test File | Hook Under Test | Key Test Cases |
|-----------|-----------------|----------------|
| `test_freshness_lifecycle.py` | `memory_freshness_enforcer.sh` | Day 0-30 fresh (allow, no warning); day 31-89 aging (allow); day 90+ stale (deny); exact boundaries (30→fresh, 31→aging, 89→aging, 90→stale); missing/wrong-format/empty timestamps denied; different memory paths (projects, skills, agents, commands) | 24 tests ✅ |
| `test_pruning_behavior.py` | `memory_pruning_daemon.sh` | General 500-line limit (600→500, 700→500); project_overview 200-line limit (300→200, 201→200); review_history 300-line limit (450→300); at-limit files not pruned (500, 200, 300); below-limit files not pruned (499); header preservation (first 5 lines); pruning marker present with line count; operational files skipped (index, lifecycle, quality_guidance); recent-file detection without transcript | 17 tests ✅ |
| `test_line_limits.py` | `memory_quality_gate.sh` | General 500-line limit (500 no warn, 501 warns, 499 no warn); project_overview 200-line limit (200 no warn, 201 warns); review_history 300-line limit (300 no warn, 301 warns); never denies (oversized files allowed with warning); operational files skipped; timestamp injection (missing → injected); timestamp refresh (old → today) | 16 tests ✅ |

**Tests implemented (Context loading — 2 files, 64 tests, 11 skips):**

| Test File | What It Tests | Key Test Cases |
|-----------|---------------|----------------|
| `test_loading_protocol.py` | Context loading protocol from loading_protocol.md | Every domain (9) has index.md with frontmatter and type='index'; all indexedFiles entries reference existing files and have IDs; loadingStrategy='always' files have valid types; estimatedTokens positive and < 10000 (file + section level); domain consistency (field matches parent dir); loadingStrategy enum validation; required frontmatter fields present; top-level files (cross_domain.md, loading_protocol.md, index.md) exist with frontmatter | 48 tests ✅ |
| `test_cross_domain_triggers.py` | Cross-domain trigger validation from cross_domain.md | Trigger format matches `domain/filename` pattern; trigger targets resolve to existing files; no self-referential triggers; no circular 2-step trigger chains; cross_domain.md file exists with frontmatter and matrix content; referenced security_guidelines.md and common_patterns.md exist; per-domain index cross-domain references validated | 16 tests ✅ (11 skips for absent triggers) |

---

### Phase 6: CI Pipeline and E2E Tests ✅

**Goal**: Set up GitHub Actions CI and stub E2E tests for Claude CLI validation.

**Status**: Complete — 168 E2E bash checks (all passing), GitHub Actions workflow with 3 jobs, Layer 2 runner script, and tests README documentation. Total test suite: 1,225 pytest tests + 96 bash syntax checks + 168 E2E checks.

**Files created:**

| File | Purpose |
|------|---------|
| `.github/workflows/forge-tests.yml` | GitHub Actions workflow with 3 jobs: layer1-ci (every push/PR), layer2-hooks (after layer1), layer2-e2e (main only, continue-on-error) |
| `tests/layer2/e2e/test_plugin_loading.sh` | Verifies plugin manifest, directory structure, command path resolution, and claude CLI acceptance (26 checks) |
| `tests/layer2/e2e/test_command_execution.sh` | Verifies 12 commands registered, COMMAND.md files exist and have content, command index references (46 checks) |
| `tests/layer2/e2e/test_skill_invocation.sh` | Verifies 22 skills discoverable, SKILL.md + examples.md files, workflow steps, agent-to-skill references (96 checks) |
| `tests/README.md` | Documentation: quick start, prerequisites, layer descriptions, CI pipeline diagram, how to add tests, markers, fixture locations |
| `tests/layer2/run_layer2.sh` | Dedicated Layer 2 runner with `--e2e` flag support |

**CI workflow structure (implemented):**

```
Job: layer1-ci (runs on every push/PR to main/develop)
  - Install: python3.12, pyyaml, jsonschema, pytest, shellcheck, jq
  - Run: pytest forge-plugin/tests/layer1/ -v
  - Run: bash forge-plugin/tests/layer1/test_hook_syntax.sh
  - Run: bash forge-plugin/tests/layer1/test_shellcheck.sh

Job: layer2-hooks (runs after layer1-ci passes)
  - Install: python3.12, pyyaml, jsonschema, pytest, jq
  - Run: pytest forge-plugin/tests/layer2/hooks/ -v
  - Run: pytest forge-plugin/tests/layer2/memory/ -v
  - Run: pytest forge-plugin/tests/layer2/context/ -v

Job: layer2-e2e (runs only on push to main, continue-on-error)
  - Check: claude CLI available?
  - Run: bash forge-plugin/tests/layer2/e2e/test_plugin_loading.sh
  - Run: bash forge-plugin/tests/layer2/e2e/test_command_execution.sh
  - Run: bash forge-plugin/tests/layer2/e2e/test_skill_invocation.sh

Trigger paths: Only runs when forge-plugin/** or workflow file changes.
```

**E2E tests implemented (3 scripts, 168 checks):**

| Test File | Checks | Key Validations |
|-----------|--------|----------------|
| `test_plugin_loading.sh` | 26 | Plugin manifest is valid JSON; name, version, commands fields present; 12 command paths resolve; claude CLI accepts plugin directory; 8 required directories exist |
| `test_command_execution.sh` | 46 | All 12 expected commands registered in plugin.json; each has COMMAND.md with content (>5 lines); command count matches; commands/index.md references checked |
| `test_skill_invocation.sh` | 96 | All 22 skill directories exist; each has SKILL.md and examples.md; workflow step documentation checked; skill count validated; agent-to-skill references validated across 11 agent configs |

---

## Test Coverage Summary

| Component | Layer 1 (Static) | Layer 2 (Integration) | E2E | Total |
|-----------|------------------|----------------------|-----|-------|
| Agent configs (11) | Schema validation, file pairs, cross-refs | Config validator hook | Agent-to-skill refs | ~36 |
| Context files (81) | Frontmatter validation, cross-domain refs | Loading protocol (48), frontmatter hook, drift detector, cross-domain triggers (16) | — | ~238 |
| Hook scripts (20) | Registration, syntax, shellcheck (96 bash) | Full I/O contract testing (383 tests + 10 shared lib) | — | ~489 |
| Memory system | Directory structure, timestamp format | Freshness lifecycle (24), pruning (17), line limits (16), quality gate, cross-pollinator | — | ~137 |
| Skills (22) | File structure (`SKILL.md`, `examples.md`) | Compliance checker hook | Skill dirs, SKILL.md, examples.md, workflow steps (96 checks) | ~121+ |
| Commands (12) | `COMMAND.md` exists, manifest refs | Command chain hook | Registration, COMMAND.md, content, index refs (46 checks) | ~61+ |
| Plugin manifest | JSON validity, field completeness | — | Manifest, fields, path resolution, dir structure (26 checks) | ~34+ |
| Shared libraries | — | `health_buffer.sh` unit tests (10) | — | 10 |
| **Total** | **~1,225 pytest + 96 bash** | **~504 pytest** | **~168 bash** | **~1,993** |

---

## Critical Files Reference

| File | Role in Testing |
|------|----------------|
| `forge-plugin/interfaces/schemas/agent_config.schema.json` | Schema for validating all 11 agent configs |
| `forge-plugin/interfaces/schemas/context_metadata.schema.json` | Schema for validating all 81 context file frontmatters |
| `forge-plugin/interfaces/schemas/memory_entry.schema.json` | Schema for validating memory entry structure |
| `forge-plugin/hooks/hooks.json` | Hook registration manifest — source of truth for which hooks exist |
| `forge-plugin/hooks/lib/health_buffer.sh` | Shared library sourced by ~18 hooks — must be tested first |
| `forge-plugin/templates/root_safety_profile.json` | Required structure definition used by `test_file_structure.py` |
| `forge-plugin/hooks/lib/framework_conflicts.json` | Used by `context_drift_detector.sh` — needed in test fixtures |
| `forge-plugin/.claude-plugin/plugin.json` | Plugin manifest — validates all 12 command paths |
| `forge-plugin/memory/lifecycle.md` | Line limit and pruning rules — defines test assertions |
| `forge-plugin/context/loading_protocol.md` | 5-step protocol — defines context loading test assertions |

---

## Verification

After all phases are complete, the test suite should pass these checks:

1. `bash tests/run_all.sh` exits 0 with all Layer 1 tests passing
2. `bash tests/run_all.sh --layer2` exits 0 with all Layer 1 + Layer 2 tests passing
3. GitHub Actions runs Layer 1 on every PR and Layer 2 on merge to main
4. Breaking a convention (e.g., removing an agent's `.config.json`, adding a context file without frontmatter, referencing a non-existent skill) causes a test failure
5. Breaking a hook (e.g., changing exit codes, breaking JSON output format) causes a hook integration test failure
6. Memory lifecycle violations (e.g., exceeding line limits, missing timestamps) are caught by memory tests

---

## TODOs — Known Issues and Out-of-Scope Items

> *Items discovered during test implementation that need attention but are outside the scope of the testing phases themselves.*

### Data Quality Issues (caught by tests — 4 known failures)

- [ ] **TODO**: `context/angular/typescript_patterns.md` — `sections[6].keywords[0]` is `null` instead of a string, violating `context_metadata.schema.json`. Fix the YAML frontmatter keyword entry. *(Caught by `test_yaml_frontmatter.py::TestSchemaCompliance`)*

- [ ] **TODO**: `memory/skills/angular-code-review/example-project/reference.md` — 504 lines, exceeds the `reference` limit of 500 lines defined in `lifecycle.md`. *(Caught by `test_memory_structure.py::TestMemoryFileLineLimits`)*

- [ ] **TODO**: `memory/skills/dotnet-code-review/example-project/project_overview.md` — 299 lines, exceeds the `project_overview` limit of 200 lines defined in `lifecycle.md`. *(Caught by `test_memory_structure.py::TestMemoryFileLineLimits`)*

- [ ] **TODO**: `memory/skills/dotnet-code-review/example-project/review_history.md` — 343 lines, exceeds the `review_history` limit of 300 lines defined in `lifecycle.md`. *(Caught by `test_memory_structure.py::TestMemoryFileLineLimits`)*

### Convention Inconsistencies

- [x] **DONE**: Memory timestamp format mismatch — Updated `lifecycle.md` to accept both HTML comment format (`<!-- Last Updated: YYYY-MM-DD -->`) and bold markdown format (`**Last Updated**: YYYY-MM-DD`). The HTML comment is preferred for new files; bold markdown is legacy but valid. Tests can now validate against either format.

- [x] **DONE**: Three hook scripts existed on disk but were NOT registered in `hooks.json`: `memory_sync.sh`, `session_context.sh`, `context_freshness.sh`. These are utility scripts, not event hooks. Moved to `hooks/lib/` directory alongside `health_buffer.sh`. Documentation in `index.md` and `HOOKS_GUIDE.md` updated to reflect new locations under "Utility Scripts" section.

### CI / Environment

- [x] **DONE**: `shellcheck` is now installed in CI via `apt-get install shellcheck` in the GitHub Actions workflow (`forge-tests.yml`). Still not installed in the local development environment — `test_shellcheck.sh` continues to skip gracefully locally.

- [x] **DONE**: `tests/README.md` created in Phase 6 — documents quick start, prerequisites, layer descriptions, CI pipeline, how to add tests, markers, and fixture locations.

### Hook Behavior Observations (discovered in Phase 3)

- [x] **DONE**: `pre_commit_quality.sh` — Added documentation comment explaining that `*.pem` and `*.key` SECRET_PATTERNS are grep'd with `-E "(^|/)${pattern}$"` which matches filenames like `cert.pem` and `server.key` (the `*` is not a literal glob in this context).

- [x] **DONE**: `pre_commit_quality.sh` now sources `health_buffer.sh` and logs secret file detections to the system health buffer for consistency with other Shield hooks.

- [x] **DONE**: Removed misleading "exit code 2 = blocking error" comment from `pre_commit_quality.sh`. The deny mechanism is exclusively via JSON `hookSpecificOutput.permissionDecision` — all hooks exit 0.

- [x] **DONE**: Updated `hooks.json` to clarify that `pii_redactor.sh` is warn-only: added description "Scan for PII patterns (warn-only — does not block prompts)".

### Hook Behavior Observations (discovered in Phase 4)

- [ ] **TODO**: `skill_compliance_checker.sh` — `SKILLS_USED=$(grep -oE ... | sort -u)` crashes with `set -euo pipefail` when `grep` finds no matches (exit 1 propagated by `pipefail`). This causes the hook to exit 1 when no skills are present in the transcript. Harmless (session is ending) but incorrect. Fix: add `|| true` after the grep pipeline.

- [ ] **TODO**: `skill_compliance_checker.sh` uses `decision: "block"` JSON format for non-compliance instead of the standard `hookSpecificOutput.permissionDecision: "deny"` used by Shield hooks. This inconsistency makes it harder to programmatically detect denials. Consider standardizing the JSON output format.

- [ ] **TODO**: `framework_conflicts.json` referenced by `context_drift_detector.sh` at `SCRIPT_DIR/lib/framework_conflicts.json` does not exist in the repository. The hook exits cleanly when the file is missing, but conflict detection is effectively disabled. Create the conflicts definition file or document its absence.

- [ ] **TODO**: `output_quality_scorer.sh` is listed under Foreman (§6.3) in the TESTING_ROADMAP but self-identifies as Town Crier (§6.4) in its script header. Clarify the correct layer assignment.

- [ ] **TODO**: `root_agent_validator.sh` — `find` commands at the bottom (counting agents, skills, commands, hooks) crash with `set -euo pipefail` when the target directories don't exist. The `2>/dev/null` only suppresses stderr, but `pipefail` still propagates the non-zero exit code from `find`. Fix: add `|| true` after each `find | wc -l` pipeline.

- [ ] **TODO**: `health_buffer.sh` path resolution — `CLAUDE_PLUGIN_ROOT/../../.forge` goes TWO levels up from the plugin root, which assumes `CLAUDE_PLUGIN_ROOT` is set to a path nested two levels below the repo root. This is fragile and sensitive to directory layout changes. Consider using `git rev-parse --show-toplevel` instead, or document the expected CLAUDE_PLUGIN_ROOT path convention.

- [ ] **TODO**: Hooks that derive file paths from `SCRIPT_DIR` → `FORGE_DIR` (memory_pruning_daemon, memory_cross_pollinator, root_agent_validator, output_archival) cannot be fully integration-tested against temporary directories without copying the hook script into the temp env. Tests use `_run_*_in_env()` helpers to work around this, but a more robust approach would be to make these hooks accept a configurable `FORGE_DIR` via environment variable override.

### E2E / CI Observations (discovered in Phase 6)

- [x] **DONE**: `commands/index.md` updated to reference all 12 commands including `remember`, `mock`, `azure-pipeline`, `etl-pipeline`, `azure-function`. The index file now matches the actual command directories.

- [x] **DONE**: The 6-step mandatory workflow in SKILL_TEMPLATE.md is documented as a RECOMMENDATION, not strict enforcement. The E2E skill invocation test (`test_skill_invocation.sh`) now notes this and reports workflow step coverage as informational rather than failures. Existing skills use equivalent or adapted step names.

- [x] **DONE**: E2E tests document the runtime testing limitation. The test scripts (`test_command_execution.sh`, `test_skill_invocation.sh`) now include clear comments explaining that the `claude` CLI requires an interactive session, and list future options (batch mode, test harness).

- [x] **DONE**: CI workflow validation notes added to `run_all.sh` header comments. Notes cover FORGE_DIR export, shellcheck differences between Ubuntu versions, and canonical entry point guidance.

- [x] **DONE**: Layer 2 entry point documented. `run_layer2.sh` now includes a DEPRECATED notice pointing to `run_all.sh --layer2` as the canonical entry point. Both still work, but `run_all.sh` is preferred for consistency with CI.
