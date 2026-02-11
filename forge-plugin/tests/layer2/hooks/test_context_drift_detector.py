"""Tests for context_drift_detector.sh — The Foreman: Context Drift Detector.

Validates that dependency file changes are scanned for framework conflicts
against loaded context files. Uses framework_conflicts.json to detect drift.

Event: PostToolUse (matcher: Write|Edit)
"""

import json

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, FORGE_DIR


SCRIPT = "context_drift_detector.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_post_input(file_path: str):
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": file_path},
    }


# ── Non-dependency files are ignored ────────────────────────────────────

class TestNonDependencyFilesIgnored:
    """Hook should silently exit for non-dependency files."""

    def test_python_source_file(self, runner):
        result = runner.run(_make_post_input("src/main.py"))
        assert result.exit_code == 0
        assert result.is_allow
        assert not result.has_warning

    def test_markdown_file(self, runner):
        result = runner.run(_make_post_input("README.md"))
        assert result.exit_code == 0
        assert result.is_allow

    def test_config_file(self, runner):
        result = runner.run(_make_post_input(".gitignore"))
        assert result.exit_code == 0
        assert result.is_allow


# ── Dependency file recognition ─────────────────────────────────────────

class TestDependencyFileRecognition:
    """Hook should recognize various dependency file types."""

    def test_package_json_recognized(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "package.json",
            json.dumps({
                "dependencies": {"express": "^4.18.0"},
            }),
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0

    def test_requirements_txt_recognized(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "requirements.txt",
            "flask==2.3.0\nrequests==2.31.0\n",
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0

    def test_pyproject_toml_recognized(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "pyproject.toml",
            '[tool.poetry.dependencies]\npython = "^3.11"\nfastapi = "^0.100"\n',
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0

    def test_csproj_recognized(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "MyApp.csproj",
            '<PackageReference Include="Newtonsoft.Json" Version="13.0.1" />\n',
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0


# ── Missing conflicts file handled gracefully ──────────────────────────

class TestMissingConflictsFile:
    """If framework_conflicts.json is missing, hook should exit silently."""

    def test_no_conflicts_file_exits_cleanly(self, runner, temp_forge_env):
        """With a valid dep file but no framework_conflicts.json, should exit 0."""
        env = temp_forge_env()
        fp = env.create_file(
            "requirements.txt",
            "flask==2.3.0\n",
        )
        # Run without the conflicts file in the expected location
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0


# ── Non-conflicting dependency changes ──────────────────────────────────

class TestNonConflictingChanges:
    """Dependency changes that don't conflict with context should pass silently."""

    def test_single_framework_no_drift(self, runner, temp_forge_env):
        env = temp_forge_env()
        fp = env.create_file(
            "requirements.txt",
            "requests==2.31.0\npytest==7.4.0\n",
        )
        result = runner.run(
            _make_post_input(str(fp)),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert result.is_allow


# ── Always exits 0 ─────────────────────────────────────────────────────

class TestAlwaysExitsZero:
    """Context drift detector is advisory — always exits 0."""

    def test_exits_zero_on_any_input(self, runner):
        result = runner.run(_make_post_input("anything.txt"))
        assert result.exit_code == 0

    def test_exits_zero_on_empty_file_path(self, runner):
        result = runner.run({
            "tool_name": "Write",
            "tool_input": {},
        })
        assert result.exit_code == 0
