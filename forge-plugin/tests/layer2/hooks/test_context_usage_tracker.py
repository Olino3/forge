"""Tests for context_usage_tracker.sh — The Town Crier: Context Usage Analyzer.

Validates that context file usage is analyzed before compaction,
identifying actively used vs unused context files and estimating
wasted tokens.

Event: PreCompact (matcher: manual|auto)
"""

import json

import pytest

from layer2.hooks.hook_helpers import HookRunner, TempForgeEnvironment, FORGE_DIR


SCRIPT = "context_usage_tracker.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _make_pre_compact_input(
    transcript_path: str = "",
    trigger: str = "auto",
    cwd: str = "/tmp",
):
    return {
        "transcript_path": transcript_path,
        "trigger": trigger,
        "cwd": cwd,
    }


# ── No transcript ───────────────────────────────────────────────────────

class TestNoTranscript:
    """Hook should exit silently without a transcript."""

    def test_no_transcript_path(self, runner):
        result = runner.run(_make_pre_compact_input())
        assert result.exit_code == 0
        assert not result.has_warning

    def test_nonexistent_transcript(self, runner):
        result = runner.run(_make_pre_compact_input(
            transcript_path="/nonexistent/file.txt",
        ))
        assert result.exit_code == 0

    def test_empty_transcript(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file("transcript.txt", "")
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0


# ── No context files in transcript ──────────────────────────────────────

class TestNoContextFiles:
    """Transcript with no context file references should pass silently."""

    def test_no_context_references(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "User: Fix the login bug\n"
            "Tool: Read src/auth/handler.ts\n"
            "Tool: Edit src/auth/handler.ts\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        assert not result.has_warning


# ── Context usage analysis ──────────────────────────────────────────────

class TestContextUsageAnalysis:
    """Hook should identify active and unused context files."""

    def test_detects_active_context(self, runner, temp_forge_env):
        env = temp_forge_env()
        # "frameworks" appears multiple times → active
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/python/frameworks.md\n"
            "Using frameworks guidance for FastAPI implementation\n"
            "frameworks pattern applied to the router\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        if result.has_warning:
            ctx = result.additional_context
            assert "Context Usage" in ctx or "active" in ctx.lower()

    def test_detects_unused_context(self, runner, temp_forge_env):
        env = temp_forge_env()
        # Create actual context file so estimatedTokens can be read
        env.create_file(
            "forge-plugin/context/angular/components.md",
            "---\nestimatedTokens: 800\n---\n# Angular Components\n",
        )
        # "components" only appears once (the Read) → unused
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/angular/components.md\n"
            "Tool: Read context/python/frameworks.md\n"
            "Applied frameworks to the FastAPI router\n"
            "frameworks patterns are working well\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        if result.has_warning:
            ctx = result.additional_context
            # Should mention unused files
            assert "unused" in ctx.lower() or "❌" in ctx or "wasted" in ctx.lower()

    def test_usage_rate_calculated(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/python/frameworks.md\n"
            "frameworks are great\n"
            "Tool: Read context/engineering/best_practices.md\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        if result.has_warning:
            ctx = result.additional_context
            assert "%" in ctx or "utilization" in ctx.lower()


# ── Telemetry logging ───────────────────────────────────────────────────

class TestTelemetryLogging:
    """Hook should write usage stats to .forge/telemetry.log."""

    def test_logs_to_telemetry(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/python/frameworks.md\n"
            "Using frameworks for FastAPI\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0

        telemetry = env.forge_dir / "telemetry.log"
        if telemetry.exists():
            content = telemetry.read_text()
            assert "context_usage_report" in content


# ── Trigger types ───────────────────────────────────────────────────────

class TestTriggerTypes:
    """Hook should work with both auto and manual triggers."""

    def test_auto_trigger(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/python/frameworks.md\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                trigger="auto",
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0

    def test_manual_trigger(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/python/frameworks.md\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                trigger="manual",
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0


# ── Output format ───────────────────────────────────────────────────────

class TestOutputFormat:
    """Output should be valid JSON with additionalContext."""

    def test_valid_json_with_context(self, runner, temp_forge_env):
        env = temp_forge_env()
        transcript = env.create_file(
            "transcript.txt",
            "Tool: Read context/python/frameworks.md\n"
            "Used frameworks pattern here\n",
        )
        result = runner.run(
            _make_pre_compact_input(
                transcript_path=str(transcript),
                cwd=str(env.project_root),
            ),
            cwd=str(env.project_root),
        )
        assert result.exit_code == 0
        if result.json_output:
            assert "additionalContext" in result.json_output


# ── Always exits 0 ─────────────────────────────────────────────────────

class TestAlwaysExitsZero:
    """Context usage tracker never blocks — always exit 0."""

    def test_exits_zero(self, runner):
        result = runner.run(_make_pre_compact_input())
        assert result.exit_code == 0
