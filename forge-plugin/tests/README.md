# ⚒️ The Forge — Test Suite

How to run tests, what each layer covers, and how to add new tests.

---

## Quick Start

```bash
# From the forge-plugin/ directory:

# Run Layer 1 only (static/CI tests — fast, no runtime needed)
bash tests/run_all.sh

# Run Layer 1 + Layer 2 (integration tests)
bash tests/run_all.sh --layer2

# Run everything including E2E (requires claude CLI)
bash tests/run_all.sh --e2e
```

### Prerequisites

| Tool | Required | Install |
|------|----------|---------|
| Python 3.10+ | Yes | `apt install python3` or `brew install python` |
| pytest | Yes | `pip install pytest` |
| pyyaml | Yes | `pip install pyyaml` |
| jsonschema | Yes | `pip install jsonschema` |
| jq 1.6+ | Yes | `apt install jq` or `brew install jq` |
| shellcheck | Optional | `apt install shellcheck` or `brew install shellcheck` |
| claude CLI | Optional | Required only for E2E tests |

Install all Python dependencies at once:

```bash
pip install pytest pyyaml jsonschema
```

---

## Test Layers

### Layer 1: Static/CI Tests

**Purpose**: Validate file structure, schemas, syntax, and cross-references. No runtime needed.

**Runs on**: Every push and PR to `main`/`develop` via GitHub Actions.

| Test File | What It Validates |
|-----------|-------------------|
| `test_json_schemas.py` | Agent configs against JSON schema, hooks.json structure, plugin.json fields |
| `test_file_structure.py` | Required dirs/files, agent `.md`+`.config.json` pairs, skill/command dirs |
| `test_yaml_frontmatter.py` | 81 context files have valid YAML frontmatter with correct enums |
| `test_cross_references.py` | Skills in agent configs exist, domains exist, memory paths exist |
| `test_hooks_registration.py` | All hook scripts registered in hooks.json, all registered scripts exist |
| `test_memory_structure.py` | Memory directory structure, timestamps, line limits |
| `test_plugin_manifest.py` | plugin.json validity, 12 commands, command paths resolve |
| `test_hook_syntax.sh` | Shebangs, `set -euo pipefail`, `bash -n` syntax, executable permissions |
| `test_shellcheck.sh` | Bash linting (skips gracefully if shellcheck not installed) |

**Run independently:**

```bash
# All Layer 1 tests
bash tests/layer1/run_layer1.sh

# Individual pytest files
cd tests && python -m pytest layer1/test_json_schemas.py -v

# Or without pytest
python3 tests/layer1/test_json_schemas.py
```

### Layer 2: Integration Tests

**Purpose**: Runtime validation of hooks, memory lifecycle, and context loading.

**Runs on**: After Layer 1 passes in GitHub Actions.

#### Hooks (20 test modules)

Each of the 20 hook scripts has a dedicated test module that feeds JSON on stdin and asserts on exit codes and JSON stdout.

| Layer | Hooks Tested |
|-------|-------------|
| Shield (Security) | sandbox_boundary_guard, pii_redactor, dependency_sentinel, git_hygiene_enforcer, pre_commit_quality |
| Chronicle (Memory) | memory_freshness_enforcer, memory_quality_gate, memory_cross_pollinator, memory_pruning_daemon |
| Foreman (Workflow) | frontmatter_validator, agent_config_validator, skill_compliance_checker, output_quality_scorer, context_drift_detector, command_chain_context, output_archival, root_agent_validator |
| Town Crier (Telemetry) | system_health_emitter, forge_telemetry, context_usage_tracker |
| Shared Library | health_buffer.sh |

#### Memory Lifecycle (3 test modules)

| Test File | What It Tests |
|-----------|---------------|
| `test_freshness_lifecycle.py` | Day 0-90+ aging progression, boundary cases |
| `test_pruning_behavior.py` | Line limit enforcement, header preservation, pruning markers |
| `test_line_limits.py` | Per-type limits (200/300/500), warning vs denial behavior |

#### Context Loading (2 test modules)

| Test File | What It Tests |
|-----------|---------------|
| `test_loading_protocol.py` | 5-step loading protocol, index files, strategy validation |
| `test_cross_domain_triggers.py` | Trigger format, circular references, target resolution |

**Run independently:**

```bash
# All Layer 2 tests
bash tests/layer2/run_layer2.sh

# Specific hook tests
cd tests && python -m pytest layer2/hooks/test_sandbox_boundary_guard.py -v

# All memory tests
cd tests && python -m pytest layer2/memory/ -v

# All context tests
cd tests && python -m pytest layer2/context/ -v
```

### E2E Tests

**Purpose**: Validate the full plugin structure, command registration, and skill discovery. Runtime invocation tests require the `claude` CLI.

**Runs on**: Push to `main` only, with `continue-on-error` (claude CLI may not be available in CI).

| Test File | What It Validates |
|-----------|-------------------|
| `test_plugin_loading.sh` | Plugin manifest, directory structure, command path resolution |
| `test_command_execution.sh` | 12 commands registered, COMMAND.md files, index references |
| `test_skill_invocation.sh` | 22 skills discoverable, SKILL.md files, workflow steps, agent refs |

**Run independently:**

```bash
# All E2E tests
bash tests/layer2/run_layer2.sh --e2e

# Individual E2E tests
bash tests/layer2/e2e/test_plugin_loading.sh
bash tests/layer2/e2e/test_command_execution.sh
bash tests/layer2/e2e/test_skill_invocation.sh
```

---

## CI Pipeline

GitHub Actions workflow: `.github/workflows/forge-tests.yml`

```
┌─────────────────────────────────────────┐
│  layer1-ci (every push/PR)              │
│  ├── pytest layer1/ -v                  │
│  ├── test_hook_syntax.sh                │
│  └── test_shellcheck.sh                 │
└──────────────┬──────────────────────────┘
               │ (must pass)
┌──────────────▼──────────────────────────┐
│  layer2-hooks (after layer1)            │
│  ├── pytest layer2/hooks/ -v            │
│  ├── pytest layer2/memory/ -v           │
│  └── pytest layer2/context/ -v          │
└──────────────┬──────────────────────────┘
               │ (must pass, main only)
┌──────────────▼──────────────────────────┐
│  layer2-e2e (main only, continue-on-err)│
│  ├── test_plugin_loading.sh             │
│  ├── test_command_execution.sh          │
│  └── test_skill_invocation.sh           │
└─────────────────────────────────────────┘
```

**Trigger paths**: Only runs when `forge-plugin/**` or the workflow file changes.

---

## Adding New Tests

### Adding a Layer 1 Test

1. Create `tests/layer1/test_your_feature.py`
2. Use the `forge_dir` and `repo_root` fixtures from `conftest.py`
3. Add `@pytest.mark.layer1` marker to test classes/functions
4. Tests are auto-discovered by pytest via `pytest.ini`

### Adding a Hook Integration Test

1. Create `tests/layer2/hooks/test_your_hook.py`
2. Import `HookRunner` from the hooks `conftest.py`:

```python
from conftest import HookRunner

class TestYourHook:
    def setup_method(self):
        self.runner = HookRunner("your_hook.sh")

    def test_allows_safe_input(self):
        result = self.runner.run({"toolName": "Write", ...})
        assert result.is_allow

    def test_blocks_dangerous_input(self):
        result = self.runner.run({"toolName": "Write", ...})
        assert result.is_deny
        assert "expected reason" in result.deny_reason
```

3. Add fixture JSON files to `tests/fixtures/hook_inputs/` if needed
4. Add `@pytest.mark.hooks` marker

### Adding a Memory/Context Test

1. Create test files in `tests/layer2/memory/` or `tests/layer2/context/`
2. Use `TempForgeEnvironment` for stateful tests that need file I/O
3. Add appropriate markers (`@pytest.mark.memory` or `@pytest.mark.context`)

### Adding an E2E Test

1. Create `tests/layer2/e2e/test_your_feature.sh`
2. Follow the pattern: check for `claude` CLI, skip if absent, exit 0/1
3. Make it executable: `chmod +x tests/layer2/e2e/test_your_feature.sh`

---

## Test Fixtures

```
tests/fixtures/
├── hook_inputs/         # JSON stdin for hook tests
├── memory_files/        # Sample memory files (fresh, stale, oversized, etc.)
├── context_files/       # Sample context files for validation
├── agent_configs/       # Sample agent config.json files
└── transcripts/         # Mock session transcripts
```

---

## Markers

Run tests by category using pytest markers:

```bash
cd tests

# Run only hook tests
python -m pytest -m hooks -v

# Run only memory tests
python -m pytest -m memory -v

# Run only context tests
python -m pytest -m context -v

# Run only Layer 1
python -m pytest -m layer1 -v
```

---

## Exit Code Contract

| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | One or more tests failed |
| 0 (skip) | Optional dependency not available, test skipped gracefully |

---

## Current Test Counts

| Component | Layer 1 | Layer 2 | E2E | Total |
|-----------|---------|---------|-----|-------|
| Agent configs | ~25 | ~11 | — | ~36 |
| Context files | ~174 | ~64 | — | ~238 |
| Hook scripts | ~96 bash | ~383 | — | ~479 |
| Memory system | ~25 | ~57 | — | ~82 |
| Skills | ~25 | — | ~22+ | ~47+ |
| Commands | ~15 | — | ~12+ | ~27+ |
| Plugin manifest | ~8 | — | ~5+ | ~13+ |
| Shared libraries | — | ~10 | — | ~10 |
| **Total** | **~368** | **~525** | **~39+** | **~932+** |
