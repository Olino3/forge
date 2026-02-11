"""Tests for memory_pruning_daemon.sh — The Chronicle: Memory Pruning Daemon.

Validates that the SessionEnd hook prunes oversized memory files,
preserving headers and respecting per-type line limits.

Event: SessionEnd
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from layer2.hooks.hook_helpers import (
    HookResult,
    HookRunner,
    TempForgeEnvironment,
    HOOKS_DIR,
)


SCRIPT = "memory_pruning_daemon.sh"


@pytest.fixture
def runner():
    return HookRunner(SCRIPT)


def _run_pruning_in_env(env: TempForgeEnvironment, inp: dict) -> HookResult:
    """Run the pruning daemon with SCRIPT_DIR inside the temp env.

    The hook derives FORGE_DIR from SCRIPT_DIR (via BASH_SOURCE), so we
    must copy the hook into the temp env so file-path resolution targets
    the temporary directory instead of the real repository.
    """
    hooks_dir = env.project_root / "forge-plugin" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    lib_dir = hooks_dir / "lib"
    lib_dir.mkdir(parents=True, exist_ok=True)

    # Copy hook + shared lib into temp env
    shutil.copy2(HOOKS_DIR / SCRIPT, hooks_dir / SCRIPT)
    (hooks_dir / SCRIPT).chmod(0o755)
    shutil.copy2(HOOKS_DIR / "lib" / "health_buffer.sh", lib_dir / "health_buffer.sh")

    # CLAUDE_PLUGIN_ROOT must be 2 levels deep so ../../.forge → env/.forge
    plugin_root = env.project_root / "_plugin" / "_level2"
    plugin_root.mkdir(parents=True, exist_ok=True)

    proc = subprocess.run(
        ["bash", str(hooks_dir / SCRIPT)],
        input=json.dumps(inp),
        capture_output=True,
        text=True,
        timeout=30,
        env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(plugin_root)},
        cwd=str(env.project_root),
    )
    return HookResult(proc.returncode, proc.stdout, proc.stderr)


def _make_session_end_input(
    transcript_path: str = "",
    session_id: str = "test-session",
    cwd: str = "/tmp",
    reason: str = "user_exit",
):
    return {
        "transcript_path": transcript_path,
        "session_id": session_id,
        "cwd": cwd,
        "reason": reason,
    }


def _make_oversized_file(line_count: int, header_lines: int = 5) -> str:
    """Generate file content with a header and many lines."""
    lines = [f"<!-- Last Updated: 2025-01-01 -->"]
    lines.append("# Test Memory File")
    lines.append("")
    lines.append("## Summary")
    lines.append("Header content that should be preserved.")
    for i in range(line_count - header_lines):
        lines.append(f"Content line {i + 1}: some information here.")
    return "\n".join(lines) + "\n"


# ── Operational files are skipped ───────────────────────────────────────

class TestOperationalFilesSkipped:
    """Operational files should never be pruned."""

    def test_index_not_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_oversized_file(600)
        fp = env.create_file("forge-plugin/memory/index.md", content)
        transcript = env.create_file(
            "transcript.txt",
            f"Read {fp}\nEdit {fp}\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        # index.md should remain untouched
        assert len(fp.read_text().split("\n")) >= 600

    def test_lifecycle_not_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_oversized_file(600)
        fp = env.create_file("forge-plugin/memory/lifecycle.md", content)
        transcript = env.create_file(
            "transcript.txt",
            f"Read {fp}\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        assert len(fp.read_text().split("\n")) >= 600


# ── Pruning to default limit (500 lines) ────────────────────────────────

class TestDefaultPruningLimit:
    """General memory files should be pruned to 500 lines."""

    def test_oversized_general_file_pruned(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_oversized_file(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/findings.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        new_content = fp.read_text()
        line_count = len([l for l in new_content.split("\n") if l.strip() or l == ""])
        # Should be at or below 500 lines (with some tolerance for pruning marker)
        assert line_count <= 510, f"Expected ≤510 lines, got {line_count}"


# ── Pruning to project_overview limit (200 lines) ──────────────────────

class TestProjectOverviewLimit:
    """project_overview files should be pruned to 200 lines."""

    def test_project_overview_pruned_to_200(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_oversized_file(400)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/project_overview.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/projects/test/project_overview.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        new_content = fp.read_text()
        line_count = len(new_content.strip().split("\n"))
        assert line_count <= 210, f"Expected ≤210 lines, got {line_count}"


# ── Pruning to review_history limit (300 lines) ────────────────────────

class TestReviewHistoryLimit:
    """review_history files should be pruned to 300 lines."""

    def test_review_history_pruned_to_300(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_oversized_file(500)
        fp = env.create_file(
            "forge-plugin/memory/projects/test/review_history.md",
            content,
        )
        transcript = env.create_file(
            "transcript.txt",
            "memory/projects/test/review_history.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        new_content = fp.read_text()
        line_count = len(new_content.strip().split("\n"))
        assert line_count <= 310, f"Expected ≤310 lines, got {line_count}"


# ── Header preservation ─────────────────────────────────────────────────

class TestHeaderPreservation:
    """First 5 lines (header) should be preserved after pruning."""

    def test_preserves_first_five_lines(self, temp_forge_env):
        env = temp_forge_env()
        content = _make_oversized_file(700)
        fp = env.create_file(
            "forge-plugin/memory/skills/analyze/proj/findings.md",
            content,
        )
        original_lines = content.split("\n")[:5]
        transcript = env.create_file(
            "transcript.txt",
            "memory/skills/analyze/proj/findings.md\n",
        )
        inp = _make_session_end_input(
            transcript_path=str(transcript),
            cwd=str(env.project_root),
        )
        _run_pruning_in_env(env, inp)
        new_content = fp.read_text()
        new_lines = new_content.split("\n")
        # First 5 lines should match original
        for i, orig_line in enumerate(original_lines):
            # Timestamp may be refreshed, so skip first line comparison
            if i == 0:
                assert "Last Updated" in new_lines[0] or new_lines[0] == orig_line
            else:
                assert new_lines[i] == orig_line, f"Line {i} changed: {new_lines[i]} != {orig_line}"


# ── No transcript path ──────────────────────────────────────────────────

class TestNoTranscript:
    """Hook should handle missing transcript gracefully."""

    def test_no_transcript_path(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_session_end_input(cwd=str(env.project_root))
        result = runner.run(inp, cwd=str(env.project_root))
        assert result.exit_code == 0

    def test_empty_transcript_path(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_session_end_input(
            transcript_path="",
            cwd=str(env.project_root),
        )
        result = runner.run(inp, cwd=str(env.project_root))
        assert result.exit_code == 0

    def test_nonexistent_transcript(self, runner, temp_forge_env):
        env = temp_forge_env()
        inp = _make_session_end_input(
            transcript_path="/nonexistent/transcript.txt",
            cwd=str(env.project_root),
        )
        result = runner.run(inp, cwd=str(env.project_root))
        assert result.exit_code == 0
