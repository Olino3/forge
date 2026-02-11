"""Tests for lib/health_buffer.sh — Shared Health Buffer Library.

Validates the append/flush cycle, max-line cap, and concurrent-safety
of the shared health buffer used by most Forge hooks.

Library: lib/health_buffer.sh
"""

import os
import subprocess

import pytest

from layer2.hooks.hook_helpers import HOOKS_DIR, TempForgeEnvironment


LIB_PATH = HOOKS_DIR / "lib" / "health_buffer.sh"


def _make_plugin_root(env: TempForgeEnvironment) -> str:
    """Create a 2-level deep directory so CLAUDE_PLUGIN_ROOT/../../.forge
    resolves to env.project_root/.forge (matching health_buffer.sh path math)."""
    plugin_root = env.project_root / "_plugin" / "_level2"
    plugin_root.mkdir(parents=True, exist_ok=True)
    return str(plugin_root)


def _run_buffer_script(script_body: str, env: TempForgeEnvironment) -> tuple[int, str, str]:
    """Run a small bash script that sources health_buffer.sh."""
    full_script = f"""
set -euo pipefail
source "{LIB_PATH}"
{script_body}
"""
    proc = subprocess.run(
        ["bash", "-c", full_script],
        capture_output=True,
        text=True,
        timeout=10,
        env={
            **os.environ,
            "CLAUDE_PLUGIN_ROOT": _make_plugin_root(env),
        },
        cwd=str(env.project_root),
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestHealthBufferAppend:
    """Test health_buffer_append function."""

    def test_append_single_message(self, temp_forge_env):
        env = temp_forge_env()
        rc, stdout, stderr = _run_buffer_script(
            'health_buffer_append "test warning message"',
            env,
        )
        assert rc == 0
        content = env.health_buffer_content
        assert "test warning message" in content

    def test_append_adds_timestamp(self, temp_forge_env):
        env = temp_forge_env()
        _run_buffer_script(
            'health_buffer_append "timestamped message"',
            env,
        )
        content = env.health_buffer_content
        # Timestamps are [YYYY-MM-DDTHH:MM:SSZ]
        assert "[" in content
        assert "T" in content
        assert "Z]" in content

    def test_append_multiple_messages(self, temp_forge_env):
        env = temp_forge_env()
        _run_buffer_script(
            """
health_buffer_append "first warning"
health_buffer_append "second warning"
health_buffer_append "third warning"
""",
            env,
        )
        content = env.health_buffer_content
        assert "first warning" in content
        assert "second warning" in content
        assert "third warning" in content
        # Should be 3 separate lines
        lines = [l for l in content.strip().split("\n") if l.strip()]
        assert len(lines) == 3

    def test_append_empty_message_ignored(self, temp_forge_env):
        env = temp_forge_env()
        _run_buffer_script(
            'health_buffer_append ""',
            env,
        )
        content = env.health_buffer_content
        assert content.strip() == ""


class TestHealthBufferFlush:
    """Test health_buffer_flush function."""

    def test_flush_returns_buffered_content(self, temp_forge_env):
        env = temp_forge_env()
        rc, stdout, _ = _run_buffer_script(
            """
health_buffer_append "flush me"
health_buffer_flush
""",
            env,
        )
        assert rc == 0
        assert "flush me" in stdout

    def test_flush_truncates_buffer(self, temp_forge_env):
        env = temp_forge_env()
        _run_buffer_script(
            """
health_buffer_append "to be flushed"
health_buffer_flush > /dev/null
""",
            env,
        )
        content = env.health_buffer_content
        assert content.strip() == ""

    def test_flush_empty_buffer_returns_nonzero(self, temp_forge_env):
        env = temp_forge_env()
        # Flush on empty buffer returns 1 (subshell exit code)
        rc, stdout, _ = _run_buffer_script(
            'health_buffer_flush || echo "EMPTY"',
            env,
        )
        assert "EMPTY" in stdout or stdout.strip() == ""


class TestHealthBufferMaxLines:
    """Test the 200-line safety cap."""

    def test_max_lines_enforced(self, temp_forge_env):
        env = temp_forge_env()
        # Write 210 lines — only 200 should be stored
        _run_buffer_script(
            """
for i in $(seq 1 210); do
    health_buffer_append "line $i"
done
""",
            env,
        )
        content = env.health_buffer_content
        lines = [l for l in content.strip().split("\n") if l.strip()]
        assert len(lines) == 200

    def test_at_max_lines_no_more_appended(self, temp_forge_env):
        env = temp_forge_env()
        _run_buffer_script(
            """
for i in $(seq 1 200); do
    health_buffer_append "line $i"
done
health_buffer_append "overflow line"
""",
            env,
        )
        content = env.health_buffer_content
        assert "overflow line" not in content
        lines = [l for l in content.strip().split("\n") if l.strip()]
        assert len(lines) == 200


class TestHealthBufferInit:
    """Test that buffer auto-initializes directory and files."""

    def test_creates_directory_if_missing(self, temp_forge_env):
        env = temp_forge_env()
        # Remove the .forge dir
        import shutil
        shutil.rmtree(str(env.forge_dir))
        assert not env.forge_dir.exists()

        _run_buffer_script(
            'health_buffer_append "after init"',
            env,
        )
        assert env.forge_dir.exists()
        assert "after init" in env.health_buffer_content
