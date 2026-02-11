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

### Phase 1: Foundation and Infrastructure

**Goal**: Create the test directory structure, runner scripts, shared configuration, and the first high-value static tests.

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

### Phase 2: Static Validation (Context, Memory, Cross-References)

**Goal**: Validate all 81 context files, memory structure, plugin manifest, cross-reference integrity, and hook registration completeness.

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

### Phase 3: Hook Test Harness and Security Hooks

**Goal**: Build the hook testing infrastructure and test the 5 Shield-layer security hooks — the highest-risk components.

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

### Phase 4: Chronicle and Foreman Hook Tests

**Goal**: Test the 12 remaining hooks — memory lifecycle (Chronicle layer) and workflow quality (Foreman layer).

**Tests to implement (Chronicle layer — 4 hooks):**

| Test File | Hook | Key Test Cases |
|-----------|------|----------------|
| `test_memory_freshness_enforcer.py` | `memory_freshness_enforcer.sh` | Fresh memory (< 30d) allowed; aging memory (31-90d) allowed with warning; stale memory (> 90d) denied; non-memory reads ignored; handles missing timestamp |
| `test_memory_quality_gate.py` | `memory_quality_gate.sh` | Validates freshness timestamp present; warns on oversized files; checks specificity (no absolute paths outside project); checks completeness for `project_overview` |
| `test_memory_cross_pollinator.py` | `memory_cross_pollinator.sh` | Critical skill findings propagated to shared `cross_skill_insights.md`; non-critical findings not propagated; creates file if absent |
| `test_memory_pruning_daemon.py` | `memory_pruning_daemon.sh` | Prunes files > line limit; preserves header (first 5 lines); respects per-type limits (200/300/500); inserts pruning marker; skips operational files (`index.md`, `lifecycle.md`); handles `review_history` 300-line limit |

**Tests to implement (Foreman layer — 8 hooks):**

| Test File | Hook | Key Test Cases |
|-----------|------|----------------|
| `test_frontmatter_validator.py` | `frontmatter_validator.sh` | Blocks context writes without frontmatter; blocks invalid domain enum; allows valid frontmatter; skips non-context files (skills, memory) |
| `test_agent_config_validator.py` | `agent_config_validator.sh` | Validates agent config on SubagentStart; blocks agents with missing config; validates schema compliance |
| `test_skill_compliance_checker.py` | `skill_compliance_checker.sh` | Detects compliant 6-step workflow in transcript; detects skipped steps; reports specific missing steps; handles multi-skill sessions |
| `test_output_quality_scorer.py` | `output_quality_scorer.sh` | Scores `/claudedocs/` output completeness; handles missing outputs; validates naming convention |
| `test_context_drift_detector.py` | `context_drift_detector.sh` | Detects dependency changes conflicting with loaded context; uses `framework_conflicts.json`; allows non-conflicting changes |
| `test_command_chain_context.py` | `command_chain_context.sh` | Persists ExecutionContext to `.forge/chain_state.json`; handles first command in chain; handles chained commands |
| `test_output_archival.py` | `output_archival.sh` | Archives `/claudedocs/` output with manifest tracking |
| `test_root_agent_validator.py` | `root_agent_validator.sh` | Validates required directories exist; validates required files exist; creates `.forge/` runtime dir; outputs session context with component counts |

**Tests to implement (Town Crier layer — 3 hooks):**

| Test File | Hook | Key Test Cases |
|-----------|------|----------------|
| `test_system_health_emitter.py` | `system_health_emitter.sh` | Aggregates health buffer warnings; outputs combined report; handles empty buffer |
| `test_forge_telemetry.py` | `forge_telemetry.sh` | Collects session statistics from transcript; logs to `.forge/telemetry.log` |
| `test_context_usage_tracker.py` | `context_usage_tracker.sh` | Identifies unreferenced context files; identifies over-used files; writes to `.forge/context_usage.json` |

**Shared library test:**

| Test File | Library | Key Test Cases |
|-----------|---------|----------------|
| `test_health_buffer_lib.py` | `lib/health_buffer.sh` | Append + flush cycle works; concurrent-safe with flock; max 200 lines enforced; graceful failure on lock timeout |

**Fixture files needed for Phase 4:**
- `fixtures/memory_files/` — Fresh, aging, stale, oversized, no-timestamp memory files
- `fixtures/transcripts/` — Compliant and non-compliant skill session transcripts
- `fixtures/hook_inputs/` — SessionEnd, Stop, SubagentStart, TaskCompleted, PreCompact event inputs

---

### Phase 5: Memory and Context Lifecycle Tests

**Goal**: Test the memory lifecycle simulation and context loading protocol independently of hooks.

**Tests to implement (Memory lifecycle):**

| Test File | What It Tests |
|-----------|---------------|
| `test_freshness_lifecycle.py` | Create memory files with various timestamps; verify classification (fresh/aging/stale); verify the 30d/90d boundaries are exact |
| `test_pruning_behavior.py` | Create oversized files in temp dirs; run `memory_pruning_daemon.sh`; verify correct truncation; verify header preservation; verify pruning markers |
| `test_line_limits.py` | Create files at exact boundaries (200, 300, 500 lines); verify `memory_quality_gate.sh` warns at limit+1 but not at limit; verify per-type limits (`project_overview`=200, `review_history`=300, general=500) |

**Tests to implement (Context loading):**

| Test File | What It Tests |
|-----------|---------------|
| `test_loading_protocol.py` | Every domain has `index.md`; index files with `indexedFiles` reference existing files; `loadingStrategy: always` files have appropriate type; `estimatedTokens` values are reasonable (> 0, < 10000); domain consistency (file's `domain` field matches parent dir name) |
| `test_cross_domain_triggers.py` | All `crossDomainTriggers` target existing files; no self-referential triggers; trigger format matches `domain/filename` pattern; no circular trigger chains |

---

### Phase 6: CI Pipeline and E2E Tests

**Goal**: Set up GitHub Actions CI and stub E2E tests for Claude CLI validation.

**Files to create:**

| File | Purpose |
|------|---------|
| `.github/workflows/forge-tests.yml` | GitHub Actions workflow with Layer 1 (always) and Layer 2 (on merge to main) |
| `tests/layer2/e2e/test_plugin_loading.sh` | Verify plugin loads via `claude --plugin-dir` (skips if no CLI) |
| `tests/layer2/e2e/test_command_execution.sh` | Verify commands are registered and invocable (skips if no CLI) |
| `tests/layer2/e2e/test_skill_invocation.sh` | Verify skills are discoverable and invocable (skips if no CLI) |
| `tests/README.md` | Documentation: how to run, what each layer covers, how to add tests |

**CI workflow structure:**

```
Job: layer1-ci (runs on every push/PR to main/develop)
  - Install: python3, pyyaml, jsonschema, pytest, shellcheck, jq
  - Run: pytest forge-plugin/tests/layer1/ -v
  - Run: bash forge-plugin/tests/layer1/test_hook_syntax.sh
  - Run: bash forge-plugin/tests/layer1/test_shellcheck.sh

Job: layer2-hooks (runs after layer1-ci passes)
  - Install: python3, pyyaml, jsonschema, pytest, jq
  - Run: pytest forge-plugin/tests/layer2/hooks/ -v
  - Run: pytest forge-plugin/tests/layer2/memory/ -v
  - Run: pytest forge-plugin/tests/layer2/context/ -v

Job: layer2-e2e (runs only on push to main, continue-on-error)
  - Check: claude CLI available?
  - Run: bash forge-plugin/tests/layer2/e2e/test_plugin_loading.sh

Trigger paths: Only runs when forge-plugin/** or workflow file changes.
```

---

## Test Coverage Summary

| Component | Layer 1 (Static) | Layer 2 (Integration) | Total Tests |
|-----------|------------------|----------------------|-------------|
| Agent configs (11) | Schema validation, file pairs, cross-refs | Config validator hook | ~25 |
| Context files (81) | Frontmatter validation, cross-domain refs | Loading protocol, frontmatter hook | ~90 |
| Hook scripts (20) | Registration, syntax, shellcheck | Full I/O contract testing | ~100+ |
| Memory system | Directory structure, timestamp format | Freshness, pruning, line limits | ~30 |
| Skills (22) | File structure (`SKILL.md`, `examples.md`) | Compliance checker hook | ~25 |
| Commands (12) | `COMMAND.md` exists, manifest refs | Command chain hook, E2E | ~15 |
| Plugin manifest | JSON validity, field completeness | E2E loading | ~8 |
| Shared libraries | — | `health_buffer.sh` unit tests | ~5 |
| **Total** | **~100** | **~200** | **~300** |

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
