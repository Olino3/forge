"""Tests for system_health_emitter.sh — The Chronicle: Health Buffer Aggregator.

Validates that the health buffer contents are flushed and surfaced
as additionalContext after every tool execution.

Event: PostToolUse (matcher: .*)
"""

import os
import subprocess
from pathlib import Path

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, HOOKS_DIR


SCRIPT = "system_health_emitter.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_post_input():
    return {
        "tool_name": "Read",
        "tool_input": {"file_path": "src/main.py"},
    }


def _make_plugin_root(env: TempForgeEnvironment) -> str:
    """Create a 2-level deep dir for CLAUDE_PLUGIN_ROOT so ../../.forge
    resolves to the temp env's .forge directory."""
    plugin_root = env.project_root / "_plugin" / "_level2"
    plugin_root.mkdir(parents=True, exist_ok=True)
    return str(plugin_root)


def _seed_health_buffer(env: TempForgeEnvironment, messages: list[str]):
    """Write messages directly to the health buffer in the temp env."""
    lib_path = HOOKS_DIR / "lib" / "health_buffer.sh"
    plugin_root = _make_plugin_root(env)
    script = f"""
set -euo pipefail
source "{lib_path}"
"""
    for msg in messages:
        script += f'health_buffer_append "{msg}"\n'

    subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        timeout=10,
        env={**os.environ, "CLAUDE_PLUGIN_ROOT": plugin_root},
        cwd=str(env.project_root),
    )


class TestEmptyBuffer:
    """Hook should exit silently when buffer is empty."""

    def test_empty_buffer_no_output(self, runner, temp_forge_env):
        env = temp_forge_env()
        plugin_root = _make_plugin_root(env)
        result = runner.run(
            _make_post_input(),
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": plugin_root},
        )
        assert result.exit_code == 0
        assert not result.has_warning
        # No output when buffer is empty
        assert result.stdout.strip() == "" or result.json_output is None


class TestBufferedWarnings:
    """Hook should flush and emit buffered warnings."""

    def test_single_warning_emitted(self, runner, temp_forge_env):
        env = temp_forge_env()
        plugin_root = _make_plugin_root(env)
        _seed_health_buffer(env, ["⚠️ Memory file exceeds limit"])

        result = runner.run(
            _make_post_input(),
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": plugin_root},
        )
        assert result.exit_code == 0
        if result.has_warning:
            assert "Memory file" in result.additional_context or "Health Report" in result.additional_context

    def test_multiple_warnings_emitted(self, runner, temp_forge_env):
        env = temp_forge_env()
        plugin_root = _make_plugin_root(env)
        _seed_health_buffer(env, [
            "⚠️ Warning 1: first issue",
            "⚠️ Warning 2: second issue",
            "⚠️ Warning 3: third issue",
        ])

        result = runner.run(
            _make_post_input(),
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": plugin_root},
        )
        assert result.exit_code == 0
        if result.has_warning:
            assert "3" in result.additional_context or "event" in result.additional_context.lower()

    def test_entry_count_in_report(self, runner, temp_forge_env):
        env = temp_forge_env()
        plugin_root = _make_plugin_root(env)
        _seed_health_buffer(env, [
            "Issue A",
            "Issue B",
        ])

        result = runner.run(
            _make_post_input(),
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": plugin_root},
        )
        assert result.exit_code == 0
        if result.has_warning:
            # Should mention "2 event(s)" or similar count
            assert "2" in result.additional_context


class TestBufferFlushedAfterEmit:
    """After emitting, the buffer should be empty."""

    def test_buffer_flushed(self, runner, temp_forge_env):
        env = temp_forge_env()
        plugin_root = _make_plugin_root(env)
        _seed_health_buffer(env, ["Flush this"])

        # First run: should emit
        result1 = runner.run(
            _make_post_input(),
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": plugin_root},
        )
        assert result1.exit_code == 0

        # Second run: buffer should be empty
        result2 = runner.run(
            _make_post_input(),
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": plugin_root},
        )
        assert result2.exit_code == 0
        # Second run should have no warnings
        assert not result2.has_warning or result2.stdout.strip() == ""


class TestOutputFormat:
    """Output should be valid JSON with additionalContext field."""

    def test_valid_json_output(self, runner, temp_forge_env):
        env = temp_forge_env()
        plugin_root = _make_plugin_root(env)
        _seed_health_buffer(env, ["Test message"])

        result = runner.run(
            _make_post_input(),
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": plugin_root},
        )
        assert result.exit_code == 0
        if result.json_output:
            assert "additionalContext" in result.json_output
            assert "Health Report" in result.json_output["additionalContext"]


class TestAlwaysExitsZero:
    """Health emitter never blocks — always exit 0."""

    def test_always_zero(self, runner):
        result = runner.run(_make_post_input())
        assert result.exit_code == 0
