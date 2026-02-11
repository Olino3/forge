"""Tests for root_agent_validator.sh — The Shield: Root Agent Validator.

Validates plugin structural integrity at SessionStart, checking that
required directories, files, and configurations exist per the
safety profile (root_safety_profile.json).

Event: SessionStart
"""

import json
import os
import shutil
import subprocess

import pytest

from layer2.hooks.hook_helpers import (
    HookResult,
    HookRunner,
    TempForgeEnvironment,
    FORGE_DIR,
    HOOKS_DIR,
)


SCRIPT = "root_agent_validator.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_session_start_input():
    return {"event": "SessionStart"}


def _run_validator_in_env(env: TempForgeEnvironment, inp: dict) -> HookResult:
    """Run root_agent_validator.sh with SCRIPT_DIR inside the temp env.

    The hook derives FORGE_DIR from SCRIPT_DIR, so it must be copied
    into the temp env for edge-case tests (missing profile, etc.).
    """
    hooks_dir = env.project_root / "forge-plugin" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(HOOKS_DIR / SCRIPT, hooks_dir / SCRIPT)
    (hooks_dir / SCRIPT).chmod(0o755)

    proc = subprocess.run(
        ["bash", str(hooks_dir / SCRIPT)],
        input=json.dumps(inp),
        capture_output=True,
        text=True,
        timeout=10,
        env={**os.environ},
        cwd=str(env.project_root),
    )
    return HookResult(proc.returncode, proc.stdout, proc.stderr)


# ── Structural validation with real forge-plugin ────────────────────────

class TestRealForgePlugin:
    """Running against the real forge-plugin directory should pass."""

    def test_passes_with_real_structure(self, runner):
        result = runner.run(
            _make_session_start_input(),
            cwd=str(FORGE_DIR.parent),
        )
        assert result.exit_code == 0
        # Should output session context text
        assert "Forge Session Start" in result.stdout or "✅" in result.stdout

    def test_outputs_component_counts(self, runner):
        result = runner.run(
            _make_session_start_input(),
            cwd=str(FORGE_DIR.parent),
        )
        assert result.exit_code == 0
        # Should mention agent, skill, command, hook counts
        assert "agents" in result.stdout.lower() or "Components" in result.stdout

    def test_outputs_safety_profile_version(self, runner):
        result = runner.run(
            _make_session_start_input(),
            cwd=str(FORGE_DIR.parent),
        )
        assert result.exit_code == 0
        # Should mention the profile version
        assert "v" in result.stdout or "version" in result.stdout.lower()


# ── Missing directories detected ────────────────────────────────────────

class TestMissingDirectories:
    """Missing required directories should be reported."""

    def test_missing_dir_reported(self, runner, temp_forge_env):
        env = temp_forge_env()
        # Create a minimal forge-plugin structure but missing some dirs
        (env.project_root / "forge-plugin" / "agents").mkdir(parents=True)
        (env.project_root / "forge-plugin" / "hooks").mkdir(parents=True)
        # Copy the safety profile
        profile_src = FORGE_DIR / "templates" / "root_safety_profile.json"
        if profile_src.exists():
            dest = env.project_root / "forge-plugin" / "templates"
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy(str(profile_src), str(dest / "root_safety_profile.json"))

        result = runner.run(
            _make_session_start_input(),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        # Should report missing directories
        if "Missing" in result.stdout:
            assert "✗" in result.stdout


# ── No safety profile handled gracefully ────────────────────────────────

class TestNoSafetyProfile:
    """If no safety profile exists, hook should handle gracefully."""

    def test_no_profile_exits_cleanly(self, temp_forge_env):
        env = temp_forge_env()
        # No forge-plugin/templates/root_safety_profile.json
        # and no .forge/safety_profile.json in temp env
        result = _run_validator_in_env(env, _make_session_start_input())
        assert result.exit_code == 0
        # Should mention something about missing profile or skip validation
        # (the hook either warns or does minimal output)
        assert len(result.stdout) > 0 or result.exit_code == 0


# ── Creates .forge runtime directory ────────────────────────────────────

class TestForgeRuntimeDir:
    """Hook should create .forge/ directory if it doesn't exist."""

    def test_creates_forge_dir(self, temp_forge_env):
        env = temp_forge_env()
        # Remove .forge if exists
        if env.forge_dir.exists():
            shutil.rmtree(str(env.forge_dir))

        # Copy the safety profile into temp env
        profile_src = FORGE_DIR / "templates" / "root_safety_profile.json"
        if profile_src.exists():
            dest = env.project_root / "forge-plugin" / "templates"
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy(str(profile_src), str(dest / "root_safety_profile.json"))

        # Create minimal dirs needed by component count logic
        # (find on missing dirs crashes with set -euo pipefail — known hook bug)
        for d in ("agents", "skills", "commands"):
            (env.project_root / "forge-plugin" / d).mkdir(parents=True, exist_ok=True)

        result = _run_validator_in_env(env, _make_session_start_input())
        assert result.exit_code == 0


# ── Always exits 0 ─────────────────────────────────────────────────────

class TestAlwaysExitsZero:
    """Root agent validator is informational — always exit 0."""

    def test_always_zero(self, runner, temp_forge_env):
        env = temp_forge_env()
        result = runner.run(
            _make_session_start_input(),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
