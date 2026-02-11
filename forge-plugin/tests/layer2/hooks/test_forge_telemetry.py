"""Tests for forge_telemetry.sh — The Town Crier: Session Telemetry Logger.

Validates that session metrics are extracted from transcripts and logged
to .forge/telemetry.log.

Event: Stop (no matcher)
"""

import json

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment


SCRIPT = "forge_telemetry.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_stop_input(
    transcript_path: str = "",
    stop_hook_active: bool = False,
    session_id: str = "session-001",
    cwd: str = "/tmp",
):
    return {
        "transcript_path": transcript_path,
        "stop_hook_active": stop_hook_active,
        "session_id": session_id,
        "cwd": cwd,
    }


# ── Stop hook guard ─────────────────────────────────────────────────────

class TestStopHookGuard:
    """Hook should exit early when stop_hook_active is true."""

    def test_stop_hook_active_exits(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file("transcript.txt", "some content\n")
        inp = _make_stop_input(
            transcript_path=str(transcript),
            stop_hook_active=True,
            cwd=str(env.project_root),
        )
        result = runner.run(inp, cwd=str(env.project_root))
        assert result.exit_code == 0
        # No telemetry should be written
        telemetry = env.forge_dir / "telemetry.log"
        assert not telemetry.exists() or telemetry.read_text().strip() == ""


# ── No transcript ───────────────────────────────────────────────────────

class TestNoTranscript:
    """Hook should exit silently without a transcript."""

    def test_no_transcript_path(self, runner):
        result = runner.run(_make_stop_input())
        assert result.exit_code == 0

    def test_nonexistent_transcript(self, runner):
        result = runner.run(_make_stop_input(
            transcript_path="/nonexistent/file.txt",
        ))
        assert result.exit_code == 0


# ── Telemetry logging ───────────────────────────────────────────────────

class TestTelemetryLogging:
    """Hook should write metrics to .forge/telemetry.log."""

    def test_creates_telemetry_log(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            '"tool_name" "Read"\n'
            '"tool_name" "Write"\n'
            '"tool_name" "Bash"\n',
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        result = runner.run(inp, cwd=str(env.project_root))
        assert result.exit_code == 0

        telemetry = env.forge_dir / "telemetry.log"
        assert telemetry.exists()

    def test_telemetry_contains_timestamp(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            '"tool_name" "Read"\n',
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        runner.run(inp, cwd=str(env.project_root))

        telemetry = env.forge_dir / "telemetry.log"
        content = telemetry.read_text()
        assert "timestamp:" in content

    def test_telemetry_contains_session_id(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            '"tool_name" "Read"\n',
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            session_id="my-test-session",
            cwd=str(env.project_root),
        )
        runner.run(inp, cwd=str(env.project_root))

        telemetry = env.forge_dir / "telemetry.log"
        content = telemetry.read_text()
        assert "my-test-session" in content


# ── Metrics extraction ──────────────────────────────────────────────────

class TestMetricsExtraction:
    """Hook should extract various metrics from transcript."""

    def test_counts_tool_calls(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            '"tool_name" "Read"\n'
            '"tool_name" "Read"\n'
            '"tool_name" "Write"\n'
            '"tool_name" "Bash"\n'
            '"tool_name" "Edit"\n',
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        runner.run(inp, cwd=str(env.project_root))

        telemetry = env.forge_dir / "telemetry.log"
        content = telemetry.read_text()
        assert "tools:" in content
        assert "read:" in content or "Read" in content

    def test_counts_skill_invocations(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Read skills/analyze/SKILL.md\n"
            "Read skills/implement/SKILL.md\n",
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        runner.run(inp, cwd=str(env.project_root))

        telemetry = env.forge_dir / "telemetry.log"
        content = telemetry.read_text()
        assert "skills:" in content

    def test_counts_memory_operations(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Read memory/projects/test/overview.md\n"
            "Write memory/projects/test/overview.md\n"
            "Edit memory/projects/test/overview.md\n",
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        runner.run(inp, cwd=str(env.project_root))

        telemetry = env.forge_dir / "telemetry.log"
        content = telemetry.read_text()
        assert "memory:" in content

    def test_counts_context_loads(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Read context/python/frameworks.md\n"
            "Read context/engineering/best_practices.md\n",
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        runner.run(inp, cwd=str(env.project_root))

        telemetry = env.forge_dir / "telemetry.log"
        content = telemetry.read_text()
        assert "context:" in content

    def test_detects_forge_commands(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "/analyze my-project\n"
            "/implement feature-x\n",
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        runner.run(inp, cwd=str(env.project_root))

        telemetry = env.forge_dir / "telemetry.log"
        content = telemetry.read_text()
        assert "commands:" in content


# ── Health buffer notification ──────────────────────────────────────────

class TestHealthBufferNotification:
    """Hook should append a summary to the health buffer."""

    def test_writes_to_health_buffer(self, runner, temp_forge_env):
        env = temp_forge_env()
        # CLAUDE_PLUGIN_ROOT must be 2 levels deep so ../../.forge → env/.forge
        plugin_root = env.project_root / "_plugin" / "_level2"
        plugin_root.mkdir(parents=True, exist_ok=True)

        transcript = env.create_file(
            "transcript.txt",
            '"tool_name" "Read"\n'
            '"tool_name" "Write"\n',
        )
        inp = _make_stop_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        runner.run(
            inp,
            cwd=str(env.project_root),
            env_overrides={"CLAUDE_PLUGIN_ROOT": str(plugin_root)},
        )

        buffer = env.health_buffer_content
        assert "Telemetry" in buffer or "📊" in buffer or "telemetry" in buffer.lower()


# ── Always exits 0 ─────────────────────────────────────────────────────

class TestAlwaysExitsZero:
    """Telemetry logger is purely observational — always exit 0."""

    def test_exits_zero(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file("transcript.txt", "content\n")
        result = runner.run(
            _make_stop_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
